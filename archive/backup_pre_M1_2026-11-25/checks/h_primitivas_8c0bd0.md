# H — Primitivas da cadeia de `0x8C0BD0` e transcrição do bloco aritmético

**Fonte única:** `dumpsooth/nyx_soothe3_dump.bin` (137.003.008 B, SHA-256
`68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`), layout flat (RVA = offset).
**Método:** `py -3 tools/show_func.py <rva>` (chain-aware, `.pdata` + `UNW_FLAG_CHAININFO`),
`py -3 tools/dispatch.py`, desmontagem Capstone com bytes lidos em `re_lib.data()`.
Nenhum decompilado participou; decompilado/spec antiga só foram consultados *depois* para
conferência, e onde divergem desta leitura a instrução vence (ver §5).
Convenção Win64: inteiros `rcx, rdx, r8, r9`; floats `xmm0, xmm1, xmm2` (ordem independente).

---

## 1. Tabela — assinatura provada, registro por registro

| thunk | impl | assinatura provada (registradores) | in place? | instrução que prova (RVA + bytes) |
|---|---|---|---|---|
| `0x1190` | `0x4BC0` (480 B) | `void f(const f32 *a/*rcx*/, const f32 *b/*rdx*/, f32 *dst/*r8*/, int n/*r9d*/)` — `dst[i] = a[i]*b[i]` | **NÃO** (3º ponteiro) | `00004BC7 48 89 d5` `mov rbp,rdx`; `00004BCA` `test rcx,rcx`; `00004BDC` `test r8,r8`; `00004BE5` `test r9d,r9d`; `00004C60 c5 fa 10 04 81` `vmovss xmm0,[rcx+rax*4]`; `00004C65 c5 fa 59 4c 85 00` `vmulss xmm1,xmm0,[rbp+rax*4]`; `00004C6B c4 c1 7a 11 0c 86` `vmovss [r8+rax*4],xmm1` |
| `0x1550` | wrapper `0xC560` → impl `0x63640` (4224 B) | `void f(const f32 *den/*rcx*/, const f32 *num/*rdx*/, f32 *dst/*r8*/, int n/*r9d*/)` — `dst[i] = num[i]/den[i]` | **NÃO** (3º ponteiro) | wrapper: `0000C577` `test r9d,r9d`; `0000C57C e8 bf 70 05 00` `call 0x63640` (repassa rcx/rdx/r8/r9 intactos); impl: `00063653` `mov rdi,r8` (dst); `00063676 48 89 d5` `mov rbp,rdx` (numerador); `000636E0 c4 a1 7c 10 04 a1` `vmovups ymm0,[rcx+r12*4]`; `000636E6` `vmovups ymm1,[rbp+r12*4]`; `0006376F` `vblendvps` (den 0 → 1.0f); `00063775 c5 fc 53 c5` `vrcpps ymm0,ymm5`; `00063787 c4 c1 7c 59 45 20` `vmulps ymm0,ymm0,[r13+0x20]`; `00063A27 c4 81 7c 11 04 98` `vmovups [r8+r11*4],ymm0`; `0006467A c4 c1 7c 11 00` `vmovups [r8],ymm0` |
| `0x11F0` | `0x5BC0` (0x5BC0–0x5CFA) | `void f(const f32 *src/*rcx*/, float s/*xmm1*/, f32 *dst/*r8*/, int n/*r9d*/)` — `dst[i] = dst[i] + s*src[i]` | **SIM** (`dst` é lido e escrito) | `00005BC4` `test rcx,rcx`; `00005BCD` `test r8,r8`; `00005BD6` `test r9d,r9d`; `00005BDF 4d 63 d1` `movsxd rdx,r9d` (rdx **não** é dado); `00005C40 c4 a1 7a 10 04 91` `vmovss xmm0,[rcx+r10*4]`; `00005C46 c4 82 71 a9 04 90` `vfmadd213ss xmm0,xmm1,[r8+r10*4]`; `00005C4C` `vmovss [r8+r10*4],xmm0`; `00005C5A c4 e2 7d 18 c1` `vbroadcastss ymm0,xmm1`; `00005C85` `vfmadd213ps ymm2,ymm0,[r8+rax*4]`; `00005C8B` `vmovups [r8+rax*4],ymm2` |
| `0x1370` | `0xA120` (416 B) | `void f(const f32 *src/*rcx*/, f32 *dst/*rdx*/, int n/*r8d*/)` — `dst[i] = dst[i] + src[i]` | **SIM** | `0000A125 48 89 d7` `mov rdi,rdx` (dst); `0000A128` `test rcx,rcx`; `0000A131` `test rdi,rdi`; `0000A13A` `test r8d,r8d`; `0000A1A0 c5 fa 10 04 91` `vmovss xmm0,[rcx+rdx*4]`; `0000A1A5 c5 fa 58 0c 97` `vaddss xmm1,xmm0,[rdi+rdx*4]`; `0000A1AA c5 fa 11 0c 97` `vmovss [rdi+rdx*4],xmm1` |
| `0x1100` | `0x3480` (0x3480–0x375F) | `void f(f32 *buf/*rcx*/, int n/*edx*/, float bound/*xmm2*/, int mode/*r9d*/)` — `mode 4` → `buf[i]=min(bound,buf[i])`; `mode 0` → `buf[i]=max(bound,buf[i])` | **SIM** (1 ponteiro) | `00003484` `test rcx,rcx`; `0000348D` `test edx,edx`; `00003495 45 85 c9` `test r9d,r9d` → `00003498 je 0x35D9` (modo 0); `0000349E` `cmp r9d,4`; `000034A4 b8 fb ff ff ff` `mov eax,-5`; `00003500 c5 ea 5d 04 81` `vminss xmm0,xmm2,[rcx+rax*4]`; `00003505` `vmovss [rcx+rax*4],xmm0`; `00003640 c5 ea 5f 04 81` `vmaxss xmm0,xmm2,[rcx+rax*4]`; `00003645` `vmovss [rcx+rax*4],xmm0` |

