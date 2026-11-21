#!/usr/bin/env python3
"""Unpack the crunched PRGs by running their own decruncher in tools/cpu6502.py, and check the result.

Run from the project root:   python3 tools/unpack_sfx.py [--check]

Each packed PRG starts at its BASIC SYS ($100D), copies the decruncher onto the stack page and unpacks
the game downwards from $3FFF. The run stops when the stack-page decruncher jumps to the game's entry.
Only RAM is modelled (no TED, no ROM): the decruncher reads nothing from either, and the result is the
same for any starting stack pointer. The image saved is exactly the range the decruncher wrote.

Without --check, writes build/<part>_unpacked.prg (load address + bytes).
With --check, compares that image with the VICE dump in original/ and exits 1 on any difference.
"""
import argparse
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
from cpu6502 import CPU  # noqa: E402
from media import read_prg  # noqa: E402

# part, packed PRG, game entry the decruncher jumps to, VICE dump of the unpacked memory
PARTS = [
    ("day_one", "original/daley_thompsons_star_events_day_one.prg", 0x1010, "original/day_one_unpacked_vice.prg"),
    ("day_two", "original/daley_thompsons_star_events_day_two.prg", 0x2111, "original/day_two_unpacked_vice.prg"),
]


class Mem(bytearray):
    """64 KB of RAM that records every address written."""
    def __setitem__(self, k, v):
        if isinstance(k, int):
            self.written.add(k)
        bytearray.__setitem__(self, k, v)


def unpack(packed, entry):
    load, data = read_prg(ROOT / packed)
    mem = Mem(0x10000)
    mem.written = set()
    mem[load:load + len(data)] = data
    mem.written = set()
    cpu = CPU(mem)
    cpu.pc, cpu.sp, prev, steps = 0x100D, 0xF6, 0, 0
    while not (cpu.pc == entry and 0x100 <= prev < 0x200):  # the jump from the stack-page decruncher
        prev = cpu.pc
        cpu.step()
        steps += 1
        if steps > 5_000_000:
            raise SystemExit(f"{packed}: decruncher did not reach ${entry:04X}")
    game = [a for a in mem.written if 0x0400 <= a < 0x4000]  # skip zero page, stack, tables and TED
    lo, hi = min(game), max(game)
    return lo, bytes(mem[lo:hi + 1]), cpu.cycles


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="compare with the VICE dumps in original/")
    args = ap.parse_args()
    ok = True
    for part, packed, entry, dump in PARTS:
        lo, img, cycles = unpack(packed, entry)
        line = f"{part}: ${lo:04X}–${lo + len(img) - 1:04X}, {len(img)} bytes, entry ${entry:04X}, {cycles} cycles"
        if args.check:
            vload, vdata = read_prg(ROOT / dump)
            same = vload == lo and vdata == img
            ok &= same
            print(f"{line}, VICE dump {'IDENTICAL' if same else 'DIFFERS'}")
        else:
            out = ROOT / "build" / f"{part}_unpacked.prg"
            out.parent.mkdir(exist_ok=True)
            out.write_bytes(bytes([lo & 0xFF, lo >> 8]) + img)
            print(f"{line} -> {out.relative_to(ROOT)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
