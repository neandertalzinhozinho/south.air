# R — divisão `0x1550` → `0x63640` (2026-11-25)

> Fecha o **mapa de despacho** e as **duas aritméticas** da divisão do estágio. Tudo com
> instrução + RVA em `checks/63640.dis` (1.006 linhas, `0x63640`–`0x646C0`). O que não foi
> lido fica `NÃO PROVADO` no §5 — não é estimado.

---

## 0. Assinatura e semântica

`0x1550` é wrapper `0xC560` → impl `0x63640`; `rcx = den`, `rdx = num`, `r8 = dst`,
`r9d = n`, `dst[i] = num[i] / den[i]` (3 ponteiros, sem aliasing):

```
0000C57C  call 0x63640          ; repassa rcx/rdx/r8/r9 intactos
00063653  mov  rdi, r8          ; dst
00063676  mov  rbp, rdx         ; num
```

O corpo usa um **scratch local** de 16 floats (8 `den` + 8 `num`), alinhado a 64 B e
inicializado com `1.0` (`ymm4 = [0x1DF9DA0]`):

```
0006365E..0006366E  r13 = (rsp+0xaf) & ~0x3f
0006368F            ymm4 = [0x1DF9DA0]            ; 1.0 por lane
000636AA/000636B0   [r13] = [r13+0x20] = ymm4     ; padding 1.0
```

O `1.0` é o **padding**: quando o bloco tem menos de 8 elementos, as lanes que sobram ficam
`1.0/1.0 = 1.0` e são descartadas na escrita.

---

## 1. Despacho — o resultado depende de `n` **e** do alinhamento de `dst`

| Etapa | Condição | Trecho | Aritmética |
|---|---|---|---|
| cabeça | `h = min(8 − ((dst & 0x1c) >> 2), n)` | `00063697`–`00063A5D` | **A** (8 lanes) |
| laço 16 | `n16 = n >> 4` | `00063A61`–`0006400D` | **B** (2×8 lanes) |
| bloco 8 | `n & 8` | `000643DD`–`0006468D` | **A** |
| resto 1..7 | `rem = n & 7` | `0006401A`–`00064335` | **A**, com padding `1.0` |

Prova do cálculo da cabeça:

```
0006366A  and  rdi, 0x1c        ; (dst mod 32) em bytes
00063697  test edi, edi
00063699  je   0x63a61          ; dst já 32-B alinhado -> sem cabeça
0006369F  shr  edi, 2           ; elementos até o alinhamento
000636A2  neg  edi
000636A4  add  edi, 8
000636B6  cmovge edi, r9d       ; h = min(h, n)
```

Depois da cabeça, `rcx/rbp/r8` avançam `h*4` (`00063A51`–`00063A5D`) e `r9d -= h`
(`00063A51`), então o `dst` está 32-B alinhado. O laço de 16 é `sar r12d, 4`
(`00063A67`). O bloco de 8 é testado por `test r9d, 8` (`0006400D`) e o resto por
`and r9d, 7` (`0006401A`).

---

## 2. As duas aritméticas (comum + A + B)

Comum a todas as lanes:

```
m    = (den == 0)              0006376A vcmpeqps  (16 lanes: 00063ACD/00063AD2)
den' = blend(den, 1.0, m)      0006376F vblendvps (16 lanes: 00063AE2/00063AEA)
r0   = vrcpps(den')            00063775            (16 lanes: 00063AF0/00063AF4)
mask = (r0 != 0)               00063779 vcmpneq_oqps
d    = den' & mask             0006377E vandps
e    = 1 − d·r0                00063782 vfnmadd213ps
```

**A — refina o quociente (8 lanes: cabeça, bloco 8 e resto):**

```
q0 = r0 · num                  00063787 vmulps   ymm0,ymm0,[r13+0x20]
q  = q0 · e + q0               00063791 vfmadd213ps
q  = q  · e + q0               00063796 vfmadd213ps
```

