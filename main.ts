// gta6-meme-x-01 entry: "13 Years Waiting for GTA 6".
//
// This program is the whole deliverable the grader runs. It takes the
// two files that define the entry out of this repository and puts them
// in the output directory, byte for byte:
//
//   POST.json  -> the address of the X post that carries the meme
//   meme.png   -> the meme picture itself (1080x1080)
//
// The post is the entry: the house reads the post from X, takes its
// first picture and its text, and an AI judge ranks it against the
// other posts. Nothing this program prints or writes is judged.
//
// Node 22, standard library only. No network, no clock, no files
// outside the repository, so two runs always write the same bytes.
//
// Run it locally the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// The two files that make up the entry. Keep this list short and
// explicit: if either one is missing, fail loudly instead of
// handing the grader a half-empty output directory.
const ENTRY_FILES = ["POST.json", "meme.png"];

mkdirSync(OUTPUT_DIR, { recursive: true });

for (const name of ENTRY_FILES) {
  const source = join(BOT_DIR, name);
  const target = join(OUTPUT_DIR, name);
  if (!existsSync(source)) {
    console.error(`entry file missing from ${BOT_DIR}: ${name}`);
    process.exit(1);
  }
  try {
    copyFileSync(source, target);
  } catch (err) {
    console.error(`could not copy ${name} to ${OUTPUT_DIR}: ${(err as Error).message}`);
    process.exit(1);
  }
}

console.log(`wrote ${ENTRY_FILES.join(", ")} to ${OUTPUT_DIR}`);
