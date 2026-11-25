import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = re_lib.data()
print('funcs parsed:', len(re_lib.funcs()))
print('first 5:', [(hex(b), hex(e)) for b, e, u in re_lib.funcs()[:5]])
print('last 5:', [(hex(b), hex(e)) for b, e, u in re_lib.funcs()[-5:]])

md = Cs(CS_ARCH_X86, CS_MODE_64)
for rva in [0x319180, 0x319080, 0x314B10, 0x1798F12, 0x336BA0, 0x325960, 0x363460, 0x353500, 0x48A440, 0x490F00]:
    f = re_lib.func_at(rva)
    print(f'--- 0x{rva:X} func_at={f and (hex(f[0]), f[1]-f[0])} bytes={d[rva:rva+16].hex()}')
    for ins in md.disasm(d[rva:rva+40], rva):
        print('    ', ins.mnemonic, ins.op_str)
        if ins.mnemonic in ('ret', 'jmp'):
            break
