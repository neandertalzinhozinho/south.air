# Especificação do motor de áudio do soothe3 (extraída do dump)

**Atualizado:** 2026-11-24 — §8, §19.6 e §24.5 sincronizados com o plano (`§23.9`, `§23.15`,
`§25`); a FFT foi confirmada no caminho de áudio e o packing é CCS (§5, §19.6).
**Oráculo:** **FECHADO em 2026-11-24** — `host/test/out_soothe3.wav` (48 kHz, bloco 512,
48.000 frames, latência 2304 não compensada, SHA-256 `1218C801A5E61A7591DCE500C40A166E8598532666AE5B7808816899B42BE67B`),
gerado pelo host em `host/` (`PLANO_MOTOR_AUDIO.md` §23.10/§15.3). É validação, não extração:
nenhum coeficiente sai dele.

> Fonte: `dumpsooth/nyx_soothe3_dump.bin` (SHA-256 `68d30368…4f55c`), layout plano
> (`offset == RVA`), base de imagem `0x180000000`, base de ponteiros absolutos
> **`0x199B0000`**.
>
> Regra deste documento: **toda linha tem endereço**.
>
> **DIRETRIZ (2026-11-21):** nada estimado, nada heurístico. Só entra aqui o que foi
> extraído do dump. O que não foi extraído é marcado `NÃO EXTRAÍDO` e **bloqueia** a
> fase — não é substituído por aproximação, "algoritmo equivalente" ou ajuste empírico.
> As seções marcadas `[HEURÍSTICO — PROIBIDO]` são registro histórico e **não são
> especificação**.

---

## 1. Identificação da classe (provado)

O dump **tem RTTI**: cada vtable aponta, em `vtable[-8]`, para um
`CompleteObjectLocator` em `.rdata`, cujo `TypeDescriptor` (offset `+12`) leva ao
nome da classe em `.rdata`.

| Vtable | COL | TypeDescriptor | Classe |
|---|---|---|---|
| `0x2037A58` | `0x2095B50` | `0x23ADE08` | **`.?AVSoothe3AudioProcessor@@`** |
| `0x2036E48` | `0x2096FE0` | `0x23AC970` | `.?AV?$JUCEAudioProcessor@Uvisualisation_data@@$0IP@@kali@@` |
| `0x1F49508` | `0x2087F48` | `0x23A7F70` | `.?AVILok2Commander@pace@@` (protetor — ignorar) |

Ferramenta: `tools/rtti_name.py` (lê `vtable[-8]`, subtrai `0x199B0000`, decodifica
o COL e o `TypeDescriptor`).

Conclusão: `Soothe3AudioProcessor` deriva de
`kali::JUCEAudioProcessor<visualisation_data, 8>` (8 bandas), que deriva de
`juce::AudioProcessor`.

> Nota: o construtor em `0x61BF30` **não** é o do AudioProcessor — ele grava a vtable
> `0x2050B90` (`.?AUMainComponent@@`), ou seja, é o construtor da **UI**.

---

## 2. Vtable de `Soothe3AudioProcessor` (`0x2037A58`)

Slots resolvidos com `v - 0x199B0000` e conferidos contra `.pdata`
(`tools/vtable_dump.py`):

| Slot | RVA | Tamanho | Observação |
|---:|---|---:|---|
| 0 | `0x3467A0` | 136 | destrutor (complete) |
| 1 | `0x490F00` | 135 | destrutor (deleting) |
| 2 | `0x319180` | thunk | ajuste de base |
| 3 | `0x319180` | thunk | ajuste de base |
| 4 | `0x34C3C0` | 33 | retorna `"soothe3"` → **`getName()`** |
| 5 | `0x48A440` | 105 | `getTailLengthSeconds` / programa |
| 6 | `0x350F20` | 9682* | **stub de proteção — NÃO é `processBlock`** (ver §4) |
| 7–9 | `0x314B10` | — | `__cxa_pure_virtual` / stubs |
| 11 | `0x48B980` | 68 | lê `[this+0xD8]`, `[this+0x10C]` (busca de barramento) |
| 12 | `0x48B8E0` | 68 | par do anterior |
| 24 | `0x34F970` | 5538 | **stub de proteção** (mesmo padrão do slot 6) |

\* `9682` é a extensão do `RUNTIME_FUNCTION` em `.pdata` (cobre *offcuts* e blocos
inalcançáveis). O corpo decompilado pelo Ghidra tem **1.019 bytes**.

`getName()` (`0x34C3C0`) monta a string em `rdx` a partir de `0x1C2BC08` e devolve
`"soothe3"`.

---

## 3. Tabela de parâmetros (provado)

- Endereço base: `.data 0x238E9B0`, passo **`0x68`** (`104` bytes).
- Nome inline em `+0x14` (C string, buffer de `0x2C` bytes).
- Dois doubles em `+0x40` e `+0x48`.
- Flags em `+0x50` (`0x101` = booleano/stepped, `0x10001` = bypass).
- **143 parâmetros** legíveis → `docs/engine/params.csv`.

Mapa de campos verificado nos bytes (`checks/pentry2.py`, 2026-11-23):

| Campo | Tipo | Conteúdo provado |
|---:|---|---|
| `+0x00` | qword | ponteiro para **código** em `.text` (ex. `0x19CE5910` → RVA `0x335910`; `0x19CC9170` → `0x319170`, vizinho dos thunks de vtable `0x319180`) |
| `+0x08` | qword | idem (segundo ponteiro de código; `0x19CE5CB0` → `0x335CB0`) |
| `+0x10` | dword | **índice sequencial** `0..142` (`0x238E9B0` = 0, `0x238EA18` = 1, … `0x2392360` = 142) |
| `+0x14` | `char[0x2C]` | nome ASCII inline |
| `+0x40` | f64 | valor A (`Depth` = 10.0, `Mix` = 100.0) |
| `+0x48` | f64 | valor B (`Depth` = 5.0, `Mix` = 100.0) |
| `+0x50` | dword | flags |
| `+0x58` | qword | ponteiro para código em `.text` (`0x19CE51A0` → `0x3351A0`; `0x19CE58F0` → `0x3358F0`) |
| `+0x60` | qword | idem (`0x19CE51E0` → `0x3351E0`) |

**`NÃO PROVADO`:** o papel de `+0x40`/`+0x48` (mín/máx? A/B?) e o das quatro funções
apontadas. O que está provado é que os quatro ponteiros caem em `.text` (base
`0x199B0000`) e que o dword `+0x10` é o índice — logo a tabela é um **registro de
descritores com callbacks**, não um `AudioProcessorValueTreeState`.

Exemplos comprovados:

| Parâmetro | RVA | `+0x40` | `+0x48` | flags |
|---|---|---:|---:|---|
| Depth | `0x238E9B0` | 10.0 | 5.0 | 0x0 |
| Low latency | `0x238EA18` | 1.0 | 0.0 | 0x101 |
| Quality | `0x238EAE8` | 2.0 | 0.0 | 0x101 |
| Detail | `0x238EBB8` | 10.0 | 5.0 | 0x0 |
| Attack | `0x238EC20` | 10.0 | 5.0 | 0x0 |
| Release | `0x238EC88` | 10.0 | 3.0 | 0x0 |
| Stereo focus | `0x238F100` | 1.0 | 0.5 | 0x0 |
| Band 1 used | `0x238F168` | 1.0 | 1.0 | 0x101 |

Layout das 8 bandas (9 parâmetros cada): `used`, `enabled`, `frequency`, `depth`,
`q`, `slope`, `focus`, `channels`, `shape`. Globais: `Band solo`, `Max cut`,
`Wet trim`, `Mix`, `Out trim`, `Delta`, `Bypass`, `Stereo mode/link/focus`,
`Linear phase`, 5 grupos surround, 16 enables de canal.

### Preset padrão (valores `+0x48` da tabela — provado)

| Banda | used | enabled | shape | freq | depth | q | slope | focus |
|---:|:--:|:--:|---|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | Low cut (0) | 100 Hz | 0.0 | 0.707 | 5.0 | 0.5 |
| 2 | 1 | 1 | Bell (2) | 4 kHz | 2.5 | 0.707 | 5.0 | 0.5 |
| 3 | 1 | 1 | High cut (7) | 16 kHz | 0.0 | 0.707 | 5.0 | 0.5 |
| 4–8 | 0 | 0 | Bell (2) | 1 kHz | 0.0 | 0.707 | 5.0 | 0.5 |

`channels` default = `0` na tabela (o original trata 0 como "todos"); o port usa
`0b11` (L+R) para não silenciar o lado. O port já reflete esses defaults em
`settings::default_bands()`.

---

## 4. `processBlock` e o grafo DSP — cadeia PROVADA, entrada indireta

**Estado: a cadeia de áudio está PROVADA; o slot que a chama não tem nome provado.**
A hipótese anterior (slot 6, `0x350F20`) foi **refutada por descompilação**.

### 4.1 Cadeia provada (execução real + estático)

```
0x8646A2  (12.686 B)  topo — 0 refs diretas (despacho por tabela)
  └─ 0x8677F0  ( 1.043 B)  escalonador (lê global DAT_1826B1818)
       └─ 0x8774A0  (  135 B)  tarefa por canal
            └─ 0x881050  (  969 B)  buffers alinhados a 16 floats
                 └─ 0x889BB0  (4.720 B)
                      └─ 0x899940  (2.388 B)
                           └─ 0x8ACC40  (1.634 B, chain-aware)
                                └─ 0x8AD2B0  (5.021 B)
                                     └─ 0x8B3ED0  (20.209 B)  orquestrador
                                          └─ 0x8BF5C0–0x8C4300  cluster aritmético (plano §15.1)
```

> `0x8B3ED0` **não contém a conta**: 4.473 instruções, 1.513 `movups`, 127 `call` e
> **zero** `*ps`/FMA. A aritmética está no cluster `0x8BF5C0–0x8C4300`; ver plano §15.1.

`0x88AC75`, `0x8999AE`, `0x8ACCAE`, `0x8B4268` e `0x86161E` não têm chamada direta:
aparecem como RVA de 32 bits em tabelas de descritores (`0x278B0xx`, `0x2128Dxx`,
`0x21292xx`, `0x21296xx`).

### 4.2 Contradição resolvida (2026-11-22)

A afirmação anterior — "o núcleo está sob virtualização do Themida; ler o DSP exige
devirtualização" — é **falsa**. O `.text` do dump é byte-idêntico ao da imagem viva
(sha256 `af39001e804969f2`), e a cadeia acima foi lida por descompilação estática.
O Themida protege **execução/integridade**, não a leitura do dump.

> **NÃO EXTRAÍDO:** qual slot/vtable chama `0x8646A2` (a chamada é indireta por tabela
> de descritores de 32 bits), e a semântica de `0x8646A2`.

Ghidra, corpo de `0x350F20`:

```c
local_58 = DAT_1821c7640 ^ (ulonglong)auStack_138;   // canário de pilha
do { uVar1 = rdtsc(); ... } while (uVar3 != 0);      // predicado opaco
uVar2 = FUN_180612ae0(0,0xbe57);                     // chamada indireta
if (1 < uVar2) { uVar2 = FUN_180330280(); }
```

- `0x350F20` é um **stub de proteção**: `rdtsc`, predicado opaco e chamada indireta.
  Não contém DSP.
- `0x34F970` (slot 24) tem o mesmo padrão.
- O corpo decompilado tem **1.019 bytes**; os 9.682 vêm da extensão do
  `RUNTIME_FUNCTION` em `.pdata`, não do corpo da função.

### 4.3 Vtable do processador (não é o áudio)

```
Soothe3AudioProcessor (vtable 0x2037A58)
  ├─ getName()   0x34C3C0  → "soothe3"        PROVADO
  ├─ slot 6      0x350F20  → stub de proteção  PROVADO (não é DSP)
  └─ slot 24     0x34F970  → stub de proteção  PROVADO (não é DSP)

MainComponent ctor  0x61BF30                   UI, não áudio
  └─ 0x66A710  → layout de parâmetros ("low latency", "quality", ...)
```

Os dois "stubs" fazem `rdtsc` + predicado opaco + chamada indireta: são checagem de
integridade, não processamento.

---

## 5. FFT / STFT — **CORRIGIDO 2026-11-24: a FFT está no caminho de áudio**

> O título antigo era "RESOLVIDO: FFT é só da UI". A medição de 2026-11-24 (§19.6 e
> `PLANO_MOTOR_AUDIO.md` §24.5-(4)) refuta a separação: o `fwd` do wrapper IPP do áudio é
> `0x72480`, o mesmo ponteiro que `0x6F360` instala no `juce::dsp::FFT`, e ele chama
> `0x1D69E00` (FFT complexa de `n/2`). Ver a nota de correção em §5.1.

### 5.1 Prova de que a FFT não está no caminho de áudio — **REFUTADA em 2026-11-24**

- `0x1D69E00` (FFT do IPP) tem **4** chamadores diretos: `0x72480`, `0x72A40`,
  `0x73440`, `0x1C1080`.
- `0x72480` e `0x72A40` **não têm chamada direta**: são gravados como ponteiros de
  função por `0x6F360` (construtor `juce::dsp::FFT`), nos `lea` de `0x6F4D8`
  (`0x72480`), `0x6F4E6` (`0x72A40`) e `0x6F4F4` (`0x73440`).
- `0x73440` só é chamado por `0x74180`, `0x74CA0`, `0x75AA0`.
- Nenhum deles é alcançável a partir da cadeia do §4.1 (BFS sobre `xrefs.csv`).
- As funções de áudio `0x885040`, `0x8875F0`, `0x88FB20`, `0x892770`, `0x8AD2B0`,
  `0x8B8E70`, `0x8B3ED0`, `0x8A1D10`, `0x8ABAA0`, `0x8AC510` **não chamam FFT nenhuma**.

As 3.504 chamadas a `0x1D69E00` observadas no processo vivo eram do **espectro da UI**.

> **Correção de 2026-11-22 (§10.6):** esta prova vale **só para a FFT do JUCE**
> (`0x1D69E00`). O áudio **usa** transformada pelos stubs IPP (`IPPCODE`/`IPPDATA` estão
> linkados): `0x885040 → 0x8B2680 → 0x1010/0x1280/0x15E0`. A afirmação "FFT é só da UI"
> fica **retirada** como afirmação geral; ver `PLANO_MOTOR_AUDIO.md` §24 e §10.6 abaixo.
>
> **Correção de 2026-11-24 (medição, §19.6):** o caminho do áudio chega, sim, a `0x1D69E00`:
> `000725BA`..`000725D6` (dentro de `0x72480`, o `fwd` que `0x72180` grava em `wrapper+0x18`)
> chama `0x1D69E00` com `rdx = n/2` para a ordem 9. Ou seja, o **mesmo** `0x72480` que `0x6F360`
> instala no `juce::dsp::FFT` é o forward do áudio; a separação "FFT do JUCE × FFT do áudio"
> não existe neste binário. O que a medição mostra é que `0x1D69E00` é uma FFT complexa de
> `n/2` sobre pares intercalados (§19.6) e que o CCS vem depois, em `0x895C0`.

### 5.2 O que substitui o STFT — PROVADO

| Item | Valor | Evidência |
|---|---|---|
| Bloco | **N = 256** @ 44,1 kHz (278 @ 48 k, 557 @ 96 k) | `0x873440`, constante `1/44100` em `0x2079D04` |
| Campos derivados | `ctx+0x28=N`, `+0x38=2N`, `+0x40=N+1`, `+0x60=N/2` | `0x873440` |
| Janela | **Hann periódica** `w[i] = (1 − cos(2π·i/N))·0.5` | `0x877DD0` |
| Constantes da janela | `1.0` `0x207A138`, `2π` `0x207A1E0`, `0.5` `0x207A0B8` (todos double) | dump |
| Normalização / hop | `NÃO EXTRAÍDO` | — |

Variante com offset (`0x87A370`), para janela parcial/crossfade:

```c
b[i] = (double)i / N * (1.0 - p) + p;    // p = param_3 (float)
w[i] = (double)(1.0 - cos(b[i] * 2π)) * 0.5;
```

### 5.3 Histórico: FFTPACK presente, não usado no áudio

Texto de licença **FFTPACK** em `.rdata` `0x1FBAF17` e `0x1FC7F27`: prova que há código
FFTPACK embutido, **não** que o áudio o chame. Os buffers de 256 floats em `.rdata`
(`0x1DF3F80`, `0x2037240`) eram candidatos a janela e **foram descartados**: a janela
real é gerada em runtime por `0x877DD0`.

> **Nomes reais das opções no dump:** as strings do construtor de layout são
> `normal`, `ultra`, `minimum phase`, `linear phase`, `low latency`, `quality`.
> Os nomes `Eco / High / Extreme` que apareciam aqui **não existem no binário** e
> foram removidos.

> **[HEURÍSTICO — PROIBIDO]** O port usava `1024 / 2048 / 4096 / 8192` como tamanho
> de FFT. Esse valor é inventado e **não é especificação**.

---

## 6. O que está provado vs. estimado

| Item | Estado | Evidência |
|---|---|---|
| Classe `Soothe3AudioProcessor` | **PROVADO** | RTTI/COL `0x2095B50` → `0x23ADE08` |
| Vtable `0x2037A58` | **PROVADO** | `tools/vtable_dump.py` |
| `getName()` = `"soothe3"` | **PROVADO** | `0x34C3C0` |
| 143 parâmetros + ranges | **PROVADO** | tabela `0x238E9B0`, `params.csv` |
| Código FFTPACK presente no binário | **PROVADO** | strings de licença `0x1FBAF17`, `0x1FC7F27` |
| FFT usada no caminho de áudio | **REFUTADO** | §5.1 — nenhuma rota de áudio alcança a FFT |
| `processBlock` (slot com nome) | **NÃO IDENTIFICADO** | cadeia provada (§4.1); a entrada é indireta por tabela |
| Cadeia de áudio até o núcleo | **PROVADO** | §4.1 — `0x8646A2 … 0x8B3ED0` |
| Tamanho de bloco | **PROVADO** | `0x873440` → N = 256 @ 44,1 kHz |
| Janela | **PROVADO** | `0x877DD0` — Hann periódica + RVAs das constantes |
| Hop / overlap-add / normalização | **PROVADO** | `0x8B2680`: hop `n/2`, overlap-add, escala `1/n` (plano §24.4) |
| Tipo de filtro por banda | **PROVADO em parte** | `0x882FC0` fechado (§8.2(f)): curvas `A^(1−σ)` por `0x1340`. Falta a origem de `A1`/`A2` e o `0x87B2A0`. `0x879CF0` **descartado**: é curva de normalização, não espaçamento (§9.2) |
| Estagiador + mistura final por grupo | **PROVADO estrutural** | §8.4 — `0x8C1440`: 5 grupos, 16 buffers, `dst←(1−g)dst+g·staged` |
| Detecção Soft/Hard, knee, gate | **NÃO EXTRAÍDO** | cluster `0x8BF5C0–0x8C4300` + `0x8C5FD8` (plano §15.1) |
| Coeficientes de attack/release | **NÃO EXTRAÍDO** | idem |
| Curvas das 8 bandas (Q/slope/focus) | **PROVADO (curva)** | `0x882DE0` = sino gaussiano em log2-freq (§10.4); o mapeamento Q/slope/focus→parâmetro segue `NÃO PROVADO` |
| Núcleo DSP sob virtualização Themida | **REFUTADO** | §4.2 — `.text` do dump é byte-idêntico à imagem viva |

---

## 7. Mapa port (Rust) ↔ original

| Módulo Rust | Bloco do original | Estado |
|---|---|---|
| `app/src/dsp/stft.rs` | **nada** — não existe FFT no áudio (§5.1) | **FORA DA DIRETRIZ** (realfft + tamanhos inventados) |
| `app/src/dsp/detect.rs` | detecção soft/hard, detail, tilt, gate | **FORA DA DIRETRIZ** (heurístico) |
| `app/src/dsp/curve.rs` | 8 bandas × shapes, slope, focus | **FORA DA DIRETRIZ** (heurístico) |
| `app/src/dsp/envelope.rs` | attack/release | **FORA DA DIRETRIZ** (heurístico) |
| `app/src/dsp/stereo.rs` | link/focus/balance/M-S/sidechain | **FORA DA DIRETRIZ** (heurístico) |
| `app/src/dsp/output.rs` | mix/wet/out trim/delta/max cut | **FORA DA DIRETRIZ** (heurístico) |
| `app/src/settings.rs` | 143 parâmetros | 8 bandas + globais reais — **PROVADO** (tabela `0x238E9B0`) |

A estrutura (8 bandas, nomes, ranges e defaults) vem da tabela de descritores e está
provada. As **fórmulas** não foram extraídas. Nenhum módulo de `app/src/dsp/` é
especificação enquanto a Fase 3 não produzir pseudocódigo rastreável.

---

## 8. Cluster aritmético — estágios fechados (2026-11-22)

Detalhe completo e prova instrução-por-instrução no plano, §16.

### 8.1 `0x8C3C20` — suavização forward-backward (PROVADO)

465 B, zero chamadas. Percorre `count` arrays de `length` floats e aplica, **in place**,
um one-pole com coeficiente `0.1f` (`0x2079DB0`) duas vezes: para frente e para trás.

```c
// 0x8C3C20 — estrutura: { void *arrays[128]; int32 count; int32 length; }
for (i = 0; i < count; i++) {
    float *v = arrays[i];
    float p = v[0];
    for (j = 0; j < length; j++) { p += (v[j] - p) * 0.1f; v[j] = p; }   // 0x8C3C90
    for (j = length - 2; j >= 0; j--) { p += (v[j] - p) * 0.1f; v[j] = p; } // 0x8C3D50
}
```

Chamada de dentro do núcleo (`808B3ED0.c:2666`) sobre um local de 130 qwords
(`local_908`) cujos campos `+0x400` (count) e `+0x404` (length) são o mesmo layout usado
como comprimento de `fill` em `808B3ED0.c:4838`.

**NÃO PROVADO:** que os arrays sejam "ganhos por banda" (o formato é genérico).

### 8.2 `0x8B3ED0` — a dinâmica **inline** (PROVADO parcial, 2026-11-23)

