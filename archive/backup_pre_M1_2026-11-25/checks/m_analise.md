# Etapa M — análise (`0x8B8E70`, `0x8BA1B0`, `0x8BA7B0`, `0x8B35A0`)

Fonte de verdade: `dumpsooth\nyx_soothe3_dump.bin`
(SHA-256 `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`).
Endereços = RVAs (base de imagem `0x180000000`). Ponteiros de dado no dump: VA base
`0x199B0000`, `RVA = VA − 0x199B0000`.

Regra aplicada: toda afirmação leva instrução + RVA. Desmontagem chain-aware por
`tools/show_func.py` (nunca `functions.csv`). Nada foi executado, hookado ou escrito no
binário/processo. Não se usa `params.csv` como prova. Onde a leitura parou, está marcado
`NÃO PROVADO` com o RVA.

Arquivos de apoio gravados nesta etapa (desmontagem, não são fonte):
`checks/m_8b8e70.dis`, `m_8ba1b0.dis`, `m_8ba7b0.dis`, `m_8b35a0.dis`,
`m_8a1ee0.dis`, `m_8ad2b0.dis`, `m_86f480.dis`, `m_867cc0.dis`, `m_867c20.dis`,
`m_1c8880.dis`.

---

## 0. Correção de atribuição de chamador (bate byte a byte)

O plano dizia "`0x8B8E70` … chamado pelo núcleo em `008B4A1C`". A leitura do dump
mostra que **`008B4A1C` chama `0x8BA1B0`**, não `0x8B8E70`:

```
008B4A1C  call 0x8BA1B0          ; E8 disp32 -> 0x8BA1B0 (conferido)
008B4AB8  call 0x8BA7B0          ; E8 disp32 -> 0x8BA7B0
```

Varredura de todos os `call rel32` (`E8`) do dump para os quatro alvos:

| alvo | sítios `call` (RVA) |
|---|---|
| `0x8B8E70` | `008AD9FA`, `008AF7FA`, `008BCF4A`, `008BE95A` |
| `0x8BA1B0` | `008ADF9B`, `008AFD9B`, `008B4A1C`, `008BD4EB`, `008BEEFB`, `008C678C` |
| `0x8BA7B0` | `008AE096`, `008AFE96`, `008B4AB8`, `008BD5E6`, `008BEFF6`, `008C6828` |
| `0x8B35A0` | `00890323`, `00892F73`, `008A1FE1`, `008A4213`, `008A6E63`, `008BA8B1` |

`008B4A1C` está no núcleo `0x8B3ED0`; `008C678C`/`008C6828` estão no gêmeo `0x8C5C40`
(mesmo deslocamento). `008AD9FA`/`008ADF9B`/`008AE096` estão dentro de `0x8AD2B0`
(processador de canal). Portanto: **`0x8B8E70` é chamado por `0x8AD2B0` (e por 3 cópias
irmãs), não pelo núcleo**; o núcleo chama o par `0x8BA1B0`/`0x8BA7B0`.

---

## 1. `0x8B8E70` — 4.036 B (`0x8B8E70..0x8B9E34`), 20 `call`, 1 `divss`

### 1.1 Chamadores e argumentos (no sítio `008AD9FA`, dentro de `0x8AD2B0`)

```
008AD986  lea  r9, [rbp + 0xd0]        ; arg4
008AD98D  mov  [rsp+0x20], r14         ; arg5 (stack; arena)
008AD996  lea  r8, [rbx + 0x68]        ; arg3
008AD99D  lea  rdx, [rbp + 0x1de0]     ; arg2
008AD9A9  lea  rcx, [rbp]              ; arg1
008AD9FA  call 0x8B8E70
```

Ou seja `0x8B8E70(arg1=rbp, arg2=&rbp+0x1DE0, arg3=rbx+0x68, arg4=&rbp+0xD0, arg5=r14)`.
O descritor `arg2` é montado em `0x8AD8BB..0x8AD9F3` copiando 8×`0x80` B de
`rbp+0x11B0` para `rbp+0x1DE0` mais o trailer de 16 B em `rbp+0x21E0`
(`008AD930..008AD981`, `008AD983..008AD99A`).

