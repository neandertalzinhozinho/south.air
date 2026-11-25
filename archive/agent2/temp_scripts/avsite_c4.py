import struct
from pathlib import Path
from capstone import *
dll=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll').read_bytes()
dump=Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
pat=bytes.fromhex('f30f6f0af3420f6f54')
def findall(b,p):
    o=[];s=0
    while True:
        i=b.find(p,s)
        if i<0:break
        o.append(i);s=i+1
    return o
print('DLL hits:',[hex(x) for x in findall(dll,pat)])
print('DUMP hits:',[hex(x) for x in findall(dump,pat)])
# map fileoff->RVA for R2TEXT: rva=fileoff+0x1a00 for R2TEXT, text rva=fileoff+0xc00
def off2rva(o):
    if 0x326600<=o<0x326600+0x365c00: return o+0x1a00
    if 0x400<=o<0x400+0x326200: return o+0xc00
    return None
md=Cs(CS_ARCH_X86,CS_MODE_64)
for o in findall(dll,pat):
    r=off2rva(o)
    print('\n--- DLL fileoff 0x%x RVA 0x%s ---'%(o,hex(r) if r else '?'))
    code=dll[o-0x40:o+0x60]
    for ins in md.disasm(code,(r or 0)-0x40):
        print('0x%x  %-24s %s'%(ins.address,ins.bytes.hex(),ins.mnemonic+' '+ins.op_str))
