"""Read-only readers for the original media: PRG files, Oric TAP blocks and BASIC stubs.

Nothing here writes to an input file. Used by prg_info.py, disasm.py and new_project.py.
"""
import hashlib
from pathlib import Path

# BASIC tokens from $80, enough to read a SYS or CALL line. C16 BASIC 3.5 shares the
# C64's first tokens; $9E is SYS on both.
CBM_TOKENS = ("END FOR NEXT DATA INPUT# INPUT DIM READ LET GOTO RUN IF RESTORE GOSUB RETURN REM STOP ON "
              "WAIT LOAD SAVE VERIFY DEF POKE PRINT# PRINT CONT LIST CLR CMD SYS OPEN CLOSE GET NEW").split()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_prg(path):
    """Return (load_address, payload) of a CBM PRG: two-byte little-endian address, then data."""
    raw = Path(path).read_bytes()
    if len(raw) < 3:
        raise ValueError(f"{path}: too short for a PRG")
    return raw[0] | raw[1] << 8, raw[2:]


def tap_blocks(path):
    """Yield the blocks of an Oric .TAP: dict(name, type, auto, start, end, header, data, offset)."""
    d = Path(path).read_bytes()
    i = 0
    while (j := d.find(b"\x16\x16\x16", i)) >= 0:
        k = j
        while k < len(d) and d[k] == 0x16:
            k += 1
        if k >= len(d) or d[k] != 0x24:
            i = k
            continue
        h = d[k + 1:k + 10]
        n = d.index(0, k + 10)
        start, end = h[6] << 8 | h[7], h[4] << 8 | h[5]
        data = d[n + 1:n + 1 + end - start + 1]  # end address is inclusive
        yield dict(name=d[k + 10:n].decode("ascii", "replace"), type=h[2], auto=h[3], start=start,
                   end=end, header=bytes(h), data=data, offset=j)
        i = n + 1 + len(data)


def cbm_basic_lines(load, data):
    """Decode the BASIC lines of a CBM program loaded at `load`. Returns (lines, end_address)."""
    lines, p = [], 0
    while p + 4 <= len(data):
        link = data[p] | data[p + 1] << 8
        if link == 0:
            return lines, load + p + 2
        number = data[p + 2] | data[p + 3] << 8
        q, text, quote = p + 4, "", False
        while q < len(data) and data[q]:
            c = data[q]
            quote ^= c == 0x22
            if c >= 0x80 and not quote:
                text += CBM_TOKENS[c - 0x80] if c - 0x80 < len(CBM_TOKENS) else f"{{${c:02X}}}"
            else:
                text += chr(c) if 32 <= c < 127 else f"{{${c:02X}}}"
            q += 1
        lines.append((number, text))
        if not load < link <= load + len(data):
            break
        p = link - load
    return lines, None


def basic_entry(machine, load, data):
    """If the program starts with a BASIC stub that SYSes into itself, return (lines, stub_end, entry)."""
    if machine != "c16" or load not in (0x1001, 0x0801):
        return None
    lines, end = cbm_basic_lines(load, data)
    if not lines or end is None:
        return None
    for _, text in lines:
        if text.startswith("SYS"):
            rest = text[3:].lstrip(" (")
            digits = rest[:len(rest) - len(rest.lstrip("0123456789"))]
            if digits:
                return lines, end, int(digits)
    return lines, end, None
