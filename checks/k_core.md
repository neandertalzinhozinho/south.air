# K — miolo aritmético do núcleo (`0x8B3ED0`) + `0x8C33D0` + satélites

Status: leitura estática, somente leitura. Nenhum hook/patch/injeção/escrita.
Arquivo gerado por blocos; blocos concluídos são anexados no fim.

## (a) Contexto e método

Fonte de verdade: `dumpsooth/nyx_soothe3_dump.bin`
SHA-256 `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`
(conferido nesta sessão com `Get-FileHash`).

Convenções:
- Endereços citados são RVAs (base de imagem `0x180000000`).
- Ponteiros de dado gravados no dump usam VA base `0x199B0000`;
  `RVA = VA - 0x199B0000`. Ex.: tabela de dispatch `0x199BAC20` → `RVA 0xAC20`.
- Toda linha de pseudocódigo leva o RVA da instrução entre colchetes.
- Constantes float são citadas por RVA e, quando útil, pelos bytes.
- `0x8B3ED0` é uma função só, chain-aware `0x8B3ED0..0x8B8DC1` (20.209 B).
  O `functions.csv` dá 49 B para ela — não foi usado.
- `winmm`/prim `powf`, `logf`, `expf` foram resolvidos por `checks/thunk_map.txt`
  (IAT + DLL) e conferidos no dump: o slot de IAT guarda o ponteiro de runtime.
  Observação: `tools/resolve_thunk.py` não acha esses slots porque o dump só preserva
  os 4 descritores de import de sistema (KERNEL32/USER32/ADVAPI32/SHELL32) em
  `RVA 0x79CF76C`; os thunks da CRT (`api-ms-win-crt-math-l1-1-0.dll`) têm slot em
  `0x1D8D7xx..0x1D8D8xx`, mas o descritor correspondente não está no dump.
  A prova usada é: (i) o slot de IAT em `0x1D8D818` contém um ponteiro de runtime
  válido (`0x7FFAE7A59F20`, lido do dump), e (ii) `checks/thunk_map.txt:309` nomeia
  `0x1C9AA01 -> IAT 0x1D8D818 powf`. O mesmo vale para `logf` (`0x1C9A9FB` →
  IAT `0x1D8D808`) e `expf` (`0x1C9A9D7` → IAT `0x1D8D7F0`).

Chamadores de `0x8B3ED0` (varredura `re_lib.callers`): `008ABDE6`, `008AC856`,
`008AD601`, `008AF401`.

### Primitivas de dispatch IPP usadas neste bloco (todas índice 4)

O padrão de stub é sempre:

```
movsxd rax, dword ptr [rip+disp]   ; índice de CPU
lea    r10, [rip+disp]             ; tabela de implementações
jmp    qword ptr [r10+rax*8]
```

O índice lido do dump é **4** em todos os stubs abaixo. Resolução (tabela → VA →
RVA → corpo):

| Stub | slot do índice | tabela | alvo VA | RVA do corpo | corpo |
|---|---|---|---:|---:|---|
| `0x1400` | `0x21C7408` = 4 | `0x21C6288` | `0x199BAC20` | `0xAC20` | wrapper SSE → `0x5F5C0` |
| `0x1C8500` | `0x21C7408` = 4 | `0x21C6AA8` | `0x19B78A00` | `0x1C8A00` | `mov rax,[0x21C70E8]; jmp rax` |
| `0x1C84A0` | `0x21C7408` = 4 | `0x21C6A28` | `0x19B78880` | `0x1C8880` | `mov rax,[0x21C6F08]; jmp rax` |
| `0x1C84D0` | `0x21C7408` = 4 | `0x21C6A68` | `0x19B78940` | `0x1C8940` | `mov rax,[0x21C6FF8]; jmp rax` |
| `0x1C8530` | `0x21C7408` = 4 | `0x21C6AE8` | `0x19B78AC0` | `0x1C8AC0` | `mov rax,[0x21C71D8]; jmp rax` |
| `0x1220` | `0x21C7408` = 4 | `0x21C6008` | `0x199B6160` | `0x6160` | `ippsMulC` in place |
| `0x13D0` | `0x21C7408` = 4 | `0x21C6248` | `0x199BAAA0` | `0xAAA0` | wrapper → `0x5F1A0` (`vmaxps`, ippsMax) |
| `0x1160` | `0x21C7408` = 4 | `0x21C5F08` | `0x199B46E0` | `0x46E0` | multiplica in place (memória) |
| `0x1250` | `0x21C7408` = 4 | `0x21C6048` | `0x199B69C0` | `0x69C0` | combina 2 buffers com escalar |
| `0x1100` | `0x21C7408` = 4 | `0x21C5E88` | `0x199B3480` | `0x3480` | buffer, r9d = modo (0/4) |
| `0x1340` | `0x21C7408` = 4 | `0x21C6188` | `0x199B9BA0` | `0x9BA0` | buffer (2 ponteiros) |

**`0x1400` resolvido:** o stub em `0x1400` é
`movsxd rax,[0x21C7408]` (índice 4), `lea r10,[0x21C6288]`, `jmp [r10+rax*8]`
→ `0x199BAC20` (RVA `0xAC20`). `0xAC20` valida `rcx`, `rdx`, `r9` ≠ 0 e `r8d > 0`
(`008AC28..008AC3A`; erro `-8`/`-6` em `008AC52`/`008AC3C`), e chama `0x5F5C0`.
`0x5F5C0` é, instrução a instrução, um **produto escalar**:
`vmulss` de `[r10+rax*4]` por `[rcx+rax*4]` acumulando em `xmm0`
(`0005F640`, `0005F646`, `0005F64E`; versão AVX2 com `vfmadd231ps` em
`0005F68D`/`0005F693`), e grava o resultado em `[r9]` (`0005F6F7 vmovss [r9],xmm0`).
Portanto a assinatura de `0x1400` é `(const float *a, const float *b, int n, float *out)`
com `n = r8d`, e o efeito é `*out = Σ_{i<n} a[i]*b[i]` (ordem de acumulação: a do corpo
acima, não uma reordenação livre).
A tabela `0x2077680` é **argumento**, não tabela de salto: `rdx=0x2077680` e
`r8d=0x20` são os dois primeiros argumentos de dados; a tabela de salto é
`0x21C6288` (correção ao texto de §23.15, que citava `0x2077680` como tabela de salto).

`0x1220` = `0x6160`: para cada amostra, `xmm1 = xmm0 * [rdx+i]`, grava de volta em
`[rdx+i]` (`00006200 vmulss`, `00006205 vmovss`). Isto é multiplicação **in place** por
escalar.

`0x13D0` = `0xAAA0` → `0x5F1A0`: `vmaxps` sobre o buffer (`0005F2C5`, `0005F2C7`,
`0005F2D5`) e store em `[r8]`; logo devolve o **máximo** das amostras (não |max|).

`0x86E780` (chamado em `008B5060`): itera `[rcx+0x400]` buffers, chama
`0x13D0(buffer_i, [rcx+0x404], &tmp)` (`0086E7C0..0086E7CB`), acumula com
`maxss` (`0086E7D9`) partindo de `-FLT_MAX` (`0x207A76C`, `0086E7A0`), e devolve
`xmm0 = max` (`0086E7EF`). Ou seja `M = max_i (max(buffer_i))`.

---

## (b) As cinco faixas de `0x8B3ED0`

### F1 — `0x8B5060..0x8B50B5` (ganho dB→linear a partir de `state+4`) + aplicação `0x8B5189..0x8B51CF`

Origem dos operandos de clamp (provada):
- `xmm13 = 0.0f` — `008B4DF4 xorps xmm13,xmm13`.
- `xmm11 = 1.0f` — `008B4FC7 movss xmm11,[0x2079F9C]` (bytes `0000803f`).
- `xmm10 = 0.05f` — `008B4FD0 movss xmm10,[0x2079D88]` (bytes `cdcc4c3d`).
- `xmm12 = 10.0f` — `008B506F movss xmm12,[0x207A360]` (bytes `00002041`).

