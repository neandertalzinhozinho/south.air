import json, os, collections
os.chdir(r'D:\PROJETOS\shadowFILES')
files = {
 'run1': 'analysis/startup_audit/post_create_candidate_data.bin',
 'run2': 'analysis/startup_audit/post_create_candidate2_data.bin',
 'run3': 'analysis/startup_audit/post_create_candidate3_data.bin'}
r = {k: open(v,'rb').read() for k,v in files.items()}
o = open('analysis/startup_audit/original_post_data.bin','rb').read()
fb = set(json.load(open('analysis/startup_audit/noise_floor_original.json'))['volatile_offsets'])
fc = set(json.load(open('analysis/startup_audit/noise_floor_candidate.json'))['volatile_offsets'])
N = len(o)
xs = list(r.values())
noise = {i for i in range(N) if not (xs[0][i]==xs[1][i]==xs[2][i])}
mask = fb | fc | noise
J2 = (0x23CC700-0x217F000, 9436); J1 = (0x26AF000-0x217F000, 4096)
mask_sem_noise = fb | fc
def regs(x):
    d = {i for i in range(N) if x[i]!=o[i]}
    def c(a,n): return len([i for i in d if a<=i<a+n])
    return {"bruto": len(d),
            "fora_piso_sem_volatilidade": len(d-mask_sem_noise),
            "fora_piso_e_volatilidade": len(d-mask),
            "janela2": c(*J2), "janela1": c(*J1),
            "resto": len([i for i in d if not (J2[0]<=i<J2[0]+J2[1] or J1[0]<=i<J1[0]+J1[1])])}
S = {i for i in range(N) if xs[0][i]!=o[i]} - mask
blocks = collections.Counter(i>>16 for i in S)
out = {
 "data": "captura .data a partir de RVA 0x217F000, 6.217.208 bytes; offsets do arquivo = RVA - 0x217F000",
 "oraculo": "analysis/startup_audit/original_post_data.bin",
 "execucoes": {k: {"arquivo": v, "nao_zero": sum(1 for b in r[k] if b)} for k,v in files.items()},
 "pisos_usados": {"original_buildB": len(fb), "candidato_load": len(fc)},
 "volatilidade_create": {
   "uniao_3_execucoes": len(noise),
   "nota": "bytes que diferem entre execucoes identicas do candidato (mesmo binario, mesma lista de 261 inits, mesmo ponto de captura)"},
 "resultado_por_execucao": {k: regs(v) for k,v in r.items()},
 "divergencia_estavel": {
   "bytes": len(S),
   "igual_nas_3_execucoes": True,
   "candidato_zero_oraculo_nao_zero": sum(1 for i in S if xs[0][i]==0 and o[i]!=0),
   "ambos_nao_zero": sum(1 for i in S if xs[0][i] and o[i]),
   "candidato_nao_zero_oraculo_zero": sum(1 for i in S if xs[0][i] and o[i]==0),
   "janela1": len([i for i in S if J1[0]<=i<J1[0]+J1[1]]),
   "janela2": len([i for i in S if J2[0]<=i<J2[0]+J2[1]]),
   "blocos_64k_maiores": {hex(b<<16): c for b,c in blocks.most_common(8)},
   "pares_de_valor_frequentes": [[list(k), v] for k,v in
       collections.Counter((xs[0][i], o[i]) for i in S if xs[0][i] and o[i]).most_common(4)]},
 "create_classe_0": {
   "receita": ["analysis/startup_audit/final_candidate_init_order.vst3",
               "analysis/startup_audit/init_order_plus_lock.json"],
   "inits": 261, "erros_init": 0, "status_retornado": 0, "repeticoes": "3/3",
   "teardown": {"exit_code": -1073740791, "hex": "0xC0000409",
                "observacao": "falha depois do dump, no descarregamento/destruicao; todas as 3 execucoes"}},
 "veredito": "S3 NAO APROVADO. A distancia pos-create de execucao unica (348.524 fora de piso B+candidato) e majoritariamente volatil: 388.337 bytes variam entre execucoes identicas. Divergencia reproduzivel = 100.901 bytes, dos quais 95.679 sao escrita extra do candidato (oraculo zero) concentrada em 0x530000-0x593FFF e 5.035 sao escrita ausente. S4 segue parcial: create classe 0 retorna 0, mas o teardown falha 0xC0000409 e classes 1/2 nao foram testadas."
}
p='analysis/startup_audit/post_create_stability.json'
open(p,'w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
print(json.dumps(out,ensure_ascii=False,indent=1)[:2500])
