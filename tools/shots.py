#!/usr/bin/env python3
"""Scripted VICE screenshots of the original and rebuilt PRGs, for stage 5 (no input: start-up only).

Run from the project root:   python3 tools/shots.py [CYCLES ...]

For each part, starts the original packed PRG, the rebuilt packed PRG (autostart) and the rebuilt
unpacked image (loaded by the monitor, jump to the entry), lets each run CYCLES CPU cycles in warp,
saves a PNG in build/shots/ and reports whether the screenshots of the three match. A matching
screenshot shows the same start-up, not that the game plays the same.
"""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "build" / "shots"
RUNS = {
    "one": [("original", "original/daley_thompsons_star_events_day_one.prg", None),
            ("rebuilt", "build/day_one_packed.prg", None),
            ("unpacked", "build/day_one.prg", 0x1010)],
    "two": [("original", "original/daley_thompsons_star_events_day_two.prg", None),
            ("rebuilt", "build/day_two_packed.prg", None),
            ("unpacked", "build/day_two.prg", 0x2111)],
}


def shot(prg, entry, cycles, out):
    cmd = [shutil.which("xplus4"), "-default", "+saveres", "-model", "c16pal", "-ramsize", "16", "-warp", "+sound",
           "-limitcycles", str(cycles), "-exitscreenshot", str(out)]
    if entry is None:
        cmd += ["-autostart", str(ROOT / prg)]
    else:
        mon = SHOTS / f"{out.stem}.mon"
        mon.write_text(f'load "{(ROOT / prg).as_posix()}" 0\ng {entry:x}\n')
        cmd += ["-initbreak", "ready", "-moncommands", str(mon)]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    return hashlib.sha256(out.read_bytes()).hexdigest()[:12] if out.exists() else "none"


def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    cycles = [int(c) for c in sys.argv[1:]] or [20_000_000]
    for part, runs in RUNS.items():
        for cyc in cycles:
            hashes = {name: shot(prg, entry, cyc, SHOTS / f"day_{part}_{name}_{cyc // 1_000_000}M.png")
                      for name, prg, entry in runs}
            print(f"day_{part} at {cyc // 1_000_000}M cycles: " + ", ".join(f"{k} {v}" for k, v in hashes.items()))


if __name__ == "__main__":
    main()
