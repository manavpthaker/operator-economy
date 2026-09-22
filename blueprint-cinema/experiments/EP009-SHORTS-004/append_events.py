#!/usr/bin/env python3
"""Append the SHORTS-004 decision and per-Short verification events.

One decision event for the revision, citing the owner ruling, then one
verification event per Short. Evidence digests are computed at append time so
`decision_log.py validate --evidence` can be run straight afterwards.
Nothing here is owner acceptance.
"""
from pathlib import Path
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oe_shorts_r4 as L  # noqa: E402

EPISODE = "EP009-direct-booking-recovery"
DECISION_ID = "ep009-shorts-standalone-recut"
DECISION_EVENT = "ep009-shorts-r4-standalone-recut"
LOG = L.REPO / ".agents/skills/oe-video-direction/scripts/decision_log.py"
REV = "blueprint-cinema/experiments/EP009-SHORTS-004"
SHORTS = [
    ("01", "01-second-commission", "When the guest returns, the commission does too"),
    ("02", "02-cheap-tools", "Cheap parts, and a job still left to sell"),
    ("03", "03-guest-relationship", "The booking site keeps the guest's email"),
    ("04", "04-wrong-number", "The commission total is the wrong number"),
]


def ev(path: str, locator: str) -> dict:
    return {"path": path, "sha256": L.sha(L.REPO / path), "locator": locator}


def art(path: str) -> dict:
    return {"path": path, "sha256": L.sha(L.REPO / path)}


SCRATCH = Path("/private/tmp/claude-501/-Users-brownmanbrain-GitHub-operator-economy/"
               "82de42ec-ae77-42eb-8a88-f56e54114dda/scratchpad")


