# Changelog

---

## [0.8.1] 22-11-2026

### Added

- Graphics, all drawn from the originals by `tools/render_graphics.py`: Day One's screen from its own
  `DrawPackedScreen` and `DrawSceneryRows` (run in `tools/cpu6502.py`), the hurdle and finish-line object block,
  Day Two's title lettering and score digits, and the shot and javelin. The renderer now uses VICE's full TED
  palette, sampled from one screenshot.
- Screenshots of the Day Two title screen and Day One's GAME OVER (`tools/doc_shots.py titles`).
- Worklist: the graphics list is done; new check for the R marker left at GAME OVER.

---

## [0.8.0] 22-11-2026

### Added

- `docs/WORKLIST.md`: what is checked in VICE, what needs a person or real hardware, what is left to check in the
  code, and which graphics the handbook still lacks.
- Graphics: the six advertising boards (`advert_boards_day_two.svg`) and Day Two's athlete frames
  (`athlete_day_two.svg`), from `tools/render_graphics.py`.
- Names: `NextBoardChar`, `BoardStarts`, `BoardColours`, `TopFrameTable`, `BottomFrameTable`, `AthleteCellOffsets`.

### Changed

- The `$0400` data (`ADDS`) is the advertising-board artwork, shown as characters `$80`–`$FF` because TED takes a
  256-character set on a 2 KB boundary; the graphics chapter and memory map now say so.
- Quirk: top frame 9 repeats frame 1 and is never selected.

---

## [0.7.3] 22-11-2026

### Added

- The joystick port: both days read control port 2 only (`$FD` to `$FF08`, fire on bit 7), confirmed with a
  keyboard-driven joystick on each port in VICE. In the player guide, analysis and evidence.

---

## [0.7.2] 22-11-2026

### Added

- Day One's keys, found from a snapshot where keys didn't respond: Day One has no key option, but its joystick read
  also selects keyboard row 1, so A and 4 are left and right and E or SHIFT is fire. Confirmed in VICE; in the
  player guide, analysis, evidence and quirks.

---

## [0.7.1] 22-11-2026

### Changed

- The Day Two keys are confirmed in VICE: J and K select JOY and KEY, and Q, Y and SPACE are left, right and fire.
  The open item on the key mapping is closed.

---

## [0.7.0] 22-11-2026

### Added

- Names for Day Two's flight code: the shot, javelin and long-jump loops and their variables (`ShotY`, `JavelinY`,
  `JavelinPhase`, `InFlight`, `FlightStep`, `FollowThrough`, `RunwayBandColour` and others).
- `tools/flight_probe.py`: forces take-offs in VICE RAM at chosen speeds, angles and positions and reads the
  distances back.

### Changed

- The distance-counter section of `CODEBASE_ANALYSIS.md` and the Day Two tips in `docs/PLAYING.md`, now from
  measured distances.

---

## [0.6.0] 21-11-2026

### Added

- Names for the rest of both main loops: Day One's athlete, track marks, scenery scroll, hurdles, finish line,
  distance, records box, sounds and the 13 raster splits; Day Two's events (`LongJump`, `ShotPut`, `Javelin`),
  take-off angle, runway scroll, distance counter, score line, high score, title and its 13 splits.
- VICE execution-map coverage of three runs: every executed instruction is in the traced code.
- `CODEBASE_ANALYSIS.md` and the chapters `HISTORY_AND_CREDITS`, `PLAYING`, `ARTIFACTS`, `GRAPHICS`,
  `SOURCE_AND_VALIDATION`, `BUILD_AND_RUN`, `HTML_DOCUMENTATION` and the generated `CODE_REFERENCE`.
- The offline handbook `docs/DALEY_THOMPSON.html` (`make docs`, `make docs-check`), with the shared C16 generator
  in `scripts/`.
- `tools/doc_shots.py` (event screenshots), `tools/render_graphics.py` (character sets, athlete frames as SVG)
  and `tools/code_reference.py`.

