# Decomposition project (c16). `make verify` is the gate: it must pass after every change.
PY ?= python3

all: disasm

# Regenerate src/*.s from tools/symbols.py and check every block rebuilds byte for byte.
disasm:
	$(PY) tools/disasm.py

# Originals unchanged, and src/*.s as committed rebuilds every block byte for byte.
verify:
	cd original && shasum -a 256 -c SHA256SUMS
	$(PY) tools/unpack_sfx.py --check
	$(PY) tools/tape_check.py
	$(PY) tools/disasm.py --check

# Describe the original files.
info:
	$(PY) tools/prg_info.py --machine c16 original/*

# PART=one (default) or two. `run` starts the rebuilt packed PRG (decruncher and all);
# `run-unpacked` loads the rebuilt game image and jumps to its entry, skipping the decruncher.
PART ?= one
ENTRY_one = 1010
ENTRY_two = 2111

run: disasm
	$(PY) tools/run_vice.py build/day_$(PART)_packed.prg

run-unpacked: disasm
	$(PY) tools/run_vice.py build/day_$(PART).prg --entry $(ENTRY_$(PART))

run-original:
	$(PY) tools/run_vice.py original/daley_thompsons_star_events_day_$(PART).prg

# Documentation: the generated code reference and the offline HTML handbook (needs Node 20+).
NODE ?= node

docs:
	$(PY) tools/code_reference.py
	$(NODE) scripts/build_docs.mjs

docs-check:
	$(PY) tools/code_reference.py --check
	$(NODE) scripts/build_docs.mjs --check

clean:
	rm -rf build

.PHONY: all disasm verify info run run-unpacked run-original docs docs-check clean
