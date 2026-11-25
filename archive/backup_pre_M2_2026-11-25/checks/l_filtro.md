# L — Tipo de filtro e curva por banda (soothe3)

> Status: **CONCLUÍDO** para o escopo pedido; itens abertos em §6.
> Fonte única: `dumpsooth/nyx_soothe3_dump.bin`
> SHA-256 verificado nesta sessão: `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`
> Convenção: endereços são **RVAs** (imagem `0x180000000`). Ponteiros de dado no dump têm VA base `0x199B0000`; `RVA = VA - 0x199B0000`.
> Somente leitura estática. Nenhum hook/patch/injeção/escrita em binário ou processo.
> Ferramentas: `tools/show_func.py` (chain-aware, resolve `.pdata` UNW_FLAG_CHAININFO), `tools/win2.py`, `tools/resolve_thunk.py`, `tools/scan_region.py`.
> `functions.csv` **não** foi usado como prova. `params.csv` **não** foi usado como prova.

Extensão real das funções (via `chain_extent`, não via CSV):

| função | início | fim | tamanho | observação |
|---|---|---|---|---|
| `0x87BB60` | `0x87BB60` | `0x87DB28` | 8136 B | 35 `call` (confere com o enunciado) |
| `0x87E220` | `0x87E220` | `0x87F0BB` | 3739 B | |
| `0x87B2A0` | `0x87B2A0` | `0x87B674` | 980 B | |
| `0x8CAB40` | `0x8CAB40` | `0x8CAE8F` | 847 B | |
| `0x8CB040` | `0x8CB040` | `0x8CB2E8` | 680 B | |
| `0x8CB2F0` | `0x8CB2F0` | `0x8CB5E5` | 757 B | |

---

## 1. Já provado antes dos alvos: stub `0x1400`, `0x86F480` e satélites

### 1.1 Stub de despacho `0x1400` → tabela `0x21C6288` → `0xAC20` (linha única — alvo do agente K)

Prova (dump):

```
00001400  movsxd rax, dword ptr [0x21C7408]   ; índice = 4
00001407  lea    r10, [0x21C6288]              ; tabela de ponteiros
0000140E  jmp    qword ptr [r10 + rax*8]       ; [4] = 0x199BAC20 -> RVA 0xAC20
```

- Tabela: `0x21C6288`; índice `4` (`0x21C7408` = 4); alvo `0x199BAC20` → **RVA `0xAC20`**.
- Registrado **apenas como dependência estrutural** (chamado em `0x8CB24B`). **Não** foi dissecado: pertence ao agente K.

### 1.2 `0x86F480` — construtor de view deslocada (chamado por `0x8CAB40` em `0x8CAB6B`)

Escreve um descritor grande de destino a partir de uma origem `+offset`.

```
0086F4A1  edi  = [rcx + 0x90]              ; comprimento
0086F4B8  edi -= [rax + 0x88]              ; ajuste pelo stride
0086F4C1  rcx  = (i64)[rax + 0x88]         ; stride
0086F59D  rax  = (i64)[r9 + 0x90]          ; len
0086F698  rcx  = rbp - 0x50                ; lista de ponteiros local
0086F69C  r8   = edx*8                     ; bytes de ponteiros
0086F6A5  call 0x1798F36                   ; memcpy (thunk_map.txt:160)
0086F6B2  [rbx]     = xmm0                 ; cabeçalho do descritor de destino
0086F6BD  [rbx+0x10]= xmm1
0086F6C5  [rbx+0x20]= xmm0
0086F6CC  [rbx+0x30]= xmm1
```

**Efeito:** materializa uma view do descritor grande deslocada em `[rcx+0x90]`/`[rax+0x88]`, copiando a lista de ponteiros e gravando o cabeçalho em `[rbx]…[rbx+0x30]`. Não toca amostras.

### 1.3 Descritor grande (formato dos satélites)

| offset | tipo | significado |
|---|---|---|
| `+0x00 … +0x3F8` | `void*[128]` | até 128 ponteiros |
| `+0x400` | `int32` | contagem |
| `+0x404` | `int32` | contagem (len) |
| `+0x408` | `int32` | stride em bytes |

Prova: `0x867CC0` escreve `[r15+0x400]=ebx`, `[r15+0x408]=r9*4`, `[r15+0x404]=r9d` (`0x867D03`–`0x867D18`) e percorre `[r14+0x400]` ponteiros (`0x867D1F`); `0x8CAB40` copia `0x400` bytes em 8 blocos de `0x80` (`0x8CABE2` `mov r14d,8`, laço `0x8CAC00`–`0x8CAC51`).

### 1.4 `0x8CAB40` (847 B) — view deslocada + cópia

Chamadores (2):

| sítio | função |
|---|---|
| `0x8BF955` | `0x8BF650` |
| `0x8BFB84` | `0x8BF99F` |

Assinatura (por uso): `void f(ctx=rcx, view_ou_src=rdx)`.
- `0x8CAB57` `r8d = [rcx+0x404]` (contagem), `0x8CAB61` `r13 = rcx`.
- `0x8CAB68` `rcx = rdx` (origem), `0x8CAB6B` `call 0x86F480(rcx=origem, rdx=&local0x50, r8d=contagem)` — ver §1.2.
- `0x8CABDD` `call 0x867CC0(rcx=&local0xd0, rdx=ctx, r8d=0, r9d=edi)` — `0x867CC0` zera o destino, copia a contagem de `[src+0x400]`, grava count/stride e ajusta cada ponteiro por `offset*4` (`0x867D03`–`0x867D54`), i.e. **recorta uma janela de canais**.
- `0x8CABE2` `mov r14d,8` + laço `0x8CAC00`–`0x8CAC51`: copia **0x400 bytes** (8×0x80) do descritor para `[rbp+0x4e0]` — cópia integral da lista de 128 ponteiros.
- `0x8CACA0`/`0x8CACE9`/`0x8CAE30`/`0x8CAE69` `call 0x10A0` — copia dados entre a view e o buffer (`0x10A0` → `0x2C80`).

**Efeito estrutural:** materializa uma **view deslocada** de um bloco multichannel (até 128 ponteiros) e copia os dados entre origem e destino; não altera amostras, só resolve ponteiros/stride.

### 1.5 `0x8CB040` (680 B) — reduz banda → 1 float