```
; M = retorno de 0x86E780 (máximo por buffer, ver (a))
008B5060  call 0x86E780                    ; xmm0 = M
008B5065  rax = [r13+0x2C38]               ; state = *(void**)(engine+0x2C38)
008B506C  xmm6 = xmm0                      ; guarda M
008B506F  xmm12 = 10.0f
008B5078  xmm0 = xmm12                     ; base do powf
008B507C  eax = [state+4]                  ; dword; é o f32 "Detail" (índice 5)
008B507F  xmm1 = (float)eax                ; bits crus (dword) como f32
008B5083  xmm1 = maxss(xmm1, xmm13)        ; clamp inferior 0.0
008B5088  xmm1 = minss(xmm1, xmm11)        ; clamp superior 1.0
008B508D  xmm1 *= 20.0f                    ; [0x207A3B0]
008B5095  xmm1 -= 60.0f                    ; [0x207A474]  -> dB = 20*x-60
008B509D  xmm1 *= xmm10                    ; *0.05 = /20
008B50A2  call powf                        ; 0x1C9AA01; xmm0 = 10^(dB/20)
008B50A7  xmm7 = xmm0                      ; ganho linear
008B50AA  rax = &[rbp+0x24A0]              ; bloco de ponteiros destino
008B50B1  xmm7 *= xmm6                     ; g = 10^(0.05*(20*Detail-60)) * M
; ---- aplicação (por buffer) ----
008B5189  eax = [rbp+0x1040]               ; nº de buffers
008B5191  if (eax <= 0) goto 008B5546
008B5197  esi = [rbp+0x1044]               ; nº de amostras
008B519D  rbx = 0
008B51A2  rdx = [rbp+rbx+0x1050]           ; dst_i
008B51AA  xmm3 = xmm7                      ; escalar g
008B51AD  rcx = [rbp+rbx+0x24A0]           ; src_i
008B51B5  r8d = esi
008B51B8  [rsp+0x20] = 0
008B51BD  call 0x1250                      ; -> 0x69C0 (2 buffers + escalar)
008B51C2  rbx += 8 ; --edi ; loop
```

Conclusão F1: `state+4` entra cru como f32, é preso a `[0,1]`, convertido para dB
(`20*x-60`) e para linear (`10^(dB/20)`), e o resultado é multiplicado por `M`
(máximo medido). A conversão dB→linear é literalmente `powf(10, 0.05*(20x-60))`;
o `0.05` é `1/20`.

### F2 — `0x8B5343..0x8B53D4` (operação com tabela de 32 coeficientes) — loop `0x8B5390..0x8B5481`

```
008B5343  movups xmm0,[rcx]                ; fecha a cópia de blocos para [rbp+0x1050]
008B5346  rdx = &[rbp+0x10]
008B534A  rcx = &[rbp+0x1050]
008B5351  movups [rax],xmm0
008B5354  call 0x8C0230                    ; (não aberto nesta etapa)
008B5359  cmp [r13+0x48],0
008B5361  xmm12 = 10.0f
008B536A  if (<=0) goto 008B5490
008B5370  xmm1 = -0.4500000179f            ; [0x207A68C] bytes 6766e6be
008B5378  xmm0 = xmm12                     ; 10.0
008B537C  call powf                        ; w = 10^(-0.45)
008B5381  xmm7 = xmm0                      ; w
008B5384  r12 = &[rbp+0xc40]
; ---- loop por buffer (0x8B5390..0x8B5481) ----
008B5390  rcx = [r12]                      ; buffer_i
008B5394  r9  = &[rbp+0x4A38]              ; &out (float)
008B539B  r8d = 0x20                       ; n = 32
008B53A1  [rbp+0x4A38] = 0                 ; out = 0
008B53AB  rdx = 0x2077680                  ; tabela de coeficientes (32 f32)
008B53B2  call 0x1400                      ; P = Σ_{k<32} buffer[k]*coef[k]
008B53B7  xmm6 = [rbp+0x4A38]              ; P
008B53BF  rax = &[rbp+0x1050]
008B53C6  xmm6 *= xmm7                     ; P * 10^(-0.45)
008B53CA  rcx = &[rbp+0xc40]
008B53D1  rdx = rsi
; ---- cópia de 8 blocos de 0x80 B (008B53E0..008B5431) ----
008B5436  edx = [rbp+0x1040]               ; nº buffers
008B5443  esi = [rbp+0x1044]               ; nº amostras
008B5449  rbx = &[rbp+0x1050]
008B5452  rdx = [rbx]                      ; buffer_i
008B5458  xmm0 = xmm6                      ; g = P*w
008B545B  call 0x1160                      ; -> 0x46E0: buffer *= g (in place)
008B546A  ...
008B5473  ++r14d ; r12 += 8
008B547D  if (r14 < [r13+0x48]) goto 008B5390
```

A tabela `0x2077680` contém 32 f32 decrescentes
(`0.0479208529, 0.0478631295, 0.0476901010, … , 0.00235136482`);
`k=32..` já é a tabela seguinte (`0x2077700`: `0.999981046, …`). O `r8d=0x20`
fixa **32 taps**.

Conclusão F2: para cada buffer, `P = dot(buffer, coef[32])` por `0x1400`, e o buffer é
multiplicado por `P * 10^(-0.45)`. Não há normalização por `n`.

### F3 — `0x8B6549..0x8B665E` (8 buffers, `powf(state+4,4)`, par `0.25 / -0.25`)

```
008B6549  eax = [rbp+0x1860]               ; nº de buffers
008B654F  if (eax <= 0) goto 008B6582
008B6553  esi = [rbp+0x1864]               ; nº amostras
008B6559  rbx = 0
008B655C  edi = eax
008B6560  rdx = [rbp+rbx+0x1460]           ; dst_i
008B6568  r8d = esi
008B656B  rcx = [rbp+rbx+0x1050]           ; src_i
008B6573  call 0x1C8500                    ; -> 0x1C8A00 -> [0x21C70E8]=0x293760
008B6578  rbx += 8 ; --edi ; loop
008B6582  xmm1 = 4.0f                      ; [0x207A2B8] bytes 00008040
008B658A  xmm0 = xmm9                      ; xmm9 = [rsp+0x30] = state+4 (008B5B07)
008B658E  call powf                        ; powf(state+4, 4.0)
008B6593  r8 = [r13+0x40]
008B6597  rdx = &[rbp+0x2090]
008B659E  rcx = r12
008B65A1  xmm7 = xmm0                      ; p = powf(state+4,4)
008B65A4  call 0x8AE6F0                    ; retorna rax = bloco de buffers
008B65A9..008B6616  copia 8 × 0x80 B de rax para [rbp+0x1460]
008B6619  eax = [rbp+0x1860]
008B661F  if (eax <= 0) goto 008B85AF
008B6627  xmm7 *= 0.25f                    ; [0x2079E18] bytes 0000803e
008B662F  rbx = &[rbp+0x1460]
008B6636  edi = eax
008B6638  esi = [rbp+0x1864]
008B663E  xmm6 = -0.25f                    ; [0x207A67C] bytes 000080be
008B6646  xmm6 -= xmm7                     ; s = -0.25 - 0.25*p
008B6650  rdx = [rbx] ; r8d = esi
008B6656  xmm0 = xmm6
008B6659  call 0x1220                      ; buffer *= s (in place)
008B665E  rbx += 8 ; --edi ; loop
008B6668  jmp 008B85AF
```

Prova de que `xmm9 = state+4` em `008B658A`:
- prólogo grava `[state+4]` em `[rsp+0x30]` (`008B3FA9`/`008B3FAC`);
- `008B5B07 movss xmm9,dword ptr [rsp+0x30]`;
- `xmm9` é não-volátil em Win64 (xmm6–xmm15), e o prólogo salva xmm6..xmm13
  (`008B3F17..008B3F42`), então o valor sobrevive às chamadas intermediárias.

Prova do "8 buffers":
- `r14d = 8` em `008B6278` (e `008B5E97`, `008B5FD8`); o laço de cópia usa
  `rdx = r14` em `008B64D6`, portanto copia 8 blocos de 0x80 B.
- o laço de aplicação usa o contador `[rbp+0x1860]`, que é o nº de buffers
  (gravado em `008B768E mov [rbp+0x1860],esi`; `esi` = contagem de canais).

`0.25` e `-0.25` são literais em `.rdata` (`0x2079E18`, `0x207A67C`); não vêm de
`state`. A fórmula executada é `s = -0.25 - 0.25*powf(state+4, 4.0)`.

Nota sobre `0x1C8500`: o stub resolve para `0x1C8A00`, que é
`mov rax,[0x21C70E8]; jmp rax` e o qword em `0x21C70E8` vale `0x19C43760`
(RVA `0x293760`). O corpo em `0x293760` é a implementação vetorial (0x293760,
`.pdata` chain; `0x1c8a00.dis` existe em `checks/`). O nome/semântica dessa
primitiva **não** está provado por nome; a única coisa provada é a assinatura
`(rcx=src, rdx=dst, r8d=n)` e que o laço de F3 a chama 1× por buffer.

### F4 — `0x8B77F0..0x8B7B4D` (curva com `logf`/`expf` sobre `state+4`)

