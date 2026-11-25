# Etapa O - saida, estereo e ring buffer (soothe3)

Fonte: `dumpsooth/nyx_soothe3_dump.bin`
SHA-256 verificada nesta sessao: `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`
Enderecos: RVAs (imagem base 0x180000000). Ponteiros de dado: VA base 0x199B0000 (RVA = VA - 0x199B0000).

Metodo: disassembly estatico com `tools/show_func.py` (chain-aware) e `tools/win2.py`;
despacho IPP resolvido pelas tabelas em `.data` (`[0x21C7408] = 4` -> indice 4).
Nada foi executado, hookado, patcheado ou injetado.

## 0. Resultado antecipado (o que fecha e o que nao fecha)

- A selecao entre `0x880640` e `0x881050` em `0x8774A0` e um teste de byte:
  `cmp byte ptr [rax],0` com `rax = [rcx]` (0x8774A6/0x8774AC/0x8774AF).
  Byte != 0 -> `0x880640` (e `*out` = 0 em 0x8774CC);
  byte == 0 -> `0x881050` (0x8774E6..0x87751C).
- `0x880640` e `0x881050` sao *wrappers* de descritores IPP: nao fazem soma nem ganho
  (zero instrucoes addss/mulss/subss/divss em ambos). A saida e escrita pelos calleos,
  nos buffers apontados pelos descritores montados na pilha.
- `0x880640` -> `0x885040` + `0x8875F0` (cadeia com 4 chamadas a 0x8B2680).
- `0x881050` -> `0x889BB0` + `0x88AE20` (cadeia sem 0x8B2680).
- `0x885040` e `0x8875F0` sao duas instancias quase identicas do mesmo processamento
  por canal; diferem apenas no estagio final (0x898A80 vs 0x8991E0).
- Rings: tres descritores de 0x90 bytes em `ctx+0x00`, `ctx+0x90`, `ctx+0x120`
  (0x8782FA, 0x87830D). Campos quentes: +0x80 (contadores write/read),
  +0x88 (comprimento), +0x8C (numero de canais). Comprimento = 0x10000
  (0x870790 e 0x873D5D).

---

## 1. Selecao em 0x8774A0 (0x8774A0..0x877527, 135 B)

Chamador direto unico: 0x86786B, dentro de 0x8677F0 (0x8677F0..0x867880).

```
008674... (fora do alvo)
0086780F  mov  rax,[rcx]                    ; param[0] = ponteiro do chamador
00867815  mov  [rbp+0x60],rax               ; param+0x00 = esse ponteiro
0086781C  lea  rax,[rbp+0x180]
00867823  mov  dword [rbp+0x180],0          ; flag local = 0
0086782D  mov  [rbp+0x68],rax               ; param+0x08 = &flag local
00867834  mov  rax,[rcx+8]
00867838  mov  [rbp+0x70],rax               ; param+0x10 = ctx (base)
00867850  mov  [rbp+0x78],rdx               ; param+0x18 = arg2
00867854  mov  [rbp+0x80],rbx               ; param+0x20 = arg3
0086785B  mov  [rbp+0x88],r9                ; param+0x28 = arg4
0086783C  mov  rax,[rbp+0x1a0]              ; arg5 de pilha
00867843  mov  [rbp+0x90],rax               ; param+0x30 = arg5
00867862  cmp  eax,4                        ; [0x26B1818] == 4 ?
00867867  lea  rcx,[rbp+0x60]
0086786B  call 0x8774A0
00867872  cmp  eax,1
00867877  lea  rcx,[rbp+0x60]
0086787B  call 0x881740                     ; modo 1: outra variante
```

Dentro de 0x8774A0:

```
008774A6  mov  rax,[rcx]          ; rax = param+0x00 (ponteiro)
008774AC  cmp  byte ptr [rax],0   ; TESTE: primeiro byte do objeto apontado
008774AF  je   0x8774E6          ; == 0 -> caminho 0x881050
; ---- caminho byte != 0 -> 0x880640 ----
008774B1  mov  rax,[rcx+8]        ; rax = param+0x08 (out int*)
008774B5  mov  rcx,[rcx+0x10]     ; ctx
008774B9  mov  r9,[rbx+0x28]      ; arg4
008774BD  add  rcx,0x5ED0         ; rcx = ctx+0x5ED0 (arg1 de 0x880640)
008774C4  mov  r8,[rbx+0x20]      ; arg3
008774C8  mov  rdx,[rbx+0x18]     ; arg2
008774CC  mov  dword ptr [rax],0  ; *out (param+0x08) = 0, antes de chamar
008774D2  mov  rax,[rbx+0x30]     ; arg5 de pilha
008774D6  mov  [rsp+0x20],rax
008774DB  call 0x880640
; ---- caminho byte == 0 -> 0x881050 ----
008774E6  mov  rcx,[rcx+0x10]
008774EA  add  rcx,0x5F8          ; rcx = ctx+0x5F8
008774F1  call 0x868730          ; eax = f(ctx+0x5F8)
008774F6  mov  rcx,[rbx+8]        ; out int*
00877506  mov  dword ptr [rcx],eax ; *out = f(ctx+0x5F8)
00877508  mov  rcx,[rbx+0x10]
00877510  add  rcx,0x5F8          ; rcx = ctx+0x5F8
0087751C  call 0x881050
```

