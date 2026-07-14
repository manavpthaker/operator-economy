#!/bin/bash
# publish_mon.sh — the "Monday 11:00 ET auto-fire" runner.
#
# Flips voice-agent-agency to live in site/data/episodes.json, git-pushes so
# Vercel redeploys with the new state, then emails notify:{slug} subscribers
# via Resend. Auto-answers the notify confirm prompt (yes) because this runs
# unattended.
#
# Scheduled via macOS `at` (see the at-queue this project's launch registered).
# All output is appended to studio/originate/voice-agent-agency/launch/publish_mon.log.

set -u
SLUG="voice-agent-agency"
REPO="/Users/manavthaker/Documents/GitHub/operator-economy"
LOG="$REPO/studio/originate/$SLUG/launch/publish_mon.log"

exec >>"$LOG" 2>&1
echo "==== publish_mon.sh @ $(date -Iseconds) ===="

# Load site .env.local so DATABASE_URL + RESEND_API_KEY are available.
if [ -f "$REPO/site/.env.local" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$REPO/site/.env.local"
  set +a
fi

cd "$REPO/studio" || { echo "cd studio failed"; exit 1; }

echo "-- flip status → live"
python3 scripts/originate/publish.py "$SLUG" --rev A || { echo "publish flip failed"; exit 1; }

echo "-- git commit + push (Vercel picks up the deploy)"
cd "$REPO" || exit 1
git add site/data/episodes.json
if git diff --cached --quiet; then
  echo "no changes to commit (episodes.json unchanged?)"
else
  git commit -m "publish: $SLUG live (auto-fire $(date -u +%Y-%m-%dT%H:%MZ))" || {
    echo "commit failed"; exit 1; }
  git push origin main || { echo "push failed"; exit 1; }
fi

echo "-- send notify:$SLUG (Resend, auto-yes)"
cd "$REPO/studio" || exit 1
echo "y" | python3 scripts/originate/publish.py "$SLUG" --rev A --notify \
  || { echo "notify failed (subscribers may need manual send)"; }

echo "==== done @ $(date -Iseconds) ===="