Chamador (1): `0x8C33BD` em `0x8C32C0`.

Assinatura (por uso): `void f(rcx=bloco, rdx=?, r8=descritor, r9=saída)`.
- `0x8CB071` `edx = [r9+0x18]`, `0x8CB074` `r10d = [rdx+0x404]`, `0x8CB091` `rax = [rcx+0x404]`, `0x8CB0B7` `r8 = [rcx+0x400]`, `0x8CB0F2` `ecx = [rdx+0x404]`.
- `0x8CB100` `eax = [r14+0x80]` (campo `+0x80` do elemento/descritor corrente), `0x8CB107` `rdx = [r14]` (offset).
- `0x8CB132`/`0x8CB140`: `ecx = [rdi+0x190]`, se 0 usa `[rdi+0x180]`; stride `[rdi+0x188]` — três descritores aninhados no bloco `r13` (`+0x100`, `+0x180/0x188/0x190`, `+0x198`).
- `0x8CB21E` `call 0x1798F36` (`memcpy`) da lista de ponteiros.
- `0x8CB24B` `call 0x1400` — resolvido em §1.1 para **RVA `0xAC20`** (alvo do K; registrado só como dependência).
- `0x8CB266` `movss [r12 + r15*4], xmm0` — grava **um float por elemento** (redução).

**Efeito estrutural:** por elemento de banda, monta a lista de ponteiros, aplica a operação `0xAC20` entre buffers deslocados e **escreve um escalar por elemento**; é o estágio que reduz banda → número.

### 1.6 `0x8CB2F0` (757 B) — acumula banda com FMA

Chamador (1): `0x8C3EFD` em `0x8C3E00`.

Assinatura (por uso): `void f(rcx=bloco, rdx=?, r8=descritor)`.
- `0x8CB31F` `mov r10d,8` + laço `0x8CB330`–`0x8CB389`: copia **0x400 bytes** (8×0x80) de `rcx` para a pilha (cópia integral do descritor grande).
- `0x8CB3A2` `eax = [rbp+0x3e0]`; `0x8CB3C5` `call 0x10D0` — **zera** cada ponteiro (contagem em `+0x3e0`, stride `+0x3e4`).
- `0x8CB3DB` `rax = [r12+0x404]`, `0x8CB3F2` `r8 = [r11+0x400]`, `0x8CB420` `eax = [r15+0x80]`, `0x8CB427` `rdx = [r15]` — mesmo esquema de offset por elemento.
- `0x8CB451`/`0x8CB460`: `ecx = [r13+0x190]` senão `[r13+0x180]`, stride `[r13+0x188]`, ponteiros em `[r13+0x100]`.
- `0x8CB54C` `call 0x1798F36` (`memcpy`) da lista de ponteiros.
- `0x8CB562` `xmm1 = [rbx+rsi*4]` (coeficiente por elemento), `0x8CB571` `call 0x11F0` — kernel FMA (`0x21C5FC8[4]` → `0x199B5BC0` = RVA `0x5BC0`, `vfmadd213ss/ps`), i.e. **`dst += coef · src` para cada canal**.

**Efeito estrutural:** acumula cada banda escalada por um coeficiente no buffer de saída (mistura soma-ponderada). Não tem aritmética escalar própria; toda a conta é o FMA `0x11F0`.

---

## 2. `0x87BB60` — estágio por banda (tipo de filtro / coeficientes / flag@0x80)

### 2.1 Chamadores (22 sítios, varredura `E8/E9 rel32` em `.text`)

| sítio do `call` | função chamadora |
|---|---|
| `0x8730FB` | `0x86FE90` |
| `0x8769F6` | `0x873440` |
| `0x88539E` | `0x885040` |
| `0x88794E` | `0x8875F0` |
| `0x889F4C` | `0x889C18` |
| `0x88B1BC` | `0x88AE88` |
| `0x88EC71`, `0x88EC93` | `0x88E8A0` |
| `0x8918E1`, `0x891903` | `0x891510` |
| `0x894573` | `0x894170` |
| `0x8960F3` | `0x895CF0` |
| `0x89AF7E` | `0x89AC20` |
| `0x89D52E` | `0x89D1D0` |
| `0x89FB2C` | `0x89F7F8` |
| `0x8A0D9C` | `0x8A0A68` |
| `0x8A2B61`, `0x8A2B83` | `0x8A2790` |
| `0x8A57D1`, `0x8A57F3` | `0x8A5400` |
| `0x8A8463` | `0x8A8060` |
| `0x8A9FE3` | `0x8A9BE0` |

Cadeia de chamada provada em `0x86FE90` (mesmo objeto `rdi` = ctx, `rdx = r15` = arena de scratch):

```
008730DA  mov  rcx, rdi
008730DD  call 0x878070
008730E2  mov  rcx, rdi
008730E5  call 0x87b2a0      ; estágio anterior
008730EA  mov  rdx, r15
008730ED  mov  rcx, rdi
008730F0  call 0x87b680
008730F5  mov  rdx, r15
008730F8  mov  rcx, rdi
008730FB  call 0x87bb60      ; <<< este alvo
00873100  mov  rdx, r15
00873103  mov  rcx, rdi
00873106  call 0x87db30
0087310B  mov  rdx, r15
0087310E  mov  rcx, rdi
00873111  call 0x87e220      ; estágio posterior
```

Idem em `0x873440`: `0x8769E0 call 0x87b2a0` → `0x8769F6 call 0x87bb60` → `0x876A0C call 0x87e220`.

### 2.2 Mapa completo dos 35 `call` (alvo + RVA do sítio)

