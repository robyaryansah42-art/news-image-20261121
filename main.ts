// News-image entry for make.fun (news-image-20261121), Node 22, stdlib only.
//
// The finished front page lives in this repository as entry.png; this
// program's only job is to place an exact copy of it at the output path
// the harness expects. It reads nothing else and reaches for no network,
// so two runs always produce identical bytes.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(HERE, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const bytes = readFileSync(SOURCE);
const target = join(outDir, "entry.png");
writeFileSync(target, bytes);

// Fail loudly rather than hand the grader a truncated copy.
if (readFileSync(target).length !== bytes.length) {
  throw new Error(`entry.png copy mismatch: wrote ${bytes.length} bytes`);
}
