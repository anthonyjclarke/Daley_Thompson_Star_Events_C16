# Daley Thompson's Star Events – Evidence

One entry per name that claims a role: what was seen, how, and when. The source comment states the conclusion; the proof lives here. Rungs follow the skill's evidence ladder (1 code, 2 seen running, 3 controlled run, 4 confirmed by Anthony).

---

## Unpacking

| Item                   | Evidence                                                    | Date       |
|:-----------------------|:------------------------------------------------------------|:-----------|
| Packed (both parts)    | Entropy 7.88 and 7.90 bits/byte; `SYS` lands on a 12-byte copy loop | 21-11-2026 |
| Decruncher type        | 52-entry tables at `$0334`/`$0368`/`$039C`, bit reader at `$0100`: Exomizer SFX layout (structure only, not checked against an Exomizer build) | 21-11-2026 |
| Unpacked images        | `tools/unpack_sfx.py` and a VICE dump at the decruncher's final `JMP` agree byte for byte | 21-11-2026 |
| Entries `$1010`/`$2111` | The final `JMP` of each decruncher (stack-page copy at `$019D` / `$01A2`) | 21-11-2026 |

---

## Part 1 (`day_one`)

| Name                  | Rung | Evidence                                                  | Date       |
|:----------------------|:-----|:----------------------------------------------------------|:-----------|
| `InstallIrq_day_one`  | 1    | Writes `$1584` to `$0314/$0315`, `$02` to `$FF0A` (raster IRQ only) | 21-11-2026 |
| `IrqHandler_day_one`  | 1    | Acks `$FF09`, `JSR` patched from `SplitTable_day_one` by `$0F`, `$0F` wraps at 13 | 21-11-2026 |
| `SplitTable_day_one`  | 1    | 13 words, each the start of a routine that writes `$FF0B` and TED colours | 21-11-2026 |
| `DrawPackedScreen`    | 1    | Reader of `$3000` onward; control codes `$FB`–`$FF`; writes `$0Cxx` and `$08xx` (address `EOR #$04`) | 21-11-2026 |
| `EventNumber`         | 1    | Stepped 1–4 by `StartEvent_day_one`; selects `EventNameText`/`EventDistanceText` offsets 0, 20, 10, 30, which give 100 m sprint, 110 m hurdles, 400 m, 200 m hurdles, the inlay's order | 21-11-2026 |
| `Counter117C`         | 1    | Set to 3; that many `$12` characters drawn at `$0CF1` (seen as three glyphs left of SPRINT); `ShowGameOver` when 0 | 21-11-2026 |
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
