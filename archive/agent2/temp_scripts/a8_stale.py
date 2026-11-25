import struct
from pathlib import Path
data=Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
hits=[]
for r in range(0,len(data)-8,8):
    v=struct.unpack_from('<Q',data,r)[0]
    if 0x7FF000000000 <= v < 0x800000000000:
        if (v & 0xFFF)==0xE00 or (v & 0xFFFF)==0xFE00 or (v & 0xFFF)==0xBC:
            hits.append((r,v))
print('candidates:',len(hits))
for r,v in hits[:200]:
    print(f'{r:#x}: {v:#018x}  low12={v&0xfff:#x}')