### 1.2 Mapa dos 20 `call`

| RVA | alvo | efeito provado / cadeia |
|---|---|---|
| `008B8E98` | `0x17978C0` | probe de pilha (`mov eax,0x15C8` em `008B8E93`; `sub rsp,rax` em `008B8E9D`) |
| `008B8F52` | `0x1798F42` | memset (`rcx=rbp+0x68`, `r8d=0x3F8` em `008B8F40/8B8F44`) |
| `008B90D7` | `0x1C84A0` | **expf vetorial**: `0x1C84A0`→tab `0x21C6A28[4]`=`0x1C8880`→`[0x21C6F08]`=`0x199B0C00` = RVA **`0x240C00`**; impl: `00240C44 mov r14,rcx` (src), `00240C38 mov r12,rdx` (dst), `00240C15 mov ebp,r8d` (n), `00240F2E vmovups [r12+r8*4],ymm0` |
| `008B927F` | `0x1798F42` | memset |
| `008B93FC` | `0x1280` | **FFT inversa**: `0x1280`→tab `0x21C6088[4]` = RVA **`0x7B40`** (spec §19/§24, já provado) |
| `008B94A9` | `0x1220` | `dst[i] *= escalar` in place: `0x1220`→RVA `0x6160` (spec §17.6) |
| `008B965F` | `0x1798F42` | memset |
| `008B9696` | `0x1798F36` | memcpy (`r8=r12*8` em `008B968B`) |
| `008B96C1` | `0x1798F42` | memset |
| `008B9888` | `0x1190` | `dst[i]=a[i]*b[i]`: `0x1190`→RVA `0x4BC0` (spec §17.6) |
| `008B98C6` | `0x1190` | idem |
| `008B9947` | `0x1798F36` | memcpy |
| `008B9975` | `0x1798F42` | memset |
| `008B99EB` | `0x1798F42` | memset |
| `008B9A25` | `0x1798F36` | memcpy |
| `008B9B98` | `0x1190` | `dst=a*b` |
| `008B9BD6` | `0x1190` | `dst=a*b` |
| `008B9C05` | `0x1798F42` | memset |
| `008B9CF6` | `0x10D0` | zero-fill: `0x10D0`→RVA `0x2F60` (spec §17.6) |
| `008B9DFB` | `0x1010` | **FFT direta**: `0x1010`→tab `0x21C5D48[4]` = RVA **`0x20E0`** (spec §19) |

### 1.3 O `divss` e suas constantes

```
008B940B  movd     xmm0, dword ptr [r13 + 0x18]   ; N = arg3->+0x18
008B9418  movss    xmm6, dword ptr [0x2079F9C]    ; 1.0f
008B9424  cvtdq2ps xmm0, xmm0                     ; (float)N
008B942A  divss    xmm6, xmm0                      ; xmm6 = 1.0f / (float)N
...
008B94A0  mov      rdx, qword ptr [rbx]            ; buffer i (saída da IFFT)
008B94A6  movaps   xmm0, xmm6
008B94A9  call     0x1220                          ; buffer[i] *= 1/N
```

É a **única** `divss` do corpo e o único uso de `0x2079F9C`; `0x2079F9C` = bytes
`00 00 80 3F` = `1.0f`. Portanto o fator é **1/N**, com `N = [arg3+0x18]`
(`008B8EA0 mov eax,[r8+0x18]` também prova a leitura de `N`).

Não há segunda constante float em `0x8B8E70`; a outra referência RIP é
`008B9549 cmp dword [0x21C7690],2` (`05 00 00 00` = i32 5), que é checagem de nível de
CPU (igual em `0x8BA1B0`, `008BA4C6`), não coeficiente de áudio.

### 1.4 Ordem real das operações (RVA por linha)