Varredura de operandos RIP-relativos nos cinco impls (`0x4BC0`, `0x5BC0`, `0xA120`, `0x3480`,
`0xC560`): **nenhum**. Não há constante float nessas funções; o escalar chega só por `xmm1`/`xmm2`.
`0x63640` tem exatamente 3 operandos RIP-relativos: `0x21C7640` (cookie de pilha, `00063679` e
`00063682`) e `0x1DF9DA0` (vetor de oito `1.0f`, `0x3F800000` ×8, `0006368F`), usado no blend do
denominador 0 (`0006376F`) e no refinamento de Newton (`00063782`).

### 1.1 O que cada impl faz no laço (carga → conta → store)

**`0x4BC0` (`0x1190`, multiplicação vetorial, fora do lugar).** Três ponteiros independentes.
Laço escalar de prólogo (desalinhamento): `00004C60 vmovss xmm0,[rcx+rax*4]` →
`00004C65 vmulss xmm1,xmm0,[rbp+rax*4]` → `00004C6B vmovss [r8+rax*4],xmm1`.
Corpo AVX2: `00004C80/00004C85` carregam `[rcx+rsi*4]` e `[rcx+rsi*4+0x20]`;
`00004C8B vmulps ymm1,ymm0,[rbp+rsi*4]`; `00004C91 vmulps ymm3,ymm2,[rbp+rsi*4+0x20]`;
`00004C97/00004C9D vmovups [r8+rsi*4]`. Cauda 128-bit em `00004D00–00004D0C`
(`rsi=rcx+rdx*4`, `rdi=rbp+rdx*4`, `r10=r8+rdx*4`, montados em `00004CD5/00004CDC/00004CE1`) e
cauda escalar em `00004D40–00004D4B`. `rdx` é lido **antes** de ser usado como scratch
(`00004BC7`), logo é a 2ª entrada. Retornos: `00004D79 mov eax,-6` (n≤0), `00004D82 mov eax,-8`
(ponteiro nulo), `00004D58 xor eax,eax` (sucesso).

