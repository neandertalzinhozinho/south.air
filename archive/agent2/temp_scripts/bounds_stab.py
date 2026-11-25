import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
A = 'analysis/startup_audit/'
rd = lambda p: open(p, 'rb').read()
o = [rd(f'{A}xA_create_r{i}_data.bin') for i in (1, 2, 3)]
c = [rd(f'{A}xC306_create_r{i}_data.bin') for i in (1, 2, 3)]
n = len(o[0])
fo = {i for i in range(n) if not (o[0][i] == o[1][i] == o[2][i])}
fc = {i for i in range(n) if not (c[0][i] == c[1][i] == c[2][i])}
rows = []
for a in c:
    for b in o:
        diff = {i for i in range(n) if a[i] != b[i]}
        rows.append({"upper": len(diff - fo), "lower": len(diff - (fo | fc))})
print('upper across 9 pairs:', sorted({r["upper"] for r in rows}))
print('lower across 9 pairs:', sorted({r["lower"] for r in rows}))
print('oracle floor', len(fo), 'candidate floor', len(fc))
out = {"data": "2026-11-13T17:05:00Z",
       "receita": "306",
       "upper_oracle_floor_only_9_pairs": sorted({r["upper"] for r in rows}),
       "lower_union_9_pairs": sorted({r["lower"] for r in rows}),
       "conclusao": ("limite inferior e estavel nas 9 combinacoes; limite superior NAO e "
                     "estavel -> o superior e diagnostico de instabilidade, nao numero de gate")}
json.dump(out, open(f'{A}xgate_306_bounds_stability.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)[:600])