```
; ---- fase 1: copia descritor arg2 (D128) e aloca ----
008B8ED1  mov  edx, 8          ; 8 blocos de 0x80 B = 0x400 B (capacidade p/ 128 ponteiros)
008B8EE0..008B8F39  copia 8x0x80 B  arg2 -> rbp+0xC90
008B8F3B  movups xmm0,[rax]    ; rax = arg2+0x400
008B8F4E  movups [r10],xmm0    ; trailer 16 B -> rbp+0x1090
008B8F52  memset(rbp+0x68, 0, 0x3F8)
008B8F57  movsxd r14,[rbp+0x1094]   ; len   = [arg2+0x404]
008B8F61  movsxd r12,[rbp+0x1090]   ; count = [arg2+0x400]
008B8F90..008B8FC7  aloca r12 buffers de r14 floats (arena arg5, cursor em arg5+0x18)
; ---- fase 2: expf sobre cada buffer de arg2 ----
008B8FD7  mov edx, 8           ; copia arg2 -> rbp+0x10A0 (0x410 B)
008B90BE..008B90E4
    rcx = [rbp+rbx+0x10A0] = arg2->ptr[i]
    rdx = [rbp+rbx+0x880]  = alloc[i]
    r8d = r14
    call 0x1C84A0              ; expf(arg2->ptr[i], alloc[i], len)
; ---- fase 3: real->complex (imag=0) em arg1 ----
008B9192  movups xmm1,[rsi+0x80]   ; rsi=arg1; count=+0x80, len=+0x84
008B91D0..008B9258
    dst = arg1->ptr[i]; src = alloc[i]
    dst[2k] = src[k]; dst[2k+1] = 0.0f     ; 008B923C/8B923F/8B9243
; ---- fase 4: IFFT ----
008B926B  movsxd r15,[r13+0x18]    ; N
008B9307..008B93C1  copia arg1->ptr para stack / aloca buffers de N
008B93E0..008B9409
    rcx = arg1->ptr[i]; rdx = allocN[i]
    r8 = [[arg3]+8]; r9 = [[arg3+8]]
    call 0x1280                     ; FFT inversa
; ---- fase 5: normaliza 1/N ----
008B942A  divss xmm6,xmm0           ; 1.0f/N
008B94A0..008B94B6
    call 0x1220                     ; allocN[i] *= 1/N
; ---- fase 6: arg4 (segunda metade / janela) ----
008B94CF  mov r10d,[rbx+0x84]       ; L = arg4->+0x84
008B94D9  mov r14d,[rbx+0x80]       ; M = arg4->+0x80
008B94E1/8B94E6  L/2
008B9620  mov rax,[rbx+rdx*8]      ; arg4->ptr[i]
008B9624  lea rcx,[rax+rsi*4]      ; + (L/2) floats
008B9888/008B98C6  call 0x1190     ; produto vetorial nas metades
...
008B9CF6  call 0x10D0               ; zero-fill
008B9DFB  call 0x1010               ; FFT direta (fase final)
```

### 1.5 Layout de buffers provado em `0x8B8E70`

| arg | tipo provado | offsets | instrução |
|---|---|---|---|
| `arg2` (rdx) | descritor **D128** | `ptr[0..127]` qword @0; `int count` @`+0x400`; `int len` @`+0x404` | `008B8F3B/8B8F4E` copia `arg2+0x400`; `008B8F57/8B8F61` lê count/len |
| `arg1` (rcx) | descritor **D16** | `ptr[0..15]` qword @0; `int count` @`+0x80`; `int len` @`+0x84` | `008B9192 movups xmm1,[rsi+0x80]`; `008B9199 movd ecx,xmm1`; `008B91BD movd eax,xmm1` |
| `arg3` (r8) | contexto de FFT | `int N` @`+0x18`; qword `a` @0, `b` @8 (→ `[a+8]`, `[b]` são args da FFT) | `008B8EA0` / `008B926B`; `008B93E0..008B93F8` |
| `arg4` (r9) | descritor **D16** (mesma forma) | `int count` @`+0x80`; `int len` @`+0x84`; `ptr[i]` @`+8i` | `008B94CF/8B94D9`; `008B9620 mov rax,[rbx+rdx*8]` |
| `arg5` (stack) | arena bump | `void* base` @0; `int cursor (floats)` @`+0x18` | `008B8EAB mov r15,[rbp+0x1530]`; `008B8F90 mov rax,[r15]`; `008B8FC0 mov [r15+0x18],edx` |

