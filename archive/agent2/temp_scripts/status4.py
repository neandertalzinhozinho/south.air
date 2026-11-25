p = r'D:\PROJETOS\shadowFILES\analysis\startup_audit\STATUS.md'
s = open(p, encoding='utf-8').read()
head = '## Atualização 13/11/2026 13h35 (-03) — o residual nasce no LOAD (4.640), não no create\n\n'
body = (
    'Captura load-only (load + dump, sem inits, sem create), 3× por imagem (`dump_load_only.py`):\n\n'
    '| Região | Piso oráculo | Piso candidato | Residual load | Residual pós-create |\n'
    '|---|---|---|---|---|\n'
    '| `.data` | 4.706 | 1.893 | **4.276** (= inferior = superior) | 404 |\n'
    '| `.data001` | 16 | 0 | **359** | 359 |\n'
    '| `.rdata01` | 0 | 0 | **5** | 5 |\n'
    '| **total** | | | **4.640** | **768** |\n\n'
    'No load não há ambiguidade de máscara: 4.260 bytes oráculo-não-zero/candidato-zero, 16 ambos,\n'
    '**0 extras**. A receita de 306 inits **cura 3.923** desses 4.276 — porque reproduz os\n'
    'inicializadores estáticos que o builder deixou de rodar ao zerar `TLS.AddressOfCallBacks`.\n\n'
    '**Prova direta:** `LicenseDbRemote`, `IlokCloudRemote`, `iLok2Remote`, `iLok3Remote`,\n'
    '`LicenseDb`, `ImlIasm_` **já existem no oráculo antes de qualquer init** e nunca aparecem no\n'
    'candidato. Janela 0x52F000–0x532000: 1.265 → 182. O que sobra é o subsistema de licença.\n\n'
    '**Correção de método (controle negativo):** chamar `__dyn_tls_init` à mão **também falha no\n'
    'oráculo** (RVA 0x179790B, rax 0x181D9000B). O callback não é reentrante — a falha do candidato\n'
    'em RIP=0 **não** prova estado ausente. Só um artefato regenerado, com o loader executando a\n'
    'cadeia naturalmente, pode testar isso.\n\n'
    'Seções exclusivas do candidato: `.imports` (0x82A5000) e `.inits` (0x82B8000, 0x5ABBC).\n\n'
    'Entregas: **Claude OK** (`post_create_stability_review.json` reproduziu 514.595/388.337/3.290/\n'
    '3.191 exatamente; rejeitou as decomposições 3-vias por falta da baseline load-pure — agora\n'
    'suprida). **Codex BLOCKED** (limite de 5h nos dois terminais; S3-LASTMILE não entregue, parcial\n'
    'no terminal: 67/41 e 66/40 são IDs de facets de `std::locale` via MSVCP140).\n\n'
    'Evidência: `s3_load_stage_gate.json`, `tls_chain_slots.json`.\n\n---\n\n'
)
if '13h35 (-03) — o residual nasce' not in s:
    open(p, 'w', encoding='utf-8').write(head + body + s)
    print('inserted')
