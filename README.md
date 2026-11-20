# The World in One Day — Thursday 19 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/mumun110795/news-image-20261119-v3/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/mumun110795/news-image-20261119-v3/reward.svg)](https://make.fun/bounty/news-image-20261119)

A newspaper front page in one picture: all of Thursday 19 November 2026 on a
single page — a giant date masthead, a region bar and stat strip, three
illustrated hero stories (the Shenzhen three-way summit, the ICJ genocide
verdict against Myanmar, and Anthropic's record IPO), ten numbered story
cards, a "Markets at the Close" box, and an "Also on Thursday" list that
brings the page to 53 stories from 7 regions.

`main.py` (Python 3, standard library only, no network) draws everything in
code — its own bitmap fonts, its own PNG encoder, and flat illustrations of
the summit skyline and flags, the scales of justice, and the IPO chart — and
writes a deterministic `entry.png` (byte-identical on every run).

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024×1024, well under 1 MiB).

<sub>Entered on [make.fun](https://make.fun/?ref=vdsf53gd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
