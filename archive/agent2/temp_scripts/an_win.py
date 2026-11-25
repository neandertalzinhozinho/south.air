import json, collections
import numpy as np
from pathlib import Path

C = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0\captures')
A = np.fromfile(C / 'A_r1_data.bin', dtype=np.uint8)
B = np.fromfile(C / 'B_r1_data.bin', dtype=np.uint8)

A1 = [np.fromfile(C / f'A_r{i}_data.bin', dtype=np.uint8) for i in (1,2,3)]
B1 = [np.fromfile(C / f'B_r{i}_data.bin', dtype=np.uint8) for i in (1,2,3)]
va = ~((A1[0]==A1[1]) & (A1[0]==A1[2]))
vb = ~((B1[0]==B1[1]) & (B1[0]==B1[2]))
stable = ~(va|vb)
diff = (A!=B) & stable
idx = np.flatnonzero(diff)

def block(o):
    s = o & ~0xF
    return s, A[s:s+16].tobytes().hex(), B[s:s+16].tobytes().hex()

print('=== blocos de 16 B por janela (valores absolutos) ===')
for w in sorted(set(int(i)//65536 for i in idx)):
    offs = idx[idx//65536 == w]
    blks = sorted({int(o) & ~0xF for o in offs})
    print(f'\n--- janela {w} .data+0x{w*65536:06X} | {len(offs)} B em {len(blks)} blocos ---')
    for o in blks[:14]:
        s, ah, bh = block(o)
        a8 = int.from_bytes(A[s:s+8].tobytes(),'little'); b8 = int.from_bytes(B[s:s+8].tobytes(),'little')
        d = b8 - a8
        tag = f' d={d:+#x}' if 0x10000 < a8 and 0x10000 < b8 and abs(d) < 0x1000000 else ''
        print(f'  +0x{s:07X} A={ah} B={bh}{tag}')
    if len(blks) > 14: print(f'  ... +{len(blks)-14} blocos')

# deltas de ponteiro: constantes?
ptrs = []
for o in idx:
    a8 = int.from_bytes(A[o:o+8].tobytes(),'little'); b8 = int.from_bytes(B[o:o+8].tobytes(),'little')
    if a8 > 0x10000 and b8 > 0x10000 and (a8 >> 32) == (b8 >> 32) and abs(a8-b8) < 0x2000000:
        ptrs.append(b8 - a8)
print(f'\n=== {len(ptrs)} offsets com valor tipo-ponteiro; deltas distintos ===')
for d, n in collections.Counter(ptrs).most_common(12):
    print(f'   delta {d:+#x}  x{n}')
