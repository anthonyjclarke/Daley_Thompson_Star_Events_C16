# History and Credits

---

## The Game

*Daley Thompson's Star Events* for the Commodore 16 was written in 1985 by Anthony Clarke and Jason Perkins, for Ocean Software. It was released in two parts on the two sides of one cassette: Day One with the four running events, Day Two with the three field events. The cassette label says so: "4 events on one side of cassette and 3 events on reverse".

![The 1985 cassette](<../Original Assets/dt_star_events_tape.jpg>)

The game follows Ocean's C64 decathlon game. The C64 title screen kept with the originals is *Daley Thompson's Decathlon*, and Ocean's 1985 advert for *Daley Thompson's Super-Test* offers Star Events as "a special version" for the C16 and Plus/4 at £6.95. Six of its seven events are decathlon events; the 200 m hurdles is not.

![The C64 Daley Thompson's Decathlon title screen](<../Original Assets/daley_thompsons_decathlon_title.png>)

![Ocean's 1985 advert, with Star Events for the C16 and Plus/4](<../Original Assets/daley_thompsons_star_events_advert.jpg>)

---

## Recollections

Anthony gave these on 21 November 2026, about 41 years after the event. They're recorded as memory, not proof; the [evidence](evidence.md) keeps them alongside what the code shows.

| Topic            | Recollection                                                    |
|:-----------------|:----------------------------------------------------------------|
| Authors          | Anthony and Jason Perkins wrote it together; no one else was involved |
| Commission       | D.C. Ward, who owned Ocean, commissioned the C16 version        |
| Brief            | Replicate the C64 game as faithfully as the C16 allowed         |
| Source material  | None from Ocean: everything was done by watching the C64 version |
| Two parts        | Memory was very tight, so many C64 features were dropped and the game split in two |
| Tools            | Written and assembled on a C64; the runtime was loaded onto the C16 |
| Advert boards    | Copied from the C64 version                                     |
| Running control  | Probably alternating two keys, or moving the joystick left and right |

Most other details aren't remembered: the attempts counter, scoring, menus, the joystick port, the tunes, the screen packer, the unused routines, the label names, the tape loader and where the crunched PRGs came from.

---

## What the Code Adds

Several of these recollections can now be checked against the code:

- **Running control.** The run is joystick left-right alternation in both parts (`JoyWaggle`, `JoyWaggle_day_two`). Day Two also offers keys, which look like Q and Y with SPACE for fire.
- **Two parts.** Each part fills the 16 KB machine to `$3FFF`, and Day Two loads its character set into colour RAM and copies it down to fit.
- **Watching the C64 version.** Without the C64 source, the C16 game has its own design throughout: a character-mode athlete, scenery scrolled by rotating character bitmaps, and hurdles drawn pixel by pixel into the character set.

---

## The Surviving Copies

Two kinds of copy survive. The tape images are 2004 files of the 1985 cassette. Their perfectly regular timing shows they were generated from the file data by software rather than recorded from a cassette, but they keep the release's files, names and loader. The two PRGs are a later crunched conversion of the same memory, of unknown origin. [The artifacts](ARTIFACTS.md) describe both.

---

## This Restoration

The decomposition was made in 2026 with the OldCode_Restoration toolkit and Claude Code. It turns the surviving binaries into a documented disassembly that rebuilds byte for byte. The disassembler (`da65`, `ca65` and `ld65`) comes from the cc65 project, and runs use the VICE emulator (`xplus4`).

This handbook's generator, its reader script and its styles are shared with the other C16 restorations. It embeds Marked and Mermaid, whose licences are at the end of the HTML.
