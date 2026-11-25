#!/usr/bin/env python3
"""Scan .text for RIP-less memory operands with a given displacement.

Usage: py tools/scan_disp.py 0x1410 [0x1408 ...]
Prints every instruction referencing [reg +/- disp] with function RVA.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
d = re_lib.data()

DISPS = {int(x, 16) for x in sys.argv[1:]} or {0x1410}
starts = {}
for b, e, u in re_lib.funcs():
    starts.setdefault(b, e)

seen = set()
for b, e in sorted(starts.items()):
    if not (0x1000 <= b < 0x1CD6487):
        continue
    for ins in md.disasm(d[b:e], b):
        if ins.address in seen:
            continue
        seen.add(ins.address)
        for op in ins.operands:
            if op.type == CS_OP_MEM and op.mem.disp in DISPS:
                print(f"0x{ins.address:08X} func=0x{b:X} {ins.mnemonic} {ins.op_str}")
                break