Leitura do campo: o byte testado e `*(uint8_t*)param[0]`; `param[0]` vem de
`[arg1]` do chamador (0x86780F/0x867815). No unico chamador direto 0x8677F0 o
flag passado em `param+0x08` e um dword local zerado (0x867823), mas o byte
testado NAO e esse: e o objeto apontado por `param[0]`.

**NAO PROVADO**: quem escreve o byte `*(uint8_t*)[arg1]` para torna-lo != 0 no
chamador 0x8677F0. Ponto de parada: 0x86786B (unico xref direto de 0x8774A0).
Tambem nao foi provado o significado do modo `[0x26B1818]` (valor 4) alem do
despacho em 0x867862.

---

## 2. 0x880640 (0x880640..0x880AD9, 1177 B, 4 call, 0 float)

Chamadores: 0x8774DB (unico). Assinatura de fato (pela sequencia de uso):
`0x880640(ctx5ED0, arg2, arg3, arg4, arg5)`.

```
00880640  mov  [rsp+0x20],r9
00880645  mov  [rsp+0x18],r8
00880665  movsxd r14,[rcx+0x50]   ; r14 = ctx->0x50 (inteiro de controle)
00880675  mov  r10d,[rcx+0x48]    ; r10 = ctx->0x48 (inteiro de controle)
0088067C  mov  r11d,[rcx+0x2C90]  ; r11 = ctx->0x2C90 (segundo passo)
00880672  mov  r13,rdx            ; arg2 preservado
0088066B  mov  rbx,[rbp+0xA40]    ; arg5 (descritor/arena IPP)
0088068D  mov  eax,[rbx+0x18]     ; cursor de alocacao
...
```

O bloco 0x8806B0..0x880A46 apenas converte `n` valores em ponteiros de trabalho
com alinhamento de 16 bytes e grava de volta o cursor em `[rbx+0x18]`
(ex.: 0x8806CF and eax,0xF; 0x8806D5 add rdx,0x10; 0x8806DC cmove; 0x8806E3 mov [rbx+0x18],edx).
Sao duas listas de ponteiros:
- `[rbp + i*8 + 0x1B0]` (0x8806BE, 0x88070E) e
- `[rbp + i*8 + 0x5C0]` (0x88081A, 0x8808AD).

Chamada 1 (0x880A6C -> 0x885040):

```
00880A48  mov  [rsp+0x30],rbx      ; arg5 = arena
00880A4D  lea  rcx,[r15+0x2C50]    ; arg1 = ctx+0x2C50
00880A54  mov  [rsp+0x28],sil      ; modo = byte [[ctx]+0x51] (0x88092F)
00880A59  lea  r9,[rbp+0x90]      ; arg4
00880A60  mov  r8,r10              ; arg3 = [rbp+0xA30] (7o arg; r10 recarregado em 0x8808DA)
00880A63  mov  byte [rsp+0x20],0
00880A68  lea  rdx,[rbp-0x40]      ; arg2 = descritor local
00880A6C  call 0x885040
```

Chamada 2 (0x880AB9 -> 0x8875F0):

```
00880A75  lea  rax,[rbp+0x50]      ; arg stack = &[rbp+0x50]
00880A7D  lea  rcx,[r15+8]         ; arg1 = ctx+8
00880A85  lea  r9,[rbp+0x90]
00880A90  lea  r8,[rbp-0x40]
00880A98  mov  rdx,r13             ; arg2 = arg2 original
00880A9F  mov  [rsp+0x30],rbx
00880AA4  mov  [rsp+0x28],sil
00880AB4  mov  [rsp+0x20],rax
00880AB9  call 0x8875F0
```

Fim: restaura o cursor do alocador e retorna:

```
00880ABE  mov  eax,[rsp+0x50]      ; cursor salvo em 0x880690
00880AC2  mov  [rbx+0x18],eax
00880AC5  add  rsp,0xAD8
```

Constantes/limites observados em 0x880640: apenas inteiros de alinhamento
(0xF/0x10) e o `0x3F8` em 0x88073F/0x880861; nao ha constante float.
**Nao ha soma, copia direta nem ganho neste wrapper**: o efeito de saida esta
nos calleos.

---

## 3. 0x881050 (0x881050..0x881419, 969 B, 2 call, 0 float)

Chamador: 0x87751C (unico). Mesma construcao de descritores de 0x880640
(0x8810C0..0x881398; cursor em `[rbx+0x18]`, restaurado em 0x8813FE/0x881402).

```
00881075  movsxd r14,[rcx+0x50]
00881086  mov  r11d,[rcx+0x48]
0088108D  mov  edi,[rcx+0x2C90]
00881249  mov  r11,[rbp+0x560]     ; arg de contexto/pilha
00881398  mov  [rsp+0x30],rbx
0088139D  lea  rcx,[rsi+0x2C50]    ; arg1
008813A4  mov  [rsp+0x28],dil      ; modo = byte [[rsi]+0x51] (0x88128A)
008813A9  lea  r9,[rbp+0x60]
008813AD  mov  r8,r11
008813B0  mov  byte [rsp+0x20],0
008813B5  lea  rdx,[rbp-0x60]
008813B9  call 0x889BB0
008813C3  mov  [rsp+0x30],rbx
008813C8  lea  rax,[rbp+0x30]
008813D0  lea  rcx,[rsi+8]         ; arg1 = ctx+8
008813D4  mov  [rsp+0x28],dil
008813DD  lea  r9,[rbp+0x60]
008813E5  lea  r8,[rbp-0x60]
008813E9  mov  rdx,r12
008813F4  mov  [rsp+0x20],rax
008813F9  call 0x88AE20
008813FE  mov  eax,[rsp+0x4C]
00881402  mov  [rbx+0x18],eax
```