Alinhamento do cursor da arena: `008B8FAC and eax,0xF` / `008B8FB2 add rdx,0x10` /
`008B8FB9 cmove rdx,rcx` (arredonda para múltiplo de 16 floats).

---

## 2. `0x8BA1B0` — 1.533 B (`0x8BA1B0..0x8BA7AD`), 8 `call`, 0 float próprio

### 2.1 Chamador `008B4A1C` (núcleo `0x8B3ED0`)

```
008B4A06  lea  r8, [rbp + 0x830]    ; arg3
008B4A0D  lea  rdx, [rsp + 0x50]    ; arg2
008B4A15  lea  rcx, [rbp + 0x1050]  ; arg1
008B4A1C  call 0x8BA1B0
```

(`0x8AD2B0` chama em `008ADF9B` com `rcx=&rbp+0xDA0`, `rdx=&rbp+0x580`, `r8=&rbp`.)

### 2.2 Mapa dos 8 `call`

| RVA | alvo | efeito provado |
|---|---|---|
| `008BA1EE` | `0x86F480` | sem aritmética float (varredura `0x86F480..0x86F600`: `fma=0 mul=0 add=0 sub=0 div=0`); identidade **NÃO PROVADA** |
| `008BA25C` | `0x1798F36` | memcpy (`r8=edi*8` em `008BA250`) |
| `008BA279` | `0x867CC0` | 0 ops float no próprio corpo (varredura `0x867CC0..0x867E00` só atribui aritmética a `0x867D80`, o escritor de estado da etapa G) |
| `008BA3F5` | `0x1190` | `dst[i]=a[i]*b[i]` (RVA `0x4BC0`) |
| `008BA433` | `0x1190` | idem |
| `008BA5ED` | `0x867CC0` | idem |
| `008BA745` | `0x1190` | idem |
| `008BA783` | `0x1190` | idem |

### 2.3 Constantes e offsets provados

- Única referência RIP: `008BA4C6 cmp dword [0x21C7690],2` = `05 00 00 00` (i32 5). Não é
  coeficiente.
- `008BA1DA mov r8d,[rcx+0x404]` → `arg1` é descritor com `int` em `+0x404` (mesma forma
  D128 do `arg2` de `0x8B8E70`).
- `008BA1FD mov edi,[r14+0x80]` → `arg3` é descritor D128/D16 com count em `+0x80`.
- `008BA3CB mov r15d,[rbp+0x5F4]` e `008BA3B9 mov eax,[rbp+0x5F0]` → contagens dos
  descritores internos montados por `0x867CC0` (offsets `+0x5F0`/`+0x5F4`).
- `008BA420..008BA433`: `r8=[rbp+rdi+0x600]` (dst), `rcx=[rbp+rdi-0x50]` (a),
  `rdx=[rbp+rdi+0x40]` (b) → multiplicação vetorial de dois estagiários.
- **Conclusão de aritmética**: `0x8BA1B0` não tem `mulss/addss/subss/divss` no próprio
  corpo; toda a aritmética são 4 chamadas `0x1190` (produto vetorial).

---

## 3. `0x8BA7B0` vs `0x8A1EE0` — confirmação byte a byte

Comparação dos 270 B dos dois corpos (`0x8BA7B0..0x8BA8BE` × `0x8A1EE0..0x8A1FEE`):
**não são idênticos**; há **9 bytes diferentes**.