| # | sítio | alvo | resolução do alvo |
|---:|---|---|---|
| 1 | `0x0087BC17` | `0x1C9A9FB` | `logf` (`thunk_map.txt:308`, `jmp [0x1D8D808]`) |
| 2 | `0x0087BC49` | `0x1C9A9D7` | `expf` (`thunk_map.txt:302`, `jmp [0x1D8D7F0]`) |
| 3 | `0x0087BC6D` | `0x1C9A9FB` | `logf` |
| 4 | `0x0087BC7D` | `0x1C9A9FB` | `logf` |
| 5 | `0x0087BC9B` | `0x1C9A9D7` | `expf` |
| 6 | `0x0087BF57` | `0x87A7A0` | preenche descritor com `1.0` |
| 7 | `0x0087BFC9` | `0x87A7A0` | idem |
| 8 | `0x0087C231` | `0x882FC0` | duas curvas `A^(1−σ)` (spec §8.2(f)) |
| 9 | `0x0087C4DA` | `0x882FC0` | idem |
| 10 | `0x0087C5E0` | `0x1340` | `→ 0x21C6188[4] = 0x199B9BA0 = RVA 0x9BA0` = multiplicação in-place `dst[i]*=src[i]` |
| 11 | `0x0087C619` | `0x1340` | idem |
| 12 | `0x0087C6FD` | `0x1340` | idem |
| 13 | `0x0087C739` | `0x1340` | idem |
| 14 | `0x0087CA0E` | `0x879CF0` | processamento log-ratio de descritores |
| 15 | `0x0087CA7A` | `0x1220` | `→ 0x21C6008[4] = 0x199B6160 = RVA 0x6160` = preenche com escalar |
| 16 | `0x0087CA9B` | `0x1C9A9FB` | `logf` |
| 17 | `0x0087CBF9` | `0x879CF0` | idem 14 |
| 18 | `0x0087CC10` | `0x1C9A9FB` | `logf` |
| 19 | `0x0087CC2C` | `0x1C9A9D7` | `expf` |
| 20 | `0x0087CDFE` | `0x8833F0` | preenche descritor com escalar (`xmm1`) |
| 21 | `0x0087CEA1` | `0x8834C0` | mistura/limita descritor com escalar |
| 22 | `0x0087D07B` | `0x8833F0` | idem 20 |
| 23 | `0x0087D11E` | `0x8834C0` | idem 21 |
| 24 | `0x0087D2C1` | `0x8833F0` | idem 20 |
| 25 | `0x0087D3C3` | `0x1340` | multiplicação in-place |
| 26 | `0x0087D3F9` | `0x1340` | idem |
| 27 | `0x0087D4F0` | `0x1340` | idem |
| 28 | `0x0087D529` | `0x1340` | idem |
| 29 | `0x0087D5F7` | `0x8834C0` | idem 21 |
| 30 | `0x0087D7A3` | `0x8833F0` | idem 20 |
| 31 | `0x0087D890` | `0x1340` | multiplicação in-place |
| 32 | `0x0087D8C9` | `0x1340` | idem |
| 33 | `0x0087D9C0` | `0x1340` | idem |
| 34 | `0x0087D9F9` | `0x1340` | idem |
| 35 | `0x0087DAC7` | `0x8834C0` | idem 21 |

Prova de que `0x1340` é multiplicação in-place (não é "mult" do contexto §17; aqui é o kernel `0x9BA0`):

```
00009BA0  endbr64
00009BA4  push   rdi
00009BA5  mov    rdi, rdx            ; rdi = dst
00009BA8  test   rcx, rcx            ; src
00009BB1  test   rdi, rdi            ; dst
...
00009C20  vmovss xmm0, [rcx + rdx*4] ; xmm0 = src[i]
00009C25  vmulss xmm1, xmm0, [rdi + rdx*4]
00009C2A  vmovss [rdi + rdx*4], xmm1  ; dst[i] *= src[i]
```

Stub de despacho (prova de resolução):

```
00001340  movsxd rax, [0x21C7408]    ; i32 = 4
00001347  lea    r10, [0x21C6188]
0000134E  jmp    [r10 + rax*8]       ; [4] = 0x199B9BA0 -> RVA 0x9BA0
```

### 2.3 Transcrição da aritmética (ordem real das instruções)

#### Bloco A — três escalares de parâmetro (`0x87BB60`–`0x87BCD9`)

```
; ---- escalar 1: razão param/taxa ----
0087BB88  rdx = [rcx+0x60]            ; inteiro (taxa/base)
0087BBD3  test rdx,rdx / js
0087BBD8  cvtsi2ss xmm0, rdx          ; (com correção de sinal em 0x87BBDF-0x87BBF0)
0087BBF4  xmm1 = [rcx+0x20]           ; f32
0087BC00  divss xmm1, xmm0            ; xmm1 = [ctx+0x20] / (f32)[ctx+0x60]
0087BC0F  [rbp+0x6a0] = xmm1          ; guardado; usado em 0x87DA6B
; ---- escalar 2: curva em log entre 9*[...] ----
0087BC07  xmm0 = 2008.0               ; [0x207A5B0]
0087BC17  call logf
0087BC1C  subss xmm0, 2.19722462      ; [0x207A1C0] = ln(9)
0087BC24  xmm15 = 1.0                 ; [0x2079F9C]
0087BC2D  xmm7  = 0
0087BC04  ebx = [[ctx+0x2c38]+8]
0087BC30  xmm1 = (f32)ebx
0087BC34  maxss xmm1, xmm7            ; clamp inferior 0
0087BC38  minss xmm1, xmm15           ; clamp superior 1
0087BC3D  mulss xmm0, xmm1
0087BC41  addss xmm0, 2.19722462      ; ln(9) + w*(ln2008 - ln9)
0087BC49  call expf                   ; = 9*(2008/9)^w
0087BC4E  subss xmm0, 8.0             ; [0x207A350]
0087BC60  [rbp-0x40] = xmm0           ; usado em 0x87D276 -> xmm1 de 0x8833F0@0x87D2C1
; ---- escalar 3: curva em log entre 33*[...] ----
0087BC56  ebx = [[ctx+0x2c38]+0xc]
0087BC65  xmm0 = 33.0                 ; [0x207A418]
0087BC6D  call logf                   ; xmm6 = ln(33)
0087BC72  xmm6 = xmm0
0087BC75  xmm0 = 2003.0               ; [0x207A5AC]
0087BC7D  call logf
0087BC82  subss xmm0, xmm6            ; ln(2003) - ln(33)
0087BC86  xmm1 = (f32)ebx
0087BC8A  maxss xmm1, xmm7
0087BC8E  minss xmm1, xmm15
0087BC93  mulss xmm0, xmm1
0087BC97  addss xmm0, xmm6            ; ln(33) + w*(ln2003 - ln33)
0087BC9B  call expf                   ; = 33*(2003/33)^w
0087BCAE  subss xmm0, 3.0             ; [0x207A248]
0087BCD1  [rbp+0x210] = xmm0          ; usado em 0x87D755 -> xmm1 de 0x8833F0@0x87D7A3
```

