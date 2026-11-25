# N — processador de canal e ordem real dos estágios

Fonte única: `dumpsooth/nyx_soothe3_dump.bin`
SHA-256 `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`.
Endereços = RVA (imagem 0x180000000). Ponteiro de dado no dump: VA base 0x199B0000.
Somente leitura estática (Capstone via `tools/show_func.py`, `tools/win2.py`,
`tools/resolve_thunk.py`). Nenhum hook/patch/escrita.

Método por linha: instrução `RVA  mnemônico  operandos`. Toda afirmação abaixo
aponta a instrução. O que não fecha está em **NÃO PROVADO** com o RVA onde parou.
`functions.csv` não foi usado.

Desmontagens usadas:
- `checks/8ad2b0.dis` (já existente, 1.127 linhas, 0x8AD2B0..0x8AE64D)
- `checks/889bb0.dis` (gerada nesta etapa, 982 linhas, 0x889BB0..0x88AE20)
- `checks/8b3ed0_full.dis`, `checks/8c1440.u8.dis` (contexto já provado)
- `checks/8ac...`, trechos de 0x8ACC40/0x899940/0x881050/0x8634A0/0x86A4E0/0x86FE90

---

## 0. Modelo de objetos (nomes usados neste documento)

Cadeia de chamada provada (sítio a sítio):

```
0x8774A0 (0087751C) -> 0x881050
0x881050 (008813B9) -> 0x889BB0        ; rcx = [canal] + 0x2C50
0x889BB0 (0088AE0F) -> 0x899940
0x899940 (0089A06B) -> 0x8ACC40
0x8ACC40 (008ACF2B) -> 0x8AD2B0
0x8AD2B0 (008AD601) -> 0x8B3ED0        ; núcleo
0x8B3ED0 (008B605C / 008B80DC) -> 0x8C0BD0   ; detector
0x8B3ED0 (008B606E / 008B80EE) -> 0x8C1440   ; estagiador + mistura
```

Nomes:

| Nome | Definição provada | Prova |
|---|---|---|
| `C` | objeto canal = argumento 1 de `0x881050` | `0088108A mov rsi,rcx`; `0088139D lea rcx,[rsi+0x2c50]` |
| `X` | subobjeto `C+0x2C50`; argumento 1 de `0x889BB0` e do núcleo | `0088139D`; `00889BD7 mov rbx,rcx`; `008B3F14 mov r13,rcx` |
| `CTX` | argumento 1 de `0x8AD2B0` = `{arena*, X*, byte*, byte*, byte*}` montado em `0x889BB0` | `0088AC7C..0088ACB2`; `008AD2DE mov rdi,rcx`; `008AD301 mov rax,[rcx+8]` |

`CTX` (5 qwords, montado em `0x889BB0`, `0088AC75`–`0088ACB2`):

| off | valor provado | prova |
|---:|---|---|
| +0x00 | `r12` (8º argumento de `0x889BB0`) | `0088AC7C mov [rbp+0x2b0],r12` |
| +0x08 | `X` | `0088AC96 mov [rbp+0x2b8],rbx` (rbx=rcx em `00889BD7`) |
| +0x10 | `&[rbp+0x3F8]` (byte) | `0088AC83/0088ACAB..0088ACB2` |
| +0x18 | `&[rsp+0x40]` (byte, `=([X+0x2C38]->0xB0==1)`) | `00889BE7..00889BFD`; `0088AC9D` |
| +0x20 | `&[rbp+0x3F0]` (byte) | `0088ACB2 mov [rbp+0x2d0],rax` |

Logo, dentro de `0x8AD2B0`, **`[engine+0x40]` = `X+0x40`** e
**`[engine+0x48]` = `X+0x48`**, porque `008AD2E1 mov r14,[rcx]` (=CTX+0),
`008AD301 mov rax,[rcx+8]` (=X) e `008AD30C/008AD310` leem `[X+0x40]/[X+0x48]`.
O mesmo `X` é `e` de `0x8C1440` (`008B606B mov rcx,r13`).

---

## 1. `0x8AD2B0` — processador de canal (5.021 B, 25 `call`, 0 op float)

`.pdata`: `0x8AD2B0..0x8AE64D`, tamanho **5.021** (fim em `008AE64C ret`,
`008AE64D int3`).

### 1.1 Assinatura (lida do prólogo, sem inferência)

```
0x8AD2B0(CTX *rcx, void *rdx /*arg2*/, void *r8 /*arg3*/, void *r9 /*arg4*/)
```

- `008AD2DE mov rdi,rcx` — arg1 = CTX.
- `008AD2B5 mov [rsp+0x10],rdx` — casa de arg2; relido em
  `008AE1C8 mov rdx,[rbp+0x2658]` (rbp+0x2658 = casa de arg2).
- `008AD2B0 mov [rsp+0x18],r8` — casa de arg3; relido em
  `008AD4C1 mov r15,[rbp+0x2660]` (= home de r8).
- `008AD2F9 mov r12,r9` — arg4 = struct de 0xA0 B copiada para `[rbp+0x580]`
  (`008AD4CF`–`008AD56A`).

### 1.2 Mapa dos 25 `call` (sítio, alvo, argumentos por registrador)

