import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
A = 'analysis/startup_audit/'
rd = lambda p: open(p, 'rb').read()
regions = [("data", 0x217F000), ("data001", 0x79CD000), ("rdata01", 0x79CC000)]
out = {}
for name, rva in regions:
    o = [rd(f'{A}xA_create_r{i}_{name}.bin') for i in (1, 2, 3)]
    c = [rd(f'{A}xC273_create_r{i}_{name}.bin') for i in (1, 2, 3)]
    n = len(o[0])
    fo = {i for i in range(n) if not (o[0][i] == o[1][i] == o[2][i])}
    fc = {i for i in range(n) if not (c[0][i] == c[1][i] == c[2][i])}
    diff = {i for i in range(n) if c[0][i] != o[0][i]}
    out[name] = {
        "diff_raw": len(diff),
        "residual_oracle_floor_only": len(diff - fo),
        "residual_candidate_floor_only": len(diff - fc),
        "residual_union": len(diff - (fo | fc)),
        "hidden_by_union_vs_oracle_floor": len((diff - fo) - (fo | fc)),
        "volatile_oracle_only": len(fo - fc),
        "volatile_candidate_only": len(fc - fo),
        "volatile_both": len(fo & fc),
    }
print(json.dumps(out, indent=1))
open(f'{A}xgate_mask_bounds.json', 'w', encoding='utf-8').write(json.dumps({
    "data": "2026-11-13T16:10:00Z",
    "objetivo": "medir quanto a uniao de pisos esconde, para nao apresentar um numero sub-mascarado como gate",
    "por_regiao": out,
    "leitura": ("residual_oracle_floor_only e o limite superior (piso mais estreito); "
                "residual_union e o limite inferior; a diferenca e o que a uniao esconde")},
    ensure_ascii=False, indent=1))
