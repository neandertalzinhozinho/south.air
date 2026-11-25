# PROMPT DE RETOMADA — extração do DSP do soothe3

> **Atualizado em 2026-11-25 (M4)**, sincronizado com `PLANO_MOTOR_AUDIO.md` §25/§26/§23.15.
> Autocontido: não depende de conversa anterior. Se este arquivo divergir do plano, **o plano
> vence** — este prompt é um resumo operacional, não a fonte.

---

Objetivo: continuar a extração estática do motor de áudio DSP do soothe3, do ponto exato em
que a sessão anterior parou, e avançar as etapas na ordem do `PLANO_MOTOR_AUDIO.md` §23.12/§25.

## Regra de ouro

Este trabalho **não é aproximação**. A entrega só existe com os 5 itens, por função:
(a) endereço no dump, (b) pseudocódigo/desmontagem comentada, (c) constantes lidas do dump
com RVA, (d) estruturas com offsets provados, (e) código com a mesma aritmética, mesma
ordem, mesmos coeficientes.

Proibido: estimar qualquer número, inventar nome de opção, propor "algoritmo equivalente",
ajustar até o null-test bater, inferir fórmula pelo nome do parâmetro, tratar indício como
prova, ou considerar decompilado como prova (prova é a instrução, com RVA). O que não foi
lido do dump é marcado `NÃO EXTRAÍDO` / `NÃO PROVADO` e o trabalho para naquele ponto.

Proibido escrever no processo alvo: sem hook, sem patch de checksum, sem injeção, sem
Frida. Só dump estático e processo somente-leitura.

## Fontes (não substituir, não editar)

| Papel | Caminho | Identidade |
|---|---|---|
| FONTE DE VERDADE | `dumpsooth\nyx_soothe3_dump.bin` | 137.003.008 B, SHA-256 `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C` |
| O QUE O IDA ABRE | `dumpsooth\soothe3_unpacked.dll` | mesmo dump em PE válido, `ImageBase 0x180000000`, 30.859 funções `.pdata` |
| BANCO DO IDA | `C:\Users\tromb\AppData\Local\Temp\opencode\ida_pe\soothe3_pe.dll.i64` | já analisado; é o banco do PE acima |
| NÃO É FONTE | `original\soothe3.vst3` | `.text` 100% cifrado; só serve de black box para o null-test |

`LEMBRAR DISSO.md` é **congelado**: leia, não altere. Hash de referência
`D10EB333C140FC4800B06C6CA234171B62EDA7348872E33C88BDA378B7BECE49`. Se algo nele divergir
da leitura do dump, registre o conflito no `PLANO_MOTOR_AUDIO.md` §23.14 e siga a leitura —
sem tocar no arquivo.

## Onde a sessão anterior parou (estado real, 2026-11-24)

**Etapas fechadas — NÃO REFAZER:**

