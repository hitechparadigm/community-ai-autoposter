#!/usr/bin/env bash
# Commit state.json and push it. If another run pushed first, merge both runs' changes and retry.
set -u
git config user.name "autopost-bot"
git config user.email "autopost-bot@users.noreply.github.com"
git add state.json
git diff --cached --quiet && exit 0
git commit -q -m "Update state"
for attempt in 1 2 3 4 5 6; do
  git push -q && exit 0
  echo "Push rejected (attempt $attempt); merging with the newer state"
  git show HEAD~1:state.json > /tmp/base.json
  cp state.json /tmp/ours.json
  git fetch -q origin main
  git reset -q --hard origin/main
  python3 bot.py merge-state /tmp/base.json /tmp/ours.json
  git add state.json
  git diff --cached --quiet && exit 0
  git commit -q -m "Update state (merged)"
  sleep $((RANDOM % 6 + 2))
done
exit 1
