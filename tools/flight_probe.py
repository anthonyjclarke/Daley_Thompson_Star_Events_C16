#!/usr/bin/env python3
"""Measure Day Two's distances in VICE for chosen take-off speeds, angles and positions.

Run from the project root:   python3 tools/flight_probe.py [--position] [event ...]   (0 long jump, 1 shot-put, 2 javelin)

The monitor can't press fire, so each attempt is forced in RAM: at the run-up wait ($24D9) the probe
sets RunSpeed_day_two, AthleteX and the athlete's column as a full run-up leaves them and jumps to the
take-off ($24EE); at the angle check ($2506) it sets Angle and jumps past the angle loop ($2EF4). The
event's own flight code then runs unchanged, and the distance is read when judging ends ($32FC). The
FIRE TO START wait is skipped with $25D0 = 0 and the event is held at StartEvent_day_two ($244B).
VICE RAM only; the build is untouched. Prints one line per attempt. With --position, varies AthleteX at
speed $1F and 45 degrees instead of the speed and angle grid.
"""
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from run_tape import Monitor  # noqa: E402

SPEEDS = [0x08, 0x10, 0x18, 0x1C, 0x1D, 0x1E, 0x1F]
ANGLES = [25, 35, 45, 55, 59, 60, 66, 67, 75]
ATHLETE_X = 0x50          # at the line: TakeOffDelay = $50 / 4 - $13 = 1
COLUMN = 0x0E             # AthleteCol after a full run-up (SpeedUp stops moving it at $0E)
POSITIONS = [0x50, 0x60, 0x70, 0x80, 0x90, 0x9B]
START_X = {1: 0x03, 2: 0x01}  # shot / javelin column before the run-up (InitAthlete_day_two)


def mem(mon, a, b):
    out, bs = mon.send(f"m {a:04x} {b:04x}", 0.3), []
    for line in out.splitlines():
        m = re.search(r">C:[0-9a-f]{4}\s+((?:[0-9a-f]{2}\s+)+)", line)
        if m:
            bs += [int(x, 16) for x in m.group(1).split()]
    return bs[:b - a + 1]


def wait_stop(mon, text="", limit=90):
    t0 = time.time()
    while time.time() - t0 < limit:
        text += mon.read(0.3)
        m = re.search(r"\(Stop on\s+exec ([0-9a-f]{4})\)", text, re.I)
        if m:
            return int(m.group(1), 16)
    raise SystemExit("no breakpoint within the time limit")


def probe(event, cases):
    vice = subprocess.Popen([shutil.which("xplus4"), "-default", "+saveres", "-model", "c16pal", "-ramsize", "16",
                             "-warp", "+sound", "-remotemonitor", "-remotemonitoraddress", "ip4://127.0.0.1:6510",
                             "-autostart", str(ROOT / "original/daley_thompsons_star_events_day_two.prg")],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    mon, results = Monitor(), []
    try:
        time.sleep(4)
        mon.send("> 25d0 00", 0.2)
        for addr in ("244b", "24d9", "2506", "32fc"):
            mon.send(f"break exec {addr}", 0.2)
        pending = mon.send("x", 0.1)
        todo = list(cases)
        while todo:
            pc = wait_stop(mon, pending)
            speed, angle, athlete_x = (todo[0] + (ATHLETE_X,))[:3]
            if pc == 0x244B:
                mon.send(f"> 42 {event:02x}", 0.1)
            elif pc == 0x24D9:
                pokes = [f"> 37 {speed:02x}", f"> 4c {athlete_x:02x}",
                         f"> 38 {COLUMN:02x}", f"> 5c {COLUMN:02x}", f"> 5e {COLUMN:02x}"]
                if event in START_X:
                    x = START_X[event] + COLUMN - 2
                    pokes += [f"> 6f {x:02x}", f"> 71 {x:02x}", f"> 68 {x:02x}", f"> 6a {x:02x}"]
                for p in pokes:
                    mon.send(p, 0.05)
                mon.send("r pc = 24ee", 0.1)
            elif pc == 0x2506:
                bcd = int(str(angle), 16)
                mon.send(f"> 66 {angle:02x}", 0.05)
                mon.send(f"> 65 {bcd:02x}", 0.05)
                mon.send(f"> 2772 {ord(str(angle)[0]):02x} {ord(str(angle)[1]):02x}", 0.05)
                mon.send("r pc = 2ef4", 0.1)
            elif pc == 0x32FC:
                dist = bytes(mem(mon, 0x2774, 0x2778)).decode("latin1")
                metres = f"{dist[:3].lstrip('0') or '0'}.{dist[3:]}"
                results.append((event, speed, angle, athlete_x, metres))
                print(f"event {event}  speed ${speed:02X}  angle {angle:2d}  AthleteX ${athlete_x:02X}  "
                      f"distance {metres} m", flush=True)
                todo.pop(0)
            pending = mon.send("x", 0.05)
    finally:
        try:
            mon.send("quit", 0.3)
        except OSError:
            pass
        try:
            vice.wait(timeout=10)
        except subprocess.TimeoutExpired:
            vice.kill()
    return results


def main():
    args = [a for a in sys.argv[1:] if a != "--position"]
    events = [int(a) for a in args] or [0, 1, 2]
    for event in events:
        if "--position" in sys.argv:
            probe(event, [(0x1F, 45, x) for x in POSITIONS])
        else:
            probe(event, [(s, a) for a in ANGLES for s in SPEEDS])


if __name__ == "__main__":
    main()