| # | sítio | alvo | argumentos (registrador/stack) |
|---:|---|---|---|
| 1 | `008AD2D3` | `0x17978C0` | `eax=0x2708`; sonda de pilha (identidade exata NÃO PROVADA; mesmo alvo de `008C145F`) |
| 2 | `008AD31B` | `memset` (`0x1798F42` → IAT `0x1D8D580`) | `rcx=&[rbp+0x11B8]`, `edx=0`, `r8d=0x3F8` |
| 3 | `008AD3B7` | `memset` | `rcx=&[rbp+0x21F8]`, `edx=0`, `r8d=0x3F8` |
| 4 | `008AD453` | `memset` | `rcx=&[rbp+0x15C8]`, `edx=0`, `r8d=0x3F8` |
| 5 | `008AD601` | `0x8B3ED0` (núcleo) | `rcx=[rdi+8]=X`; `rdx=&[rbp+0x11B0]`; `r8=&[rbp+0x21F0]`; `r9=&[rbp+0x15C0]`; `[rsp+0x20]=&[rbp]` (cópia de `*arg3`); `[rsp+0x28]=&[rbp+0x580]` (cópia de `*arg4`); `[rsp+0x30]=byte[[rdi+0x10]]`; `[rsp+0x38]=byte[[rdi+0x18]]`; `[rsp+0x40]=r14=[rdi]` (arena) |
| 6 | `008AD63D` | `memset` | `rcx=&[rbp+0x998]`, `edx=0`, `r8d=0x3F8` |
| 7 | `008AD6DE` | `memset` | `rcx=&[rbp+0x19D8]`, `edx=0`, `r8d=0x3F8` |
| 8 | `008AD8A3` | `0x8AE650` | `rcx=&[rbp+0x170]`, `rdx=&[rbp+0x580]`; retorno `rax`→`r11` (`008AD8B3`) |
| 9 | `008AD9FA` | `0x8B8E70` | `rcx=&[rbp]`; `rdx=&[rbp+0x1DE0]`; `r8=X+0x68`; `r9=&[rbp+0xD0]`; `[rsp+0x20]=r14=[rdi]` (arena) |
| 10 | `008ADB03` | `0x8AE650` | `rcx=&[rbp+0x170]`, `rdx=&[rbp+0x580]` |
| 11 | `008ADC52` | `0x8B9E40` | `rcx=&[rbp+0xD0]`; `rdx=&[rbp+0x1DE0]`; `r8=X+0x68`; `r9=&[rbp]`; `[rsp+0x20]=r14` (arena) |
| 12 | `008ADD26` | `0x10D0` (stub IPP) | `rcx=[rbp+0xDA0+i*8]`, `edx=r15d=[rbp+0xD94]`; laço `i<[rbp+0xD90]` |
| 13 | `008ADE13` | `memset` | `rcx=&[rbp+0x178]`, `edx=0`, `r8d=0x3F8` |
| 14 | `008ADE4D` | `memcpy` (`0x1798F36` → IAT `0x1D8D590`) | `rcx=&[rbp+0x170]`, `rdx=&[rbp+0x990]`, `r8=r13*8` |
| 15 | `008ADF9B` | `0x8BA1B0` | `rcx=&[rbp+0xDA0]`; `rdx=&[rbp+0x580]`; `r8=&[rbp]`; `r9` **não recarregado neste sítio** (herdado do ramo 9/11) |
| 16 | `008ADFE0` | `memset` | `rcx=&[rbp+0x588]`, `edx=0`, `r8d=0x3F8` |
| 17 | `008AE01A` | `memcpy` | `rcx=&[rbp+0x580]`, `rdx=&[rbp+0x990]`, `r8=r15*8` |
| 18 | `008AE096` | `0x8BA7B0` | `rcx=&[rbp+0xDA0]`, `rdx=r14=[X+0x10]`, `r8=[rdi]` (arena) |
| 19 | `008AE1AF` | `0x1010` (stub IPP, FFT direta) | `rcx=[rbp+rbx+0x1DE0]`, `rdx=[rbp+rbx+0xDA0]`, `r8=*(void**)(X+0x68+8)`, `r9=*(void**)(X+0x70)` |
| 20 | `008AE1EC` | `0x619D90` | `rcx=[rdi]` (arena), `rdx=[rbp+0x2658]=arg2`, `r8=[X+0x48]`, `r9=[X+0x38]` |
| 21 | `008AE321` | `memcpy` | `rcx=&[rsp+0x50]`, `rdx=&[rbp+0x170]`, `r8=edx*8` |
| 22 | `008AE420` | `0x1520` (stub IPP, cópia) | `rcx=[rbp+rsi]` (array i), `rdx=[rbp+rsi+0x990]`, `r8d=[rbp+0xD94]` |
| 23 | `008AE459` | `0x1520` | `rcx=r15` (buffer único), `rdx=[rsi]` (array i de 0x990), `r8d=[rbp+0xD94]` |
| 24 | `008AE55F` | `0x8BA8C0` | `rcx=X+0x68`, `rdx=&[rbp+0x1DE0]`, `r8=&[rbp+0xDA0]` |
| 25 | `008AE5EC` | `0x8A1EE0` | `rcx=&[rbp+0xDA0]`, `rdx=[[rdi+8]+0x10]=[X+0x10]`, `r8=[rdi]` (arena) |

Os três `memset` 2–4 zeram o cabeçalho (`0x3F8 B`, até `+0x400`) de três
descritores de `0x410 B`; os `+0x400/+0x404/+0x408` são gravados em seguida
(§4). Os descritores ficam em `[rbp+0x11B0]`, `[rbp+0x21F0]`, `[rbp+0x15C0]`.

### 1.3 Ordem real dos estágios (1 → 25)

```
[0x8AD2B0 entrada]
  (1) sonda de pilha
  (2)(3)(4) três descritores de arena zerados
  (5) 0x8B3ED0  ÚNICO núcleo        <-- 0x8C0BD0 e 0x8C1440 rodam DENTRO daqui
  (6)(7) dois descritores zerados
  ramo de 0x8AD75B:
     cfg = [X+0x2C38]; se byte[cfg+0x58]!=0 -> (8)(9)  [0x8AE650 + 0x8B8E70]
                                        senão      -> (10)(11)[0x8AE650 + 0x8B9E40]
  (12) 0x10D0 preenche N buffers de comprimento [rbp+0xD94]
  (13)(14) descritor + cópia da lista de ponteiros
  (15) 0x8BA1B0
  se byte[[X+0x2C38]+0x52]!=0:
     (16)(17) descritor + cópia
     (18) 0x8BA7B0
  (19) 0x1010 em laço (FFT direta), N = [rbp+0xD90]
  (20) 0x619D90 (monta descritor count=[X+0x48], len=[X+0x38])
  (21) cópia de lista de ponteiros
  comparação de contagens:
     igual      -> (22) 0x1520 em laço
     edx==1     -> (23) 0x1520
  (24) 0x8BA8C0
  se byte[[X+0x2C38]+0x52]!=0:
     (25) 0x8A1EE0
[retorno rax=rbx=0x8AD8B3... ver 008AE636 mov rax,rbx]
```

**Consequência provada:** a hipótese “análise → núcleo → estagiador → mistura”
como ordem linear dentro de `0x8AD2B0` está **refutada**. O estagiador/mistura
`0x8C1440` é chamado **dentro** do núcleo (`008B606E`, `008B80EE`), e as funções
de análise `0x8B8E70`/`0x8B9E40`/`0x8BA1B0`/`0x8BA7B0` são chamadas **depois**
do núcleo (sítios 9/11/15/18). A única coisa que roda antes de `0x8AD2B0` na
cadeia é o bloco de `0x889BB0` (§2).

### 1.4 Ramos e flags (quem decide cada caminho)

