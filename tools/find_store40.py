#!/usr/bin/env python3
"""List every instruction in a window that WRITES float data at [reg+0x40].

Narrow probe for the 32-float kernel block at ctx+0x40 used by 0x8B2C30
(see checks/8b2c30.dis / checks/8b2680.dis). Chain-aware, read-only.
"""
import struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from show_func import chain_extent
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

PDATA_RVA = 0x2758000
PDATA_MAX = 0x5223000
lo = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x870000
hi = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x8E0000

d = re_lib.data()
starts = []
for i in range(0, PDATA_MAX, 12):
    b, e, u = struct.unpack_from("<III", d, PDATA_RVA + i)
    if b == 0 and e == 0:
        break
    if lo <= b < hi and e > b:
        starts.append(b)

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
seen = set()
for s in starts:
    if s in seen:
        continue
    end, size = chain_extent(d, s)
    if not end:
        continue
    for x in md.disasm(d[s:end], s):
        if x.address in seen:
            continue
        seen.add(x.address)
        if not x.operands or x.operands[0].type != X86_OP_MEM:
            continue
        if x.operands[0].mem.disp != 0x40:
            continue
        if not x.mnemonic.startswith("mov"):
            continue
        print("0x%08X  func 0x%08X  %-8s %s" % (x.address, s, x.mnemonic, x.op_str))
