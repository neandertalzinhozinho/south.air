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

O sítio `000640D1` (bloco 8) usa **A**; `00064403` (bloco 8 da cauda) usa **A**; só o laço
`00063AF0` usa **B**.

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

---

## 5. `NÃO PROVADO` / a fazer

- valor de `x` e de `[rbp+0x430]` em `0x86FE90` (logo `N` e `n` em 48 kHz);
- alinhamento da base da arena (decide se a cabeça de 8 elementos existe) nos 4 sítios
  `008C2545` / `008C263D` / `008C273B` / `008C2828`;
- ordem exata do bloco de 8 da cauda (`000643DD`–`0006468D`): lido que é **A**; falta a
  cópia/contagem interna;
- o `call 0x1796910` em `000643CC` é o `__security_check_cookie` (epílogo), não aritmética.
