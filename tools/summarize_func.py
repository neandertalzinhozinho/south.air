import sys
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

rva = int(sys.argv[1], 0)
f = re_lib.func_at(rva)
if not f:
    print('not in a function'); sys.exit(1)
b, e, u = f
print(f'function 0x{b:X}..0x{e:X} size={e-b}')
d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
calls = {}
strings = []
n = 0
for ins in md.disasm(d[b:e], b):
    n += 1
    if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == 2:
        t = ins.operands[0].imm & 0xFFFFFFFFFFFFFFFF
        if 0x1000 <= t < 0x1D8BB7D:
            calls.setdefault(t, []).append(ins.address)
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
            if 0x1D8C000 <= t < 0x2758000 and re_lib.printable_at(t):
                s = re_lib.cstr(t, 70)
                strings.append((ins.address, t, s))
print('instructions', n)
print('--- direct calls (unique) ---')
for t in sorted(calls):
    cf = re_lib.func_at(t)
    sz = (cf[1]-cf[0]) if cf else 0
    print(f'  0x{t:X}  size={sz}  count={len(calls[t])}')
print('--- strings (first 80) ---')
for a, t, s in strings[:80]:
    print(f'  0x{a:X} -> 0x{t:X}  {s!r}')
print('--- callers ---')
for a, fb in re_lib.callers(b):
    print(f'  0x{a:X} in func 0x{fb:X}' if fb else f'  0x{a:X}')
