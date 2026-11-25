import hashlib
import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
rd = lambda p: open(p, 'rb').read()

out = {
    "data_utc": "2026-11-13T12:40:00Z",
    "contrato": "S3-TLS-BUILDER-GAP (coordenador)",
    "objetivo": "explicar por que o candidato nao executa a cadeia de inicializadores dinamicos que o build A executa no load",
    "metodo": "comparacao de cabecalho PE (TLS directory) nos dois arquivos + dump em memoria das secoes '001' + gate S3 de 3 execucoes por receita",
    "achados": {}
}
a = out["achados"]

a["tls_directory"] = {
    "rva_diretorio": "0x79cc428",
    "campo_address_of_callbacks_rva": "0x79cc440",
    "original_valor": "0x1879cc158",
    "candidato_valor": "0x0",
    "array_callbacks_rva": "0x79cc158",
    "array_conteudo_ambos": ["0x1879cb190", "0x0"],
    "conclusao": "o builder zerou AddressOfCallBacks; o array e a funcao de callback (__dyn_tls_init, RVA 0x79cb190) estao intactos e identicos nos dois arquivos"
}

a["callback_estatica"] = {
    "rva": "0x79cb190",
    "secao": ".text001",
    "text001_identico_em_disco_nos_dois": True,
    "semantica": "__dyn_tls_init: no PROCESS_ATTACH chama o init do CRT e depois le um bloco de estado global",
    "instrucao_que_desreferencia_o_ponteiro": "0x79cb22a mov rax,[0x79cf610] -> cmp qword [rax],0",
    "valor_0x79cf610_original": "0x181d90040",
    "valor_0x79cf610_candidato": "0x0",
    "efeito_no_candidato": "restaurar so o ponteiro de callbacks produz AV em 0x79cb22a durante LoadLibrary (exit 0xC0000005); experimento candidate_tlscb.vst3"
}

a["secao_data001"] = {
    "rva": "0x79cd000",
    "virtual_size": "0x2828",
    "bytes_nao_zero_em_memoria": {"original": 400, "candidato": 27},
    "bytes_divergentes_primeiros_0x3000": 375,
    "conteudo_original": [
        "C:\\Program Files (x86)\\Common Files\\PACE\\Services\\LicenseServices\\LDSvc.exe",
        "https://activation.paceap.com/InitiateActivation",
        "PACE License Services", "LocalSystem"
    ],
    "conclusao": "bloco de estado PACE/iLok praticamente zerado pelo builder; inclui o ponteiro lido por __dyn_tls_init",
    "fora_do_gate_atual": "o gate S3 cobre .data 0x217F000 + 6.217.208 bytes (ate 0x2757DF8); 0x79CD000 nunca foi medido"
}

# gate com a familia de inicializadores dinamicos ausentes
r = [rd(f'analysis/startup_audit/oracleA_create_r{i}_data.bin') for i in (1, 2, 3)]
c = [rd('analysis/startup_audit/post_create_candidate_data.bin'),
     rd('analysis/startup_audit/post_create_candidate2_data.bin'),
     rd('analysis/startup_audit/post_create_candidate3_data.bin')]
t = [rd('analysis/startup_audit/missing_init_create_data.bin'),
     rd('analysis/startup_audit/missing_init_create2_data.bin'),
     rd('analysis/startup_audit/missing_init_create3_data.bin')]
