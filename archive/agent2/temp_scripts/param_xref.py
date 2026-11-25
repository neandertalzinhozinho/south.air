import collections
from capstone import *
from capstone.x86 import *
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
hits=[]
addr=0x1000; last=addr
while addr<0x1cd6487:
    got=0
    for ins in md.disasm(d[addr:min(addr+0x2000,0x1cd6487)], addr):
        got+=1; last=ins.address
        for op in ins.operands:
            if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
                t=(ins.address+ins.size+op.mem.disp)&0xffffffffffffffff
                if 0x238e000<=t<0x2392500:
                    hits.append((ins.address,hex(t),ins.mnemonic,ins.op_str))
    addr=last+1 if got else addr+1
print('hits',len(hits))
for h in hits[:60]: print(hex(h[0]),h[1],h[2],h[3])
