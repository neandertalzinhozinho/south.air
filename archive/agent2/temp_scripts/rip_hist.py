import struct, time, collections
from capstone import *
from capstone.x86 import *
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
START=0x1000; END=0x1cd6487
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
hist=collections.Counter(); ex={}
last=START; n=0; bad=0
addr=START
while addr<END:
    got=0
    for ins in md.disasm(d[addr:min(addr+0x1000,END)], addr):
        n+=1; got+=1; last=ins.address
        for op in ins.operands:
            if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
                tgt=(ins.address+ins.size+op.mem.disp)&0xffffffffffffffff
                b=tgt>>24; hist[b]+=1; ex.setdefault(b,(hex(ins.address),hex(tgt)))
    if got==0:
        bad+=1; addr+=1
    else:
        addr=last+1
print('insns',n,'bad bytes',bad,'last',hex(last))
for b,c in hist.most_common(15):
    print(hex(b<<24),c,ex[b])