Leitura literal: os dois escalares são `9·(2008/9)^w − 8` e `33·(2003/33)^w − 3`, com `w = clamp(campo, 0, 1)` lido de `[[ctx+0x2c38]+8]` e `[[ctx+0x2c38]+0xc]`. **Não** são "frequências 2008/2003 Hz": `2008` e `2003` entram como argumento de `logf` e o resultado passa por `expf`; a forma provada é a interpolação geométrica acima.

#### Bloco B — inicialização de dois buffers de coeficientes (`0x87BCE0`–`0x87BFCE`)

```
0087BDCB  r9d  = [ctx+0x7c8]          ; nº de ponteiros a copiar
0087BDD2  r8   = ctx+0x748            ; array de ponteiros (8 slots: +0x00..+0x70)
0087BDD9  r10d = [r8+0x88]            ; stride
0087BDF0  test r9d / jle
0087BE10  copia qwords [ctx+0x748+i*8] -> [rbp+0x230+i*8]   ; laço até edx<r9d
0087BF57  call 0x87A7A0               ; preenche conjunto A com 1.0
0087BFC9  call 0x87A7A0               ; preenche conjunto B com 1.0
```

`0x87A7A0` copia 8 ponteiros (`[rcx]`…`[rcx+0x70]`), lê a contagem em `[rcx+0x80]` (`0x87A7F3`), o stride `[rcx+0x88]` (`0x87A812`) e para cada ponteiro chama `0x1040` com `xmm0 = 1.0` (`0x87A81F`, `0x87A839`):

```
0087A7F3  movd eax, xmm([rcx+0x80])
0087A812  esi = [rcx+0x88]
0087A81F  xmm6 = 1.0
0087A830  rdx = [rbx]        ; ponteiro i
0087A836  xmm0 = xmm6
0087A839  call 0x1040         ; 0x1040 -> 0x21C5D88[4] -> RVA 0x2300 = memset_32f
```

`0x1040` → `0x2300` (`vvmovss` + `call 0x1d2e460` = `memset`) — preenche o buffer com o escalar.

#### Bloco C — as duas chamadas a `0x882FC0` (curvas por banda)

Sítio 1 — `0x87C231`:

```
0087C0B8  rax = [ctx+0x2c38]
0087C0CB  r9d  = [rax+0x1c]
0087C0CF  rax = [ctx+0x2c38]
0087C0D6  r10d = [rax+0x18]
0087C0DA  rax  = (i64)[ctx+0x748+0x88]   ; stride
0087C0E1  ecx  = [ctx+0x748+0x80]        ; contagem do descritor
0087C219  xmm3 = (f32)r9d                ; A2 = [[ctx+0x2c38]+0x1c]
0087C21E  xmm2 = (f32)r10d               ; A1 = [[ctx+0x2c38]+0x18]
0087C231  call 0x882FC0                  ; (rcx=descritor A = rbp+0xf0  -> 0x87C165,
                                         ;  rdx=descritor B = rbp+0x60  -> 0x87C157,
                                         ;  xmm2=A1, xmm3=A2, [rsp+0x20]=rdi=arena)
```

Sítio 2 — `0x87C4DA`:

```
0087C33B  rax = [ctx+0x2c38]
0087C34E  r9d  = [rax+0x24]
0087C352  rax = [ctx+0x2c38]
0087C359  r10d = [rax+0x20]
0087C364  ecx  = [ctx+0x748+0x80]        ; contagem do descritor
0087C482  xmm3 = (f32)r9d                ; A2 = [[ctx+0x2c38]+0x24]
0087C487  xmm2 = (f32)r10d               ; A1 = [[ctx+0x2c38]+0x20]
0087C4DA  call 0x882FC0
```

(`[rsp+0x20] = rdi` em `0x87C15B` / `0x87C3DE`: 5º argumento = arena.)

#### Bloco D — produto das duas curvas (`0x87C5B4`–`0x87C748`)

```
0087C5A3  cmp eax, ecx        ; eax = contagem da curva 1, ecx = contagem da curva 2
0087C5B4  jne 0x87C5F1
0087C5D0  rdx = [rsp+rbx+0x30]      ; ponteiro do buffer
0087C5D8  rcx = [rbp+rbx+0xf0]      ; ponteiro do buffer 2
0087C5E0  call 0x1340               ; dst[i] *= src[i]
... (ramo "1 ponteiro": 0x87C5F1/0x87C610/0x87C619)
0087C6D3  cmp eax, ecx
0087C6F0  ... 0087C6FD call 0x1340
0087C730  ... 0087C739 call 0x1340  ; segundo par de buffers
```

Ou seja: as duas curvas geradas em C são multiplicadas ponto a ponto (4 chamadas a `0x1340`, todas as combinações "N ponteiros"/"1 ponteiro" × 2 pares).

#### Bloco E — curva de ganho via `0x879CF0` e constante temporal (`0x87C748`–`0x87CC3F`)

```
0087C758  eax = [[ctx+0x2c38]+0xb0]
0087C75E  cmp eax, 1
0087C76F  r10b = (eax==1)                 ; FLAG DE MODO (não é flag por banda)
0087C8CA  test r10b,r10b
0087C8CD  je   0x87CACC                   ; modo 0
; ---- modo 1 (r10b==1) ----
0087C8D3..0087C9F8  monta descritores
0087CA0E  call 0x879CF0                   ; descritor -> curva
0087CA13  xmm15 = 2.0                     ; [0x207A188]
0087CA70  rdx = [r14] ; 0087CA76 xmm0 = 2.0
0087CA7A  call 0x1220                     ; preenche com 2.0
0087CA89  rax = [ctx+0x2c38]
0087CA90  xmm0 = 50.0                     ; [0x207A450]
0087CA98  ebx = [rax+4]
0087CA9B  call logf                       ; ln(50)
0087CAA0  subss xmm0, 2.30258512          ; [0x207A1D0] = ln(10)
0087CAA8  xmm1 = (f32)ebx
0087CAAC  xmm3 = 0
0087CAAF  maxss xmm1, xmm3
0087CAB3  minss xmm1, 1.0                 ; [0x2079F9C]
0087CABB  mulss xmm0, xmm1
0087CABF  addss xmm0, 2.30258512          ; ln10 + w*(ln50-ln10) = ln(10*5^w)
0087CAC7  jmp 0x87CC2C                    ; expf
; ---- modo 0 (r10b==0) ----
0087CACC..0087CBF2  monta descritores (xmm2=1000.0 [0x207A590], xmm3=2.0)
0087CBF9  call 0x879CF0
0087CC05  xmm0 = 250.0                    ; [0x207A514]
0087CC0D  ebx = [[ctx+0x2c38]+4]
0087CC10  call logf                       ; ln(250)
0087CC15  xmm1 = (f32)ebx
0087CC19  xmm3 = 0
0087CC1C  maxss xmm1, xmm3
0087CC20  minss xmm1, 1.0
0087CC28  mulss xmm0, xmm1
0087CC2C  call expf                       ; modo0: 250^w ; modo1: 10*5^w
0087CC52  [rbp+0x6a8] = xmm0
```

