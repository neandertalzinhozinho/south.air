# Q — `0x8C1440`: papéis dos 16 buffers, coeficiente por grupo e cadeia do estágio (2026-11-25)

> Fecha os itens 1–5 de §8.4.8 da `dsp-spec.md`. Tudo abaixo tem instrução + RVA em
> `checks/8c1440.u8.dis` (1.787 linhas, `0x8C1440`–`0x8C32B7`). O que não fecha fica
> marcado `NÃO PROVADO` no §9 — não foi estimado.
>
> Ordem de argumentos usada (já provada, `PLANO` §23.4/§23.12):
> `0x1580`: `rcx=a`, `rdx=b`, `r8=dst`, `r9d=n`, `dst += a*b`;
> `0x1370`: `rcx=src`, `rdx=dst`, `r8d=n`, `dst += src`;
> `0x1550`: `rcx=den`, `rdx=num`, `r8=dst`, `r9d=n`, `dst = num/den`;
> `0x10D0`: `rcx=dst`, `edx=n`, zera;
> `0x1220`: `rdx=dst`, `r8d=n`, `xmm0=s`, `dst *= s`;
> `0x11F0`: `r8=dst`, `rcx=src`, `r9d=n`, `xmm1=s`, `dst = src*s + dst` (MAC com FMA:
> `00005C46 vfmadd213ss`, `00005C85 vfmadd213ps`).
>
> Além dos `call`, vale a semântica de opcode (não é leitura de tabela): `movaps [A],xmm`
> grava 16 B no slot (`{p0,p1}`), `movsd [A+0x10],xmm` grava o `n`; um descritor de par é
> `{float *p0; float *p1; int n;}` = `0x18` B e é consumido por `0x1580`/`0x1370`/
> `0x1550`/`0x1220`/`0x11F0` via `r8 = [desc + 8*i]`.

---

## 1. Alocação: 8 pares, 16 buffers

A spec §8.4.3 dizia "16 `call` em `008C1800`–`008C19C6`". São **8 sítios estáticos** de
`0x10D0`, cada um dentro de um laço de **2 iterações** (`cmp rbx,2` / `jl`):

| Par | `float*` (slot) | `n` em | Alocação |
|---:|---|---|---|
| 0 | `[rbp+0x00]` / `[rbp+0x08]` | `[rbp+0x10]` | bump inline `008C150F` / `008C155D` |
| 1 | `[rbp+0x40]` / `[rbp+0x48]` | `[rbp+0x50]` | bump inline `008C15A7` / `008C15D6` |
| 2 | `[rbp+0xa0]` / `[rbp+0xa8]` | `[rbp+0xb0]` | bump inline `008C161E` / `008C1656` |
| 3 | `[rbp+0x60]` / `[rbp+0x68]` | `[rbp+0x70]` | bump inline `008C169B` / `008C16D2` |
| 4 | `[rbp+0x80]` / `[rbp+0x88]` | `[rbp+0x90]` | bump inline `008C171A` / `008C1754` |
| 5 | `[rbp-0x20]` / `[rbp-0x18]` | `[rbp-0x10]` | `0x8CAFD0` `008C179A` |
| 6 | `[rbp+0x20]` / `[rbp+0x28]` | `[rbp+0x30]` | `0x8CAFD0` `008C17BE` |
| 7 | `[rbp-0x40]` / `[rbp-0x38]` | `[rbp-0x30]` | `0x8CAFD0` `008C17E2` |

Zeroização: laços de 2 em `008C1800`–`008C1814`, `1830`–`1844`, `1870`–`1886`, `18B0`–`18C7`,
`18F0`–`1907`, `1930`–`1946`, `1970`–`1986`, `19B0`–`19C6` — **16 buffers**, um `0x10D0` por
buffer (`edx = n`).

**Aliasing de slots (crítico):** os *slots* são reutilizados como cópias de descritor, não
como dados. Em `008C24BD` o slot `[rbp-0x20]` passa a conter o descritor do par 0; em
`008C2607` `[rbp+0xa0]` recebe `T1`; em `008C2703` `[rbp+0x80]` recebe `T2` (`008C269E`); em
`008C27F7` `[rbp+0x20]` recebe `T3` (`008C2795`). **Mais um, novo:** `008C250E` põe o
descritor da divisão 1 em `[rbp-0x40]`. Quem lê o slot depois do RVA lê o **novo**
descritor — a leitura anterior que tratava `[rbp-0x40]` como "par 7" após `008C250E` estava
errada (ver §4).

