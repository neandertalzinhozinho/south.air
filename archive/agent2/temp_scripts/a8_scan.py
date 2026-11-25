import struct
from pathlib import Path

data = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
BASE = 0x18CC0000

def q(rva):
    return struct.unpack_from('<Q', data, rva)[0]

print('=== IAT-ish slots near 0x1d8d700 ===')
for r in range(0x1d8d700, 0x1d8d810, 8):
    v = q(r)
    if v:
        print(f'{r:#x}: {v:#018x}')
print('=== 0x1d8c000..0x1d8c200 nonzero ===')
for r in range(0x1d8c000, 0x1d8c200, 8):
    v = q(r)
    if v:
        print(f'{r:#x}: {v:#018x}')

print('=== qword == 0x801 / 0x808 occurrences (first 80) ===')
c1 = c2 = 0
for r in range(0, len(data)-8, 8):
    v = struct.unpack_from('<Q', data, r)[0]
    if v == 0x801:
        c1 += 1
        if c1 <= 40: print(f'0x801 @ {r:#x}')
    elif v == 0x808:
        c2 += 1
        if c2 <= 40: print(f'0x808 @ {r:#x}')
print(f'total aligned qwords: 0x801={c1} 0x808={c2}')
