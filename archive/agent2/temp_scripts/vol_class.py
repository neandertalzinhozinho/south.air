import collections
import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
A = 'analysis/startup_audit/'
rd = lambda p: open(p, 'rb').read()
o = [rd(f'{A}xA_create_r{i}_data.bin') for i in (1, 2, 3)]
c = [rd(f'{A}xC273_create_r{i}_data.bin') for i in (1, 2, 3)]
n = len(o[0])
fo = {i for i in range(n) if not (o[0][i] == o[1][i] == o[2][i])}
fc = {i for i in range(n) if not (c[0][i] == c[1][i] == c[2][i])}
only_c = fc - fo
only_o = fo - fc
print('oracle floor', len(fo), 'candidate floor', len(fc), 'only_candidate', len(only_c), 'only_oracle', len(only_o))

# page distribution of candidate-only volatility
pg = collections.Counter(i >> 12 for i in only_c)
print('top pages (candidate-only volatility):')
for k, v in pg.most_common(8):
    print('  RVA', hex(0x217F000 + (k << 12)), 'bytes', v)

# are the varying values pointer-like? read 8 aligned bytes around the first offsets
sample = sorted(only_c)[:12]
for i in sample:
    a = i & ~7
    print('  off', hex(i), 'runs', [c[j][a:a + 8].hex() for j in range(3)], 'oracle', o[0][a:a + 8].hex())

# count how many candidate-only-volatile 8-byte words look like pointers (top bytes 0x0000018x / 0x0000028x)
ptr = 0
tot = 0
seen = set()
for i in only_c:
    a = i & ~7
    if a in seen:
        continue
    seen.add(a)
    tot += 1
    v = int.from_bytes(c[0][a:a + 8], 'little')
    if 0x100000000 <= v < 0x800000000000:
        ptr += 1
print('words touched by candidate-only volatility', tot, 'pointer-like', ptr, '(%.1f%%)' % (100.0 * ptr / max(tot, 1)))

# Same statistic for oracle-only volatility, as control
ptr_o = tot_o = 0
seen = set()
for i in only_o:
    a = i & ~7
    if a in seen:
        continue
    seen.add(a)
    tot_o += 1
    v = int.from_bytes(o[0][a:a + 8], 'little')
    if 0x100000000 <= v < 0x800000000000:
        ptr_o += 1
print('control (oracle-only) words', tot_o, 'pointer-like', ptr_o, '(%.1f%%)' % (100.0 * ptr_o / max(tot_o, 1)))

json.dump({"data": "2026-11-13T16:15:00Z",
           "floors": {"oracle": len(fo), "candidate": len(fc)},
           "candidate_only_volatile": len(only_c),
           "oracle_only_volatile": len(only_o),
           "candidate_only_words": tot, "candidate_only_pointer_like": ptr,
           "oracle_only_words": tot_o, "oracle_only_pointer_like": ptr_o,
           "top_pages": [{"rva": hex(0x217F000 + (k << 12)), "bytes": v} for k, v in pg.most_common(10)]},
          open(f'{A}xgate_volatility_class.json', 'w', encoding='utf-8'), indent=1)
