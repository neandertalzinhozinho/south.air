import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_RDX

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

# scan plugin override cluster for AudioBuffer-style access: [rdx+8] then [reg+reg*8]
seen = {}
for b, e, u in re_lib.funcs():
    if not (0x34B000 <= b < 0x360000):
        continue
    ins_list = list(md.disasm(d[b:e], b))
    hits = 0
    bufread = 0
    for i, ins in enumerate(ins_list):
        if ins.mnemonic == 'mov' and len(ins.operands) == 2:
            dst, src = ins.operands
            if src.type == X86_OP_MEM and src.mem.base == X86_REG_RDX and src.mem.disp == 8 and dst.type == X86_OP_REG:
                bufread += 1
                # look ahead for [reg + reg*8]
                for j in range(i + 1, min(i + 12, len(ins_list))):
                    n = ins_list[j]
                    for op in n.operands:
                        if op.type == X86_OP_MEM and op.mem.index != 0 and op.mem.scale == 8:
                            hits += 1
    if bufread or hits:
        print(f'0x{b:X} size={e-b} ins={len(ins_list)} [rdx+8]={bufread} scaled8={hits}')