| decisão | instrução | condição | destino |
|---|---|---|---|
| caminho A/B da “análise” | `008AD75B mov rax,[rdi+8]`; `008AD764 mov rcx,[rax+0x2c38]`; `008AD76B movzx eax,byte [rcx+0x58]`; `008AD79F test al,al`; `008AD7A1 je 0x8ADA04` | `byte[[X+0x2C38]+0x58] != 0` → A (0x8B8E70); `==0` → B (0x8B9E40) | A: `008AD9FA`; B: `008ADC52`; ambos juntam em `008ADC57` |
| atalho que pula análise+núcleo-de-bandas+FFT+mistura | `008ADC5B mov rdx,[rax+8]`; `008ADC5F mov eax,[rdx+8]`; `008ADC62 cmp [rdx],eax`; `008ADC68 sete cl`; `008ADC6B cmp byte [X+0x59],0`; `008ADC6F jne 0x8ADC8C`; `008ADC78 movzx eax,byte[[X+0x2C38]+0x51]`; `008ADC7C test al,al`; `008ADC7E jne 0x8ADC8C`; `008ADC80 test cl,cl`; `008ADC82 je 0x8ADC8C` | `X+0x59==0` **e** `[[X+0x2C38]+0x51]==0` **e** `[ [X+8] ] == [ [X+8]+8 ]` | `008ADC84 mov r15b,1`; `008ADC87 jmp 0x8AE1C1` (salta 8–24) |
| `0x8BA7B0` só se flag | `008ADFA0 mov rax,[rdi+8]`; `008ADFA4 mov rcx,[rax+0x2c38]`; `008ADFAB movzx eax,byte [rcx+0x52]`; `008ADFB6 test al,al`; `008ADFB8 je 0x8AE09B` | `byte[[X+0x2C38]+0x52] != 0` | `008AE096` |
| ramo de `0x1520` | `008AE3E9 mov eax,[rbp+0xD90]`; `008AE3EF cmp eax,edx`; `008AE3F1 jne 0x8AE431` | `N_da0 == edx` (contagem do wrapper de `[rbp+0x170]`) | igual → laço `008AE420`; `008AE431 cmp edx,1` / `008AE434 jne 0x8AE473` → `008AE459` |
| `0x8A1EE0` só se flag | `008AE564 mov rax,[rdi+8]`; `008AE568 mov rax,[rax+0x2c38]`; `008AE56F movzx eax,byte [rax+0x52]`; `008AE573 test al,al`; `008AE575 je 0x8AE5F1` | `byte[[X+0x2C38]+0x52] != 0` | `008AE5EC` |

### 1.5 Constantes e offsets usados nesta função

| valor | RVA da constante/instrução | uso |
|---:|---|---|
| `0x3F8` | imediato em `008AD2F3`/`008AD39B`/`008AD437`/`008AD620`/`008AD6D0`/`008ADFD2` | bytes zerados do cabeçalho do descritor de 0x410 B |
| `0x410` | decorre de `0x3F8`+`0x18`; descritores em passos de `0x80`×8 | ver `008AD930..008AD981` (8×0x80) |
| `0x400/0x404/0x408` | `008AD32A..008AD337`, `008AD3C6..008AD3D3`, `008AD462..008AD46F` | count / len / stride*4 do descritor |
| `0x2C38` | `008AD764`, `008ADC71`, `008ADFA4`, `008AE568` | ponteiro de configuração dentro de X |
| `0x2BC8` | núcleo `008B3EF7 cmp byte [rcx+0x2bc8],0` | flag de reset do núcleo; escrita por `0x889BB0` em `0088AC13` |

### 1.6 Structs provados nesta etapa

- **Descritor de arrays (`0x410 B`)**: `+0x000..+0x3FF` = `void*[128]`;
  `+0x400 i32 count`; `+0x404 i32 len`; `+0x408 i64 len*4`.
  Prova: `008AD31B` zera `0x3F8` a partir de `+0x8` (base `+0x0` = 0),
  `008AD32A` grava `+0x400`, `008AD330` grava `+0x404`, `008AD337` grava
  `+0x408`; cópia de `0x400`=8×0x80 em `008AD930`.
- **CTX**: ver §0.
- **Wrapper de `0x8AE650`**: `+0x80 i32 count` (copia `count` qwords),
  `+0x84 i32 cap`, `+0x88 i64 cap*8` (`008AE650..008AE6E6`).
- **Wrapper de `0x8AE6F0`**: `+0x400 i32 count`, `+0x404 i32 n`,
  `+0x408 i64 n*4` (`008AE70A/008AE740/008AE747/008AE736`).

---

## 2. `0x889BB0` — bloco que precede o processador de canal

Desmontagem: `checks/889bb0.dis` (982 linhas, `0x889BB0..0x88AE20`).

### 2.1 Tamanho real (`.pdata`, não estimativa)

| fragmento | início | `.pdata` |
|---|---|---|
| 1 | `0x889BB0` | 104 B |
| 2 | `0x889C18` | 924 B |
| 3 | `0x889FB4` | 2.009 B |
| 4 | `0x88A78D` | 1.171 B |
| 5 | `0x88AC20` | 85 B |
| 6 | `0x88AC75` | 427 B |

Fim: `00889B..`→ último `ret` em `0088AE1F`, `int3` depois. Total **4.720 B**
(`0x889BB0..0x88AE20`), confirmado pelo cabeçalho do `.dis`
(`# function 0x889BB0..0x88AE20  size=4720`). Os 10.617 B citados no plano
estão **refutados**. O gêmeo `0x88AE20..0x88C090` tem os mesmos 6 fragmentos
com os mesmos tamanhos: `checks/88AE20.dis` (`# size=4720` idem).

### 2.2 Chamador único e assinatura

`0x889BB0` tem **um** chamador: `008813B9 call 0x889bb0`, dentro de `0x881050`.

```
00881398  mov      qword ptr [rsp + 0x30], rbx      ; arg7 = rbx
0088139D  lea      rcx, [rsi + 0x2c50]              ; arg1 = C+0x2C50  (X)
008813A4  mov      byte ptr [rsp + 0x28], dil        ; arg6 = dil (byte)
008813A9  lea      r9, [rbp + 0x60]                  ; arg4 = &[rbp+0x60]
008813AD  mov      r8, r11                           ; arg3 = r11 = arg3 de 0x881050
008813B0  mov      byte ptr [rsp + 0x20], 0          ; arg5 = 0
008813B5  lea      rdx, [rbp - 0x60]                 ; arg2 = &[rbp-0x60]
008813B9  call     0x889bb0
```

Origem de `r11`: `00881249 mov r11,[rbp+0x560]` = casa de `arg3` de `0x881050`
(`rbp = rsp_entrada-0x548`; `+0x560` = `+0x18` da entrada).
Origem de `rbx`: `0088107C mov rbx,[rbp+0x570]` = casa de **`arg5` de
`0x881050`** (`+0x570` = `+0x28` da entrada), e `0088109D mov eax,[rbx+0x18]`
lê o cursor desse objeto.

```
0x889BB0(X *rcx, void *rdx /*arg2*/, void *r8 /*arg3*/, void *r9 /*arg4*/,
         uint8_t arg5, uint8_t arg6, void *arg7 /*arena*/)
```

