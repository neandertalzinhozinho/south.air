import struct, collections
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
IB=0x180000000; SIZE=0x82a8000
cands=[0x1b8c0000,0x1b800000,0x1b8d0000,0x1b8a0000,0x1b900000,0x1b000000,0x180000000]
for B in cands:
    good=0;tot=0
    for o in range(0x1d8c000,0x217f000,8):
        v=struct.unpack_from('<Q',d,o)[0]
        if v>0x10000:
            tot+=1
            if 0<=v-B<SIZE: good+=1
    print(hex(B),'good',good,'of',tot, round(100*good/tot,2),'%')
# specific: pointer to help string rva 0x1fbf760
for B in cands:
    v=B+0x1fbf760
    if v<2**64:
        b=struct.pack('<Q',v)
        print('string ptr base',hex(B),hex(v),'count',d.count(b))
# check code at 0x17518
from capstone import *
md=Cs(CS_ARCH_X86,CS_MODE_64)
print('disasm 0x17518')
for ins in md.disasm(d[0x17510:0x17560],0x17510):
    print('  %x %s %s'%(ins.address,ins.mnemonic,ins.op_str))
print('qwords at 0x17500:', [hex(struct.unpack_from('<Q',d,0x17500+i*8)[0]) for i in range(8)])
