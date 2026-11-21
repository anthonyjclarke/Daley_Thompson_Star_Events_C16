"""Names, ranges and comments for Daley Thompson's Star Events: the master for tools/disasm.py.

Edit this file, then run `make disasm`; never edit src/*.s by hand. Add a name only when the
evidence supports it (skill: references/shared/disassembly.md) and record why in docs/evidence.md.

LABELS: {addr: (name, block comment or '')}      RANGES: [(start, end, type, name, comment)]
INLINE: {addr: 'comment'}                          types: Code, ByteTable, WordTable, AddrTable, TextTable
A block's own "labels", "ranges" and "inline" add to the global ones (for overlapping blocks).

The four blocks overlap in memory ($1001 upwards), so every name lives in its block's own dicts.
"""

MACHINE = "c16"
TITLE = "Daley Thompson's Star Events"

# Raster-split handlers, read from each part's split table (the IRQ handler patches its own JSR).
D1_SPLITS = [0x15C6, 0x15EB, 0x15F6, 0x1601, 0x160C, 0x1621, 0x1631, 0x1649, 0x1654, 0x165F, 0x166A, 0x1675, 0x1680]
# Calls that carry two inline words after the JSR (the callee pulls its return address, copies the
# words to $12-$15 and returns past them): the words are data, the RTS after them is code.
D1_INLINE_CALLS = [0x22E6, 0x22EE, 0x22F6]
D2_INLINE_CALLS = [0x1806, 0x180E, 0x1816]


def inline_words(calls):
    return [(c + 3, c + 6, "WordTable", "", "") for c in calls]


D2_SPLITS = [0x2213, 0x223A, 0x2243, 0x224D, 0x2257, 0x2261, 0x226F, 0x228D, 0x229B, 0x22B6, 0x22D1, 0x22EC, 0x2302]

STUB = (0x1001, 0x100C, "ByteTable", "BasicStub", "BASIC line 20 SYS4109 that starts the decruncher")

