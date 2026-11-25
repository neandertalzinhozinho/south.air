#!/usr/bin/env python3
"""Resolve any ipp stub (movsxd/lea/jmp pattern) or trampoline to impl RVA."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

d = re_lib.data()
BASE = 0x199B0000
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def rips(rva, n=2):
    out = []
    for ins in md.disasm(d[rva:rva + 24], rva):
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                out.append((ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF)
        if len(out) >= n:
            break
    return out


def resolve(rva, depth=0):
    b = d[rva:rva + 8]
    # mov rax,[rip+x]; jmp rax  (trampoline)
    if b[0:3] == b"\x48\x8b\x05" and b[7] == 0xE0 or (b[0:2] == b"\x48\x8b" and b[6:8] == b"\xff\xe0"):
        t = rips(rva, 1)[0]
        ptr = re_lib.u64(t)
        impl = ptr - BASE if BASE <= ptr < BASE + len(d) else ptr
        return resolve(impl, depth + 1) if depth < 3 else impl
    if b[0] == 0xF3 and b[1] == 0x0F and b[2] == 0x1E:  # endbr64
        b = d[rva + 4:rva + 12]
        rva = rva + 4
    if b[0:3] == b"\x48\x63\x05":  # movsxd rax,[rip+x]
        t1, t2 = rips(rva, 2)
        lvl = re_lib.u32(t1)
        ptr = re_lib.u64(t2 + 8 * lvl)
        impl = ptr - BASE if BASE <= ptr < BASE + len(d) else ptr
        return resolve(impl, depth + 1) if depth < 3 else impl
    return rva


for a in sys.argv[1:]:
    rva = int(a, 0)
    print("0x%X -> 0x%X" % (rva, resolve(rva)))

# scalar values of interest
for t in (0x2079EA8, 0x2079EAC):
    import struct
    print("f32 @0x%X = %.9g  (u32=0x%08X)" % (t, struct.unpack_from("<f", d, t)[0], re_lib.u32(t)))