**`0xC560` → `0x63640` (`0x1550`, divisão).** O thunk (`idx=4` em `0x21C7408`, tabela de saltos
`0x21C6448`) aponta para `0xC560`, que **não calcula nada**: valida `rcx`/`rdx`/`r8` não nulos e
`r9d>0` (`0000C568`–`0000C57A`), chama `0x63640` com os quatro registradores intactos
(`0000C57C`) e converte o retorno: `mov edx,2; test eax,eax; cmovne eax,edx` (`0000C581`–
`0000C588`) → devolve `0` ou `2`.
Dentro de `0x63640`: `rdi=r8` é o destino (`00063653`), `rbp=rdx` é o **numerador**
(`00063676`), `rcx` é o **denominador**. Caminho vetorial de 8 floats: copia `[rcx]` e `[rbp]`
para um scratch de 64 B (`000636E0`, `000636E6`, stores em `000636ED`/`000636FB`);
`0006376A vcmpeqps` marca denominador 0, `0006376F vblendvps ymm5,ymm2,ymm4,ymm1` troca 0 por
`1.0f` (ymm4 = `[0x1DF9DA0]`), `00063775 vrcpps`, `00063782 vfnmadd213ps ymm3,ymm0,ymm4`
(resíduo `1−d·r`), `00063787 vmulps ymm0,ymm0,[r13+0x20]` (r × numerador), dois passos de Newton
`00063791`/`00063796`, store em `00063A27`/`00063A20`. Caminho de 32 floats:
`00063AC0`/`00063AC6` carregam dois ymm do denominador, `00063B37 vmulps ymm7,ymm8,[r15+r10]`
multiplica o recíproco refinado pelo numerador (`r10 = rbp = rdx`, `r15+rdi` = `rcx`),
store em `0006467A vmovups [r8],ymm0`, avanço `00064681/85/89 add rcx/rbp/r8,0x20`, laço em
`0006401A`. Cauda escalar: `00064380–00064385` (`mov edx,[r13+r9*4]` → `mov [r8+r9*4],edx`), que
também é store **em `r8`**. Saída: `00064391` recarrega o cookie, `000643AB cmp rcx,[0x21C7640]`,
`000643CB ret` devolvendo `eax` = OR dos flags de caso especial (0 ou 1); o wrapper converte em
`0`/`2` (`0000C588 cmovne`). Ou seja: **`dst = num/den`, `den=rcx`, `num=rdx`** — divisão, não
recíproco puro.

**`0x5BC0` (`0x11F0`, FMA).** `rdx` não é argumento (`00005BDF movsxd rdx,r9d` só monta o
contador). O escalar entra em **`xmm1`** (primeira leitura antes de qualquer escrita:
`00005C46`, e `00005C5A vbroadcastss ymm0,xmm1`). `vfmadd213ss xmm0,xmm1,[r8+r10*4]` significa
`xmm0 = xmm0*xmm1 + mem`, com `mem = dst[i]` → `dst[i] += src[i]*s`; store em
`00005C4C`. AVX2 em `00005C80–00005C8B`, cauda em `00005CC0–00005CCC`.

**`0xA120` (`0x1370`, soma vetorial in place).** `rdx` é o **destino** (`0000A125 mov rdi,rdx`),
`rcx` a fonte, `r8d` o `n`. **Não há escalar**: a primeira instrução que toca xmm é
`0000A1A0 vmovss xmm0,[rcx+rdx*4]` (leitura de memória); nenhum `xmm` é lido como entrada e não
há operando RIP-relativo. Logo `0xA120` é `dst += src`, não `+=` escalar.

**`0x3480` (`0x1100`, clamp in place).** Um único ponteiro (`rcx`), `n` em `edx`, limite em
**`xmm2`** (primeira leitura de xmm: `00003500`/`00003640`), modo em `r9d`. `r9d==0` desvia em
`00003498` para o bloco de `vmaxss` (`00003640`); `r9d==4` cai em `000034AA` (bloco `vminss`,
`00003500`); qualquer outro valor devolve `-5` (`000034A4`). `vminss xmm0,xmm2,mem` = `min(xmm2,
mem)` e o store é na própria memória → `mode 4` = teto, `mode 0` = piso. Vetorial:
`00003520/00003526 vminps`, `00003660/00003666 vmaxps`; 128-bit `00003580`, `000036C0`; cauda
escalar `000035C3`, `00003703`. Retornos `-6` (`00003735`), `-8` (`0000373B`).

---