Prova do mapa de casas: `00889BB0 mov r11,rsp` (rsp da entrada);
`00889BB3 mov [r11+0x20],r9`; `00889BB7 mov [r11+0x18],r8`;
`00889BBB mov [r11+0x10],rdx`; 3 pushes (`00889BBF..00889BC3`);
`00889BC3 lea rbp,[r11-0x3c8]`. Logo `rbp+0x3C8 = rsp_entrada`,
`rbp+0x3F0 = arg5`, `rbp+0x3F8 = arg6`, `rbp+0x400 = arg7`.
Confirmação direta:
- `00889BE0 mov r12,[rbp+0x400]` → `r12 = arg7` («arena»).
- `0088AC75 lea rax,[rbp+0x3F8]` / `0088ACB2` grava em `CTX+0x20` → `arg6`.
- `0088ACAB lea rax,[rbp+0x3F0]` / `0088AC83` grava em `CTX+0x10` → `arg5`.
- `arg8` (`[rsp+0x38]` na chamada): **nenhuma escrita** entre `00881393` e
  `008813B9` → `NÃO PROVADO` (ver §5).

### 2.3 Ordem interna real (RVA por linha)

```
00889BD1  mov   eax,[rcx+0x2c30]            ; contador em X+0x2C30
00889BD7  mov   rbx,rcx                     ; rbx = X
00889BDA  sub   eax,[rdx+0x84]              ; -= campo +0x84 de arg2 (semântica: §5)
00889BE7  mov   [rcx+0x2c30],eax
00889BED  mov   rax,[rcx+0x2c38]            ; cfg = [X+0x2C38]
00889BF4  mov   eax,[rax+0xb0]
00889BFA  cmp   eax,1
00889BFD  sete  byte ptr [rsp+0x40]         ; flag = (cfg->0xB0 == 1)
00889C02  cmp   dword ptr [rcx+0x2c30],0
00889C09  jge   0x88ac75                    ; contador >= 0 -> pula TUDO
00889C0F  mov   ecx,[rcx+0x60]              ; incremento = [X+0x60]
00889C30  add   eax,ecx                     ; eax += incremento
00889C32  js    0x889c30                    ; repete enquanto negativo
00889C34  mov   [rbx+0x2c30],eax            ; contador resultante >= 0
```

Snapshot + limpeza atômica de 6 bytes de estado (`xchg` com 0):

```
00889C44  mov  [rbp+0x400],al   ; al = [X+0x2C40]   (via 00889C3C)
00889C4C  xchg [rbx+0x2c40],al  ; = 0
00889C52  movzx r14d,[rbx+0x2c41] / 00889C5D xchg [rbx+0x2c41],0
00889C63  movzx r9d,[rbx+0x2c45]  / 00889C6E xchg [rbx+0x2c45],0
00889C74  movzx r13d,[rbx+0x2c44] / 00889C7F xchg [rbx+0x2c44],0
00889C85  movzx r15d,[rbx+0x2c43] / 00889C90 xchg [rbx+0x2c43],0
00889C96  movzx esi,[rbx+0x2c42]  / 00889CA7 xchg [rbx+0x2c42],0
00889C9F  mov  [rbp+0x3d0],sil  ; guarda 2C42
```

Estágios, em ordem:

```
00889CB2  mov  rcx,rbx / 00889CB5 call 0x878070      ; só se r14b (2C41) != 0
00889CBF  mov  rcx,rbx / 00889CC2 call 0x868F90      ; só se r9b  (2C45) != 0
00889CC7  cmp  byte [rbp+0x400],dil / je 0x889f37    ; se 2C40 == 0, pula bloco
   00889CD4..00889DF6  0x10D0 em laço: rcx=[rsp+0x50+i*8], edx=r15d
                        (conjunto X+0xA18, count [X+0xAA0])
   00889E05..00889F26  0x10D0 em laço: mesmo esquema
                        (conjunto X+0xB38, count [X+0xBC0])
00889F37  test sil / jne  ; 2C42
00889F3C  test r14b / jne ; 2C41
00889F41  test r15b / je 0x889f58 ; 2C43
00889F46  mov  rdx,r12 / 00889F4C call 0x87BB60     ; (X, arg7)
00889F58  test r13b / je 0x889f68                   ; 2C44
00889F5D  mov  rdx,r12 / 00889F63 call 0x87E220     ; (X, arg7)
00889F68  cmp  byte [rbp+0x400],dil / jne 0x889f7f  ; 2C40
00889F71  test sil / jne 0x889f7f                   ; 2C42
00889F76  test r13b / je 0x88ac4d                   ; 2C44 -> sai sem processar
00889F7F  mov  rcx,rbx / 00889F82 call 0x87B2A0     ; (X)
00889F87  test sil / jne 0x889f95
00889F8C  test r13b / je 0x88ac4d                   ; 2C44 -> sai sem processar
```

Bloco principal (só entra com `2C40` ou `2C42` ou `2C44` != 0):

```
00889F95..0088A1C9  monta dois conjuntos temporários e chama 0x87F0C0
00889FAD  mov  xmm2,[rbx+0x5c]        ; float [X+0x5C]
0088A0E6  mov  r9,[rbx+0x2c38]        ; cfg
0088A0F8  mov  r8,[rbx+0x10]          ; <-- [X+0x10]
0088A1C9  movss [rsp+0x20],xmm2
0088A10E  mov  [rsp+0x28],r12         ; arg7
0088A1CF  call 0x87F0C0               ; (rcx=&[rbp+0x100], rdx=&[rbp+0x220],
                                      ;  r8=[X+0x10], r9=cfg, f=[X+0x5C], arg7)
0088A1D4  mov  r14d,[rbx+0xa08]       ; count do conjunto X+0x988
0088A1E2  mov  eax,[r12+0x18] / 0088A1F0 mov [rbp+0x3d0],eax  ; salva cursor
0088A480..0088A49A  0x1250 em laço:
        rcx=[rbp+r15+0x220], rdx=[rbp+r15+0x100], r8d=esi, xmm3=1.0,
        0088A496 mov [rsp+0x20],edi (=0)
0088A500..0088A509  0x1C8530 em laço: rcx=[r15], rdx=rcx, r8d=esi
0088A518..0088A693  monta conjunto de X+0x988; 0x8981E0(&[rsp+0x50],&[rbp+0x220])
0088A710..0088A719  0x12E0 em laço: rdx=[r15], r8d=esi, xmm0=1.0
0088A728..0088A783  monta conjunto de X+0x478 (count [X+0x4F8], len [X+0x500])
0088A783  cmp byte [rbx+0x58],dil      ; <-- flag X+0x58
0088A787  je  0x88aa8d
   caminho A (X+0x58 != 0):
    0088A84C cmp edx,r14d / jne 0x88a881 ; counts iguais -> par a par
    0088A870 / 0088A8A9  call 0x1340     ; (dst=[rbp+rsi+0x100] ou r13=[rbp+0x70],
                                          ;  src=[rsp+rsi+0x50] ou [rsi], n=r15d)
    0088A8B8..0088AA79   segundo conjunto de X+0x478; 0x1370 em laço
   caminho B (X+0x58 == 0), sítio 0088AA8D:
    0088AB70 / 0088ABA9  call 0x1340     ; mesmo esquema de par
0088ABB8  mov  rdx,r12 / 0088ABBE call 0x87F780     ; (X, arg7)
0088AC13  mov  byte [rbx+0x2bc8],1                  ; <-- marca "sujo" p/ o núcleo
0088AC1A  cmp  qword [rbx+0x48],rdi / jbe 0x88ac42  ; <-- count = [X+0x48]
0088AC30  inc  edi / 0088AC32 mov byte [rcx],1      ; rcx = X+0x2BB8+i
0088AC3C  cmp  rax,[rbx+0x48] / jb 0x88ac30         ; laço i < [X+0x48]
0088AC42  mov  eax,[rbp+0x3d0] / 0088AC48 mov [r12+0x18],eax ; devolve cursor
```

