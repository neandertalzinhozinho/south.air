p = r'D:\PROJETOS\shadowFILES\analysis\startup_audit\STATUS.md'
s = open(p, encoding='utf-8').read()
head = '## Atualização 13/11/2026 12h55 (-03) — gate estendido, piso do mesmo harness: 3.954 bytes\n\n'
body = (
    'Superfície completa, 3 capturas do build A e 3 execuções do candidato (273 inits) no mesmo\n'
    'harness (`analysis/scripts/dump_extended_gate.py`):\n\n'
    '| Região | RVA | Piso oráculo | Piso candidato | Residual |\n|---|---|---|---|---|\n'
    '| `.data` | 0x217F000 | 315.923 | 518.125 | **3.590** (3.559/31/0) |\n'
    '| `.data001` | 0x79CD000 | 16 | 0 | **359** (358/0/1) |\n'
    '| `.rdata01` | 0x79CC000 | 0 | 0 | **5** = `AddressOfCallBacks` |\n'
    '| `.text001` | 0x79CA000 | 0 | 0 | **0** |\n'
    '| **total** | | | | **3.954**, igual nas 9 combinações |\n\n'
    '**Revogação com histórico:** 3.290 e 3.191 não são números de gate. O piso **não é propriedade\n'
    'da imagem** — o mesmo build A, mesma receita, deu piso 514.595 num harness e 315.923 neste.\n'
    'Comparar capturas de harnesses distintos com o piso de um deles sub-mascara. Piso só vale no\n'
    'harness onde foi medido.\n\n'
    'Os 5 bytes de `.rdata01` são exatamente o campo TLS zerado (0x79CC440…444: `58 c1 9c 87 01`\n'
    'vs zeros) — a causa estrutural do builder, agora dentro do gate e medida.\n\n'
    'Evidência: `xgate_12h55.json` (artefatos `xA_create_r{1,2,3}_*`, `xC273_create_r{1,2,3}_*`).\n\n---\n\n'
)
if '12h55' not in s:
    open(p, 'w', encoding='utf-8').write(head + body + s)
    print('inserted')
