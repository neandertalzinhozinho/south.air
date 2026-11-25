import json,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
ROOT=Path(r'D:\PROJETOS\shadowFILES')
data=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
units={}
for rp in (ROOT/'analysis/recovered_native/units').glob('rva_*/roundtrip.json'):
    j=json.loads(rp.read_text())
    if not j.get('byte_identical'): continue
    s=int(j['start'],16); e=int(j['end_exclusive'],16)
    units[s]=(e,rp.parent.name)
starts=sorted(units)
PATCHED_EXPLICIT={0x1d8d720,0x1d8d730,0x1d8d740,0x1d8d750,0x1d8d7f0,0x1d8d808,0x1d8d8c8,0x1d8c3a0}
def owner(rva):
    import bisect
    k=bisect.bisect_right(starts,rva)-1
    if k>=0 and rva<units[starts[k]][0]: return starts[k]
    return None
seen=set(); queue=[0x8637d0]; stale=[]
depth={0x8637d0:0}
while queue:
    rva=queue.pop(0)
    if rva in seen or len(seen)>3000: continue
    seen.add(rva)
    o=owner(rva)
    if o is None: continue
    e,name=units[o]
    for i in md.disasm(data[o:e],0x18CC0000+o):
        a=i.address-0x18CC0000
        if i.mnemonic in ('call','jmp'):
            for op in i.operands:
                if op.type==2 and op.imm is not None:
                    t=op.imm-0x18CC0000
                    if 0<=t<len(data) and owner(t) is not None and depth.get(rva,0)<4:
                        if t not in seen: depth[t]=depth.get(rva,0)+1; queue.append(t)
                elif op.type==3 and op.mem.base==41 and op.size==8:
                    t=i.address+i.size+op.mem.disp-0x18CC0000
                    if t+8<=len(data):
                        v=struct.unpack_from('<Q',data,t)[0]
                        if 0x7FF000000000<=v<0x800000000000 and not (0x1d8c000<=t<0x1d8d000) and t not in PATCHED_EXPLICIT:
                            stale.append((a,name,i.mnemonic,t,v,depth.get(rva,0)))
print('visited units',len(seen))
print('stale indirect call sites',len(stale))
for x in sorted(set(stale)): print(x)
