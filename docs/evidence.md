# Daley Thompson's Star Events – Evidence

One entry per name that claims a role: what was seen, how, and when. The source comment states the conclusion; the proof lives here. Rungs follow the skill's evidence ladder (1 code, 2 seen running, 3 controlled run, 4 confirmed by Anthony).

---

## Anthony's Recollections

Given 21-11-2026, about 41 years after the event. Memory is evidence, not proof.

| Topic                | Recollection                                                   |
|:---------------------|:---------------------------------------------------------------|
| Authors              | Written jointly by Anthony and Jason Perkins; no one else involved |
| Commission           | D.C. Ward (Ocean) commissioned the C16 version                 |
| Brief                | Replicate the C64 game as faithfully as the C16 allowed        |
| Source material      | None from Ocean: everything done by watching the C64 version   |
| Two parts            | Memory was very tight, so many C64 features were dropped and the game split in two |
| Tools                | Written and assembled on a C64; the runtime loaded onto the C16 |
| Advert boards        | Copied from the C64 version                                    |
| Running control      | Probably alternate two keys or move the joystick left and right |
| Not remembered       | Attempts counter, scoring, menu, joystick port, tunes, screen packer, unused routines, `NOP`s, bugs, label names, the `$0600` loader, the PRGs' origin |

---

## Unpacking

| Item                   | Evidence                                                    | Date       |
|:-----------------------|:------------------------------------------------------------|:-----------|
| Packed (both parts)    | Entropy 7.88 and 7.90 bits/byte; `SYS` lands on a 12-byte copy loop | 21-11-2026 |
| Decruncher type        | 52-entry tables at `$0334`/`$0368`/`$039C`, bit reader at `$0100`: Exomizer SFX layout (structure only, not checked against an Exomizer build) | 21-11-2026 |
| Unpacked images        | `tools/unpack_sfx.py` and a VICE dump at the decruncher's final `JMP` agree byte for byte | 21-11-2026 |
| Entries `$1010`/`$2111` | The final `JMP` of each decruncher (stack-page copy at `$019D` / `$01A2`) | 21-11-2026 |

---

## Tapes

| Item                  | Evidence                                                    | Date       |
|:----------------------|:------------------------------------------------------------|:-----------|
| Tape format           | Only three wave lengths (53, 105, 210 × 8 cycles); KERNAL encoding: long+medium marker, short+medium = 0, medium+short = 1, odd parity, countdown `$89`/`$09` | 21-11-2026 |
| Tape timing           | Synthetic: all but 6 waves per side are exactly 53, 105 or 210 (× 8 cycles); a sampled cassette varies. Generated from file data by software, origin unknown | 21-11-2026 |
| Tape integrity        | All 12 blocks on both sides: both copies pass their checksums and agree; no parity errors | 21-11-2026 |
| `TapeLoader_side1/2`  | KERNAL `SETLFS`/`SETNAM`/`LOAD` with secondary address 0 to `$1000`, then `$3000` (side 1) or `$0800` (side 2); `JMP` to the entry | 21-11-2026 |
| Tape = PRG contents   | `tools/tape_check.py`: every tape file, placed where the loader puts it, equals the unpacked image | 21-11-2026 |
| Tape start in VICE    | `tools/run_tape.py`: `LOAD"",1,1`, PLAY, `SYS1536`; reaches `$1010` / `$2111` and the same screens as the PRGs | 21-11-2026 |

---

## Part 1 (`day_one`)