---

## 2. Passagem A — acumulação (`008C1A58`–`008C2361`)

Laço de grupos em `008C1A4D`–`008C2361` (5 iterações, tabela `0x2014360 = {8,9,10,6,5}`);
por grupo, laço de registros de `0x18 B` (`008C1AB0`, incremento `008C1E09`/`008C2311`).

`tipo = {8,9,10,6,5}[g]` (`008C1A60`), `t = [rbp+0x13D8]`, `n = t+0x404`, `rec->sel = rec+0`,
`rec->first_buf = rec+8`, `rec->nch = rec+0x10`, `enable = state[0x1BF + 8g]`
(`008C1A64`/`008C1A6E`, `state = [e+0x2c38]`).

**A acumulação é filtrada pelo predicado nos dois ramos** — não é "todo registro". A árvore
de participação (`008C1AB0`–`008C1B6E`, ramo `enable != 0`; `008C1EE4`–`008C1F43`, ramo
`enable == 0`) reproduz `0x61B790`:

| `tipo` | participa se |
|---:|---|
| 0 | sempre (nunca ocorre: tabela é `{8,9,10,6,5}`) |
| 1 | `sel != 0xA` |
| 2 | `sel != 9` |
| 3 | `sel ∉ {9,0xA}` |
| 4 | `sel ∉ {8,9,0xA}` |
| 5 | `sel ∈ {0x10,0x11,0x12}` |
| 6 | `h(4,sel) && !h(5,sel)` (`008C1B2F`/`008C1B43`, `008C1F9E`/`008C1FB2`) |
| 7 | `sel ∈ {8,9}` |
| 8/9/0xA | `sel == tipo` |

### 2.1 Ramo `enable != 0` (`008C1A8F je` não tomado)

Para cada registro que participa, com `nch == 2` (`008C1B74 cmp [r13+0x10],2`):

```
008C1D10 r8  = [rsp+rbx+0x60]   ; par 0
008C1D18 rdx = [rbp+rbx+0xed0]  ; cópia do descritor de canais
008C1D20 rcx = [rbp+rbx+0x6b0]  ; a mesma cópia
008C1D28 call 0x1580            ; par0 += ch*ch
...
008C1DE0 rdx = [rbp+rbx-0x70]   ; par 1
008C1DE8 rcx = [rbp+rbx+0xac0]  ; cópia do descritor de canais
008C1DF0 call 0x1370            ; par1 += ch
```

⇒ **par 0 = `Σ ch²`, par 1 = `Σ ch`**, por canal, somados sobre os registros do grupo que
passam no predicado. O ramo `nch != 2` (`008C1B79 jne 0x8C1E4B`, inclui `nch == 1`) usa só
`track->buffers[first_buf]` (`008C1E61 rdi = [rsi + rax*8]`): `par0 += ch²` (`008C1E81`) e
`par1 += ch` (`008C1EAB`).

### 2.2 Ramo `enable == 0` (`008C1EBE`–`008C2323`)

O par usado depende de `(al, tipo, [rbp+0x13E8])`. `[rbp+0x13E8]` é o *home slot* de `r9`
reusado como byte e vale `1` **somente** se `state[0x1BF]==0 && state[0x1C7]==0`
(`008C1A14`–`008C1A38`), ou seja, quando o **grupo 0 e o grupo 1 estão ambos desabilitados**.

| Condição | `rsi` recebe `ch²` | `[rbp-0x50]` recebe `ch` | RVA |
|---|---|---|---|
| `al != 0` **e** `[rbp+0x13E8] != 0` | par 2 (`rbp+0xa0`) | par 3 (`rbp+0x60`) | `008C200F`, `008C1F70` |
| `al == 0` **e** `tipo == 6` | par 4 (`rbp+0x80`) | par 5 (`rbp-0x20`) | `008C1F59`, `008C201D` |
| `al == 0` **e** `tipo == 5` **e** `sel ∈ {0x10,0x11,0x12}` | par 6 (`rbp+0x20`) | par 7 (`rbp-0x40`) | `008C1F2B`–`008C1F32`, `008C1F60`, `008C2021` |
| qualquer outro (`tipo ∉ {5,6}`, `al == 0`, ou `tipo 5` com `sel` fora) | **não acumula** | — | `008C2311` |

