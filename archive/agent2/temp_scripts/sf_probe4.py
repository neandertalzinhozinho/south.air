import json, re, struct
from pathlib import Path
import pefile
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
print('=== dump around 0x26ae7e0 ===')
r=0x26ae7e0
print('dump bytes', dump[r-0x20:r+0x20].hex(' '))
for off in range(r-0x20,r+0x20,8):
    v=struct.unpack_from('<Q',dump,off)[0]
    print(f'  {off:#x}: {v:#018x}  dword@0={dump[off:off+4].hex()}')
print('\n=== DLL dump_26ae7e0 symbol ===')
dr=syms.get('dump_26ae7e0'); print('dll rva',hex(dr) if dr else None)
if dr:
    print('dll bytes',dllread(dr,0x20).hex(' '))
print('\n=== qword at dump_26ae7e0 and neighbors, with _tls_index write simulated ===')
v=struct.unpack_from('<Q',dump,r)[0]
print(f'orig qword {v:#018x} (low32={v&0xffffffff:#x}, high32={v>>32:#x})')
for tls in (1,2,3,4,5):
    print(f'  after writing tls_index={tls}: {(v & 0xffffffff00000000)|tls:#018x}')
print('\n=== _tls_index symbol in map / PE TLS dir ===')
for n,vv in syms.items():
    if 'tls_index' in n.lower() or n=='_tls_index': print(' ',n,hex(vv))
tls=pe.DIRECTORY_ENTRY_TLS
if tls:
    print('TLS dir AddressOfIndex',hex(tls.struct.AddressOfIndex),'raw',tls.struct.AddressOfIndex-0x180000000 if tls.struct.AddressOfIndex>=0x180000000 else '?')
    print('TLS callbacks',getattr(tls,'struct',None).AddressOfCallBacks)
print('\n=== which dump qwords equal 0x27000000xx / 0x24a00000xx style ===')
for off in range(0,len(dump)-8,8):
    v=struct.unpack_from('<Q',dump,off)[0]
    hi=v>>32
    if hi in (0x27,0x24a) and (v&0xffffffff)<0x1000:
        print(f'  dump@{off:#x} = {v:#018x}')