O `*out = f(ctx+0x5F8)` ocorre no chamador 0x8774E6..0x877506 (0x868730 chamado
em 0x8774F1, resultado gravado em 0x877506), **antes** de 0x881050. Portanto
0x881050 nao escreve esse int; ele consome o mesmo `ctx+0x5F8`.

---

## 4. 0x885040 (0x885040..0x8875E1, 9633 B) - cadeia do canal A

Assinatura usada por 0x880640: `(ctx2C50, desc, n, ptr, modo, arena)`.
Cadeia de chamadas (RVA de cada call):

```
0088517B  0x868C40        ; preparacao/inicializacao
00885278  0x10D0          ; IPP -> 0x2F60 (zero)
00885378  0x10D0          ; IPP -> 0x2F60 (zero)
0088539E  0x87BB60
008853B5  0x87E220
008853CF  0x87B2A0
008853FA  movss xmm2,[rdi+0x5C]   ; constante/parametro float do estado
00885621  movss [rsp+0x20],xmm2
00885627  0x87F0C0        ; computador de ganho (float)
008857F5  movss xmm6,[0x2079F9C]  ; 1.0f
008858DB  0x1250          ; IPP -> 0x69C0
0088592B  0x1C8530        ; ipp-dispatch direto
00885AC4  0x8981E0
00885B49  0x12E0          ; IPP -> 0x8FA0
00885CB0  0x1340          ; IPP -> 0x9BA0
00885CE9  0x1340
00885E80  0x1370          ; IPP -> 0xA120
00885EC9  0x1370
00885FC0  0x1340
00885FF9  0x1340
0088600E  0x87F780
0088692C  0x877530        ; analise/estado
00886A69  0x8B2680        ; 4x processamento escalar
00886BC9  0x8B2680
00886D69  0x8B2680
00886EE9  0x8B2680
00886FC6  0x10D0
00886FE3  0x8982C0
00887114  0x898300
00887127  0x8982C0
0088721B  0x898300
0088722E  0x8982C0
008872FA  0x86DF00
00887406  0x898A80        ; estagio final canal A
008874F0  0x10A0          ; IPP -> 0x2C80 (copia 32f)
00887539  0x10A0
```

A unica aritmetica float visivel no corpo e a leitura de `[rdi+0x5C]` (0x8853FA),
o `1.0f` (0x8857F5) e as chamadas 0x87F0C0 (0x885627) e 0x8B2680 (0x886A69 etc.).
`0x885040` em si nao contem addss/mulss/subss/divss.

**NAO PROVADO**: quais campos de `desc` (arg2) recebem a saida final e a formula
exata do ganho aplicado dentro de 0x87F0C0. Ponto de parada: 0x885627 e 0x898A80.

---

## 5. 0x8875F0 (0x8875F0..0x889BA1, 9649 B) - cadeia do canal B

Identica a 0x885040 ate 0x8898BA; muda o estagio final:

```
0088772B  0x868C40
00887BD7  0x87F0C0
00887DA5  movss xmm6,[0x2079F9C]  ; 1.0f
...
008899C6  0x8991E0        ; estagio final canal B (vs 0x898A80 em 0x885040)
00889AB0  0x10A0
00889AF9  0x10A0
```

`0x898A80` e `0x8991E0` sao clones de 1881 B: mesma sequencia de copias
(0x8B3DA0 em 0x898DC5 e 0x899525/0x899834), diferindo apenas no ultimo
callee: `0x8AB760` (0x899161, canal A) vs `0x8AC1D0` (0x8998C1, canal B);
estes por sua vez chamam `0x8ABAA0` (0x8ABA39) vs `0x8AC510` (0x8AC4A9).
Nao ha float nesses tres niveis (0 addss/mulss/divss).

Conclusao provada: **estereo = duas instancias paralelas do mesmo processamento,
uma por canal**; nao ha matriz mid/side nem soma L+R nesses niveis.

---

## 6. 0x8BAA10 (0x8BAA10..0x8BAB5D, 333 B, 0 float) - zerar planos

```
008BAA2F  mov  r8d,edx          ; arg2 = comprimento/canais
008BAA32  lea  rdx,[rbp-0x50]    ; saida do descritor de listas
008BAA36  call 0x86F480          ; preenche descritor (ponteiros + contagens)
008BAA8D  test eax,eax           ; eax = [rbp+0x30] (1a contagem)
008BAAA0  mov  rcx,[rbx]         ; buffer
008BAAA3  mov  edx,esi           ; [rbp+0x34] (comprimento)
008BAAA5  call 0x10D0            ; IPP -> 0x2F60: memset(buf,0,4*len)
...
008BAB23  test eax,eax           ; eax = contagem da 2a lista
008BAB30  mov  rcx,[rbx]
008BAB33  mov  edx,esi
008BAB35  call 0x10D0
```

