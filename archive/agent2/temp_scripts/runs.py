import json
import numpy as np
from pathlib import Path

C = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0\captures')

def runs(idx, gap=24):
    out, cur = [], [int(idx[0])]
    for o in idx[1:]:
        o = int(o)
        if o - cur[-1] <= gap: cur.append(o)
        else: out.append((cur[0], cur[-1])); cur = [o]
    out.append((cur[0], cur[-1]))
    return out

for region in ('data', 'data001', 'rdata01'):
    A = [np.fromfile(C / f'A_r{i}_{region}.bin', dtype=np.uint8) for i in (1,2,3)]
    B = [np.fromfile(C / f'B_r{i}_{region}.bin', dtype=np.uint8) for i in (1,2,3)]
    va = ~((A[0]==A[1]) & (A[0]==A[2])); vb = ~((B[0]==B[1]) & (B[0]==B[2]))
    idx = np.flatnonzero((A[0]!=B[0]) & ~(va|vb))
    rs = runs(idx)
    print(f'\n######## {region}: {len(idx)} bytes em {len(rs)} corridas ########')
    for lo, hi in rs:
        s = max(0, (lo & ~0x1F) - 0x20); e = min(len(A[0]), (hi & ~0x1F) + 0x40)
        print(f'\n--- 0x{lo:07X}..0x{hi:07X}  ({hi-lo+1} B) ---')
        for k in range(s, e, 16):
            ma = ''.join('.' if 32 <= c < 127 else f'{c:02x}'[-1] for c in A[0][k:k+16])
            print(f'  A 0x{k:07X} {A[0][k:k+16].tobytes().hex()}  {ma}')
        for k in range(s, e, 16):
            print(f'  B 0x{k:07X} {B[0][k:k+16].tobytes().hex()}')
