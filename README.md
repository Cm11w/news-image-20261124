[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Cm11w/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Cm11w/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

# Sum up 24 November's world news in one image

One 1024x1024 newspaper front page for **Tuesday, November 24, 2026**:
40 stories from 10 regions, led by Nvidia reinstating Jensen Huang
(shares closed +31% — their best day since 2003 — Bitcoin +17% off
its low to $64,505), with three drawn panels — a Bitcoin chart, a
Russian corvette sunk by Ukrainian sea drones, and the Democrats'
258+ House seats.

## How it is built

- `draw_entry.py` — draws `entry.png` with PIL (fixed fonts, fixed
  layout, no clock or randomness, so re-runs are byte-identical).
  Run it with `python3 draw_entry.py`.
- `main.ts` — the entrypoint (Node 22, standard library only). It
  copies `entry.png` into the grading output directory after
  validating it: PNG magic, at most 1 MiB and 1024x1024, and every
  chunk's CRC through to IEND.
- `research-24nov.md` — the 40 stories and their sources, plus the
  Tuesday-morning refresh (Monday's market close, NATO, peace talks).

## Run

```sh
python3 draw_entry.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
