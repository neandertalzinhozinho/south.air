import json,re,struct
from pathlib import Path
ROOT=Path(r'D:\PROJETOS\shadowFILES')
CL=json.loads((ROOT/'analysis/recovered_native/dsp/dependency_build.json').read_text())
dump=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
UNITS=ROOT/'analysis/recovered_native/units'
print('=== short_external_jumps stats ===')
tot=0;units=0;examples=[]
for r in CL:
    s=int(r['start'],16)
    p=UNITS/f'rva_{s:x}'/'roundtrip.json'
    if not p.exists():continue
    j=json.loads(p.read_text())
    sj=j.get('short_external_jumps',[])
    if sj:
        units+=1;tot+=len(sj)
        if len(examples)<20: examples.append((s,sj,j.get('end_exclusive')))
print(' units with unpatched short jumps',units,'total jumps',tot)
for s,sj,e in examples: print(f'   {s:#x} emitted_end={e} jumps={sj}')
print('\n=== check if runtime patches short_external anywhere ===')
src=(ROOT/'analysis/recovered_native/testdll/support_template.c').read_text()
print('  short_external in support_template.c:', 'short_external' in src)
print('\n=== closure end mismatch direction counts ===')
pos=neg=0;posunits=[]
for r in CL:
    if not (r.get('byte_identical') and r.get('status')=='passed'):continue
    s=int(r['start'],16);e=int(r['end'],16)
    p=UNITS/f'rva_{s:x}'/'roundtrip.json'
    if not p.exists():continue
    ee=int(json.loads(p.read_text())['end_exclusive'],16)
    if ee<e: pos+=1;posunits.append((s,e,ee))
    elif ee>e: neg+=1
print(' truncated (emitted<closure end):',pos,' overlong:',neg)
print(' top-10 truncated by phantom size:')
for s,e,ee in sorted(posunits,key=lambda x:x[1]-x[2],reverse=True)[:10]:
    print(f'   {s:#x}: end {e:#x} emitted {ee:#x} missing {e-ee:#x}B')
print('\n=== context of packed (heap_high<<32)|small values ===')
for a in (0x219b71d,0x21bb51d,0x21d8340,0x7b4de60):
    print(f'  around dump@{a:#x}:')
    for off in range(a-0x10,a+0x11,8):
        v=struct.unpack_from('<Q',dump,off)[0]
        print(f'    {off:#x}: {v:#018x}')
print('\n=== dump full 0x71360 (closure end 0x713eb) ===')
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
md=Cs(CS_ARCH_X86,CS_MODE_64)
for i in md.disasm(dump[0x71360:0x713eb],0x180000000+0x71360):
    print(f'  +{i.address-0x180000000-0x71360:03x}: {i.bytes.hex():22s} {i.mnemonic} {i.op_str}')
