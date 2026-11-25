import json, hashlib, os, collections
from pathlib import Path

ROOT = Path(r'D:\PROJETOS\shadowFILES')
F0 = ROOT / 'analysis/stage_reports/fase0'
J = F0 / 's3_captures_v2.json'
d = json.loads(J.read_text(encoding='utf-8'))

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

print('report =', d.get('report'))
print('chaves  =', list(d))
inputs = d['inputs']
print('\n-- inputs (%d) --' % len(inputs))
for i in inputs:
    real = sha(i['path']) if os.path.exists(i['path']) else 'AUSENTE'
    print('  %-8s %s' % ('OK' if real == i['sha256'] else 'DIVERGE', Path(i['path']).name))
    if real != i['sha256']:
        print('     declared', i['sha256'])
        print('     real    ', real)

caps = d['captures']
print('\n-- captures: %d --' % len(caps))
bad = 0
for c in caps:
    if not os.path.exists(c['path']):
        print('  AUSENTE', c['path']); bad += 1; continue
    b = Path(c['path']).stat().st_size
    if b != c['bytes'] or sha(c['path']) != c['sha256']:
        print('  DIVERGE', c['path'], b, c['bytes']); bad += 1
print('  divergencias:', bad)
print('  por prefixo:', collections.Counter(c['prefix'] for c in caps))

print('\n-- floors --')
for side, regs in d['floors'].items():
    print(' ', side, {k: v['varying_offsets'] for k, v in regs.items()})

pairs = d['pairs']
print('\n-- pairs: %d --' % len(pairs))
byreg = collections.defaultdict(list)
for p in pairs:
    s = sum(cl['bytes'] for cl in p['clusters'])
    ok = (s == p['diff_bytes'])
    if p['region'] == 'data':
        print('  %s x %s  stable=%-8d diff=%-7d sum(clusters)=%-7d %s' %
              (p['a'], p['b'], p['stable_offsets'], p['diff_bytes'], s, 'ok' if ok else 'ERRO'))
    if not ok: print('    SOMA NAO FECHA', p['region'], p['a'], p['b'])
    byreg[p['region']].append(p['diff_bytes'])

print('\n-- totals --')
print(json.dumps(d.get('totals', {}), indent=1)[:800])
print('\ndiff_bytes por regiao (min/med/max):')
for r, v in byreg.items():
    print('  %-9s %d pares  min=%d max=%d  distintos=%s' % (r, len(v), min(v), max(v), sorted(set(v))))
