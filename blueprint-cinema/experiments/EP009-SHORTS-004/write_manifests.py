#!/usr/bin/env python3
"""Write one shorts_contract.py manifest per Short, with exact-copy anchors.

Every spoken anchor is derived from the locked word transcript by word id, so
hook_line, payoff_line and closing_line are exact substrings of spoken_copy by
construction rather than by transcription. Nothing here is a declared payoff the
cut does not speak: each payoff_line is a word range that is audible in the
delivered MP4.
"""
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oe_shorts_r4 as L  # noqa: E402

P = Path(__file__).resolve().parent
WI = L.word_index()


def text(lo: str, hi: str) -> str:
    return " ".join(WI[f"W{n:06d}"]["token"]
                    for n in range(int(lo[1:]), int(hi[1:]) + 1))


PIN_01 = (
    "Full episode: [EPISODE_URL]\n\n"
    "The arithmetic this Short stops short of: the inn's four modeled inputs, the "
    "reported commission band, and the ceiling that caps what an outside operator "
    "could charge for the work. Commission mechanics are from Booking.com's own "
    "partner help, which says commission is a set percentage of the whole booking, "
    "charged at checkout."
)
PIN_02 = (
    "[EPISODE_URL]\n\n"
    "The drafting step you are watching is Node-RED calling a language model on a "
    "fictional guest, with nothing sent. The full episode builds the rest of the job "
    "around it and prices the retainer against the recoverable amount rather than the "
    "commission total."
)
PIN_03 = (
    "[EPISODE_URL]\n\n"
    "Booking.com's own partner help says it does not share private guest email "
    "addresses: both sides see an alias ending @guest.booking.com, and partners are "
    "asked to keep the conversation on the platform. The full episode covers what an "
    "outside operator can and cannot legally do with a guest list under those terms."
)
PIN_04 = (
    "[EPISODE_URL]\n\n"
    "The full episode runs this on an illustrative inn: 20 rooms, $180 average daily "
    "rate, 70 percent occupancy, and the booking-site share Cloudbeds reports "
    "worldwide. It shows why the recoverable amount, not the commission total, sets "
    "what the inn can pay, and what is left after the work."
)

