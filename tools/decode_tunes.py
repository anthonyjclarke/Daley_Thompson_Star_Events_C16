#!/usr/bin/env python3
"""Decode the tunes of both parts into notes and lengths, by following the tune player's own rules.

Run from the project root:   python3 tools/decode_tunes.py [--markdown]

The player (part 1 $2900-$2ADC, part 2 the same code $AE2 lower) reads each voice as byte pairs:
  $00-$2F note: index into the frequency tables (lo, hi); the next byte picks a length from LengthTable
  $30     rest, with a length byte like a note
  $FF     end of the voice (only at call depth 0)
  $FE     return from a call
  $FD     word: copy 23 bytes of instrument to the voice's effect record
  $FC     word: copy 12 bytes (the start of the record)
  $FB     word: copy 9 bytes to record offsets $0E-$16
  $FA     word: copy 16 bytes to the length table (record offsets $1A-$29)
  other   voice 1: call the word; voice 2: $F9 calls, the rest jump (goto)
Lengths count calls of the player, one a frame. TED pitch: 111860.78 / (1024 - value) Hz on PAL; note 0
($007) gives 110.0 Hz, A2, and the 35 entries rise a semitone each to G5.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAMES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def note_name(i):
    return f"{NAMES[i % 12]}{2 + (i + 9) // 12}"


PARTS = {
    "day_one": dict(prg="original/day_one_unpacked_vice.prg", shift=0,
                    tunes=[("Start (each race)", 0x2523, 0x258F), ("GAME OVER", 0x2405, 0x24B6),
                           ("Unused ($22F6)", 0x25E5, 0x2621)]),
    "day_two": dict(prg="original/day_two_unpacked_vice.prg", shift=0xAE2,
                    tunes=[("Title (FIRE TO START)", 0x1925, 0x19D6), ("Event", 0x1A43, 0x1AAF),
                           ("Qualified", 0x1B05, 0x1B41)]),
}


def load(prg):
    data = (ROOT / prg).read_bytes()
    base = data[0] | data[1] << 8
    mem = bytearray(0x10000)
    mem[base:base + len(data) - 2] = data[2:]
    return mem


def decode_voice(mem, shift, start, voice):
    freq_lo, freq_hi = 0x2B71 - shift, 0x2B94 - shift
    lengths = list(mem[0x2AF7 - shift:0x2B07 - shift]) if voice == 1 else list(mem[0x2B41 - shift:0x2B51 - shift])
    ptr, stack, events, seen = start, [], [], set()
    for _ in range(2000):
        b = mem[ptr]
        if b <= 0x30:
            ln = lengths[mem[ptr + 1] - 1] if 1 <= mem[ptr + 1] <= 16 else None
            if b == 0x30:
                events.append(("rest", ln))
            else:
                value = mem[freq_lo + b] | mem[freq_hi + b] << 8
                events.append((note_name(b), ln, round(111860.78 / (1024 - value), 1)))
            ptr += 2
        elif b == 0xFF:
            events.append(("end",) if not stack else ("end inside a call: BRK",))
            break
        elif b == 0xFE:
            if not stack:
                events.append(("return at depth 0: BRK",))
                break
            ptr = stack.pop()
        else:
            word = mem[ptr + 1] | mem[ptr + 2] << 8
            if b == 0xFA:
                lengths = list(mem[word:word + 16])
                events.append(("lengths", word, lengths))
                ptr += 3
            elif b in (0xFB, 0xFC, 0xFD):
                events.append(("instrument", b, word))
                ptr += 3
            elif voice == 1 or b == 0xF9:
                stack.append(ptr + 3)
                ptr = word
            else:
                if word in seen:
                    events.append(("repeat", word))
                    break
                seen.add(word)
                ptr = word
    return events


def summary(events):
    notes = [e for e in events if e[0] not in ("rest", "lengths", "instrument", "end", "repeat")
             and not e[0].startswith(("end", "return"))]
    frames = sum(e[1] or 0 for e in events if len(e) > 1 and isinstance(e[1], int) and e[0] not in
                 ("lengths", "instrument", "repeat"))
    return notes, frames


def main():
    md = "--markdown" in sys.argv
    for part, info in PARTS.items():
        mem = load(info["prg"])
        for title, v1, v2 in info["tunes"]:
            print(f"\n{part}: {title}" if not md else f"\n### {title} ({part})\n")
            for voice, start in ((1, v1), (2, v2)):
                events = decode_voice(mem, info["shift"], start, voice)
                notes, frames = summary(events)
                low = min(notes, key=lambda e: e[2])[0] if notes else "-"
                high = max(notes, key=lambda e: e[2])[0] if notes else "-"
                tail = events[-1][0]
                line = " ".join(f"{e[0]}/{e[1]}" if e[0] not in ("lengths", "instrument", "repeat") and len(e) > 1
                                else (f"[instr ${e[2]:04X}]" if e[0] == "instrument" else
                                      f"[lengths ${e[1]:04X}]" if e[0] == "lengths" else
                                      f"[repeat ${e[1]:04X}]" if e[0] == "repeat" else f"[{e[0]}]")
                                for e in events)
                print(f"  voice {voice} at ${start:04X}: {len(notes)} notes, {frames} frames "
                      f"({frames / 50:.1f} s PAL), {low}–{high}, ends: {tail}")
                print(f"    {line}")


if __name__ == "__main__":
    main()
