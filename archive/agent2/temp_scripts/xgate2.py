import json
import os

os.chdir(r'D:\PROJETOS\shadowFILES')
A = 'analysis/startup_audit/'
d = json.load(open(f'{A}xgate_12h55.json', encoding='utf-8'))

d['data'] = dict(d['data'])
d['data']['note'] = ("mesma receita 273; piso medido no MESMO harness das duas imagens. "
                     "O piso NAO e propriedade da imagem: o build A deu 514.595 com um harness e "
                     "315.923 com outro (mesmo binario, mesma receita) -> piso so vale dentro do harness "
                     "onde foi medido")
d['rdata01']['identified_bytes'] = {
    "offsets": ["0x79cc440", "0x79cc441", "0x79cc442", "0x79cc443", "0x79cc444"],
    "field": "IMAGE_DIRECTORY_ENTRY_TLS.AddressOfCallBacks (RVA 0x79CC440)",
    "oracle": "0x1879cc158", "candidate": "0x0",
    "conclusion": "os 5 bytes residuais de .rdata01 sao exatamente o campo TLS zerado; .text001 = 0"
}
d['data001']['identified'] = ("bloco de estado PACE/iLok; 358 escritas ausentes + 1 extra; "
                              "16 bytes volatilidade do proprio oraculo (ponteiros de processo)")
d['floor_harness_finding'] = {
    "fact": "build A, mesma receita, dois harnesses diferentes: piso de .data 514.595 vs 315.923",
    "implication": "comparar capturas de harnesses distintos com piso de um deles sub-mascara; "
                   "o 3.290 anterior (oracleA vs create_inits_dump_worker) fica REVOGADO como numero de gate",
    "replacement": "3.590 (.data) + 359 (.data001) + 5 (TLS) + 0 (.text001) = 3.954, 9/9 estavel"
}
d['verdict'] = ("S3 NAO APROVADO em 3.954 bytes medidos numa superficie completa e com piso do mesmo harness: "
                "3.590 em .data, 359 em .data001 (PACE/iLok), 5 no campo TLS, 0 em .text001. "
                "O numero 3.191/3.290 fica REVOGADO por piso de harness diferente.")
open(f'{A}xgate_12h55.json', 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
print(json.dumps({k: v for k, v in d.items() if k in ('total', 'verdict')}, ensure_ascii=False, indent=1))
