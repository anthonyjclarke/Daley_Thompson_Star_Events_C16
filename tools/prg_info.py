#!/usr/bin/env python3
"""Describe original files without changing them: PRG, Oric TAP or C16 D64.

Usage: prg_info.py [--machine c16|oric] FILE...

PRG:  load address, end, length, SHA-256, and any BASIC SYS stub with its entry.
TAP:  every block (name, type, autorun, start, inclusive end, length, SHA-256).
D64:  the directory, with each PRG's load address.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from media import basic_entry, read_prg, sha256, tap_blocks  # noqa: E402


def describe_prg(path, machine):
    load, data = read_prg(path)
    print(f"{path}: PRG, load ${load:04X}–${load + len(data) - 1:04X}, {len(data)} bytes + 2-byte header")
    print(f"  SHA-256 {sha256(Path(path).read_bytes())}")
    stub = basic_entry(machine, load, data)
    if stub:
        lines, end, entry = stub
        for number, text in lines:
            print(f"  BASIC {number} {text}")
        print(f"  BASIC ends at ${end - 1:04X}" + (f"; SYS entry ${entry:04X} ({entry})" if entry else "; no SYS found"))
        if entry and not load <= entry < load + len(data):
            print("  note: SYS target lies outside this file (a loader?)")
    elif machine == "c16" and load in (0x1001, 0x0801):
        print("  starts at the BASIC area but no SYS stub was decoded")
    else:
        print("  no BASIC stub: loaded with LOAD\"…\",8,1 and started at an address to find (try the load address)")


def describe_tap(path):
    raw = Path(path).read_bytes()
    print(f"{path}: Oric TAP, {len(raw)} bytes, SHA-256 {sha256(raw)}")
    for n, b in enumerate(tap_blocks(path)):
        kind = {0x00: "BASIC", 0x80: "code"}.get(b["type"], f"type ${b['type']:02X}")
        print(f"  block {n}: {b['name']!r} {kind}, autorun ${b['auto']:02X}, ${b['start']:04X}–${b['end']:04X} "
              f"({len(b['data'])} bytes), header {b['header'].hex(' ')}, SHA-256 {sha256(b['data'])[:16]}…")
        if len(b["data"]) != b["end"] - b["start"] + 1:
            print("    WARNING: block is shorter than its header says")


def describe_d64(path):
    from d64_image import D64Image
    print(f"{path}: D64")
    for f in D64Image(path).files():
        extra = f", load ${f.data[0] | f.data[1] << 8:04X}" if f.kind == "PRG" and len(f.data) > 2 else ""
        print(f"  {f.name:16} {f.kind} {f.blocks:3} blocks, {len(f.data)} bytes{extra}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--machine", choices=("c16", "oric"), default="c16")
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()
    for f in args.files:
        suffix = Path(f).suffix.lower()
        if suffix == ".tap":
            describe_tap(f)
        elif suffix == ".d64":
            describe_d64(f)
        else:
            describe_prg(f, args.machine)


if __name__ == "__main__":
    main()