Ramificação de `0x1340` (idêntica nos dois caminhos):

```
0088A84C  cmp  edx,r14d          ; edx = count do conjunto X+0x478
0088A84F  jne  0x88a881
0088A851  test edx,edx / jle 0x88a8b8      ; vazio -> nada
0088A881  cmp  r14d,1
0088A885  jne  0x88a8b8          ; só trata "1 -> N" se a contagem de destino é 1
```

Montagem do `CTX` e cauda:

```
0088AC7C  mov  [rbp+0x2b0],r12        ; CTX+0x00 = arg7 (arena)
0088AC96  mov  [rbp+0x2b8],rbx        ; CTX+0x08 = X
0088AC83  mov  [rbp+0x2c0],rax        ; CTX+0x10 = &[rbp+0x3F8] (arg6)
0088AC9D  mov  [rbp+0x2c8],rax        ; CTX+0x18 = &[rsp+0x40] (flag 0xB0==1)
0088ACB2  mov  [rbp+0x2d0],rax        ; CTX+0x20 = &[rbp+0x3F0] (arg5)
```

Cópias por valor de `*arg4`, `*arg3`, `*arg2` (0x90 B cada):

```
0088ACC0  mov  rax,[rbp+0x3e8]        ; = arg4 (casa +0x20 da entrada)
0088ACCC..0088AD31  copia 9 x 16 B -> [rbp+0x100]
0088AD23  mov  rax,[rbp+0x3e0]        ; = arg3 (casa +0x18)
0088AD38..0088AD9D  copia 9 x 16 B -> [rbp+0x220]
0088AD8F  mov  rax,[rbp+0x3d8]        ; = arg2 (casa +0x10)
0088ADA4..0088AE0B  copia 9 x 16 B -> [rsp+0x50]
```

Chamada final:

```
0088AC8A  lea  rcx,[rbx+0x1408]      ; arg1 = &X[0x1408]
0088ACC7  lea  rdx,[rsp+0x50]        ; arg2 = cópia de *arg2
0088ACB9  lea  r8,[rbp+0x220]        ; arg3 = cópia de *arg3
0088ACA4  lea  r9,[rbp+0x100]        ; arg4 = cópia de *arg4
0088ADFE  mov  rax,[rbx+0x60] / 0088AE02 mov [rsp+0x20],rax   ; arg5 = [X+0x60]
0088ADF5  mov  rax,[rbx+0x28] / 0088ADF9 mov [rsp+0x28],rax   ; arg6 = [X+0x28]
0088ADF0  mov  [rsp+0x30],rax        ; arg7 = &CTX ([rbp+0x2b0])
0088AE0F  call 0x899940
```

Isto fecha a origem do `CTX` que `0x8AD2B0` recebe: `0x889BB0` monta `CTX`
na **própria pilha** `[rbp+0x2B0]` e o passa como 7º argumento a `0x899940`,
que o repassa até `0x8AD2B0` (`008AD2DE mov rdi,rcx`;
`008AD301 mov rax,[rcx+8]`).

### 2.4 Stubs IPP chamados por `0x889BB0` (identidade por tabela de despacho)

Cada stub faz `movsxd rax,[0x21C7408]` e `jmp [tab + rax*8]`; `[0x21C7408] = 4`
nesta máquina-alvo. Tabela `checks/thunk_semantics.txt` + leitura direta do dump:

| stub | tabela | idx=4 → | corpo | assinatura usada |
|---|---|---|---|---|
| `0x10D0` | `0x21C5E48` | `0x2F60` | `call 0x1D2E9E0`/`0x26640` | `(rcx=ptr, edx=n)` zera `n` floats |
| `0x1250` | `0x21C6048` | `0x69C0` | `vminps`/`vmaxps` | `(rcx,rdx,r8d, xmm3, stack)` saturação |
| `0x12E0` | `0x21C6108` | `0x8FA0` | `00008FA4 mov rcx,rdx`; `vaddss` | `(rdx=ptr, r8d=n, xmm0=s)` `ptr[i] += s` |
| `0x1340` | `0x21C6188` | `0x9BA0` | `00009C25 vmulss xmm1,xmm0,[rdi+rdx*4]`, store em `[rdi+…]` | `(rcx=a, rdx=b, r8d=n)` `b[i] *= a[i]` |
| `0x1370` | `0x21C61C8` | `0xA120` | `0000A1A5 vaddss xmm1,xmm0,[rdi+rdx*4]`, store em `[rdi+…]` | `(rcx=a, rdx=b, r8d=n)` `b[i] += a[i]` |
| `0x1C8530` | `0x21C6AE8` | `0x1C8AC0` → `jmp [0x21C71D8]` = `0x29B260` | `0029B328 fnstcw`; blocos de 32 | `(rcx, rdx=rcx, r8d=n)` transformada in-place |

`0x29B260` salva o control word x87 (`0029B328 fnstcw`) e processa em blocos
de 32 (`0029B28C and ebx,0xffffffe0`): a identidade IPP exata fica em
**NÃO PROVADO**; o que está provado é que é a transformada in-place do bloco.

### 2.5 Relação com `0x8AD2B0`

- `0x889BB0` **não** chama `0x8AD2B0` diretamente: encadeia via
  `0088AE0F → 0x899940 → 0089A06B → 0x8ACC40 → 008ACF2B → 0x8AD2B0`.
- `0x889BB0` escreve `byte[X+0x2BC8] = 1` (`0088AC13`); o núcleo lê esse byte
  em `008B3EF7 cmp byte [rcx+0x2bc8],0`. É o elo de estado entre o bloco daqui
  e o núcleo.
- `0x889BB0` escreve `1` em `[X+0x2BB8 .. X+0x2BB8+[X+0x48])`
  (`0088AC32 mov byte [rcx],1`, laço `0088AC1A`-`0088AC40` com limite
  `[X+0x48]`). Outros leitores do mesmo array: `00877D9F lea r8,[rcx+0x2bb8]`
  (`0x877D90`), `00886022 lea rcx,[rdi+0x2bb8]` (`0x885040`),
  `008885D2` (`0x8875F0`), `0088BE90` (`0x88AE20`). Nenhuma referência a
  `0x2BB8` existe no núcleo `0x8B3ED0` — o consumidor é um dos anteriores
  (qual deles: **NÃO PROVADO**, ver §5).
