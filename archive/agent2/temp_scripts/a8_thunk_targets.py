import struct
from pathlib import Path
data=Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
print('thunk slots:')
for a in range(0x1c9ad37,0x1c9ad85,6):
    b=data[a:a+6]
    if b[:2]!=b'\xff\x25': break
    d=struct.unpack_from('<i',b,2)[0]
    t=a+6+d
    v=struct.unpack_from('<Q',data,t)[0]
    print(f'{a:#x}: jmp [rip+{d:#x}] -> slot {t:#x} = {v:#018x}')
print('0x1d8d818 =',hex(struct.unpack_from('<Q',data,0x1d8d818)[0]))
