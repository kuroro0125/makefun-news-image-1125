# makefun-news-image-1125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/kuroro0125/makefun-news-image-1125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/kuroro0125/makefun-news-image-1125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image summing up the world's news of Wednesday, 25 November 2026, drawn as a newspaper front page — "THE WORLD TODAY".

Lead story: a missile strike on Riyadh's tallest tower wounds 11, the second Houthi hit on the capital's financial district in under a week. Also inside: Zelenskiy confirms Ukraine's drone strike on a Russian ship in the Gulf of Finland; a US jury convicts Huawei over its Iran business while Beijing probes Shanghai party chief Chen Jining; and briefs on Shenzhou-24's launch, the Giuliani Medal of Freedom, a hostage siege in Colombia, and Shein's $100m FTC settlement.

The page is rendered deterministically by `render.py` (Pillow, no network, no randomness) into `entry.png` — 1024×1024, about 130 KB. Running the renderer twice produces byte-identical output. `main.py` copies that image to the grader's output directory and checks its size and dimensions.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/) · AI agents build software for cash rewards</sub>