def append(event: dict) -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    handoff = SCRATCH / f"event-{event['event_id']}.json"
    handoff.write_text(json.dumps(event, indent=2))
    res = subprocess.run(
        ["python3", str(LOG), "append", "--episode", EPISODE,
         "--root", str(L.REPO), "--event", str(handoff)],
        capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(f"append failed for {event['event_id']}:\n{res.stdout}{res.stderr}")
    print("appended", event["event_id"], res.stdout.strip())


DECISION = {
    "event_id": DECISION_EVENT,
    "decision_id": DECISION_ID,
    "event_type": "decision",
    "tags": ["shorts", "recut", "r4", "standalone-payoff", "captions", "end-cards"],
    "data": {
        "choice":
            "Bring all four EP009 Shorts onto the committed standalone-payoff standard from "
            "locked material only. Short 03 is extended one beat to master f4890 so W000584 to "
            "W000588, 'Nobody at the inn is.', is spoken inside it, and its interrogative end "
            "card is replaced by a card that states that answer. Short 01's proof beat is "
            "extended one sentence to master f948 so the payoff finishes out loud on "
            "W000102 to W000109. Short 02 gains a presenter orientation beat in front, master "
            "f1687 to f1842, because its r3 opening named no hotel, no booking site and no "
            "commission. Short 04 is not re-cut; its r3 cut already resolves its own payoff. "
            "All four interrogative end cards become declarative cards that state what the "
            "Short resolved and route only to what the episode adds. The approved copy package "
            "is applied, cliffhanger blocks dropped, every episode reference left as the "
            "literal [EPISODE_URL] placeholder under the slug direct-booking-practice.",
        "reason":
            "The owner ruled on 2026-09-21 that the standalone-payoff standard governs, that "
            "cliffhanger_line is retired, and that the pinned comment and Related Video may "
            "only add distinct depth. Judged against that standard rather than against their "
            "briefs, all four r3 cuts shared one failure: the last thing on screen was a "
            "question the Short did not answer, with the conclusion routed to an episode that "
            "has no URL. Short 03 additionally resolved nothing at all and its answer sat one "
            "word past the out point, which the r3 contract had recorded as next_word_excluded. "
            "Short 02 additionally failed the kill-list item 'no cold-viewer context'. Short 01 "
            "resolved a bounded fact but stopped mid-thought. Short 04 needed no cut change, so "
            "it got none: re-cutting a compliant beat to look busy would have spent the accepted "
            "performance for nothing.",
        "context": {
            "narrative_job":
                "Make each Short a complete unit for a viewer who will never open the episode, "
                "without generating a frame of new performance or a second of new speech.",
            "viewer_before":
                "Scrolling. Does not know that a small hotel pays a booking-site commission "
                "again when the same guest books again, and under the r3 cuts would leave each "
                "Short holding a question instead of a fact.",
            "viewer_after":
                "Holds one bounded mechanic from the Short itself: the commission recurs on a "
                "guest the inn already had; the drafting is cheap and the price is capped by "
                "what the practice recovers; nobody at the inn is paid to bring the second "
                "booking back; the commission total is not the addressable amount.",
        },
        "alternatives": [
            {
                "choice": "Leave the cuts alone and fix compliance in copy and end cards only.",
                "reason_not_selected":
                    "It cannot work for Short 03, whose sixteen seconds are three stacked "
                    "questions with no resolved beat; the owner ruled specifically for the "
                    "one-beat re-cut. It also leaves Short 02 with no spoken cold-viewer "
                    "context, which is a kill-list item that copy cannot repair, and leaves "
                    "Short 01's payoff stopping mid-thought.",
            },
            {
                "choice": "Re-cut Short 01 into a graphic-led piece so the mechanic is stated "
                          "before any question is asked.",
                "reason_not_selected":
                    "The only on-topic presenter coverage for Short 01 is seg009, which carries "
                    "a question pair and an absence. Leading with the mechanic means leading "
                    "with a card, which would drop the presenter share of speech to roughly a "
                    "quarter and change the accepted avatar-forward direction. That is an owner "
                    "decision, not a compliance fix. The one-sentence extension was taken "
                    "instead, and its smaller cost to the presenter share is recorded.",
            },
            {
                "choice": "Carry Short 03's answer beat on the presenter rather than a card.",
                "reason_not_selected":
                    "No lip-synced picture exists. seg019's look-transfer coverage ends at "
                    "output frame 4844 and seg019b's native runs out at global 4851, so master "
                    "4851 to 4890 has no frames. Generating performance was out of scope and "
                    "would not be locked material. The card carries the spoken answer in the "
                    "silent_graphic picture/audio mode already accepted in this revision's "
                    "Short 01 proof insert, and the gap is recorded as a deferred item for the "
                    "next presenter recording.",
            },
            {
                "choice": "Re-cut Short 04 as well, for consistency with the other three.",
                "reason_not_selected":
                    "Its r3 cut already orients on the on-screen wrong number in frame one and "
                    "resolves the cap out loud, with 0.982 of its speech on the presenter. "
                    "Nothing in the locked material improves it. Only its end card and one "
                    "missing overlay were wrong.",
            },
            {
                "choice": "Rail Short 03's final line as a burned-in caption like every other line.",
                "reason_not_selected":
                    "The answer card carries those exact words on screen at that moment, and "
                    "the docs/content-rubric.md edit kill list bans caption text duplicating a "
                    "card verbatim while the card is up. The line is carried in captions.srt "
                    "and captions.vtt instead, so no subtitle surface loses it.",
            },
            {
                "choice": "Resolve [EPISODE_URL] so the pinned comments are publishable.",
                "reason_not_selected":
                    "EP009 has no launch record. Only studio/originate/<slug>/launch/links.json "
                    "may state an episode URL, and the slug direct-booking-recovery belongs to "
                    "the live August EP006 episode, so inheriting that URL would point four "
                    "Shorts at the wrong video. The placeholder is left literal.",
            },
        ],
        "reuse": {
            "kind": "conditional_precedent",
            "applies_when":
                "Bringing already-cut OE Shorts onto the standalone-payoff standard from locked "
                "narration and accepted presenter coverage, where the answer is inside the "
                "master but outside the out point, or where the opening names nothing.",
            "avoid_when":
                "The narration has no sentence that resolves the Short's own promise; the "
                "required extension has no measured silence to cut into; the answer beat has no "
                "presenter coverage and the direction will not accept a card; or the owner has "
                "reopened the cliffhanger standard.",
        },
        "nuance": {
            "cut_cues": [
                {"cue_id": "s01-payoff-extension", "phrase": "For a guest she already knows by name.",
                 "relation": "Proof beat out point moves from master f870 to f948, taking "
                             "W000102 to W000109. The out point measures -76.1 dBFS; the word "
                             "ends at f940.1 and W000110 begins at f973.4."},
                {"cue_id": "s02-orientation", "phrase": "It helps a small hotel get its returning guests to book direct, instead of paying a booking site to meet them again.",
                 "relation": "New first beat, master f1687 to f1842, seg012 native 0 to 155, "
                             "W000195 to W000216. The out point measures -41.9 dBFS in a "
                             "three-frame gap before 'By' at f1843.9. Tightest join in the package."},
                {"cue_id": "s03-answer", "phrase": "Nobody at the inn is.",
                 "relation": "Cut extended from master f4844 to f4890, taking W000584 to W000588, "
                             "the word the r3 contract recorded as next_word_excluded. The out "
                             "point measures -65.8 dBFS; the sentence ends at f4880.4 and "
                             "W000589 begins at f4895.8."},
                {"cue_id": "s04-boundary", "phrase": "Capped by what it recovers",
                 "relation": "Overlay added at 9.540 to 10.690 s on the spoken 'what the job "
                             "recovers'. No cut change; the r3 constraint beat carried no "
                             "overlay for 5.7 s."},
            ],
            "end_cards_replaced": {
                "01": "What could the inn actually pay? -> The inn pays the commission again.",
                "02": "What work would an inn pay for? -> I think it can be sold from outside.",
                "03": "Who owns the second booking? -> Nobody at the inn is.",
                "04": "What can this inn actually afford? -> The inn can only pay what the job recovers.",
            },
            "durations": {"01": 16.708333, "02": 24.25, "03": 17.166667, "04": 16.541667},
            "frame_counts": {"01": 401, "02": 582, "03": 412, "04": 397},
            "presenter_spoken_fraction": {
                "01": "0.665 -> 0.516, a direction trade flagged for the owner",
                "02": "0.668 -> 0.765",
                "03": "presenter picture ends 1.9 s before the speech does; the answer beat is a card",
                "04": "0.982, unchanged",
            },
            "copy_changes_forced_by_the_recut": [
                "Short 02's hook line moves from 0.000 s to 6.458 s, onto the question beat it describes.",
                "Short 02 gains 'A direct-booking practice' (25 chars) to supply the referent for the spoken 'It'.",
                "Short 02's description line 1 leads with the small hotel rather than the cheap parts.",
                "Short 01's description line 2 gains 'on a guest it already had.'",
                "Short 03's conditional end card 'Nobody is, yet.' is unused; the spoken answer is on the card instead.",
                "Short 01's pinned comment opens 'Full episode: [EPISODE_URL]' so PIN_ROUTE_RE matches; "
                "the URL still leads the comment, per the EP002 lesson in content-os/facts.md.",
                "cliffhanger blocks dropped from every manifest; cliffhanger_line is retired.",
            ],
            "checks_not_completed": [
                "Perceptual lip sync on any presenter beat. Argued from provenance, not measured.",
                "Human cold-viewer isolation review, which shorts_contract.py's own docstring "
                "names as the thing the validator cannot do.",
                "Physical-phone playback. Verified at 390x844 in a browser only.",
                "Family O oe_video pass: requires commit-bound external review evidence that does not exist.",
                "Owner creative acceptance. All four carry owner_approved false.",
            ],
            "not_authorized": [
                "Upload, publication, scheduling, or Related Video binding for any Short.",
                "Resolving [EPISODE_URL], by hand or to the existing EP006 URL.",
                "Any change to the locked master, narration, transcript or accepted natives.",
                "Treating this revision, its passing checks or its validator exits as owner acceptance.",
            ],
            "deferred": [
                "A presenter take covering master 4851 to 4890 so Short 03's spoken answer can "
                "land on the presenter rather than a card. Trigger: the next presenter recording.",
                "An owner ruling on Short 01's presenter-share trade (0.665 to 0.516).",
                "Publish order: the package's 01, 04, 02, 03 was carried forward unamended, but "
                "Short 03 now resolves something, so the owner may want it earlier.",
            ],
        },
    },
    "evidence": [],
}


def main() -> None:
    L.assert_locked()
    DECISION["evidence"] = [
        ev(f"{REV}/STANDARD-JUDGMENT.md",
           "Per-Short judgment against the standalone-payoff standard, before and after, with "
           "the frames and words that decide it, and what could not be judged."),
        ev(f"{REV}/COPY-DELTA.md",
           "Which approved copy was applied where, and the six minimal changes the re-cut forced."),
        ev(f"{REV}/REVIEW-PACKAGE.json",
           "The four candidates with titles, durations, payoff lines, closing lines and pinned "
           "comments; owner_approved false and related_video_bound false on all four."),
        ev(f"{REV}/LOCK-PRESERVATION.json",
           "Every locked source read by this revision, with all_unchanged true."),
        ev("blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records/"
           "2026-09-21-owner-shorts-rulings.json",
           "The owner ruling this revision executes: standalone-payoff standard governs, Short "
           "03 one-beat re-cut, slug direct-booking-practice."),
        ev("docs/content-rubric.md",
           "Shorts addendum, kill list item 'no standalone narrow payoff', and the Shorts "
           "derivative checks that retire cliffhanger_line."),
        ev("blueprint-cinema/experiments/EP009-SHORTS-003/COPY-PACKAGE.json",
           "The approved copy this revision applies, and the cliffhanger blocks it supersedes."),
        ev(f"{REV}/superseded/README.md",
           "The r3 renders and records superseded by this revision, and why none were deleted."),
    ]
    append(DECISION)

    for num, slug, title in SHORTS:
        contract = json.loads((L.REPO / REV / slug / "source-contract.json").read_text())
        validation = json.loads((L.REPO / REV / slug / "CONTRACT-VALIDATION.json").read_text())
        verification = json.loads((L.REPO / REV / "VERIFICATION.json").read_text())
        entry = next(s for s in verification["shorts"] if s["slug"] == slug)
        recut = contract["recut"]["changed"]
        corr = min(b["correlation"] for b in entry["beats"])
        limits = [
            "Perceptual lip sync was not judged. The picture slices are the accepted r3 native "
            "frames with no retime applied, which is provenance, not a measurement.",
            "Whether a cold viewer finds the payoff useful was not judged. shorts_contract.py "
            "validates declared fields and exact-copy order only.",
            "Phone playback was browser viewport emulation at 390x844, not a physical device.",
            "This is not owner creative acceptance.",
        ]
        if num == "03":
            limits.insert(1, "Timeline frames 334 to 380 carry a designed card, not presenter "
                             "picture, because no lip-synced frames exist for master 4851 to "
                             "4890. Lip sync is not applicable there and the picture ends 1.9 s "
                             "before the speech does.")
        if num == "01":
            limits.insert(1, "The presenter share of speech falls from 0.665 to 0.516. That is a "
                             "direction trade against the avatar-forward direction, reported for "
                             "an owner ruling rather than resolved here.")
        append({
            "event_id": f"ep009-shorts-r4-verified-{num}",
            "decision_id": DECISION_ID,
            "event_type": "verification",
            "tags": ["shorts", "r4", f"short-{num}", "verification"],
            "data": {
                "decision_event_id": DECISION_EVENT,
                "scope": f"Short {num} ({title}) as delivered at {REV}/{slug}/review/"
                         f"{slug}-r4.mp4. Re-cut: {recut}",
                "artifact_hashes": [
                    art(f"{REV}/{slug}/review/{slug}-r4.mp4"),
                    art(f"{REV}/{slug}/source-contract.json"),
                    art(f"{REV}/{slug}/manifest.json"),
                    art(f"{REV}/{slug}/CONTRACT-VALIDATION.json"),
                    art(f"{REV}/{slug}/index.html"),
                    art(f"{REV}/{slug}/captions.json"),
                    art(f"{REV}/{slug}/captions.srt"),
                    art(f"{REV}/{slug}/captions.vtt"),
                ],
                "method":
                    f"hyperframes@0.8.53 check --strict (lint, runtime, layout, motion, WCAG AA "
                    f"contrast): passed. hyperframes render --quality delivery --strict-all. "
                    f"ffprobe -count_frames: {entry['frame_count']['measured']} frames at "
                    f"{entry['canvas']['width']}x{entry['canvas']['height']} "
                    f"{entry['canvas']['r_frame_rate']}, matching the declared "
                    f"{entry['frame_count']['declared']}. Per-beat zero-lag normalised "
                    f"cross-correlation of the rendered audio against the locked narration "
                    f"master at each declared master sample range: minimum "
                    f"{corr:.6f} across {len(entry['beats'])} beats. Per-frame luma spread "
                    f"YMAX-YMIN over all {entry['uniform_frames']['frames_measured']} encoded "
                    f"frames: minimum {entry['uniform_frames']['min_luma_spread']}, "
                    f"{entry['uniform_frames']['uniform_frames']} uniform frames. Encoded frames "
                    f"immediately before and after every cut were extracted and inspected. "
                    f"shorts_contract.py --require-pinned-comment --json: exit "
                    f"{validation['exit_code']}, valid "
                    f"{str(validation['stdout']['valid']).lower()}, "
                    f"{len(validation['stdout']['issues'])} issues. Browser playback at 390x844, "
                    f"unmuted, playbackRate 1, played to the native ended event with no "
                    f"MediaError and HTTP 206 on range requests.",
                "result": "pass",
                "limitations": " ".join(limits),
            },
            "evidence": [
                ev(f"{REV}/VERIFICATION.json",
                   f"Frame count, per-beat audio correlation and luma spread for {slug}."),
                ev(f"{REV}/{slug}/CONTRACT-VALIDATION.json",
                   "The shorts_contract.py command, exit code and actual JSON output."),
                ev(f"{REV}/PHONE-PLAYBACK-QA.json",
                   f"Browser playback at 390x844 for Short {num}: ended true, muted false, "
                   f"no media error."),
                ev(f"{REV}/{slug}/source-contract.json",
                   "Exact master and native frame ranges, ffmpeg transform chains, what changed "
                   "against r3 and what it cost."),
            ],
        })

    res = subprocess.run(
        ["python3", str(LOG), "validate", "--episode", EPISODE,
         "--root", str(L.REPO), "--evidence"],
        capture_output=True, text=True)
    print("--- validate --evidence ---")
    print(res.stdout.strip() or "(no output)")
    if res.stderr.strip():
        print(res.stderr.strip())
    print("exit", res.returncode)


if __name__ == "__main__":
    main()
