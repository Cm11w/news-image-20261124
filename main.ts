// main.ts — entrypoint for news-image-20261124 (Node 22, standard library only).
//
// The entry image is drawn by draw_entry.py and shipped in this repository
// as entry.png. This program copies it to the output directory after
// checking it is a whole, valid PNG: correct magic bytes, at most 1 MiB,
// 1024 by 1024 pixels, and a correct CRC on every chunk up to IEND.
// It reads the copy back and confirms it matches the gated source, so
// the run delivers exactly the bytes it checked. Every run writes the
// same bytes.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

// CRC-32 (IEEE 802.3) over a chunk's type + data, as PNG requires.
const CRC_TABLE = new Uint32Array(256);
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  CRC_TABLE[n] = c >>> 0;
}

function crc32(buf: Buffer): number {
  let crc = 0xffffffff;
  for (const byte of buf) crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function fail(message: string): never {
  throw new Error(`entry.png failed the gate: ${message}`);
}

function checkPng(bytes: Buffer): void {
  if (bytes.length > MAX_BYTES) {
    fail(`size ${bytes.length} bytes exceeds ${MAX_BYTES}`);
  }
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    fail("first eight bytes are not the PNG signature");
  }
  // Walk the chunk list: length (4) + type (4) + data + CRC (4).
  let offset = 8;
  let sawIhdr = false;
  let sawIend = false;
  while (offset + 8 <= bytes.length) {
    const length = bytes.readUInt32BE(offset);
    const type = bytes.toString("ascii", offset + 4, offset + 8);
    const dataStart = offset + 8;
    const dataEnd = dataStart + length;
    if (dataEnd + 4 > bytes.length) fail(`chunk ${type} runs past the end of the file`);
    const storedCrc = bytes.readUInt32BE(dataEnd);
    const actualCrc = crc32(bytes.subarray(offset + 4, dataEnd));
    if (storedCrc !== actualCrc) fail(`chunk ${type} has a bad CRC`);
    if (type === "IHDR") {
      sawIhdr = true;
      const width = bytes.readUInt32BE(dataStart);
      const height = bytes.readUInt32BE(dataStart + 4);
      if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
        fail(`dimensions are ${width}x${height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`);
      }
    }
    offset = dataEnd + 4;
    if (type === "IEND") {
      sawIend = true;
      break;
    }
  }
  if (!sawIhdr) fail("no IHDR chunk");
  if (!sawIend) fail("no IEND chunk");
  if (offset !== bytes.length) fail("trailing bytes after IEND");
}

const repoRoot = dirname(fileURLToPath(import.meta.url));
const source = join(repoRoot, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const target = join(outputDir, "entry.png");

const bytes = readFileSync(source);
checkPng(bytes);
mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);
// Read the copy back: the run must deliver exactly the gated bytes.
const writtenBytes = readFileSync(target);
if (!writtenBytes.equals(bytes)) {
  fail("the copied file differs from the gated source");
}
console.log(`wrote ${target} (${writtenBytes.length} bytes)`);
