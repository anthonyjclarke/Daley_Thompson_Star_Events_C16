# Daley Thompson's Star Events

Decomposition of *Daley Thompson's Star Events* for the Commodore 16, which I wrote with my business partner Jason Perkins in 1985 for Ocean Software. It is a conversion of the C64 game, kept as close to it as the C16 allowed. The game comes in two parts, one on each side of the tape: Day One (100 m, 110 m hurdles, 400 m, 200 m hurdles) and Day Two (long jump, shot-put, javelin).

---

## Originals

`original/` holds what survives, read-only and checked by hash: the two sides of the 1985 cassette as tape images, the two crunched PRGs made from them much later with Exomizer 2.0, and the two unpacked images dumped from VICE for this project. [The artifacts](docs/ARTIFACTS.md) describe each file and how they relate; [source and validation](docs/SOURCE_AND_VALIDATION.md) shows how every one of them is rebuilt byte for byte.

---

## Building

`make verify` checks the originals and rebuilds every block byte for byte; `make docs` regenerates the code reference and the handbook. The other targets and every script are in [build and run](docs/BUILD_AND_RUN.md).

---

## Documentation

The [complete handbook](docs/DALEY_THOMPSON.html) is one offline HTML file with every chapter, the screenshots, graphics, diagrams and sound clips. Open it in a browser. Its chapters are the Markdown files here:

| Chapter                                                | What it covers                                     |
|:-------------------------------------------------------|:---------------------------------------------------|
| [History and credits](docs/HISTORY_AND_CREDITS.md)     | Who wrote it, the packaging, recollections         |
| [Playing the game](docs/PLAYING.md)                    | Loading, controls, every event, scoring            |
| [Artifacts](docs/ARTIFACTS.md)                         | The tapes, the loader and the crunched PRGs        |
| [Codebase analysis](CODEBASE_ANALYSIS.md)              | How both parts work, with the sounds               |
| [Graphics](docs/GRAPHICS.md)                           | Screens, character sets, the athlete, the boards   |
| [Source and validation](docs/SOURCE_AND_VALIDATION.md) | How the work was done and how it is checked        |
| [Build and run](docs/BUILD_AND_RUN.md)                 | Make targets, scripts and tools                    |
| [Evidence](docs/evidence.md)                           | The proof behind each name                         |
| [Quirks](docs/quirks.md)                               | What the original does oddly, kept in the build    |
| [Worklist](docs/WORKLIST.md)                           | What is checked and what still needs a person      |
| [Changelog](CHANGELOG.md)                              | Every change to the project                        |
| [Code reference](docs/CODE_REFERENCE.md)               | Every name, generated from `tools/symbols.py`      |

`make docs` regenerates the code reference and the HTML; see [maintaining the HTML](docs/HTML_DOCUMENTATION.md).
