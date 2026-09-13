"""Offline guard checks. No credentials, files, network, or generation calls."""
import io
import json
import unittest
import wave
from unittest import mock

import restore


def wav_bytes(rate=48000, channels=1, width=2, count=2000):
    stream = io.BytesIO()
    with wave.open(stream, "wb") as audio:
        audio.setframerate(rate)
        audio.setnchannels(channels)
        audio.setsampwidth(width)
        audio.writeframes(b"\0" * count * channels * width)
    return stream.getvalue()


def picture():
    return {"sha256": "a" * 64, "frame_count": 24, "duration_seconds": 1,
            "width": 720, "height": 1280, "frame_rate": "24/1", "audio_stream_count": 0}


def qa_record():
    return {"video": {"sha256": "a" * 64}, "matched_probe": {"streams": [
        {"codec_type": "video", "width": 720, "height": 1280, "r_frame_rate": "24/1",
         "duration": "1.000000", "nb_read_frames": "24"}], "format": {"duration": "1.000000"}}}


class GuardTests(unittest.TestCase):
    def test_api_host_is_checked_before_credentials(self):
        with mock.patch.object(restore, "credential") as secret:
            for url in ["http://queue.fal.run/x", "https://queue.fal.run.evil.test/x",
                        "https://evil.test/x", "https://queue.fal.run:444/x",
                        "https://user@queue.fal.run/x"]:
                with self.subTest(url=url), self.assertRaises(ValueError):
                    restore.api(url, {"video_url": "x"})
            secret.assert_not_called()

    def test_redirects_are_denied(self):
        self.assertIsNone(restore.NoRedirect().redirect_request(None, None, 302, None, None, "https://evil.test"))

    def test_wav_actual_format_count_and_truncation(self):
        good = wav_bytes()
        self.assertEqual(restore.wav_info(good, 2000)["sample_count"], 2000)
        for bad in [wav_bytes(rate=44100), wav_bytes(channels=2), wav_bytes(width=1),
                    wav_bytes(count=1999), good[:-20]]:
            with self.subTest(length=len(bad)), self.assertRaises((ValueError, wave.Error, EOFError)):
                restore.wav_info(bad, 2000)

    def test_pinned_root_probe_is_required_to_match_actual_fields(self):
        self.assertEqual(restore.video_from_qa(qa_record(), picture())["frame_count"], 24)
        mutations = [lambda d: d["video"].update(sha256="b" * 64),
                     lambda d: d["matched_probe"]["streams"][0].update(nb_read_frames="23"),
                     lambda d: d["matched_probe"]["streams"][0].update(r_frame_rate="30/1"),
                     lambda d: d["matched_probe"]["streams"].append({"codec_type": "audio"}),
                     lambda d: d["matched_probe"]["streams"][0].update(duration="1.2")]
        for change in mutations:
            record = qa_record()
            change(record)
            with self.assertRaises(ValueError):
                restore.video_from_qa(record, picture())

    def test_media_cannot_escape_revision07(self):
        with self.assertRaises(ValueError):
            restore.pinned_bytes({"local_path": "../outside.wav", "sha256": "a" * 64}, media=True)

    def test_local_and_hosted_hash_mismatches_stop_validation(self):
        video = dict(picture(), local_path="video", url="https://example.test/video")
        audio_data = wav_bytes(count=48000)
        audio = {"local_path": "audio", "url": "https://example.test/audio", "sha256": restore.digest(audio_data),
                 "sample_count": 48000, "sample_rate_hz": 48000, "channels": 1, "sample_width_bytes": 2}
        video["sha256"] = restore.digest(b"video-bytes")
        qa = qa_record()
        qa["video"]["sha256"] = video["sha256"]
        incoming = {"section_index": 1, "video": video, "audio": audio,
                    "video_qa": {"local_path": "qa"}, "source_audio": {"local_path": "source"},
                    "script": {"local_path": "script"}, "voice_proof": {"local_path": "proof"}}
        values = {"video": b"video-bytes", "audio": audio_data, "qa": json.dumps(qa).encode(),
                  "source": b"source", "script": b"script", "proof": b"{}"}
        def local(item, media=False):
            return values[item["local_path"]]
        with mock.patch.object(restore, "pinned_bytes", side_effect=local), mock.patch.object(restore, "fetch") as get:
            get.side_effect = [b"video-bytes", audio_data]
            self.assertTrue(restore.validate(incoming, hosted=True)["hosted_bytes_checked"])
            get.side_effect = [b"wrong-video"]
            with self.assertRaisesRegex(ValueError, "Hosted video"):
                restore.validate(incoming, hosted=True)
            get.side_effect = [b"video-bytes", b"wrong-audio"]
            with self.assertRaisesRegex(ValueError, "Hosted audio"):
                restore.validate(incoming, hosted=True)
            incoming["audio"]["sample_count"] -= 1
            with self.assertRaisesRegex(ValueError, "times 2000"):
                restore.validate(incoming, hosted=False)

    def test_one_post_and_uncertain_post_both_consume_the_intent(self):
        for fail in (False, True):
            saved = {}
            class MemoryPath:
                def __init__(self, name=""):
                    self.name = name
                def __truediv__(self, name):
                    return MemoryPath(name)
                def exists(self):
                    return self.name in saved
                def read_bytes(self):
                    return b"bound request bytes"
            def persist(name, value, exclusive=False):
                if exclusive and name in saved:
                    raise FileExistsError(name)
                saved[name] = value
            request = {"input": {"video_url": "https://example.test/v", "audio_url": "https://example.test/a",
                                 "sync_mode": "cut_off"}}
            incoming = {"video": {"sha256": "a" * 64}, "audio": {"sha256": "b" * 64}}
            with mock.patch.object(restore, "BASE", MemoryPath()), \
                 mock.patch.object(restore, "save", side_effect=persist), \
                 mock.patch.object(restore, "bound", return_value=(incoming, request)), \
                 mock.patch.object(restore, "validate", return_value={}), \
                 mock.patch.object(restore, "credential", return_value="never-used-secret"), \
                 mock.patch.object(restore, "api") as post:
                post.side_effect = RuntimeError("uncertain") if fail else None
                post.return_value = {"request_id": "offline-only"}
                if fail:
                    with self.assertRaises(RuntimeError):
                        restore.submit()
                else:
                    restore.submit()
                with self.assertRaisesRegex(ValueError, "second POST"):
                    restore.submit()
                post.assert_called_once_with("https://queue.fal.run/fal-ai/sync-lipsync/v2/pro", request["input"])
                self.assertEqual(saved["SUBMISSION-INTENT.json"]["max_submission_calls"], 1)


if __name__ == "__main__":
    unittest.main()