Prova da seleção: `008C1F57 test cl,cl` + `008C1F59 lea rsi,[rbp+0x80]` +
`008C1F60 lea rdx,[rbp+0x20]` + `008C1F64 cmove rsi,rdx` (`cl = (tipo==6)`); depois
`008C201B test cl,cl` + `008C201D lea r13,[rbp-0x20]` + `008C2021 lea rax,[rbp-0x40]` +
`008C2025 cmove r13,rax`. O `0x1580` está em `008C21D8` (2 canais) / `008C220E` (mono) e o
`0x1370` em `008C22D0` / `008C22FB`.

**Correção da tabela anterior:** a linha "`al == 0`, `tipo ≠ 6` → par 6/7" estava larga. O
código exige `tipo == 5` (`008C1F4D cmp r14,5; jne 0x8c2311`) **e** `sel ∈ {0x10,0x11,0x12}`
(`008C1F2B lea eax,[r8-0x10]; 008C1F32 ja 0x8c2311`). Para `tipo == 0xA` desabilitado o
registro é **descartado** e nada é acumulado.

**`tipo 10` desabilitado — FECHADO:** em `008C1FDB`–`008C1FF1` o teste é
`sel == tipo` seguido de `lea rax,[r14-8]; cmp rax,1; ja 0x8c1f38`. Para `tipo == 0xA`,
`r14-8 = 2 > 1` ⇒ `al = 0` **incondicionalmente**; e como `tipo != 5,6`, cai em `008C2311`.
Logo o grupo 2 (tipo 10), desabilitado, **nunca acumula e nunca mistura**.

---

## 3. Guarda e normalização

### 3.1 Clamp

Quatro `0x1100` com `r9d = 0` (modo **max**, §17.2) e `bound = 1.00000001e-07f`
(`0x2079CEC`, `008C2367`), um por par **ímpar**:

| Par | Cópia usada | RVA do `call` |
|---:|---|---|
| 1 | `rbp+0x1a0` (`008C2371`/`008C2379`) | `008C2393` |
| 3 | `rsp+0x60` (`008C23A1`/`008C23AB`) | `008C23CD` |
| 5 | `rbp-0x70` (`008C23DB`/`008C23E6`) | `008C240D` |
| 7 | `rbp+0x60` (`008C241B`/`008C2426`) | `008C244D` |

⇒ {1,3,5,7} = conjunto **denominador**, protegido contra zero. Em `008C241B` o descritor do
par 7 é **copiado para `xmm11`** (`xmm12 = n`) **antes** de o slot `[rbp-0x40]` ser
reaproveitado em `008C250E` — é essa cópia que a divisão 4 usa (§4).

### 3.2 As quatro divisões (`0x1550`)

Cada divisão escreve em **uma alocação nova de 2 buffers** e guarda o descritor no slot do
par que serviu de numerador (aliasing):

| # | `dst` (novo par) | `num` (`rdx`) | `den` (`rcx`) | `call` | `dst` gravado em |
|---:|---|---|---|---|---|
| 1 | `new1` (`[rbp+0xf0]`: `008C24AF`/`008C24EF`) | par 0 (`[rbp-0x20]`, `008C24BD`) | par 1 (`[rbp+0x240]`, `008C248B`) | `008C2545` | `[rbp-0x40]` (`008C250E`) |
| 2 | `T1` (`[rbp+0x140]`) | par 2 (`[rbp+0x260]`, `008C259D`) | par 3 (`[rbp+0x280]`, `008C2581`) | `008C263D` | `[rbp+0xa0]` (`008C2607`) |
| 3 | `T2` (`[rbp+0x160]`) | par 4 (`[rbp+0x1e0]`, `008C2697`) | par 5 (`[rbp+0x200]`, `008C2679`) | `008C273B` | `[rbp+0x80]` (`008C2703`) |
| 4 | `T3` (`[rbp+0x180]`) | par 6 (`[rbp+0x220]`, `008C278E`) | par 7 (`[rbp+0x120]`, `008C2770`) | `008C2828` | `[rbp+0x20]` (`008C27F7`) |

