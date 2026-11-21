#!/usr/bin/env python3
"""Screenshots of every event for the documentation, from the original PRGs in VICE.

Run from the project root:   python3 tools/doc_shots.py

Part 1: runs with SpeedDecay patched to RTS in RAM and RunSpeed set to $70 once each race starts, so
every event qualifies and the next one follows; a shot is taken in each event once its distance passes
20 m. Part 2: removes the FIRE TO START wait in RAM, sets EventIndex at StartEvent_day_two ($244B) and
takes a shot of each event's screen. The patches change RAM in VICE only, never the build. Writes
docs/images/event_*.png.
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

OUT = ROOT / "docs/images"
PART1_EVENTS = {1: "event_100m", 2: "event_110m_hurdles", 3: "event_400m", 4: "event_200m_hurdles"}
PART2_EVENTS = {0: "event_long_jump", 1: "event_shot_put", 2: "event_javelin"}


def start(prg):
    vice = subprocess.Popen([shutil.which("xplus4"), "-default", "+saveres", "-model", "c16pal", "-ramsize", "16",
                             "-warp", "+sound", "-remotemonitor", "-remotemonitoraddress", "ip4://127.0.0.1:6510",
                             "-autostart", str(ROOT / prg)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return vice, Monitor()


def stop(vice, mon):
    try:
        mon.send("quit", 0.3)
    except OSError:
        pass
    try:
        vice.wait(timeout=10)
    except subprocess.TimeoutExpired:
        vice.kill()


def mem(mon, a, b):
    out, bs = mon.send(f"m {a:04x} {b:04x}", 0.4), []
    for line in out.splitlines():
        m = re.search(r">C:[0-9a-f]{4}\s+((?:[0-9a-f]{2}\s+)+)", line)
        if m:
            bs += [int(x, 16) for x in m.group(1).split()]
    return bs[:b - a + 1]


def shot(mon, name):
    path = OUT / f"{name}.png"
    path.unlink(missing_ok=True)
    mon.send(f'screenshot "{path}" 2', 2)
    print(f"{name}: {'saved' if path.exists() else 'not saved'}")


def part1():
    vice, mon = start("original/daley_thompsons_star_events_day_one.prg")
    todo, t0 = dict(PART1_EVENTS), time.time()
    try:
        while todo and time.time() - t0 < 120:
            time.sleep(0.3)
            running, event = mem(mon, 0x169D, 0x169D), mem(mon, 0x1121, 0x1121)
            if running == [1]:
                mon.send("> 1996 60", 0.1)
                mon.send("> 1987 70", 0.1)
                dist = bytes(mem(mon, 0x0FD0, 0x0FD3)).decode("latin1")
                if event and event[0] in todo and dist.isdigit() and int(dist) >= 20:
                    shot(mon, todo.pop(event[0]))
            mon.send("x", 0.05)
    finally:
        stop(vice, mon)


def part2():
    for index, name in PART2_EVENTS.items():
        vice, mon = start("original/daley_thompsons_star_events_day_two.prg")
        try:
            time.sleep(4)
            mon.send("> 25d0 00", 0.2)  # fall through the FIRE TO START wait
            mon.send("break exec 244b", 0.2)
            mon.send("x", 0.1)
            text, t1 = "", time.time()
            while "stop on" not in text.lower() and time.time() - t1 < 60:
                text += mon.read(1)
            mon.send(f"> 42 {index:02x}", 0.2)
            mon.send("del", 0.2)
            mon.send("x", 0.1)
            time.sleep(3)
            shot(mon, name)
        finally:
            stop(vice, mon)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    part1()
    part2()