### Changed

- `$2772` renamed `AngleDigits`: its first two digits are the take-off angle, not the distance.
- Quirks: the race clock runs once a frame, so a displayed second is 1.2 s on PAL; the keys decode to J/K for
  JOY/KEY and Q, Y, SPACE for play (matrix as recalled, not checked in VICE).

---

## [0.5.0] 21-11-2026

### Added

- Part 2 names: input (`InputBits`, `ReadInput`, `ReadKeys`, `InputMode`, `SelectInputMode`), speed (`JoyWaggle_day_two`,
  `SpeedUp_day_two`, `SpeedDecay_day_two`), events and attempts (`EventIndex`, `AttemptNumber`, `AttemptResults`,
  `JudgeAttempt`) and the WORLD RECORD, QUALIFYING LENGTH and BEST tables.
- Evidence for them, including a VICE run of the attempt cycle.
- Open item: an uncalled hex-print routine at `$241D` in part 2.

---

## [0.4.0] 21-11-2026

### Added

- Part 1 race names: `RunSpeed`, `JoyWaggle`, `SpeedUp`, `SpeedDecay`, the speed meter, `StartCountdown` and its texts,
  `RaceClock`, `CheckEventEnd`, `JudgeTime` and `QualifyTimes`, `Score`, `AddScore` and `AwardTimeBonus`.
- Evidence for them, including a controlled VICE run (speed held at maximum) that qualifies every event.
- Quirk: part 1 runs its four events again after the 200 m hurdles.

### Changed

- `Lives`: the qualified path is now observed; the open item for it is closed.

---

## [0.3.0] 21-11-2026

### Added

- Both 1985 tape sides decoded (`tools/c16_tap.py`): KERNAL format, every block's two copies checked.
- `tools/tape_check.py` in `make verify`: the tape's `MAIN` and `ADDS` files equal the unpacked images.
- The `$0600` tape loaders as blocks `loader_side1` and `loader_side2` (`kind="c16tap"` in `tools/disasm.py`).
- `tools/run_tape.py`: loads a side from tape in VICE with `LOAD"",1,1`, PLAY and `SYS1536`.
- Anthony's recollections in `docs/evidence.md`; tape quirks in `docs/quirks.md`.
- Note that the tape images have jitter-free timing, so they were generated by software, not sampled.

### Changed

- `Counter117C` named `Lives` and `EventNumber` confirmed (rung 3) by sampling an unattended run.
- README: the tape is the 1985 form; the PRGs are a later crunched copy of its memory.

---

## [0.2.0] 21-11-2026

### Added

- Unpacked images of both parts (VICE dumps) as originals and blocks `day_one` and `day_two`;
  `tools/unpack_sfx.py` reproduces them by running the decruncher, and `make verify` checks the two agree.
- Both side tapes (`dt_star_events_side1.tap`, `dt_star_events_side2.tap`) in `original/`, hashed.
- Entries for the IRQ handlers, their 13 raster splits, the sound jump tables, part 2's event jump table
  and the code after inline `JSR` parameters; first names for start-up, main loops, IRQ and sound.
- `docs/quirks.md`, `docs/evidence.md` entries, `tools/shots.py` and the stage 5 screenshot sheet.
- `make run-unpacked` and `PART=one|two` for the run targets.

### Changed

- Blocks renamed `day_one_packed` and `day_two_packed`; each block's names live in its own dicts.
- `tools/disasm.py` stops the trace quietly at bytes declared as data.

### Fixed

- Both packed blocks shared the global label at `$100D`, so part 1's entry name was lost.

---

## [0.1.0] 21-11-2026

### Added

- Project created from daley_thompsons_star_events_day_one.prg, daley_thompsons_star_events_day_two.prg with the OldCode_Restoration toolkit;
  first disassembly rebuilds every block byte for byte.