**B — refina o recíproco e multiplica no fim (laço de 16 lanes):**

```
r1 = r0 · e + r0               00063B24 vfmadd213ps ymm8,ymm7,ymm0
r2 = r1 · e + r0               00063B29 vfmadd213ps ymm8,ymm7,ymm0
q  = r2 · num                  00063B37 vmulps      ymm7,ymm8,[r15+r10]
```

> **A ≠ B em ponto flutuante.** As duas calculam `r0·num·(1+e)²` em reais, mas arredondam
> em pontos diferentes. "vrcpps + dois Newton" **não** descreve a função: é preciso
> replicar o despacho.

O sítio `000640D1` (**resto 1..7**) usa **A**; `00064403` (**bloco 8** da cauda) usa **A**;
só o laço `00063AF0` usa **B**. *(Correção de 2026-11-25: a versão anterior chamava
`000640D1` de "bloco 8"; pelo fluxo, `0006400D test r9d,8; jne 0x643dd` leva ao bloco 8 em
`000643DD`, e `000640D1` fica no resto, depois de `0006401A and r9d,7`.)*

**Máscara do recíproco nulo — diferente em A e B (lido em 2026-11-25):**

```
A: 00063779 vcmpneq_oqps ymm2,ymm0,ymm3 ; 0006377E vandps  ymm3,ymm5,ymm2   ; d = den' se r0 ordenado e != 0
B: 00063AF8 vcmpeqps     ymm9,ymm0,ymm2 ; 00063B0E vandnps ymm7,ymm9,ymm7   ; d = 0 só se r0 == ±0
```

Só muda o resultado quando `r0` é NaN (`den'` NaN). `r0 == 0` ocorre de fato: `vrcpps`
devolve `+0` para `|den'| ≳ 2^126` (medido nesta CPU: `rcp(f32::MAX) = 0`); aí `d = 0`,
`e = 1` e o quociente sai `0·num` nas duas aritméticas.

**Ordem do bloco de 8 da cauda (`000643DD`–`0006468D`) — FECHADA:** `vmovups ymm3,[rcx]` /
`ymm5,[rbp]` (`000643DD`/`000643E3`) → cópia para o scratch (`000643E8`/`000643EE`) →
`vcmpeqps`/`vblendvps` (`000643F8`/`000643FD`) → `vrcpps` (`00064403`) → `vcmpneq_oqps`
(`00064407`) → `q0 = r0·num` (`0006440C`, antes de `e`; independente, mesmo valor) →
`vandps` (`00064410`) → `e` (`00064414`) → dois `vfmadd213ps` com addend `q0`
(`0006441D`/`00064422`) → fixup (`00064439`–`00064674`, teste `cmp [r13+4i],0` sobre o `den`
copiado) → `vmovups [r8],ymm0` (`0006467A`) → `rcx/rbp/r8 += 0x20`
(`00064681`–`00064689`) → `jmp 0x6401a` (resto). Não há contador interno: são exatamente
8 lanes.

**Wrapper e retorno:** `0x1550` → `jmp [0x21C6448 + 8·[0x21C7408]]`; no dump
`[0x21C7408] = 4` e `[0x21C6468] = 0x199BC560` → `0xC560`. `0xC560` recusa ponteiro nulo e
`r9d ≤ 0` (`0000C568`..`0000C57A`), chama `0x63640` (`0000C57C`) e troca `eax ≠ 0` por `2`
(`0000C581`..`0000C588`). `eax` vale `1` se alguma lane passou pelo fixup
(`000637F4`, `00063BA6`, `00064335 or eax,ecx`, `0006467F or eax,edi`). O estágio descarta
o retorno (`008C254A add rbx,8` logo após o `call`).

---

## 3. Fixup de `den == 0` (inalcançável no estágio)

Para lanes com `den == 0`, depois da conta:

