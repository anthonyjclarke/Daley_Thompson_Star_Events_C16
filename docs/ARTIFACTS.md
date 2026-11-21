# Artifacts

What survives of the 1985 release, what each file is, and how the files relate. The originals live in `original/`, read-only, with their SHA-256 hashes in `original/SHA256SUMS`; `make verify` checks them first.

---

## The Originals

| File                                      | Size      | SHA-256 (start)    |
|:------------------------------------------|:----------|:-------------------|
| `dt_star_events_side1.tap`                | 620,778   | `3b813b1e3196a2f2` |
| `dt_star_events_side2.tap`                | 662,707   | `54f04c3b20e55727` |
| `daley_thompsons_star_events_day_one.prg` | 6,269     | `2c96ffea6fc42dbe` |
| `daley_thompsons_star_events_day_two.prg` | 7,697     | `f52acec3ff49a422` |
| `day_one_unpacked_vice.prg`               | 12,292    | `175f57575a143316` |
| `day_two_unpacked_vice.prg`               | 14,340    | `006b2048ec2eaefd` |

The two tapes are the earliest form: images of the two sides of the 1985 cassette. The two crunched PRGs are a later conversion of the same game into single files, of unknown origin. The two unpacked images were made for this project from the crunched PRGs (see [validation](SOURCE_AND_VALIDATION.md)).

`Original Assets/` holds the cassette and C64 title-screen pictures, Ocean's 1985 advert, the cassette inlay and the revised loading instructions, as PDFs.

---

## The Tapes

Each side is in the C16 KERNAL's own tape format, with no turbo loader. `tools/c16_tap.py` decodes them: each value in the TAP file is one full wave in units of 8 CPU cycles. A long and a medium wave mark each byte, a short and a medium make a 0 bit, a medium and a short make a 1 bit, eight bits go least significant first with an odd parity bit, and each block is written twice after a countdown (`$89`…`$81` for the first copy, `$09`…`$01` for the second) and ends with an XOR checksum.

| Side | File     | Type | Header range      | Bytes  | Loaded at |
|:-----|:---------|:-----|:------------------|:-------|:----------|
| 1    | `DALEY1` | 1    | `$0600`–`$0642`   | 67     | `$0600`   |
| 1    | `MAIN1`  | 1    | `$1000`–`$2FFE`   | 8,191  | `$1000`   |
| 1    | `ADDS1`  | 1    | `$3000`–`$3FFE`   | 4,095  | `$3000`   |
| 2    | `DALEY`  | 1    | `$0600`–`$0642`   | 67     | `$0600`   |
| 2    | `MAIN`   | 1    | `$1000`–`$3FFE`   | 12,287 | `$1000`   |
| 2    | `ADDS`   | 1    | `$1400`–`$17FF`   | 1,024  | `$0800`   |

Every block on both sides decodes cleanly: both copies pass their checksums and agree, with no parity errors.

**The timing is synthetic.** All but six waves per side are exactly 53, 105 or 210 units long. A cassette sampled by a real tape interface always wobbles, so these 2004 files were generated from the file data by software. They record the release's files, names and loader, but not the audio of a real tape.

**The loader.** `DALEY1` / `DALEY` is a 67-byte program at `$0600`, started by `SYS 1536` as the loading instructions say. It calls the KERNAL's `SETLFS`, `SETNAM` and `LOAD` for each game file with secondary address 0, which makes `LOAD` use the loader's own address rather than the file's header. That is why side 2's `ADDS`, saved from `$1400`, lands at `$0800`. It then jumps to the game: `$1010` on side 1, `$2111` on side 2. The loaders are the blocks `loader_side1` and `loader_side2` and rebuild byte for byte.

**Tape oddities.** Each game file was saved with its end address one byte short, so the last byte of each intended range isn't on the tape. Side 2's loader names its files `MAIN*` and `ADDS*` but passes a length of 4, so the `*` is never used. Both are listed in [the quirks](quirks.md).

---

## Tape and PRG Hold the Same Game

`tools/tape_check.py` places each tape file where the loader puts it and compares it with the unpacked PRG image. Every file is identical, byte for byte. The image bytes not from the tape are few: the last byte of each file's range (the one the tape never saved), the two bytes below `$1000` or `$0800`, and in Day Two the 1 KB screen at `$0C00`–`$0FFF`, which the crunched PRG carries but the tape doesn't load (4 and 1,027 bytes). So the PRGs are a crunched copy of the memory the tape leaves, and anything in the PRG image is also in the 1985 release. That includes the ten `NOP`s in Day Two and its character-set copy.

`make verify` runs this check every time.

---

## The Crunched PRGs

Each PRG is a BASIC line `SYS 4109` followed by a self-extracting decruncher and the packed game: entropy 7.88 and 7.90 bits per byte. The decruncher's layout (52-entry tables at `$0334`, `$0368` and `$039C`, a bit reader copied to `$0100`) matches Exomizer's self-extracting decruncher; that is a structural match, not checked against an Exomizer build. It unpacks the game into `$0FFE`–`$3FFF` (Day One) or `$07FE`–`$3FFF` (Day Two) and ends with a `JMP` from the stack page: `$019D` to `$1010`, or `$01A2` to `$2111`.
