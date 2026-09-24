#!/usr/bin/env python3
"""Read-only native provider QA. Writes diagnostics only under this script's directory."""
from pathlib import Path
import argparse, hashlib, json, math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path("/Users/brownmanbrain/GitHub/operator-economy")
BASE = ROOT / "blueprint-cinema/experiments/EP007-PRESENTER-001"
OWNED = Path(__file__).resolve().parent
SOURCE = BASE / "media/repair-r2/scope-two-sentences.wav"
SOURCE_HASH = "c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566"
LABELS = ["omnihuman-01", "omnihuman-02", "infinitalk-01", "infinitalk-02"]
RATE = 48000

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(args, binary=False):
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="replace")[-4000:])
    return p.stdout if binary else p.stdout.decode()

def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]))

def pcm(path):
    raw = run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0",
               "-ac", "1", "-ar", str(RATE), "-c:a", "pcm_f32le", "-f", "f32le", "-"], True)
    return np.frombuffer(raw, dtype="<f4").astype(np.float64)

def align(source, target, begin, end, search_seconds=1.0):
    start, stop = round(begin * RATE), round(end * RATE)
    x = source[start:stop]
    low = max(-round(search_seconds * RATE), -start)
    high = min(round(search_seconds * RATE), len(target) - stop)
    if len(x) < 100 or high < low:
        return {"status": "insufficient_overlap", "source_window_seconds": [begin, end]}
    y = target[start + low:stop + high]
    xc = x - np.mean(x)
    norm_x = np.sum(xc * xc)
    if norm_x < 1e-10:
        return {"status": "source_window_too_quiet", "source_window_seconds": [begin, end]}
    fft_n = 1 << (len(x) + len(y) - 2).bit_length()
    conv = np.fft.irfft(np.fft.rfft(y, fft_n) * np.fft.rfft(xc[::-1], fft_n), fft_n)
    dots = conv[len(x)-1:len(y)]
    sums = np.concatenate(([0.0], np.cumsum(y)))
    sums2 = np.concatenate(([0.0], np.cumsum(y * y)))
    count = len(y) - len(x) + 1
    ys = sums[len(x):] - sums[:count]
    ys2 = sums2[len(x):] - sums2[:count]
    denom = np.sqrt(norm_x * np.maximum(ys2 - ys * ys / len(x), 1e-30))
    correlations = np.clip(dots / denom, -1, 1)
    k = int(np.argmax(correlations))
    lag = low + k
    return {
        "status": "measured", "source_window_seconds": [begin, end],
        "lag_samples": lag, "lag_ms": lag * 1000 / RATE,
        "aligned_pearson": float(correlations[k]),
        "search_lag_samples": [low, high],
        "best_lag_at_search_boundary": k in (0, len(correlations)-1),
        "interpretation": "Positive lag means source event appears later in decoded output audio; not a visual lip-sync measurement."
    }

def rate_number(text):
    try:
        a,b = text.split("/")
        return float(a) / float(b)
    except Exception:
        return None

def frames_info(path):
    d = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames",
       "-show_entries", "frame=best_effort_timestamp_time,pts_time,duration_time,pkt_duration_time",
       "-of", "json", str(path)]))
    rows = []
    for i,f in enumerate(d.get("frames", [])):
        t = f.get("best_effort_timestamp_time", f.get("pts_time"))
        dur = f.get("duration_time", f.get("pkt_duration_time"))
        rows.append({"index": i, "pts_seconds": float(t) if t is not None else None,
                     "duration_seconds": float(dur) if dur is not None else None})
    return rows