| Etapa | Objeto | Resultado provado | Doc |
|---|---|---|---|
| D0 | `0x8B2C30` | FIR de **32 taps**, coeficientes por bloco em `ctx+0x40`; anel `buf[32]` + `pos` em `S+0x80`; 27 `mulss` não são 27 taps | §23.4 / spec §10 |
| A | `0x8CAE90` | MAC em lotes de bandas; `0x1580` é MAC com FMA, não soma | §23.1 / spec §11 |
| B | 9 primitivas | ordem dos argumentos provada por opcode (`0x1580` MAC, etc.) | §23.2 / spec §17.6 |
| C | descritores 24 B | escritor `0x85E6C0` (23 casos, tabela `0x85FFA0`), alocador `0x563E40`, `[outer+8]=ctx`, tabela caso→vetor | §23.3 / spec §18.4 |
| D1 | `0x8BF650` / `0x8BFD30` | plumbing de despacho | §23.5 / spec §18.1 |
| E | `0x8C33D0` | pseudocódigo por desmontagem (2.128 B) | §23.6 / spec §18.2 |
| §24 | `0x20E0` / `0x7B40` | FFT **direta** e **inversa** do IPP no caminho de áudio; wrapper de 256 B, `[spec]==7`; Rust em `checks/stage_fft_rust.rs` | §24.4 / spec §19 |
| F | `0x873440`/`0x880390`/`0x8B2C30` | **`K = δ0`** por construção: `0x873440` zera os segmentos, grava `1.0f` em `[0]` e só então copia 32 floats por valor para `band+0x40`; o FIR de 32 taps é passa-direto (`y=x`), com `count=0` → `y=0`. Sem aritmética de parâmetro | §23.7 / spec §10.4 |
| G | `0x867D80` | escritor único dos campos de estado: cadeia `0x862E40` → `0x8634A0` → `[obj+0]` → `0x862EF0` → `0x867D80`; `state = engine+0x54`; **mapa 143 índices → offset** com store provado; índice = `+0x10` da tabela `0x238E9B0` (isomorfismo 143/143) | §23.8 / spec §8.3.1 |
| H | `0x8B3ED0`/`0x8C0BD0`/`0x8C1440` | dinâmica inline (4 blocos), detector, smoother, MAC, estagiador+mistura, curvas `A^(1−σ)` | §23.9 / spec §8.2/§8.4 |
| J | `checks/j4_fft.rs` + `checks/stage_j_*.rs` | port Rust: J1/J2/J3/J4/J5/J6, **57 testes verdes** (FFT ordens 8..19 + split, ring/canal, motor G/H); kernels como fonte única em `port/src/` | §24.5 / §25 |

**Fechada também, como subproduto de F:** a math do design — `0x1C8500` = **ln** (impl
`0x293760`) e `0x1C84A0` = **exp** (impl `0x240C00`), provado por instrução; `0x882DE0` =
sino gaussiano em log2-frequência com `out(f) = (10^(D/20))^g(f)`, fórmula completa com RVA
em §23.7 / spec §10.4.

**Pendências residuais — não bloqueiam K, mas ficam marcadas:**

- **G** (§23.8): mapa completo provado. Em 2026-11-24 o par `+0x5F8`/`+0x5ED0` fechou
  (`checks/p_extras.md` §P1: subobjetos embutidos, construtores `0x86A4E0`/`0x86A8C0` em
  `00863929`/`008639E3`, destruidor `0x863140`). Resta `NÃO PROVADO` só a identidade do
  callback `[rdx+0x50]` — provado que **não** é campo da tabela `0x238E9B0` (§P2).
- **H** (§23.9): o papel dos 16 buffers de `0x8C1440` e a atribuição grupo→coeficiente
  foram **FECHADOS em 2026-11-25** (`checks/q_8c1440_buffers.md`; spec §8.4.3/§8.4.7/§8.4.8);
  resta `NÃO PROVADO` só o nome/unidade dos 4 coeficientes, a faixa de `g`, a intenção
  musical e `nch > 2`. Continua `NÃO EXTRAÍDO` a origem de `A1`/`A2` em `0x882FC0`
  (spec §8.2(f)); o campo de sample rate em `0x8B68AB` segue `NÃO PROVADO` (`r13` = arg1 de
  `0x8B3ED0`); `0x1400` **PROVADO** (dot product); `0x86F170` **mecânica PROVADA**, nome
  `NÃO PROVADO` (`checks/p_extras.md` §7a/§7b).
- **F**: refutada IFFT na cadeia de `K` (nenhum `call` a `0x1010`/`0x1280` em
  `0x87B680`/`0x87BB60`/`0x87DB30`/`0x882FC0`/`0x882DE0`/`0x8834C0`).

## Pendências de verificação de K–O — **TODAS FECHADAS (2026-11-24)**

K–O foram **entregues** (`checks/k_core.md`, `l_filtro.md`, `m_analise.md`, `n_canal.md`,
`o_saida.md`) e o balanço verificado está em `checks/verificacao_k_o.md` e no
`PLANO_MOTOR_AUDIO.md` §23.15 — "Balanço K–O". **Não refaça o que já está provado.**

Três resultados mudaram o desenho:

1. **N** — a ordem é **núcleo → análise**: `008AD601 call 0x8B3ED0` vem antes de `008AD9FA`
   (`0x8B8E70`), `008ADC52` (`0x8B9E40`), `008ADF9B` (`0x8BA1B0`), `008AE096` (`0x8BA7B0`),
   `008AE5EC` (`0x8A1EE0`). "Análise → núcleo" está **refutada**.
