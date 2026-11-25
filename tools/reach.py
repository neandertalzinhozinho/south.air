import csv, sys
from collections import defaultdict, deque

edges = defaultdict(set)
rev = defaultdict(set)
with open(r'docs\engine\xrefs.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['kind'] != 'call':
            continue
        try:
            a = int(r['func'], 16)
            t = int(r['target'], 16)
        except ValueError:
            continue
        edges[a].add(t)
        rev[t].add(a)

def bfs(start, targets, maxdepth=40):
    q = deque([(start, [start])])
    seen = {start}
    hits = []
    while q:
        n, path = q.popleft()
        if n in targets:
            hits.append(path)
        if len(path) > maxdepth:
            continue
        for m in edges.get(n, ()):
            if m not in seen:
                seen.add(m)
                q.append((m, path + [m]))
    return hits

targets = {0x72480, 0x72A40, 0x73440, 0x1D69E00, 0x877DD0, 0x6F360}
for start in (0x8646A2, 0x861DB0, 0x862E40, 0x8634A0, 0x86A8C0, 0x873440):
    print('=== BFS from 0x%X' % start)
    hits = bfs(start, targets)
    if not hits:
        print('   no target reachable')
    for p in hits:
        print('   ' + ' -> '.join('0x%X' % x for x in p))

# reverse: who calls the FFT fns (all depths up to 3)
for t in sorted(targets):
    print('=== callers of 0x%X' % t)
    # BFS backwards
    q = deque([(t, [t])])
    seen = {t}
    out = []
    while q:
        n, path = q.popleft()
        if len(path) > 4:
            continue
        for m in rev.get(n, ()):
            if m not in seen:
                seen.add(m)
                out.append([m] + path)
                q.append((m, [m] + path))
    for p in out[:20]:
        print('   ' + ' -> '.join('0x%X' % x for x in p))
    print('   total ancestors found:', len(out))
