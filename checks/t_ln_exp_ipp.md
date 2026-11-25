# M3 — `ln` (`0x293760`) e `exp` (`0x240C00`) da IPP, bit a bit (2026-11-25)

Fonte: `dumpsooth/nyx_soothe3_dump.bin` (SHA-256 `68D30368…F55C`). Desmontagem:
`checks/293760.dis`, `checks/293f80.dis`, `checks/240c00.dis`, `checks/2414c0.dis`
(`tools/dis_range.py`). Port: `port/src/ippmath.rs`. Conferência:
`checks/j_ln_exp_avx.rs`.

## 1. Despacho

| Stub | Tabela `[0x21C7408]=4` | Destino | Impl |
|---|---|---|---|
| `0x1C8500` (ln) | `0x21C6AA8[4]` = `0x1C8A00` | `[0x21C70E8]` | **`0x293760`** (2.080 B) |
| `0x1C84A0` (exp) | `0x21C6A28[4]` = `0x1C8880` | `[0x21C6F08]` | **`0x240C00`** (2.240 B) |

Os cinco valores são lidos do dump e conferidos em `check_consts` de
`checks/j_ln_exp_avx.rs`. Os ponteiros usam VA na base `0x199B0000`. O índice
`4` é o mesmo de M2.

## 2. Assinatura e despacho por `n`

- `rcx = src`, `rdx = dst`, `r8d = n` (`002937A4`/`00293798`/`00293775`;
  `00240C44`/`00240C38`/`00240C15`).
- Retorno:
  - `n <= 0` → `0xFFFFFFFA`;
  - ponteiro nulo → `0xFFFFFFF8`;
  - senão, `eax = r15d`, que é o status da **última** lane especial com
    status `≠ 0`, em ordem crescente de índice.
- **ln:**
  - blocos de 16 (`n & ~15`, `0029378C`), em duas metades de 8;
  - máscaras especiais combinadas como `esi | edi<<8` (`002939D9`);
  - cauda em pedaços de `min(n−i, 8)`, com carga mascarada (máscara em
    `0x1ECA980 + 32·cnt`), padding `0.75` (`0x1ECAF40`) e escrita mascarada
    (máscara em `0x1ECAAC0 + 32·cnt`).
- **exp:**
  - blocos de 32 (`n & ~31`, `00240C2C`), em quatro quartos;
  - máscaras combinadas em `00240F12..00240F22`;
  - cauda com máscaras `0x1E6F940`/`0x1E6FA80` e padding `0.75` (`0x1E6FF80`).
- **Lanes especiais:** a entrada é salva em pilha e refeita pela função
  escalar (`0x293F80` / `0x2414C0`).
  - Se o status é `≠ 0`, o binário chama `0x2D74A0`, que é `endbr64; ret`
    (provado em M2), e o valor fica o da escalar.
  - Por isso o valor de cada lane **não depende** de `n` nem do alinhamento.
- **MXCSR:** forçado a `RN, FTZ=DAZ=0` e restaurado no fim, igual a M2
  (`00293852..0029388A`, `00240CF5..00240D2D`).

## 3. ln — lane vetorial (`002938F3`..`002939CF`)

`i = bits(x)`. A lane é especial quando `(i + 0x00800000) <s 0x01000000`
(`002938F3`/`0029390F`). Isso pega ±0, denormais, negativos, ±inf e NaN. Só
os normais positivos finitos seguem pela conta abaixo:

```
t  = i − 0x3F2AAAAB                       002938FD vpsubd
e  = (float)(t >>s 23)                    00293905 / 0029392B
m  = bits((t & 0x7FFFFF) + 0x3F2AAAAB)    00293901 / 0029390B   (m ∈ [2/3, 4/3))
f  = m − 1                                00293930
p  = CC0·f + CA0 ; ·f+C80 ; ·f+C60 ; ·f+C40 ; ·f+C20 ; ·f+C00   (FMA, 00293957..002939A9)
r  = f·p ; r = r·f + f                    002939B3 vmulps / 002939BD FMA
y  = e·ln2 + r                            002939CF FMA
```