| RVA `0x8BA7B0` | bytes | RVA `0x8A1EE0` | bytes | instrução |
|---|---|---|---|---|
| `008BA899` | `C6 44 24 20 01` | `008A1FC9` | `44 88 54 24 20` | `mov byte [rsp+0x20], 1` **vs** `mov byte [rsp+0x20], r10b` |
| `008BA8B2..B5` | `EA 8C FF FF` | `008A1FE2..E5` | `BA 15 01 00` | `rel32` do `call` — alvo é o **mesmo** `0x8B35A0` nos dois |

`r10b` vale 0: `008A1EE7 mov r10d,8` e `008A1FBD sub r10,1; 008A1FC1 jne` deixam `r10=0`
ao sair do laço. Logo:

- `0x8BA7B0` grava **flag = 1** (`008BA899`).
- `0x8A1EE0` grava **flag = 0** (`008A1FC9`, via `r10b`).

**Único parâmetro que difere: o 5º argumento (byte de flag) de `0x8B35A0`.** Ele é lido no
callee em `008B377E cmp byte ptr [rsp+0x8C0],0` (callee: `rsp_e+0x28` = 1º arg de pilha).
Flag≠0 → ramo `008B379B`/`008B37B3` (`0x1070` com `xmm1=0.5`); flag=0 → ramo
`008B37CD`/`008B37E2` (`0x10A0` cópia). O restante dos corpos é idêntico em semântica.

---

## 4. `0x8B35A0` — 659 B (`0x8B35A0..0x8B3833`), 9 `call`, sem float próprio além de `0.5`

### 4.1 Chamadores e argumentos

Chamado por `0x8BA7B0` em `008BA8B1` e por `0x8A1EE0` em `008A1FE1` (mesma chamada, flag
diferente), além de `00890323`, `00892F73`, `008A4213`, `008A6E63`.

Em `0x8BA7B0`:
```
008BA896  mov  r9, r8              ; arg4 = arg3 original (lista de descritores)
008BA899  mov  byte [rsp+0x20],1   ; flag = 1
008BA89E  mov  r8, rdx             ; arg3 = arg2 original
008BA8A1  lea  rcx,[rsp+0x440]     ; arg1 = 1ª cópia do arg1 original (D128)
008BA8A9  lea  rdx,[rsp+0x30]      ; arg2 = 2ª cópia do arg1 original (D128)
008BA8B1  call 0x8B35A0
```

### 4.2 Aritmética provada (impls resolvidas por tabela)

| RVA | thunk | impl | aritmética provada | prova |
|---|---|---|---|---|
| `008B375E` | `0x15B0` | `0xCF40` | `dst[i] = a[i] + b[i]` (`a=rcx`, `b=rdx`, `dst=r8`, `n=r9d`) | `0000CF47 mov rbp,rdx`; `0000CFE0 vmovss xmm0,[rcx+rax*4]`; `0000CFE5 vaddss xmm1,xmm0,[rbp+rax*4]`; `0000CFEB vmovss [r8+rax*4],xmm1` |
| `008B3779` | `0x11C0` | `0x50E0` | `dst[i] = b[i] − a[i]` (`a=rcx`, `b=rdx`, `dst=r8`) | spec §17.6 (`0005180 vmovss xmm0,[rbp]`; `0005186 vsubss xmm1,xmm0,[rcx]`; `000518B` store `[r8]`) |
| `008B379B`, `008B37B3` | `0x1070` | `0x2760` | `dst[i] = escalar × src[i]` (`src=rcx`, `dst=r8`, `n=r9d`, `escalar=xmm1`) | `00002769 mov rdx,r8`; `00002800 vmulss xmm0,xmm1,[rcx+r10*4]`; `00002806 vmovss [rdx+r10*4],xmm0` |
| `008B367A`, `008B37CD`, `008B37E2` | `0x10A0` | `0x2C80` | cópia de N floats (`src=rcx`, `dst=rdx`) | spec §17.6 / §10.4 |

