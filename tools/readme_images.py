#!/usr/bin/env python3
"""Make the README's badges and screenshot montage.

Run from the project root:   python3 tools/readme_images.py

The badges (docs/images/badges/*.svg) are flat shields in the style of the other C16 restorations; edit
BADGES when a value changes. The montage (docs/images/montage.png) tiles six of the VICE screenshots that
tools/doc_shots.py takes, three from each day, with a black gap between them. Standard library only.
"""
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "docs/images"

BADGES = [  # (file, label, value, colour)
    ("version", "version", "0.10.2", "#007ec6"),
    ("platform", "platform", "Commodore 16", "#8a5a00"),
    ("byte-match", "byte match", "40,724 of 40,724", "#2e8b30"),
    ("toolchain", "toolchain", "cc65", "#6a3fa0"),
    ("emulator", "emulator", "VICE 3.10", "#4a6b8a"),
    ("status", "status", "preservation", "#555555"),
]
MONTAGE = ["event_100m", "event_110m_hurdles", "event_400m", "title_day_two", "event_long_jump", "event_javelin"]
COLUMNS, GAP = 3, 8


def text_width(s):
    """Approximate width of Verdana 11 px, as shields.io measures it."""
    return sum(4 if c in "il.,:;'|!" else 5 if c in "fjrt " else 9 if c in "mwMW" else 7 for c in s) + 10


def badge(label, value, colour):
    lw, vw = text_width(label), text_width(value)
    w = lw + vw
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{label}: {value}">
<title>{label}: {value}</title>
<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>
<clipPath id="r"><rect width="{w}" height="20" rx="3" fill="#fff"/></clipPath>
<g clip-path="url(#r)"><rect width="{lw}" height="20" fill="#555"/><rect x="{lw}" width="{vw}" height="20" fill="{colour}"/><rect width="{w}" height="20" fill="url(#s)"/></g>
<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
<text x="{lw / 2:.1f}" y="15" fill="#010101" fill-opacity=".3">{label}</text><text x="{lw / 2:.1f}" y="14">{label}</text>
<text x="{lw + vw / 2:.1f}" y="15" fill="#010101" fill-opacity=".3">{value}</text><text x="{lw + vw / 2:.1f}" y="14">{value}</text>
</g>
</svg>
"""


def read_png(path):
    """Decode an 8-bit RGB or RGBA, non-interlaced PNG to rows of RGB tuples."""
    data = path.read_bytes()
    pos, idat, width = 8, b"", 0
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        if kind == b"IHDR":
            width, height, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
            if depth != 8 or ctype not in (2, 6) or interlace:
                raise SystemExit(f"{path.name}: unsupported PNG")
            bpp = 4 if ctype == 6 else 3
        elif kind == b"IDAT":
            idat += body
        pos += 12 + n
    raw, stride, rows, prev = zlib.decompress(idat), width * bpp, [], bytearray(width * bpp)
    for y in range(height):
        f, line = raw[y * (stride + 1)], bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b, c = prev[i], prev[i - bpp] if i >= bpp else 0
            if f == 1:
                line[i] = (line[i] + a) & 0xFF
            elif f == 2:
                line[i] = (line[i] + b) & 0xFF
            elif f == 3:
                line[i] = (line[i] + (a + b) // 2) & 0xFF
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 0xFF
        rows.append(bytes(line[x * bpp + k] for x in range(width) for k in range(3)))
        prev = line
    return width, height, rows


def write_png(path, width, height, rows):
    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
    raw = b"".join(b"\x00" + r for r in rows)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def main():
    (IMAGES / "badges").mkdir(exist_ok=True)
    for name, label, value, colour in BADGES:
        (IMAGES / "badges" / f"{name}.svg").write_text(badge(label, value, colour))
    shots = [read_png(IMAGES / f"{n}.png") for n in MONTAGE]
    w, h = shots[0][0], shots[0][1]
    rows_n = (len(shots) + COLUMNS - 1) // COLUMNS
    W, H = COLUMNS * w + (COLUMNS - 1) * GAP, rows_n * h + (rows_n - 1) * GAP
    canvas = [bytearray(W * 3) for _ in range(H)]
    for k, (_, _, rows) in enumerate(shots):
        x0, y0 = (k % COLUMNS) * (w + GAP), (k // COLUMNS) * (h + GAP)
        for y, r in enumerate(rows):
            canvas[y0 + y][x0 * 3:(x0 + w) * 3] = r
    write_png(IMAGES / "montage.png", W, H, [bytes(r) for r in canvas])
    print(f"badges: {len(BADGES)}; montage: {W}x{H}")


if __name__ == "__main__":
    main()
