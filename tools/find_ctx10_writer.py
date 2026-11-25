#!/usr/bin/env python3
"""Stage C: locate the writer of ctx+0x10 (pointer to the {begin,end} pair).

Strategy: find every `mov [reg+0x10], reg` store inside functions that also
reference the proven ctx fields (0x2C28/0x2C30/0x2C38, 0x404/0x400, 0x978/0x980).
Those disambiguate the big per-channel context from unrelated objects.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM, CS_OP_REG

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
d = re_lib.data()

CTX_MARKS = {0x2C28, 0x2C30, 0x2C38, 0x404, 0x400, 0x978, 0x980, 0x1498, 0x1528}
starts = {}
for b, e, u in re_lib.funcs():
    starts.setdefault(b, e)

seen = set()
for b, e in sorted(starts.items()):
    if not (0x800000 <= b < 0x8D2000):   # DSP region only
        continue
    insns = [x for x in md.disasm(d[b:e], b) if x.address not in seen]
    for x in insns:
        seen.add(x.address)
    marks = set()
    for x in insns:
        for op in x.operands:
            if op.type == CS_OP_MEM and op.mem.disp in CTX_MARKS:
                marks.add(op.mem.disp)
    if not marks:
        continue
    for x in insns:
        if x.mnemonic != "mov" or len(x.operands) != 2:
            continue
        dst, src = x.operands
        if dst.type != CS_OP_MEM or dst.mem.disp != 0x10:
            continue
        if src.type == CS_OP_MEM and src.mem.disp == 0:
            pass
        print(f"0x{x.address:08X} func=0x{b:X} {x.mnemonic} {x.op_str}   marks={sorted(hex(m) for m in marks)}")