| Name                  | Rung | Evidence                                                  | Date       |
|:----------------------|:-----|:----------------------------------------------------------|:-----------|
| `InstallIrq_day_one`  | 1    | Writes `$1584` to `$0314/$0315`, `$02` to `$FF0A` (raster IRQ only) | 21-11-2026 |
| `IrqHandler_day_one`  | 1    | Acks `$FF09`, `JSR` patched from `SplitTable_day_one` by `$0F`, `$0F` wraps at 13 | 21-11-2026 |
| `SplitTable_day_one`  | 1    | 13 words, each the start of a routine that writes `$FF0B` and TED colours | 21-11-2026 |
| `DrawPackedScreen`    | 1    | Reader of `$3000` onward; control codes `$FB`–`$FF`; writes `$0Cxx` and `$08xx` (address `EOR #$04`) | 21-11-2026 |
| `EventNumber`         | 3    | Stepped 1–4 by `StartEvent_day_one`; selects `EventNameText`/`EventDistanceText` offsets 0, 20, 10, 30, which give 100 m sprint, 110 m hurdles, 400 m, 200 m hurdles, the inlay's order. Sampled in VICE with no input: 1 → 2 → 3 as each event ends | 21-11-2026 |
| `Lives`               | 3    | Predicted from the code (set to 3, glyphs at `$0CF1`, `ShowGameOver` at 0) and the inlay ("number of attempts"). Sampled in VICE with no input, so every event ends unqualified: 3 → 2 → 1 → 0 at each event's end, then GAME OVER. With `RunSpeed` held at `$70` every event qualifies and `Lives` stays 3 over 13 events | 21-11-2026 |
| `RunSpeed`            | 3    | Raised only by `SpeedUp` (from `JoyWaggle`), lowered by `SpeedDecay`, drawn as a bar by `DrawSpeedMeter`. Controlled run in VICE (original PRG): `SpeedDecay` patched to `RTS` in RAM and `RunSpeed` set to `$70` at each race start. Every event then ends QUALIFIED, `Lives` stays 3 and `Score` rises; with no input every event fails | 21-11-2026 |
| `JoyWaggle`, `WaggleSeen` | 1 | Only reached on a change of the `$FF08` value; bit 2 low (left) sets bit 1, bit 3 low (right) sets bit 0; at 3, five `SpeedUp` calls (two from `$40`). Agrees with Anthony's recollection of moving the joystick left and right | 21-11-2026 |
| `SpeedDecay`          | 3    | Counts down `$19BC` from 6 (3 from `RunSpeed` `$60`), then `RunSpeed` − 1; two calls per main-loop pass. Patched out in the run above, `RunSpeed` stayed at `$70` | 21-11-2026 |
| `DrawSpeedMeter`, `ClearSpeedMeter` | 1 | Characters `$21`–`$24` to `$0FC6` onward, `RunSpeed / 4` steps; `ClearSpeedMeter` copies 8 bytes from `$16C2` there | 21-11-2026 |
| `Score`, `ScorePending`, `AddScore` | 3 | `AddScore` adds the 6 pending digits into `Score` with decimal carry and prints it at `$0C30`. In the run above the score at `$0C30` rose after each qualified event by 588, 606, 570, 612 … | 21-11-2026 |
| `AwardTimeBonus`      | 3    | Adds 6 points 255 − (sum of three ASCII time digits) times. Every rise in the run above is a multiple of 6 | 21-11-2026 |
| `RaceRunning`         | 2    | Set by `StartCountdown`, cleared by `CheckEventEnd`; gates `TickRaceClock` in the split at `$15C6`. Sampled 1 during each race, 0 between | 21-11-2026 |
| `StartCountdown`, texts | 1 | Screen codes at `$1A73`/`$1A80`/`$1A87` decode to ON YOUR MARKS, GET SET, GO; seen on screen at stage 5 | 21-11-2026 |
| `RaceClock`, `TickRaceClock` | 1 | Five ASCII digits stepped with carry ($1834 wraps after 5, the rest after 9), printed at `$0FDD`–`$0FE2`. Tick rate not yet measured | 21-11-2026 |
| `CheckEventEnd`       | 1    | Per event, compares the distance digits at `$0FD1` with `1`, `11`, `4`, `2` (100, 110, 400, 200 m); or ends at `RaceClock` tens digit `7` | 21-11-2026 |
| `JudgeTime`, `QualifyTimes`, `QualifyIndex` | 3 | Compares the time with the event's entry (13, 15, 60, 38 s for 100 m, 110 m hurdles, 400 m, 200 m hurdles); QUALIFIED and the bonus, or FAILED and `Lives` − 1. Both outcomes seen in VICE | 21-11-2026 |
| `WaitTicks`, `DelayTicks` | 1 | `DelayTicks` set to 100 and spun on; decremented by the split at `$15C6` | 21-11-2026 |
| `MainLoop_day_one`    | 2    | Reached in VICE: the 100 m start sequence ("ON YOUR MARKS", "GET SET") runs from it | 21-11-2026 |
| `JoyLast`             | 1    | Holds the last `$FF08` value read with `$FD` written to `$FD30`/`$FF08`; fire mask `$C0` | 21-11-2026 |
| `SoundSilence_day_one` | 1   | Zeroes `$FF0E`–`$FF11`, clears bits 0–1 of `$FF12`; same routine as part 2's `$1CA2` apart from addresses and one `SEI` | 21-11-2026 |
| `PlayTunePair_day_one` | 1   | Pulls the return address, copies 4 bytes to `$12`–`$15`, returns past them; three callers, each `JSR` + 2 words + `RTS` | 21-11-2026 |

---

## Part 2 (`day_two`)

| Name                  | Rung | Evidence                                                  | Date       |
|:----------------------|:-----|:----------------------------------------------------------|:-----------|
| `InstallIrq_day_two`  | 1    | Writes `$234E` to `$0314/$0315`, raster compare `$2E`     | 21-11-2026 |
| `IrqHandler_day_two`  | 1    | Acks `$FF09`, saves `$21`–`$24`, calls via `SplitTable_day_two`, next line from `SplitRasters_day_two`; the last split sets `$27` to `$FF` | 21-11-2026 |
| `EventJumpTable_day_two` | 1 | Three words read by `$42 * 2` into the `JMP` at `$2F11`   | 21-11-2026 |
| `ScreenRowTable`      | 1    | 25 words `$0C00 + 40n`, read by `ScreenAddress`           | 21-11-2026 |
| `ClearScreen`         | 1    | Space to `$0C00`–`$0FFF`, `$71` to `$0800`–`$0BFF`        | 21-11-2026 |
| `StartGame_day_two`   | 2    | Reached in VICE: the long jump "FIRE TO START" screen with the scrolling advert boards | 21-11-2026 |
