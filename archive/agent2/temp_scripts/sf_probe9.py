import json,struct,re
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
ROOT=Path(r'D:\PROJETOS\shadowFILES')
pe=__import__('pefile').PE(str(ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
data=pe.__data__;IB=0x180000000
def dllread(rva,n):
    for s in pe.sections:
        if s.VirtualAddress<=rva<s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            o=s.PointerToRawData+(rva-s.VirtualAddress);return pe.__data__[o:o+n]
print('=== disasm around wrong short-jump target 0x61d8d4 ===')
b=dllread(0x61d8b5,0x40)
md=Cs(CS_ARCH_X86,CS_MODE_64)
for i in md.disasm(b,IB+0x61d8b5):
    print(f'  {i.address-IB:#x}: {i.bytes.hex():18s} {i.mnemonic} {i.op_str}')
    if i.address-IB>0x61d8e5: break
print('\n=== brute-force branch scan for target 0x61d8b0 ===')
T=IB+0x61d8b0
hits=[]
for s in pe.sections:
    if not (s.Characteristics & 0x20000000):continue
    buf=data[s.PointerToRawData:s.PointerToRawData+s.SizeOfRawData]
    base=IB+s.VirtualAddress
    n=len(buf)
    for p in range(n-6):
        b0=buf[p]
        if b0 in (0x75,0x74,0xeb,0x7c,0x7d,0x7e,0x7f,0x72,0x73,0x76,0x77,0x78,0x79,0x7a,0x7b):
            t=base+p+2+((buf[p+1]^0x80)-0x80)
            if t==T: hits.append((s.Name.decode().rstrip(),base+p-IB,'rel8',buf[p:p+2].hex()))
        if b0 in (0xe8,0xe9) or (b0==0x0f and 0x80<=buf[p+1]<=0x8f):
            k=p+1 if b0 in (0xe8,0xe9) else p+2
            if k+4>n:continue
            disp=struct.unpack_from('<i',buf,k)[0]
            t=base+k+4+disp
            if t==T: hits.append((s.Name.decode().rstrip(),base+p-IB,'rel32',buf[p:k+4].hex()))
print(' hits',len(hits))
for h in hits[:40]:print('  ',h)
print('\n=== closure record for 0x24144a / 0x24142b / is dump_24144a linked? ===')
CL=json.loads((ROOT/'analysis/recovered_native/dsp/dependency_build.json').read_text())
for r in CL:
    if int(r['start'],16) in (0x24144a,0x24142b,0x24144f):
        print('  ',json.dumps(r))
# map presence
mp=ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map'
print('  dump_24144a in map:', ' dump_24144a ' in (' '+mp.read_text(encoding='latin-1')+' '))
