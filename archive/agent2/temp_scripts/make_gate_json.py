import json, os, collections
os.chdir(r'D:\PROJETOS\shadowFILES')
rd=lambda p: open(p,'rb').read()
r=[rd(f'analysis/startup_audit/oracleA_create_r{i}_data.bin') for i in (1,2,3)]
c=[rd('analysis/startup_audit/post_create_candidate_data.bin'),
   rd('analysis/startup_audit/post_create_candidate2_data.bin'),
   rd('analysis/startup_audit/post_create_candidate3_data.bin')]
pre=rd('analysis/startup_audit/precreate261_after_inits_data.bin')
o=rd('analysis/startup_audit/original_post_data.bin')
N=len(r[0])
onoise={i for i in range(N) if not(r[0][i]==r[1][i]==r[2][i])}
cnoise={i for i in range(N) if not(c[0][i]==c[1][i]==c[2][i])}
mask=onoise|cnoise
res={i for i in range(N) if c[0][i]!=r[0][i]}-mask
srt=sorted(res); rng=[]; st=pr=srt[0]
for x in srt[1:]:
    if x==pr+1: pr=x
    else: rng.append((st,pr)); st=pr=x
rng.append((st,pr))
J1=(0x530000,0x1000); J2=(0x23CC700-0x217F000,9436)
def cls():
    d=lambda i,cand=False: (c[0][i] if cand else r[0][i])
    return {
      "faltando_candidato_zero": sum(1 for i in res if c[0][i]==0 and r[0][i]!=0),
      "valor_divergente": sum(1 for i in res if c[0][i] and r[0][i]),
      "extra_candidato": sum(1 for i in res if c[0][i] and r[0][i]==0)}
out={
 "data":"2026-11-13T11:05:00Z",
 "objetivo":"piso de create do lado do oraculo (build A) e gate S3 pos-create",
 "oraculo_build":{"arquivo":"analysis/host_reference/startup_capture/original_before_load.vst3",
   "sha256_prefix":"35a685f6","capturas":["oracleA_create_r1","oracleA_create_r2","oracleA_create_r3"],
   "create_status":0,"InitDll":True,"exit_code":-1073740791,"exit_hex":"0xC0000409",
   "nota":"o original tambem falha no teardown neste harness; o 0xC0000409 nao e defeito do candidato"},
 "piso_create_oraculo":{"execucoes":3,"bytes_volateis":len(onoise)},
 "piso_create_candidato":{"execucoes":3,"bytes_volateis":len(cnoise)},
 "mascara":{"uniao":len(mask)},
 "gate":{"candidato":"analysis/startup_audit/final_candidate_init_order.vst3 + init_order_plus_lock.json",
   "referencia":"oracleA_create_r1",
   "distancia_bruta":sum(1 for i in range(N) if c[0][i]!=r[0][i]),
   "fora_da_mascara":len(res),
   "igual_nas_3_execucoes":True,
   "classificacao":cls(),
   "recusados_por_execucao_unica":True},
 "residual":{
   "janela1_0x26AF000":len([i for i in res if J1[0]<=i<J1[0]+J1[1]]),
   "janela2_0x23CC700":len([i for i in res if J2[0]<=i<J2[0]+J2[1]]),
   "faixas_maiores":[{"inicio":hex(s),"fim":hex(e),"bytes":e-s+1} for s,e in sorted(rng,key=lambda t:t[1]-t[0],reverse=True)[:10]],
   "total_faixas":len(rng),
   "exemplos":{hex(i):{"oraculo":r[0][i],"candidato":c[0][i]} for i in (0x48610,0x49b90,0x49b94,0x5301c8)}},
 "achados":{
   "flags_crc":{"offset":"0x5301c8","oraculo":"0x80000009","candidato":"0x80000005"},
   "faltando_ponteiro":{"offset":"0x49b90","oraculo":"08 1c f3 81 01 00 00 00","candidato":"zero",
     "leitura":"valor 0x0000000181f31c08 = base+0x1F31C08, ponteiro determinístico (base fixa); escrita ausente no candidato"},
   "nao_determinismo_candidato":{"campo":"janela2 0x23CC700+8/+0xC/+0x10","oraculo":"1/4/1 nas 3","candidato":"2/5/2 na run1; 1/4/1 nas runs 2 e 3"},
   "extras_95k":{"status":"ARTEFATO DE MEDICAO","explicacao":"2.456 dos 2.481 extras contra uma unica captura do oraculo estao dentro do piso de create do oraculo; com 3 capturas o 'extra' reproduzivel cai a 25 bytes"}},
 "precreate261":{
   "arquivo":"analysis/startup_audit/precreate261_after_inits_data.bin",
   "nao_zero_apos_261_inits":sum(1 for b in pre if b),
   "nao_zero_oraculo":sum(1 for b in r[0] if b),
   "nao_zero_candidato_pos_create":sum(1 for b in c[0] if b),
   "conclusao":"as 261 inits deixam o .data praticamente no nivel do oraculo (+1.403 bytes nao-zero); as ~340k escritas novas sao do createInstance"},
 "veredito":"S3 NAO APROVADO por 3.290 bytes, mas o alvo agora e pequeno e reproduzivel: 3.227 escritas ausentes, 38 valores divergentes, 25 extras; 100 bytes em janela1, 0 em janela2. Numeros anteriores (348.524 / 100.901 / 95.679) ficam REVOGADOS como artefato de piso insuficiente."}
open('analysis/startup_audit/create_gate_13nov.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
print(json.dumps({k:out[k] for k in ('piso_create_oraculo','piso_create_candidato','gate','achados')},ensure_ascii=False,indent=1)[:2200])