Despacho IPP 0x10D0: `[0x21C5E08 + 4*8] = 0x199B2F60` -> RVA 0x2F60.
0x2F60: `shl edx,2` (0x2F71), `call 0x1D2E9E0` (0x2F7C, memset) => **zera floats**.
Efeito: 0x8BAA10 zera todos os planos de duas listas; nao aplica ganho.

---

## 7. 0x8BAB60 (0x8BAB60..0x8BACA8, 328 B, 0 float) - acumular com ganho

```
008BAB75  mov  r8d,[rdx+8]      ; comprimento
008BAB79  mov  r14,rdx           ; descritor
008BAB7C  lea  rdx,[rsp+0x40]    ; saida do descritor de listas
008BAB86  movaps xmm6,xmm2       ; xmm2 = ganho (float)
008BAB89  call 0x86F170          ; preenche listas
008BAB93  mov  rsi,[r14]         ; base de origem
...
008BABD8  call 0x11F0            ; dst[i] += src[i]*gain  (1a lista)
008BAC57  call 0x11F0            ; idem, 2a parte
008BAC7C  call 0x11F0            ; idem, 2a lista
008BAC1B  movsd xmm0,[rsp+0x68]
008BAC21  movsxd rcx,ebp         ; salto de ebp amostras
008BAC38  lea  rbp,[rax+rcx*4]   ; src2 = base + ebp*4
```

Despacho IPP 0x11F0: `[0x21C5FC8 + 4*8] = 0x199B5BC0` -> RVA 0x5BC0.
0x5BC0 e um `ippsAddProductC_32f`:
```
00005C40  vmovss   xmm0,[rcx+r10*4]        ; src
00005C46  vfmadd213ss xmm0,xmm1,[r8+r10*4] ; src*alpha + dst
00005C4C  vmovss   [r8+r10*4],xmm0         ; dst
```
com alpha em `xmm1` (passado de `xmm6` em 0x8BABD2/0x8BAC51/0x8BAC76).
Efeito: **overlap-add ponderado**: `dst[i] += src[i] * gain`. Sem float no wrapper.

---

## 8. Ring descriptors: +0x80 / +0x88 / +0x90 e comprimento 0x10000

`0x8688B0(desc, edx, r8d)` inicializa um descritor:

```
008688BF  mov  ebx,r8d
008688C2  mov  edi,edx
008688C4  mov  rsi,rcx
008688C7  call 0x868840
008688CC  mov  [rsi+0x88],ebx     ; +0x88 = comprimento do ring (amostras/canal)
008688D4  mov  [rsi+0x8C],edi     ; +0x8C = numero de canais
008688F1  movsxd rcx,[rbp]        ; rbp = &desc+0x88 -> rcx = comprimento
008688F5  shl  rcx,2              ; bytes = 4*len
0086890A  call qword [0x1D8D730]  ; operador new
00868930  mov  [rsi],rax          ; +0x00 = ponteiro do plano
```

`0x878200` inicializa TRES descritores contiguos de 0x90 bytes:

```
0087821B  xor  r15d,r15d           ; 0
0087825B  mov  [rcx+0x90],r15      ; desc1 = rcx+0x90
00878293  mov  [rcx+0x108],rax
0087829A  mov  [rcx+0x110],rax     ; desc1+0x80 (contadores)
008782A1  mov  [rcx+0x118],r15     ; desc1+0x88
008782A8  mov  [rcx+0x120],r15     ; desc2 = rcx+0x120
008782E0  mov  [rcx+0x198],rax
008782E7  mov  [rcx+0x1A0],rax     ; desc2+0x80
008782EE  mov  [rcx+0x1A8],r15     ; desc2+0x88
008782F5  call 0x8688B0            ; desc0 = rcx
008782FA  lea  rcx,[rbx+0x90]
00878306  call 0x8688B0            ; desc1
0087830D  lea  rcx,[rbx+0x120]
0087831C  call 0x8688B0            ; desc2
00878360  mov  [rbx+0x80],r15      ; desc0 contadores = 0
0087836F  cmp  [rbx+0x11C],r15d    ; desc1 canais
00878380  mov  edx,[rbx+0x118]     ; desc1 comprimento
00878386  call 0x10D0              ; zera plano
008783A0  mov  [rbx+0x110],r15     ; desc1 contadores = 0
008783AA  cmp  [rbx+0x1AC],r15d    ; desc2 canais
008783C0  mov  edx,[rbx+0x1A8]     ; desc2 comprimento
008783E8  mov  [rbx+0x1A0],r15     ; desc2 contadores = 0
```

Comprimento 0x10000: os dois chamadores de 0x878200 empilham literal 0x10000:

```
00870790  mov  dword [rsp+0x20],0x10000
00870798  mov  edx,r9d
0087079B  call 0x878200
...
00873D5D  mov  dword [rsp+0x20],0x10000
00873D65  mov  edx,r9d
00873D68  call 0x878200
```