```
008B77F0  edi = esi                        ; contador (nº buffers)
008B77F2  rdx = [rbp+rbx+0x34E0]           ; dst_i
008B77FA  r8d = r14d
008B77FD  rcx = [rbp+rbx+0x4520]           ; src_i
008B7805  call 0x1C8500                    ; -> 0x293760 (mesma primitiva de F3)
008B780A  rbx += 8 ; --edi ; loop
008B7814  edi = 8
; ---- monta bloco de ponteiros [rbp+0x2CC0] e [rbp+0x30D0] ----
008B75BD  xmm10 = [rsp+0x30]               ; x = state+4  (recarregado aqui)
008B7AFC  xmm0 = 2.0f                      ; [0x207A188] bytes 00000040
008B7B04  xmm10 *= xmm10                   ; x^2
008B7B09  xmm0 -= xmm10                    ; 2 - x^2
008B7B0E  xmm0 += 0.3330000043f            ; [0x2079E54] bytes fa7eaa3e
008B7B16  call 0x1C9A9FB                   ; logf(2 - x^2 + 0.333...)
008B7B1B  xmm0 -= -1.099612832f            ; [0x207A6AC] -> +1.099612832
008B7B23  xmm1 = [rbp-0x10]                ; state+0
008B7B28  xmm1 = maxss(xmm1, xmm13)        ; clamp 0
008B7B2D  xmm1 = minss(xmm1, xmm11)        ; clamp 1
008B7B32  xmm0 *= xmm1                     ; * clamp(state+0,0,1)
008B7B36  xmm0 -= 1.099612832f             ; [0x2079FC0] bytes 1dc08c3f
008B7B3E  call 0x1C9A9D7                   ; expf
008B7B43  xmm7 = xmm0
008B7B46  rax = &[rbp+0x24A0]
008B7B4D  xmm7 -= 0.3330000043f            ; [0x2079E54]
; ---- aplicação ----
008B7BBD  rdi = &[rbp+0x24A0]
008B7BC4  r14d = esi                       ; nº buffers
008B7BD0  rdx = [rdi] ; r8d = ebx
008B7BD6  xmm0 = xmm7
008B7BD9  call 0x1220                      ; buffer *= curva (in place)
008B7BDE  rdi += 8 ; --r14 ; loop
```

Forma fechada (nomeada por RVA, sem batismo):
```
x = state+4            (f32 cru)
y = exp( clamp(state+0,0,1) * ( ln(2 - x*x + 0.3330000043) + 1.099612832 ) - 1.099612832 )
      - 0.3330000043
```
O `logf` é `0x1C9A9FB` (IAT `0x1D8D808`), `expf` é `0x1C9A9D7`
(IAT `0x1D8D7F0`). Não há nome de curva no binário; fica "curva de
`0x8B7AF0..0x8B7B4D`".

### F5 — `0x8B84B0..0x8B86D0` (`ln` em 8 buffers + gate `[rbp+0x4A20]` + dois `logf(powf(10,·))`)

```
008B84A9  eax = [rbp+0x1860]               ; nº buffers
008B84B1  if (eax <= 0) goto 008B84E2
008B84B3  esi = [rbp+0x1864]               ; nº amostras
008B84C0  rdx = [rbp+rbx+0x1460]           ; dst_i
008B84C8  r8d = esi
008B84CB  rcx = [rbp+rbx+0x2090]           ; src_i
008B84D3  call 0x1C8500                    ; -> 0x293760
008B84D8  rbx += 8 ; --edi ; loop
008B84E2  r8 = [r13+0x40]
008B84E6  rdx = &[rbp+0x2090]
008B84ED  rcx = r12
008B84F0  call 0x8AE6F0                    ; rax = bloco de buffers
008B84F5..008B8557  copia 8 × 0x80 B de rax para [rbp+0x1460]
008B855A  eax = [rbp+0x1860]
008B8562  if (eax <= 0) goto 008B8599
008B8564  esi = [rbp+0x1864]
008B856A  rbx = &[rbp+0x1460]
008B8580  rdx = [rbx] ; r8d = esi
008B8586  xmm0 = xmm8                      ; xmm8 = -1.0 (008B7A23, 0x207A6A8)
008B858A  call 0x1220                      ; buffer *= -1.0
008B858F  rbx += 8 ; --edi ; loop
008B8599  eax = [rbp-8]
008B859C  xmm12 = 10.0f                    ; [0x207A360]
008B85A5  [r14+0x18] = eax
008B85A9  r14d = 8
; ---- gate ----
008B85AF  if (byte[rbp+0x4A20] == 0) goto 008B8690
008B85F8  call 0x8BFCB0(rcx=r13, rdx=r12)
008B8603  call 0x8BFD30(rcx=r13, rdx=r12)
008B8608..008B8681  copia r12 -> [rbp+0x2090] (8 × 0x80 B)
008B8676  r9 = [r13+0x10]
008B867A  rdx = [r13+0x2C38]               ; state
008B8684  rcx = &[rbp+0x2090]
008B868B  call 0x8C3F10
; ---- dois log(pow(10,·)) ----
008B8690  xmm1 = -3.0f                     ; [0x207A6E4] bytes 000040c0
008B8698  xmm0 = xmm12                     ; 10.0
008B869C  call powf                        ; 10^(-3)
008B86A1  call 0x1C9A9FB                   ; logf(10^-3) = -6.907755...
008B86A6  xmm1 = [rsp+0x40]                ; state+0x4C
008B86AF  xmm1 *= -0.0500000007f           ; [0x207A66C] bytes cdcc4cbd
008B86B7  xmm0 = xmm12                     ; 10.0
008B86BB  call powf                        ; 10^(-0.05*state[0x4C])
008B86C0  call 0x1C9A9FB                   ; logf(...)
008B86C5  cmp [r13+0x48],0
008B86CA  xmm6 = xmm0
008B86CD  xmm12 = [rsp+0x4A60]
```

Prova do gate `byte[rbp+0x4A20]`:
- é escrito no prólogo: `008B3FC1 mov rax,[r13+0x48]`; `008B3FCC cmp qword [r13+0x48],2`;
  `008B3FD1 seta byte [rbp+0x4A20]`. Logo `gate = ([engine+0x48] > 2)` (unsigned).
- o mesmo gate é reusado em `008B4DC5 cmp byte [rbp+0x4A20],0` antes de
  `0x8BFCB0`/`0x8BFD30` (`008B4DD8`/`008B4DE7`).
- aqui, se `gate`, roda `0x8BFCB0` (`008B85F8`), `0x8BFD30` (`008B8603`) e
  `0x8C3F10` (`008B868B`); se não, salta direto para `008B8690`.

O trecho `logf(powf(10,-3))` e `logf(powf(10,-0.05*state[0x4C]))` é redundante em
matemática (`log(10^(x)) = x*ln(10)`), mas é assim que está emitido: dois `powf`
e dois `logf` reais, ordem `powf`→`logf` em `008B869C`→`008B86A1` e
`008B86BB`→`008B86C0`.

## (c) Tabela de constantes usadas neste bloco

| RVA | bytes (32-bit) | f32 | usada em |
|---|---|---|---|
| `0x2079F9C` | `00 00 80 3F` | 1.0 | `008B4FC7` (xmm11), `008B7B2D` (clamp) |
| `0x2079D88` | `CD CC 4C 3D` | 0.05000000074505806 | `008B4FD0` (xmm10, F1) |
| `0x207A360` | `00 00 20 41` | 10.0 | `008B506F`, `008B5361`, `008B859C`, `008B8698`, `008B86B7` |
| `0x207A3B0` | `00 00 A0 41` | 20.0 | `008B508D` |
| `0x207A474` | `00 00 70 42` | 60.0 | `008B5095` |
| `0x207A68C` | `67 66 E6 BE` | -0.45000001788139343 | `008B5370` |
| `0x2079E18` | `00 00 80 3E` | 0.25 | `008B6627` |
| `0x207A67C` | `00 00 80 BE` | -0.25 | `008B663E` |
| `0x207A2B8` | `00 00 80 40` | 4.0 | `008B6582` |
| `0x207A188` | `00 00 00 40` | 2.0 | `008B7AFC` |
| `0x2079E54` | `FA 7E AA 3E` | 0.33300000429153442 | `008B7B0E`, `008B7B4D` |
| `0x207A6AC` | `1D C0 8C BF` | -1.099612832069397 | `008B7B1B` |
| `0x2079FC0` | `1D C0 8C 3F` | +1.099612832069397 | `008B7B36` |
| `0x207A6E4` | `00 00 40 C0` | -3.0 | `008B8690` (expoente do 1º `powf`) |
| `0x207A66C` | `CD CC 4C BD` | -0.05000000074505806 | `008B86AF` |
| `0x207A76C` | `FF FF 7F FF` | -3.4028234663852886e38 | `0086E7A0` (`-FLT_MAX`) |
| `0x2079E08` | `48 AF BC 9A F2 D7 7A 3E` | f64 1e-7 | `008B4E0D` (denominador do laço de média) |
| `0x2079F48` | `FC A9 F1 D2 4D 62 50 3F` | f64 0.001 | `008B4E16`, comparado em `008B4F93` |
| `0x207BAE0` | `FF FF FF 7F FF FF FF 7F` | máscara `0x7FFFFFFF`×2 | `008B4DFE` (andps = |·|) |
| `0x207A6A8` | `00 00 80 BF` | -1.0 | `008B7A23` (xmm8, usado em F5 `008B8586`) |
| `0x2077680` | `A8 48 44 3D …` | 32 f32, 1º = 0.047920852899551392 | argumento de dados de `0x1400` em `008B53AB` |