2. **L** — `+0x80` do descritor é **contagem de ponteiros** (`008832C1`/`00883371`), não flag.
3. **O** — não há lei de estéreo em `0x899940` (0 op float); o único ganho é `arg2/arg3`
   (`008AD0B9 divss`), igual para todos os canais.

Fechamento item a item (todos com RVA):

1. ~~`0x5F5C0`~~ — **PROVADO**: `0x1400` → `0x21C6288[4]`=`0x199BAC20` → `0xAC20` →
   `0000AC46 call 0x5F5C0`; `vmulss`/`vaddss`/`vfmadd231ps`, store `0005F6F7` ⇒ dot.
2. ~~`0x8C33D0`~~ — **PROVADO**: primitivas (`0x11C0`→`0x50E0`, `0x11F0`→`0x5BC0`,
   `0x1250`→`0x69C0`, `0x1100`→`0x3480`) e `008C34BD`/`008C34C7` lidos (`B+0x404`/`B+0x400`
   da cópia em `[rbp+0x340]`); `0x8C32C0` não escreve esse cabeçalho.
3. ~~satélites~~ — **OK** (`0x8AE6F0` contínua após o `.pdata` em `008AE78F`; `0x8C3F10`,
   `0x8C42D0`, `0x8C32C0`, `0x8C3E00` conferidos por mapa de `call`).
4. ~~`0x87BB60`~~ — **OK (negativa)**: 23 ops float, todas escalares em registrador →
   não há biquad/state-space nem recursão por amostra.
5. ~~`0x8BA7B0` vs `0x8A1EE0`~~ — **FECHADO**: 60 instruções cada, 3 diferenças (2 desvios de
   branch + `mov byte [rsp+0x20],1` vs `r10b` com `r10=0`). Único parâmetro distinto = 5º
   argumento de `0x8B35A0` (1 vs 0). Ramos de `0x8AD2B0` **fechados agora**:
   `[state+0x58]` (`008AD76B`) escolhe o layout do descritor — `r8+0x238`/`+0x2C0`
   (`008AD7A7`/`008AD7AE`) se ≠ 0, ou `r8+0x1A8`/`+0x230` (`008ADA04`/`008ADA0B`) se = 0;
   `[state+0x52]` (`008ADFAB`, `008AE56F`) porteia `0x8BA7B0` (`008AE096`) e `0x8A1EE0`
   (`008AE5EC`).
6. ~~Restante de P~~ — **fechado/delimitado em 2026-11-24** (`checks/p_extras.md`, segunda
   rodada): `0x86F340`/`0x860B90` = clones espelhados provados; `0x86F170` = dois descritores
   (0x30 B) com deslocamento `4*d`; 16 buffers de `0x8C1440` = **FECHADOS em 2026-11-25**
   (`checks/q_8c1440_buffers.md`); sabor da FFT = **CCS PROVADO por medição** (`n/2+1` pares em ordem
   natural, `Im(DC)=Im(Nyq)=0`; §24.5 reescrito em 2026-11-24 — a exclusão anterior de CCS
   estava errada);
   linear phase = `NÃO EXTRAÍDO` como instância (ganho é zero-fase por multiplicação de bins);
   sample rate = identidade `NÃO PROVADA` (`r13` = arg1 de `0x8B3ED0`, `008B3F14`).
7. Produtor de `B+0x400/+0x404`: **`0x8C32C0` não é** (escreve em `arg1+0x1A0`,
   `008C33A6`/`008C33BD`); cadeia para em `008B6A16` → `NÃO PROVADO`.