```
000637BA..00063889 (8 lanes) / 00063B6A.. (16 lanes)
  num finito != 0  ->  ±inf com o sinal de num   (sign | 0x7F800000)
  num == 0 ou NaN  ->  0x7FBFFFFF (NaN)
```

É a semântica IEEE de `num/0`. No estágio o denominador vem do clamp `0x1100`
(`CLAMP_MIN = 0x33D6BF95`, `1.00000001e-07f`), então `den ≥ 1e-7` e o fixup **não roda**;
fica transcrito por completude.

---

## 4. `n` no estágio é **ímpar**

```
008C14B0  mov r15d,[rdx+0x404]        ; n do estágio
00619DE4  mov [r14+0x404],edi         ; edi = r9d = [X+0x40]   (N §4.1)
0086FF35  cvttss2si eax,xmm3          ; xmm3 = x · 2.26757365e-05
0086FF39  imul eax,[rbp+0x430]
0086FF43  mov [rcx+0x28],r8           ; N
0086FF47  lea rax,[r8+r8]
0086FF4B  mov [rcx+0x38],rax          ; 2N
0086FF4F  shr rax,1
0086FF52  inc rax
0086FF55  mov [rcx+0x40],rax          ; N+1
```

⇒ `n = N + 1` é **ímpar**, logo `n & 7 != 0` sempre e a cauda (bloco 8 e/ou resto) roda em
toda chamada. Não existe caminho "só laço de 16".

### 4.1 `x` e `[rbp+0x430]` em `0x86FE90` — PROVADO (2026-11-25)

`0x86FE90` tem só dois chamadores, ambos em `0x86A4E0` (`xrefs.csv`):

```
0086A543  mov dword [rsp+0x20],0x800 ; 0086A54B call 0x86fe90 ; rcx = E'+8      (1ª, arg5 = 2048)
0086A555  lea rcx,[r15+0x2c50]
0086A579  mov dword [rsp+0x20],0x100 ; 0086A581 call 0x86fe90 ; rcx = E'+0x2C50 (2ª, arg5 = 256)
```

`0x86FE90`: `rbp = rsp_entrada − 0x408` (`0086FE90`/`0086FEA8`) ⇒ `[rbp+0x430]` = `arg5`;
`xmm3` = `arg4` (float), repassado intacto por `0x86A4E0` (`0086A53B`/`0086A561`). O `X` do
estágio é o da **2ª** chamada: `0x8774A0` passa `C = [p+0x10]+0x5F8` (`00877508`/`00877510`),
`0x881050` faz `X = C+0x2C50` (`0088108A`/`0088139D`) e o `X` chega a `0x8B3ED0` como `r13`
(`checks/n_canal.md` §2.3/§4). O `xmm3` vem de `0x8634A0` (único chamador de `0x86A4E0`,
`00863929`, com `rcx = E+0x5F8` em `008638D6`):

```
008634A3  movss [rax+0x20],xmm3       ; a = arg4 de 0x8634A0 (home em rbp+0x218)
0086350F  movss xmm0,[rbp+0x218]
00863531  addss xmm0,xmm7             ; a + 1.0   (xmm7 = [0x2079F9C] = 0x3F800000)
0086353C  mulss xmm0,[0x2079D04]      ; · 0x37BE37C6 (1/44100)
00863544  cvttss2si ecx,xmm0
00863548  cmp ecx,r13d ; 0086354B cmovg eax,ecx   ; k = max(t, 1)
00863552  mov [r14+0x2c],eax          ; [E+0x2C] = k
008638CE  movss xmm3,[rbp+0x218]
0086391C  movd xmm0,[r14+0x2c] ; 00863922 cvtdq2ps ; 00863925 divss xmm3,xmm0   ; x = a / k
0086FEB6  maxss xmm3,[0x207A5E4]      ; max(x, 44100.0)  (0x472C4400)
0086FF1E  mulss xmm3,[0x2079D04]
0086FF35  cvttss2si eax,xmm3
0086FF39  imul eax,[rbp+0x430]        ; · 0x100
```

