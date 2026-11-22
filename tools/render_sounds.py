#!/usr/bin/env python3
"""Render the game's tunes and sound effects to audio files for the handbook.

Run from the project root:   python3 tools/render_sounds.py

Each clip runs the game's own sound code in tools/cpu6502.py: the routine that starts a tune or effect,
then the sound step once per frame (as raster split 7 / 13 calls it), recording TED's sound registers
$FF0E-$FF12 after every frame. A small TED model turns the registers into sound: two square-wave voices
at 1773447 / (16 * (1024 - ((value + 1) & 1023))) Hz (PAL, as tools/ted_pitch.py measures VICE), voice 2
optionally noise, volume 0-8 from $FF11. The footsteps read the BASIC ROM for their pitch, so VICE's Plus/4
BASIC ROM is loaded at $8000 when it can be found.

The model is simple (no filtering, idealised waveforms), so the clips show the notes, rhythm and effects
as the code plays them, not the exact tone of a real TED. Writes docs/sounds/*.m4a (AAC, via macOS
afconvert); keeps the .wav if afconvert is missing.
"""
import math
import random
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from cpu6502 import CPU  # noqa: E402

OUT = ROOT / "docs/sounds"
RATE = 22050
FPS = 1773447 / 35568          # PAL frame rate measured in VICE (cycles per frame)
TED_CLOCK = 1773447 / 16      # PAL; pitch = TED_CLOCK / (1024 - ((value + 1) & 1023))
BASIC_ROMS = ["/opt/homebrew/share/vice/PLUS4/basic-318006-01.bin",
              "/Applications/Vice/VICE.app/Contents/Resources/share/vice/PLUS4/basic-318006-01.bin"]

PARTS = {
    "day_one": dict(prg="original/day_one_unpacked_vice.prg", step=0x22E0, silence=0x2783),
    "day_two": dict(prg="original/day_two_unpacked_vice.prg", step=0x1800, silence=0x1CA2),
}
# (file, part, [(frame, routine), ...], seconds)
CLIPS = [
    ("title_tune", "day_two", [(0, 0x180E)], 40),          # PlayTitleTune: Chariots of Fire
    ("event_fanfare", "day_two", [(0, 0x1806)], 15.5),     # PlayEventTune = Day One's PlayStartTune
    ("qualified_tune", "day_two", [(0, 0x1816)], 5.5),     # PlayQualifiedTune
    ("day_two_effects", "day_two", [(0, 0x181E), (50, 0x1826)], 2.5),   # SoundEffectA, SoundEffectB
    ("day_one_effects", "day_one", [(0, 0x22FE), (60, 0x2306)], 3),     # QUALIFIED, FAILED
    ("footsteps", "day_one", [(f, 0x230E) for f in range(0, 150, 12)], 3),  # PlayFootstep at a run
]


def load(prg):
    data = (ROOT / prg).read_bytes()
    base = data[0] | data[1] << 8
    mem = bytearray(0x10000)
    mem[base:base + len(data) - 2] = data[2:]
    rom = next((Path(p) for p in BASIC_ROMS if Path(p).exists()), None)
    if rom:
        mem[0x8000:0xC000] = rom.read_bytes()[:0x4000]
    return mem


def call(mem, addr):
    cpu = CPU(mem)
    cpu.sp = 0xFD
    cpu.push(0xFF)
    cpu.push(0xFE)       # RTS lands on $FFFF
    cpu.pc = addr
    for _ in range(200_000):
        if cpu.pc == 0xFFFF:
            return
        cpu.step()
    raise SystemExit(f"routine ${addr:04X} did not return")


def registers(part, starts, seconds):
    info = PARTS[part]
    mem = load(info["prg"])
    call(mem, info["silence"])
    frames, todo = [], dict(starts)
    for frame in range(int(seconds * FPS)):
        if frame in todo:
            call(mem, todo[frame])
        call(mem, info["step"])
        frames.append(bytes(mem[0xFF0E:0xFF13]))
    return frames


def synth(frames):
    out, phase, noise, lfsr = [], [0.0, 0.0], 0, 0xFF
    per_frame = RATE / FPS
    for i, (f1lo, f2lo, f2hi, ctrl, f1hi) in enumerate(frames):
        regs = [f1lo | (f1hi & 3) << 8, f2lo | (f2hi & 3) << 8]
        freq = [TED_CLOCK / (1024 - ((r + 1) & 1023)) if r < 0x3FE else 0 for r in regs]
        vol = min(ctrl & 0x0F, 8) / 8 * 0.35
        on = [ctrl & 0x10, ctrl & 0x20, ctrl & 0x40]
        n = int(round((i + 1) * per_frame)) - int(round(i * per_frame))
        for _ in range(n):
            s = 0.0
            for v in (0, 1):
                if freq[v]:
                    prev = phase[v]
                    phase[v] = (phase[v] + freq[v] / RATE) % 1.0
                    if v == 1 and phase[v] < prev:          # noise steps once a cycle of voice 2
                        lfsr = ((lfsr << 1) | (((lfsr >> 7) ^ (lfsr >> 5) ^ (lfsr >> 4) ^ (lfsr >> 3)) & 1)) & 0xFF
                        noise = lfsr & 1
            if on[0] and freq[0]:
                s += vol if phase[0] < 0.5 else -vol
            if on[1] and freq[1]:
                s += vol if phase[1] < 0.5 else -vol
            elif on[2] and freq[1]:
                s += vol if noise else -vol
            out.append(max(-1.0, min(1.0, s)))
    # trim trailing silence, keep a short tail
    last = max((k for k, x in enumerate(out) if x), default=0)
    return out[:min(len(out), last + RATE // 4)]


def write_wav(path, samples):
    with open(path, "wb") as f:
        data = b"".join(struct.pack("<h", int(x * 32767)) for x in samples)
        f.write(b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVEfmt " +
                struct.pack("<IHHIIHH", 16, 1, 1, RATE, RATE * 2, 2, 16) + b"data" + struct.pack("<I", len(data)) + data)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    encoder = shutil.which("afconvert")
    with tempfile.TemporaryDirectory() as td:
        for name, part, starts, seconds in CLIPS:
            samples = synth(registers(part, starts, seconds))
            wav = Path(td) / f"{name}.wav"
            write_wav(wav, samples)
            if encoder:
                dst = OUT / f"{name}.m4a"
                subprocess.run([encoder, "-f", "m4af", "-d", "aac", "-b", "48000", str(wav), str(dst)], check=True)
            else:
                dst = OUT / f"{name}.wav"
                shutil.copy(wav, dst)
            print(f"{dst.relative_to(ROOT)}: {len(samples) / RATE:.1f} s, {dst.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
