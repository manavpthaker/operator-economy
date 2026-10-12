#!/bin/bash
# publish_mon.sh — the Monday 11:00 ET site-flip runner.
#
# Flips the GIVEN slug live by writing its episode URL into
# site/data/episode-urls.json (from launch/links.json), commits that file, and
# emails notify:{slug} subscribers via Resend. Auto-answers the notify confirm
# prompt (yes), since this may run unattended.
#
# It does NOT push by default. Production builds from `main`, so the flip only
# reaches the site once the commit is on `main` — and putting a commit on `main`
# is the owner's call. Set OE_PUBLISH_PUSH=1 to have this script push too.
#
# USAGE: publish_mon.sh <slug>
# The slug is REQUIRED and must be passed explicitly. It used to be hardcoded to
# "voice-agent-agency" (EP002); a stale `at` job firing this would have silently
# republished EP002. Refusing to run without an explicit slug is the guard.
#
# Before 2026-10-12 this flipped site/data/episodes.json, which no longer drives
# the library. See studio/scripts/originate/publish.py.

set -u
SLUG="${1:?REFUSING TO RUN: no slug given. Usage: publish_mon.sh <slug>}"
# Resolve the repo from this script's own location rather than a hardcoded home
# directory — the old absolute path had gone stale and broke the whole run.
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
LOG="$REPO/studio/originate/$SLUG/launch/publish_mon.log"

exec >>"$LOG" 2>&1
echo "==== publish_mon.sh @ $(date -Iseconds) ===="
echo "repo: $REPO"

# Load site .env.local so DATABASE_URL + RESEND_API_KEY are available.
if [ -f "$REPO/site/.env.local" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$REPO/site/.env.local"
  set +a
fi

cd "$REPO/studio" || { echo "cd studio failed"; exit 1; }

echo "-- flip the episode URL into the site registry"
python3 scripts/originate/publish.py "$SLUG" || { echo "publish flip failed"; exit 1; }

echo "-- git commit"
cd "$REPO" || exit 1
git add site/data/episode-urls.json
if git diff --cached --quiet; then
  echo "no changes to commit (already flipped?)"
else
  git commit -m "publish: $SLUG live (auto-fire $(date -u +%Y-%m-%dT%H:%MZ))" || {
    echo "commit failed"; exit 1; }
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "${OE_PUBLISH_PUSH:-0}" = "1" ]; then
  echo "-- push $BRANCH (OE_PUBLISH_PUSH=1)"
  if [ "$BRANCH" != "main" ]; then
    echo "REFUSING TO PUSH: on '$BRANCH', not main. Production builds from main."
  else
    git push origin main || { echo "push failed"; exit 1; }
  fi
else
  echo "-- not pushing (OE_PUBLISH_PUSH unset). The flip is committed on '$BRANCH';"
  echo "   it reaches the site only once that commit is on main."
fi

echo "-- send notify:$SLUG (Resend, auto-yes)"
cd "$REPO/studio" || exit 1
echo "y" | python3 scripts/originate/publish.py "$SLUG" --notify \
  || { echo "notify failed (subscribers may need manual send)"; }

echo "==== done @ $(date -Iseconds) ===="
