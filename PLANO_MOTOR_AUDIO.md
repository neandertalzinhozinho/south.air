# Plano — Extração do motor de áudio do soothe3

**Projeto:** Resonia (`D:\PROJETOS\soultree`)
**Alvo:** `dumpsooth\nyx_soothe3_dump.bin` (imagem descriptografada)
**Atualizado:** 2026-11-22 (revisão 3 — âncora do objetivo; §22 leitura do cluster; ordem do §20 reescrita)

> **Âncora do projeto:** `LEMBRAR DISSO.md` (arquivo permanente, não se altera).
> Se este plano divergir dele em qualquer ponto, o `LEMBRAR DISSO.md` vence.
> Integridade da âncora: SHA-256 `D10EB333C140FC4800B06C6CA234171B62EDA7348872E33C88BDA378B7BECE49`
> (`Get-FileHash "LEMBRAR DISSO.md" -Algorithm SHA256`). Se o hash mudar, o arquivo foi
> alterado — volte a este valor antes de confiar nele.

---

## 0. Objetivo e fonte de dados — leia antes de tudo

**Objetivo:** extrair o motor de áudio DSP do soothe3 a partir do dump e colocar esse
mesmo motor dentro do **Resonia (VST3)** — mesma aritmética, mesma ordem, mesmos
coeficientes.

**A extração é 100% estática e sai do dump.** O caminho é este, e não outro:

```
dumpsooth\nyx_soothe3_dump.bin     137.003.008 B   <- FONTE DE VERDADE
        │  tools/normalize_dump.py
        ▼
dumpsooth\soothe3_unpacked.dll     137.003.008 B   <- PE válido, 19 seções
        │  ImageBase = 0x180000000, .pdata = 30.859 funções
        ▼
        IDA 9.3  ->  docs/engine/decomp/ida_*.c
        ▼
   RVA + instrução  ->  docs/engine/dsp-spec.md  ->  Rust no Resonia
```

| Papel | Arquivo | Serve para extrair? |
|---|---|---|
| Fonte de verdade | `dumpsooth/nyx_soothe3_dump.bin` | **sim** (SHA-256 `68D30368…4F55C`) |
| O que o IDA abre | `dumpsooth/soothe3_unpacked.dll` | **sim** — é o dump já como PE |
| Plugin original em disco | `original/soothe3.vst3` (47.500.552 B) | **NÃO** — `.text` 100% cifrado |

**O plugin original não é fonte de extração.** Verificado página a página: `7.382` de
`7.382` páginas de `.text` diferem do dump. As seções têm os mesmos nomes (`.text`,
`IPPCODE`, `IPPDATA`, `.data`, `.pdata`, `.oldrel`, `.proxy`, `.guard`), mas o conteúdo é
cifrado e só existe em claro depois que o loader dele decifra em memória — que é
exatamente o que o dump já contém. Ele serve, no máximo, como **caixa-preta que toca
áudio** (referência para o null-test da Fase 4), nunca como fonte de coeficiente.

---

## 1. Diretriz

> **"Eu não quero nada estimado, nada heurístico. Eu quero o DSP — somente o DSP —
> extraído do dump. O motor DSP de áudio."**

### Entrega só conta com os 5 itens

1. Endereço da função no dump.
2. Pseudocódigo/desmontagem comentada dessa função.
3. Constantes lidas do dump, com o RVA.
4. Estruturas de dados com offsets comprovados.
5. Código Rust com **a mesma aritmética, na mesma ordem**, com os mesmos coeficientes.

### Proibido

| Proibido | Exemplo |
|---|---|
| Estimar tamanho de FFT | `1024/2048/4096/8192` em `stft.rs` |
| Inventar nome de opção | `Eco/Normal/High/Extreme` (não existem no dump) |
| "Algoritmo equivalente" | portar "algo tipo PFFFT" |
| Ajustar até o null-test bater | tuning empírico |
| Inferir fórmula pelo nome do parâmetro | `detect.rs`, `curve.rs`, `envelope.rs` atuais |
| Chamar indício de prova | "FFT = FFTPACK PROVADO" só pela licença no `.rdata` |

**Consequência:** o `app/src/dsp/*` que existia era heurístico e **não era entrega**. Foi
perdido junto com `app/` (§19.5). O que entrar no lugar tem que ser o código extraído —
não uma versão ajustada dele.

---

## 2. Estado atual

| Fase | Estado | Evidência |
|---|---|---|
| 0 — Normalizar dump | **CONCLUÍDA** | `tools/normalize_dump.py` → `dumpsooth/soothe3_unpacked.dll` (137.003.008 B) |
| 1 — Mapa de funções/params/RTTI | **CONCLUÍDA** | `docs/engine/functions.csv` (30.859), `params.csv` (143), `rtti_classes.csv` (2.743 TypeDescriptors → 1.942 vtables) |
| 2 — Caminho de áudio | **CONCLUÍDA** | cadeia real provada em execução; vtable `0x2037A58` **não** é o áudio |
| 3 — Especificação do DSP | **EM ANDAMENTO** | provados: N=256, janela Hann, **FFT fora do áudio**, núcleo `0x8B3ED0` = 20.209 B (ver §14), ordem do pipeline (§14.2), IPP de vetor (§14.3), **núcleo é orquestrador + cluster aritmético `0x8BF5C0–0x8C4300`** (§15), **1ª função do cluster fechada: `0x8C3C20`** (§16.1), **camada vetorial resolvida por opcode — 33 primitivas, 45 chamadas no núcleo** (§17), **IDA consertado: 12 das 13 funções do cluster + o gêmeo `0x8C5FD8` decompilados** (§19). **Falta**: ler o decompilado, tipo de filtro por banda, detector, e onde a lei de ganho entra |
| 4 — Oráculo | **WAV GRAVADO (2026-11-24)** | Host reconstruído em `host/` (Rust std-only, FFI crua, sem injeção/hook). 48 kHz/bloco 512: 48.000 frames, 94 blocos `S_OK`, latência **2304**, determinístico (SHA-256 `1218C801…E67B`, reproduzido). WAV em `host/test/out_soothe3.wav`. **O plugin não é transparente no estado padrão** (RMS da diferença alinhada: −6,6 dBFS) e **a saída muda com o tamanho do bloco** — o null-test tem de fixar o bloco e comparar plugin × reconstrução |
| 5 — Port Rust | **AUSENTE DO DIRETÓRIO** | `app/src/` não existe mais (§19.5). O port heurístico citado nas revisões anteriores foi perdido junto com `app/`, `checks/` e o resto |
| 6 — Integração/build | **AUSENTE** | `app/dist/Resonia.vst3` sumiu com `app/` (§19.5). Nada a validar agora |

---

## 3. Fatos provados sobre o dump

| Item | Valor |
|---|---|
| Tamanho | 137.003.008 B = `0x82A8000` (= `SizeOfImage`) |
| SHA-256 | `68d30368936c738490f10a852304a5e67b7b4fdd563f62513c5a5bc81034f55c` |
| Formato | PE32+ x86-64; header diz `0x180000000`, **base real `0x199B0000`** |
| Layout | **plano: offset do arquivo == RVA** (header mente nos `PointerToRawData`) |
| Entry point | `0x79CDEA0` (`.text001`, stub do protetor) |
| Export DLL | `soothe3.vst3` |
| Exports | 236: 231 `?dvs_*_mfort6317_` + `GetPluginFactory` `0x327A50` + `InitDll`/`ExitDll` `0x325960` + `aani_GetDescription` `0x862E30` |
| Imports | loader + UCRT via API sets (`api-ms-win-crt-*`), resolvidos em IAT de runtime |
| `.pdata` | 30.859 `RUNTIME_FUNCTION` exatos, cobrindo `0x1CFB871` B |
| RTTI | `.?AVSoothe3AudioProcessor@@` (vtable `0x2037A58`, COL `0x2095B50`) |
| Protetor | **Themida/WinLicense** (`.proxy`, `.guard`, `.reloc64`, `.oldrel`, `?dvs_*_mfort6317_`) |
| Licenciamento | PACE/iLok, camada separada (`.?AVILok2Commander@pace@@`) |

### Seções

| Seção | RVA | VSize | Papel |
|---|---|---|---|
| `.text` | `0x1000` | `0x1CD5487` | código **descriptografado** (entropia 6.545) |
| `IPPCODE` | `0x1CD7000` | `0xB4B7D` | Intel IPP estático |
| `.rdata` | `0x1D8C000` | `0x3F2D38` | strings, tabelas, RTTI |
| `.data` | `0x217F000` | `0x5D8DD8` | params, RTTI, estado |
| `.pdata` | `0x2758000` | `0x5A684` | 30.859 entradas |
| `.text001` | `0x79CD000` | `0x125A` | entrada do protetor |
| `.proxy` / `.guard` | `0x79D6000` / `0x7B82000` | — | runtime Themida (`.guard` entropia 7.226) |

### Prova de que o dump é a imagem viva

```
.text sha256 no dump : af39001e804969f2
.text sha256 na RAM  : af39001e804969f2   (FL64 PID 23792, base 0x197D0000)
entropia .text       : 6.545 (dump) = 6.545 (RAM)   [no disco: 8.000]
```

**Não é preciso "vencer" o Themida para extrair o DSP.** A imagem já está descriptografada;
só não se pode escrever no processo.

### Parâmetros

Tabela em `.data` `0x238E9B0`, passo `0x68`, nome inline em `+0x14`, `max` em `+0x40`,
`default` em `+0x48`, flags em `+0x50` → **143 parâmetros** legíveis.

---

## 4. Anti-tamper (regra operacional)

O SecureEngine faz **checksum das páginas de código**. `Interceptor.attach` grava o
trampolim `FF 25 00 00 00 00 <addr64>` no prólogo → checksum falha → o plugin exibe
`soothe3 cannot run because it is corrupted` e derruba o host.

Não é detecção de licença nem de injeção: a injeção **funcionou** (37 hooks, contadores
subindo). É checksum de bytes.

| Método | Escreve no alvo? | Uso |
|---|---|---|
| Análise estática do dump | não | **principal** |
| `ReadProcessMemory` | não | **permitido** |
| Amostragem de pilha (`SuspendThread` + `.pdata`) | não | permitido |
| ETW/WPR sampling | não | permitido |
| Intel PT | não | permitido (setup pesado) |
| Breakpoint de hardware (DR0–DR7) | não (só registradores) | risco médio |
| **Hook inline (Frida)** | **sim** | **proibido** |
| Patchear o checksum no `.guard` | sim | proibido |

---

## 5. Caminho de áudio (PROVADO)

Capturado em execução real (`FL64.exe` PID 23792, base `0x197D0000`,
objeto `Soothe3AudioProcessor` em `0x1041A540`, vptr `0x1B807A58`).

Contagens em ~30 s de áudio (37 hooks, 0 falhas de instalação):

```
0x7D9550 = 18401    0x1D69E00 = 3504    0x196B1B0 = 48
0x9BA0   = 7        0x6CE80   = 6       0x86161E  = 4
todos os slots da vtable 0x2037A58 (incl. 0x350F20, 0x34F970) = 0
```

**Conclusão:** `0x350F20` e `0x34F970` são stubs de proteção e **nunca** rodam no áudio.
A vtable `0x2037A58` não é o caminho de processamento.

### Cadeia real

```
0x8646A2  (12.686 B)  topo — chamado indiretamente (0 refs diretas)
  └─ 0x8677F0  ( 1.043 B)  escalonador
       └─ 0x8774A0  (  135 B)  lambda/tarefa por canal
            └─ 0x881050  (  969 B)  aloca buffers alinhados a 16 floats
                 └─ 0x889BB0  (4.720 B)
                      └─ 0x899940  (2.388 B)
                           └─ 0x8ACC40  (1.634 B)
                                └─ 0x8AD2B0  (5.021 B)
                                     └─ 0x8B3ED0  (20.209 B)  núcleo
```

> Tamanhos conferidos com unwind encadeado do `.pdata` — ver §14.1. `0x8ACC40` e
> `0x8AD2B0` estavam subestimados aqui e foram corrigidos.

`0x88AC75`, `0x8999AE`, `0x8ACCAE`, `0x8B4268` e `0x86161E` **não têm chamada direta**:
aparecem como RVA de 32 bits em tabelas de descritores (`0x278B0xx`, `0x2128Dxx`,
`0x21292xx`, `0x21296xx`) — despacho por tabela.

`0x7D9550` **não é DSP**: é wrapper de filas (incrementa `[rcx+0x10]` em 4, chama slots
`+0x50`, `+0x70`, `+0x78`, `+0x180`, faz `Release` em `+8`).

### Escalonador `0x8677F0`

Lê o global `DAT_1826B1818`: `4` → `0x8774A0`; `1` → `0x881740`.

Ring buffer em `ctx + 0xBFF8`:

```
+0xC078  write index
+0xC07C  read  index
+0xC080  mask (potência de 2)
+0xC084  count
```

Multi-canal passa por `0x86AE00` e `0x86CFF0`.

### Tarefa `0x8774A0`

```c
struct job { char *flag; int *out; char *ctx; u64 a3,a4,a5,a6; };
if (*flag == 0) { *out = f(ctx + 0x5F8);  FUN_180881050(ctx + 0x5F8,  a3,a4,a5,a6); }
else            { *out = 0;               FUN_180880640(ctx + 0x5ED0, a3,a4,a5,a6); }
```

`0x880640` é o caminho alternativo (bypass/delta), 1.177 B.

---

## 6. FFT (PROVADO)

`FUN_180072480(undefined8, float*, plan*, ulonglong)`:

- `plan + 0x04` = `log2(N)`
- `plan + 0x08` = tipo
- `plan + 0x10`, `+0x18`, `+0x30`, `+0x38`, `+0x50` = tabelas/parâmetros

Despacho por tabela de ponteiros absolutos (base `0x199B0000`):

```
0x1DFA2C8 / 0x1DFA2F8 / 0x1DFA320 / 0x1DFA358
kernels: 0x20C00 0x20C20 0x20C60 0x899C0 0x89AC0 0x89DC0 0x101A0
         0x21920 0x21940 0x8A5E0 0x8A6C0 0x8A980 0x22500 0x22520 ...
```

`N >= 2^8` → `FUN_181D69E00` (IPP, AVX, checagem de alinhamento de 32 bytes).

Pós-processamento de FFT real (truque DC/Nyquist), transcrito:

```c
fVar1 = *param_2;
*param_2   = param_2[1] + fVar1;   // DC
param_2[1] = fVar1 - param_2[1];   // Nyquist
FUN_1800895C0(param_2, iVar4, 1, *(param_3 + 0x50));
...
param_2[lVar2]     = param_2[1];
param_2[lVar2 + 1] = 0.0;
param_2[1]         = 0.0;
```

---

## 7. Núcleo `0x8B3ED0`

### Constantes (RVA → valor)

```
0x2077680  0.0479208529
0x2077700  0.999981046
0x2077740  3.64401984e-08
0x2077800  0.135227725
0x2077840  1.59999971e-07
0x2079CEC  1.00000001e-07
0x2079CF8  9.99999975e-06
0x2079D24  0.00100000005
0x2079D48  0.00999999978
0x2079DB0  0.100000001
0x2079E08  1e-07            (double)
0x2079E54  0.333000004      (1/3)
0x2079EA8  0.5
0x2079F38  0.800000012
0x2079F48  0.001            (double)
0x2079F9C  1
0x2079FC0  1.09961283
0x207A00C  1.38629436       (ln 4)
0x207A030  0.1              (double)
0x207A138  1                (double)
0x207A188  2
0x207A1D0  2.30258512       (ln 10)
0x207A2D8  5.00000048
0x207A560  500
0x207A6AC  -1.09961283
0x207A6D4  -2.30258512      (-ln 10)
```

### Fórmulas (transcritas do decompilado)

Joelho suave + curva de potência (`808B3ED0.c`, linhas 4067–4105):

```c
t = clamp((x - 0.8f) * 5.0f, 0.0f, 1.0f);
e = expf(t * 1.38629436f);                  // 4^t
p = powf(e, k);                             // 2 argumentos
y = (logf(p + 0.1f) + 2.30258512f) * m - 2.30258512f;
z = expf(y);
```

Variante com `1.09961283` (linha 3345):

```c
y2 = (logf((2.0f - v*v) + 0.333000004f) + 1.09961283f) * m - 1.09961283f;
z2 = expf(y2);
```

### Funções de math (aridade/uso provados)

```
0x1C9A9D7  1 argumento, usado como exp(x * ln4)    -> expf
0x1C9A9FB  1 argumento                             -> logf
0x1C9AA01  2 argumentos (xmm0 base, xmm1 expoente) -> powf
```

Thunks `jmp [IAT]` da UCRT (`api-ms-win-crt-math-l1-1-0.dll`, string em `0x217A81E`);
IAT de runtime na região `0x1D8D7xx`.

---

## 8. O que falta

1. **Pipeline por banda** no **cluster `0x8BF5C0–0x8C4300`** (+ `0x8C5FD8`) e em
   `0x8B9E40` / `0x8B8E70` / `0x8BA1B0`: detecção de ressonância, suavização temporal,
   suavização em frequência, lei de ganho final. *`0x8B3ED0` só orquestra (§15.1).*
2. **Tipo de filtro por banda** (`0x879CF0`, `0x87E220`, `0x87B2A0`). *N e janela já estão
   provados (§13.1/§13.2); falta como o filtro é construído.*
3. **Struct de estado**: `ctx + 0x2C38`, `ctx + 0xBFF8`, `ctx + 0x5F8`, `ctx + 0x5ED0`
   com offsets provados campo a campo.
4. **Mapeamento dos 143 parâmetros** para os campos de estado.
5. **Port Rust** substituindo `app/src/dsp/*`.

Nada disso exige tocar no FL Studio: é estático no dump já provado íntegro.

---

## 9. Próximo passo

Reordenado em 2026-11-22 depois de fechar a ferramenta (§19). A ordem agora é a do §20;
este item fica como índice.

1. ~~**Semântica dos thunks vetoriais**~~ — **FEITO** (§17). Artefatos originais
   (`checks/vector_primitives.txt`, `checks/core_vector_calls.txt`) **sumiram do
   diretório** (§19.5); `tools/vector_primitives.py` e `tools/core_vector_calls.py`
   regeneram.
2. ~~**IDA não decompila o cluster**~~ — **FEITO** (§19). 12 das 13 funções do cluster e o
   gêmeo `0x8C5FD8` (116.125 caracteres) estão em `docs/engine/decomp/ida_*.c`.
3. ~~**Ler o cluster pelo decompilado do IDA**~~ — **FEITO 2026-11-23/24**: `0x8C1440`
   (H), `0x8C0BD0` (H), `0x8BF650`/`0x8BFD30` (H), `0x8C02F0` (H); cada linha com RVA.
4. **Oráculo**: **FEITO 2026-11-24** — host reconstruído em `host/`, WAV gravado em
   `host/test/out_soothe3.wav` (§15.3). Restrições medidas: alinhar por 2304 e fixar o
   mesmo bloco nos dois lados. Sem isso não existe null-test; com isso, existe.
5. ~~**Identificar o tipo de filtro**~~ — **FEITO 2026-11-24** (L): `0x87BB60` é
   multiplicação de curva de ganho no domínio espectral, sem recursão (23 ops float). `0x87E220`
   segue `A CONFERIR` (clamp `[10^−4.8, 10^2.4]` citado pelo agente).
6. **Struct de estado** (`ctx+0x2C38`, `+0xBFF8`, `+0x5F8`, `+0x5ED0`) + mapa dos 143 params —
   **PARCIAL**: `+0x5F8`/`+0x5ED0` fechados (`checks/p_extras.md`); mapa de 143 params não é
   extração de DSP e não entra no port.
7. ~~**Transcrever para `docs/engine/dsp-spec.md`**~~ — **FEITO** (§8.2/§8.3/§8.4/§19 por
   etapa; segunda rodada sincronizada em 2026-11-24).
8. **Reescrever o port Rust** a partir do extraído (não há `app/` — §19.5) — **INICIADO
   2026-11-24**: `checks/stage_j_core.rs` **10 testes** + `checks/stage_j_pipe.rs` **12
   testes**; J2 (ordem de soma) e J3 (descritores/ordem) fechados.
9. Validação **somente leitura**.

---

## 10. Ferramentas

| Ferramenta | Caminho | Uso |
|---|---|---|
| Ghidra 12.2 | `D:\TOOLS\ghidra_12.2_PUBLIC` | **confirmado instalado em 2026-11-22** (`ghidraRun.bat`, `support\analyzeHeadless.bat`); scripts em `tools/ghidra/` |
| IDA Pro 9.3 + Hex-Rays | `D:\TOOLS\IDA` | **funciona** — ver a receita do §19.2. Abrir sempre o **PE normalizado**, nunca o dump cru |
| REA (MCP) | sessão | `analyze_function`, `batch_decompile`, `get_call_graph`, etc. |
| Frida (REA) | sessão | **apenas leitura**; hook inline proibido |

Scripts próprios: `tools/normalize_dump.py`, `re_lib.py`, `rtti_scan.py`, `rtti_name.py`,
`vtable_dump.py`, `xref_scan.py`, `func_summary.py`, `live_probe.py`, `find_instance.py`,
`find_soothe_pid.py`.

Adicionados em 2026-11-22 (leitura do núcleo):

| Script | Para quê |
|---|---|
| `tools/thunk_map.py` | resolve thunk → nome de import (372 entradas, regra do §14.5) |
| `tools/dispatch.py` | resolve thunk de dispatch IPP → implementação escolhida |
| `tools/ipp_ident.py` | classifica a implementação por instruções vetoriais |
| `tools/imports_dump.py` | despeja descritores/int/iat e valida o pareamento |
| `tools/float_density.py` | ranking de densidade de ops float (acha onde está a aritmética) |
| `tools/find_kernels.py` | ranking de densidade aritmética em **todas** as 30.859 funções — usa o tamanho do `.pdata`; para o núcleo isso subconta (§22.5) |
| `tools/scan_region.py <lo> <hi> [n]` | **o correto para o núcleo**: varre uma janela de RVA chain-aware (segue `UNW_FLAG_CHAININFO`), deduplica instrução por endereço e conta `mulss`/`addss`/`subss`/`divss`/FMA por função. Foi o que achou `0x8B2C30` |
| `tools/reach_kernels.py` | **DESCARTADO** — BFS sobre `xrefs.csv` alcança 98 funções do núcleo e 1 com aritmética: o grafo não captura call indireto (§22.5) |
| `tools/show_func.py <rva>` | desmontagem *chain-aware* de uma função, com RVA e o valor das constantes RIP |
| `tools/ida/decompile_batch.py` + `tools/ida/batch_list.txt` | decompila uma lista de RVAs para `docs/engine/decomp/ida_XXXXXXXX.c` |
| `tools/ida/run_batch.ps1` | dispara o batch no `idat.exe` e mata o processo quando o relatório aparece |

---

## 11. Arquivos relevantes

| Caminho | Conteúdo |
|---|---|
| `dumpsooth/nyx_soothe3_dump.bin` | dump original (plano) |
| `dumpsooth/soothe3_unpacked.dll` | PE normalizado — **é este que o IDA abre** (§19.2) |
| `dumpsooth/soothe3_loadable.dll` | cópia de trabalho para `live_probe` (`tools/make_loadable.py`) — dump repachado para a base real `0x199B0000`, reloc limpo, `GetPluginFactory`/`InitDll`/`ExitDll` exportados. **Mas `LoadLibraryW` morre com `0xC0000005` dentro do DllMain** (§19.7) |
| `original/soothe3.vst3` | **plugin original empacotado** (47.500.552 B, PE64 x64, 19 seções, v1.0.6, SHA-256 `15B87B2F…AC9A0C`). Recuperado de `D:\PROJETOS\vst3dec\originalutil\` em 2026-11-22. **Não é fonte de extração** — `.text` cifrado (§0). Serve só como caixa-preta para gerar áudio de referência (§20 passo 7) |
| `docs/engine/functions.csv` | 30.859 funções |
| `docs/engine/params.csv` | 143 parâmetros |
| `docs/engine/rtti_classes.csv` | 2.743 classes + vtables |
| `docs/engine/xrefs.csv` | grafo de referências usado no BFS do §13.3 |
| `docs/engine/phase2-notes.md` | notas da fase 2 |
| `docs/engine/decomp/` | descompilados: `808B3ED0.c` etc. (Ghidra) + `ida_XXXXXXXX.c` (IDA 9.3, §19.3) |
| `checks/ida_cluster.txt` | resultado do lote IDA do cluster (§19.3) |
| `checks/ida_extra.txt` | `0x8C33D0` (falhou) e `0x8C5FD8` (116.125 car.) |
| `docs/engine/dsp-spec.md` | especificação (parcial; tudo não provado = `NÃO EXTRAÍDO`). **Atrás do plano** — ver §21 |
| `tools/` | scripts de leitura (ver §10) |

> **`checks/*` antigos não existem mais** (§19.5). `thunk_map.txt`, `imports_dump.txt`,
> `math_imports.txt`, `vector_primitives.txt`, `core_vector_calls.txt`, `_8b3ed0.dis` e
> os demais foram perdidos com o resto do diretório. Os geradores estão em `tools/`;
> `tools/thunk_map.py`, `tools/imports_dump.py`, `tools/vector_primitives.py` e
> `tools/core_vector_calls.py` regeneram cada um.

---

## 12. Plano de ataque e decisões (2026-11-22)

### 12.1 Decisões fechadas

| Item | Decisão | Base |
|---|---|---|
| Caminho inicial | **estéreo (2 canais)** | default de DAW; menor superfície; surround/8ch depois |
| Qualidade | **índice 0** (default) | `params.csv`: Quality `max=2`, **`default=0`** |
| Fase | **minimum phase** | `params.csv`: Linear phase `max=1`, **`default=0`** |
| Low latency | **off** | `params.csv`: `default=0` |
| Meta beta | **tolerância** (a definir; alvo inicial ≤ −120 dB RMS) | decisão do usuário |
| Meta final | **bit-exact** | decisão do usuário |

Consequência: o primeiro alvo é o caminho que o plugin usa **por default**. Nada de
escolher modo "melhor" por gosto — é o que o original executa sem o usuário mexer.

### 12.2 O que falta para conquistar o DSP

| # | Bloco | O que extrair | Onde | Estado |
|---|---|---|---|---|
| A | Bloco / filtro | N=256, janela Hann, overlap-add, normalização, latência e **tipo de filtro por banda** | `0x87B2A0`/`0x87E220`/`0x879CF0`/`0x8B3ED0` | N e janela **provados**; tipo de filtro **não** |
| B | Análise | magnitude/potência, dBFS de referência, tilt | `0x8B8E70`, `0x8BA1B0` | não |
| C | Detecção | envelope de referência, comparação, knee, gate, threshold | `0x8B3ED0` | parcial (joelho) |
| D | Lei de ganho | 8 bandas, 8 shapes, depth, Q/slope, focus, channels | `0x8B3ED0`, `0x8BAA10`, `0x8BAB60` | não |
| E | Dinâmica | attack/release, suavização por bin e no tempo | `0x8B3ED0` | não |
| F | Estéreo/sidechain | link, focus, mid/side, sidechain, listen | `0x899940`, `0x8ACC40` | não |
| G | Saída | mix, wet/out trim, delta, max cut, limiter | `0x880640` | não |
| H | Linear phase | FIR, overlap maior, latência | instância separada | não |
| I | Estado | offsets `ctx+0x2C38`, `ctx+0x5F8`, `ctx+0x5ED0`, `ctx+0xBFF8` + mapa dos 143 params | structs | não |
| J | Validação | oráculo + null-test | - | WAV do oráculo **existe** (`host/test/out_soothe3.wav`, §15.3); falta o null-test do port |

Gargalo: **D/E dentro de `0x8B3ED0`** (20.209 B, fluxo achatado).

### 12.3 Ferramentas

| Ferramenta | Para quê |
|---|---|
| **IDA Pro 9.3 + Hex-Rays** | decompilador melhor em código achatado; tipar structs |
| **Ghidra 12.2** | scripts, xrefs, call graph, tabelas |
| **Unicorn Engine** | executar funções extraídas offline com entradas controladas → oráculo branco |
| **Capstone + pefile** | desmontagem/parse |
| **numpy / scipy / soundfile** | null-test, espectro, comparação de WAV |
| **REA MCP** | `batch_decompile`, `get_call_graph`, xrefs |
| **Frida (só leitura)** | ler estado vivo; **hook inline proibido** |
| **Diaphora / hash de função** | deduplicar instâncias de template |
| **Triton (fallback)** | execução simbólica se o achatamento resistir |

### 12.4 Limitações e como quebrar

| Limitação | Como quebrar |
|---|---|
| Anti-tamper do Themida | já resolvido: só leitura/estático; não precisamos vencê-lo |
| Oráculo bloqueado | loopback do FL / Reaper-Bitwig offline / Unicorn (ver 12.5) |
| Código achatado | Hex-Rays + anotação manual + Unicorn para confirmar cada ramo |
| Instâncias de template | hash das funções; extrair **uma** (estéreo) e provar equivalência |
| IPP proprietário | extrair os kernels exatos de `IPPCODE`, não "equivalente" |
| Ordem de float/FMA | transcrever ordem exata; `mul_add` onde o binário usa; sem contração onde não usa |
| Sem símbolos | nomear só por evidência (RVA + papel provado) |
| Escala (8 bandas × 8 shapes × surround) | estéreo + qualidade default primeiro |

### 12.5 Oráculo — as três rotas

| Rota | Como funciona | Prós | Contras |
|---|---|---|---|
| **Loopback do FL** | tocar WAV conhecido pelo soothe3 e gravar a saída do master (WASAPI loopback) | usa o plugin real; zero alteração | tempo real, não determinístico, sofre resample/buffer do device |
| **Reaper/Bitwig offline** | host renderiza a faixa pelo plugin para WAV, offline | determinístico, sample-accurate, null-test fácil | instalar outro host; mesma licença iLok |
| **Nosso host VST3** | consertar o `render_host` que hoje recebe `kResultFalse` | controle total, sem terceiros | precisa descobrir por que o `IAudioProcessor` é recusado |

Recomendação: **beta** = loopback do FL (rápido); **final bit-exact** = Reaper offline ou
nosso host consertado. Unicorn serve para validar bloco a bloco em paralelo.

### 12.6 Riscos declarados

1. `0x8B3ED0` é grande e achatado — é o gargalo de tempo.
2. Bit-exact pode ser inatingível se o IPP usar ordem/instruções não reproduzíveis;
   por isso a meta beta é tolerância.
3. Pode haver mais de um caminho (qualidade/fase); extrair um e provar os demais.
4. Onde não houver leitura, fica `NÃO EXTRAÍDO` — nunca estimativa.

### 12.7 Ordem de execução (revisada em 2026-11-22, ver §14 e §15)

1. **Cluster aritmético do núcleo** — `0x8BF5C0–0x8C4300` (12 funções) e o gêmeo
   `0x8C5FD8`. É onde há aritmética de verdade (§15.1). Começar por `0x8C3C20`
   (465 B, 30 ops, 0 chamadas) e `0x8C1440` (7.800 B, 58 chamadas).
2. **A — tipo de filtro por banda** (`0x87BB60` → `0x879CF0`×2, `0x882FC0`×2,
   `0x8833F0`/`0x8834C0`; `0x87E220` → `powf(2.4/-4.8)`).
3. **I — struct de estado** (offsets provados) + mapa dos 143 params.
4. **B/C/D/E** em `0x8B9E40` → `0x8B8E70` → `0x8BA1B0`.
5. **F/G** (`0x8BA7B0`/`0x8A1EE0` → `0x8B35A0`, `0x899940`, `0x8ACC40`, `0x880640`).
6. **H** linear phase (depois do caminho mínimo).
7. **J** validação — **fechado o lado do oráculo em 2026-11-24**: WAV em
   `host/test/out_soothe3.wav` (§15.3); falta o null-test do port.

---

## 13. Extração — janela, bloco e arquitetura (2026-11-22)

Esta seção corrige o rumo do §12: **o soothe3 não processa áudio por FFT.** O que está
provado é um processamento **no domínio do tempo, em blocos de 256 amostras com janela Hann
para overlap-add**. Tudo abaixo tem endereço, constante e RVA.

> **Correção de status (2026-11-22):** a expressão "banco de filtros de 1/3 de oitava" que
> aparecia aqui é **indício, não prova**. O que está provado é que `0x882C30` usa
> `pow(2, 1/3)` (`§13.5`). **Não está provado** que esse fator seja o espaçamento das bandas
> do filtro principal, nem qual o número real de bandas. Pela diretriz do §1, fica
> registrado como `NÃO PROVADO` até alguém ler o código que consome essa tabela.

### 13.1 Tamanho de bloco — PROVADO

`0x86A8C0` (linha 24 do decompilado) chama:

```c
FUN_180873440(param_1 + 0x58a, param_2, param_3, param_4, 0x100, 0, ...);
```

`0x873440` (inicialização):

```c
if (sample_rate <= 44100.0f) sample_rate = 44100.0f;     // 0x207A5E4
*(float *)(ctx + 4) = sample_rate;
ctx[6]  = 2;                                             // ctx+0x30 = 2
uVar31  = (int)(sample_rate * 2.26757365e-05f) * 0x100;  // 0x2079D04 = 1/44100
ctx[5]  = uVar31;                                        // ctx+0x28 = N
ctx[7]  = uVar31 * 2;                                    // ctx+0x38 = 2N
ctx[8]  = (uVar31 & 0x7fff...) + 1;                      // ctx+0x40 = N+1
ctx[0xc]= uVar31 >> 2;                                   // ctx+0x60 = N/4 (linha 143)
...
ctx[0xc]= ctx[5] >> 1;                                   // ctx+0x60 = N/2 (linha 2835, sobrescreve)
```

| Amostragem | N = `ctx+0x28` |
|---|---|
| 44.100 Hz | **256** |
| 48.000 Hz | 278 |
| 96.000 Hz | 557 |

Constantes: `44100.0f` @ `0x207A5E4`, `1/44100 = 2.26757365e-05f` @ `0x2079D04`,
`48000.0f` @ `0x207A5E8`.

### 13.2 Janela Hann — PROVADO

`0x877DD0`, chamada por `0x873440` (linha 2836):

```c
N = 2 * *(int *)(ctx + 0x60);            // = N do bloco
// aloca 1 buffer de N floats em ctx+0x2c08 (contagem em +0x2c1c = 1)
for (i = 0; i < N; i++) b[i] = (double)i / N;
for (i = 0; i < N; i++) {
    w[i] = (1.0 - cos(b[i] * 2π)) * 0.5;  // Hann periódica
    if (w[i] <= 0.0) w[i] = 0.0;
}
```

| RVA | Valor (double) | Uso |
|---|---|---|
| `0x207A138` | `1.0` | termo `1 - cos` |
| `0x207A1E0` | `6.283185307179586` | **2π** |
| `0x207A0B8` | `0.5` | escala |

Variante com offset (`0x87A370`), para janela parcial/crossfade:

```c
b[i] = (double)i / N * (1.0 - p) + p;    // p = param_3 (float)
w[i] = (1.0 - cos(b[i] * 2π)) * 0.5;
```

### 13.3 A FFT é só da UI — PROVADO

- `0x1D69E00` (FFT do IPP) tem **4** chamadores diretos: `0x72480`, `0x72A40`, `0x73440`,
  `0x1C1080`.
- `0x72480` e `0x72A40` **não têm chamada direta**: são gravados como ponteiros de função
  por `0x6F360` (construtor `juce::dsp::FFT`), nos `lea` de `0x6F4D8` (`0x72480`),
  `0x6F4E6` (`0x72A40`) e `0x6F4F4` (`0x73440`).
- `0x73440` só é chamado por `0x74180`, `0x74CA0`, `0x75AA0`.
- Nenhum deles é alcançável a partir da cadeia de áudio `0x8646A2 → … → 0x8B3ED0`
  (BFS sobre `docs/engine/xrefs.csv` + listas de `tools/func_summary.py`).
- As funções de áudio `0x885040`, `0x8875F0`, `0x88FB20`, `0x892770`, `0x8AD2B0`,
  `0x8B8E70`, `0x8B3ED0`, `0x8A1D10`, `0x8ABAA0`, `0x8AC510` **não chamam FFT nenhuma**.

**Consequência:** o item A do §12.2 não é STFT. O DSP é banco de filtros + janela de
overlap-add. As 3504 chamadas de `0x1D69E00` vistas no processo vivo eram do **espectro da
UI**, não do áudio.

### 13.4 Processadores por canal — PROVADO

| Função | Bytes | Papel |
|---|---|---|
| `0x885040` | 9.633 | processador por canal (variante A) |
| `0x8875F0` | 9.649 | processador por canal (variante A') |
| `0x88FB20` | 6.627 | processador por canal (variante B) |
| `0x892770` | 6.643 | processador por canal (variante B') |
| `0x89AC20` | 9.633 | idem A (outra instância de canais) |
| `0x89D1D0` | 9.649 | idem A' |
| `0x8A3A10` | 6.627 | idem B |
| `0x8A6660` | 6.643 | idem B' |

Todas chamam o mesmo setup: `0x87BB60`, `0x87E220`, `0x87B2A0`, `0x87F0C0`, `0x8981E0`,
`0x87F780`, e os construtores de span `0x8982C0` / `0x898300`.

### 13.5 Fator `pow(2, 1/3)` — PROVADO o cálculo; uso como espaçamento de banda NÃO PROVADO

`0x882C30` calcula `pow(2.0, 1/3)` e preenche a tabela de frequências:

```c
dVar4 = pow(2.0, 1.0/3.0);          // 2.0 @0x207A190, 1/3 @0x207A078 (double)
fill(dst, count, (float)(dVar4 * param_3), 4);
```

`0x879CF0` usa `pow(2.0, 1.0 / (param_4 / param_5))` para as bordas de banda.
`0x87B2A0` aplica a curva de ganho e chama `0x882C30`.

> **Limite:** está provado que esse fator é calculado e usado para preencher uma tabela.
> **Não** está provado que a tabela resultante seja o espaçamento do banco de filtros
> principal, nem quantas bandas existem. Ver a correção no início do §13.

### 13.6 Estrutura de estado — PROVADO

`0x868480` copia **0x98 (152) bytes** de estado e avança o índice de ring buffer:

```c
memcpy(dst, src, 0x98);
dst->idx = (src->idx + off) & (src->mask - 1);   // idx @ +0x90, mask @ +0x88
```

### 13.7 O que muda no plano

| Antes (§12) | Agora (provado) |
|---|---|
| Bloco A = STFT (janela + hop + FFT) | **Banco de filtros**, bloco N=256, janela Hann de overlap-add |
| "pipeline por-bin" | **por banda** (1/3 de oitava) |
| FFT no áudio | **FFT só na UI** |
| 1024–8192 de FFT | **N = 256 @ 44,1 kHz** (escala com sample rate) |

### 13.8 O que falta (atualizado)

1. **Tipo de filtro por banda**: biquad, FIR ou state-space. Ler `0x879CF0` + `0x8B3ED0`
   com tipos aplicados (o decompilado está sem tipos).
2. **Detector**: envelope, attack/release, `detail`, `tilt`.
3. **Lei de ganho**: as fórmulas `4^t`, `pow`, `log`, `exp` já extraídas — falta saber
   **onde** entram (por banda, por amostra).
4. **Overlap-add** e latência (`0x8ACC40` gerencia os ring buffers `+0x80/+0x88/+0x90`).
5. **Mapa dos 143 parâmetros** para campos de estado.
6. **Transcrição Rust** do extraído (substituir `app/src/dsp/*`).

---

## 14. Infraestrutura de leitura — verificado em 2026-11-22

Esta seção fecha três buracos que atrapalhavam a leitura do código e registra a ordem real
do pipeline. Nada aqui é estimativa: cada linha saiu de `.pdata`, de desmontagem ou de
leitura direta do dump.

### 14.1 Tamanho real das funções — **PROVADO** (unwind encadeado)

O `.pdata` **não** tem uma entrada por função: tem uma por *fragmento*. O primeiro
fragmento tem `UNWIND_INFO.Flags = 0` e os seguintes têm `Flags = 4`
(`UNW_FLAG_CHAININFO`), que significa "continuação da função anterior".

Exemplo medido em `0x8B3ED0`:

| RUNTIME_FUNCTION | Faixa | Bytes | Flags |
|---|---|---:|---|
| `0x8B3ED0` | `0x8B3ED0–0x8B3F01` | 49 | **0** (início real) |
| `0x8B3F01` | `0x8B3F01–0x8B3F0C` | 11 | 4 (chain) |
| `0x8B3F0C` | `0x8B3F0C–0x8B3F17` | 11 | 4 (chain) |
| `0x8B3F17` | `0x8B3F17–0x8B3F27` | 16 | 4 (chain) |
| `0x8B3F27` | `0x8B3F27–0x8B4268` | 833 | 4 (chain) |
| `0x8B4268` | `0x8B4268–0x8B85F2` | 17.290 | 4 (chain) |
| `0x8B85F2` | `0x8B85F2–0x8B86E3` | 241 | 4 (chain) |
| `0x8B86E3` | `0x8B86E3–0x8B8AE0` | 1.021 | 4 (chain) |
| `0x8B8AE0` | `0x8B8AE0–0x8B8C80` | 416 | 4 (chain) |
| `0x8B8C80` | `0x8B8C80–0x8B8CFF` | 127 | 4 (chain) |
| `0x8B8CFF` | `0x8B8CFF–0x8B8DC1` | 194 | 4 (chain) |
| `0x8B8DD0` | `0x8B8DD0–0x8B8E70` | 160 | **0** (próxima função) |

**Conclusão:** `0x8B3ED0` é **uma única função de 20.209 B** (`0x8B3ED0–0x8B8DC1`),
confirmando o valor do §5/§7. O `functions.csv` lista os fragmentos como se fossem
funções separadas — **nunca usar o `size` dessa região como tamanho de função**.

Correções de tamanho em outras funções da cadeia (mesmo método):

| Função | `.csv` / antes | **Real (chain-aware)** |
|---|---:|---:|
| `0x8ACC40` | 1.605 | **1.634 B** (`0x8ACC40–0x8AD2A2`) |
| `0x8B35A0` | 157 | **659 B** (`0x8B35A0–0x8B3833`) |
| `0x8AD2B0` | 5.013 | **5.021 B** |

### 14.2 Ordem real do bloco — **PROVADO**

Lida na lista de chamadas de `0x8AD2B0` (5.021 B), em ordem de execução:

```
1. 0x8B3ED0  (20.209 B)  entrada: buffers de estado +0x40 (amostras) / +0x48 (canais)
2. 0x8B9E40  (   871 B)  copia estruturas de 130 qwords + buffers de 1.016 B
3. 0x8B8E70  ( 4.036 B)
4. 0x8BA1B0  ( 1.533 B)
5. 0x8BA7B0  (   270 B)  chama 0x8B35A0 com flag = 1
6. 0x619D90  (   121 B)
7. 0x8BA8C0  (    36 B)
8. 0x8A1EE0  (   270 B)  chama 0x8B35A0 com flag = 0
```

`0x8BA7B0` e `0x8A1EE0` são **o mesmo código**, diferindo apenas no byte de flag
(`mov byte ptr [rsp+0x20], 1` vs `r10b` = 0) — ambos copiam 2×`0x400` B para a pilha e
chamam `0x8B35A0` (659 B). Ou seja: `0x8B35A0` é o mesmo caminho com dois modos.

Cada `0x8B3ED0` recebe três descritores de buffer montados a partir de
`estado+0x40` e `estado+0x48`; o preenchimento alinha cada canal em múltiplos de 16 floats.

### 14.3 Camada vetorial — **PROVADO** (classe), nome IPP exato **NÃO PROVADO**

O plugin usa **IPP estático com dispatch por CPU**. Mecanismo:

```asm
movsxd rax, dword ptr [rip + global]   ; ippJumpIndex
lea    r10,  [rip + tabela]
jmp    qword ptr [r10 + rax*8]          ; 8 variantes por CPU
```

- Global `ippJumpIndex` em **`0x21C7408`**, valor **4** no dump.
- Escrito por `0x2FB880` (init de features de CPU).
- Mapeamento completo: **372 thunks** em `checks/thunk_map.txt`.

Classe de operação das implementações (medida pela mistura de instruções vetoriais):

| Classe | Implementações | Instruções |
|---|---|---|
| multiplicar | `0x2760`, `0x4BC0`, `0x6160`, `0x9BA0` | `vmulss`/`vmulps` |
| somar | `0x95A0`, `0xA120`, `0xCF40` | `vaddss`/`vaddps` |
| subtrair | `0x50E0`, `0xA6A0` | `vsubss`/`vsubps` |
| clamp | `0x69C0` | `vminss`/`vmaxss` |
| preencher / copiar / converter | `0x2300`, `0x2F60`, `0x2C80`, `0xAC20`, `0xADA0`, `0xAF20`, `0xB500`, `0xB880`, `0xC560`, `0xCCE0` | sem aritmética vetorial |

Thunks mais usados no núcleo e sua classe:

| Thunk | Implementação | Classe | Usos em `0x8B3ED0` |
|---|---|---|---:|
| `0x1340` | `0x9BA0` | multiplicar | 13 |
| `0x1100` | `0x3480`* | preencher/converter | 9 |
| `0x1220` | `0x6160` | multiplicar | 7 |
| `0x10A0` | `0x2C80` | copiar | 4 |
| `0x10D0` | `0x2F60` | preencher | 3 |
| `0x1580` | `0xCCE0` → `0x65EA0` → `0x6CE80` | **MAC `dst += src1*src2`, com `vfmadd213ps` em `0006CEBB`** (corrigido em §23.1; a linha "sem aritmética vetorial" acima vale só para o corpo de 64 B de `0xCCE0`) | 2 |
| `0x1370` | `0xA120` | somar | 2 |
| `0x1190` | `0x4BC0` | multiplicar | 2 |

\* `0x3480` não é início de função no `.pdata`; a classe foi lida no trecho alcançado.

**Limite declarado:** o dump não tem os nomes das funções IPP (não existe string `ipps*`).
A *classe* é prova por instrução; o *nome* (`ippsMul_32f` etc.) é inferência e **não** entra
como especificação.

### 14.4 O que `0x8B9E40` realmente copia — **PROVADO (tamanho) / NÃO PROVADO (papel)**

- Copia uma estrutura de **130 qwords (1.040 B)** = 8 iterações de 16 qwords + 2.
- Aloca **2 buffers de 1.016 B** (254 floats cada) em `auStack_c50`.
- Lê a contagem em `param_2 + 0x80`.

Não está provado que 130 seja "número de bandas". Registro apenas o tamanho e o offset.

### 14.5 Regra de pareamento dos imports — **PROVADO** (corrige leitura anterior)

A tabela de descritores fica em `0x2174EFC`, passo `0x14`, campos `{name, IAT, INT}`.
O pareamento **não** é `descritor[i].INT → descritor[i].IAT`, e sim:

```
nomes( INT do descritor i )  →  IAT do descritor i+1
```

Verificação: `INT = 0x2176878` (descritor 16) contém `ceil, log10f, hypot, cos, …` e o
`IAT` do descritor 17 é `0x1D8D790` — exatamente o `MATH_IAT` já usado em
`checks/math_imports.txt`. O mesmo vale para os outros 20 descritores.

Thunk adicional resolvido por esse método: **`0x1C9A5AD` = `pow` (double)**, usado por
`0x879CF0` e `0x882C30`.

---

## 15. Correção de rota — onde a aritmética realmente está (2026-11-22)

Esta seção nasceu da revisão de **todos** os artefatos do projeto (inclusive `app/`, que
não é só o port). Ela corrige duas conclusões minhas e destrava a Fase 4.

### 15.1 `0x8B3ED0` **não é** onde a conta acontece — PROVADO

Desmontagem completa do corpo (`0x8B3ED0–0x8B8DC1`, 20.209 B, **4.473 instruções**):

| Classe | Contagem |
|---|---:|
| `movups` | 1.513 |
| `mov` / `lea` | 889 / 509 |
| `call` | **127** |
| `movaps` / `movss` / `movsd` | 281 / 37 / 12 |
| `mulss` | 23 |
| `subss` | 17 |
| `maxss` / `minss` | 7 / 5 |
| `divss` | 4 |
| `addss` | 3 |
| **aritmética vetorial (`*ps`) / FMA** | **0** |

Ou seja: `0x8B3ED0` é **orquestrador** — copia estado, percorre canais, chama 127 vezes.
Nenhuma `vmulps`/`vfmadd`. A conta por banda está nos **callees**.

**Cluster aritmético do núcleo** (chamado de dentro do corpo, via o fragmento
`0x8B4268`; tamanhos *chain-aware*):

| Função | Bytes | float ops | calls | Observação |
|---|---:|---:|---:|---|
| `0x8BF650` | 1.411 | 0 | 6 | chama `0x8CAB40` |
| `0x8BFBE0` | 199 | 0 | 2 | |
| `0x8BFD30` | 1.275 | 0 | 8 | usa `memset` + `0x61B790` |
| `0x8C0230` | 177 | 0 | 2 | |
| `0x8C02F0` | 2.079 | 0 | 9 | chama `0x8CAE90` ×2 |
| `0x8C0B10` | 177 | 0 | 2 | |
| `0x8C0BD0` | 2.150 | 1 | 14 | |
| `0x8C1440` | **7.800** | 6 | **58** | maior despachante |
| `0x8C32C0` | 266 | 0 | 1 | chama `0x8CB040` |
| `0x8C33D0` | 2.117 | 0 | 11 | |
| `0x8C3C20` | 465 | **30** | **0** | `subss`10/`mulss`10/`addss`10 — **maior densidade aritmética** |
| `0x8C3E00` | 266 | 0 | 1 | chama `0x8CB2F0` |

Candidato número 1 a "lei de ganho / curva por banda": **`0x8C3C20`** (465 B, 30 ops
escalares, zero chamadas, constante `0.100000001` em `0x8C3C20+…`, ver
`checks/core_callees.txt`).

**Gêmeo de `0x8B3ED0` — PROVADO por perfil de instruções:** `0x8C5FD8` (19.289 B) tem
**exatamente** o mesmo perfil float (`mulss` 23, `subss` 17, `maxss` 7, `minss` 5,
`divss` 4) e 123 `call`s, e é chamado pelas mesmas funções do cluster. É o **mesmo corpo
em outro modo** (canal/modo alternativo), não uma segunda implementação.

> **Consequência para o plano:** o alvo de leitura muda de `0x8B3ED0` para
> **`0x8BF5C0–0x8C4300` + `0x8C5FD8`**. Ler 20 KB de orquestrador não dá fórmula nenhuma.

### 15.2 As stubs `0x1C84xx` **são resolvíveis** — PROVADO (corrige §14.3)

Elas são o mesmo mecanismo `ippJumpIndex`, mas com **tabela própria por stub**. Cadeia
completa, resolvida com índice 4:

| Stub | Tabela | Trampolim | Slot | **Implementação** |
|---|---|---|---|---|
| `0x1C84A0` | `0x21C6A28` | `0x1C8880` | `0x21C6F08` | **`0x240C00`** (200 B) |
| `0x1C84D0` | `0x21C6A68` | `0x1C8940` | `0x21C6FF8` | **`0x277C00`** (246 B) |
| `0x1C8500` | `0x21C6AA8` | `0x1C8A00` | `0x21C70E8` | **`0x293760`** (197 B) |
| `0x1C8530` | `0x21C6AE8` | `0x1C8AC0` | `0x21C71D8` | **`0x29B260`** (200 B) |

Classe por instrução (não por nome):

| Impl | Instruções dominantes | Classe |
|---|---|---|
| `0x240C00` | `vfmadd231ps` 4, `vsubps` 4, `vandps`/`vpcmpgtd`/`vmovmskps` 4 cada | multiplicar-subtrair com máscara |
| `0x277C00` | `vmovups`/`vmovdqu` + `cmp`/`and` | copiar/encher |
| `0x293760` | `vfmadd213ps` 10, `vmovups` 24 | acumular produto (dot/FIR) |
| `0x29B260` | `vrcpps` 4, `vpsubd`/`vpand`/`vpcmpgtd` | recíproco (divisão) |

A stub **`0x1C8530`** (→ `0x29B260`, recíproco) é chamada por **`0x885040`** — o setup
por canal — e por toda a cadeia por canal (`0x8875F0`, `0x889FB4`, `0x88B224`, `0x88D7B0`,
`0x88DD60`, `0x88DF50`, `0x88E130`, `0x89AC20`, `0x89D1D0`, `0x89FB94`, `0x8A0E04`, …).
Isso põe uma **divisão por amostra** no caminho de áudio e dá um ponto de ancoragem para
o detector normalizado.

> **Nome exato ainda NÃO PROVADO** (não há strings `ipps*`), mas o **endereço da
> implementação está provado**. Nomear é opcional para o port; a aritmética não é.

### 15.3 Fase 4 — o oráculo **já funciona** (corrige "BLOQUEADA")

Existem **dois** hosts VST3 no projeto e eles não se comportam igual:

| Arquivo | Uso | Estado |
|---|---|---|
| `app/src/host.rs` | CLI `render_host.exe` (COM cru) | **falha** — `IAudioProcessor` → `kResultFalse` |
| `app/src/vst3host.rs` | in-process, usado por `--measure-original` | **funciona** no soothe3 instalado |

Evidência já produzida por ele (arquivos existentes, não promessa):

```
app/equivalence/original-curves.tsv   28 curvas (7 casos × 4 sinais) + latência + CPU
  #latency  2304      amostras @ 48 kHz = 48 ms
  #cpu      0.011736  (1,17 % de um núcleo em tempo real)
app/equivalence/original-parameters.txt   lista de parâmetros como o plugin os reporta
app/equivalence/score-check.md           comparação medida Resonia × original
```

Resultado medido em `score-check.md`: diferença média de **1,42 dB por banda** e
seletividade **12,0 (original) vs 3,2 (Resonia)**. Ou seja: o port heurístico é
**3,7× menos seletivo** — número objetivo, não opinião.

**FECHADO em 2026-11-24 — o WAV existe.** `app/` não voltou; o host foi reconstruído do zero
em `host/` (Rust std-only, FFI crua de `kernel32`, **sem** injeção/hook/patch; carrega o
`.vst3` read-only por `GetPluginFactory`). Resultado **reproduzido nesta sessão**:

- 48 kHz, bloco 512: 3 classes, `Audio Module Class` CID `01EFCDAB…`; `initialize`,
  `setupProcessing(kOffline,…)`, `setActive`, `setProcessing` = `S_OK`; 94 blocos, todos
  `S_OK`; 48.000 frames de saída.
- Latência reportada **2304** e **não** compensada no WAV; constante com bloco 512, 4096 e
  48.000.
- Determinístico: duas execuções → SHA-256 `1218C801A5E61A7591DCE500C40A166E8598532666AE5B7808816899B42BE67B`.
- **Não é transparente no estado padrão**: diferença alinhada por 2304 tem RMS **−6,6 dBFS**
  (pico −1,4 dBFS) com bloco 512. O null-test compara **plugin × reconstrução**, não
  entrada × saída.
- **A saída depende do bloco** (medido nesta sessão): RMS da diferença alinhada =
  −6,6 dBFS (512) / −8,2 dBFS (4096) / −11,6 dBFS (48000). Causa **`NÃO EXTRAÍDO`**
  (parada no protocolo `process`, sem RVA do plugin). O null-test tem de fixar o mesmo
  bloco nos dois lados.

Comandos: `cargo build --release --offline`; `host <plugin.vst3> <in.wav> <out.wav> [blocos]`.
WAVs/logs em `host/test/` (`out_soothe3.wav`, `out_44k1.wav`, `run4.log`, `run_44k1.log`).

### 15.4 "8 bandas" — PROVADO como UI, **NÃO PROVADO** como DSP

`kali::JUCEAudioProcessor<visualisation_data, 8>` e a tabela `0x238E9B0` (8 grupos × 9
parâmetros) provam **8 nós de banda na interface**. Continuam **não provados**:
o número de bandas do filtro de análise e o espaçamento delas. O fator `pow(2, 1/3)` do
`0x882C30` é cálculo provado, uso como espaçamento **não**.

### 15.5 `app/MECHANICS.md` está desatualizado — corrigir antes de usar

O documento afirma (cabeçalho e "What decompiling found") que o `.text` está cifrado,
que o DSP é `FFTPACK/PFFFT` e que as fórmulas são estimadas. As três coisas estão
**refutadas** pelo §13/§14 deste plano. O texto continua útil como inventário de
**parâmetros e textos de ajuda**; tudo que ele diz sobre o motor deve ser lido como
histórico.

---

## 16. Cluster aritmético — primeira função fechada (2026-11-22)

Esta seção registra o que foi **lido no código**, não o que se esperava encontrar. Ela
também corrige uma classificação errada do §15.2.

### 16.1 `0x8C3C20` — suavização forward-backward — **PROVADO**

465 B (`0x8C3C20–0x8C3DF1`), **zero `call`**, 30 operações escalares. Desmontagem lida
inteira. É o estágio aritmético mais denso do cluster e o primeiro a ser fechado.

**Estrutura que ele recebe** (em `rcx`):

| Offset | Tipo | Papel |
|---:|---|---|
| `+0x000 … +0x3FF` | `void *[128]` | até 128 ponteiros para arrays de `float` |
| `+0x400` | `int32` | `count` — quantos arrays |
| `+0x404` | `int32` | `length` — floats por array |

**Algoritmo** (transcrito de `0x8C3C20`; constante `0.1f` em `0x2079DB0`):

```c
for (i = 0; i < count; i++) {
    float *v = arrays[i];
    float p = v[0];
    for (j = 0; j < length; j++) {            // 0x8C3C90 (4x desenrolado)
        p = p + (v[j] - p) * 0.1f;
        v[j] = p;
    }
    for (j = length - 2; j >= 0; j--) {       // 0x8C3D50 (4x desenrolado)
        p = p + (v[j] - p) * 0.1f;
        v[j] = p;
    }
}
```

Detalhes que importam para o port:

- O coeficiente é **`0.1f`** (`movss xmm3, [0x2079DB0]` em `0x8C3C43`), não `0.9`.
  A forma é `p += (x − p)·0.1`.
- O passe para trás **começa em `length−2`** (`lea rbx,[r10−2]` em `0x8C3C50`), não em
  `length−1`: o último elemento só recebe o passe direto.
- O estado `p` **é carregado** do passe direto para o passe traseiro (mesmo `xmm2`).
- Os dois laços são desenrolados de 4 em 4 e têm cauda escalar — mas a ordem das
  operações por elemento é a mesma, então a transcrição acima é fiel.
- `count`/`length` vêm de `+0x400`/`+0x404`. O mesmo layout aparece em
  `808B3ED0.c:4838`, onde `param_2 + 0x404` é passado como comprimento de `fill`.

**Chamadores:** `0x8B4268` (fragmento do corpo de `0x8B3ED0`) e `0x8CA362`
(`808B3ED0.c:2666`). O argumento é `local_908`, declarado como `longlong local_908[130]`
— 1.040 B, compatível com 128 ponteiros + `count` + `length`.

**NÃO PROVADO:** que os arrays sejam ganhos por banda, bins ou canais. O formato é
genérico; o papel depende de quem preenche o descritor (próximo item).

### 16.2 `0x8C3F10` — varredura de descritores com flag — **PARCIAL**

952 B. Chamada em `808B3ED0.c:4822` logo depois de `0x8C3C20`, com
`*(longlong *)(param_1 + 0x2c38)` (o ponteiro de configuração) como 2º argumento.

O que está **provado** por instrução:

- Varre dois blocos de descritores com passo 8: `[rdx+0x1b8 … rdx+0x1e0)` duas vezes,
  testando **bytes em `+5` e `+6`** de cada descritor (`0x8C3F50`, `0x8C3F90`). Se todos
  forem zero, retorna sem fazer nada (`0x8C42BE`).
- Lê um `int32` do início do descritor (`r8d = [r14]`) e compara com `r13`, que é
  carregado **uma vez** de `*(int32 *)0x2014360` (`0x8C4008`), valor **8** no dump.
- Passa por uma cadeia de comparações `r13 == 1,2,3,4,5,6,7` antes do caso default
  (`0x8C4020–0x8C40DB`). Como `r13` é 8 nesta chamada, **todos esses ramos são
  inalcançáveis aqui** e o efeito observável é `(descritor->type == 8)`. Isso é um fato
  do binário, não uma leitura de intenção: ou a tabela é genérica e compartilhada, ou há
  um caminho que não foi lido.
- Usa `[rbx+0x404]` como comprimento (`0x8C4106`) — o mesmo campo `length` do §16.1.

**NÃO PROVADO:** o significado do teste (enable? shape permitido?), o que são os bytes
`+5`/`+6`, e o papel de `0x61B790` (chamado 2x no ramo `r13==6`). Não escrever
"gate de banda" como se fosse prova.


### 16.3 `0x1C84D0` **não é cópia** — é potência inteira — **PROVADO** (corrige §15.2)

A cadeia de dispatch resolve para `0x277C00`. Lendo a implementação:

| Bloco | Instruções | Operação |
|---|---|---|
| `0x27C260` | `mov`/`vmovups` | **cópia pura** |
| `0x27BC60` | `vmulss x,x` | **x²** |
| `0x27B920` | `x·x·x` | **x³** |
| `0x27B5C0` | 4 multiplicações | **x⁴** |
| `0x27B280` | 5 | **x⁵** |
| `0x27AF40` | 6 | **x⁶** |
| `0x27A980` | 7–8 | **x⁷/x⁸** |

Ou seja: `0x1C84D0(dst, k, src, len)` = `dst[i] = src[i]^k`, com caminho rápido para
`k` inteiro pequeno. A classificação "copiar/enchér" do §15.2 estava **errada** e fica
corrigida aqui.

### 16.4 `0x879CF0` — par expoente/recíproco — **PROVADO o par; fórmula final NÃO**

12.557 B de decompilado. Sobre uma lista de arrays (descritor com `count` em
`param_1+0x80` e campos `+0x84/+0x88/+0x8c`), a ordem executada é:

```c
// 80879CF0.c:181   operação vetorial (thunk 0x1310) entre dst e src, com c0
// 80879CF0.c:194   dVar2 = 1.0 / max(param_3, c0)
// 80879CF0.c:218   operação vetorial com (float)dVar2 (thunk 0x1220)
// 80879CF0.c:244   dVar1 = pow(2.0, 1.0 / (param_4 / param_5))
// 80879CF0.c:250   operação vetorial com (float)(dVar1 * param_3) (thunk 0x1100)
// 80879CF0.c:280   arr = pow_int(arr, param_4 / param_5)     // 0x1C84D0 (§16.3)
// 80879CF0.c:311   operação vetorial com 1.0f (thunk 0x12E0)
```

**O que está provado:** o código calcula `pow(2.0, 1.0/(p4/p5))` e depois eleva o array
a `p4/p5`. O par expoente/recíproco é **o mesmo número por construção** — é isso, e só
isso, que sustenta a leitura de que `param_4/param_5` é o divisor de oitava (passos por
oitava).

**NÃO PROVADO — e por isso não há fórmula final aqui:**

1. o valor numérico de `param_4/param_5` (vem do chamador `0x87BB60`);
2. a semântica dos thunks `0x1310`, `0x1220`, `0x1100`, `0x12E0`. Sem ela não se sabe se
   cada passo é **elementwise** ou **preenchimento com constante**, e portanto não se
   pode escrever a expressão resultante. Uma tentativa anterior de fechar a álgebra
   (`(a·2^k)^(1/k)`) foi **descartada** justamente por depender dessa suposição;
3. que a tabela gerada seja o espaçamento do filtro principal.

Continua valendo o aviso do §13: `pow(2, 1/3)` é cálculo provado; uso como espaçamento
**não**.

> **Correção (2026-11-22, §17.3):** os dois chamadores reais passam `param_4 == param_5`,
> então o expoente é 1 e o `pow` é identidade. Esta subseção fica como histórico da
> leitura; a função **não** gera espaçamento de bandas.



### 16.5 Ambiente — Ghidra saiu, IDA entrou (mudança operacional) — **CORRIGIDA em §19**

> **Correção de 2026-11-22 (verificado agora):** a primeira linha desta subseção estava
> **errada**. O Ghidra **está instalado**: `GHIDRA_INSTALL_DIR=D:\TOOLS\ghidra_12.2_PUBLIC`,
> com `ghidraRun.bat` e `support\analyzeHeadless.bat` presentes, e
> `C:\Users\tromb\AppData\Local\Temp\ghidra` existe. O que **não** existe é
> `ghidra_proj/soothe3.gpr` — o projeto não está no diretório. O texto abaixo fica como
> registro do que se acreditava naquele momento.

- `GHIDRA_INSTALL_DIR` está **vazio** e `C:\Users\tromb\AppData\Local\Temp\ghidra` está
  **vazia**: o Ghidra não está mais instalado. O projeto `ghidra_proj/soothe3.gpr`
  sobreviveu, mas não há binário para abri-lo.
- **IDA Pro 9.3 + Hex-Rays** está em **`D:\TOOLS\IDA`** (`idat.exe`), com banco do dump
  em `C:\Users\tromb\AppData\Local\Temp\opencode\ida_work` e uma **cópia de trabalho**
  em `...\ida_cluster` (não tocar na original).
- Ferramentas novas no repositório:
  - `tools/show_func.py <rva>` — desmonta uma função *chain-aware* e resolve
    float/double/int e nomes de import nos operandos RIP.
  - `tools/ida/decompile_batch.py` + `tools/ida/batch_list.txt` — decompila uma lista
    de RVAs para `docs/engine/decomp/` e escreve `checks/ida_batch.txt`.
- **Limite medido (à época):** o lote com `0x8C5FD8` (19.289 B) ficou **26 min de CPU sem
  terminar**. A causa não era o tamanho: era o banco errado (§19.1). Com o PE certo,
  `0x8C5FD8` decompila em **0,1 s** e rende 116.125 caracteres (§19.3).

### 16.6 Nota operacional sobre subagentes

As duas tentativas de paralelizar com subagentes falharam com
`Free usage limit reached` **antes de escrever qualquer arquivo**. Nenhum artefato foi
produzido por eles e nenhum `.md` foi tocado. Todo o §16 é leitura feita pelo agente
principal. Enquanto o limite existir, o trabalho segue em série.



---

## 17. Camada vetorial resolvida - as primitivas tem nome por opcode (2026-11-22)

O bloqueio numero 1 do §16.4 (`"nao sei se o thunk e elementwise ou fill"`) caiu.
Os "thunks" `0x1010..0x1610` nao sao copias nem caixas-pretas: sao as primitivas de
vetor da IPP, cada uma com um **indice de dispatch** (`ippJumpIndex` em `0x21C7408`,
valor 4 no dump), uma **tabela** propria e uma implementacao selecionada. A operacao
foi lida do **opcode**, e o sentido (in-place ou fora-do-lugar) foi lido do **registrador
de destino do store**. Nenhum nome foi adivinhado.

### 17.1 Metodo (reprodutivel)

`tools/vector_primitives.py`:

1. varre RVAs 4-alinhados em `0x1000..0x30000`;
2. aceita o candidato so se as 3 primeiras instrucoes forem o padrao de dispatch
   (global com o indice + base da tabela + `jmp reg`);
3. resolve `entry = u64(tab + idx*8) - base`;
4. caminha o CFG a partir de `entry` (fallthrough + saltos diretos, para em `ret`);
5. conta os mnemonicos de ponto flutuante alcancaveis.

Saida: `checks/vector_primitives.txt` (33 primitivas).
`tools/core_vector_calls.py` cruza com `808B3ED0.c` -> `checks/core_vector_calls.txt`.

### 17.2 As 4 primitivas usadas por `0x879CF0` - PROVADO com store

| Thunk | Impl | Semantica provada | Prova |
|---|---|---|---|
| `0x1310` | `0x95A0` | `out[i] = in[i] + s` (**fora do lugar**) | `0x9640 vaddss` le `[rcx+..]`; `0x9646 vmovss [rdx+..]` grava; `0x95AA mov rdx,r8` |
| `0x1220` | `0x6160` | `a[i] *= s` (**in place**) | `0x6200 vmulss xmm1,xmm0,[rdx+..]`; `0x6205` grava em `[rdx+..]` |
| `0x12E0` | `0x8FA0` | `a[i] += s` (**in place**) | `0x9020 vaddss`; `0x9025` grava em `[rcx+..]` |
| `0x1100` | `0x3480` | **clamp com escalar**: `r9d==4` -> `min`, `r9d==0` -> `max` | `0x3495 test r9d/r9d; je 0x35D9` (max, `0x3640 vmaxss`); `0x349E cmp r9d,4; je 0x34AA` (min, `0x3500 vminss`) |

O `0x1100` e o unico com dois modos. O modo vem do **4o argumento inteiro**, nao do
nome da funcao - e por isso que ele parecia "fill" quando lido so pela assinatura.

### 17.3 `0x879CF0` reescrito com a semantica real - e a hipotese de "bandas" caiu

Com os thunks resolvidos, a sequencia do §16.4 deixa de ser especulacao. Por array
(as duas primeiras linhas usam `param_1` como origem e `param_2` como destino; o resto
e in place):

```c
// 80879CF0.c:181   out = in + fVar5                       (0x1310, fora do lugar)
// 80879CF0.c:194   dVar2 = 1.0 / max(param_3, fVar5)
// 80879CF0.c:218   out *= dVar2                            (0x1220, in place)
// 80879CF0.c:244   dVar1 = pow(2.0, 1.0/(param_4/param_5))
// 80879CF0.c:250   out = min(out, dVar1*param_3)           (0x1100 modo 4)
// 80879CF0.c:280   out = pow(out, param_4/param_5)         (0x1C84D0 -> 0x277C00)
// 80879CF0.c:311   out += 1.0f                             (0x12E0)
// 80879CF0.c:341   out = 1.0f / out                        (0x1C8530 -> 0x29B260, vrcpps)
// 80879CF0.c:371   out = max(out, 0.0f)                    (0x1100 modo 0)
// 80879CF0.c:376   param_5 *= 0.166666672f                 (1/6, 0x2079DE0)
// 80879CF0.c:402   out = pow(out, param_5)
// 80879CF0.c:431   out = min(out, 1.0f)                    (0x1100 modo 4)
```

**Valores reais nos dois chamadores (`0x87BB60`, instrucoes lidas):**

| Chamada | `param_3` | `param_4` | `param_5` | `param_4/param_5` |
|---|---:|---:|---:|---:|
| `0x87CA0E` | `250.0f` (`0x207A514`) | `2.0f` (`0x207A188`, via `xmm15`) | `2.0f` (mesmo `xmm15`) | **1.0** |
| `0x87CBF9` | `1000.0f` (`0x207A590`) | `2.0f` | `2.0f` | **1.0** |

Prova: `0x87C961 movss xmm2,[0x207A514]`, `0x87C91F movaps xmm3,xmm15`,
`0x87C9B9 movss [rsp+0x20],xmm15` (1a chamada); `0x87CB10 movss xmm2,[0x207A590]`,
`0x87CB18 movaps xmm3,xmm15`, `0x87CBEB movss [rsp+0x20],xmm15` (2a chamada);
`xmm15` = `2.0f` em `0x87CA13`/`0x87CB07`.

**Consequencia (fato, nao interpretacao):** nos dois chamadores `param_4 == param_5`,
logo `pow(2, 1/1) = 2` e `pow(x, 1) = x`. O expoente geometrico e **identidade** aqui.
A leitura do §16.4 ("serie geometrica de bandas / divisor de oitava") **esta errada
para estes chamadores** e fica retirada.

Substituindo os valores reais (com `fVar5 = 1.1920929e-07 = FLT_EPSILON`, `0x2079CF0`):

```c
// a = param_3 (250 ou 1000); x = valor de entrada
y = x / a;                    // (x + eps) / max(a, eps), o eps e irrelevante
y = y + 1.0f;                 // o min(y, 2*a) da linha 250 nao atua para x < 2*a^2
y = 1.0f / y;                 // 0x29B260
y = powf(y, 1.0f/3.0f);       // param_5 = 2.0 * 1/6 = 1/3
y = min(y, 1.0f);
```

ou seja, uma **curva de normalizacao racional**:

```
y = min( ( 1 / (x/a + 1) )^(1/3) , 1 )
```

O expoente e **bit-exato** igual a `1.0f/3.0f`, nao "aproximadamente 1/3":
`0x2079DE0` = `0.1666666716337204f`; `2.0f * 0.1666666716337204f` =
`0.3333333432674408f` = bits `0x3EAAAAAB`, que sao os mesmos bits de `1.0f/3.0f`.
Verificado por `struct.pack` em Python, nao por inspecao visual.

Outros detalhes que so agora ficaram visiveis:

- `0x1C8530` nao e "mais uma potencia": resolve por `0x21C71D8 -> 0x29B260`, cuja
  assinatura e `vrcpps` (reciproco), nao `vmulps` em cadeia.
- `0x1C84D0 -> 0x277C00` e **potencia com expoente real** e o despacho e por
  **comparacao exata do bit pattern** do expoente (`0x277F56`):

  | expoente | destino |
  |---:|---|
  | `1.0f` (`0x3F800000`) | `0x27C177` -> **copia pura** (`0x27C260` escalar, `0x27C280` `vmovups`) |
  | `2.0f` | `0x27BE7B` |
  | `3.0f` | `0x27BB7F` |
  | `4.0f` | `0x27B823` |
  | `5.0f` / `6.0f` / `7.0f` / `8.0f` / `9.0f` | `0x27B4C7` / `0x27B18B` / `0x27AE52` / `0x27AB10` / `0x27A7B8` |
  | `-1.0f` .. `-4.0f` | `0x27A781` / `0x27A46C` / `0x27A150` / `0x279DEB` |
  | `0.5f` / `-0.5f` / `1.5f` | `0x279DB4` / `0x279D7D` / `0x279CD7` |
  | **qualquer outro** | `0x278006` (caminho geral) |

  Consequencia para o port, e ela importa para o alvo bit-exact:

  - `param_4/param_5 = 1.0f` cai no ramo de **copia pura** -> identidade bit-exata,
    provada. A simplificacao do §17.3 acima e legitima.
  - `param_5 * 1/6 = 0.3333333432674408f` (`0x3EAAAAAB`) **nao** esta na tabela ->
    vai pelo **caminho geral** (`0x278006`, que chama `0x2D74A0`, `0x2EEF00`,
    `0x2EF8A0` e o reciproco `0x29B260`). Ou seja: o `^(1/3)` **nao** e `cbrtf`, e o
    port tem de reproduzir esse caminho, nao substituir por `powf`.
- `DAT_18207a190` = **2.0** (double, `0x207A190`); `DAT_18207a138` = **1.0** (double,
  `0x207A138`); `DAT_182079f9c` = **1.0f** (`0x2079F9C`); `_DAT_182079de0` =
  **0.166666672f** (`0x2079DE0`).

**Continua NAO PROVADO:** o que sao as arrays de entrada (o descritor e generico) e em
que ponto do pipeline essa curva e usada. O que esta provado e que ela **nao** e o
espacamento de bandas.


### 17.4 Primitivas usadas pelo nucleo `0x8B3ED0` (45 chamadas)

| Thunk | Vezes | Operacao (por opcode) |
|---|---:|---|
| `0x1340` | 13 | multiplicacao por escalar (in place) |
| `0x1100` | 9 | clamp escalar (min/max conforme modo) |
| `0x1220` | 7 | multiplicacao por escalar (in place) |
| `0x1250` | 3 | clamp entre dois vetores (`vminps`/`vmaxps`) |
| `0x1190` | 2 | multiplicacao (in place) |
| `0x1400` | 3 | **produto escalar** (impl `0x5F5C0`: `vmulss`+`vaddss` acumulando) |
| `0x1430` | 2 | **reciproco** (impl `0x63640`: `vrcpps` + Newton) |
| `0x1550` | 2 | **reciproco** (mesma impl `0x63640`, um nivel de wrapper a mais) |
| `0x1580` | 2 | **soma de array** (impl `0x65EA0`: `vaddss`/`vaddps` acumulando `[rdx]`) |
| `0x1160` | 1 | subtracao por escalar |
| `0x1010` | 1 | dispatcher de struct (`[obj]==7` -> chamada por vtable `[obj+8]->[+0x18]`) |

> **Cadeia de dispatch — catalogada em 2026-11-22 (§19.4).** A coluna "Impl" acima é a
> implementação **interna**, não o alvo do `jmp [tabela]`. O alvo do dispatch é um wrapper
> de 20–40 B que faz a validação de argumentos e então chama a implementação. Resolvido por
> leitura da tabela (`ippJumpIndex = 4`) e do corpo de cada wrapper:
>
> | thunk | alvo do dispatch | cadeia até a implementação |
> |---|---|---|
> | `0x1400` | `0xAC20` | `call 0x5F5C0` (produto escalar) |
> | `0x1430` | `0xADA0` | `call 0xC560` → `call 0x63640` (recíproco, 2 hops) |
> | `0x1550` | `0xC560` | `call 0x63640` (recíproco) |
> | `0x1580` | `0xCCE0` | `call 0x65EA0` (soma) |
> | `0x1010` | `0x20E0` | `call [rcx]`, `call [rax+0x18]` (dispatch por vtable) |
>
> É por isso que `checks/core_vector_calls.txt` mostra `impl=0xAC20` para `0x1400` e este
> documento mostra `0x5F5C0`: os dois estão certos, em níveis diferentes. Sem esta nota a
> próxima sessão acha que um dos dois está errado.

`0x1040` (impl `0x2300`) e **preenchimento com constante** (`vmovd ecx,xmm0` +
`call 0x1D2E460`, sem op float) - nao e usado diretamente por `0x8B3ED0`.

Isso da, pela primeira vez, uma leitura **aritmetica** do nucleo. Somando a coluna
"Vezes": **22 multiplicacao** (`0x1340`+`0x1220`+`0x1190`), **12 clamp**
(`0x1100`+`0x1250`), **3 produto escalar**, **4 reciproco** (`0x1430`+`0x1550`),
**2 soma**, **1 subtracao**, **1 dispatcher** = **45**. Nenhuma delas e FFT.

### 17.5 IDA - causa raiz encontrada, e o lote **ainda** nao entrega

Historico, para nao repetir o erro:

1. O lote anterior nao travou decompilando: ele **nunca chegou ao script**. O log para
   em `Autoanalysis subsystem has been initialized` e nao mostra nada do IDAPython.
   O banco usado (`...\ida_cluster`) estava **corrompido** (`Database ... is not
   closed`, `contains inconsistencies`, `repaired`) - 108 min de CPU sem uma linha.
2. Trocado pelo banco **bom** (`...\ida_work`), o sintoma continuou. A causa real e
   **outra**: `ida_auto.auto_wait()` **nunca retorna** nesta imagem de 137 MB - o
   banco tem analise pendente que o IDA tenta terminar indefinidamente. Um script
   trivial (`tools/ida/hello.py`, sem `auto_wait`) **executa e escreve o arquivo**,
   o que isola a culpa no `auto_wait`.
3. Corrigido: `tools/ida/decompile_batch.py` nao chama mais `auto_wait()`, abre o
   relatorio em modo escrita e faz `flush` a cada funcao (um kill nao perde nada).
   Tambem e obrigatorio `-S"caminho"` **sem espaco** depois do `-S`.

**Estado atual, sem maquiagem:** com essas duas correcoes o script roda de fato, mas
para os RVAs do cluster ele responde `NOFUNC` (`add_func` devolve `False`) e o
diagnostico mostra `imagebase=0x0` no banco. Ou seja: **IDA ainda nao decompilou
`0x8C1440` nem nenhuma outra funcao do cluster**. O lote completo continua parado.

> **RESOLVIDO em 2026-11-22 — ver §19.** O sintoma (`imagebase=0x0`, `seg=none`,
> `add_func=False`) nao era do `auto_wait` nem do tamanho: o lote abria
> `ida_run\soothe3_unpacked_mem.bin` (136.990.720 B, dump de memoria cru) em vez do PE
> normalizado (137.003.008 B). Com o PE, o IDA cria as 30.859 funcoes do `.pdata` na
> carga e o cluster decompila. Esta subsecao fica como historico do diagnostico errado.

Consequencia pratica: a leitura segue com `tools/show_func.py` (desmontagem
chain-aware), que ja produziu tudo o que esta no §16 e no §17 sem depender de IDA.

### 17.6 Ferramentas novas

| Arquivo | Papel |
|---|---|
| `tools/thunk_semantics.py` | resolve indice/tabela/entrada de cada thunk |
| `tools/thunk_ops.py` / `thunk_ops2.py` / `thunk_ops3.py` | versoes do classificador (a 3 e a valida: CFG + `.pdata`) |
| `tools/vector_primitives.py` | tabela completa das 33 primitivas -> `checks/vector_primitives.txt` |
| `tools/core_vector_calls.py` | cruzamento com o nucleo -> `checks/core_vector_calls.txt` |
| `tools/ida/batch_list_full.txt` | lista completa de RVAs para o IDA |

---

## 18. Para que serve a camada vetorial: um fragmento real do nucleo (2026-11-22)

Esta secao existe para responder a pergunta "como isso ajuda na extracao?". O teste e
concreto: pegar um trecho de `0x8B3ED0` que **antes era ilegivel** e transcreve-lo.

### 18.1 O trecho

`808B3ED0.c:2028-2048` / desmontagem `0x8B67B6..0x8B6898` (`checks/_8b3ed0.dis`,
linhas 2279-2323).

Antes do §17, as tres chamadas abaixo eram indistinguiveis de copia ou preenchimento:

```
008B6814  call 0x1400   ; -> 0x5F5C0
008B6847  call 0x1400   ; -> 0x5F5C0
008B6871  call 0x11f0   ; -> 0x5BC0
008B6893  call 0x11f0   ; -> 0x5BC0
```

Depois do §17: `0x1400` = produto escalar (`vmulss`+`vaddss` acumulando, `0x5F646`),
`0x11F0` = FMA in place (`vfmadd213ss xmm0, xmm1, [r8+r10*4]` em `0x5C46`, store em
`0x5C4C`), ou seja `dst[i] += coef[i]*s`.

### 18.2 Transcricao (instrucao por instrucao)

```c
// 0x8B67D2  xmm8 = 1.00000001e-07f   (0x2079CEC)
// 0x8B67E2  xmm9 = xmm11 - xmm10     (valores definidos antes do laco; NAO PROVADOS)
// 0x8B67B6  contagem = *(int64 *)(param_1 + 0x48)
for (i = 0; i < count; i++) {
    float *a = arrays[i];                 // 0x8B67F0  rbx = [rdi]
    float s1 = 0.0f, s2 = 0.0f;

    dot(0x2077800, a, 16, &s1);           // 0x8B6814  call 0x1400
    dot(0x2077740, a, 16, &s2);           // 0x8B6847  call 0x1400

    float x = s1; if (x <= 1e-7f) x = 1e-7f;   // 0x8B6842  maxss xmm7, xmm8
    float y = s2; if (y <= 1e-7f) y = 1e-7f;   // 0x8B685B  maxss xmm6, xmm8

    float t1 = (y / x) * x;               // 0x8B6869 divss, 0x8B686D mulss
    fma_add(0x2077700, t1, a, len);       // 0x8B6871  call 0x11f0

    float t2 = ((x / y) * y) * xmm9;      // 0x8B6876 divss, 0x8B6887 mulss, 0x8B688B mulss
    fma_add(0x2077840, t2, a, len);       // 0x8B6893  call 0x11f0
}
```

### 18.3 As quatro tabelas de coeficientes (16 taps cada)

| RVA | 4 primeiros valores | Papel no codigo |
|---|---|---|
| `0x2077800` | `0.135227725, 0.135201931, 0.135059059, 0.134432733` | numerador do 1o dot |
| `0x2077740` | `3.64401984e-08, 8.97622442e-07, 9.88739339e-06, 7.73675929e-05` | numerador do 2o dot |
| `0x2077700` | `0.999981046, 0.99979037, 0.998733819, 0.994102299` | coeficiente do 1o FMA |
| `0x2077840` | `1.59999971e-07, 3.94124027e-06, 4.3413118e-05, 0.000339702121` | coeficiente do 2o FMA |

### 18.4 Dois detalhes que so aparecem por causa da camada vetorial

1. **`(y/x)*x` nao e `y`.** O compilador emitiu `divss` seguido de `mulss`
   (`0x8B6869`, `0x8B686D`). Em IEEE-754 isso tem **duas rondagens** e o resultado pode
   diferir de `y` em ulps. Para o alvo bit-exact, a transcricao tem de manter a
   divisao e a multiplicacao, nao "simplificar" para `y`.
2. **`maxss` nao e `fmaxf`.** `maxss xmm7, xmm8` devolve o segundo operando quando
   qualquer um e NaN; `fmaxf` tem outra regra. O `if (x <= eps) x = eps` do decompilado
   e uma aproximacao de leitura - o port deve usar a semantica de `maxss`.

### 18.5 O que isso muda, em uma frase

O nucleo `0x8B3ED0` tem 20.209 B e 127 `call`, dos quais 45 sao vetoriais. Antes, cada
um desses 45 era "chamada desconhecida" e o nucleo nao podia ser escrito. Agora os 45
tem operacao provada (`checks/core_vector_calls.txt`), e o trecho acima - que e
aritmetica de verdade, com tabela de coeficientes e acumulacao - pode ser transcrito
para Rust sem adivinhar nada.

O que **nao** ajuda: `0x879CF0` (§17.3) nao e DSP, e curva de normalizacao. O ganho ali
foi negativo: eliminou uma hipotese errada (espacamento de bandas) que teria
contaminado o port.

---

## 19. IDA consertado — causa raiz, receita e resultado (2026-11-22)

Esta seção existe porque o §17.5 parou o projeto num diagnóstico errado. A ferramenta
nunca esteve quebrada. O banco é que apontava para o arquivo errado.

### 19.1 Causa raiz — **PROVADO**

`tools/ida/run_batch.ps1` abria:

```
...\ida_run\soothe3_unpacked_mem.bin     136.990.720 B   <- dump de memória cru
```

e não o PE normalizado:

```
dumpsooth\soothe3_unpacked.dll           137.003.008 B   <- PE completo
```

Diferença: **12.288 B = 0x3000** (headers + alinhamento de seção). Um `.bin` cru carrega
como *binary file*: sem seções PE, sem diretório de exceção, base 0. É exatamente o
sintoma registrado no §17.5:

```
imagebase=0x0
seg=none mapped=False code=False func=none
add_func(0x8C3C20) -> False
funcs in [0x8B0000,0x8D0000): 0
```

Os bancos `ida_work` e `ida_cluster` são do **mesmo** `soothe3_unpacked_mem.bin`
(136.990.720 B) — por isso tinham o mesmo defeito. O `auto_wait` que nunca retornava era
sintoma de análise sem seções, não de tamanho.

O PE normalizado tem tudo que faltava:

| Diretório | RVA | Size |
|---|---:|---:|
| exception (`.pdata`) | `0x2758000` | `0x5A684` = 370.308 B = **30.859 × 12** |
| import | `0x79CF76C` | `0x64` |
| security | `0x2D48A00` | `0x4308` |
| reloc | `0x79D5000` | `0x20` |

19 seções, todas com `PointerToRawData == VirtualAddress` (layout plano, como o §3 já
dizia), `ImageBase = 0x180000000`, `SizeOfImage = 0x82A8000`.

### 19.2 Receita que funciona (reprodutível)

```powershell
# 1. banco novo, a partir do PE
$w = "C:\Users\tromb\AppData\Local\Temp\opencode\ida_pe"
Copy-Item D:\PROJETOS\soultree\dumpsooth\soothe3_unpacked.dll "$w\soothe3_pe.dll" -Force

# 2. primeira carga (cria o banco). -S sem espaço depois do -S.
D:\TOOLS\IDA\idat.exe -A -c -S"$w\script.py" -L"$w\ida.log" "$w\soothe3_pe.dll"

# 3. cargas seguintes: sem -c (reabre o banco existente)
D:\TOOLS\IDA\idat.exe -A -S"$w\script.py" -L"$w\ida.log" "$w\soothe3_pe.dll"
```

O log da primeira carga confirma a correção:

```
Parsing .pdata and creating 30859 functions...
File '...\soothe3_pe.dll' has been successfully loaded into the database.
```

`imagebase=0x180000000`. Logo `EA = 0x180000000 + RVA`.

**Armadilha 2 — `.pdata` cria a função, mas não desmonta o corpo.** Sem essa segunda
etapa o Hex-Rays devolve `JUMPOUT(0x...25LL)` e o decompilado tem 51 caracteres. A
correção é forçar análise da faixa antes de decompilar:

```python
ida_auto.plan_and_wait(f.start_ea, f.end_ea)      # <- o que faltava
cf = ida_hexrays.decompile(f.start_ea)
```

`plan_and_wait` retorna `1` em ~0,1 s por função. Não precisa de `auto_wait()` global,
que é justamente o que travava.

Detalhes operacionais medidos:

- `-A` + `-S` sem `auto_wait` é o modo correto; `auto_wait()` não é necessário e não deve
  ser usado.
- `qexit(0)` não encerra na hora; o processo fica vivo depois do script. Rodar com
  deadline e matar depois do `DONE` funciona (o texto já foi gravado e tem `flush`).
- sobra um `soothe3_pe.dll.$$$` (250 MB) na pasta de trabalho; é lixo do IDA, apagável.

### 19.3 Resultado — cluster decompilado

Comando: `decomp_cluster.py` (RVAs do §15.1 + `0x8C3F10`). Saída em
`docs/engine/decomp/ida_XXXXXXXX.c`, log em `checks/ida_cluster.txt`.

| RVA | Bytes | chars do decompilado | arquivo |
|---|---:|---:|---|
| `0x8BF650` | 1.411 | 8.337 | `ida_008BF650.c` |
| `0x8BFBE0` | 199 | 1.263 | `ida_008BFBE0.c` |
| `0x8BFD30` | 1.275 | 7.429 | `ida_008BFD30.c` |
| `0x8C0230` | 177 | 947 | `ida_008C0230.c` |
| `0x8C02F0` | 2.079 | 12.333 | `ida_008C02F0.c` |
| `0x8C0B10` | 177 | 947 | `ida_008C0B10.c` |
| `0x8C0BD0` | 2.150 | 13.168 | `ida_008C0BD0.c` |
| **`0x8C1440`** | **7.800** | **44.464** | `ida_008C1440.c` |
| `0x8C32C0` | 266 | 1.559 | `ida_008C32C0.c` |
| `0x8C33D0` | 2.117 | **0 — falhou** | `ida_008C33D0.c` (só o cabeçalho) |
| `0x8C3C20` | 465 | 2.418 | `ida_008C3C20.c` |
| `0x8C3E00` | 266 | 1.558 | `ida_008C3E00.c` |
| `0x8C3F10` | 952 | 4.694 | `ida_008C3F10.c` |
| **`0x8C5FD8`** (gêmeo) | 19.289 | **116.125** | `ida_008C5FD8.c` |

Total ≈ 216.000 caracteres de decompilado onde antes havia 0.

**Validação cruzada imediata:** `ida_008C3C20.c` reproduz o §16.1 sem divergência —
`*(int *)(a1 + 1024)` = `count`, `*(int *)(a1 + 1028)` = `length`, coeficiente `0.1f`,
laço direto desenrolado de 4 em 4 e o traseiro começando em `length − 2`. O que o
`show_func.py` tinha dado por leitura manual, o Hex-Rays confirmou.

**Primitivas vetoriais dentro de `0x8C1440` — contadas do decompilado.** O Hex-Rays não
resolve os destinos dos thunks (aparecem como `unk_1800010xx`), mas o endereço está lá e a
tabela do §17 dá a operação. As 45 chamadas indiretas se distribuem assim:

| thunk | vezes | operação (§17) |
|---|---:|---|
| `0x10D0` | 12 | preencher com constante |
| `0x1370` | 9 | `+=` escalar |
| `0x1580` | 5 | soma de array |
| `0x1100` | 4 | clamp |
| `0x1550` | 4 | recíproco |
| `0x1220` | 4 | `*=` escalar |
| `0x11F0` | 4 | FMA in place |
| `0x8CAFD0` | 3 | função própria do cluster (não é thunk IPP) |

Ou seja: `0x8C1440` é **set-up de buffers + aritmética por banda**, não um kernel único.
Comparado com `0x8B3ED0` (22 multiplicações, 12 clamps, 3 dot, 4 recíprocos, 2 somas),
aqui predominam `fill` e somas — o que é coerente com "montar/encerrar estado", não com
"calcular ganho". `0x8C02F0` usa só 4 (`0x11C0` subtração ×2, `0x1250` clamp vetorial,
`0x1100`) e `0x8C0BD0` usa 11.

**Pendência:** `0x8C33D0` decompila com corpo **vazio** (sem exceção; `decompile_func`
devolve cfunc sem texto). Desmontagem de `0x8C33D0` é normal (`show_func.py` lê o
prólogo: `mov eax,0x1090` / `call 0x17978C0` / `sub rsp,rax`). Ler por instrução até
achar a causa; não presumir que a função é vazia.

> **Regra do §1 continua valendo:** decompilado é **leitura**, não prova. Toda fórmula que
> entrar no `dsp-spec.md` precisa de desmontagem + RVA por linha, como no §18.

### 19.4 Correção do §17.4 — alvo de dispatch ≠ implementação

A tabela do §17.4 lista a implementação **interna**; `checks/core_vector_calls.txt`
listava o **alvo do `jmp [tabela]`**. Resolvido lendo a tabela e o wrapper:

| thunk | tabela | alvo (idx 4) | cadeia |
|---|---|---|---|
| `0x1400` | `0x21C6288` | `0xAC20` | `call 0x5F5C0` |
| `0x1430` | `0x21C62C8` | `0xADA0` | `call 0xC560` → `call 0x63640` |
| `0x1550` | `0x21C6448` | `0xC560` | `call 0x63640` |
| `0x1580` | `0x21C6488` | `0xCCE0` | `call 0x65EA0` |
| `0x11F0` | `0x21C5FC8` | `0x5BC0` | — |
| `0x1010` | `0x21C5D48` | `0x20E0` | `call [rcx]`, `call [rax+0x18]` |
| `0x1340` | `0x21C6188` | `0x9BA0` | — |

Nenhum dos dois documentos estava errado; faltava dizer que há um hop de wrapper. Fica
registrado para não se "corrigir" um contra o outro.

### 19.5 Estado do diretório — **arquivos sumiram durante a sessão**

Fato observado, sem interpretação:

| Momento | Conteúdo da raiz |
|---|---|
| início desta sessão | `app/ attachments/ capture/ checks/ docs/ dumpsooth/ inbox/ investigation.cany/ pinned/ reference/ tools/` + `PLANO_MOTOR_AUDIO.md`, `agent-session.jsonl`, `build-activity.log`, `craft.json`, `feed.json`, `questions.json`, `usage.json` |
| após **2026-11-22 08:08:48** | `docs/ dumpsooth/ tools/ PLANO_MOTOR_AUDIO.md` |

- `app/` inteiro desapareceu: `src/dsp/*`, `src/vst3host.rs`, `src/calibrate.rs`,
  `equivalence/*`, `dist/Resonia.vst3`, `Cargo.toml`.
- `checks/` inteiro desapareceu (todos os artefatos dos §14–§18).
- A pasta foi recriada só com os arquivos novos desta sessão (`ida_cluster.txt`,
  `ida_extra.txt`, `ida_test.txt`).
- **Não estão na lixeira** (`D:\$RECYCLE.BIN` só tem entradas de `D:\PROJETOS\vst3dec`,
  `RtsPixel` etc.).
- Busca por `vst3host.rs` em todo `D:\PROJETOS`: **nenhum resultado**.
- Sobreviveram: `dumpsooth/` (os 3 arquivos, intactos), `docs/engine/` (CSVs, `decomp/`,
  `dsp-spec.md`), `tools/` (todos os scripts).

**Consequências para este plano:**

1. §15.3 cita `app/equivalence/original-curves.tsv`, `original-parameters.txt` e
   `score-check.md` — **não existem mais**. As medições do oráculo foram perdidas; o
   número de latência (2.304 amostras @ 48 kHz) fica como registro histórico, não como
   artefato.
2. A Fase 4 (oráculo) precisa ser refeita do zero, e a Fase 5 (port) também: não há
   código Rust para substituir.
3. Todo o §18 depende de `checks/_8b3ed0.dis`, `checks/core_vector_calls.txt` e
   `checks/vector_primitives.txt`, que sumiram. Os geradores existem
   (`tools/vector_primitives.py`, `tools/core_vector_calls.py`, `tools/show_func.py`) e
   reproduzem os artefatos.

**Causa:** desconhecida por mim. Não apaguei nada além de um arquivo inexistente
(`checks/ida_cluster.txt`, `Remove-Item` com `-ErrorAction SilentlyContinue`). O evento
precede a primeira gravação desta sessão.

### 19.6 O que regenerar (barato)

```powershell
py -3 tools/thunk_map.py        # -> checks/thunk_map.txt
py -3 tools/imports_dump.py     # -> checks/imports_dump.txt
py -3 tools/vector_primitives.py# -> checks/vector_primitives.txt
py -3 tools/core_vector_calls.py# -> checks/core_vector_calls.txt
py -3 tools/show_func.py 0x8B3ED0 > checks/_8b3ed0.dis
```

### 19.7 `soothe3_loadable.dll` — o artefato do oráculo, e o porquê de não carregar

O `dumpsooth/soothe3_loadable.dll` (137.003.008 B, SHA-256
`B7D9426689C61B5DEF422562110CE7BE2269348A300DCF98CBE6C86F1EE40694`, 21/11 23:08:33) é o
dump repachado por `tools/make_loadable.py` para a base real em que foi capturado:

| campo | `soothe3_unpacked.dll` | `soothe3_loadable.dll` |
|---|---|---|
| `ImageBase` | `0x180000000` | `0x199B0000` |
| diretório `BASERELOC` | `0x79D5000` / `0x20` | `0` / `0` (limpo) |
| `DllCharacteristics` | `0x120` (sem `DYNAMIC_BASE`) | `0x120` |

Exporta o que um VST3 precisa: `GetPluginFactory`, `InitDll`, `ExitDll` (236 exports, o
resto é lixo `?dvs_…_mfort6317_`).

**Mas não carrega.** Medido em 2026-11-22, duas formas independentes:

```
py -3 tools/load_probe.py dumpsooth\soothe3_loadable.dll
  loading …
  exit = -1073740791  (0xC0000005, violação de acesso) — morre dentro de LoadLibraryW,
                                                          antes de devolver o handle

py -3 -c "ctypes.CDLL(...)"
  exit = -1073740791  (0xC0000005)
```

**Onde está o problema — diagnóstico de bandeira:**

```
LoadLibraryExW(..., LOAD_LIBRARY_AS_DATAFILE)       -> ok, não crasha
LoadLibraryExW(..., LOAD_LIBRARY_AS_IMAGE_RESOURCE) -> ok
LoadLibraryExW(..., DONT_RESOLVE_DLL_REFERENCES)    -> ok
```

`AS_DATAFILE` não roda `DllMain` nem resolve import. Ou seja: **a imagem em si mapeia
normalmente**; o crash está no caminho de inicialização (`DllMain` / entry point), não no
layout.

Pistas no header que explicam:

- `SizeOfHeapReserve = 0x199B0000` (429 MB) e `SizeOfStackReserve = 0x6512722`
  (~100 MB). Valor normal de DLL é `0x100000`/`0x100000`. São valores de dump, não de PE.
- O entry point `0x79CDEA0` vive em `.text001` (0x1400 B), junto com `.oldrel`, `.proxy`,
  `.guard`, `.reloc` de 0x200 B. O corpo chama por IAT (`call [rip+…]` para
  `0x79CF140`, `0x79CF118`, `0x79CF110`, `0x79CF130`, `0x79CF108`) e faz init de
  globais em `.data001`. É stub de packer, feito para rodar uma única vez, no processo
  original.

**Consequência:** o oráculo não é "carregar e tocar". São duas rotas possíveis, ambas
ainda não feitas:

1. **Loader manual**: mapear a imagem (o `AS_DATAFILE` já prova que mapeia), resolver a
   IAT na mão e chamar `GetPluginFactory` **sem** rodar `DllMain`. Read-only, sem patch,
   sem hook.
2. Usar um **host VST3 de verdade** (o mesmo papel que o `app/src/vst3host.rs` fazia,
   que sumiu).

De qualquer forma isso é o **passo 7 do §20**, é validação, e **não é pré-requisito da
extração**: nenhum coeficiente sai daqui.

Nada disso depende de `app/`.

---

## 20. Novo plano de ataque (2026-11-22, revisão 4)

Substitui o §12.7, a ordem do §9 e a revisão 2. Critério: **o que destrava mais prova
por hora**. Revisão 3 incorporou o §22 (leitura de `0x8C1440`, `0x8C02F0`, `0x8C0BD0`);
a **revisão 4** detalha cada passo em folha de execução no **§23** (comando, saída exigida
e critério de saída), corrige as ferramentas do IDA (§23.0) e corrige um erro meu de região
no §22.5.

| # | Passo | Estado | Por quê | Custo |
|---|---|---|---|---|
| 1 | Ler `0x8C1440` no decompilado do IDA | **FEITO** | 1.653 linhas; 45 thunks, 23 `case`, padding de 16 B — **montagem de buffer, não kernel** (§19.3) | — |
| 2 | Ler `0x8C02F0` e `0x8C0BD0` | **FEITO** | os dois são plumbing; `0x8C0BD0` tem a cadeia recíproco+clamp+FMA por descritor (§22) | — |
| 3 | **`0x8B2C30`** (1.163 B chain-aware) | **FEITO** | FIR de **32 taps** variante no tempo (scatter-add em anel de 32), kernel em `ctx+0x40` copiado por `0x8803CE`. §23.4 | — |
| 4 | **`0x8CAE90`** (307 B chain-aware) | **FEITO** | MAC em lotes de bandas; revelou que `0x1580` é MAC com FMA, não soma (§23.1, spec §11) | — |
| 5 | **Fixar a ordem dos argumentos** de `0x63640` (divisão) e `0x5BC0` (FMA) | **FEITO** | 9 primitivas provadas em §17.6; corrigidos 4 rótulos do plano | — |
| 6 | **Struct de bandas**: lista de descritores de 24 B (`+8` ponteiro, `+16` tipo, passo 24) | aberto | é a primeira estrutura de bandas vista; liga o DSP aos params | médio |
| 7 | **`0x8BF650` + `0x8BFD30`** (8,3 e 7,4 mil car.) | aberto | completam o cluster; `0x8BF650` chama `0x8CAB40` | baixo |
| 8 | **Fechar `0x8C33D0`** por desmontagem | aberto | único que o Hex-Rays não entregou; `plan_and_wait` já corrigido (§23.0) | baixo |
| 9 | **Tipo de filtro**: `0x87BB60` → `0x882FC0`; `0x87E220` (`powf` 2.4/−4.8) | aberto | último grande buraco de arquitetura (§12.2 item A) | médio |
| 10 | **Struct de estado** `ctx+0x2C38 / +0xBFF8 / +0x5F8 / +0x5ED0` + mapa dos 143 params | aberto | sem isso o port não conecta entrada a saída | médio |
| 11 | **Oráculo**: host mínimo + WAV de referência | **FECHADO 2026-11-24** | `host/` + `host/test/out_soothe3.wav` (§15.3); latência 2304, saída depende do bloco, não transparente. `soothe3_loadable.dll` não carrega (§19.7) | — |
| 12 | **Port Rust** dentro do Resonia | — | só depois de 3–10; latência só depois de medir no 1.0.6 (o 2.304 @48k é do 1.0.5) | alto |

A **ordem de execução** está no §23.12; a numeração desta tabela é só inventário.

O passo 11 é **validação**, não extração: nenhum coeficiente sai dele. É independente de
3–10 e pode correr em paralelo. Mas hoje está **bloqueado por diagnóstico**, não por
trabalho: o `LoadLibraryW` morre em `0xC0000005` dentro do `DllMain`, e a imagem em si
mapeia (§19.7).

**Regra de leitura valendo a partir de agora:** decompilado é leitura. Toda fórmula que
vierar de `0x8C0BD0` só entra no `dsp-spec.md` depois de transcrita do impl da primitiva,
instrução por instrução (§22.3).

---

## 21. Sincronização de documentos (dívida aberta)

| Documento | Estado | O que falta |
|---|---|---|
| `PLANO_MOTOR_AUDIO.md` | sincronizado (revisão 4: §0, §10, §11, §19.7, §20, §22, §23) | — |
| `LEMBRAR DISSO.md` | **âncora, congelada** | SHA-256 `D10EB333C140FC4800B06C6CA234171B62EDA7348872E33C88BDA378B7BECE49` |
| `docs/engine/dsp-spec.md` | **atrasado** | §16.2 (`0x8C3F10`), §16.3 (`0x1C84D0` = potência), §16.5, §17.5, **§18 inteiro** (as 4 tabelas de 16 taps), §19, §20, §22 e §23 |
| `app/MECHANICS.md` | **inexistente** | o arquivo sumiu com `app/` (§19.5); o que ele dizia sobre o motor já estava refutado (§15.5) |
| `docs/engine/phase2-notes.md` | ok | — |
| `archive/agent2/` | **novo** | 319 scripts + 6 unidades MASM + bundle oráculo 1.0.5, resgatados do Temp (§19.8) |

Regra: `dsp-spec.md` só recebe o que tem RVA. O decompilado do §19.3 é **leitura**; entra
no spec apenas depois de conferido instrução por instrução.

---

## 22. Leitura do cluster — o que `0x8C02F0` e `0x8C0BD0` realmente são (2026-11-22)

Decompilados lidos: `ida_008C02F0.c` (593 linhas) e `ida_008C0BD0.c` (497 linhas).
Sem novas suposições: só o que está no decompilado, com o RVA da função.

### 22.1 Conclusão em uma linha

**Os dois são plumbing de buffer, não kernel.** Os dois alocam na arena
(`*(_QWORD *)a5 + 4 * offset`, com arredondamento de 16 B em `a5+24`), copiam blocos de
128 bits, e chamam primitivas vetoriais IPP. A conta por banda está nos **callees** e nos
**thunks**.

### 22.2 `0x8C02F0` — 2.079 B, 9 `call`

| linha do decomp. | o quê |
|---|---|
| 180–212 | copia 8×128 b do buffer de entrada para o quadro local |
| 213 | `unk_181798F42(dst, 0, 1016)` — zero de 1.016 B (CRT) |
| 219–235 | **aloca `v23` ponteiros** na arena `a5` (passo de 16 B) |
| 306–325 | se `count == a1[8]` (modo por banda): `unk_1800011C0(v155[i], v179[i], ·, v21)` |
| 326–341 | senão, se `a1[8] == 1` (modo só uma): `unk_1800011C0(v155[0], v179[i], ·, v21)` |
| 343 | zero de 1.016 B |
| 349–365 | **aloca outro vetor de ponteiros** na arena |
| 421–431 | `unk_180001250(v155[i], v179[i], v61)` — clamp entre dois vetores |
| 459–469 | `unk_180001100(*v100++, v21, v62, 0)` — clamp escalar, modo 0 |
| **531** | **`sub_1808CAE90(&v164, v179, &v155)`** ← o trabalho real |
| **592** | **`sub_1808CAE90(&v155, v179, &v164)`** ← segunda passada |

Primativas: `0x11C0` (subtração vetorial, §17) ×2 por banda, `0x1250` (clamp vetorial) ×1,
`0x1100` (clamp escalar) ×1. Nada de constante float própria.

**`0x8CAE90` tem 245 B** (`functions.csv`) e é o próximo alvo de leitura — é quem
transforma os dois buffers.

### 22.3 `0x8C0BD0` — 2.150 B (chain-aware), 14 `call`

Estrutura: `if ( *(int *)(a1 + 1024) != 1 )` → loop `for (i = *a3; v7 != a3[1]; )` com
passo `v7 += 24` (linha 495), e dentro um bloco `if ( *(int *)(v7 + 16) == 2 )`
(linha 150). Ou seja: **percorre uma lista de descritores de 24 B e age nos que têm o
campo `+16 == 2`**. Cada descritor tem um ponteiro em `+8` (linha 163).

A cadeia aritmética, na ordem em que aparece:

| linha | primitiva | semântica (§17) |
|---|---|---|
| 290 / 305 | `unk_180001190` | multiplicação **in place** (impl `0x4BC0`) |
| 350 | `unk_1800010D0` | preencher |
| 357 | `unk_180001370` | `+=` escalar |
| 389 | `unk_1800010D0` | preencher |
| 396 | `unk_180001370` | `+=` escalar |
| 401 | `unk_180001100` | clamp escalar, **modo 0 = max** |
| 408 | `unk_180001550` | **recíproco** (impl `0x63640`) |
| 443 | `unk_180001220` | `*=` escalar (in place) |
| 477 / 485 | `unk_1800011F0` | **FMA in place** (impl `0x5BC0`) |

É a **única função do cluster com recíproco + FMA + clamp juntos**, e percorre
descritores — coerente com "calcula o ganho de cada banda". **Mas a ordem exata dos
argumentos de cada primitiva ainda é leitura, não prova**: falta abrir o impl de cada
uma (`0x4BC0`, `0x2F60`, `0xA120`, `0x3480`, `0x63640`, `0x6160`, `0x5BC0`) e transcrever
instrução por instrução, como foi feito em §17.2/§18.2.

### 22.4 Correção de rota que isso implica

O §15.1 diz que a conta por banda está nos callees. Confirmado por leitura: **os wrappers
do cluster não têm constante float nenhuma**; eles só montam buffers e chamam. Onde
procurar agora:

1. `0x8CAE90` (245 B) — callee de `0x8C02F0`.
2. Os impls das primitivas que `0x8C0BD0` usa, em especial `0x63640` (recíproco) e
   `0x5BC0` (FMA), para fixar a ordem dos argumentos.
3. A lista de descritores de 24 B (`v7 += 24`, campo `+16 == 2`, ponteiro em `+8`) — é a
   estrutura de bandas, e está **mais perto** do mapa de params do que qualquer coisa
   vista até agora.

### 22.5 Densidade aritmética por função — e uma correção minha

`tools/find_kernels.py` (todas as funções, `MAX_SIZE` e `TOP` como argumentos) e
`tools/reach_kernels.py` (só as alcançáveis do núcleo, via `xrefs.csv`).

**Correção (2026-11-22, mesma sessão):** a primeira versão desta seção dizia que os RVAs
abaixo eram "os mais densos da região do DSP". **Errado.** Eles têm **5 dígitos**
(`0x08A980`, `0x08B660`, `0x08C280`…) — estão em `0x8A000–0x8D000`, a ~570 KB, que é a
**região da biblioteca IPP/matemática**, não o cluster do DSP, que fica em `0x8B0000–
0x8D2000` (~9 MB). Eram kernels do IPP, onde FMA e constante float são o esperado. A nota
anterior que dizia que `0x8B660` caía dentro de `0x8B3ED0` era absurda: `0x08B660` =
570.976, `0x8B3ED0` = 9.126.610.

Lição registrada: **RVA de 5 dígitos e RVA de 6–7 dígitos são regiões diferentes.** Conferir
o número de dígitos antes de comparar.

Varredura correta, **chain-aware** e com instruções deduplicadas
(`tools/scan_region.py 0x8A0000 0x8E0000`, novo): **655 entradas `.pdata`, 60.951
instruções únicas, zero FMA, 90 `mulss`, 57 `addss`, 50 `subss`, 19 `divss`.** A conta é
escalar, escrita à mão — coerente com banco de filtros no tempo:

| RVA (chain-aware) | bytes | insns | mul | add | sub | fma | call | leitura |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`0x8B2C30`** | **1.163** | 300 | **27** | **27** | 0 | 0 | **0** | **kernel candidato**: `mul` = `add`, ~300 instruções, **zero chamadas**. `mov rax,[rcx+0x80]`, `and r8,~3`, `ebx=0x1f` → linha de atraso circular de 32 posições, soma ponderada |
| `0x8B3ED0` | 20.209 | 4.473 | 23 | 3 | 17 | 0 | 127 | o núcleo (bate com o §15.1) |
| `0x8C5C40` | 20.209 | 4.473 | 23 | 3 | 17 | 0 | 127 | **gêmeo**: corpo idêntico ao do núcleo, mesma contagem. O gêmeo *começa* em `0x8C5C40`; `0x8C5FD8` é o fragmento do meio (é o que a âncora cita) |
| `0x8C3C20` | 465 | 109 | 10 | 10 | 10 | 0 | 0 | o one-pole, agora com tamanho chain-aware (465 B, não 266) |

**Trampa do `functions.csv`:** os tamanhos são de `.pdata` e mentem no núcleo.

| RVA | tamanho no CSV | chain-aware (`show_func.py`) |
|---|---:|---:|
| `0x8B3ED0` | **49 B** | **20.209 B** (`0x8B3ED0–0x8B8DC1`) |
| `0x8B4268` | 17.290 B | 19.289 B (fragmento: começa no meio do corpo) |
| `0x8B2C30` | 37 B | 1.163 B |
| `0x8B2C55` | 578 B | 1.126 B (fragmento de `0x8B2C30`) |

Qualquer ranking por tamanho do CSV subestima o núcleo em ~400×. **Para o núcleo, sempre
`tools/show_func.py` / `tools/scan_region.py` (chain-aware), nunca `functions.csv` sozinho.**

`xrefs.csv` é **latin1**, não UTF-8 — abrir com `encoding='latin1'`.

O `reach_kernels.py` só achou **98** funções alcançáveis do núcleo e **1** com aritmética —
o grafo não captura os calls indiretos (o kernel de `0x8B2C30` não aparece nele). Rota
descartada.

---

## 23. Próximas etapas — folha de execução (2026-11-22, revisão 4)

Ordem por **o que destrava mais prova**. Cada etapa diz o que abrir, o que provar e qual é
o critério de saída. Nenhuma etapa se declara pronta por leitura: só por instrução com RVA.

### 23.0 Estado das ferramentas (corrigido nesta revisão)

Três falhas que fariam a próxima sessão repetir trabalho perdido:

| Arquivo | Defeito | Correção aplicada |
|---|---|---|
| `tools/ida/run_batch.ps1` | abria `ida_run\soothe3_unpacked_mem.bin` — o **dump de memória cru** (136.990.720 B), não o PE. Foi a causa raiz dos batches vazios (§19) | agora abre `ida_pe\soothe3_pe.dll.i64`, o DB já analisado |
| `tools/ida/decompile_batch.py` | não chamava `ida_auto.plan_and_wait` — `.pdata` cria a função mas não desmonta o corpo, então o Hex-Rays devolve corpo vazio (a âncora chama isso de `JUMPOUT`) | chama `plan_and_wait(fn.start_ea, fn.end_ea)` quando a função ainda não tem instruções |
| `tools/ida/decompile_batch.py` | gravava `%08X.c`, **colidindo** com a saída do Ghidra (`808B3ED0.c`, `80879CF0.c`…), que seriam sobrescritos | grava `ida_%08X.c`, como os 13 arquivos do cluster |

> `soothe3_pe.dll.i64` **é** o banco do PE normalizado `ida_pe\soothe3_pe.dll` — não é o
> `.bin` de memória cru que a âncora proíbe. Abrir o `.i64` só evita reparsear as 30.859
> funções. Se o banco for apagado, o `normalize_dump.py` + o PE regeneram tudo.

### 23.1 Etapa A — `0x8CAE90` — **FEITO: MAC em lotes de bandas** (2026-11-22)

Estado: **FEITO**. Cinco itens da regra de entrega em `dsp-spec.md` §11. Desmontagem
chain-aware em `checks/8cae90.dis` (307 B, **não** 245 B — o `.pdata` mentiu de novo),
pseudocódigo comentado em `docs/engine/decomp/manual_008CAE90.c`, chamador em
`checks/8c02f0.dis`.

**(a) RVA:** `0x8CAE90..0x8CAFC3`, 307 B, 80 instruções. Chamado 2× por `0x8C02F0`
em `008C099C` e `008C0AE5`.

**(b) Assinatura + calls:**

```c
void batch_mac(Set16* dst /*rcx*/, Set128* a /*rdx*/, Set16* b /*r8*/)
```

| RVA do call | Alvo | Argumentos (ordem provada) |
|---|---|---|
| `008CAEFE` | `0x1580` | `rcx=a[i]`, `rdx=b[i]`, `r8=dst[i]`, `r9d=dst->len` |
| `008CAF4D` | `0x1580` | `rcx=a[i]`, `rdx=b[0]`, `r8=dst[i]`, `r9d=dst->len` |
| `008CAF9E` | `0x1580` | `rcx=a[0]`, `rdx=b[0]`, `r8=dst[i]`, `r9d=dst->len` |

**(c) Constantes:** **zero constantes float próprias** — `findstr rip checks\8cae90.dis`
devolve 0 linhas. Único imediato: `1` em `008CAF12`/`008CAF1B`/`008CAF5E`/`008CAF65`/
`008CAF6F` (broadcast).

**(d) Structs:** `Set16` = 16 ptr (`+0x00..0x7F`, passo 8 em `008CAF03`) + `int n`
(`+0x80`, `008CAEC8`) + `int len` (`+0x84`, `008CAED8`) = 0x88 B. `Set128` = 128 ptr
(`+0x00..0x3FF`, passo 8 em `008CAF52`) + `int n` (`+0x400`, `008CAEA2`) = 0x404 B.
No chamador, `Set16` em `[rbp+0x340]` e `[rsp+0x30]`, `Set128` em `[rbp+0xB60]`
(`008C0917`, `008C0921`, `008C092B`, `008C0A76`, `008C0A82`, `008C0A8C`).

**(e) Rust:** `dsp-spec.md` §11.5.

**Correção material:** `0x1580` NÃO é "soma" (como dizia §9.3 do spec). É MAC in place:
`0x1580 → 0xCCE0 (tabela 0x21C6488[4], seletor 0x21C7408=4) → 0x65EA0 → 0x6CE80`,
com `0006CEBB vfmadd213ps ymm1,ymm0,[r8]` e store em `[r8]`. Variante escalar `0xC620`
(tabela[0]): `0000C6A0 movss` / `0000C6A5 mulss` / `0000C6AA addss` / `0000C6B0 movss`.
Ordem: `(src1=rcx, src2=rdx, dst_acumulador=r8, len=r9d)`. O nome IPP continua
**NÃO PROVADO** (§14.3). A tabela de classes do §14.3 está corrigida em consequência.

**Observação para o port:** o caminho de áudio passa por FMA dentro de `IPPCODE` — o
"0 FMA" da varredura cobre só `0x8A0000–0x8E0000`, não a seção IPP. Reproduzir
`mulss`+`addss` separados **não** bate bit-a-bit com a variante selecionada.

### 23.2 Etapa B — ordem dos argumentos das 9 primitivas — **FEITO (2026-11-22)**

Estado: **FEITO**. As 9 linhas com proto, registradores e instrução que prova estão em
`dsp-spec.md` §17.6. Desmontagens em `checks/{c560,5bc0,4bc0,2f60,a120,3480,6160,50e0,69c0,63640,1d2e9e0,26640}.dis`.
Mapeamento thunk→impl provado pela tabela de despacho `0x21C5xxx[4]` com seletor
`0x21C7408 = 4` (§24): `0x11C0 → 0x50E0` (tabela `0x21C5F88`) e `0x1250 → 0x69C0`
(tabela `0x21C6048`) — antes constavam como "—" nesta tabela.

| thunk | impl | proto provada | correção sobre o rótulo antigo |
|---|---|---|---|
| `0x1550` | `0xC560`→`0x63640` | `(den=rcx, num=rdx, dst=r8, n=r9d)` | é **divisão** com refinamento, não recíproco puro |
| `0x11F0` | `0x5BC0` | `(src=rcx, escalar=xmm1, dst=r8, n=r9d)` | escalar em xmm1; `rdx` é só contador |
| `0x1190` | `0x4BC0` | `(a=rcx, b=rdx, dst=r8, n=r9d)` | dst separado — **não é in place** |
| `0x10D0` | `0x2F60` | `(dst=rcx, n=edx)` | zero-fill por `vxorps`, valor não é argumento |
| `0x1370` | `0xA120` | `(src=rcx, dst=rdx, n=r8d)` | adição de vetores — **não é escalar** |
| `0x1100` | `0x3480` | `(dst=rcx, n=edx, bound=xmm2, modo=r9d)` | modo 0=max, 4=min (confirmado) |
| `0x1220` | `0x6160` | `(dst=rdx, escalar=xmm0, n=r8d)` | in place (confirmado §18.2) |
| `0x11C0` | `0x50E0` | `(a=rcx, b=rdx, dst=r8, n=r9d)` | `dst=b−a`, ordem rdx−rcx; dst separado |
| `0x1250` | `0x69C0` | `(src=rcx, dst=rdx, n=r8d, bound=xmm3, modo=[rsp+0x30])` | vetor contra escalar, não entre vetores |

**Critério de saída atendido:** 9 linhas preenchidas com instrução + RVA, nenhuma inferida
de nome. A cadeia de `0x8C0BD0` (§22.3) deixa de ser leitura e passa a ser prova.

### 23.3 Etapa C — a lista de descritores de 24 B — **FECHADA (2026-11-23)**

> **Histórico (não apagado):** a revisão de 2026-11-22 dizia "LEITURA PROVADA; escritor
> `NÃO PROVADO`". A leitura daquela revisão continua válida e está preservada abaixo em
> "Leitura (2026-11-22)". O que faltava — escritor, alocador, contagem e seleção — está
> provado nesta revisão. **CORRIGIDO em 2026-11-23:** `[ctx+0x10]` **não** aponta para um
> par de 16 B; aponta para um `std::vector` de 24 B `{begin, end, cap}` (3 ponteiros; o
> alocador grava o `cap` em `008563EC6`).

#### Leitura (2026-11-22)

**Par em `[ctx+0x10]`** (ponteiro para `{begin,end}` de 16 B):

| Offset | Prova |
|---|---|
| `+0x00` = `begin` | `008C0C1F mov rsi,[r8]`; `008BFDA0` |
| `+0x08` = `end` | `008C0C0D mov rax,[r8+8]`; `008BFD9C` |

**Descritor (stride `0x18` = 24 B):**

| Offset | Prova |
|---|---|
| `+0x00` i32 campo A | `008BFDB4 mov r8d,[r15]` (lido no consumidor `0x8BFD30`) |
| `+0x08` i32 índice | `008C0CDA movsxd rax,[rsi+8]` → `008C0CE6 lea rax,[rax*8]` |
| `+0x10` i32 tipo | `008C0C90 cmp dword [rsi+0x10],2` (discriminador ativo = 2) |
| `+0x14..0x17` | `NÃO EXTRAÍDO` |

**Consumidor `0x8C0BD0`:** `008C0C01 r14=a1`; `008C0C26 salva end`; `008C0C2F cmp rsi,rax`
(loop `begin != end`); `008C0CDE lea r8,[rbp-0x60]`; `008C0CEE sub rax,r8` e `008C0CF1 lea
r8,[rax+r14]` (destino = `r14 + idx*8 - temp`); `008C13C9 recarrega end`; `008C13CD add
rsi,0x18`; `008C13D6/D9 cmp/jne` fecha o loop.

**Chamadores:** `0x8B3ED0` (chain-aware; `.pdata` reporta `0x8B4268`) em `008B6046 mov
r8,[r13+0x10]` e `008B605C call 0x8c0bd0`, com `r13=rcx` desde `008B3F14` e `ctx=[outer+8]`
em `008ABCE3`; gêmeo `0x8C5FD8` em `008C7DB6`/`008C7DCC`. Segundo consumidor `0x8BFD30`:
`008BFEBF movsxd rax,[r15+8]`, `008BFF97 add r15,0x18`.

**Correção ao relatório do agente:** ele citou `008BFE99` como confirmação do `cmp ...,2`.
A instrução real em `008BFE99` é `mov r8d,[r15+0x10]` (leitura do campo tipo); o `cmp` com
`2` existe só em `008C0C90`.

**Constantes com RVA:** `2` (`008C0C90`), `0x18` (`008C13CD`, `008BFF97`), `0x3F8`
(`008C0CAB`), `1.0f` `0x2079F9C` (`008C0C73`), `1.1920929e-07` `0x2079CF0` (`008C0C85`).
O padrão `lea edx,[rax+rax*2]/shl edx,3` em `008E2D41/47` está no parser de fontes BDF
(`STARTFONT`, `008E2B50`) — **rejeitado**, sem ligação.

#### Escritor, alocador e contagem — PROVADO (2026-11-23)

**A. Quem escolhe a tabela e grava `E+0x18` / `E+0x20`.**

`0x862E40` é a fábrica do motor: aloca `E` com `new(0xC1A8)` (`00862E52 mov ecx,0xC1A8`;
`00862E5D call 0x1796CF4`) e chama o construtor `0x8634A0` (`00862E72`) com `arg2 = rcx`
original e `arg3 = rdx` original (`00862E5A mov rbx,rdx`; `00862E65 mov r8,rbx`).

```
0x8634A0 (ctor de E)
008634CD  mov [rcx],rdx              ; E+0 = arg2
008634D7  mov [rcx+8],rbx            ; E+8 = arg3
008634FB  mov ecx,[r8]               ; caso A = dword [arg3+0]
008634FE  call 0x85E6C0
00863503  mov [r14+0x18],rax         ; E+0x18 = ponteiro do vetor A
00863507  mov ecx,[rbx+8]            ; caso B = dword [arg3+8]
0086350A  call 0x85E6C0
00863535  mov [r14+0x20],rax         ; E+0x20 = ponteiro do vetor B
```

**B. Quem grava `[ctx+0x10]` / `[ctx+0x18]`.**

```
0x8634A0
008638D6  lea rcx,[r14+0x5F8]        ; objeto em E+0x5F8; ctx = E+0x600
008638EC  mov rax,[r14+0x20]         ; E+0x20
008638F0  mov [rsp+0x30],rax         ; 7º arg de 0x86A4E0
008638F5  mov rax,[r14+0x18]         ; E+0x18
00863900  mov [rsp+0x28],rax         ; 6º arg de 0x86A4E0
00863929  call 0x86A4E0

0x86A4E0 (construtor do ctx; rbp = entry_rsp − 0x3F em 0086A4F8)
0086A503  mov rsi,[rbp+0x67]         ; 0x67−0x3F = 0x28 → 5º arg
0086A518  mov rbx,[rbp+0x6F]         ; 0x6F−0x3F = 0x30 → 6º arg = [E+0x18]
0086A530  mov [rcx],rsi              ; E+0x5F8 = 5º arg
0086A533  add rcx,8                  ; this = E+0x600
0086A526  mov [rsp+0x38],rbx         ; 8º arg de 0x86FE90
0086A521  mov [rsp+0x40],rdi         ; 9º arg de 0x86FE90 (= [E+0x20])
0086A54B  call 0x86FE90

0x86FE90 (ctor do ctx; rbp = entry_rsp − 0x408 em 0086FEA8)
0086FF03  mov rax,[rbp+0x448]        ; 0x448−0x408 = 0x40 → 8º arg
0086FF0A  mov [rcx+0x10],rax         ; ctx+0x10 = vetor A
0086FF0E  mov rax,[rbp+0x450]        ; 9º arg
0086FF15  mov [rcx+0x18],rax         ; ctx+0x18 = vetor B
```

`arg8`/`arg9` do ctor são o 6º/7º arg de `0x86A4E0`, que por sua vez são `[E+0x18]`/`[E+0x20]`.
Isso fecha os dois ponteiros.

**C. Quem escreve os campos `+0/+8/+0x10` — `0x85E6C0`.**

`0x85E6C0` é um `switch` de 23 posições: `0085E6CE cmp ecx,0x16`; `0085E6E1 mov
ecx,[rdx+rax*4+0x85FFA0]` (tabela em `0x85FFA0`, entradas absolutas; `rdx = 0` por
`0085E6DA lea rdx,[rip-0x85E6E1]`); `0085E6E8 add rcx,rdx`; `0085E6EB jmp rcx`.

Cada caso faz init preguiçoso sob mutex (`call 0x17969E0`) e monta uma
`initializer_list` na pilha. Exemplo (caso 5, vetor `0x2754E40`):

```
0085EDE7  lea rax,[rsp+0x30]         ; list.begin
0085EDEC  mov dword [rsp+0x30],8     ; desc[0].+0
0085EDF4  mov [rsp+0x20],rax
0085EDF9  lea rdx,[rsp+0x78]         ; list.end (0x78−0x30 = 0x48 = 3×24)
0085EDFE  mov [rsp+0x28],rdx
0085EE03  lea rcx,[rip+0x1EF6036]    ; rcx = &vetor 0x2754E40
0085EE23  mov dword [rsp+0x40],2     ; desc[0].+0x10
0085EE2B  mov dword [rsp+0x48],9     ; desc[1].+0
0085EE33  mov qword [rsp+0x50],2     ; desc[1].+8
0085EE3C  mov dword [rsp+0x58],1     ; desc[1].+0x10
0085EE44  mov dword [rsp+0x60],0x13  ; desc[2].+0
0085EE4C  mov qword [rsp+0x68],3     ; desc[2].+8
0085EE55  mov dword [rsp+0x70],1     ; desc[2].+0x10
0085EE5D  call 0x563E40              ; constrói vector<Desc> a partir da lista
0085EE62  lea rcx,[rip+0x1471EF7]    ; registra destrutor 0x1CD0D60
```

**D. Alocador e contagem — `0x563E40`.**

```
00563E55  mov rbx,[rdx+8]            ; list.end
00563E5B  sub rbx,[rdx]              ; end − begin
00563E5E  movabs rbp,0xAAAAAAAAAAAAAAAB
00563E68  sar rbx,3
00563E6F  imul rbx,rbp               ; n = (end−begin)/24
00563E86  movabs rax,0xAAAAAAAAAAAAAAA
00563E90  cmp rbx,rax                ; guarda de overflow
00563E95  lea rcx,[rbx+rbx*2]
00563E9E  shl rcx,3                  ; 24·n
00563EA2  call 0x32B810              ; operator new (0x32B810 chama 0x1796CF4)
00563EA7  mov [r14],rax              ; vec.begin = base
00563EB8  mov [r14+8],rax            ; vec.end   = base
00563EBF  lea rax,[rax+rcx]          ; base + 24·n
00563EC6  mov [r14+0x10],rax         ; vec.cap   = base + 24·n
00563ED0  call 0x1798F3C             ; memcpy(base, list.begin, end−begin)
00563EE4  lea rcx,[rsi+rax]          ; base + (24·n)
00563EED  mov [r14+8],rcx            ; vec.end   = base + 24·n
```

Portanto: **contagem = `(end−begin)/24`**, calculada em `00563E55`–`00563E6F`; **array =
`operator new(24·n)`** em `00563EA2`; `cap = base+24·n` em `00563EC6`. O header do vetor
estático fica em `.data` (`0x2754xxx`), mas os 24·n bytes de elementos são heap:
`0x2754BC8` no dump vivo aponta para `0x0FAA5890`, fora do dump de 137 MB.

**E. Tabela caso → vetor → descritores (lida de `0x85E6C0`/`0x85FFA0` e da `.data`).**

| caso | vetor | descritores `(code, idx, kind)` |
|---|---|---|
| 0 | `0x2752208` | vazio (`0085EBCA lea rax,[rip+0x1EF3637]`; `{0,0,0}`) |
| 1 | `0x2754DB8` | (9,0,1) |
| 2 | `0x2754BC8` | (8,0,2) |
| 3 | `0x2754D80` | (8,0,2) (9,2,1) |
| 4 | `0x2754C88` | (8,0,2) (15,2,2) |
| 5 | `0x2754E40` | (8,0,2) (9,2,1) (19,3,1) |
| 6 | `0x2754D48` | (8,0,2) (9,2,1) (13,3,2) |
| 7 | `0x2754C00` | (8,0,2) (9,2,1) (10,3,1) (13,4,2) |
| 8 | `0x2754CD0` | (8,0,2) (9,2,1) (13,3,2) (19,5,1) |
| 9 | `0x2754BE0` | (8,0,2) (9,2,1) (10,3,1) (13,4,2) (19,6,1) |
| 10 | `0x2754DD8` | (8,0,2) (9,2,1) (14,3,2) (15,5,2) |
| 11 | `0x2754CA8` | (8,0,2) (9,2,1) (13,3,2) (11,5,2) |
| 12 | `0x2754DF0` | (8,0,2) (9,2,1) (10,3,1) (14,4,2) (15,6,2) |
| 13 | `0x2754E28` | (8,0,2) (9,2,1) (10,3,1) (13,4,2) (11,6,2) |
| 14 | `0x2754D28` | (8,0,2) (9,2,1) (10,3,1) (13,4,2) (16,6,2) |
| 15 | `0x2754C68` | (8,0,2) (9,2,1) (10,3,1) (13,4,2) (16,6,2) (18,8,2) |
| 16 | `0x2754E10` | (8,0,2) (9,2,1) (14,3,2) (15,5,2) (16,7,2) |
| 17 | `0x2754CF0` | (8,0,2) (9,2,1) (10,3,1) (14,4,2) (15,6,2) (16,8,2) |
| 18 | `0x2754D98` | (8,0,2) (9,2,1) (10,3,1) (14,4,2) (15,10,2) (16,6,2) (18,8,2) |
| 19 | `0x2754C40` | (8,0,2) (9,2,1) (10,3,1) (12,12,2) (14,4,2) (15,10,2) (16,6,2) (18,8,2) |
| 20 | `0x2754D10` | (8,0,2) (9,2,1) (10,3,1) (12,12,2) (14,4,2) (15,10,2) (16,6,2) (17,14,2) (18,8,2) |
| 21 | `0x2754D68` | (8,0,2) (9,2,1) (10,3,1) (12,6,2) (14,4,2) (15,8,2) (16,10,2) (18,12,2) |
| 22 | `0x2754C20` | (8,0,2) (9,2,1) (10,3,1) (12,6,2) (14,4,2) (15,8,2) (16,10,2) (17,14,2) (18,12,2) |

Cada vetor é construído **uma vez por processo** (mutex + flag), não por voz. A tabela acima
foi gerada por `tools/stage_c_table.py` (lê `checks/85e6c0.dis` + `.data`), saída em
`checks/stage_c_table.json`.

**F. Quem lê `+0` — e a correção do "discriminador".**

`+0x10` é o discriminador de ramo (`1` ou `2`), não `+0`. `+0` é comparado com literais:

```
008BFDB4  mov r8d,[r15]              ; descritor campo +0
008BFDC6  cmp r8d,0xA
008BFDEA  lea eax,[r8-9]; cmp eax,1  ; aceita 9 e 10
008BFE02  lea eax,[r8-0x10]; cmp eax,2  ; aceita 0x10,0x11,0x12
008BFE17  lea eax,[r8-8]; cmp eax,2     ; aceita 8,9,10
008BFE5A  lea eax,[r8-8]; cmp eax,1     ; aceita 8,9
008BFE6C  cmp edx,r8d
008BFE99  mov r8d,[r15+0x10]         ; tipo
008BFEBF  movsxd rax,[r15+8]         ; idx
008BFF97  add r15,0x18
```

`+8` indexa dois arrays de ponteiros: `008B3664 mov rbx,[rsi+8]`; `008B366F mov
rdx,[r14+rbx*8]`; `008B3676 mov rcx,[r15+rbx*8]` (consumidor `0x8B35A0`); e `008C0CDA
movsxd rax,[rsi+8]` (consumidor `0x8C0BD0`). `+0x10 == 1` em `008B3660`; `+0x10 == 2` em
`008C0C90`; `008C43A0 cmp dword [rdi+0x10],1` (consumidor `0x8C42D0`). O quarto consumidor
`0x8C3F10` também usa `008C4151 movsxd rcx,[r14+8]` e `008C4245 add r14,0x18`.

**G. Quem grava `[outer+8]` — PROVADO.**

`0x88E8A0` monta um struct local em `rbp` e o passa como 4º arg para `0x8AB760`:

```
0088E8C0  lea rbp,[rsp-0x35A8]       ; rsp = entry−0x40 (8 pushes) → rbp = entry−0x35E8
0088FB5A  mov r13,[rbp+0x35F8]       ; = entry+0x10 → home de arg2
0088FB61  mov r14,[rbp+0x35F0]       ; = entry+0x08 → home de arg1
0088FB7D  mov [rbp+0x10],rax         ; outer+0x10 = &(arg1+0x1408)  (rax de 0088FBB1)
0088FB9C  mov [rbp+8],r14            ; outer+8 = arg1
0088FBB1  lea rax,[r14+0x1408]
0088FBB8  mov [rbp-0x50],rax
0088E8D5  mov eax,[rcx+0x2C30]       ; arg1+0x2C30 (arg1 = ctx; escrito em 00870933)
008912FB  lea r9,[rbp]               ; 4º arg de 0x8AB760 = &outer
00891319  mov rcx,[rbp-0x50]         ; arg1 de 0x8AB760 = ctx+0x1408
0089131D  call 0x8AB760
0x8AB760  008AB959 mov rcx,rsi       ; rsi = r9 = &outer
0x8ABAA0  008ABABC mov rax,[rcx]     ; outer+0
0x8ABAA0  008ABDEB mov rax,[rsi+8]   ; outer+8 = ctx
```

Logo `outer` é o struct local em `rbp` de `0x88E8A0`; `outer+8 = ctx` (o mesmo objeto cujo
`+0x2C30`/`+0x2C38` são escritos por `0x86FE90` em `00870933`/`00870941`), e
`outer+0x10 = ctx+0x1408` (buffer-set inicializado em `00870786` por `0x878200`).

**H. Constantes com RVA.** `0x16` `0085E6CE`; tabela `0x85FFA0` `0085E6E1`; tabela de
vazio `0x2752208` `0085EBCA`; `0x18` stride `008C13CD`/`008BFF97`; divisor `24` via
`0xAAAAAAAAAAAAAAAB` `00563E5E`; `24·n` `00563E95`/`00563E9E`; `0xC1A8` `00862E52`;
`0x5F8` `008638D6`; `0x600` `0086A533`; `0x1408` `0088FBB1`; limites de `+0`
`008BFDC6`/`008BFDEA`/`008BFE02`/`008BFE17`/`008BFE5A`.

**I. Rust (mesma aritmética, mesma ordem, mesmos coeficientes).** Arquivo gerado:
`checks/stage_c_rust.rs`. Trecho essencial:

```rust
#[repr(C)]
#[derive(Clone, Copy, Debug)]
pub struct BandDesc {          // 24 B, provado pelos destrutores 0x1CD0E60/0x1CD0DE0
    pub code: i32,             // +0x00  (lido em 008BFDB4)
    pub _pad0: i32,            // +0x04  (nunca escrito pela initializer_list)
    pub idx: i64,              // +0x08  (lido em 008C0CDA/008B3664)
    pub kind: i32,             // +0x10  (1 ou 2; 008C0C90/008B3660)
    pub _pad1: i32,            // +0x14
}
const _: () = assert!(core::mem::size_of::<BandDesc>() == 24);

const EMPTY: &[BandDesc] = &[];
static CASE_01: &[BandDesc] = &[BandDesc { code: 9, _pad0: 0, idx: 0, kind: 1, _pad1: 0 }];
static CASE_05: &[BandDesc] = &[
    BandDesc { code: 8,  _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9,  _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 19, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
];
// ... casos 2..22 completos em checks/stage_c_rust.rs

pub fn select_band_table(case: i32) -> &'static [BandDesc] {
    match case {
        1 => CASE_01, /* ... */ 5 => CASE_05, /* ... */
        22 => CASE_22,
        _ => EMPTY, // 0 e >0x16: 0085EBA7 → 0x2752208
    }
}
```

**`NÃO PROVADO` (o que honestamente sobra):** o significado semântico dos valores de `+0`
(8..19), de `idx` e de `kind`; a identidade do objeto `arg3` de `0x862E40` (só se provou que
os casos vêm de `[arg3]` e `[arg3+8]`, dwords 0..0x16); o consumidor do campo `+0` fora de
`0x8BFD30` não foi esgotado; e os 24·n bytes de elementos vivem no heap (fora do dump), de
modo que a **ordem** e os **valores** acima vêm das listas estáticas, não de uma cópia de
heap.

**Critério de saída:** fechado — (a) RVAs; (b) desmontagem comentada; (c) constantes;
(d) structs com offsets provados; (e) Rust. Detalhe em `dsp-spec.md` §18.4.

### 23.4 Etapa D0 — `0x8B2C30` — **FECHADO: FIR de 32 taps com coeficientes por bloco** (2026-11-22)

Estado: **FEITO**. Os cinco itens da regra de entrega estão abaixo. Desmontagem completa em
`checks/8b2c30.dis` (301 linhas), chamador em `checks/8b2680.dis`, escritor do kernel em
`checks/8803ce.dis`.

**1. Endereço e entrada.** `0x8B2C30`, chain-aware `0x8B2C30–0x8B30BB` = 1.163 B. Prólogo
real `mov [rsp+0x18],rbx` / `mov [rsp+0x20],rdi` / `push r14` / `sub rsp,0x10`. Os pedaços
`0x8B2BCE` e `0x8B2BD6` do `.pdata` **não** são o começo desta função: são o epílogo de um
kernel *irmão* dentro do mesmo chamador (`0x8B2680`, que termina em `0x8B2C29`). Prova:
`0x8B2BD6` acessa `[rsi+0x140]`/`[rsi+0x148]` e guarda com `movss [r11+rax*4], xmm8` (store),
enquanto `0x8B2C30` usa `[rcx+0x80]` e **soma** (`addss ... ; mov [rcx+rax*4], r9d`). São
dois: um kernel 32 fixo (`0x8B2C30`) e um kernel com máscara dinâmica em `[obj+0x148]`
(epílogo em `0x8B2BD6`).

**2. Assinatura real** (Win64: rcx=arg1, xmm1=arg2 float, r8=arg3):

```
float fir32_scatter(Fir32* S /*rcx*/, float x /*xmm1*/, const float* K /*r8*/)
```

`rdx` e `r9` não são lidos. Chamada única em `0x8B26A8` (`call 0x8b2c30`), de dentro de
`0x8B2680`, com `rcx = ctx+0x188`, `xmm1 = x`, `r8 = ctx+0x40`.

**3. Pseudocódigo comentado** — cada linha é instrução de `checks/8b2c30.dis`:

```c
// 008B2C40  mov rax,[rcx+0x80]          p = S->pos        (0..31)
// 008B2C47  lea r10,[r8+4]              src = &K[1]
// 008B2C62  mulss xmm6,[r8]             acc = x * K[0]
// 008B2C7C  addss xmm6,[rcx+rax*4]      acc = acc + S->buf[p]
// 008B2C81  mov [rcx+rax*4],r9d         S->buf[p] = 0        (r9d = 0 de 008B2C4F)
// 008B2C85  sub rbx,[rcx+0x80]          n1 = 31 - p
// 008B2C67/2CA1  ebx=0x1f, and rdx,~3   desenrola de 4 em 4
float y = x * K[0];
y += S->buf[p];
S->buf[p] = 0.0f;
for (unsigned j = 1; j <= 31 - p; ++j)      // 008B2CD0..008B2E7E, 4x/16x + resto
    S->buf[p + j] += x * K[j];              //   mulss ; addss ; movss
// 008B2E8A  cmp [rcx+0x80],r9 ; je 0x8B308F
if (p != 0)
    for (unsigned j = 0; j < p; ++j)         // 008B2EE0..008B308D
        S->buf[j] += x * K[32 - p + j];
// 008B308F..008B30AD
S->pos = (p + 1) & 0x1f;                     // 008B30A6 and eax,0x1f ; 008B30AD store
return y;                                    // 008B3096 movaps xmm0,xmm6
```

Semântica em uma linha: a cada amostra, o vetor de coeficientes `K[0..31]` é **espalhado**
no anel de 32 somas parciais com rotação `p`, e o que sai do anel é o acumulado das 32
amostras anteriores. Equivale a

```
y[n] = Σ_{m=0}^{31} K^{(n-m)}[m] · x[n-m]
```

ou seja, **FIR de 32 taps com coeficientes que mudam por amostra/bloco** (convolução
variante no tempo). Não é média móvel simples: para virar boxcar faltaria `subss`, e o
`scan_region.py` conta **zero `subss`** em 1.163 B. Não é delay: há 27 `mulss`.

**4. Estruturas com offset provado.**

| Offset | Tipo | Prova |
|---|---|---|
| `S+0x000` | `float buf[32]` | `[rcx+rax*4]` em `008B2C7C`, `008B2C81`, `008B2E1A`, `008B2E3A` |
| `S+0x080` | `uint64_t pos` | escrita `(p+1)&0x1f` em `008B30A6`/`008B30AD`; leitura em `008B2C40`, `008B2C85`, `008B2E8A` |

O objeto que o chamador passa (`ctx+0x188`) tem exatamente 0x88 bytes: 0x80 de `buf` +
8 de `pos`. Prova do zero-init em `0x8817D0`: aloca `0x240` (`call 0x1797578`, `ecx=0x240`,
`edx=0x40`), `memset` com `0x1798F42(ptr,0,0x240)`, depois zera 8×16 B em `[rsi+0x188]` e
grava `[rsi+0x208] = 0` (`00881960`–`00881989`); `0x869490` repete a limpeza (128 B + `pos`).

**5. Contexto de banda — offsets provados (`ctx` = objeto de 0x240 B, `0x8817D0`).**

| Offset | Conteúdo | Prova |
|---|---|---|
| `+0x040` | **`float K[32]`** — coeficientes do FIR | `lea r8,[rcx+0x40]` em `008B2690`; `lea rdx,[r14+0x40]` + `call 0x10A0` com `r8d=0x20` em `00880419` |
| `+0x0C0` | ponteiro do anel de entrada (frame) | `mov r11,[rsi+0xc0]` `008B26B4`; `movss [r11+rax*4],xmm8` `008B2BE3` |
| `+0x0D8` | ponteiro do anel de overlap-add | `mov r14,[rsi+0xd8]` `008B26BB`; `addss xmm0,[r14+rax*4]` `008B2AB7` etc. |
| `+0x140` | contador de amostra | `cmp [rsi+0x140],r9` / `test byte [rsi+0x140],0x1f` |
| `+0x148` | máscara do anel (`and rax,[rsi+0x148]`) | `008B2AAA`, `008B2B73`; **zero no construtor** (`0088189D`) |
| `+0x188` | `Fir32` do `0x8B2C30` | `add rcx,0x188` antes do call `008B269D` |
| `+0x210` | buffer de trabalho do bloco | `mov rbx,[rsi+0x210]` `00880450` |

**6. Constantes lidas do dump.**

| Valor | Onde | Como aparece |
|---|---|---|
| `0x1F` = 31 | `008B2C67` (`mov ebx,0x1f`), `008B30A6` (`and eax,0x1f`) | imediato — máscara do anel de 32 |
| `32` | `008B2C85` (`sub rbx,[rcx+0x80]` sobre base 31) e `008B2EA5` (`lea r10,[r14+r10*4]` com `r10 = 32-p`) | aritmética, não literal |
| `1.0f` | `0x2079F9C` (`.rdata`) | `movss xmm7,[rip+0x17c7865]` em `008B272F` (usado no `1.0f / n`) |

O kernel **não tem constante float própria**; os 32 coeficientes vêm de `ctx+0x40`.

**7. Quem escreve `ctx+0x40` — PROVADO (nível da cópia).** `0x8803CE`, laço em
`00880400`–`00880560` (uma volta por banda):

```
00880403  mov r8d, 0x20            ; 32 floats
00880409  mov r14, [rdx+rax]       ; r14 = ctx da banda
00880419  lea rdx, [r14+0x40]      ; dst = ctx->K
0088041D  call 0x10a0              ; 0x10A0 = IPP Copy(src=rcx, dst=rdx, len=r8d)
```

A ordem dos argumentos **não é suposta**: `0x10A0` despacha para `0x2C80`, que faz
`shl r8d,2` e chama `0x26540`, que por sua vez chama `0x1D2EB40`, onde está a direção:

```
01D2EB42  mov rdi, rcx        ; rcx = origem
01D2EB45  mov rsi, rdx        ; rdx = destino
01D2EB67  vmovdqu ymm0,[rdi]  ; lê   de rcx
01D2EB81  vmovdqu [rsi],ymm0  ; grava em rdx
```

Logo `rcx=src`, `rdx=dst` (`memcpy(dst=rdx, src=rcx, n)`), e a cópia de `0x8803CE` escreve
**em** `ctx+0x40`.

Ou seja: o kernel de 32 taps é **copiado para dentro de cada banda a cada bloco**, de um
array de ponteiros (`[rdx+8*i]`, passo 8 em `0088053C`). **FECHADO em 2026-11-23 (§23.7): o
array contém `{1.0f,0,…,0}`** — `0x873440` zera cada segmento e grava `1.0f` em `[0]`
imediatamente antes da cópia (`00874024`–`00874063`), e o design posterior escreve na arena,
não em `band+0x40`. Não há "IFFT da curva de ganho" nesse array; `K = δ0`.

**8. Chamadores (para ligar o filtro ao grafo).** `0x8B2680` (1.449 B) chama `0x8B2C30`
**uma vez por amostra**; `0x8B2680` tem **32 sítios de chamada** em `0x885040` e `0x8875F0`,
todos dentro de laços por amostra:

```
00886A30  mov rax,[rdi+0x2bd8]     ; vetor de contextos de banda
00886A47  mov r12,[rax+r13]        ; ctx da banda
00886A60  movss xmm1,[r15+rbx]     ; x = entrada[k]
00886A66  mov rcx, r12
00886A69  call 0x8b2680            ; y = driver(ctx, x)
00886A6E  movss [rbx], xmm0        ; saída[k] = y
```

**9. Rust equivalente (mesma ordem, mesmos coeficientes).** Ver `docs/engine/dsp-spec.md`
§10, onde está o código com o comentário de cada instrução.

**Correção de leitura que fica registrada:** a contagem estática de **27 `mulss`** (§22.5)
não é "27 taps". Taps = **32** (máscara `0x1f`); a contagem de instruções é menor porque o
compilador gera laços desenrolados com caminhos de resto que se sobrepõem e reaproveitam
registradores. Contar instruções para inferir número de taps é erro; neste caso daria 27 em
vez de 32.

**Aberto (D0-b):** produtor do array de coeficientes consumido em `0x8803CE`; e a identidade
do `N` de bloco (`ctx+0x000` comparado a `0x20`, `desc->+0x18` usado como `n` do `1/n`).

### 23.5 Etapa D1 — `0x8BF650` e `0x8BFD30` — **FEITO (2026-11-22): plumbing de despacho**

Estado: **FEITO**. Desmontagens em `checks/8bf650.dis` (434 linhas, `0x8BF650..0x8BFD50`,
1792 B) e `checks/8bfd30.dis` (428 linhas, `0x8BFD30..0x8C03B0`, 1664 B). Nenhuma das duas
contém FMA, mulss/addss/divss novo nem constante de coeficiente: são **seleção e cópia de
descritores seguida de chamada às primitivas já provadas**. Não são kernel de DSP novo.

**`0x8BF650` — 9 calls, todos com RVA:**
- `008BF719`, `008BFCFE` → thunk `0x10D0` → `0x2F60` (zero-fill, §17.6)
- `008BF827`, `008BFA48` → `memset` (thunk `0x1798F42`)
- `008BFA17` → `memcpy` (thunk `0x1798F36`)
- `008BF955`, `008BFB84` → `0x8CAB40` (288 B; chama `0x86F480` em `008CAB6B` e `0x867CC0`
  em `008CABDD` — nomes IPP **NÃO PROVADOS**, §14.3)
- `008BFC3E`, `008BFC7D` → thunk `0x1190` → `0x4BC0` (mul vetorial, §17.6)

Prova de cópia em blocos: `008BF66B mov esi,8`, loop `008BF690..008BF6A5` (8×`0x80 B`).
Prova de iterar descritores de 24 B: `008BF9B7 mov rax,[rsi+8]`, `008BF9B0 movsxd
r13,[rsi+0x10]`, `008BFB8D add rsi,0x18`, `008BFB9F cmp rsi,[rbp+0xc48]`.

**`0x8BFD30` — 8 calls dentro da função (`0x8BFD30..0x8C022A`), todos com RVA:**
- `008BFE32`, `008BFE46`, `008C003E`, `008C0052` → `0x61B790` (despacho por tipo; chamado
  com `(tipo-2, campo)` e `(tipo-1, campo)` em `008BFE2E`/`008BFE4E`/`008C003A`/`008C004E`)
- `008BFE94`, `008C00B3` → `memset` (thunk `0x1798F42`)
- `008BFF85` → thunk `0x10D0` → `0x2F60` (zero-fill)
- `008C01A9` → thunk `0x1220` → `0x6160` (escalar × vetor, §17.6)
- `008C0313` (`__chkstk`) pertence a `0x8C02F0`, **não** a esta função.

Prova de 5 passadas: `008BFD60 lea rax,[rip+0x17545f9]` → tabela `0x2014360` com
`i32 = [8, 9, 10, 6, 5]` (lida do dump), `008C01E5 inc r15d`, `008C01EB cmp rax,5`,
`008C0202 jb 0x8BFD80`. Seletor por tipo em `008BFDB4..008C007D`: `r14` é o tipo da
passada, `[r15]` o campo `+0` do descritor (`008BFDB4 mov r8d,[r15]`); comparações
`008BFDC6 cmp r8d,0xA` (tipo 1), `008BFDD8 cmp r8d,9` (tipo 2), `008BFDEA lea eax,[r8-9]`
(tipo 3), `008BFE02 lea eax,[r8-0x10]` (tipo 5), `008BFE17 lea eax,[r8-8]` (tipo 4),
`008C0066 lea eax,[r8-8]` (tipo 7). Isso é **despacho**, não cálculo de amostra.
As funções auxiliares subsequentes `0x8C0230` (2× `0x1340` → `0x9BA0` em
`008C027A`/`008C02BA`) e `0x8C02F0` já estavam fechadas como plumbing.

**Critério de saída atendido:** os dois lidos; plumbing provado pela contagem de calls e
pelos RVAs acima. Nenhum tamanho de FFT, nome IPP ou coeficiente foi inferido.

### 23.6 Etapa E — `0x8C33D0` (2.128 B) por desmontagem — **PSEUDOCÓDIGO FEITO (2026-11-22)**

Estado: **FEITO**. O Hex-Rays entregou vazio (`ida_008C33D0.c` só tem o cabeçalho), então a
função foi lida por `show_func.py`: `checks/8c33d0.dis` (519 linhas, `0x8C33D0..0x8C3C14`,
`ret` em `008C3C14`, `int3` até `008C3C1F`). Pseudocódigo manual com RVA por bloco em
`docs/engine/decomp/manual_008C33D0.c`.

Não é código morto: a desmontagem prova chamadas às primitivas B já fechadas —
`008C3698`/`008C36D6`/`008C3A43`/`008C3B93 call 0x11c0`, `008C389B call 0x1250` (modo `4` em
`008C3893`), `008C393B call 0x1100` (modo `0` em `008C3933`). As duas metades são gêmeas
(`0x8B6A7E` e `0x8C87EE` chamam a mesma função). Copia `8 × 0x80 B = 1024 B = 256 floats`
(`008C340B mov r14d,8`, loop `008C3440..008C3495`) — **isso é um buffer de 256 floats, não a
prova do N da FFT**; o N continua `NÃO PROVADO` (§23.14).

**NÃO PROVADO e registrado como tal:** a origem de `[rbp+0x740]`/`[rbp+0x744]` no primeiro
trecho — leitura em `008C34BD`/`008C34C7` precede a escrita em `008C371A`/`008C3724`. Pode ser
estado do chamador ou trecho emendado; não foi inferido.

**Critério de saída atendido:** pseudocódigo comentado com RVA por instrução; nenhum nome
inventado, nenhuma operação estimada.

### 23.7 Etapa F — origem de `ctx+0x40` — **FECHADA (2026-11-23): `K = δ0`, sem aritmética**

Estado: **fechada em 2026-11-23**. A cópia dos 32 coeficientes está provada e o valor copiado
está provado como **constante**: `K = {1.0f, 0, …, 0}` (`count>0`) ou `{0, …, 0}`
(`count=0`). Não existe aritmética de parâmetro na origem dos taps. Prova na subseção
"Fechamento 2026-11-23" abaixo e em `dsp-spec.md` §10.4. RVAs reverificados na
desmontagem (`show_func.py`), não apenas recebidos do agente:

- `0x880390` (.pdata 272 B) é a entrada real; `0x8803CE` é o fragmento da cópia.
- `00880403 mov r8d,0x20` (32 dwords), `00880409 mov r14,[rdx+rax]` (ctx da banda),
  `0088040D mov rax,[rdx+r9]` (origem), `00880419 lea rdx,[r14+0x40]`, `0088041D call 0x10A0`.
- `0x10A0` resolve (via `dispatch.py`) para `idx@0x21C7408=4`, `tab=0x21C5E08`,
  **RVA `0x2C80`**; `00002D25 shl r8d,2` + `00002D29 call 0x26540` provam `memcpy` de 128 B.
- Dois chamadores em `0x873440`: `00874107` (`arg1=rdi+0x2BD8`, `arg2=rbp+0x10B0`) e
  `00874184` (`arg1=rdi+0x2BF0`, `arg2=rbp-0x20`). Ambos os structs de origem vêm de 8
  cópias de `0x80 B` a partir de `[rbp+0x480]` (`008740A0..00874104`, `00874120..00874181`).
- Struct de ponteiros de `0x619D90`: `+0x400` nº de ponteiros (`00619DDD`), `+0x404` floats
  por segmento (`00619DE4`), `+0x408` bytes por segmento (`00619DD6`), tabela preenchida
  por `0x61A9A0` (`0061A9D0..0061AA02`).

`powf(10, 2.4)` e `powf(10, -4.8)` estão provados em `0087EF78`/`0087EF80`/`0087EF8B` e
`0087EFEF`/`0087EFFA` (constantes `0x207A360`, `0x207A1E8`, `0x207A6F0`), mas **`0x87E220`
é chamado em `00873111`, caminho distinto de `0x873440` (`0086A92B`/`0086A961`)**. Sem
instrução de ligação, não são atribuídos a `K[32]`. Forma do filtro (`0x87BB60`→`0x882FC0`)
continua **NÃO LIDA**: registrar como tal, sem "parece biquad".

**Critério de saída — atendido em 2026-11-23:** constantes com RVA sim; a "fórmula" é
`K = δ0` (constante gravada, não conta): a cadeia até `00873F1A` não contém store de float
com aritmética observável (`0x56B140`, `0x619EA0`, `0x877780` zera, `0x878200` aloca).

#### Leitura 2026-11-23 — cadeia da arena até `ctx+0x40` (PROVADA; fechamento abaixo)

Esta leitura **liga** a origem dos 32 floats ao `ctx+0x40` e **refuta a hipótese de IFFT**
para esta cadeia. Tudo abaixo tem instrução e RVA; desmontagens em `checks/`.

**1. A curva de redução nasce de parâmetros — PROVADO.** `0x8634A0` (3.022 B) copia
`r14+0x30` e registra os nomes `reduction_curve_freq_points_lo` (`0x2077580`),
`reduction_curve_freq_points_hi` (`0x2077560`), `reduction_curve_magnitudes_lo`
(`0x2077540`) e `reduction_curve_magnitudes_hi` (`0x2077520`) em
`00863577`/`0086358B`/`008635A0`/`008635B2` (`call [r15+0x18]`). O container
`r14+0x30` é inicializado por `0x868B50` em `00863563` (`lea rcx,[r14+0x30]`), que
aloca `max([r14+0x10],2) << 16` floats (`00868B75`–`00868BBF`).

**2. Quem passa o banco para o design — PROVADO.** `0x86A4E0` chama `0x86FE90`
(`0086A54B`, `0086A581`) e `0x86A8C0` chama `0x873440` (`0086A92B`, `0086A961`).
Em `0x86A8C0`, o arg8 (`r12`, lido em `[rbp+0x7f]` = arg8) é empilhado em
`[rsp+0x48]` (`0086A8FC`) e vira arg10 de `0x873440` (`0086A92B`); em `0x873440`
ele é `r14 = [rbp+0x15d8]` (`00873E6D`).

**3. O banco é um vetor `{base, count, cap, offset}` — PROVADO.** `0x619EA0`
(chamado em `0086FF98` e `00873565`) zera `[obj]`,
`[obj+8]`, `[obj+0x10]`, grava `[obj+0x18]=n` e chama `0x6165A0`
(reserve: `operator new` em `006165DE`, `00616609`). Em `0x619D90`
(`00873F1A`) a tabela de ponteiros é montada: `[table]=0` e `memset(table+8,0,0x3f8)`
(`00619DA8`–`00619DC4`), `[table+0x400]=count` (`00619DDD`),
`[table+0x404]=32` (`00619DE4`), `[table+0x408]=128` (`00619DD6`); `0x61A9A0`
grava `table[i] = *(obj) + obj->offset*4` (`0061A9D0`–`0061A9DB`) e avança
`offset += 32` alinhado a 16 (`0061A9E3`–`0061AA02`).

**4. A cópia para cada banda — PROVADO.** `0x880390` (`00874107`, `00874184`) copia
32 floats (`00880403 mov r8d,0x20`) de `*(table + 8*i)` (`0088040D`) para
`ctx+0x40` (`00880419 lea rdx,[r14+0x40]`; `0088041D call 0x10A0`). O argumento
`table` é o mesmo `r14` de `0x873440` (`00873F1A call 0x619D90` com `rcx=r14`).

**5. O FIR roda em paralelo ao STFT — PROVADO.** `0x8B2680` chama `0x8B2C30` com
`K = ctx+0x40` (`008B2690 lea r8,[rcx+0x40]`; `008B26A8 call`) e soma o resultado
ao overlap-add do STFT: `008B2BDD addss xmm6,[r14+rax*4]`. Portanto `K[32]` é um
**caminho FIR de 32 taps somado ao caminho FFT**, não o ganho espectral.

**6. Quem escreve na arena — PROVADO; a aritmética era `NÃO EXTRAÍDA` (fechada em 2026-11-23).**
Em `0x873440` a cadeia é chamada com `rdx = r14` (a arena):
`008769E5 mov rdx,r14` → `0x87B680`; `008769F0` → `0x87BB60`; `008769FB` →
`0x87DB30`; `00876A06` → `0x87E220`. Em `0x86FE90` a mesma cadeia é chamada em
`008730F0`/`008730FB`/`00873106`/`00873111` com `rdx=r15`.

- `0x87BB60` (8.136 B) aloca na arena `N` segmentos de `r10 = [r13+0x748+0x88]`
  floats (`0087BD8B`–`0087BDC3`), preenche com `1.0f` via `0x87A7A0`
  (`0087BF57`, `0087BFC9`) e chama `0x882FC0` (`0087C231`, `0087C4DA`).
- `0x882FC0` (1.063 B) converte frequência: `log10f` (`0x1c9a5a1`, = IAT `log10f`) e
  `powf(10, 0.5*log10(x))` = `sqrt(x)` (`0x1c9aa01` = IAT `powf`) em
  `00883107`/`00883112` e `00883207`/`00883212`; chama `0x88E130` com `-20*log10(x)`.
  Constantes com RVA: `500` `0x207A560`, `2000` `0x207A5A8`, `20` `0x207A3B0`,
  `0.5` `0x2079EA8`, `0.05` `0x2079D88`, `10` `0x207A360`, `12` `0x207A384`.
  **CORRIGIDO:** `0x1340` é multiplicação **array×array** com `dst=arg2`
  (`00009C20`–`00009C2A`), não "mul por escalar"; os sítios `008832E4`/`00883309`/
  `00883388`/`008833A9` multiplicam vetores, e a aritmética completa segue `NÃO EXTRAÍDA`
  (etapa H).
- `0x87E220` (3.739 B) escala por `powf(10,2.4)` (`0x207A360`, `0x207A1E8`) e
  `powf(10,-4.8)` (`0x207A6F0`) em `0087EF78`–`0087EF8B` e `0087EFF7`–`0087F04B`
  com `0x1100`; **não** escreve os taps.
- `0x877DD0` (669 B) gera uma janela de Hann `w[i] = max(0,(1−cos(2πi/N))/2)`
  (`00877F92`, `00878010`–`00878044`; constantes `2π` `0x207A1E0`, `0.5`
  `0x207A0B8`, `1.0` `0x207A138`) e grava em `band+0x2c08`, não na arena.

**7. O que fica `NÃO PROVADO` (e por quê).** Não há chamada de FFT/IFFT em
`0x87B680`, `0x87BB60`, `0x87DB30`, `0x882FC0`, `0x882DE0` nem `0x8834C0`
(varredura de `call`): só `0x1040`/`0x10A0`/`0x10D0`/`0x1220`/`0x1250`/`0x1310`/
`0x1340`/`0x12E0` e math (`0x1c9a5a1`=`log10f`, `0x1c9aa01`=`powf`). Portanto a hipótese
"`K[32]` = IFFT da curva de ganho" **não se sustenta nesta cadeia**. **SUPERSEDIDO pelo
"Fechamento 2026-11-23" abaixo:** o segmento copiado é `[0..31]` do início de cada
segmento da arena, mas a cópia ocorre **depois** do reset que zera e grava `1.0f` — logo
`K = δ0` e não há fórmula a extrair. O "próximo comando" antigo (ler `0x882FC0`/`0x87B680`)
ficou como etapa H.

#### Fechamento 2026-11-23 — `K = δ0` (PROVADO; encerra a etapa)

A leitura de `0x882FC0` (dB→linear, `10^(x/20)`) e de `0x87B680` (curva de redução na
arena) mostra que essas funções escrevem **curvas**, não os 32 taps. A origem dos 32 taps
está no **reset que precede a cópia**, dentro de `0x873440`:

| # | RVA | Instrução | Efeito |
|---|---|---|---|
| 1 | `00873F1A` | `call 0x619D90` (`rcx=r14` arena, `rdx=rbp+0x480`, `r8=[rdi+0x48]`, `r9=[rdi+0x38]>>1`) | tabela de `count` ponteiros, `table[i]=base+offset*4`, `offset+=N` |
| 2 | `00873F40` / `00873FB0` | loops 8×`0x80` B | copia a tabela p/ `rbp+0x890` e `rbp+0xCA0` |
| 3 | `00874010`–`00874037` | `0x10D0(table[i], N)` p/ `i<count` | **zera N floats** de cada segmento |
| 4 | `00874039`–`00874063` | `00874059 mov dword [rax],0x3F800000` | **`table[i][0] = 1.0f`** |
| 5 | `00874072` / `00874084` | `0x8780D0` | cria `count` bandas (`0x8817D0`, `0x240` B) e `0x8784A0` grava `band+0 = N` |
| 6 | `008740F6`/`00874107` e `00874176`/`00874184` | `0x880390` | `memcpy(src=table[i], dst=band+0x40, 32 floats)` |
| 7 | `00874189` | `mov [r14+0x18],esi` | restaura o cursor da arena |
| 8 | `00876217`… / `008769E5`–`00876A0C` | design | só **depois** da cópia |

Provas pontuais: `0x10D0`→`0x2F60` (`00002F71 shl edx,2`; `00002F7C call 0x1D2E9E0`) é
memset; `0x8784A0` grava `*param_1 = param_2` (Ghidra `checks/decomp/0x1808784a0.c`), ou
seja `band+0 = N`; `xref_scan.py 0x880390` devolve **2 refs**, ambas em `0x873440`
(`00874107`, `00874184`) — nenhum outro escritor de `band+0x40`.

**Correções que isto impõe (registradas):**
- `table+0x404` **não é 32**: é `N = [this+0x38]>>1 = [this+0x28] =
  int(max(fs,44100)/44100 * fft_size)` (`0087346D maxss 0x207A5E4=44100`;
  `008734CA mulss 0x2079D04=1/44100`; `00873509 imul [rbp+0x15B0]`). `fft_size` é o
  **arg5** de `0x873440`: **2048** na 1ª chamada (`0086A923 mov dword [rsp+0x20],0x800`) e
  **256** na 2ª (`0086A959 mov dword [rsp+0x20],0x100`). Os 32 de `00880403 r8d=0x20` são
  a quantidade de taps copiados, não o tamanho do segmento.
- `0x10A0` é **IPP ordem-fonte**: `src=rcx`, `dst=rdx`, provado em `0x1D2EB40`
  (`01D2EB42 mov rdi,rcx`; `01D2EB45 mov rsi,rdx`; `01D2EB67 vmovdqu ymm0,[rdi]`;
  `01D2EB81 vmovdqu [rsi],ymm0`; retorno `rax=rsi`). Não é `memcpy(dst=rcx,...)`.

**Consequência no FIR (PROVADA):** com `K=δ0`, `0x8B2C30` devolve `y = x`
(`008B2C62 mulss xmm6,[r8]`; `008B2C7C addss`; `008B2C81` zera `buf[p]`; os laços
`j=1..31` somam `x*K[j]=0`). O FIR de 32 taps é **passa-direto**; com `count=0`, `K=0` e
`y=0`.

**Continua `NÃO PROVADO`:** o papel dos blocos `≥32` de `0x880390`
(`00880450`–`00880511`, que copiam `arena+32` para `band+0x210` — fonte zerada pelo passo 3);
quem lê a curva de ganho que `0x882DE0`/`0x882FC0` gravam na arena; e a intenção DSP do
caminho. Nada disso muda o valor de `K` (cópia por valor, já feita).

Detalhe completo: `dsp-spec.md` §10.4.

#### Design que escreve na arena — `0x882DE0` (PROVADO, 2026-11-23)

`0x882DE0` (476 B) é o "peaking" do design: calcula a curva de ganho e grava na **mesma
arena** (span `p` = `[r12]+rcx*4`, `0087B800`/`0087B80E`). Não toca `band+0x40`, e
`0x880390` copiou por valor — logo isto **não** reabre `K`.

```
sig  = (double)B * 0.601591280067049 * 0.7071067811865475   ; 00882E29/00882E36
sig2 = sig*sig                                                 ; 00882E80
s1   = logf(powf(10.0f, D*0.05f))                              ; 00882E3E powf, 00882E43 logf
k    = 1.0 / max((double)A, 2^-23)                             ; 00882E67/6F/89 (f64 -> f32)
e    = -0.5 / sig2                                             ; 00882E4E/9A
p[i] = inbuf[i] + 1.1920929e-07f                               ; 00882E9F 0x1310 (escalar xmm1)
p[i] = p[i] * (float)k                                         ; 00882EBE 0x1220
p[i] = ln(p[i])                                                ; 00882EE1 0x1C8500
p[i] = p[i] * 1.44269502f                                      ; 00882EE6/00882EF4 0x1220
p[i] = p[i] * p[i]                                             ; 00882F12 0x1340 (rcx=rdx=p)
p[i] = p[i] * (float)e                                         ; 00882F28/00882F32 0x1220
p[i] = exp(p[i])                                               ; 00882F50 0x1C84A0
p[i] = p[i] * (float)s1                                        ; 00882F66/00882F70 0x1220
p[i] = exp(p[i])                                               ; 00882F8E 0x1C84A0
```

Equivalente: `g(f) = exp(-0.5*(log2((f+eps)/max(A,eps))/sig)^2)` e
`out(f) = (10^(D/20))^g(f)`. Para bit-exact: **não** trocar `logf(powf(10,D*0.05f))` por
`D*0.11512925`.

**Math identificada por instrução** (não por nome): `0x1C8500` = **ln** (impl `0x293760`,
`002939CF vfmadd213ps ymm9, ymm15, ymm12` com `ymm15` = `0x1ECAE40` = `ln 2`);
`0x1C84A0` = **exp** (impl `0x240C00`, `00240D96 vfmadd231ps ymm10, ymm4, ymm15` com
`ymm4` = `0x1E6FBC0` = `log2 e` + `0x1E6FC00` = `12582912` = `1.5·2^23`);
`0x1C9AA01`/`0x1C9A9FB`/`0x1C9A5A1` são thunks de IAT para `powf`/`logf`/`log10f`
(descriptor `0x2175044`, `OFT 0x2176878`, `FT 0x1D8D790`; índices 17/15/1).

**Chamador `0x87B930`:** `A=2000` (`0087B8CD`), `B=2.5` (`0087B8C5`), `D=3`
(`0087B91C`→`[rsp+0x20]`), logo `sig = 1.06348` oitavas.

**`0x882FC0`:** `00883054` = `log10f(arg3)` (thunk `0x1C9A5A1` → `FT` idx 1 = `log10f`);
`00883107` = `powf(10, 0.5*log10(arg3))` = `sqrt(arg3)`; repete com `arg4` (`0088315E`),
`008831D1 xmm2=2000` e `00883176 xmm3=12`, e chama `0x88E130` com `-20*log10(...)`
(`008830E7`/`008831E7`). Restante **`NÃO EXTRAÍDO`** (etapa H).

### 23.8 Etapa G — struct de estado — **FECHADA (2026-11-23): escritor `0x867D80` e os 143 índices ligados a offset**

Varredura linear de todo o `.text` (capstone, filtro `disp in {0x2C38,0xBFF8,0x5ED0}`,
127 refs) salva em `checks/state_offset_refs.txt`. Não é decompilado: cada linha tem RVA,
função e operando.

**`ctx+0x2C38` — 2 stores provados, o resto são leituras:**

| RVA do store | Função | Valor |
|---|---|---|
| `00870941 mov [rdi+0x2c38], rax` | `0x86FE90` | `rax = [rbp+0x440]` (`008708FD`) |
| `00873F06 mov [rdi+0x2c38], rax` | `0x873440` | `rax = [rbp+0x15c0]` (`00873ECF`) |

Ambos os sítios zeram antes `[rdi+0x2bb8..0x2c18]` (`008708A6`–`008708F6` e
`00873E80`–`00873EC8`), e gravam `+0x2c40` (`dword`) e `+0x2c44` (`word`) em seguida
(`0087090B`/`00870911`, `00873EDD`/`00873EE3`). As ~120 leituras (`mov rax,[reg+0x2c38]`)
alimentam todas as gigantes (`0x885040`, `0x8875F0`, `0x8B4268`, `0x8C5FD8`, …). O
**conteúdo** do objeto apontado não foi lido campo a campo: `NÃO PROVADO`.

**`ctx+0xBFF8` — 1 store provado:** `00863CD9 mov [r14+0xbff8], rdi` em `0x8634A0`.
`rdi` vem de 16 alocações de `0x1040 B` (`00863C80 mov ecx,0x1040`, chamada indirecta via
`0x1D8D750`, loop `00863C80..00863CB7` com `cmp rbx,0x10`), com os ponteiros em
`[rsi + rbx*8]` (`00863CAC`) e os metadados `[rsi+0x80]=0x10`, `[rsi+0x88]=0x400`
(`00863CB9`, `00863CCB`). Zero dos 16 blocos em `00863CE2..00863D15`.

**`ctx+0x5ED0` / `ctx+0x5F8` — FECHADO em 2026-11-24 (`checks/p_extras.md` §P1):** não há
store de ponteiro; são **subobjetos embutidos** construídos em `0x8634A0` —
`008638D6 lea rcx,[r14+0x5f8]` + `00863929 call 0x86A4E0`, e
`00863994 lea rcx,[r14+0x5ed0]` + `008639E3 call 0x86A8C0`. Destruídos em `0x862F40`
(`00862F90`/`00862F9C call 0x863140`), que zera `+0x58A8`/`+0x58C0` → tamanho ≥ `0x58C8`
(encaixa: `0x5F8+0x58C8 = 0x5EC0`). `0x8774A0` escolhe pelo byte `[engine]` (`008774AC`);
caminho `+0x5ED0` → `0x880640`, caminho `+0x5F8` → `0x868730` + `0x881050`. Os dois modos
diferem no parâmetro de `0x873440` (`1`/`0x800` vs `0`/`0x100`) — significado `NÃO PROVADO`.

**Callback `[rdx+0x50]` — corrigido em 2026-11-24:** é **ponteiro de código**
(`00867DFC mov rax,[rdx+0x50]`, `00867E10 call rax`), mas **não** é o `+0x50` da tabela
`0x238E9B0`: ali o campo tem só 4 valores (`0`, `1`, `0x101`, `0x10001`) e `+0x28`/`+0x30`
caem dentro do nome. O descritor de runtime do setter é outra estrutura; o elo
descritor↔linha da tabela é `NÃO PROVADO` (`checks/p_table_fields.txt`).

**Mapa dos 143 params — `NÃO EXTRAÍDO` (leitura de 2026-11-22, superada no fechamento abaixo):**
a tabela `0x238E9B0` tem apenas 3 refs RIP (`0x3314C0`, `0x331AC8`, `0x331B0A`), nenhuma com
store em campo de estado. Não há instrução que ligue um parâmetro nomeado a um offset de
`ctx` **por nome** — a ligação de 2026-11-23 é por **índice**, e os nomes vêm do `+0x14` da
própria tabela. Não usar os nomes de `params.csv` como prova.

**Caminho de setup não lê parâmetro diretamente (2026-11-23):** `0x861DB0` (4.217 B) é o
**único** chamador do factory `0x862E40` (que aloca `0xC1A8`, chama `00862E72 0x8634A0` com
`rdx=arg1`, `r8=arg2`, `xmm3`). O prólogo de `0x861DB0` é aritmética de dispatch/proteção
que **não lê argumento**: `00861DF4 and edx,0x80000001`, `00861E33 mov eax,0x1948b0fd` +
`imul`, `00861E50 imul eax,edx,0x51` (candidato a predicado opaco; **`NÃO PROVADO`** que seja
ofuscação). `0x8634A0` recebe dois **enums de tipo/contagem**, não valores contínuos:
`[r8]`/`[r8+8]` passam por `0x56B140` (`008634E5`, `008634EE`; mesma função que mapeia o
enum de bandas) e por `0x85E6C0` (`008634FB`–`0086350A`), gravando no objeto criado:
`+0x10 = 0x56B140([r8])`, `+0x14 = 0x56B140([r8+8])`, `+0x18 = 0x85E6C0([r8])`,
`+0x20 = 0x85E6C0([r8+8])`, `+0x28 = arg4` (`0086350F`/`0086352B`). A ligação de `[r8]`/
`[r8+8]` com um parâmetro nomeado **não foi lida** → `NÃO EXTRAÍDO`. Não usar `params.csv`
como prova.

#### Leitura 2026-11-23 — o objeto de `ctx+0x2C38` tem 6 campos lidos (PROVADO)

`0x8B3ED0` carrega `state = *(void **)(ctx + 0x2C38)` cinco vezes no prólogo e copia campos
para a pilha (`008B3F5C`–`008B3FBA`). É o primeiro mapa de **leituras** de estado com RVA:

| Offset | Tipo | Destino | Instrução de carga | Instrução de store na pilha |
|---:|---|---|---|---|
| `+0x00` | f32 | `[rbp-0x10]` | `008B3F82 mov eax,[rax]` | `008B3F84 mov [rbp-0x10],eax` |
| `+0x04` | f32 | `[rsp+0x30]` | `008B3FA9` | `008B3FAC` |
| `+0x28` | f32 | `[rbp]` | `008B3F9C` | `008B3F9F` |
| `+0x3C` | f32 | `[rbp+8]` | `008B3FB7` | `008B3FBA` |
| `+0x4C` | f32 | `[rsp+0x40]` | `008B3F8E` | `008B3F91` |
| `+0x52` | u8 | `[rbp+0x4A30]` | `008B3F71 movzx eax,byte [rax+0x52]` | `008B3F75` |

`+0x00` e `+0x04` são exatamente as duas entradas do escalar de ganho (§8.2c da spec:
`008B5AFB` e `008B5B07`). Os stores desses seis campos estão provados no fechamento abaixo
(2026-11-23).

#### Fechamento 2026-11-23 — o escritor é o setter de parâmetro `0x867D80` (PROVADO)

`state = engine+0x54` (já provado). O escritor é `0x867D80` (1.792 B), alcançado pelo thunk
`0x862EF0` (`00862EF0 mov rcx,[rcx]`, `00862EF3 cvtsd2ss xmm2,xmm2`, `00862EF7 jmp 0x867D80`),
instalado como `[obj+8]` em `00862E90`. Cadeia de posse, toda com RVA:

| # | RVA | Fato |
|---|---|---|
| 1 | `00862E52` `00862E72` | `0x862E40` aloca `0xC1A8` e chama `0x8634A0(rcx=novo, rdx=arg1, r8=arg2)` |
| 2 | `008634CA` `00864057` | `0x8634A0` faz `r14 = rcx` e devolve `rax = r14` |
| 3 | `00862E7C` `00862ED9` | `0x862E40` grava `[obj+0] = rax` (base do motor) |
| 4 | `0086369D` `008636A5` | `0x8634A0` inicializa o estado em `r14+0x54` (`0x864070`) |
| 5 | `008638CA` `00863905` `00863929` | `0x8634A0` põe `r14+0x54` no 5º argumento e chama `0x86A4E0` |
| 6 | `00870941` | `0x86FE90` grava esse ponteiro em `[ctx+0x2C38]` |

⇒ `rbx` em `0x867D80` (`00867DA6 mov rbx,rcx`) é a base do motor; **`[rbx+0x54+k]` é
`state+k`**. Stores em `[rbx+0x50]` (`00867F07`) e `[rbx+0x4a]` (`00867F4D`) ficam **fora**
do estado — são o subobjeto anterior.

**Entrada:** `xmm8 = clamp(xmm2,0,1)` (`00867DC2` com `xmm10=0`; limite `1.0f` em `0x2079F9C`,
`00867DE2`/`00867DED`); `xmm6` = valor do descritor (`min/max` de `[rdx+0x28]`,
`[rdx+0x30]` e `call qword ptr [rdx+0x50]` em `00867E10`, depois `call 0x1798F8A` =
`roundf` em `00867E43`); `r8b = xmm8 >= 0.5f` (`0x2079EA8`, `00867E48`/`00867E5C`);
`idx = [rdx]` (`00867E50`); `idx > 0x8E` → epílogo (`00867E60`/`00867E65`);
`sel = byte[0x8683CC+idx]` (`00867E72`) e `alvo = dword[0x868348+sel*4]` (`00867E7B`).
A tabela de bytes tem **143 entradas**; a de alvos, **33**.

**Os 6 campos lidos pela dinâmica:**

| Offset | Tipo | Índice | Handler / store | Valor |
|---:|---:|---:|---|---|
| `+0x00` | f32 | 0 | `0x867F6E` / `00867F73` | `xmm8` |
| `+0x04` | f32 | 5 | `0x867F7B` / `00867F80` | `xmm8` |
| `+0x28` | f32 | 17 | `0x868061` / `00868066` | `xmm8` |
| `+0x3C` | f32 | 18 | `0x86806E` / `00868073` | `xmm8` |
| `+0x4C` | f32 | 92 | `0x8681CD` / `008681E7` | `xmm8 < 0.999` ? `xmm6` : `60.0f` (`0x207A474`; f64 `0.999` em `0x207A120`) |
| `+0x52` | u8 | 16 | `0x868055` / `00868055` | `r8b` |

**Mapa completo índice → offset (PROVADO; `s = state`):**

| Índices | Handler | Destino | Tipo | Valor |
|---|---|---|---|---|
| 0 | `0x867F6E` | `s+0x00` | f32 | `xmm8` |
| 1 | `0x867E88` | `s+0x57` | u8 | `r8b` |
| 2 | `0x867EC8` | `s+0xB0` | i32 | `min(r9d-1,7)` |
| 3 | `0x867F07` | `engine+0x50` (**fora do estado**) | i32 | `r9d` |
| 4 | `0x867F10` | `s+0x58` | u8 | `r8b` |
| 5 | `0x867F7B` | `s+0x04` | f32 | `xmm8` |
| 6 | `0x867FBD` | `s+0x08` | f32 | `xmm8` |
| 7 | `0x867FFF` | `s+0x0C` | f32 | `xmm8` |
| 8 | `0x867FAB` | `s+0x10` | f32 | `xmm6` |
| 9 | `0x867FB4` | `s+0x14` | f32 | `xmm6` |
| 10 | `0x867FED` | `s+0x18` | f32 | `xmm6` |
| 11 | `0x867FF6` | `s+0x1C` | f32 | `xmm6` |
| 12 | `0x868009` | `s+0x20` | f32 | `xmm6` |
| 13 | `0x868012` | `s+0x24` | f32 | `xmm6` |
| 14 | `0x86801B` | `s+0x51` | u8 | `r8b` |
| 15 | `0x868038` | `s+0x53` | u8 | `r8b` |
| 16 | `0x868055` | `s+0x52` | u8 | `r8b` |
| 17 | `0x868061` | `s+0x28` | f32 | `xmm8` |
| 18 | `0x86806E` | `s+0x3C` | f32 | `xmm8` |
| 19..90 | `0x86807E` | `s+0xB8+0x20·b` | — | `b=(i-19)/9`, `r=(i-19)%9` (tabela abaixo) |
| 91 | `0x867F55` | `s+0xAC` | i32 | `min(r9d-1,7)` (**`-1` = nenhum**: ctor grava `0xFFFFFFFF` em `+0xAC`) |
| 92 | `0x8681CD` | `s+0x4C` | f32 | ver acima |
| 93 | `0x8681F2` | `s+0x40` | f32 | `powf(10, 0.05·xmm6)` = `10^(v/20)` (`0x207A360`, `0x2079D88`) |
| 94 | `0x868219` | `s+0x44` | f32 | `0.01·xmm6` (`0x2079D48`) |
| 95 | `0x868230` | `s+0x48` | f32 | `powf(10, 0.05·xmm6)` |
| 96 | `0x868257` | `s+0x54` | u8 | `r8b` |
| 97 | `0x868263` | `s+0x55` | u8 | `r8b` |
| 98..122 | `0x86826F` | `s+0x1B8+8·g+{0,4,5,6,7}` | f32/u8 | `g=(i-98)/5`, `r=(i-98)%5` |
| 123 | `0x8682F4` | `s+0x2C` | f32 | `xmm8` |
| 124 | `0x868301` | `s+0x30` | f32 | `xmm8` |
| 125 | `0x86830E` | `s+0x34` | f32 | `xmm8` |
| 126 | `0x86831B` | `s+0x38` | f32 | `xmm8` |
| 127..142 | `0x868328` | `s+0x1D+i` (`0x9C..0xAB`) | u8 | `r8b` (`0086832A [rax+rbx+0x71]`) |

Bloco de bandas 19..90 — `base = s+0xB8+0x20·b`:

| `r` | DV | Tipo | Valor |
|---:|---:|---|---|
| 0 | `+0x00` | u8 | `r8b` (`008680D2`) |
| 1 | `+0x01` | u8 | `r8b` (`008680DF`) |
| 2 | `+0x04` | f32 | `xmm6` — frequência (`008680F0`) |
| 3 | `+0x08` | f32 | `24·xmm8 - 12` (`0x207A3C8`=24, `0x207A384`=12) |
| 4 | `+0x0C` | f32 | `0` se `x<=0`, senão `2·asinh(1/(2x))/ln2` (`0086812D`, IAT `0x1D8D810` = `asinh`, `0x207A1A0` = 2.8853900817779268) |
| 5 | `+0x10` | f32 | `expf(ln6 + xmm8·(ln128-ln6))` = `6·(128/6)^t` (`0x207A4C4`=128, `0x207A0D8`=ln 6, IAT `logf` `0x1D8D808`/`expf` `0x1D8D7F0`) |
| 6 | `+0x14` | f32 | `xmm6` (`00868185`) |
| 7 | `+0x18` | i32 | `r9d` (`0086818E`) |
| 8 | `+0x1C` | i32 | `r9d` (`00868198`) |

Grupos de canal 98..122 — `base = s+0x1B8+8·g`, 5 grupos: `r=0` → `+0x00` f32 `xmm8`;
`r=1..4` → `+0x04/+0x05/+0x06/+0x07` u8 `r8b` (`008682DC`, `008682D2`, `008682C8`,
`008682BE`). Isso casa com as leituras `+0x1BF`/`+0x1C7` de `0x8C1440`: são o 5º byte
(`link_all`) dos grupos 0 e 1.

**Constantes lidas:** `0x2079F9C`=1.0f, `0x2079EA8`=0.5f, `0x207A3C8`=24.0f, `0x207A384`=12.0f,
`0x207A4C4`=128.0f, `0x207A0D8`=1.7917595f (ln 6), `0x207A120`=f64 0.999, `0x207A474`=60.0f,
`0x2079D88`=0.05f, `0x2079D48`=0.01f, `0x207A360`=10.0f.
**Nomes dos imports (diretório em `0x2175044`, ILT `0x2176878`):** `0x1D8D7E0`=roundf,
`0x1D8D7F0`=expf, `0x1D8D808`=logf, `0x1D8D810`=asinh, `0x1D8D818`=powf.

**Índice == campo `+0x10` da tabela `0x238E9B0` (PROVADO por isomorfismo, não por nome):**
os 143 descritores têm os mesmos cortes da tabela de despacho — 0..18 avulsos, **19..90 =
8×9**, **91** avulso, **92..97 = 6**, **98..122 = 5×5**, **123..126 = 4**, **127..142 = 16**
(`Channel 1..16 enabled`). O handler de 127..142 grava 16 bytes consecutivos (`0x9C..0xAB`);
o de 98..122 usa passo 8 sobre 5 grupos. Fecha o mapa: **índice → offset do estado**, com o
nome lido da própria tabela (`+0x14`), não de `params.csv`.

**Ainda `NÃO PROVADO`:** (a) o significado DSP de cada campo (só `+0x00`/`+0x04` têm uso
provado, §8.2c); (b) a identidade do callback `[rdx+0x50]` (normalização valor↔unidade);
(c) que o host entregue a este setter o índice `+0x10` da tabela `0x238E9B0`; (d) store por
ponteiro derivado do estado (a varredura de completude é por deslocamento — ver spec §8.3.1,
que lista os acertos rejeitados: `0x861B60`, `0x8634A0`, `0x867600`, `0x867730`).

**Artefato:** `tools/param_map.py` gera `checks/param_map.txt` com as 143 linhas
(`índice`, nome de `+0x14`, handler, store, tipo, valor); ele próprio confere
`[0x238E9B0+i*0x68+0x10] == i` para todo `i`.

**Tabela `0x238E9B0` decodificada (PROVADO por conteúdo):** passo `0x68`; `+0x00` e `+0x08`
são **ponteiros de código** (base `0x199B0000`; ex. `0x19CE5910` → RVA `0x335910`,
`0x19CC9170` → `0x319170`, ao lado do thunk de vtable `0x319180`); `+0x10` é o **índice
sequencial 0..142**; `+0x14` é o nome ASCII (`char[0x2C]`); `+0x40`/`+0x48` são dois `f64`;
`+0x50` são as flags; `+0x58`/`+0x60` são mais dois ponteiros de código (`0x19CE51A0` →
`0x3351A0`, `0x19CE51E0` → `0x3351E0`). As três refs RIP (`0x3314C0`, `0x331AC8`,
`0x331B0A`) são construtoras de um handle `{int index; const Table *base}` — `0x3314C0:
mov [rcx],edx; mov [rcx+8],rax` com `rax = 0x238E9B0`. Logo a tabela é um **registro de
descritores com 4 callbacks**, não um `AudioProcessorValueTreeState`; o mapa
parâmetro→offset fecha no fechamento acima (por índice, `+0x10`).

**Critério de saída (cumprido em 2026-11-23):** os stores de `+0x2C38` (2 sítios) e os stores
dos 6 campos lidos estão provados; o mapa **143 índices → offset** está fechado com RVA por
linha. Ficam explícitos como `NÃO EXTRAÍDO`: o store de `+0x5F8`/`+0x5ED0` (os `lea`
`00862F89`/`00862F95`/`00863994` ainda não foram ligados a um store) e a identidade do
callback `[rdx+0x50]` do descritor.



### 23.9 Etapa H — `dsp-spec.md` em dia — **FECHADA (2026-11-23)**: dinâmica inline, curvas de banda e `0x8C1440`

#### Leitura 2026-11-23 — a dinâmica está **inline** em `0x8B3ED0` (corrige §15.1)

`tools/scan_div.py` (varredura de `divss`/`maxss`/`minss` na região `0x8A0000–0x8E0000`,
chain-aware) mostra que os blocos de dinâmica estão **no próprio orquestrador**
`0x8B3ED0` — 23 `mulss`, 17 `subss`, 7 `maxss`, 5 `minss`, 4 `divss`
(`checks/fops8b3ed0.txt`). O §15.1 acertou só sobre a camada **vetorial** (`*ps`/FMA = 0).

**Bloco (a) `008B4E20`–`008B4FAC` — rugosidade média de cada array de banda.**
`acc += (double)fabsf(v[k]-prev)/((double)prev+1e-7)` em laço (`008B4E8B`–`008B4F23`),
`m = (float)(acc/n)` (`008B4F88`), e se `m < 0.001` (`008B4F93 comisd`, constante f64
`0x2079F48`) escala o array por `m` (`008B4FA7 call 0x1220`). Máscara de abs em
`0x207BAE0` via `008B4E93 andps`; `1e-7` f64 em `0x2079E08` (`008B4E0D`).

**Bloco (b) `008B68AB`–`008B6939` — coeficiente de one-pole a partir de tempo.**
Se `[r13+0x58]!=0`: `N=(float)(int64)[r13+0x60]` (`008B68BC`–`008B68E0`);
`x=((float)[r13+0x20]/N)*0.001f*500.0f` (`008B68E4`/`008B68F9`/`008B6901`, constantes
`0x2079D24` e `0x207A560`); `coef = 1.0 - pow(0.1, 1.0/x)` (`008B690C divsd` com
`xmm6=1.0` de `0x207A138`; `008B6918 call 0x1C9A5AD` = **`pow` double**, IAT
`0x1D8D848`; `0x207A030` = `0x3FB99999A0000000` = `(double)0.1f`; `008B6932 subsd`).
**`NÃO PROVADO`:** qual de `+0x20`/`+0x58`/`+0x60` é sample rate e qual é tempo.

**Bloco (c) `008B5AF2`–`008B5CA7` — escalar de ganho aplicado a todas as bandas.**
Entradas `s0 = state[0x00]` (`008B5AFB`) e `A = state[0x04]` (`008B5B07`):

```
T  = clamp((s0-0.8f)*5, 0, 1)                            ; 008B5B36/46, clamp por cmov 008B5B4E-67
u  = 4^clamp((1-0.5f*A)*T, 0, 1)                         ; expf 008B5B84, ln4=0x207A00C (1.3862944)
y  = expf((logf(powf(10,2.4f)+0.1f)+ln10)*clamp(s0,0,1)-ln10)-0.1f ; 008B5B99-008B5BD5
v  = powf(10, -24*0.05f*clamp(A*A,0,1)) = 10^(-1.2*clamp(A²,0,1)) ; 008B5BE2-008B5BFD
scale = u*(y*v)                                           ; y*v 008B5C02, *u 008B5C8A
0x1220(banda, n, scale) para cada banda                    ; 008B5C90-008B5CA7
```
Constantes: `0.5f` `0x2079EA8`, `0.8f` `0x2079F38`, `5.0f` `0x207A2D8`, `0.1f`
`0x2079DB0`, `2.4f` `0x207A1E8`, `-2.3025851f` `0x207A6D4`, `+2.3025851f` `0x207A1D0`
(`ln 10`), `-24.0f` `0x207A734`, `0.05f` `0x2079D88`, `10.0f` `0x207A360`, `1.0f`
`0x2079F9C`. Thunks: `0x1C9A9D7`=`expf`, `0x1C9A9FB`=`logf`, `0x1C9AA01`=`powf`
(`checks/thunk_map.txt`). **`NÃO PROVADO`:** nomes de `s0`/`A` e o ramo `r14b==0`
(`008B4FDC`→`008B51D4`, que chama `0x8C0230` e usa `powf(10,-0.45)` em `008B5370`).

**Bloco (d) `0x8CAE90` (245 B; 307 B chain-aware) — adaptador de layout do MAC**, não
detector. Assinatura (spec §11.1): `batch_mac(dst /*rcx*/, src1 /*rdx*/, src2 /*r8*/)`;
`n = dst->n` (`+0x80`), `len = dst->len` (`[rcx+0x84]`); `src1->n` em `[rdx+0x400]`.
Modo 1 (`008CAEB1`, contagens iguais): `mac(src1[i], src2[i], dst[i])` — no sítio
`008CAEF0`–`008CAEFA` isso vira `rcx=src1[i]`, `rdx=src2[i]`, `r8=dst[i]`, `r9d=len`.
Modo 2 (`008CAF12`, `dst->n==1`): `dst[0] += src1[i]*src2[i]`. Modo 3 (`008CAF65`).
O kernel real é `0x6CE80`: `0086CEBB vfmadd213ps ymm1,ymm0,[r8]` + `0086CEC4 vmovups
[r8],ymm1` ⇒ **`dst[i] += a[i]*b[i]` em float32 linear** (`dst=r8`, fontes `rcx`/`rdx`),
sem `ln/exp/pow/div`.

**Bloco (e) `0x8C3C20` já estava certo em §8.1** (smoother forward-backward `a=0.1`);
reverificado agora: `008C3C43 movss xmm3,[0x2079DB0]=0.1`, laço para frente
`008C3C90` e para trás `008C3D50` (começa em `n-2`, `008C3C50 lea rbx,[r10-2]`).

#### O que continua aberto na dinâmica

1. ~~**Detector de envelope (attack/release por banda)**: não localizado por instrução.~~
   **FECHADO em 2026-11-23**: `0x8C1440` transcrito (§23.9–H, spec §8.4); é estagiador de
   5 grupos + lei de mistura `dst ← (1−g)·dst + g·staged` (`g/2` **só** em `nch != 2` — correção
   de 2026-11-24 em §23.9-H), não o detector
   one-pole.
2. **Quem consome a curva de ganho** gravada na arena (§23.7) — `NÃO EXTRAÍDO`.
3. **Mapa param→offset** — **FECHADO em 2026-11-23** (§23.8 / spec §8.3.1): 143 índices →
   offset, escritor `0x867D80`. Em 2026-11-24: `+0x5F8`/`+0x5ED0` **fechados** (subobjetos
   embutidos, construtores `0x86A4E0`/`0x86A8C0` — `checks/p_extras.md` §P1); o callback
   `[rdx+0x50]` continua `NÃO PROVADO`, e ficou provado que ele **não** é campo da tabela
   `0x238E9B0` (§23.8, `checks/p_extras.md` §P2).

**Bloco (f) `0x8C0BD0` — detector por descritor, média suavizada (PROVADO por subagente,
2026-11-23; entrega em `checks/h_primitivas_8c0bd0.md`).** A função monta **5 descritores
locais de `0x410 B`** (`ptr[128]` + header `{2, N, N*4}`) em `rbp-0x60`, `rbp+0x3B0`,
`rbp+0x7C0`, `rbp+0xBD0`, `rbp+0xFE0`; cópias provadas em `008C0DB3`/`008C0E32`/`008C0EA5`
(8×`0x80` + `0x10`). Para cada descritor com `+0x10 == 2`:

```
sum2 = P0*P0 + P1*P1                     ; 008C0F3B
sum  = P0 + P1                           ; 008C10D9
sum  = max(sum, eps)                     ; 008C1199, eps=1.1920929e-7 @0x2079CF0
R    = sum2 / sum                        ; 008C11BF / 008C1218  (0x1550 = divisão)
P_k  = (1-g)*P_k + g*R                   ; 008C12B9 / 008C139C  (0x11F0 = dst += src*s)
```
`R = (P0²+P1²)/(P0+P1)` é uma **magnitude combinada** (limite entre `max` e `soma`), e
`P_k ← (1-g)P_k + g·R` é o one-pole — é o candidato mais forte a **detector com linking**.
Constantes: `1.0f` `0x2079F9C`, `1.1920929e-7f` `0x2079CF0`, vetor `1.0f×8` `0x1DF9DA0`.
**`NÃO PROVADO`:** identidade de `P0`/`P1` (L/R? bandas?), papel de `+0x10 == 2`, semântica
de `+0x400`/`+0x404`, e o que é `g` (attack/release?). `0x207A360 = 10.0f` **não** é usado
aqui.

**Correções de semântica das primitivas (subagente, 2026-11-23, contra §22.3/§17):**

| Thunk | Assinatura provada (RVA da prova) |
|---|---|
| `0x1190`/`0x4BC0` | `dst[i]=a[i]*b[i]`, **fora do lugar**: `a=rcx`, `b=rdx`, `dst=r8`, `n=r9d` (`00004BC7 mov rbp,rdx`; stores `00004C60`) |
| `0x1550`/`0x63640` | **divisão** `dst=num/den`: `den=rcx`, `num=rdx`, `dst=r8`, `n=r9d` (`00063676`, `00063787 vmulps`) |
| `0x11F0`/`0x5BC0` | `dst[i]+=src[i]*s`: `src=rcx`, `dst=r8` (in place), `n=r9d`, `s=xmm1` (`00005C46 vfmadd213ss xmm0,xmm1,[r8]`) |
| `0x1370`/`0xA120` | `dst[i]+=src[i]` — **vetor, não escalar**: `src=rcx`, `dst=rdx`, `n=r8d` (`0000A125`, `0000A1A5`) |
| `0x1100`/`0x3480` | clamp in place: `buf=rcx`, `n=edx`, **`bound=xmm2`**, `mode=r9d` (`4`=min `00003500`, `0`=max `00003640`, outro `= -5` `000034A4`) |
| `0x1220`/`0x2300` | `dst[i] *= s`: `dst=rcx`, `n=rdx`, `s=xmm0` (`0000232B call 0x1D2E460`; tabela `0x21C6008[4]`) |
| `0x12E0`/`0x8FA0` | `dst[i] += s`: `dst=rcx`, `n=rdx`, `s=xmm0`; **sai cedo se `s==0`** (`00008FC1`; tabela `0x21C6108[4]`) |
| `0x1340`/`0x9BA0` | `dst[i] *= a[i]` **in place**: `a=rcx`, `dst=rdx`, `n=r8d` (`00009C4D vmulps ymm1,ymm0,[rdi+r9*4]`, `00009C5A` store; `00009BA5 mov rdi,rdx`; tabela `0x21C6188[4]`) |
| `0x8CAFD0` | **não é thunk IPP**: alocador de bump da arena (`008CAFD0`–`008CB03E`), descritor `{p0,p1,n@0x10,4n@0x14}` |
| `0x61B790` | predicado `sel→val` (tabela em §23.9–H/spec §8.4.5), `0061B790`–`0061B85C` |
| `0x17978C0` | sonda de pilha antes de `sub rsp,0x14B0` (`008C145F`); identidade exata `NÃO PROVADA` (provavelmente `__chkstk`) |

#### Bloco (g) `0x8C1440` — FECHADO (2026-11-23; spec §8.4)

Desmontagem completa: `checks/8c1440.u8.dis` (1.787 linhas, LF, 7.800 B). Assinatura provada
pela posição dos *home slots* (`008C1440`–`008C145F` + `lea rbp,[rsp-0x13b0]` +
`008C145A sub rsp,0x14B0`, relidos em `008C19C8`/`008C3226`):

```c
void f8C1440(engine *e /*rcx*/, track *t /*rdx*/, arena *ar /*r8*/, void *r9_unused);
```

- `t+0x400 <= 2` ⇒ retorno imediato (`008C1467`/`008C1474`); `t+0x404` = **`n`**
  (`008C14B0` e repetido em `008C1582`/`008C15FB`/`008C167A`/`008C16F3`).
- `e+0x10` → vetor `{rec* begin; rec* end;}` (`008C1A77`/`008C1A8C`/`008C1A97`); registro de
  **0x18 B**: `+0x00` i32 `sel`, `+0x08` i32 `first_buf`, `+0x10` i32 `nch` (stride
  `008C1E09`/`008C2DFD`/`008C31ED`).
- **16 buffers de `n` floats**: 5 pares construídos inline em `008C150F`…`008C1763` e 3
  chamadas de `0x8CAFD0` (`008C179A`/`008C17BE`/`008C17E2`) que alocam 2 cada. Zeroização:
  8 sítios de `0x10D0` (`008C1808`…`008C19BA`), cada um em laço de 2 = 16 buffers.
- `0x8CAFD0` = **alocador de bump da arena** (`008CAFD0`–`008CB03E`): `p0 = base+fill·4`,
  `fill += align16(n)`, `p1` idem, `fill += align16(n)`; descritor
  `{p0@0, p1@8, n@0x10, 4n@0x14}`. O cursor é salvo em `[rbp+0xE0]` (`008C147A`) e
  **restaurado** em `008C32AA`.
- 5 grupos: tabela `0x2014360` = `{8,9,10,6,5}` (`008C1A4D`/`008C2356`/`008C2AA5`), laço
  `5` (`008C234D`/`008C321C`), enable `byte[state+0x1BF+8g]` (`008C1A6E`, `008C2ABA`).
- Predicado `0x61B790(sel, val)` **resolvido por inteiro** (`0061B790`–`0061B85C`):
  `0→1`; `1→val!=10`; `2→val!=9`; `3→(u)(val-9)>1`; `4→(u)(val-8)>2`;
  `5→(u)(val-0x10)<=2`; `6→h(4)&&!h(5)`; `7→(u)(val-8)<=1`; outro→`sel==val`.
  `0x8C1440` chama o helper 8× (`008C1B2F`, `008C1B43`, `008C1F9E`, `008C1FB2`, `008C2B6A`,
  `008C2B7D`, `008C2ED3`, `008C2EE6`) e inlina a mesma tabela 4× (`008C1AB4`, `008C1EE4`,
  `008C2AF4`, `008C2E24`).
- Fases: setup → leitura dos 10 campos (`008C19CF`–`008C1A38`) → passagem A
  (`008C1A58`–`008C1E17`, MAC `0x1580` + acumulação `0x1370`) → guarda `max(x,1e-7)`
  (`008C2367`–`008C2459`, 4 pares) → normalização `0x1550`×4 (`008C2545`/`008C263D`/
  `008C273B`/`008C2828`) → passagem B (`008C2AA5`–`008C31FA`) → restaura o cursor.
- **Lei de mistura** (`008C2CC4`–`008C2DF5`, `008C30A4`–`008C31E0`):
  `0x1220(canais, n, 1−g)` e depois `0x11F0(canais, D, n, g)`.
  **Correção 2026-11-24 (J3):** o `×0,5` **não** é o caminho estéreo. `nch == 2`
  (`008C2BAE`/`008C2BB4`, `008C2F88`/`008C2F8D`) usa `g` inteiro no laço por canal
  (`008C2D90`..`008C2DB4`, `008C3180`..`008C31A3`); o caminho `nch != 2`
  (`008C2DB8`/`008C31A7`) faz alvo `1−g` e MAC `g·0,5` (`008C2DEA`/`008C31D5 mulss`,
  `xmm11 = 0,5` em `008C2A67`, `0x2079EA8`).
  **Correção 2026-11-25:** `dst` = buffers de canal do registro; `src` = **resultado da
  divisão** (`new1`/`T1`/`T2`/`T3`), não o "buffer estagiado". Logo
  `ch ← (1−g)·ch + g·D`, `D = Σregistros ch² / Σregistros ch`.
- **Papéis dos 16 buffers, divisões e coeficiente por grupo — PROVADOS em 2026-11-25**
  (`checks/q_8c1440_buffers.md`, spec §8.4.3/§8.4.7/§8.4.8):
  pares 0/2/4/6 = `Σ_ch ch²` (`0x1580` com `a=b=canais`); pares 1/3/5/7 = `Σ_ch ch`
  (`0x1370`, `src=canais`, `dst=par`) e único conjunto clampado (`0x1100` max, `1e-7`,
  `008C2393`/`23CD`/`240D`/`244D`). As 4 divisões escrevem em **alocação nova** e
  reaproveitam o slot do numerador: `new1=par0/par1` (`008C2545`, slot `[rbp-0x40]` em
  `008C250E`), `T1=par2/par3` (`008C263D`), `T2=par4/par5` (`008C273B`), `T3=par6/par7`
  (`008C2828`). O `den` de `T3` é o par 7 **capturado em `xmm11`** (`008C241B`) antes do
  reaproveitamento do slot — o par 7 nunca é destino. `A/B/C/D` (`008C298E`/`29CE`/`2A0E`/
  `2A4E`) somam os 2 canais de `new1/T1/T2/T3` e só o caminho mono os consome.
  Mapa coeficiente: `enable != 0` ⇒ `state+0x2C`; desabilitado, `tipo 8/9` ⇒ `+0x30`
  (exige flag), `tipo 6` ⇒ `+0x34`, `tipo 5` (`sel ∈ {0x10..0x12}`) ⇒ `+0x38`, `tipo 0xA` ⇒
  **nunca**. `0x882FC0`:
  **0 ocorrências** no corpo — a hipótese "buffer recebe a curva" está refutada.
- `NÃO PROVADO` (mesmo doc, §9): nome/unidade dos 4 coeficientes; faixa válida de `g`;
  intenção musical da média ponderada por potência; `nch > 2` (o ramo `008C1E4B` usa só
  `t->buffers[first_buf]`).

#### Bloco (h) `0x882FC0` + `0x88E130` — FECHADOS (2026-11-23; spec §8.2(e)/(f))

`0x88E130(dst, src, A /*xmm2*/, k /*xmm3*/, G /*5º arg*/)` (`checks/88e130.u8.dis`):

```
se fabsf(k) <= 1.1920929e-7 → dst[i] = 1.0
senão, por amostra (v = dst[i], semeado de src[i] se src->flag@0x80==1):
  u = (v + 1.1920929e-7) / max(A, 1.1920929e-7)      ; 0088E256, 0088E275
  y = exp( G·0.115129255·(1/(1+exp(-(k/6)·log2 u)) − 0.5) )
                                                      ; 0088E298..0088E3B7
```

Ordem provada: `ln` (`0088E298`, `0x1C8500`→`0x293760`) → `·1.44269502` (`0088E2AB`,
`0x207A020`) → `·(−k/6)` (`0088E1E7` `1/6`@`0x2079DE0`, `0088E2B3 xorps`, `0088E2D0`) →
`exp` (`0088E2EE`, `0x1C84A0`→`0x240C00`) → `+1` (`0088E311`) → **recíproco aproximado**
(`0088E32F`, `0x1C8530`→`0x29B260`, `vrcpps`+Newton `0029B442`/`0029B456`) → `−0.5`
(`0088E352`, `0x207A690`) → `·G` (`0088E376`, `[rsp+0x100]`) → `·0.115129255`
(`0088E399`, `0x2079DBC`) → `exp` (`0088E3B7`).

`0x882FC0(this, band, A1, A2, arena)` (`checks/882fc0.u8.dis`): aloca 2 buffers temporários
na arena (`0088301F`–`00883050`, `00883117`–`0088315A`) e restaura o cursor
(`008833C0`); bloco 1 chama `0x88E130(bufA, &bandcopy, 500.0f, 12.0f, −20·log10(A1))`
(`008830E7`; `500`@`0x207A560`, `12`@`0x207A384`) e multiplica por
`powf(10, 0.5·log10(A1))` (`00883107`, `00883112`); bloco 2 idem com `A2` e `2000.0f`
(`008831D1`, `0x207A5A8`); depois `0x87A7A0` (`0088327A`) e `0x1340` (mul elemento a
elemento: `dst[i] *= a[i]`, `00009C4D vmulps`) aplicado a `this[0]` (1 ponteiro se
`this[0x80]==1`, senão `this[0x80]` ponteiros) — `008832E4`/`00883309`/`00883388`/
`008833A9`. Fator resultante por amostra: **`A1^(1−σ1)·A2^(1−σ2)`**, com
`σ_i = 1/(1+exp(−(12/6)·log2((v_i+eps)/max(A_i,eps))))`.
`NÃO PROVADO`: se `band->flag@0x80 == 1` nos dois sítios de `0x87BB60`, e a origem de
`A1`/`A2`.

**Novos offsets de estado lidos (PROVADO, `0x8C19CF`–`0x8C1A22`; mesmo objeto de
`ctx+0x2C38`):** `+0x2C`, `+0x30`, `+0x34` (f32, para `[rbp+0xC0/0xC4/0xC8]`) e `+0x38`
(f32, para `[rsp+0x28]`); `+0x1BF` e `+0x1C7` (u8, via `movzx`, `008C1A14`/`008C1A22`).
Total: **10 campos lidos** do objeto de `ctx+0x2C38` (§8.3 da spec).

### 23.10 Etapa I — oráculo (**FECHADA 2026-11-24**)

`app/` não existe mais, então o host foi reconstruído do zero em **`host/`** (Rust std-only,
FFI crua de `kernel32`, sem dependência externa, sem injeção/hook). Ele carrega
`original/soothe3.vst3` read-only por `GetPluginFactory` (o módulo **não** exporta
`DllGetClassObject`), inicializa `IComponent`/`IAudioProcessor` e grava WAV float32.

Verificado nesta sessão, 48 kHz/bloco 512: 94 blocos `S_OK`, 48.000 frames, latência
**2304**, duas execuções com SHA-256 idêntico
(`1218C801A5E61A7591DCE500C40A166E8598532666AE5B7808816899B42BE67B`), WAV em
`host/test/out_soothe3.wav`. Três fatos que o null-test tem de respeitar:

1. o plugin **não é transparente** no estado padrão (RMS da diferença alinhada por 2304:
   −6,6 dBFS) — comparar plugin × port, não entrada × saída;
2. a saída **muda com o bloco** (mesma métrica: −6,6 / −8,2 / −11,6 dBFS em 512 / 4096 /
   48000); causa `NÃO EXTRAÍDO`;
3. o preset é o de fábrica (o host não faz `setState`).

A rota do dump repachado (`dumpsooth/soothe3_loadable.dll`, `ImageBase 0x199B0000`) continua
morta: `LoadLibraryW` morre em `0xC0000005` dentro do `DllMain` (§19.7). A rota viva é o
host VST3 — que agora existe de novo.

Nenhum coeficiente sai do oráculo: é validação, não extração.

### 23.11 Etapa J — port Rust

Só depois de A–G. Cada linha do port precisa apontar para a linha da spec, que aponta para
o RVA. O que não tiver prova fica marcado `NÃO EXTRAÍDO` no código, nunca aproximado.

### 23.12 Ordem recomendada para a próxima sessão

```
D0 [FEITO] -> A [FEITO] -> B [FEITO] -> E [FEITO] -> D1 [FEITO]
   -> C [FEITO em 2026-11-23: escritor, alocador, contagem e tabela caso->vetor]
   -> §24 [PROVADO em 2026-11-23: 0x20E0 = FFT fwd, 0x7B40 = FFT inv; sabor NÃO PROVADO]
   -> F [FECHADO em 2026-11-23: K=δ0 por construção; FIR passa-direto; math do design
         identificada (ln/exp) e fórmula de 0x882DE0]
   -> G [FECHADA em 2026-11-23: escritor 0x867D80; 143 índices -> offset; 6 campos de estado]
   -> H [FECHADA em 2026-11-23: dinâmica inline (4 blocos), 0x8C0BD0 = detector,
         0x8C3C20 = smoother, 0x8C1440 = estagiador+mistura, 0x882FC0/0x88E130 = curvas]
   -> K [FECHADA 2026-11-24: 5 faixas + `0x8C33D0` + satélites + `0x1400` (dot) PROVADOS]
   -> L [FECHADA 2026-11-24: +0x80 = contagem; "curva espectral" sem recursão (23 ops)]
   -> M [FECHADA 2026-11-24: bandas runtime; `0x8BA7B0`/`0x8A1EE0` = 1 vs 0]
   -> N [FECHADA 2026-11-24: ordem núcleo→análise]
   -> O [FECHADA 2026-11-24: sem lei de estéreo; ganho de overlap-add]
   -> P [FECHADO 2026-11-24: `p_extras.md`; sobras marcadas `NÃO EXTRAÍDO` com RVA]
   -> I [FECHADO 2026-11-24: host em `host/`, WAV em `host/test/out_soothe3.wav`]
   -> J [FECHADO 2026-11-24: J1/J2 10 testes, J3 12, J4 13, J5 7, J6 8]
   -> J0 [FEITO 2026-11-25: crate `port/` com os kernels como fonte única + runner;
          57 testes J + 18 do port verdes; gaps de `pending.rs` com RVA]
   -> Q [FECHADO 2026-11-25: 0x8C1440 / 16 buffers + coeficiente por caso;
         `checks/q_8c1440_buffers.md`, spec §8.4.3/§8.4.5/§8.4.7/§8.4.8]
   -> Q-port [FEITO 2026-11-25: `port/src/stage.rs` (passagem A, clamp, 4 divisões,
         somas, passagem B) + 12 testes; `pipe::mix_lane` corrigido para FMA
         (`00005C85`); divisão 0x1550->0x63640 é o gap bloqueante]
   -> PRÓXIMO: transcrever 0x63640 (divisão vrcpps+Newton) -> ln/exp IPP bit a bit
      -> recíproco 0x88E130 -> sample rate -> port completo -> null-test
      (mesmo bloco, alinhamento 2304)
```

D0 (§23.4): `0x8B2C30` é FIR de 32 taps com coeficientes por bloco. A (§23.1): `0x8CAE90`
é MAC em lotes de bandas; `0x1580` é MAC com FMA, não soma. B (§23.2): ordem das 9
primitivas provada por opcode. E (§23.6): pseudocódigo de `0x8C33D0` com RVA. D1 (§23.5):
`0x8BF650`/`0x8BFD30` são despacho/plumbing. F (§23.7) **FECHADA em 2026-11-23**: `K=δ0`
por construção (reset + `1.0f` antes da cópia por valor); FIR é passa-direto. G (§23.8)
**FECHADA em 2026-11-23**: o setter `0x867D80` é o escritor dos campos de estado (cadeia
`0x862E40` → `0x8634A0` → `[obj+0]` → `0x862EF0` → `rbx`), o mapa 143 índices → offset está
provado e o índice é o `+0x10` da tabela `0x238E9B0`. H (§23.9) **FECHADA em 2026-11-23**:
dinâmica inline em `0x8B3ED0` (4 blocos), `0x8C0BD0` = detector, `0x8C3C20` = smoother,
`0x8CAE90` = despacho de MAC, **`0x8C1440`** = estagiador por grupo + lei de mistura
(spec §8.4) e **`0x882FC0`/`0x88E130`** = curvas `A^(1−σ)` (spec §8.2(e)/(f)).

C (§23.3) **fechada em 2026-11-23**: `[ctx+0x10]`/`[ctx+0x18]` vêm de `[E+0x18]`/`[E+0x20]`
(escritos em `00863503`/`00863535` pelo retorno de `0x85E6C0`), os descritores são montados
por `0x85E6C0` (23 casos, tabela `0x85FFA0`) e alocados por `0x563E40` com
`operator new(24·n)`; `[outer+8] = ctx` em `0088FB9C`. Tabela caso→vetor e Rust em §23.3.

**§24 fechado em 2026-11-23** (§24.4): `0x1010`/`0x1280` são stubs de dispatch de CPU da
IPP (índice 4 → `0x20E0`/`0x7B40`); os dois corpos de 256 B são o mesmo wrapper de spec,
diferindo só no slot (`0000214A call [rcx]` = forward, `00007BAA call [rcx+8]` = inverse),
validando `[spec]==7`. O chamador `0x8B2680` faz FFT → multiplicação de `n/2+1` pares
complexos → FFT inversa → escala `1/n`. **Consequência:** o port reimplementa a
transformada. `NÃO PROVADO`: sabor (RToCCS/RToPerm/RToPack) e construtor da spec.

**Próximo: null-test plugin × port — J (port Rust) FECHADO em 2026-11-24.** K–P estão fechados
(§23.15 balanço, `checks/p_extras.md`). G e H fecharam o *esqueleto* (estagiador, mistura,
detector, smoother, curvas); K fechou o miolo que produz o ganho por banda (5 faixas de
`0x8B3ED0`) e L fechou o tipo de filtro (curva espectral, sem recursão). As sobras de P estão
marcadas `NÃO EXTRAÍDO`/`NÃO PROVADO` com RVA e entram no código como comentário — não como
aproximação. J fechou em J1–J6 (`stage_j_core.rs` 10, `stage_j_pipe.rs` 12, `j4_fft.rs` 13,
`stage_j_chan.rs` 7, `stage_j_engine.rs` 8), com `0x88300` e os twiddles fora do áudio
(`NÃO EXTRAÍDO`, §24.5-(3)). O null-test exige um port completo do motor (hoje há fragmentos).

De G sobra só `NÃO EXTRAÍDO`: store de `+0x5F8`/`+0x5ED0` e identidade do callback
`[rdx+0x50]`. De H, o papel dos 16 buffers e a atribuição grupo→coeficiente de `0x8C1440`
foram **PROVADOS** em 2026-11-25 (`checks/q_8c1440_buffers.md`); resta `NÃO PROVADO` só o
nome/unidade dos 4 coeficientes, a faixa de `g`, a intenção musical e `nch > 2`. Continua
`NÃO EXTRAÍDO` a origem de `A1`/`A2` em `0x882FC0` (spec §8.2(f)).
I **fechada** em 2026-11-24: host reconstruído em `host/` e WAV do null-test em
`host/test/out_soothe3.wav` (§23.10/§15.3).

### 23.13 O que não fazer

- Não estimar tamanho de FFT, taxa de bandas ou constante de tempo. Se não está no dump,
  é `NÃO EXTRAÍDO`.
- Não usar `reach_kernels.py` como filtro (§22.5).
- **Não confundir RVA de 5 dígitos com RVA de 7.** `0x8B660` (570.976) e `0x8B3ED0`
  (9.126.610) são regiões diferentes; foi assim que o §22.5 nasceu errado.
- **Não usar o tamanho do `functions.csv` para o núcleo:** `0x8B3ED0` aparece com 49 B e
  tem 20.209 B chain-aware. Usar `show_func.py`.
- Não tratar `.pdata` sobreposto (`0x8B4268`, `0x8B2C55`) como função independente.
- **Não inferir número de taps pela contagem de `mulss`.** `0x8B2C30` tem 27 `mulss` e é um
  FIR de **32** taps: o compilador gera laços desenrolados cujos caminhos de resto se
  sobrepõem. Taps vêm da máscara (`0x1f`), não da contagem de instruções.
- **Não tratar as "primitivas" `0x1010/0x10A0/0x10D0/0x1220/0x1280/0x15E0` como código do
  plugin**: são stubs de dispatch do IPP (seções `IPPCODE`/`IPPDATA`). O corpo está em
  `tabela[4]` (§24.2).
- **Ponteiro de dado no dump é VA na base `0x199B0000`**, não `0x180000000`. Converter com
  `RVA = VA − 0x199B0000` antes de comparar com endereço do IDA.
- Não usar os scripts `frida_*.py` de `archive/agent2/temp_scripts/` — são hook/attach,
  proibidos pela regra anti-tamper.
- Não medir nada no bundle `archive/agent2/oracle_bundle_1.0.5/`: é **v1.0.5**, o dump é
  **v1.0.6**.

### 23.14 Conflito registrado com a âncora (não resolvido por edição)

`LEMBRAR DISSO.md` é congelado e **vence qualquer outro documento**. Ele lista, em
"O que ainda falta", item 2:

> Detector e lei de ganho — **provavelmente** em `0x8C02F0` / `0x8C0BD0`.

O §22 leu os dois e provou que são **plumbing de buffer**: nenhuma constante float própria,
só alocação na arena, cópias de 128 bits e chamadas às primitivas. O trabalho de
transformação está em `0x8CAE90` e nas primitivas.

Como o arquivo não pode ser alterado, a divergência fica registrada aqui e a leitura
correta é esta:

| Onde a âncora aponta | O que a leitura mostrou |
|---|---|
| `0x8C02F0` / `0x8C0BD0` = detector e lei de ganho | são wrapper: montam buffers e chamam. O detector/ganho está **depois** deles: `0x8CAE90` (callee de `0x8C02F0`) e a cadeia de `0x8C0BD0` (recíproco → clamp → FMA), cujos impls faltam abrir (§23.2) |
| "Núcleo `0x8B3ED0`, 20.209 B, 127 call, zero FMA" | bate — mas só via `show_func.py`. O `functions.csv` dá **49 B** para `0x8B3ED0`; quem confiar no CSV conclui que o núcleo é um stub (§22.5) |
| "Cluster aritmético `0x8BF5C0–0x8C4300`" | o cluster é real, mas é **plumbing** (§22). A aritmética densa da região está antes do núcleo, em `0x8B2C30` (28 `mulss`/`addss`, zero calls) — etapa D0 |
| "`N = 256` / `278` / `557`" | os três valores existem como bit pattern float no dump, mas `278 = round(256 × 48000/44100)` e `557 = round(256 × 96000/44100)`: os três são **uma fórmula**, não três constantes. Falta ler a instrução que escolhe o N — `NÃO PROVADO` até lá. **Lida em 2026-11-25 (M1)** para o `X` do estágio (`E+0x5F8+0x2C50`): `N = trunc(max(a/k,44100)·(1/44100))·256` (`0086FF35`/`0086FF39`, `arg5 = 0x100` em `0086A579`; `k = max(trunc((a+1)/44100),1)` em `00863531`..`00863552`) ⇒ **`a = 48000` → `N = 256`**, não 278 (e `a = 96000` → `k = 2`, `N = 256`). A âncora diverge da instrução; fica registrado aqui e vale a leitura (`checks/r_divisao_63640.md` §4.1). A identidade de `a` como taxa de amostragem é `NÃO PROVADA` (M4) |
| "latência 2.304 amostras @ 48 kHz", item 5 | medida no build **1.0.5** (bundle oráculo), não no dump 1.0.6. Registro histórico, **não** especificação do port (§19.5) |

Não há contradição de *fato* no item 2: a âncora escreve "provavelmente", e a própria âncora
diz "indício não é prova". O item 2 continua sendo o lugar de onde começar a procurar — só
que a busca avança um nível para dentro.

Os outros quatro itens de "O que ainda falta" (tipo de filtro, struct de estado, oráculo,
port) continuam válidos e estão mapeados nas etapas F, G, I e J.

**Segundo conflito (2026-11-24).** A âncora diz, na linha 79:

> O DSP é **banco de filtros no domínio do tempo**, não FFT. A FFT do binário é da GUI.

A leitura por instrução mostra que o caminho de áudio **usa** FFT. `000725BA`..`000725D6`
(dentro de `0x72480`, o `fwd` que `0x72180` grava em `wrapper+0x18`, alcançado por
`0x20E0` → spec → wrapper) chama `0x1D69E00` com `rdx = n/2` para a ordem 9, e a medição
(§24.5-(4)) mostra que `0x1D69E00` é uma **FFT complexa de `n/2`** sobre pares intercalados.
O "banco de filtros no domínio do tempo" continua verdadeiro para o **núcleo de bandas**
(`0x8B3ED0`, etapas D0/K/H), mas **não** descreve a análise espectral que alimenta o
detector/`delta`. A âncora não é editada; fica registrado aqui, e a spec §5 foi corrigida
para não afirmar "FFT é só da UI".

### 23.15 Ordem canônica da extração — **K–P e J FECHADOS; PRÓXIMO: null-test**

Esta subseção substitui a leitura anterior "próximo = J (port)". Ela é a ordem de
**dependência**: cada bloco só usa o que já está fechado com instrução + RVA. K–P vêm antes
de J; I corre em paralelo (é validação, não extração).

**Por que a ordem mudou.** A contagem de aritmética real do cluster inteiro, medida nesta
sessão com Capstone (SSE **e** VEX, deduplicada por corpo):

| Função | Bytes | `call` | ops float (`*ss`/`*ps`/FMA) | Estado |
|---|---:|---:|---:|---|
| `0x8B3ED0` | 20.209 | 127 | **59** (23 `mulss`, 17 `subss`, 7 `maxss`, 5 `minss`, 4 `divss`, 3 `addss`) | esqueleto + 4 blocos provados; **5 faixas** abertas |
| `0x8C5C40` (gêmeo) | 20.209 | 127 | **59** (mesma quebra) | corpo idêntico — cai junto com `0x8B3ED0` |
| `0x87BB60` | 8.136 | 35 | **23** (5 `mulss`, 5 `subss`, 4 `addss`, 4 `maxss`, 4 `minss`, 1 `divss`) | **aberto** (L) |
| `0x8C1440` | 7.800 | 58 | 6 | **fechado** (H, spec §8.4) |
| `0x87B2A0` | 980 | 9 | 5 | **aberto** (L) |
| `0x8ACC40` | 1.634 | 10 | 3 (2 `addss`, 1 `divss`) | **aberto** (O) |
| `0x8C42D0` | 323 | 2 | 3 (2 `mulss`, 1 `subss`) | **aberto** (K) |
| `0x8C0BD0` | 2.150 | 14 | 1 | fechado (H) |
| `0x8B8E70` | 4.036 | 20 | 1 (`divss`) | **aberto** (M) |
| `0x8CAB40` / `0x8CB040` / `0x8CB2F0` | 847 / 680 / 757 | 7 / 2 / 3 | **0 / 0 / 0** | **aberto** (L) |
| `0x8C3F10` | 952 | 4 | 0 | **aberto** (K) |
| `0x8AD2B0` / `0x889BB0` | 5.021 / 10.617 | 25 / 44 | 0 / 0 | **aberto** (N) |
| `0x8BA1B0` / `0x8B35A0` / `0x8BA7B0` | 1.533 / 659 / 270 | 8 / 9 / 1 | 0 / 0 / 0 | **aberto** (M) |
| `0x880640` / `0x881050` | 1.177 / 969 | 4 / 2 | 0 / 0 | **aberto** (O) |
| `0x899940` | 2.412 | 8 | 0 | **aberto** (O) |
| `0x8AE6F0` | 834 | 7 | 0 | **aberto** (K) |
| `0x8C33D0` | 2.117 | 11 | 0 | só pseudocódigo (E) — K |

Consequência dura: **fora do núcleo, o cluster restante quase não tem aritmética** — é
copiar/despachar buffer. Só **quatro** funções fora de `0x8B3ED0` têm ops float
(`0x87BB60` 23, `0x87B2A0` 5, `0x8ACC40` 3, `0x8C42D0` 3, `0x8B8E70` 1). Logo a
bit-exatidão se decide em **K** (as 5 faixas) e **L** (`0x87BB60`), e o resto é ordem e
estrutura — que é o que L/M/N/O fecham.

---

#### K — miolo aritmético de `0x8B3ED0` + `0x8C33D0` (**FECHADA 2026-11-24**)

Mapa de `call` do núcleo lido nesta sessão (`capstone`, 127 sites; os relevantes):

```
0x8B452A 0x8BF5C0   0x8B4609 0x8BF650   0x8B47FE 0x8BFBE0
0x8B4A1C 0x8BA1B0   0x8B4AB8 0x8BA7B0   0x8B4DD8 0x8BFCB0   0x8B4DE7 0x8BFD30
0x8B5354 0x8C0230   0x8B58DB 0x8C02F0   0x8B5A35 0x8C0B10
0x8B605C 0x8C0BD0   0x8B606E 0x8C1440   0x8B645E 0x8AE6F0   0x8B65A4 0x8AE6F0
0x8B67B1 0x8C32C0   0x8B6A7E 0x8C33D0   0x8B7240 0x8C3C20   0x8B79AE 0x8C3E00
0x8B80DC 0x8C0BD0   0x8B80EE 0x8C1440   0x8B83C0 0x8AE6F0   0x8B84F0 0x8AE6F0
0x8B85F8 0x8BFCB0   0x8B8603 0x8BFD30   0x8B868B 0x8C3F10   0x8B8B51 0x8C42D0
```

Ou seja: o núcleo roda o par **detector + estagiador duas vezes** (`0x8B605C/0x8B606E` e
`0x8B80DC/0x8B80EE`, ambos `0x8C0BD0`+`0x8C1440`) — coerente com a lei de mistura já provada
e com os dois `0x8C1440` de H.

**K1 — `0x8AE6F0`** (834 B, 7 `call`, 0 float). Chamado 4× pelo núcleo (`0x8B645E`,
`0x8B65A4`, `0x8B83C0`, `0x8B84F0`) com `(rcx=r12, rdx=&buf, r8=[engine+0x40])`. Interno:
`memset` (`008AE72A`), `memcpy` ×3 (`008AE87C`, `008AE8A5`, `008AEA00`), `0x10A0` ×2
(`008AE984`, `008AE9A3`), `0x86F170` (`008AE968`, identidade `NÃO PROVADA`).

**K2 — os quatro satélites do núcleo**: `0x8C3F10` (952 B; `0x61B790` ×2 em `008C40A1`/
`008C40B5`, `memset` `008C4123`, `0x10D0` `008C4225`), `0x8C42D0` (323 B; 2 `mulss` 1
`subss`, `0x1220` ×2 em `008C43D0`/`008C43E2`), `0x8C32C0` (266 B) e `0x8C3E00` (266 B).
Os quatro têm **0 float ops** exceto o `0x8C42D0`.

**K3 — as 5 faixas aritméticas que sobraram de `0x8B3ED0`** (as 4 de §8.2(a)–(d) e o escalar
de ganho já estão provados — não reabrir):

| Faixa | Sítios (lidos) | O que falta provar |
|---|---|---|
| `0x8B5060`–`0x8B50B5` | `008B5065 [engine+0x2C38]+4`, `008B5083 maxss`, `008B5088 minss`, `008B508D mulss 20` (`0x207A3B0`), `008B5095 subss 60` (`0x207A474`), `008B509D mulss xmm10`, `008B50A2 powf`, `008B50B1 mulss xmm7,xmm6` | origem dos clamps `xmm13`/`xmm11`; qual campo (`state+4` = índice 5 da tabela) e por que dB→linear |
| `0x8B5343`–`0x8B53D4` | `008B5370 −0.45` (`0x207A68C`), `008B537C powf`, `008B5390..` laço 8 bandas, `008B53B2 call 0x1400` (`rdx=0x2077680`, `r8d=0x20`, saída `[rbp+0x4A38]`), `008B53C6 mulss` | a primitiva **`0x1400`** (usada 3× no núcleo: `008B53B2`, `008B6814`, `008B6847`) **não está na tabela de §9**; resolver como as outras |
| `0x8B6549`–`0x8B665E` | `008B6573 ln` ×8, `008B6593 [engine+0x40]`, `008B65A4 0x8AE6F0`, `008B6627 mulss 0.25` (`0x2079E18`), `008B663E −0.25` (`0x207A67C`), `008B6646 subss`, `008B6659 0x1220` | por que 8 buffers e de onde vem o par `0.25 / −0.25` |
| `0x8B77F0`–`0x8B7B4D` | `008B7805 ln` ×8, `008B7AFC 2` (`0x207A188`), `008B7B04 mulss x²`, `008B7B0E +0.333000004` (`0x2079E54`), `008B7B16 powf`, `008B7B1B −(−1.09961283)` (`0x207A6AC`), `008B7B36 −1.09961283` (`0x2079FC0`), `008B7B3E exp` | a curva em si (nomear por RVA, não por palpite) |
| `0x8B84B0`–`0x8B86D0` | `008B84D3 ln` ×8, `008B84F0 0x8AE6F0`, `008B858A 0x1220`, `008B869C powf(10,−3)` (`0x207A6E4`), `008B86AF mulss −0.05` (`0x207A66C`), `008B86BB/86C0 powf` | o gate `byte[rbp+0x4A20]` (`008B85AF`) que decide rodar `0x8BFCB0`+`0x8BFD30`+`0x8C3F10` |

**K4 — `0x8C33D0` (2.117 B)**: só existe pseudocódigo (§23.6). Falta a transcrição
instrução-a-instrução, em especial `008C34BD`/`008C34C7` (leitura antes da escrita,
`NÃO PROVADO` desde E).

**Critério de saída de K**: as 5 faixas com pseudocódigo comentado + constantes com RVA +
ordem de operações preservada, e `0x1400` resolvido (ou marcado `NÃO EXTRAÍDO` com o RVA do
`jmp [rdx+rax*8]`). Nada de "algoritmo equivalente".

---

#### L — tipo de filtro e curva por banda (`0x87BB60`, `0x87E220`, `0x87B2A0`)

Último grande buraco de arquitetura (§12.2-A, §23.14). `0x87BB60` (8.136 B, 35 `call`,
**23 float ops**) é o único lugar fora do núcleo com aritmética relevante: é ele que chama
`0x882FC0` (fechado em §8.2(f)) e `0x8834C0`. Junto vão `0x87E220` (3.739 B, 0 float — usa
`powf(2.4/−4.8)` em `0087E...`, §13.5) e `0x87B2A0` (980 B, 5 ops, chama `0x882C30`, o
`pow(2,1/3)`).

O que L fecha: **tipo de filtro por banda** (FIR/biquad/state-space), a **origem de
`A1`/`A2`** e se `band->flag@0x80 == 1` nos dois sítios de `0x882FC0` (as duas pendências de
H), e o **número real de bandas de análise** (§15.4: 8 bandas estão provadas só como UI).

Satélites: `0x8CAB40` (847 B, 0 float; chamado por `0x8BF650` em `008BF955`/`008BFB84`),
`0x8CB040` (680 B, 0 float; chamado por `0x8C32C0`), `0x8CB2F0` (757 B, 0 float; chamado por
`0x8C3E00`).

#### M — análise (`0x8B8E70`, `0x8BA1B0`, `0x8BA7B0`, `0x8B35A0`)

`0x8B8E70` (4.036 B, 20 `call`, 1 `divss`) e `0x8BA1B0` (1.533 B, 8 `call`, 0 float) são
chamados pelo núcleo (`008B4A1C`) e pelo processador de canal (`0x8AD2B0`). `0x8BA7B0`
(270 B, 0 float) é chamado em `008B4AB8` e é o mesmo código de `0x8A1EE0` com flag `= 1`
(§23.6 nota, §12.2-B). `0x8B35A0` (659 B, 0 float) é chamado por `0x8BA7B0`.

O que M fecha: magnitude/potência, dBFS de referência, tilt, e **qual é o número de bandas
do filtro de análise** (não o da UI).

#### N — processador de canal (`0x8AD2B0`, `0x889BB0`)

`0x8AD2B0` (5.021 B, 25 `call`, 0 float) é o elo provado da cadeia §5
(`0x899940 → 0x8ACC40 → 0x8AD2B0 → 0x8B3ED0`). `0x889BB0` tem **10.617 B**
chain-aware (o §5 dizia 4.720 — corrigir lá).

O que N fecha: a **ordem real** dos estágios dentro do canal (análise → núcleo → estagiador
→ mistura), o significado de `[engine+0x10]`, `[engine+0x40]`, `[engine+0x48]`, e do par
`t+0x400 <= 2` / `n = t+0x404` que `0x8C1440` consome.

#### O — saída, estéreo e ring buffer (`0x880640`, `0x881050`, `0x899940`, `0x8ACC40`)

`0x880640` (1.177 B, 4 `call`, 0 float) é o **caminho alternativo** ligado em `0x8774A0`
(`else` → `0x880640(ctx+0x5ED0)`) e chama `0x885040`/`0x8875F0`. `0x881050` (969 B) é o
caminho principal (`*out = f(ctx+0x5F8)`).

`0x899940` (2.412 B, 8 `call`) e `0x8ACC40` (1.634 B, 10 `call`, 3 ops) fecham
estéreo/sidechain (link, focus, mid/side, listen) e o ring/overlap-add
(`+0x80/+0x88/+0x90`, §13.8-4). `0x8ACC40` chama `0x8AD2B0`, `0x8BAA10` e `0x8BAB60`
(estes dois últimos com 333 B / 328 B, 0 float).

#### Balanço K–O (2026-11-24, verificado — `checks/verificacao_k_o.md`)

Entregas em `checks/k_core.md` (49 KB), `l_filtro.md` (22 KB), `m_analise.md` (21 KB),
`n_canal.md` (22 KB), `o_saida.md` (28 KB). O que já está **provado e conferido por instrução**:

- **K** — as cinco faixas transcritas: F1 `10^(0.05·(20·clamp(state+4,0,1)−60))·M`
  (`008B507C`–`008B50B1`); F2 `g = (Σ buffer[k]·coef[32])·10^(−0.45)` (`008B539B`–`008B53C6`);
  F3 `s = −0.25 − 0.25·powf(state+4,4)` (`008B6627`–`008B6659`); F4
  `exp(c·(ln(2+1/3−x²)+1.0996)−1.0996)−1/3` (`008B7AFC`–`008B7B4D`); F5 gate
  `[engine+0x48]>2` (`008B3FCC`/`008B3FD1`) + `0x8C3F10` (`008B868B`) + dois
  `logf(powf(10,·))` (`008B869C`–`008B86C0`). `0x1400` = produto escalar **provado**
  (`0x21C6288[4]`=`0x199BAC20` → `0xAC20` → `0000AC46 call 0x5F5C0`, `vmulss`+`vaddss`+
  `vmadd231ps`, store `0005F6F7`). Satélites `0x8AE6F0`/`0x8C3F10`/`0x8C42D0`/`0x8C32C0`/
  `0x8C3E00` conferidos (mapas de `call`). `0x8C33D0`: primitivas conferidas
  (`0x11C0`→`0x50E0` sub, `0x11F0`→`0x5BC0` FMA, `0x1250`→`0x69C0` min, `0x1100`→`0x3480`
  min), falta só a leitura de `+0x400/+0x404` (`008C34BD`/`008C34C7`) linha a linha.
- **L** — `+0x80` do descritor é **contagem de ponteiros**, não flag: `008832C1 cmp eax,1` e
  `00883371 cmp eax,1`. Varredura completa de `0x87BB60` (8.136 B, 1.641 linhas): 23 ops
  float, todas escalares em registrador, nenhuma acumulação float com memória indexada →
  **não há biquad/state-space nem recursão por amostra** dentro da função.
- **M** — número de bandas é **runtime**: `008AD301 mov rax,[rcx+8]`, `008AD30C mov r15,[rax+0x40]`,
  `008AD310 mov rbx,[rax+0x48]`; contagem consumida em `008B8F61`. (O `.md` cita `008AD314` —
  RVA errado, corrigido aqui.)
- **N** — a ordem "análise → núcleo" está **refutada**: `008AD601 call 0x8B3ED0` vem antes de
  `008AD9FA` (`0x8B8E70`), `008ADC52` (`0x8B9E40`), `008ADF9B` (`0x8BA1B0`), `008AE096`
  (`0x8BA7B0`), `008AE5EC` (`0x8A1EE0`); `0x8C0BD0`/`0x8C1440` rodam dentro do núcleo.
- **O** — não há lei de estéreo em `0x899940` (0 op float); o único peso é
  `gain = arg2/arg3` em `008AD0B9 divss xmm6,xmm0`; ring `w/r/len` em `+0x110/+0x114/+0x118`
  com `len = 0x10000` e avanço `(r+n)&(len−1)` (`008ACC5D`–`008ACD79`).

**Correção ao item (f) de K:** `0x293760` (alvo de `0x1C8500`) carrega `ln 2` de `0x1ECAE40`
em `002939C7`/`00293A3B`/`00293D0D` e os coeficientes de `ln(1+x)` em `0x1ECAC20..0x1ECAE00`.
Logo **`0x1C8500` = ln** continua provado; o `NÃO PROVADO` do agente está errado.

**Segunda rodada (2026-11-24) — pendências fechadas ou delimitadas:**

- **`0x8C33D0` — cabeçalho de B:** `+0x400`/`+0x404` são lidos em `008C34BD movsxd rsi,[rbp+0x744]`
  e `008C34C7 movsxd r12,[rbp+0x740]` (cópia de B em `[rbp+0x340]`). **`0x8C32C0` não os
  escreve**: copia A/B para a pilha (`008C32E7`–`008C33A3`) e escreve em `arg1+0x1A0`
  (`008C33A6 lea r8,[rcx+0x1a0]`, `008C33BD call 0x8CB040`). Produtor do cabeçalho:
  `NÃO PROVADO`, cadeia para em `008B6A16` (o descritor já está montado).
- **`0x8BA7B0` vs `0x8A1EE0` (diff fechado):** 60 instruções cada, 3 diferenças — 2 desvios de
  branch (`008BA7D0`/`008A1F00`, `008BA840`/`008A1F70`) e **uma** semântica:
  `mov byte [rsp+0x20],1` (`0x8BA7B0`) vs `mov byte [rsp+0x20],r10b` (`0x8A1EE0`, `r10=0` ao
  fim do laço `008A1FBD`/`008A1FC1`). Único parâmetro distinto: o 5º argumento de `0x8B35A0`
  (1 vs 0), constante em cada função — não vem do chamador.
- **`r13` em `0x8B68AB` = argumento 1 de `0x8B3ED0`** (`008B3F14 mov r13,rcx`). Logo
  `[r13+0x58]` (gate `cmp byte`) e `[r13+0x60]` (divisor `qword` inteiro) são campos do
  **contexto**, não do bloco de estado (`state = [ctx+0x2C38]`). "Sample rate" segue
  `NÃO PROVADO`.
- **`0x86F170`:** 457 B; chama `0x86F340` (`0086F210`/`0086F2E0`) e `0x860B90` (`0086F271`).
  Mecânica **provada** em `checks/p_extras.md` §7a/§7b: os dois são clones espelhados
  (`0x86F340` = `(src=rcx, dst=rdx)`, `0x860B90` = `(dst=rcx, src=rdx)`) que copiam
  `n = [src+8]` qwords somando `4*arg3`; `0x86F170` devolve **dois descritores de 0x18 B**
  (em `rdx+0` e `rdx+0x18`) usando `len − [sub+0x88] + arg3`. Nome/identidade: `NÃO PROVADO`.
- **`0x1100` (`0x3480`):** `00003520 vminps ymm1,ymm0,[rcx+r9*4]` + `0000352D vmovups
  [rcx+r9*4]` ⇒ `dst = min(bound, dst)`. O modo já estava provado em **§17.2** desta folha:
  `r9d==4` → min, `r9d==0` → max (`0x3495 test r9d,r9d; je 0x35D9`).

#### P — sobras de bit-exatidão (fechadas ou delimitadas em 2026-11-24; `checks/p_extras.md`)

1. ~~store de `ctx+0x5F8` e `ctx+0x5ED0`~~ — **FECHADO**: subobjetos embutidos
   (`00863929`/`008639E3` → `0x86A4E0`/`0x86A8C0`; destrutor `0x863140`).
2. callback `[rdx+0x50]` do descritor de `0x867D80` — **NÃO PROVADO**: é `call` indireto
   (`00867E10`); provado que não vem do campo `+0x50` de `0x238E9B0`.
3. 16 buffers de `0x8C1440` — **FECHADO em 2026-11-25** (`checks/q_8c1440_buffers.md`):
   pares 0/2/4/6 = `Σch²`, pares 1/3/5/7 = `Σch` (clampados), as 4 divisões em alocações
   novas (`new1/T1/T2/T3`) e as somas `A/B/C/D` dos 2 canais. Resta só o **nome/unidade** dos
   4 coeficientes e a intenção musical (não existem no binário).
4. campo de sample rate em `0x8B68AB` — **PARCIAL**: `r13` = arg1 de `0x8B3ED0`
   (`008B3F14`); `[ctx+0x60]` é campo do contexto lido como `qword` (`008B68BC`); a
   identidade "sample rate" segue **NÃO PROVADA**.
5. sabor da FFT — **PARCIAL**: CCS excluído (`0xBD40` trata o par 0 como complexo comum,
   `0000BDCC`/`0000BDE0`; 8 B por bin); `RToPerm` vs `RToPack` e o construtor de `[spec]==7`
   seguem **NÃO PROVADOS** (§24.5).
6. linear phase — **`NÃO EXTRAÍDO` como instância**: os consumidores da curva (`0x87DB30`,
   0 op float; `0x877D90`, só flags) não têm FIR nem histórico; o ganho é multiplicação real
   de bins (`0x1340` em `0087DE86`/`0087DEA9`) ⇒ **fase zero** no estágio de ganho.
7. ~~primitiva `0x1400`~~ — **PROVADO: produto escalar** (§8.2(g)); `0x86F170` —
   **mecanicamente PROVADO** (`checks/p_extras.md` §7a/§7b): `0x86F340`/`0x860B90` são clones
   espelhados (destino/fonte trocados) que copiam `n = [src+8]` qwords somando `4*arg3`;
   `0x86F170` produz **dois descritores** (0x30 B) a partir de `len - [sub+0x88] + arg3`.
   Identidade/nome: **NÃO PROVADO**.

#### I e J

- **I** — **FECHADO em 2026-11-24**: host reconstruído em `host/` e WAV processado em
  `host/test/out_soothe3.wav` (§15.3). Latência 2304 não compensada; saída depende do bloco
  (−6,6/−8,2/−11,6 dBFS em 512/4096/48000) e o plugin não é transparente no estado padrão.
  O null-test compara **plugin × port** com o mesmo bloco.
- **J** — port Rust. **INICIADO em 2026-11-24** com `checks/stage_j_core.rs` (compila, **10**
  testes): F1, F2, F3, F4, gate de F5, `0x1220`/`0x11F0`/`0x1250`, one-pole e o produto
  escalar com **ordem bit-exata**. Cada linha aponta spec → RVA; o que sobrar entra como
  `// NÃO EXTRAÍDO: <RVA>`, nunca como aproximação. **`powf`/`logf`/`expf` = imports da
  UCRT** (`checks/thunk_map.txt`), com equivalência de bits provada em 17.832.179 amostras
  (`checks/j_crt_equiv.rs`): não há kernel a portar.
  **J2 fechado** — `0x5F5C0` com `n = 16`/`32` reduz na ordem `0005F68D`..`0005F6BE`
  (dois acumuladores de 8 lanes → `L[i]=acc0+acc1` → `x2` → `x4` → `vaddss`); emulação
  escalar conferida contra as **mesmas instruções AVX/FMA** em hardware: 400.000 casos,
  `bad=0` (`checks/j_dot32_avx.rs`); vetores fixos `0x400068db` (n=32) e `0x40b6c8b4`
  (n=16) embutidos como teste. **J3 fechado** — `checks/stage_j_pipe.rs` (12 testes):
  descritor de `0x410 B`, par de `0x18 B` do estagiador, descritor de ring de `0x90 B`
  (`len = 0x10000`), `align16`, avanço `(i+n)&(len−1)` e `chain_plan` com os 25 estágios de
  `0x8AD2B0` (ramos `state+0x58`/`+0x52`; atalho `008ADC6B`→`008AE1C1`). Corrigiu a spec
  §8.4.7: `g/2` é `nch != 2`, não o estéreo.
  **J4, J5 e J6 fechados.** J4: ordens 8..19 e o split `0x895C0` nos dois caminhos (rápido e
  lento), bit a bit (`checks/j4_fft.rs`, 13 testes). J5: `checks/stage_j_chan.rs` (7 testes,
  ring de `0x90 B`, ganho `arg2/arg3`, `0x8BAA10`/`0x8BAB60`). J6: `checks/stage_j_engine.rs`
  (8 testes, smoother, detector, one-pole, curvas `0x88E130`/`0x882FC0` e escalar de ganho
  `u·(y·v)`). Fora do áudio continuam `NÃO EXTRAÍDO`: `0x88300` (ordem > 0x13, inalcançável
  para o áudio — ver §24.5-(3)) e os geradores de twiddle (`0x806E0`/`0x876E0`/`0x87AA0`).
  A cadeia até o kernel foi fechada e MEDIDA no próprio plugin (read-only) por
  `checks/fft_probe.rs` e `checks/fft_generic_probe.rs`; ver §24.5. `checks/stage_j_fft.rs`
  (7 testes) + vetores-ouro bit-exatos `checks/fft_golden.rs` (ordens 6..9 ×
  `impulse`/`cos`/`ramp`) fixam layout e tabela ordem→kernel. **O kernel do áudio
  (`0x1D69E00`, ordem 9) é uma FFT complexa de `n/2` sobre pares intercalados** (§24.5-(4),
  provado por medição: erro `2.8e-06` contra CFFT em f64 e impulsos exatos). **Todas as
  ordens 8..19 estão FECHADAS bit a bit** (2026-11-24): as quatro passadas em
  `checks/j4_fft.rs` reproduzem `J9_WS` (512/512), `KD` (512/512) e `FWD` (514/514); os
  caminhos `01D6BD19` (ordem 8), `01D6B249` (10..12) e `rdx>0x800` (13..19,
  `kernel_large`), além do split `0x895C0` rápido e lento, também estão bit a bit. Restam
  apenas `0x88300` (ordem > 0x13) e os geradores de twiddle, ambos fora do caminho de áudio
  (§24.5-(3)).

## 24. Consequência nova (2026-11-22): o áudio **usa** transformada do IPP

Isto **não** é descoberta de que existe IPP no binário — isso já está no §2 (seção
`IPPCODE` em `0x1CD7000`), no §9 e na tabela de dispatch (`ippJumpIndex` em `0x21C7408` = 4,
`0x10A0→0x2C80`, `0x1010→0x20E0`, tabela em `0x21C5D48`). O que é novo é **o caminho de
áudio que chega nesses stubs**, e a consequência para o §5 do `dsp-spec.md`.

### 24.1 Cadeia nova, provada por chamada

```
0x885040 / 0x8875F0  (process, laço por banda e por amostra)
   0x886A69  call 0x8B2680          ; 1 chamada por amostra
0x8B2680
   0x8B26A8  call 0x8B2C30          ; FIR 32 taps (Etapa D0, §23.4)
   0x8B2846  call 0x10A0            ; IPP copy  (tabela 0x21C5E08 -> 0x2C80)
   0x8B2894  call 0x10D0            ; IPP fill  (tabela 0x21C5E48 -> 0x2F60)
   0x8B290F  call 0x1280            ; tabela 0x21C6088 -> 0x7B40   [novo]
   0x8B2929  call 0x1220            ; IPP scale (tabela 0x21C6008 -> 0x6160)
   0x8B28D6  call 0x1010            ; tabela 0x21C5D48 -> 0x20E0  (fwd?)
   0x8B2988  call 0x15E0            ; tabela 0x21C6508 -> 0xD380  [novo]
   0x8B2A48  call 0x15E0
```

Escala `1.0f/n` em `008B2914`–`008B2929` (`movd xmm1,[rbx+0x18]`; `cvtdq2ps`; `divss` com
`1.0f` de `0x2079F9C`; `call 0x1220`) e **overlap-add** em `008B2AA0`–`008B2B89`
(`buf[(n+k)&mask] += bloco[k]`). Frame de entrada em `ctx+0xC0` (`008B2842`, `008B2876`).

### 24.2 O que isso refuta

`dsp-spec.md` §5.1 provou que a FFT do **JUCE** (`0x1D69E00`) não está no áudio. Continuar
disso para "FFT é só da UI" é **falso**: o áudio passa por `0x20E0`, que valida `[spec]==7`,
lê `[spec+8]` como vtable e chama `[vtable]` — o padrão de wrapper de `IppsFFTSpec`.
`0x7B40` (impl de `0x1280`) faz a mesma validação `[spec]==7`.

> **CORRIGIDO em 2026-11-23.** A frase "`NÃO PROVADO` que `0x20E0` seja FFT: pode ser
> outro objeto IPP com o mesmo magic" foi **resolvida** — ver §24.4. O que continua
> `NÃO PROVADO` é só o *sabor* exato (RToCCS / RToPerm / RToPack) e o construtor da spec.

### 24.3 Regra de conversão de ponteiro (repetida, porque é onde se erra)

VA em dado → `RVA = VA − 0x199B0000` (base real, §2). Ex.: `0x199B20E0` = `0x20E0`.
O `ImageBase 0x180000000` do PE normalizado **não** foi aplicado aos ponteiros absolutos.

### 24.4 PROVADO (2026-11-23): `0x20E0` é a FFT direta do IPP; `0x7B40` é a inversa

**(a) RVA.** As duas entradas vêm de stubs de dispatch de CPU da IPP, com
`[0x21C7408] = 4`:

```
0x1010  movsxd rax,[0x21C7408]        ; = 4
        lea    r10,[0x21C5D48]
        jmp    qword ptr [r10+rax*8]  ; [0x21C5D68] = 0x199B20E0 -> RVA 0x20E0
0x1280  movsxd rax,[0x21C7408]        ; = 4
        lea    r10,[0x21C6088]
        jmp    qword ptr [r10+rax*8]  ; [0x21C60A8] = 0x199B7B40 -> RVA 0x7B40
```

Conferido por leitura direta do dump: `[0x21C5D68]=0x199B20E0`, `[0x21C60A8]=0x199B7B40`,
`dword [0x21C7408]=4`.

**(b) Desmontagem — os dois corpos são o mesmo wrapper, diferindo só no slot.**

`0x20E0` (256 B, `0x20E0..0x21E0`) e `0x7B40` (256 B, `0x7B40..0x7C40`) são idênticos
instrução por instrução, exceto duas linhas:

| `0x20E0` (fwd) | `0x7B40` (inv) |
|---|---|
| `0000214A call qword ptr [rcx]` | `00007BAA call qword ptr [rcx+8]` |
| `000021B1 call qword ptr [rax+0x18]` | `00007C12 call qword ptr [rax+0x20]` |

Assinatura comum, provada pela movimentação de argumentos:

```
000020E0  sub rsp,0x38
000020E8  mov rax,r8        ; arg3 = spec
000020EB  mov r8,rdx        ; arg2 = dst
000020EE  mov rdx,rcx       ; arg1 = src
000020F1  test rax,rax / je 0x21B9          -> -8
000020FA  cmp dword ptr [rax],7             ; magic do IppsFFTSpec*
000020FF  mov eax,0xFFFFFFF3                ; -13 (ippStsContextMatchErr)
00002109  test rdx,rdx / je 0x21B9          -> -8
00002112  test r8,r8  / je 0x21B9           -> -8
0000211B  mov rcx,[rax+8]                   ; objeto interno
0000211F  mov rax,[rcx+0x18]
00002128  cmp dword ptr [rax],3             ; caminho alternativo
00002130  mov qword ptr [rsp+0x30],0x36     ; descritor empilhado
00002139  mov qword ptr [rsp+0x28],r9       ; arg4 = buffer
00002142  mov qword ptr [rsp+0x20],0
0000214A  call qword ptr [rcx]              ; vtable[0] = forward
```

`0x7B40` repete tudo com `0x7B5A cmp dword ptr [rax],7` e `0x7BAA call qword ptr [rcx+8]`.
Ou seja: **é um par forward/inverse sobre a mesma spec (magic 7)** — a assinatura
`(src, dst, spec, buffer)` é a de `ippsFFTFwd_*` / `ippsFFTInv_*`.

**(c) Constantes.**

| RVA | valor | uso |
|---|---|---|
| `0x20FF` | `0xFFFFFFF3` | `-13`, erro de magic |
| `0x21B9` | `0xFFFFFFF8` | `-8`, ponteiro nulo |
| `0x2130` | `0x36` | qword empilhado p/ a vtable |
| `0x214A` | `[rcx]` | slot forward |
| `0x7BAA` | `[rcx+8]` | slot inverse |
| `0x8B272F` | `[0x2079F9C] = 1.0f` | numerador da escala |
| `0x8B28AA`/`0x8B28AD` | `shr rdi,1` / `inc rdi` | `bins = n/2 + 1` |
| `0x8B291C`/`0x8B2925` | `cvtdq2ps n` / `divss` | escala `1/n` |

**(d) Estruturas com offsets provados.**

| Objeto | Offset | Prova |
|---|---|---|
| `IppSpec` | `+0` i32 magic == 7 | `000020FA cmp dword ptr [rax],7` |
| `IppSpec` | `+8` ptr interno | `0000211B mov rcx,[rax+8]` |
| interno | `+0x18` ptr descritor alt. | `0000211F mov rax,[rcx+0x18]` |
| interno | `+0` vtable fwd | `0000214A call [rcx]` |
| interno | `+8` vtable inv | `00007BAA call [rcx+8]` |
| descritor alt. | `+0` == 3 | `00002128 cmp dword ptr [rax],3` |
| descritor alt. | `+0x18` fwd / `+0x20` inv | `000021B1` / `00007C12` |
| estágio | `+0x18` i32 n | `008B2753 movsxd r15,[rax+0x18]` |
| vetor de pares complexos | 8 B `(re,im)` | `0000BDE0 vmovsd`; `0000BDF0 vshufps 0xb1`; `0000BDFD vfmaddsub213ps` |

**(e) Rust.** `checks/stage_fft_rust.rs` (compila: `rustc --edition 2021 --crate-type lib`):
reproduz a validação magic-7, os códigos `-13/-8/-2`, o par de slots `[rcx]`/`[rcx+8]`,
o descritor `0x36`, `bins = n/2+1`, a escala `1/n` e a multiplicação complexa interleaved
de `0xBD40` na mesma ordem. As borboletas ficam `unimplemented!` com RVA do ponto não lido.

**Consequência para o port (Etapa J):** a transformada **precisa** ser reimplementada. O
áudio não usa FFT própria — usa um par FFT/IPP real→complexo de tamanho `n`, multiplica os
`n/2+1` bins por coeficientes complexos interleaved e faz a inversa com escala `1/n`.

### 24.5 Medido em 2026-11-24 (substitui os dois itens antes `NÃO PROVADO`)

Sonda read-only `checks/fft_probe.rs` (`LoadLibraryW` + ponteiros `base+RVA`, nenhum
patch/hook/injeção): o mesmo objeto que o áudio usa, chamado nos RVAs do despacho.

#### (1) Sabor da FFT — **PROVADO: CCS, ordem natural, `n/2+1` pares**

A hipótese antiga ("CCS excluído porque `0xBD40` percorre todos os bins") estava errada. Medição
direta (`fwd` de `0x20E0`, `flag=8`, ordem 9):

| entrada | saída medida | leitura |
|---|---|---|
| impulso `x[0]=1` | todos os `n/2+1` pares `(1,0)`, bits `3f800000/00000000` | espectro plano, `Im(DC)=Im(Nyq)=0` |
| `cos(2π·3i/n)` | pico único no par 3 = `(255.99998, ~0)`; `dst[1]=dst[n+1]=0` bit a bit | bin `k` em `dst[2k..2k+2]` |
| `ramp` / `cos` | conferido contra DFT em f64: erro relativo < `2e-5` | **ordem natural**, sem permutação |

Ou seja `dst = [(Re X0, 0), (Re X1, Im X1), …, (Re X_{n/2}, 0)]`, `bins = n/2+1`, `n+2` floats.
`RToPerm` e `RToPack` ficam **descartados**. O par 0 ser `(DC,0)` explica por que `0xBD40`
multiplica todos os pares sem caso especial: `(DC,0)·(g,0)` continua real.
Consumo provado (inalterado): `n = [estágio+0x18]` (`008B2753`), máscara `n/2−1`
(`008B275A`/`008B275D`), `bins = n/2+1` (`008B28AA`/`008B28AD`, `008B28E2`), inversa com `n`
(`008B291F`) e escala `1/n` (`008B291C`/`008B2925`/`008B2929`).

#### (2) Construtor da spec — **PROVADO** (não há store imediato de 7 solto)

O `7` é gravado em `000088C2 mov dword ptr [r13],7` dentro de `0x8840` (o `init` do thunk
`0x12B0`, chamado por `0x6166DE`), depois de `0x75FC0` zerar o bloco. Cadeia medida:

| passo | prova |
|---|---|
| `getSize(order, flag=8, hint=1)` → `spec/init/buf` = 6656/0/2176 (ordem 9) | `0x4100`, medido |
| `0x8840` grava `spec+0 = 7` e `spec+8 = spec+0x10` | `000088C2` / `000088CA` / `000089A0` |
| descritor (`0x340` B) zerado por `0x75FC0` e preenchido por `0x70480` via `0x69C80` | `000004BF`, `0000899B` |
| `desc[0]=0x6F6A0`, `desc[8]=0x6F760` (genéricos) | `0006F603`/`0006F608` (via `0x6FF80`) |
| `desc+0x18` = wrapper marker 3; `wrapper+8` = ctx | `0006F5E5`/`0006F5ED`; `00072180` |
| `wrapper+0x18`=fwd `0x72480`, `+0x20`=inv `0x726A0` | `0006F502`..`0006F51B`, medido no probe |
| ctx: `+0`=6, `+4`=order, `+8`=0 com flag 8, `+0x10`=escala, `+0x18`=workspace (`0x800`) | `0007245C`..`00072470`, medido |
| kernel por ordem: 6→`0x8BFE0`, 7→`0x8C280`, 8..0x13→`0x1D69E00`, >0x13→`0x88300` | `00072552`..`000725D6`, medido |

#### (3) O que resta `NÃO EXTRAÍDO` (J4 fechado para o caminho de áudio)

Fechado nesta rodada: o **kernel genérico `0x1D69E00` para as ordens 8..19**, bit a bit (KD, WS
e FWD). O despacho `01D6B225` manda `m=0x40`→`01D6BB87`, `m=0x80`→`01D6BD19`,
`m=0x100`→`01D6B8C9` e `m>=0x200`→`01D6B249` (laço radix-8) com re-despacho em `01D6B89E`.
O caminho `rdx > 0x800` (ordens 13..19, `01D6A18B`..`01D6B035`, variantes
`01D6A1EB`/`01D6A3E9`/`01D6A6B0`/`01D6AD25`) está transcrito em `kernel_large` e foi medido
contra o plugin com `rand` (goldens `j13..j19_stage_rand.bits`): **dst e ws 0 divergências**
(ordem 13: 8192; 14: 16384; 15: 32768; 16: 65536; 17: 131072; 18: 262144; 19: 524288).
**Split `0x895C0` FECHADO (2026-11-24).** Os dois caminhos estão em `checks/j4_fft.rs`:
`split_ccs_fast` (`000089600`..`000089757`, `len < 0x40000`, `len = n/2`) e
`split_ccs_slow` (`0000897A0`..`000089988`, `len >= 0x40000`, ativado na **ordem 19**, onde
`len = 0x40000`). `split_ccs` despacha por `len` como `000895E0`. O caminho lento processa a
tabela em blocos de `0x800` pares; o twiddle de bloco vem de `tw[0x2000/4 + 2·block]`
(`00089770` `lea rax,[r9+0x2000]`, `000897A0` `vmovsd xmm2,[rax]`), é duplicado
(`000897A7` `vmovhps xmm4,xmm2,[rax]` + `000897B5` `vinsertf128`) e vira broadcast por lane de
128 b via `vshufps 0xa0`/`0xf5` (`[w0]×8`/`[w1]×8`). O lado "high" entra escalado por `0.5`
(`00089768` `ymm1 = [0x1DFC7C0] = 0.5`). Dois detalhes de rounding provados na validação:
`00089820` é `vfmaddsub213ps` (não `vfmadd213ps`) e `vfmaddsub213/231` exigem FMA **fundido**
(um arredondamento); separar em `mul`+`addsub` dá erro de 1 ULP (`bad=45448`). Com o FMA
correto o split isolado (`checks/_try_split_direct.rs`) fecha `bad=0 / 524290` na ordem 19, e a
cadeia completa `rfft_generic` fecha `FWD bad=0` nas **ordens 13..19** (16..18 pelo caminho
rápido, 19 pelo lento).

Continua `NÃO EXTRAÍDO`: o kernel `0x88300` (ordem > 0x13) e os geradores de twiddle
(`0x806E0`, `0x876E0`, `0x87AA0`). `0x8BFE0` (ordem 6), `0x8C280` (ordem 7) e `0x1D69E00`
(ordens 8..19) estão **bit-exatos**. Ordem 7 dentro do genérico (`01D6BB87` com `m=0x40`) não é
usada porque a ordem 7 vai para `0x8C280`.

**`0x88300` — inalcançável para o áudio do plugin.** O despacho só o chama quando
`r15d > 0x13` (`0007259B cmp r15d,0x13` / `0007259F jle 0x725BA` / `000725A1..000725AE
call 0x88300`), isto é, FFT de tamanho `> 2^19`. O áudio usa `N = round(256·fs/44100)`
(§23.10): `fs = 192 kHz` → `N = 1115`, ordem **11**; mesmo a 1 MHz, `N = 5805` → ordem 13.
Para cair em `0x88300` seria preciso `N > 2^19` (`n = 2^20`), isto é `fs > 90,3 MHz` — fora de
qualquer taxa de áudio. O corpo (411 linhas, `checks/.build/88300.dis`) chama só internos de
IPP — `0x26540` (`0008836F`),
`0x68DC0` (`00088454`, `0008848E`, `00088533`, `0008856D`, `00088670`, `000886C5`,
`000887C0`), `0x68E80` (`000884C9`, `000884F2`, `000885A8`, `000885D1`, `00088703`,
`0008872F`, `000887F7`), `0x1D7CD60` (`00088466`, `000884A2`, `00088545`, `00088581`,
`0008868E`, `000886D7`, `000887D0`), `0x1D6C160` (`000888DE`, `000889F6`), `0x6160`
(`000888F7`) e `0x87F00` (`00088930`, `00088977`) — e nenhum deles tem tabela/identidade
lida; por isso fica `NÃO EXTRAÍDO`, sem pseudocódigo inventado.

**Twiddles (`0x806E0`, `0x876E0`, `0x87AA0`)** também `NÃO EXTRAÍDO` como geradores: as
tabelas de `ctx+0x38`/`ctx+0x50` são **medidas** e fixadas nos goldens, mas a geração não foi
transcrita. `0x876E0`/`0x87AA0` leem a tabela de senos e emitem twiddles complexos;
`0x806E0` constrói a tabela radix/twiddle grande. `tools/find_calls.py` e
`tools/find_refs_any.py` não acharam chamada direta nem ponteiro absoluto para nenhum dos
três (alcance por tabela indireta/IPP interno, `NÃO PROVADO`).

**Correção da sonda (2026-11-24):** o `IDX` gravado pela sonda estava zerado a partir do
primeiro dword (`idx[0]==0` é lixo, não sentinela — a 1ª passada lê `idx[16], idx[32], …` em
passos de 16). A leitura agora usa `VirtualQuery` e para no `0` sentinela em passo 16
(`idx[16·k]==0`), o que também eliminou o crash `0xC0000005` da ordem 19 na leitura de `TW50`.
Sem essa correção as ordens 13..15 pareciam falhar em `rand` e só impulsos passavam.

#### (4) Kernel genérico `0x1D69E00` = **FFT complexa de `n/2`** (PROVADO 2026-11-24)

Isto **corrige** a leitura anterior de que o kernel seria o motor "real→complexo". O kernel
recebe `rdx = n/2` (`000725C7 mov r8d,r14d`, `00072543 lea r9d,[r15-1]`,
`00072547 shlx r14d,r13d,r9d`) e faz uma **FFT complexa de tamanho `m = n/2` sobre os pares
intercalados** `(src[2t], src[2t+1])`, saída **intercalada em ordem natural**, **sem escala**.
A conversão real→CCS é feita depois, por `000725F6` (`pack_dc_nyq`) + `00072620 call 0x895C0`.

Prova por medição (`checks/fft_generic_probe.rs`, read-only, ordem 9, `m = 256`):

| entrada | saída `KD` medida | conclusão |
|---|---|---|
| aleatória (xorshift) | `max abs(KD − CFFT_256) = 2.794e-06` em f64 | é FFT complexa de 256, sem escala |
| `src[0]=1` (complexo `1`) | `KD[2k]=1`, `KD[2k+1]=0` para todo `k` (bits exatos) | saída intercalada `(re,im)` |
| `src[1]=1` (complexo `i`) | `KD[2k]=0`, `KD[2k+1]=1` para todo `k` | entrada **intercalada**; layout "split" refutado |

Ou seja, o truque é o clássico "duas sequências reais em uma complexa":
`Z = FFT_{n/2}(x[2t] + i·x[2t+1])`, e `0x895C0` desfaz o packing para o CCS de tamanho `n`.
É exatamente por isso que `pack_dc_nyq` combina `Z[0]` em DC/Nyquist (`0007260B`/`0007260F`).

**Consequência para a spec §5.1:** o "FFT do JUCE não está no áudio" cai. `0x72480` é o mesmo
ponteiro que `0x6F360` instala no `juce::dsp::FFT` (`0006F4D8`) **e** o `fwd` que `0x72180`
grava em `wrapper+0x18`; o áudio o alcança por `0x20E0` → spec → `wrapper+0x18`. A distinção
"FFT da UI × FFT do áudio" não existe neste binário — o que muda é só qual objeto chama.

Mapa de passadas do caminho do áudio (`rdx = 0x100`, ordem 9), todo por instrução:

| trecho | RVA | conteúdo |
|---|---|---|
| entrada | `01D69E80`..`01D69EA7` | `rbp=rdx`; `r12=src`; `r13=ws` (`r9`); `r14=ws+2·rbp`; `r10=rbx+2·rbp`; se `src!=dst` e `dst` alinhado a 32 B, `ws=dst` (`01D69E8E`) |
| 1ª passada | `01D69EAC`..`01D6A16A` | 4 iterações; índice lido em `01D6A04B` (`[r11+0x40]`, `r11+=0x40`, `rbx = src + idx*32`); `idx[16]=4`, `idx[32]=2`, `idx[48]=6`, `idx[64]=0` = **sentinela**. Cada iteração `i` grava **8 grupos de 16 floats** em `16i, 64+16i, 128+16i, 192+16i, 256+16i, 320+16i, 384+16i, 448+16i`; as 4 borboletas leem `base+{0,256,128,384}`, `{64,320,192,448}`, `{8,136,264,392}`, `{72,328,200,456}` **em floats** |
| fim da 1ª | `01D6A170`..`01D6A185` | `r10=4`, `r11=rdx>>2`; se `rdx<=0x800` → `01D6B03A` |
| 2ª passada | `01D6B03A`..`01D6B20C` | `r11=(rdx>>2)>>2=16`, `sub r11,2` → 8 iterações de 64 floats; 6 twiddles `dup4` de `tw[0..0x60)`; 8 slots de 8 floats em `+0,0x20,…,0xe0`; **bloco-local** |
| despacho | `01D6B212`..`01D6B249` | `rbx += 0x60` (twiddles), `r10=0x10`; `m=0x40`→`01D6BB87`, `m=0x80`→`01D6BD19`, `m=0x100`→`01D6B8C9`, senão `01D6B249` |
| 3ª passada (m=0x100) | `01D6B8C9`..`01D6BA2C` | `r11=rdx>>6=4` blocos, `r10=0x80`, `rax=0x180`, `r12=r13=ws` (**no lugar**); twiddle reinicia em `rcx` por bloco (`01D6B8FA`; `rcx=tw+0x60`) e avança `+0xc0`/passo (`01D6B987`), 2 passos/bloco (`r12=0x10`, `sub r12,8`); `r13 += 0x40`/passo (`01D6BA12`), `+= rax`/bloco (`01D6BA20`); offsets `o+{0x00,0x20,0x80,0xa0,0x100,0x120,0x180,0x1a0}`; epílogo `01D6BA2C mov rcx,rbx` → `tw+0x1e0` |
| 4ª passada (m=0x100) | `01D6BB87`..`01D6BD14` | `r10=0x40<<3=0x200`, `rax=0x600`, 8 iterações (`r11=0x40`, `sub r11,8`); lê `x0` em `+0/+0x20`, `B` em `+0x200/+0x220`, `A` em `+0x400/+0x420`, `D` em `+0x600/+0x620`; escreve `dst` intercalado via `vunpcklps`/`vunpckhps`/`vperm2f128(0x20/0x31)` (`01D6BC7C`..`01D6BCFB`); twiddles de `tw+0x1e0`, `+0xc0`/iteração (`01D6BC26`); epílogo `01D6C0E7` |

Tabela de twiddles (`ctx+0x38`, medida): `tw[0..4] = cos(0, π/8, π/4, 3π/8)`,
`tw[4..8] = −sin` dos mesmos ângulos (ou seja `W8^0..W8^3`); `tw[8..16] = W8^{2k}`;
`tw[16..24] = W8^{3k}`; de `tw[24]` em diante, tabela de 64 pontos com passo `π/64` (cos em
`24+8j`, `−sin` em `32+8j`). A 4ª passada lê até `tw+0x7df` (última iteração `tb=0x720`, mais
`0xa0`, 32 B), logo a tabela tem **≥0x7e0 B**; o probe lê `0x800` B (512 f32). O valor
`0x660` B registrado antes era o **ponteiro final** da 3ª passada (`tw+0x60+0x180`), não o
tamanho da tabela.

**Estado da transcrição (2026-11-24): ORDENS 8..19 FECHADAS BIT A BIT.** `checks/j4_fft.rs` tem
os estágios genéricos (`kernel_stage1`, `pass2`, `stage16`/`pass3a_step`, `radix8_levels`,
`radix8_final`, `radix4_final`, `kernel_large`, `kernel_generic`) e **13 testes**, todos verdes:
`orders_8_10_11_12_are_bit_exact` (KD, WS e FWD bit a bit para **ordens 8, 9, 10, 11 e 12**),
`kernel9_workspace_matches` (workspace pós-3ª = `J9_WS`, 512/512 bits), `kernel9_is_bit_exact`
(`KD`, 512/512), `order9_chain_is_bit_exact` (`FWD` via `0x20E0`, 514/514) e
`order9_matches_probe_golden` (`impulse`/`cos`/`ramp`, de `checks/fft_golden.rs`). As **ordens
13..19** do caminho `rdx > 0x800` foram validadas com `checks/_try_large.rs` contra os goldens
`j13..j19_stage_rand.bits` (dst e ws, `0` divergências em todas). Conferência independente: o
despejo do Rust (`checks/j9_dbg.rs`) dá `max|rust − plugin| = 0.0` para workspace e para `KD`
(ordem 9).

**Caminho `rdx > 0x800` (`kernel_large`, 2026-11-24).** Driver literal
`01D6A18B`..`01D6B035`: fatia `rdx = n/2` em blocos de `0x800` complexos (`0x1000` floats);
por bloco roda `pass2` (`01D6A1EB`, `r10==4`), depois `stage16`/`radix8_levels` conforme
`mask = rdx & 0x55555555` e `r10` (`01D6A3E9`/`01D6A6B0`), com `r10`/`sub28`/`r11` recalculados
(`01D6A3CA`/`01D6A3D6`/`01D6A6A6`); ao fim dos blocos, os estágios finais sobre o array inteiro
(`01D6AD77`): `stage16` enquanto `[rsp+0x28] != 4`, então `radix4_final` (`01D6BB87`). `rdx`
nunca é modificado no laço, logo `mask` usa sempre o `n/2` original. Parâmetros finais por
ordem: 13→`radix4_final(0x400)`; 14→`radix4_final(0x800)`; 15→`stage16(0x400,16)`+
`radix4_final(0x1000)`; 16→`stage16(0x800,16)`+`radix4_final(0x2000)`;
17→`stage16(0x400,64)`+`stage16(0x1000,16)`+`radix4_final(0x4000)`;
18→`stage16(0x800,64)`+`stage16(0x2000,16)`+`radix4_final(0x8000)`;
19→`stage16(0x400,256)`+`stage16(0x1000,64)`+`stage16(0x4000,16)`+`radix4_final(0x10000)`.

Os quatro estágios reaproveitados pelas ordens (mesma instrução, `r10` e extensão por ordem):
`kernel_stage1` (`01D69EAC`..`01D6A16A`), `pass2` (`01D6B03A`..`01D6B20C`, `rdx/32` iterações),
`stage16` (`01D6B8C9`..`01D6BA2C`), `radix8_levels`/`radix8_final` (corpo radix-8 comum),
`radix4_final` (`01D6BB87`..`01D6BD14`) e o despacho `kernel_generic` (`01D6B225`/`01D6B89E`).
Tamanhos medidos: `ws = n*4` B; `TW38 = 0x400 << (order−8)` B (ordem 12 = **0x4000**, não
0x8000); a 1ª passada roda `n/128` iterações (o `idx` precisa de `n/8+16` dwords até o `0`
sentinela).

O defeito que sobrou até aqui era a **semântica de `vunpcklpd`/`vunpckhpd`** no modelo de
validação: elas intercalam as **palavras de 64 bits baixas/altas** de cada lane (pares de
floats), não floats isolados — `vunpcklpd a,b = [a0,a1,b0,b1 | a4,a5,b4,b5]`. Com isso a 1ª
passada fecha; `tools/pass1_model.py` e `tools/full_model.py` reproduzem `KD` com erro `0.0`
para `imp,e1..e9,e16,e32,e64,e128,e256` e ≤3.1e-06 (só arredondamento float64) no resto.

Ferramentas desta rodada: `checks/fft_generic_probe.rs` (modos `rand`/`imp`/`eN`, grava
`SRC/KD/WS/FWD/IDX/TW38/TW50` em `checks/.build/j<order>_stage_<modo>.bits`; `IDX` lê `n/8+16`
dwords e `TW38` lê `(tw50_ptr − tw38_ptr)/4` floats), `tools/gen_j9_golden.py` (gera
`checks/j{8,9,10,11,12}_golden.rs`), `tools/full_model.py` (cadeia completa em Python,
referência validada para a ordem 9), `tools/pass1_model.py`, `tools/recover_pass1.py`,
`checks/j9_dbg.rs`/`tools/cmp_rust.py` (despejo do Rust × Python × plugin),
`tools/show_bits.py`, `tools/cmp_dft.py`, `tools/check_cfft.py`.



## 25. Estado da retomada (2026-11-24)

**ETAPA ATUAL: J1–J6 fechados em Rust (2026-11-24).** J1/J2 (`checks/stage_j_core.rs`, 10
testes), J3 (`checks/stage_j_pipe.rs`, 12 testes), J4 (`checks/j4_fft.rs`, 13 testes), J5
(`checks/stage_j_chan.rs`, 7 testes) e J6 (`checks/stage_j_engine.rs`, 8 testes). I fechada
(host em `host/`). A cadeia da FFT até o kernel está **fechada e medida** no próprio plugin
(`checks/fft_probe.rs` e `checks/fft_generic_probe.rs`, somente leitura) e o §24.5 foi
reescrito com o que foi medido: **o packing é CCS, `n/2+1` pares em ordem natural** (a exclusão
anterior de CCS está refutada), o construtor da spec é `0x8840`
(`000088C2 mov dword ptr [r13],7`) e o kernel `0x1D69E00` é **FFT complexa de `n/2` sobre pares
intercalados** (§24.5-(4)). `checks/stage_j_fft.rs` (7 testes) e `checks/fft_golden.rs`
(36 arrays SRC/DST/BACK, ordens 6..9) fixam layout, tabela ordem→kernel e vetores-ouro
bit-exatos.

**J4 fechado para o áudio (2026-11-24).** As **ordens 8..19** estão bit a bit —
`orders_8_10_11_12_are_bit_exact` compara KD, WS e FWD para as ordens 8..12 e os goldens
`j13..j19_stage_rand.bits` fecham o caminho `kernel_large` (dst e ws, `0` divergências). O
**split `0x895C0` está FECHADO** (rápido e lento; §24.5-(3)), inclusive na ordem 19 (caminho
lento), com `rfft_generic` `FWD bad=0` nas ordens 13..19. Continuam `NÃO EXTRAÍDO` o kernel
`0x88300` (ordem > 0x13, inalcançável: N ≤ 1115 → ordem 11; §24.5-(3)) e os geradores de
twiddle (`0x806E0`, `0x876E0`, `0x87AA0`), com as tabelas medidas em vez de transcritas.

**J5 fechado:** `checks/stage_j_chan.rs` (7 testes) transcreve os três descritores de ring de
`0x90 B` (`out@0`, `A@0x90`, `B@0x120`), `len = 0x10000`, `available`/`advance_read`/
`advance_write` (`008ACC5D`..`008ACC82`), o único ganho `(float)arg2/(float)arg3`
(`008AD06B`..`008AD0B9`) e `0x8BAA10`/`0x8BAB60`. `NÃO EXTRAÍDO` com RVA: layout de
`+0x08..+0x7F` (`0x868840`), atribuição da lista de `0x86F170` a A/B e o plano `nch > 1`.

**J6 fechado:** `checks/stage_j_engine.rs` (8 testes) transcreve `0x8C3C20` (`a=0.1`),
`0x8C0BD0` (`R=(P0²+P1²)/max(P0+P1,eps)`, `P←(1-g)P+gR`), `0x8B68AB` (`1-0.1^(1/x)`),
`0x88E130`, `0x882FC0` e o escalar `0x8B5AF2`–`0x8B5CA7` na ordem exata `u·(y·v)`. Ficam
`NÃO PROVADO`: `0x293760`/`0x240C00` (ln/exp da IPP) vs `f32::ln`/`f32::exp` bit a bit
(o recíproco vetorial de `0x88E130` foi fechado em M2, 2026-11-25: `port/src/rcp.rs`,
§26); `NÃO EXTRAÍDO`: o significado físico de `s0/A/A1/A2/k/G` e a
atribuição grupo→coeficiente de §8.4.8.

**Próximo:** null-test plugin × port com o mesmo bloco e alinhamento 2304 — bloqueado até
existir um port completo do motor (hoje há J1–J6 como fragmentos). O host e
`host/test/analise.py` já existem para quando houver render do port.

**Etapa J0 — FECHADA em 2026-11-25 (engenharia, sem prova nova).** Os kernels de J1–J6
saíram de `checks/*.rs` para o crate `port/` (`soultree_port`), fonte única: `core_dsp.rs`
(J1/J2), `pipe.rs` (J3), `fft_layout.rs` + `fft_kernels.rs` (J4), `chan.rs` (J5) e
`engine.rs` (J6). Os arquivos de teste ficaram só com os testes e apontam para o kernel com
`#[path = "../port/src/<modulo>.rs"]`; a extração é reprodutível por
`tools/extract_port_modules.py` (backup em `checks/.build/pre_port/`). `port/src/pending.rs`
lista os 12 gaps com status, RVA e `blocks_null_test`; `port/src/chain.rs` usa a ordem
provada de `pipe::chain_plan` e devolve o primeiro gap bloqueante (`0x1550 -> 0x63640`) em
vez de produzir amostras. Runner único: `powershell -File port\run_tests.ps1` (**57 testes
J + 18 do port, 0 falhas**; `-Slow` inclui `j_dot32_avx.rs` e `j_crt_equiv.rs`). Nenhum
número, ordem ou coeficiente foi alterado na extração.
**Atualização M1 (2026-11-25):** o crate tem `port/src/div.rs` (`0x63640`); o primeiro gap
bloqueante passou a ser `0x293760` (ln); o runner roda **57 J + 36 do port + 17 de
`checks/j_div_avx.rs`** (16 de `div.rs` + 1 conferência contra hardware AVX/FMA), 0 falhas.
Ressalva do runner: no modo `-Slow`, `j_dot32_avx.rs` e `j_crt_equiv.rs` só têm `main` e são
compilados com `--test` ⇒ rodam **0 testes** (o `main` não executa); não corrigido em M1.
**Atualização M2 (2026-11-25):** o crate tem `port/src/rcp.rs` (`0x29B260`, recíproco de
`0x88E130`), usado por `engine.rs`; o gap do recíproco saiu de `pending.rs` (o primeiro
bloqueante continua `0x293760`). O runner roda **9 suítes: 64 J (57 + 7 de `rcp.rs` incluídos
por `checks/stage_j_engine.rs`) + 44 do port + 17 de `j_div_avx.rs` + 8 de
`checks/j_rcp_avx.rs`** (7 de `rcp.rs` + 1 contra hardware), 0 falhas. O exaustivo 2^32 de
`j_rcp_avx.rs` (`--exhaustive`, `-O`) roda fora do runner (~26 s).

**Q — `0x8C1440` (2026-11-25, FECHADO):** `checks/q_8c1440_buffers.md`.
- 16 buffers: pares 0/2/4/6 = `Σch²` (`0x1580`); 1/3/5/7 = `Σch` (`0x1370`) e único conjunto
  clampado (`0x1100` max, `1e-7`, `008C2393`/`23CD`/`240D`/`244D`).
- 4 divisões `0x1550` em **alocação nova** reaproveitando o slot do numerador:
  `new1=par0/par1` (`008C2545`, slot `[rbp-0x40]` em `008C250E`), `T1=par2/par3` (`008C263D`),
  `T2=par4/par5` (`008C273B`), `T3=par6/par7` (`008C2828`). O `den` de `T3` é o par 7
  capturado em `xmm11` (`008C241B`) **antes** do reaproveitamento — par 7 nunca é destino.
- `A/B/C/D` (`008C298E`/`29CE`/`2A0E`/`2A4E`) = soma dos 2 canais de `new1/T1/T2/T3`, só no
  caminho mono com `g/2`.
- Mistura: `dst` = canais do registro, `src` = resultado da divisão:
  `ch ← (1−g)·ch + g·D`, `D = Σregistros ch² / Σregistros ch`.
- Coeficiente por caso: `enable != 0` ⇒ `+0x2C`; habilitado cobre todos os `tipo`;
  desabilitado, `tipo 8/9` ⇒ `+0x30` (exige flag `state[0x1BF]==state[0x1C7]==0`),
  `tipo 6` ⇒ `+0x34`, `tipo 5` (`sel ∈ {0x10..0x12}`) ⇒ `+0x38`, `tipo 0xA` ⇒ **nunca**
  (não acumula nem mistura, `008C1FDB`–`008C2F27`). Não é tabela índice→coeficiente; é
  condicional.
- `0x882FC0`: 0 ocorrências no corpo — hipótese "buffer recebe a curva" **refutada**.
- Resta `NÃO PROVADO`: nome/unidade dos 4 coeficientes, faixa válida de `g`, intenção musical
  da média ponderada, e `nch > 2` (o ramo `008C1E4B` usa só `t->buffers[first_buf]`).

**Último RVA lido (2026-11-24, J4):** `0x4100`, `0x8840`, `0x20E0`/`0x7B40` (wrappers),
`0x75FC0`, `0x70480`/`0x69C80`, `0x6F360`/`0x6FF80`, `0x6F6A0`/`0x6F760`, `0x72180` (ctx),
`0x72480`/`0x726A0`, `0x895C0`, `0x8BFE0`/`0x8C280` (inteiros), `0x1D69E00` inteiro
(`checks/.build/1d69e00_full.dis`, 1.726 linhas; pass1 1–201, pass2 899–977, despacho
978–987, pass3a 1302–1373, pass3b 1442–1521), tabelas `0x1DFA2F8`/`0x1DFA358`, as do `ctx`
(`+0x30` índices, `+0x38` twiddles, `+0x50`/`+0x58` do split) e as constantes
`0x797B640`/`0x797B660`/`0x797B680` (NEG_EVEN).

**Nesta rodada (J5/J6 + fecho de J4/J5/J6):** `0x88300` inteiro (411 linhas,
`checks/.build/88300.dis`), `008AD06B`..`008AD0B9` (ganho `arg2/arg3`),
`0x8BAA10`/`0x8BAB60`, `008ACCF7`..`008AD280` (ring), `0x8C3C20`, `0x8C0BD0`, `0x8B68AB`,
`0x88E130`, `0x882FC0`, `0x8B5AF2`..`0x8B5CA7` (escalar `u·(y·v)`).

**Etapa atual:** C **FECHADA** (§23.3; spec §18.4; Rust em `checks/stage_c_rust.rs`).
§24 **TESTADO em 2026-11-24** (§24.5 reescrito com medição; o "FECHADO em 2026-11-23" acima
vale só para o contrato magic-7/`0xBD40` de `checks/stage_fft_rust.rs`, não para o packing).
**F
FECHADA em 2026-11-23**: `K = δ0` por construção (reset + `1.0f` antes da cópia, passo 4/5
do §23.7); não existe aritmética de parâmetro nos 32 taps. O design que escreve na mesma
arena é a **curva de ganho** (`0x882DE0` = sino gaussiano em log2-freq; math identificada:
`0x1C8500`=ln, `0x1C84A0`=exp), e não altera `K` porque a cópia é por valor.
**G FECHADA (2026-11-23):** o escritor dos campos de estado é o setter de parâmetro
`0x867D80` (1.792 B), alcançado por `0x862EF0` (`00862EF0 mov rcx,[rcx]` com `[obj+0]` =
base do motor, gravada em `00862ED9`; `0x8634A0` devolve `r14` em `00864057`). Despacho por
`idx=[rdx]` → `byte[0x8683CC+idx]` → `dword[0x868348+sel*4]`; **143 índices, 33 alvos**.
Mapa completo índice → offset com RVA na spec §8.3.1 e em §23.8: `+0x00`←0, `+0x04`←5,
`+0x28`←17, `+0x3C`←18, `+0x4C`←92, `+0x52`←16; bandas 19..90 → `s+0xB8+0x20·b`;
grupos 98..122 → `s+0x1B8+8·g`. O índice é o campo `+0x10` da tabela `0x238E9B0`
(isomorfismo 143/143 dos blocos). `NÃO EXTRAÍDO` só: store de `+0x5F8`/`+0x5ED0` e a
identidade do callback `[rdx+0x50]`.
**H FECHADA (2026-11-23):** a dinâmica está **inline** em `0x8B3ED0` — rugosidade
(`008B4E20`), one-pole `1-0.1^(1/x)` (`008B68AB`), escalar de ganho `u·(y·v)` (`008B5AF2`;
`v` primeiro em `008B5C02`, `u` depois em `008B5C8A`),
convolução 16 taps por banda (`008B67F0`); `0x8C0BD0` = detector `R=(P0²+P1²)/(P0+P1)` com
`P←(1-g)P+gR`; `0x8C3C20` = smoother forward-backward `a=0.1` (confirmado);
`0x8CAE90` = despacho de MAC em 3 modos. E nesta sessão: **`0x8C1440`** (assinatura, 16
buffers, 5 grupos `{8,9,10,6,5}`, registros de 0x18 B, predicado `0x61B790`, lei de mistura
`(1−g)/g`, com `g/2` **só em `nch != 2`** — §23.9-H corrigido em 2026-11-24), **`0x882FC0`** (duas curvas `A^(1−σ)`, `σ=1/(1+(v/A)^(-k/6))`)
e **`0x88E130`** (fórmula fechada + ordem exata, recíproco aproximado). Tudo em §23.9–H e na
spec §8.2(e)/(f) e §8.4.
**Próxima: null-test plugin × port** — J1–J6 em Rust, I **fechada** em 2026-11-24 (host em
`host/`, WAV em `host/test/out_soothe3.wav`, §23.10). O null-test depende de um port completo
do motor (hoje há fragmentos J1–J6); usar o mesmo bloco e o alinhamento **2304**. Fora do
caminho de áudio, `0x88300` e os geradores de twiddle ficam `NÃO EXTRAÍDO` (§24.5-(3)).
Refutada a hipótese de IFFT na cadeia de `K` (nenhum `call` para `0x1010`/`0x1280` em
`0x87B680`/`0x87BB60`/`0x87DB30`/`0x882FC0`/`0x882DE0`/`0x8834C0`).

**Último RVA lido (2026-11-23, H):** `0x8C1440` inteiro (`checks/8c1440.u8.dis`, 1.787
linhas), `0x882FC0` inteiro (`checks/882fc0.u8.dis`, 249), `0x88E130` inteiro
(`checks/88e130.u8.dis`, 155), `0x8CAFD0` (`008CAFD0`–`008CB03E`), `0x61B790`
(`0061B790`–`0061B85C`), `0x1220`/`0x2300`, `0x12E0`/`0x8FA0`, `0x1340`/`0x9BA0`, tabelas
`0x2014360`/`0x21C6008`/`0x21C6108`/`0x21C6188`. Antes (G): `0x867D80` inteiro (1.792 B,
`checks/867d80.dis`), `0x862E40` (171 B), `0x8634A0`, `0x69AE90`, tabelas
`0x868348`/`0x8683CC`, IAT `0x1D8D7E0`–`0x1D8D818`, diretório de importação em `0x2175044`
(ILT `0x2176878`); `0x8B3ED0` trechos, `0x8CAE90`, `0x8C3C20`, `0x882DE0`, `0x293760`/`0x240C00`.

**K–O ENTREGUES em 2026-11-24 — verificação em `checks/verificacao_k_o.md`.**

Entregas: `k_core.md`, `l_filtro.md`, `m_analise.md`, `n_canal.md`, `o_saida.md`. O balanço
com as instruções conferidas está em **§23.15 — "Balanço K–O"**. Três resultados mudam o
desenho:

1. **N**: a ordem é **núcleo → análise** (`008AD601` antes de `008AD9FA`/`008ADC52`/
   `008ADF9B`/`008AE096`/`008AE5EC`); "análise → núcleo" está refutada.
2. **L**: `+0x80` do descritor é **contagem de ponteiros** (`008832C1`/`00883371`), não flag.
3. **O**: não há lei de estéreo em `0x899940` (0 op float); o único ganho é
   `arg2/arg3` em `008AD0B9`.

**FECHADO na 2ª rodada (2026-11-24) — todos os 6 itens:**

1. ~~`0x5F5C0`~~ — **PROVADO**: `0x1400` → `0x21C6288[4]`=`0x199BAC20` → `0xAC20` →
   `0000AC46 call 0x5F5C0`; `vmulss`/`vaddss`/`vfmadd231ps`, store `0005F6F7` ⇒
   `out = Σ a[i]·b[i]`.
2. ~~`0x8C33D0`~~ — **primitivas PROVADAS** (`0x11C0`→`0x50E0` sub; `0x11F0`→`0x5BC0` FMA;
   `0x1250`→`0x69C0` min; `0x1100`→`0x3480` minps) e `008C34BD`/`008C34C7` lidos
   (`B+0x404`/`B+0x400` da cópia em `[rbp+0x340]`); `0x8C32C0` **não** escreve esse cabeçalho
   (escreve em `arg1+0x1A0`, `008C33A6`/`008C33BD`).
3. ~~satélites~~ — **OK** (`0x8AE6F0` contínua além do `.pdata` em `008AE78F`; mapas de `call`
   de `0x8C3F10`/`0x8C42D0`/`0x8C32C0`/`0x8C3E00`).
4. ~~`0x87BB60`~~ — **OK (negativa)**: varredura chain-aware de 8.136 B, 23 ops float, todas
   escalares em registrador ⇒ sem biquad/state-space/recursão por amostra.
5. ~~`0x8BA7B0`/`0x8A1EE0` e ramos de `0x8AD2B0`~~ — diff = 3 instruções (2 branches + 5º
   argumento 1 vs 0). `[state+0x58]` (`008AD76B`) escolhe `r8+0x238`/`+0x2C0` (`008AD7A7`/
   `008AD7AE`) vs `r8+0x1A8`/`+0x230` (`008ADA04`/`008ADA0B`); `[state+0x52]` (`008ADFAB`/
   `008AE56F`) porteia `0x8BA7B0` (`008AE096`) e `0x8A1EE0` (`008AE5EC`).
6. ~~Restante de P~~ — **fechado/delimitado** (`checks/p_extras.md`, 2ª rodada):
   `0x86F340`/`0x860B90` clones espelhados; `0x86F170` = dois descritores 0x30 B; 16 buffers
   = **FECHADOS em 2026-11-25** (`checks/q_8c1440_buffers.md`); CCS excluído (`0xBD40` trata o
   par 0 como complexo); linear phase = `NÃO EXTRAÍDO` como instância (ganho zero-fase);
   sample rate `NÃO PROVADO`.

**Correção de rota registrada:** o agente K marcou `0x1C8500` (= `0x293760`) como semântica
`NÃO PROVADA`; a releitura mostra `ln 2` em `0x1ECAE40` (`002939C7`/`00293A3B`/`00293D0D`) e
a série de `ln(1+x)` em `0x1ECAC20..0x1ECAE00` → **continua ln**.

**Pendências explícitas `NÃO EXTRAÍDO`/`NÃO PROVADO` (vão para o código marcadas, não
estimadas) — lista consolidada em 2026-11-24:**

- identidade do callback `[rdx+0x50]` do descritor de runtime (G; provado que não é campo da
  tabela `0x238E9B0`) — parada `00867E10`;
- ~~papel dos 16 buffers de `0x8C1440` e atribuição grupo→coeficiente~~ — **FECHADO em
  2026-11-25** (`checks/q_8c1440_buffers.md`, spec §8.4.3/§8.4.7/§8.4.8): pares
  `0/2/4/6 = Σch²`, `1/3/5/7 = Σch` (clampados), divisões `new1/T1/T2/T3` em alocação nova,
  somas `A/B/C/D`, e mapa `enable→+0x2C`, `tipo 8/9→+0x30`, `tipo 6→+0x34`,
  `tipo 5 (sel 0x10..0x12)→+0x38`, `tipo 0xA→nunca`. Resta só `NÃO PROVADO` o nome/unidade
  dos coeficientes, a faixa de `g`,
  a intenção musical e `nch > 2`;
- identidade de `r13` no bloco `0x8B68AB`: é arg1 de `0x8B3ED0` (`008B3F14`), o divisor
  `[ctx+0x60]` é `qword` (`008B68BC`), mas "sample rate" não está provado;
- sabor da FFT: CCS excluído, `RToPerm`/`RToPack` e construtor de `[spec]==7` `NÃO PROVADOS`
  (§24.5; `0xBD40` em `0000BDCC`/`0000BDE0`);
- linear phase: nenhuma instância de FIR localizada no caminho lido (`0x87DB30` tem 0 op float,
  `0x877D90` só escreve flags; ganho aplicado como multiplicação de bins, `0087DE86`/
  `0087DEA9`) — parada `0x87E0B0`;
- `0x86F170`: mecânica provada (dois descritores de 0x18 B, deslocamento `4*[sub+0x88]`),
  identidade `NÃO PROVADA` (`checks/p_extras.md` §7a/§7b).
**Fechado em 2026-11-24 (P, `checks/p_extras.md`):** `+0x5F8`/`+0x5ED0` são subobjetos
embutidos construídos por `0x86A4E0`/`0x86A8C0` (`00863929`/`008639E3`), destruídos por
`0x863140` via `0x862F40`; aritmética do one-pole `1−0.1^(1/x)` transcrita com constantes.

**J2/J3 — Rust de 2026-11-24:**

- **J2** (`checks/stage_j_core.rs`, 10 testes): ordem de soma de `0x5F5C0` para `n = 16`/`32`
  (`0005F68D`..`0005F6BE`), conferida contra hardware AVX/FMA em **400.000** casos
  (`checks/j_dot32_avx.rs`, `bad=0`); a soma ingênua diverge em 298.626.
- **J3** (`checks/stage_j_pipe.rs`, 12 testes): descritor de `0x410 B`
  (`008AD32A`/`008AD330`/`008AD337`), par de `0x18 B` do estagiador
  (`008CAFE2`/`008CB015`), descritor de ring de `0x90 B` com `len = 0x10000`
  (`008688CC`/`008AD26C`/`008ACCF7`), `align16` (`008C3510`..), avanço do ring
  (`008ACC5D`..) e `chain_plan` com a ordem de `0x8AD2B0` (ramos `state+0x58`/`+0x52`,
  atalho `008ADC6B`..`008AE1C1`).
- **Correção material de J3:** o `g/2` da mistura **não** é o ramo estéreo. `nch == 2` usa
  `g` inteiro (`008C2D90`..`008C2DB4`); `nch != 2` usa `g·0,5` (`008C2DB8`,
  `008C2DEA mulss xmm1,xmm11`). Spec §8.4.7 e §23.9-H corrigidos.

**I FECHADO em 2026-11-24 — o WAV do oráculo existe** (§15.3): `host/` (Rust std-only, FFI
crua, sem injeção/hook) carrega `original/soothe3.vst3` read-only por `GetPluginFactory`,
processa 48.000 frames em 94 blocos `S_OK` (48 kHz/512) e grava
`host/test/out_soothe3.wav`; latência **2304** não compensada; duas execuções com SHA-256
idêntico (`1218C801…E67B`), reproduzido nesta sessão. Três fatos medidos que o null-test
tem de respeitar: (i) o plugin **não é transparente** no estado padrão (RMS da diferença
alinhada −6,6 dBFS); (ii) a saída **muda com o bloco** (−6,6 / −8,2 / −11,6 dBFS em
512/4096/48000; causa `NÃO EXTRAÍDO`); (iii) o preset é o de fábrica (sem `setState`).
A reconstrução do port deve ser comparada **plugin × port** com o mesmo bloco e alinhamento
de 2304 — não entrada × saída.

**Arquivos novos (H):** `checks/8c1440.u8.dis` (1.787 linhas), `checks/882fc0.u8.dis` (249),
`checks/88e130.u8.dis` (155), `checks/87a7a0.u8.dis`; `tools/resolve_thunk.py`.

**Fechado em §24 (2026-11-23) — resumo:**

- `0x1010` e `0x1280` são stubs de dispatch de CPU da IPP (`[0x21C7408]=4`);
  `[0x21C5D68]=0x199B20E0` e `[0x21C60A8]=0x199B7B40`.
- `0x20E0` e `0x7B40` são **o mesmo wrapper de 256 B**, diferindo só no slot:
  `0000214A call [rcx]` (forward) vs `00007BAA call [rcx+8]` (inverse). Ambos validam
  `cmp dword [spec],7`, assinatura `(src,dst,spec,buffer)`, descritor `0x36`.
- Chamador `0x8B2680`: FFT → multiplicação de `n/2+1` pares complexos (`0xBD40`,
  `vmovsd`/`vshufps 0xb1`/`vfmaddsub213ps`) → FFT inversa → escala `1/n`
  (`008B272F` = `1.0f` em `0x2079F9C`; `008B291C`/`008B2925`). `bins = n/2+1` em
  `008B28AA`/`008B28AD`. Overlap-add com hop `n/2` (`008B2761 test [rsi+0x140],n/2-1`).
- **Decisão para o port:** reimplementar a transformada (é FFT real→complexa de tamanho
  `n`, com inversa não normalizada e escala `1/n`).

**Arquivos novos desta sessão:** `tools/parse_desc_vectors.py`, `tools/map_desc_cases.py`,
`tools/stage_c_table.py`, `tools/stage_c_rust.py`, `tools/find_tag7.py`, `tools/rd_dis.py`,
`tools/lsweep.py`; `checks/desc_vectors.txt`, `checks/stage_c_table.json`,
`checks/stage_c_rust.rs`, `checks/stage_fft_rust.rs`, `checks/85e6c0.dis`,
`checks/563e40.dis`, `checks/32b810.dis`, `checks/8bfd30.dis`, `checks/8c3f10.dis`,
`checks/8c42d0.dis`, `checks/8b35a0.dis`, `checks/878200.dis`, `checks/8688b0.dis`,
`checks/8ab760.dis`, `checks/8abaa0.dis`, `checks/20e0.dis`, `checks/1010.dis`,
`checks/7b40.dis`, `checks/bd40.dis`, `checks/2f60.dis`, `checks/2300.dis`,
`checks/2c80.dis`, `checks/3480.dis`, `checks/8817d0.dis`, `checks/881a80.dis`,
`checks/881af0.dis`, `checks/881b60.dis`, `checks/869490.dis`, `checks/878000.dis`,
`checks/861db0.dis`, `checks/862e40.dis`.

**Arquivos novos da retomada de 2026-11-23 (F):** `checks/87e220.dis`, `checks/87b680.dis`,
`checks/87bb60.dis`, `checks/87db30.dis`, `checks/87b2a0.dis`, `checks/878070.dis`,
`checks/882fc0.dis`, `checks/8834c0.dis`, `checks/882de0.dis`, `checks/87a7a0.dis`,
`checks/8833f0.dis`, `checks/87a370.dis`, `checks/87a570.dis`, `checks/87a680.dis`,
`checks/87a870.dis`, `checks/87a930.dis`, `checks/877dd0.dis`, `checks/877d90.dis`,
`checks/9ba0.dis`, `checks/8fa0.dis`.

**Perguntas abertas:** (1) identidade do objeto `arg3` de `0x862E40` (os dois dwords que
escolhem o caso em `0x85E6C0`); (2) semântica de `code`/`idx`/`kind`; (3) **sabor** da FFT
(RToCCS/RToPerm/RToPack) e **construtor** da spec (quem grava `[spec]==7`); (4) quem grava
`ctx+0x108`/`+0x120`/`+0x138` **do objeto 0x240** (o `+0x108` de `0x877C30` é outro objeto,
contagem `edi*4`, não ponteiro); (5) ~~**aritmética final** de `K[32]`~~ — **FECHADA em
2026-11-23**: `K = δ0`, sem aritmética (§23.7).

**REFUTADO / CORRIGIDO nesta sessão:**

- **REFUTADO (definitivo):** "`0x20E0` pode ser outro objeto IPP com o mesmo magic" — é a
  FFT **direta**; `0x7B40` é a **inversa**. Prova: corpos de 256 B idênticos, slot
  `[rcx]` vs `[rcx+8]` (`0000214A` / `00007BAA`), e o chamador faz fwd → mul espectral →
  inv → `1/n` (§24.4).
- **REFUTADO:** procurar o tag 7 como imediato — 0 ocorrências reais em toda a imagem
  (`tools/find_tag7.py`); o tag é construído/copiado.
- **REFUTADO:** `0x86FE90` não chama nenhum thunk de init de FFT (`0x1310..0x14F0`); a spec
  é criada fora do ctor do `ctx`.
- **CORRIGIDO:** `[rbp+0x35F0]` em `0x88E8A0` **não** é o 5º argumento de pilha; é o home
  slot de `arg1` (`entry+8`; `rbp = entry−0x35E8`, pois `0088E8C0` roda depois de 8 pushes).
  `arg1` é o `ctx` (§23.3-G).
- **CORRIGIDO:** `[ctx+0x10]` não é par de 16 B; é `std::vector` de 24 B `{begin,end,cap}`
  (cap em `00563EC6`).

## 26. Roteiro até o null-test (2026-11-25)

**M1 — FECHADA em 2026-11-25** (resíduo `NÃO PROVADO` abaixo). Divisão `0x1550 -> 0x63640`
transcrita em `port/src/div.rs` (despacho cabeça 8 / laço 16 / bloco 8 / resto 1..7, as duas
aritméticas e o fixup) e usada pelas 4 divisões de `port/src/stage.rs`. Prova em
`checks/r_divisao_63640.md` §2/§4.1/§5/§6. Fatos:

- conferido instrução a instrução contra `checks/63640.dis` (1.005 instruções, re-desmontadas
  do dump, 0 diferenças); **A ≠ B no ULP**; a máscara do recíproco nulo é **diferente** em A
  (`vcmpneq_oqps`+`vandps`, `00063779`) e B (`vcmpeqps`+`vandnps`, `00063AF8`/`00063B0E`) —
  corrigido no port; `vrcpps(|x| ≳ 2^126) = 0` ⇒ quociente `0·num`;
- `n` do estágio: `N = trunc(max(a/k,44100)·(1/44100))·256` (`0086FF35`/`0086FF39`,
  `arg5 = 0x100` em `0086A579`; `k` de `00863531`..`00863552`) ⇒ **`a = 48000` → `N = 256`,
  `n = 257`** = 16 laços B + 1 lane A (o bloco de 8 não roda);
- alinhamento dos 4 `dst`: `dst ≡ [arena] (mod 64 B)` provado dentro de `0x8C1440` (cursor
  sempre `align16`); base `[E+0x30]` de `0x868B50` (`00868B98`/`00868B9C`) = 64 B ⇒
  `dst & 0x1c = 0` ⇒ **sem cabeça**;
- `checks/j_div_avx.rs`: emulação AVX/FMA da sequência do binário × `div.rs`, 2.807.920
  lanes, `bad = 0` (debug, `-O`, `+fma`); mutação de controle detectada.
- Os 2 testes que falhavam estavam **errados** (o código estava certo): o laço de 16 conta
  `n − h` (`00063A51` antes de `00063A67`), e `vrcpps(f32::MAX) = 0`.

**Resíduo `NÃO PROVADO` de M1** (gap em `port/src/pending.rs`): o `E` de
`0x864410` (despacho indireto) ser o objeto de `0x8634A0` (só offsets coincidem); ausência de
outro escritor de `[E+0x30]`; `a` = taxa de amostragem (M4); o gêmeo `0x8C5C40` não
rastreado; sinal/payload de NaN; `vrcpps` é bit a bit só na mesma CPU do oráculo.

**M2 — FECHADA em 2026-11-25** (resíduo `NÃO PROVADO` abaixo). Recíproco de `0x88E130`
(`0088E32F`, in-place) transcrito em `port/src/rcp.rs` e usado por
`port/src/engine.rs::shelf_curve_in_place`. Prova em `checks/s_reciproco_88e130.md`
(`checks/29b260.dis`, `checks/29b9a0.dis`). Fatos:

- despacho: `0x1C8530` → `[0x21C6AE8 + 8·[0x21C7408]=4]` = `0x1C8AC0` → `[0x21C71D8]` =
  **`0x29B260`** (1.856 B pelo `.pdata`; o "200 B" do §15.2 está errado);
- lane normal (`|bits| ∈ [0x00800000, 0x7E7FE800]`, constantes `0x1ED0500`/`0x1ED04C0`/
  `0x1ED0540`): `r0 = vrcpps(x)`, `e = 1 − x·r0`, `r = e·r0 + r0` (FMA, `0029B40E`/`0029B442`/
  `0029B456`); lane especial (`±0`, denormal, `|x| > 0x7E7FE800`, inf, NaN): `1.0f/x` por
  `vdivss` em `0x29B9A0` (`0029B9B5`), status `0x12` para `±0`; handler `0x2D74A0` = `ret`;
- blocos de 32 + cauda de 8 mascarada (padding `0.75`, `0x1ED0600`), sem cabeça de
  alinhamento ⇒ o valor por lane **não depende** de `n` nem de alinhamento;
- MXCSR forçado a `0x1F80` (RN, FTZ = DAZ = 0) e restaurado (`0029B355`..`0029B38D`,
  `0029B59A`..`0029B5D0`), transcrito;
- `checks/j_rcp_avx.rs` (emulador por intrinsics, constantes lidas do dump): `bad = 0`
  estrito (inclui payload de NaN) em 917.568 lanes (debug, `-O`, `-O +avx2,+fma`; host com
  FTZ+DAZ+RZ incluso) e **exaustivo 2^32 `bad = 0`**; 3 mutações de controle detectadas.

**Resíduo `NÃO PROVADO` de M2:** `vrcpps` é bit a bit só na mesma CPU do oráculo (aqui AMD
Ryzen 5 4600G); o índice `4` de `0x21C7408` é o do dump — os caminhos `0x297EE0` (índices
`0..2`) e `0x299C60` (`3`) não foram lidos; os outros chamadores de `0x1C8530` (`0x879CF0`,
`0x885040`, `0088A500`, `0087E0B0`) não foram religados ao `rcp.rs` (fora de M2).

**M3 — FECHADA em 2026-11-25** (resíduo `NÃO PROVADO` abaixo). O `ln` (`0x1C8500` →
`0x1C8A00` → `0x293760`) e o `exp` (`0x1C84A0` → `0x1C8880` → `0x240C00`) da IPP estão
transcritos em `port/src/ippmath.rs`. `engine.rs` os usa por `ipp_ln`/`ipp_exp`. A prova está em
`checks/t_ln_exp_ipp.md`, com as desmontagens `checks/293760.dis`, `293f80.dis`, `240c00.dis` e
`2414c0.dis`. Fatos:

- **Lane vetorial:** só usa `add`/`sub`/`mul`/FMA IEEE com RN, e as duas funções têm o mesmo
  despacho.
  - Blocos: 16 no ln, 32 no exp; cauda de 8 com padding `0.75`.
  - As lanes especiais são refeitas em ordem crescente.
  - `eax` = último status `≠ 0`.
  - O valor por lane não depende de `n` nem do alinhamento.
- **ln:**
  - lane vetorial: redução `m ∈ [2/3, 4/3)` por `i − 0x3F2AAAAB` e polinômio de grau 6;
  - lane especial `0x293F80`: f64, tabela `0x1ECAF60` de **65** entradas `[c,a,b]`, caminho
    perto de 1 (`|d−1| ≤ 2^−6.68`) e −inf/0/negativo/NaN.
- **exp:**
  - lane vetorial: `t = log2e·x + 1.5·2^23`, `y = bits((t<<23) + p)`;
  - lane especial `0x2414C0`: f32, redução **sem** FMA, overflow (`0xC`) e underflow ou
    denormal (`0x11`).
- **Não depende da CPU:** não há `vrcpps`, então o resultado é bit a bit em qualquer CPU com
  FMA. Diferente de M1/M2.
- **`checks/j_ln_exp_avx.rs`:**
  - emulador AVX2/FMA com constantes, máscaras e tabela lidas do dump;
  - amostral: 33.894 lanes por função, `bad = 0`, com MXCSR FTZ+DAZ+RZ restaurado;
  - mutações detectadas: sem especial (ln 6.312, exp 5.012) e FMA partido (ln 30, exp 812);
  - **exaustivo 2^32: `bad = 0` no ln e no exp**. Os dois diferem da libm em 92.579.785
    (ln) e 94.993.725 (exp) entradas.
- **A IPP ≠ libm:** o `ln` difere de `f32::ln` em ~10% das lanes da amostra, e o `exp` difere
  de `f32::exp` em ~51%. As curvas de `0x88E130` mudaram de bits com a troca.
- **Ambiente:** o Windows App Control bloqueia às vezes os `.exe` recém-compilados (`os error
  4551`; o caso mais comum é o harness do `cargo test`). Quando isso acontece, rodar com
  `rustc --test` direto em outro nome de saída. Não é falha de teste.

**Resíduo `NÃO PROVADO` de M3:**

- os caminhos de CPU dos índices `0..3` de `0x21C7408` não foram lidos;
- o port ignora o `eax` de ln/exp, e falta conferir que todos os chamadores do motor também
  ignoram (fica para M5).

(Nota: `pending::first_blocking()` agora devolve `0x8B68AB (008B68BC)`, o sample rate de M4.)

**M4 — PRÓXIMO.** Identidades de estado: sample rate `[ctx+0x60]` (rastrear `r13` em `0x8B3ED0`) e
callback `[rdx+0x50]` (`00867E10`).

**M5** Port do miolo `0x8B3ED0`: F1–F5 (K) + `0x8B8E70`/`0x8B9E40`/`0x8BA1B0`/`0x8BA7B0`/
`0x8A1EE0`/`0x8BA8C0` + satélites `0x8C33D0`/`0x8C3F10`/`0x8C42D0`/`0x8B35A0` + filtro
`0x87BB60`/`0x87E220`/`0x87B2A0`.

**M6** Cadeia completa: 25 estágios de `0x8AD2B0`, `0x8ACC40`, `0x885040`/`0x8875F0`,
rings, estado inicial default.

**M7** Null-test: bloco 512, alinhamento 2304, 0 divergências em `host/test/analise.py`.

Ordem: M1 -> M2 -> M3 -> M4 -> M5 -> M6 -> M7. M3/M4 independentes; M5 é o maior.
