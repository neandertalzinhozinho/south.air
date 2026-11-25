import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
BASE=0x199b0000; T0,T1=0x1000,0x1d8bb7d
d=re_lib.data()

def vlen(vt):
    n=0
    while True:
        v=struct.unpack_from('<Q',d,vt+8*n)[0]
        if not (T0<=v-BASE<T1): break
        n+=1
        if n>2000: break
    return n

for rva in [int(x,0) for x in sys.argv[1:]]:
    f=re_lib.func_at(rva)
    if not f: print(hex(rva),'no func'); continue
    b,e,u=f
    md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
    seen={}
    for ins in md.disasm(d[b:e],b):
        for op in ins.operands:
            if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
                t=(ins.address+ins.size+op.mem.disp)&0xFFFFFFFFFFFFFFFF
                if 0x1d8c000<=t<0x2758000:
                    seen.setdefault(t,[]).append(ins.address)
    print('=== func',hex(b),'size',e-b)
    for t,addrs in seen.items():
        n=vlen(t)
        if n>=5:
            print('  vt?',hex(t),'len',n,'refs',[hex(a) for a in addrs[:4]])
