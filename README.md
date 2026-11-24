# News Image — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Cm11w/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Cm11w/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One page that sums up the world's news of **Tuesday, November 24, 2026**:
37 stories across 7 regions, led by Nvidia bringing Jensen Huang back
as shares jump 31% — the Nasdaq's best day since April 2025.

- **Bounty:** [Sum up 24 November's world news in one image](https://make.fun/c/news-image-20261124) — $100 shared by the top 50 entries
- **Deadline:** 26 November 2026, 00:00 UTC

## How it works

`draw_entry.py` (Python 3, Pillow) draws `entry.png` — a 1024×1024
newspaper front page: masthead, lead story, three picture panels
(Bitcoin rebound, the corvette sunk off Libya, COP31 collapsing) and a
33-story grid grouped by region. `main.ts` (Node 22, standard library
only) copies `entry.png` to the output directory after checking it is a
whole, valid PNG: correct magic bytes, at most 1 MiB, 1024×1024 pixels,
and a correct CRC on every chunk up to IEND.

```sh
python3 draw_entry.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Both commands are deterministic: every run writes the same bytes.

## Sources

`research-24nov.md` lists the 37 stories and where each was reported
(Reuters, CNN, CoinDesk, Finnhub, BBC and others, all Monday 23 November
closes or stories first reported Tuesday 24 November 2026).

## License

MIT — see [LICENSE](LICENSE).
