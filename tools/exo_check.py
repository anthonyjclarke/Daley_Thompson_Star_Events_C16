#!/usr/bin/env python3
"""Re-crunch the rebuilt game with Exomizer 2.0 and compare with the surviving crunched PRGs.

Run from the project root after `make verify`:   python3 tools/exo_check.py EXOMIZER

EXOMIZER is an Exomizer 2.0beta7-2.0.9 binary (build it from the tag in
https://bitbucket.org/magli143/exomizer, e.g. 2.0.9: `make -C src`). 2.0.10 and later, 3.x and 1.x
produce different files. The commands that reproduce the originals byte for byte:

  part 1 ($1000-$3FFF):  exomizer sfx 0x1010 -t4 -n
  part 2 ($0800-$3FFF):  exomizer sfx 0x2111 -t4 -n -s"lda #$0b sta $ff06" -f"lda #$1b sta $ff06"
                         (2.0beta7-2.0.3 need "sei lda #$0b sta $ff06": later versions add the SEI)

The inputs are cut from build/day_one.prg and build/day_two.prg, the images rebuilt from src/, so a match
proves the chain from the source to the crunched files as they survive.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = [("day_one", 0x1000, 0x1010, [], "original/daley_thompsons_star_events_day_one.prg"),
         ("day_two", 0x0800, 0x2111, ["-slda #$0b sta $ff06", "-flda #$1b sta $ff06"],
          "original/daley_thompsons_star_events_day_two.prg")]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    exo = sys.argv[1]
    ok = True
    with tempfile.TemporaryDirectory() as td:
        for name, start, entry, frags, original in PARTS:
            rebuilt = (ROOT / "build" / f"{name}.prg").read_bytes()
            base = rebuilt[0] | rebuilt[1] << 8
            body = rebuilt[2 + start - base:]
            src = Path(td) / f"{name}.prg"
            src.write_bytes(bytes([start & 0xFF, start >> 8]) + body)
            want = (ROOT / original).read_bytes()
            # Part 2's enter fragment: later 2.0 versions add the SEI themselves, earlier ones need it given.
            tries = [frags, [frags[0].replace("-s", "-ssei ", 1)] + frags[1:]] if frags else [frags]
            for f in tries:
                out = Path(td) / f"{name}_sfx.prg"
                subprocess.run([exo, "sfx", f"0x{entry:04X}", "-t4", "-n", *f, "-q", "-o", str(out), str(src)],
                               check=True, capture_output=True)
                got = out.read_bytes()
                same = got == want
                if same:
                    break
            ok &= same
            print(f"{name}: ${start:04X}-${start + len(body) - 1:04X} crunched to {len(got)} bytes, "
                  f"{'IDENTICAL to' if same else 'DIFFERS from'} {original} ({len(want)} bytes)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