com `r9d = [rdi+0x48]` (0x870782 / 0x873D4F), passado tambem como `r8d` e
`edx`. Em 0x878200, `edi = [rsp+0x60]` (0x87820D) e vai como `r8d` para
0x8688B0 (0x878301), logo **+0x88 = 0x10000** nos tres descritores.

Layout provado do descritor (base D, 0x90 bytes):
| offset | tipo | significado provado | RVA que prova |
|---|---|---|---|
| +0x00 | ptr | plano/canal 0 (array de ponteiros) | 0x868930, 0x878340 |
| +0x80 | dword | write index | 0x8AD26C |
| +0x84 | dword | read index | 0x8ACC66/0x8ACD06 |
| +0x88 | dword | comprimento (0x10000) | 0x8688CC, 0x870790 |
| +0x8C | dword | numero de canais | 0x8688D4 |

Logo, com S = base usada por 0x899940/0x8ACC40:
`S+0x90` = descritor A; `S+0x120` = descritor B; e os offsets quentes sao
`S+0x110` (= A+0x80), `S+0x118` (= A+0x88), `S+0x11C` (= A+0x8C);
`S+0x1A0` (= B+0x80), `S+0x1A8` (= B+0x88), `S+0x1AC` (= B+0x8C).

---

## 9. 0x899940 (0x899940..0x89A2AC, 2412 B, 8 call, 0 float)

Chamador direto: 0x88AE0F (fragmento .pdata 0x88AC75..0x88AE20, cauda de 0x889BB0).

Assinatura de fato (pela sequencia): `(S, descIn, descAux, descAux2, block,
countB, ..., outBase)`; os argumentos 5..9 vem da pilha ([rbp+0x160]..
[rbp+0x190]).

### 9.1 Mapa de call (todos os 8)

| RVA do call | alvo | efeito provado |
|---|---|---|
| 0x899C6F | 0x1798F36 | `memcpy` (thunk IAT 0x1D8D590) |
| 0x899CC5 | 0x8B3DA0 | copia planos do descritor para destino |
| 0x899D26 | 0x1798F36 | `memcpy` |
| 0x899F7F | 0x1798F36 | `memcpy` |
| 0x899FD5 | 0x8B3DA0 | copia planos (2a lista) |
| 0x89A02B | 0x1798F36 | `memcpy` |
| 0x89A06B | 0x8ACC40 | escreve no ring com overlap-add |
| 0x89A237 | 0x8AE790 | copia saida do ring para destino |

### 9.2 Fluxo real (ordem de instrucoes)

```
00899969  mov  rsi,[rbp+0x180]   ; limite de bloco
00899973  mov  ecx,[rdx+0x84]    ; campo de contagem do desc arg2
00899990  mov  edx,[rdx+0x80]    ; campo de offset do desc arg2
00899996  movsxd r8,[r8+0x80]    ; offset do desc arg3
0089999D  movsxd rbx,[rdi+0x80]  ; offset do desc arg4 (rdi=r9)
008999BE  lea  r14,[rax+0x120]   ; S+0x120 = desc B
008999CD  lea  r15,[rax+0x90]    ; S+0x90  = desc A
00899A08  cmp  ecx,esi
00899A17  cmovl r12d,ecx         ; n = min(disponivel, limite)
...
; monta lista de ponteiros com offset r13*4
00899B00  movdqu xmm0,[rax+rcx]
00899B13  paddq  xmm0,xmm2       ; + offset (pmovsxdq/psllq em 0x899ACE-0x899AD3)
00899B1B  movdqu [rcx-0x50],xmm0
...
; fase 1: uma copia por canal do desc A
00899C11  movsxd rax,[r15+0x8C] ; canais
00899C22  mov  edx,[r15+0x80]   ; posicao
00899C8C  lea  rcx,[rbp+0xD0]   ; destino (struct)
00899C96  lea  rdx,[rbp+0xC0]   ; origem (struct)
00899CC5  call 0x8B3DA0
...
; avanca o cursor do desc arg2
00899D2F  mov  ecx,[rdx+0x80]
00899D3E  add  ecx,esi
00899D40  dec  eax
00899D42  and  ecx,eax
00899D53  mov  [rdx+0x80],ecx
; fase 2: mesma copia, offset r13 (xmm6 = r13d em 0x899A0A/0x899DE6)
00899F21  movsxd rax,[r14+0x8C]
00899F32  mov  edx,[r14+0x80]
00899FD5  call 0x8B3DA0
...
; avanca desc B (S+0x120)
0089A034  mov  ecx,[rdx+0x80]
0089A040  add  ecx,esi
0089A049  dec  eax
0089A052  and  ecx,eax
0089A05B  mov  [rdx+0x80],ecx
; escrita no ring de saida
0089A061  mov  rdx,rsi          ; n
0089A064  mov  rcx,[rbp+0x160]  ; base do ring de saida
0089A06B  call 0x8ACC40
; copia do ring para a saida
0089A0EE  mov  rbx,[rbp+0x168]
0089A1D9  mov  r8d,[rbp+0x188]
0089A1E9  mov  rcx,[rbp+0x160]
0089A237  call 0x8AE790
0089A23F  add  r13d,esi         ; avanca bloco
0089A26C  cmp  r13d,[rbp-0x38]
0089A270  jl   0x899A00
```

