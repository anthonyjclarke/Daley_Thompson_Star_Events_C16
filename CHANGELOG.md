# Changelog

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