## 2. `0x8C0BD0` — assinatura de entrada e moldura de pilha

```
008C0BD0  mov  [rsp+8],rcx          ; arg0 self
008C0BD6  push rbp/r13/r14
008C0BDA  lea  rbp,[rsp-0x1440]     ; moldura total 0x1540
008C0BE2  mov  eax,0x1540 / 008C0BE7 call 0x17978C0  ; probe de pilha (padrão __chkstk)
008C0BF6  mov  r13,r9               ; arg3 = arena (r9)
008C0C01  mov  r14,rcx              ; self
008C0C04  movaps xmm7,xmm1          ; g (único float de entrada)
```
`rcx`=self, `r8`=lista de descritores (lê `[r8]`=`begin` em `008C0C1F`, `[r8+8]`=`end` em
`008C0C0D`), `r9`=arena. **`rdx` nunca é lido como argumento** (o primeiro uso é
`008C0C11 mov edx,[rcx+0x404]`); **`xmm0` nunca é lido**. Logo só se prova: escalar de entrada em
`xmm1` e, por isso, ≥6 parâmetros na declaração original.

Campos de `self` provados por uso: `008C0BEF 83 b9 00 04 00 00 01` `cmp dword [rcx+0x400],1`
(saída antecipada), `008C0C11 8b 91 04 04 00 00` `mov edx,[rcx+0x404]` → `N` (guardado em
`[rsp+0x20]`, `008C0C22`).

**Estrutura local (provada por offsets):** cinco descritores contíguos de **0x410 B** cada,
`{ f32 *ptr[128] ; i32 count ; i32 len ; i32 len*4 }` — o header mora no fim (últimos 0x10 B):

| descritor | tabela | header (`count`,`len`,`len*4`) | `len` usado em |
|---|---|---|---|
| `T` (temp) | `rbp-0x60` | `rbp+0x3A0` (escrito em `008C0CC3/CC9/CCF`) | — (é a origem das cópias) |
| `DA` | `rbp+0x3B0` | `rbp+0x7B0` (vem da cópia de `AR`) | `008C0F17 mov r15d,[r15]` com `r15=rbp+0x7B4` |
| `AR` (arena) | `rbp+0x7C0` | `rbp+0xBC0` (escrito em `008C0D4D/53/59`) | — (é a origem da cópia de `DA`) |
| `DB` | `rbp+0xBD0` | `rbp+0xFD0` (vem da cópia de `T`) | `008C128D lea rax,[rbp+0xFD4]` |
| `DC` | `rbp+0xFE0` | `rbp+0x13E0` (vem da cópia de `T`) | — |

Cada bloco é copiado por inteiro (0x400 B de tabela + 0x10 B de header = **0x410 B**), provado em
`008C0DBA mov edx,8` / laço `008C0DD0` (8 × 0x80 B) / `008C0E1D sub rdx,1` / store final de 16 B em
`008C0E23–008C0E2F`. Os headers `{2, N, N*4}` são escritos em `008C0CC3/CC9/CCF`
(`[rbp+0x3A0/A4/A8]`) e `008C0D4D/53/59` (`[rbp+0xBC0/C4/C8]`) — e por isso `[rbp+0x7B4]` e
`[rbp+0xFD4]` (headers de `DA` e `DB`) ficam inicializados **por cópia**, não são lixo de pilha.

---

## 3. Pseudocódigo do bloco aritmético (RVA em cada linha)