`0x15B0` e `0x1070` **não estavam** na tabela §17; resolvidos agora por
`jmp [tab+4*8]` (`0x15B0`→`0xCF40`, `0x1070`→`0x2760`).

### 4.3 Ordem real por entrada de descritor

```
; r9 = arg3 = lista de entradas de 24 B; [r9]=início, [r9+8]=fim
008B362C  mov rsi,[r8]        ; rsi = entrada atual
008B3634  cmp rsi,[r8+8]
008B3660  cmp dword [rsi+0x10],1   ; mode
008B3664  mov rbx,[rsi+8]          ; index
; --- cópia (mode==1 e arg1!=arg2) ---
008B366F  mov rdx,[r14+rbx*8]      ; dst = arg1->ptr[index]
008B3676  mov rcx,[r15+rbx*8]      ; src = arg2->ptr[index]
008B367A  call 0x10A0
; --- senão: soma/diferença do par (index, index+1) ---
008B36D0..008B36E4  Q[0..1] = arg2->ptr[index..index+1]   ; 2 ponteiros
008B3732..008B3746  P[0..1] = arg1->ptr[index..index+1]
008B3748  rdx = Q[1]
008B3753  rcx = Q[0]
008B375E  call 0x15B0            ; rbp = Q[0] + Q[1]
008B3763  rdx = Q[0]
008B376E  rcx = Q[1]
008B3779  call 0x11C0            ; r12 = Q[0] − Q[1]   (dst = rdx−rcx)
008B377E  cmp byte [rsp+0x8C0],0
; flag!=0:
008B379B  call 0x1070            ; P[0] = 0.5 * rbp    (xmm1=0.5, xmm6)
008B37B3  call 0x1070            ; P[1] = 0.5 * r12
; flag==0:
008B37CD  call 0x10A0            ; P[0] = rbp
008B37E2  call 0x10A0            ; P[1] = r12
008B37EA  add rsi,0x18           ; próxima entrada
```

Constante única: `008B3650 movss xmm6,[0x2079EA8]` = bytes `00 00 00 3F` = `0.5f`.

**Aritmética provada:** por par de buffers, `out0 = in0 ± in1` e `out1 = in0 ∓ in1`,
escalados por `0.5` quando flag=1. O rótulo "mid/side" é interpretação — a aritmética
(`add`/`sub`/`0.5·`) é que está provada.

### 4.4 Layout provado em `0x8B35A0`

| arg | offsets provados | instrução |
|---|---|---|
| `arg1` (rcx) | `int len` @`+0x404`; `ptr[i]` @`+8i` | `008B35B6 mov edi,[rcx+0x404]`; `008B366F mov rdx,[r14+rbx*8]` |
| `arg2` (rdx) | `ptr[i]` @`+8i` | `008B3676 mov rcx,[r15+rbx*8]` |
| `arg3` (r8) | lista de entradas de **24 B**: `[+8]=index (qword)`, `[+0x10]=mode (int)`; `[r8]=início`, `[r8+8]=fim` | `008B362C/8B3628`; `008B3660/8B3664`; `008B37EA add rsi,0x18` |
| `arg4` (r9) | arena bump: `void* base` @0, `int cursor` @`+0x18` | `008B35BF mov ebx,[r9+0x18]`; `008B35C6 mov rax,[r9]`; `008B35F9/8B3624` grava cursor |
| `arg5` (pilha) | flag byte | `008B377E cmp byte [rsp+0x8C0],0` |

Alocação: `008B35D6 lea rbp,[rax+r10*4]` (buffer 1) e `008B3603 lea r12,[rax+rcx*4]`
(buffer 2), cada um com `edi = [arg1+0x404]` floats, cursor arredondado por
`008B35E7 and eax,0xF` / `008B35ED add rdx,0x10` / `008B35F5 cmove`.

---

## 5. Respostas explícitas

### (a) magnitude ou potência?