BLOCKS = [
    # The crunched PRGs as they survive. Code here is only the start-up copy and the decruncher;
    # everything else is packed data until tools/unpack_sfx.py or VICE unpacks it.
    dict(name="day_one_packed", kind="prg", file="original/daley_thompsons_star_events_day_one.prg",
         entries=[0x100D], ranges=[STUB],
         labels={0x100D: ("SfxStart_day_one", "Packed part 1: copies the decruncher to the stack page. Provisional name.")}),
    dict(name="day_two_packed", kind="prg", file="original/daley_thompsons_star_events_day_two.prg",
         entries=[0x100D], ranges=[STUB],
         labels={0x100D: ("SfxStart_day_two", "Packed part 2: blanks the screen, copies the decruncher. Provisional name.")}),

    # The 1985 tape loaders (SYS 1536): load MAIN and ADDS with secondary address 0 at fixed addresses, then
    # jump to the game. tools/tape_check.py proves the tape's MAIN and ADDS are the unpacked images' bytes.
    dict(name="loader_side1", kind="c16tap", file="original/dt_star_events_side1.tap", index=0, entries=[0x0600],
         ranges=[(0x0639, 0x063D, "ByteTable", "MainName_side1", "'MAIN1' (length 5)"),
                 (0x063E, 0x0642, "ByteTable", "AddsName_side1", "'ADDS1' (length 5)")],
         labels={0x0600: ("TapeLoader_side1", "SYS 1536: LOAD 'MAIN1' at $1000 and 'ADDS1' at $3000 from tape, then start part 1."),
                 0x1010: ("Entry_day_one", "")}),
    dict(name="loader_side2", kind="c16tap", file="original/dt_star_events_side2.tap", index=0, entries=[0x0600],
         ranges=[(0x0639, 0x063D, "ByteTable", "MainName_side2", "'MAIN*', used with length 4 as 'MAIN'"),
                 (0x063E, 0x0642, "ByteTable", "AddsName_side2", "'ADDS*', used with length 4 as 'ADDS'")],
         labels={0x0600: ("TapeLoader_side2", "SYS 1536: LOAD 'MAIN' at $1000 and 'ADDS' at $0800 (not its header's $1400),\n"
                          "then start part 2."),
                 0x2111: ("Entry_day_two", "")}),

    # The unpacked game, as the decruncher leaves it (VICE dump, checked by tools/unpack_sfx.py --check).
    dict(name="day_one", kind="prg", file="original/day_one_unpacked_vice.prg",
         entries=[0x1010, 0x1584, 0x22E3] + D1_SPLITS + [c + 7 for c in D1_INLINE_CALLS],
         ranges=[(0x15AC, 0x15C5, "AddrTable", "SplitTable_day_one", "Raster-split handlers, called in turn by the IRQ (13 entries)")]
         + inline_words(D1_INLINE_CALLS),
         labels={0x1010: ("Entry_day_one", "Entry point of part 1 (the decruncher's final JMP). Provisional name."),
                 0x156E: ("InstallIrq_day_one", "Point the KERNAL IRQ vector ($0314) at IrqHandler_day_one; raster IRQ only."),
                 0x1584: ("IrqHandler_day_one", "Raster IRQ: acknowledge, call the next split handler from SplitTable_day_one,\n"
                          "step the split counter ($0F) through 0-12. Exits through the KERNAL's register pull."),
                 0x158A: ("IrqSplitCall_day_one", ""),
                 0x1024: ("FetchPackedByte", "Load the byte at the packed-screen pointer (the LDA operand at $1025/$1026 is the pointer)."),
                 0x106E: ("AdvancePackedPtr", "Step the packed-screen pointer by one."),
                 0x1077: ("DrawPackedScreen", "Decode the packed screen at $3000 into screen $0C00 and colour $0800.\n"
                          "Codes: $FB run, $FC set address, $FD next row (+40), $FE set colour, $FF end; others are characters."),
                 0x1121: ("EventNumber", "1-4: the event being run; picks its name, distance and set-up."),
                 0x1123: ("EventDistanceText", "Four 10-byte fields: ' 100', ' 400', ' 110', ' 200' (indexed 0, 10, 20, 30)."),
                 0x114B: ("EventNameText", "Four 10-byte fields: SPRINT, RUN, HURDLES, HURDLES."),
                 0x1173: ("GameOverText", "'GAME OVER', drawn by ShowGameOver."),
                 0x117C: ("Lives", "Set to 3; one glyph each at $0CF1. One is lost when an event ends unqualified; 0 ends the game."),
                 0x1191: ("ShowGameOver", "Print GAME OVER, play a tune, wait for fire."),
                 0x123C: ("InitGame_day_one", "Clear the score tables and set Lives to 3, then fall into the event set-up."),
                 0x125A: ("StartEvent_day_one", "Draw the screen, step EventNumber, print the event's name and distance, set TED, install the IRQ."),
                 0x139B: ("MainLoop_day_one", "Once a frame: read the joystick, act on a change, wait for raster line $A8, update, check the event's end."),
                 0x14D9: ("JoyLast", "Last value read from TED_KEYLATCH with $FD written to $FD30/$FF08; a change calls JoyWaggle."),
                 0x117E: ("ScorePending", "Six decimal digits (0-9, most significant first) waiting to be added by AddScore."),
                 0x1184: ("Score", "Six decimal digits (0-9, most significant first), shown at $0C30 by AddScore."),
                 0x11ED: ("AwardTimeBonus", "Add 6 points to the score 255 - (sum of three of the time's ASCII digits) times."),
                 0x1214: ("AddScore", "Add ScorePending to Score digit by digit with carry, print Score at $0C30, clear ScorePending."),
                 0x169D: ("RaceRunning", "1 from the end of the start countdown until the event ends; gates the race clock."),
                 0x16B4: ("ClearSpeedMeter", "Copy the 8 characters at $16C2 to the speed meter at $0FC6."),
                 0x16CB: ("DrawSpeedMeter", "Draw RunSpeed / 4 steps at $0FC6 with characters $21-$24, four steps to a cell."),
                 0x1834: ("RaceClock", "Five ASCII digits, least significant first ($1834 counts 0-5, the others 0-9).\n"
                          "Shown most significant first at $0FDD-$0FE2 by TickRaceClock."),
                 0x183F: ("TickRaceClock", "Step RaceClock and print it; called from the split at $15C6 while RaceRunning is set."),
                 0x1987: ("RunSpeed", "Runner's speed, 0-$70. Raised by JoyWaggle, lowered by SpeedDecay, shown by DrawSpeedMeter."),
                 0x1988: ("SpeedUp", "RunSpeed + 1 up to $70, then redraw the meter."),
                 0x1996: ("SpeedDecay", "Every 6 calls (3 once RunSpeed >= $60), RunSpeed - 1 down to 0, then redraw the meter."),
                 0x19BE: ("JoyWaggle", "Record left and right in WaggleSeen; once both are seen, RunSpeed + 5 (+2 from $40) and clear it."),
                 0x1A0A: ("WaggleSeen", "Bit 0: right seen, bit 1: left seen, since the last speed step."),
                 0x1A0C: ("StartCountdown", "Show ON YOUR MARKS, GET SET and GO at $0E8E, waiting between them, then set RaceRunning."),
                 0x1A5B: ("ClearMessage", "Blank the 13 characters at $0E8E."),
                 0x1A68: ("WaitTicks", "Set DelayTicks to 100 and wait for the IRQ to count it to 0."),
                 0x1A73: ("OnYourMarksText", "Screen codes, 13 bytes."),
                 0x1A80: ("GetSetText", "Screen codes, 7 bytes."),
                 0x1A87: ("GoText", "Screen codes, 2 bytes."),
                 0x1A89: ("DelayTicks", "Counted down by the split at $15C6."),
                 0x1A8B: ("CheckEventEnd", "End the event when the distance shown at $0FD1 reaches its length (with RunSpeed > 0),\n"
                          "or when RaceClock's tens digit reaches 7; JudgeTime decides, then StartEvent_day_one."),
                 0x21C0: ("QualifyIndex", "Offset of this event's entry in QualifyTimes: 0, 12, 6, 18 for events 1-4."),
                 0x21C1: ("QualifyTimes", "Four 6-character ASCII times: 013:00, 060:00, 015:00, 038:00."),
                 0x21D9: ("TimeToJudge", "RaceClock copied into QualifyTimes' layout."),
                 0x21DF: ("JudgeTime", "Compare the time with QualifyTimes: under it, QUALIFIED and AwardTimeBonus;\n"
                          "over it, FAILED and one of Lives lost."),
                 0x222E: ("QualifiedText", "Screen codes, 9 bytes."),
                 0x2237: ("FailedText", "Screen codes, 6 bytes."),
                 0x2783: ("SoundSilence_day_one", "Clear the sound driver's tables and zero $FF0E-$FF11 and the voice 1 high bits in $FF12.\n"
                          "Reached only through SoundVectors_day_one+3, which part 1 never calls."),
                 0x27C6: ("SoundStep_day_one", "Sound driver step, called from the raster split at $1631. TODO(name)"),
                 0x2BB7: ("PlayTunePair_day_one", "Take two inline words after the JSR (copied to $12-$15), start both voices, return past them.\n"
                          "TODO(name): the words look like voice 1 and voice 2 data pointers."),
                 0x22E0: ("SoundVectors_day_one", "Jump table into the sound driver (same layout as part 2's at $1800).\n"
                          "$22E3 has no caller in part 1; its target matches the part 2 routine at $1CA2. TODO(name)")}),
    dict(name="day_two", kind="prg", file="original/day_two_unpacked_vice.prg",
         entries=[0x2111, 0x234E, 0x300C, 0x308C] + D2_SPLITS + [c + 7 for c in D2_INLINE_CALLS],
         ranges=[(0x23EE, 0x23FA, "ByteTable", "SplitRasters_day_two", "Raster line of each split (13 entries)"),
                 (0x21C7, 0x21F8, "WordTable", "ScreenRowTable", "Screen address of each of the 25 rows ($0C00 + 40 * row)"),
                 (0x2F14, 0x2F19, "AddrTable", "EventJumpTable_day_two", "Per-event handler, indexed by $42; patched into the JMP at $2F11 (3 entries)"),
                 (0x23FB, 0x2414, "AddrTable", "SplitTable_day_two", "Raster-split handlers, called in turn by the IRQ (13 entries)")]
         + inline_words(D2_INLINE_CALLS),
         labels={0x2111: ("Entry_day_two", "Entry point of part 2 (the decruncher's final JMP): copy $0800-$0BDF to $0400-$07DF,\n"
                          "ten NOPs, reset the stack, go to InitGame_day_two."),
                 0x2333: ("InstallIrq_day_two", "Point the KERNAL IRQ vector ($0314) at IrqHandler_day_two; raster IRQ at line $2E."),
                 0x234E: ("IrqHandler_day_two", "Raster IRQ: acknowledge, save $21-$24, call the next split handler from\n"
                          "SplitTable_day_two, set the next raster line from SplitRasters_day_two."),
                 0x2374: ("IrqSplitCall_day_two", ""),
                 0x2F11: ("EventJump_day_two", "Self-modified JMP: operand set from EventJumpTable_day_two."),
                 0x1CA2: ("SoundSilence_day_two", "Clear the sound driver's tables and zero $FF0E-$FF11 and the voice 1 high bits in $FF12."),
                 0x1CE4: ("SoundStep_day_two", "Sound driver step, called from the last raster split. TODO(name)"),
                 0x20D5: ("PlayTunePair_day_two", "Take two inline words after the JSR (copied to $12-$15), start both voices, return past them.\n"
                          "TODO(name): the words look like voice 1 and voice 2 data pointers."),
                 0x2164: ("DelayXY", "Busy-wait: X outer loops of 256 inner loops."),
                 0x2170: ("ClearZeroPage", "Zero $02-$FF."),
                 0x217A: ("ClearScreen", "Fill screen $0C00-$0FFF with spaces and colour $0800-$0BFF with $71, then zero $0DB8-$0E07."),
                 0x21A6: ("ScreenAddress", "Row Y, column X -> screen pointer $21/$22 (copy in $23) and colour pointer $23/$24."),
                 0x2437: ("InitGame_day_two", "Clear zero page, silence the sound, set up, install the IRQ, go to $2584."),
                 0x2584: ("StartGame_day_two", "Reset scores and state, draw the screen, play a tune until fire. TODO(name)"),
                 0x1800: ("SoundVectors_day_two", "Jump table into the sound driver. TODO(name)")}),
]

LABELS = {
    0x0314: ("CINV", ""),  # KERNAL IRQ vector in RAM (lo $0314, hi $0315)
    0x0315: ("CINV_HI", ""),
}

RANGES = []

INLINE = {}
