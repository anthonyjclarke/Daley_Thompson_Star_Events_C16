# Playing the Game

A player's guide to the C16 *Daley Thompson's Star Events*, written from the code. The tips follow from how the game actually works ([codebase analysis](../CODEBASE_ANALYSIS.md)); manual play on a real C16 has not yet been done, so treat the feel of each event as untested.

---

## Loading

Each part is on its own side of the tape. Type `LOAD"",1,1`, press PLAY, and when the loader has loaded type `SYS1536`. The loader then loads the game's two files from the same tape and starts it. Side 1 holds Day One, side 2 Day Two. In VICE, `python3 tools/run_tape.py 1` (or `2`) does all of this for you.

---

## Day One: The Running Events

![100 m, waiting for the start](images/event_100m.png)

Day One is four races in a fixed order: 100 m, 110 m hurdles, 400 m, 200 m hurdles. You start with three attempts (the R symbols under the distance), and each race you fail costs one.

**Start.** Each race starts by itself: the game shows ON YOUR MARKS, GET SET and GO, then the clock runs. After GAME OVER, press fire to play again.

**Running.** Move the joystick left and right in turn. Speed rises only when both directions have been seen since the last step, so holding one direction, or wiggling only one way, does nothing. Each full left-right pair adds 5 to the speed, or 2 once you are past about half the meter, and the speed bleeds away all the time, faster near the top. The SPEED meter at the bottom shows where you are.

**Hurdles.** In the hurdle events, press fire to jump. A jump can't start until the last one has finished, and each jump costs a little speed. Knocking a hurdle over only changes its picture: in this version it costs no time.

![110 m hurdles](images/event_110m_hurdles.png)

**Qualifying.** Each race has a qualifying time, shown at the top (QUALIFY). Beat it and you see QUALIFIED and score points; miss it and you see FAILED and lose an attempt. The race also ends if the clock reaches 70.

| Event           | Qualify | Records box (1st, 2nd, 3rd)  |
|:----------------|:--------|:-----------------------------|
| 100 m           | 13:00   | 9:58, 10:50, 12:60           |
| 110 m hurdles   | 15:00   | 12:29, 14:10, 14:90          |
| 400 m           | 60:00   | 42:51, 44:01, 46:60          |
| 200 m hurdles   | 38:00   | 20:08, 35:50, 37:00          |

The clock counts in its own units: one displayed second is 60 frames, which is 1.2 real seconds on a PAL C16, and the last digit only goes up to 5.

**Points.** A qualified race scores 6 × (255 − the sum of three of the time's digits as characters). Faster times give smaller digits and so more points. After the 200 m hurdles the four races start again, with your score kept, until the attempts run out.

![400 m](images/event_400m.png)

![200 m hurdles](images/event_200m_hurdles.png)

---

## Day Two: The Field Events

![Long jump](images/event_long_jump.png)

Day Two is long jump, shot-put and javelin, with three attempts at each. Qualify with any of the three to go on to the next event; fail all three and you're back at the start screen.

**Controls.** On the start screen, press J for joystick or K for keys; the choice shows as JOY or KEY at the bottom left. With keys, Q and Y are left and right and SPACE is fire. (These key names come from reading the keyboard matrix in the code and haven't yet been checked on a machine.) The keyboard's speed drains a little more slowly than the joystick's.

**Run-up.** Alternate left and right as in Day One to build speed.

**Angle.** At the line, hold fire: the angle shown before `°` counts up from 20. Release fire to take off or throw. The angle stops at 83 if you hold on. Running on past the take-off point without releasing is a foul.

![Shot-put](images/event_shot_put.png)

**Judging.** The box at the top shows the event's WORLD RECORD, its QUALIFYING LENGTH and your BEST. An attempt longer than the qualifying length qualifies; the three marks by FOUL show how each attempt went.

| Event      | World record | Qualifying |
|:-----------|:-------------|:-----------|
| Long jump  | 11.87 m      | 6.80 m     |
| Shot-put   | 17.60 m      | 13.90 m    |
| Javelin    | 101.30 m     | 65.70 m    |

**Points.** Each attempt's metres and tenths are added to your score, and the best score stays as the high score on the start screen.

**What makes a long throw or jump.** The distance is counted while the ground scrolls under the flight, so three things matter ([how far](../CODEBASE_ANALYSIS.md#how-far-the-distance-counter)):

- **Speed at take-off** sets how fast the ground scrolls during the flight. Waggle hard right up to the line.
- **The angle** sets how long the flight lasts. A steeper angle flies longer, but in the long jump 60° or more halves your speed, so aim just under 60°.
- **The shot-put's angle band.** The shot only keeps your run-up speed between 35° and 54°. For the javelin, stay under 67°.
- **Taking off close to the line** matters. The counting starts only after a delay that grows the earlier you take off; the shortest delay is right at the line, and one step later is a foul.

A few hundredths of each distance are random.

![Javelin](images/event_javelin.png)
