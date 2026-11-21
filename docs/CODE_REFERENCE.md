# Code Reference

Every name in the disassembly, generated from `tools/symbols.py` by `tools/code_reference.py`. Don't edit this file: change the names and comments in `symbols.py`, then run `make docs`. Names starting `L` followed by an address are not listed; they are still neutral. `docs/evidence.md` holds the proof for each name that claims a role.

Shared by every block: `$0314` **CINV**, `$0315` **CINV_HI**.

---

## Part 1, crunched PRG

Block `day_one_packed`, from `original/daley_thompsons_star_events_day_one.prg`. Source `src/day_one_packed.s`.

### Declared Data

- `$1001`–`$100C` **BasicStub** (ByteTable) – BASIC line 20 SYS4109 that starts the decruncher

### Names

- `$100D` **SfxStart_day_one** – Exomizer 2.0 sfx stub (part 1): copies the decruncher to the stack page.

---

## Part 2, crunched PRG

Block `day_two_packed`, from `original/daley_thompsons_star_events_day_two.prg`. Source `src/day_two_packed.s`.

### Declared Data

- `$1001`–`$100C` **BasicStub** (ByteTable) – BASIC line 20 SYS4109 that starts the decruncher

### Names

- `$100D` **SfxStart_day_two** – Exomizer 2.0 sfx stub (part 2): blanks the screen (enter fragment), copies the decruncher.

---

## Tape loader, side 1

Block `loader_side1`, from `original/dt_star_events_side1.tap`. Source `src/loader_side1.s`.

### Declared Data

- `$0639`–`$063D` **MainName_side1** (ByteTable) – 'MAIN1' (length 5)
- `$063E`–`$0642` **AddsName_side1** (ByteTable) – 'ADDS1' (length 5)

### Names

- `$0600` **TapeLoader_side1** – SYS 1536: LOAD 'MAIN1' at $1000 and 'ADDS1' at $3000 from tape, then start part 1.
- `$1010` **Entry_day_one**

---

## Tape loader, side 2

Block `loader_side2`, from `original/dt_star_events_side2.tap`. Source `src/loader_side2.s`.

### Declared Data

- `$0639`–`$063D` **MainName_side2** (ByteTable) – 'MAIN*', used with length 4 as 'MAIN'
- `$063E`–`$0642` **AddsName_side2** (ByteTable) – 'ADDS*', used with length 4 as 'ADDS'

### Names

