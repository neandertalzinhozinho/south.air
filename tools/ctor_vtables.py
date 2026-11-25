import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_OP_REG

rva = int(sys.argv[1], 0)
b, e, u = re_lib.func_at(rva)
d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
last_lea = {}
for ins in md.disasm(d[b:e], b):
    # track lea reg, [rip+x]
    if ins.mnemonic == 'lea' and len(ins.operands) == 2 and ins.operands[0].type == X86_OP_REG:
        op = ins.operands[1]
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
            last_lea[ins.operands[0].reg] = (t, ins.address)
    # store reg -> [mem]
    if ins.mnemonic.startswith('mov') and len(ins.operands) == 2:
        dst, src = ins.operands
        if dst.type == X86_OP_MEM and src.type == X86_OP_REG and src.reg in last_lea:
            t, la = last_lea[src.reg]
            if 0x1D8C000 <= t < 0x2758000:
                print(f'  0x{ins.address:X}: store vtable 0x{t:X} -> mem {dst.mem.base}/{dst.mem.disp}  (lea@0x{la:X})')
