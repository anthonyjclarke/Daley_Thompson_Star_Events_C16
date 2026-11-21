# Source and Validation

How the disassembly is made, what proves it matches the original, and how the names are kept honest.

---

## No Source Survives

Anthony and Jason wrote the game on a C64 and loaded the result onto a C16; no source disk survives. The source in `src/` is therefore a disassembly, regenerated from the original binaries by `tools/disasm.py` with cc65's `da65`, under the names and comments in `tools/symbols.py`. `symbols.py` is the master: `src/*.s` is never edited by hand.

| Block            | From                                       | Range           |
|:-----------------|:-------------------------------------------|:----------------|
| `day_one_packed` | `daley_thompsons_star_events_day_one.prg`  | `$1001`–`$287B` |
| `day_two_packed` | `daley_thompsons_star_events_day_two.prg`  | `$1001`–`$2E0F` |
| `loader_side1`   | `dt_star_events_side1.tap`, file 1         | `$0600`–`$0642` |
| `loader_side2`   | `dt_star_events_side2.tap`, file 1         | `$0600`–`$0642` |
| `day_one`        | `day_one_unpacked_vice.prg`                | `$0FFE`–`$3FFF` |
| `day_two`        | `day_two_unpacked_vice.prg`                | `$07FE`–`$3FFF` |

The two packed blocks cover the decrunchers; their game data stays as bytes. The unpacked blocks are where the game is.

---

## The Gate: `make verify`

Every change has to pass `make verify`, which checks four things in turn:

1. The originals are unchanged (`shasum -c original/SHA256SUMS`).
2. Running each decruncher in a 6502 emulator (`tools/unpack_sfx.py`) gives exactly the unpacked images, which were dumped from VICE at the decruncher's final `JMP`. Two independent methods, one result.
3. Every game file on both tapes, placed where the loader puts it, equals the unpacked image (`tools/tape_check.py`).
4. Every block, reassembled from `src/` with `ca65` and `ld65`, is byte-identical to its original (`tools/disasm.py --check`).

One more check runs by hand, because it needs an old Exomizer: `tools/exo_check.py` re-crunches the images rebuilt from `src/` with Exomizer 2.0 (2.0beta7–2.0.9) and gets both crunched PRGs byte for byte (see [the artifacts](ARTIFACTS.md)).

Original bugs and oddities stay in the build; they are recorded in [the quirks](quirks.md) instead of being fixed.

---

## Finding the Code

`da65` needs to know which bytes are code. `disasm.py` traces from each block's entry points, following branches, `JSR` and `JMP`, and stops at bytes declared as data. The entry points beyond the start address come from the code itself:

- **Raster splits.** The 13 split handlers in each part, read from the tables the IRQ handler patches its `JSR` from.
- **The event jump.** Day Two's three event handlers, from the table its self-modified `JMP` at `$2F11` reads.
- **Inline parameters.** The code after each `JSR PlayTunePair` call: the call is followed by two data words, and the `RTS` after them is code.

About 40% of Day One and 36% of Day Two trace as code; the rest is character sets, screens, tunes and tables.

**Coverage check.** VICE's execution map recorded which addresses ran during three runs of the original. Every executed instruction falls on an instruction start of the traced code, so the trace is missing nothing those runs reached. Details are in [the evidence](evidence.md).

---

## Names and Evidence

Names follow the evidence ladder from the restoration skill:

| Rung | Evidence                               | Allows                          |
|:-----|:---------------------------------------|:--------------------------------|
| 1    | Seen in the code                       | Descriptive names               |
| 2    | Seen running (screen, sample, trace)   | It runs, how often, from where  |
| 3    | Behaves as predicted in a controlled run | Role names: `Lives`, `RunSpeed` |
| 4    | Confirmed by Anthony                   | What a sprite, sound or mode is |

Each role-claiming name has a row in [the evidence](evidence.md) with what was seen and when. The source comment states the conclusion; the proof lives in the evidence. Names still at `Lxxxx` are neutral: nothing yet justifies a role.

The controlled runs change RAM in VICE only, never the build. For example, `SpeedDecay` is patched to `RTS` to hold `RunSpeed` at its maximum, and Day Two's FIRE TO START wait is removed so attempts run without input. `tools/doc_shots.py` reproduces the screenshots used in these documents the same way. `tools/flight_probe.py` forces Day Two take-offs: it sets the speed, position and angle at two breakpoints, lets the event's flight code run, and reads the distance.

---

## Not Yet Done

Manual play, sound and real hardware haven't been tested. Everything here comes from the code and from VICE. The open questions are listed in [the quirks](quirks.md#open-items), and what still needs testing in [the worklist](WORKLIST.md).