Resultado provado: a constante final é `10·5^w` quando `[[ctx+0x2c38]+0xb0]==1`, e `250^w` caso contrário, com `w = clamp([[ctx+0x2c38]+4], 0, 1)`.

#### Bloco F — quatro pares `0x8833F0` + `0x8834C0` (`0x87CDFE`–`0x87DAC7`)

```
0087CDFE  call 0x8833F0   ; preenche com xmm1 = escalar (vem do bloco anterior)
0087CEA1  call 0x8834C0   ; mistura/limita
0087D07B  call 0x8833F0
0087D11E  call 0x8834C0
0087D276  xmm1 = [rbp-0x40]          ; escalar 9*(2008/9)^w - 8
0087D2C1  call 0x8833F0
0087D3C3  call 0x1340      ; multiplicação in-place
0087D3F9  call 0x1340
0087D4F0  call 0x1340
0087D529  call 0x1340
0087D5F7  call 0x8834C0
0087D755  xmm1 = [rbp+0x210]         ; escalar 33*(2003/33)^w - 3
0087D7A3  call 0x8833F0
0087D890  call 0x1340
0087D8C9  call 0x1340
0087D9C0  call 0x1340
0087D9F9  call 0x1340
0087DA6B  xmm1 = [rbp+0x6a0]         ; razão [ctx+0x20]/[ctx+0x60]
0087DAC7  call 0x8834C0
```

### 2.4 Constantes (RVA, bytes, valor)

| RVA | bytes (LE) | valor | usada em |
|---|---|---|---|
| `0x207A5B0` | `00 00 FB 44` | f32 `2008.0` | `0x87BC07` |
| `0x207A1C0` | `54 9F 0C 40` | f32 `2.19722462` = ln(9) | `0x87BC1C`, `0x87BC41` |
| `0x207A1C4` | `00 00 80 40` | f32 `4.0` (lixo de leitura de 8 B) | — |
| `0x2079F9C` | `00 00 80 3F` | f32 `1.0` | `0x87BC24`, `0x87CAB3`, `0x87CC20` |
| `0x207A350` | `00 00 00 41` | f32 `8.0` | `0x87BC4E` |
| `0x207A418` | `00 00 04 42` | f32 `33.0` | `0x87BC65` |
| `0x207A5AC` | `00 60 FA 44` | f32 `2003.0` | `0x87BC75` |
| `0x207A248` | `00 00 40 40` | f32 `3.0` | `0x87BCAE` |
| `0x207A1D0` | `8E 5D 13 40` | f32 `2.30258512` = ln(10) | `0x87CAA0`, `0x87CABF` |
| `0x207A188` | `00 00 00 40` | f32 `2.0` | `0x87CA13`, `0x87CB07` |
| `0x207A590` | `00 00 7A 44` | f32 `1000.0` | `0x87CB10` |
| `0x207A450` | `00 00 48 42` | f32 `50.0` | `0x87CA90` |
| `0x207A514` | `00 00 7A 43` | f32 `250.0` | `0x87CC05` |

### 2.5 Layout de struct provado

Descritor **pequeno** (usado por `0x87A7A0`, `0x882FC0`, `0x8833F0`, `0x8834C0`, `0x87BB60`):

| offset | tipo | significado |
|---|---|---|
| `+0x00 … +0x70` | `void*[8]` | até 8 ponteiros de buffer (canais) |
| `+0x80` | `int32` | **contagem de ponteiros** (1..8) |
| `+0x88` | `int32` | stride em elementos |

Prova do `+0x80` como contagem (não flag booleano):
- `0x87A7F3` `movd eax, xmm([rcx+0x80])` seguido de `test eax,eax; jle` (`0x87A801`) e laço `sub rdi,1; jne` (`0x87A842`) — o valor é usado como **limite de laço** sobre a lista de ponteiros.
- `0x8834C0`: `0x88351E` carrega `[rcx+0x80]`, `0x8835AC test eax,eax; jle`, `0x8835C6 mov esi,eax` — idem.
- `0x882FC0`: `0x8832C1` e `0x883371` fazem `cmp eax,1` / `jne` para escolher "1 ponteiro" vs "N ponteiros", e no ramo N usam `[rbp+0x54]`/`[rbp+0x140]` como stride.

### 2.6 Resposta: que filtro é por banda, onde estão os coeficientes, e a flag@0x80

