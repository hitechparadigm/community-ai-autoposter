#!/usr/bin/env python3
"""Community AI autoposter (settings: config.py, editorial instructions: prompts.py, code: autoposter/).

  python bot.py tick      - every 5 minutes: run what's due by config.SCHEDULE, then publish approved posts
  python bot.py draft     - news drafts ("draft tips" = a 💡 Варто знати practical story)
  python bot.py digest    - the morning digest
  python bot.py thisday   - one "This day in history" post
  python bot.py history   - one history long-read ("history community" = a community-history story)
  python bot.py history-from SOURCE [thisday] - a long-read from a page or wiki:Article_title
  python bot.py approve   - read approvers' taps, replies and ideas; publish approved posts
  python bot.py review    - the monthly review of feedback and reader reactions, now
  python bot.py rewrite PAGE SOURCE - rewrite a published Telegraph long-read in place
  python bot.py post | edit LINK | recard MATCH | cards [FILE] | check - manual tools (see the workflows)
  python bot.py merge-state BASE OURS - used by save_state.sh

No third-party packages needed (standard library only).
"""
from autoposter.cli import main

if __name__ == "__main__":
    main()