Prova de que o numerador é preservado: antes de sobrescrever o slot, o descritor é copiado
para o argumento (`008C246A movups xmm0,[rbp]` → `008C24BD`; `008C255C movups xmm0,[rbp+0xa0]`
→ `008C259D`; `008C2654 movups xmm0,[rbp+0x80]` → `008C2697`; `008C2751 movups
xmm0,[rbp+0x20]` → `008C278E`).

Prova de que o denominador da divisão 4 é o **par 7 original**: `008C241B movdqu
xmm11,[rbp-0x40]` + `008C2426 movsd xmm12,[rbp-0x30]` acontecem **antes** de `008C250E`;
`008C2770 movaps [rbp+0x120],xmm11` + `008C2781 movsd [rbp+0x130],xmm12` rematerializam o
descritor para o `008C2828`. Portanto **D4 = par6 / par7**, e não `par6 / D1`.

**Reconciliação do par 7 — FECHADA:** o par 7 nunca é destino de divisão. Ele é o `Σ ch` do
grupo de `tipo 5` (grupo 4), escrito em `008C2021`/`008C22D0`; `008C250E` só **reaproveita o
slot** como descritor de `new1`. O `den` da divisão 4 é o **dado** do par 7, capturado em
`xmm11`.

### 3.3 Bloco de acumulação `008C296B`–`008C2A5A` (4 somas de canais)

Quatro alocações novas (`A = [rbp-0x80]` `008C2868`, `B = [rbp+0x1c0]` `008C28B1`,
`C = [rbp]` `008C28F6`, `D = [rbp+0x40]` `008C2943`), cada uma zerada por `0x10D0` e depois
recebendo `dst += src` (`0x1370`) de **ambos os canais** do par correspondente:

| Soma | Fonte | RVAs |
|---|---|---|
| `A` | `new1` (= `Σch²/Σch` dos grupos habilitados) | `008C296B` (zero), `008C298E` (2× `0x1370`, `src=[rbp+rbx+0x120]`) |
| `B` | `T1` (= `Σch²/Σch` do par 2/3) | `008C29B7`, `008C29CE` (`src` rematerializado em `008C29A8` de `xmm6 = T1`) |
| `C` | `T2` (= `Σch²/Σch` do par 4/5) | `008C29F2`, `008C2A0E` (`src` = `xmm8 = T2`) |
| `D` | `T3` (= `Σch²/Σch` do par 6/7) | `008C2A37`, `008C2A4E` (`src` = `xmm10 = T3`) |

⇒ `A/B/C/D` são a **soma sobre os 2 canais** de cada resultado de divisão. São eles que o
caminho mono da passagem B consome (o fator `g/2` compensa a soma).

---

## 4. Passagem B — a lei de mistura de verdade (`008C2AA5`–`008C3201`)

Carga **única** dos coeficientes, antes do laço de grupos (`008C2A70`–`008C2A8B`); `xmm10 =
1.0f` (`008C2A5C`) e `xmm11 = 0.5f` (`008C2A67`) também são únicos:

| Registrador | Fonte | Campo de estado |
|---|---|---|
| `xmm8` | `[rbp+0xC0]` (`008C2A70`) | `state + 0x2C` (`008C19D6`) |
| `xmm12` | `[rbp+0xC4]` (`008C2A79`) | `state + 0x30` (`008C19E6`) |
| `xmm13` | `[rbp+0xC8]` (`008C2A82`) | `state + 0x34` (`008C19F6`) |
| `xmm14` | `[rsp+0x28]` (`008C2A8B`) | `state + 0x38` (`008C1A06`) |

A mistura tem `dst = buffers de canal do registro` (a cópia `[rbp+0x6b0]` aponta para
`t->buffers[first_buf..]`, `008C2C30`/`008C2D20`) e `src = resultado da divisão`:

```
0x1220(dst = canais, n, 1.0f - g)                     ; calls 008C2CE9 / 008C30C9
0x11F0(dst = canais, src = D, n, g)                   ; calls 008C2DA7 / 008C3196
```