⇒ `N = trunc(max(a/k, 44100)·c)·256`, `n = [X+0x40] = N+1`. Para **`a = 48000`**: `k = 1`,
`x = 48000`, `48000·c = 1,088…` → `N = 256`, **`n = 257`**. (Também `a = 44100` → `N = 256`,
porque `44100·c` arredonda para `1.0` em f32; `a = 96000` → `k = 2`, `x = 48000`, `N = 256`.)
Transcrito em `port/src/div.rs::stage_division_len`, teste `stage_len_at_48k_is_257`.

Despacho a 48 kHz (`dst` alinhado, §5): `257 = 16·16 + 1` → **16 laços B**, `257 & 8 = 0`
(o bloco de 8 **não** roda), **1 lane de resto A**.

`a` é `(float)xmm2` de `0x862E40` (`00862E68 cvtsd2ss xmm3,xmm6`, único chamador de
`0x8634A0`, `00862E72`). Que `a` seja a taxa de amostragem é **`NÃO PROVADO`** (M4).

**Conflito com a âncora:** `LEMBRAR DISSO.md` lista `N = 278 @ 48 kHz`. A instrução dá
`N = 256` para o `X` do estágio (o `k` de `0x8634A0` e o `cvttss2si` de `0x86FE90`
truncam a razão). Registrado em `PLANO_MOTOR_AUDIO.md` §23.14; a âncora não é editada.

---

## 5. Alinhamento dos 4 `dst` e o que fica `NÃO PROVADO` (2026-11-25)

**PROVADO dentro de `0x8C1440`** (`checks/8c1440.u8.dis`): `dst = [arena] + 4·cursor`, com
`cursor = [arena+0x18]` (`008C247D`/`008C2480`/`008C249C`, `008C24E5`..`008C24EF` e os
análogos de `T1/T2/T3`). As **únicas** escritas do cursor antes de `008C24E1` são
`008C154F`, `008C157F`, `008C15C9`, `008C15F8`, `008C1646`, `008C1677`, `008C16C1`,
`008C16F0`, `008C174B`, `008C1781` e `0x8CAFD0` (`008CB007`/`008CB03A`), todas
`align16` em floats (`and eax,0xf; sub; add 0x10; test 0xf; cmove`). Os `call` entre
`008C17E7` e `008C245B` (`0x10D0` ×8, `0x1580` ×5, `0x1370` ×5, `0x1100` ×4, `0x61B790` ×4
com `ecx`/`edx` inteiros, `0x1798F42` = `memset([rbp+0x2a8],0,0x3f8)` ×2 em
`008C1BA0`/`008C2053`) não recebem a arena. Logo o
cursor nos 4 sítios é múltiplo de 16 floats e `dst ≡ [arena] (mod 64 B)`, independentemente do
cursor de entrada (que só afeta o 1º buffer do par 0, `008C1502`). A base `[arena]` não é
escrita em `0x8C1440`.

**PROVADO a base (por instrução, com a ressalva abaixo):** a arena de `0x8C1440` é `r8 =
r12 = r10 = [rbp+0x4a60]` = `arg9` de `0x8B3ED0` (`008B6061`, `008B5DDF`, `008B5DB6`;
`rbp = rsp_entrada − 0x4a18` por `008B3ED0`..`008B3EE2`), que é `[rsp+0x40] = [CTX]` em
`008AD601`/`008AD2E1`, `CTX+0 = arg7` de `0x889BB0` (`0088AC7C`), `rbx` de `0x881050`
(`00881398`, `0088107C` = `arg5`), `[p+0x30]` em `0x8774A0` (`0087750C`/`00877517`),
`arg5` de `0x8677F0` (`0086783C`/`00867843`), e em `0x8646A2` `lea rax,[rbp]`
(`00865649`/`00865658`) — o ramo de `[E+0x2C] ≤ 1` (`00865231`/`00865242`), que é o de
`a = 48000` (`k = 1`). O objeto local `[rbp]` recebe `[rbp] = [E+0x30]`
(`00865210`/`00865222`/`00865236`, cópia de `[E+0x38] = 1` qword) e cursor `0`
(`0086523A`, `0086563A`). `[E+0x30]` é gravado por `0x868B50` (único chamador `00863563`,
`lea rcx,[r14+0x30]` em `0x8634A0`): `rbx = (malloc+0x40) & ~0x3f` (`00868B98`/`00868B9C`),
`[rdi] = rbx` (`00868BAB`), `[rdi+8] = 1` (`00868BBF`). ⇒ base **64 B alinhada** ⇒
`dst & 0x1c = 0` nos 4 sítios ⇒ a **cabeça não roda** (`00063699 je 0x63a61`).

