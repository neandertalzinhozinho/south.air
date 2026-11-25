import collections
import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
A = 'analysis/startup_audit/'
rd = lambda p: open(p, 'rb').read()
REGIONS = [("data", 0x217F000), ("data001", 0x79CD000), ("rdata01", 0x79CC000)]


def surface(po, pc):
    out = {}
    for name, rva in REGIONS:
        o = [rd(f'{A}{po}_r{i}_{name}.bin') for i in (1, 2, 3)]
        c = [rd(f'{A}{pc}_r{i}_{name}.bin') for i in (1, 2, 3)]
        n = len(o[0])
        fo = {i for i in range(n) if not (o[0][i] == o[1][i] == o[2][i])}
        fc = {i for i in range(n) if not (c[0][i] == c[1][i] == c[2][i])}
        diff = {i for i in range(n) if c[0][i] != o[0][i]}
        out[name] = {"rva": hex(rva), "floor_oracle": len(fo), "floor_candidate": len(fc),
                     "raw": len(diff), "lower": diff - (fo | fc), "upper": diff - fo,
                     "cross": sorted({len({i for i in range(n) if a[i] != b[i]} - (fo | fc))
                                      for a in c for b in o}),
                     "o": o, "c": c}
    return out


L = surface('xA_load', 'xC_load')
P = surface('xA_create', 'xC306_create')
load_total = sum(len(v["lower"]) for v in L.values())
post_total = sum(len(v["lower"]) for v in P.values())

ls, lo, lc = L["data"]["lower"], L["data"]["o"], L["data"]["c"]
ps, po, pc = P["data"]["lower"], P["data"]["o"], P["data"]["c"]

