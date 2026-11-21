"""Hardware and ROM names that disasm.py gives da65, per machine.

Only fixed hardware and ROM addresses belong here, never a game's own layout.
C16 TED names follow the usual Plus/4 register map; the Oric names come from
Hopper (src/oric.inc, src/vars.inc) and Light Cycle (tools/symbols.py), BASIC
1.0. Check a name against a reference before building an argument on it, and
add sources to the skill's references when one is confirmed.
"""

C16 = {
    # TED timers, control, keyboard, interrupts
    0xFF00: "TED_T1_LO", 0xFF01: "TED_T1_HI", 0xFF02: "TED_T2_LO", 0xFF03: "TED_T2_HI",
    0xFF04: "TED_T3_LO", 0xFF05: "TED_T3_HI",
    0xFF06: "TED_CTRL1", 0xFF07: "TED_CTRL2", 0xFF08: "TED_KEYLATCH",
    0xFF09: "TED_IRQ_FLAGS", 0xFF0A: "TED_IRQ_MASK", 0xFF0B: "TED_RASTER_CMP",
    0xFF0C: "TED_CURSOR_HI", 0xFF0D: "TED_CURSOR_LO",
    # TED sound (see the skill's references/c16/machine.md)
    0xFF0E: "TED_V1_FREQ_LO", 0xFF0F: "TED_V2_FREQ_LO", 0xFF10: "TED_V2_FREQ_HI",
    0xFF11: "TED_SOUND_CTRL", 0xFF12: "TED_BITMAP_V1HI",
    # TED video
    0xFF13: "TED_CHARSET", 0xFF14: "TED_SCREEN_BASE",
    0xFF15: "TED_BG0", 0xFF16: "TED_BG1", 0xFF17: "TED_BG2", 0xFF18: "TED_BG3", 0xFF19: "TED_BORDER",
    0xFF1A: "TED_BMRELOAD_HI", 0xFF1B: "TED_BMRELOAD_LO", 0xFF1C: "TED_VLINE_HI", 0xFF1D: "TED_VLINE_LO",
    0xFF1E: "TED_HPOS", 0xFF1F: "TED_BLINK_VSUB",
    0xFF3E: "TED_ROM_ON", 0xFF3F: "TED_RAM_ON",
    # KERNAL jump table (same entries as the C64)
    0xFFC0: "KERNAL_OPEN", 0xFFC3: "KERNAL_CLOSE", 0xFFC6: "KERNAL_CHKIN", 0xFFC9: "KERNAL_CHKOUT",
    0xFFCC: "KERNAL_CLRCHN", 0xFFCF: "KERNAL_CHRIN", 0xFFD2: "KERNAL_CHROUT", 0xFFD5: "KERNAL_LOAD",
    0xFFD8: "KERNAL_SAVE", 0xFFBA: "KERNAL_SETLFS", 0xFFBD: "KERNAL_SETNAM", 0xFFE1: "KERNAL_STOP",
    0xFFE4: "KERNAL_GETIN", 0xFFE7: "KERNAL_CLALL",
    # Vectors
    0xFFFA: "VEC_NMI", 0xFFFC: "VEC_RESET", 0xFFFE: "VEC_IRQ",
}

ORIC = {
    # 6522 VIA
    0x0300: "VIA_ORB", 0x0301: "VIA_ORA", 0x0302: "VIA_DDRB", 0x0303: "VIA_DDRA",
    0x0304: "VIA_T1CL", 0x0305: "VIA_T1CH", 0x0306: "VIA_T1LL", 0x0307: "VIA_T1LH",
    0x0308: "VIA_T2CL", 0x0309: "VIA_T2CH", 0x030A: "VIA_SR", 0x030B: "VIA_ACR",
    0x030C: "VIA_PCR", 0x030D: "VIA_IFR", 0x030E: "VIA_IER", 0x030F: "VIA_ORA_NH",
    # BASIC 1.0 workspace (skill: references/oric/rom.md)
    0x0012: "ROM_CURPTR", 0x020F: "ROM_SCRATCH", 0x022B: "NMI_VECTOR", 0x0269: "ROM_CURCOL",
    0x026A: "ROM_SCRFLAGS", 0x0271: "ROM_TIMERS", 0x02DF: "ROM_KEY",
    # Fixed video memory
    0xA000: "HIRES_SCREEN", 0xB400: "STD_CHARSET", 0xB800: "ALT_CHARSET", 0xBB80: "TEXT_SCREEN",
    0xBFDF: "SCREEN_LAST",
}

MACHINES = {"c16": C16, "oric": ORIC}
