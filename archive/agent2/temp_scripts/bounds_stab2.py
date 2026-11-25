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
stats = {
    "floor_oracle": len(fo),
    "floor_candidate": len(fc),
    "volatile_both": len(fo & fc),
    "volatile_oracle_only": len(fo - fc),
    "volatile_candidate_only": len(fc - fo),
    "non_zero_oracle": sum(1 for b in o[0] if b),
    "non_zero_candidate": sum(1 for b in c[0] if b),
}
doc = json.load(open(f'{A}xgate_306_bounds_stability.json', encoding='utf-8'))
doc['volatilidade_306'] = stats
doc['regra_revisada'] = {
    "gate": 768,
    "composicao": {"data": 404, "data001": 359, "rdata01": 5, "text001": 0},
    "por_que": ("o limite inferior e o unico estavel nas 9 combinacoes (404); o superior varia "
                "{8927, 131411, 212374} e por isso e diagnostico, nao gate"),
    "defeito_separado": ("determinismo do candidato: %d bytes variam so no candidato contra %d do "
                         "oraculo; precisa de gate proprio (S3-D), nao de mascaramento no S3"
                         % (stats['volatile_candidate_only'], stats['floor_oracle']))
}
json.dump(doc, open(f'{A}xgate_306_bounds_stability.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(doc['volatilidade_306'], indent=1))
print(doc['regra_revisada']['defeito_separado'])