8. **J - INICIADO em 2026-11-24.** `checks/stage_j_core.rs` passa **10 testes** e
   `checks/stage_j_pipe.rs`, **12 testes** (`rustc --edition 2021 --test <arquivo>`): F1
   (`f1_gain`/`f1_apply`), F2
   (`f2_apply`), F3, F4, gate de F5, `0x1220`/`0x11F0`/`0x1250`, one-pole de §8.2(b)
   (`008B68BC`..`008B6932`) e `dot16`/`dot32` bit-exatos.
   **`powf`/`logf`/`expf` não precisam de port**: são imports da UCRT (`checks/thunk_map.txt`:
   `0x1C9AA01→powf`, `0x1C9A9FB→logf`, `0x1C9A9D7→expf`) e `checks/j_crt_equiv.rs` provou
   **17.832.179** amostras com `bad=0` entre `f32::*` e os imports.
   **J2 fechado**: ordem de soma de `0x5F5C0` transcrita (`0005F68D`..`0005F6BE`, dois
   acumuladores de 8 lanes → `L` → `x2` → `x4` → `vaddss`) e conferida contra hardware
   AVX/FMA em **400.000** casos, `bad=0` (`checks/j_dot32_avx.rs`); vetores fixos
   `0x400068db`/`0x40b6c8b4` viram teste.
   **J3 fechado**: `checks/stage_j_pipe.rs` (12 testes) transcreve o descritor de `0x410 B`,
   o par de `0x18 B` do estagiador, o descritor de ring de `0x90 B` (`len = 0x10000`),
   `align16`, o avanço do ring e a ordem de `0x8AD2B0` (`chain_plan`, ramos `state+0x58`/
   `+0x52` + atalho `008ADC6B`→`008AE1C1`).
   **Correção de J3, material:** `g/2` da mistura é `nch != 2` (`008C2DB8`/`008C2DEA`);
   `nch == 2` usa `g` inteiro (`008C2D90`..`008C2DB4`). Spec §8.4.7 corrigida.
   Próximos incrementos: (i) **J4** FFT — **ordens 8..19 FECHADAS bit a bit em 2026-11-24**.
   Cadeia até o kernel fechada e medida (`checks/fft_probe.rs` e
   `checks/fft_generic_probe.rs`, read-only; `checks/stage_j_fft.rs` 7 testes;
   `checks/fft_golden.rs` 36 arrays). Kernel por ordem: 6→`0x8BFE0`, 7→`0x8C280`,
   8..19→`0x1D69E00`, >19→`0x88300` (`00072552`..`000725D6`). `checks/j4_fft.rs` tem
   `kernel6`/`kernel7`, os estágios genéricos de `0x1D69E00` (`kernel_stage1`, `pass2`,
   `stage16`/`pass3a_step`, `radix8_levels`, `radix8_final`, `radix4_final`, `kernel_generic`),
   o caminho `rdx > 0x800` (`kernel_large`, ordens 13..19) e o split `0x895C0` rápido e lento
   (`split_ccs_fast`/`split_ccs_slow`); **13 testes, todos verdes**:
   `orders_8_10_11_12_are_bit_exact` (KD/WS/FWD para as ordens 8, 9, 10, 11 e 12),
   `kernel9_workspace_matches` (512/512), `kernel9_is_bit_exact` (512/512),
   `order9_chain_is_bit_exact` (514/514) e impulse/cos/ramp de `checks/fft_golden.rs`; os
   goldens `j13..j19_stage_rand.bits` fecham `kernel_large` (dst e ws, `0` divergências) e
   `rfft_generic` fecha `FWD bad=0` nas ordens 13..19 (19 pelo split lento).
   **`0x1D69E00` é FFT complexa de `n/2` sobre pares intercalados** (medido: `2.8e-06` contra
   CFFT em f64; impulso `src[1]=1` → `KD[2k+1]=1`), ver plano §24.5-(4) e spec §19.6. O último
   defeito da ordem 9 era a semântica de `vunpcklpd`/`vunpckhpd` (palavras de 64 bits por lane)
   no modelo Python de validação. Ficam `NÃO EXTRAÍDO`: `0x88300` (ordem > 0x13, inalcançável —
   N ≤ 1115 → ordem 11; §24.5-(3)) e os geradores de twiddle (`0x806E0`, `0x876E0`, `0x87AA0`,
   tabelas medidas);
   (ii) **J5 fechado** — `checks/stage_j_chan.rs`, 7 testes: três descritores de ring de `0x90 B`
   (`out@0`/`A@0x90`/`B@0x120`), `len=0x10000`, `available`/`advance_read`/`advance_write`,
   ganho `(float)arg2/(float)arg3` (`008AD06B`..`008AD0B9`), `0x8BAA10`/`0x8BAB60`;
   (iii) **J6 fechado** — `checks/stage_j_engine.rs`, 8 testes: `0x8C3C20` (`a=0.1`),
   `0x8C0BD0`, `0x8B68AB`, `0x88E130`, `0x882FC0` e `0x8B5AF2`–`0x8B5CA7` na ordem exata
   `u·(y·v)`.

