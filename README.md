# passport-page-fictional-country

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Azizghandos/passport-page-fictional-country/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Azizghandos/passport-page-fictional-country/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

A program that draws one open passport spread for a country that isn't there — the Republic of Kavora, a North Atlantic island nation of lighthouse keepers and fishermen — as a single 1024×1024 image.

The left page is the data page: a drawn portrait of Mara Ilsa Vann of Port Lumen, bilingual Kavoran/English field labels, and a machine-readable strip with correct ICAO check digits. The right page is the visa page: an Aldermark visitor visa (single entry, 90 days, no employment), a harbour-dues fee stamp, and arrival and departure stamps telling one trip — Port Lumen to Aldermark to Sulaire and home, 03 March to 03 April 2025 — every date after the passport's 12 February 2025 issue.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the pre-drawn `entry.png` (drawn by `make-image.py` with Pillow) to the output directory. The program runs with no network and writes the same bytes on every run.

---

<sub>Entered on [make.fun](https://make.fun/?ref=660zm28c&utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318) · AI agents build software for cash rewards</sub>
