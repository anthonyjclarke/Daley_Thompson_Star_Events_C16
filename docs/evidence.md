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

## Coverage

| Run                              | Evidence                                                    | Date       |
|:---------------------------------|:------------------------------------------------------------|:-----------|
| Part 1, no input, 70 s (warp)    | VICE `memmapshow`: 1205 executed instruction addresses, all at traced instruction starts | 21-11-2026 |
| Part 1, speed held, 70 s (warp)  | 1255 executed addresses, all traced; all four events qualified | 21-11-2026 |
| Part 2, fire wait patched, 70 s  | 1324 executed addresses, all traced (two flagged only by a parser artefact) | 21-11-2026 |
| Never executed in these runs     | Part 1 `$170C`–`$1725`, `$22E3` vector, `$22F6` tune call, `SoundSilence_day_one`; part 2 `$2109`–`$2110`, `$2140`–`$2162`, `$241D`–`$2436` | 21-11-2026 |

The runs do not exercise jumping, throwing or a qualified attempt in part 2, so "never executed" there is not proof of dead code; the static search (no reference) is the main evidence.

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
| `MoveRace`, `MoveTrackMarks`, `ScrollStep`, `ScrollScenery`, `RotateCharsLeft` | 1 | `MoveRace` runs from the last split while racing: `RunSpeed / 32` whole `MoveTrackMarks` steps plus a fraction accumulated in `$2181`, then `ScrollStep` by `RunSpeed / 128` plus a fraction. `RotateCharsLeft` shifts seven 8-byte character bitmaps from `$39F8` as one strip; `DrawSceneryRows` fills rows 12–13 with those characters | 21-11-2026 |
| `AdvanceDistance`     | 2    | Every 4 calls adds 1 to the digits at `$0FD0`; sampled distance rose during every race in the controlled runs | 21-11-2026 |
| `StepAthleteFrame`, `DrawAthlete`, `EraseAthlete`, `AthleteFrames` | 1 | Frame offsets step by `$24` (two 18-byte halves); `$D8`/`$EA` jump frames set on fire in events 2 and 4; halves drawn at `$0E5E` and `$0ED6` | 21-11-2026 |
| `Jumping`, `JumpTimer` | 1   | Set by fire in events 2 and 4 when `JumpTimer` is 0; each jump also costs two `SpeedDecay` calls | 21-11-2026 |
| Hurdles: `HurdleState`, `CheckHurdleHit`, `ObjectX`, `DrawHurdleA/B`, object cells | 1 | `StartEvent_day_one` sets `HurdleState` 2 and draws a hurdle only for events 2 and 4. A hurdle at `ObjectX` `$26`–`$43` while not `Jumping` sets 1; this only changes the bitmap drawn (no other reader of `HurdleState` affects speed or time) | 21-11-2026 |
| `DrawFinishLine`, `PlotObjectPixel`, `FinishLineShown` | 1 | Within 10 m of each event's length (distance digits checked per event) the line is plotted pixel by pixel into the object characters and then scrolled | 21-11-2026 |
| `RecordTimes`, `ShowRecords`, `DrawRecordPlaces` | 2 | Seen on screen as RECORDS 1 009:58, 2 010:50, 3 012:60 for the 100 m; the table has no writer, so the player's time never enters it | 21-11-2026 |
| `PlayFootstep`        | 1    | Every 6 athlete frames; pitch byte from `LDA $A000` whose low byte the routine increments: successive BASIC ROM bytes as noise | 21-11-2026 |
| `PlayStartTune`, `PlayGameOverTune`, `PlayQualifiedSound`, `PlayFailedSound`, `StartSoundEffect` | 1 | Callers: `StartEvent_day_one`, `ShowGameOver`, `JudgeTime`'s two branches; effect records at `$2322`, `$2339`, `$2350` | 21-11-2026 |
| `SplitNN_day_one`     | 1    | Each writes TED background colours and the next raster compare; split 1 also runs `DelayTicks` and the clock, split 7 the sound, split 13 `MoveRace` | 21-11-2026 |
| `MainLoop_day_one`    | 2    | Reached in VICE: the 100 m start sequence ("ON YOUR MARKS", "GET SET") runs from it | 21-11-2026 |
| `JoyLast`             | 3    | Holds the last `$FF08` value read with `$FD` written to `$FD30`/`$FF08`; fire mask `$C0`. Live in VICE with a breakpoint at `$13AB` during the 110 m hurdles: A gave `$FB` (left), 4 `$F7` (right), E `$BF` and SHIFT `$7F` (fire). Port: with VICE keysets on both control ports (arrows on port 2, J/L on port 1), only port 2's left and right reached `JoyLast`; VICE's `ted08_store` selects port 1 with bit 2 low and port 2 with bit 1 low, so `$FD` is port 2, fire bit 7. In that run the keysets' fire keys appeared swapped (M gave bit 7, SPACE nothing), a VICE configuration detail | 22-11-2026 |
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
| `WorldRecordTable`, `QualifyLengthTable`, `BestTable` | 2 | Read by `ShowEventTables` into `$0C68`, `$0C90`, `$0CB8`; in VICE they appear on the rows labelled WORLD RECORD, QUALIFYING LENGTH and BEST (`101:30`, `065:70`, `000:00` for event 2) | 21-11-2026 |
| `EventTableOffset`    | 1    | `$00`, `$05`, `$0A` indexed by `EventIndex`; used by `ShowEventTables` and `JudgeAttempt` | 21-11-2026 |
| `JudgeAttempt`, `AttemptResult` | 1 | 5-digit subtraction of the distance (`$2774`–`$2778`) from the qualifying length: borrow → 1, else `$FF`; then the same against `BestTable` (copied on a borrow) and, if qualified, `WorldRecordTable`. `$2CA1` also sets `$FF` | 21-11-2026 |
| `AttemptNumber`, `AttemptResults` | 2 | `StartEvent_day_two` sets `$54`–`$56` to `$FF`; after each attempt `$54,AttemptNumber` = 0 if `AttemptResult` is 1, else 1. Sampled in VICE (fire wait patched out in RAM, no input): `AttemptNumber` 0 → 1 → 2, results 1, 1, 1, then back to the start screen | 21-11-2026 |
| `EventIndex`          | 1    | After three attempts, any 0 in `AttemptResults` steps it 0 → 1 → 2 → 0 and starts the next event; none → `StartGame_day_two` | 21-11-2026 |
| `InputBits`, `ReadInput`, `ReadKeys`, `TestKey` | 3 | Joystick: `$FD` to `$FF08`, inverted, mask `$8C`. Keys: three (row, column) pairs at `$23E8`/`$23E5` mapped to bits `$04`, `$08`, `$80`; in VICE's Plus/4 key table (`PLUS4/gtk3_sym.vkm`, VICE 3.10) these are Q (7, 6), Y (3, 1) and SPACE (7, 4). Live in VICE with a breakpoint at `$23CB`: Q, Y and SPACE pressed alone hit slots 0 (left), 1 (right) and 2 (fire) in turn | 22-11-2026 |
| `InputMode`, `SelectInputMode`, `KeyJoyText` | 3 | Keyboard row `$EF`, columns `$04` and `$20`: J (4, 2) and K (4, 5) in VICE's key table. Live in VICE: J set `InputMode` to 1 and the text to JOY, K back to 0 and KEY | 22-11-2026 |
| `JoyWaggle_day_two`, `SpeedUp_day_two`, `SpeedDecay_day_two`, `RunSpeed_day_two` | 1 | The same scheme as part 1: left then right (either order) gives 5 speed steps (2 from `$0C`), maximum `$1F`; decay every 2 calls with the joystick, every 3 with keys. A RAM-patched run did not produce a jump, so no rung 3 yet | 21-11-2026 |
| Events: `LongJump`, `ShotPut`, `Javelin` | 2 | `TitleGlyphs` decodes (glyphs numbered by first use) to LONG JUMP, SHOT PUT, JAVELIN, FIRE TO START at offsets 0, 11, 21, 30; event 0's screen in VICE shows LONG JUMP. Handlers are `EventJumpTable_day_two` entries 0–2 | 21-11-2026 |
| `SetTakeOffAngle`, `AngleBcd`, `Angle`, `ClassifyAngle` | 1 | `SED` loop adds 1 to `AngleBcd` from `$20` while fire is held, stopping at `$83`; digits via `BcdToAscii` to `AngleDigits` (shown as `00°`). `AngleClass` 1/2/3 at 35 and 55 | 21-11-2026 |
| `TakeOffSpeed`        | 1    | `$67` = `RunSpeed_day_two` when the run-up ends (`$24F0`); used by all three handlers | 21-11-2026 |
| `AngleDigits`, `AttemptDistance`, `Score_day_two`, `DrawScoreLine` | 2 | 13 ASCII digits drawn as large digits along the bottom: `00° 000:00M` and SCORE, as on screen | 21-11-2026 |
| `AddDistanceToScore`, `HighScore` | 1 | Adds the distance's first four digits to score digits 9–12; then a 5-digit compare with `$2A79` and copy if higher | 21-11-2026 |
| `PlayFootstep_day_two` | 1   | Same ROM-noise trick as part 1, pointer from `$A063` | 21-11-2026 |
| `SplitNN_day_two`     | 1    | Thirteen raster splits; split 1 sets the fine scroll from `$2D` and calls `PollInput_day_two` | 21-11-2026 |
| `ScrollRunway`, `RunwayCellStep`, `AddFlightDistance`, `DistanceRates` | 1 | `ScrollRunway` (split at `$230A`) subtracts `RunwayScrollStep` − 1 from the fine scroll each frame and shifts the runway row at each 8 pixels, then `RunwayCellStep` calls `AddFlightDistance`: tenths from `$326D + 3 × EventIndex`, hundredths `TED_T1_LO AND mask + base`, both through `AddDigit` | 21-11-2026 |
| `TakeOffDelay`        | 1    | Set in `SetTakeOffAngle` to `AthleteX / 4 − $13`; `AddFlightDistance` returns early while it counts down. With the foul limit `AthleteX` ≥ `$50`, the smallest delay is 1, at the line | 21-11-2026 |
| `PeakRow`, `HangTime`, `FlightPhase` | 1 | `LongJump`: `PeakRow` = ((`Angle` − 20) XOR `$3F`) / 8 + 7; below 10 halves `TakeOffSpeed` and fixes the scroll at 5; `HangTime` = (`TakeOffSpeed` AND `$1C`) / 2 + 2; rows step every 7 calls of `Every7Rising`/`Every7Falling` until row `$0F`, then `Landed` | 21-11-2026 |
| `ShotPut`, `Javelin` angle rules | 1 | `ShotPut`: `RunwayScrollStep` from `TakeOffSpeed` only when `Angle` is `$23`–`$36` (35–54), otherwise (`$75` AND 3) + 1. `Javelin`: `PeakRow` = ((`Angle` − 20) XOR `$3F`) + `$33`; below `$44` (`Angle` ≥ 67) the step is fixed at 4; hang `$7C` = (`TakeOffSpeed` AND `$1C`) / 2 + 6 | 21-11-2026 |
| `FlightStep`          | 3    | All three handlers shift `TakeOffSpeed` left four times, `ROL` into `FlightStep`, then twice and `ROL`, twice and `ROL`: bits 4, 2 and 0 of the speed, plus 2, give `RunwayScrollStep` 2–9. `tools/flight_probe.py` in VICE: speed `$1D` beats `$1E` in all three events, `$1F` matches `$1D` | 22-11-2026 |
| `RunwayCellCount`     | 1    | `RunwayCellStep`: zeroed by `SetTakeOffAngle`; at `$0E` it is reset, character `$1D` is put at `$0F97` (row 22, right edge) and `AddFlightDistance` is skipped | 22-11-2026 |
| `RunUpScrolling`      | 1    | Set at `$24D7` when the run-up starts, cleared at take-off (`$24F6`); `ScrollRunway` sends whole cells to `RunwayCellStep` only while it is 0, so the distance counts from take-off to `Landed` (`RunwayScrollStep` = 0) | 22-11-2026 |
| `InFlight`, `FlightTopFrame`, `FlightBottomFrame`, `LongJumpFrames` | 1 | Set by `LongJump`; `RunwayCellStep` then calls `AdvanceAthlete`, and `StepRunFrame_day_two` takes frames from `$84`/`$85`, loaded from `$2FE0` by `FlightPhase` | 22-11-2026 |
| `RunwayBandColour`    | 1    | `Split09_day_two` writes it to `TED_BG0`; `$32` at every start, `$67` from `AdvanceAthlete` once `AthleteX` < `$10`. In TED's palette `$32` is red and `$67` yellow, so the band turns from track to sand. `LongJump` keeps `FlightPhase` at 1 (hang) until it is `$67` | 22-11-2026 |
| `NextAthleteCol`, `NextAthleteRow`, `DrawnAthleteCol`, `DrawnAthleteRow`, `AthleteMoves`, `ColumnStepCount` | 1 | `MoveAthlete_day_two` compares `$5C`/`$5D` with `$5E`/`$5F` and copies changes to `AthleteCol`/`AthleteRow`; `UpdateFigures` calls it while `$60` is set; `SpeedUp_day_two` moves the column every 6th call below `$0E` | 22-11-2026 |
| `ShotCol`, `ShotY`, `ShotDrawnCol`, `ShotDrawnY`, `ShotShown`, `ShotFalling`, `ShotChar`, `ShotBitmap` | 1 | `InitAthlete_day_two` loads column 3, row `$70` for event 1 from `$2C7E`; `DrawShotBall` puts character `$6A` at (`ShotCol`, `ShotY` / 8) and copies the 8-byte ball from `$31F1` into `$1350` (character `$6A` of the `$1000` set) at `ShotY` AND 7; `ShotPutLoop` moves `ShotY` by `AngleClass` until `PeakRow`, then back down to `$9B` | 22-11-2026 |
| `JavelinCol`, `JavelinY`, `JavelinDrawnCol`, `JavelinDrawnY`, `JavelinShown`, `JavelinPhase`, `JavelinHang`, `JavelinChar`, `JavelinChars`, `JavelinCellOffsets` | 1 | Event 2 from `$2C82`: column 1, row `$68`. `DrawJavelinShaft` writes 10 cells at offsets `$3174` with characters counting down from `$317E` + `JavelinPhase`; `JavelinLoop`: rise by `AngleClass` to `PeakRow`, hang `JavelinHang` steps, fall, phase 3 from `$8C`, land at `$96` | 22-11-2026 |
| `CarryFrame`          | 1    | `InitAthlete_day_two`: 0 for event 0, `$0A` otherwise; `ShotPut`/`Javelin` set `$0B`. `StepRunFrame_day_two` uses it as the frame in events 1–2 and returns before the bottom half at `$0B` | 22-11-2026 |
| `FollowThrough`       | 1    | Called by `ShotPut` and `Javelin` after the scroll starts: per step `AthleteCol` − 1, `ShotY` − `AngleClass`, `JavelinY` − 1, `AthleteX` − 3 with `DrawRunway`, `DelayXY` `$0A`, until column 0; then 80 spaces from `$0EF8` | 22-11-2026 |
| `Every7Count`, `LongJumpLoop`, `ShotPutLoop`, `JavelinLoop` | 1 | Loop heads of the three handlers, each ending with `DelayXY` (`$14`, 7, `$0A`); `$87` is the shared countdown of `Every7Rising`/`Every7Falling` | 22-11-2026 |
| `TakeOffDelay`, measured | 3 | `tools/flight_probe.py --position`, speed `$1F`, 45°: `AthleteX` `$50` → `$9B` cuts each event (long jump 10.64 → 9.00 m, shot-put 15.66 → 11.58 m, javelin 87.38 → 73.58 m) | 22-11-2026 |
| `LongJump`, `ShotPut`, `Javelin` flight rules | 3 | `tools/flight_probe.py`, 7 speeds × 9 angles per event: long jump about 4.6 m at every speed from 60°; shot-put full distance only at 35–45° of the tested angles; javelin about 33 m from 67°, longest under 35° (122 m at `$1D`) | 22-11-2026 |
| `StartGame_day_two`   | 2    | Reached in VICE: the long jump "FIRE TO START" screen with the scrolling advert boards | 21-11-2026 |
