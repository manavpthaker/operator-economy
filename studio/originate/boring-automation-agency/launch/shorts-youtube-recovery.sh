#!/usr/bin/env bash
# EP003 shorts — YouTube upload recovery (week-driver, Tue 2026-07-28)
#
# WHY THIS EXISTS: launch.py --go uploaded the episode but no shorts
# (links.json "shorts": []). All four MP4s are rendered in remotion/out/,
# nothing is on the channel, and Tue 7/28's 8:30 short did not go live.
#
# Publish times are set to Wed 7/29 - Sat 8/1 at 8:30 AM ET so the YouTube
# shorts pair 1:1 with the LinkedIn OE-page posts in shorts-schedule-kit.md
# (that kit already moved to Wed-Sat to avoid colliding with Tuesday's
# 8:30 episode post). 12:30Z == 8:30 AM ET.
#
# Run from studio/ :   bash originate/boring-automation-agency/launch/shorts-youtube-recovery.sh
# Uploads are scheduled (privacy=private + publishAt), AI-disclosure auto-set.
#
# AFTER UPLOAD, still manual (force-ssl scope not yet on the token, backlog #1):
#   - pin an @operatoreconomy comment on each short routing to episode + blueprint
#   - paste the returned URLs into launch/links.json "shorts"

set -euo pipefail
cd "$(dirname "$0")/../../.."   # -> studio/

EP="https://youtu.be/tvlVy6sIoYo"
BP="https://theoperatoreconomy.com/episodes/boring-automation-agency"
DESCDIR="originate/boring-automation-agency/launch/short-descriptions"
mkdir -p "$DESCDIR"

write_desc () { # $1=n  $2=tease line
  cat > "$DESCDIR/short-$1.txt" <<EOF
Full episode, The 5 Billion Dollar Business That Sounds Boring: $EP

The Operator Blueprint № 003, free, every source and number flagged: $BP

$2

Research, not an income promise. Reported figures are flagged as reported.
EOF
}

write_desc 01 "The full breakdown of who's actually charging this and how is in the episode."
write_desc 02 "What those workflows actually looked like, and what to charge for them, is in the full episode."
write_desc 03 "The full pricing bands and where the money actually comes from are in the full video."
write_desc 04 "The exact stack, cost, and where this node fits are in the full breakdown."

up () { # $1=n  $2=title  $3=publishAt
  echo "--- uploading short-$1 ($3) ---"
  python scripts/originate/upload_youtube.py "remotion/out/short-$1.mp4" \
    --title "$2" \
    --description-file "$DESCDIR/short-$1.txt" \
    --privacy private \
    --publish-at "$3"
}

up 01 "The \$5B Business Nobody Wants to Build"              "2026-07-29T12:30:00Z"
up 02 "Why One Person Can Now Do an Integration Team's Job"  "2026-07-30T12:30:00Z"
up 03 "The Real Reason Small Businesses Pay for This"        "2026-07-31T12:30:00Z"
up 04 "The One AI Node That Changes the Pricing"             "2026-08-01T12:30:00Z"

echo
echo "Done. Paste the four URLs into launch/links.json -> shorts[].url,"
echo "then pin the routing comment on each once it publishes."
