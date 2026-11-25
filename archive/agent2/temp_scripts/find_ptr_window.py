from pathlib import Path
import struct
p = Path(r'D:\PROJETOS\shadowFILES\analysis\startup_audit\fl_seq\oracleA_51_44100_512_setup_data.bin')
d = p.read_bytes()
best = []
for base in range(0, len(d) - 0x1000, 0x1000):
    n = 0
    for off in range(base, base + 0x1000 - 7, 8):
        v = struct.unpack_from('<Q', d, off)[0]
        if 0x180000000 <= v < 0x182800000:
            n += 1
    best.append((n, base))
best.sort(reverse=True)
for n, b in best[:10]:
    print(hex(b), n)
