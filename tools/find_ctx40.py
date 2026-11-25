#!/usr/bin/env python3
"""Find functions that pass `X+0x40` as the destination of a copy/transform call.

Used to locate the writer of the 32-float kernel block at ctx+0x40 in the
per-band context (see checks/8b2680.dis). Bounded, chain-aware, read-only.
"""
import struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from show_func import chain_extent
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM

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
    ins = list(md.disasm(d[s:end], s))
    for i, x in enumerate(ins):
        if x.mnemonic != "lea" or len(x.operands) != 2:
            continue
        dst, src = x.operands
        if dst.type != X86_OP_REG or src.type != X86_OP_MEM:
            continue
        if src.mem.disp != 0x40:
            continue
        # look ahead for a call, and whether this reg is its first arg
        for y in ins[i + 1:i + 9]:
            if y.mnemonic == "call":
                print("0x%08X lea %s <- %s ; then %s at 0x%08X" %
                      (x.address, x.reg_name(dst.reg), x.op_str, y.op_str, y.address))
                break
            if y.mnemonic in ("jmp", "ret", "jne", "je", "jb", "jae", "ja", "jbe"):
                break
