# S — recíproco de `0x88E130`: `0x1C8530` → `0x29B260` (M2, 2026-11-25)

> Fecha a etapa M2 do `PLANO_MOTOR_AUDIO.md` §26. Toda afirmação tem instrução + RVA em
> `checks/29b260.dis` (`0x29B260`–`0x29B9A0`, 1.856 B pelo `.pdata`, 383 linhas) e
> `checks/29b9a0.dis` (lane especial). Os dois foram gerados do dump
> (`dumpsooth/nyx_soothe3_dump.bin`, SHA-256 `68D30368…F55C` conferido nesta sessão) com
> `tools/show_func.py`. Port: `port/src/rcp.rs`. Conferência: `checks/j_rcp_avx.rs`.
> O que não foi lido fica `NÃO PROVADO` no §6.

---

## 1. Despacho (CPU path) — PROVADO

```
001C8530  movsxd rax,[0x21C7408]          ; = 4 (dump)
001C8537  lea    r10,[0x21C6AE8]
001C853E  jmp    [r10+rax*8]              ; [0x21C6B08] = 0x19B78AC0 -> 0x1C8AC0
001C8AC0  endbr64
001C8AC4  mov    rax,[0x21C71D8]          ; = 0x19C4B260 -> 0x29B260 (base 0x199B0000)
001C8ACB  jmp    rax
```

Tabela `0x21C6AE8` no dump: índices `0..4` = `0x1C8A40`, `0x1C8A60`, `0x1C8A80`, `0x1C8AA0`,
`0x1C8AC0` (`[0x21C6B10] = 0x19B78AE0`, `[0x21C6B18] = 0`). Os stubs `0..3` saltam para
`[0x21C7138]`/`[0x21C7160]`/`[0x21C7188]` = `0x297EE0` e `[0x21C71B0]` = `0x299C60` — **não
lidos** (o dump fixou o índice `4`). O corpo usa AVX2 (`vpsubd ymm`), FMA, BMI2 (`shrx`) e
POPCNT. `0x29B260` retorna direto para `0x88E130` (o stub é `jmp`).

Sítio em `0x88E130` (`checks/88e130.u8.dis`), **in-place**:

```
0088E316  movaps xmm1,[rsi]               ; {ptr, ?, n}
0088E31D  movq   rcx,xmm1                 ; src = ptr
0088E327  mov    rdx,rcx                  ; dst = src
0088E32A  movd   r8d,xmm0                 ; n = dword [rsi+8]
0088E32F  call   0x1c8530
0088E334  movaps xmm1,[rsi]               ; eax não é lido até 0088E352 call 0x12e0
```

## 2. Assinatura, entrada e retorno — PROVADO

`rcx = src` (`0029B2A4 mov r14,rcx`), `rdx = dst` (`0029B298 mov r12,rdx`), `r8d = n`
(`0029B275 mov ebp,r8d`). `n <= 0` → `eax = 0xFFFFFFFA` (`0029B30E`/`0029B310` →
`0029B971`); `src` ou `dst` nulo → `0xFFFFFFF8` (`0029B316`..`0029B322` → `0029B90B`).
Senão `eax = r15d` (`0029B5FC`): `0` (`0029B2B0`), ou `0x12` se alguma lane foi `±0`
(`0029B8E0`/`0029B7A1`).

## 3. Aritmética — PROVADO

**Teste de lane especial** (`0029B3DE`..`0029B40A`, `0029B546`/`0029B54A`/`0029B55C`):

```
t       = (bits(x) − [0x1ED0500]) & [0x1ED04C0]     ; vpsubd / vpand
special = t >s [0x1ED0540]                          ; vpcmpgtd (com sinal)
```

| RVA | Valor (8 lanes iguais) | Papel |
|---|---|---|
| `0x1ED0500` | `0x00800000` | subtraendo |
| `0x1ED04C0` | `0x7FFFFFFF` | valor absoluto |
| `0x1ED0540` | `0x7DFFE800` | limite |
| `0x1ED05C0` | `0x3F800000` (`1.0`) | `1` do FMA |
| `0x1ED0600` | `0x3F400000` (`0.75`) | padding da cauda |
| `0x1ED0620` | `0x3F800000` (escalar) | dividendo de `0x29B9A0` |
| `0x1ED0240 + 32·c` | `c` lanes `0xFFFFFFFF`, resto `0` (`c = 0..8`) | máscara de carga |
| `0x1ED0380 + 32·c` | idem | máscara de escrita |

⇒ lane **normal** sse `|bits(x)| ∈ [0x00800000, 0x7E7FE800]`; **especial**: `±0`, denormal,
`|x| > 0x7E7FE800`, `±inf`, NaN.

**Lane normal:**

```
0029B40E  vrcpps       ymm12,ymm4            ; r0 = rcp(x)
0029B442  vfnmadd231ps ymm8,ymm4,ymm12       ; e = 1 − x·r0   (ymm8 = [0x1ED05C0])
0029B456  vfmadd213ps  ymm8,ymm12,ymm12      ; r = e·r0 + r0
```

(cauda: `0029B542`, `0029B552 vfnmadd231ps ymm6,ymm10,ymm5`, `0029B557 vfmadd213ps
ymm6,ymm10,ymm10` — a mesma conta.) Um único passo de Newton com FMA.

**Lane especial** — `0x29B9A0(&x, &r)` chamado por lane (`0029B899`, `0029B756`):