**Provado nesta função:**
- `0x87BB60` **não contém** laço por amostra, nem leitura de amostra anterior, nem escrita de estado de recursão. Todas as leituras de `ctx` são escalares/descritores; todas as escritas vão para buffers via kernels (`0x1340`, `0x1220`, `0x10A0`, `0x1040`).
- A operação por banda é: (i) montar duas curvas `A^(1−σ)` por dois pares de escalares (`0x882FC0` em `0x87C231` e `0x87C4DA`); (ii) **multiplicar** as duas curvas ponto a ponto (`0x1340`, sítios `0x87C5E0`/`0x87C619`/`0x87C6FD`/`0x87C739`); (iii) modular por `0x879CF0` e por `0x8834C0` com escalares geométricos (`10·5^w` / `250^w`, `9·(2008/9)^w−8`, `33·(2003/33)^w−3`, `[ctx+0x20]/[ctx+0x60]`).
- **Conclusão de tipo:** não é biquad nem state-space (não há coeficientes `a1/a2` nem histórico por amostra). É **filtragem por multiplicação de curva de ganho no domínio espectral** (resposta de magnitude aplicada por banda; fase zero). No código, os "coeficientes" são as **curvas/arrays nos buffers do descritor pequeno** (`ctx+0x748` e os descritores de scratch em `rbp+0xf0`/`rbp+0x60`), preenchidos por `0x87A7A0` (1.0), `0x882FC0` (curvas A^(1−σ)), `0x8833F0` (escalar) e `0x8834C0` (mistura/limite).
- **NÃO PROVADO:** que esses buffers sejam consumidos por um FIR/biquad/state-space em outro estágio; dentro de `0x87BB60` isso não existe. Ponto onde a prova para: consumo dos buffers fora da função (`0x877D90`, `0x87DB30` chamados em `0x873106`/`0x873119`).

**Relação com `+0x80` nos dois sítios de `0x882FC0`:**
- Nos dois sítios (`0x87C0E1` e `0x87C364`) o valor `[ctx+0x748+0x80]` é lido e vira **contagem de ponteiros** do descritor; **não** é testado como flag antes da chamada (não há `cmp/jne` sobre ele em `0x87BB60`).
- Dentro de `0x882FC0`, o campo `+0x80` do descritor é comparado com `1` em **dois** pontos (`0x8832C1` e `0x883371`), escolhendo o caminho de 1 ponteiro vs N ponteiros.
- Portanto, "band->flag@0x80 == 1" **não** é uma flag por banda; é a contagem de ponteiros (canais).

---

## 3. `0x87E220` — clamp de ganho por banda (`powf(10,2.4)` / `powf(10,-4.8)`)

### 3.1 Chamadores (18)

`0x873111` (`0x86FE90`), `0x876A0C` (`0x873440`), `0x8853B5` (`0x885040`), `0x887965` (`0x8875F0`),
`0x889F63` (`0x889C18`), `0x88B1D3` (`0x88AE88`), `0x88ECAC` (`0x88E8A0`), `0x89191C` (`0x891510`),
`0x89459A` (`0x894170`), `0x89611A` (`0x895CF0`), `0x89AF95` (`0x89AC20`), `0x89D545` (`0x89D1D0`),
`0x89FB43` (`0x89F7F8`), `0x8A0DB3` (`0x8A0A68`), `0x8A2B9C` (`0x8A2790`),
`0x8A580C` (`0x8A5400`), `0x8A848A` (`0x8A8060`), `0x8AA00A` (`0x8A9BE0`).

Cadeia: chamado **imediatamente depois** de `0x87BB60` em `0x873111` e `0x876A0C` (ver §2.1).

### 3.2 Mapa de `call`

| sítio | alvo | resolução |
|---|---|---|
| `0x0087E39F` | `0x87A7A0` | preenche descritor com 1.0 |
| `0x0087E7AC` | `0x883940` | curva/ganho por banda (3324 B; chama `0x882DE0`, `0x88E130`, `0x1340`, `0x1370`, `0x1220`, `0x1100`) |
| `0x0087E956` | `0x10D0` | zera buffer (`0x2F60`) |
| `0x0087EA56`, `0x0087EA67` | `0x61B790` | — |
| `0x0087EAA2` | `0x1798F42` | `memset` (VCRUNTIME140, `thunk_map.txt:162`) |
| `0x0087ED98` | `0x883940` | idem |
| `0x0087EE3F` | `0x1040` | preenche com escalar (1.0) |
| `0x0087EF30`, `0x0087EF69` | `0x1340` | multiplicação in-place |
| `0x0087EF8B` | `0x1C9AA01` | **`powf`** |
| `0x0087EFE0` | `0x1100` | clamp, `r9d=4` |
| `0x0087EFFA` | `0x1C9AA01` | **`powf`** |
| `0x0087F04B` | `0x1100` | clamp, `r9d=0` |

### 3.3 Transcrição do trecho dos `powf` (`0x87EF78`–`0x87F058`)

```
0087EF78  xmm7 = 10.0                 ; [0x207A360]
0087EF80  xmm1 = 2.4000001            ; [0x207A1E8]
0087EF88  xmm0 = xmm7
0087EF8B  call powf                   ; powf(10, 2.4) = 251.1886...
0087EF96  xmm6 = xmm0
0087EFC6  test edi,edi / jle
0087EFD2  rcx = [rsi]                 ; ponteiro de buffer
0087EFD5  r9d = 4
0087EFDB  xmm2 = xmm6
0087EFDE  edx = ebx                   ; len
0087EFE0  call 0x1100                 ; modo 4 = MIN -> limite superior
...
0087EFF7  xmm1 = -4.80000019          ; [0x207A6F0]
0087EFFA  call powf                   ; powf(10, -4.8) = 1.5848932e-05
0087F005  xmm6 = xmm0
0087F043  r9d = 0
0087F046  xmm2 = xmm6
0087F04B  call 0x1100                 ; modo 0 = MAX -> limite inferior
```

Prova de que `0x1100` modo 4 = `min` e modo 0 = `max`:

```
0000349E  cmp r9d,4 / je 0x34aa
00003500  vminss xmm0, xmm2, [rcx+rax*4]   ; modo 4
00003640  vmaxss xmm0, xmm2, [rcx+rax*4]   ; modo 0
```

**Efeito provado:** o buffer de ganho é grampeado em `[10^(-4.8), 10^2.4] ≈ [1.585e-05, 251.19]`.
Expoentes em RVAs distintos: `2.4000001` em `0x207A1E8` (sítio `0x87EF80`) e `-4.80000019` em `0x207A6F0` (sítio `0x87EFF7`); base `10.0` em `0x207A360` (`0x87EF78`).

### 3.4 Constantes

