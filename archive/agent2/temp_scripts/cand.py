import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_RDX, X86_REG_R8

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
T0, T1 = 0x1000, 0x1CD6487

cands = [0x350F20, 0x34F970, 0x353510, 0x354F90, 0x356970, 0x3589B0, 0x359F70,
         0x34C400, 0x34DB80, 0x34C3F0]

print('#### candidate buffer-arg analysis')
for rva in cands:
    f = re_lib.func_at(rva)
    if not f:
        print(f'0x{rva:X} no func'); continue
    b, e, u = f
    rdx_mem = {}
    r8_mem = {}
    n = 0
    bad = 0
    for ins in md.disasm(d[b:e], b):
        n += 1
        if n > 6000: break
        for op in ins.operands:
            if op.type == X86_OP_MEM:
                if op.mem.base == X86_REG_RDX:
                    rdx_mem[op.mem.disp] = rdx_mem.get(op.mem.disp, 0) + 1
                elif op.mem.base == X86_REG_R8:
                    r8_mem[op.mem.disp] = r8_mem.get(op.mem.disp, 0) + 1
    print(f'0x{rva:X} size={e-b} ins={n} rdx_disp={sorted(rdx_mem.items())[:12]} r8_disp={sorted(r8_mem.items())[:8]}')

print('#### refs to window tables')
def find_lea(target_rva, limit=25):
    out = []
    for i in range(T0, T1 - 8):
        if d[i] != 0x8D: continue
        modrm = d[i + 1]
        if (modrm & 0xC7) != 0x05: continue
        disp = struct.unpack_from('<i', d, i + 2)[0]
        if i + 6 + disp == target_rva:
            f = re_lib.func_at(i)
            out.append((i, f[0] if f else None))
            if len(out) >= limit: break
    return out

for t in (0x1DF3F80, 0x2037240):
    print(f'--- 0x{t:X}')
    for i, fb in find_lea(t):
        print(f'   0x{i:X} in func 0x{fb:X}' if fb else f'   0x{i:X}')
