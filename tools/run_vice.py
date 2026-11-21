#!/usr/bin/env python3
"""Start a C16 or Plus/4 PRG in VICE xplus4.

Usage:
  run_vice.py FILE.prg                     autostart (for a PRG with a BASIC SYS stub)
  run_vice.py FILE.prg --entry 1800        load at the PRG's own address, then jump (no stub)
  run_vice.py FILE.prg --model plus4pal --ram 64

Uses the launch the C16 repos use: a fresh default configuration (-default +saveres), a C16 PAL with
16 KB unless told otherwise, and monitor commands for --entry. Logs go to build/vice/.
"""
import argparse
import shutil
import subprocess
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("prg", type=Path)
    ap.add_argument("--entry", help="hex address to jump to after loading (skips autostart)")
    ap.add_argument("--model", default="c16pal", help="xplus4 -model value (c16pal, plus4pal, …)")
    ap.add_argument("--ram", default="16", help="RAM size in KB (16, 32, 64)")
    ap.add_argument("--monitor", action="store_true", help="open the VICE monitor at start")
    args = ap.parse_args()

    xplus4 = shutil.which("xplus4")
    if not xplus4:
        raise SystemExit("xplus4 not found: install VICE (brew install vice)")
    prg = args.prg.resolve(strict=True)
    logs = Path("build/vice")
    logs.mkdir(parents=True, exist_ok=True)
    cmd = [xplus4, "-default", "+saveres", "-model", args.model, "-ramsize", args.ram,
           "-logfile", str(logs / "vice.log")]
    if args.entry:
        mon = logs / "start.mon"
        mon.write_text(f'load "{prg.as_posix()}" 0\n' + ("" if args.monitor else f"g {int(args.entry, 16):x}\n"))
        cmd += ["-initbreak", "ready", "-moncommands", str(mon)]
    else:
        cmd += ["-autostart", str(prg)]
        if args.monitor:
            cmd += ["-initbreak", "ready"]
    with (logs / "console.log").open("w") as log:
        p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    print(f"VICE started (PID {p.pid}): {prg}")


if __name__ == "__main__":
    main()
