import struct,sys
from pathlib import Path
sys.path.insert(0,"tools")
import re_lib
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
from capstone.x86 import X86_OP_MEM,X86_OP_IMM,X86_REG_RIP
d=re_lib.data()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
sys.path.insert(0,"tools")
import show_func
b=0x8C1440
e,_=show_func.chain_extent(d,b)
print("func",hex(b),hex(e),"size",e-b)
calls={}
consts={}
for ins in md.disasm(d[b:e],b):
    for op in ins.operands:
        if op.type==X86_OP_IMM and ins.mnemonic=="call":
            calls.setdefault(op.imm,0); calls[op.imm]+=1
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
            t=ins.address+ins.size+op.mem.disp
            if 0x1D8C000<=t<0x217F000 or 0x217F000<=t:
                f=struct.unpack_from("<f",d,t)[0]
                if abs(f)>1e-12 and abs(f)<1e12:
                    consts.setdefault((t,f),0); consts[(t,f)]+=1
print("CALLS",len(calls))
for k in sorted(calls): print(hex(k),calls[k])
print("CONSTS",len(consts))
for (t,f),c in sorted(consts.items()): print(hex(t),repr(f),"x",c)
