# Daley Thompson's Star Events

Decomposition of *Daley Thompson's Star Events* for the Commodore 16, which I wrote with my business partner Jason Perkins in 1985 for Ocean Software. It is a conversion of the C64 game, kept as close to it as the C16 allowed. The game comes in two parts, one on each side of the tape: Day One (100 m, 110 m hurdles, 400 m, 200 m hurdles) and Day Two (long jump, shot-put, javelin).

---

## Originals

| File                                    | What it is                                 | Block            |
|:----------------------------------------|:-------------------------------------------|:-----------------|
| `daley_thompsons_star_events_day_one.prg` | Part 1, crunched, `SYS 4109`, $1001–$287B | `day_one_packed` |
| `daley_thompsons_star_events_day_two.prg` | Part 2, crunched, `SYS 4109`, $1001–$2E0F | `day_two_packed` |
| `day_one_unpacked_vice.prg`             | Part 1 unpacked, $0FFE–$3FFF, entry $1010  | `day_one`        |
| `day_two_unpacked_vice.prg`             | Part 2 unpacked, $07FE–$3FFF, entry $2111  | `day_two`        |
| `dt_star_events_side1.tap`              | Side 1 of the 1985 tape: `DALEY1`, `MAIN1`, `ADDS1` | `loader_side1` |
| `dt_star_events_side2.tap`              | Side 2 of the 1985 tape: `DALEY`, `MAIN`, `ADDS`    | `loader_side2` |

The tapes are 2004 tape images (origin unknown) of the 1985 release. Their timing is perfectly regular (every wave exactly 53, 105 or 210 units, with no jitter), so they were generated from the file data by software, not sampled from a cassette: they record the release's files, names and loader, not its audio. Each side is in the C16 KERNAL's own format, with no turbo: a 67-byte loader at `$0600`, which `SYS 1536` starts, LOADs the game's two files and jumps to the game. Every block decodes cleanly (`tools/c16_tap.py`), and `tools/tape_check.py` shows that each file, placed where the loader puts it, is byte for byte the unpacked image. So the tape and the PRGs hold the same game, and the tape keeps the earlier form: the loader, the file names and where each file loads.

The two PRGs are crunched with what looks like Exomizer's self-extracting decruncher: a later conversion of the tape's memory, of unknown origin. They stay as originals too.

The unpacked images were made by starting each PRG in VICE (`xplus4`, C16 PAL, 16 KB), stopping at the decruncher's final `JMP` (`$019D` for part 1, `$01A2` for part 2) and saving the range the decruncher wrote with the monitor's `save` command. `tools/unpack_sfx.py` runs the same decruncher in a 6502 emulator, and `make verify` checks that both ways give the same bytes.

---

## Building

| Command               | Does                                                        |
|:----------------------|:------------------------------------------------------------|
| `make verify`         | Originals unchanged; unpack and tape match; every block rebuilds byte for byte |
| `make disasm`         | Regenerate `src/` from `tools/symbols.py`                   |
| `make run-original`   | Original part 1 in VICE (`PART=two` for part 2)             |
| `make run`            | Rebuilt packed PRG in VICE                                  |
| `make run-unpacked`   | Rebuilt unpacked image, started at its entry                |
| `python3 tools/shots.py` | Scripted start-up screenshots of all three, compared    |
| `python3 tools/run_tape.py 1` | Load a side from tape in VICE (`LOAD`, PLAY, `SYS1536`) and screenshot it |

`docs/evidence.md` holds the proof for each name, and `docs/quirks.md` the original's oddities and the open items.
