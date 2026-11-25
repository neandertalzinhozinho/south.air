import json

p = r'D:\PROJETOS\shadowFILES\analysis\stage_reports\VALIDATION_LEDGER.json'
d = json.load(open(p, encoding='utf-8'))
d['s3_extended_gate_12h55'] = {
    "data": "2026-11-13T15:55:00Z",
    "metodo": ("3 capturas do build A e 3 execucoes do candidato (receita 273) no MESMO harness "
               "(analysis/scripts/dump_extended_gate.py): load, inits, InitDll, factory, "
               "createInstance classe 0; piso = bytes que variam entre as 3 do mesmo lado; "
               "mascara = uniao dos dois pisos; residual = divergencia fora da mascara"),
    "superficie": {
        "data": {"rva": "0x217F000", "bytes": 6217208, "floor_oracle": 315923,
                 "floor_candidate": 518125, "residual": 3590,
                 "class": {"ausentes": 3559, "divergentes": 31, "extras": 0}},
        "data001": {"rva": "0x79CD000", "bytes": 10280, "floor_oracle": 16,
                    "floor_candidate": 0, "residual": 359,
                    "class": {"ausentes": 358, "divergentes": 0, "extras": 1}},
        "rdata01": {"rva": "0x79CC000", "bytes": 3072, "floor_oracle": 0,
                    "floor_candidate": 0, "residual": 5,
                    "identified": "AddressOfCallBacks 0x79CC440..444: 0x1879CC158 vs 0x0"},
        "text001": {"rva": "0x79CA000", "bytes": 5120, "residual": 0}
    },
    "total_residual": 3954,
    "estabilidade": "identico nas 9 combinacoes candidato x oraculo",
    "revogacao": {
        "numeros": ["3.290 (gate 08h05)", "3.191 (receita 273, gate 12h40)"],
        "motivo": ("piso depende do harness, nao da imagem: o mesmo build A, mesma receita, deu "
                   "piso 514.595 num harness e 315.923 no outro; comparar capturas de harnesses "
                   "distintos com piso de um deles sub-mascara"),
        "substituto": "3.954 com piso medido no mesmo harness"
    },
    "veredito": "S3 NAO APROVADO em 3.954 bytes",
    "evidencia": "analysis/startup_audit/xgate_12h55.json",
    "artefatos": ["analysis/startup_audit/xA_create_r{1,2,3}_*.bin",
                  "analysis/startup_audit/xC273_create_r{1,2,3}_*.bin"]
}
d['atualizado'] = "2026-11-13T15:55:00Z"
d['proximo_alvo'] = [
    "3.590 bytes em .data (massa em 0x532000-0x538000)",
    "359 bytes em .data001 (PACE/iLok)",
    "5 bytes do campo TLS AddressOfCallBacks",
    "validar entregas Codex S3-MASS e Claude S3-DIFFCHECK",
    "classes 1/2, process (0x325070), createView (0x31e530)"]
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(d), d['s3_extended_gate_12h55']['total_residual'])
