#!/usr/bin/env python3
"""Resolve IPP dispatch stubs at low RVAs: stub -> table -> entry[cpu_level] -> impl RVA."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

d = re_lib.data()
BASE = 0x199B0000  # runtime base used by absolute pointers in .data
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def rips(rva, n=3):
    out = []
    for ins in md.disasm(d[rva:rva + 16], rva):
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                out.append((ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF)
        if len(out) >= n:
            break
    return out


level = re_lib.u32(0x21C7408)
print("cpu level index @0x21C7408 =", level)

stubs = [0x1010, 0x10D0, 0x1190, 0x11F0, 0x1220, 0x1280, 0x1580,
         0x1C84A0, 0x1C84D0, 0x1C8500, 0x1C8530]
for rva in stubs:
    t1, t2 = rips(rva, 2)
    lvl = re_lib.u32(t1)
    ptr = re_lib.u64(t2 + 8 * lvl)
    impl = ptr - BASE if BASE <= ptr < BASE + len(d) else ptr
    print("stub 0x%X: level@0x%X=%d table=0x%X entry[%d]=0x%X -> impl RVA 0x%X"
          % (rva, t1, lvl, t2, lvl, ptr, impl))
    # also print all 8 entries
    print("   entries:", " ".join("0x%X" % (re_lib.u64(t2 + 8 * i) - BASE
                                            if BASE <= re_lib.u64(t2 + 8 * i) < BASE + len(d)
                                            else re_lib.u64(t2 + 8 * i)) for i in range(8)))