- `$0600` **TapeLoader_side2** – SYS 1536: LOAD 'MAIN' at $1000 and 'ADDS' at $0800 (not its header's $1400), then start part 2.
- `$2111` **Entry_day_two**

---

## Part 1 (Day One)

Block `day_one`, from `original/day_one_unpacked_vice.prg`. Source `src/day_one.s`.

### Declared Data

- `$15AC`–`$15C5` **SplitTable_day_one** (AddrTable) – Raster-split handlers, called in turn by the IRQ (13 entries)

### Names

- `$1010` **Entry_day_one** – Entry point of part 1 (the decruncher's final JMP). Provisional name.
- `$1013` **EntryPad** – 17 bytes after the entry JMP; the self-modified operands point into them in the image, but no code reads them.
- `$1024` **FetchPackedByte** – Load the byte at the packed-screen pointer (the LDA operand at $1025/$1026 is the pointer).
- `$1025` **PackedPtr** – Packed-screen read pointer: the LDA operand in FetchPackedByte.
- `$1026` **PackedPtrHi**
- `$104E` **RunScreenPtr** – Screen and colour pointers of DrawPackedScreen's run loop: STA operands, copied from ScreenPtr and ColourPtr and stepped with them.
- `$104F` **RunScreenPtrHi**
- `$1054` **RunColourPtr**
- `$1055` **RunColourPtrHi**
- `$106E` **AdvancePackedPtr** – Step the packed-screen pointer by one.
- `$1077` **DrawPackedScreen** – Decode the packed screen at $3000 into screen $0C00 and colour $0800. Codes: $FB run, $FC set address, $FD the row below the last $FC address, $FE set colour, $FF end; others are characters.
- `$109F` **ScreenPtr** – Screen and colour write pointers of DrawPackedScreen: STA operands.
- `$10A0` **ScreenPtrHi**
- `$10A5` **ColourPtr**
- `$10A6` **ColourPtrHi**
- `$1116` **PackedRowLo** – Low byte of the last $FC address; $FD sets the screen pointers to the row below it.
- `$1117` **PackedColour** – Colour for the next characters, set by the $FE code.
- `$1121` **EventNumber** – 1-4: the event being run; picks its name, distance and set-up.
- `$1122` **EventSpare** – Cleared by StartEvent_day_one; nothing reads it.
- `$1123` **EventDistanceText** – Four 10-byte fields: ' 100', ' 400', ' 110', ' 200' (indexed 0, 10, 20, 30).
- `$114B` **EventNameText** – Four 10-byte fields: SPRINT, RUN, HURDLES, HURDLES.
- `$1173` **GameOverText** – 'GAME OVER', drawn by ShowGameOver.
- `$117C` **Lives** – Set to 3; one glyph each at $0CF1. One is lost when an event ends unqualified; 0 ends the game.
- `$117D` **ScoreCarryOut** – Where AddScore's carry out of the top digit lands (ScorePending - 1).
- `$117E` **ScorePending** – Six decimal digits (0-9, most significant first) waiting to be added by AddScore.
- `$1184` **Score** – Six decimal digits (0-9, most significant first), shown at $0C30 by AddScore.
- `$118A` **ScoreSpare** – Six bytes after Score, cleared with ScorePending each event; nothing reads them.
- `$1191` **ShowGameOver** – Print GAME OVER, play a tune, wait for fire.
- `$11EC` **BonusCount** – AwardTimeBonus's count of 6-point additions.
- `$11ED` **AwardTimeBonus** – Add 6 points to the score 255 - (sum of three of the time's ASCII digits) times.
- `$1214` **AddScore** – Add ScorePending to Score digit by digit with carry, print Score at $0C30, clear ScorePending.
- `$123C` **InitGame_day_one** – Clear the score tables and set Lives to 3, then fall into the event set-up.
- `$125A` **StartEvent_day_one** – Draw the screen, step EventNumber, print the event's name and distance, set TED, install the IRQ.
- `$139B` **MainLoop_day_one** – Once a frame: read the joystick, act on a change, wait for raster line $A8, update, check the event's end.
- `$14D8` **FinishLineShown** – 1 once the finish line is drawn (within 10 m of the end); ScrollTrackObjects then moves it.
- `$14D9` **JoyLast** – Last value read from TED_KEYLATCH with $FD written to $FD30/$FF08; a change calls JoyWaggle.
- `$14DA` **Jumping** – 1 from fire (hurdle events) until StepAthleteFrame returns to the running frames.
- `$14DB` **JumpTimer** – Set to 10 on a jump; stepped down by StepAthleteFrame; a new jump waits for 0.
- `$14DC` **EventActive** – 1 from before the start countdown until CheckEventEnd; with RaceRunning it gates the clock and the distance.
- `$14DD` **StepAthleteFrame** – Every 4 calls, move the athlete to the next running frame (36 bytes on), or through the jump frames and back; called each time a track mark crosses a character.
- `$1561` **ScrollStep** – ScrollScenery once and AdvanceDistance twice.
- `$156B` **FootstepTimer** – Counts athlete frames down from 6; PlayFootstep at 0.
- `$156C` **FrameStepped** – Set by StepAthleteFrame; the main loop clears it and counts FootstepTimer.
- `$156D` **RunCycleBack** – 1 while the run cycle steps back through the frames (top frame - $24 each step).
- `$156E` **InstallIrq_day_one** – Point the KERNAL IRQ vector ($0314) at IrqHandler_day_one; raster IRQ only.
- `$1584` **IrqHandler_day_one** – Raster IRQ: acknowledge, call the next split handler from SplitTable_day_one, step the split counter ($0F) through 0-12. Exits through the KERNAL's register pull.
- `$158A` **IrqSplitCall_day_one**
- `$158B` **IrqSplitCallHi_day_one**
- `$15C6` **Split01_day_one** – Top of frame: colours, DelayTicks - 1, TickRaceClock while racing.
- `$15EB` **Split02_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$15F6` **Split03_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$1601` **Split04_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$160C` **Split05_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$1621` **Split06_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$1631` **Split07_day_one** – Colours, then SoundStep_day_one.
- `$1649` **Split08_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$1654` **Split09_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$165F` **Split10_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$166A` **Split11_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$1675` **Split12_day_one** – Set the background colour(s) for the next band and the next raster line.
- `$1680` **Split13_day_one** – Colours, then MoveRace while racing.
- `$169D` **RaceRunning** – 1 from the end of the start countdown until the event ends; gates the race clock.
- `$169E` **FrameStepSeen** – Set to 1 by StepAthleteFrame; nothing reads it.
- `$169F` **ResetSpeedMeter** – Fill the meter template at $16C2 with character $21 and end mark $25, then ClearSpeedMeter.
- `$16B4` **ClearSpeedMeter** – Copy the 8 characters at $16C2 to the speed meter at $0FC6.
- `$16C2` **MeterTemplate** – The 8 speed-meter characters copied by ClearSpeedMeter.
- `$16CB` **DrawSpeedMeter** – Draw RunSpeed / 4 steps at $0FC6 with characters $21-$24, four steps to a cell.
- `$1727` **MoveTrackMarks** – Move the two marks on row 23 ($0F98) left one step: characters $3B-$3F give the sub-character positions; each whole character calls StepAthleteFrame; a mark leaving the left edge returns at column 39.
- `$176F` **RaceMoved** – Set by MoveRace each frame; ScrollTrackObjects clears it.
- `$1770` **TrackMarkColumn** – Column of each of the two track marks.
- `$1772` **TrackMarkChar** – Character ($3B-$3F) of each of the two track marks.
- `$1774` **ScrollScenery** – Rotate the scenery characters one pixel left: two passes over rows 0-7, two over rows $38-$3F.
- `$179D` **RotateCharsLeft** – Rotate seven characters' bitmaps (from $39F8, 8 bytes apart) left one pixel as one strip, rows X to $17FC - 1.
- `$17C6` **DrawSceneryRows** – Fill screen rows 12 and 13 with the repeating characters $3F-$45 and $46-$4C.
- `$17FB` **RotateCount** – Decremented by RotateCharsLeft and reset to 8 each event; nothing tests it.
- `$17FC` **RotateEnd** – RotateCharsLeft's end row (X stops here).
- `$17FF` **AdvanceDistance** – While racing, every 4 calls add 1 to the four-digit distance at $0FD0 (ASCII on screen).
- `$182D` **DistanceTimer** – Counts 4 calls of AdvanceDistance per metre.
- `$1834` **RaceClock** – Five ASCII digits, least significant first ($1834 counts 0-5, the others 0-9). Shown most significant first at $0FDD-$0FE2 by TickRaceClock.
- `$183F` **TickRaceClock** – Step RaceClock and print it; called from the split at $15C6 while RaceRunning is set.
- `$18AC` **ColourSpeedMeter** – Colour the 8 meter cells at $0BC6 with $7C, $6C ... $0C (one luminance step each).
- `$18BF` **DrawRecordPlaces** – Print 1, 2, 3 down the records box at $0CBD.
- `$18D7` **RecordTimes** – Three ASCII times per event, 7 bytes each with a 0 end: the RECORDS box. Never written.
- `$192B` **RecordEnd** – ShowRecords' end index in RecordTimes.
- `$192C` **RecordStart** – ShowRecords' start index in RecordTimes.
- `$192D` **ShowRecords** – Print the event's three RecordTimes in the RECORDS box at $0CBF.
- `$1987` **RunSpeed** – Runner's speed, 0-$70. Raised by JoyWaggle, lowered by SpeedDecay, shown by DrawSpeedMeter.
- `$1988` **SpeedUp** – RunSpeed + 1 up to $70, then redraw the meter.
- `$1996` **SpeedDecay** – Every 6 calls (3 once RunSpeed >= $60), RunSpeed - 1 down to 0, then redraw the meter.
- `$19BC` **DecayTimer** – Frames to the next SpeedDecay step (6, or 3 at RunSpeed $60 and above).
- `$19BD` **ScratchA** – Scratch: the character code in DrawSpeedMeter and DrawSceneryRows (row 12).
- `$19BE` **JoyWaggle** – Record left and right in WaggleSeen; once both are seen, RunSpeed + 5 (+2 from $40) and clear it.
- `$1A0A` **WaggleSeen** – Bit 0: right seen, bit 1: left seen, since the last speed step.
- `$1A0B` **ScratchB** – Scratch: the inverted joystick in JoyWaggle, the row 13 character in DrawSceneryRows.
- `$1A0C` **StartCountdown** – Show ON YOUR MARKS, GET SET and GO at $0E8E, waiting between them, then set RaceRunning.
- `$1A5B` **ClearMessage** – Blank the 13 characters at $0E8E.
- `$1A68` **WaitTicks** – Set DelayTicks to 100 and wait for the IRQ to count it to 0.
- `$1A73` **OnYourMarksText** – Screen codes, 13 bytes.
- `$1A80` **GetSetText** – Screen codes, 7 bytes.
- `$1A87` **GoText** – Screen codes, 2 bytes.
- `$1A89` **DelayTicks** – Counted down by the split at $15C6.
- `$1A8A` **CountdownSpare** – Cleared by StartCountdown; nothing reads it.
- `$1A8B` **CheckEventEnd** – End the event when the distance shown at $0FD1 reaches its length (with RunSpeed > 0), or when RaceClock's tens digit reaches 7; JudgeTime decides, then StartEvent_day_one.
- `$1B05` **DrawAthlete** – Draw the athlete's two 6x3-character halves at $0E5E and $0ED6 from AthleteFrames, skipping spaces; colour 8.
- `$1B6D` **FrameStepLock** – Set when StepAthleteFrame steps; EraseAthlete clears it, so one step per redraw.
- `$1B6E` **EraseAthlete** – Blank the athlete's lower half where it still holds the frame's characters, and a few fixed cells.
- `$1BCD` **ClearObjectChars** – Zero the 256 bytes of character bitmap at $3B08 used for hurdles and the finish line.
- `$1BD8` **InitTrackObjects** – Set the first track object's position and timers, then fall into ScrollTrackObjects.
- `$1BF1` **ScrollTrackObjects** – Move the hurdles (and the finish line once shown) along the track and redraw them into the object characters.
- `$1C9C` **ObjectRowsLeft** – Rows left to draw of the object's 4x4 cells.
- `$1C9D` **ObjectDrawn** – Non-zero once the object's cells are on screen, so ScrollTrackObjects writes them again.
- `$1C9E` **ObjectX** – Pixel position of the track object (hurdle or line), from $F8 moving left 8 per step.
- `$1CA6` **ObjectY** – Pixel row of the track object ($90); its character row picks the screen row.
- `$1CAE` **ObjectIndex** – Index of the track object; always 0 (one object).
- `$1CAF` **NextObjectChar** – Next object character code to place ($61 upwards).
- `$1CB0` **ObjectEndCol** – Column after the object's last cell in the row.
- `$1CB1` **BitmapIndex** – CopyCellBitmaps' write index in UnderBitmaps, counting down from $7F.
- `$1CB2` **AnimTimer** – Counts down to the next athlete frame (4, or $18 at the start of a jump).
- `$1CB5` **AthleteTopFrame** – Offset in AthleteFrames of the top half.
- `$1CB6` **AthleteBottomFrame** – Offset in AthleteFrames of the bottom half.
- `$1CB7` **AthleteHalf** – 0: DrawAthlete draws the top half next, 1: the bottom half.
- `$1CB8` **UnderCells** – Screen codes of the 16 cells under the object, read by ReadObjectCells.
- `$1CC8` **ObjectCells** – Codes WriteObjectCells puts in the 16 cells.
- `$1CF8` **ObjectColours** – Colours WriteObjectCells puts in the 16 cells.
- `$1D08` **PixelMasks** – $80 down to $01: the bit for each pixel column.
- `$1D21` **UnderBitmaps** – Bitmaps of the 16 characters under the object (128 bytes).
- `$1E21` **RowAddrHi** – High byte of the screen address of rows 0-25, column 2.
- `$1E3B` **RowAddrLo** – Low byte of the same addresses.
- `$1E55` **RowsLeft** – Rows left in DrawAthlete and EraseAthlete (3).
- `$1E56` **AthleteFrames** – Character codes of the athlete's frames, 18 bytes (6x3) per half.
- `$1F52` **RedrawObject** – Read the screen cells under the object, rebuild their character bitmaps with the object merged in (CheckHurdleHit, MergeObjectChars).
- `$1F67` **CopyCellBitmaps** – Copy the bitmaps of the 16 characters under the object into the buffer at $1D21.
- `$1F9F` **ReadObjectCells** – Copy the screen codes of the object's 4x4 cells (pointer $02/$03) to $1CB8.
- `$1FD2` **ObjectPtrUp3** – Move the cell pointers at $02/$04 back three rows ($78).
- `$1FE2` **MergeObjectChars** – Object characters $3B08-$3B87 = buffer $1D21 OR the object bitmap at $3B88.
- `$1FF1` **WriteObjectCells** – Write the object's character codes ($1CC8) and colours ($1CF8) to its 4x4 cells.
- `$2032` **HurdleState** – 0: no hurdles (flat events); 2: set by StartEvent_day_one for the hurdle events; 1: the hurdle reached the athlete ($26-$43) while not Jumping. Picks the bitmap drawn.
- `$2033` **CopyObjectCells** – Copy the 16 cell codes from $1CB8 to $1CC8.
- `$203F` **HurdleSpare** – Set to 8 by both hurdle drawers; nothing reads it.
- `$2043` **CheckHurdleHit** – Set HurdleState from ObjectX and Jumping, then draw the hurdle bitmap it selects.
- `$2078` **DrawHurdleA** – ClearObjectChars, then copy the bitmap set from $3900-$394F into the object characters.
- `$20A4` **DrawHurdleB** – ClearObjectChars, then copy the bitmap set from $3950-$396F into the object characters.
- `$2111` **MoveRace** – Once a frame while racing (last split): from RunSpeed, move the track marks and objects (whole steps plus a fractional accumulator) and scroll the scenery and distance.
- `$217B` **MarkSteps** – RunSpeed / 32: whole MoveTrackMarks steps this frame.
- `$217C` **SpeedDiv64** – RunSpeed / 64; nothing reads it.
- `$217D` **SceneSteps** – RunSpeed / 128: whole ScrollStep steps this frame.
- `$217E` **SpeedFraction** – RunSpeed, added to the two fraction accumulators.
- `$217F` **SpeedCopy** – RunSpeed; nothing reads it.
- `$2180` **SpeedHalf** – RunSpeed / 2; nothing reads it.
- `$2181` **MarkFraction** – Fraction accumulator: a carry moves the track marks one more step.
- `$2183` **SceneFraction** – Fraction accumulator: a carry scrolls the scenery one more step.
- `$2184` **ShowQualifyTime** – Pick QualifyIndex for EventNumber and print the time at $0C40.
- `$21C0` **QualifyIndex** – Offset of this event's entry in QualifyTimes: 0, 12, 6, 18 for events 1-4.
- `$21C1` **QualifyTimes** – Four 6-character ASCII times: 013:00, 060:00, 015:00, 038:00.
- `$21D9` **TimeToJudge** – RaceClock copied into QualifyTimes' layout.
- `$21DF` **JudgeTime** – Compare the time with QualifyTimes: under it, QUALIFIED and AwardTimeBonus; over it, FAILED and one of Lives lost.
- `$222E` **QualifiedText** – Screen codes, 9 bytes.
- `$2237` **FailedText** – Screen codes, 6 bytes.
- `$2259` **PlotObjectPixel** – Set pixel (PlotX, PlotY) in the object character bitmap at $3B08 (mask from $1D08).
- `$2289` **PlotOffset** – PlotObjectPixel's byte offset in ObjectChars.
- `$228A` **PlotY**
- `$228B` **PlotX**
- `$228C` **LineStepX** – DrawFinishLine's X and Y fraction steps ($FF), accumulators and pixel count.
- `$228D` **LineStepY**
- `$228E` **LineFracX**
- `$228F` **LineFracY**
- `$2290` **LineLength**
- `$2291` **DrawFinishLine** – Plot the slanted finish line, 12 steps of two pixels, from row $0D.
- `$22D8` **WrapEvents** – After the fourth event: EventNumber 0, so StartEvent_day_one starts the 100 m again.
- `$22E0` **SoundVectors_day_one** – Jump table into the sound driver (same layout as part 2's at $1800). $22E3 has no caller in part 1; its target matches the part 2 routine at $1CA2. TODO(name)
- `$22E6` **PlayStartTune** – PlayTunePair_day_one with the tune at $2523/$258F; called by StartEvent_day_one.
- `$22EE` **PlayGameOverTune** – PlayTunePair_day_one with $2405/$24B6; called by ShowGameOver.
- `$22FE` **PlayQualifiedSound** – StartSoundEffect with the record at $2322.
- `$2306` **PlayFailedSound** – StartSoundEffect with the record at $2339.
- `$230E` **PlayFootstep** – StartSoundEffect with the record at $2350, its pitch byte taken from the next byte of the BASIC ROM (self-modified pointer from $A000).
- `$230F` **FootstepRomPtr** – Low byte of PlayFootstep's LDA $A000 operand, stepped each call.
- `$2350` **FootstepFx** – PlayFootstep's 23-byte effect record; byte 12, its pitch, comes from the BASIC ROM.
- `$2657` **Fx1SweepLen_day_one** – Steps in each of the three pitch-sweep segments
- `$2658` **Fx1SweepLenB_day_one**
- `$2659` **Fx1SweepLenC_day_one**
- `$265A` **Fx1StartDelay_day_one** – Frames before the sweep starts
- `$265B` **Fx1SweepRate_day_one** – Frames between sweep steps
- `$265C` **Fx1SweepMode_day_one** – After the three segments: 0 stop, positive repeat, negative restart from StartFreq
- `$265D` **Fx1SweepStepLo_day_one** – Three signed words added to Freq, one per segment
- `$265E` **Fx1SweepStepHi_day_one**
- `$2663` **Fx1StartFreqLo_day_one** – Starting TED frequency (a tune note's NoteFreqLo/Hi)
- `$2664` **Fx1StartFreqHi_day_one**
- `$2665` **Fx1AttackStep_day_one** – Level added per envelope tick until PeakLevel
- `$2666` **Fx1PeakLevel_day_one**
- `$2667` **Fx1DecayStep_day_one** – Level taken per tick down to SustainLevel
- `$2668` **Fx1SustainLevel_day_one**
- `$2669` **Fx1ReleaseStep_day_one** – Level taken per tick in the release
- `$266A` **Fx1NoteTicks_day_one** – Envelope ticks before the release
- `$266B` **Fx1ReleaseTicks_day_one** – Ticks the release lasts
- `$266C` **Fx1EnvRate_day_one** – Frames per envelope tick
- `$266D` **Fx1VoiceBits_day_one** – Record byte $16 AND $F0: the voice/waveform bits ORed into $FF11
- `$266E` **Fx1SweepCount_day_one** – Steps left in each segment
- `$266F` **Fx1SweepCountB_day_one**
- `$2670` **Fx1SweepCountC_day_one**
- `$2671` **Fx1EnvTimer_day_one** – Frames to the next envelope tick
- `$2672` **Fx1SweepTimer_day_one** – Frames to the next sweep step
- `$2673` **Fx1FreqLo_day_one** – Current TED frequency
- `$2674` **Fx1FreqHi_day_one**
- `$2675` **Fx1EnvPhase_day_one** – $FC attack, $FD decay, $FE hold, $FF release, 0 off
- `$2676` **Fx1Level_day_one** – Current volume (0-15), the louder voice's goes to $FF11
- `$2677` **Fx2SweepLen_day_one**
- `$2678` **Fx2SweepLenB_day_one**
- `$2679` **Fx2SweepLenC_day_one**
- `$267A` **Fx2StartDelay_day_one**
- `$267B` **Fx2SweepRate_day_one**
- `$267C` **Fx2SweepMode_day_one**
- `$267D` **Fx2SweepStepLo_day_one**
- `$267E` **Fx2SweepStepHi_day_one**
- `$2683` **Fx2StartFreqLo_day_one**
- `$2684` **Fx2StartFreqHi_day_one**
- `$2685` **Fx2AttackStep_day_one**
- `$2686` **Fx2PeakLevel_day_one**
- `$2687` **Fx2DecayStep_day_one**
- `$2688` **Fx2SustainLevel_day_one**
- `$2689` **Fx2ReleaseStep_day_one**
- `$268A` **Fx2NoteTicks_day_one**
- `$268B` **Fx2ReleaseTicks_day_one**
- `$268C` **Fx2EnvRate_day_one**
- `$268D` **Fx2VoiceBits_day_one**
- `$268E` **Fx2SweepCount_day_one**
- `$268F` **Fx2SweepCountB_day_one**
- `$2690` **Fx2SweepCountC_day_one**
- `$2691` **Fx2EnvTimer_day_one**
- `$2692` **Fx2SweepTimer_day_one**
- `$2693` **Fx2FreqLo_day_one**
- `$2694` **Fx2FreqHi_day_one**
- `$2695` **Fx2EnvPhase_day_one**
- `$2696` **Fx2Level_day_one**
- `$2697` **StartSoundEffect** – Copy the 23-byte effect record at Y:X into the driver; byte $16 picks the voice.
- `$26FB` **StepEnvelope_day_one** – Step one voice's volume envelope (X = 0 voice 1, $20 voice 2): rise by the attack step to the peak, fall by the decay step to the sustain level, hold, then release to 0.
- `$2783` **SoundSilence_day_one** – Clear the sound driver's tables and zero $FF0E-$FF11 and the voice 1 high bits in $FF12. Reached only through SoundVectors_day_one+3, which part 1 never calls.
- `$27C6` **SoundStep_day_one** – Sound driver step, called from the raster split at $1631. TODO(name)
- `$2ADD` **TuneInstrument1_day_one** – Voice 1's 23-byte effect record, loaded by the tune commands $FB-$FD; StartSoundEffect plays it.
- `$2AE9` **TuneNoteLo1_day_one** – Voice 1's note frequency in the record, from NoteFreqLo/Hi.
- `$2AEA` **TuneNoteHi1_day_one**
- `$2AF4` **TunePlaying1_day_one** – Non-zero while voice 1's tune runs; cleared by $FF at call depth 0.
- `$2AF5` **TuneWait1_day_one** – Frames left of voice 1's current note.
- `$2AF6` **TuneDepth1_day_one** – Voice 1's call stack index ($0F empty); the 16 bytes after it are the note lengths, indexed 1-16.
- `$2B07` **TuneReturnLo1_day_one** – Voice 1's call return addresses, low bytes.
- `$2B17` **TuneReturnHi1_day_one** – Voice 1's call return addresses, high bytes.
- `$2B27` **TuneInstrument2_day_one** – Voice 2's 23-byte effect record.
- `$2B33` **TuneNoteLo2_day_one** – Voice 2's note frequency in the record.
- `$2B34` **TuneNoteHi2_day_one**
- `$2B3E` **TunePlaying2_day_one** – Non-zero while voice 2's tune runs.
- `$2B3F` **TuneWait2_day_one** – Frames left of voice 2's current note.
- `$2B40` **TuneDepth2_day_one** – Voice 2's call stack index ($0F empty); the 16 bytes after it are its note lengths.
- `$2B51` **TuneReturnLo2_day_one** – Voice 2's call return addresses, low bytes.
- `$2B61` **TuneReturnHi2_day_one** – Voice 2's call return addresses, high bytes.
- `$2B71` **NoteFreqLo_day_one** – TED frequency of 35 notes, A2 to G5 a semitone apart, low bytes (note 0 = $007, 110 Hz).
- `$2B94` **NoteFreqHi_day_one** – The same notes' high bits (0-3).
- `$2BB7` **PlayTunePair_day_one** – Take two inline words after the JSR (copied to $12-$15), start both voices, return past them. TODO(name): the words look like voice 1 and voice 2 data pointers.
- `$3900` **BlankChar** – Character $20 of the $3800 set: blank.
- `$3930` **HurdleArt** – Characters $26-$2D of the $3800 set: the pieces the hurdle drawers copy.
- `$39F8` **SceneryChars** – Characters $3F-$45 of the $3800 set: the scenery strip RotateCharsLeft scrolls.
- `$3B08` **ObjectChars** – Characters $61-$70: the 16 cells under the object, rebuilt with it merged in.
- `$3B88` **ObjectBitmap** – Characters $71-$80: the hurdles and finish line are drawn here, then merged into ObjectChars.

---

## Part 2 (Day Two)

Block `day_two`, from `original/day_two_unpacked_vice.prg`. Source `src/day_two.s`.

### Declared Data

- `$21C7`–`$21F8` **ScreenRowTable** (WordTable) – Screen address of each of the 25 rows ($0C00 + 40 * row)
- `$23EE`–`$23FA` **SplitRasters_day_two** (ByteTable) – Raster line of each split (13 entries)
- `$23FB`–`$2414` **SplitTable_day_two** (AddrTable) – Raster-split handlers, called in turn by the IRQ (13 entries)
- `$2D3B`–`$2DBA` **MarkerShapes** (ByteTable) – Runway marker patterns: two sets of 4 positions x 16 bytes (two characters interleaved)
- `$2E87`–`$2EA4` **TopFrameTable** (AddrTable) – Addresses of the athlete's 15 top-half frames, 144 bytes each
- `$2EA5`–`$2EB6` **BottomFrameTable** (AddrTable) – Addresses of the athlete's 9 bottom-half frames, 144 bytes each
- `$2F14`–`$2F19` **EventJumpTable_day_two** (AddrTable) – Per-event handler, indexed by $42; patched into the JMP at $2F11 (3 entries)
- `$326D`–`$3275` **DistanceRates** (ByteTable) – Per event, 3 bytes: tenths per cell, random mask, hundredths base. Long jump 1/1/0, shot-put 2/3/0, javelin 7/3/0.

### Names

- `$002D` **BoardFineScroll** – Fine horizontal scroll (0-7) of the advert boards, written to $FF07 by split 1.
- `$002E` **BoardScrollSpeed** – Pixels the boards move a frame (1 means every other frame); 3 on the title screen.
- `$002F` **BoardScrollTemp** – StepBoardScroll's working copy of the step.
- `$0030` **BoardFrameToggle** – Counted each frame at speed 1; the boards move on even counts.
- `$0031` **NextBoardChar** – Next advertising-board character ScrollAdvertBoards writes at the right edge: $80-$B9, with $3A added for the bottom row.
- `$0032` **RunwayFineScroll** – TED fine scroll (0-7) of the runway band.
- `$0033` **RunwayScrollStep** – Runway scroll per frame plus 1 (0 stops it); set from TakeOffSpeed in flight.
- `$0036` **RunwayBandColour** – Background colour Split09_day_two gives the runway band: $32 (red track), $67 (yellow sand) once AdvanceAthlete has carried the jumper below AthleteX $10.
- `$0037` **RunSpeed_day_two** – 0-$1F: raised by SpeedUp_day_two, lowered by SpeedDecay_day_two.
- `$0038` **AthleteCol** – Screen column of the athlete's 6x6 block (DrawAthlete_day_two).
- `$0039` **AthleteRow** – Screen row of the athlete's 6x6 block.
- `$0040` **WaggleSeen_day_two** – Bit 0: left seen, bit 1: right seen, since the last speed step.
- `$0041` **InputBits** – Bit 7 fire, bit 3 right, bit 2 left (1 = pressed), from the joystick or the keys.
- `$0042` **EventIndex** – 0-2: the event being run; indexes EventTableOffset and EventJumpTable_day_two.
- `$0049` **RunUpMetres** – Metres to the line in BCD (30, 20, 30 by event), printed on row 23 and lowered by 10 every 120 runway cells.
- `$004A` **LineDue** – Set when the run-up has scrolled 120 cells; ApproachLine then brings the line in.
- `$004B` **LineInView** – Set by ApproachLine; from then on fire counts and the athlete runs on to the line.
- `$004C` **AthleteX** – Athlete's position along the runway; DrawRunway and AdvanceAthlete use it; below $50 at the line is a foul ($2CA1).
- `$004D` **MarkerSubCell** – AthleteX AND 3: the pixel offset ShiftRunwayMarker draws.
- `$004E` **RunwayCellCount** – Counts runway characters scrolled in flight; every 14th ($0E) puts a marker at the right edge and adds no distance.
- `$004F` **AttemptNumber** – 0-2: the attempt at this event.
- `$0050` **RunUpActive** – 1 while JoyWaggle_day_two may raise RunSpeed_day_two.
- `$0051` **RunUpScrolling** – Set during the run-up, when the runway scrolls with RunSpeed_day_two; cleared at take-off, after which each scrolled cell goes to RunwayCellStep.
- `$0053` **AttemptResult** – 1: the attempt beat the qualifying length; $FF: it did not (or a foul).
- `$0054` **AttemptResults** – Three bytes, one per attempt: 0 qualified, 1 not, $FF not yet taken.
- `$005B` **ColumnStepCount** – Counts SpeedUp_day_two calls; every 6th moves the athlete (and shot or javelin) one column right, up to column $0E.
- `$005C` **NextAthleteCol** – Column MoveAthlete_day_two draws the athlete at next.
- `$005D` **NextAthleteRow** – Row MoveAthlete_day_two draws the athlete at next; the long jump's height.
- `$005E` **DrawnAthleteCol** – Column the athlete was last drawn at.
- `$005F` **DrawnAthleteRow** – Row the athlete was last drawn at.
- `$0060` **AthleteMoves** – Non-zero: UpdateFigures runs MoveAthlete_day_two each pass.
- `$0065` **AngleBcd** – Take-off angle in BCD, 20-83, raised while fire is held.
- `$0066` **Angle** – Take-off angle in binary, 20-83.
- `$0067` **TakeOffSpeed** – RunSpeed_day_two when the run-up ended.
- `$0068` **JavelinDrawnCol** – Column the javelin was last drawn at.
- `$0069` **JavelinDrawnY** – Pixel row the javelin was last drawn at.
- `$006A` **JavelinCol** – Javelin column; follows the athlete during the run-up.
- `$006B` **JavelinY** – Javelin pixel row: $68 at the start, down to PeakRow in flight, landed at $96.
- `$006C` **JavelinShown** – Non-zero in the javelin: DrawJavelinShaft draws it.
- `$006D` **JavelinChar** – DrawJavelinShaft: next character code, counting down from the phase's first.
- `$006F` **ShotDrawnCol** – Column the shot was last drawn at.
- `$0070` **ShotDrawnY** – Pixel row the shot was last drawn at.
- `$0071` **ShotCol** – Shot column; follows the athlete during the run-up.
- `$0072` **ShotY** – Shot pixel row: $70 at the start, down to PeakRow in flight, landed at $9B.
- `$0073` **ShotShown** – Non-zero in the shot-put: DrawShotBall draws it.
- `$0074` **PeakRow** – Top of the flight, lower (higher on screen) for a steeper Angle: a character row for the long jumper, a pixel row for the shot and javelin.
- `$0075` **FlightStep** – Event handlers: the RunwayScrollStep being built from TakeOffSpeed.
- `$0076` **ShotFalling** – Shot-put: 0 rising, 1 falling.
- `$0077` **JavelinPhase** – Javelin: 0 rising, 1 at the top, 2 falling, 3 nose-down from row $8C; picks its characters (JavelinChars).
- `$0078` **TakeOffDelay** – Runway cells to pass before the distance counts: AthleteX / 4 - $13 at take-off.
- `$0079` **AngleClass** – 1 below 35 degrees, 2 from 35, 3 from 55; set by ClassifyAngle.
- `$007B` **CarryFrame** – Shot and javelin: fixed run-up frame $0A, $0B at the throw (bottom half left as is); 0 in the long jump, which runs the full cycle.
- `$007C` **JavelinHang** – Steps the javelin stays level at the top: (TakeOffSpeed & $1C) / 2 + 6.
- `$007F` **TitleMode** – 1 on the FIRE TO START screen, 0 in play.
- `$0082` **HangTime** – Steps the long jumper stays at the top: (TakeOffSpeed & $1C) / 2 + 2.
- `$0083` **FlightPhase** – Long jump: 0 rising, 1 at the top, 2 falling.
- `$0084` **FlightTopFrame** – Top-half frame while InFlight.
- `$0085` **FlightBottomFrame** – Bottom-half frame while InFlight.
- `$0086` **InFlight** – Set by LongJump: frames come from FlightTopFrame/FlightBottomFrame and each scrolled cell runs AdvanceAthlete.
- `$0087` **Every7Count** – Countdown for Every7Rising and Every7Falling.
- `$0800` **ColourRam** – Colour RAM, $0800-$0BFF. At load it holds ADDS, which Entry_day_two copies to $0400.
- `$0C00` **ScreenRam** – Screen RAM, $0C00-$0FFF.
- `$10D8` **MarkerCharA** – Character $1B of the $1000 set: the runway marker's left half, rebuilt by ShiftRunwayMarker.
- `$10E0` **MarkerCharB** – Character $1C: the marker's right half.
- `$1350` **ShotChar** – Character $6A of the $1000 set: DrawShotBall clears it and redraws ShotBitmap at the shot's pixel row within the cell.
- `$1518` **AthleteTopChars** – Characters $A3-$B4: the athlete's top half, copied from the current frame.
- `$15A8` **AthleteBottomChars** – Characters $B5-$C6: the athlete's bottom half.
- `$17F8` **FillChar** – Character $FF, filled with FillCharPattern for the event.
- `$1800` **SoundVectors_day_two** – Jump table into the sound driver. TODO(name)
- `$1803` **SilenceSound** – Jump to SoundSilence_day_two (vector at $1803).
- `$1806` **PlayEventTune** – PlayTunePair_day_two with the tune at $1A43/$1AAF; called as an event is drawn.
- `$180E` **PlayTitleTune** – PlayTunePair_day_two with $1925/$19D6; repeated on the FIRE TO START screen.
- `$1816` **PlayQualifiedTune** – PlayTunePair_day_two with $1B05/$1B41; called after a qualified attempt.
- `$181E` **SoundEffectA_day_two** – StartSoundEffect_day_two with the record at $1842; called when AttemptResult is not $FF.
- `$1826` **SoundEffectB_day_two** – StartSoundEffect_day_two; called when AttemptResult is $FF, with ShowFailMessage.
- `$182E` **PlayFootstep_day_two** – StartSoundEffect_day_two with a pitch byte from the BASIC ROM (self-modified pointer from $A063).
- `$182F` **FootstepRomPtr_day_two** – Low byte of PlayFootstep_day_two's LDA $A063 operand, stepped each call.
- `$1870` **FootstepFx_day_two** – PlayFootstep_day_two's 23-byte effect record; byte 12, its pitch, comes from the BASIC ROM.
- `$1B77` **Fx1SweepLen_day_two** – Steps in each of the three pitch-sweep segments
- `$1B78` **Fx1SweepLenB_day_two**
- `$1B79` **Fx1SweepLenC_day_two**
- `$1B7A` **Fx1StartDelay_day_two** – Frames before the sweep starts
- `$1B7B` **Fx1SweepRate_day_two** – Frames between sweep steps
- `$1B7C` **Fx1SweepMode_day_two** – After the three segments: 0 stop, positive repeat, negative restart from StartFreq
- `$1B7D` **Fx1SweepStepLo_day_two** – Three signed words added to Freq, one per segment
- `$1B7E` **Fx1SweepStepHi_day_two**
- `$1B83` **Fx1StartFreqLo_day_two** – Starting TED frequency (a tune note's NoteFreqLo/Hi)
- `$1B84` **Fx1StartFreqHi_day_two**
- `$1B85` **Fx1AttackStep_day_two** – Level added per envelope tick until PeakLevel
- `$1B86` **Fx1PeakLevel_day_two**
- `$1B87` **Fx1DecayStep_day_two** – Level taken per tick down to SustainLevel
- `$1B88` **Fx1SustainLevel_day_two**
- `$1B89` **Fx1ReleaseStep_day_two** – Level taken per tick in the release
- `$1B8A` **Fx1NoteTicks_day_two** – Envelope ticks before the release
- `$1B8B` **Fx1ReleaseTicks_day_two** – Ticks the release lasts
- `$1B8C` **Fx1EnvRate_day_two** – Frames per envelope tick
- `$1B8D` **Fx1VoiceBits_day_two** – Record byte $16 AND $F0: the voice/waveform bits ORed into $FF11
- `$1B8E` **Fx1SweepCount_day_two** – Steps left in each segment
- `$1B8F` **Fx1SweepCountB_day_two**
- `$1B90` **Fx1SweepCountC_day_two**
- `$1B91` **Fx1EnvTimer_day_two** – Frames to the next envelope tick
- `$1B92` **Fx1SweepTimer_day_two** – Frames to the next sweep step
- `$1B93` **Fx1FreqLo_day_two** – Current TED frequency
- `$1B94` **Fx1FreqHi_day_two**
- `$1B95` **Fx1EnvPhase_day_two** – $FC attack, $FD decay, $FE hold, $FF release, 0 off
- `$1B96` **Fx1Level_day_two** – Current volume (0-15), the louder voice's goes to $FF11
- `$1B97` **Fx2SweepLen_day_two**
- `$1B98` **Fx2SweepLenB_day_two**
- `$1B99` **Fx2SweepLenC_day_two**
- `$1B9A` **Fx2StartDelay_day_two**
- `$1B9B` **Fx2SweepRate_day_two**
- `$1B9C` **Fx2SweepMode_day_two**
- `$1B9D` **Fx2SweepStepLo_day_two**
- `$1B9E` **Fx2SweepStepHi_day_two**
- `$1BA3` **Fx2StartFreqLo_day_two**
- `$1BA4` **Fx2StartFreqHi_day_two**
- `$1BA5` **Fx2AttackStep_day_two**
- `$1BA6` **Fx2PeakLevel_day_two**
- `$1BA7` **Fx2DecayStep_day_two**
- `$1BA8` **Fx2SustainLevel_day_two**
- `$1BA9` **Fx2ReleaseStep_day_two**
- `$1BAA` **Fx2NoteTicks_day_two**
- `$1BAB` **Fx2ReleaseTicks_day_two**
- `$1BAC` **Fx2EnvRate_day_two**
- `$1BAD` **Fx2VoiceBits_day_two**
- `$1BAE` **Fx2SweepCount_day_two**
- `$1BAF` **Fx2SweepCountB_day_two**
- `$1BB0` **Fx2SweepCountC_day_two**
- `$1BB1` **Fx2EnvTimer_day_two**
- `$1BB2` **Fx2SweepTimer_day_two**
- `$1BB3` **Fx2FreqLo_day_two**
- `$1BB4` **Fx2FreqHi_day_two**
- `$1BB5` **Fx2EnvPhase_day_two**
- `$1BB6` **Fx2Level_day_two**
- `$1BB7` **StartSoundEffect_day_two** – Copy the 23-byte effect record at Y:X into the driver; byte $16 picks the voice.
- `$1C1A` **StepEnvelope_day_two** – Step one voice's volume envelope (X = 0 voice 1, $20 voice 2): rise by the attack step to the peak, fall by the decay step to the sustain level, hold, then release to 0.
- `$1CA2` **SoundSilence_day_two** – Clear the sound driver's tables and zero $FF0E-$FF11 and the voice 1 high bits in $FF12.
- `$1CE4` **SoundStep_day_two** – Sound driver step, called from the last raster split. TODO(name)
- `$1FFB` **TuneInstrument1_day_two** – Voice 1's 23-byte effect record, loaded by the tune commands $FB-$FD; StartSoundEffect plays it.
- `$2007` **TuneNoteLo1_day_two** – Voice 1's note frequency in the record, from NoteFreqLo/Hi.
- `$2008` **TuneNoteHi1_day_two**
- `$2012` **TunePlaying1_day_two** – Non-zero while voice 1's tune runs; cleared by $FF at call depth 0.
- `$2013` **TuneWait1_day_two** – Frames left of voice 1's current note.
- `$2014` **TuneDepth1_day_two** – Voice 1's call stack index ($0F empty); the 16 bytes after it are the note lengths, indexed 1-16.
- `$2025` **TuneReturnLo1_day_two** – Voice 1's call return addresses, low bytes.
- `$2035` **TuneReturnHi1_day_two** – Voice 1's call return addresses, high bytes.
- `$2045` **TuneInstrument2_day_two** – Voice 2's 23-byte effect record.
- `$2051` **TuneNoteLo2_day_two** – Voice 2's note frequency in the record.
- `$2052` **TuneNoteHi2_day_two**
- `$205C` **TunePlaying2_day_two** – Non-zero while voice 2's tune runs.
- `$205D` **TuneWait2_day_two** – Frames left of voice 2's current note.
- `$205E` **TuneDepth2_day_two** – Voice 2's call stack index ($0F empty); the 16 bytes after it are its note lengths.
- `$206F` **TuneReturnLo2_day_two** – Voice 2's call return addresses, low bytes.
- `$207F` **TuneReturnHi2_day_two** – Voice 2's call return addresses, high bytes.
- `$208F` **NoteFreqLo_day_two** – TED frequency of 35 notes, A2 to G5 a semitone apart, low bytes (note 0 = $007, 110 Hz).
- `$20B2` **NoteFreqHi_day_two** – The same notes' high bits (0-3).
- `$20D5` **PlayTunePair_day_two** – Take two inline words after the JSR (copied to $12-$15), start both voices, return past them. TODO(name): the words look like voice 1 and voice 2 data pointers.
- `$2111` **Entry_day_two** – Entry point of part 2 (the decruncher's final JMP): copy $0800-$0BDF to $0400-$07DF, ten NOPs, reset the stack, go to InitGame_day_two.
- `$213F` **InputMode** – 1: joystick, 0: keys. Set by SelectInputMode.
- `$2164` **DelayXY** – Busy-wait: X outer loops of 256 inner loops.
- `$2170` **ClearZeroPage** – Zero $02-$FF.
- `$217A` **ClearScreen** – Fill screen $0C00-$0FFF with spaces and colour $0800-$0BFF with $71, then zero $0DB8-$0E07.
- `$21A6` **ScreenAddress** – Row Y, column X -> screen pointer $21/$22 (copy in $23) and colour pointer $23/$24.
- `$21F9` **BcdToAscii** – A (BCD) to two ASCII digits: X tens, Y units.
- `$220A` **WaitTuneEnd** – Wait until TunePlaying1_day_two and TunePlaying2_day_two are both 0.
- `$2213` **Split01_day_two** – Fine scroll from $2D, colours, PollInput_day_two.
- `$223A` **Split02_day_two** – Raster split: colours or scroll for the next band.
- `$2243` **Split03_day_two** – Raster split: colours or scroll for the next band.
- `$224D` **Split04_day_two** – Raster split: colours or scroll for the next band.
- `$2257` **Split05_day_two** – Raster split: colours or scroll for the next band.
- `$2261` **Split06_day_two** – Raster split: colours or scroll for the next band.
- `$226F` **Split07_day_two** – Raster split: colours or scroll for the next band.
- `$228D` **Split08_day_two** – Raster split: colours or scroll for the next band.
- `$229B` **Split09_day_two** – Raster split: colours or scroll for the next band.
- `$22B6` **Split10_day_two** – Raster split: colours or scroll for the next band.
- `$22D1` **Split11_day_two** – Raster split: colours or scroll for the next band.
- `$22EC` **Split12_day_two** – Raster split: colours or scroll for the next band.
- `$2302` **Split13_day_two** – Raster split: colours or scroll for the next band.
- `$2333` **InstallIrq_day_two** – Point the KERNAL IRQ vector ($0314) at IrqHandler_day_two; raster IRQ at line $2E.
- `$234E` **IrqHandler_day_two** – Raster IRQ: acknowledge, save $21-$24, call the next split handler from SplitTable_day_two, set the next raster line from SplitRasters_day_two.
- `$2374` **IrqSplitCall_day_two**
- `$2375` **IrqSplitCallHi_day_two**
- `$2392` **ReadInput** – Set InputBits from the joystick ($FD to $FF08) or, with InputMode 0, from three keys.
- `$23BA` **ReadKeys** – Test the three keys in KeyColumns/KeyRows and set the matching KeyBits in InputBits.
- `$23D6` **TestKey** – Select keyboard row Y, test column mask A; carry set if the key is down.
- `$23E5` **KeyColumns** – Column mask of each of the three keys.
- `$23E8` **KeyRows** – Row select of each of the three keys.
- `$23EB` **KeyBits** – InputBits bit for each key: left, right, fire.
- `$2415` **RowOffsets** – $00, $28, $50, $78, $A0: five row offsets 40 apart, for DrawEventScreen.
- `$241A` **EventTableOffset** – Offset of each event's entry in the distance tables: 0, 5, 10. The bytes after them, from $241D, are a routine nothing calls (see docs/quirks.md).
- `$2437` **InitGame_day_two** – Clear zero page, silence the sound, set up, install the IRQ, go to $2584.
- `$244B` **StartEvent_day_two** – Mark all three attempts not taken, draw the event, then run the attempts.
- `$2478` **StartAttempt_day_two** – Reset the distance and the athlete, draw the screen, wait for the run-up to end.
- `$2584` **StartGame_day_two** – Reset scores and state, draw the screen, play a tune until fire. TODO(name)
- `$25E8` **StepBoardScroll** – Move the boards' fine scroll by BoardScrollSpeed; when it wraps, shift the boards a character.
- `$260E` **ScrollAdvertBoards** – Shift the two advert-board rows ($0DB8, $0DE0) and their colours left one character.
- `$266F` **BoardStarts** – First character of each of the six advertising boards.
- `$2675` **BoardColours** – Colour of each board, written when its first character scrolls in.
- `$267B` **ScrollRunway** – Once a frame: fine-scroll the runway by RunwayScrollStep - 1 pixels; each whole character shifts the runway row and runs RunwayCellStep.
- `$2702` **RunwayCellStep** – Per runway character: AdvanceAthlete if moving, count RunwayCellCount, AddFlightDistance.
- `$2724` **AdvanceAthlete** – AthleteX - 2 and redraw the runway, until it is below $10.
- `$2739` **SetupTed_day_two** – Character set, multicolour and the first raster line for part 2.
- `$2758` **DrawScoreLine** – Draw the 13 AngleDigits as two-row large digits (characters $40 + 2n) on rows 23-24.
- `$2772` **AngleDigits** – Two ASCII digits of the take-off angle, then AttemptDistance and Score_day_two: 13 digits drawn by DrawScoreLine.
- `$2774` **AttemptDistance** – Five ASCII digits, metres to hundredths (shown 000:00).
- `$2779` **Score_day_two** – Six ASCII digits; AddDistanceToScore adds the distance to it.
- `$277F` **ScoreLineColumns** – Screen column of each digit DrawScoreLine prints.
- `$278C` **DrawSpeedMeterFrame** – Characters $6C/$6D and colours from $27DF for the 9 meter cells on rows 23-24.
- `$27A6` **DrawSpeedMeter_day_two** – Eight meter cells from RunSpeed_day_two: full cells for each 4, then the remainder.
- `$27D1` **SetSpeedCell** – Set meter cell X to fill level A (0-3).
- `$27DF` **MeterColours** – Colour of each speed-meter cell, $0C to $7C.
- `$27E8` **DrawScoreLabels** – Print SCORE and SPEED and the fixed marks, then DrawScoreLine and the meter.
- `$282C` **ScoreLabelText** – 'SCORE'.
- `$2831` **SpeedLabelText** – 'SPEED'.
- `$2836` **DrawAthlete_day_two** – Draw the athlete's 36 characters ($C6 down) at AthleteCol/AthleteRow, colour 8, using the cell offsets at $289C.
- `$2854` **EraseAthlete_day_two** – Blank the athlete's 36 cells.
- `$2868` **UpdateFigures** – Move the athlete if $60 is set, then draw the shot (event 1) or the javelin (event 2).
- `$2881` **MoveAthlete_day_two** – Erase, take the new column/row from $5C/$5D, redraw if changed.
- `$289C` **AthleteCellOffsets** – Screen offsets of the athlete's 36 cells: four 3x3 blocks.
- `$28C0` **DrawEventScreen** – Draw the information box, its labels, ShowEventTables and the event's scenery.
- `$2935` **WorldRecordText** – Information-box row 1, 35 bytes: 'WORLD RECORD - 000:00 METRES'.
- `$2958` **QualifyingText** – Row 2: 'QUALIFYING LENGTH - 000:00 METRES'.
- `$297B` **FoulsText** – Row 3: 'FOULS % % % BEST - 000:00 METRES'; the % are the attempt marks.
- `$29BF` **PollInput_day_two** – ReadInput, then JoyWaggle_day_two while RunUpActive.
- `$29C7` **JoyWaggle_day_two** – Record left and right in WaggleSeen_day_two; once both are seen, RunSpeed_day_two + 5 (+2 from $0C) and clear it.
- `$2A0A` **SpeedUp_day_two** – RunSpeed_day_two + 1 up to $1F; also steps the athlete's animation.
- `$2A31` **SpeedDecay_day_two** – Every 2 (joystick) or 3 (keys) calls, RunSpeed_day_two - 1 down to 0.
- `$2A4C` **WorldRecordTable** – Three 5-digit ASCII lengths shown as WORLD RECORD: 011.87, 017.60, 101.30.
- `$2A5B` **QualifyLengthTable** – Three 5-digit ASCII lengths shown as QUALIFYING LENGTH: 006.80, 013.90, 065.70.
- `$2A6A` **BestTable** – Three 5-digit ASCII lengths shown as BEST; a better attempt is copied in by JudgeAttempt.
- `$2A78` **HighScore** – Six ASCII digits; replaced by Score_day_two when that is higher.
- `$2A7E` **ShowEventTables** – Print this event's world record, qualifying length and best at $0C68, $0C90, $0CB8.
- `$2AF3` **HighText** – 'HIGH', shown with the high score.
- `$2AF7` **TitleGlyphs** – Big-font titles as glyph numbers: a start column, then glyphs, $00 a space, $FF the end. LONG JUMP, SHOT PUT, JAVELIN, FIRE TO START.
- `$2B24` **TitleOffsets** – Offset in TitleGlyphs of each title: 0, 11, 21, 30 (EventIndex + TitleMode).
- `$2B28` **CycleTitleColours** – On the FIRE TO START screen, rotate the colours of the title rows.
- `$2B96` **PulseTitleColour** – Step the luminance of row 1's colours through the table at $2BEB.
- `$2BB4` **ColourTitleRows** – On the FIRE TO START screen, set the title rows' colours from $2BCB.
- `$2BCB` **TitleColourRamp** – $02-$72: one colour at eight luminances, for the title rows.
- `$2BEB` **TitleLumaSteps** – $00-$70: the eight luminance bits PulseTitleColour cycles.
- `$2BFB` **DrawPieceList** – Draw a list of (screen address, character, ...) entries from Y:X until $FF.
- `$2C2D` **InitAthlete_day_two** – Set the athlete's frames and position for EventIndex from the tables at $2C77.
- `$2C74` **FillCharPattern** – Per event: the byte FillChar is filled with ($FF long jump, 0 others).
- `$2C77` **RunUpLengths** – Per event: RunUpMetres at the start (BCD 30, 20, 30).
- `$2C7A` **AthleteSetup** – Per event, 4 bytes: JavelinShown, ShotShown, the implement's column and its Y.
- `$2C86` **ApproachLine** – When LineDue is set, set LineInView and AthleteX $9B; then, while the run-up scrolls, draw the runway at AthleteX, or set AttemptResult $FF once AthleteX is below $50.
- `$2CAC` **DrawRunway** – Draw the athlete's position marker / runway cells on rows 22-23 for X (= $4C).
- `$2D14` **ShiftRunwayMarker** – Copy characters $1B/$1C ($10D8, $10E0) from MarkerShapes for MarkerSubCell; the long jump uses the second set (+$40).
- `$2D3C` **MarkerShapesOdd** – MarkerShapes + 1: the odd bytes, for character $1C.
- `$2DBB` **SetRunwayScroll** – From RunSpeed_day_two, set the runway scroll step $33 while $51 is set.
- `$2DD9` **ShowAttemptMarks** – Colour the three attempt marks: colour $71 qualified, $42 failed; untaken left.
- `$2DF8` **RunFrameTimer** – While moving, count $58 down and step the run cycle at 0.
- `$2E02` **StepRunFrame_day_two** – Set the frame delay from RunSpeed_day_two and step the run cycle (9 frames for the long jump); footstep sound on the first frame.
- `$2E47` **TopFramePtr** – Source of the top-half frame copy: LDA operand set from TopFrameTable.
- `$2E48` **TopFramePtrHi**
- `$2E64` **CopyBottomFrame** – Copy bottom-half frame X (FlightBottomFrame in flight) to the athlete's characters at $15A8.
- `$2E7C` **BottomFramePtr** – Source of the bottom-half frame copy: LDA operand set from BottomFrameTable.
- `$2E7D` **BottomFramePtrHi**
- `$2EB7` **SetTakeOffAngle** – At the line: count the angle up from 20 while fire is held (max 83), showing it, then jump to this event's handler through EventJump_day_two.
- `$2F11` **EventJump_day_two** – Self-modified JMP: operand set from EventJumpTable_day_two.
- `$2F12` **EventJumpTarget** – Operand of EventJump_day_two, set from EventJumpTable_day_two.
- `$2F13` **EventJumpTargetHi**
- `$2F1A` **ClassifyAngle** – Set AngleClass from Angle.
- `$2F2B` **LongJump** – Long jump flight: height and length from Angle and TakeOffSpeed.
- `$2F88` **LongJumpLoop** – One step of the long jump: rise, hang or fall, then DelayXY $14.
- `$2FE0` **LongJumpFrames** – FlightPhase x 2: top and bottom frames (0/0, $0D/$07, $0E/$08).
- `$2FE6` **Landed** – Stop the runway and judge the attempt.
- `$2FF4` **Every7Rising** – Carry set every 7th call (rising).
- `$3000` **Every7Falling** – Carry clear every 7th call (falling).
- `$300C` **ShotPut** – Shot-put throw: flight from Angle and TakeOffSpeed.
- `$3055` **ShotPutLoop** – One step of the shot: ShotY up or down by AngleClass, then DelayXY 7.
- `$308C` **Javelin** – Javelin throw: flight from Angle and TakeOffSpeed.
- `$30D9` **JavelinLoop** – One step of the javelin: JavelinY up or down by AngleClass, then DelayXY $0A.
- `$3123` **DrawJavelinShaft** – Event 2: draw the javelin's 10 cells at $68/$69 (cell offsets $3174).
- `$3174` **JavelinCellOffsets** – Screen offsets of the javelin's 10 cells: five columns, two rows.
- `$317E` **JavelinChars** – First character of the javelin's picture for each JavelinPhase.
- `$3182` **DrawShotBall** – Event 1: draw the shot at $6F/$70.
- `$31F1` **ShotBitmap** – The shot's 8-byte ball, copied into character $6A at the shot's pixel row.
- `$31F9` **FollowThrough** – Shot and javelin release: walk the athlete left to column 0, lifting the shot by AngleClass and the javelin by 1 a step and moving AthleteX - 3, then clear his rows.
- `$3236` **AddFlightDistance** – After TakeOffDelay cells, add the event's tenths (DistanceRates) and 0-1 or 0-3 random hundredths (TED timer 1) to AttemptDistance.
- `$325D` **RandomMask** – AND operand in AddFlightDistance: the event's random mask from DistanceRates.
- `$3260` **RandomBase** – ADC operand in AddFlightDistance: the event's hundredths base from DistanceRates.
- `$326D` **DistanceRates** – Per event, 3 bytes: tenths per cell, random mask, hundredths base. Long jump 1/1/0, shot-put 2/3/0, javelin 7/3/0.
- `$326E` **DistanceMasks** – DistanceRates + 1: each event's random mask.
- `$326F` **DistanceBases** – DistanceRates + 2: each event's hundredths base.
- `$3277` **AddDigit** – Add A to digit Y of AngleDigits' block with decimal carry to the left.
- `$3294` **DigitTemp** – AddDigit's value being added.
- `$3295` **JudgeAttempt** – AttemptResult 1 if the distance beats QualifyLengthTable, else $FF; copy it to BestTable if better; if qualified, compare it with WorldRecordTable.
- `$32FF` **ShowFailMessage** – Print the 8-character message at $3310 at $0E42 (custom characters).
- `$3310` **FailMessageChars** – Character codes of the failure message, drawn by ShowFailMessage.
- `$3318` **FlashAttemptMessage** – Show the 10-character message at $334A at $0E3F, flash its colour 100 times, then erase it.
- `$334A` **AttemptMessageChars** – Character codes FlashAttemptMessage draws.
- `$3354` **AddDistanceToScore** – Add the distance's first four digits to Score_day_two (metres x 10 points), then copy the score to HighScore if higher.
- `$3390` **AddScoreDigit** – Add the low nibble of A to digit Y (AddDigit).
- `$3395` **SelectInputMode** – One key sets InputMode to joystick, another to keys; print KEY or JOY at $0F99.
- `$33D5` **KeyJoyText** – 'KEY' and 'JOY', 3 bytes each, indexed by InputMode * 3.
- `$34A0` **AthleteFrames_day_two** – The athlete's frames, 144 bytes each ($34A0-$3FDF), listed in TopFrameTable and BottomFrameTable.
