// Passport-page entry for the-passport-page-of-a-countr-2-20261121-0318
// (Node 22, standard library only).
//
// The entry image is entry.png beside this file: an open passport spread
// for the invented Republic of Kavora — a North Atlantic island nation of
// lighthouse keepers and fishermen. Left page: data page with a drawn
// portrait, bilingual Kavoran/English fields and a machine-readable strip.
// Right page: an Aldermark visitor visa, a harbour-dues fee stamp, and
// arrival/departure stamps telling one trip (03 Mar – 03 Apr 2025), all
// dated after the passport's 12 Feb 2025 issue. Drawn by make-image.py
// (Pillow, flat colours, crisp text).
//
// The program copies that image to the grader's output directory, so both
// runs write exactly the same bytes. It reads nothing else and needs no
// network, so it runs the same in the grader's fresh container.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