Constantes auxiliares do bloco de ganho escalar (`0x8B5B..`, fora das 5 faixas, só
para não confundir): `0x2079EA8=0.5`, `0x2079F38=0.8`, `0x207A2D8=5.0`,
`0x207A00C=1.38629436`, `0x207A1E8=2.4`, `0x2079DB0=0.1`, `0x207A6D4=-2.30258512`,
`0x207A1D0=+2.30258512`, `0x207A734=-24.0`, `0x2079CEC=1e-7`.

## (d) Offsets de struct provados neste bloco

`engine = r13` (prólogo `008B3F14 mov r13,rcx`); `state = *(void**)(engine+0x2C38)`
(`008B5065`, `008B3F5C`).

| Objeto | Offset | Tipo | Provado em |
|---|---:|---|---|
| `state` | `+0x00` | f32 | `008B3F82/84` → `[rbp-0x10]`; usado em F4 (`008B7B23`) |
| `state` | `+0x04` | f32 (dword cru) | `008B3FA9/AC` → `[rsp+0x30]`; F1 `008B507C`, F3 `008B5B07`, F4 `008B75BD` |
| `state` | `+0x28` | f32 | `008B3F9C/9F` → `[rbp]` |
| `state` | `+0x3C` | f32 | `008B3FB7/BA` → `[rbp+8]` |
| `state` | `+0x4C` | f32 | `008B3F8E/91` → `[rsp+0x40]`; F5 `008B86A6` |
| `state` | `+0x52` | u8 | `008B3F71/75` → `[rbp+0x4A30]` |

`state+4` é o **índice 5** da tabela de parâmetros:
- o dispatcher de `0x867D80` lê o índice em `[rsi]` e faz
  `movzx eax, byte [r11+rax+0x8683CC]` / `mov ecx, dword [r11+rax*4+0x868348]` /
  `add rcx,r11` / `jmp rcx` (`00867E50..00867E86`, com `r11=0`);
- lendo essas tabelas no dump: índice 5 → byte 5 → alvo `0x867F7B`;
- `0x867F7B movd eax,xmm8` / `0x867F80 xchg dword [rbx+0x58],eax`;
- `state = engine+0x54` (G/§8.3), logo `rbx+0x58 = state+0x04`.

Outros offsets de `engine` provados: `+0x40` (contagem/ponteiro de canais, lido em
`008B4CA0`, `008B6593`, `008B84E2`), `+0x48` (nº de buffers; `008B3FC1`, `008B5359`,
`008B547D`, `008B86C5`), `+0x10` (`008B8676`), `+0x2C38` (ptr `state`).

Blocos de ponteiros de 0x400 B (128 ponteiros; `count/len` em `+0x400/+0x404`, lidos
por `0x86E780`): bases `rbp+0x0C40`, `+0x1050`, `+0x1460`, `+0x2090`, `+0x24A0`,
`+0x2CC0`, `+0x30D0`, `+0x34E0`, `+0x38F0`, `+0x3D00`, `+0x4110`, `+0x4520`.
Contadores em `rbp+0x1040` (nº buffers), `rbp+0x1044` (nº amostras),
`rbp+0x1860` (nº buffers), `rbp+0x1864` (nº amostras).

## (e) Respostas explícitas

1. **F1 — origem dos clamps e campo de estado.**
   `xmm13=0.0f` (`008B4DF4 xorps`), `xmm11=1.0f` (`008B4FC7`, `0x2079F9C`),
   `xmm10=0.05f` (`008B4FD0`, `0x2079D88`). O campo é `state+4` (dword lido cru em
   `008B507C`), provado como índice 5 por `0x8683CC/0x868348` → `0x867F7B` →
   `[rbx+0x58]` (`state=engine+0x54`). A conversão é dB→linear porque o expoente é
   `0.05*(20*x-60)` e a base é `10`: `10^(dB/20)`, `dB = 20*x-60`.

2. **F2 — primitiva `0x1400`.**
   Stub em `0x1400` = dispatcher IPP (índice 4 em `0x21C7408`, tabela `0x21C6288`),
   alvo `0x199BAC20`/RVA `0xAC20`, que chama `0x5F5C0`. `0x5F5C0` é produto escalar
   (`vmulss`/`vaddss` em `0005F640/646/64E`, FMA em `0005F68D/693`, store em
   `0005F6F7`). Assinatura `(a,b,n,out)`, `out=Σ a[i]*b[i]`; aqui `n=0x20=32`.
   A tabela `0x2077680` é o **vetor de coeficientes**, não a tabela de salto
   (esta é `0x21C6288`). Correção registrada.

3. **F3 — por que 8 buffers e de onde vem 0.25/-0.25.**
   8 = `r14d=8` em `008B6278` (também `008B5E97`, `008B5FD8`), usado como contador
   das cópias de 0x80 B em `008B64D6`. `0.25`/`-0.25` são literais de `.rdata`
   (`0x2079E18`/`0x207A67C`), não vêm de estado. Resultado:
   `s = -0.25 - 0.25*powf(state+4,4.0)`, aplicado multiplicando cada buffer
   (`008B6627`→`008B6659`).

4. **F4 — a curva.**
   `y = exp( clamp(state+0,0,1) * (ln(2 - x^2 + 0.3330000043) + 1.099612832)
   - 1.099612832 ) - 0.3330000043`, com `x = state+4` (`008B7AFC..008B7B4D`).

5. **F5 — o gate.**
   `byte[rbp+0x4A20] = ([engine+0x48] > 2)` (`008B3FCC/008B3FD1`). Se verdadeiro,
   roda `0x8BFCB0` (`008B85F8`), `0x8BFD30` (`008B8603`) e `0x8C3F10` (`008B868B`);
   se falso, pula para `008B8690`. Não é um flag de estado: é derivado da contagem
   de canais/buffers.

## (f) NÃO PROVADO / NÃO EXTRAÍDO (deste bloco)

- **Semântica nominal de `0x293760`** (alvo de `0x1C8500`, usado em F3 `008B6573`,
  F4 `008B7805`, F5 `008B84D3`): assinatura `(src,dst,n)` provada; nome e algoritmo
  (`ln`? outra primitiva vetorial) **NÃO PROVADOS**. A cadeia para em `008B7805` /
  `008B6573` / `008B84D3`; o ponteiro de implementação está em `0x21C70E8` →
  `0x19C43760` (RVA `0x293760`).
- **Semântica nominal de `0x1C84A0`, `0x1C84D0`, `0x1C8530`, `0x1100`, `0x1250`,
  `0x1340`**: só a assinatura/argumentos foram lidos; o efeito exato de `0x1250`
  (`0x69C0`) e `0x1100` (`0x3480`) **NÃO PROVADO**.
- **`0x8C0230`** (chamado em `008B5354`, dentro de F2): não aberto nesta etapa.
- **`0x86E780`**: a semântica de "máximo" está provada pelo corpo
  (`0086E7C0..0086E7EF` + `0x13D0`→`0x5F1A0`); o **layout exato** do objeto em
  `rcx` (por que `+0x400` é contagem e `+0x404` é comprimento) **NÃO PROVADO**.

---

## (b6) `0x8C33D0` — transcrição instrução a instrução (2.128 B chain-aware)

Chamadores (`re_lib.callers`): `008B6A7E` (dentro de `0x8B3ED0`) e `008C87EE`.

Assinatura observada no prólogo: `rcx = A` (`008C3426 mov r13,rcx`),
`rdx = B` (`008C3419 mov rbx,rdx`), `xmm2` (`008C341F movaps xmm7,xmm2`),
`xmm3` (`008C341C movaps xmm6,xmm3`), 6º argumento na pilha
`r15 = [rbp+0xFF0]` (`008C33F5`). `r14d = 8` (`008C340B`).

### Bloco 1 — cópia de B (0x410 B) para `[rbp+0x340]` e zero de `[rbp+0x750]`