| RVA | bytes | valor | uso |
|---|---|---|---|
| `0x207A360` | `00 00 20 41` | f32 `10.0` | base dos dois `powf` (`0x87EF78`) |
| `0x207A1E8` | `9A 99 19 40` | f32 `2.4000001` | expoente (`0x87EF80`) |
| `0x207A6F0` | `9A 99 99 C0` | f32 `-4.80000019` | expoente (`0x87EFF7`) |
| `0x207A188` | `00 00 00 40` | f32 `2.0` | `0x87E3CC`/`0x87E426` (limiar 2 vs 1) |
| `0x207A0B8` | `00 00 00 00 00 00 E0 3F` | f64 `0.5` | `0x87E411`, `0x87E994` (escala quando modo ≠ 1) |
| `0x207A138` | `00 00 00 00 00 00 F0 3F` | f64 `1.0` | `0x87E3AC` |
| `0x207A190` | `00 00 00 00 00 00 00 40` | f64 `2.0` | `0x87E3CC` |

### 3.5 Laço de 8 registros

```
0087E3A4  rsi = [ctx+0x2c38]
0087E3B5  rsi += 0xb8
0087E3BC  r15 = rsi + 0x100
0087E3C6  cmp rsi,r15 / je 0x87e7e9    ; [0xb8,0x1b8) passo 0x20 => 8 registros
0087E3E0  movzx eax,[rsi]              ; flag 0 (precisa != 0)
0087E3EC  movzx eax,[rsi+1]            ; flag 1 (precisa != 0)
0087E3F9  eax = [rsi+0x1c]             ; tipo
0087E400  cmp eax,3 / je skip          ; este laço pula tipo==3
0087E419  eax = [rsi+8] (f32 via movd)
0087E421  comiss 0 ; se < 0 => 2.0, senão 1.0        (0x87E426/0x87E42B)
0087E43F  mulsd xmm0,xmm1              ; xmm1 = 1.0 se modo==1, senão 0.5
0087E482  cvtsd2ss xmm2,xmm0           ; limiar do registro
0087E7AC  call 0x883940
0087E7B9  rsi += 0x20
0087E7BD  cmp rsi,r15 / jne 0x87e3e0
```

Segundo laço `0x87E9B0`–`0x87EDB4`: mesmo intervalo de 8 registros, processa apenas `[rsi+0x1c]==3` (`0x87E9C9`/`0x87E9CD`) e finaliza com o clamp de §3.3.

### 3.6 Papel provado na cadeia

Recebe o buffer de ganho produzido por `0x87BB60` (mesma posição de pipeline em `0x86FE90`/`0x873440`), percorre os 8 registros de `[ctx+0x2c38]+0xB8…+0x1B8`, calcula um limiar por registro e grampeia o ganho final em `[10^-4.8, 10^2.4]`. É **limitador de faixa dinâmica do ganho**, não filtro temporal.

---

## 4. `0x87B2A0` — cutoff por banda (`pow(2,1/3)`)

### 4.1 Chamadores (18)

`0x8730E5` (`0x86FE90`), `0x8769E0` (`0x873440`), `0x8853CF` (`0x885040`), `0x88797F` (`0x8875F0`),
`0x889F82` (`0x889C18`), `0x88B1F2` (`0x88AE88`), `0x88ECC7` (`0x88E8A0`), `0x891937` (`0x891510`),
`0x8945B9` (`0x894170`), `0x896139` (`0x895CF0`), `0x89AFAF` (`0x89AC20`), `0x89D55F` (`0x89D1D0`),
`0x89FB62` (`0x89F7F8`), `0x8A0DD2` (`0x8A0A68`), `0x8A2BB7` (`0x8A2790`), `0x8A5827` (`0x8A5400`),
`0x8A84A9` (`0x8A8060`), `0x8AA029` (`0x8A9BE0`).

É o **primeiro** estágio (antes de `0x87BB60` nos dois chamadores principais).

### 4.2 Aritmética (`0x87B2A0`)

```
0087B2C2  edx = [ctx+0x4f8]           ; contagem
0087B2C8  r9  = ctx+0x478             ; descritor
0087B2E4  rcx = [r9+0x88]             ; stride
0087B36A  rax = [ctx+0x2c38]
0087B376  eax = [rax+0x10]
0087B379  rax = [ctx+0x2c38]
0087B380  eax = [rax+0xb0]
0087B386  cmp eax,1
0087B389  jne 0x87b396
0087B38B  xmm8 = 16000.0              ; [0x207A5CC]
0087B394  jmp 0x87b39f
0087B396  xmm8 = 6000.0               ; [0x207A5C0]
0087B39F  rax = [ctx+0x2c38]
0087B3A6  xmm0 = 1000.0               ; [0x207A590]
0087B3AE  ebx = [rax+4]
0087B3B1  call logf                   ; xmm7 = ln(1000)
0087B3B6  xmm1 = 2.0                  ; [0x207A188]
0087B3C1  xmm0 = (f32)ebx
0087B3C5  call powf                   ; ebx^2
0087B3D0  maxss xmm6, 0
0087B3D8  minss xmm6, 1.0
0087B3E0  call logf                   ; ln(16000) ou ln(6000)
0087B3E5  subss xmm0, xmm7            ; ln(fmax) - ln(1000)
0087B3E9  mulss xmm6, xmm0
0087B3ED  addss xmm6, xmm7            ; ln(1000) + w*(ln fmax - ln 1000)
0087B3F4  call expf                   ; f = 1000*(fmax/1000)^w
0087B4E7  call 0x882C30               ; pow(2,1/3) = razão de 1/3 de oitava
0087B4F0  cmp byte [r14+0x58], dil
0087B504  call 0x1220                 ; se [ctx+0x58]==0: preenche com -1.0
0087B517  call 0x12E0                 ; e depois com 1.0
0087B51C  cmp qword [r14+0x48], 1
0087B612  call 0x10A0                 ; cópia (ramo 1 ponteiro)
0087B639  call 0x10A0                 ; cópia (ramo N ponteiros)
```

**Papel provado:** mapeia `[[ctx+0x2c38]+4]` para `f = 1000·(16000/1000)^w` (modo `[[ctx+0x2c38]+0xb0]==1`) ou `f = 1000·(6000/1000)^w` (demais), com `w = clamp(param²,0,1)`. `0x882C30` entra em `0x87B4E7` com `xmm2 = f` (`0x87B41A`) como razão `pow(2,1/3)` (passo de 1/3 de oitava). Posiciona a banda de análise; **não** calcula ganho.

### 4.3 Constantes

