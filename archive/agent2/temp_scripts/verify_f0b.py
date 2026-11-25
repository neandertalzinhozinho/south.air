import json, collections
from pathlib import Path

F0 = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0')
d = json.loads((F0 / 's3_captures_v2.json').read_text(encoding='utf-8'))

print('report =', d['report'], '| pares =', len(d['pairs']))
bad = [p for p in d['pairs'] if sum(c['diff_bytes'] for c in p['clusters']) != p['diff_bytes']]
print('pares com soma de clusters diferente:', len(bad))
overlap = 0
for p in d['pairs']:
    ws = [c['window'] for c in p['clusters']]
    if len(ws) != len(set(ws)):
        overlap += 1
print('pares com janela repetida:', overlap)

by = collections.defaultdict(lambda: collections.defaultdict(list))
for p in d['pairs']:
    by[p['region']][(p['a'], p['b'])].append(p['diff_bytes'])

print('\n== diff_bytes por regiao (9 pares) ==')
for reg, pairs in by.items():
    vals = [v[0] for k, v in pairs.items()]
    print('  %-9s min=%-8d max=%-8d distintos=%s' % (reg, min(vals), max(vals), sorted(set(vals))))

ref = next(p for p in d['pairs'] if p['a'] == 'A_r1' and p['b'] == 'B_r1' and p['region'] == 'data')
print('\n== A_r1 x B_r1 / data: %d bytes em %d janelas ==' % (ref['diff_bytes'], len(ref['clusters'])))
for c in ref['clusters']:
    off = c['window'] * 65536
    in_lic = 0x530000 <= off < 0x540000
    print('  janela %3d  .data+0x%06X  %5d B  (1o 0x%X, ult 0x%X)%s' %
          (c['window'], off, c['diff_bytes'], c['first_offset'], c['last_offset'], '   <-- janela de licenca' if in_lic else ''))

print('\n== A_r1 x B_r1 por regiao ==')
for reg in ('data', 'data001', 'rdata01', 'text001'):
    p = next(x for x in d['pairs'] if x['a'] == 'A_r1' and x['b'] == 'B_r1' and x['region'] == reg)
    print('  %-9s stable=%-9d diff=%-6d janelas=%d' % (reg, p['stable_offsets'], p['diff_bytes'], len(p['clusters'])))

print('\n== amostras de bytes (3 primeiras janelas de data) ==')
for c in ref['clusters'][:3]:
    print('  0x%X: A=%s' % (c['first_offset'], c['a_first_16_bytes']))
    print('           B=%s' % (c['b_first_16_bytes']))
