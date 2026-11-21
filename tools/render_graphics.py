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
from cpu6502 import CPU  # noqa: E402

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


# VICE's built-in TED palette (TEDExternalPalette=0), colours $00-$7F, sampled from a VICE screenshot of 128
# solid cells, one per colour-RAM value.
TED_PALETTE = (
    "000000 202020 5e0700 003940 56006c 004a00 150aae 2b3600 "  # $00
    "541600 422600 124300 5f0038 004508 001a9a 2e00ac 004a00 "  # $08
    "000000 303030 6e1710 004950 66067c 005a00 251abe 3b4600 "  # $10
    "642600 523600 225300 6f0b48 005518 0e2aaa 3e0dbc 0b5a00 "  # $18
    "000000 404040 7e2720 025960 76168c 0a6a00 352ace 4b5600 "  # $20
    "743600 624600 326300 7f1b58 016528 1e3aba 4e1dcc 1b6a00 "  # $28
    "000000 505050 8e3730 126970 86269c 1a7a04 453ade 5b6600 "  # $30
    "844600 725600 427300 8f2b68 117538 2e4aca 5e2ddc 2b7a00 "  # $38
    "ffffff 787878 b65f58 3a9198 ae4ec4 42a22c 6d62ff 838e00 "  # $40
    "ac6e25 9a7e00 6a9b00 b75390 399d60 5672f2 8655ff 53a203 "  # $48
    "000000 909090 ce7770 52a9b0 c666dc 5aba44 857aff 9ba602 "  # $50
    "c4863d b29616 82b304 cf6ba8 51b578 6e8aff 9e6dff 6bba1b "  # $58
    "000000 c0c0c0 fea7a0 82d9e0 f696ff 8aea74 b5aaff cbd632 "  # $60
    "f4b66d e2c646 b2e334 ff9bd8 81e5a8 9ebaff ce9dff 9bea4b "  # $68
    "000000 ffffff ffe7e0 c2ffff ffd6ff caffb4 f5eaff ffff72 "  # $70
    "fff6ad ffff86 f2ff74 ffdbff c1ffe8 defaff ffddff dbff8b "  # $78
).split()
TED_RGB = {i: '#' + c for i, c in enumerate(TED_PALETTE)}
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


def run_routine(name, addrs, pokes=()):
    """Run routines of an original image, in order, in tools/cpu6502.py; give back the 64K memory."""
    base, data = read_prg(ROOT / "original" / name)
    mem = bytearray(0x10000)
    mem[base:base + len(data)] = data
    for a, v in pokes:
        mem[a] = v
    for addr in addrs:
        cpu = CPU(mem)
        cpu.sp = 0xFD
        cpu.push(0xFF)  # return to $FFFF (pushed as $FFFE, RTS adds 1)
        cpu.push(0xFE)
        cpu.pc = addr
        for _ in range(2_000_000):
            if cpu.pc == 0xFFFF:
                break
            cpu.step()
        else:
            raise SystemExit(f"{name}: routine at ${addr:04X} did not return")
    return mem


def cell_pixels(bitmap, colour, x0, y0, scale, shades):
    """One TED character cell: hi-res in its colour, or multicolour pairs when colour bit 3 is set."""
    out = []
    if colour & 0x08:
        for row, byte in enumerate(bitmap):
            for pair in range(4):
                v = (byte >> (6 - pair * 2)) & 3
                if v:
                    fill = TED_RGB[colour & 0x77] if v == 3 else shades[v]
                    out.append(f'<rect x="{x0 + pair * 2 * scale}" y="{y0 + row * scale}" width="{2 * scale}" '
                               f'height="{scale}" fill="{fill}"/>')
    else:
        for row, byte in enumerate(bitmap):
            for col in range(8):
                if byte & (0x80 >> col):
                    out.append(f'<rect x="{x0 + col * scale}" y="{y0 + row * scale}" width="{scale}" '
                               f'height="{scale}" fill="{TED_RGB[colour & 0x7F]}"/>')
    return out


