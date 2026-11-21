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
| Part 1 | After the fourth event (200 m hurdles) `EventNumber` returns to 1 and the four events run again with the score kept; there is no hand-over to part 2 | Undocumented coherent: the parts are on separate tape sides |

---

## Open Items

| Where | What | Leading hypothesis |
|:------|:-----|:-------------------|
| Part 1 `$170C`–`$1725` | Code-shaped bytes (increment six screen digits at `$0C2F`); no `JSR`, `JMP`, table or lo/hi pair reaches `$170C` | Unused score routine (remnant); check with a VICE breakpoint during play |
| Part 2 `$2140`–`$2162` | Code-shaped bytes reading TED timers `$FF00`/`$FF02` into `$28`–`$2B`; no reference to `$2140` | Unused random-number routine (remnant); same check |
| Part 2 `$241D`–`$2436` | Bytes after `EventTableOffset` that decode as a routine printing A as two hex digits at `$0F99,X`; no `JSR`, `JMP` or pointer reaches `$241D` | Debug remnant: a hex printer left from development |
| Part 2 `$2109`–`$2110` | Eight bytes before `Entry_day_two` (`EA 20 58 60 EA …`) | Leftover bytes; not code reached from anywhere |
| Part 1 `RaceClock` | The last digit counts 0–5 and the one before it 0–9, so the clock is not true hundredths; how often `TickRaceClock` runs per frame is not yet measured | A frame counter shown as a time; measure ticks per second in VICE |
| Both | Most variables and routines below the main loops are still neutral names | Later slices of stage 4 |