**Correção registrada:** `0x1C8500` (= `0x293760`) **é ln** — `ln 2` em `0x1ECAE40`
(`002939C7`/`00293A3B`/`00293D0D`) e série de `ln(1+x)` em `0x1ECAC20..0x1ECAE00`. O
`NÃO PROVADO` do agente K nesse item está errado.

## Ordem das etapas seguintes (folha vinculante: §23.15)

1. ~~**F**~~, ~~**G**~~, ~~**H**~~, ~~**K**~~, ~~**L**~~, ~~**M**~~, ~~**N**~~, ~~**O**~~,
   ~~**P**~~ — entregues (§23.15 balanço; verificação em `checks/verificacao_k_o.md` e
   `checks/p_extras.md`).
2. ~~**Pendências de verificação de K/L**~~ — fechadas em 2026-11-24 (`0x5F5C0`, `0x8C33D0`,
   `0x87BB60`; §23.15 “2ª rodada”).
3. ~~**I**~~ — **FECHADO 2026-11-24**: WAV do oráculo em `host/test/out_soothe3.wav`, host em
   `host/` (§15.3). Null-test tem de alinhar por **2304** e fixar o **mesmo bloco**; o plugin
   não é transparente no estado padrão.
4. ~~**J**~~ — **J1–J6 FECHADOS** em 2026-11-24: J1/J2 (`stage_j_core.rs`, 10 testes), J3
   (`stage_j_pipe.rs`, 12), J4 (`j4_fft.rs`, 13 — ordens 8..19 e split `0x895C0` rápido/lento
   bit a bit), J5 (`stage_j_chan.rs`, 7 — ring/ganho) e J6 (`stage_j_engine.rs`, 8 — detector,
   smoother, curvas, escalar `u·(y·v)`). `0x88300` e os geradores de twiddle ficam
   `NÃO EXTRAÍDO` (fora do áudio; §24.5-(3)). Próximo e único pendente: null-test plugin × port
   com o mesmo bloco e alinhamento 2304 — bloqueado até existir o port completo do motor.
