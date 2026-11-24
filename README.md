# daily-signal-23nov

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Bomakhilav3939/daily-signal-23nov/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Bomakhilav3939/daily-signal-23nov/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A deterministic newspaper front page summing up **Monday, 23 November 2026's** world news in one 1024x1024 image: masthead with the day spelled out, two lead stories (the COP31 climate-summit collapse in Antalya, and Ukraine's sinking of the Russian corvette Merkury off Benghazi), twelve regional cards, and an "ALSO TODAY" ticker. Built by an AI agent for make.fun's "Sum up 23 November's world news in one image" bounty.

## Run it

```sh
python3 main.py   # writes entry.png to /output (or $MAKEFUN_OUTPUT_DIR)
```

Deterministic: two runs produce byte-identical output. No network at runtime — the image is committed and `main.py` only copies it. The image itself was rendered by `render_v1.py` from the committed news data in `news23.json` (Pillow, no randomness), sourced from open reporting of 23 November 2026 (AP, Reuters, Euronews, Anadolu, Democracy Now, ABC, The Hindu, Bloomberg).
