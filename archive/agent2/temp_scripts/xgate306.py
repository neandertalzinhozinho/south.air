import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
A = 'analysis/startup_audit/'
rd = lambda p: open(p, 'rb').read()
regions = [("data", 0x217F000), ("data001", 0x79CD000), ("rdata01", 0x79CC000), ("text001", 0x79CA000)]
out = {}
lo = up = 0
for name, rva in regions:
    o = [rd(f'{A}xA_create_r{i}_{name}.bin') for i in (1, 2, 3)]
    c = [rd(f'{A}xC306_create_r{i}_{name}.bin') for i in (1, 2, 3)]
    n = len(o[0])
    fo = {i for i in range(n) if not (o[0][i] == o[1][i] == o[2][i])}
    fc = {i for i in range(n) if not (c[0][i] == c[1][i] == c[2][i])}
    diff = {i for i in range(n) if c[0][i] != o[0][i]}
    low = diff - (fo | fc)
    upp = diff - fo
    cross = sorted({len({i for i in range(n) if a[i] != b[i]} - (fo | fc)) for a in c for b in o})
    out[name] = {"rva": hex(rva), "diff_raw": len(diff), "floor_oracle": len(fo),
                 "floor_candidate": len(fc), "lower_union": len(low), "upper_oracle_floor": len(upp),
                 "class": {"cand_zero": sum(1 for i in low if c[0][i] == 0 and o[0][i]),
                           "both": sum(1 for i in low if c[0][i] and o[0][i]),
                           "extra": sum(1 for i in low if c[0][i] and not o[0][i])},
                 "cross_check_lower": cross}
    lo += len(low)
    up += len(upp)
doc = {"data": "2026-11-13T16:35:00Z",
       "receita": "init_order_plus_tables.json (306 = 261 + 12 dinamicos + 33 da auditoria S3-MASS)",
       "create_status": [0, 0, 0],
       "por_regiao": out,
       "total": {"lower_union": lo, "upper_oracle_floor": up},
       "comparacao": {"receita_273": {"lower": 3954, "upper": 215048},
                      "receita_306": {"lower": lo, "upper": up}},
       "veredito": "S3 NAO APROVADO" if up else "S3 APROVADO"}
json.dump(doc, open(f'{A}xgate_306.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({"data": {k: v for k, v in out['data'].items() if k != 'class'},
                  "data001": out['data001'], "rdata01": out['rdata01'], "text001": out['text001'],
                  "total": doc['total']}, indent=1))
