#!/usr/bin/env bash
# Commit the bot's memory (state.json) and push it: to the private state repository when it was checked out
# into .state, otherwise to this repository. If another run pushed first, merge both runs' changes and retry.
set -u
BOT="$(cd "$(dirname "$0")" && pwd)/bot.py"
if [ -d .state ]; then cd .state; fi
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
[ "$BRANCH" = "HEAD" ] || [ -z "$BRANCH" ] && BRANCH=main
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
[ -f state.json ] || exit 0
git add state.json
git diff --cached --quiet && exit 0
git commit -q -m "Update state"
for attempt in 1 2 3 4 5 6; do
  git push -q origin "HEAD:$BRANCH" && exit 0
  echo "Push rejected (attempt $attempt); merging with the newer state"
  git show HEAD~1:state.json > /tmp/base.json 2>/dev/null || echo '{}' > /tmp/base.json
  cp state.json /tmp/ours.json
  git fetch -q origin "$BRANCH"
  git reset -q --hard "origin/$BRANCH"
  python3 "$BOT" merge-state /tmp/base.json /tmp/ours.json
  git add state.json
  git diff --cached --quiet && exit 0
  git commit -q -m "Update state (merged)"
  sleep $((RANDOM % 6 + 2))
done
exit 1
