import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True


def brief(rva, maxins=4000):
    f = re_lib.func_at(rva)
    if not f:
        print(f'0x{rva:X}: not a function start'); return
    b, e, u = f
    calls = {}
    strs = []
    vt = []
    n = 0
    for ins in md.disasm(d[b:e], b):
        n += 1
        if n > maxins: break
        if ins.mnemonic == 'call' and ins.operands:
            o = ins.operands[0]
            if o.type == 2 and 0x1000 <= o.imm < 0x1D8BB7D:
                calls.setdefault(o.imm, 0)
                calls[o.imm] += 1
            elif o.type == 3 and o.mem.base not in (0,) and o.mem.disp:
                pass
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                if re_lib.printable_at(t) and 0x1D8C000 <= t < 0x2758000:
                    s = re_lib.cstr(t, 40)
                    if (t, s) not in strs: strs.append((t, s))
    print(f'=== 0x{b:X} size={e-b} ins={n}')
    print('  calls:', ', '.join(f'0x{t:X}({c})' for t, c in sorted(calls.items())[:40]))
    print('  strings:', [s for _, s in strs[:12]])


for a in sys.argv[1:]:
    brief(int(a, 0))
