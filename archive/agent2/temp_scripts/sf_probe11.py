import re,json,bisect
from pathlib import Path
ROOT=Path(r'D:\PROJETOS\shadowFILES')
MAPP=ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map'
syms={}
for line in MAPP.read_text(encoding='latin-1').splitlines():
    mm=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?',line)
    if mm:
        v=int(mm.group(2),16)
        if 0x180000000<=v<0x190000000:syms[mm.group(1)]=v-0x180000000
ss=sorted((r,n) for n,r in syms.items() if n.startswith('dump_') or n.startswith('Audio_'))
st=[r for r,n in ss]
def at(rva):
    i=bisect.bisect_right(st,rva)-1
    return f'{ss[i][1]}+0x{rva-ss[i][0]:x}' if i>=0 and rva>=ss[i][0] else '?'
print('=== phantom span consequences for the 3 AV units ===')
for name,s,e,ee in [('dump_71360',0x71360,0x713eb,0x71380),
                    ('dump_715c0',0x715c0,0x71864,0x717c0),
                    ('dump_24140b',0x24140b,0x2414b0,0x24142b)]:
    a=syms[name]
    print(f'\n {name}: sym DLL RVA={a:#x}, emitted {s:#x}..{ee:#x}, closure span to {e:#x}')
    for t in (ee, (ee+e)//2, e-1):
        dst=a+(t-s)
        print(f'   t={t:#x} -> r2_lookup_addr = {dst:#x} = {at(dst)}')
print('\n=== 0x71360 fall-through proof ===')
a=syms['dump_71360'];b=syms['dump_715c0']
print(f'  dump_71360 @{a:#x} + emitted 0x20 = {a+0x20:#x}; dump_715c0 @{b:#x} -> equal? {a+0x20==b}')
print('\n=== dump_6f360 call sites to dump_71360 / dump_715c0 ===')
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
pe=__import__('pefile').PE(str(ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
for s in pe.sections:
    if s.Name.decode().rstrip()!='.text':continue
    buf=pe.__data__[s.PointerToRawData:s.PointerToRawData+s.SizeOfRawData]
    base=0x180000000+s.VirtualAddress
    md=Cs(CS_ARCH_X86,CS_MODE_64)
    a6=syms['dump_6f360']
    for i in md.disasm(buf[a6-s.VirtualAddress:a6-s.VirtualAddress+0x300],0x180000000+a6):
        if i.mnemonic=='call' and i.op_str.startswith('0x'):
            t=int(i.op_str,16)-0x180000000
            if t in (syms['dump_71360'],syms['dump_715c0'],syms['dump_71400'],syms['dump_72180']):
                print(f'   +{i.address-0x180000000-a6:03x}: call {t:#x}  {[n for n,r in syms.items() if r==t][:1]}')
