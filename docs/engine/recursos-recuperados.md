# Auditoria de `RECURSOS_VALIDADOS_recuperados` (2026-11-25)

Auditoria só de leitura dos 231 arquivos (108.513.904 B) de
`RECURSOS_VALIDADOS_recuperados\`. Nenhum binário foi executado, carregado ou registrado.
Os PE/COFF foram lidos byte a byte, e os `.npz` foram lidos por `zipfile` com o cabeçalho
`.npy` (sem numpy, sem pickle). Os scripts ficaram no scratchpad da sessão, fora do projeto.

**Orientação do usuário, que vale para todo o documento.** O DSP oficial é o deste projeto:
dump `68D30368…`, `port\` e as etapas M1..M7. O material recuperado é apoio para GUI,
fontes e parâmetros. Ele **não** substitui o DSP nem muda a direção do trabalho, e
`recovered_native`/`.npz` não viram base nem oráculo do motor.

**Proveniência.** O material vem de **outro projeto**. Os JSON citam caminhos de outra
máquina e de outro usuário Windows: `C:\Users\<outro>\Documents\Projetos-claude\shadowFILES\…`.
Aqui ele é tratado como dado de terceiro, não confiável. A pasta externa citada não foi
consultada, por instrução do usuário.

---

## 1. Inventário por grupo (cobertura total, 231/231 por script)

| Grupo | Arq. | O que é | Utilidade |
|---|---:|---|---|
| `parameter_table_143_params.json` | 1 | tabela dos 143 descritores de parâmetro (id, nome, min, max, default candidato, flags, 4 ponteiros de callback), mais 4 tabelas de enum | **alta** (Resonia e M4/M6, como pista) |
| `svg\` | 29 | ícones e formas do editor (logo 450×600, botões 72×11, setas 18×18…) | **média** (referência visual; proprietário) |
| `png\` | 12 | texturas do editor (1×16 até 236×236) | **média** (idem) |
| `shaders_hlsl\` | 6 | fonte HLSL dos 6 pares de shader da GUI (reductionCurve, outline, renderTarget, shape, texture, gradient) | **média** (referência de render; proprietário) |
| `fontes\` | 3 | CoFo Sans Medium, CoFo Sans Regular (comerciais) e Noto Sans Math (OFL) | **baixa/risco** (ver §5) |
| `json\` | 2 | atlas de glyphs (`nodes` w/x/y) e métricas de glyph (`bearing`, `buffer_offset`) | baixa |
| `shaders_compilados\` | 12 | DXBC `vs_5_0`/`ps_5_0` compilados localmente pelo outro projeto; **não** estão em nenhum dump | baixa |
| `manifest.json`, `resource_validation.json`, `INDICE_RECURSOS.md` | 3 | controle: offset, tamanho e SHA-256 de cada recurso | média (serviram para reconferir tudo) |
| `preview_contact_sheet.png` | 1 | folha de contato gerada pelo outro projeto; não está em dump | nenhuma |
| `recovered_native\units\rva_*` | 42 dirs (127 arq.) + `host_validation.json` | 42 rotinas do **build 1.0.5** remontadas em MASM (`.asm`/`.obj`/`roundtrip.json`; `rva_61b790` tem `comparison_text.bin`) | baixa (só pista de mapeamento) |
| `recovered_native\dsp\` | 10 + 5 | `dsp_entry.*` = rotina **0x864740** (1.0.5) de 12.773 B, `link_closure`, `dependency_build`, 2+2 `.npz` | baixa (pista); `.npz` = nenhuma para M7 |
| `recovered_native\imports\` | 10 | `native_imports_candidate.vst3` (PE com seção `.imports` enxertada) e logs de falha de `InitDll` | **nenhuma / não usar** |
| `recovered_native\` (raiz) | 9 | `cold_sections_candidate.vst3` (1.0.5 com seções decifradas reinseridas), `recovered.{asm,obj,dll,lib,exp,def}` (PlainToNormal, NormalToPlain, GetLatencySamples), `manifest.json`, `validation.json` | nenhuma como entrega; o `.vst3` serviu **só como bytes** do 1.0.5 nesta auditoria |

A contagem fecha: 5 na raiz + 64 de mídia + 9 + 15 + 10 + 128 em `units` = 231.
O grupo homogêneo `units\rva_*` foi processado inteiro por script: 42 rotinas, mais a
rotina de `dsp\`, somam 43.

---

## 2. Respostas

### 2.1 Origem e identidade: **outro build** (1.0.5), não o dump do projeto (1.0.6)

| | Recuperado (`1176f5a1…`) | Projeto (`68D30368…`) |
|---|---|---|
| Versão nas strings de `.rdata` | `1.0.5` ×8, `1.0.6` ×0 | `1.0.6` ×8, `1.0.5` ×0 |
| PE TimeDateStamp | `0x6A423610` (2026-06-29 09:08:32 UTC) | `0x6AEC5AE2` (2026-11-05 10:30:58 UTC) |
| SizeOfImage / tamanho do dump | `0x82A5000` / 136.990.720 B | `0x82A8000` / 137.003.008 B |
| EntryPoint | `0x79CAEA0` | `0x79CDEA0` |
| Base de runtime | `0x18CC0000` | `0x199B0000` |
| `.text` vsize | `0x1CD57F7` | `0x1CD5487` |

- O dump `1176f5a1…` **não** está no FORK, então o hash dele não foi recalculado. A
  identidade foi conferida pelo `cold_sections_candidate.vst3`. A tabela de seções dele é
  igual à do artefato `1176f5a1` do `manifest.json`, e o cabeçalho traz
  `ImageBase = 0x18CC0000`, o mesmo valor de `inferred_runtime_base` da tabela de parâmetros.
  As 43 rotinas e os 50 recursos batem nele no RVA declarado.
- `original\soothe3.vst3` tem o mesmo cabeçalho do dump do projeto e `1.0.6` ×8 em claro.
  Portanto é o **mesmo build** do dump.
- **Conflito documental, para o orquestrador.** O `PROMPT_RETOMADA.md` diz que "latência
  2.304 é do build 1.0.5, não do dump 1.0.6". Porém `host\NOTAS.md` §7 mediu 2304 no
  `original\soothe3.vst3`, que é 1.0.6. E `GetLatencySamples` (`0x324E90`, 15 B) é idêntico
  nos dois builds. Este documento não altera aquele arquivo.

**Comparação por bytes** (dump do projeto em layout de memória, offset de arquivo = RVA;
`manifest.json` usa "file offset in supplied memory image", que também é RVA do 1.0.5):

- **Rotinas (43).** Reconstruí cada uma a partir do `.obj`, aplicando as relocações
  REL32/REL32_1 de `roundtrip.json`. Resultado: 43/43 com o SHA declarado e 43/43 iguais
  ao 1.0.5. No dump do projeto:
  - 1 é idêntica no mesmo RVA (`0x61B790`);
  - 2 estão no mesmo RVA e diferem só em campos relocados (`0x31E530`, `0x327A50`);
  - 18 são idênticas byte a byte em **RVA − 0x330**;
  - 22 são idênticas em RVA − 0x330, com exceção dos campos rel32;
  - nenhuma ficou sem correspondência.
- **Funções de `recovered_native\manifest.json`.** `PlainToNormal 0x3351A0` e
  `GetLatencySamples 0x324E90` são idênticas no mesmo RVA. `NormalToPlain 0x3351E0` difere
  em 1 byte: o disp do `movsd` passa de `0x207A140` para `0x207A138`, e o valor é o mesmo
  `1.0`. O `real_207a140` do manifest, no 1.0.6, está em `0x207A138`. Em `0x207A140` o
  1.0.6 tem `1.04`.
- **Alvos externos (110 pares).**
  - 71 PROC são iguais em 16 B, com deslocamento 0 (stubs IPP `0x1070..0x15B0`) ou −0x330.
  - 6 PROC diferem só em thunk de IAT ou TLS.
  - 21 constantes BYTE são iguais no RVA deslocado: em geral −8, por exemplo
    `0x2079FA4→0x2079F9C` (`1.0f`); também `0x20143F0→0x2014360` (−0x90) e `0x2077700→0x20777C0`.
  - 12 BYTE diferem: tabelas de ponteiro rebaseadas (`0x18CC0000` vs `0x199B0000`, alvo no
    mesmo RVA − 0x330), IAT, e `.data` de runtime (`0x26B1838`).
- **`.text` inteiro, em blocos de 16 B.** São 1.889.663 blocos: 382.423 (20,2%) no mesmo RVA,
  1.113.855 (58,9%) em −0x330 e 393.385 (20,8%) diferentes. O deslocamento começa perto do
  RVA antigo `0x84FC00`.
- **Cluster DSP.** Comparei o antigo `[0x860330, 0x8E0330)` com o novo `[0x860000, 0x8E0000)`.
  São 519.840/524.288 bytes iguais (99,15%), em 2.210 trechos divergentes. O maior trecho
  tem 15 B, e 2.070 deles têm 2 B. No miolo `0x8A0000–0x8D2000` são 203.572/204.800 (99,40%).
  **INCERTO:** que todas as divergências sejam só deslocamentos rip-relative. Não houve
  desmontagem para provar isso.
- **Recursos (50).** 50/50 batem com o hash do arquivo e com o 1.0.5 no offset. No 1.0.6,
  12/50 estão no mesmo RVA e 50/50 foram achados em outro RVA: o deslocamento é −16 na
  maioria, e também −32, +16, +32, +1664, −4544 ou 0. 48/50 também aparecem em claro em
  `original\soothe3.vst3`.
- **Tabela de parâmetros.** No 1.0.6 está no mesmo RVA `0x238E9C0`. Os campos sem ponteiro
  são iguais nos 143 registros, e os 572 ponteiros de callback apontam para o mesmo RVA.

**Armadilha de RVA.** Todo RVA do material recuperado é do 1.0.5.
`units\rva_868840` **não** é o `0x868840` do projeto, que inicializa o ring e é o
`NÃO EXTRAÍDO` de `port/src/chan.rs`. No 1.0.6 essa unidade está em `0x868510`. O
`dsp_entry.*` também não é `0x868840`: é `0x864740`, que no 1.0.6 fica em `0x864410`
(há decompilado em `docs/engine/decomp/80864410.c`).

### 2.2 Código nativo: o que cobre e o que adianta (pouco)

Mapa 1.0.5 → 1.0.6 das 43 rotinas (Δ = −0x330, exceto as três primeiras):

`0x61B790→0x61B790`, `0x31E530→0x31E530`, `0x327A50→0x327A50` (GetPluginFactory),
`0x1797BF0→0x17978C0`, `0x864740→0x864410` (dsp_entry), `0x860EC0→0x860B90`,
`0x861E90→0x861B60`, `0x867B20→0x8677F0` (escalonador), `0x867FF0→0x867CC0`,
`0x868840→0x868510`, `0x868A60→0x868730`, `0x868F00→0x868BD0`, `0x868F70→0x868C40`,
`0x8692C0→0x868F90`, `0x869600→0x8692D0`, `0x86B0A0→0x86AD70`, `0x86B130→0x86AE00`,
`0x86B5D0→0x86B2A0`, `0x86C750→0x86C420`, `0x86D320→0x86CFF0`, `0x86D7F0→0x86D4C0`,
`0x86DA10→0x86D6E0`, `0x86DEE0→0x86DBB0`, `0x86E310→0x86DFE0`, `0x86E6B0→0x86E380`,
`0x86EB80→0x86E850`, `0x86F3F0→0x86F0C0`, `0x86F4A0→0x86F170`, `0x86F670→0x86F340`,
`0x86F7B0→0x86F480`, `0x86FC50→0x86F920`, `0x876FB0→0x876C80`, `0x877450→0x877120`,
`0x8777D0→0x8774A0`, `0x877860→0x877530`, `0x877BB0→0x877880`, `0x8808E0→0x8805B0`,
`0x880970→0x880640` (bypass/delta), `0x881380→0x881050` (aloca buffers),
`0x881A70→0x881740`, `0x8852E0→0x884FB0`, `0x88C3C0→0x88C090`, `0x88C860→0x88C530`.
São 44.186 B no total. Todo RVA novo é início de função em `functions.csv`, exceto
`0x868510`, que é folha sem `.pdata`.

- **Gaps de `pending.rs` e de M1..M7.** O material **não cobre** nenhum deles: divisão
  `0x63640`, recíproco `0x88E130`/`0x29B260`, ln/exp `0x293760`/`0x240C00`, sample rate
  `0x8B68AB`, miolo `0x8B3ED0` (seria `0x8B4200` no 1.0.5) e cadeia `0x8AD2B0` (seria
  `0x8AD5E0`). Ganho para M1..M7: **zero como prova**.
- A rotina `0x86F170` (gap não bloqueante "identidade de `0x86F170`") está entre as 43 como
  `rva_86f4a0`. O `.asm` é listagem MASM sem nomes e não traz a identidade.
- O `.asm` é desmontagem de outro build. Pela regra 5 ele é leitura, não prova. Ler a mesma
  função no IDA do 1.0.6 custa o mesmo e é a fonte válida.

### 2.3 O que os `bit_identical: true` provam (e o que não provam)

- **Provam só isto.** O texto MASM remonta para os mesmos bytes do 1.0.5 (conferido aqui:
  43/43 SHA). Num processo que carregou **e inicializou o módulo original 1.0.5**, trocar
  a rotina pela cópia remontada não mudou a saída. Como os bytes são idênticos, o resultado
  é esperado por construção e não demonstra entendimento nem port.
- **Dependências que vinham do original.**
  - `dsp\roundtrip.json`: 33 alvos externos (27 PROC + 6 BYTE).
  - `link_closure.json`: com 20 rotinas locais, ainda há **36 alvos não resolvidos**
    (23 PROC + 13 BYTE): stubs IPP, thunks de CRT/IAT, constantes e `.data` de runtime.
  - `linked_dependencies`: 39 callees religados, mas ainda sobre o "Original initialized
    state" (o escopo declarado no JSON).
  - Não é port independente.
- **`.npz`, conferidos bit a bit.**
  - `dsp\reference_render` vs `candidate_render`: 3 arrays.
  - `linked_dependencies\reference` vs `candidate`: 18 arrays.
  - Todos são `<f4`, `shape (2, 32768)`, ou seja, 2 canais × 32.768 frames, sem compressão.
  - Os 21 pares são idênticos, com 0 palavras diferentes. `default_tones_256` é idêntico a
    `tones_256` (SHA `78d9ab93…`).
  - Faltam no arquivo: o sinal de entrada, o sample rate, o bloco (só se infere pelo sufixo
    `_256/_127/_512`, **INCERTO**), os valores de preset (só há nomes como `deep_fast`,
    `delta_mix`, `ms_unlinked`, `hard_quality`, `linear_lowlatency`) e o host.
  - `*_silence_tail_512` não é silêncio fora de `default`: o pico chega a 0,62. **INCERTO:**
    se isso é estado herdado do caso anterior.
- **Conclusão (orientação do usuário).** Os `.npz` são saídas do 1.0.5 com host não
  descrito. **Não** servem de oráculo para o M7. O oráculo continua `host\` sobre o 1.0.6.

### 2.4 `parameter_table_143_params.json` vs `params.csv` e §8.3.1: **concorda**, e acrescenta

Conferi o arquivo contra o **dump do projeto**: a tabela está em `0x238E9C0`, com
registros de 104 B (`0x68`) e ids 0..142 sequenciais.

- **Contra `params.csv`.** Bate em 143/143: nome, `value_a = max`, `value_b = default` e
  `flags`. O `rva` do CSV é o início do registro − 0x10, o que é coerente com a spec
  ("índice = campo `+0x10` da tabela `0x238E9B0`").
- **Contra §8.3.1.** Os nomes por índice são coerentes com o mapa de handlers: 0 Depth,
  5/6/7 Detail/Attack/Release, 16 Stereo mode, 17 Stereo link, 18 Stereo focus, bandas
  19..90 em blocos de 9 ("Band 1 used"…), 92 Max cut, 93 Wet trim, 94 Mix, 95 Out trim,
  96 Delta, 97 Bypass, 98.. grupos ("LR depth"), 123 Link all, 127.. "Channel N enabled". A tabela não contém offsets de estado, então não
  contradiz o mapa índice → offset.
- **O que acrescenta, tudo lido também no dump 1.0.6:**
  - **`minimum`**, que falta no CSV: 32 parâmetros com min ≠ 0. Exemplos: tilts 0,1..10;
    frequência de banda 20..20000; depth de banda −10..10; Q 0,1..10.
  - **Defaults por banda.** Exemplos: Band 1 freq 100 e Q 0,707; Band 2 freq 4000 e
    depth 2,5. O JSON marca isso como `initial_or_default_candidate`: o consumidor que grava
    o estado inicial **não** está provado.
  - **Ponteiros de callback** (campos +72/+80/+88/+96 a partir do id): +72 é
    valor → normalizado e +80 é normalizado → valor. `0x3351A0`/`0x3351E0` são as lineares
    (43 parâmetros); há também `0x335240`/`0x335300` (35), `0x3358F0` (43), `0x3353B0`/`0x335470`,
    `0x335550`/`0x335670` e `0x335790`/`0x335830`.
  - **Enums com rótulos.**
    - band_shape: Low cut, Low shelf, Bell, Bandpass, Band reject, Tilt, High shelf, High cut.
    - stereo_mode: L/R, M/S.
    - quality: normal, high, ultra.
    - band_channels: 20 rótulos de canal.
    - As tabelas de band_shape e stereo_mode foram resolvidas no 1.0.6 (8/8 e 2/2, strings
      com deslocamento −16). As de quality e band_channels vêm de switch e **não** foram
      reconferidas aqui (**INCERTO** no 1.0.6).
- **Pista para M4 (callback `[rdx+0x50]`).** O setter `0x867D80` lê `idx=[rdx]`,
  `min=[rdx+0x28]` e `max=[rdx+0x30]`. Esse é exatamente o layout do registro a partir do
  id (id@0, min@40, max@48). Se `rdx` apontar para o id, `[rdx+0x50]` é o campo +80, o
  ponteiro normalizado → valor (`0x3351E0` nos lineares). Isso é compatível com
  `callback((double)xmm8)` seguido de clamp em `[min,max]`.
  - O §P2 da spec mediu "+0x50 da tabela `0x238E9B0`". Esse endereço é id+0x40, o campo de
    flags (0/1/0x101). Há indício de **desalinhamento de 0x10** nessa refutação.
  - `NÃO PROVADO`: que `rdx` aponte para esse registro (pode ser uma cópia de runtime).
    Conferir no dump em `00867DFC`/`00867E10` e na origem de `rdx`.

### 2.5 GUI: validação, utilidade e licença

- **Hashes reconferidos.**
  - 50/50 recursos com o SHA de `manifest.json`.
  - As 3 flags de `resource_validation.json` concordam com o recalculado.
  - 12/12 shaders: SHA do HLSL e do DXBC iguais aos de `resource_validation.json`.
  - O DXBC é saída de compilação local: não está em nenhum dump.
  - Os 2 `json\` estão nos dois dumps; no 1.0.6, em outro RVA.
- **Fontes, pela tabela `name`.**
  - `font_01fd02e0.ttf` (CoFo Sans Medium) e `font_01ff1e30.ttf` (CoFo Sans Regular), v2.005:
    "© 2018 LLC Contrast Foundry … All rights reserved", vendor `COFO`, `fsType = 4`
    (embedding restrito a preview/print). **Fonte comercial de terceiro: risco alto para
    distribuição.** Não embutir no Resonia sem licença própria.
  - `font_021edad0.ttf` (Noto Sans Math 2.001, Google/Monotype) está sob a **SIL OFL 1.1**,
    com `fsType = 0`. Pode ser usada, mas é melhor baixar do upstream do que usar a cópia
    extraída.
- **SVG, PNG, HLSL e JSON** são arte e código de GUI da oeksound, propriedade de terceiro
  comercial. **Risco de distribuição**: servem como referência de dimensão, estrutura e
  técnica de render, não como asset para empacotar no Resonia.
- `host_validation.json` traz `createView rect = [0,0,1050,621]`. É **pista** do tamanho da
  janela, obtida por método proibido (ver §2.7).

### 2.6 Código-fonte do Resonia ou scripts geradores

- **Não há** código do Resonia nem nada que ajude `resonia\RECUPERACAO.md`: nenhum Rust,
  nenhum `Cargo.*`.
- Scripts geradores citados que **não vieram**: `check_module_startup.py`,
  `observe_native_import_fault.py`, `test_native_imports.py` e o esquema
  `soothe3_parameters_schema.json`. Não foi investigado mais (instrução do usuário).

### 2.7 Conflitos com `LEMBRAR DISSO.md`

O método do outro projeto incluiu: `LoadLibrary` e `InitDll` do original 1.0.5;
`.vst3` modificados (seções decifradas reinseridas; seção `.imports` enxertada em
`0x82A5000`); código remontado ligado dentro do módulo original já inicializado; e
contagem dinâmica de chamadas. A troca de código num módulo vivo é **escrita no processo
alvo** e viola a regra 6. Os artefatos são de outro build, o que conflita com "toda
constante sai do dump".

| Pode usar como prova | Só como pista | Não usar |
|---|---|---|
| Nada do material, por si. Valem as releituras feitas aqui **no dump 1.0.6**: tabela `0x238E9C0` (min/max/default/flags/ponteiros), bytes dos recursos, constantes deslocadas | mapa de RVA 1.0.5→1.0.6; `.asm` das 43 rotinas; semântica dos campos +72/+80 e dos enums; ligação `[rdx+0x50]` ↔ campo +80; `createView 1050×621`; contagens de `helper_calls` | os dois `.vst3` candidatos (binários alterados: **não carregar**); `recovered.dll/.obj/.lib`; os `bit_identical`; os `.npz` como oráculo; os logs de startup e exceção |

---

## 3. Plano de aproveitamento

| Etapa | Aproveitamento |
|---|---|
| M1, M2, M3 | nenhum: os RVAs não estão no material |
| M4 | pista do campo +80 para `[rdx+0x50]`; provar no dump a origem de `rdx` em `0x867D80` e ler `0x3351E0`/`0x335300`/`0x3358F0`/… no 1.0.6 |
| M5 | nenhum (`0x8B3ED0` não está coberto) |
| M6 | os defaults dos 143 parâmetros (lidos no 1.0.6) como candidatos do estado inicial; continua `NÃO PROVADO` até achar o consumidor que grava o estado |
| M7 | nenhum; o oráculo continua `host\` + `original\soothe3.vst3` (1.0.6), mesmo bloco e alinhamento 2304 |
| Resonia: parâmetros | usar nomes, ids, min/max/default, flags e rótulos de enum, reconferidos no 1.0.6, como especificação da camada de parâmetros. A curva normalização↔valor é linear nos 43 que usam `0x3351A0`/`0x3351E0`; as demais 5 famílias de callback ainda precisam ser lidas |
| Resonia: GUI | SVG/PNG/HLSL como referência de layout e render, com janela 1050×621 (pista). Redesenhar ou reimplementar sem empacotar os assets. Fontes: Noto Sans Math do upstream (OFL) e substituto livre para CoFo Sans |

## 4. Verificado e não verificado

- **Verificado por script:**
  - inventário 231/231 com SHA;
  - cabeçalhos PE dos 6 binários;
  - 43/43 rotinas reconstruídas e localizadas no 1.0.6;
  - 110 alvos externos;
  - diff do `.text` e do cluster DSP;
  - 50/50 recursos e 12/12 shaders;
  - 21/21 pares `.npz`;
  - 143/143 parâmetros contra o dump e contra `params.csv`;
  - tabelas `name` dos TTF.
- **INCERTO / não verificado:**
  - o SHA `1176f5a1…` em si (arquivo ausente do FORK);
  - que as diferenças do cluster DSP sejam só deslocamentos;
  - as tabelas de enum quality e band_channels no 1.0.6;
  - o significado dos sufixos dos `.npz`;
  - a origem de `rdx` no setter.
