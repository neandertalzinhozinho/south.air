import json, collections
import numpy as np
from pathlib import Path

C = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0\captures')
REG = {'data': '_data.bin', 'data001': '_data001.bin', 'rdata01': '_rdata01.bin', 'text001': '_text001.bin'}

def arr(side, region, i):
    return np.fromfile(C / f'{side}_r{i}{REG[region]}', dtype=np.uint8)

def strings_np(b, base, minlen=6):
    printable = (b >= 32) & (b < 127)
    out = []
    n = len(b)
    i = 0
    # find runs
    d = np.diff(np.concatenate(([0], printable.view(np.int8), [0])))
    starts = np.flatnonzero(d == 1)
    ends = np.flatnonzero(d == -1)
    for s, e in zip(starts, ends):
        if e - s >= minlen:
            out.append((base + int(s), bytes(b[s:e]).decode('ascii')))
    return out

report = {}
for region in REG:
    A = [arr('A', region, i) for i in (1, 2, 3)]
    B = [arr('B', region, i) for i in (1, 2, 3)]
    va = ~((A[0] == A[1]) & (A[0] == A[2]))
    vb = ~((B[0] == B[1]) & (B[0] == B[2]))
    stable = ~(va | vb)
    diff = (A[0] != B[0]) & stable
    raw = (A[0] != B[0])
    idx = np.flatnonzero(diff)
    print(f'\n===== {region} =====')
    print(f'  volateis A={int(va.sum())}  B={int(vb.sum())}  stable={int(stable.sum())}')
    print(f'  diff bruto={int(raw.sum())}  diff estavel={int(diff.sum())}')

    rec = {'volatile_A': int(va.sum()), 'volatile_B': int(vb.sum()), 'stable': int(stable.sum()),
           'diff_raw': int(raw.sum()), 'diff_stable': int(diff.sum()), 'windows': {}}
    if len(idx) == 0:
        report[region] = rec
        continue

    wins = np.unique(idx // 65536)
    for w in wins:
        offs = idx[idx // 65536 == w]
        kinds = collections.Counter()
        for o in offs[:20000]:
            a8 = int.from_bytes(A[0][o:o+8].tobytes(), 'little')
            b8 = int.from_bytes(B[0][o:o+8].tobytes(), 'little')
            if a8 > 0x10000 and b8 > 0x10000 and abs(a8 - b8) > 0x1000:
                kinds['ptr_delta'] += 1
            elif abs(int(A[0][o]) - int(B[0][o])) == 4:
                kinds['lowbyte_d4'] += 1
            elif a8 < 0x100 and b8 < 0x100:
                kinds['small_int'] += 1
            else:
                kinds['other'] += 1
        rec['windows'][int(w)] = {'diff': int(len(offs)), 'first': int(offs[0]),
                                  'last': int(offs[-1]), 'kinds': dict(kinds)}

    lo = (int(idx[0]) // 65536) * 65536
    hi = (int(idx[-1]) // 65536 + 1) * 65536
    sa = strings_np(A[0][lo:hi], lo); sb = strings_np(B[0][lo:hi], lo)
    seta = {s for _, s in sa}; setb = {s for _, s in sb}
    only_a = [(o, s) for o, s in sa if s not in setb]
    only_b = [(o, s) for o, s in sb if s not in seta]
    rec['strings_only_A'] = only_a[:40]; rec['strings_only_B'] = only_b[:40]
    print(f'  strings no miolo do diff: A={len(sa)} B={len(sb)} | exclusivas A={len(only_a)} B={len(only_b)}')
    for o, s in only_a[:6]: print(f'    A-only +0x{o:07X} {s!r}')
    for o, s in only_b[:6]: print(f'    B-only +0x{o:07X} {s!r}')

    for w in wins:
        r = rec['windows'][int(w)]
        print(f'  janela {int(w):3d} .+0x{int(w)*65536:07X} {r["diff"]:5d} B {r["kinds"]}')
    for o in idx[:6]:
        print(f'      +0x{int(o):07X}  A={A[0][o:o+8].tobytes().hex()}  B={B[0][o:o+8].tobytes().hex()}')
    report[region] = rec

Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\f0_classified.json').write_text(
    json.dumps(report, indent=1), encoding='utf-8')
print('\nok')
