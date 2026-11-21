# Testing Worklist

What still needs testing or checking, and how. Items already checked, in the code or in VICE, are listed once with where the proof lives; everything else is open. Tick items off by moving them to the first table and recording the result in [the evidence](evidence.md) or [the quirks](quirks.md).

---

## Checked

| Item                           | How it was checked                           | Recorded in             |
|:-------------------------------|:---------------------------------------------|:------------------------|
| Byte-identical rebuild         | `make verify`, every change                  | `SOURCE_AND_VALIDATION` |
| Tapes equal the unpacked PRGs  | `tools/tape_check.py`                        | `ARTIFACTS`             |
| Code coverage                  | VICE execution map over three runs           | evidence, Coverage      |
| Day One race speed             | `SpeedDecay` patched in a controlled run     | evidence, part 1        |
| Day Two distances              | `tools/flight_probe.py`, 189 forced attempts | analysis, How Far       |
| Day Two keys J, K, Q, Y, SPACE | Pressed in VICE, breakpoint at `$23CB`       | evidence, part 2        |
| Day One keys A, 4, E, SHIFT    | Pressed in VICE, breakpoint at `$13AB`       | evidence, part 1        |
| Joystick port                  | Keyset joystick on each port; VICE source    | evidence, part 1        |
| Advertising boards             | Rendered from `ADDS`, matched to the screen  | `GRAPHICS`              |
| All other graphics             | Rendered from the originals; VICE shots      | `GRAPHICS`              |
| Day Two JOY mode key row       | Code read: row 4 stays selected              | evidence, part 2        |
| Unused code, indirect callers  | Both images searched; none found             | evidence, Coverage      |
| Day One `RecordTimes`          | Every store checked; nothing writes it       | evidence, part 1        |
| NTSC race clock                | `c16ntsc` in VICE: 1.00 s a displayed second | evidence, part 1        |
| Day One GAME OVER R marker     | Code read; screen redraw run in `cpu6502.py` | quirks                  |
| Tunes decoded                  | `tools/decode_tunes.py`; title timed in VICE | analysis, The Tunes     |
| Sound clips                    | `render_sounds.py`; matches VICE's dump      | analysis, Sound         |
| Day Two on NTSC                | 189 forced attempts with `--ntsc`            | analysis, How Far       |
| Names                          | Every data label named; branch targets left  | evidence; worklist      |
| Decruncher                     | Exomizer 2.0 re-crunch is byte-identical     | artifacts; exo_check.py |

---

## Needs a Person at the Machine

These need hands, ears or real hardware; the monitor can't do them.

| Item                   | What to do                                                       | What to note                            |
|:-----------------------|:-----------------------------------------------------------------|:----------------------------------------|
| Day One feel           | Play all four races with a joystick on port 2                    | Can you qualify? Is 13 s fair?          |
| Hurdles                | Jump and hit hurdles in both hurdle races                        | Does a hit really cost nothing?         |
| Day One restart        | Lose all attempts, press fire at GAME OVER                       | Score and event reset as expected?      |
| Long jump              | Jump at 55–59° and at 60°+ at full speed                         | Near 11 m, then about 4.6 m?            |
| Shot-put               | Throw at 45°, then at 60° slow and fast                          | Slow beats fast outside 35–54°?         |
| Javelin                | Throw under 35° at full speed                                    | Beats the 101.30 m world record?        |
| Speed quirk            | Compare runs ending just below and at full speed                 | Noticeable in play?                     |
| Day Two attempts       | Fail three times; qualify once                                   | Back to title / next event?             |
| High score             | Score, return to the title                                       | High score kept and shown?              |
| Sound: Day One         | Listen to start, qualified, failed, game over and footsteps      | Same as the handbook's clips?           |
| Sound: Day Two         | Listen to the title tune, event tune, qualified tune and effects | Same as the handbook's clips?           |
| Real C16               | Load both tape sides on a PAL C16 (16 KB)                        | Loads, runs, any difference to VICE     |
| Plus/4                 | Load and play on a Plus/4                                        | Does it run unchanged?                  |
| Real keyboard aliasing | Try A, 4, E, SHIFT in Day One on hardware                        | Same as in VICE?                        |
| Day Two joystick mode  | Press J, then try J, 0 and N during an event                     | Left, right and fire, as the code says? |

---

## To Check in the Code

Nothing is open: every code check is done.

### Names Still Neutral

Every routine, variable, table and patched operand in both parts now has a name (22-11-2026). What remains neutral is 526 branch targets, 250 in Day One and 276 in Day Two, each inside a routine that has a name and a block comment. They stay `Lxxxx` by choice: they are jump points within a routine, not things of their own.