def screen_day_one():
    """Day One's screen built by its own code: DrawPackedScreen ($1077), then DrawSceneryRows ($17C6)."""
    mem = run_routine("day_one_unpacked_vice.prg", [0x1077, 0x17C6])
    scale = 2
    width, height = 40 * 8 * scale + 16, 25 * 8 * scale + 40
    body = [f'<rect x="8" y="24" width="{40 * 8 * scale}" height="{25 * 8 * scale}" fill="#000000"/>',
            f'<text x="8" y="16" font-size="12" fill="{INK}">Day One screen built by DrawPackedScreen and '
            f'DrawSceneryRows: $3800 characters in colour-RAM colours; band colours not shown</text>']
    shades = [None, "#5a6378", "#8a8f9c", None]
    for i in range(1000):
        code, colour = mem[0x0C00 + i], mem[0x0800 + i]
        if code == 0x20:
            continue
        x0, y0 = 8 + (i % 40) * 8 * scale, 24 + (i // 40) * 8 * scale
        body += cell_pixels(mem[0x3800 + code * 8:0x3800 + code * 8 + 8], colour, x0, y0, scale, shades)
    return svg(width, height, "".join(body))


def object_block(mem, x0, y0, scale):
    """The 4x8-character object block at $3B08 (characters $61-$80), laid out as PlotObjectPixel addresses it."""
    out = [f'<rect x="{x0}" y="{y0}" width="{32 * scale}" height="{64 * scale}" fill="none" stroke="{GRID}"/>']
    for y in range(64):
        for x in range(32):
            byte = mem[0x3B08 + (y & 0xF8) * 4 + (y & 7) + (x & 0xF8)]
            if byte & (0x80 >> (x & 7)):
                out.append(f'<rect x="{x0 + x * scale}" y="{y0 + y * scale}" width="{scale}" height="{scale}" '
                           f'fill="{INK}"/>')
    return out


def objects_day_one():
    scale, gap = 4, 40
    width, height = 3 * (32 * scale + gap) + gap, 64 * scale + 60
    body = [f'<text x="{gap}" y="16" font-size="12" fill="{INK}">Day One object block ($3B08, 4x8 characters $61-$80) '
            f'after each drawing routine, as 1-bit pixels</text>']
    shots = [("DrawHurdleA ($2078)", 0x2078, ()), ("DrawHurdleB ($20A4)", 0x20A4, ()),
             ("DrawFinishLine ($2291), PlotX = 8", 0x2291, ((0x228B, 8),))]
    for i, (label, addr, pokes) in enumerate(shots):
        mem = run_routine("day_one_unpacked_vice.prg", [0x1BCD, addr], pokes)  # ClearObjectChars first
        x0 = gap + i * (32 * scale + gap)
        body += object_block(mem, x0, 28, scale)
        body.append(f'<text x="{x0}" y="{28 + 64 * scale + 16}" font-size="10" fill="{INK}">{label}</text>')
    return svg(width, height, "".join(body))


def lettering_day_two():
    read = image("day_two_unpacked_vice.prg")
    glyphs, offsets = read(0x2AF7, 0x2E), read(0x2B24, 4)
    scale = 2
    names = ["LONG JUMP", "SHOT PUT", "JAVELIN", "FIRE TO START"]
    width, height = 40 * 8 * scale + 16, 4 * (8 * scale + 24) + 140
    body = [f'<text x="8" y="16" font-size="12" fill="{INK}">Day Two title lettering (TitleGlyphs $2AF7): glyph g is '
            f'characters $CB+2g and $CC+2g of the $1000 set</text>']
    for t in range(4):
        y0 = 28 + t * (8 * scale + 24)
        i = offsets[t]
        col = glyphs[i]
        i += 1
        while glyphs[i] != 0xFF:
            g = glyphs[i]
            if g:
                for k in range(2):
                    code = ((g << 1) + 0xCB + k) & 0xFF
                    body += char_runs(read(0x1000 + code * 8, 8), 8 + (col + k) * 8 * scale, y0, scale)
            col += 2
            i += 1
        body.append(f'<text x="8" y="{y0 + 8 * scale + 12}" font-size="9" fill="{INK}">{names[t]} '
                    f'(offset {offsets[t]})</text>')
    # the large score digits: $40 + 2d over $41 + 2d
    y0 = 28 + 4 * (8 * scale + 24) + 10
    body.append(f'<text x="8" y="{y0}" font-size="10" fill="{INK}">Score-line digits 0-9 (DrawScoreLine): '
                f'character $40+2d over $41+2d</text>')
    for d in range(10):
        for k in range(2):
            code = 0x40 + 2 * d + k
            body += char_runs(read(0x1000 + code * 8, 8), 8 + d * 2 * 8 * scale, y0 + 8 + k * 8 * scale, scale)
    return svg(width, height + 40, "".join(body))


def implements_day_two():
    read = image("day_two_unpacked_vice.prg")
    scale = 4
    offsets, firsts = read(0x3174, 10), read(0x317E, 4)
    width, height = 4 * (5 * 8 * scale + 30) + 140, 2 * 8 * scale + 70
    body = [f'<text x="8" y="16" font-size="12" fill="{INK}">Day Two shot (ShotBitmap $31F1) and javelin in its four '
            f'JavelinPhase pictures (JavelinChars $317E, cells $3174)</text>']
    body += char_runs(read(0x31F1, 8), 8, 28, scale)
    body.append(f'<text x="8" y="{28 + 8 * scale + 14}" font-size="10" fill="{INK}">shot</text>')
    for ph in range(4):
        x0 = 70 + ph * (5 * 8 * scale + 30)
        for x in range(10):
            code = (firsts[ph] - (9 - x)) & 0xFF
            off = offsets[x]
            col, row = off % 40, off // 40
            body += char_runs(read(0x1000 + code * 8, 8), x0 + col * 8 * scale, 28 + row * 8 * scale, scale)
        body.append(f'<text x="{x0}" y="{28 + 2 * 8 * scale + 14}" font-size="10" fill="{INK}">phase {ph}: '
                    f'from ${firsts[ph]:02X}</text>')
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
        "screen_day_one.svg": screen_day_one(),
        "objects_day_one.svg": objects_day_one(),
        "lettering_day_two.svg": lettering_day_two(),
        "implements_day_two.svg": implements_day_two(),
    }
    for name, text in sheets.items():
        (OUT / name).write_text(text)
        print(f"wrote docs/images/{name} ({len(text) // 1024} KB)")


if __name__ == "__main__":
    main()