Constantes, em bits:

| RVA | Bits | Valor |
|---|---|---|
| `0x1ECAC00` | `BF000000` | −0,5 |
| `0x1ECAC20` | `3EAAAEE7` | |
| `0x1ECAC40` | `BE80061D` | |
| `0x1ECAC60` | `3E4AFB81` | |
| `0x1ECAC80` | `BE289358` | |
| `0x1ECACA0` | `3E2DB86B` | |
| `0x1ECACC0` | `BE1B6A22` | |
| `0x1ECAE40` | `3F317218` | ln 2 |

## 4. ln — lane especial `0x293F80` (f64)

- **Expoente f32 = 0xFF:**
  - só −inf → `0/0` em f64 → `0xFFC00000` ("real indefinite"), status `0x13`;
  - os demais (+inf e qualquer NaN) → `x·x` (`002941E3`).
- **±0:**
  - `d = (double)x`; o expoente f64 é zero, então `d·2^60` e `adj = −60`
    (`00293FC1`);
  - `d ≤ 0` (`00293FDD`) e `d == 0` → `(−1)/(+0) = −inf`, status `0x12`;
  - negativo → `0/0`, status `0x13`.
- **Positivo** (aqui só denormais):
  - `z = d − 1`;
  - se `|z| ≤ 0.009765625` (`0x1ECB598`): `y = P(z)·z² + z` (`0029413A..0029417C`);
  - senão:
    - `m` é `d` com o expoente trocado para `0x3FF`;
    - `e = adj + exp − 0x3FF`;
    - `j = low32(m + (2^46+1)) & 0x7F`, com `j ∈ 0..=64`;
    - lê `[c, a, b]` de `0x1ECAF60 + 24·j` (65 entradas);
    - `hi = ln2hi·e + a`;
    - `lo = e·ln2lo + b`;
    - `mh = (m + 2^21) − 2^21`;
    - `ml = m − mh`;
    - `rh = mh·c − 1` (FMS, `002940CD`);
    - `t = c·ml`;
    - `hi += rh`;
    - `r = rh + t`;
    - `lo = t + lo`;
    - `y = hi + (P(r)·r² + lo)`, com `P` de grau 6 (`0x1ECB5B8..0x1ECB5E8`);
    - por fim, `vcvtsd2ss` (RN).
- A tabela é copiada **byte a byte** do dump para `LN_TAB` (65 × 3 u64).

## 5. exp — lane vetorial (`00240D96`..`00240F0D`)

A lane é especial quando `(bits & 0x7FFFFFFF) >s 0x42AEAC4F` (`|x| > 87.33654`,
inf, NaN; `00240DD3`). Senão:

```
t  = log2e·x + 1.5·2^23                   00240D96 FMA   (0x3FB8AA3B, 0x4B400000)
k  = t − 1.5·2^23                         00240DAA
r  = −(ln2hi·k) + x                       00240E2B FNMA  (0x3F317200)
r  = −(k·ln2lo) + r                       00240E4F FNMA  (0x35BFBE8E)
p  = C5·r + C4 ; ·r+C3 ; ·r+C2 ; ·r+C1 ; ·r+C0           (FMA, 00240E75..00240EE5)
y  = bits( (bits(t) << 23) + bits(p) )    00240DE0 vpslld / 00240F00 vpaddd (inteiro)
```

Constantes `C0..C5`:

| RVA | Bits |
|---|---|
| `0x1E6FD00` | `3F800000` |
| `0x1E6FD40` | `3F7FFFFE` |
| `0x1E6FD80` | `3EFFFF34` |
| `0x1E6FDC0` | `3E2AACAC` |
| `0x1E6FE00` | `3D2B8392` |
| `0x1E6FE40` | `3C07D9FE` |

## 6. exp — lane especial `0x2414C0` (f32, **sem** FMA na redução)

- **Expoente 0xFF:** −inf → `+0` (grava `eax = 0`, `002416FB`); os demais →
  `x·x`.
