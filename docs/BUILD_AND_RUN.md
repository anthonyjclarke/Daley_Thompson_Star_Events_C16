# Build and Run

---

## Tools

| Tool          | Used for                                              |
|:--------------|:------------------------------------------------------|
| Python 3.10+  | Every script in `tools/` (standard library only)      |
| cc65          | `da65` to disassemble, `ca65` and `ld65` to rebuild    |
| VICE 3.x      | `xplus4`, as a C16 PAL with 16 KB, for every run      |
| Node.js 20+   | Generating the HTML handbook (`scripts/build_docs.mjs`) |

---

## Make Targets

| Command                    | Does                                                        |
|:---------------------------|:------------------------------------------------------------|
| `make verify`              | Originals unchanged; unpack and tape match; every block rebuilds byte for byte |
| `make disasm`              | Regenerate `src/` from `tools/symbols.py` and compare       |
| `make run-original`        | Original Day One PRG in VICE (`PART=two` for Day Two)       |
| `make run`                 | Rebuilt crunched PRG in VICE                                |
| `make run-unpacked`        | Rebuilt unpacked image, started at its entry                |
| `make docs`                | Regenerate the code reference and the HTML handbook         |
| `make docs-check`          | Fail if the code reference or the HTML is out of date       |
| `make info`                | Describe the original files                                 |
| `make clean`               | Remove `build/`                                             |

To change a name or comment, edit `tools/symbols.py`, run `make disasm`, then `make verify`. Never edit `src/*.s`: it's regenerated.

---

## Scripts

| Script                       | Does                                                     |
|:-----------------------------|:---------------------------------------------------------|
| `tools/run_tape.py SIDE`     | Load a tape side in VICE (`LOAD"",1,1`, PLAY, `SYS1536`) and screenshot the game |
| `tools/shots.py`             | Start-up screenshots of the original, rebuilt crunched and rebuilt unpacked PRGs |
| `tools/doc_shots.py`         | The event screenshots in `docs/images/`                  |
| `tools/flight_probe.py`      | Day Two distances for forced take-offs (`--position`, `--ntsc`) |
| `tools/decode_tunes.py`      | Every tune of both parts as notes and lengths            |
| `tools/exo_check.py EXO`     | Re-crunch the rebuilt game with Exomizer 2.0 and compare with the PRGs |
| `tools/c16_tap.py FILE`      | Decode a C16 TAP file and list its blocks                |
| `tools/tape_check.py`        | Compare the tape files with the unpacked images          |
| `tools/unpack_sfx.py`        | Run a decruncher in a 6502 emulator; `--check` against the dumps |
| `tools/code_reference.py`    | Write `docs/CODE_REFERENCE.md` from `symbols.py`         |

---

## Running from Tape in VICE

VICE's `-autoload` never presses PLAY, so a tape load needs the monitor's `tapectrl 1` after the `LOAD`. `tools/run_tape.py` does it through VICE's remote monitor: it types `LOAD"",1,1`, presses PLAY, waits for the loader at `$0600`, types `SYS1536` and lets the loader load the game. The monitor's memory dump groups bytes in fours with a double space, which the script allows for.

VICE's autostart timing varies from run to run, so screenshots of the original and the rebuild can differ by a frame. Compare what's on screen, not the image hashes.