| RVA | bytes | valor | uso |
|---|---|---|---|
| `0x207A590` | `00 00 7A 44` | f32 `1000.0` | `0x87B3A6` |
| `0x207A5CC` | `00 00 7A 46` | f32 `16000.0` | `0x87B38B` (modo 1) |
| `0x207A5C0` | `00 80 BB 45` | f32 `6000.0` | `0x87B396` (modo 0) |
| `0x207A188` | `00 00 00 40` | f32 `2.0` | `0x87B3B6` (expoente de `powf`) |
| `0x2079F9C` | `00 00 80 3F` | f32 `1.0` | `0x87B3D8` (clamp) |
| `0x207A6A8` | `00 00 80 BF` | f32 `-1.0` | `0x87B4F6` |

---

## 5. Respostas explícitas

### (a) Origem de A1/A2 em `0x882FC0`

Provado nos dois sítios de `0x87BB60`:

| sítio | A1 (`xmm2`) | A2 (`xmm3`) | instruções |
|---|---|---|---|
| `0x87C231` | `[[ctx+0x2c38]+0x18]` | `[[ctx+0x2c38]+0x1c]` | `0x87C0D6` (`r10d`), `0x87C0CB` (`r9d`), `0x87C21E`/`0x87C219` |
| `0x87C4DA` | `[[ctx+0x2c38]+0x20]` | `[[ctx+0x2c38]+0x24]` | `0x87C359` (`r10d`), `0x87C34E` (`r9d`), `0x87C487`/`0x87C482` |

Ou seja, **A1/A2 são quatro floats consecutivos do objeto apontado por `ctx+0x2c38`** (pares `+0x18/+0x1c` e `+0x20/+0x24`), passados por valor em `xmm2`/`xmm3`; o `xmm2` é consumido como `xmm0`/`xmm12` em `0x882FFD`/`0x883005` e segue para `log10f` (`0x883054`/`0x88315E`) e `0x88E130` (`0x8830E7`/`0x8831E7`). O 5º argumento (arena) é `rdi`, gravado em `[rsp+0x20]` (`0x87C15B`/`0x87C3DE`).

`ctx+0x2c38` é atribuído em `0x870941` (`0x86FE90`) e `0x873F06` (`0x873440`) a partir de `[rbp+0x440]` — um objeto de parâmetros externo. **Quem escreve `+0x18…+0x24` desse objeto não foi localizado** (ver NÃO PROVADO).

### (b) `band->flag@0x80 == 1` nos dois sítios?

**Não.** O campo `+0x80` **não é flag por banda**: é a **contagem de ponteiros** do descritor pequeno (1..8), como provado em §2.5 (usado como limite de laço em `0x87A842`, `0x8835C6`, ramo `cmp eax,1` em `0x8832C1`/`0x883371`).

- Em `0x87BB60`, `[ctx+0x748+0x80]` é lido em `0x87C0E1` (sítio 1) e `0x87C364` (sítio 2) e apenas **copia** a contagem para o descritor; **não há `cmp`/`jne` sobre esse valor antes das chamadas** `0x87C231`/`0x87C4DA`.
- Logo, não se pode afirmar estaticamente `== 1`: o valor é de runtime. O que existe são **dois** testes `cmp eax,1` **dentro** de `0x882FC0`, em `0x8832C1` e `0x883371`, que selecionam 1 ponteiro vs N ponteiros.
- Resposta: **NÃO PROVADO que seja `1`; provado que é contagem, não flag.** RVA onde a prova para: `0x87C0E1`/`0x87C364` (leitura) e `0x8832C1`/`0x883371` (comparação).

### (c) Número real de bandas de análise/filtro

- Tabela de registros: `[ctx+0x2c38]+0xB8` até `+0x1B8`, passo `0x20` → **8 registros** (prova: `0x87E3B5` `add rsi,0xb8`; `0x87E3BC` `lea r15,[rsi+0x100]`; `0x87E7BD` `cmp rsi,r15`; incremento `0x87E7B9` `add rsi,0x20`). Mesmo intervalo repetido em `0x87E976`/`0x87E984` (segundo laço).
- Descritor pequeno: **até 8 ponteiros** (`+0x00…+0x70`; contagem `+0x80`), provado pela cópia de 8 qwords em `0x87A7AA`–`0x87A7E7`.
- Resposta: **8 bandas** (limite estrutural do código). O número da UI não aparece nesta função; não foi usado.

---

## 6. NÃO PROVADO / onde a prova parou

1. **Escritores de `[ctx+0x2c38]+0x18…+0x24` (A1..A4):** não localizados. `ctx+0x2c38` só foi provado como atribuído em `0x870941` (`0x86FE90`) e `0x873F06` (`0x873440`) a partir de `[rbp+0x440]`; a varredura por `movss [reg+0x18..0x24]` com base carregada de `[..+0x2c38]` não retornou sítio (parou em `0x870941`).
2. **Consumidor final dos buffers de curva de `0x87BB60`:** `0x87DB30` (`0x873106`) e `0x877D90` (`0x873119`) não foram abertos nesta etapa. Se o filtro temporal (FIR/biquad/state-space) existir, está lá; **dentro de `0x87BB60` não há**.
3. **Significado semântico de `[[ctx+0x2c38]+0xb0]`:** provado apenas como seletor binário (`cmp eax,1` em `0x87B386`, `0x87C75E`, `0x87E2A4`); o nome do parâmetro não foi usado como prova.
4. **`0xAC20` (alvo de `0x1400` em `0x8CB24B`):** pertence ao agente K; registrado só como tabela `0x21C6288` → `0xAC20` (§1.1). Não foi dissecado aqui.
5. **Número "de UI" de bandas:** não extraído (proibido por regra); a resposta (c) é estrutural (8 registros/8 ponteiros), não o valor da interface.
6. **`0x883940`** (chamado em `0x87E7AC`/`0x87ED98`): papel descrito só pelo mapa de chamadas (`0x882DE0`, `0x88E130`, `0x1340`, `0x1370`, `0x1100`); não foi transcrito linha a linha nesta etapa.
7. **`0x87B2A0` → `0x882C30`:** o valor `pow(2,1/3)` em `0x87B4E7` foi atribuído pelo uso de `xmm2 = f` (`0x87B41A`); a constante `1/3` não foi lida byte a byte dentro de `0x882C30` nesta etapa. Prova para em `0x87B4E7`/`0x87B41A`.

