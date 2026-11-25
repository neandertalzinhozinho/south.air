import json

p = r'D:\PROJETOS\shadowFILES\analysis\startup_audit\s3_load_stage_gate.json'
d = json.load(open(p, encoding='utf-8'))

d['correcao_data001_17h55'] = {
    "data": "2026-11-13T17:55:00Z",
    "afirmacao_revogada": ("'o builder zerou .data001: original 400 bytes nao-zero, candidato 27' "
                           "(ROADMAP bloco 12h40, s3_tls_builder_gap.json)"),
    "medicao_que_a_refuta": {
        "metodo": "leitura do cabecalho PE + bytes crus da secao .data001 em DISCO nos dois arquivos",
        "oracle": {"virtual_size": "0x2828", "raw_size": "0x200", "nao_zero_no_arquivo": 27},
        "candidato": {"virtual_size": "0x2828", "raw_size": "0x200", "nao_zero_no_arquivo": 27},
        "faixa_coberta_pelo_arquivo": "RVA 0x79CD000..0x79CD1FF",
        "exemplo": "0x79CF610 esta ALEM do raw_size, portanto e zero-preenchido em AMBOS os arquivos"
    },
    "conclusao": ("o builder NAO apagou .data001. Em disco os dois arquivos sao identicos la (27 bytes "
                  "nao-zero, mesma raw_size 0x200). Os ~400 bytes nao-zero do oraculo sao ESCRITOS EM "
                  "RUNTIME, no load, pela cadeia __dyn_tls_init. O '400 vs 27' medido antes era comparacao "
                  "de MEMORIA pos-load, nao de arquivo - e por isso nao provava causa de builder."),
    "consequencia_para_a_causa": ("as 'duas causas estruturais' colapsam em UMA: TLS.AddressOfCallBacks "
                                  "zerado. O estado PACE em .data001 e CONSEQUENCIA do load, nao uma "
                                  "segunda alteracao do builder."),
    "consequencia_para_o_contrato_do_builder": ("'restaurar .data001' e VAZIO: nao ha o que restaurar num "
                                                "bloco que e zero em disco nos dois arquivos e preenchido "
                                                "em tempo de execucao. O unico campo a restaurar e "
                                                "TLS.AddressOfCallBacks (RVA 0x79CC440 = 0x1879CC158)."),
    "ainda_nao_explicado": ("por que 0x79CA760 nao inicializa 0x79CF610 quando o callback e reabilitado "
                            "por patch de cabecalho (AV em 0x79CB22A). Hipoteses nao medidas: realocacao "
                            "interna (builder moveu .inits/.imports), ou pre-condicao de secao que so o "
                            "loader do oraculo satisfaz."),
}

d['frente_funcional_17h55'] = {
    "data": "2026-11-13T17:55:00Z",
    "script": "analysis/scripts/functional_dsp_probe.py",
    "objetivo": "exercitar IComponent::initialize + IAudioProcessor setup/process fora do gate S3",
    "resultado": {
        "oraculo": {"create_class0": "executado", "initialize": "AV",
                    "veh": {"code": "0xc0000005", "rip_rva": "0x322789"}},
        "leitura": ("o AV em initialize ocorre no ORACULO, nao no candidato: e limitacao do harness "
                    "(falta o grafo de objetos do host), nao defeito do candidato")
    },
    "fato_de_harness": ("o harness validado (analysis/scripts/harness_core.py, probe_class) NUNCA chama o "
                        "slot 3: so createInstance + QueryInterface + release. initialize/process/"
                        "createView seguem nao exercitados em qualquer imagem."),
    "armadilha_de_metodo": ("o .text do oraculo e CRIPTOGRAFADO em repouso; disasm a partir do arquivo do "
                            "oraculo produz lixo (0x322740 saiu como 'cld'). Disassembly do oraculo so e "
                            "valido a partir da memoria mapeada."),
}

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok; keys', len(d))
print(d['correcao_data001_17h55']['conclusao'][:160])