SHORTS = [
    {
        "id": "01",
        "slug": "01-second-commission",
        "title": "When the guest returns, the commission does too",
        "beats": [("W000151", "W000165"), ("W000089", "W000109"), ("W000140", "W000149")],
        "hook": ("W000151", "W000158"),
        "payoff": ("W000090", "W000101"),
        "closing": ("W000140", "W000149"),
        "cold_viewer_context":
            "A small inn takes a booking through a booking site and pays it a "
            "commission; a year later the same guest books the same room through the "
            "same booking site.",
        "standalone_payoff":
            "The second booking costs the inn a second commission the same size as the "
            "first, charged on a guest the inn already had.",
        "episode_extension":
            "The four modeled inputs that price the work, and the monthly ceiling they "
            "produce for an illustrative inn.",
        "pinned_comment": PIN_01,
        "description": [
            "A small inn takes a booking through a booking site, pays commission, and "
            "then the same guest books the same way again.",
            "Commission is charged per booking, so the second stay costs the inn what "
            "the first one did, on a guest it already had. Booking.com's own partner "
            "help describes that mechanic.",
            "Nobody selling a fix for it has published the arithmetic. EP009 runs it on "
            "an illustrative 20-room inn.",
            "Full episode: [EPISODE_URL]",
        ],
        "claims_cited": ["C004", "C016", "C022"],
    },
    {
        "id": "02",
        "slug": "02-cheap-tools",
        "title": "Cheap parts, and a job still left to sell",
        "beats": [("W000195", "W000216"), ("W001024", "W001038"),
                  ("W002018", "W002035"), ("W000646", "W000666")],
        "hook": ("W000195", "W000206"),
        "payoff": ("W000654", "W000666"),
        "closing": ("W000660", "W000666"),
        "cold_viewer_context":
            "A small hotel pays a booking site a commission to meet its own returning "
            "guests again, and the parts of a direct-booking follow-up are cheap: a "
            "language model drafts the messages.",
        "standalone_payoff":
            "The drafting is the cheap part. What is left to sell is the job around it, "
            "and its price is capped by what the practice recovers.",
        "episode_extension":
            "How the rest of that job is designed around the drafting step, and the "
            "retainer it supports.",
        "pinned_comment": PIN_02,
        "description": [
            "A small hotel pays a booking site a commission to meet its own returning "
            "guests again. The parts of a direct-booking follow-up are cheap: a "
            "language model drafts the thank you and the review request.",
            "The screen recording is that drafting step running in Node-RED, on a "
            "fictional guest, with nothing sent and every draft awaiting human review.",
            "So what is left for an outside operator to sell is the job around it, and "
            "what it recovers is what caps the price. EP009 works that out.",
            "Full episode: [EPISODE_URL]",
        ],
        "claims_cited": ["C020", "C022", "C023"],
    },
    {
        "id": "03",
        "slug": "03-guest-relationship",
        "title": "The booking site keeps the guest's email",
        "beats": [("W000538", "W000588")],
        "hook": ("W000538", "W000547"),
        "payoff": ("W000584", "W000588"),
        "closing": ("W000584", "W000588"),
        "cold_viewer_context":
            "When a guest books a small hotel through a booking site, the site "
            "introduces the guest and holds the contact address.",
        "standalone_payoff":
            "Nobody at the inn is paid to make sure the returning guest's second "
            "booking comes to the inn instead of back through the site.",
        "episode_extension":
            "What an outside operator may legally do with a guest list under the "
            "platform's own partner terms.",
        "pinned_comment": PIN_03,
        "description": [
            "A guest books a small inn through a booking site. The site introduces the "
            "guest and holds the contact address. Booking.com's partner help says it "
            "does not share private email addresses, and both sides see an alias.",
            "When that guest comes back, nobody at the inn is paid to make sure the "
            "second booking comes to the inn instead.",
            "EP009 asks whether somebody outside the property can be, and what the job "
            "is worth.",
            "Full episode: [EPISODE_URL]",
        ],
        "claims_cited": ["C007", "C008", "C022"],
    },
    {
        "id": "04",
        "slug": "04-wrong-number",
        "title": "The commission total is the wrong number",
        "beats": [("W001447", "W001475"), ("W001305", "W001322")],
        "hook": ("W001447", "W001461"),
        "payoff": ("W001305", "W001313"),
        "closing": ("W001314", "W001322"),
        "cold_viewer_context":
            "A small hotel's commission problem is usually stated as its total "
            "booking-site commissions.",
        "standalone_payoff":
            "The commission total is not the addressable amount, because the inn still "
            "needs the sites. What it can pay is capped by what the recovery job "
            "actually shifts.",
        "episode_extension":
            "That cap computed on an illustrative inn from four inputs, and what is "
            "left after the work.",
        "pinned_comment": PIN_04,
        "description": [
            "Total booking-site commissions is the easy number to reach for. It is the "
            "wrong one, because a small inn is never going to move all of it. It needs "
            "the sites.",
            "The number that matters is what a recovery service can actually shift, and "
            "that is what caps what the inn can pay for the job.",
            "Nobody selling this work has published that figure. EP009 calculates it on "
            "an illustrative 20-room inn.",
            "Full episode: [EPISODE_URL]",
        ],
        "claims_cited": ["C014", "C018", "C020", "C022"],
    },
]


def main() -> None:
    L.assert_locked()
    written = []
    for short in SHORTS:
        contract = json.loads((P / short["slug"] / "source-contract.json").read_text())
        spoken = " ".join(text(lo, hi) for lo, hi in short["beats"])
        record = {
            "id": short["id"],
            "slug": short["slug"],
            "title": short["title"],
            "duration_s": contract["duration"],
            "frame_count": contract["frame_count"],
            "cold_viewer_context": short["cold_viewer_context"],
            "hook_line": text(*short["hook"]),
            "payoff_line": text(*short["payoff"]),
            "standalone_payoff": short["standalone_payoff"],
            "closing_line": text(*short["closing"]),
            "last_line": text(*short["closing"]),
            "spoken_copy": spoken,
            "episode_extension": short["episode_extension"],
            "pinned_comment": short["pinned_comment"],
            "description": short["description"],
            "claims_cited": short["claims_cited"],
            "episode_url": "[EPISODE_URL]",
            "hashtags": [],
            "owner_approved": False,
            "published": False,
        }
        payload = {
            "schema": "oe-shorts-standalone-manifest-v1",
            "revision": "EP009-SHORTS-004",
            "episode": "EP009",
            "episode_slug": "direct-booking-practice",
            "standard": "docs/content-rubric.md Shorts addendum and Shorts derivative checks "
                        "(standalone payoff; cliffhanger_line retired)",
            "owner_ruling": "ep009-owner-shorts-standard-ruling-v1",
            "standalone_contract": {
                "context_rule": "Each Short names the small-hotel booking-site commission "
                                "situation in its own speech or its own frame-one design, "
                                "with no reliance on another Short.",
            },
            "scripts": [record],
        }
        out = P / short["slug"] / "manifest.json"
        L.write_json(out, payload)
        written.append(str(out.relative_to(L.REPO)))
    print("\n".join(written))


if __name__ == "__main__":
    main()
