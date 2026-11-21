#!/usr/bin/env python3
"""Decode a raw C16 tape image (C16-TAPE-RAW, version 1) recorded in the KERNAL's own format.

Usage:  c16_tap.py FILE.tap [--out DIR] [--verbose]

Reads the image without changing it. Each value is one full wave in units of 8 cycles (0 = a 3-byte
length follows). The KERNAL writes three wave lengths: short (~53), medium (~105) and long (~210).
A byte is a long+medium marker, then 9 bit pairs (short+medium = 0, medium+short = 1, LSB first),
the ninth an odd-parity bit. A block starts with a countdown ($89..$81, or $09..$01 for the repeat),
then its bytes, then an XOR checksum. Each block is written twice; both copies are checked.

Header blocks (first byte 1 = relocatable program, 3 = absolute program, 4 = data, 5 = end of tape)
carry the start and end address and a 16-byte name; the program block that follows holds the bytes.
With --out, writes each program as a PRG (load address + bytes) named after the side and its index.
"""
import argparse
from pathlib import Path

SHORT_MAX, MEDIUM_MAX, LONG_MAX = 79 * 8, 157 * 8, 400 * 8  # cycle thresholds between wave classes


def waves(path):
    raw = Path(path).read_bytes()
    if raw[:12] != b"C16-TAPE-RAW" or raw[12] != 1:
        raise SystemExit(f"{path}: not a C16-TAPE-RAW version 1 image")
    body, out, i = raw[20:], [], 0
    while i < len(body):
        v = body[i]
        if v == 0:
            out.append(int.from_bytes(body[i + 1:i + 4], "little"))
            i += 4
        else:
            out.append(v * 8)
            i += 1
    return out


def classify(w):
    return "S" if w < SHORT_MAX else "M" if w < MEDIUM_MAX else "L" if w < LONG_MAX else "|"


def segments(sym):
    """Split the wave symbols at pauses ('|')."""
    return [s for s in sym.split("|") if len(s) > 50]


def bytes_of(seg):
    """Decode every byte marker in a segment; returns (bytes, parity errors, odd pairs)."""
    out, perr, bad, i = [], 0, 0, 0
    while True:
        i = seg.find("LM", i)
        if i < 0 or i + 2 + 18 > len(seg):
            break
        bits = []
        for k in range(9):
            pair = seg[i + 2 + 2 * k:i + 4 + 2 * k]
            bits.append(0 if pair == "SM" else 1 if pair == "MS" else None)
        if None in bits:
            bad += 1
            i += 2
            continue
        val = sum(b << n for n, b in enumerate(bits[:8]))
        if (sum(bits[:8]) + bits[8]) % 2 != 1:
            perr += 1
        out.append(val)
        i += 20
    return out, perr, bad


def blocks(seg_bytes):
    """Split a segment's bytes into its two copies by the countdown."""
    found = []
    for first in (0x89, 0x09):
        cd = list(range(first, first - 9, -1))
        for i in range(len(seg_bytes) - 9):
            if seg_bytes[i:i + 9] == cd:
                found.append((first, i + 9))
                break
    found.sort(key=lambda x: x[1])
    out = []
    for n, (first, start) in enumerate(found):
        end = found[n + 1][1] - 9 if n + 1 < len(found) else len(seg_bytes)
        body = seg_bytes[start:end]
        out.append((first, body))
    return out


def xor(b):
    x = 0
    for v in b:
        x ^= v
    return x


def decode(path, verbose=False):
    """Return a list of (kind, info, payload) per block, each copy checked."""
    sym = "".join(classify(w) for w in waves(path))
    result = []
    for n, seg in enumerate(segments(sym)):
        data, perr, bad = bytes_of(seg)
        copies = blocks(data)
        checked = []
        for first, body in copies:
            payload, chk = body[:-1], body[-1] if body else None
            checked.append((first, bytes(payload), chk == xor(payload)))
        if verbose:
            print(f"  segment {n}: {len(seg)} waves, {len(data)} bytes, parity errors {perr}, odd pairs {bad}, "
                  + ", ".join(f"copy ${f:02X} {len(p)} bytes checksum {'ok' if ok else 'BAD'}" for f, p, ok in checked))
        good = [p for f, p, ok in checked if ok]
        same = len({p for f, p, ok in checked}) == 1
        result.append(dict(segment=n, payload=good[0] if good else (checked[0][1] if checked else b""),
                           copies=len(checked), all_ok=all(ok for _, _, ok in checked) and len(checked) == 2,
                           copies_agree=same, parity_errors=perr))
    return result


def programs(path):
    """Each program on the tape: header fields and the checked data block."""
    out, header = [], None
    for b in decode(path):
        p = b["payload"]
        if not (b["all_ok"] and b["copies_agree"]):
            raise SystemExit(f"{path}: segment {b['segment']} has a bad or disagreeing copy")
        if header is None and len(p) == 192 and p[0] in (1, 3, 4, 5):
            header = dict(type=p[0], start=p[1] | p[2] << 8, end=p[3] | p[4] << 8,
                          name=bytes(p[5:21]).decode("latin-1").rstrip())
        elif header:
            out.append(dict(header, data=bytes(p)))
            header = None
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tap")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    blks = decode(args.tap, args.verbose)
    header, prg_n = None, 0
    for b in blks:
        p = b["payload"]
        status = f"2 copies {'ok' if b['all_ok'] else 'NOT ok'}, {'agree' if b['copies_agree'] else 'DIFFER'}"
        if header is None and len(p) == 192 and p[0] in (1, 3, 4, 5):
            start, end = p[1] | p[2] << 8, p[3] | p[4] << 8
            name = bytes(p[5:21]).decode("latin-1").rstrip()
            header = (p[0], start, end, name)
            print(f"header: type {p[0]}, ${start:04X}–${end - 1:04X}, name {name!r}; {status}")
        elif header:
            typ, start, end, name = header
            print(f"  data: {len(p)} bytes (header says {end - start}); {status}")
            if args.out:
                args.out.mkdir(parents=True, exist_ok=True)
                f = args.out / f"{Path(args.tap).stem}_{prg_n}.prg"
                f.write_bytes(bytes([start & 0xFF, start >> 8]) + p)
                print(f"  -> {f}")
                prg_n += 1
            header = None
        else:
            print(f"block of {len(p)} bytes without a header; {status}")


if __name__ == "__main__":
    main()