```c
/* 0x8C0BD0(self=rcx, rdx=morto, list=r8, ar=r9, xmm0=morto, g=xmm1) */
008C0BEF  if (*(i32 *)(self + 0x400) == 1) return;
008C0C0D  end = *(u64 *)(list + 8);
008C0C11  N   = *(i32 *)(self + 0x404);            /* [rsp+0x20] */
008C0C1F  d   = *(u64 *)(list + 0);
008C0C2F  if (d == end) return;
008C0C73  one = 1.0f;                              /* [0x2079F9C] */
008C0C85  eps = 1.1920929e-7f;                     /* [0x2079CF0] */

008C0C90  for (; d != end; d += 0x18) {             /* 008C13CD add rsi,0x18 ; 008C13D6 cmp */
008C0C90      if (*(i32 *)(d + 0x10) != 2) continue;        /* 83 7e 10 02 ; 0f 85 33 07 */
008C0CDA      i = *(i32 *)(d + 0x08);                      /* movsxd rax,[rsi+8] */
008C0CE6      /* T.ptr[0..1] = ((u64*)self)[i .. i+1] : offset = i*8, base = self */
008C0CA7      T.ptr[0] = 0;   008C0CB1  memset(&T.ptr[1], 0, 0x3F8);   /* zera a tabela de 128 slots */
008C0CC3      T = { 2, N, N*4 };                            /* [rbp+0x3A0..0x3A8] */
008C0D00      for (k = 0; k < 2; k++) T.ptr[k] = *(u64 *)(self + (i + k)*8);
008C0D1D      saved = ar->cursor;                          /* lido em 008C0D1D, guardado em [rsp+0x4C] */
008C0D34      AR.ptr[0] = 0;  008C0D3B  memset(&AR.ptr[1], 0, 0x3F8);
008C0D4D      AR = { 2, N, N*4 };                           /* [rbp+0xBC0..0xBC8] */
008C0D70      for (k = 0; k < 2; k++) {                          /* 008C0DA7 cmp r8,r9 */
008C0D70          AR.ptr[k] = (f32 *)(ar->base + ar->cursor*4);      /* [r13] + cursor*4 */
008C0D8F          ar->cursor = (v & 0xf) ? (v - (v & 0xf) + 0x10) : v;   /* v = cursor + N */
008C0DA3      }
008C0DB3      DC = T;   008C0E32  DB = T;   008C0EA5  DA = AR;        /* cópia de 0x410 B */
008C0F20      for (k = 0; k < 2; k++)                                /* rsi = r14d = 2 */
008C0F3B          mul_32f(rcx=DB.ptr[k], rdx=DC.ptr[k], r8=DA.ptr[k], r9d=N);
                     /* DA[k][j] = P_k[j] * P_k[j]  (quadrado de cada buffer) */

008C0FB8      P1 = ar->base + ar->cursor*4;   /* [rsp+0x70] = { P1, N, N*4 } */
008C0FF9      P2 = ar->base + ar->cursor*4;   /* [rsp+0x60] = { P2, N, N*4 } */
008C1015      DB = AR;      /* dest 0xBD0 (008C1015), src 0x7C0 (008C1030), laço 008C1040 */
008C10AA      memset_32f(rcx=P1, edx=N);                          /* 0x10D0 */
008C10D0      for (k = 0; k < 2; k++)
008C10D9          add_32f(rcx=DB.ptr[k], rdx=P1, r8d=N);            /* P1 += quadrados */
008C10FD      DC = T;                                              /* 008C10ED dest 0xFE0 */
008C116E      memset_32f(rcx=P2, edx=N);
008C1190      for (k = 0; k < 2; k++)
008C1199          add_32f(rcx=DC.ptr[k], rdx=P2, r8d=N);            /* P2 += P_k */
008C11BF      clamp_32f(rcx=P2, edx=N, xmm2=eps, r9d=0);            /* P2 = max(P2, eps) */
008C11DD      P3 = ar->base + ar->cursor*4;      /* 008C11C4..008C1211 aloca {P3,N,N*4} */
008C1218      div_32f(rcx=P2, rdx=P1, r8=P3, r9d=N);               /* P3 = P1 / P2 */
008C1229      DB = T;
008C128D      n2 = *(i32 *)((u8 *)&DB + 0x404);    /* [rbp+0xFD4] = N (header de DB) */
008C12A4      xmm6 = one - g;                    /* 008C12A0/008C12A4 subss */
008C12B0      for (k = 0; k < 2; k++)
008C12B9          scale_32f(rdx=DB.ptr[k], xmm0=xmm6, r8d=n2);      /* P_k *= (1-g) */
008C12D9      DA = T;
008C1390      for (k = 0; k < 2; k++)
008C139C          fma_32f(rcx=P3, r8=DA.ptr[k], r9d=N, xmm1=g);     /* P_k += g*P3 */
008C13AB      ar->cursor = saved;                                  /* [r13+0x18] = [rsp+0x4C] */
008C13CD  }                                                        /* d += 0x18 */
```

