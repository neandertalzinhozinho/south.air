import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

targets = {int(x, 0): [] for x in sys.argv[1:]}
d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
lo, hi = 0x1000, 0x1D8BB7D
chunk = d[lo:hi]
for ins in md.disasm(chunk, lo):
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
            if t in targets:
                f = re_lib.func_at(ins.address)
                targets[t].append((ins.address, f[0] if f else 0, f[1] if f else 0))
for t, hits in targets.items():
    print(f'target 0x{t:X}: {len(hits)} refs')
    for a, fb, fe in hits[:20]:
        print(f'   ref 0x{a:X} in func 0x{fb:X} size={fe-fb if fb else 0}')