**`NÃO PROVADO` (resíduo de M1, em `port/src/pending.rs`):**

- que o `E` de `0x864410`/`0x8646A2` (`0086444C`/`0086453D`, `E = arg1`; despacho
  indireto) seja o objeto construído por `0x8634A0` — hoje só coincidem os offsets
  (`+0x10`, `+0x2C`, `+0x30`, `+0x5F8`);
- que nenhum outro código escreva `[E+0x30]` depois de `00868BAB` (só os chamadores diretos
  foram varridos; `xrefs.csv` não captura `call` indireto);
- que `a` (= `arg4` de `0x8634A0`) seja a taxa de amostragem (M4);
- o `0x8C1440` chamado pelo gêmeo `0x8C5C40` (`008C7DDE`/`008C9E5E`, chamadores
  `0x8BAFF0`/`0x8BBA60`/`0x8BC800`/`0x8BE210`): `n` e arena **não** rastreados;
- sinal/payload de NaN no port (ver §6).

O `call 0x1796910` em `000643CC` é o `__security_check_cookie` (epílogo), não aritmética.

---

## 6. Port e conferência (2026-11-25)

- `port/src/div.rs` — `div_block` / `div_block_mod32` (despacho e as duas aritméticas, com a
  máscara distinta de A/B e o fixup), `stage_division_len`. 16 testes.
- `port/src/stage.rs` — as 4 divisões chamam `div_block_mod32(num, den, dst, 0)`; teste
  `divisions_use_0x63640_not_ieee_division`.
- `checks/j_div_avx.rs` — emulador por intrinsics da sequência de `checks/63640.dis` (RVA por
  linha, alinhamento lido do ponteiro) contra `div.rs`: 40.800 chamadas (`n = 1..80, 255..258,
  513`, os 8 alinhamentos de `dst`, valores especiais: `±0`, denormais, `2^125`, `2^126`,
  `f32::MAX`, `±inf`, NaN) + 2.000 blocos no domínio do estágio (`n = 257`, `den ≥ 1e-7`):
  **`bad = 0`** e **`stage_bad = 0`** em 2.807.920 lanes, em debug, `-O` e `-O +avx2,+fma`.
  Mutação de controle (bloco 8 com B): `bad = 49.347`.
- **NaN:** para lanes cujo resultado é NaN o veredito exige só NaN nos dois lados. O
  sinal/payload depende da ordem de operandos que o LLVM escolhe para `vmulps`/`vfmadd*`
  (o próprio emulador muda entre builds: ex. `den = 0x7FA00001` → `0xFFE00001` em debug,
  `0x7FE00001` em `-O`) ⇒ payload de NaN **`NÃO PROVADO`** no port. No estágio `den ≥ 1e-7`
  e só há NaN se a entrada já for NaN.
- **`vrcpps` depende da CPU:** a tabela não é fixada pela ISA (Intel ≠ AMD). O port usa a
  instrução do hardware em que roda; o bit a bit vale na mesma CPU do oráculo
  (esta máquina: AMD Ryzen 5 4600G).