Chamadas e contagem: `008C0F3B` e `008C0F86` (`0x1190`), `008C10AA` e `008C116E` (`0x10D0`),
`008C10D9` e `008C1199` (`0x1370`), `008C11BF` (`0x1100`), `008C1218` (`0x1550`), `008C12B9`
(`0x1220`), `008C1366` e `008C139C` (`0x11F0`) — 14 `call` com `008C0CB1`/`008C0D3B`
(`0x1798F42`, chamada com `(ptr,0,0x3F8)`; padrão de `memset`) e `008C0BE7` (`0x17978C0`, probe de
pilha) — coerente com "14 calls".

Os dois caminhos "solteiro" (`008C0F4C`, `008C134E`) exigem `count==1`; como a porta é
`*(i32*)(d+0x10)==2`, `r14d` e `edi` valem 2 em `008C0F09`/`008C1349` e esses caminhos são
**inalcançáveis** neste gate.

### 3.1 O que a cadeia calcula (i)

Para cada descritor de 24 B com `+0x10 == 2`, com `P0, P1` = `((f32**)self)[i]`, `((f32**)self)[i+1]`
(`i` = `*(i32*)(d+8)`), elemento a elemento em `j = 0..N-1`:

```
sum2 = P0² + P1²                                  (0x1190 em DA, 0x1370 somando em P1)
sum  = P0 + P1                                    (0x1370 somando em P2)
sum  = max(sum, 1.1920929e-7f)                    (0x1100 modo 0, R=0x2079CF0)
R    = sum2 / sum                                 (0x1550: dst = rdx/rcx)
P_k  = (1 - g) * P_k + g * R      para k = 0,1    (0x1220 e 0x11F0)
```

Ou seja: **média ponderada por potência** `R = (P0²+P1²)/max(P0+P1, ε)`, e cada um dos dois
buffers é misturado a ela com peso `g` (dry/wet). Consequência aritmética direta das mesmas
instruções: se `P1 = 0`, então `R = P0` e `P0` fica intacto enquanto `P1 ← g·P0` (o buffer mudo
recebe uma cópia do outro, atenuada por `g`); se `P0 = -P1`, o denominador cai em `ε` e `R` fica
enorme — **não existe clamp superior nesta cadeia** (só o `max` em `008C11BF`).

---

## 4. Constantes

| RVA | bits | valor | onde é lida |
|---|---|---|---|
| `0x2079F9C` | `0x3F800000` | `1.0f` | `008C0C73 f3 44 0f 10 05 20 93 7b 01` `movss xmm8,[rip]`; usada em `008C12A4 subss xmm6,xmm8,xmm7` |
| `0x2079CF0` | `0x34000000` | `1.19209290e-7f` (`2^-23`) | `008C0C85 f3 44 0f 10 0d 62 90 7b 01` `movss xmm9,[rip]`; passada em `008C11B8 movaps xmm2,xmm9` |
| `0x1DF9DA0` | `0x3F800000` ×8 | vetor de `1.0f` | `0006368F c5 fc 10 25 09 67 d9 01` `vmovups ymm4,[rip]` (blend do denominador 0 em `0006376F`, Newton em `00063782`) |
| `0x21C7640` | — | cookie de pilha (`xor rax,rsp`) | `00063679`, `00063682`, conferência no epílogo |
| imediatos de `0x63640` | `0x7F800000`, `0x7FBFFFFF`, `0x80000000` | `+inf`, `0x7FBFFFFF` (NaN), máscara de sinal | tratamento de denominador 0: `000637D2`–`000639EC`, `00063B81`–`00064674` |

`0x207A360 = 0x41200000 = 10.0f` **não é referenciado por `0x8C0BD0`** nem pelos cinco impls
(a varredura de operandos RIP-relativos devolve só `0x2079F9C`, `0x2079CF0` e o cookie).

Constantes inteiras de moldura (não float): `0x1540` (tamanho da pilha, `008C0BE2`), `0x3F8`
(zero-fill das tabelas, `008C0CB1`/`008C0D3B`), `0x18` (passo do descritor, `008C13CD`), `0x410`
(tamanho de cada bloco copiado = `8 × 0x80 + 0x10`).

