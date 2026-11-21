# Daley Thompson's Star Events – Quirks and Open Items

What the original does that looks accidental or unfinished, kept as it is in the faithful build, and code the trace cannot yet account for. Each item gives its class (skill `analysis.md`) and evidence.

---

## Quirks

| Where | What | Class |
|:------|:-----|:------|
| Part 1 `$22E3` | Second entry of the sound jump table (`JMP $2783`, silence) has no caller in part 1; part 2's counterpart at `$1803` is called from five places | Unreachable |
| Part 2 `$212F` | Ten `NOP`s between the start-up copy loop and the stack reset; present on the 1985 tape too | Uncertain: likely padding left from editing |
| Part 2 `$0800`–`$0BDF` | The tape loader puts `ADDS` (1 KB) in colour RAM at `$0800`; `Entry_day_two` copies it down to `$0400`–`$07DF` before using the screen | Undocumented coherent |
| Tapes | Each file was saved with an end address one short (`$2FFF`, `$3FFF`), so the last byte of each intended range is not on the tape; the PRGs have whatever was in RAM there (`$7D`, `$DE`, `$AA`) | Likely defect (mastering), harmless |
| Tape side 2 | `ADDS` was saved from `$1400` (its header) but the loader loads it at `$0800` | Undocumented coherent: saved from where it lived during development |
| Tape side 2 | The loader's file names are `MAIN*` and `ADDS*`, used with length 4, so the `*` is never read | Remnant |
| Part 2 | After the third event `EventIndex` returns to 0; three unqualified attempts at any event return to the start screen | Undocumented coherent |
| Part 1 `$22F6` | A third `JSR PlayTunePair_day_one` with two words (`$25E5`, `$2621`) and `RTS`; nothing calls it. Decoded, it is note for note Day Two's qualified tune; Day One plays a short effect for QUALIFIED instead | Remnant: a tune that lost its caller |
| Part 1 | Hitting a hurdle only changes its picture; it costs no speed or time | Uncertain: a simplification or an omission |
| Part 1 `RecordTimes` | The RECORDS box never takes the player's time: no store, indexed store or pointer in part 1 reaches `$18D7`–`$192A` | Undocumented coherent |
| Part 2 `WorldRecordTable` | WORLD RECORD for the long jump is 11.87 m (the real record in 1985 was 8.90 m); shot-put 17.60 m, javelin 101.30 m | Uncertain: placeholder or deliberate |
| Both | Footstep pitch comes from reading successive BASIC ROM bytes (`$A000`, `$A063`) | Undocumented coherent: cheap noise source |
| Part 1 `RaceClock` | `TickRaceClock` runs once a frame (split 1); its last digit counts 0–5 and the next 0–9, so a displayed second is 60 frames: 1.2 real seconds on a PAL C16, and the last digit never shows 6–9. On an NTSC C16 (60 Hz) the game runs unchanged and a displayed second is 1.0 s (measured in VICE) | Uncertain: a 60 Hz assumption, or a deliberate easing of the qualifying times |
| Part 1 | After the fourth event (200 m hurdles) `EventNumber` returns to 1 and the four events run again with the score kept; there is no hand-over to part 2 | Undocumented coherent: the parts are on separate tape sides |
| Part 2 `FlightStep` | The scroll rate in flight is built from bits 4, 2 and 0 of `TakeOffSpeed`, not its top bits, so speed `$1D` scrolls at 9 and `$1E` at 8; measured in VICE, `$1D` goes about an eighth further than `$1E` in all three events (below 60° in the long jump) | Likely defect: two shifts between `ROL`s where one was meant |
| Part 2 `ShotPut` | Outside 35–54° the scroll is (`FlightStep` AND 3) + 1, so a fast run-up throws less than a slow one (1.5 m against 3.2 m at 55°, measured) | Uncertain: a deliberate penalty with an accidental twist |
| Part 2 `Javelin` | Below 35° the javelin falls one pixel a step, and a full-speed throw measures about 122 m, past the 101.30 m WORLD RECORD | Likely defect: angle balance not tested at the shallow end |
| Part 2 `RunwayCellStep` | Every 14th runway cell in flight places a marker and adds no distance | Undocumented coherent |
| Part 2 `LongJump` | The hang lasts until the runway band turns to sand (`RunwayBandColour`), so the jumper always reaches the pit; a slow jump still measures about 3.5 m | Undocumented coherent |
| Part 1 `MainLoop_day_one` | Writing `$FD` to `$FD30` as well as `$FF08` selects keyboard row 1, so A, 4, E and SHIFT act as left, right and fire although Day One has no key option | Uncertain: deliberate key support or a side effect of the latch write |
| Part 1 `Lives` markers | One R per attempt is printed at `$0CF2` only when an event starts; a failed race lowers `Lives` without removing one, so the markers lag by a race and GAME OVER still shows one R | Undocumented coherent: the markers show the attempts at the start of the race |
| Part 2 `ReadInput` | In JOY mode the `$FF08` reading also takes keyboard row 4, which `SelectInputMode` leaves selected in `$FD30` every frame, so J acts as left, 0 as right and N as fire | Uncertain: a side effect, like part 1's keys |
| Part 1 `$170C`–`$1725` | Code-shaped bytes (increment six screen digits at `$0C2F`); nothing reaches `$170C`, directly or indirectly | Remnant: an unused score routine |
| Part 2 `$2140`–`$2162` | Code-shaped bytes reading TED timers `$FF00`/`$FF02` into `$28`–`$2B`; nothing reaches `$2140` | Remnant: an unused random-number routine |
| Part 2 `$241D`–`$2436` | Bytes after `EventTableOffset` that decode as a routine printing A as two hex digits at `$0F99,X`; nothing reaches `$241D` | Remnant: a hex printer left from development |
| Part 2 `$2109`–`$2110` | Eight bytes before `Entry_day_two` (`EA 20 58 60 EA …`); nothing reaches them | Remnant: leftover bytes |
| Part 2 flight on NTSC | Flight steps are paced by `DelayXY` (CPU cycles) while distance is added each frame, so on an NTSC C16 a step lasts about 7.8 frames against 4.5 on PAL and every distance comes out about 1.5 times longer (javelin up to 182.5 m) | Undocumented coherent: written and tuned for PAL |
| Both tune players | A misplaced tune command (`$FF` inside a call, `$FE` at depth 0, calls nested past 16) executes `BRK` with a code in X (1–3), dropping into the KERNAL's monitor | Undocumented coherent: a development trap left in |
| Part 2 `TopFrameTable` | Entry 9 (`$3890`) repeats frame 1 and is never selected: the run cycle wraps at 9 | Remnant: purpose unknown |

---

## Open Items

None at present. The unused blocks are now quirks: a search of both images (below, in [the evidence](evidence.md)) found no indirect route to any of them.
