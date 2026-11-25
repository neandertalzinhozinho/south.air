import struct, math, collections
from capstone import *
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
# entropy per 64k over .text
def ent(b):
    if not b: return 0
    c=collections.Counter(b); n=len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())
print('windows:')
for off in range(0x1000, 0x1000+0x1cd5487, 0x400000):
    print(hex(off), round(ent(d[off:off+0x400000]),2))
md=Cs(CS_ARCH_X86, CS_MODE_64); md.detail=False
for base in [0x1000, 0x2000, 0x100000, 0x1000000]:
    print('=== disasm at',hex(base))
    n=0
    for ins in md.disasm(d[base:base+256], base):
        print('  %x: %s %s'%(ins.address, ins.mnemonic, ins.op_str)); n+=1
        if n>=12: break