**Nenhuma das duas.** Não existe `sqrt`/`sqrtss`/`sqrtps`/`vsqrt*`/`rsqrtps` em
`0x8A0000..0x8E0000` (varredura de bytes: 0 ocorrências). Em `0x8B8E70` a única
aritmética é:

- `expf` vetorial sobre cada buffer de entrada — `008B90D7 call 0x1C84A0` →
  `0x1C8880` → `0x240C00` (`00240C44 mov r14,rcx` src; `00240C38 mov r12,rdx` dst;
  `00240C15 mov ebp,r8d` n);
- **1/N** — `008B942A divss xmm6,xmm0`, com `1.0f` em `0x2079F9C` (`008B9418`) e
  `N=[arg3+0x18]` (`008B940B/8B9424`);
- FFT inversa `008B93FC` (→ `0x7B40`) e FFT direta `008B9DFB` (→ `0x20E0`).

`0x8BA1B0` só tem produto vetorial `0x1190` (4 sítios); `0x8B35A0` só tem
`soma`/`diferença`/`×0.5`; `0x8BA7B0` só tem cópias. **Portanto M não calcula
magnitude nem potência.** O que `0x8B8E70` faz é aplicar `exp` (converte domínio
logarítmico→linear) e transformar espectro↔tempo. A fórmula provada é:

```
h[n] = (1/N) · IFFT{ exp(x[k]) }        ; 008B90D7 (exp), 008B93FC (IFFT), 008B942A (1/N)
```

O domínio exato de `x` (dB, ln-amplitude ou ln-potência) em `arg2` é **NÃO PROVADO** —
parou no produtor do descritor em `0x8AD2B0` (`008AD930..008AD9F3` copia `rbp+0x11B0`
para `arg2`; a origem de `rbp+0x11B0` não foi rastreada até o cálculo).

### (b) dBFS de referência e onde está a constante

**Não existe constante de dBFS em nenhuma das quatro funções.** As únicas referências
RIP são `0x2079F9C` (`1.0f`, `008B9418`), `0x2079EA8` (`0.5f`, `008B3650`) e
`0x21C7690` (`i32 5`, `008B9549`/`008BA4C6`, checagem de CPU). `0x8BA1B0`,
`0x8BA7B0` e `0x8B35A0` não têm `log10`/`20`/`0.115129255` no corpo.

O único fator dB↔linear já provado na cadeia está **fora de M**: `0x2079DBC` =
`0.115129255f` (= `ln(10)/20`, bytes `E3 C8 EB 3D`), usado em `0088E399`
(spec §8.2). O dBFS de referência de M é, portanto, **NÃO PROVADO**; o valor, se
existir, está no cálculo que alimenta `arg2`, acima de `008AD9F3`.

### (c) tilt (se existe) e fórmula

**Não existe em M.** Nenhum coeficiente dependente de frequência é lido nas quatro
funções: só `1.0f` (`0x2079F9C`), `0.5f` (`0x2079EA8`) e o inteiro de CPU
(`0x21C7690`). O `0.5f` de `0x8B35A0` é fator escalar de soma/diferença por par, não
tilt. Qualquer tilt tem de estar a montante de `008AD9F3` — **NÃO PROVADO**.

### (d) número de bandas do filtro de análise (não o da UI)

**Nenhum literal fixa esse número em M.** O número é **campo de runtime**:

- consumidor em `0x8B8E70`: `008B8F61 movsxd r12,[rbp+0x1090]`, onde
  `[rbp+0x1090]` recebeu `[arg2+0x400]` em `008B8F3B/8B8F4E`. `r12` é o contador dos
  laços (`008B8FC4 cmp r8,r12`; `008B90E0 sub rsi,1`; `008B94B2 sub rsi,1`).
- produtor em `0x8AD2B0`: `008AD310 mov rbx,[rax+0x48]` → `008AD32A mov [rbp+0x15B0],ebx`
  (campo count do D128 em `rbp+0x11B0`, `+0x400`), e o laço `008AD345..008AD383` usa
  `r9=ebx`.