5. ~~**J0**~~ — **FEITO 2026-11-25** (engenharia, sem prova nova): crate `port/`
   (`soultree_port`) é a fonte única dos kernels J1–J6; os `checks/*.rs` apontam para ele com
   `#[path]` e mantêm só os testes. `port/src/pending.rs` = 12 gaps com RVA e
   `blocks_null_test`; `port/src/chain.rs` = ordem de `pipe::chain_plan` e parada no primeiro
   gap (desde M4: `0x8B3ED0`, miolo `NÃO TRANSCRITO` = M5). Runner:
   `powershell -ExecutionPolicy Bypass -File port\run_tests.ps1` (10 suítes desde M3, com
   `checks/j_ln_exp_avx.rs`). Em 2026-11-25 (M3), todas verdes:
   - lib do port: 50 testes;
   - J1–J5: 10/12/7/13/7;
   - J6: 20;
   - M1: 17;
   - M2: 8;
   - M3: 6.

   Ressalva: o Windows App Control às vezes bloqueia um `.exe` recém-compilado
   (`os error 4551`). Quando bloqueia, rodar `rustc --test` com outro nome de saída.
   Extração
   reprodutível: `tools/extract_port_modules.py`. **Atenção:** no `-Slow`, `j_dot32_avx.rs` e
   `j_crt_equiv.rs` só têm `main` e o runner compila com `--test` ⇒ 0 testes executados
   (bug do runner, não corrigido).
   **Q (2026-11-25, FECHADO):** `0x8C1440` — `checks/q_8c1440_buffers.md` prova os papéis
   dos 16 buffers (pares 0/2/4/6 = `Σch²`; 1/3/5/7 = `Σch`, únicos clampados), as 4 divisões
   em **alocação nova** (`new1=par0/par1`, `T1=par2/par3`, `T2=par4/par5`, `T3=par6/par7`; o
   `den` de `T3` é o par 7 capturado em `xmm11`/`008C241B` antes do reaproveitamento do slot
   em `008C250E`), as somas `A/B/C/D` dos 2 canais, a lei
   `ch ← (1-g)·ch + g·D` com `D = Σch²/Σch`, e o mapa de coeficiente
   `enable→+0x2C`, `tipo 8/9→+0x30`, `tipo 6→+0x34`, `tipo 5 (sel 16..18)→+0x38`,
   `tipo 0xA→nunca`; `0x882FC0` não é chamado. Resta só `NÃO PROVADO` o nome/unidade dos 4
   coeficientes, a faixa de `g`, a intenção musical e `nch > 2`.
   **Q-port (2026-11-25, FEITO):** `port/src/stage.rs` transcreve `0x8C1440` inteiro
   (passagem A com `0x1580` FMA / `0x1370`, clamp `0x1100` modo 0 nos pares ímpares, as 4
   divisões, as somas `A/B/C/D` e a passagem B via `pipe::mix_lane`, cujo MAC foi corrigido
   para FMA — `00005C85`) com 12 testes. O gap de
   `0x8C1440` saiu de `pending.rs`.
   **M1 (2026-11-25, FECHADA):** divisão `0x1550 -> 0x63640` em `port/src/div.rs` (despacho
   cabeça 8 / laço 16 / bloco 8 / resto 1..7, aritméticas A/B, fixup; máscara do recíproco
   nulo **diferente** em A e B, `00063779` vs `00063AF8`/`00063B0E`), usada pelas 4 divisões
   de `stage.rs`; conferida contra a sequência AVX/FMA do binário em `checks/j_div_avx.rs`
   (2.807.920 lanes, `bad=0`). `n` a 48 kHz = **257** (`N = 256`, `0086FF39` com
   `arg5 = 0x100` em `0086A579`) → 16 laços B + 1 lane A. `dst & 0x1c = 0` nos 4 sítios
   (cursor `align16` em `0x8C1440`; base `[E+0x30]` de `0x868B50`, 64 B) → sem cabeça.
   Os 2 testes que falhavam em `div.rs` estavam errados (o laço de 16 conta `n − h`;
   `vrcpps(f32::MAX) = 0`). Resíduo `NÃO PROVADO` (gap em `pending.rs`): `E` de `0x864410` =
   objeto de `0x8634A0`; `a` = taxa (M4); gêmeo `0x8C5C40`; payload de NaN; `vrcpps` só é
   bit a bit na mesma CPU do oráculo. Prova: `checks/r_divisao_63640.md` §2/§4.1/§5/§6.
   **M2 (2026-11-25, FECHADA):** recíproco de `0x88E130` (`0088E32F`, in-place)
   `0x1C8530 -> 0x1C8AC0 -> [0x21C71D8] = 0x29B260` (1.856 B) em `port/src/rcp.rs`, usado por
   `engine.rs::shelf_curve_in_place`. Lane normal (`|bits| ∈ [0x00800000, 0x7E7FE800]`):
   `vrcpps` + `e = 1 − x·r0`, `r = e·r0 + r0` (FMA, `0029B40E`/`0029B442`/`0029B456`); lane
   especial: `1.0f/x` por `vdivss` (`0x29B9A0`); blocos de 32 + cauda de 8 com padding `0.75`,
   sem cabeça (valor por lane independe de `n`/alinhamento); MXCSR forçado a `0x1F80`.
   `checks/j_rcp_avx.rs` (constantes lidas do dump): `bad = 0` estrito (com payload de NaN) e
   **exaustivo 2^32 `bad = 0`**; 3 mutações detectadas. Resíduo `NÃO PROVADO`: `vrcpps` só na
   mesma CPU; caminhos de CPU `0x297EE0`/`0x299C60` não lidos; outros chamadores de `0x1C8530`
   não religados. Prova: `checks/s_reciproco_88e130.md`.
   **PRÓXIMO — roteiro até o null-test (2026-11-25):**
   ~~**M1**~~, ~~**M2**~~ (fechadas acima).
   ~~**M3**~~ **(2026-11-25, FECHADA):** ln `0x293760` (+ escalar `0x293F80`, f64, tabela
   `0x1ECAF60` de 65 entradas) e exp `0x240C00` (+ escalar `0x2414C0`) da IPP, em
   `port/src/ippmath.rs`, usados por `engine.rs::ipp_ln`/`ipp_exp`.
   - Prova: `checks/j_ln_exp_avx.rs` (emulador AVX2/FMA com constantes do dump).
   - **Exaustivo 2^32: `bad = 0`** no ln e no exp.
   - Sem `vrcpps`, então o resultado não depende da CPU.
   - A IPP **difere** de `f32::ln`/`f32::exp` (~9×10^7 entradas cada), então as curvas de
     `0x88E130` mudaram de bits.
   - Resíduo: os caminhos de CPU `0..3` não foram lidos; falta conferir que os chamadores
     ignoram o `eax` (M5).
   - Doc: `checks/t_ln_exp_ipp.md`.

   ~~**M4**~~ **(2026-11-25, FECHADA):** `checks/u_estado_m4.md`.
   - `a` = taxa do host em `[eng+0x28]`, e `k = max(1, trunc((a+1)/44100))`.
   - Há dois ctx, construídos por `0x873440`:
     - **A** em `eng+0x5ED8`: `N = 2048`, gate `1`;
     - **B** em `eng+0x8B20`: `N = 256`, gate `0`.
   - `[ctx+0x20] = max(a/k, 44100)`.
   - `[ctx+0x60] = N/2` (`008769D4`), então o divisor de `0x8B68AB` é 1024 e **não** é
     sample rate.
   - Medido 32k..192k pelo host com `SOULTREE_PROBE=1` (somente-leitura): **N não muda com fs**.
   - `E` de `0x864410` = `[handle]` = objeto de `0x8634A0`.
   - `[rdx+0x50]` = callback norm→plain da entrada `0x238E9C0 + i·0x68`, em 6 famílias,
     transcritas em `port/src/params.rs` + `param_entries.rs`. O P2 tinha errado a base em
     `0x10`.
   - Resíduo: o elo host→create (ofuscado) está provado só por medição; a conferência dos
     callbacks valor a valor fica para M6.

   **M5 (PRÓXIMO)** port do miolo `0x8B3ED0` (F1–F5 + 6 callees +
   satélites + filtro `0x87BB60`). **M6** cadeia completa (`0x8AD2B0`, `0x8ACC40`,
   `0x885040`/`0x8875F0`, rings, estado inicial). **M7** null-test (bloco 512, alinhamento
   2304, 0 divergências).
   **Fatos novos (2026-11-25):** `0x63640` tem **duas** aritméticas (A = quociente, B =
   recíproco; A ≠ B no ULP) e `n = N+1` é **ímpar** — a cauda sempre roda. **Conflito com a
   âncora:** a instrução dá `N = 256` a 48 kHz para o `X` do estágio, não 278 (§23.14).