> **Correção de 2026-11-23.** §15.1 do plano dizia que `0x8B3ED0` não tem conta ("zero
> `*ps`/FMA"). A parte vetorial **não** está lá, mas a conta **escalar da dinâmica está**:
> 23 `mulss`, 17 `subss`, 7 `maxss`, 5 `minss`, 4 `divss` dentro de
> `0x8B3ED0–0x8B8DC1` (`checks/fops8b3ed0.txt`). Quatro blocos provados:

**(a) `0x8B4E20`–`0x8B4FAC` — rugosidade média de cada array de banda.** Laço por banda;
`rdi` percorre `rbp+0xC40` (ponteiros), `n = [r13+0x40] >> 2` (`008B4E29`, `008B4E31`).

```c
prev = v[0]; acc = 0.0;                                   // 008B4E38, xmm6/xmm13=0 (008B4DF4)
for (k = 1; k < n; k++) {
    acc += (double)fabsf(v[k] - prev) / ((double)prev + 1e-7);  // 008B4E8B..008B4F23
    prev = v[k];
}
m = (float)(acc / n);                                     // 008B4F88 divss
if (m < 0.001) scale_all(v, m);                           // 008B4F93 comisd, 008B4FA7 call 0x1220
```
Prova: `008B4E93 andps xmm0,xmm7` com `xmm7 = [0x207BAE0]` (máscara de sinal `0x7FFFFFFF`,
por isso lê como NaN); `008B4E0D movsd xmm8,[0x2079E08]` = `1e-7` (f64); `008B4E16 movsd
xmm9,[0x2079F48]` = `0.001` (f64); `008B4F88 divss xmm6,xmm1` (acumulado/n); `008B4F93
comisd xmm1,xmm9`; `008B4FA4 movaps xmm0,xmm6` + `008B4FA7 call 0x1220` (`a[i] *= s`).

**(b) `0x8B68AB`–`0x8B6939` — coeficiente de one-pole a partir de um tempo.** Bloco
condicionado por `[r13+0x58] != 0` (`008B68AB`/`008B68B6`):

```c
N    = (float)(int64)*(qword *)(r13 + 0x60);              // 008B68BC..008B68E0 (cvtsi2ss)
x    = ((float)*(dword *)(r13 + 0x20) / N) * 0.001f * 500.0f;  // 008B68E4..008B6901
coef = 1.0 - pow(0.1, 1.0 / x);                           // 008B690C..008B6932
```
Prova: `008B6918 call 0x1C9A5AD` → IAT `0x1D8D848` = **`pow` (double)**
(`checks/thunk_map.txt`); `008B6910 movsd xmm0,[0x207A030]` = `0x3FB99999A0000000` =
`0.10000000149011612` = `(double)0.1f`; `008B68F9 mulss [0x2079D24]` = `0.001f`,
`008B6901 mulss [0x207A560]` = `500.0f`; `008B6932 subsd xmm6,xmm0` com `xmm6 = 1.0`
(`0x207A138`). `r13` é o **argumento 1 de `0x8B3ED0`** (`008B3F14 mov r13,rcx`), logo
`+0x20`/`+0x58`/`+0x60` são campos do **objeto de contexto**, não do bloco de estado
(`state = [ctx+0x2C38]`). **`NÃO PROVADO`:** qual campo (`+0x20`/`+0x58`/`+0x60`) é sample
rate, qual é tempo, e em que unidade; `+0x60` é lido como `qword` inteiro de 64 bits em
`008B68BC`, e a aritmética `(t / [ctx+0x60]) · 0.001 · 500` não é dimensionalmente
`t·fs/1000`.

**(c) `0x8B5AF2`–`0x8B5CA7` — escalar de ganho aplicado a **todas** as bandas.** Entradas
lidas do bloco de estado (ver §8.3): `s0 = state[0x00]` (`008B5AFB`), `A = state[0x04]`
(`008B5B07`).

```c
T = clamp((s0 - 0.8f) * 5.0f, 0, 1);                      // 008B5B36, 008B5B46, 008B5B6B
u = expf(ln4 * clamp((1.0f - 0.5f*A) * T, 0, 1));          // 008B5B21/42, expf(008B5B84) com ln4=0x207A00C
y = expf( (logf(powf(10.0f, 2.4f) + 0.1f) + ln10) * clamp(s0,0,1) - ln10 ) - 0.1f;
                                                          // 008B5B99 powf, 008B5B9E +0.1,
                                                          // 008B5BA6 logf, 008B5BAB -(-ln10),
                                                          // 008B5BBD *clamp(s0), 008B5BC1 -ln10,
                                                          // 008B5BC9 expf, 008B5BD5 -0.1
v = powf(10.0f, -24.0f * 0.05f * clamp(A*A, 0, 1));       // 008B5BE2..008B5BFD = 10^(-1.2*clamp(A²,0,1))
scale = u * (y * v);                                      // y*v em 008B5C02; *u em 008B5C8A
for each band: 0x1220(band, n, scale);                     // 008B5C90..008B5CA7
```
Constantes com RVA e valor: `0.5f` `0x2079EA8`, `0.8f` `0x2079F38`, `5.0f` `0x207A2D8`,
`1.3862943649291992f` `0x207A00C` (= `ln 4`), `0.1f` `0x2079DB0`, `2.4f` `0x207A1E8`,
`-2.3025851249694824f` `0x207A6D4`, `+2.3025851249694824f` `0x207A1D0` (= `ln 10`),
`-24.0f` `0x207A734`, `0.05f` `0x2079D88`, `10.0f` `0x207A360`, `1.0f` `0x2079F9C`,
`0.0f` (`xorps xmm13,xmm13` em `008B4DF4`).
Thunks de math usados: `0x1C9A9D7` = `expf` (IAT `0x1D8D7F0`), `0x1C9A9FB` = `logf`
(`0x1D8D808`), `0x1C9AA01` = `powf` (`0x1D8D818`).

**Ordem exata (corrigida em 2026-11-24).** `u` fica em `xmm8` (`008B5B91`), `y` em `xmm7`
(`008B5BCE`/`008B5BD5`) e `v` em `xmm0` (`008B5BFD`); `008B5C02 mulss xmm7,xmm0` calcula
**`y·v` primeiro** e `008B5C8A mulss xmm8,xmm7` multiplica por `u`, ou seja `u·(y·v)` — não
`(u·y)·v` (a ordem muda o arredondamento). Além disso `y` tem o termo `−ln10` **depois** do
produto por `clamp(s0)`: `008B5BAB subss xmm0,[0x207A6D4]` soma `+ln10` dentro do log, e
`008B5BC1 subss xmm0,[0x207A1D0]` subtrai `ln10` antes do `expf`. A transcrição em Rust é
`checks/stage_j_engine.rs` (`band_gain_scale`, `u * (y * v)`).

**`NÃO PROVADO`:** o significado de `s0`/`A` (nomes) e o ramo `r14b == 0`
(`008B4FDC..008B51D4` → `008B51D4`, que chama `0x8C0230` e usa `powf(10, -0.45)`
em `008B5370`/`008B537C`).

**(d) `008B67F0`–`008B68A5` — convolução de 16 taps no eixo da frequência, por banda.**
Laço por banda (`rdi = rbp+0x30D0`); para cada banda:

```c
c7 = max(dot16(band, K7 @0x2077800), 1e-7f);   // 008B680D lea rcx,K7; 008B6814 call 0x1400; 008B6842 maxss
c6 = max(dot16(band, K6 @0x2077740), 1e-7f);   // 008B683B; 008B6847 call 0x1400; 008B685B maxss
0x11F0(band, K7, n, /*s*/ (c6/c7)*c7);         // 008B6866-008B6871
0x11F0(band, K6, n, /*s*/ (c7/c6)*c6*(xmm11-xmm10)); // 008B6876-008B6893
```
`0x11F0` está provado (subagente, 2026-11-23) como `dst[i] += src[i]*s`, com
`src=rcx`, `dst=r8`, `n=r9d`, `s=`**`xmm1`** (`0005C46 vfmadd213ss xmm0,xmm1,[r8]`).
`0x1400` = thunk IPP → impl `0xAC20` (assinatura **`NÃO PROVADA`**). Os dois kernels têm
16 floats: `K7` em `0x2077800` (`0.13522772`, …) e `K6` em `0x2077740`
(`3.6440198e-08`, …); `xmm8 = 1e-7f` (`0x2079CEC`). `(c6/c7)*c7` e `(c7/c6)*c6` são
**identidades módulo arredondamento** — não há clamp escondido ali.

**(e) `0x88E130` — gerador de curva sigmoide ("shelf curve"), PROVADO (2026-11-23).**
Desmontagem completa: `checks/88e130.u8.dis` (155 linhas). Assinatura:

```c
void f88E130(block *dst /*rcx*/, const block *src /*rdx*/,
             float A /*xmm2*/, float k /*xmm3*/, float G /*5º arg, [rsp+0x100]*/);
```

`block` = `{float *p; int n;}` em `+0x00`/`+0x08` (lido como 16 B: `0088E158 movaps
xmm3,[rdx]`, `0088E164 movaps xmm2,[rcx]`); `src` tem ainda um `int flag` em `+0x80`
(`0088E15D` / `0088E1D8` / `0088E219`). `G` é o **5º argumento, passado em pilha**:
`[rsp+0x100]` = 5º *home slot*/caller-frame +0x28 (`0088E36D`).

Ramo constante (`0088E144`–`0088E1C2`): se `fabsf(k) <= 1.1920929e-7f`
(`0088E144 andps [0x207BAE0]`, `0088E14E comiss [0x2079CF0]`), então
`dst ← src` (só se `src->flag == 1`, `0088E181 call 0x10A0`), `dst[i] *= 0.0f`
(`0088E19F call 0x1220` com `xmm0 = 0`), `dst[i] += 1.0f` (`0088E1C2 call 0x12E0`) ⇒
**`dst[i] = 1.0f`**.

Ramo geral (`0088E1D8`–`0088E3E5`), nesta ordem exata:

```
A1   = max(A, 1.1920929e-7f)            ; 0088E1DF  maxss [0x2079CF0]
invA = 1.0f / A1                        ; 0088E208 1.0 [0x2079F9C] / 0088E211 divss
ks   = k * 0.166666672f                 ; 0088E1E7  mulss [0x2079DE0] = 1/6
if (src->flag == 1) dst <- src          ; 0088E233  call 0x10A0
dst += 1.1920929e-7f                    ; 0088E256  call 0x12E0
dst *= invA                             ; 0088E275  call 0x1220
dst  = ln(dst)                          ; 0088E298  call 0x1C8500  (impl 0x293760)
dst *= 1.44269502f                      ; 0088E29D..0088E2AB, 0x207A020 = log2(e)
ks   = -ks                              ; 0088E2B3  xorps [0x207BB20] (máscara de sinal)
dst *= ks                               ; 0088E2D0  call 0x1220
dst  = exp(dst)                         ; 0088E2EE  call 0x1C84A0  (impl 0x240C00)
dst += 1.0f                             ; 0088E311  call 0x12E0
dst  = rcp(dst)                         ; 0088E32F  call 0x1C8530  (impl 0x29B260, vrcpps+1 FMA; M2)
dst += -0.5f                            ; 0088E352  call 0x12E0, 0x207A690
dst *= G                                ; 0088E376  call 0x1220, G = [rsp+0x100]
dst *= 0.115129255f                     ; 0088E399  call 0x1220, 0x2079DBC = ln10/20
dst  = exp(dst)                         ; 0088E3B7  call 0x1C84A0
```

Forma fechada, por amostra, com `v` = `dst[i]` depois da cópia opcional (isto é, `v = src[i]`
quando `src->flag == 1`):

```
u  = (v + 1.1920929e-7) / max(A, 1.1920929e-7)
σ  = 1 / (1 + exp(-(k/6)·log2(u)))          # = 1 / (1 + u^(-k/6))
y  = exp( G · 0.115129255 · (σ − 0.5) )
```

Notas de port (bit-exatidão):
- o recíproco é **aproximado** (`vrcpps` + Newton em `0029B442`/`0029B456`), não `divss`.
  **PROVADO em M2 (2026-11-25, `checks/s_reciproco_88e130.md`):** despacho
  `0x1C8530` → `0x1C8AC0` → `[0x21C71D8]` = `0x29B260`; lane normal
  (`|bits(x)| ∈ [0x00800000, 0x7E7FE800]`, constantes `0x1ED0500`/`0x1ED04C0`/`0x1ED0540`):
  `r0 = vrcpps(x)`, `e = 1 − x·r0`, `r = e·r0 + r0` (FMA, `0029B40E`/`0029B442`/`0029B456`);
  lane especial (`±0`, denormal, `|x| > 0x7E7FE800`, inf, NaN): `r = 1.0f/x` por `vdivss`
  (`0x29B9A0`, `0029B9B5`); blocos de 32 + cauda de 8 com padding `0.75` (`0x1ED0600`), sem
  cabeça de alinhamento — o valor por lane não depende de `n` nem de alinhamento; MXCSR forçado
  a `0x1F80` (FTZ = DAZ = 0) durante a conta (`0029B355`..`0029B38D`). Port:
  `port/src/rcp.rs`; `checks/j_rcp_avx.rs`: `bad = 0` estrito, exaustivo 2^32. Resíduo
  `NÃO PROVADO`: `vrcpps` só é bit a bit na mesma CPU do oráculo; caminhos de CPU `0..3`
  (`0x297EE0`, `0x299C60`) não lidos;
- `log2` é feito como `ln·1.44269502f` e `exp` é o wrapper `0x1C84A0`, não `powf`;
- `k/6` usa a constante float `0.166666672`, não `1.0/6.0` em f64;
- `G` é multiplicado **depois** de `σ − 0.5` (a ordem trocada muda o arredondamento).

`NÃO PROVADO`: semântica física de `A` (frequência?) e de `k` (inclinação). O nome "shelf"
descreve só a forma `σ`.

Transcrição Rust (J6, `checks/stage_j_engine.rs`, 8 testes): `shelf_curve_in_place` (`0x88E130`)
e `shelf_pair_apply` (`0x882FC0`), além de `smoother_fwd_back` (`0x8C3C20`),
`detector2_in_place` (`0x8C0BD0`) e `one_pole_coef` (`0x8B68AB`). Desde M3 (2026-11-25), o ln e
o exp de `0088E298`/`0088E2EE`/`0088E3B7` são as impls IPP `0x293760`/`0x240C00` transcritas bit a
bit em `port/src/ippmath.rs` (antes eram `f32::ln`/`f32::exp`, que diferem da IPP). O recíproco vetorial de `0x88E130` (`0x1C8530` →
`0x29B260`) **não** é mais `1.0/x`: desde M2 (2026-11-25) é `rcp::inv_32f_in_place`
(`port/src/rcp.rs`), bit a bit com o binário na mesma CPU.

**(f) `0x882FC0` — duas curvas de shelf aplicadas a buffers de banda, PROVADO (2026-11-23).**
Desmontagem completa: `checks/882fc0.u8.dis` (249 linhas). Assinatura:

```c
void f882FC0(this /*rcx, n = this+0x84*/, const band *b /*rdx, 0x90 B*/,
             float A1 /*xmm2*/, float A2 /*xmm3*/, arena *ar /*5º arg*/);
```

Provas de papel dos argumentos: `00882FE6 mov ebx,[rcx+0x84]` = `n`;
`00882FF6 mov rdi,rdx` (band); `00882FFD`/`00883005` guardam `xmm2`→`xmm0` e `xmm3`→`xmm12`;
`00882FEF mov r14,[rbp+0x160]` = 5º arg = arena `{float *base; int fill@+0x18}`
(`00883014 mov r13d,[r14+0x18]`, `0088301C mov rax,[r14]`).

Alocação (cursor da arena): buffer A em `base + fill*4` (`0088301F`–`00883050`), buffer B no
mesmo padrão (`00883117`–`0088315A`); o cursor é **restaurado** no fim
(`008833C0 mov [r14+0x18],r13d`) — os dois buffers são temporários.

Bloco 1 (`00883054`–`00883112`):

```
L1  = log10f(A1)                        ; 00883054  thunk 0x1C9A5A1 → IAT 0x1D8D798
bw1 = -20.0f * L1                       ; 0088307D  mulss 20.0 [0x207A3B0]
                                        ; 008830C8/008830CB xorps sinal ⇒ [rsp+0x20] = G
tmp = *b (0x90 B copiados)              ; 00883059..008830D2 (chunks de 16 B, [rsp+0x40]..[rbp-0x40])
f88E130(bufA{n}, &tmp, 500.0f, 12.0f, bw1)
                                        ; 008830E7 ; 500 [0x207A560], 12 [0x207A384]
bufA *= powf(10.0f, 0.5f*L1)            ; 008830EC ×0.5 [0x2079EA8]; 008830FC ×0.05 [0x2079D88]
                                        ; 00883107 powf [0x207A360=10]; 00883112 0x1220
```

Bloco 2 (`0088315E`–`00883212`) é idêntico com `A2` (`xmm12`), `f88E130` com
`A = 2000.0f` (`008831D1`, `0x207A5A8`) em vez de `500.0f`, e `powf`/escala em
`00883207`/`00883212`.

`powf(10, 0.5·log10(A))` é `sqrt(A)` **matematicamente**, mas o binário usa `powf`; manter a
chamada para bit-exatidão.

Aplicação (`00883217`–`008833B6`): copia `this` (0x90 B) para a pilha, chama `0x87A7A0`
(`0088327A`), e lê `c = this[0x80]` (i32, `008832C1 movd eax,xmm1`) e `p = this[0]`
(u64, `008832D7 movq rdx,xmm2`). Então:

```
if (c == 1)       0x1340(curve, p,       n)   ; 008832E4
else if (c > 0)   for i<c: 0x1340(curve, this_ptr[i], n)   ; 00883309
repete para curve B                             ; 00883388 / 008833A9
```

`0x1340` = **multiplicação elemento a elemento, in place**: `dst[i] = a[i]·dst[i]` com
`a=rcx`, `dst=rdx`, `n=r8d`. Prova: selector 4 → tabela `0x21C6188[4] = 0x9BA0`
(`00009C40 vmovups ymm0,[rcx+r9*4]` … `00009C4D vmulps ymm1,ymm0,[rdi+r9*4]` …
`00009C5A vmovups [rdi+r9*4],ymm1`, com `00009BA5 mov rdi,rdx`).

Logo o fator multiplicativo final aplicado a cada amostra `X` de um buffer alvo é
`sqrt(A1)·exp(bw1·0.115129255·(σ1−0.5)) · sqrt(A2)·exp(bw2·0.115129255·(σ2−0.5))` com

```
bw_i = -20·log10(A_i)
σ_i  = 1 / (1 + exp(-(12/6)·log2((v_i + eps)/max(A_i, eps))))
```

e `v_i` = amostra do **bloco `src`** (`b`, copiado) quando `b->flag@0x80 == 1`. Simplificando
`sqrt(A_i)·exp(-20·log10(A_i)·0.115129255·(σ_i−0.5)) = A_i^(1−σ_i)`, o fator é

```
A1^(1−σ1) · A2^(1−σ2)
```

que é exatamente `X^(1−σ)` **no caso em que o bloco `src` é o próprio bloco alvo**. Em geral
`σ_i` é função do conteúdo de `b` e o fator multiplica outro buffer (§10.4: `0x87BB60`
pré-preenche os segmentos com `1.0f` e chama `0x882FC0` em `0087C231`/`0087C4DA`).

`NÃO PROVADO`: se `b->flag@0x80` vale 1 nos dois sítios de chamada de `0x87BB60`; qual é o
buffer de banda real por trás de `this[0]`; a origem de `A1`/`A2` (frequências de corte?).

**Primitivas usadas por (e)/(f) — implementação provada, com RVA:**

| Thunk | Implementação (selector `[0x21C7408]=4`) | Semântica |
|---|---|---|
| `0x1220` | `0x2300` (tabela `0x21C6008[4]`) | `dst[i] *= s` (`0000232B call 0x1D2E460`) |
| `0x12E0` | `0x8FA0` (tabela `0x21C6108[4]`) | `dst[i] += s`; sai cedo se `s == 0` (`00008FC1`) |
| `0x1340` | `0x9BA0` (tabela `0x21C6188[4]`) | `dst[i] *= a[i]` (`00009C4D vmulps`) |
| `0x10A0` | — | cópia N floats |
| `0x10D0` | — | zera N floats (memset) |
| `0x11F0` | `0x5BC0` | `dst[i] += src[i]*s` (`s` em `xmm1`) |
| `0x1370` | `0xA120` | `dst[i] += src[i]` (vetor) |
| `0x1550` | `0x63640` | `dst = num/den` (`den=rcx`, `num=rdx`, `dst=r8`) |
| `0x1580` | `0xCCE0`→`0x65EA0`→`0x6CE80` | `dst[i] += a[i]*b[i]` (FMA) |
| `0x1100` | `0x3480` | clamp in place (`bound=xmm2`, `mode=r9d`: `0`=max, `4`=min) |

**(g) As cinco faixas aritméticas do núcleo (K, PROVADO por instrução em 2026-11-24 —
`checks/k_core.md`, verificado em `checks/verificacao_k_o.md`).**

Todas operam sobre `state = *(void**)(engine+0x2C38)`; `x = state+4` (índice 5, f32, lido cru
por `008B507C mov eax,[rax+4]` + `008B507F movd`).

| Faixa | Fórmula provada | RVAs |
|---|---|---|
| F1 | `g = 10^(0.05·(20·clamp(x,0,1) − 60)) · M`, com `M` = máximo medido por `0x86E780` | `008B5060`, `008B5083`–`008B5095`, `008B50A2`, `008B50B1`; aplicação `008B51BD call 0x1250` |
| F2 | por buffer: `P = Σ_{k<32} buf[k]·coef32[k]`; `buf *= P·10^(−0.45)` | `008B5370`/`008B537C` (powf), `008B539B` (`n=0x20`), `008B53AB` (tabela `0x2077680`), `008B53B2` (`0x1400`), `008B53C6`, `008B545B` (`0x1160`) |
| F3 | `s = −0.25 − 0.25·powf(x,4)`; `buf *= s` | `008B6582`/`008B658E` (powf), `008B6627`, `008B663E`, `008B6646`, `008B6659` (`0x1220`) |
| F4 | `y = exp(c·(ln(2 + 1/3 − x²) + 1.099612832) − 1.099612832) − 1/3`, `c = clamp(state+0,0,1)` | `008B7AFC`–`008B7B4D` (logf `0x1C9A9FB`, expf `0x1C9A9D7`) |
| F5 | gate `([engine+0x48] > 2)` → `0x8BFCB0`+`0x8BFD30`+`0x8C3F10`; depois `logf(powf(10,−3))` e `logf(powf(10, −0.05·v))` | `008B3FCC`/`008B3FD1` (seta), `008B868B`, `008B869C`–`008B86C0` |

Constantes: `0x207A360`=10, `0x2079D88`=0.05, `0x207A3B0`=20, `0x207A474`=60, `0x207A68C`=−0.45,
`0x2079E18`=0.25, `0x207A67C`=−0.25, `0x207A2B8`=4, `0x207A188`=2, `0x2079E54`=0.3330000043,
`0x207A6AC`=−1.099612832, `0x2079FC0`=+1.099612832, `0x207A6E4`=−3, `0x207A66C`=−0.05,
`0x2079F9C`=1.0, `0x207A138`=1.0 (f64).

`0x1400` = stub IPP (índice 4, tabela `0x21C6288`) → `0xAC20` → `0x5F5C0`, produto escalar
**PROVADO**: `out = Σ a[i]·b[i]` (`0005F646 vmulss`, `0005F64E vaddss`, `0005F68D
vfmadd231ps`, store `0005F6F7 vmovss [r9],xmm0`). `0x2077680` é o vetor de 32 coeficientes,
não a tabela de salto.

**Ordem de soma (bit-exata, 2026-11-24):** só dois `n` chegam a `0x5F5C0` no núcleo —
`n = 0x20` (`008B539B`, F2) e `n = 0x10` (`008B6807`/`008B6828`). Ambos caem em
`0005F705` (`and r8d,~15`) e percorrem o mesmo laço: dois acumuladores de 8 lanes
(`acc0 += b[k..k+8]·a[k..k+8]` em `0005F68D`; `acc1 += b[k+8..k+16]·a[k+8..k+16]` em
`0005F693`, `k = 0,16`), depois `L[i]=acc0[i]+acc1[i]` (`0005F6A3`),
`x2=[L0+L4,L1+L5,L2+L6,L3+L7]` (`0005F6AD`), `x4=[x2[0]+x2[2],x2[1]+x2[3]]`
(`0005F6B1`/`0005F6B5`) e `x4[0]+x4[1]` (`0005F6B9 vshufps 0xf5` / `0005F6BE vaddss`).
`checks/j_dot32_avx.rs` compara a emulação escalar com as **mesmas instruções AVX/FMA** em
hardware: 400.000 casos, `bad=0`; a soma sequencial ingênua diverge em 298.626 deles.

**`0x8C33D0` (K, PROVADO nas primitivas):** `D = B − A` (`0x11C0` → `0x50E0`, `vsubss`
`00005186`), `D = min(D,0)` duas vezes (`0x1250` → `0x69C0`, `vminss xmm0,xmm0,xmm3`
`00006A65`; `0x1100` → `0x3480`, `vminps` `00003520`), e dois acúmulos
`dst += D·peso` (`0x11F0` → `0x5BC0`, `vfmadd213ss` `00005C46`) com pesos `xmm2`/`xmm3`
(`008C3A43`/`008C3B93`).

O cabeçalho do descritor `B` é lido em `008C34BD movsxd rsi,[rbp+0x744]` (= `B+0x404`,
comprimento) e `008C34C7 movsxd r12,[rbp+0x740]` (= `B+0x400`, contagem), a partir da cópia
de `B` em `[rbp+0x340]`. **`0x8C32C0` não escreve esses campos:** ele copia `A` e `B` para a
pilha (`008C32E7`–`008C33A3`) e escreve o resultado em `arg1+0x1A0` (`008C33A6 lea
r8,[rcx+0x1a0]`, `008C33BD call 0x8CB040`). `NÃO PROVADO`: quem preenche
`[rbp+0x1050]+0x400/+0x404` antes de `008B6A7E` — a cadeia para em `008B6A16`, onde o
descritor já está montado.

**Ordem no pipeline (N):** o núcleo roda **antes** das análises —
`008AD601 call 0x8B3ED0`, depois `008AD9FA` (`0x8B8E70`), `008ADC52` (`0x8B9E40`),
`008ADF9B` (`0x8BA1B0`), `008AE096` (`0x8BA7B0`), `008AE5EC` (`0x8A1EE0`).

**Rust (etapa J, incrementos 1–2):** `checks/stage_j_core.rs` transcreve F1, F2, F3, F4, o
gate de F5, `0x1220`/`0x11F0`/`0x1250`, o one-pole de §8.2(b) e o produto escalar com a ordem
bit-exata acima. Compila e passa **10 testes**:
`rustc --edition 2021 --test checks/stage_j_core.rs -o stage_j_core_tests && ./stage_j_core_tests`.

`powf`/`logf`/`expf` **não são kernels do dump**: `checks/thunk_map.txt` mostra
`0x1C9AA01 → IAT 0x1D8D818 powf`, `0x1C9A9FB → IAT 0x1D8D808 logf`,
`0x1C9A9D7 → IAT 0x1D8D7F0 expf`, todos em `api-ms-win-crt-math-l1-1-0.dll`. Portanto a
bit-exatidão vem de chamar a **mesma UCRT**: `checks/j_crt_equiv.rs` compara `f32::powf`/
`ln`/`exp`/`mul_add` com os imports em **17.832.179** amostras e dá `bad=0`. Requisito:
compilar para `x86_64-pc-windows-msvc` e rodar na mesma família de UCRT.

### 8.3 Bloco de estado lido pela dinâmica — `ctx+0x2C38` (PROVADO, 2026-11-23 — leitor e escritor)

`0x8B3ED0` carrega `state = *(void **)(ctx + 0x2C38)` cinco vezes e lê campos **float
consecutivos**, o que dá o primeiro mapa de offsets de estado com leitura provada
(`008B3F5C`–`008B3FBA`):

| Offset no objeto | Tipo | Destino | Instruções |
|---:|---|---|---|
| `+0x00` | f32 | `[rbp-0x10]` (→ `xmm7`, §8.2c) | `008B3F82 mov eax,[rax]` / `008B3F84 mov [rbp-0x10],eax` |
| `+0x04` | f32 | `[rsp+0x30]` (→ `xmm9`/`xmm10`, §8.2c) | `008B3FA9` / `008B3FAC` |
| `+0x28` | f32 | `[rbp]` | `008B3F9C` / `008B3F9F` |
| `+0x3C` | f32 | `[rbp+8]` | `008B3FB7` / `008B3FBA` |
| `+0x4C` | f32 | `[rsp+0x40]` | `008B3F8E` / `008B3F91` |
| `+0x52` | u8 | `[rbp+0x4A30]` | `008B3F71 movzx eax,byte [rax+0x52]` / `008B3F75` |

Lidos também por `0x8C1440` (`008C19CF`–`008C1A22`), no mesmo objeto:

| Offset | Tipo | Destino | Instruções |
|---:|---|---|---|
| `+0x2C` | f32 | `[rbp+0xC0]` | `008C19D6 mov eax,[rax+0x2c]` / `008C19D9` |
| `+0x30` | f32 | `[rbp+0xC4]` | `008C19E6` / `008C19E9` |
| `+0x34` | f32 | `[rbp+0xC8]` | `008C19F6` / `008C19F9` |
| `+0x38` | f32 | `[rsp+0x28]` | `008C1A06` / `008C1A09` |
| `+0x1BF` | u8 | `ecx` (flag) | `008C1A14 movzx ecx,byte [rax+0x1bf]` |
| `+0x1C7` | u8 | `edx` (flag) | `008C1A22 movzx edx,byte [rax+0x1c7]` |

São **10 campos lidos** ao todo (6 acima + 4 f32 e 2 u8 por `0x8C1440`).

Os dois últimos formam o **enable por grupo** que `0x8C1440` consulta a cada iteração:
`byte[state + 0x1BF + 8·g]` para `g = 0..4` (`008C1A6E movzx ecx,byte [rax+rcx*8+0x1bf]`,
`008C2ABA` idem), e o estado inicial de `[rbp+0x13E8]` vem de `+0x1BF`/`+0x1C7`
(`008C1A14`, `008C1A22`, `008C1A2D`/`008C1A38`). Os 8 blocos de grupo em `state+0x1B8`
(§8.3.1) têm o byte de enable em `+0x07` de cada bloco.

#### 8.3.1 Quem escreve esses campos — `0x867D80` (PROVADO, 2026-11-23)

O objeto é `state = engine + 0x54` e o **único** escritor dos campos é o setter de parâmetro
`0x867D80` (1.792 B), alcançado pelo thunk `0x862EF0`:

```
00862EF0  mov  rcx, qword ptr [rcx]     ; rcx = [obj+0]
00862EF3  cvtsd2ss xmm2, xmm2           ; valor do host (double) -> f32
00862EF7  jmp  0x867D80
```

`[obj+8] = 0x862EF0` em `00862E90`. Cadeia de posse, toda lida:

| Passo | RVA | Fato |
|---|---|---|
| 1 | `00862E52` `00862E72` | `0x862E40` aloca `0xC1A8` e chama `0x8634A0(rcx=novo, rdx=arg1, r8=arg2)` |
| 2 | `008634CA` / `00864057` | `0x8634A0` faz `r14 = rcx` e devolve `rax = r14` |
| 3 | `00862E7C` `00862ED9` | `0x862E40` grava `[obj+0] = rax` (base do motor) |
| 4 | `0086369D` `008636A5` | `0x8634A0` inicializa o estado: `lea rcx,[r14+0x54]` + `call 0x864070` |
| 5 | `008638CA` `00863905` `00863929` | `lea rdx,[r14+0x54]`; `mov [rsp+0x20],rdx` (5º argumento); `call 0x86A4E0` |
| 6 | `00870941` | `0x86FE90` grava esse ponteiro em `[ctx+0x2C38]` |

Logo `rbx` em `0x867D80` (`00867DA6 mov rbx,rcx`) é a base do motor e **`[rbx+0x54+k]` é
`state+k`**. Store com deslocamento **abaixo** de `0x54` (ex. `00867F07 [rbx+0x50]`,
`00867F4D [rbx+0x4a]`) atinge o subobjeto anterior, não o estado.

Varredura de completude (`tools/scan_state_stores3.py`, todas as funções `.pdata` de
`0x860000`–`0x8F0000`, store sem índice e com base fora da pilha): só `0x867D80` cobre os
seis deslocamentos a partir da base do motor. Os outros acertos foram conferidos e
**rejeitados**: `0x861B60` (`00861D8E [rbx+0x58]`, objeto cujo `+0x00` é um `f64` lido, não o
motor), `0x8634A0` — `00863A5A` grava em `engine+0xB7A8` (16 registros de `0x78`,
`008639F0 lea r12,[r14+0xb7a8]`) e `00863C4E` grava em `engine+0xBF68`
(`00863C0C lea rsi,[r14+0xbf68]`), não no estado — e `0x867600`/`0x867730`
(`[r11+0x58]`/`[rdx+0x58]`), inicialização de um objeto com cabeçalho em `+0x80/+0x84/+0x88`.
**`NÃO PROVADO`:** store por ponteiro derivado (`lea rax,[engine+0x54]` seguido de
`[rax+off]`), que essa varredura por deslocamento não alcança.

**Entrada e despacho (lidos):**

- `xmm8 = clamp(xmm2, 0, 1)` — `00867DC2 comiss xmm2,xmm10` (0.0) e o limite `1.0f` de
  `0x2079F9C` (`00867DE2`, `00867DED`).
- `xmm6 = clamp(callback, min, max)`, com `min = (float)[rdx+0x28]` (`00867D98`, cache em
  `[rsp+0x20]` em `00867E0A`) e `max = (float)[rdx+0x30]` (`00867DBA`, cache em `[rsp+0x28]`
  em `00867DF1`); `callback = call qword ptr [rdx+0x50]` recebe `(double)xmm8` e é
  **NÃO IDENTIFICADO** (`00867DFC mov rax,[rdx+0x50]`, `00867E10 call rax`). Em 2026-11-24
  ficou provado que esse `+0x50` **não** é campo da tabela `0x238E9B0` (lá os 4 valores são
  flags `0/1/0x101/0x10001`); o descritor de runtime é outra estrutura — `checks/p_extras.md`
  §P2. O clamp é o par `comiss`/`cmovae` de `00867E23`–`00867E3C`. Em
  seguida `call 0x1798F8A` = **`roundf`** (`00867E43`) e `cvttss2si r9d` (`00867E57`).
- `r8b = (xmm8 >= 0.5f)` — `0x2079EA8`, `00867E48` / `00867E5C setae`.
- `idx = [rdx]` (`00867E50`); `idx > 0x8E` → epílogo (`00867E60`/`00867E65`); senão
  `sel = byte[0x8683CC+idx]` (`00867E72`) e `alvo = dword[0x868348+sel*4]` (`00867E7B`).
  A tabela de bytes tem **143 entradas** (0..142) e a de alvos, **33**.

**Os 6 campos lidos pela dinâmica:**

| Offset | Tipo | Índice | Handler / store | Valor gravado |
|---:|---:|---:|---|---|
| `+0x00` | f32 | 0 | `0x867F6E` / `00867F73` | `xmm8` |
| `+0x04` | f32 | 5 | `0x867F7B` / `00867F80` | `xmm8` |
| `+0x28` | f32 | 17 | `0x868061` / `00868066` | `xmm8` |
| `+0x3C` | f32 | 18 | `0x86806E` / `00868073` | `xmm8` |
| `+0x4C` | f32 | 92 | `0x8681CD` / `008681E7` | `xmm8 < 0.999` ? `xmm6` : `60.0f` (`0x207A474`; limiar f64 `0.999` em `0x207A120`) |
| `+0x52` | u8 | 16 | `0x868055` / `00868055` | `r8b` |

**Mapa completo índice → offset (PROVADO instrução a instrução).** `s = state`:

| Índices | Handler | Destino | Tipo | Valor |
|---|---|---|---|---|
| 0 | `0x867F6E` | `s+0x00` | f32 | `xmm8` |
| 1 | `0x867E88` | `s+0x57` | u8 | `r8b` |
| 2 | `0x867EC8` | `s+0xB0` | i32 | `min(r9d-1, 7)` |
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
| 19..90 | `0x86807E` | `s+0xB8+0x20·b` (ver abaixo) | — | `b=(i-19)/9`, `r=(i-19)%9` |
| 91 | `0x867F55` | `s+0xAC` | i32 | `min(r9d-1, 7)` |
| 92 | `0x8681CD` | `s+0x4C` | f32 | ver acima |
| 93 | `0x8681F2` | `s+0x40` | f32 | `powf(10, 0.05·xmm6)` = `10^(v/20)` (`00868205`, `0x207A360`=10, `0x2079D88`=0.05) |
| 94 | `0x868219` | `s+0x44` | f32 | `0.01·xmm6` (`0x2079D48`) |
| 95 | `0x868230` | `s+0x48` | f32 | `powf(10, 0.05·xmm6)` |
| 96 | `0x868257` | `s+0x54` | u8 | `r8b` |
| 97 | `0x868263` | `s+0x55` | u8 | `r8b` |
| 98..122 | `0x86826F` | `s+0x1B8+8·g+{0,4,5,6,7}` | f32/u8 | `g=(i-98)/5`, `r=(i-98)%5` |
| 123 | `0x8682F4` | `s+0x2C` | f32 | `xmm8` |
| 124 | `0x868301` | `s+0x30` | f32 | `xmm8` |
| 125 | `0x86830E` | `s+0x34` | f32 | `xmm8` |
| 126 | `0x86831B` | `s+0x38` | f32 | `xmm8` |
| 127..142 | `0x868328` | `s+0x1D+i` → `0x9C..0xAB` | u8 | `r8b` (`0086832A [rax+rbx+0x71]`, `rax=i`) |

Bloco de bandas (19..90) — `base = s+0xB8+0x20·b`, 9 subcampos, `b` de 0 a 7:

| `r` | DV | Tipo | Valor |
|---:|---:|---|---|
| 0 | `+0x00` | u8 | `r8b` (`008680D2`) |
| 1 | `+0x01` | u8 | `r8b` (`008680DF`) |
| 2 | `+0x04` | f32 | `xmm6` — frequência (`008680F0`) |
| 3 | `+0x08` | f32 | `24·xmm8 - 12` (`0x207A3C8`=24, `0x207A384`=12, `008680FC`–`00868121`) |
| 4 | `+0x0C` | f32 | `0x69AE90(xmm6)` = `0` se `x<=0`, senão `2·asinh(1/(2x))/ln2` (`0086812D`) |
| 5 | `+0x10` | f32 | `expf(ln6 + xmm8·(ln128 - ln6))` = `6·(128/6)^t` (`0x207A4C4`=128, `0x207A0D8`=ln 6, IAT `logf`/`expf`) |
| 6 | `+0x14` | f32 | `xmm6` (`00868185`) |
| 7 | `+0x18` | i32 | `r9d` (`0086818E`) |
| 8 | `+0x1C` | i32 | `r9d` (`00868198`) |

Grupos de canal (98..122) — `base = s+0x1B8+8·g`, `g` de 0 a 4: `r=0` → `+0x00` f32 `xmm8`
(`008682EB`); `r=1..4` → `+0x04/+0x05/+0x06/+0x07` u8 `r8b` (`008682DC`, `008682D2`, `008682C8`,
`008682BE`). Isso confere com as leituras `+0x1BF` e `+0x1C7` de `0x8C1440` (§8.3): são o
quinto byte (`link_all`) dos grupos 0 e 1.

**Constantes (lidas com RVA):** `0x2079F9C`=1.0f, `0x2079EA8`=0.5f, `0x207A3C8`=24.0f,
`0x207A384`=12.0f, `0x207A4C4`=128.0f, `0x207A0D8`=1.7917595f (=ln 6), `0x207A120`=f64 0.999,
`0x207A474`=60.0f, `0x2079D88`=0.05f, `0x2079D48`=0.01f, `0x207A360`=10.0f.
**Import (nomes provados pelo diretório de importação em `0x2175044`, ILT `0x2176878`):**
`0x1D8D7E0`=roundf, `0x1D8D7F0`=expf, `0x1D8D808`=logf, `0x1D8D810`=asinh, `0x1D8D818`=powf.

**Espaço de índices == tabela `0x238E9B0` (PROVADO por isomorfismo estrutural).** A tabela de
143 descritores (passo `0x68`, índice em `+0x10`, nome em `+0x14`) tem os mesmos cortes da
tabela de despacho: 0..18 avulsos, **19..90 = 8 blocos de 9**, **91** avulso, **92..97 = 6**,
**98..122 = 5 blocos de 5**, **123..126 = 4**, **127..142 = 16 avulsos** (nomes
`Channel 1..16 enabled`). O handler de 127..142 escreve exatamente 16 bytes consecutivos
(`0x9C..0xAB`) e o de 98..122 usa passo 8 sobre 5 grupos. Logo o índice é o mesmo campo
`+0x10` da tabela.

**`NÃO PROVADO`:** (a) o significado DSP de cada campo (só `+0x00`/`+0x04` têm uso provado,
§8.2c); (b) a identidade do callback `[rdx+0x50]` (normalização valor↔unidade); (c) que o
host entregue o índice da tabela `0x238E9B0` a este mesmo setter. Os nomes de
`docs/engine/params.csv` são os da tabela `0x238E9B0` (mesmo campo `+0x14`), não inferência.

Artefato reproduzível: `tools/param_map.py` → `checks/param_map.txt` (143 linhas, com
`[0x238E9B0+i*0x68+0x10] == i` verificado para todo `i`).

---

### 8.4 `0x8C1440` — estagiador por grupo + mistura final (PROVADO estrutural, 2026-11-23)

Desmontagem completa: `checks/8c1440.u8.dis` (1.787 linhas, 7.800 B, 58 `call`). É o maior
consumidor dos 10 campos de §8.3 e o estágio imediatamente antes da aplicação de ganho.

#### 8.4.1 Assinatura e argumentos (PROVADO)

```c
void f8C1440(engine *e /*rcx*/, track *t /*rdx*/, arena *ar /*r8*/, void *r9_unused);
```

Prova da convenção de pilha: `008C1440`–`008C145F` salvam `rcx`/`rdx`/`r8`/`r9` nos *home
slots*; com `push rbp/rbx/rsi` + `lea rbp,[rsp-0x13b0]` + `sub rsp,0x14B0` (`008C145A`), os
slots caem em `rbp+0x13D0` (rcx), `+0x13D8` (rdx), `+0x13E0` (r8), `+0x13E8` (r9). Os mesmos
endereços são relidos: `008C19C8 mov r8,[rbp+0x13d0]`, `008C232D mov rsi,[rbp+0x13d8]`,
`008C2F93 mov rdi,[rbp+0x13d8]` e `008C3226 mov rcx,[rbp+0x13e0]`.

| Campo | Tipo | Uso provado (RVA) |
|---|---|---|
| `t+0x400` | i32 | `<= 2` ⇒ **retorno imediato** (`008C1467 cmp`,`008C1474 jle 0x8C32AD`) |
| `t+0x404` | i32 | **`n`**, comprimento de todo buffer e `n` de todo `call` IPP (`008C14B0`; refeito em `008C1582`, `008C15FB`, `008C167A`, `008C16F3`) |
| `t+0x000` | `float**` | tabela de ponteiros de buffer, indexada por `rec->first_buf` (`008C1E4B mov rax,[r13+8]` + `008C1E61 mov rdi,[rsi+rax*8]`) |
| `e+0x2C38` | ptr → state | §8.3 (`008C19CF`) |
| `e+0x010` | ptr → `{rec* begin; rec* end;}` | `008C1A77 mov rax,[r8+0x10]`, `008C1A8C mov r13,[rax]`, `008C1A97 mov r8,[rax+8]` |
| `ar+0x000` | `float*` base | `008C1506`, `008C1553`, `008C15A0` |
| `ar+0x018` | i32 cursor | `008C147A mov eax,[r8+0x18]`; **restaurado** no fim (`008C3226 mov rcx,[rbp+0x13e0]`, `008C322D mov eax,[rbp+0xe0]`, `008C32AA mov [rcx+0x18],eax`) |

#### 8.4.2 Arena: `0x8CAFD0` é o alocador de bump (PROVADO)

`0x8CAFD0(arena /*rcx*/, desc /*rdx*/)`, corpo `008CAFD0`–`008CB03E`:

```
desc->p0 = arena->base + arena->fill * 4;
arena->fill += align16(desc->n);          // 008CAFE5..008CB003 (and 0xf / +0x10 / cmove)
desc->p1 = arena->base + arena->fill * 4;
arena->fill += align16(desc->n);          // 008CB019..008CB03A
```

`desc` = `{float *p0@0; float *p1@8; int n@0x10; int bytes4n@0x14}`. Não retorna valor.
As **3** chamadas em `0x8C1440` (`008C179A`, `008C17BE`, `008C17E2`) produzem 6 buffers.

#### 8.4.3 Os 16 buffers de trabalho (papéis PROVADOS em 2026-11-25; ver `q_8c1440_buffers.md`)

| Par | `float*` (local) | `n` em | Origem |
|---:|---|---|---|
| 0 | `[rbp+0x00]` / `[rbp+0x08]` | `[rbp+0x10]` | bump inline `008C150F`/`008C155D` |
| 1 | `[rbp+0x40]` / `[rbp+0x48]` | `[rbp+0x50]` | `008C15A7`/`008C15D6` |
| 2 | `[rbp+0xa0]` / `[rbp+0xa8]` | `[rbp+0xb0]` | `008C161E`/`008C1656` |
| 3 | `[rbp+0x60]` / `[rbp+0x68]` | `[rbp+0x70]` | `008C169B`/`008C16D2` |
| 4 | `[rbp+0x80]` / `[rbp+0x88]` | `[rbp+0x90]` | `008C171A`/`008C1754` |
| 5 | `[rbp-0x20]` / `[rbp-0x18]` | `[rbp-0x10]` | `0x8CAFD0` `008C179A` |
| 6 | `[rbp+0x20]` / `[rbp+0x28]` | `[rbp+0x30]` | `0x8CAFD0` `008C17BE` |
| 7 | `[rbp-0x40]` / `[rbp-0x38]` | `[rbp-0x30]` | `0x8CAFD0` `008C17E2` |

**Correção 2026-11-25:** são **8 sítios estáticos** de `0x10D0` (`008C1808`, `1838`, `187A`,
`18BB`, `18FB`, `193A`, `197A`, `19BA`), cada um dentro de um laço de **2 iterações**
(`cmp rbx,2`/`jl`) — 8 × 2 = 16 buffers. (Não são 16 `call` estáticos; a versão anterior
desta linha contava as iterações.)

**Papéis (PROVADOS, `checks/q_8c1440_buffers.md`):** pares 0/2/4/6 acumulam `Σ_ch ch²`
(`0x1580` com `a = b = canais`, `dst = par`); pares 1/3/5/7 acumulam `Σ_ch ch`
(`0x1370`, `src = canais`, `dst = par`) e são os **únicos clampados** (`0x1100` modo max,
`bound = 1e-7`, `008C2393`/`23CD`/`240D`/`244D`) — conjunto denominador. A acumulação é
**filtrada pelo predicado** de §8.4.5 (não é "todo registro"), e o par escolhido depende de
`(enable, tipo, al, flag)` — tabela em §8.4.6.

As quatro divisões `0x1550` escrevem cada uma em **uma alocação nova** (`new1/T1/T2/T3`) e
guardam o descritor no slot do par que serviu de numerador: `new1 = par0/par1` (`008C2545`,
slot `[rbp-0x40]` em `008C250E`), `T1 = par2/par3` (`008C263D`, slot `[rbp+0xa0]`),
`T2 = par4/par5` (`008C273B`, slot `[rbp+0x80]`), `T3 = par6/par7` (`008C2828`, slot
`[rbp+0x20]`). O par 7 **não** é destino: o `den` da divisão 4 é o descritor do par 7
capturado em `xmm11` (`008C241B`) antes do reaproveitamento do slot. **Aliasing de slots:**
`008C24BD`, `008C250E`, `008C2607`, `008C2703` e `008C27F7`; quem lê o slot depois desses
RVAs lê o novo descritor.

As somas `A/B/C/D` (`008C298E`, `008C29CE`, `008C2A0E`, `008C2A4E`) acumulam os **dois
canais** de `new1/T1/T2/T3` e alimentam o caminho mono da passagem B (§8.4.7).

#### 8.4.4 Tabela de grupos e registros (PROVADO)

`0x2014360` = `{8, 9, 10, 6, 5}` (i32×5; `008C1A4D`, `008C2356`, `008C2AA5`), indexada pelo
contador de grupo; o laço é `5` iterações (`008C234D cmp rax,5` / `008C321C cmp rax,5`).
Logo `type[g] = {8,9,10,6,5}[g]`, e o enable é `state[0x1BF+8g]`.

Registro de banda (`e+0x10` → vetor), stride **0x18** (`008C1E09`, `008C2DFD`, `008C31ED`):

| Offset | Tipo | Uso provado |
|---:|---|---|
| `+0x00` | i32 `sel` | discriminante do predicado (`008C1AB0`, `008C1EE4`, `008C2AF0`, `008C2E24`) |
| `+0x08` | i32 `first_buf` | índice em `t->buffers[]` (`008C1BD3 movsxd rax,[r13+8]`, `008C2C11`) |
| `+0x10` | i32 `nch` | `== 2` ⇒ caminho estéreo (`008C1B74`, `008C1F88`, `008C2F88`); `== 1` ⇒ mono (`008C1D39`, `008C1E1C`) |

#### 8.4.5 Predicado `0x61B790(sel, val)` (PROVADO por inteiro)

`bool 0x61B790(int sel /*ecx*/, int val /*edx*/)` — `0061B790`–`0061B85C`:

| `sel` | retorno |
|---:|---|
| 0 | `1` (`0061B79C`) |
| 1 | `val != 10` (`0061B7A9`) |
| 2 | `val != 9` (`0061B7BA`) |
| 3 | `(unsigned)(val-9) > 1` (`0061B7CB`–`0061B7D1 seta`) |
| 4 | `(unsigned)(val-8) > 2` (`0061B7F3`–`0061B7F9 seta`) |
| 5 | `(unsigned)(val-0x10) <= 2` (`0061B7DF`–`0061B7E5 setbe`) |
| 6 | `h(4,val) && !h(5,val)` (`0061B80C`, `0061B81C`, retornos em `0061B825`/`0061B833`) |
| 7 | `(unsigned)(val-8) <= 1` (`0061B843`–`0061B849 setbe`) |
| outro | `sel == val` (`0061B852 sete`) |

`0x8C1440` chama `0x61B790` **8× diretamente**, sempre com `sel = 4` e `sel = 5`
(`lea ecx,[r14-2]` / `lea ecx,[r14-1]` dentro do ramo `type == 6`): `008C1B2F`, `008C1B43`,
`008C1F9E`, `008C1FB2`, `008C2B6A`, `008C2B7D`, `008C2ED3`, `008C2EE6`. O resto é
**inlinado** 4× (`008C1AB4`–`008C1B6E`, `008C1EE4`–`008C1FF9`, `008C2AF4`–`008C2BA8`,
`008C2E24`–`008C2F29`). As cópias inline reproduzem a tabela acima para
`sel` 1/2/3/4/5/7/default.

**Composição (PROVADA em 2026-11-25):** com `tipo = {8,9,10,6,5}[g]`, um registro participa
se

```
tipo == 0            -> 1
tipo == 1            -> sel != 0xA
tipo == 2            -> sel != 9
tipo == 3            -> sel ∉ {9, 0xA}
tipo == 4            -> sel ∉ {8, 9, 0xA}
tipo == 5            -> sel ∈ {0x10, 0x11, 0x12}
tipo == 6            -> h(4,sel) && !h(5,sel)
tipo == 7            -> sel ∈ {8, 9}
tipo ∈ {8,9,0xA}     -> sel == tipo
```

Prova: `008C1AB0`–`008C1B6E` (ramo `enable != 0` da passagem A), `008C1EE4`–`008C1F43`
(ramo `enable == 0` da passagem A), `008C2AF4`–`008C2BA8` e `008C2E24`–`008C2F29` (passagem
B). Para `tipo == 0xA` o teste adicional `008C1F19 lea rax,[r14-8]; cmp rax,1; ja 0x8c1f38`
(`008C1FDB`–`008C1FF1`, `008C2F19`–`008C2F27`) força `al = 0`, e como `tipo != 5,6` o
registro é descartado (`008C2311`/`008C31ED`). `NÃO PROVADO`: a **intenção** dos tipos
(nome de cada `sel`); a tabela é o que o binário executa.

#### 8.4.6 Esqueleto de controle (PROVADO)

1. **Setup** `008C1467`–`008C19C6`: early-return, `mark = ar->fill`, `n = t->404`,
   alocação e zeroização dos 16 buffers.
2. **Leitura do estado** `008C19CF`–`008C1A38` (§8.3): `q0=+0x2C`, `q1=+0x30`, `q2=+0x34`,
   `q3=+0x38` para `[rbp+0xC0]`/`[rbp+0xC4]`/`[rbp+0xC8]`/`[rsp+0x28]`; flag
   `[rbp+0x13E8] = (state[0x1BF]==0 && state[0x1C7]==0)`.
3. **Passagem A** `008C1A58`–`008C1E17`: por grupo `g` (5) e por registro que passa no
   predicado (§8.4.5), acumula `Σch²` (`0x1580`, `008C1D28`/`008C1D4E`/`008C1E81`) e `Σch`
   (`0x1370`, `008C1DF0`/`008C1E3B`/`008C1EAB`) no par que depende de `(enable, tipo, al,
   flag)`:
   - `enable != 0` ⇒ par 0/1;
   - `enable == 0`: `tipo 8/9 && al && flag` ⇒ par 2/3; `tipo 6 && !al` ⇒ par 4/5;
     `tipo 5 && sel ∈ {0x10,0x11,0x12}` ⇒ par 6/7; `tipo 0xA` ⇒ nada.
4. **Guarda de divisão** `008C2367`–`008C2459`: `0x1100` (clamp, `mode=0` ⇒ `max`) com
   `bound = 1.00000001e-07f` (`0x2079CEC`) nos 4 pares ímpares = 8 buffers.
5. **Normalização** `008C245B`–`008C2A5A`: 4 `0x1550` (`dst = num/den`, `008C2545`,
   `008C263D`, `008C273B`, `008C2828`) em alocações novas, e 4 somas de canal
   `0x1370` (`008C298E`, `008C29CE`, `008C2A0E`, `008C2A4E`) produzindo `A/B/C/D`.
6. **Passagem B** `008C2AA5`–`008C31FA`: repete a varredura de 5 grupos e aplica a lei de
   mistura (§8.4.7), grupo a grupo, registro a registro.
7. **Fim** `008C31FA`–`008C32B7`: `ar->fill = mark` (`008C32AA`).

#### 8.4.7 Lei de mistura (PROVADO; corrigido em 2026-11-25)

`dst` = **buffers de canal do registro** (a cópia `[rbp+0x6b0]` aponta para
`t->buffers[first_buf..]`), `src` = **resultado da divisão** (`new1`/`T1`/`T2`/`T3`), `g` =
coeficiente daquele caso:

```
0x1220(dst, n, 1.0f - g)              ; calls 008C2CE9 / 008C30C9
0x11F0(dst, src, n, g)                ; calls 008C2DA7 / 008C3196
```

⇒ **`ch ← (1−g)·ch + g·D`** por canal, com `D = Σregistros ch² / Σregistros ch` (média
ponderada por potência dos registros empilhados no grupo). Para 1 registro, `D = ch` e a
mistura é identidade.

`0x1220` é `vmulps` (`00006220`): `dst *= (1−g)` com **um** arredondamento. `0x11F0` é MAC
**com FMA** (`00005C46 vfmadd213ss`, `00005C85 vfmadd213ps`): `dst = src·g + dst` com um
arredondamento. O port (`pipe::mix_lane`) usa `*d *= a` e `s.mul_add(b, *d)`; a forma
`dst + src*g` com dois arredondamentos divergiria no ULP.

Roteamento (tabela completa em `checks/q_8c1440_buffers.md` §4):

| Caso | `src` | `g` |
|---|---|---|
| `enable != 0` | `new1` = par0/par1 | `state+0x2C` (`008C2CC4`/`008C2DA3`) |
| `enable == 0`, `al != 0`, flag | `T1` = par2/par3 | `state+0x30` (`008C2F3F`) |
| `enable == 0`, `tipo == 6` | `T2` = par4/par5 | `state+0x34` (`008C2F50`) |
| `enable == 0`, `tipo == 5` (`sel ∈ {0x10,0x11,0x12}`) | `T3` = par6/par7 | `state+0x38` (`008C2E9B`) |
| `enable == 0`, `tipo == 0xA` | não mistura | — |

No caminho `nch == 2` (`008C2D79`/`008C2F88`) o laço por canal usa `g` **inteiro**
(`008C2D90..008C2DB4`, `008C3180..008C31A3`). No caminho `nch != 2`
(`008C2DB8`/`008C31A7`) o `src` é a soma `A/B/C/D` (`A` = `[rbp-0x80]`, `B` = `[rbp+0x1c0]`,
`C` = `[rbp]`, `D` = `[rbp+0x40]`) e o coeficiente é `g·0,5` (`008C2DEA mulss xmm1,xmm11`,
`008C31D5`, `xmm11 = 0,5f` em `008C2A67`, constante `0x2079EA8`):

```
ch ← (1−g)·ch + (g/2)·Soma_canais(D)
```

> **Correção 2026-11-24 (etapa J3), mantida.** A versão anterior dizia "`g/2` no ramo
> estéreo", o que está **invertido**: o `0,5` está no ramo `nch != 2`. O portão
> `cmp edi,2` (`008C2D79`/`008C3169`) é **redundante**: `edi = [rbp+0x6A0]` é a contagem de
> ponteiros do descritor local, fixada em `2` (`008C2C0B`/`008C2FE4`) porque esse bloco só
> roda no ramo `nch == 2` (`008C2BAE`/`008C2F88`); logo a condição é sempre verdadeira e não
> decide coeficiente nenhum.

> **Correção 2026-11-25.** A versão anterior identificava o `src` como "buffer estagiado do
> grupo": o buffer estagiado é o **`dst`** (os canais); o `src` é o resultado da divisão.

Constantes usadas: `1.0f` `0x2079F9C`, `0.5f` `0x2079EA8`, `1.00000001e-07f` `0x2079CEC`,
tabela `0x2014360`. Nenhuma outra constante em `.rdata` é referenciada
(`008C1A4D`, `008C2356`, `008C2367`, `008C2A5C`, `008C2A67`, `008C2AA5`).

#### 8.4.8 Papéis e coeficientes — FECHADO em 2026-11-25

`checks/q_8c1440_buffers.md` fecha, com instrução + RVA:

- o papel dos 16 buffers (§8.4.3): pares pares = `Σ_ch ch²`; ímpares = `Σ_ch ch` e conjunto
  clampado/denominador; as quatro divisões com `dst`/`num`/`den` por RVA, **em alocações
  novas** (`new1/T1/T2/T3`), não no par 7;
- o **mapa grupo → coeficiente** (§4 do doc): `enable != 0` ⇒ `+0x2C`; desabilitado,
  `tipo 8/9` ⇒ `+0x30` (exige flag), `tipo 6` ⇒ `+0x34`, `tipo 5` (`sel ∈ {0x10..0x12}`) ⇒
  `+0x38`, `tipo 0xA` ⇒ sem mistura. A escolha é condicional (`enable`, `al`, flag
  `[rbp+0x13E8]`, `tipo`), não por índice de tabela;
- a composição do predicado de participação (§8.4.5) e o descarte do `tipo 0xA`;
- o encadeamento `008C296B`–`008C2A5A`: `A/B/C/D` = soma dos 2 canais de `new1/T1/T2/T3`,
  consumida só no caminho mono com `g/2`;
- a hipótese "um dos 16 buffers recebe a curva de `0x882FC0`" está **refutada** (0
  ocorrências); a curva é aplicada em `0x8B3ED0` (§8.2(e)/(f)).

**Continua `NÃO PROVADO`:** nome/unidade dos 4 coeficientes `+0x2C/+0x30/+0x34/+0x38`; a
faixa válida de `g` (o código calcula `1−g` sem clamp; depende do escritor de `+0x2C..+0x38`);
a **intenção musical** da média ponderada por potência; `nch > 2` (o ramo `008C1E4B` usa só
`track->buffers[first_buf]`, sem laço para os demais canais).

**Port (2026-11-25):** `port/src/stage.rs` transcreve o estágio inteiro — passagem A
(`0x1580` com FMA para `Σch²`, `0x1370` para `Σch`), clamp `0x1100` modo 0 nos pares
ímpares, as 4 divisões, as somas `A/B/C/D` e a passagem B via `pipe::mix_lane` (MAC com FMA,
`00005C85`) — com 12 testes (`count <= 2`, identidade, média ponderada, clamp, roteamento
por `(enable, tipo, sel)`, mono com `g/2`, `tipo 5` só em `sel 16..18`, `tipo 0xA` nunca).
A divisão `0x1550` → `0x63640` **não** é um único "vrcpps + Newton". O despacho depende de
`n` e do alinhamento de `dst` (cabeça 8 em `00063697`, laço 16 em `00063A67` sobre `n − h`,
bloco 8 em `0006400D`, resto 1..7 em `0006401A`) e há **duas aritméticas**: o laço de 16
refina o **recíproco** (`00063B24`/`00063B29`) e multiplica no fim (`00063B37`); as demais
rotas refinam o **quociente** (`00063791`/`00063796`). A máscara do recíproco nulo também
difere: A usa `vcmpneq_oqps`+`vandps` (`00063779`/`0006377E`), B usa `vcmpeqps`+`vandnps`
(`00063AF8`/`00063B0E`); `vrcpps(|x| ≳ 2^126) = 0` ⇒ quociente `0·num`.

**M1 (2026-11-25, PROVADO com resíduo):** `port/src/div.rs` transcreve `0x63640` e o estágio
o usa nas 4 divisões (`div_block_mod32(num, den, dst, 0)`); conferido contra a sequência
AVX/FMA do binário em `checks/j_div_avx.rs` (2.807.920 lanes, `bad = 0`). No estágio
`n = [X+0x40] = 257` para `a = 48000` (`N = trunc(max(a/k,44100)·(1/44100))·256`,
`0086FF35`/`0086FF39`, `arg5 = 0x100` em `0086A579`) ⇒ 16 laços B + 1 lane A. `dst & 0x1c = 0`
nos 4 sítios: cursor sempre `align16` dentro de `0x8C1440` e base `[E+0x30]` de `0x868B50`
(64 B, `00868B98`/`00868B9C`) ⇒ a cabeça não roda. `NÃO PROVADO`: o `E` de `0x864410` ser o
objeto de `0x8634A0`; `a` = taxa de amostragem; o caminho do gêmeo `0x8C5C40`; sinal/payload
de NaN; `vrcpps` é bit a bit só na mesma CPU do oráculo. Prova em
`checks/r_divisao_63640.md` §2/§4.1/§5/§6.

#### 8.4.9 Camada de descritores e ordem da cadeia — etapa J3 (PROVADO)

`checks/stage_j_pipe.rs` transcreve as estruturas provadas e passa **12 testes**
(`rustc --edition 2021 --test checks\stage_j_pipe.rs`).

| Estrutura | Bytes | Layout provado (RVA) |
|---|---:|---|
| descritor de arrays | `0x410` | `+0x000 void*[128]`; `+0x400 i32 count` (`008AD32A`); `+0x404 i32 len` (`008AD330`); `+0x408 i64 len*4` (`008AD337`) |
| par do estagiador | `0x18` | `{p0@0, p1@8, n@0x10, 4n@0x14}` (`008CAFE2`, `008CB015`, `008CAFDA`) |
| descritor de ring | `0x90` | `plane@0` (`00868930`), `write@0x80` (`008AD26C`), `read@0x84` (`008ACCF7`), `len@0x88` = `0x10000` (`008688CC`/`00870790`), `nch@0x8C` (`008688D4`); `+0x08..+0x7F` = `NÃO EXTRAÍDO` (`0x868840`) |

Alocação bump: `cursor += align16(len)` em floats no descritor
(`008C34FC`..`008C3524`) e duas vezes no par (`008CAFE5`..`008CB03A`); `align16(x)` é
`(x & ~0xF) + 0x10` quando `x & 0xF != 0` (`008C3510`..`008C351D`).

Ring: `avail = (write − read) & (len−1)` (`008ACC5D`..`008ACC82`); avanço
`i = (i + n) & (len−1)` (`008ACD06`..`008ACD0E`, `008AD26C`..`008AD280`).
`checks/stage_j_chan.rs` (J5, **7 testes**) transcreve os três descritores contíguos
(`out@0`/`A@0x90`/`B@0x120`), `len = 0x10000`, `available`/`advance_read`/`advance_write`,
`overlap_gain(n,m) = n/m`, `zero_planes` (`0x8BAA10`) e o FMA `0x8BAB60`
(`dst[i] += src[i]·gain`, `00005C46 vfmadd213ss`). `NÃO EXTRAÍDO` em J5: `+0x08..+0x7F` do
ring (`0x868840`), a atribuição da lista de `0x86F170` a A/B e o plano `nch > 1`.

Ordem da cadeia de `0x8AD2B0` (25 estágios; `checks/n_canal.md` §1.3): `byte[state+0x58]`
escolhe `0x8B8E70` vs `0x8B9E40` (`008AD76B`/`008AD7A1`); `byte[state+0x52]` liga
`0x8BA7B0` e `0x8A1EE0` (`008ADFAB`, `008AE56F`); o atalho
`!byte[X+0x59] && !byte[state+0x51] && contagens iguais` (`008ADC6B`..`008ADC82`) salta de
`008ADC8C` para `008AE1C1` e pula os estágios 8–19. `chain_plan` devolve essa sequência.

Mistura (`0x8C1440`): `g = f32[state+0x2C]` (`008C19D9`), `1,0` em `008C2A5C`
(`0x2079F9C`); coeficientes por `nch` em §8.4.7 (corrigida em J3).

`NÃO PROVADO` em J3: semântica das funções dos estágios 8–11, 15, 18, 19, 22–25 (só
sítio/assinatura); papel dos 16 buffers (§8.4.8); portão `cmp edi,2` da mistura (§8.4.7);
quem grava `+0x14` do par do estagiador — paradas `008B6A16`, `0x8C1440`, `008C2D79`,
`008CAFDA`.

**PRÓXIMO:** null-test plugin × port (mesmo bloco, alinhamento 2304). J1–J6 já estão em Rust:
J1/J2 (`stage_j_core.rs`, 10 testes), J3 (`stage_j_pipe.rs`, 12), J4 (`j4_fft.rs`, 13 —
ordens 8..19 e split `0x895C0` rápido/lento), J5 (`stage_j_chan.rs`, 7 — ring/ganho) e J6
(`stage_j_engine.rs`, 8 — detector, smoother, curvas, escalar `u·(y·v)`). Os pontos acima entram
no código Rust como `// NÃO EXTRAÍDO: <RVA>` — nunca como aproximação.

--- 

## 9. Camada vetorial — primitivas resolvidas por opcode (2026-11-22)

Detalhe completo no plano, §17. Aqui só o que muda para o port.

As chamadas `FUN_1800010xx/11xx/12xx/13xx/15xx` do núcleo **não** são caixas-pretas:
são as primitivas de vetor da IPP, com índice de dispatch em `0x21C7408` (= 4) e tabela
própria. A operação vem do opcode; o sentido (in-place ou fora-do-lugar) vem do
registrador de destino do `store`.

### 9.1 As quatro usadas por `0x879CF0`

| Thunk | Semântica provada | Prova |
|---|---|---|
| `0x1310` | `out[i] = in[i] + s` — **fora do lugar** | `0x9640 vaddss` lê `[rcx]`; `0x9646 vmovss` grava `[rdx]`; `0x95AA mov rdx,r8` |
| `0x1220` | `a[i] *= s` — in place | `0x6200 vmulss`; `0x6205` grava em `[rdx]` |
| `0x12E0` | `a[i] += s` — in place | `0x9020 vaddss`; `0x9025` grava em `[rcx]` |
| `0x1100` | clamp escalar: arg4 `==4` → `min`; `==0` → `max` | `0x3495 test r9d,r9d; je 0x35D9` (max); `0x349E cmp r9d,4; je 0x34AA` (min) |

O `0x1100` tem **dois modos** escolhidos pelo 4º argumento inteiro. Ler a assinatura
sem ler o opcode faz parecer "fill" — era o erro do §16.4.

### 9.2 `0x879CF0` com a semântica real — e a hipótese de "bandas" caiu

```c
// 80879CF0.c:181   out = in + eps                        (0x1310)
// 80879CF0.c:194   dVar2 = 1.0 / max(param_3, eps)
// 80879CF0.c:218   out *= dVar2                          (0x1220)
// 80879CF0.c:244   dVar1 = pow(2.0, 1.0/(param_4/param_5))
// 80879CF0.c:250   out = min(out, dVar1*param_3)         (0x1100 modo 4)
// 80879CF0.c:280   out = pow(out, param_4/param_5)       (0x277C00)
// 80879CF0.c:311   out += 1.0f                           (0x12E0)
// 80879CF0.c:341   out = 1.0f / out                      (0x29B260, vrcpps)
// 80879CF0.c:371   out = max(out, 0.0f)                  (0x1100 modo 0)
// 80879CF0.c:376   param_5 *= 0.166666672f               (1/6, 0x2079DE0)
// 80879CF0.c:402   out = pow(out, param_5)
// 80879CF0.c:431   out = min(out, 1.0f)                  (0x1100 modo 4)
```

**Valores reais nos dois chamadores (`0x87BB60`):** `param_3` = `250.0f`
(`0x207A514`) na 1ª chamada (`0x87CA0E`) e `1000.0f` (`0x207A590`) na 2ª
(`0x87CBF9`); `param_4 == param_5 == 2.0f` (`0x207A188`, via `xmm15`) nas duas.
Logo `param_4/param_5 = 1.0`, o `pow` de base 2 vale 2 e `pow(x,1) = x`.

Com `eps = 1.1920929e-07` (`0x2079CF0`, FLT_EPSILON), a curva efetiva é:

```
y = min( ( 1 / (x/a + 1) )^(1/3) , 1 )        a = 250 ou 1000
```

**Precisão para o alvo bit-exact:** `0x277C00` despacha por comparação exata do bit
pattern do expoente (`0x277F56`). `1.0f` → `0x27C177`, que é **cópia pura**
(`0x27C260`/`0x27C280`): identidade bit-exata, então o `^1` do meio pode ser omitido.
Já `0.3333333432674408f` (`0x3EAAAAAB`) **não** está na tabela e cai no caminho geral
(`0x278006`), que não é `cbrtf` — o port precisa reproduzir esse caminho.

**A leitura anterior ("série geométrica de bandas / divisor de oitava") está errada
para estes chamadores** e fica retirada. O que sobrou de não provado: o que são as
arrays de entrada e onde a curva é usada no pipeline.


### 9.3 Primitivas que o núcleo usa (45 chamadas em `0x8B3ED0`)

`0x1340` ×13 e `0x1220` ×7 (multiplicação por escalar), `0x1100` ×9 e `0x1250` ×3
(clamp), `0x1190` ×2 (multiplicação), `0x1400` ×3 (**produto escalar**, impl `0x5F5C0`),
`0x1430` ×2 e `0x1550` ×2 (**recíproco**, impl `0x63640` = `vrcpps` + Newton),
`0x1580` ×2 (**MAC `dst += src1*src2`**, impl `0xCCE0` → `0x65EA0` → `0x6CE80`; a leitura antiga "soma" estava ERRADA — ver §11.2), `0x1160` ×1 (subtração), `0x1010` ×1
(dispatcher de struct).

Tabela completa: `checks/vector_primitives.txt`; cruzamento com o núcleo:
`checks/core_vector_calls.txt`.

---

## 10. `0x8B2C30` — FIR de 32 taps, coeficientes por bloco (PROVADO, 2026-11-22)

Primeiro kernel de filtro fechado. Desmontagem: `checks/8b2c30.dis` (301 linhas,
chain-aware `0x8B2C30–0x8B30BB`, 1.163 B). Chamador: `checks/8b2680.dis`.

### 10.1 Assinatura e operação

```
float fir32_scatter(Fir32* S, float x, const float* K)     // rcx, xmm1, r8
```

```
y = x*K[0] + S->buf[p];        // 008B2C62 mulss ; 008B2C7C addss
S->buf[p] = 0;                 // 008B2C81
for (j = 1; j <= 31-p; ++j)
    S->buf[p+j] += x*K[j];     // 008B2CD0..008B2E7E
if (p != 0)
    for (j = 0; j < p; ++j)
        S->buf[j] += x*K[32-p+j];   // 008B2EE0..008B308D
S->pos = (p+1) & 31;           // 008B30A6 / 008B30AD
return y;
```

Equivale a `y[n] = Σ_{m=0..31} K^{(n-m)}[m]·x[n-m]` — FIR de 32 taps com coeficientes
variantes no tempo, implementado como scatter-add num anel de 32 somas parciais. **Sem
`subss`** em toda a função (`scan_region.py`), logo não é média móvel nem delay.

### 10.2 Estruturas (offsets provados)

| Offset | Tipo | Evidência |
|---|---|---|
| `S+0x00` | `f32 buf[32]` | `[rcx+rax*4]` em `008B2C7C`, `008B2C81`, `008B2E1A`, `008B2E3A` |
| `S+0x80` | `u64 pos` | store `(p+1)&0x1f` em `008B30AD`; loads em `008B2C40`/`008B2C85` |

Contexto de banda (alocado com `0x240` B e zerado em `0x8817D0`: `call 0x1797578` com
`ecx=0x240`, `call 0x1798F42(ptr,0,0x240)`):

| Offset | Conteúdo | Evidência |
|---|---|---|
| `+0x40` | `f32 K[32]` — coeficientes | `lea r8,[rcx+0x40]` `008B2690`; escrita em `00880419` (`0x10A0`, `r8d=0x20`) |
| `+0xC0` | `f32*` anel de entrada | `008B26B4`, `008B2BE3` |
| `+0xD8` | `f32*` anel de overlap-add | `008B26BB`, `008B2AB7` |
| `+0x140` | `u64` contador de amostra | `008B2680` linhas 12/18 |
| `+0x148` | `u64` máscara do anel | `008B2AAA`, `008B2B73`; 0 no construtor `0088189D` |
| `+0x188` | `Fir32` acima | `add rcx,0x188` `008B269D` |

### 10.3 Constantes

| Valor | RVA | Uso |
|---|---|---|
| `31` (`0x1F`) | imediato `008B2C67` / `008B30A6` | máscara/tamanho do anel |
| `1.0f` | `0x2079F9C` | `1.0f/n` em `008B272F`–`008B2929` |

Sem literais float próprios: os 32 coeficientes vêm de `ctx+0x40`.

### 10.4 Quem alimenta `K` — FECHADO (2026-11-23): `K = δ0`, constante, sem aritmética

Entrada real: `0x880390` (`.pdata` 272 B); o fragmento começa em `0x8803CE`. A cópia de
32 dwords para `ctx+0x40` está provada em `checks` (reverificada instrução por instrução):

```
00880400  mov  rax, [r8]          ; *arg1 -> índice do ctx
00880403  mov  r8d, 0x20          ; len = 32 dwords
00880409  mov  r14, [rdx+rax]     ; ctx da banda
0088040D  mov  rax, [rdx+r9]      ; [arg2] -> ponteiro de origem
00880411  mov  rcx, rax           ; src
00880419  lea  rdx, [r14+0x40]    ; dst = ctx+0x40
0088041D  call 0x10A0             ; thunk -> 0x2C80
```

`0x10A0` resolve por `dispatch.py`: `idx@0x21C7408=4`, `tab=0x21C5E08`, `entry=0x199B2C80`,
**RVA `0x2C80`**. O impl `0x2C80` prova que é cópia de bytes: `00002D25 shl r8d,2`,
`00002D29 call 0x26540` (que por sua vez chama `0x1D2EB40` ou `0x699C0` conforme o tamanho).
Ou seja: `memcpy(dst=ctx+0x40, src, 32*4=128 bytes)`.

**Ordem dos argumentos de `0x10A0` — PROVADA (corrige a convenção):** `0x2C80` repassa sem
reordenar (`0x26540` também não reordena). O laço de cópia em `0x1D2EB40` **carrega de
`rcx` e grava em `rdx`**: `01D2EB42 mov rdi,rcx` / `01D2EB45 mov rsi,rdx` /
`01D2EB67 vmovdqu ymm0,[rdi]` / `01D2EB81 vmovdqu [rsi],ymm0` / `01D2EB4B mov rax,rsi`
(retorno = `rdx`). Portanto a convenção é **IPP, fonte primeiro**: `0x10A0(src=rcx,
dst=rdx, len=r8d)`. Em `00880411` `rcx=table[i]` é a **fonte** e `00880419` `rdx=ctx+0x40`
é o **destino** — a conclusão anterior (`ctx+0x40` recebe) continua, mas o mapeamento
`rcx=dst` que circulou em leituras antigas está **errado**.

**Dois sítios de chamada**, ambos dentro de `0x873440` (confirmado por `xref_scan.py` e pela
desmontagem):

```
008740F6  lea rcx, [rdi+0x2BD8]   ; arg1
008740FD  lea rdx, [rbp+0x10B0]   ; arg2
00874107  call 0x880390

00874176  lea rcx, [rdi+0x2BF0]   ; arg1
0087417D  lea rdx, [rbp-0x20]     ; arg2
00874184  call 0x880390
```

Ambos os structs de origem são cópias de `0x80 B` a partir de `[rbp+0x480]`: loops
`008740A0..00874104` e `00874120..00874181` (8× 16 B, passo `0x80`).

**Struct de ponteiros** construído por `0x619D90` (chamado em `00873F1A`):

| Offset | Prova (RVA) | Conteúdo |
|---|---|---|
| `+0x000` | `00619DA8 mov qword [rdx],0`; memset `00619DB9 r8d=0x3F8` a partir de `00619DAF lea rcx,[rdx+8]` | 8 B zero + 1016 B zero |
| `+0x400` | `00619DDD mov [r14+0x400], ebx` (`ebx = r8`, arg3) | nº de ponteiros |
| `+0x404` | `00619DE4 mov [r14+0x404], edi` (`edi = r9`, arg4) | floats por segmento |
| `+0x408` | `00619DD6 mov [r14+0x408], rax` (`rax = r9<<2`, `00619DCF shl rax,2`) | bytes por segmento |

`0x61A9A0` preenche a tabela: `0061A9D0 mov rax,[r9]`, `0061A9D3 movsxd r8,[r9+0x18]`,
`0061A9D7 lea rdx,[rax+r8*4]`, `0061A9DB mov [r11+r10*8], rdx` — ponteiro para
`vector.dados + vector.indice*4`; `0061AA02 mov [r9+0x18], ecx` avança o índice com alinhamento
a 16 floats (`0061A9EE and eax,0xF`, `0061A9F1 sub`, `0061A9F4 add 0x10`, `0061A9FB cmove`).

**Cadeia até a arena — PROVADA em 2026-11-23** (desmontagens em `checks/`; o fechamento
está na subseção "Fechamento 2026-11-23" abaixo, que corrige o que aqui era `NÃO EXTRAÍDO`):

1. **Curva de redução.** `0x8634A0` registra os parâmetros
   `reduction_curve_freq_points_lo` (`0x2077580`), `..._hi` (`0x2077560`),
   `reduction_curve_magnitudes_lo` (`0x2077540`) e `..._hi` (`0x2077520`) em
   `00863577`/`0086358B`/`008635A0`/`008635B2` (`call [r15+0x18]`); o container
   `r14+0x30` é inicializado por `0x868B50` em `00863563`.
2. **Antes do design.** `0x86A4E0` chama `0x86FE90` (`0086A54B`, `0086A581`);
   `0x86A8C0` chama `0x873440` (`0086A92B`, `0086A961`). O arg8 de `0x86A8C0`
   (`r12`, `0086A8EA`; empilhado em `0086A8FC`) vira o arg10 de `0x873440`
   (`r14 = [rbp+0x15d8]`, `00873E6D`): é o **banco/arena**.
3. **Banco.** `0x619EA0` (`0086FF98`; `0x873565`) zera `{base,count,cap}` e grava
   `offset=n` (`00619EAF`–`00619EBA`); `0x6165A0` reserva (`006165DE`,`00616609`).
4. **Segmentação.** `0x619D90` em `00873F1A` monta a tabela: `+0x400=count`
   (`00619DDD`, `ebx=r8d=[this+0x48]`), `+0x404=N` (`00619DE4`, `edi=r9d`),
   `+0x408=4N` (`00619DD6`); `0x61A9A0` grava `table[i] = base + offset*4`
   (`0061A9D0`–`0061A9DB`) e avança **N** floats alinhados a 16
   (`0061A9E3`–`0061AA02`). **CORRIGIDO (2026-11-23):** `+0x404` **não é 32**.
   `r9 = [this+0x38] >> 1` (`00873EEA`, `00873F11`), e `[this+0x38] = 2*[this+0x28]`
   (`00873517`,`0087351B`), com
   `[this+0x28] = int(max(fs,44100)/44100 * fft_size)`
   (`0087346D maxss 0x207A5E4=44100`; `008734CA mulss 0x2079D04=1/44100`;
   `00873509 imul [rbp+0x15B0]`). `fft_size` é o **arg5** de `0x873440`
   (`[rbp+0x15B0]`, slot de arg5 da convenção Win64) e vale **`0x800` = 2048** na 1ª
   chamada (`0086A923`) e **`0x100` = 256** na 2ª (`0086A959`). Logo os segmentos têm
   2048 floats (banco principal) e 256 floats (banco secundário), não 32.
   O `32` de `00880403 r8d=0x20` é só a **quantidade de taps copiados**, não o segmento.
5. **Cópia.** `0x880390` (`00874107`, `00874184`) copia 32 floats
   (`00880403 r8d=0x20`) de `*(table+8*i)` (`0088040D`) para `ctx+0x40`
   (`00880419`; `call 0x10A0` em `0088041D`).
6. **Consumo.** `0x8B2680` passa `K=ctx+0x40` ao FIR (`008B2690 lea r8,[rcx+0x40]`,
   `008B26A8 call 0x8B2C30`) e **soma** a saída ao overlap-add do STFT
   (`008B2BDD addss xmm6,[r14+rax*4]`).
7. **Quem escreve na arena.** Em `0x873440`, a cadeia recebe `rdx=r14` (arena):
   `008769E5` → `0x87B680`, `008769F0` → `0x87BB60`, `008769FB` → `0x87DB30`,
   `00876A06` → `0x87E220`. Em `0x86FE90`: `008730F0`/`008730FB`/`00873106`/
   `00873111` com `rdx=r15`.
   - `0x87BB60` aloca `N` segmentos de `[r13+0x748+0x88]` floats na arena
     (`0087BD8B`–`0087BDC3`), preenche com `1.0f` (`0x87A7A0` em `0087BF57`,
     `0087BFC9`) e chama `0x882FC0` (`0087C231`, `0087C4DA`).
   - `0x882FC0` → ver **§8.2(f)** (fechado em 2026-11-23): duas curvas de shelf
     `A^(1−σ)` com `σ = 1/(1+(v/A)^(-k/6))`, aplicadas por `0x1340` aos buffers;
     constantes `500` `0x207A560`, `2000` `0x207A5A8`, `20` `0x207A3B0`, `0.5` `0x2079EA8`,
     `0.05` `0x2079D88`, `10` `0x207A360`, `12` `0x207A384`; `0x1c9a5a1` (`log10f`) e
     `0x1c9aa01` (`powf`) em `00883107`/`00883112` e `00883207`/`00883212`; `0x1220` em
     `00883112`/`00883212` e `0x1340` (mul elemento a elemento) em
     `008832E4`/`00883309`/`00883388`/`008833A9`.
   - `0x87E220` escala por `powf(10,2.4)` (`0x207A360`,`0x207A1E8`) e
     `powf(10,-4.8)` (`0x207A6F0`) em `0087EF78`–`0087F04B`; **não** é o FIR.
   - `0x877DD0` gera janela de Hann `max(0,(1−cos(2πi/N))/2)` (`00877F92`,
     `00878010`–`00878044`; `2π` `0x207A1E0`, `0.5` `0x207A0B8`) em `band+0x2c08`.

**REFUTADO (2026-11-23):** "`0x87E220` está em caminho distinto, sem ligação com
`ctx+0x40`". A ligação existe e é a arena: a cadeia recebe a mesma arena que `0x619D90`
segmenta e que `0x880390` copia. **REFUTADO também:** "`K[32]` é IFFT da curva" — não há
`call` para `0x1010`/`0x1280` em `0x87B680`, `0x87BB60`, `0x87DB30`, `0x882FC0`,
`0x882DE0` nem `0x8834C0`; só `0x1040`/`0x10A0`/`0x10D0`/`0x1220`/`0x1250`/`0x1310`/
`0x1340`/`0x12E0` e math.

**`NÃO EXTRAÍDO` (histórico, resolvido logo abaixo):** a aritmética final que produz os 32
valores. A leitura de `0x882FC0`/`0x87B680` e o rastreio do cursor da arena mostraram que
**não há fórmula**: a cópia ocorre sobre segmentos que foram zerados e marcados com `1.0f`
em `[0]` imediatamente antes. Ver "Fechamento 2026-11-23".

#### Fechamento 2026-11-23 — os 32 taps são `δ0` (PROVADO)

Ordem real das instruções dentro de `0x873440`, na **mesma** invocação:

1. `00873565 call 0x619EA0` com `rcx=this+0x68`, `edx=[this+0x38]=2N` — objeto interno.
2. `00873F1A call 0x619D90(arena, table=rbp+0x480, count=[this+0x48], N)` — monta a tabela
   (`table[i] = arena->base + offset*4`, `offset += N`).
3. `00873F40`/`00873FB0` — duas cópias da **tabela de ponteiros** (8×`0x80` B) para
   `rbp+0x890` e `rbp+0xCA0` (`00873F8D`, `00874001`).
4. `00874010`–`00874037` — **reset**: `eax=[rbp+0x880]=count`, e para `i<count`
   `0x10D0(table[i], [rbp+0x884]=N)` zera N floats. `0x10D0`→`0x2F60`:
   `00002F71 shl edx,2` + `00002F7C call 0x1D2E9E0` (memset). Não há branch que pule este
   bloco: os únicos saltos para dentro do trecho são os dos próprios laços
   (`00874018`, `00874037`, `00874063`).
5. `00874039`–`00874063` — **identidade**: para `i<count`, `table[i][0] = 0x3F800000`
   (`00874059 mov dword ptr [rax],0x3F800000` = 1.0f).
6. `00874072`/`00874084` — `0x8780D0(this+0x2BD8, count, N)` e `(this+0x2BF0, count, N)`
   criam as bandas (`0x8817D0`: `ecx=0x240`, `0x1798F42` zera) e `0x8784A0(band,N)` grava
   **`band+0 = N`** (`checks/decomp/0x1808784a0.c`: `*param_1 = param_2`).
7. `00874089`–`008740F3` e `0087410C`–`0087417D` — mais duas cópias da tabela
   (`rbp+0x10B0`, `rbp-0x20`).
8. `00874107`/`00874184 call 0x880390` — `memcpy(src=table[i], dst=band+0x40, 32 floats)`.
9. `00874189 mov [r14+0x18], esi` — restaura o cursor da arena; `esi` foi salvo em
   `00873F0D` (`mov esi,[r14+0x18]`) → `00873F14` (`mov [rbp+0x15B0],esi`) → recarregado
   em `0087403F`.
10. Só **depois** vem o design: `00876217` em diante e `008769E5`–`00876A0C` com `rdx=r14`.

Logo, no instante da cópia, `table[i][0..31] = {1.0f, 0, …, 0}`. **Não existe outro escritor
de `band+0x40`**: `xref_scan.py 0x880390` devolve **2 refs**, ambas em `0x873440`
(`00874107`, `00874184`). Resultado:

| Condição | `K[0]` | `K[1..31]` |
|---|---|---|
| `count>0` e `N>0` | `1.0f` (`0x3F800000`) | `0.0f` |
| `count=0` (enum → 0; tabela vazia, cópia não ocorre) | `0.0f` | `0.0f` (ctor `0x8817D0` zera) |

`K` **não depende de nenhum parâmetro**: os 32 valores são constantes gravadas por
`0x873440`, não o resultado de uma conta. Isto encerra a pergunta "qual aritmética produz os
32 taps": não há aritmética.

**Consequência direta no FIR — PROVADA.** `0x8B2C30` faz `y = x*K[0] + S->buf[p]`
(`008B2C62 mulss`, `008B2C7C addss`), zera `S->buf[p]` (`008B2C81`) e soma `x*K[j]` em
`S->buf[(p+j)&31]` para `j=1..31` (`008B2CD0`–`008B308D`). Com `K=δ0` nenhum `j≥1`
contribui, o anel fica em zero e **`y = x`**: o FIR de 32 taps é passa-direto. Com `K=0`
(count=0) a saída é `y = 0`.

**O que continua `NÃO PROVADO`** (e não altera o acima):

- O que o design (`0x87B680`/`0x87BB60`/`0x87DB30`/`0x87E220`, `008769E5`–`00876A0C`)
  escreve na mesma arena **depois** da cópia. Nenhuma instrução lida reordena os dois
  passos; em toda invocação o reset (passo 4) precede a cópia (passo 8). Isto **não**
  reabre `K`: `0x880390` copia **por valor** 128 B (`00880419 lea rdx,[r14+0x40]` +
  `0088041D call 0x10A0`), então escritas posteriores na arena não alcançam `band+0x40`.
  O que o design grava na arena é a **curva de ganho** — ver anexo abaixo.
- O papel dos blocos `≥32` em `0x880390` (`00880450`–`00880511`): com `band+0 = N = 2048`
  o laço roda e copia `arena+32` para `band+0x210` (e zera a 2ª metade), mas a fonte está
  zerada pelo passo 4. Quem preenche `band+0x210` e o uso de `0x1010` (FFT direta, §19.1)
  seguem `NÃO PROVADO`.
- A intenção DSP do caminho (splitter? detector?) — **NÃO PROVADO**; não inferir pelo nome.

Isto é compatível com §5.1/§13.3/§15.4 (FFT e "bandas" fora do caminho de áudio): o que se
fecha aqui é apenas que o FIR de `K` é neutro por construção, e que `ctx+0x40` **não** é
ganho, curva nem IFFT.

**Anexo 2026-11-23 — o que o design grava na arena: `0x882DE0` (PROVADO).**
`0x882DE0` (476 B, `00882DE0`–`00882FBB`, `.pdata`) **não** produz os 32 taps: produz a
**curva de ganho por frequência** e a escreve na arena (o ponteiro do span vem de
`0x87B680`: `0087B800 mov rax,[r12]` + `0087B80E lea r14,[rax+rcx*4]`, a mesma arena de
`0x619D90`). Fórmula transcrita instrução por instrução:

```
arg1 rcx=&span{float* p; int n}   (00882E0B mov rsi,rcx; 00882E48 movaps xmm2,[rsi];
                                  00882E95 movd r9d,xmm0 = n)
arg2 rdx=&inbuf                  (00882E5B mov rcx,[rbx] = inbuf)
arg3 xmm2 = A                    (00882E16 movaps xmm6,xmm2)
arg4 xmm3 = B                    (00882E20 cvtss2sd xmm7,xmm3)
arg5 [rsp+0x120] = D             (00882DF3 movss xmm1,[rsp+0x120])

sig  = (double)B * 0.601591280067049 * 0.7071067811865475   ; 00882E29, 00882E36
sig2 = sig * sig                                               ; 00882E80 mulsd xmm7,xmm7
s1   = logf(powf(10.0f, D*0.05f))                              ; 00882E3E powf, 00882E43 logf,
                                                               ; 00882E77 cvtss2sd xmm9,xmm0
k    = 1.0 / max((double)A, 1.1920928955078125e-07)            ; 00882E67, 00882E6F, 00882E89
e    = -0.5 / sig2                                             ; 00882E4E movsd -0.5; 00882E9A
p[i] = inbuf[i] + 1.1920929e-07f                               ; 00882E9F 0x1310 (escalar xmm1)
p[i] = p[i] * (float)k                                         ; 00882EBE 0x1220 (escalar xmm0)
p[i] = ln(p[i])                                                ; 00882EE1 0x1C8500
p[i] = p[i] * 1.44269502f                                      ; 00882EE6/00882EF4 0x1220
p[i] = p[i] * p[i]                                             ; 00882F12 0x1340 rcx=rdx=p
p[i] = p[i] * (float)e                                         ; 00882F28/00882F32 0x1220
p[i] = exp(p[i])                                               ; 00882F50 0x1C84A0
p[i] = p[i] * (float)s1                                        ; 00882F66/00882F70 0x1220
p[i] = exp(p[i])                                               ; 00882F8E 0x1C84A0
```

Equivalente algébrico (as duas `exp` são a exponencial natural de `0x1C84A0`; a conversão de
dB usa `logf(powf(...))`, que é `ln(10^(D/20))`):

```
g(f)   = exp( -0.5 * ( log2((f+eps) / max(A,eps)) / sig )^2 )    ; gaussiana em log2-freq
out(f) = (10^(D/20)) ^ g(f)
```

| Constante | RVA | Valor (bits do dump) |
|---|---|---|
| `0.05f` | `0x2079D88` | `0x3D4CCCCD` = `0.05000000074505806` |
| `10.0f` | `0x207A360` | `0x41200000` = `10.0` |
| `0.601591280067049` (f64) | `0x207A0D0` | `0x3FE3403C5B2E4BCB` |
| `0.7071067811865475` (f64) | `0x207A0E8` | `0x3FE6A09E667F3BCC` (= 1/√2) |
| `-0.5` (f64) | `0x207A6B8` | `0xBFE0000000000000` |
| `1.0` (f64) | `0x207A138` | `0x3FF0000000000000` |
| `2^-23` (f64) | `0x2079E20` | `0x3E80000000000000` = `1.1920928955078125e-07` |
| `1.1920929e-07f` | `0x2079CF0` | `0x34000000` = `FLT_EPSILON` |
| `1.44269502f` | `0x207A020` | `0x3FB8AA3B` = `log2(e)` |

**Identificação das funções de math (PROVADA por instrução):**

- `0x1C8500` = **ln** in-place: `idx@0x21C7408=4` → `tab 0x21C6AA8` → `0x1C8A00` →
  `[0x21C70E8]` → RVA `0x293760`; no corpo, `002939CF vfmadd213ps ymm9, ymm15, ymm12`
  com `ymm15` = `0x1ECAE40` = `0.693147182` (`ln 2`) — `ln = expoente·ln2 + série`.
- `0x1C84A0` = **exp** in-place: `tab 0x21C6A28` → `0x1C8880` → `[0x21C6F08]` →
  RVA `0x240C00`; `00240D96 vfmadd231ps ymm10, ymm4, ymm15` com `ymm4` = `0x1E6FBC0` =
  `1.44269502` (`log2 e`) e `00240D43` `ymm0` = `0x1E6FC00` = `12582912` = `1.5·2^23`
  (magic do `2^k`) — construção clássica de `e^x`.
- **M3 (2026-11-25): ln e exp transcritos bit a bit** em `port/src/ippmath.rs`
  (`checks/t_ln_exp_ipp.md`).
  - **ln:**
    - lane vetorial: `t = i − 0x3F2AAAAB`, `e = t>>23`, `m ∈ [2/3,4/3)`,
      polinômio de grau 6 em `f = m−1` por FMA, `y = e·ln2 + (f·p·f + f)`;
    - lanes especiais (`(i+0x800000) <s 0x1000000`) vão para `0x293F80`, em f64
      com a tabela `0x1ECAF60` (65 × `[c,a,b]`).
  - **exp:**
    - lane vetorial: `t = log2e·x + 1.5·2^23`, `r = x − hi·k − lo·k` (FNMA),
      polinômio de grau 5, `y = bits((t<<23) + p)`;
    - `|x| > 87.33654` vai para `0x2414C0`, em f32 com redução sem FMA, escala
      `2^k` e caminhos de overflow, underflow e denormal.
  - **Prova:** `checks/j_ln_exp_avx.rs`, emulador AVX2/FMA com as constantes do
    dump. Deu `bad = 0` no teste amostral, com mutações detectadas, e
    `bad = 0` no **exaustivo 2^32** das duas funções.
  - **Sem `vrcpps`:** vale em qualquer CPU com FMA.
  - **A IPP difere de `f32::ln`/`f32::exp`** em até alguns ulp.
- `0x1C9AA01` = **powf**, `0x1C9A9FB` = **logf**, `0x1C9A5A1` = **log10f**: thunks de IAT
  (não são IPP). Import descriptor em `0x2175044` (`OFT 0x2176878`, `FirstThunk 0x1D8D790`);
  índice 15 (`0x1D8D808`) = `logf`, índice 17 (`0x1D8D818`) = `powf`, índice 0 (`0x1D8D790`)
  = `ceil`, índice 1 (`0x1D8D798`) = `log10f`.

**Valores do chamador `0x87B930` (prova do uso):** `A = 2000.0f` (`0087B8CD`, `0x207A5A8`),
`B = 2.5f` (`0087B8C5`, `0x207A1F8`), `D = 3.0f` (`0087B91C`→`0087B924 [rsp+0x20]`,
`0x207A248`). Logo `sig = 2.5·0.425390... = 1.06348` oitavas: um sino de +3 dB centrado em
2 kHz. Para bit-exact, manter `logf(powf(10,D*0.05f))` — **não** substituir por
`D*0.11512925`.

**`0x882FC0` (1.063 B, o outro designer) — FECHADO em 2026-11-23, ver §8.2(f).** Resumo dos
sítios: bloco 1 — `00882FFD movaps xmm0,xmm2` (arg3) → `00883054 call 0x1C9A5A1` =
`log10f(arg3)`; `0088307D mulss 20` → `008830EC mulss 0.5` → `008830FC mulss 0.05` →
`powf(10, 0.5·log10(arg3))` em `00883107` (`0x1C9AA01`); `008830C8`/`008830CB` negam
`20·log10(arg3)` em `[rsp+0x20]` (5º arg); `008830E7 call 0x88E130` com `A=500` e `k=12`;
`00883112 call 0x1220` aplica o `powf` ao buffer. Bloco 2 — `00883152 movaps xmm0,xmm12`
(arg4), mesmo padrão, com `008831D1 xmm2=2000.0`, `008831E7 call 0x88E130`, `00883207 powf`,
`00883212 0x1220`. Depois `0088327A call 0x87A7A0` e `0x1340` multiplica os buffers por cada
curva (`008832E4`/`00883309`/`00883388`/`008833A9`). Fórmula fechada, ordem exata e o que
continua `NÃO PROVADO`: **§8.2(f)**.

### 10.5 Rust equivalente (mesma aritmética, mesma ordem)

```rust
#[derive(Clone, Copy)]
pub struct Fir32 { pub buf: [f32; 32], pub pos: u32 }

#[inline]
pub fn fir32_scatter(s: &mut Fir32, x: f32, k: &[f32; 32]) -> f32 {
    let p = s.pos as usize;          // 0..31
    let mut y = x * k[0];            // mulss
    y += s.buf[p];                   // addss
    s.buf[p] = 0.0;                  // movss, imediato 0
    let mut j = 1usize;
    while j <= 31 - p {              // 008B2C85: 31 - p
        s.buf[p + j] += x * k[j];
        j += 1;
    }
    if p != 0 {
        let mut i = 0usize;
        while i < p {
            s.buf[i] += x * k[32 - p + i];
            i += 1;
        }
    }
    s.pos = ((p as u32) + 1) & 0x1f;
    y
}
```

Sem FMA (`vfmadd`): o dump usa `mulss` seguido de `addss` em escalar, e `mulps`/`addps` nas
versões desenroladas. Compilar com `-C target-feature=-fma` ou usar `mul_add` proibido —
`mul_add` gera FMA e muda o arredondamento.

### 10.6 Correção que isto impõe ao §5.1

O áudio **usa** transformada: `0x885040`/`0x8875F0` → `0x8B2680` → stubs IPP
`0x1010`/`0x1280`/`0x15E0` (impls `0x20E0`, `0x7B40`, `0xD380`) com escala `1.0f/n` e
overlap-add. O que o §5.1 provou foi apenas que a FFT do **JUCE** (`0x1D69E00`) não está no
áudio. Ver `PLANO_MOTOR_AUDIO.md` §24. A identidade exata de `0x20E0` (FFT do IPP ou outro
objeto de spec com magic 7) ainda é `NÃO PROVADA`.


---

## 11. `0x8CAE90` — MAC em lotes de bandas (PROVADO, 2026-11-22)

Primeira função lida da Etapa A. Desmontagem completa: `checks/8cae90.dis`
(80 linhas, chain-aware `0x8CAE90..0x8CAFC3`, 307 B). Pseudocódigo comentado:
`docs/engine/decomp/manual_008CAE90.c`. Chamador: `0x8C02F0` (2 sítios:
`0x8C099C`, `0x8C0AE5`; `checks/8c02f0.dis`).

### 11.1 Assinatura e controle

```
void batch_mac(Set16* dst /*rcx*/, Set128* a /*rdx*/, Set16* b /*r8*/)
```

Três caminhos, todos com a mesma forma `mac(src1, src2, dst_acc, len)`:

| Condição (RVA do cmp) | Laço | Chamada |
|---|---|---|
| `dst->n == a->n == b->n` (`008CAEB1`, `008CAEC0`) | `008CAEF0..008CAF0B` | `008CAEFE`: `mac(a[i], b[i], dst[i], len)` |
| `a->n > 1` e `b->n == 1` (`008CAF12`, `008CAF1B`) | `008CAF40..008CAF5A` | `008CAF4D`: `mac(a[i], b[0], dst[i], len)` |
| `a->n == 1` e `b->n == 1` (`008CAF5E`, `008CAF65`, `008CAF67`) | `008CAF91..008CFA9` | `008CAF9E`: `mac(a[0], b[0], dst[i], len)` |

Qualquer outra combinação retorna sem fazer nada (`008CAFB0`). `n = dst->n` em todos
os caminhos (`008CAEC8`, `008CAF25`, `008CAF71`); `len = dst->len` vem de `[rcx+0x84]`
(`008CAED8`, `008CAF31`, `008CAF8A`) e vai para `r9d` (`008CAEF4`, `008CAF44`, `008CAF95`).

### 11.2 Correção material: `0x1580` **não é soma**, é MAC in place

Cadeia de despacho provada:

```
0x1580 (thunk, seletor 0x21C7408 = 4)
  -> tabela 0x21C6488[4] = 0xCCE0
  -> 0xCCE0  call 0x65EA0          (0000CD06)
  -> 0x65EA0 call 0x6CE80          (00065ED5)
```

`0x6CE80`, variante AVX:

```asm
0006CEAF  vmovups        ymm1, [rcx]              ; src1
0006CEB7  vmovups        ymm0, [rdx]              ; src2
0006CEBB  vfmadd213ps    ymm1, ymm0, [r8]         ; ymm1 = src1*src2 + dst
0006CEC4  vmovups        [r8], ymm1               ; dst = ymm1
```

Variante escalar `0xC620` (tabela[0]) confirma sem FMA:

```asm
0000C6A0  movss xmm0, [rcx+rdx*4]   ; src1
0000C6A5  mulss xmm0, [rsi+rdx*4]   ; src2 (rsi = rdx de entrada)
0000C6AA  addss xmm0, [r8+rdx*4]    ; + dst
0000C6B0  movss [r8+rdx*4], xmm0    ; -> dst
```

Logo a ordem dos argumentos é `(src1=rcx, src2=rdx, dst_acumulador=r8, len=r9d)` e a
operação é **`dst[k] = dst[k] + src1[k]*src2[k]`**. A anotação antiga "soma" em §9.3
está retirada. Isto também invalida a classe atribuída a `0xCCE0` na tabela do
`PLANO_MOTOR_AUDIO.md` §14.3 ("sem aritmética vetorial"): o corpo de 64 B de `0xCCE0`
não tem vetores, mas o chamado `0x6CE80` tem `vfmadd213ps`. O nome IPP continua
**NÃO PROVADO** (§14.3).

### 11.3 Structs (offsets provados)

| Struct | Offset | Conteúdo | Instrução |
|---|---|---|---|
| `Set16` | `+0x00..+0x7F` | 16 ponteiros, passo 8 | `008CAF03 lea rbx,[rbx+8]` |
| `Set16` | `+0x80` | `int n` | `008CAEC8 movsxd rbp,[rcx+0x80]`; `008CAEB1/008CAEC0 cmp` |
| `Set16` | `+0x84` | `int len` | `008CAED8 mov r14d,[rcx+0x84]` |
| `Set128` | `+0x00..+0x3FF` | 128 ponteiros, passo 8 | `008CAF52 lea rdi,[rdi+8]` |
| `Set128` | `+0x400` | `int n` | `008CAEA2 mov eax,[rdx+0x400]`; `008CAF12 cmp ...,1` |

Tamanhos: `Set16` = 0x88 B, `Set128` = 0x404 B. No chamador `0x8C02F0` os dois
`Set16` são `[rbp+0x340]` e `[rsp+0x30]` e o `Set128` é `[rbp+0xB60]`
(`008C0917`, `008C0921`, `008C092B`, `008C0A76`, `008C0A82`, `008C0A8C`).

### 11.4 Constantes

**Zero constantes float próprias**: `show_func.py 0x8CAE90 | findstr rip` devolve
0 linhas. Única constante: imediato `1` em `008CAF12`, `008CAF1B`, `008CAF5E`,
`008CAF65`, `008CAF6F` (detecção de broadcast). Nenhum coeficiente numérico.

### 11.5 Rust equivalente (mesma aritmética e ordem)

```rust
pub struct Set16 { pub ptr: [Option<&'static mut [f32]>; 16], pub n: i32, pub len: i32 }
pub struct Set128 { pub ptr: [Option<&'static [f32]>; 128], pub n: i32 }

// auxiliares só para desembrulhar os Option do esquema acima
#[inline(always)] fn src<'a>(p: &'a Option<&'a [f32]>) -> &'a [f32] { p.as_ref().unwrap() }
#[inline(always)] fn dst<'a>(p: &'a mut Option<&'a mut [f32]>) -> &'a mut [f32] { p.as_deref_mut().unwrap() }

#[inline(never)]
fn mac(src1: &[f32], src2: &[f32], dst: &mut [f32], len: i32) {
    // 0x6CE80: vfmadd213ps => uma única operação de multiplicar-somar por elemento.
    // Compilar sem contrair mul+add em FMA alteraria o arredondamento do IPP;
    // o despacho 0x6CE80 usa FMA, então a ordem a reproduzir é src1*src2 + dst.
    for k in 0..len as usize {
        dst[k] = (src1[k] * src2[k]) + dst[k];
    }
}

pub fn batch_mac(dst: &mut Set16, a: &Set128, b: &Set16) {
    if dst.n == a.n && dst.n == b.n {
        for i in 0..dst.n as usize {
            mac(src(&a.ptr[i]), src(&b.ptr[i]), dst(&mut dst.ptr[i]), dst.len);
        }
        return;
    }
    if a.n > 1 {
        if b.n == 1 {
            for i in 0..dst.n as usize {
                mac(src(&a.ptr[i]), src(&b.ptr[0]), dst(&mut dst.ptr[i]), dst.len);
            }
        }
        return;
    }
    // 008CAF5E cmp a->n,1 ; 008CAF65 jne -> exige a->n == 1
    // 008CAF67 cmp b->n,1 ; 008CAF6F jne -> exige b->n == 1
    if a.n == 1 && b.n == 1 {
        for i in 0..dst.n as usize {
            mac(src(&a.ptr[0]), src(&b.ptr[0]), dst(&mut dst.ptr[i]), dst.len);
        }
    }
}
```

**Atenção ao port:** o `0x1580` executa FMA (`vfmadd213ps`, `0006CEBB`) na variante
selecionada (`ippJumpIndex=4`, `0x21C7408`). A varredura "0 FMA" do §23 cobre só
`0x8A0000–0x8E0000`; o IPP fica em `IPPCODE` (`0x1CD7000`) e **tem FMA**. Chaos de
arredondamento: `f32::mul_add` ou compilação com FMA; **`mulss` seguido de `addss`
não reproduz bit-a-bit o IPP nesta variante**. A variante escalar `0xC620` (índice 0)
usa `mulss`+`addss`, mas não é a selecionada no dump.


---

## 17. Primitivas vetoriais — ordem real dos argumentos (PROVADO, 2026-11-22)

Numeração: o `PLANO_MOTOR_AUDIO.md` §17 inventaria as primitivas; esta é a **§17.6**
("ordem dos argumentos"), fechada na Etapa B do §23. As subseções 17.1–17.5 e os
números 12–16 do spec ficam reservados — não há conteúdo lido para eles ainda.
Cada linha abaixo vem de `checks/<nome>.dis` (`show_func.py`, chain-aware), não de nome
de parâmetro nem de decompilado. convenção Win64: rcx, rdx, r8, r9d / xmm0–xmm3.

### 17.6 As 9 primitivas da cadeia de `0x8C0BD0` (todas com instrução que prova)

| thunk | impl | proto provada (registradores) | aritmética provada | instrução que prova (RVA) |
|---|---|---|---|---|
| `0x1550` | `0x63640` via `0xC560` | `(den=rcx, num=rdx, dst=r8, n=r9d)` | `dst[i] = num[i]/den[i]` via `vrcpps` + série `(1+e+e²)` com FMA, em **duas** aritméticas (A quociente / B recíproco; despacho por `n` e `dst & 0x1c`, §8.4.8); denominador 0 é substituído por 1.0 antes do recíproco | `000636E0 vmovups ymm0,[rcx]`; `000636E6 vmovups ymm1,[rbp]` (`rbp=rdx` em `00063676`); `0006376F vblendvps ymm5,ymm2,ymm4,ymm1` (zero→1.0); `00063775 vrcpps ymm0,ymm5`; `00063787 vmulps ymm0,ymm0,[r13+0x20]`; `00063791`/`00063796 vfmadd213ps`; `00063A27 vmovups [r8],ymm0` |
| `0x11F0` | `0x5BC0` | `(src=rcx, escalar=xmm1, dst=r8, n=r9d)` | `dst[i] = escalar*src[i] + dst[i]` (MAC in place) | `0005BC4 test rcx`; `0005BCD test r8`; `0005C40 vmovss xmm0,[rcx+r10*4]`; `0005C46 vfmadd213ss xmm0,xmm1,[r8+r10*4]`; `0005C4C vmovss [r8+r10*4],xmm0`; `0005C85 vfmadd213ps ymm2,ymm0,[r8+rax*4]` |
| `0x1190` | `0x4BC0` | `(a=rcx, b=rdx, dst=r8, n=r9d)` | `dst[i] = a[i]*b[i]` — **dst é terceiro ponteiro, NÃO é in place** | `0004BC7 mov rbp,rdx`; `0004C60 vmovss xmm0,[rcx]`; `0004C65 vmulss xmm1,xmm0,[rbp]`; `0004C6B vmovss [r8],xmm1`; `0004C8B vmulps ymm1,ymm0,[rbp]`; `0004C91 vmulps ymm3,ymm2,[rbp+0x20]`; stores `0004C97`/`0004C9D vmovups [r8]` |
| `0x10D0` | `0x2F60` | `(dst=rcx, n=edx)` | **zero-fill**: `dst[0..n-1]=0`; valor é constante `vxorps`, não argumento | `0002F71 shl edx,2`; `0002F7C call 0x1D2E9E0`; impl `01D2E9E5 mov rsi,rdx`; `01D2E9EE vxorps ymm0,ymm0,ymm0`; `01D2EA0B vmovdqu [rdi],ymm0` |
| `0x1370` | `0xA120` | `(src=rcx, dst=rdx, n=r8d)` | `dst[i] = src[i] + dst[i]` — **adição de vetores in place, NÃO escalar** | `000A125 mov rdi,rdx`; `000A1A0 vmovss xmm0,[rcx]`; `000A1A5 vaddss xmm1,xmm0,[rdi]`; `000A1AA vmovss [rdi],xmm1`; `000A1CD vaddps` + store `000A1DA` |
| `0x1100` | `0x3480` | `(dst=rcx, n=edx, bound=xmm2, modo=r9d)` | modo `4`: `dst[i]=min(bound,dst[i])`; modo `0`: `dst[i]=max(bound,dst[i])`; outro modo → `-5` (`00034A4`) | `0003495 test r9d`; `000349E cmp r9d,4`; `0003500 vminss xmm0,xmm2,[rcx]`; `0003505 vmovss [rcx]`; `0003640 vmaxss xmm0,xmm2,[rcx]`; `0003645 vmovss [rcx]` |
| `0x1220` | `0x6160` | `(dst=rdx, escalar=xmm0, n=r8d)` | `dst[i] *= escalar`; atalhos: escalar `1.0` → retorno (`00062FA`), escalar `0` → `call 0x2F60` zero-fill (`00062F0`) | `0006168 test rdx`; `0006171 test r8d`; `0006200 vmulss xmm1,xmm0,[rdx]`; `0006205 vmovss [rdx],xmm1` |
| `0x11C0` | `0x50E0` | `(a=rcx, b=rdx, dst=r8, n=r9d)` | `dst[i] = b[i] - a[i]` — **ordem rdx−rcx; dst separado, NÃO in place** | `00050E7 mov rbp,rdx`; `0005180 vmovss xmm0,[rbp]`; `0005186 vsubss xmm1,xmm0,[rcx]`; `000518B vmovss [r8],xmm1` |
| `0x1250` | `0x69C0` | `(src=rcx, dst=rdx, n=r8d, bound=xmm3, modo=[rsp+0x30])` | modo `4`: `dst[i]=min(src[i],bound)`; modo `0`: `dst[i]=max(src[i],bound)`; outro → `-5` (`00069F1`) | `00069E0 mov eax,[rsp+0x30]` (5º arg); `00069E4 test eax`; `00069EC cmp eax,4`; `0006A60 vmovss xmm0,[rcx]`; `0006A65 vminss xmm0,xmm0,xmm3`; `0006A69 vmovss [rdx],xmm0`; `0006BC5 vmaxss xmm0,xmm0,xmm3` |

### 17.6.1 Correções impostas pela leitura (o rótulo do §23.2 estava errado)

- `0x4BC0` (mult) e `0x50E0` (sub) escrevem em **r8**, terceiro ponteiro — não são
  "in place" como o plano dizia. A cadeia de `0x8C0BD0` passa um buffer de destino distinto.
- `0xA120` é `dst += src` com **dois ponteiros** (rcx e rdx), não "`+=` escalar".
- `0x69C0` compara um vetor (rcx) contra um **escalar em xmm3**, não "entre vetores".
- `0x2F60` zera com `vxorps`; o valor não é parâmetro.
- `0x5BC0` não usa `rdx` como dado: `0005BDF movsxd rdx,r9d` é só contador local; o
  escalar entra em **xmm1**.
- `0x63640` é uma **divisão** (`vrcpps` + refinamento), não um recíproco puro: `rcx` é o
  denominador e `rdx` o numerador (`00063787 vmulps ymm0,ymm0,[r13+0x20]`).

### 17.6.2 Constantes com RVA

| Função | Constante | RVA | Uso provado |
|---|---|---|---|
| `0x63640` | vetor de `1.0f` (8 floats) | `0x1DF9DA0` | `0006368F vmovups ymm4,[rip]`; blend do zero em `0006376F` e refinamento em `00063782` |
| `0x63640` | `0x7F800000` (+inf) / `0x7FBFFFFF` | imediatos em `000637D2`–`0006390C` | tratamento do denominador zero |
| `0x6160` | `1.0f` | `0x1DF4190` | `000617A vucomiss xmm0,[rip]` (atalho de retorno) |

As outras seis primitivas **não têm constante float própria** (`show_func.py | findstr rip`
devolve 0 linhas). Nenhum nome de função IPP é afirmado — os nomes continuam **NÃO PROVADOS**
(§14.3 do plano).

## 18. Consolidação das etapas D1/E/G (2026-11-22) — só instruções lidas

### 18.1 `0x8BF650` e `0x8BFD30` — plumbing de despacho

`checks/8bf650.dis` (1792 B, 9 calls) e `checks/8bfd30.dis` (1664 B, 8 calls dentro da
função). Nenhum FMA, mulss/addss/divss novo nem coeficiente: copiam descritores de 24 B
(`008BF9B7 mov rax,[rsi+8]`, `008BFB8D add rsi,0x18`, `008BFB9F cmp rsi,[rbp+0xc48]`) e
chamam primitivas já provadas:

| RVA | Alvo | Efeito provado (§17.6) |
|---|---|---|
| `008BF719`, `008BFCFE`, `008BFF85` | thunk `0x10D0` → `0x2F60` | zero-fill |
| `008BF827`, `008BFA48`, `008BFE94`, `008C00B3` | `memset` | zerar 0x3F8 B |
| `008BFA17` | `memcpy` | copiar descritor |
| `008BF955`, `008BFB84` | `0x8CAB40` | chama `0x86F480`/`0x867CC0` (nomes IPP **NÃO PROVADOS**) |
| `008BFC3E`, `008BFC7D` | thunk `0x1190` → `0x4BC0` | mul vetorial |
| `008C01A9` | thunk `0x1220` → `0x6160` | escalar × vetor |

`0x8BFD30` faz 5 passadas: `008BFD60` → tabela `0x2014360` com `i32=[8,9,10,6,5]`;
`008C01E5 inc r15d`, `008C01EB cmp rax,5`, `008C0202 jb 0x8BFD80`. O tipo da passada é
`r14`, o campo do descritor é `[r15]` (`008BFDB4 mov r8d,[r15]`); o despacho compara
`008BFDC6 cmp r8d,0xA`, `008BFDD8 cmp r8d,9`, `008BFDEA lea eax,[r8-9]`,
`008BFE02 lea eax,[r8-0x10]`, `008BFE17 lea eax,[r8-8]`, `008C0066 lea eax,[r8-8]`.
`008BFE32/46`, `008C003E/52` chamam `0x61B790` com `(tipo-2, campo)` e `(tipo-1, campo)`.

### 18.2 `0x8C33D0` — MAC de bandas com as primitivas B

Hex-Rays entregou vazio; `checks/8c33d0.dis` (519 linhas, 2128 B) lida por
`show_func.py`; pseudocódigo manual em `docs/engine/decomp/manual_008C33D0.c`. Cópia de
`8×0x80 B = 256 floats` (`008C340B mov r14d,8`, loop `008C3440..008C3495`) — **buffer de
256 floats, não prova do N da FFT**. Chamadas: `008C3698`/`008C36D6`/`008C3A43`/`008C3B93
call 0x11C0` (subtração), `008C389B call 0x1250` (modo `4` em `008C3893` = `min(src,0)`),
`008C393B call 0x1100` (modo `0` em `008C3933` = `max(bound,dst)`). Alinhamento da arena
em 16 floats: `008C3510 and eax,0xf`, `008C3513 sub`, `008C3516 add 0x10`, `008C351D
cmove`. `NÃO PROVADO`: origem de `[rbp+0x740]`/`[rbp+0x744]` no primeiro trecho (leitura em
`008C34BD`/`008C34C7` antes da escrita em `008C371A`/`008C3724`).

### 18.3 Struct de estado — stores com RVA

Varredura em `checks/state_offset_refs.txt` (127 refs, offsets `0x2C38`, `0xBFF8`, `0x5ED0`):

| Campo | Store provado | Origem |
|---|---|---|
| `ctx+0x2C38` | `00870941 mov [rdi+0x2c38],rax` (`0x86FE90`) | `rax=[rbp+0x440]` em `008708FD` |
| `ctx+0x2C38` | `00873F06 mov [rdi+0x2c38],rax` (`0x873440`) | `rax=[rbp+0x15c0]` em `00873ECF` |
| `ctx+0xBFF8` | `00863CD9 mov [r14+0xbff8],rdi` (`0x8634A0`) | 16 blocos de `0x1040 B` (`00863C80`), 16 ponteiros em `[rsi+rbx*8]` (`00863CAC`), `[rsi+0x80]=0x10`, `[rsi+0x88]=0x400` |

Os dois sítios de `+0x2C38` zeram `[rdi+0x2bb8..0x2c18]` antes (`008708A6..008708F6`,
`00873E80..00873EC8`) e escrevem `+0x2c40`/`+0x2c44` depois (`0087090B`/`00870911`,
`00873EDD`/`00873EE3`). As ~120 leituras de `+0x2C38` alimentam as gigantes.

**O conteúdo do objeto agora tem 6 leituras provadas** (§8.3, `008B3F5C`–`008B3FBA`):
`+0x00` f32, `+0x04` f32, `+0x28` f32, `+0x3C` f32, `+0x4C` f32, `+0x52` u8. Os dois
primeiros (`+0x00`/`+0x04`) são os que alimentam o escalar de ganho de §8.2c.

`+0x5F8` e `+0x5ED0` só aparecem como `lea` a destrutores/helpers (`00862F89`, `00862F95`,
`00863994`): **store `NÃO PROVADO`**.

**Mapa dos 143 params: `NÃO EXTRAÍDO` (mas a tabela está decodificada).** A tabela
`0x238E9B0` tem 3 refs RIP (`0x3314C0`, `0x331AC8`, `0x331B0A`), todas construtoras de um
handle `{int index; const Table *base}` (`0x3314C0: mov [rcx],edx; mov [rcx+8],rax` com
`rax = 0x238E9B0`). Nenhuma liga um parâmetro a um offset de `ctx`; os nomes de
`params.csv` continuam não sendo prova. Ver §3 para o mapa de campos.

### 18.4 Lista de descritores de 24 B — escritor, alocador e contagem PROVADOS (2026-11-23)

> **Histórico:** a versão de 2026-11-22 era "leitura provada, escritor `NÃO PROVADO`".
> A leitura continua válida e está mantida; o escritor/alocador/contagem foram provados
> nesta revisão. **CORRIGIDO em 2026-11-23:** `[ctx+0x10]` aponta para um `std::vector`
> de 24 B `{begin, end, cap}`, não para um par de 16 B.

`ctx+0x10` aponta para um `std::vector` de 24 B `{begin, end, cap}` (só os dois primeiros
são lidos no loop). O consumidor `0x8C0BD0` lê:

```
008C0C1F  mov  rsi, [r8]        ; begin = par.begin
008C0C0D  mov  rax, [r8+8]      ; end   = par.end
008C0C2F  cmp  rsi, rax         ; loop enquanto begin != end
008C0C90  cmp  dword [rsi+0x10], 2   ; tipo ativo = 2
008C0CDA  movsxd rax, dword [rsi+8]  ; índice s32
008C0CE6  lea  rax, [rax*8]
008C0CDE  lea  r8, [rbp-0x60]
008C0CEE  sub  rax, r8
008C0CF1  lea  r8, [rax+r14]    ; dst = base + idx*8 - temp
008C13CD  add  rsi, 0x18        ; stride = 24 B
008C13D6  cmp  rsi, rax
008C13D9  jne  0x8C0C90
```

| Campo | Offset | Prova |
|---|---|---|
| `par.begin` | `+0x00` | `008C0C1F`, `008BFDA0` |
| `par.end` | `+0x08` | `008C0C0D`, `008BFD9C` |
| descritor campo A (i32) | `+0x00` | `008BFDB4 mov r8d,[r15]` |
| descritor índice (i32) | `+0x08` | `008C0CDA`, `008C0CE6` |
| descritor tipo (i32) | `+0x10` | `008C0C90 cmp ...,2` |
| descritor `+0x14..0x17` | — | `NÃO EXTRAÍDO` |

Chamadores: `0x8B3ED0` (chain-aware; `.pdata` reporta `0x8B4268`) com `008B6046 mov
r8,[r13+0x10]` / `008B605C call 0x8C0BD0`, `r13=rcx` desde `008B3F14`, `ctx=[outer+8]` em
`008ABCE3`, `outer=r14+0x1408` em `0088FBB1`. Gêmeo em `0x8C5FD8` (`008C7DB6`,
`008C7DCC`). Segundo consumidor `0x8BFD30`: `008BFEBF`, `008BFF97`.

Constantes: `2` `008C0C90`; `0x18` `008C13CD`/`008BFF97`; `0x3F8` `008C0CAB`;
`1.0f` `0x2079F9C` em `008C0C73`; `1.1920929e-07` `0x2079CF0` em `008C0C85`. A nota
`008BFE99` como `cmp ...,2` está corrigida: a instrução é `mov r8d,[r15+0x10]`.

#### Escritor, alocador e contagem — PROVADO (2026-11-23)

**Seleção e destino.** `0x862E40` aloca `E` (`00862E52 mov ecx,0xC1A8`; `00862E5D call
0x1796CF4`) e chama `0x8634A0` (`00862E72`). `0x8634A0` guarda `arg2`/`arg3` em `E+0`/`E+8`
(`008634CD`, `008634D7`), escolhe a tabela por `[arg3]` e `[arg3+8]` (`008634FB`, `00863507`)
e grava o retorno de `0x85E6C0`:

```
008634FE  call 0x85E6C0
00863503  mov [r14+0x18],rax      ; E+0x18 = vetor A
0086350A  call 0x85E6C0
00863535  mov [r14+0x20],rax      ; E+0x20 = vetor B
008638D6  lea rcx,[r14+0x5F8]     ; ctx = E+0x600
008638EC/F0  [rsp+0x30] = [E+0x20]   ; 7º arg de 0x86A4E0
008638F5/900 [rsp+0x28] = [E+0x18]   ; 6º arg de 0x86A4E0
00863929  call 0x86A4E0
```

`0x86A4E0` (rbp = entry−0x3F, `0086A4F8`) lê `arg6 = [rbp+0x6F] = [entry+0x30]` (`0086A518`)
e o repassa como 8º arg do ctor (`0086A526 mov [rsp+0x38],rbx`); `arg7` vai como 9º
(`0086A521 mov [rsp+0x40],rdi`). `0x86FE90` grava:

```
0086FF03  mov rax,[rbp+0x448]     ; rbp = entry−0x408 (0086FEA8); = 8º arg
0086FF0A  mov [rcx+0x10],rax      ; ctx+0x10 = vetor A (= [E+0x18])
0086FF0E  mov rax,[rbp+0x450]     ; 9º arg
0086FF15  mov [rcx+0x18],rax      ; ctx+0x18 = vetor B (= [E+0x20])
```

**Campos dos descritores.** `0x85E6C0` é `switch` de 23 posições (`0085E6CE cmp ecx,0x16`;
tabela `0x85FFA0` em `0085E6E1`; `0085E6EB jmp rcx`). Cada caso monta uma
`initializer_list` de elementos de 24 B na pilha e chama `0x563E40`. Exemplo (caso 5,
vetor `0x2754E40`): `0085EDE7 lea rax,[rsp+0x30]` (begin), `0085EDF9 lea rdx,[rsp+0x78]`
(end; 0x78−0x30 = 0x48 = 3×24), `0085EE23/2B/3C/44/55` gravam `+0x10/+0/+8/+0x10/+0`,
`0085EE5D call 0x563E40`.

**Alocador/contagem.** `0x563E40`: `00563E55/5B` = `end−begin`; `00563E5E movabs
rbp,0xAAAAAAAAAAAAAAAB`; `00563E68 sar rbx,3`; `00563E6F imul rbx,rbp` → `n=(end−begin)/24`;
`00563E95 lea rcx,[rbx+rbx*2]` + `00563E9E shl rcx,3` → `24n`; `00563EA2 call 0x32B810`
(`operator new`); `00563EA7/EB8` `begin=end=base`; `00563EBF/EC6` `cap=base+24n`;
`00563ED0 call 0x1798F3C` (memcpy); `00563EE4/EE8` `end=base+24n`.

**Tabela caso → vetor → `(code, idx, kind)`** (lida de `0x85FFA0` + `.data`; gerada por
`tools/stage_c_table.py`):

| caso | vetor | descritores |
|---|---|---|
| 0 | `0x2752208` | vazio (`0085EBCA`) |
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

**`+0` é lido como discriminador de faixa** (não `+0x10`): `008BFDB4 mov r8d,[r15]`;
`008BFDC6 cmp r8d,0xA`; `008BFDEA lea eax,[r8-9]`; `008BFE02 lea eax,[r8-0x10]`;
`008BFE17 lea eax,[r8-8]`; `008BFE5A lea eax,[r8-8]`. `+8` indexa dois arrays de ponteiros:
`008B3664 mov rbx,[rsi+8]` / `008B366F mov rdx,[r14+rbx*8]`; `008C0CDA movsxd rax,[rsi+8]`.

**`[outer+8]` — provado.** `0x88E8A0` (`0088E8C0 lea rbp,[rsp-0x35A8]`, rsp=entry−0x40)
guarda `0088FB9C mov [rbp+8],r14` com `r14 = [rbp+0x35F0] = [entry+8]` (home de `arg1`),
e `0088FB7D/BB1` gravam `outer+0x10 = arg1+0x1408`. `arg1` é o ctx: `0088E8D5 mov
eax,[rcx+0x2C30]` e `0x86FE90` escreve `[rdi+0x2C30]` em `00870933`. `0x88E8A0` passa
`008912FB lea r9,[rbp]` (4º arg) e `00891319 rcx=[rbp-0x50]` (=`ctx+0x1408`) para `0x8AB760`,
que em `008AB959 mov rcx,rsi` entrega `&outer` a `0x8ABAA0`; o consumidor lê
`008ABDEB mov rax,[rsi+8]` = ctx.

**Rust:** `checks/stage_c_rust.rs` (gerado por `tools/stage_c_rust.py`) — `BandDesc` com
`#[repr(C)]` e `assert!(size_of == 24)`, os 22 vetores estáticos e
`select_band_table(case)` com `_ => EMPTY` reproduzindo `0085EBA7 → 0x2752208`.

**`NÃO PROVADO`:** significado de `code`/`idx`/`kind`; identidade do objeto `arg3` de
`0x862E40` (só se provou que os casos vêm de `[arg3]`/`[arg3+8]`, dwords 0..0x16); os
elementos vivem no heap (fora do dump de 137 MB) — a ordem/valores vêm das listas estáticas.

## 19. FFT do IPP no caminho de áudio — PROVADO (2026-11-23)

> Corrige §5.1: `0x885040` **chama** a FFT (via `0x8B2680`), e a transformada é do IPP.
> `PLANO_MOTOR_AUDIO.md` §24.4 é a folha desta etapa.

### 19.1 Cadeia e RVAs

```
0x885040 00886A69 call 0x8B2680        ; 1 por amostra
0x8B2680 008B28D6 call 0x1010          ; FFT direta   -> 0x199B20E0 (RVA 0x20E0)
         008B2949 call 0x1010          ; 2º caminho
         008B28F6 call 0x1520          ; multiplicação espectral -> 0xBD40
         008B290F call 0x1280          ; FFT inversa  -> 0x199B7B40 (RVA 0x7B40)
         008B2929 call 0x1220          ; escala 1/n   -> 0x6160
```

Resolução dos stubs (leitura direta do dump): `dword [0x21C7408] = 4`;
`[0x21C5D48 + 4*8] = 0x199B20E0`; `[0x21C6088 + 4*8] = 0x199B7B40`.

### 19.2 Desmontagem — par forward/inverse

`0x20E0` e `0x7B40` têm 256 B cada e são o **mesmo wrapper**, exceto duas instruções:

| forward (`0x20E0`) | inverse (`0x7B40`) |
|---|---|
| `0000214A call qword ptr [rcx]` | `00007BAA call qword ptr [rcx+8]` |
| `000021B1 call qword ptr [rax+0x18]` | `00007C12 call qword ptr [rax+0x20]` |

```
// assinatura reconstruida de 0x20E0 (arg1=rcx, arg2=rdx, arg3=r8, arg4=r9)
if (!spec)              return -8;   // 000020F1 / 000021B9
if (spec->magic != 7)   return -13;  // 000020FA / 000020FF
if (!src || !dst)       return -8;   // 00002109 / 00002112
inner = spec->inner;                 // 0000211B
alt   = inner->alt;                  // 0000211F
if (alt && alt->kind == 3)           // 00002128
    return alt->fwd(src, dst, alt->data, buf);      // 000021A7..000021B1
u64 desc[2] = { 0x36, 0 };            // 00002130 / 00002142
return inner->vtbl->fwd(inner, src, dst, desc, buf); // 0000214A
```

O caminho especial (`alt->kind == 3`) **é o que o áudio usa**: `0006F5E5 mov dword
ptr [r12],3` grava o marcador e `0006F5ED mov [r14+0x18],r12` publica o objeto;
os kernels ficam em `alt+0x18` (fwd `0x72480`) e `alt+0x20` (inv `0x726A0`)
(`0006F502`..`0006F51B`). O caminho genérico (`call [rcx]`/`[rcx+8]` = descritor
`+0`/`+8` = `0x6F6A0`/`0x6F760`, `0006F603`/`0006F608`) não é exercitado com
`kind == 3`.

### 19.3 Constantes

| RVA | valor |
|---|---|
| `0x20FF` | `0xFFFFFFF3` (−13) |
| `0x21B9` | `0xFFFFFFF8` (−8) |
| `0x2130` | `0x36` |
| `0x8B272F` | `1.0f` lido de `0x2079F9C` |
| `0x8B28AA`/`0x8B28AD` | `shr rdi,1` / `inc rdi` → `bins = n/2+1` |
| `0x8B291C`/`0x8B2925` | `cvtdq2ps n` / `divss` → escala `1/n` |
| `0xBDE0`..`0xBDFD` | `vmovsd` / `vshufps 0xb1` / `vfmaddsub213ps` (par complexo) |

### 19.4 Estruturas

| Objeto | Offset | Prova |
|---|---|---|
| spec | `+0` i32 == 7 | `000020FA` |
| spec | `+8` ptr interno | `0000211B` |
| interno | `+0` vtbl forward | `0000214A` |
| interno | `+8` vtbl inverse | `00007BAA` |
| interno | `+0x18` ptr descritor alt. | `0000211F` |
| alt. | `+0` == 3, `+8` dado, `+0x18` fwd, `+0x20` inv | `00002128`, `000021AD`, `000021B1`, `00007C12` |
| estágio | `+0x18` i32 n | `008B2753` |
| estágio | `+0x140` posição (mask `n/2−1`) | `008B2761` |

Desdobramento medido em 2026-11-24 (init e kernels), tudo com RVA:

| Objeto | Offset | Prova |
|---|---|---|
| spec | `+0x10` = descritor (bloco de `0x340` B) | `000088CA lea r15,[rcx+r15+0x10]`; `000089A0 mov [r13+8],r15` |
| descritor | `+0` = fwd genérico `0x6F6A0`; `+8` = inv `0x6F760` | `0006F603`/`0006F608` (via `0006FF80` chamado em `0000899B`) |
| descritor | `+0x18` = objeto "alt" (marker 3) | `0006F5E5` `mov dword [r12],3`; `0006F5ED` `mov [r14+0x18],r12` |
| descritor | `+0x28` = tabela de init `0x21C69A0` | `00069CBE`/`00069CC5` |
| alt | `+8` = ctx (magic 6) | `0006F4B8` `lea rcx,[r12+8]` + `0x72180` grava `[rcx]=ctx` |
| alt | `+0x18..+0x40` = kernels fwd/inv/variantes | `0006F502`..`0006F51B` (`0x72480`,`0x726A0`,`0x72A40`,`0x72E20`,`0x73440`,`0x735E0`) |
| ctx | `+0` i32 = 6; `+4` = order; `+8` = flag; `+0x10` = escala f32 | `0007223D`/`000722FF`; `00072245`; `00072257` |
| ctx | `+0x18` = tamanho do workspace (0 p/ ordem ≤ 7) | `000723BE`; `0007244E` |
|ctx | `+0x30`/`+0x38`/`+0x50`/`+0x58` = tabelas | `00072381`; `000723A1`; `000723EC`; `00072402` |
| wrapper `0x72480` | `[ctx+4]` = order; kernels por ordem | `000724A5`; tabelas abaixo |

### 19.5 Rust

`checks/stage_fft_rust.rs` (compila com `rustc --edition 2021 --crate-type lib`): validação
magic-7, códigos `-13/-8/-2`, slots `[rcx]`/`[rcx+8]`, descritor `0x36`, `bins = n/2+1`,
escala `1/n`, multiplicação complexa interleaved de `0xBD40` na mesma ordem.

`checks/stage_j_fft.rs` (7 testes, `rustc --edition 2021 --test`) fixa o que foi medido em
2026-11-24: tabela ordem→kernel (com `ctx+8 == 0`, que é o caso do áudio), slots do wrapper,
magic do ctx, e **vetores-ouro bit-exatos** em `checks/fft_golden.rs` para ordens 6..9 e três
entradas (`impulse`, `cos`, `ramp`), colhidos por `checks/fft_probe.rs`.

`checks/j4_fft.rs` (13 testes) é a **transcrição literal** do caminho real:
`kernel6` (`0x8BFE0`, 32 pontos complexos), `kernel7` (`0x8C280`, 64 pontos), `split_ccs`
(`0x895C0`, caminho rápido `len < 0x40000` **e** caminho lento `len >= 0x40000`,
`split_ccs_slow`), `pack_dc_nyq` (`000725F6`..`00072617`) e o
`move` final (`0007262E`..`0007263C`). Cada vetor é um `ymm`, cada helper é a instrução AVX
(`shuf`=`vshufps`, `perm`=`vperm2f128`, `fma132`/`fma213`/`fnmadd231`/`addsub`) e as
constantes são os **bits** de `0x1DFD120`/`0x1DFD3C0`/`0x1DFD3D0`, `0x1DFCFA0..0x1DFD100`
(kernel 6) e `0x1DFD140..0x1DFD3A0` (kernel 7).

Prova: `checks/fft_stage_probe.rs` chama cada peça isolada no plugin (read-only) e grava
`checks/.build/j4_stage_<ordem>.bits` (`SRC`/`KD`/`MAN`/`FWD`/`TW`); `tools/gen_j4_golden.py`
gera `checks/j4_golden_<ordem>.rs`. Resultados: `kernel6` e `kernel7` batem **bit a bit**
com `KD`; a cadeia `kernel → pack → split → move` bate **bit a bit** com `0x20E0` (`FWD`,
`diffs = 0` para ordens 6 e 7) e com os vetores independentes de `checks/fft_golden.rs`.

**Kernel genérico `0x1D69E00` (o do áudio) — FECHADO bit a bit para as ordens 8..19 (2026-11-24).**
É uma **FFT complexa de `m = n/2`** sobre os pares intercalados `(src[2t], src[2t+1])`, saída
intercalada em ordem natural e sem escala (prova em §19.6). `checks/j4_fft.rs` traz a transcrição
literal **por estágio**, com o mesmo corpo reaproveitado pelas ordens:

* `kernel_stage1` (`01D69EAC`..`01D6A16A`), `R = n/2` **bytes**; roda `n/128` iterações
  (`idx[16], idx[32], …` até o `0` sentinela em `01D6A04B`/`01D6A167`);
* `pass2` (`01D6B03A`..`01D6B20C`), bloco-local de 8 slots, `rdx/32` iterações de 0x100 B;
* `stage16` (`01D6B8C9`..`01D6BA2C`), `r11>>2` blocos × `[rsp]/8` passos radix-4
  (`pass3a_step`, `01D6B901`..`01D6BA0B`), no lugar;
* `radix8_levels` (`01D6B249`..`01D6B585`) e `radix8_final` (`01D6BD19`..`01D6BD14`), que
  compartilham o mesmo corpo radix-8 (`01D6B28C`..`01D6B55F` / `01D6BD41`..`01D6C0C7`), com
  `vmulps` por `0x3f3504f4`/`0xbf3504f4` (`0x797B640`/`0x797B660`, lidos do dump);
* `radix4_final` (`01D6BB87`..`01D6BD14`);
* `kernel_generic` reproduz o despacho de `01D6B225` (`rdx` 0x40/0x80/0x100/senão) e o
  re-despacho de `01D6B89E` (`r11` 4/8/0x10/>0x10).

Provas: `orders_8_10_11_12_are_bit_exact` compara **KD, WS e FWD bit a bit** para ordens 8, 9,
10, 11 e 12; os testes de ordem 9 (`kernel9_workspace_matches`, `kernel9_is_bit_exact`,
`order9_chain_is_bit_exact`, `order9_matches_probe_golden`) continuam verdes — **13/13**.
Vetores medidos em `checks/j{8,9,10,11,12}_golden.rs` (`SRC/KD/WS/FWD/IDX/TW38/TW50`, via
`checks/fft_generic_probe.rs`, modos `rand`/`imp`/`eN`). O tamanho de `TW38` é
`tw50_ptr − tw38_ptr` = `0x400 << (order−8)` bytes (ordem 12 = **0x4000**, não 0x8000).

**Caminho `rdx > 0x800` (`kernel_large`, ordens 13..19) — FECHADO bit a bit (2026-11-24).**
Driver literal `01D6A18B`..`01D6B035`: fatia `rdx = n/2` em blocos de `0x800` complexos
(`0x1000` floats); por bloco roda `pass2` (`01D6A1EB`, `r10==4`), depois
`stage16`/`radix8_levels` conforme `mask = rdx & 0x55555555` e `r10`
(`01D6A3E9`/`01D6A6B0`), com `r10`/`sub28`/`r11` recalculados
(`01D6A3CA`/`01D6A3D6`/`01D6A6A6`); ao fim dos blocos, os estágios finais sobre o array
inteiro (`01D6AD77`): `stage16` enquanto `[rsp+0x28] != 4`, então `radix4_final`
(`01D6BB87`). `rdx` nunca é modificado no laço, logo `mask` usa sempre o `n/2` original.
Parâmetros finais por ordem: 13→`radix4_final(0x400)`; 14→`radix4_final(0x800)`;
15→`stage16(0x400,16)`+`radix4_final(0x1000)`; 16→`stage16(0x800,16)`+
`radix4_final(0x2000)`; 17→`stage16(0x400,64)`+`stage16(0x1000,16)`+
`radix4_final(0x4000)`; 18→`stage16(0x800,64)`+`stage16(0x2000,16)`+
`radix4_final(0x8000)`; 19→`stage16(0x400,256)`+`stage16(0x1000,64)`+
`stage16(0x4000,16)`+`radix4_final(0x10000)`. Validação: goldens
`j13..j19_stage_rand.bits` com **dst e ws, 0 divergências** em todas as sete ordens, e
`rfft_generic` `FWD bad=0` nas ordens 13..19 (16..18 no split rápido, 19 no lento).

### 19.6 `NÃO PROVADO` / corrigido em 2026-11-24

**Correção material:** o packing **não** é `RToPerm`/`RToPack`; é a forma "CCS" com
`n/2+1` pares `(re,im)` em **ordem natural** e `Im(DC) = Im(Nyquist) = 0`. Medido no próprio
plugin (`checks/fft_probe.rs`, ordem 9, impulso): `dst[0..2] = (1,0)`, `dst[2..4] = (1,0)`, …,
`dst[n..n+2] = (1,0)`; para `cos(2π·3·i/n)` o único pico é `dst[6..8] = (255.99998, ~0)`
e `dst[1] = dst[n+1] = 0` bit a bit. O argumento antigo ("`0xBD40` percorre todos os bins,
logo CCS está fora") não se sustenta: o par 0 é `(DC, 0)` e é multiplicado como qualquer par.

**Kernels por ordem** (com `flag = 8`, que grava `ctx+8 = 0` em `0007245C..00072470`):

| order | kernel | prova |
|---|---|---|
| 0..4 | `0x1DFA2F8[order]` | `00072552 je` → `0007257C` → `0007258C` |
| 5..7 | `0x1DFA358[order]` | idem |
| 6 | `0x8BFE0` (FFT complexa de 32 pontos, unrolled) | tabela / medido |
| 7 | `0x8C280` (FFT complexa de 64 pontos) | tabela / medido |
| 8..0x13 | `0x1D69E00` | `0007259B` → `000725D6` |
| >0x13 | `0x88300` | `000725A1` → `000725AE` |

O comprimento do kernel complexo é `2^(order−1)` (`00072543 lea r9d,[r15-1]`,
`00072547 shlx r14d,r13d,r9d`), ou seja, `n/2`; a pós-passagem real/CCS é `0x895C0`
(`00072620 call 0x895C0`) e o remanejamento de DC/Nyquist está em `000725F6`..`0007263F`.

**Ordens 13..19 (`rdx > 0x800`) — transcritas em 2026-11-24 (correção desta seção).** Em
`01D6A17E cmp rdx,0x800` / `01D6A185 jle 0x1d6b03a`, `rdx > 0x800` desvia para `01D6A18B`, um
bloco de ~720 linhas (`01D6A18B`..`01D6AD24`) com quatro variantes desenroladas, escolhidas em
`01D6A1BF`..`01D6A1E6`: `r10 == 4` → `01D6A1EB`; `r11 (=0x200) < 4` → `01D6AD25`;
`rdx & 0x55555555 != 0` → `01D6A3E9`; `r10 == 0x10` → `01D6A6B0`; senão `01D6A3E9`. O caminho
está em `kernel_large` (parágrafo acima) e cobre `rdx` até `0x40000` (ordem 19); acima disso o
plugin desvia para `0x88300`. Continuam `NÃO EXTRAÍDO`: `0x88300` (ordem > 0x13, inalcançável
para o áudio — `N ≤ 1115` → ordem 11; `0007259B`/`000725A1..000725AE`) e os
geradores de twiddle (`0x806E0`/`0x876E0`/`0x87AA0`) — as tabelas usadas são as **medidas** do
plugin.

**Extraído e validado bit a bit em 2026-11-24:** `0x8BFE0` (ordem 6) e `0x8C280` (ordem 7),
mais o split `0x895C0` (caminho rápido **e** lento), o `pack` de DC/Nyquist e o `move` final —
ver §19.5 (`checks/j4_fft.rs`, 13 testes) e `checks/fft_stage_probe.rs` (`diffs = 0` na cadeia
manual contra `0x20E0`, para ordens 6 e 7).

**PROVADO em 2026-11-24 (medição):** `0x1D69E00` é uma **FFT complexa de `m = n/2`** sobre os
pares intercalados `(src[2t], src[2t+1])`, saída **intercalada em ordem natural**, **sem
escala**. Três medições independentes (`checks/fft_generic_probe.rs`, read-only, ordem 9,
`m = 256`): (a) entrada aleatória → `max abs(KD − CFFT_256) = 2.794e-06` em f64; (b) `src[0]=1`
(complexo `1`) → `KD[2k]=1`, `KD[2k+1]=0` para todo `k`; (c) `src[1]=1` (complexo `i`) →
`KD[2k]=0`, `KD[2k+1]=1` para todo `k`. O caso (c) refuta o layout "split" (`[re…, im…]`) e
prova que a entrada é intercalada. A conversão para CCS de tamanho `n` é a `0x895C0`
(`00072620`), precedida de `pack_dc_nyq` (`000725F6`..`00072617`) — coerente com o truque
`Z = FFT_{n/2}(x[2t] + i·x[2t+1])`.

Mapa do caminho do áudio (`rdx = 0x100`), por instrução: entrada `01D69E80`..`01D69EA7`
(`rbp=rdx`, `r12=src`, `r13=ws`, `r14=ws+2·rbp`, e `ws=dst` quando `src!=dst` e `dst`
alinhado, `01D69E8E`); 1ª passada `01D69EAC`..`01D6A16A` (4 iterações; índice em `01D6A04B`
com `r11+=0x40` e `rbx = src + idx*32`; `idx[16]=4`, `idx[32]=2`, `idx[48]=6`, `idx[64]=0`
como **sentinela**, fatias 0/16/8/24 complexos). Cada iteração `i` grava **8 grupos de 16
floats**, nos offsets `16i, 64+16i, 128+16i, 192+16i, 256+16i, 320+16i, 384+16i, 448+16i`
(`r13` anda `+0x40` por iteração; `r14=r13+0x200`; `+rbp*4` = `+0x400`); as quatro borboletas
leem `base+{0,256,128,384}`, `base+{64,320,192,448}`, `base+{8,136,264,392}` e
`base+{72,328,200,456}` **em floats** (`01D69EDD`..`01D69EF9`, `01D69F6B`..`01D69FAD`).
`01D6A170`..`01D6A185`: `r11=rdx>>2`, `rdx<=0x800` → `01D6B03A`; 2ª passada
`01D6B03A`..`01D6B20C` (`r11=(rdx>>2)>>2=16`, `sub r11,2` → 8 iterações de 64 floats, 6
twiddles `dup4` de `tw[0..0x60)`, 8 slots de 8 floats em `+0,0x20,…,0xe0`, **bloco-local**);
despacho `01D6B212`..`01D6B249` (`rbx += 0x60`, `r10=0x10`; `m=0x40`→`01D6BB87`,
`m=0x80`→`01D6BD19`, `m=0x100`→`01D6B8C9`, senão `01D6B249`).

3ª passada (só `m=0x100`, `01D6B8C9`..`01D6BA2C`): `r11=rdx>>6=4` blocos, `r10=0x80`,
`rax=0x180`; `r12=r13=ws` (**no lugar**); por bloco o twiddle **reinicia** em `rcx`
(`01D6B8FA mov rbx,rcx`, `rcx=tw+0x60`) e avança `+0xc0` por passo (`01D6B987`), 2 passos por
bloco (`r12=0x10`, `sub r12,8`); `r13 += 0x40` por passo (`01D6BA12`) e `+= rax` por bloco
(`01D6BA20`); offsets `o+{0x00,0x20,0x80,0xa0,0x100,0x120,0x180,0x1a0}`. Epílogo
`01D6BA2C mov rcx,rbx` (→ `tw+0x1e0`), `01D6BA2F jmp 01D6BB70`, `shl r10,2` (→ `0x40`).

4ª passada (`01D6BB87`..`01D6BD14`): `r10=0x40<<3=0x200`, `rax=0x600`, 8 iterações
(`r11=0x40`, `sub r11,8`); lê `ws` (`x0` em `+0/+0x20`, `B` em `+0x200/+0x220`, `A` em
`+0x400/+0x420`, `D` em `+0x600/+0x620`) e escreve `dst` intercalado via
`vunpcklps`/`vunpckhps`/`vperm2f128(0x20/0x31)` (`01D6BC7C`..`01D6BCFB`) em
`dst+{0,0x20,0x200,0x220,0x400,0x420,0x600,0x620}`; twiddles a partir de `tw+0x1e0`,
`+0xc0` por iteração (`01D6BC26`). Epílogo `01D6C0E7`.

Twiddles (`ctx+0x38`, medidos): `tw[0..4] = cos(0, π/8, π/4, 3π/8)`, `tw[4..8] = −sin` dos
mesmos ângulos (`W8^0..W8^3`), `tw[8..16] = W8^{2k}`, `tw[16..24] = W8^{3k}`; de `tw[24]` em
diante tabela de 64 pontos com passo `π/64` (cos em `24+8j`, `−sin` em `32+8j`). A 4ª passada
lê até `tw+0x7df` (última iteração `tb=0x720`, `+0xa0`, 32 B), então a tabela tem **≥0x7e0 B**;
o probe lê `0x800` B (512 f32). O valor `0x660` B antes registrado era o ponteiro final da 3ª
passada, não o tamanho da tabela.

**Continua `NÃO EXTRAÍDO`:** `0x88300` (ordens > 19; inalcançável para o áudio, §24.5-(3));
os geradores de twiddle (`0x806E0`, `0x876E0`, `0x87AA0`) e o construtor de ctx `0x72180`
(campos medidos, corpo não transcrito). Os caminhos `01D6BD19` (ordem 8), `01D6B249`
(ordens 10..12), `radix4_final` com `m=0x40` (ordem 7 dentro do genérico — não usado porque a
ordem 7 vai para `0x8C280`), `rdx > 0x800` (ordens 13..19) e o split lento de `0x895C0`
(`0000897A0`, `len >= 0x40000`) **estão fechados** — ver o mapa acima e `checks/j4_fft.rs`
(13 testes).

O que a segunda rodada (2026-11-24) **acrescentou como prova** (mantido):

- `n = [estágio+0x18]` (`008B2753 movsxd r15,[rax+0x18]`);
- máscara de posição `n/2−1` (`008B275A shr rbx,1`, `008B275D lea rax,[rbx-1]`,
  `008B2761 test [rsi+0x140],rax`);
- `bins = n/2+1` (`008B28AA shr rdi,1`, `008B28AD inc rdi`) passado ao multiplicador
  (`008B28E2 mov r8d,edi`);
- inversa com `n` (`008B291F mov r8d,r15d`) e escala `1/n` (`008B291C cvtdq2ps`,
  `008B2925 divss`, `008B2929 call 0x1220`);
- `0xBD40` percorre todos os bins desde 0 (`0000BDCC xor r10d,r10d`, `0000BDE0 vmovsd
  xmm3,[rdx+r10*8]`), 8 B por bin, **sem** packing DC/Nyquist — o que é coerente com o par
  0 ser `(DC, 0)` e com a multiplicação tratar todos os `n/2+1` pares.

O item "CCS está excluído" acima está **refutado pela medição** (ver o começo desta seção):
o layout é exatamente `n/2+1` pares em ordem natural, com DC e Nyquist reais. `RToPerm` e
`RToPack` ficam descartados; não há permutação de bins.