- Todos os objetos de arena usados no núcleo (`0x619D90` em `008AE1EC`) vêm de
  `CTX+0x00 = arg7` (`0088AC7C`), o `arg5` de `0x881050` (`0088107C`).

---

## 3. Campos `[engine+0x10]`, `[engine+0x40]`, `[engine+0x48]`

Todos são campos de `X` (§0): `[engine+0x10]` = `X+0x10`, etc.
(`008AD2E1 mov r14,[rcx]` → arena; `008AD301 mov rax,[rcx+8]` → `X`;
`008AD30C/008AD310` leem `[X+0x40]/[X+0x48]`).

### 3.1 Quem escreve (função de inicialização `0x86FE90`)

```
0086FE90  mov  rax,rsp
0086FEB6  maxss xmm3,[rip+0x180a726]     ; 0x207A5E4 = 44100.0
0086FF03  mov  rax,[rbp+0x448]           ; arg8  (rbp+0x408 = rsp de entrada)
0086FF0A  mov  [rcx+0x10],rax            ; X+0x10 = arg8
0086FF0E  mov  rax,[rbp+0x450]           ; arg9
0086FF15  mov  [rcx+0x18],rax            ; X+0x18 = arg9
0086FF19  movss [rcx+0x20],xmm3          ; X+0x20 = max(taxa,44100)
0086FF1E  mulss xmm3,[rip+0x1809dde]     ; 0x2079D04 = 2.26757365e-05 (1/44100)
0086FF2D  mov  qword [rcx+0x30],2
0086FF35  cvttss2si eax,xmm3
0086FF39  imul eax,[rbp+0x430]           ; arg5
0086FF40  movsxd r8,eax
0086FF43  mov  [rcx+0x28],r8             ; X+0x28 = n
0086FF47  lea  rax,[r8+r8]
0086FF4B  mov  [rcx+0x38],rax            ; X+0x38 = 2n  (tamanho da FFT)
0086FF4F  shr  rax,1
0086FF52  inc  rax
0086FF55  mov  [rcx+0x40],rax            ; X+0x40 = n+1
0086FF59  mov  ecx,[r9]
0086FF5C  call 0x56b140
0086FF61  mov  [rdi+0x48],rax            ; X+0x48 = 0x56B140(enum)
0086FF65  mov  ecx,[r9+8]
0086FF69  call 0x56b140
```

Mesma sequência em `0x873440`: `0087346D maxss …0x207A5E4`,
`0087348A mov [rcx+0x10],rax`, `008734CA mulss …0x2079D04`.

- **`X+0x40 = ((2n)>>1)+1 = n+1`** — provado por `0086FF43`→`0086FF55`
  (sem interpretação: é `lea rax,[r8+r8]; shr rax,1; inc rax`).
- **`X+0x48 = 0x56B140([r9])`** — `0x56B140` é um switch sobre um enum
  (`0x56B140` usa a tabela `0x56B1AC` e `jmp [rdx+rax*4]`, ver
  `checks/56b140.dis`), cujos retornos vão de 0 a 0x10. É o **número de
  arrays** do processador (ver uso em §3.3).
- **`X+0x10`** = arg8, um ponteiro; **`X+0x18`** = arg9, um ponteiro.
- `X+0x38 = 2n` é o tamanho da FFT e `X+0x28 = n`, ambos derivados de arg5
  escalado por `taxa/44100` (`0086FF1E`, `0086FF35`–`0086FF39`).

### 3.2 `X+0x10` é ponteiro para um par {início, fim}

```
008B6046  mov  r8,[r13+0x10]        ; r8 = X+0x10  -> arg3 de 0x8C0BD0
008B605C  call 0x8c0bd0
...
008C0BD0  mov  [rsp+8],rcx
008C0BF6  mov  r13,r9
008C0C0D  mov  rax,[r8+8]           ; fim
008C0C1F  mov  rsi,[r8]             ; início
008C0C2F  cmp  rsi,rax
008C0C32  je   0x8c1419             ; se início == fim, não itera
```

Logo `X+0x10` **aponta** para `{void **begin; void **end;}`, e o laço do
detector percorre `begin..end`. Isto é leitura direta de `[r8]`/`[r8+8]`, não
inferência.

Outros leitores de `X+0x10`:

| RVA | instrução | destino |
|---|---|---|
| `0088A0F8` | `mov r8,[rbx+0x10]` | arg3 de `0x87F0C0` (`0088A1CF`) |
| `008ADFD8` | `mov r14,[rax+0x10]` (`rax=[rdi+8]`) | `008AE090 mov rdx,r14` → arg2 de `0x8BA7B0` (`008AE096`) |
| `008AE5E8` | `mov rdx,[rdx+0x10]` (`rdx=[rdi+8]`) | arg2 de `0x8A1EE0` (`008AE5EC`) |
| `008C1A77` | `mov rax,[r8+0x10]` | dentro de `0x8C1440` |

Em `0x8C1440`, `r8` é `X` naquele ponto e não a arena: `008C144A mov [rsp+8],rcx`
guarda arg1; `rbp = rsp_entrada-0x13c8`, logo `rbp+0x13d0 = arg1`;
`008C19C8 mov r8,[rbp+0x13d0]` restaura `r8 = X`, e `008C1A0D/008C1A1B/008C1A64`
usam `[r8+0x2c38]` (offset exclusivo de `X`).

### 3.3 `X+0x40` e `X+0x48` — leitores provados

