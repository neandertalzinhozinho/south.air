import json,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
ROOT=Path(r'D:\PROJETOS\shadowFILES')
data=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
PATCHED_EXPLICIT={0x1d8d720,0x1d8d730,0x1d8d740,0x1d8d750,0x1d8d7f0,0x1d8d808,0x1d8d8c8,0x1d8c3a0}
PATH_UNITS={'rva_8637d0','rva_238800','rva_27990d','rva_279db4','rva_277c00','rva_1ccd6e0','rva_8e00','rva_2798b8'}
found={}
for rp in (ROOT/'analysis/recovered_native/units').glob('rva_*/roundtrip.json'):
    j=json.loads(rp.read_text())
    if not j.get('byte_identical'): continue
    s=int(j['start'],16); e=int(j['end_exclusive'],16)
    if rp.parent.name not in PATH_UNITS: continue
    for i in md.disasm(data[s:e],0x18CC0000+s):
        if i.mnemonic not in ('call','jmp'): continue
        for op in i.operands:
            if op.type==3 and op.mem.base==41 and op.size==8:
                t=i.address+i.size+op.mem.disp-0x18CC0000
                v=struct.unpack_from('<Q',data,t)[0] if t+8<=len(data) else 0
                patched = (0x1d8c000<=t<0x1d8d000) or t in PATCHED_EXPLICIT
                found.setdefault((t,v,patched),[]).append((i.address-0x18CC0000,rp.parent.name,i.mnemonic))
for (t,v,p),sites in sorted(found.items()):
    flag='PATCHED ' if p else '*** STALE?'
    print(f'{flag} slot {t:#x} = {v:#018x}')
    for a,u,m in sites[:8]: print(f'    {a:#x} ({u}) {m}')
