import json

p = r'D:\PROJETOS\shadowFILES\analysis\stage_reports\VALIDATION_LEDGER.json'
d = json.load(open(p, encoding='utf-8'))
d['s3_gate_bounds_13h15'] = {
    "data": "2026-11-13T16:15:00Z",
    "metodo": ("mesmas 3+3 capturas do gate estendido; divergencia calculada sob duas mascaras: "
               "so piso do oraculo (limite superior) e uniao dos pisos (limite inferior)"),
    "limites": {
        "inferior_divergencia_estavel": 3954,
        "superior_nao_explicado_pelo_ruido_do_oraculo": 215048,
        "por_regiao": {"data": {"bruto": 509352, "superior": 214684, "inferior": 3590},
                       "data001": {"bruto": 375, "superior": 359, "inferior": 359},
                       "rdata01": {"bruto": 5, "superior": 5, "inferior": 5}}
    },
    "achado": {
        "volatilidade_so_candidato": 339655,
        "volatilidade_so_oraculo": 137453,
        "volatilidade_ambos": 178470,
        "ponteiro_like_candidato_pct": 8.6,
        "ponteiro_like_oraculo_pct": 23.6,
        "conclusao": ("o candidato nao e deterministico no ponto de amostragem; a uniao de pisos "
                      "lava essa instabilidade como se fosse ruido")
    },
    "regra": "gate reportado como par 3.954/215.048; aprovacao exige 0 no superior",
    "veredito": "S3 NAO APROVADO",
    "evidencia": ["analysis/startup_audit/xgate_mask_bounds.json",
                  "analysis/startup_audit/xgate_volatility_class.json"]
}
d['atualizado'] = "2026-11-13T16:15:00Z"
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(d), d['s3_gate_bounds_13h15']['limites'])