| campo | RVA | instrução | uso imediato |
|---|---|---|---|
| `X+0x40` | `008AD30C` | `mov r15,[rax+0x40]` (`rax=[rcx+8]`) | len do 1º descritor de `0x8AD2B0` |
| `X+0x40` | `008AD444` | `mov r15,[rax+0x40]` (`rax=[rdi+8]`) | len do 3º descritor |
| `X+0x40` | `008AD6DA` | `mov r14,[rax+0x40]` (`rax=[rdi+8]`) | len do descritor de `0x8AE650` |
| `X+0x40` | `008B6457` | `mov r8,[r13+0x40]` | arg3 de `0x8AE6F0` (`008B645E`) |
| `X+0x40` | `008B6593` | `mov r8,[r13+0x40]` | arg3 de `0x8AE6F0` (`008B65A4`) |
| `X+0x40` | `008B83B9` | `mov r8,[r13+0x40]` | arg3 de `0x8AE6F0` (`008B83C0`) |
| `X+0x40` | `008B84E2` | `mov r8,[r13+0x40]` | arg3 de `0x8AE6F0` (`008B84F0`) |
| `X+0x40` | `008B4BEA` | `mov r9,[r13+0x40]` | **arg4 de `0x619D90`** (`008B4BFB`) |
| `X+0x48` | `008AD310` | `mov rbx,[rax+0x48]` (`rax=[rcx+8]`) | count do 1º descritor |
| `X+0x48` | `008AD3AC` | `mov rbx,[rax+0x48]` | count do 2º descritor |
| `X+0x48` | `008AD448` | `mov rbx,[rax+0x48]` (`rax=[rdi+8]`) | count do 3º descritor |
| `X+0x48` | `008AD650` | `movsxd rcx,[rax+0x48]` | vira limite de laço: `008AD65E mov [rbp+0xd90],ecx` |
| `X+0x48` | `008AD6F1` | `movsxd rcx,[rax+0x48]` | vira limite de laço: `008AD6FF mov [rbp+0x1dd0],ecx` |
| `X+0x48` | `008AE1D6` | `mov r8,[r9+0x48]` (`r9=[rdi+8]`) | **arg3 de `0x619D90`** (`008AE1EC`) |
| `X+0x48` | `008B3FC1` | `cmp [r13+0x48],rax` | comparação com contagem local |
| `X+0x48` | `008B3FCC` | `cmp [r13+0x48],2` | ramo do núcleo |
| `X+0x48` | `008B4BF1` | `mov r8,[r13+0x48]` | **arg3 de `0x619D90`** (`008B4BFB`) |
| `X+0x48` | `0088AC1A`/`0088AC3C` | `cmp [rbx+0x48],rdi` / `cmp rax,[rbx+0x48]` | limite do array `X+0x2BB8` em `0x889BB0` |
| `X+0x38` | `008AD3A8` | `mov r15,[rax+0x38]` | len em floats (2n) |
| `X+0x38` | `008AE1DA` | `mov r9,[r9+0x38]` | **arg4 de `0x619D90`** |

Resumo do significado, por instrução e não por nome:

- `X+0x40` = `n+1` = **quantidade de floats por array** (bins de 0 a n).
- `X+0x48` = retorno de `0x56B140(enum)` = **quantidade de arrays**.
- `X+0x38` = `2n` = tamanho da FFT em floats.
- `X+0x10` = ponteiro para `{begin,end}` de uma lista de ponteiros.

Prova cruzada em `0x619D90` (`checks/619d90.dis`), que recebe exatamente
`(arena, t, count, len)`:

```
00619DA8  mov  qword [rdx],0
00619DB9  mov  r8d,0x3f8
00619DC4  call 0x1798f42            ; memset(dst+8, 0, 0x3F8)
00619DC9  movsxd rax,edi            ; edi = r9d = len
00619DCF  shl  rax,2
00619DD6  mov  [r14+0x408],rax      ; +0x408 = len*4
00619DDD  mov  [r14+0x400],ebx      ; +0x400 = r8d = count
00619DE4  mov  [r14+0x404],edi      ; +0x404 = r9d = len
```

Nos dois sítios em que é chamado com `[X+0x48]`/`[X+0x40]`
(`008AE1EC` e `008B4BFB`), resulta `t+0x400 = [X+0x48]` e
`t+0x404 = [X+0x40]`.

### 3.4 Constantes usadas

| valor | RVA | uso |
|---|---|---|
| `44100.0` | `0x207A5E4`, lida em `0086FEB6`/`0087346D` | piso da taxa de amostragem |
| `1/44100` (`2.26757365e-05`) | `0x2079D04`, lida em `0086FF1E`/`008734CA` | converte tempo em amostras |
| `2` | imediato em `0086FF2D` | `X+0x30 = 2` |
| tabela do switch | `0x56B1AC`, usada em `0x56B140` | enum → nº de arrays |

---

## 4. Origem do par `t+0x400` / `t+0x404`

`t` é o 2º argumento (`rdx`) de `0x8C1440` (`008C14B0 mov r15d,[rdx+0x404]`;
`008C1471 mov rsi,rdx`). `0x8C1440` é chamado em **dois** sítios do núcleo:

```
008B6064  lea  rdx,[rbp + 0xc40]      ; t1
008B606B  mov  rcx,r13                ; X
008B6061  mov  r8,r12                 ; arena
008B606E  call 0x8c1440

008B80E4  lea  rdx,[rbp + 0x1870]     ; t2
008B80EB  mov  rcx,r13
008B80E1  mov  r8,r14
008B80EE  call 0x8c1440
```

### 4.1 `t1+0x400/+0x404` vêm de `[X+0x48]` / `[X+0x40]`

```
008B4BDE  mov  eax,[r12+0x18]
008B4BE3  lea  rdx,[rbp + 0xc40]      ; dst = t1
008B4BEA  mov  r9,[r13 + 0x40]        ; len  = [X+0x40]
008B4BEE  mov  rcx,r12                ; arena
008B4BF1  mov  r8,[r13 + 0x48]        ; count = [X+0x48]
008B4BFB  call 0x619d90
```

e, dentro de `0x619D90` (`checks/619d90.dis`):

```
00619DD6  mov  [r14+0x408],rax        ; len*4
00619DDD  mov  [r14+0x400],ebx        ; ebx = r8d = [X+0x48]
00619DE4  mov  [r14+0x404],edi        ; edi = r9d = [X+0x40]
```

Portanto: **`t1+0x400 = [X+0x48]`** (nº de arrays) e
**`t1+0x404 = [X+0x40]`** (n+1, floats por array), `t1+0x408 = 4·[X+0x40]`.

### 4.2 `0x8C1440` lê exatamente esses dois campos

```
008C1467  cmp  dword ptr [rdx + 0x400],2
008C146E  mov  rbx,r8
008C1471  mov  rsi,rdx
008C1474  jle  0x8c32ad               ; count <= 2 -> retorna sem fazer nada
008C14B0  mov  r15d,dword ptr [rdx + 0x404]   ; len = n+1
```

`0x8C0BD0` (detector) lê os mesmos offsets, mas de uma **cópia** de `t1`:

```
008B5E97  mov  r14d,8
008B5E9D  lea  rax,[rbp + 0x1460]     ; dst = cópia A
008B5EAB  lea  rcx,[rbp + 0xc40]      ; src = t1
008B5EB2  mov  edx,r14d               ; 8 x 0x80 = 0x400 B
008B5F10  lea  rax,[rax + 0x80]       ; laço
008B5F17  movups xmm0,[rcx] / 008B5F25 movups [rax - 0x80],xmm0
008B5F63  movups xmm0,[rcx]           ; rcx = t1+0x400
008B5F66  movups [rax],xmm0           ; cópia A +0x400 = t1+0x400
008B5FDE  lea  rax,[rbp + 0x1050]     ; dst = cópia B
008B5FE5  mov  rdx,r14
008B5FE8  lea  rcx,[rbp + 0xc40]      ; src = t1
008B6043  movups xmm0,[rcx] / 008B6059 movups [rax],xmm0   ; 0x1450 = t1+0x400
008B6046  mov  r8,[r13+0x10]
008B605C  call 0x8c0bd0               ; rcx = &[rbp+0x1050]
...
008C0BEF  cmp  dword ptr [rcx + 0x400],1
008C0C11  mov  edx,dword ptr [rcx + 0x404]
```

