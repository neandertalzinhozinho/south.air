import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

BASE = re_lib.BASE
d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True


def fninfo(rva):
    f = re_lib.func_at(rva)
    if not f:
        return None
    b, e, u = f
    return b, e, e - b


def refs(rva, limit=6):
    """strings + constants referenced inside function"""
    f = re_lib.func_at(rva)
    if not f:
        return [], []
    b, e, u = f
    strs, consts = [], []
    n = 0
    for ins in md.disasm(d[b:e], b):
        n += 1
        if n > 3000:
            break
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                if re_lib.printable_at(t) and 0x1D8C000 <= t < 0x2758000:
                    strs.append((ins.address, t, re_lib.cstr(t, 48)))
    return strs[:limit], []


def vlen(vt):
    n = 0
    while n < 300:
        v = struct.unpack_from('<Q', d, vt + 8 * n)[0]
        if not (0x1000 <= v - BASE < 0x1D8BB7D):
            break
        n += 1
    return n


for arg in sys.argv[1:]:
    vt = int(arg, 0)
    n = vlen(vt)
    print(f'=== vtable 0x{vt:X} len={n}')
    for i in range(n):
        v = struct.unpack_from('<Q', d, vt + 8 * i)[0]
        rva = v - BASE
        fi = fninfo(rva)
        if fi:
            b, e, sz = fi
            mark = '' if b == rva else f'  (+0x{rva-b:X} into fn)'
            s, _ = refs(rva)
            ss = ' | '.join(f'"{x[2]}"' for x in s[:4])
            print(f'  [{i:2d}] 0x{rva:X} size={sz:6d}{mark}  {ss}')
        else:
            print(f'  [{i:2d}] 0x{rva:X} NOT-A-FUNC-START  (raw 0x{v:X})')
