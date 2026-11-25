import json, re
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
ROOT=Path(r'D:\PROJETOS\shadowFILES')
MAPP=ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map'
pe=__import__('pefile').PE(str(ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
def dllread(rva,n):
    for s in pe.sections:
        if s.VirtualAddress<=rva<s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            o=s.PointerToRawData+(rva-s.VirtualAddress);return pe.__data__[o:o+n]
rows=[]
for line in MAPP.read_text(encoding='latin-1').splitlines():
    mm=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?',line)
    if mm:
        v=int(mm.group(2),16)
        if 0x18061d800<=v<=0x18061da00: rows.append((v,mm.group(1)))
print('=== map symbols 0x61d800..0x61da00 ===')
for v,n in sorted(rows): print(f'  {v-0x180000000:#x} {n}')
print('\n=== DLL bytes / disasm at dump_24140b (0x61d895) ===')
b=dllread(0x61d895,0x40)
print('  ',b.hex(' '))
md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
for i in md.disasm(b[:0x20],0x18061d895):
    print(f'  {i.address-0x180000000:#x}: {i.bytes.hex():20s} {i.mnemonic} {i.op_str}')
print('\n=== disassemble starting at fault 0x61d8b0 ===')
for i in md.disasm(b[0x1b:0x2b],0x18061d8b0):
    print(f'  {i.address-0x180000000:#x}: {i.bytes.hex():20s} {i.mnemonic} {i.op_str}')
print('\n=== roundtrip for 24144a / 24144f if present ===')
for rva in (0x24144a,0x24144f,0x24142b):
    p=ROOT/'analysis/recovered_native/units'/f'rva_{rva:x}'/'roundtrip.json'
    print(f'  {rva:#x}: dir={p.parent.exists()} rt={p.exists()}')
    if p.exists():
        j=json.loads(p.read_text());print('   ',j.get('start'),j.get('end_exclusive'),j.get('instruction_count'),j.get('short_external_jumps'),j.get('external_targets'))