### 9.3 Lei de estereo/sidechain

**NAO EXISTE formula de estereo em 0x899940.** O corpo inteiro nao tem
`addss/mulss/subss/divss` (0 ocorrencias); so inteiros, copias e `paddq` de
offset. O que ele faz e, por canal (`[desc+0x8C]`, 0x899C11/0x899F21), copiar
o plano correspondente do ring para a saida, sem qualquer peso L/R.

O unico peso numerico do caminho de saida esta em 0x8ACC40 (item 10):
`gain = (float)arg2/(float)arg3` (0x8AD0B9), **igual para todos os canais**
(loop unico em 0x8AD0E0 sobre `[rbp+0x5F0]` canais, 0x8AD0B3/0x8AD0BF).

Portanto: link, focus, mid/side e listen **NAO PROVADOS** no nivel de amostra.
Candidatos de controle (flags, nao matematica):
- byte `[[ctx]+0x51]` lido em 0x88092F (0x880640) e 0x88128A (0x881050);
- flags `ctx+0x2C40..0x2C45` alternadas por `xchg` em
  0x88AEAC..0x88AF17 (funcao 0x88AE20, chamada por 0x881050 em 0x8813F9).
Ponto de parada: 0x88AEAC (flags) e 0x87F0C0 (detector/ganho por banda).

---

## 10. 0x8ACC40 (0x8ACC40..0x8AD2A2, 1634 B, 10 call, 2 addss, 1 divss)

Chamadores: 0x895BB7 (fora deste escopo) e 0x89A06B (0x899940).
Recebe `rcx = base do ring de saida` (nao S de 0x899940), `rdx = n`,
`r8 = m`, `r9 = ptr de contexto`.

### 10.1 Guarda de espaco (ring de entrada em base+0x90)

```
008ACC5D  mov  eax,[rcx+0x110]     ; write index (desc A +0x80)
008ACC66  sub  eax,[rcx+0x114]     ; - read index (desc A +0x84)
008ACC6F  movsxd r10,eax
008ACC75  mov  eax,[rcx+0x118]     ; comprimento (desc A +0x88 = 0x10000)
008ACC7E  dec  eax
008ACC82  and  r10,rax             ; disponivel = (w-r) & (len-1)
008ACC85  cmp  r10,rdx
008ACC88  jb   0x8AD288            ; se disponivel < n -> retorna false
008AD288  xor  al,al
008AD28A  ... ret
```

### 10.2 Consumo dos dois rings de entrada

```
008ACC95  lea  rdx,[rcx+0x90]      ; desc A
008ACCF7  mov  ecx,[rdx+0x84]      ; read index A
008ACD00  mov  eax,[rdx+0x88]      ; comprimento A
008ACD06  add  ecx,esi             ; += n
008ACD08  dec  eax                 ; len-1
008ACD0A  and  ecx,eax
008ACD0E  mov  [rdx+0x84],ecx      ; read A = (read+n) & (len-1)
008ACD14  lea  rdx,[rbx+0x120]     ; desc B
008ACD5C  mov  ecx,[rdx+0x84]
008ACD65  mov  eax,[rdx+0x88]
008ACD6B  add  ecx,esi
008ACD6D  dec  eax
008ACD72  and  ecx,eax
008ACD79  mov  [rdx+0x84],ecx      ; read B = (read+n) & (len-1)
```

### 10.3 Aritmetica (unica) - ganho de overlap-add

```
008AD06B  test rsi,rsi
008AD070  cvtsi2ss xmm6,rsi        ; (float) rdx (arg2 = n)
008AD075  jmp  0x8AD08F
008AD086  cvtsi2ss xmm6,rcx        ; ALT: caminho negativo (u64->float)
008AD08B  addss  xmm6,xmm6         ; ALT: corrige bit alto
008AD092  test rdi,rdi
008AD097  cvtsi2ss xmm0,rdi        ; (float) r8 (arg3 = m)
008AD09C  jmp  0x8AD0B3
008AD0AA  cvtsi2ss xmm0,rax        ; ALT: caminho negativo
008AD0AF  addss  xmm0,xmm0         ; ALT: corrige bit alto
008AD0B9  divss  xmm6,xmm0         ; gain = (float)n / (float)m
```

Este `xmm6` e o alpha do overlap-add: em 0x8AD1F0 `movaps xmm2,xmm6` e
0x8AD21D `call 0x8BAB60`; 0x8BAB60 repassa em `xmm1` para 0x11F0 -> 0x5BC0
(`dst += src*alpha`, 0x5C46/0x5C4C).

### 10.4 Escrita no ring (zero + add-product + avanca write)

```
008AD049  call 0x8BAA10        ; zera planos (ippZero_32f)
008AD0B3  mov  ecx,[rbp+0x5F0] ; numero de canais
008AD0E0  loop por canal:
008AD21D    call 0x8BAB60      ; dst[i] += src[i]*gain
008AD26C  mov  ecx,[rbx+0x80]  ; write index do ring base+0x00
008AD272  mov  eax,[rbx+0x88]  ; comprimento
008AD278  add  ecx,esi         ; += n
008AD27A  dec  eax
008AD27C  and  ecx,eax
008AD27E  mov  al,1            ; retorna true
008AD280  mov  [rbx+0x80],ecx  ; write = (write+n) & (len-1)
```

