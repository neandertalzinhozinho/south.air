import json, collections
from pathlib import Path

C = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0\captures')
REG = {'data': '_data.bin', 'data001': '_data001.bin', 'rdata01': '_rdata01.bin', 'text001': '_text001.bin'}

def caps(side, region):
    return [(C / f'{side}_r{i}{REG[region]}').read_bytes() for i in (1, 2, 3)]

def volatile(bufs):
    n = len(bufs[0])
    return {i for i in range(n) if not (bufs[0][i] == bufs[1][i] == bufs[2][i])}

def strings(buf, base, minlen=6):
    out, cur, start = [], bytearray(), 0
    for i, c in enumerate(buf):
        if 32 <= c < 127:
            if not cur: start = i
            cur.append(c)
        else:
            if len(cur) >= minlen: out.append((base + start, bytes(cur).decode('ascii')))
            cur = bytearray()
    if len(cur) >= minlen: out.append((base + start, bytes(cur).decode('ascii')))
    return out

report = {}

for region, suf in REG.items():
    A = caps('A', region); B = caps('B', region)
    va, vb = volatile(A), volatile(B)
    stable = [i for i in range(len(A[0])) if i not in va and i not in vb]
    diff = [i for i in stable if A[0][i] != B[0][i]]
    raw = [i for i in range(len(A[0])) if A[0][i] != B[0][i]]
    print(f'\n===== {region} =====')
    print(f'  volateis A={len(va)}  B={len(vb)}  |  stable={len(stable)}')
    print(f'  diff bruto={len(raw)}  diff estavel={len(diff)}')

    # janelas
    win = collections.Counter(i // 65536 for i in diff)
    report[region] = {'volatile_A': len(va), 'volatile_B': len(vb), 'stable': len(stable),
                      'diff_raw': len(raw), 'diff_stable': len(diff), 'windows': {}}

    for w, cnt in sorted(win.items()):
        offs = [i for i in diff if i // 65536 == w]
        # contexto: que tipo de dado e' isso
        kind = collections.Counter()
        for o in offs:
            a4 = A[0][o:o+4].ljust(4, b'\0')
            b4 = B[0][o:o+4].ljust(4, b'\0')
            av = int.from_bytes(A[0][o:o+8].ljust(8, b'\0'), 'little')
            bv = int.from_bytes(B[0][o:o+8].ljust(8, b'\0'), 'little')
            if av > 0x10000 and bv > 0x10000 and abs(av - bv) > 0x1000:
                kind['ptr_delta'] += 1
            elif A[0][o] != B[0][o] and abs(A[0][o] - B[0][o]) == 4:
                kind['lowbyte+/-4'] += 1
            elif av < 0x100 and bv < 0x100:
                kind['small_int'] += 1
            else:
                kind['other'] += 1
        report[region]['windows'][w] = {'diff': cnt, 'first': min(offs), 'last': max(offs),
                                        'kinds': dict(kind)}

    # strings na faixa com diff
    if diff:
        lo, hi = min(diff) & ~0xFFFF, (max(diff) & ~0xFFFF) + 0x10000
        sa = [s for s in strings(A[0][lo:hi], lo) if any(lo <= o < hi for o, _ in [s])]
        sb = set(s for _, s in strings(B[0][lo:hi], lo))
        only_a = [s for o, s in strings(A[0][lo:hi], lo) if s not in sb]
        only_b = [s for o, s in strings(B[0][lo:hi], lo) if s not in {x for _, x in strings(A[0][lo:hi], lo)}]
        if only_a or only_b:
            print(f'  strings exclusivas A ({len(only_a)}): {only_a[:6]}')
            print(f'  strings exclusivas B ({len(only_b)}): {only_b[:6]}')

    for w, cnt in sorted(win.items())[:20]:
        offs = [i for i in diff if i // 65536 == w]
        r = report[region]['windows'][w]
        print(f'  janela {w:3d} .+0x{w*65536:07X}  {cnt:5d} B  [{r["kinds"]}]')
        for o in offs[:3]:
            print(f'      +0x{o:07X}  A={A[0][o:o+8].hex()}  B={B[0][o:o+8].hex()}')

Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\f0_classified.json').write_text(
    json.dumps(report, indent=1), encoding='utf-8')
print('\nok -> f0_classified.json')
