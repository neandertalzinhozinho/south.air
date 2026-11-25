import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

BASE = 0x199B0000
T0, T1 = 0x1000, 0x1D8BB7D
d = re_lib.data()
FUNCS = {b: (b, e) for b, e, u in re_lib.funcs()}

def slot_target(vt, i):
    v = struct.unpack_from('<Q', d, vt + 8*i)[0]
    return v - BASE

def fstrs(b, e, limit=6):
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    out = []
    for ins in md.disasm(d[b:e], b):
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                if 0x1D8C000 <= t < 0x2758000 and re_lib.printable_at(t):
                    s = re_lib.cstr(t, 60)
                    if s and len(s) > 2 and s not in out:
                        out.append(s)
        if len(out) >= limit:
            break
    return out

def vlen(vt):
    n = 0
    while n < 300:
        v = struct.unpack_from('<Q', d, vt + 8*n)[0]
        if not (T0 <= v - BASE < T1):
            break
        n += 1
    return n

for vt in [int(x, 0) for x in sys.argv[1:]]:
    n = vlen(vt)
    print(f'=== vtable 0x{vt:X} len={n}')
    for i in range(min(n, 26)):
        t = slot_target(vt, i)
        f = FUNCS.get(t)
        if f:
            b, e = f
            ss = fstrs(b, e, 4)
            print(f'  [{i:2d}] 0x{t:X} size={e-b:<6} {" | ".join(ss)[:150]}')
        else:
            print(f'  [{i:2d}] 0x{t:X}  <not a function start>')