```
0029B9B0  vcmpeqss xmm4,xmm2,xmm3            ; x == 0
0029B9B5  vdivss   xmm1,xmm0,xmm2            ; r = 1.0f / x   (IEEE)
0029B9C1  and      eax,0x12                  ; status
```

Com `status ≠ 0` grava `dst[i] = r`, chama `0x2D74A0` e relê `dst[i]` (`0029B8A2`..`0029B8E3`,
`0029B763`..`0029B7A4`). `0x2D74A0` = `002D74A0 endbr64` / `002D74A4 ret` ⇒ nada muda:
`1/±0 = ±inf`. Em ordem de lane (`0029B820 bt esi,edi`, `0029B6C0 bt esi,ebx`).

## 4. Despacho por `n` e alinhamento — PROVADO

- Blocos de 32: `ebx = n & ~31` (`0029B28C`), 4 `vmovups` de 8 (`0029B3C3`..`0029B3D7`),
  laço `0029B3C0`..`0029B4A3`.
- Cauda, pedaços de `c = min(n − i, 8)` (`0029B502`..`0029B50A`), `esi = 0xFFFFFFFF >> (32−c)`
  (`0029B513 shrx`), carga mascarada (`0029B536 vmaskmovps`) com padding `0.75`
  (`0029B53C vblendvps`), escrita mascarada (`0029B57E`). Laço `0029B500`..`0029B586`.
- **Sem cabeça de alinhamento:** só `vmovups`/`vmaskmovps`. A conta é por lane, o padding
  (`0.75`, normal) é descartado ⇒ **o valor de cada lane não depende de `n` nem do
  alinhamento**; o `n` de `0088E32A` (`[rsi+8]`) não muda resultado algum.

## 5. MXCSR — PROVADO

```
0029B355  vstmxcsr [rsp+0x300] ; ecx = mxcsr
0029B367  and esi,0xffc0 ; 0029B36D cmp esi,0x1f80 ; 0029B373 je
0029B37A  and esi,0xffff003f ; 0029B380 add esi,0x1f80 ; 0029B38D vldmxcsr   ; RN, FTZ=DAZ=0
0029B59F  (se trocou) restaura ecx           ; 0029B5A6
0029B5C1  (senão) test dl,0x1f -> and edx,0xffffffe0 ; 0029B5D0               ; limpa flags 0..4
```

A conta roda sempre com MXCSR `0x1F80` nos bits de controle, independente do host. O port
transcreve (`rcp::mxcsr_enter`/`mxcsr_leave`, `stmxcsr`/`ldmxcsr` por `asm!`). O x87
(`0029B328`..`0029B34B`, `0029B58C fnclex`, `0029B593 fldcw`) não é transcrito: nenhuma
instrução x87 faz conta no corpo.

## 6. Port e conferência (2026-11-25)

- `port/src/rcp.rs` — `inv_32f`, `inv_32f_in_place`, `is_special`, `special_lane`,
  MXCSR; 7 testes. `port/src/engine.rs::shelf_curve_in_place` chama
  `rcp::inv_32f_in_place` em `0088E32F` (o loop por amostra foi partido em dois em volta
  da passada, como no binário; cada passada é elemento a elemento).
- `checks/j_rcp_avx.rs` — emulador por intrinsics de `checks/29b260.dis`/`29b9a0.dis`
  (RVA por linha), **constantes e tabelas lidas do dump em tempo de execução** e
  comparadas com as do port, mais a cadeia `[0x21C7408]`/`[0x21C6B08]`/`[0x21C71D8]`.
  Veredito **estrito** (bits iguais inclusive sinal/payload de NaN, e `eax` igual):
  - 16.320 chamadas, `n = 1..80, 255..258, 513`, 8 alinhamentos de `src` × 4 de `dst`,
    in-place e não, bits aleatórios / especiais / domínio de `0088E32F` (`1 + e`, `e ≥ 0`),
    1/6 das chamadas com MXCSR do chamador `FTZ+DAZ+RZ`: **`bad = 0`** em 917.568 lanes
    (51.832 NaN), MXCSR restaurado em todas — em debug, `-O` e `-O +avx2,+fma`;
  - **exaustivo** (`--exhaustive`, `-O`): todas as **2^32** entradas, **`bad = 0`**
    (16.777.214 NaN, 67.121.150 especiais; 456.875.632 lanes normais ≠ `1.0f/x`);
  - **mutações de controle**, todas detectadas: sem lane especial `bad = 158.140`; sem
    forçar MXCSR (host FTZ+DAZ+RZ) `bad = 123.095`; `1.0f/x` IEEE no domínio de `0088E32F`
    `bad = 260.166` de 514.000 lanes.
- CPU desta conferência: **AMD Ryzen 5 4600G**.

**`NÃO PROVADO` (resíduo de M2):**

- `vrcpps` não é fixado pela ISA (Intel ≠ AMD): o port é bit a bit com o binário **na mesma
  CPU** do oráculo (mesma ressalva de M1);
- que o oráculo rode o índice `4` de `0x21C7408`: o valor `4` é do dump (fixado em runtime
  pela CPU onde o dump foi feito); os caminhos `0x297EE0` (índices `0..2`) e `0x299C60`
  (índice `3`) **não foram lidos**;
- os outros chamadores de `0x1C8530` (`0x879CF0`, `0x885040`, `0088A500`, `0087E0B0`) não
  foram religados ao `rcp.rs` — fora de M2.
