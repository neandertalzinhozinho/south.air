import json,bisect,struct
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
def owner(rva):
    k=bisect.bisect_right(starts,rva)-1
    if k>=0 and rva<units[starts[k]][0]: return starts[k]
    return None
parent={0x8637d0:None}; queue=[0x8637d0]
while queue and len(parent)<3000:
    rva=queue.pop(0); o=owner(rva)
    if o is None: continue
    e,name=units[o]
    for i in md.disasm(data[o:e],0x18CC0000+o):
        if i.mnemonic in ('call','jmp'):
            for op in i.operands:
                if op.type==2 and op.imm is not None:
                    t=op.imm-0x18CC0000
                    if owner(t) is not None and t not in parent:
                        parent[t]=(rva,i.address-0x18CC0000,name,i.mnemonic)
                        queue.append(t)
for target in (0x1c9ad2b,0x1799260,0x1c9ad37):
    print('=== chain to',hex(target),'===')
    cur=target; chain=[]
    while cur in parent and parent[cur] is not None:
        chain.append((cur,parent[cur])); cur=parent[cur][0]
    for a,p in reversed(chain): print(hex(a),'from',hex(p[0]),'site',hex(p[1]),p[2],p[3])
print('=== disasm 0x1c9ad2b ===')
o=owner(0x1c9ad2b); e,_=units[o]
for i in md.disasm(data[o:min(e,o+100)],0x18CC0000+o):
    print(f'{i.address-0x18CC0000:#x}: {i.mnemonic} {i.op_str}')
