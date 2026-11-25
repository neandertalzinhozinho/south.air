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
    up = len(diff - fo)
    lo = len(diff - (fo | fc))
    out[name] = {
        "diff_raw": len(diff),
        "upper_bound_oracle_floor_only": up,
        "lower_bound_union_floors": lo,
        "hidden_by_union": up - lo,
        "floor_oracle": len(fo), "floor_candidate": len(fc),
        "volatile_both": len(fo & fc),
        "volatile_oracle_only": len(fo - fc),
        "volatile_candidate_only": len(fc - fo),
    }
doc = {
    "data": "2026-11-13T16:15:00Z",
    "objetivo": ("medir quanto a uniao de pisos esconde, porque um numero sub-mascarado nao pode ser "
                 "apresentado como gate"),
    "por_regiao": out,
    "limite_inferior_total": sum(v["lower_bound_union_floors"] for v in out.values()),
    "limite_superior_total": sum(v["upper_bound_oracle_floor_only"] for v in out.values()),
    "achado": ("339.655 bytes de .data sao volateis SO no candidato (o oraculo e deterministico ali). "
               "Nao sao ruido de endereco: apenas 8,6% das palavras tocadas sao ponteiro-like, contra 23,6% "
               "no controle (volatilidade so do oraculo). O padrao tipico e `cd ab cd ab` (fill de debug "
               "heap) numa execucao e um valor pseudo-aleatorio na outra."),
    "consequencia": ("o candidato NAO e deterministico no ponto de amostragem: 518.125 bytes variam entre "
                     "execucoes identicas contra 315.923 do oraculo. Antes de contar bytes de gate, isso "
                     "precisa ser explicado - ou o gate nao tem significado."),
    "regra_resultante": ("reportar os dois limites: 3.954 (divergencia estavel, limite inferior) e "
                         "218.048 (divergencia nao explicada pelo ruido do oraculo, limite superior). "
                         "Aprovacao exige limite superior = 0."),
    "artefatos": ["xA_create_r{1,2,3}_*.bin", "xC273_create_r{1,2,3}_*.bin", "xgate_volatility_class.json"]
}
json.dump(doc, open(f'{A}xgate_mask_bounds.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, dict) else v) for k, v in out.items()}, indent=1))
print('lower', doc['limite_inferior_total'], 'upper', doc['limite_superior_total'])
