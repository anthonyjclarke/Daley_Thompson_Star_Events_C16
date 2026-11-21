#!/usr/bin/env python3
"""Generate docs/CODE_REFERENCE.md from tools/symbols.py (the master of every name).

Run from the project root:   python3 tools/code_reference.py [--check]

One section per block: its declared data ranges, then every name in address order with its comment.
--check fails if the saved file differs from what would be generated.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import symbols  # noqa: E402

OUT = ROOT / "docs/CODE_REFERENCE.md"
TITLES = {
    "day_one_packed": "Part 1, crunched PRG",
    "day_two_packed": "Part 2, crunched PRG",
    "loader_side1": "Tape loader, side 1",
    "loader_side2": "Tape loader, side 2",
    "day_one": "Part 1 (Day One)",
    "day_two": "Part 2 (Day Two)",
}


def one_line(text):
    return " ".join(text.split())


def generate():
    out = ["# Code Reference", "",
           "Every name in the disassembly, generated from `tools/symbols.py` by `tools/code_reference.py`. "
           "Don't edit this file: change the names and comments in `symbols.py`, then run `make docs`. "
           "Names starting `L` followed by an address are not listed; they are still neutral. "
           "`docs/evidence.md` holds the proof for each name that claims a role.", "",
           "Shared by every block: " + ", ".join(f"`${a:04X}` **{n}**" for a, (n, c) in sorted(getattr(symbols, "LABELS", {}).items())) + ".", ""]
    for block in symbols.BLOCKS:
        labels = block.get("labels", {})
        name = block["name"]
        out += ["---", "", f"## {TITLES.get(name, name)}", "",
                f"Block `{name}`, from `{block['file']}`. Source `src/{name}.s`.", ""]
        ranges = [r for r in block.get("ranges", []) if r[3]]
        if ranges:
            out += ["### Declared Data", ""]
            for start, end, kind, label, note in sorted(ranges):
                out.append(f"- `${start:04X}`–`${end:04X}` **{label}** ({kind}) – {one_line(note)}")
            out.append("")
        named = sorted((a, n, c) for a, (n, c) in labels.items() if n and not n.endswith("_HI"))
        if named:
            out += ["### Names", ""]
            for addr, label, comment in named:
                text = f" – {one_line(comment)}" if comment else ""
                out.append(f"- `${addr:04X}` **{label}**{text}")
            out.append("")
    return "\n".join(out).rstrip() + "\n"


if __name__ == "__main__":
    text = generate()
    if "--check" in sys.argv:
        same = OUT.exists() and OUT.read_text() == text
        print("CODE_REFERENCE.md up to date" if same else "CODE_REFERENCE.md is stale: run make docs")
        sys.exit(0 if same else 1)
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)}")
