import json

p = r'D:\PROJETOS\shadowFILES\analysis\stage_reports\VALIDATION_LEDGER.json'
d = json.load(open(p, encoding='utf-8'))
d['s3_gate_306_13h35'] = {
    "data": "2026-11-13T16:35:00Z",
    "receita": "init_order_plus_tables.json: 261 + 12 dinamicos + 33 de s3_residual_mass_audit = 306",
    "create_status": [0, 0, 0],
    "mesmo_harness": "analysis/scripts/dump_extended_gate.py (3 capturas build A, 3 execucoes candidato)",
    "resultado": {
        "data": {"diff_raw": 297501, "floor_oracle": 315923, "floor_candidate": 400601,
                 "lower_union": 404, "upper_oracle_floor": 8927,
                 "class": {"candidato_zero": 368, "ambos_nao_zero": 36, "extra": 0}},
        "data001": {"lower_union": 359, "upper_oracle_floor": 359},
        "rdata01": {"lower_union": 5, "upper_oracle_floor": 5,
                    "identified": "AddressOfCallBacks 0x79CC440"},
        "text001": {"lower_union": 0},
        "total": {"lower_union": 768, "upper_oracle_floor": 9291}
    },
    "comparacao": {"273": {"lower": 3954, "upper": 215048},
                   "306": {"lower": 768, "upper": 9291}},
    "validacao_da_entrega": {"unattributed_no_S3_MASS": 238,
                             "coincidencia_com_residual_medido": 238,
                             "veredito": "atribuicao fiel byte a byte"},
    "residual_restante": ("strings de licenciamento/PACE (LicenseDbRemote, IlokCloudRemote, "
                          "iLok2Remote, iLok3Remote, LicenseDb, ImlIasm_) + estado .data001 + campo TLS"),
    "veredito": "S3 NAO APROVADO (768 / 9.291)",
    "evidencia": "analysis/startup_audit/xgate_306.json"
}
d['atualizado'] = "2026-11-13T16:35:00Z"
d['proximo_alvo'] = [
    "404 bytes em .data: 238 ja nomeados pelo S3-MASS + 166 fora do relatorio (paginas 0x26B0000, 0x2753000, 0x26AE000)",
    "359 bytes em .data001 (PACE/iLok) e 5 bytes do campo TLS: regeneracao do builder",
    "8.927 bytes de nao determinismo residual do candidato (limite superior)",
    "classes 1/2, process (0x325070), createView (0x31e530), setComponentState"]
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(d), d['s3_gate_306_13h35']['resultado']['total'])
