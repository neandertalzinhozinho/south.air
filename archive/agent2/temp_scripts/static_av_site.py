import re, pefile, capstone, bisect
from pathlib import Path

DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
MAP = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.map')
p = pefile.PE(str(DLL))
syms=[]
for line in MAP.read_text(encoding='latin-1').splitlines():
    m=re.match(r'\s*\d{4}:([0-9a-fA-F]{8})\s+(\S+)\s+([0-9a-fA-F]+)H?',line)
    if m:
        try:
            rva=int(m.group(3),16)-0x180000000
            syms.append((rva,m.group(2)))
        except ValueError: pass
syms.sort()
starts=[s for s,_ in syms]
def sym(rva):
    i=bisect.bisect_right(starts,rva)-1
    return syms[i][1]+f'+0x{rva-syms[i][0]:x}' if i>=0 else f'?+0x{rva:x}'

def rd(rva,n):
    off=p.get_offset_from_rva(rva)
    return p.__data__[off:off+n]

md=capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail=True

def dis(rva,n,label):
    print(f'=== {label} @ RVA 0x{rva:x} ({sym(rva)}) ===')
    for i in md.disasm(rd(rva,n), rva):
        print(f'  0x{i.address:x}: {i.bytes.hex():<20} {i.mnemonic:<10} {i.op_str}   [{sym(i.address)}]')

dis(0x615600,0x200,'AV vicinity')
# find the AV instruction at 0x6156be
print('\n=== exact AV instruction bytes @0x6156be ===',rd(0x6156be,16).hex())
# find caller dump_6f360-equivalent: look up symbols with 6f360 in name
print('\n=== symbols containing 715c0/6f360 ===')
for rva,n in syms:
    if '715c0' in n or '6f360' in n or '75fc0' in n:
        print(f'  0x{rva:x} {n}')
