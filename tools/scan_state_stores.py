#!/usr/bin/env python3
"""Find stores whose displacement matches the state struct fields read by 0x8B3ED0.

State base = engine+0x54 (proved: 00863905 arg5 -> 0086FF... arg7 -> [rcx+0x2c38]).
Fields read (RVA 008B3F5C-008B3FBA): +0x00 f32, +0x04 f32, +0x28 f32, +0x3C f32,
+0x4C f32, +0x52 u8.

Two hypotheses are scanned:
  H1 base = engine pointer, disps 0x54,0x58,0x7c,0x90,0xa0,0xa6
  H2 base = state pointer,  disps 0x00,0x04,0x28,0x3c,0x4c,0x52
Report functions with >=2 matching stores (H1) or >=3 (H2), with every site.
"""
import struct
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP

H1 = {0x54, 0x58, 0x7C, 0x90, 0xA0, 0xA6}
H2 = {0x00, 0x04, 0x28, 0x3C, 0x4C, 0x52}

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

d = re_lib.data()
lo, hi = 0x1000, 0x1CD6487

hits1 = defaultdict(list)
hits2 = defaultdict(list)

for ins in md.disasm(d[lo:hi], lo):
    if not ins.operands:
        continue
    # store: first operand is memory, mnemonic starts with mov/add/sub/and/or/xor/mul/div/inc/dec/...
    op0 = ins.operands[0]
    if op0.type != X86_OP_MEM:
        continue
    base = op0.mem.base
    if base in (0, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP):
        continue
    disp = op0.mem.disp
    f = re_lib.func_at(ins.address)
    fn = f[0] if f else None
    if disp in H1:
        hits1[fn].append((ins.address, ins.mnemonic, ins.op_str))
    if disp in H2:
        hits2[fn].append((ins.address, ins.mnemonic, ins.op_str))

print("=== H1 (base=engine, disp 0x54/0x58/0x7c/0x90/0xa0/0xa6): functions with >=2 ===")
for fn, sites in sorted(hits1.items(), key=lambda kv: -len(kv[1])):
    if len(sites) >= 2:
        print("\nfunction 0x%X (%d sites)" % (fn, len(sites)))
        for a, m, o in sites:
            print("  %08X  %-8s %s" % (a, m, o))

print("\n=== H2 (base=state, disp 0x00/0x04/0x28/0x3c/0x4c/0x52): functions with >=3 ===")
for fn, sites in sorted(hits2.items(), key=lambda kv: -len(kv[1])):
    if len(sites) >= 3:
        print("\nfunction 0x%X (%d sites)" % (fn, len(sites)))
        for a, m, o in sites:
            print("  %08X  %-8s %s" % (a, m, o))
