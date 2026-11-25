import struct,sys
sys.path.insert(0,r"D:\PROJETOS\soultree\tools")
d=open(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin","rb").read()
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
import show_func
entries={}
for i in range(0,0x5223000,12):
    b,e,u=struct.unpack_from("<III",d,0x2758000+i)
    if b==0 and e==0: break
    if e>b: entries[b]=(e,u)
starts=sorted(entries)
want={"divss","maxss","minss","sqrtss","rcpss"}
res=[]
for s in starts:
    if not (0x8A0000<=s<0x8E0000): continue
    e,_=show_func.chain_extent(d,s)
    if e is None: continue
    for ins in md.disasm(d[s:e],s):
        if ins.mnemonic in want:
            res.append((ins.address,s,ins.mnemonic,ins.op_str))
print(len(res))
for a,s,m,o in res:
    print(f"0x{a:08X} f=0x{s:X} {m} {o}")