isto é, **`ch ← (1-g)·ch + g·D`**, por canal. No caminho `nch != 2`
(`008C2BAE`/`008C2BB4` e `008C2F88`/`008C2F8D` desviam para `008C2DB8`/`008C31A7`) o `src`
é a soma correspondente (`A`/`B`/`C`/`D`) e o coeficiente é `g·0.5f` (`008C2DEA`,
`008C31D5`): `ch ← (1-g)·ch + (g/2)·Soma`.

### 4.1 Roteamento `condição → divisão → soma`

| Ramo | `src` (estéreo) | `src` (mono) | `g` | RVA (g) |
|---|---|---|---|---|
| `enable != 0` (qualquer `tipo`) | `new1` (`[rbp+0xf0]` → `[rbp+0x120]` em `008C2CFC`) | `A` (`[rbp-0x80]`, `008C2DE2`) | `state+0x2C` | `008C2CC4`, `008C2DA3`, `008C2DBF` |
| `enable == 0`, `al != 0` e flag | `T1` (`[rbp+0x140]`, `008C2EA7`) | `B` (`[rbp+0x1c0]`, `008C2F71`) | `state+0x30` | `008C2F3F` |
| `enable == 0`, `al == 0`, `tipo == 6` | `T2` (`[rbp+0x160]`, `008C2F59`+`008C2F69`) | `C` (`[rbp]`, `008C2F7C`) | `state+0x34` | `008C2F50` |
| `enable == 0`, `tipo == 5` | `T3` (`[rbp+0x180]`, `008C2F59`+`008C2F69` cmove) | `D` (`[rbp+0x40]`, `008C2F80`) | `state+0x38` | `008C2E9B` |
| `enable == 0`, `tipo == 0xA` | — (não mistura) | — | — | `008C31ED` |

Prova da seleção do `src`: `008C2EA7 lea r12,[rbp+0x140]`; `008C2F59 test cl,cl` +
`008C2F5B lea r12,[rbp+0x160]` + `008C2F62 lea rdx,[rbp+0x180]` + `008C2F69 cmove r12,rdx`
(`cl = (tipo==6)`). Prova da seleção da soma mono: `008C2F71 lea r14,[rbp+0x1c0]` (al != 0);
`008C2F7C lea r14,[rbp]` + `008C2F80 lea rax,[rbp+0x40]` + `008C2F84 cmove r14,rax`.

### 4.2 Mapa `grupo → coeficiente` (derivado, com RVA)

`tipo` é `{8,9,10,6,5}[g]`; o coeficiente é escolhido por `(enable, al, flag, tipo)`, **não**
por índice:

| `g` | `tipo` | `enable != 0` | `enable == 0` |
|---:|---:|---|---|
| 0 | 8 | `+0x2C` | `+0x30` se `sel == 8` e flag; senão não mistura |
| 1 | 9 | `+0x2C` | `+0x30` se `sel == 9` e flag; senão não mistura |
| 2 | 10 | `+0x2C` (se `sel == 10`) | **nunca** |
| 3 | 6 | `+0x2C` (se `P4 && !P5`) | `+0x34` (se `P4 && !P5`) |
| 4 | 5 | `+0x2C` (se `sel ∈ {16,17,18}`) | `+0x38` (se `sel ∈ {16,17,18}`) |

---

## 5. Significado aritmético do estágio (enunciado, não nome de parâmetro)

Por canal, `D = Σ_registros ch² / Σ_registros ch` — uma **média ponderada por potência** dos
registros empilhados no grupo. Para 1 registro, `D = ch` e a mistura é identidade
(`(1-g)·ch + g·ch = ch`). Para 2 registros `a,b`, `D = (a²+b²)/(a+b)`; com `a == b`, `D = a`
(idem). A lei `ch ← (1-g)·ch + g·D` puxa o canal para essa média com peso `g`.

Os grupos 0/1 compartilham o par 2/3 (ambos têm `tipo ∈ {8,9}`), então `D2` é a média
ponderada **conjunta** dos registros dos dois grupos — o que condiz com a nota de `link_all`
de §23.8. Não há, no código, nome nem unidade para `+0x2C/+0x30/+0x34/+0x38`: são apenas
fatores de mistura em `[0,1]` (o `1-g` é calculado, não clampado).

---

## 6. `0x882FC0` **não** é chamado aqui

