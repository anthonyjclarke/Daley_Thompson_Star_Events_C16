#!/usr/bin/env python3
"""Load a side tape in VICE as the loading slip says (LOAD "",1,1 then SYS 1536) and screenshot the game.

Run from the project root:   python3 tools/run_tape.py SIDE [SECONDS_AFTER_START]

Starts xplus4 (C16 PAL, 16 KB, warp) with the tape attached and, through the remote monitor, types
LOAD"",1,1 and presses PLAY (tapectrl 1). When the loader is at $0600 it types SYS1536, as the
loading slip says, and the loader LOADs the two game files from the same tape. It breaks at the game's entry, lets the game run for SECONDS_AFTER_START (wall clock, warp), saves
build/shots/tape_sideN.png and quits VICE. A scripted start, not a play-through.
"""
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRY = {"1": 0x1010, "2": 0x2111}
LOADER_START = "a9 08 a0 00 a2 01"  # LDA #$08 / LDY #$00 / LDX #$01 at $0600


class Monitor:
    def __init__(self, port=6510):
        for _ in range(60):
            try:
                self.s = socket.create_connection(("127.0.0.1", port), timeout=2)
                break
            except OSError:
                time.sleep(0.5)
        else:
            raise SystemExit("could not reach the VICE remote monitor")
        self.s.settimeout(0.3)

    def read(self, wait):
        buf, end = b"", time.time() + wait
        while time.time() < end:
            try:
                chunk = self.s.recv(65536)
                if not chunk:
                    break
                buf += chunk
            except socket.timeout:
                pass
        return buf.decode(errors="replace")

    def send(self, text, wait=0.5):
        self.s.sendall(text.encode() + b"\n")
        return self.read(wait)


def main():
    side = sys.argv[1]
    after = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
    tap = ROOT / f"original/dt_star_events_side{side}.tap"
    out = ROOT / f"build/shots/tape_side{side}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    vice = subprocess.Popen([shutil.which("xplus4"), "-default", "+saveres", "-model", "c16pal", "-ramsize", "16",
                             "-warp", "+sound", "-remotemonitor", "-remotemonitoraddress", "ip4://127.0.0.1:6510",
                             "-1", str(tap)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    mon = Monitor()
    t0 = time.time()
    try:
        time.sleep(3)
        mon.send(r'keybuf load"",1,1\n')
        mon.send("x", 0.1)
        time.sleep(1)
        mon.send("tapectrl 1")
        mon.send("x", 0.1)
        while True:  # loader in memory, then give the KERNAL time to finish the LOAD and print READY
            time.sleep(2)
            mem = " ".join(mon.send("m 0600 0605").lower().split())  # VICE groups bytes in fours
            mon.send("x", 0.1)
            if LOADER_START in mem:
                break
            if time.time() - t0 > 400:
                raise SystemExit("loader never arrived at $0600")
        time.sleep(3)
        print(f"loader at $0600 after {time.time() - t0:.0f}s (warp)")
        mon.send(f"break exec {ENTRY[side]:04x}")
        mon.send(r"keybuf sys1536\n")
        mon.send("x", 0.1)
        t1, text = time.time(), ""
        while "stop on" not in text.lower():
            text += mon.read(2)
            if time.time() - t1 > 600:
                raise SystemExit("game entry never reached")
        print(f"entry ${ENTRY[side]:04X} reached {time.time() - t1:.0f}s after SYS 1536 (warp)")
        mon.send("del")
        mon.send("x", 0.1)
        time.sleep(after)
        mon.send(f'screenshot "{out}" 2', 2)
        print(f"screenshot: {out.relative_to(ROOT) if out.exists() else 'not saved'}")
    finally:
        try:
            mon.send("quit", 0.3)
        except OSError:
            pass
        try:
            vice.wait(timeout=10)
        except subprocess.TimeoutExpired:
            vice.kill()


if __name__ == "__main__":
    main()
