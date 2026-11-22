#!/usr/bin/env python3
"""Measure TED's tone pitch in VICE on a PAL and an NTSC C16, and score the game's note table against it.

Run from the project root:   python3 tools/ted_pitch.py

For each model, VICE starts at the BASIC prompt with its remote monitor open and records its sound output
to build/ted_pitch_<model>.wav (VICE's "wav" recording device; the playback device must be a real one, so
the tones are audible). The monitor sets voice 2 to each register value in VALUES ($FF0F, $FF10, then
$FF11 = $28: voice 2 on, volume 8), lets it sound for two seconds and silences it. Each tone's frequency
is timed from its rising crossings of the mean and compared with clock / (16 * (1024 - ((w + 1) & 1023))).
The high values separate that formula from clock / (16 * (1024 - w)): at $3F0 they differ by 6%.

The note table (NoteFreqLo / NoteFreqHi, part 1 at $2B71 / $2B94) is then scored in cents against equal
temperament from A2 = 110 Hz under each clock. VICE's TED model only, not a real machine.
"""
import math
import shutil
import struct
import subprocess
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from run_tape import Monitor  # noqa: E402

VALUES = [0x007, 0x100, 0x200, 0x300, 0x3C0, 0x3E0, 0x3F0]
CLOCKS = {"c16pal": 1773447, "c16ntsc": 1789773}
TONE, GAP = 2.0, 0.6


def ted_hz(w, clock):
    return clock / (16 * (1024 - ((w + 1) & 1023)))


def record(model):
    wav = ROOT / "build" / f"ted_pitch_{model}.wav"
    wav.parent.mkdir(exist_ok=True)
    wav.unlink(missing_ok=True)
    vice = subprocess.Popen([shutil.which("xplus4"), "-default", "+saveres", "-model", model, "-ramsize", "16",
                             "-sound", "-sounddev", "coreaudio", "-soundrate", "44100",
                             "-soundrecdev", "wav", "-soundrecarg", str(wav),
                             "-remotemonitor", "-remotemonitoraddress", "ip4://127.0.0.1:6510"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    mon = Monitor()
    try:
        time.sleep(5)
        for v in VALUES:
            mon.send(f"> ff0f {v & 0xFF:02x}", 0.2)
            mon.send(f"> ff10 {v >> 8:02x}", 0.2)
            mon.send("> ff11 28", 0.2)
            mon.send("x", 0.1)
            time.sleep(TONE)
            mon.send("> ff11 00", 0.2)
            mon.send("x", 0.1)
            time.sleep(GAP)
        mon.send("quit", 0.5)
    finally:
        time.sleep(1)
        vice.terminate()
        vice.wait(5)
    return wav


def tones(path):
    """Yield the frequency of each sounding stretch of the recording."""
    with wave.open(str(path)) as w:
        rate, ch = w.getframerate(), w.getnchannels()
        raw = w.readframes(w.getnframes())
    s = struct.unpack(f"<{len(raw) // 2}h", raw)[::ch]
    win = rate // 100
    active = [max(s[i:i + win]) - min(s[i:i + win]) > 2000 for i in range(0, len(s) - win, win)] + [False]
    start = None
    for k, a in enumerate(active):
        if a and start is None:
            start = k
        elif not a and start is not None:
            if k - start > 50:
                a0, b0 = start * win, k * win
                m = (b0 - a0) // 10
                x = s[a0 + m:b0 - m]
                mid = sum(x) / len(x)
                ups = [i + (mid - x[i]) / (x[i + 1] - x[i]) for i in range(len(x) - 1) if x[i] < mid <= x[i + 1]]
                yield (len(ups) - 1) * rate / (ups[-1] - ups[0])
            start = None


def main():
    for model, clock in CLOCKS.items():
        print(f"{model} (clock {clock} Hz)")
        for v, f in zip(VALUES, tones(record(model))):
            plain = clock / (16 * (1024 - v))
            print(f"  ${v:03X}  measured {f:8.2f} Hz   (w+1) formula {ted_hz(v, clock):8.2f}   w formula {plain:8.2f}")
    data = (ROOT / "original/day_one_unpacked_vice.prg").read_bytes()
    base, mem = data[0] | data[1] << 8, data[2:]
    table = [mem[0x2B71 - base + i] | (mem[0x2B94 - base + i] & 3) << 8 for i in range(35)]
    for model, clock in CLOCKS.items():
        cents = [1200 * math.log2(ted_hz(w, clock) / (110 * 2 ** (i / 12))) for i, w in enumerate(table)]
        print(f"note table on {model}: mean {sum(cents) / 35:+.1f} cents, {min(cents):+.1f} to {max(cents):+.1f}")


if __name__ == "__main__":
    main()
