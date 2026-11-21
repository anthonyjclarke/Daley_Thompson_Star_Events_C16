# Maintaining the HTML Documentation

`docs/DALEY_THOMPSON.html` is one self-contained file with every chapter of this handbook, the images, the sound clips, the styles, a contents sidebar, search and the Mermaid diagram renderer. It opens in a browser with no internet connection.

**Edit the Markdown, never the HTML.** The generator keeps no second copy of the prose: each chapter is read from its source file, and links between included documents become links inside the handbook.

---

## Regenerating

```sh
make docs
```

This writes `docs/CODE_REFERENCE.md` from `tools/symbols.py`, then runs `node scripts/build_docs.mjs` to write the HTML. The chapters and their order are set in `docs/handbook.json`.

Images and sounds are embedded as data, so the file needs nothing beside it. A Markdown image link to an `.svg`, `.png`, `.gif` or `.jpg` becomes a picture; one to an `.m4a`, `.mp3`, `.ogg` or `.wav` becomes an audio player captioned with the link's text. The pictures in `docs/images/` and the clips in `docs/sounds/` are made by the scripts in [build and run](BUILD_AND_RUN.md); rerun them before `make docs` when what they draw changes.

```sh
make docs-check
```

This fails if either file is stale. It regenerates both in memory and compares them with the saved files, without overwriting them.

The generator, its template, styles and reader script (`scripts/build_docs.mjs`, `scripts/docs/`) and the vendored Marked and Mermaid (`scripts/vendor/`, with their licences) are shared with the other C16 restorations. It doesn't use npm or download anything. Commit the HTML together with the Markdown it comes from.