## Armadilhas já pagas (não repita)

- **`functions.csv` mente no núcleo.** Tamanhos são de `.pdata` e a função é partida por
  `UNW_FLAG_CHAININFO`. `0x8B3ED0` aparece com **49 B** e tem **20.209 B**. Use
  `tools/show_func.py` / `tools/scan_region.py`, nunca o CSV sozinho.
- **RVA de 5 dígitos não é o cluster.** `0x8B660` = 570.976 é a região da **IPP/matemática**
  (`0x08xxxx`); o DSP está em `0x8B0000–0x8D2000` (~9 MB). Conte os dígitos.
- **O gêmeo começa em `0x8C5C40`**, não em `0x8C5FD8` (fragmento do meio). Corpo idêntico ao
  núcleo: 20.209 B, 4.473 instruções, 127 `call`.
- **`xrefs.csv` é latin1**, não UTF-8. Abra com `encoding='latin1'`.
- **`reach_kernels.py` está descartado**: o grafo de `xrefs.csv` não captura call indireto.
- **`find_kernels.py` subconta** no núcleo (usa tamanho do CSV). Use `scan_region.py`.
- **`ida_auto.auto_wait()` nunca retorna** nesta imagem de 137 MB. Use
  `ida_auto.plan_and_wait(start, end)`. `run_batch.ps1` já abre o `.i64` certo.