### 10.5 Tamanho do ring

O comprimento nao e recalculado aqui: vem de `[desc+0x88]`, provado 0x10000
em 0x8688CC + 0x870790/0x873D5D (item 8). A mascara usada e `len-1`
(0x8ACC7E, 0x8ACD6D, 0x8AD27A), logo o ring e potencia de dois.

### 10.6 Offsets provados (base = arg1 de 0x8ACC40)

| offset | uso | RVA |
|---|---|---|
| +0x80 | write index do ring de saida | 0x8AD26C / 0x8AD280 |
| +0x88 | comprimento (0x10000) | 0x8AD272 / 0x8688CC |
| +0x90 | descritor de entrada A (base dos campos abaixo) | 0x8ACC95 |
| +0x110 | write index A (= +0x90+0x80) | 0x8ACC5D |
| +0x114 | read index A (= +0x90+0x84) | 0x8ACC66/0x8ACD0E |
| +0x118 | comprimento A (= +0x90+0x88) | 0x8ACC75 |
| +0x11C | canais A (= +0x90+0x8C) | 0x8ACC8E/0x8ACDDB |
| +0x120 | descritor de entrada B | 0x8ACD14 |
| +0x1A0 | write/read index B (= +0x120+0x80) | 0x8ACD5C |
| +0x1A8 | comprimento B (= +0x120+0x88) | 0x8ACD6D |
| +0x1AC | canais B (= +0x120+0x8C) | 0x8ACD81 |

Observacao: 0x8ACC40 le a disponibilidade em A, consome A e B e escreve no
descritor em `base+0x00` (write em +0x80). Sao, portanto, TRES descritores
de 0x90 bytes contiguos (base, base+0x90, base+0x120).

---

## 11. 0x885040 / 0x8875F0 / 0x8BAA10 / 0x8BAB60 - assinatura, buffers, efeito

| funcao | tamanho | assinatura provada | buffers | efeito provado |
|---|---|---|---|---|
| 0x885040 | 9633 B | `(ctx+0x2C50, desc, n, ptr, modo, arena)` (0x880A4D..0x880A6C) | desc/arena IPP; le float `[rdi+0x5C]` (0x8853FA) | cadeia por canal com detector 0x87F0C0, 4x 0x8B2680 e saida 0x898A80 (0x887406) |
| 0x8875F0 | 9649 B | idem, `ctx+0x8` (0x880A7D..0x880AB9) | idem | cadeia identica, saida 0x8991E0 (0x8899C6) |
| 0x8BAA10 | 333 B | `(rcx, edx=len, r8)` -> preenche listas via 0x86F480 (0x8BAA36) | listas de planos em `[rbp+0x30..]` e `[rbp+0xC4..]` | zera cada plano com 0x10D0 -> 0x2F60 (`memset 4*len`) |
| 0x8BAB60 | 328 B | `(src, desc(r8d=[rdx+8]), gain em xmm2)` (0x8BAB75/0x8BAB86) | `[rsp+0x40..]` listas; `[rdx]` base src | `dst += src*gain` via 0x11F0 -> 0x5BC0 (0x5C46/0x5C4C); 2a metade usa `src+ebp*4` (0x8BAC38) |

Detalhe 0x8B3DA0 (chamado por 0x899940): 301 B, `(dst, desc, len)`; copia
planos via 0x10A0 -> 0x2C80 (`memcpy`, 0x2D25/0x2D29). Chamadas:
0x8B3DBE (0x86F170), 0x8B3E0A/0x8B3E29/0x8B3E81/0x8B3EA9 (0x10A0). Nao aplica
ganho.

0x8AE790 (chamado por 0x89A237): 674 B, `(baseRing, desc, r8d)`; copia planos
do ring para a saida: 0x8AE87C/0x8AE8A5/0x8AEA00 `memcpy`, 0x8AE968 `0x86F170`,
0x8AE984/0x8AE9A3 `0x10A0` -> 0x2C80. Sem float.

---

## 12. Respostas explicitas

**(a) Onde termina o buffer de saida e como e escrito.**
O buffer de saida nao e escrito pelos wrappers 0x880640/0x881050. Em 0x881050
a saida e montada por 0x889BB0 (0x8813B9) + 0x88AE20 (0x8813F9); em 0x880640
por 0x885040 (0x880A6C) + 0x8875F0 (0x880AB9). A escrita final no ring ocorre
em 0x8ACC40: zero com 0x8BAA10 (0x8AD049) e `dst += src*gain` com 0x8BAB60
(0x8AD21D); o cursor de escrita e `[base+0x80]` avancado por
`(write+n)&(len-1)` em 0x8AD26C..0x8AD280. O consumo do ring e
0x8AE790 (0x89A237) / 0x8B3DA0 (0x899CC5/0x899FD5).

**(b) Lei de estereo, formula e RVA.**
Nao ha lei de estereo com ganho. 0x899940 e um roteador/copia por canal
(0 canais: `[desc+0x8C]` em 0x899C11/0x899F21) e nao contem
addss/mulss/subss/divss. O unico peso e o overlap-add comum a todos os canais:
`gain = (float)arg2/(float)arg3` (0x8AD0B9), aplicado em 0x8AD21D. Logo
link/focus/mid-side/listen: **NAO PROVADOS**; pontos de parada 0x88AEAC
(flags +0x2C40..0x2C45) e 0x87F0C0 (detector).

