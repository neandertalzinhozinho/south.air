#!/usr/bin/env python3
"""Find stores that go through a pointer computed as `lea reg,[base+0x40]`.

Catches the compiler pattern
    lea  rX, [rCtx + 0x40]
    movups [rX], xmm        ; or movss [rX+4*k]
which the disp==0x40 scan misses. Bounded window, chain-aware, read-only.
"""
import struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from show_func import chain_extent
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG

PDATA_RVA = 0x2758000
PDATA_MAX = 0x5223000
lo = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x870000
hi = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x900000

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
    ins = [x for x in md.disasm(d[s:end], s) if x.address not in seen]
    for x in ins:
        seen.add(x.address)
    for i, x in enumerate(ins):
        if x.mnemonic != "lea" or len(x.operands) != 2:
            continue
        dst, src = x.operands
        if dst.type != X86_OP_REG or src.type != X86_OP_MEM or src.mem.disp != 0x40:
            continue
        r = dst.reg
        for y in ins[i + 1:i + 14]:
            if y.mnemonic in ("ret", "jmp") or (y.mnemonic == "call"):
                break
            if not y.operands or y.operands[0].type != X86_OP_MEM:
                continue
            m = y.operands[0].mem
            if m.base == r and m.index == 0 and m.disp < 0x80 and y.mnemonic.startswith("mov"):
                print("0x%08X func 0x%08X  lea %s,[%s] -> %-7s %s" %
                      (y.address, s, x.reg_name(r), x.op_str, y.mnemonic, y.op_str))
                break
