p = r'D:\PROJETOS\shadowFILES\analysis\startup_audit\STATUS.md'
s = open(p, encoding='utf-8').read()
head = '## Atualização 13/11/2026 13h15 (-03) — o candidato não é determinístico: dois limites, não um número\n\n'
body = (
    'Mesmo harness, mesmas capturas do gate estendido. Comparei a divergência sob duas máscaras:\n\n'
    '| Região | bruto | só piso do oráculo (limite superior) | união dos pisos (limite inferior) |\n'
    '|---|---|---|---|\n'
    '| `.data` | 509.352 | **214.684** | **3.590** |\n'
    '| `.data001` | 375 | 359 | 359 |\n'
    '| `.rdata01` | 5 | 5 | 5 |\n'
    '| **total** | | **215.048** | **3.954** |\n\n'
    'A união esconde **211.094 bytes** em `.data`. E o motivo não é ruído: **339.655 bytes são voláteis\n'
    '*só* no candidato** (o oráculo é determinístico ali); apenas 8,6% das palavras tocadas são\n'
    'ponteiro-like, contra 23,6% no controle (volatilidade só do oráculo). O padrão típico é\n'
    '`cd ab cd ab` (fill de debug heap) numa execução e um valor pseudo-aleatório na outra.\n\n'
    'Ou seja: **o candidato não é determinístico no ponto de amostragem** (518.125 bytes voláteis\n'
    'contra 315.923 do oráculo). Enquanto isso não for explicado, qualquer contagem de bytes de gate\n'
    'é um piso artificial. O gate passa a ser reportado como par: **3.954 (inferior) / 215.048\n'
    '(superior)**; aprovação exige o superior em zero.\n\n'
    'Evidência: `xgate_mask_bounds.json`, `xgate_volatility_class.json`.\n\n---\n\n'
)
if '13h15' not in s:
    open(p, 'w', encoding='utf-8').write(head + body + s)
    print('inserted')
