import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
BASE = re_lib.BASE
VT = 0x2037A58


def show(rva, n=8):
    f = re_lib.func_at(rva)
    if not f:
        print(f'    0x{rva:X}: <no pdata> {d[rva:rva+12].hex()}')
        return
    b, e, u = f
    k = 0
    for ins in md.disasm(d[b:min(e, b + 60)], b):
        print(f'      {ins.address:08X}: {ins.mnemonic} {ins.op_str}')
        k += 1
        if k >= n or ins.mnemonic == 'ret':
            break


print('#### FFT kernel callers')
for k in (0x17280, 0x17380, 0x17820, 0x17900, 0x17A00):
    cs = re_lib.callers(k, 12)
    print(f'  0x{k:X} -> {[(hex(a), hex(fb) if fb else None) for a, fb in cs]}')

print('#### derived vtable small slots')
n = 0
while True:
    v = struct.unpack_from('<Q', d, VT + 8 * n)[0]
    if not (0x1000 <= v - BASE < 0x1D8BB7D):
        break
    rva = v - BASE
    f = re_lib.func_at(rva)
    if f and f[1] - f[0] <= 260:
        print(f'  slot {n}: 0x{rva:X} size={f[1]-f[0]}')
        show(rva, 10)
    n += 1
print('slots:', n)