```
008C33D0  [rsp+0x18] = rbx
008C33D5..008C33DE  push rbp/rsi/rdi/r12/r13/r14/r15
008C33E0  rbp = rsp - 0xF90
008C33E8  eax = 0x1090
008C33ED  call 0x17978C0                  ; alloca/chkstk
008C33F2  rsp -= rax
008C33F5  r15 = [rbp+0xFF0]               ; 6º argumento (descritor/alocador)
008C33FC  r8 = &[rbp+0x340]
008C3403  [rsp+0x1080] = xmm6             ; salva xmm6
008C340B  r14d = 8
008C3411  [rsp+0x1070] = xmm7             ; salva xmm7
008C3419  rbx = rdx                       ; B
008C341C  xmm6 = xmm3
008C341F  xmm7 = xmm2
008C3422  eax = [r15+0x18]                ; cursor do alocador
008C3426  r13 = rcx                       ; A
008C3429  [rbp+0xFD8] = eax               ; guarda cursor
008C342F  rax = rdx                       ; fonte = B
008C3432  edx = 8
008C3440  r8 += 0x80
008C3447..008C3490  copia 0x80 B de [rax] para [r8-0x80] (8 chunks de 16 B)
008C3495  --edx ; jne 008C3440            ; 8 iterações => 0x400 B
008C349B  xmm0 = [rax]                    ; 16 B de cauda de B (= B+0x400)
008C349E  edi = 0
008C34A0  rcx = &[rbp+0x758]
008C34A7  [rbp+0x750] = 0                 ; 1º ponteiro do bloco de trabalho = NULL
008C34AE  [r8] = xmm0                     ; r8 = 0x340+0x400 = 0x740
008C34B2  r8d = 0x3F8
008C34B8  call 0x1798F42                  ; memset(&[rbp+0x758], 0, 0x3F8)
                                          ; cobre [0x758, 0xB50); NÃO cobre 0x740/0x744
```

**Resposta a `008C34BD`/`008C34C7` (leitura antes da escrita): NÃO ocorre.**
`008C34AE` grava 16 B em `[rbp+0x740]` (a cauda de B copiada em `008C349B`),
e só depois `008C34BD` lê `[rbp+0x744]` e `008C34C7` lê `[rbp+0x740]`:

```
008C34BD  movsxd rsi, dword ptr [rbp+0x744]   ; len  (escrito em 008C34AE)
008C34C4  r8d = edi                            ; edi = 0
008C34C7  movsxd r12, dword ptr [rbp+0x740]    ; count (escrito em 008C34AE)
008C34CE  rax = rsi
008C34D1  rax <<= 2                            ; len*4
008C34D5  [rbp+0xB50] = r12d                   ; count
008C34DC  [rbp+0xB54] = esi                    ; len
008C34E2  [rbp+0xB58] = rax                    ; len*4
008C34E9  if (r12d <= 0) goto 008C353A
; ---- aloca count ponteiros no descritor r15 ----
008C34EE  edx = [r15+0x18]                     ; cursor
008C34F2  rax = [r15]                          ; base
008C34F5  rcx = (int64)edx
008C34F8  rcx = rax + rcx*4
008C34FC  eax = edx + esi                      ; cursor + len
008C34FF  [rbp+r8*8+0x750] = rcx               ; ptr[i]
008C3507..008C351D  alinha eax a 16
008C3521  ++r8
008C3524  [r15+0x18] = edx                     ; novo cursor
008C3528  if (r8 < r12) goto 008C34F2
```

### Bloco 2 — cópia de A (0x90 B) para a pilha e de B (0x410 B) para `[rbp+0xB60]`

```
008C353A..008C3599  copia [r13+0x00..0x8F] para [rsp+0x30..0x7F] e [rbp-0x80..-0x50]
                     (16 B por movaps; offsets 0x00,0x10,...,0x80)
008C354B  rcx = r14 (=8)
008C35A0..008C35E9  copia 8 × 0x80 B de [rbx] (=B) para [rbp+0xB60]
008C35F3  xmm0 = [rbx] ; [rax] = xmm0        ; cauda de B em [rbp+0xB60+0x400]
```

### Bloco 3 — diferença `B - A` via `0x11C0` (condicional em `xmm2`)

```
008C3669  eax = (int)bits(xmm2)               ; movd eax,xmm2
008C366D  if (r12d != eax) goto 008C36A9      ; r12 = count
008C3672  if (r12d <= 0) goto 008C36EB
008C3680  r8  = [rbp+rbx+0x340]               ; B_i
008C3688  r9d = esi                           ; len
008C368B  rdx = [rbp+rbx+0xB60]               ; B'_i
008C3693  rcx = [rsp+rbx+0x30]                ; A_i
008C3698  call 0x11C0                         ; -> 0x50E0
008C369D  rbx += 8 ; --r14 ; loop
008C36A9  if (eax != 1) goto 008C36EB
008C36B3  r15 = [rsp+0x30]                    ; A_0 (fixo)
008C36C0  r8  = [rbp+rbx+0x340]
008C36CB  rdx = [rbp+rbx+0xB60]
008C36D3  rcx = r15
008C36D6  call 0x11C0
```

`0x11C0` → `0x50E0`: o corpo faz `vmovss xmm0,[rbp+rax*4]`;
`vsubss xmm1,xmm0,[rcx+rax*4]`; `vmovss [r8+rax*4],xmm1`
(`00005180/5186/518B`; versão `vsubps` em `000051AC/51B1`). Logo
`out[i] = rdx[i] - rcx[i]` (`rbp=rdx` em `000050E7`). Aqui
`out = [rbp+0x340]`, `rdx = [rbp+0xB60]`, `rcx = A`.

### Bloco 4 — reclampa e dois acúmulos ponderados (`0x11F0`)

```
008C36EB  rbx = [rbp+0xFF0]
008C36F2  rcx = &[rbp+0x348]
008C36F9  edx = 0
008C36FB  [rbp+0x340] = 0
008C3702  r8d = 0x3F8
008C3708  call 0x1798F42                      ; memset(&[rbp+0x348],0,0x3F8)
008C370D  rax = (int64)esi ; rax <<= 2
008C3710  r10d = r12d
008C3717  r15d = esi
008C371A  [rbp+0x740] = r12d
008C3724  [rbp+0x744] = esi
008C372A  [rbp+0x748] = rax
008C3734  if (r12d <= 0) goto 008C3788
008C3740..008C3772  reconstrói [rbp+0x340+i*8] a partir de [rbx]/[rbx+0x18]
008C3788..008C37F1  copia [rbp+0x750] -> [rsp+0x30] (8 × 0x80 B)
008C3803..008C3861  copia [rbp+0x340] -> [rbp+0xB60] (8 × 0x80 B)
008C3869  if (r10d <= 0) goto 008C38B0
; ---- min(A, 0) por buffer, via 0x1250 ----
008C3880  rdx = [rbp+rbx+0xB60]
008C3888  xmm3 = 0
008C388B  rcx = [rsp+rbx+0x30]
008C3890  r8d = r15d                          ; len
008C3893  [rsp+0x20] = 4                      ; 5º argumento = 4
008C389B  call 0x1250                         ; -> 0x69C0
; ---- copia [0x750] -> [0xB60] e clamp in place, via 0x1100 ----
008C38B0..008C3912  copia [rbp+0x750] -> [rbp+0xB60]
008C3930  rcx = [rbx]
008C3933  r9d = 0
008C3936  xmm2 = 0
008C3939  edx = esi                           ; len
008C393B  call 0x1100                         ; -> 0x3480
; ---- copia de A de novo e acúmulo com peso xmm2 (=xmm7) ----
008C3950..008C39B2  copia [rbp+0x750] -> [rbp+0xB60]
008C39B4..008C3A13  recarrega A (0x90 B) para [rsp+0x30]/[rbp-0x80]
008C3A30  r8  = [rsp+rbx+0x30]                ; A_i
008C3A35  r9d = r14d
008C3A38  rcx = [rbp+rbx+0xB60]
008C3A40  xmm1 = xmm7                         ; peso = arg xmm2
008C3A43  call 0x11F0                         ; -> 0x5BC0
; ---- último acúmulo com peso xmm3 (=xmm6) ----
008C3B80  r8  = [rsp+rdi+0x30]
008C3B85  r9d = esi
008C3B88  rcx = [rbp+rdi+0xB60]
008C3B90  xmm1 = xmm6                         ; peso = arg xmm3
008C3B93  call 0x11F0
008C3BDF  r15 = [rbp+0xFF0]
008C3C02  [r15+0x18] = eax                    ; restaura cursor do alocador
008C3C06  rsp = r11 ; pops ; ret
```

`0x1250` → `0x69C0`: `vminss xmm0,[rcx+rbx*4],xmm3` e
`vmovss [rdx+rbx*4],xmm0` (`00006A60/6A65/6A69`; `vminps` em `00006A8D`).
Logo `dst[i] = min(src[i], xmm3)`; com `xmm3=0` → `dst = min(src,0)`.