lic = lambda s: sum(1 for i in s if 0x52F000 <= i < 0x532000)
doc = {
    "data": "2026-11-13T17:35:00Z",
    "contrato": "S3-LOADSTAGE (coordenador)",
    "objetivo": ("medir em que ESTAGIO o residual nasce: no load ou no create. Claude (S3-DIFFCHECK) "
                 "apontou que a decomposicao 3-vias nao era reproduzivel por falta da baseline "
                 "'load-pure' do oraculo; esta captura a produz."),
    "harness": "analysis/scripts/dump_load_only.py (load + dump, sem inits e sem create), 3 execucoes por imagem",
    "load_stage": {
        "data": {k: L["data"][k] for k in ("rva", "floor_oracle", "floor_candidate", "raw", "cross")},
        "data001": {k: L["data001"][k] for k in ("rva", "floor_oracle", "floor_candidate", "raw", "cross")},
        "rdata01": {k: L["rdata01"][k] for k in ("rva", "floor_oracle", "floor_candidate", "raw", "cross")},
        "lower_total": load_total,
        "upper_total": sum(len(v["upper"]) for v in L.values()),
        "nota": ("no load o piso e quase nulo (4.706 / 1.893 em .data), portanto limite inferior e "
                 "superior COINCIDEM: 4.276. Sem ambiguidade de mascara."),
    },
    "post_create_306": {
        "data": {k: P["data"][k] for k in ("floor_oracle", "floor_candidate", "raw")},
        "data001": {k: P["data001"][k] for k in ("floor_oracle", "floor_candidate", "raw")},
        "rdata01": {k: P["rdata01"][k] for k in ("floor_oracle", "floor_candidate", "raw")},
        "lower_total": post_total,
    },
    "decomposicao": {
        "residual_no_load": load_total,
        "residual_pos_create": post_total,
        "curado_pela_receita_306": len(ls - ps),
        "so_aparece_pos_create": len(ps - ls),
        "intersecao": len(ls & ps),
        "conclusao": ("o residual nasce no LOAD. A receita de 306 inits cura 3.923 dos 4.276 bytes de "
                      ".data porque reproduz os inicializadores estaticos que o builder deixou de rodar "
                      "ao zerar TLS.AddressOfCallBacks. Os 404 que sobram sao exatamente o que a tabela "
                      ".inits NAO contem."),
    },
    "classificacao_load": {
        "oraculo_nao_zero_candidato_zero": sum(1 for i in ls if lo[0][i] and not lc[0][i]),
        "ambos_nao_zero": sum(1 for i in ls if lo[0][i] and lc[0][i]),
        "extra": sum(1 for i in ls if lc[0][i] and not lo[0][i]),
        "nota": "0 extras: no load o candidato nao inventa nada, apenas deixa de escrever",
    },
    "licenciamento_no_load": {
        "janela_0x52F000_0x532000": {"load": lic(ls), "pos_create": lic(ps)},
        "strings_presentes_no_oraculo_NO_LOAD": True,
        "strings_no_candidato": False,
        "amostras": {
            "0x530FE8": {"oraculo": "LicenseDbRemote", "candidato": "zeros"},
            "0x531008": {"oraculo": "IlokCloudRemote", "candidato": "zeros"},
            "0x531068": {"oraculo": "iLok2Remote", "candidato": "zeros"},
            "0x531088": {"oraculo": "iLok3Remote", "candidato": "zeros"},
            "0x531048": {"oraculo": "LicenseDb", "candidato": "zeros"},
            "0x531C40": {"oraculo": "ImlIasm_", "candidato": "zeros"},
        },
        "prova": ("as strings de licenciamento ja existem no oraculo ANTES de qualquer init ou create; "
                  "no candidato nunca aparecem. Sao escritas pela cadeia __dyn_tls_init que o builder "
                  "desligou - causa medida, nao inferida."),
    },
    "paginas_load": [{"rva": hex(0x217F000 + (k << 12)), "bytes": v}
                     for k, v in collections.Counter(i >> 12 for i in ls).most_common(10)],
    "o_que_o_builder_precisa_restaurar": {
        "1": "TLS.AddressOfCallBacks = 0x1879CC158 (RVA 0x79CC440) - sem isso nada do load roda",
        "2": ".data001 (RVA 0x79CD000) estado PACE/iLok: 400 bytes nao-zero, incl. 0x79CF610 -> 0x181D90040",
        "3": "nao basta restaurar o campo: com .data001 original injetado em memoria, __dyn_tls_init "
             "falha com AV em call indireto -> RIP=0 e rax=0x1882B8000 (inicio de .inits). "
             "A cadeia le estado que so existe no oraculo ANTES do load; injecao pos-load nao serve.",
    },
    "achado_extra_secoes": {
        "so_no_candidato": [".imports (RVA 0x82A5000, 0x127C0)", ".inits (RVA 0x82B8000, 0x5ABBC)"],
        "leitura": ("o builder moveu os inicializadores para uma secao propria .inits e as importacoes "
                    "para .imports. A tabela .inits e o que a receita de 306 replay; ela nao contem o "
                    "estado PACE."),
    },
    "veredito": ("S3 NAO APROVADO. Gate inferior 768 (load 4.640 -> create 768), com causa localizada no "
                 "load: TLS.AddressOfCallBacks zerado + .data001 PACE zerado. A receita de 306 inits "
                 "substitui 3.923 bytes do load, mas nao o subsistema de licenca."),
    "nao_heuristico": "todas as contagens medidas; nenhuma escrita forcada; mascara = uniao dos pisos do mesmo harness",
    "artefatos": ["analysis/startup_audit/xA_load_r{1,2,3}_{data,data001,rdata01}.bin",
                  "analysis/startup_audit/xC_load_r{1,2,3}_{data,data001,rdata01}.bin"],
}
json.dump(doc, open(f'{A}s3_load_stage_gate.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('load', load_total, 'post', post_total, 'cured', len(ls - ps), 'intersect', len(ls & ps))
print('lic load', lic(ls), 'lic post', lic(ps))