def diagnostic_frames(path, rows, width, height, offset, out):
    requested = [0.0,0.76,0.92,1.04,1.20,2.80,3.20,3.60,4.16,4.32,4.44,4.64,5.20]
    usable = [r for r in rows if r["pts_seconds"] is not None]
    if not usable:
        return {"status": "no_usable_pts"}
    matches = []
    for t in requested:
        f = min(usable, key=lambda r: abs(r["pts_seconds"]-(t+offset)))
        matches.append({"source_diagnostic_time": t, "target_media_time": t+offset, **f})
    matches.append({"source_diagnostic_time": None, "target_media_time": usable[-1]["pts_seconds"], **usable[-1]})
    indices = sorted({m["index"] for m in matches})
    filt = "select='" + "+".join("eq(n,%d)" % n for n in indices) + "'"
    raw = run(["ffmpeg", "-v", "error", "-noautorotate", "-i", str(path), "-map", "0:v:0",
               "-vf", filt, "-fps_mode", "passthrough", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], True)
    frame_size = width * height * 3
    assert len(raw) == frame_size * len(indices), "Unexpected decoded sample dimensions/count"
    arrays = np.frombuffer(raw, dtype=np.uint8).reshape(len(indices), height, width, 3)
    thumbs = []
    for i,n in enumerate(indices):
        im = Image.fromarray(arrays[i])
        p = out / ("frame-%04d.png" % n)
        im.save(p)
        tw = 480
        th = round(height * tw / width)
        cell = Image.new("RGB", (tw, th+30), "#eee9df")
        cell.paste(im.resize((tw,th), Image.Resampling.LANCZOS), (0,30))
        t = rows[n]["pts_seconds"]
        ImageDraw.Draw(cell).text((8,8), "%s f%d %.3fs" % (path.stem,n,t), fill="#202020")
        thumbs.append(cell)
    columns = 4
    cell_h = thumbs[0].height
    sheet = Image.new("RGB", (480*columns, math.ceil(len(thumbs)/columns)*cell_h), "#eee9df")
    for i,im in enumerate(thumbs):
        sheet.paste(im, ((i%columns)*480, (i//columns)*cell_h))
    sheet_path = out / "contact-sheet.jpg"
    sheet.save(sheet_path, quality=93)
    return {"status":"extracted_not_yet_visually_reviewed", "requested_source_times_are_diagnostic_not_phoneme_labels":True,
            "source_to_media_offset_seconds_used":offset, "matches":matches,
            "native_frame_paths":[str(out / ("frame-%04d.png" % n)) for n in indices],
            "contact_sheet":str(sheet_path)}

def review(label, expected, source, extract=True):
    path = BASE / "media/repair-r23" / (label+".mp4")
    if not path.is_file():
        return {"label":label,"status":"awaiting_file","native_path":str(path)}
    digest = sha(path)
    if expected and digest != expected:
        raise RuntimeError("Native hash mismatch for "+label)
    out = OWNED / label
    out.mkdir(parents=True, exist_ok=True)
    p = probe(path)
    (out / "ffprobe.json").write_text(json.dumps(p,indent=2)+"\n")
    videos = [s for s in p["streams"] if s["codec_type"]=="video"]
    audios = [s for s in p["streams"] if s["codec_type"]=="audio"]
    assert videos, "No video stream"
    video = videos[0]
    command = ["ffmpeg","-v","error","-xerror","-i",str(path),"-map","0:v:0","-map","0:a?","-f","null","-"]
    dec = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out/"full-decode.log").write_text(dec.stderr.decode(errors="replace"))
    rows = frames_info(path)
    (out/"frame-timestamps.json").write_text(json.dumps(rows,indent=2)+"\n")
    times = [r["pts_seconds"] for r in rows if r["pts_seconds"] is not None]
    deltas = np.diff(times)
    fps = rate_number(video.get("avg_frame_rate",""))
    fallback_duration = float(np.median(deltas)) if len(deltas) else (1/fps if fps else None)
    last_dur = rows[-1]["duration_seconds"] or fallback_duration if rows else None
    picture_end = times[-1]+last_dur if times and last_dur is not None else None
    report = {
        "label":label,"status":"technical_qa_complete" if dec.returncode==0 else "decode_failed",
        "native_path":str(path),"native_sha256":digest,"expected_hash_verified":bool(expected),
        "native_bytes":path.stat().st_size,"source_audio_sha256":SOURCE_HASH,
        "native_video":{k:video.get(k) for k in ["codec_name","width","height","pix_fmt","r_frame_rate","avg_frame_rate","time_base","start_time","duration","nb_frames"]},
        "actual_frame_count":len(rows),"first_frame_pts_seconds":times[0] if times else None,
        "picture_end_seconds":picture_end,
        "frame_pts_strictly_increasing":bool(len(times)==len(rows) and (len(deltas)==0 or np.all(deltas>0))),
        "frame_interval_min_max_seconds":[float(np.min(deltas)),float(np.max(deltas))] if len(deltas) else None,
        "full_decode":{"pass":dec.returncode==0,"exit_code":dec.returncode,"stderr":dec.stderr.decode(errors="replace")},
        "audio":{"status":"missing" if not audios else "pending"},
        "full_speed_playback_performed":False,
        "visual_lip_sync":"unverified","naturalness":"unverified","owner_accepted":False,
        "geometry_or_timing_correction":False
    }
    media_offset = 0.0
    if audios:
        target = pcm(path)
        comparisons = {name:align(source,target,a,b) for name,a,b in [
            ("overall",0.25,5.35),("early_sentence",0.25,2.85),("late_sentence",3.87,5.35),("final_word",4.95,5.35)]}
        early,late = comparisons["early_sentence"],comparisons["late_sentence"]
        overall = comparisons["overall"]
        astart = float(audios[0].get("start_time",0) or 0)
        lag = overall.get("lag_samples")
        strong = overall.get("aligned_pearson",0)>=0.98 and not overall.get("best_lag_at_search_boundary",True)
        media_offset = astart + lag/RATE if lag is not None and strong else 0.0
        final = comparisons["final_word"]
        final_lag = final.get("lag_samples")
        final_source_end = 5.35
        mapped_final_end = astart + final_source_end + final_lag/RATE if final_lag is not None else None
        report["audio"] = {
            "status":"measured","native_stream":{k:audios[0].get(k) for k in ["codec_name","sample_rate","channels","channel_layout","start_time","duration"]},
            "analysis_rate_hz":RATE,"decoded_samples":len(target),"decoded_seconds":len(target)/RATE,
            "comparison":comparisons,
            "late_minus_early_lag_ms":late["lag_ms"]-early["lag_ms"] if "lag_ms" in early and "lag_ms" in late else None,
            "sampled_peaks_or_drift_do_not_establish_visual_sync":True,
            "strong_audio_match_for_diagnostic_alignment":strong,
            "source_to_media_offset_seconds":media_offset if strong else None,
            "timeline_anchor_assumption":"Decoded first output sample is placed at audio stream start_time; nonzero start times need independent review.",
            "final_word_source_window_seconds":[4.95,5.35],
            "final_word_source_end_is_prior_window_not_exact_phoneme_end":True,
            "mapped_final_word_window_end_seconds":mapped_final_end,
            "picture_margin_after_final_word_window_seconds":picture_end-mapped_final_end if picture_end is not None and mapped_final_end is not None else None,
            "full_original_audio_extent_mapped_end_seconds":astart+len(source)/RATE+lag/RATE if lag is not None else None,
            "wording_prosody_and_visual_lip_sync":"Not certified by waveform comparison; require actual listening and moving visual review."
        }
    if extract and dec.returncode==0:
        report["sampled_images"] = diagnostic_frames(path,rows,int(video["width"]),int(video["height"]),media_offset,out)
    assert sha(path)==digest,"Source file changed during review"
    report["native_file_hash_unchanged_after_qa"] = True
    (out/"technical-review.json").write_text(json.dumps(report,indent=2)+"\n")
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips",nargs="+",choices=LABELS,default=LABELS)
    parser.add_argument("--expect",action="append",default=[],help="label=sha256")
    parser.add_argument("--no-images",action="store_true")
    parser.add_argument("--self-check",action="store_true")
    args = parser.parse_args()
    assert sha(SOURCE)==SOURCE_HASH,"Original audio hash mismatch"
    source = pcm(SOURCE)
    assert len(source)==268800,"Source duration mismatch"
    if args.self_check:
        delayed = np.concatenate((np.zeros(960),source,np.zeros(320)))
        for a,b in [(0.25,2.85),(3.87,5.35)]:
            r = align(source,delayed,a,b)
            assert r["lag_samples"]==960 and r["aligned_pearson"]>0.99999,r
        print("PASS: original audio hash/sample count; known +20ms delay recovered independently in early and late source windows.")
        return
    expected = dict(s.split("=",1) for s in args.expect)
    results = []
    for label in args.clips:
        try:
            result = review(label,expected.get(label),source,not args.no_images)
        except Exception as e:
            result = {"label":label,"status":"qa_error","error":str(e),"visual_lip_sync":"unverified","owner_accepted":False}
        results.append(result)
        print(json.dumps({k:result.get(k) for k in ["label","status","native_sha256","audio","sampled_images"]}),flush=True)
    (OWNED/"latest-batch-summary.json").write_text(json.dumps(results,indent=2)+"\n")
    if any(r["status"] in ("qa_error","decode_failed") for r in results):
        sys.exit(1)

if __name__=="__main__":
    main()

