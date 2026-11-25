import json

p = r'D:\PROJETOS\shadowFILES\analysis\stage_reports\VALIDATION_LEDGER.json'
d = json.load(open(p, encoding='utf-8'))

d['s3_load_stage_17h35'] = {
    "data": "2026-11-13T17:35:00Z",
    "metodo": ("captura load-only (LoadLibrary + dump, sem inits e sem create) 3x por imagem, "
               "harness analysis/scripts/dump_load_only.py; comparacao contra xA_create/xC306_create"),
    "load_stage": {
        "data": {"floor_oracle": 4706, "floor_candidate": 1893, "residual_lower": 4276,
                 "residual_upper": 4276, "cross_9": [4276]},
        "data001": {"residual": 359}, "rdata01": {"residual": 5},
        "total_lower": 4640, "total_upper": 4640,
        "classificacao": {"oraculo_nz_candidato_zero": 4260, "ambos_nz": 16, "extra": 0}
    },
    "decomposicao": {
        "residual_no_load": 4640, "residual_pos_create": 768,
        "curado_pela_receita_306": 3923, "intersecao": 353, "so_pos_create": 51
    },
    "prova_subsistema_licenca": {
        "janela_0x52F000_0x532000": {"load": 1265, "pos_create": 182},
        "strings_presentes_no_oraculo_no_load": ["LicenseDbRemote", "IlokCloudRemote", "iLok2Remote",
                                                 "iLok3Remote", "LicenseDb", "ImlIasm_"],
        "strings_no_candidato": False
    },
    "controle_negativo": {
        "experimento": "chamar __dyn_tls_init(base,1,0) manualmente pos-load",
        "candidato": {"resultado": "AV, RIP=0, rax=0x1882B8000"},
        "oraculo": {"resultado": "AV, RIP RVA 0x179790B, rax=0x181D9000B, retorno 0x79CB245"},
        "conclusao": ("o callback nao e reentrante em NENHUMA das duas imagens; o experimento de "
                      "injecao esta INVALIDADO como evidencia de estado ausente no candidato"),
        "artefatos": ["analysis/scripts/probe_tls_chain_fault.py", "tls_chain_slots.json"]
    },
    "secoes_exclusivas_do_candidato": {
        ".imports": "RVA 0x82A5000, 0x127C0",
        ".inits": "RVA 0x82B8000, 0x5ABBC",
        "leitura": "o builder moveu a tabela de inicializadores para .inits; ela nao contem o estado PACE"
    },
    "entrega_claude": {
        "arquivo": "analysis/startup_audit/post_create_stability_review.json",
        "validacao": ("reproduziu 514.595 / 388.337 / 394.635 / 651.306 / 659.329 / 3.290 / 3.191 "
                      "EXATAMENTE com codigo proprio"),
        "rejeicoes_dele": ["3.290/3.191 como gate de igualdade global",
                           "as decomposicoes 3-vias 3.227/38/25 e 3.151/39/1 (baseline load-pure "
                           "do oraculo ausente) - agora suprida por esta medicao",
                           "a mascara acumulativa de 3 pisos"],
        "recomendacoes": ["cobrir todas as secoes gravaveis (.data001 e TLS)", 
                          "normalizar ponteiros em vez de mascarar por posicao",
                          "piso de >=20 execucoes", "reportar distancia simetrica"],
        "aceito_como": "revisao independente valida; nao e aprovacao"
    },
    "entrega_codex_s3_lastmile": {
        "status": "BLOCKED",
        "motivo": "limite de 5h esgotado nos dois terminais Codex (term_c14e8180, term_14fe0190)",
        "parcial_observado_no_terminal": ("67/41 e 66/40 sao IDs de facets de std::locale via MSVCP140; "
                                          "ha padding de pilha nas tabelas e fragmentos de ponteiros de heap"),
        "acao": "sem retry cego; reenviar quando a janela reabrir"
    },
    "veredito": "S3 NAO APROVADO: 768 pos-create / 4.640 no load, causa no load (TLS + .data001 PACE)",
    "evidencia": "analysis/startup_audit/s3_load_stage_gate.json"
}
d['atualizado'] = "2026-11-13T17:35:00Z"
d['proximo_alvo'] = [
    "builder: novo artefato com AddressOfCallBacks restaurado, para o loader executar a cadeia naturalmente",
    "404 restantes: 182 na janela de licenca + 222 fora (paginas 0x26B0000/0x2753000/0x26AE000)",
    "S3-D: determinismo do candidato (219.131 bytes volateis so nele)",
    "frente independente: exercitar classes 1/2, process (0x325070), createView (0x31e530)"]
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('blocks', len(d), '| load', d['s3_load_stage_17h35']['load_stage']['total_lower'])
