#!/usr/bin/env python3
"""Check that the game files on the 1985 tapes are the bytes of the unpacked images.

Run from the project root:   python3 tools/tape_check.py

Each side holds a loader (DALEY at $0600) and two files. The loader LOADs them with secondary
address 0 at addresses of its own choosing, so ADDS on side 2 lands at $0800, not its header's $1400.
Each file, placed where the loader puts it, must equal the same range of the unpacked image.
Exit status 1 on any difference.
"""
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
from c16_tap import programs  # noqa: E402
from media import read_prg  # noqa: E402

# side tape, unpacked image, [(program index, address the loader loads it at)]
SIDES = [
    ("original/dt_star_events_side1.tap", "original/day_one_unpacked_vice.prg", [(1, 0x1000), (2, 0x3000)]),
    ("original/dt_star_events_side2.tap", "original/day_two_unpacked_vice.prg", [(1, 0x1000), (2, 0x0800)]),
]


def main():
    ok = True
    for tap, image, files in SIDES:
        progs = programs(ROOT / tap)
        base, img = read_prg(ROOT / image)
        covered = set()
        for index, at in files:
            p = progs[index]
            seg = img[at - base:at - base + len(p["data"])]
            same = seg == p["data"]
            ok &= same
            covered.update(range(at, at + len(p["data"])))
            print(f"{Path(tap).name} {p['name']:<6} header ${p['start']:04X}, loaded at ${at:04X}–${at + len(p['data']) - 1:04X}: "
                  f"{'IDENTICAL' if same else 'DIFFERS'} to {Path(image).name}")
        rest = [a for a in range(base, base + len(img)) if a not in covered]
        print(f"  image bytes not from the tape: {' '.join(f'${a:04X}' for a in rest[:8])}"
              + (" …" if len(rest) > 8 else "") + f" ({len(rest)})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