### 4.3 `t2+0x400/+0x404` são cópia de `t1+0x400/+0x404`

```
008B7DE8  mov  r14,[rbp + 0x4a60]
008B7DF8  mov  [rbp + 0x1870],r15     ; t2 lista de ponteiros
008B7E05  call 0x1798f42              ; memset(&t2+8, 0, 0x3F8)
008B7E0A  movsxd rdi,[rbp + 0x1044]   ; = t1+0x404
008B7E14  movsxd r9 ,[rbp + 0x1040]   ; = t1+0x400
008B7E1B  mov  rax,rdi / 008B7E1E shl rax,2
008B7E22  mov  [rbp + 0x1c70],r9d     ; t2+0x400 = t1+0x400
008B7E29  mov  [rbp + 0x1c74],edi     ; t2+0x404 = t1+0x404
008B7E2F  mov  [rbp + 0x1c78],rax     ; t2+0x408 = 4*(t1+0x404)
008B7E4D  mov  [rbp + r8*8 + 0x1870],rcx
```

`rbp+0x1040` = `t1+0x400` e `rbp+0x1044` = `t1+0x404`, porque `t1 = rbp+0xc40`
(`008B4BE3`, `008B6064`). Ou seja, o par **não é recalculado** para `t2`: é
propagado por cópia, com o mesmo layout (`memset` de `0x3F8` + `+0x400/+0x404/+0x408`).

### 4.4 `0x8AE6F0` reescreve o par em 4 sítios (com `n = [X+0x40]`)

`0x8AE6F0(src=rcx, dst=rdx, n=r8d)`:

```
008AE70A  mov  ebx,[rcx + 0x400]      ; count da origem
008AE716  lea  rcx,[rdx + 8]
008AE71F  mov  qword [rdx],0
008AE722  mov  r8d,0x3f8
008AE72A  call 0x1798f42              ; memset(dst+8,0,0x3F8)
008AE736  mov  [r15 + 0x408],rax      ; n*4
008AE740  mov  [r15 + 0x400],ebx      ; dst+0x400 = src+0x400
008AE747  mov  [r15 + 0x404],edi      ; dst+0x404 = n
```

Sítios no núcleo, todos com `r8 = [X+0x40]`:

| sítio | instruções | destino `dst` |
|---|---|---|
| `008B6457`/`008B645E` | `mov r8,[r13+0x40]`; `lea rdx,[rbp+0x2090]`; `mov rcx,r12`; `call 0x8ae6f0` | `[rbp+0x2090]` |
| `008B6593`/`008B65A4` | idem | `[rbp+0x2090]` |
| `008B83B9`/`008B83C0` | idem | `[rbp+0x2090]` |
| `008B84E2`/`008B84F0` | idem | `[rbp+0x2090]` |

Logo o par `+0x400/+0x404` de qualquer descritor desses 4 sítios tem
`+0x404 = [X+0x40]` e `+0x400 = [X+0x48]` herdado da origem `r12`
(`008B4BDE mov eax,[r12+0x18]` mostra que `r12` é o objeto de arena/cursor).

### 4.5 Cadeia final provada

```
X+0x48 (nº de arrays)  ─┐
X+0x40 (n+1 floats)    ─┴─> 0x619D90 (008B4BFB) ─> t1 (+0x400/+0x404/+0x408)
                                                        │
                        ┌───────────────────────────────┤
                        │                               │
              cópia 008B5F10..008B5F66            cópia 008B7E0A..008B7E2F
                        │                               │
                0x8C0BD0 (008B605C)                  t2 (008B80E4)
                 lê +0x400/+0x404                   0x8C1440 (008B80EE)
                        │
                0x8C1440 (008B606E)  lê +0x400 (008C1467) e +0x404 (008C14B0)
```

---

## 5. NÃO PROVADO

1. **`arg8` de `0x889BB0`** — nenhuma escrita em `[rsp+0x38]` entre
   `00881393` e `008813B9`. Parou em `008813B9`.
2. **`r9` da chamada a `0x8BA1B0` em `008ADF9B`** — não há `mov r9,…` no
   sítio; é herdado do ramo anterior. Parou em `008ADF9B`.
3. **Semântica interna** de `0x8B8E70`, `0x8B9E40`, `0x8BA1B0`, `0x8BA7B0`,
   `0x8BA8C0`, `0x8A1EE0`: só assinatura, posição e argumentos estão provados
   (§1.2). Parou nos prólogos.
4. **Identidade de `0x17978C0`** (sonda de pilha em `008AD2D3`, `008C145F`,
   `008C0BE7`, `0086FE??`). Parou em `008AD2D3`.
5. **Por que `<= 2`** em `008C1467`/`008C1474` (o corte exato de 2 arrays).
   Parou em `008C1474`.
6. **Identidade IPP exata** de `0x2F60` (`0x10D0`), `0x69C0` (`0x1250`) e
   `0x29B260` (`0x1C8530`): só a forma vetorial está provada (§2.4).
7. **`X+0x18`** (= arg9 de `0x86FE90`, `0086FF15`): nenhum consumidor
   localizado nesta etapa. Parou em `0086FF15`.
8. **`0x87F0C0`, `0x87BB60`, `0x87E220`, `0x87B2A0`, `0x87F780`, `0x878070`,
   `0x868F90`**: posição e argumentos provados; corpo não analisado.
9. **`0x8BFCB0`, `0x8BFD30`, `0x8BF5C0`** (usados com `rdx=&[rbp+0xc40]` /
   `&[rbp+0x1870]` em `008B4DD8`, `008B4DE7`, `008B452A`): não analisados.
   Parou em `008B4DD8`.
10. **`0x8AE650` / `0x8AE790`** só têm o layout do cabeçalho provado
    (`+0x80/+0x84/+0x88`); o resto do corpo não foi lido nesta etapa.
11. **Unidade de `[arg2+0x84]` (`00889BDA`) e `[X+0x60]` (`00889C0F`)** no
    contador `X+0x2C30`: o que está provado é que um é subtraído e o outro
    somado até o resultado ficar `>= 0`. Se a unidade é amostra, bloco ou
    frame, **NÃO PROVADO**. Parou em `00889BDA`.
12. **Consumidor do array `X+0x2BB8`**: existem leitores em `0x877D90`,
    `0x885040`, `0x8875F0`, `0x88AE20`, mas o corpo de nenhum deles foi lido
    nesta etapa. Parou em `00877D9F`.

