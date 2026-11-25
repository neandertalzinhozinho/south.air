import json, os
os.chdir(r'D:\PROJETOS\shadowFILES')
p='analysis/stage_reports/VALIDATION_LEDGER.json'
d=json.load(open(p,encoding='utf-8'))
if 's3_pos_create_13_nov' in d:
    d['s3_pos_create_13_nov']['status']='SUPERSEDIDO em 08h05 - piso do oraculo media mais que a distancia; numeros revogados'
d['s3_gate_08h05_piso_oraculo']={
 "data":"2026-11-13T11:05:00Z",
 "metodo":"build A (original_before_load.vst3) carregado 3x no mesmo ponto: load, InitDll, factory, createInstance classe 0, dump .data 0x217F000+6217208",
 "oraculo":{"created":[0,0,0],"exit":["0xC0000409"]*3,"nao_zero":[1708687,1709006,1710084]},
 "pisos":{"oraculo_3_capturas":514595,"candidato_3_execucoes":388337,"mascara_uniao":651306},
 "gate":{"bruto":387586,"fora_da_mascara":3290,
   "classificacao":{"escritas_ausentes":3227,"valor_divergente":38,"extras":25},
   "janela1":100,"janela2":0,"igual_nas_3":True},
 "lacuna_nominal":["TimestampUtc 0x530D38","\\\\.\\pipe\\ 0x530D98","iLok1 0x530FC8",
   "LicenseDbRemote 0x530FE8","self-pointers 0x1826af180 etc","flags 0x80000009 vs 0x80000005",
   "0x80000008 vs 0x80000004","base+0x1F31C08 ausente em 0x49B90","contadores 30/31 em 0x530000/0x530004"],
 "fato":"os 3.290 bytes estao zerados em precreate261_after_inits_data.bin; sao gravados pelo fluxo de createInstance do original",
 "defeito_proprio":"janela2 +8/+0xC/+0x10 = 2/5/2 na run1 e 1/4/1 nas runs 2-3; oraculo 1/4/1 nas 3",
 "veredito":"S3 NAO APROVADO por 3.290 bytes; alvo pequeno, reproduzivel e atribuido ao fluxo de create. Teardown 0xC0000409 e paridade com o original, nao regressao.",
 "evidencia":"analysis/startup_audit/create_gate_13nov.json"}
d['atualizado']='2026-11-13T11:05:00Z'
d['proximo_alvo']=[
 "explicar os 3.290 bytes: ponto do fluxo de createInstance que o candidato nao executa",
 "classes 1/2 com a receita de 261 inits e process/createView",
 "revisao independente do gate 3.290 (piso 514.595 do oraculo)",
 "builder: regenerar candidato com 261 inits e seed zero, sem sobrescrever"]
open(p,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=1))
print('ok')