`Select-String 882fc0` em `checks/8c1440.u8.dis` = **0 ocorrências**. A hipótese "um dos 16
buffers recebe a curva de `0x882FC0`" está **refutada** para `0x8C1440`; a curva é aplicada
em `0x8B3ED0` (J6, spec §8.2(e)/(f)). Os 16 buffers são só acumuladores, resultados de
divisão e somas de canal.

---

## 7. Resumo em uma tabela

| Slot/par | Papel provado | Prova |
|---:|---|---|
| 0 | acumulador `Σch²` dos grupos habilitados; `num` de D1 | `008C1D28`, `008C24BD` |
| 1 | acumulador `Σch` dos grupos habilitados; `den` de D1; clampado | `008C1DF0`, `008C248B`, `008C2393` |
| 2 | `Σch²` de `tipo 8/9` (flag); `num` de D2 | `008C200F`, `008C259D` |
| 3 | `Σch` de `tipo 8/9` (flag); `den` de D2; clampado | `008C1F70`, `008C2581`, `008C23CD` |
| 4 | `Σch²` de `tipo 6`; `num` de D3 | `008C1F59`, `008C2697` |
| 5 | `Σch` de `tipo 6`; `den` de D3; clampado | `008C201D`, `008C2679`, `008C240D` |
| 6 | `Σch²` de `tipo 5` (`sel ∈ {16,17,18}`); `num` de D4 | `008C1F2B`, `008C1F60`, `008C278E` |
| 7 | `Σch` de `tipo 5` (`sel ∈ {16,17,18}`); `den` de D4; clampado | `008C1F2B`, `008C2021`, `008C2770`, `008C244D` |
| `new1` | `D1 = par0/par1`; `src` da mistura dos habilitados | `008C2545`, `008C2CFC` |
| `T1` | `D2 = par2/par3`; `src` de `tipo 8/9` | `008C263D`, `008C2EA7` |
| `T2` | `D3 = par4/par5`; `src` de `tipo 6` | `008C273B`, `008C2F5B` |
| `T3` | `D4 = par6/par7`; `src` de `tipo 5` | `008C2828`, `008C2F62` |
| `A/B/C/D` | soma dos 2 canais de `new1/T1/T2/T3` | `008C298E`/`29CE`/`2A0E`/`2A4E` |

---

## 8. Fechado nesta rodada

1. Direção do `0x1370` (par acumula `ch`, não o contrário) — §2.1.
2. `tipo 10` desabilitado nunca acumula/mistura — §2.2 (`008C1FDB`–`008C1FF1`) e §4.1.
3. Reconciliação do par 7 — §3.2 (`008C241B` antes de `008C250E`).
4. Encadeamento `008C296B`–`008C2A5A` — §3.3 (A/B/C/D).
5. `src` da mistura e o mapa grupo→coeficiente — §4 (a "lei de mistura" de §8.4.7 estava
   invertida quanto a quem é `dst` e quem é `src`).

## 9. Continua `NÃO PROVADO`

1. **Nome/unidade** dos coeficientes `state+0x2C/0x30/0x34/0x38` — a seleção está provada,
   o rótulo (ex.: "blend", "layer mix") não existe no código.
2. **Intenção musical** da média ponderada por potência — a fórmula está provada; o porquê
   (anti-cancelamento? nivelamento de camadas?) não está no binário.
3. Faixa válida de `g`: o código calcula `1-g` sem clamp; se `g` pode sair de `[0,1]` só se
   prova lendo o escritor de `+0x2C..+0x38` (fora de `0x8C1440`).
4. Identidade do buffer final que `0x8B3ED0` consome depois de `0x8C1440` (cadeia de
   `0x8B605C`/`0x8B606E` e `0x8B80DC`/`0x8B80EE`) — fora do escopo desta função.
5. `nch > 2`: no ramo `enable != 0` da passagem A (`008C1E4B`) e na passagem B
   (`008C2DB8`/`008C31A7`) usa-se **só** `track->buffers[first_buf]`, sem laço para os
   demais canais; no ramo `enable == 0` da passagem A o registro com `nch ∉ {1,2}` **não
   acumula nada** (`008C21E9`/`008C22E1`). Está lido; a razão (nunca ocorrer `nch > 2`?)
   depende do escritor de `rec->nch`.