`0x1100` → `0x3480`: `vminps ymm1, xmm0, [rcx+r9*4]` e store de volta
(`00003520/3526/352D`; `vminss xmm0,xmm2,[rcx]` em `000035C3/35C7`).
Logo `src[i] = min(xmm2, src[i])` (in place); com `xmm2=0` → `src = min(src,0)`.

`0x11F0` → `0x5BC0`: `vmovss xmm0,[rcx+r10*4]`;
`vfmadd213ss xmm0,xmm1,[r8+r10*4]`; `vmovss [r8+r10*4],xmm0`
(`00005C40/5C46/5C4C`; `vfmadd213ps` em `00005C85`). Logo
`dst[i] = src[i]*xmm1 + dst[i]` (dst = r8, src = rcx).

### Efeito aritmético de `0x8C33D0` (sem nomear)

1. `D = B - A` por buffer (`0x11C0`, `008C3698`/`008C36D6`), condicionado a
   `(int)bits(xmm2) == count` (todos os buffers, `008C366D`) ou `== 1` (A_0 fixo,
   `008C36A9`).
2. `D = min(D, 0)` (`0x1250` com `xmm3=0`, `008C389B`).
3. `D = min(D, 0)` de novo, in place (`0x1100` com `xmm2=0`, `008C393B`).
4. `Acumulo_i = A_i + D_i * xmm2` (`0x11F0`, `008C3A43`), com `xmm2` = arg float.
5. `Acumulo_i += D_i * xmm3` (`0x11F0`, `008C3B93`), com `xmm3` = arg float.
   (As etapas 4/5 usam a mesma `A` recarregada de `[r13]` em `008C3A13` e o
   mesmo `D` reconstruído de `[rbp+0x340]`.)

Observação de fidelidade: `008C3669 movd eax,xmm2` interpreta os **bits** de `xmm2`
como inteiro e compara com `count`; é o que a instrução faz. Não foi atribuído
significado de tipo ao argumento.

### `NÃO PROVADO` em `0x8C33D0`

- O significado de "count" vs "len" no descritor de B (`+0x400`/`+0x404`): lidos em
  `008C34BD`/`008C34C7` e usados, mas **quem preenche** B `+0x400/+0x404` está fora
  desta função (`NÃO PROVADO`; parada em `008C34AE`).
- A semântica nominal dos chamados (`0x11C0`, `0x11F0`, `0x1250`, `0x1100`) não é
  dada por nome; o efeito acima é o do corpo executado.
- O papel de `[r13+0x80]` (lido em `008C3A02`/`008C3B57`, comparado com count em
  `008C3A17`/`008C3B6C`) não foi nomeado: só se provou que é um dword comparado
  ao count.

---

## (b7) `0x8AE6F0` — clonagem de descritor (160 B)

Chamadores (`re_lib.callers`): `008B645E`/`008B65A4`/`008B83C0`/`008B84F0`
(dentro de `0x8B4268`) e `008C81CE`/`008C8314`/`008CA130`/`008CA260`
(dentro de `0x8C5FD8`). Sítio representativo `008B645E`:
`rcx = [rbp+0x4a28]` (descritor fonte), `rdx = &[rbp+0x2090]` (descritor
destino na pilha), `r8 = [r13+0x40]` (comprimento).

Assinatura observada: `rcx = src`, `rdx = dst`, `r8d = len`
(`008AE713 mov rdi,r8`; `008AE72F movsxd rax,edi`).

```
008AE70A  ebx = dword [rcx+0x400]        ; "count" da fonte
008AE716  rcx = rdx + 8
008AE71F  qword [rdx] = 0               ; slot de ponteiro 0
008AE722  r8d = 0x3F8
008AE728  edx = 0
008AE72A  call 0x1798F42                ; memset(dst+8, 0, 0x3F8)
                                        ; => slots 1..0x7F (0x3F8/8 = 0x7F)
008AE72F  rax = (int64)edi ; rax <<= 2  ; len*4
008AE736  qword [rdx+0x408] = rax       ; tamanho em bytes
008AE740  dword [rdx+0x400] = ebx       ; copia "count"
008AE747  dword [rdx+0x404] = edi       ; copia "len"
008AE74E  if (dword [rcx+0x400] <= 0) goto 008AE775
008AE757  rdx = rcx + 0x400
008AE75E  r14 = src - dst               ; r14 = rcx - r15
008AE761  rcx = qword [r14+rax]         ; = [src + 8*i]
008AE765  ++esi
008AE767  qword [rax] = rcx             ; [dst + 8*i] = [src + 8*i]
008AE76A  rax += 8
008AE76E  cmp esi, dword [rdx]          ; i < count
008AE770  jl 008AE761
008AE775..008AE78F  restaura registradores; ret (rax = rdx = dst)
```

Efeito: `dst` recebe `count`, `len`, `len*4` e a **lista de `count`
ponteiros** de `src`, com os slots restantes zerados. `dst` é devolvido em
`rax` (`008AE73D`/`008AE772 mov rax,r15`).

Consequência provada para o layout de descritor: em descritores produzidos
por esta função, `+0x400` = número de ponteiros válidos, `+0x404` =
comprimento em floats, `+0x408` = `len*4` em bytes. Isso é o formato que
`0x8C33D0` lê em `008C34BD`/`008C34C7` (lá os campos vinham de uma cauda de
B copiada em `008C34AE`; quem a preencheu continua fora do escopo, mas o
formato `count/len/bytes` fica corroborado aqui).

### `NÃO PROVADO` em `0x8AE6F0`

- Não se provou *quem* chama `0x8AE6F0` com qual descritor fonte além dos
  sítios acima; a origem de `[r13+0x40]` (o `len`) está fora desta função
  (`008B6457`, `008B65A4` sem escrita visível de `r8`).

---

## (b8) `0x8C3F10` — zeragem condicional de faixas do descritor (952 B)

Chamadores: `008B868B` (em `0x8B85F2`) e `008CA3FB` (em `0x8CA362`).
Sítio `008B868B`: `rcx = &[rbp+0x2090]` (descritor destino),
`rdx = [r13+0x2c38]` (estado), `r9 = [r13+0x10]` (lista de itens).
O 3º argumento `r8` é salvo em `008C3F15` e **nunca lido** no corpo.

Layouts observados:

- Descritor (`rcx`, guardado em `rbx` em `008C3F3C`): lista de ponteiros em
  `+0`, `count` em `+0x400`, `len` em `+0x404` (`008C4106`, `008C4133`).
- Estado (`rdx`, `r11`): 5 registros de 8 bytes em `[+0x1b8, +0x1e0)`
  (passo 8). Bytes de flag em `+5` e `+6` de cada registro
  (`008C3F50`/`008C3F90`; fora do laço, `r15 = r11+0x1bd` em `008C3FEE`
  aponta exatamente `+0x1b8+5`, e `+8` por iteração em `008C4271`).
- Item (`r9`, `rdi`): passo `0x18`; `[+0]` = `kind` (int32),
  `[+8]` = índice inicial (int32), `[+0x10]` = contagem (int32)
  (`008C4014`, `008C4151`, `008C4128`; fim da lista em `r12`, `008C4004`,
  comparação `008C400B`/`008C4249`).

### Pré-varredura das flags (`008C3F28`..`008C3FE6`)

```
008C3F28  r8 = rdx+0x1b8 ; r10 = rdx+0x1e0
008C3F50  al = byte [r8+5] ; if (al) { r9b = 1; goto 008C3F6A }   ; 008C4032
008C3F5E  r8 += 8 ; cmp r8,r10 ; jne 008C3F50
008C3F6A  rcx = rdx+0x1b8 ; rdx += 0x1e0
008C3F90  al = byte [rcx+6] ; if (al) { al = 1; goto 008C3FA8 }  ; 008C403A
008C3F9D  rcx += 8 ; cmp rcx,rdx ; jne 008C3F90
008C3FA6  al = 0
008C3FA8  if (r9b == 0 && al == 0) goto 008C42BE   ; retorna sem fazer nada
```

### Laço externo — 5 seletores (`008C3FB5`..`008C4288`)

```
008C3FBD  rax = &0x2014360          ; tabela i32: 8, 9, 10, 6, 5  (lidos agora)
008C3FFC  r15 = state+0x1bd ; [rsp+0x20] = rax
008C4001  r14 = [item_list] ; r12 = [item_list+8]
008C4008  r13 = (int64)[rax]        ; seletor do canal
008C4014  r8d = dword [r14]         ; kind do item
... filtro de kind (abaixo) ...
008C4245  r14 += 0x18 ; cmp r14,r12 ; jne 008C4014
008C4252  rax = [rsp+0x20]+4 ; ++ecx ; r15 += 8
008C4278  cmp rax,5 ; jb 008C4001   ; 5 canais
```

