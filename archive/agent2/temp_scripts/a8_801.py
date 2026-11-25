import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

data = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
BASE=0x18CC0000
r=0x7b0aa00
print('bytes around 0x7b0aa00:')
for a in range(r-0x80, r+0x80, 16):
    print(f'{a:#x}: {data[a:a+16].hex(" ")}')
print('qwords:')
for a in range(r-0x40, r+0x40, 8):
    print(f'{a:#x}: {struct.unpack_from("<Q",data,a)[0]:#018x}')

# find dword 0x801 / 0x808 anywhere (aligned and unaligned), limited
for val,name in ((0x801,'801'),(0x808,'808')):
    hits=[]
    pat=struct.pack('<I',val)
    start=0
    while True:
        i=data.find(pat,start)
        if i<0: break
        hits.append(i); start=i+1
        if len(hits)>2000: break
    print(f'dword {name}: {len(hits)} hits, first 40:', [hex(x) for x in hits[:40]])
