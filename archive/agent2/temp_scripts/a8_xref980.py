import json,re
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
ROOT=Path(r'D:\PROJETOS\shadowFILES')
data=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
TARGETS={0x1d8d980,0x1d8c3f8,0x1d8d978,0x1d8d988}
hits=[]
for rp in (ROOT/'analysis/recovered_native/units').glob('rva_*/roundtrip.json'):
    j=json.loads(rp.read_text())
    if not j.get('byte_identical'): continue
    s=int(j['start'],16); e=int(j['end_exclusive'],16)
    for i in md.disasm(data[s:e],0x18CC0000+s):
        for op in i.operands:
            if op.type==3 and op.mem.base==41:  # X86_REG_RIP=41
                t=i.address+i.size+op.mem.disp-0x18CC0000
                if t in TARGETS:
                    hits.append((i.address-0x18CC0000,t,i.mnemonic,i.op_str,i.bytes.hex(),rp.parent.name))
print('hits',len(hits))
for h in hits[:100]: print(h)