---

## 5. Correções impostas por esta leitura

1. `0x1370`/`0xA120` **não é** `+=` escalar (rótulo da §22.3 do plano): é `dst += src`, dois
   ponteiros, sem `xmm`. Prova `0000A1A5` e ausência de leitura de `xmm` como entrada.
2. `0x1190`/`0x4BC0` **não é** in place: `dst` é `r8` (`00004BC7 mov rbp,rdx` + store em
   `[r8+rax*4]`, `00004C6B`).
3. O escalar de `0x11F0` está em **`xmm1`** (`00005C46`), não em `xmm0`; `rdx` é contador
   (`00005BDF`).
4. O limite de `0x1100` está em **`xmm2`** (`00003500`/`00003640`), não em `xmm0`/`xmm1`.
5. `0x1550` é **divisão** `num/den` com `den=rcx` e `num=rdx` (`00063787`), não recíproco puro;
   `0x1550` aponta para o wrapper `0xC560`, que só valida e repassa para `0x63640`.
6. O campo `+8` do descritor é **índice s32** (`008C0CDA movsxd rax,[rsi+8]`; `008C0CE6
   lea rax,[rax*8]`), não ponteiro — a §22.3 do plano diz "ponteiro em `+8`".

---

## 6. NÃO PROVADO

- **Identidade dos buffers `P0`/`P1`.** Que sejam "esquerda/direita", "bandas", "env" ou "sinal"
  não está provado: só se sabe que são dois `f32*` consecutivos na tabela `self[i..i+1]`
  (`008C0D00`).
- **Papel do campo `+0x10 == 2`** no descritor de 24 B. É uma comparação de igualdade com 2
  (`008C0C90`); que signifique "tipo/estágio 2" é nome, não prova. O outro campo usado é `+8`
  (índice); `+0x00` e `+0x14` do descritor nunca são lidos aqui.
- **Semântica de `self+0x400` e `self+0x404`.** `+0x404` é a contagem `N` usada em todos os `n`
  (via `[rsp+0x20]`); `+0x400 == 1` aborta a função. Que sejam "bypass" e "nº de canais" é
  hipótese.
- **Significado musical de `g` (xmm1) e existência do 5º/6º parâmetro.** `xmm0` nunca é lido;
  `rdx` nunca é lido. A ordem declarada dos parâmetros não é recuperável só dos registradores.
- **Layout/propriedade do "arena" (`r9`).** Provado por uso: `ar->base = *(u64*)ar` (`008C0D70`),
  `ar->cursor = *(i32*)(ar+0x18)` (`008C0D1D`, `008C0DA3`, restaurado em `008C13AB`), buffers de
  `N` floats alinhados a 16 floats (`008C0D8F`–`008C0D9C`). O resto do objeto é desconhecido.
- **Tipo nominal do bloco de 0x410 B** (`{ptr[128]; count; len; len*4}`). A forma está provada
  pelos offsets; ser um tipo IPP/`IppsArray` e o significado de `count==2` (nº de ponteiros) são
  inferência estrutural, não nome provado.
- **Se `0x8C0BD0` é "lei de ganho" ou "detector".** A cadeia só faz a conta acima; nenhum
  coeficiente de filtro, nenhuma constante de tempo e nenhum estado de envelope aparecem nela.
- **Ausência de clamp superior em `R`.** É o que as instruções mostram (só `max` em
  `008C11BF`), mas se isso é intencional (e como o chamador trata `R` grande) não está provado.
- **Constantes float citadas em outras seções** (p.ex. `0x207A360 = 10.0f`) não pertencem a esta
  cadeia: nenhum operando RIP-relativo de `0x8C0BD0` as referencia.

---

## Atualização 2026-11-25 — `0x63640` não é uma única sequência

O mapa de despacho e as **duas** aritméticas estão em `checks/r_divisao_63640.md`:
16 lanes refinam o recíproco (`00063B24`/`00063B29`, multiplicação no fim em `00063B37`);
8 lanes refinam o quociente (`00063791`/`00063796`); a cabeça depende de `dst & 0x1c`
(`00063697`) e `n = N+1` é ímpar, então a cauda sempre roda (`0006400D`/`0006401A`).