Filtro de `kind` (passa = segue para `008C40E6`; falha = `008C4245`):

| seletor `r13` | condição de passagem | RVAs |
|---|---|---|
| `0` | sempre passa | `008C4017 je 008C40E6` |
| `1` | `kind != 10` | `008C4026 cmp r8d,0xa` / `008C402A setne al` |
| `2` | `kind != 9` | `008C4047 cmp r8d,9` / `008C404B setne al` |
| `3` | `kind ∉ {9,10}` | `008C4059 lea eax,[r8-9]` / `008C4060 ja` |
| `4` | `kind ∈ {8,9,10}` | `008C4086 lea eax,[r8-8]` / `008C408D ja` |
| `5` | `kind ∈ {16,17,18}` | `008C4071 lea eax,[r8-0x10]` / `008C4078 ja` |
| `6` | `pred(4,kind) && !pred(5,kind)` | `008C409A`/`008C40A1` e `008C40AE`/`008C40B5` |
| `7` | `kind ∈ {8,9}` | `008C40C9 lea eax,[r8-8]` / `008C40D0 ja` |
| outro | `kind == r13` | `008C40D8 cmp r13d,r8d` / `008C40DB sete al` |

`pred` = `0x61B790(ecx, edx)`; corpo em `0061B790`..`0061B85C` retorna
`al` conforme o par `(ecx, edx)`: `ecx=0`→1 (`0061B79C`), `ecx=1`→`edx!=10`
(`0061B7A9`), `ecx=2`→`edx!=9` (`0061B7BA`), `ecx=3`→`!(edx∈{9,10})`
(`0061B7CB`), `ecx=5`→`edx∈{16,17,18}` (`0061B7DF`), `ecx=4`→`edx∈{8,9,10}`
(`0061B7F3`), `ecx=6`→ recursão `pred(4)&&!pred(5)` (`0061B807`..`0061B825`),
`ecx=7`→`edx∈{8,9}` (`0061B843`), outro→`ecx==edx` (`0061B852`).

### Portão de flags e corpo por item (`008C40E6`..`008C4232`)

```
008C40E6  cl = byte [r15+1]   ; flag f6 do canal
008C40EC  al = byte [r15]     ; flag f5 do canal
008C40F1  if (al != 0) goto 008C4245        ; pula item
008C40F9  if (r9b != 0) goto 008C4106       ; r9b = "existe algum f5 != 0"
008C40FE  if (cl != 0) goto 008C4245        ; senão exige f6 == 0
; ---- monta descritor temporário em rsp+0x28 ----
008C4106  rsi = (int64)[rbx+0x404]          ; len (do descritor destino)
008C4114  [rsp+0x28] = 0
008C411D  r8d = 0x3F8 ; rcx = rsp+0x30 ; edx = 0 ; call 0x1798F42  ; memset
008C4128  r8d = dword [r14+0x10]            ; count do item
008C412F  rax = rsi*4 ; [rsp+0x428] = r8d ; [rsp+0x42c] = esi
008C4144  [rsp+0x430] = rax                 ; count/len/bytes do temporário
008C414C  if (r8d <= 0) goto 008C4191
008C4151  rcx = (int64)[r14+8]              ; índice inicial
008C4170  rcx = [rbx + 8*(start+i)] ; [rsp+0x28+8*i] = rcx   ; copia ponteiros
008C4185  cmp edx,r8d ; jl 008C4170
008C4191  rax = rsp+0x440 ; rcx = rsp+0x28 ; edx = 8
008C41B0..008C4201  copia 8*0x80 B (=0x400) de [rcx] para [rax]
008C4203  [rax] = [rcx]                     ; cauda 16 B (base+0x400)
008C4209  if (r8d <= 0) goto 008C423C
008C4216  rbx = rsp+0x440 ; edi = r8d
008C4220  rcx = qword [rbx] ; edx = esi ; call 0x10D0
008C422A  rbx += 8 ; --edi ; jne 008C4220
008C423C  r9d = byte [rsp+0x8b0]            ; restaura flag global
```

`0x10D0` → dispatcher `000010D0` (índice 4 em `0x21C7408`, tabela
`0x21C5E48` → VA `0x199B2F60`, RVA `0x2F60`). Corpo `00002F60`:
`00002F71 shl edx,2`; `00002F7C call 0x1D2E9E0`; `00001D2E9E0` faz
`vxorps ymm0,ymm0,ymm0` e grava `ymm0` em blocos até esgotar `rsi` bytes
(`01D2E9EE`, `01D2EA0B`..`01D2EA2E`). Logo `0x10D0(ptr,len)` **zera
`len*4` bytes** em `ptr` (e retorna 0, `00002F88`).

Efeito de `0x8C3F10`: para cada canal `i` em `0..4` e cada item cujo `kind`
passa no filtro e cujas flags passam no portão, **zera**
`item.count` buffers do descritor destino, começando em `item.start`
(ou seja, `dst[start .. start+count-1][0..len-1] = 0`). Nenhuma operação
aritmética além da zeragem é executada nesta função.

### `NÃO PROVADO` em `0x8C3F10`

- O significado dos valores de `kind` (`5,6,8,9,10,16,17,18`) e dos bytes
  de flag em `state+0x1b8+8i+5/+6` não foi provado; só os testes.
- A origem da lista de itens `r9` (`008C3F2F`; chamador `008B8676`) e o
  papel do 3º argumento `r8` (salvo e não lido, `008C3F15`) — `NÃO PROVADO`.
- A tabela `0x2014360` é lida em `008C4008` como 5 `int32`; não se provou
  quem a escreve.

---

## (b9) `0x8C42D0` — dois multiplicadores por item (323 B)

Chamadores: `008B8B51` (em `0x8B8AE0`) e `008CA8C1` (em `0x8CA850`).
Assinatura observada: `rcx` = descritor (guardado em `rsi`, `008C42E4`),
`r8` = lista de **dois** ponteiros (`[r8]` em `008C4300`, `[r8+8]` em
`008C4316`), `r9b` = flag (guardado em `ebp`, `008C42E0`), `xmm1` = escalar.

```
008C42D9  if (dword [rcx+0x400] == 1) goto 008C440C   ; retorna sem tocar
008C42ED  xmm4 = f32 [0x2079F9C]                      ; bytes 00 00 80 3F = 1.0
008C4303  xmm0 = xmm4 - xmm1                          ; 1 - x
008C430E  xmm1 = xmm1 * f32 [0x207A188]               ; bytes 00 00 00 40 = 2.0 => 2x
008C4328  xmm0 = xmm0 * 2.0                           ; 2*(1-x)
008C4338  [rsp+0x24] = xmm0 (slot temporário)
008C431A  [rsp+0x24] = 0x3F800000 (=1.0)              ; limite superior
008C4321  [rsp+0x70] = 0                              ; limite inferior
008C4341  comiss xmm0, 0.0 ; cmovae rcx, &xmm0        ; 008C4344
008C434D  comiss xmm0, 1.0 ; cmovbe rax, rcx          ; 008C4350
008C435C  xmm6 = [rax]                                ; clamp(2*(1-x), 0, 1)
008C4365  [rsp+0x24] = xmm1 (2x)
008C436F  [rsp+0x20] = 1.0
008C4359  comiss xmm1, 0.0 ; cmovae rcx, &2x          ; 008C436B
008C4377  comiss xmm1, 1.0 ; cmovbe rax, rcx          ; 008C4387
008C438B  xmm7 = [rax]                                ; clamp(2*x, 0, 1)
```

Os dois clamps foram decodificados pelo par `comiss`/`cmov` com os slots
`0.0` e `1.0` acima; a instrução `008C430A subss xmm0,xmm1` (com
`xmm4=1.0`) fixa a forma `2*(1-x)` e `008C430E mulss` fixa `2*x`.

### Laço por item (`008C438F`..`008C43EE`)

`rdi` percorre `[r8]`..`[r8+8]` com passo `0x18` (`008C4300`, `008C4316`,
`008C43E7`/`008C43EE`). Itens em que `[rdi+0x10] != 1` usam dois buffers.

```
008C43A0  if (dword [rdi+0x10] == 1) goto 008C43B8
008C43A4  rcx = (int64)[rdi+8]                 ; start
008C43AA  if (bpl == 0) goto 008C43E7          ; count==1 e flag==0: pula item
008C43AF  rdx = [rsi + 8*start]
008C43B3  xmm0 = xmm6
008C43B6  goto 008C43DB
008C43B8  rdx = [rsi + 8*start]                ; count != 1
008C43BC  eax = start+1
008C43BF  r8d = dword [rsi+0x404]              ; len
008C43C6  xmm0 = xmm6
008C43CC  rbx = [rsi + 8*(start+1)]
008C43D0  call 0x1220                          ; buf[start] *= xmm6
008C43D5  rdx = rbx
008C43D8  xmm0 = xmm7
008C43DB  r8d = dword [rsi+0x404]
008C43E2  call 0x1220                          ; buf[start(+1)] *= xmm7
```

