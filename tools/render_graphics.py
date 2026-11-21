#!/usr/bin/env python3
"""Render the game's character sets and Day One's athlete frames as SVG, straight from the originals.

Run from the project root:   python3 tools/render_graphics.py

Writes docs/images/charset_*.svg (each character set as 1-bit pixels, 16 characters a row, with its
code) and docs/images/athlete_day_one.svg (the seven frames of AthleteFrames, each two 6x3 halves,
drawn as TED multicolour pixel pairs in four neutral shades: the real colours come from raster splits
and colour RAM, which vary by screen band). Also docs/images/advert_boards_day_two.svg (the 58-character
strip of advertising boards, characters $80-$B9 over $BA-$F3, each board in its own colour from $2675;
with $FF13 = $04 and 256 characters TED reads them from $0400-$079F, the data loaded at $0800) and docs/images/athlete_day_two.svg (the top and bottom halves that StepRunFrame_day_two
copies into characters $A3-$C6, from the address tables at $2E87 and $2EA5). Standard library only.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from media import read_prg  # noqa: E402

OUT = ROOT / "docs/images"
INK, PAPER, GRID = "#1d2433", "#f4f1e8", "#c9c2b0"
SHADES = [None, "#7c8aa6", "#c06c3e", "#1d2433"]  # multicolour 01, 10, 11 (00 = paper)


def image(name):
    base, data = read_prg(ROOT / "original" / name)
    return lambda a, n: bytes(data[a - base:a - base + n])


def svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
            f'height="{height}" shape-rendering="crispEdges" font-family="monospace">'
            f'<rect width="{width}" height="{height}" fill="{PAPER}"/>{body}</svg>\n')


def char_runs(bitmap, x0, y0, scale):
    """1-bit character: one rect per horizontal run of set pixels."""
    out = []
    for row, byte in enumerate(bitmap):
        col = 0
        while col < 8:
            if byte & (0x80 >> col):
                start = col
                while col < 8 and byte & (0x80 >> col):
                    col += 1
                out.append(f'<rect x="{x0 + start * scale}" y="{y0 + row * scale}" width="{(col - start) * scale}" '
                           f'height="{scale}" fill="{INK}"/>')
            else:
                col += 1
    return out


def charset_sheet(read, start, count, first_code, title):
    scale, cell, label = 3, 8 * 3 + 6, 12
    cols = 16
    rows = (count + cols - 1) // cols
    width, height = cols * cell + 8, rows * (cell + label) + 28
    body = [f'<text x="4" y="16" font-size="12" fill="{INK}">{title}</text>']
    for i in range(count):
        x = 4 + (i % cols) * cell
        y = 24 + (i // cols) * (cell + label)
        body.append(f'<rect x="{x - 1}" y="{y - 1}" width="{8 * scale + 2}" height="{8 * scale + 2}" fill="none" '
                    f'stroke="{GRID}" stroke-width="1"/>')
        body += char_runs(read(start + i * 8, 8), x, y, scale)
        body.append(f'<text x="{x}" y="{y + 8 * scale + 10}" font-size="8" fill="{INK}">{first_code + i:02X}</text>')
    return svg(width, height, "".join(body))


def multicolour_char(bitmap, x0, y0, scale):
    out = []
    for row, byte in enumerate(bitmap):
        for pair in range(4):
            value = (byte >> (6 - pair * 2)) & 3
            if value:
                out.append(f'<rect x="{x0 + pair * 2 * scale}" y="{y0 + row * scale}" width="{2 * scale}" '
                           f'height="{scale}" fill="{SHADES[value]}"/>')
    return out


def athlete_sheet():
    read = image("day_one_unpacked_vice.prg")
    frames, charset, scale = read(0x1E56, 252), 0x3800, 3
    frame_w, frame_h, gap = 6 * 8 * scale, 6 * 8 * scale, 16
    width = 7 * (frame_w + gap) + gap
    height = frame_h + 48
    body = [f'<text x="{gap}" y="16" font-size="12" fill="{INK}">Day One AthleteFrames ($1E56): seven frames, '
            f'top and bottom halves of 6x3 characters</text>']
    for f in range(7):
        x0 = gap + f * (frame_w + gap)
        y0 = 28
        for cell in range(36):
            code = frames[f * 36 + cell]
            if code == 0x20:
                continue
            cx, cy = x0 + (cell % 6) * 8 * scale, y0 + (cell // 6) * 8 * scale
            body += multicolour_char(read(charset + code * 8, 8), cx, cy, scale)
        body.append(f'<text x="{x0}" y="{y0 + frame_h + 14}" font-size="10" fill="{INK}">offset ${f * 36:02X}</text>')
    return svg(width, height, "".join(body))


# VICE's built-in TED palette (TEDExternalPalette=0), sampled from VICE screenshots of the border.
TED_RGB = {0x56: "#857aff", 0x32: "#8e3730", 0x42: "#b65f58", 0x26: "#352ace", 0x46: "#6d62ff", 0x30: "#000000"}
BOARD_STARTS = [0x80, 0x8B, 0x95, 0x9D, 0xA6, 0xAE]   # $266F
BOARD_COLOURS = [0x56, 0x32, 0x42, 0x26, 0x46, 0x30]  # $2675


def advert_boards():
    read = image("day_two_unpacked_vice.prg")
    scale, gap = 3, 12
    cell = 8 * scale
    widths = [(BOARD_STARTS[i + 1] if i < 5 else 0xBA) - BOARD_STARTS[i] for i in range(6)]
    width = sum(w * cell for w in widths) + gap * 7
    height = 2 * cell + 64
    body = [f'<text x="{gap}" y="16" font-size="12" fill="{INK}">Day Two advertising boards: characters $80-$B9 over '
            f'$BA-$F3, read from $0400-$079F, scrolled in by ScrollAdvertBoards</text>']
    x0 = gap
    for b, start in enumerate(BOARD_STARTS):
        colour = TED_RGB[BOARD_COLOURS[b]]
        w = widths[b]
        body.append(f'<rect x="{x0}" y="28" width="{w * cell}" height="{2 * cell}" fill="#ffffff" stroke="{GRID}"/>')
        for row in range(2):
            for i in range(w):
                code = start + i + row * 0x3A
                for r, byte in enumerate(read(0x0800 + (code - 0x80) * 8, 8)):  # at $0400 after the copy
                    col = 0
                    while col < 8:
                        if byte & (0x80 >> col):
                            c0 = col
                            while col < 8 and byte & (0x80 >> col):
                                col += 1
                            body.append(f'<rect x="{x0 + i * cell + c0 * scale}" y="{28 + row * cell + r * scale}" '
                                        f'width="{(col - c0) * scale}" height="{scale}" fill="{colour}"/>')
                        else:
                            col += 1
        body.append(f'<text x="{x0}" y="{28 + 2 * cell + 14}" font-size="9" fill="{INK}">${start:02X}, colour '
                    f'${BOARD_COLOURS[b]:02X}</text>')
        x0 += w * cell + gap
    return svg(width, height, "".join(body))


def athlete_day_two():
    read = image("day_two_unpacked_vice.prg")
    table = lambda a, n: [read(a + 2 * i, 2)[0] | read(a + 2 * i, 2)[1] << 8 for i in range(n)]
    tops, bottoms = table(0x2E87, 15), table(0x2EA5, 9)
    scale = 2
    half_w, half_h, gap = 6 * 8 * scale, 3 * 8 * scale, 14
    cols = 15
    width = cols * (half_w + gap) + gap
    height = 2 * (half_h + 40) + 30
    body = [f'<text x="{gap}" y="16" font-size="12" fill="{INK}">Day Two athlete halves: top frames ($2E87, 15) and '
            f'bottom frames ($2EA5, 9), 6x3 characters each, multicolour in neutral shades</text>']

    def half(addr, x0, y0):
        out = []
        for k in range(18):
            block, within = divmod(k, 9)
            row, col = divmod(within, 3)
            out.extend(multicolour_char(read(addr + k * 8, 8), x0 + (block * 3 + col) * 8 * scale,
                                        y0 + row * 8 * scale, scale))
        return out

    for row, (frames, label) in enumerate(((tops, "top"), (bottoms, "bottom"))):
        y0 = 28 + row * (half_h + 40)
        for i, addr in enumerate(frames):
            x0 = gap + i * (half_w + gap)
            body.append(f'<rect x="{x0 - 1}" y="{y0 - 1}" width="{half_w + 2}" height="{half_h + 2}" fill="none" '
                        f'stroke="{GRID}"/>')
            body += half(addr, x0, y0)
            body.append(f'<text x="{x0}" y="{y0 + half_h + 12}" font-size="8" fill="{INK}">{label} {i:X}: '
                        f'${addr:04X}</text>')
    return svg(width, height, "".join(body))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    one = image("day_one_unpacked_vice.prg")
    two = image("day_two_unpacked_vice.prg")
    sheets = {
        "charset_day_one.svg": charset_sheet(one, 0x3800, 256, 0, "Day One character set ($3800, 256 characters)"),
        "charset_day_two_0400.svg": charset_sheet(two, 0x0800, 128, 0, "Day Two advert characters at $0400 (loaded at $0800; shown as characters $80-$FF)"),
        "charset_day_two_1000.svg": charset_sheet(two, 0x1000, 256, 0, "Day Two character set at $1000 (256 characters)"),
        "athlete_day_one.svg": athlete_sheet(),
        "advert_boards_day_two.svg": advert_boards(),
        "athlete_day_two.svg": athlete_day_two(),
    }
    for name, text in sheets.items():
        (OUT / name).write_text(text)
        print(f"wrote docs/images/{name} ({len(text) // 1024} KB)")


if __name__ == "__main__":
    main()
