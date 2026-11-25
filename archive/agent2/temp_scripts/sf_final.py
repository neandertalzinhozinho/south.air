import re,json,struct
from pathlib import Path
import pefile
ROOT=Path(r'D:\PROJETOS\shadowFILES')
pe=pefile.PE(str(ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
mp=ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map'
syms={}
for line in mp.read_text(encoding='latin-1').splitlines():
    mm=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?',line)
    if mm:
        v=int(mm.group(2),16)
        if 0x180000000<=v<0x190000000:syms.setdefault(mm.group(1),v-0x180000000)
def rd(rva,n):
    for s in pe.sections:
        if s.VirtualAddress<=rva<s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            o=s.PointerToRawData+(rva-s.VirtualAddress);return pe.__data__[o:o+n]
dump=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
print('CURRENT DLL bytes',pe.__data__[:2].hex(), 'size',len(pe.__data__))
print('=== verify key structural facts on CURRENT build ===')
for name,rva,n in [('dump_71360',0x71360,0x20),('dump_24140b',0x24140b,0x20),('dump_715c0',0x715c0,0x200)]:
    d=syms[name]; b=rd(d,n)
    eq=sum(1 for i in range(n) if b[i]==dump[rva+i])
    print(f' {name}: DLL RVA {d:#x}, first {n:#x}B equal-to-dump {eq}/{n}, last4={b[-4:].hex()}')
print(' 71360 next symbol delta:', syms['dump_715c0']-syms['dump_71360'])
# short jump raw check in current DLL
d=syms['dump_24140b'];b=rd(d,0x20)
print(' 24140b short jcc bytes at +0x1d:',b[0x1d:0x1f].hex(),'-> target',hex(d+0x1f+0x1f))
print(' dump_24144a DLL RVA:',hex(syms.get('dump_24144a',0)))
print('\n=== 0x71360 full function has rets? ===')
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
md=Cs(CS_ARCH_X86,CS_MODE_64)
rets=[i.address-(0x180000000+0x71360) for i in md.disasm(dump[0x71360:0x713eb],0) if i.mnemonic=='ret']
print(' ret offsets in dump 0x71360..0x713eb:',[hex(x) for x in rets],'all beyond emitted 0x20?',all(x>=0x20 for x in rets))