`0x1220` → dispatcher `00001220` (índice 4, tabela `0x21C6008` → VA
`0x199B6160`, RVA `0x6160`). Em `00006160` os casos `xmm0==1.0`
(`0000617A`/`00006184`) e `xmm0==0.0` (`0000618E`/`00006194`) têm caminho
próprio; o caminho geral multiplica no lugar:
`00006200 vmulss xmm1,xmm0,[rdx+rax*4]`; `00006205 vmovss [rdx+rax*4],xmm1`;
vetorial em `00006220/00006226 vmulps`. Logo `0x1220(dst, w, n)` faz
`dst[i] *= w`.

Efeito de `0x8C42D0` (com `x = xmm1`):
- `w0 = clamp(2*(1-x), 0, 1)`, `w1 = clamp(2*x, 0, 1)`.
- item com `count == 1`: se `flag != 0`, `buf[start] *= w0`; se `flag == 0`,
  item é ignorado.
- item com `count != 1`: `buf[start] *= w0` e `buf[start+1] *= w1`
  (somente os dois primeiros buffers do item).
- descritor com `[+0x400] == 1` retorna em `008C440C` sem nenhuma escrita.

### `NÃO PROVADO` em `0x8C42D0`

- Não se provou por que só os dois primeiros buffers de um item com
  `count != 1` são tratados (`008C43B8`..`008C43E2`): o corpo só os lê.
- O significado de `r9b` (flag) e de `[rdi+0x10]` como "contagem" é
  operacional (comparado a 1 e usado como passo), não nominal.

---

## (b10) `0x8C32C0` (266 B) e `0x8C3E00` (266 B) — wrappers de chamada

Ambos têm o mesmo corpo, diferindo só no destino (`rcx+0x1A0` vs `rcx+0x340`)
e no chamado (`0x8CB040` vs `0x8CB2F0`).

Chamadores de `0x8C32C0`: `008B67B1` (em `0x8B4268`) e `008C8521`
(em `0x8C5FD8`). Chamadores de `0x8C3E00`: `008B79AE` (em `0x8B4268`) e
`008C971E` (em `0x8C5FD8`).

Assinatura observada: `rcx` = estado (base do destino), `rdx` = bloco A,
`r8` = bloco B. Sem prólogo de pilha além de `sub rsp,0x848`.

```
008C32C0  rsp -= 0x848 ; r10d = 8 ; rax = rsp+0x20
008C32E0..008C3339  copia 8*0x80 B de [r8] para [rsp+0x20]
008C333B  [rax] = [r8]                       ; cauda 16 B => total 0x410 B
008C3342  rax = rsp+0x430
008C3350..008C33A1  copia 8*0x80 B de [rdx] para [rsp+0x430]
008C33A3  [rax] = [rdx]                      ; cauda 16 B => total 0x410 B
008C33A6  r8 = rcx + 0x1a0
008C33AD  rdx = rsp+0x20                     ; cópia de B
008C33B2  rcx = rsp+0x430                    ; cópia de A
008C33BD  call 0x8CB040
008C33C2  rsp += 0x848 ; ret
```

```
008C3E00  rsp -= 0x848 ; r9d = 8 ; rax = rsp+0x20
008C3E20..008C3E79  copia 0x400 B de [r8] + cauda 16 B (008C3E7B) para [rsp+0x20]
008C3E90..008C3EE1  copia 0x400 B de [rdx] + cauda 16 B (008C3EE3) para [rsp+0x430]
008C3EE6  r8 = rcx + 0x340
008C3EED  rdx = rsp+0x20
008C3EF2  rcx = rsp+0x430
008C3EFD  call 0x8CB2F0
008C3F02  rsp += 0x848 ; ret
```

Nenhuma aritmética de amostra é feita aqui: só cópia de `0x410` B de cada
argumento para a pilha e a chamada.

### Fatos provados sobre `0x8CB040` (chamado em `008C33BD`)

- `008CB065 mov r12,rcx` (1º arg = descritor de saída); lê
  `[r12+0x404]` (`008CB091`) e `[r12+0x400]` (`008CB0B7`).
- Lê também `[r9+0x404]` (`008CB074`) e o cursor `[rbx+0x18]`
  (`008CB071`), devolvendo-o em `008CB2C4`.
- Chama `0x1400` em `008CB24B` com `r9 = &soma` (`008CB228`),
  `rcx`/`rdx` = buffers (`008CB23E`/`008CB246`) e `r8d` = len
  (`008CB22D`); grava o escalar em `[r12+r15*4]` (`008CB266`);
  avança `r15` até `[r12+0x404]` (`008CB289`/`008CB298`).
- `0x1400` já está provado como produto escalar neste arquivo (§b1).

### Fatos provados sobre `0x8CB2F0` (chamado em `008C3EFD`)

- `008CB30F mov r13,r8` (3º arg = destino); `008CB312`/`008CB31C`
  preservam `rdx` (2º arg) e `rcx` (1º arg); lê `[r11+0x400]`
  (`008CB3F2`) e `[r12+0x404]` (`008CB3DB`).
- Chama `0x10D0` em `008CB3C5` (zeragem de `len*4` bytes, provada em §b8)
  e `0x11F0` em `008CB571` (`dst[i] += src[i]*w`, provado em §b6).
- Escreve em `[r13+...]` com deslocamentos `+0x100`/`+0x180`/`+0x188`/
  `+0x190`/`+0x198` (`008CB451`, `008CB460`, `008CB467`, `008CB4B5`,
  `008CB4E6`).

### `NÃO PROVADO` em `0x8C32C0` / `0x8C3E00`

- A transformação completa de `0x8CB040` é `NÃO PROVADO`: a cadeia para em
  `008CB24B` (só se provou a chamada de produto escalar e o armazenamento
  em `[r12+r15*4]`; o resto do corpo, `008CB0B7`..`008CB2A1`, não foi
  reduzido a fórmula).
- A transformação completa de `0x8CB2F0` é `NÃO PROVADO`: a cadeia para em
  `008CB3C5`/`008CB571` (só se provou zeragem + acúmulo ponderado; o
  mapeamento dos campos `+0x100/+0x180/+0x188/+0x190/+0x198` não foi
  nomeado).
- O que é `rcx+0x1A0` / `rcx+0x340` no estado (`008C33A6`/`008C3EE6`)
  permanece sem nome provado.

---

## (f2) Consolidação de `NÃO PROVADO` — satélites da etapa K

Resumo dos pontos de parada por função (RVA onde a cadeia parou):

| função | efeito provado | parada / não provado |
|---|---|---|
| `0x8AE6F0` | clona descritor: `+0x400=count`, `+0x404=len`, `+0x408=len*4`, copia `count` ponteiros | origem de `len` (`r8=[r13+0x40]`) fora da função, `008B6457` |
| `0x8C3F10` | zera `count` buffers a partir de `item.start` por canal/itens filtrados | semântica dos `kind`/flags em `state+0x1b8`; `008C40E6`; `r8` não usado (`008C3F15`) |
| `0x8C42D0` | `w0=clamp(2(1-x),0,1)`, `w1=clamp(2x,0,1)`; multiplica 1 ou 2 buffers do item | por que só 2 buffers quando `count!=1`, `008C43B8` |
| `0x8C32C0` | copia A/B para pilha e chama `0x8CB040` com `r8=rcx+0x1A0` | fórmula de `0x8CB040` além do dot em `008CB24B` |
| `0x8C3E00` | copia A/B para pilha e chama `0x8CB2F0` com `r8=rcx+0x340` | fórmula de `0x8CB2F0` além de `008CB3C5`/`008CB571` |

Constantes referidas neste bloco (bytes little-endian no arquivo):

| RVA | bytes | valor | uso |
|---|---|---|---|
| `0x2079F9C` | `00 00 80 3F` | `1.0f` | `008C42ED`, `008C42F1` |
| `0x207A188` | `00 00 00 40` | `2.0f` | `008C430E`, `008C4328` |
| `0x2014360` | `08 00 00 00 09 00 00 00 0A 00 00 00 06 00 00 00 05 00 00 00` | `{8,9,10,6,5}` (i32×5) | seletores em `008C4008` |

Fica registrado que todos os efeitos acima foram lidos do corpo executado
(instrução + RVA), não de nomes de parâmetro, e que nenhuma seção deste
arquivo foi reescrita: o arquivo cresceu por append.