O literal **8** que aparece em `0x8B8E70` (`008B8ED1 mov edx,8`; `008B8FD7 mov edx,8`),
em `0x8BA1B0` (`008BA283 mov r13d,8`), em `0x8BA7B0` (`008BA7B7 mov r10d,8`) e em
`0x8A1EE0` (`008A1EE7 mov r10d,8`) é o **número de blocos de 0x80 B** copiados
(capacidade de 16 ponteiros / 1024 B), **não** o número de bandas. A afirmação
"8 bandas de análise" **não se sustenta por instrução** aqui: **NÃO PROVADO**, parou em
`008AD314` (origem de `[ctx+0x48]`).

### (e) layout dos buffers de análise

Provas por função nas seções 1.5 e 4.4. Resumo:

```
D128 (arg2 de 0x8B8E70; arg1 de 0x8B35A0/0x8BA1B0):
  +0x000  void* ptr[128]        ; 008B8EE0..008B8F39 (capacidade 0x400 B)
  +0x400  int   count           ; 008B8F3B/8B8F4E/8B8F61
  +0x404  int   len (floats)    ; 008B8F57/8B8F61; 008B35B6

D16 (arg1 e arg4 de 0x8B8E70):
  +0x000  void* ptr[16]         ; 008B9192 (0x80 B)
  +0x080  int   count           ; 008B9199/008B91BD
  +0x084  int   len (floats)    ; 008B91C4

FFT ctx (arg3 de 0x8B8E70):
  +0x000  void* a ; +0x008 void* b   ; 008B93E0/8B93E8 → usa [a+8] e [b]
  +0x018  int   N (tamanho FFT)      ; 008B8EA0, 008B926B, 008B940B

Arena (arg5 de 0x8B8E70; arg4 de 0x8B35A0):
  +0x000  void* base
  +0x018  int   cursor (floats)      ; 008B8EAB/8B8F90/8B8FC0; 008B35BF/8B35C6

Lista de descritores (arg3 de 0x8B35A0):
  entrada de 24 B: +0x08 qword index ; +0x10 int mode
  [r8]=início, [r8+8]=fim            ; 008B3628/8B362C/8B3660/8B3664/8B37EA
```

---

## 6. NÃO PROVADO (com o RVA onde parou)

1. **Domínio de `arg2` de `0x8B8E70`** (log, dB, ln-potência?): o descritor é copiado de
   `rbp+0x11B0` em `008AD930..008AD9F3`; a origem do conteúdo de `rbp+0x11B0` não foi
   rastreada. Parou em `008AD9F3`.
2. **dBFS de referência**: não há constante em M; parou na ausência de leitura em
   `0x8B8E70`/`0x8BA1B0`/`0x8BA7B0`/`0x8B35A0`. Único dB provado fora de M: `0088E399`
   (`0x2079DBC`).
3. **Tilt**: não há coeficiente em M. NÃO PROVADO se existe a montante; parou em
   `008AD9F3`.
4. **Número de bandas**: count é `[ctx+0x48]`; parou em `008AD314` (quem escreve
   `[ctx+0x48]` não foi lido nesta etapa).
5. **Identidade de `0x86F480` e `0x867CC0`** (chamados por `0x8BA1B0` em `008BA1EE` e
   `008BA279`/`008BA5ED`): sem aritmética float; nomes IPP **NÃO PROVADOS**. Parou em
   `008BA1EE`.
6. **Semântica exata da fase 6 de `0x8B8E70`** (uso de `arg4`, `L/2` em `008B94E1`, e a
   FFT direta final em `008B9DFB`): ordem transcrita; o papel dos 16 buffers
   (`arg4`) é **NÃO PROVADO**. Parou em `008B94B8`.
7. **Cópias irmãs** `008BCF4A`, `008BE95A`, `008AF7FA` (chamadores de `0x8B8E70`) e
   `008BD4EB`/`008BEEFB` (de `0x8BA1B0`): não abertas; apenas o alvo do `call` foi
   confirmado por `E8 disp32`.
