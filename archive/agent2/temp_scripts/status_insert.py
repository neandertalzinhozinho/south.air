import io

p = r'D:\PROJETOS\shadowFILES\analysis\startup_audit\STATUS.md'
s = open(p, encoding='utf-8').read()
head = '## Atualização 13/11/2026 12h40 (-03) — causa estrutural do builder: TLS e .data001 zerados\n\n'
body = (
    'Medido no cabeçalho PE e em memória, nos dois arquivos:\n\n'
    '| Item | Build A | Candidato |\n|---|---|---|\n'
    '| `TLS.AddressOfCallBacks` (RVA 0x79CC440) | `0x1879CC158` | **`0x0`** |\n'
    '| `.data001` (RVA 0x79CD000) bytes não-zero | 400 | **27** |\n'
    '| `__dyn_tls_init` (0x79CB190, `.text001`) | idêntico | idêntico |\n'
    '| array de callbacks (0x79CC158 → 0x1879CB190) | idêntico | idêntico |\n\n'
    'O builder zerou o campo do diretório TLS: o candidato **nunca executa a cadeia de\n'
    'inicializadores dinâmicos**. Restaurar só o ponteiro dá AV em `0x79CB22A`\n'
    '(`mov rax,[0x79CF610]` = 0). `.data001` é o bloco PACE/iLok (`LDSvc.exe`,\n'
    '`activation.paceap.com`) e está **fora da área do gate** (0x217F000 + 6.217.208).\n\n'
    'Teste com os 12 inicializadores dinâmicos reais (lista de 273): create 0, gate **3.191**\n'
    '(piso próprio 394.635; 9/9 combinações), corrige 0x530188/0x530D38/0x530D98/0x49B90 e\n'
    '**não** corrige 0x530FC8/0x530FE8/0x530000/4/guards. Explica ~99 dos 3.290 bytes.\n'
    'Massa restante: **3.151 escritas ausentes**, 0 na janela 2, em 0x532000–0x538000.\n\n'
    'Evidência: `s3_tls_builder_gap.json`.\n\n---\n\n'
)
if '12h40' not in s:
    open(p, 'w', encoding='utf-8').write(head + body + s)
    print('inserted')
print(open(p, encoding='utf-8').read()[:300])