- **Limites:**
  - `x > 88.72283` → `FLT_MAX²` = +inf, status `0xC`;
  - `x < −103.97208` → `tiny²` = +0, status `0x11`.
- **Redução**, com arredondamentos separados:
  - `k` vem de `x·log2e + 1.5·2^23` (`vmulss` + `vaddss`) e é a palavra baixa
    com sinal (`0024153F movsx`);
  - `r = (x − kf·hi) − kf·lo`, só com `vmulss`/`vsubss`.
- **Polinômio:** `P5..P2` e duas vezes `1.0000001` (`0x3F800001`), em FMA.
- **Escala:** `s = bits(e << 23)`, com a palavra baixa zerada.
  - Se `x < −87.33654`: `y = p·2^(k+60)·2^−60`, status `0x11`.
  - Senão, se `k + 127 ≤ 254`: `y = p·2^k`.
  - Senão: `y = p·2^(k−1)·2`.

## 7. Prova

`checks/j_ln_exp_avx.rs` reescreve as quatro funções com intrinsics AVX2/FMA e
SSE2/FMA, instrução por instrução, com o RVA em cada linha. Constantes,
máscaras e a tabela são lidas do dump em tempo de execução. O emulador é
comparado com `ippmath.rs`:

- **Amostral** (runner): 33.894 lanes por função, de tamanhos 1..70 e
  255/256/257/513, com valores aleatórios no domínio inteiro, especiais e
  faixa [−110, 110]. Inclui MXCSR do chamador com FTZ+DAZ+RZ.
  - Resultado: `bad = 0` nas duas funções, e o MXCSR é sempre restaurado.
- **Mutações de controle**, todas detectadas:

  | Mutação | ln | exp |
  |---|---|---|
  | Sem a lane especial | 6.312 lanes | 5.012 lanes |
  | FMA partido em `002939BD` (ln) / `00240EE5` (exp) | 30 lanes | 812 lanes |

- **Exaustivo 2^32** (`--exhaustive`, com `-O -C target-feature=+fma`):
  ver §7.1.

**A IPP difere da libm.** No lote amostral, o `ln` difere de `f32::ln` em
5.074/51.400 lanes, e o `exp` difere de `f32::exp` em 26.242/51.400. Ou seja,
o `f32::ln`/`f32::exp` que o port usava antes de M3 **não** era bit a bit; as
curvas de `engine.rs` (`0x88E130`) mudam de bits com a troca.

**Sem dependência de CPU:** ao contrário de M1/M2, não há `vrcpps`; só operações
IEEE com RN. O resultado vale em qualquer CPU com FMA, e `f32::mul_add` em
software também está correto.

### 7.1 Exaustivo

`checks/.build/j_ln_exp_avx_fma.exe --exhaustive` (log em
`checks/.build/m3_exhaustive.log`) percorre todos os padrões de bits, em
chamadas de 4.096 (blocos inteiros).

| Função | Entradas | `bad` | NaN na saída | Difere da libm |
|---|---|---|---|---|
| ln | 2^32 | **0** | 2.155.872.254 | 92.579.785 |
| exp | 2^32 | **0** | 16.777.214 | 94.993.725 |

- `bad` conta lanes e `eax`, comparando os bits exatos (o payload de NaN entra).
- No ln, os NaN da saída vêm de todos os negativos e dos NaN de entrada.
- A última coluna compara os bits com `f32::ln`/`f32::exp` e não conta casos em
  que os dois lados dão NaN.

## 8. Resíduo `NÃO PROVADO`

- **Outros caminhos de CPU:** o índice `4` de `0x21C7408` é o valor gravado no
  dump. Os caminhos dos índices 0..3 (outras CPUs) não foram lidos, como em M2.
- **Status ignorado:** o port descarta o status (`eax`) em `ipp_ln`/`ipp_exp`.
  Falta conferir, no dump, que **todos** os chamadores do motor ignoram o
  `eax` (`0x88E130` em `0088E298`/`0088E2EE`/`0088E3B7`; F3 em
  `008B6573`/`008B7805`/`008B84D3`; `008B90D7`). Isso entra em M5, com o miolo.
