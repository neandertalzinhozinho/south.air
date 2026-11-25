import json, os
os.chdir(r'D:\PROJETOS\shadowFILES')
p='analysis/stage_reports/VALIDATION_LEDGER.json'
d=json.load(open(p,encoding='utf-8'))
d['atualizado']='2026-11-13T10:32:00Z'
d['proximo_alvo']=[
 "medir piso de create do lado do oraculo (segunda captura do build A no mesmo ponto)",
 "explicar as 95.679 escritas extras em 0x530000-0x593FFF (pares (41,40)x64 e (47,46)x64)",
 "estender a receita de 261 inits as classes 1 e 2 e diagnosticar o teardown 0xC0000409",
 "exercitar IAudioProcessor::process e IEditController::createView no candidato"]
d['s3_pos_create_13_nov']={
 "data": "2026-11-13T10:30:00Z",
 "receita": {
   "binario": "analysis/startup_audit/final_candidate_init_order.vst3",
   "inits": "analysis/startup_audit/init_order_plus_lock.json",
   "contagem": 261,
   "composicao": "259 do boot + 0x30d310 (mode=4) + 0xc76730 (lock 0x2757DE8)",
   "create_classe_0": "status 0, objeto nao-nulo, 0 erros de init, 3/3 execucoes",
   "teardown": "0xC0000409 nas 3 execucoes, depois do dump"},
 "medicao": {
   "oraculo": "analysis/startup_audit/original_post_data.bin (build A)",
   "execucoes": ["post_create_candidate_data.bin","post_create_candidate2_data.bin","post_create_candidate3_data.bin"],
   "bruto": [351404,345926,348047],
   "fora_piso_sem_volatilidade": [348524,343408,345551],
   "volatilidade_entre_execucoes": 388337,
   "divergencia_reproduzivel": 100901,
   "escritas_extras": 95679,
   "escritas_ausentes": 5035,
   "valor_divergente": 187,
   "janela1": {"bruto": [338,304,300], "estaveis": 106},
   "janela2": {"bruto": [9332,9345,9340], "estaveis": 0, "nao_zero": [9347,9353,9339], "oraculo_nao_zero": 9346},
   "concentracao_extras": "0x530000-0x593FFF",
   "pares_valor": "((41,40) x64, (47,46) x64)"},
 "veredito": "S3 NAO APROVADO. Numero de execucao unica (348.524) e majoritariamente volatil e esta proibido como gate. Falta piso de create do lado do oraculo e explicacao das 95.679 escritas extras. S4 segue parcial: create classe 0 ok, teardown falha, classes 1/2 e process/createView nao testados.",
 "evidencia": "analysis/startup_audit/post_create_stability.json"}
open(p,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=1))
print('ok', len(json.dumps(d)))