- **`decompile_batch.py` grava `ida_%08X.c`.** Não mude para `%08X.c`: colide com o Ghidra.
- **Contar `mulss` NÃO dá o número de taps.** `0x8B2C30` tem 27 `mulss` e é FIR de **32**
  taps; o número vem da máscara `0x1f`, não da contagem.
- **As "primitivas" `0x1010/0x10A0/0x10D0/0x1220/0x1280/0x15E0` são stubs de dispatch do
  IPP** (`IPPCODE`/`IPPDATA`); o corpo é `tabela[4]`. Não tratá-las como código do plugin.
- **Ponteiro de dado no dump é VA na base `0x199B0000`**, não `0x180000000`.
  `RVA = VA − 0x199B0000` antes de comparar com endereço do IDA.
- **Latência 2.304 amostras @48 kHz é do build 1.0.5**, não do dump 1.0.6.
- **`N = 256/278/557` é uma fórmula**, não três constantes: `round(256 × fs / 44100)`.
  A instrução que escolhe o N ainda não foi lida → `NÃO PROVADO`.
- **Zero FMA em `0x8A0000–0x8E0000`.** Se aparecer FMA na sua leitura, é outra região/binário.
- **Não usar os scripts `frida_*.py` de `archive/agent2/temp_scripts/`** — são hook/attach,
  proibidos pela regra anti-tamper.
- **Não medir nada em `archive/agent2/oracle_bundle_1.0.5/`**: é v1.0.5, o dump é v1.0.6.
- **Não confundir decompilado com prova.** Prova é a instrução, com RVA.

## Como registrar o resultado

- Cada etapa concluída → atualizar a seção correspondente do `PLANO_MOTOR_AUDIO.md` (§23.x) e,
  se houver prova, a seção da `dsp-spec.md`.
- Toda afirmação técnica leva o RVA. Sem RVA, é leitura, e deve ser rotulada como tal.
- Ao terminar uma etapa, deixe a próxima marcada com **PRÓXIMO** no §23.12 e atualize o §25.
- Não invente seções novas no `dsp-spec.md` fora da numeração existente.

## Definição de pronto para esta retomada

A retomada está bem-sucedida quando: (a) os documentos estiverem sincronizados entre si
(`PLANO_MOTOR_AUDIO.md`, este prompt, `PROMPT_RETOMADA_4000.md`, `dsp-spec.md`);
(b) J1–J6 compilarem e passarem (`j4_fft.rs` 13, `stage_j_core.rs` 10, `stage_j_pipe.rs` 12,
`stage_j_fft.rs` 7, `stage_j_chan.rs` 7, `stage_j_engine.rs` 8) — verificado por
`powershell -File port\run_tests.ps1`, que também roda os 36 testes do crate `port/` e os 17 de
`checks/j_div_avx.rs`; (c) `0x88300` e os geradores
de twiddle estiverem marcados `NÃO EXTRAÍDO` com RVA e alcance provado; (d) o que resta para o
null-test estiver explícito (port completo do motor, mesmo bloco, alinhamento 2304).

K fechou em 2026-11-24 (§23.15, `checks/verificacao_k_o.md`): as 5 faixas de `0x8B3ED0`,
satélites, `0x1400` (dot) e §23.15/§25/spec atualizados.

G fechou em 2026-11-23 (§23.8, spec §8.3.1): escritor único `0x867D80`, `state = engine+0x54`,
mapa **143 índices → offset** com store provado, índice = `+0x10` da tabela `0x238E9B0`.
H fechou em 2026-11-23 (§23.9, spec §8.2/§8.4): dinâmica inline em 4 blocos, detector,
smoother, MAC, estagiador+mistura, curvas `A^(1−σ)`. F e a math do design (`0x882DE0`,
`0x1C8500`=ln, `0x1C84A0`=exp) também estão fechadas — não reabrir sem instrução nova.