**(c) O ring/overlap-add usa os mesmos N/hop da FFT provada?**
O ring usa comprimento fixo 0x10000 (0x870790/0x873D5D -> 0x8688CC), com
mascara `len-1` (0x8ACC7E). O ganho usa `n/m` (0x8AD0B9), mas os valores de
`n` e `m` chegam de `[rbp+0x180]`/`[rbp+0x188]` em 0x89A061..0x89A06B e nao
foram resolvidos ate o chamador. **NAO PROVADO** que coincidam com o N/hop da
FFT. Ponto de parada: 0x89A061.

**(d) Ha atenuacao/limite de saida e qual constante?**
Nao foi encontrada constante de atenuacao/limite de saida em nenhuma das
funcoes desta etapa (0x880640, 0x881050, 0x899940, 0x8ACC40, 0x885040,
0x8875F0, 0x8BAA10, 0x8BAB60). O unico escalar float e o ganho `n/m`
(0x8AD0B9) e o `1.0f` em 0x2079F9C (0x8857F5/0x887DA5). Candidatos de clamp
em 0x87F0C0 (-0.7f em 0x207A698/0x87F249; 2.0f em 0x207A188/0x87F225;
1.19e-7 em 0x2079CF0/0x87F362) sao do detetor, **nao** prova de limite de saida.
Ponto de parada: 0x87F0C0.

---

## 13. NAO PROVADO (com RVA onde parou)

1. Quem seta != 0 o byte testado em 0x8774AC. Parada: 0x86786B (unico xref).
2. Significado de `[0x26B1818] == 4` (despacho para 0x8774A0). Parada: 0x867862.
3. Campos de `desc` que recebem a saida em 0x885040/0x8875F0. Parada: 0x885627
   e 0x8899C6.
4. Formula interna de 0x87F0C0 (detector/ganho). Parada: 0x87F0C0.
5. Lei de estereo (link/focus/mid/side/listen). Parada: 0x88AEAC (flags) e
   0x87F0C0.
6. Relacao `n/m` de 0x8AD0B9 com N/hop da FFT. Parada: 0x89A061.
7. Limite/atenuacao de saida. Parada: 0x87F0C0.
8. Valores de `[rbp+0x180]`, `[rbp+0x188]`, `[rbp+0x190]` no chamador de
   0x899940 (fragmento 0x88AC75 sem prologo proprio). Parada: 0x88AC75.

---

## 14. Tabela de constantes (RVA, bytes, valor)

Bytes lidos diretamente do dump; `RVA` e o endereco do dado ou da instrucao.

| RVA | bytes | valor | onde e usado |
|---|---|---|---|
| 0x870790 | `C7 44 24 20 00 00 01 00` | imediato `0x10000` (65536) | comprimento do ring, 0x870790 |
| 0x873D5D | `C7 44 24 20 00 00 01 00` | imediato `0x10000` | comprimento do ring, 0x873D5D |
| 0x88073F | `41 B8 F8 03 00 00` | imediato `0x3F8` (1016) | tamanho de bloco/descritor, 0x88073F |
| 0x880861 | `41 B8 F8 03 00 00` | imediato `0x3F8` | 0x880861 |
| 0x2079F9C | `00 00 80 3F` | `1.0f` (0x3F800000) | 0x8857F5, 0x887DA5, 0x8B272F |
| 0x207A188 | `00 00 00 40` | `2.0f` (0x40000000) | 0x87F225 |
| 0x207A698 | `33 33 33 BF` | `-0.7f` (0xBF333333) | 0x87F249 |
| 0x2079CF0 | `00 00 00 34` | `1.1920929e-07f` (0x34000000) | 0x87F362 |
| 0x2079FA0 | `7B 14 AE 47 E1 7A 84 3F` | `0.01` double (0x3F847AE147AE147B) | 0x87F1F4 |
| 0x207A118 | `AE 47 E1 7A 14 AE EF 3F` | `0.99` double (0x3FEFAE147AE147AE) | 0x87F206 |
| 0x21C5E28 | `80 2C 9B 19 00 00 00 00` | ponteiro `0x199B2C80` (RVA 0x2C80) | tabela de 0x10A0 (indice 4) |
| 0x21C5E68 | `60 2F 9B 19 00 00 00 00` | ponteiro `0x199B2F60` (RVA 0x2F60) | tabela de 0x10D0 (indice 4) |
| 0x21C5FE8 | `C0 5B 9B 19 00 00 00 00` | ponteiro `0x199B5BC0` (RVA 0x5BC0) | tabela de 0x11F0 (indice 4) |
| 0x1D8D590 | ponteiro IAT | `memcpy` (VCRUNTIME140) | 0x1798F36 |
| 0x1D8D580 | ponteiro IAT | `memset` (VCRUNTIME140) | 0x1798F42 |

Os valores `2.0f`, `-0.7f`, `0.01`, `0.99` pertencem a 0x87F0C0 (detector);
nao foram observados no estagio de saida e nao provam limite de saida.
