import json, re, struct, bisect
from pathlib import Path
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM
ROOT=Path(r'D:\PROJETOS\shadowFILES')
dump=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
pe=pefile.PE(str(ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
MAPP=ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map'
syms={}
for line in MAPP.read_text(encoding='latin-1').splitlines():
    mm=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?',line)
    if mm:
        v=int(mm.group(2),16)
        if 0x180000000<=v<0x190000000: syms[mm.group(1)]=v-0x180000000
def dllread(rva,n):
    for s in pe.sections:
        if s.VirtualAddress<=rva<s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            o=s.PointerToRawData+(rva-s.VirtualAddress);return pe.__data__[o:o+n]

print('=== DLL qwords pointing at 0x61d8b0 / 0x24140b / dump_715c0 etc ===')
targets={0x61d8b0:'dump_24140b+0x1b (fault)',0x61d895:'dump_24140b',0x61565f:'dump_715c0',
         0x61563f:'dump_71360',0x6156be:'dump_715c0+0x5f'}
for s in pe.sections:
    if s.SizeOfRawData==0: continue
    data=pe.__data__[s.PointerToRawData:s.PointerToRawData+s.SizeOfRawData]
    for off in range(0,len(data)-8,8):
        v=struct.unpack_from('<Q',data,off)[0]
        for tv,desc in targets.items():
            if v==0x180000000+tv or v==tv:
                print(f'  {s.Name.decode().rstrip()} fo:{off:#x} rva:{s.VirtualAddress+off:#x} = {v:#x} -> {desc}')

print('\n=== branch targets in DLL code hitting fault addresses ===')
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
for s in pe.sections:
    if not (s.Characteristics & 0x20000000): continue
    code=pe.__data__[s.PointerToRawData:s.PointerToRawData+s.SizeOfRawData]
    base=0x180000000+s.VirtualAddress
    hits=[]
    for i in md.disasm(code,base):
        if i.mnemonic in ('call','jmp','je','jne','jz','jnz','ja','jb','jg','jl','jbe','jae','js','jns') and i.operands:
            op=i.operands[0]
            if op.type==X86_OP_IMM and op.imm in (0x180000000+t for t in targets):
                hits.append((hex(i.address-0x180000000),i.mnemonic,hex(op.imm-0x180000000)))
    for h in hits[:30]: print('  ',h)
    print('  total hits in',s.Name.decode().rstrip(),len(hits))

print('\n=== global unit placement audit: first 8 bytes dump vs DLL ===')
CL=json.loads((ROOT/'analysis/recovered_native/dsp/dependency_build.json').read_text())
UNITS=ROOT/'analysis/recovered_native/units'
bad=[];ok=0;skip=0
for r in CL:
    if not (r.get('byte_identical') and r.get('status')=='passed'): continue
    s=int(r['start'],16)
    nm=f'dump_{s:x}'
    if nm not in syms: skip+=1;continue
    dr=syms[nm]
    try: lb=dllread(dr,8); db=dump[s:s+8]
    except KeyError: skip+=1;continue
    if lb==db: ok+=1
    else: bad.append((s,dr,db.hex(),lb.hex()))
print(f'  ok={ok} bad={len(bad)} skip={skip}')
for b in bad[:40]: print(f'    {b[0]:#x} dll@{b[1]:#x} dump={b[2]} dll={b[3]}')

print('\n=== neighbor continuity of truncated units ===')
ss=sorted(syms.items(),key=lambda kv:kv[1])
for t in (0x71360,0x715c0,0x24140b):
    idx=[i for i,(n,r) in enumerate(ss) if n==f'dump_{t:x}'][0]
    print(f'  {t:#x}:')
    for n,r in ss[max(0,idx-2):idx+3]:
        print(f'    {n:28s} @{r:#x}')
