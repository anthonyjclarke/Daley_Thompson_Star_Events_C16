# Daley Thompson's Star Events – Quirks and Open Items

What the original does that looks accidental or unfinished, kept as it is in the faithful build, and code the trace cannot yet account for. Each item gives its class (skill `analysis.md`) and evidence.

---

## Quirks

| Where | What | Class |
|:------|:-----|:------|
| Part 1 `$22E3` | Second entry of the sound jump table (`JMP $2783`, silence) has no caller in part 1; part 2's counterpart at `$1803` is called from five places | Unreachable |
| Part 2 `$212F` | Ten `NOP`s between the start-up copy loop and the stack reset | Uncertain: likely padding left from editing |
| Part 2 `$0800`–`$0BDF` | The unpacked image holds 1 KB of data in colour RAM; `Entry_day_two` first copies it down to `$0400`–`$07DF` | Undocumented coherent |

---

## Open Items

| Where | What | Leading hypothesis |
|:------|:-----|:-------------------|
| Part 1 `$170C`–`$1725` | Code-shaped bytes (increment six screen digits at `$0C2F`); no `JSR`, `JMP`, table or lo/hi pair reaches `$170C` | Unused score routine (remnant); check with a VICE breakpoint during play |
| Part 2 `$2140`–`$2162` | Code-shaped bytes reading TED timers `$FF00`/`$FF02` into `$28`–`$2B`; no reference to `$2140` | Unused random-number routine (remnant); same check |
| Part 2 `$2109`–`$2110` | Eight bytes before `Entry_day_two` (`EA 20 58 60 EA …`) | Leftover bytes; not code reached from anywhere |
| Both | Most variables and routines below the main loops are still neutral names | Later slices of stage 4 |
