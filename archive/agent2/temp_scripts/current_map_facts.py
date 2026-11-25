import re, pefile, capstone
from pathlib import Path
BASE=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll')
DLL=BASE/'recovered_dsp_test.dll'; MAP=BASE/'recovered_dsp_test.map'
p=pefile.PE(str(DLL))
syms=[]
for l in MAP.read_text(encoding='latin-1').splitlines():
    m=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?',l)
    if m:
        try: syms.append((int(m.group(2),16)-0x180000000,m.group(1)))
        except ValueError: pass
syms.sort()
for r,n in syms:
    if n in ('dump_6f360','dump_715c0','dump_71360','dump_71400','Audio_863170','dump_72180'):
        print(f'{n} @ built RVA 0x{r:x}')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
def dis(rva,n,label):
    o=p.get_offset_from_rva(rva); b=bytes(p.__data__[o:o+n])
    print(f'--- {label} @0x{rva:x} ---')
    for i in md.disasm(b,rva):
        if i.mnemonic in ('call','mov') and ('3' in i.op_str or 'r13' in i.op_str or 'rsp' in i.op_str):
            print(f'0x{i.address:x} {i.bytes.hex():<18} {i.mnemonic:<8} {i.op_str}')
for name in ('dump_6f360','dump_715c0'):
    r=[x for x in syms if x[1]==name]
    if r: dis(r[0][0],0x320,name)
