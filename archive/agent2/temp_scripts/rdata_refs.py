import collections
from capstone import *
from capstone.x86 import *
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
hist=collections.Counter()
addr=0x1000; n=0; last=addr
while addr<0x1cd6487:
    got=0
    for ins in md.disasm(d[addr:min(addr+0x2000,0x1cd6487)], addr):
        got+=1; n+=1; last=ins.address
        for op in ins.operands:
            if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
                t=(ins.address+ins.size+op.mem.disp)&0xffffffffffffffff
                if 0x1d8c000<=t<0x217f000:
                    hist[t>>16]+=1
    addr = last+1 if got else addr+1
print('total rip->rdata',sum(hist.values()))
for k,c in sorted(hist.items(), key=lambda kv:-kv[1])[:25]:
    print(hex(k<<16),c)
