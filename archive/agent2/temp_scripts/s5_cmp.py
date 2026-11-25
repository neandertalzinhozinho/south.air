import json, math
from pathlib import Path

F1 = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase1')
TABLE = Path(r'D:\PROJETOS\shadowFILES\analysis\parameter_table.json')


def load(p):
    ev = [json.loads(l) for l in open(p, encoding='utf-8') if l.startswith('{')]
    ps = [e for e in ev if e['event'] == 'parameter']
    meta = {e['event']: e for e in ev if e['event'] != 'parameter'}
    return ps, meta


c, cm = load(F1 / 's5_params_wrapperstub.jsonl')
o, om = load(F1 / 's5_params_oracle.jsonl')
print('candidate', len(c), 'oracle', len(o))

FIELDS = ['id', 'title', 'shortTitle', 'units', 'stepCount', 'defaultNormalizedValue',
          'unitId', 'flags', 'status']
diffs = []
for i, (a, b) in enumerate(zip(c, o)):
    for f in FIELDS:
        if a[f] != b[f]:
            diffs.append((i, a['title'], f, a[f], b[f]))
    for pa, pb in zip(a['plain_probes'], b['plain_probes']):
        for f in ('plain', 'roundtrip'):
            if pa[f] != pb[f]:
                diffs.append((i, a['title'], f't({pa["t"]}).{f}', pa[f], pb[f]))
print('field diffs:', len(diffs))
for d in diffs[:20]:
    print('  ', d)

# cross-check against the 143-record descriptor table
tab = json.loads(TABLE.read_text(encoding='utf-8'))
tparam = tab['parameters']
print('\ntable records', len(tparam), '| runtime', len(c))
titles_t = [p['name'] for p in tparam]
titles_r = [p['title'] for p in c]
print('runtime titles == table names?', titles_r[:143] == titles_t)
extra = [t for t in titles_r if t not in titles_t]
print('runtime-only titles:', extra)
print('table-only titles:', [t for t in titles_t if t not in titles_r])

# where does the extra slot sit, and is the rest offset by one?
if extra:
    idx = titles_r.index(extra[0])
    print('extra at runtime index', idx)
    print('  context:', titles_r[max(0, idx - 2):idx + 3])
    before = titles_r[:idx]
    after = titles_r[idx + 1:]
    print('  prefix matches table:', before == titles_t[:len(before)])
    print('  suffix matches table:', after == titles_t[len(before):])

# bounds from the table vs plain mapping observed
print('\n--- plain(t) vs table [min,max] for the first 8 params ---')
for i in range(8):
    p = c[i]
    t = tparam[i] if i < len(tparam) and tparam[i]['name'] == p['title'] else None
    lo = t['minimum'] if t else None
    hi = t['maximum'] if t else None
    obs = [pr['plain'] for pr in p['plain_probes']]
    print(f'{i:3d} {p["title"]:16s} min={lo} max={hi} plain={obs}')

# how many params agree with a linear (min,max) mapping derived from plain(0)/plain(1)
agree = disagree = nonlin = 0
bad = []
by_title = {p['name']: p for p in tparam}
for p in c:
    t = by_title.get(p['title'])
    if not t:
        continue
    lo, hi = t['minimum'], t['maximum']
    obs = [pr['plain'] for pr in p['plain_probes']]
    pred = [lo + pr['t'] * (hi - lo) for pr in p['plain_probes']]
    if all(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9) for a, b in zip(obs, pred)):
        agree += 1
    else:
        nonlin += 1
        bad.append((p['title'], lo, hi, obs))
print(f'\nlinear (min,max) agreement: {agree} | non-linear: {nonlin}')
for b in bad[:12]:
    print('  ', b)