N = len(r[0])
on = {i for i in range(N) if not (r[0][i] == r[1][i] == r[2][i])}
cn = {i for i in range(N) if not (c[0][i] == c[1][i] == c[2][i])}
tn = {i for i in range(N) if not (t[0][i] == t[1][i] == t[2][i])}
mask = on | cn | tn
res = {i for i in range(N) if t[0][i] != r[0][i]} - mask
a["gate_273_inits"] = {
    "receita": "init_order_plus_missing.json (261 + 0x3104f0 0x310590 0x310d10 0x310e10 0x310ea0 0x310f30 0x311dd0 0x311e50 0x311ec0 0x3127b0 0x312840 0x312c50)",
    "create_status": 0,
    "pisos": {"oraculo": len(on), "candidato_261": len(cn), "candidato_273": len(tn), "uniao": len(mask)},
    "fora_da_mascara": len(res),
    "igual_nas_3_execucoes_x_3_capturas": True,
    "classificacao": {
        "candidato_zero_oraculo_nao": sum(1 for i in res if t[0][i] == 0 and r[0][i]),
        "ambos_nao_zero": sum(1 for i in res if t[0][i] and r[0][i]),
        "extra": sum(1 for i in res if t[0][i] and not r[0][i])
    },
    "janela1": sum(1 for i in res if 0x530000 <= i < 0x531000),
    "janela2": sum(1 for i in res if 0x24d700 <= i < 0x24d700 + 9436),
    "campos_corrigidos": ["0x530188 self-pointer", "0x530D38 TimeStampUtc", "0x530D98 \\\\.\\pipe\\",
                          "0x49B90 base+0x1F31C08"],
    "campos_ainda_errados": ["0x530FC8 iLok1 ausente", "0x530FE8 LicenseDbRemote ausente",
                             "0x530000/0x530004 18/0 vs 30/31", "0x5301C8 0x80000005 vs 0x80000009",
                             "0x5305D0 0x80000004 vs 0x80000008"],
    "veredito": "a familia de inicializadores dinamicos explica ~99 bytes (3.290 -> 3.191); NAO e a causa do grosso dos 3.290"
}

a["paridade_teardown"] = {
    "fato": "o build A tambem termina em 0xC0000409 neste harness (3/3 capturas)",
    "implicacao": "s4_lifecycle_audit.json atribui o fail-fast ao candidato sem controle do original; a atribuicao vale como 'ponto no modulo', nao como regressao"
}

a["proximo_alvo"] = {
    "massa_restante": "3.151 escritas ausentes fora da janela1, 0 na janela2, concentradas em 0x532000-0x538000 (paginas 0x537/0x534/0x533/0x535/0x536)",
    "hipoteses": ["tabela/hash construida no create (0x532000-0x538000)",
                  "estado PACE/iLok que o original carrega no load e o candidato nao (blind spot do gate)"],
    "nao_aprovado": True
}

a["experimentos_registrados"] = [
    {"arquivo": "analysis/startup_audit/candidate_tlscb.vst3", "mudanca": "AddressOfCallBacks restaurado",
     "resultado": "AV 0xC0000005 em LoadLibrary", "conclusao": "sozinho nao basta"},
    {"arquivo": "analysis/startup_audit/candidate_tlscb_state.vst3", "mudanca": "callbacks + .data001 original (imagem descriptografada)",
     "resultado": "AV 0xC0000005 em LoadLibrary", "conclusao": "o caminho TLS exige mais estado PACE; nao perseguido agora"},
    {"arquivo": "analysis/startup_audit/missing_init_create{,2,3}_data.bin", "mudanca": "12 inicializadores dinamicos reais acrescentados",
     "resultado": "create 0, gate 3.191", "conclusao": "explica 99 bytes"}
]

out["veredito"] = ("DUAS causas estruturais demonstradas por byte (TLS AddressOfCallBacks zerado; .data001 PACE zerado, fora da area do gate) "
                   "e uma familia de inicializadores dinamicos que explica 99 dos 3.290 bytes. Nenhuma delas, isolada, fecha o gate. "
                   "S3 continua NAO APROVADO com 3.191 bytes (receita de 273) como novo piso de trabalho.")
out["nao_heuristico"] = "todos os valores acima sao medidos; nenhuma escrita forcada, nenhuma mascara ampliada alem da uniao dos tres pisos de 3 execucoes"

json.dump(out, open('analysis/startup_audit/s3_tls_builder_gap.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', len(json.dumps(out)), 'bytes; gate', len(res), 'floors', len(on), len(cn), len(tn))
