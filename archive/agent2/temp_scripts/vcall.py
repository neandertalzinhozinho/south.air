import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True


def vcalls(rva):
    """indirect calls/jmps through [reg+disp]"""
    f = re_lib.func_at(rva)
    if not f:
        print(f'0x{rva:X} not a function'); return []
    b, e, u = f
    out = []
    n = 0
    for ins in md.disasm(d[b:e], b):
        n += 1
        if n > 6000: break
        if ins.mnemonic in ('call', 'jmp') and ins.operands:
            o = ins.operands[0]
            if o.type == X86_OP_MEM and o.mem.base != X86_REG_RIP:
                out.append((ins.address, ins.mnemonic, o.mem.base, o.mem.disp))
    return out


for a in sys.argv[1:]:
    rva = int(a, 0)
    f = re_lib.func_at(rva)
    sz = (f[1] - f[0]) if f else 0
    v = vcalls(rva)
    print(f'0x{rva:X} size={sz} vicalls={len(v)}')
    for addr, mn, base, disp in v[:14]:
        print(f'   0x{addr:X} {mn} [reg{base}+0x{disp:X}]  slot={disp//8 if disp>=0 else "?"}')
