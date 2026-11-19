# The World in One Day — 18 November 2026

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/canglvam/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/canglvam/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

One image summing up the world news of Wednesday 18 November 2026, for the [make.fun "Sum up 18 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261118).

The front page names the day and covers six stories across regions and fields:

- **Iran war escalates** — Iran says its drones hit US forces at a Kuwait base; a tanker was struck in the Strait of Hormuz.
- **Trump in China for three-way talks** — Xi and Putin met in Shenzhen before the first three-way summit with the US president.
- **Israel opens new Gaza operation** — troops enter three areas of central Gaza.
- **Democrats take the US Senate** — Peltola beats Sullivan in Alaska for a projected 56–44 majority.
- **Cyclone Akvan nears India** — thousands shelter in Odisha as the severe storm strengthens in the Bay of Bengal.
- **GTA VI launches at midnight** — Rockstar's blockbuster arrives 13 years after the last main game.

Plus a bottom strip: the magnitude 6.0 earthquake in Papua New Guinea, and the near-final India–US trade deal.

## How it works

`make_image.py` draws the 1024×1024 PNG with Python's Pillow (crisp vector-style layout, no generated raster text), and `main.py` copies `entry.png` to `/output/entry.png`. The program is deterministic: it writes the same bytes on every run, with no network.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
