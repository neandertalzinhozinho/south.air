# H — Detector e ganho: `0x8CAE90`, `0x8C3C20`, `0x8C1440`

Alvo: `dumpsooth/nyx_soothe3_dump.bin` (137.003.008 B, SHA-256 `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`).
Leitura estática apenas. Nada foi executado, hookado, patcheado ou injetado.

Convenções: RVA == offset no arquivo; ponteiros de `.data`/`.rdata` com VA = `0x199B0000 + RVA`.
Prova = instrução x86-64 com RVA. Decompilado não foi usado como prova.
Desmontagem: `tools/show_func.py` (chain-aware, constantes RIP resolvidas); desvios de thunk IPP resolvidos por `checks/thunk_map.txt` + `tools/dispatch.py`.

---

## 0. Cadeia provada (o que realmente faz a conta)

`0x8CAE90` **não contém aritmética**. É um adaptador de layout de descritores que despacha para um thunk IPP e termina em FMA vetorial:

```
0x8C02F0 ──(2 chamadas)──> 0x8CAE90 ──> 0x1580 (thunk, jmp [tab+4*8])
                                                 └─> 0xCCE0 ──> 0x65EA0 ──> 0x6CE80  (vfmadd213ps)
```

* `0x1580`: `movsxd rax,[0x21C7408]` (=4) / `lea r10,[0x21C6488]` / `jmp [r10+rax*8]` → entrada `0x199BCCE0` → **RVA 0xCCE0** (`tools/dispatch.py`).
* `0xCCE0`: valida `rcx,rdx,r8 != 0` e `r9d > 0`, `call 0x65EA0`, retorna `0` / `-8` / `-6`.
* `0x65EA0`: calcula `r10 = 12*len` (`lea r10,[r9+r9*2]; shl r10,2` em `0x65EB3`/`0x65EB7`), compara com `0x8000` e escreve o mesmo valor (`0` ou `0x100`) em `[rsp+0x20/0x28/0x30]` (args 5..7 = hint IPP) — **não altera rcx/rdx/r8/r9d**.
* `0x6CE80`: o kernel.

Prova de que o kernel é `dst += a*b` (ordem dos operandos):

```
0006CEAF  vmovups  ymm1, [rcx]            ; ymm1 = a
0006CEB7  vmovups  ymm0, [rdx]            ; ymm0 = b
0006CEBB  vfmadd213ps ymm1, ymm0, [r8]    ; ymm1 = a*b + [r8]
0006CEC4  vmovups  [r8], ymm1             ; dst = a*b + dst
```

Mesma operação no caminho mascarado (`0x6CF04`–`0x6CF20`, `vmaskmovps` + `vfmadd213ps ymm2,ymm5,ymm0` em `0x6CF1B` + store com máscara em `0x6CF20`) e no desenrolado 4× (`0x6CF60`–`0x6CFB0`, quatro `vfmadd213ps` em `0x6CF7E`, `0x6CF83`, `0x6CF9E`, `0x6CFA4`).

---

## A) `0x8CAE90` — adaptador de layout para MAC de descritores

Extensão: `0x8CAE90..0x8CAFC3` (307 B chain-aware; 0x8CAE90+245 cai no meio do fragmento encadeado).

### A.1 Assinatura provada

| RVA | instrução | leitura |
|---|---|---|
| `0x8CAEA8` | `mov rbx, r8` | `r8` = descritor 3 (base do laço do caso 1) |
| `0x8CAEAB` | `mov rdi, rdx` | `rdx` = descritor 2 |
| `0x8CAEAE` | `mov rsi, rcx` | `rcx` = descritor 1 (**destino**, ver A.2) |
| `0x8CAEA2` | `mov eax, [rdx+0x400]` | descritor 2 tem contagem em `+0x400` (tipo "grande") |
| `0x8CAEB1` | `cmp [rcx+0x80], eax` | descritor 1 tem contagem em `+0x80` (tipo "pequeno") |
| `0x8CAEB9` | `mov eax, [r8+0x80]` / `cmp [rcx+0x80], eax` @`0x8CAEC0` | descritor 3 também com contagem em `+0x80` |
| `0x8CAEC8` | `movsxd rbp, [rcx+0x80]` | nº de planos a percorrer = contagem do descritor 1 |
| `0x8CAED8` | `mov r14d, [rcx+0x84]` | comprimento de cada plano = `[dst+0x84]` |

`r9d` é **entrada ignorada**: o comprimento vem sempre de `[rcx+0x84]` (`0x8CAED8` no caso 1, `0x8CAF31` no caso 2, `0x8CAF8A` no caso 3).

Estrutura de descritor (provada pelos acessos, não por nome):

* **pequeno**: `float* p[16]` em `+0x00`, `int n` em `+0x80`, `int len` em `+0x84` (mínimo 0x88 bytes; o chamador copia 0x90).
* **grande**: `float* p[N]` em `+0x00`, `int n` em `+0x400`, `int len` em `+0x404` (mínimo 0x408).

### A.2 Tabela instrução-a-instrução (só o que prova)

| RVA | instrução | leitura |
|---|---|---|
| `0x8CAEB1` | `cmp [rcx+0x80], eax` | se as três contagens são iguais → caso 1 |
| `0x8CAEDF` | `sub rsi, rbx` | `rsi = dst_desc − src2_desc` (truque de base) |
| `0x8CAEE2` | `sub rdi, rbx` | `rdi = src1_desc − src2_desc` |
| `0x8CAEF0` | `mov r8, [rsi+rbx]` | `r8 = dst_desc.p[i]` |
| `0x8CAEF7` | `mov rdx, [rbx]` | `rdx = src2_desc.p[i]` |
| `0x8CAEFA` | `mov rcx, [rdi+rbx]` | `rcx = src1_desc.p[i]` |
| `0x8CAEF4` | `mov r9d, r14d` | `len = [dst+0x84]` |
| `0x8CAEFE` | `call 0x1580` | MAC (kernel em `0x6CEBB`, seção 0) |
| `0x8CAF03`/`0x8CAF0B` | `lea rbx,[rbx+8]` / `sub rbp,1` / `jne` | laço sobre o array de ponteiros (passo 8 B) |
| `0x8CAF12` | `cmp [rdx+0x400], 1` / `jle 0x8CAF65` | caso 2/3 só quando src1 tem 1 plano ou menos |
| `0x8CAF1B` | `cmp [r8+0x80], 1` | caso 2: src2 tem exatamente 1 plano |
| `0x8CAF38` | `sub rsi, rdi` | `rsi = dst_desc − src1_desc` |
| `0x8CAF3B` | `mov rbx, [r8]` | src2 vira **um único ponteiro** (broadcast) |
| `0x8CAF40`/`0x8CAF47` | `mov r8,[rsi+rdi]` / `mov rcx,[rdi]` | `dst.p[i]` × `src1.p[i]` |
| `0x8CAF4A` | `mov rdx, rbx` | 2º operando = `src2.p[0]` fixo |
| `0x8CAF67` | `cmp [r8+0x80], 1` | caso 3: src2 também com 1 plano |
| `0x8CAF7F`/`0x8CAF82` | `mov rbx,[r8]` / `mov rdi,[rdx]` | ambos os fontes viram ponteiro único |
| `0x8CAF91` | `mov r8, [rsi+rbp*8]` | `dst.p[i]` (aqui `rsi == rcx`, sem truque de base) |
| `0x8CAF9B`/`0x8CAF98` | `mov rcx, rdi` / `mov rdx, rbx` | fontes fixas |

### A.3 Pseudocódigo (com RVA por linha)

```c
// 0x8CAE90(rcx = dst_desc, rdx = src1_desc, r8 = src2_desc)
n1 = dst_desc->n;                          // 0x8CAEC8  ([rcx+0x80])
len = dst_desc->len;                       // 0x8CAED8  ([rcx+0x84])
n2 = src1_desc->n;                         // 0x8CAEA2  ([rdx+0x400])
n3 = src2_desc->n;                         // 0x8CAEB9  ([r8+0x80])

if (n1 == n2 && n1 == n3) {                // 0x8CAEB1/0x8CAEC0
    for (i = 0; i < n1; i++)               // 0x8CAF07
        mac(dst_desc->p[i],                // 0x8CAEF0  (r8 = destino do MAC)
            src1_desc->p[i],               // 0x8CAEFA
            src2_desc->p[i], len);         // 0x8CAEF7
} else if (n2 > 1 && n3 == 1) {            // 0x8CAF12/0x8CAF1B
    for (i = 0; i < n1; i++)               // 0x8CAF56
        mac(dst_desc->p[i], src1_desc->p[i], src2_desc->p[0], len);  // 0x8CAF40/0x8CAF3B
} else if (n2 == 1 && n3 == 1) {           // 0x8CAF65/0x8CAF67
    for (i = 0; i < n1; i++)               // 0x8CAFA6
        mac(dst_desc->p[i], src1_desc->p[0], src2_desc->p[0], len);  // 0x8CAF91/0x8CAF82
}
// 0x8CAFB0..0x8CAFC2: epílogo, sem conta
```
onde `mac(d,a,b,l)` é `dst += a*b` (`0x6CEBB`).

### A.4 Veredito do alvo A

* **Não é subtração, não é divisão.** É **MAC (multiplicação-acumulação) de descritores**: `dst.p[i] += src1.p[i] * src2.p[i]` por plano.
* **Domínio: float32 linear.** Prova negativa: na cadeia inteira (`0x8CAE90`→`0x1580`→`0xCCE0`→`0x65EA0`→`0x6CE80`) só existem `vmovups/vmovdqu`, `vfmadd213ps`, `vmaskmovps` e a aritmética de índice — **nenhum** `ln`, `exp`, `pow`, `log10`, nem multiplicação por 20/`0.0501`/`0.1151`; nenhum `divss`/`vdivps`. Não há conversão de/para dB em nenhum ponto do caminho.
* **É redução?** Parcialmente: acumula por plano (`+=`), mas **não reduz** para escalar — grava em vetor de mesmo tamanho (`len` amostras por plano). Não há soma horizontal (`haddps`/`vhaddps`) lida na cadeia.

### A.5 O que `0x8C02F0` faz com isso (papel dos dois operandos)

Argumentos de `0x8C02F0`: `rcx` (arg1), `rdx` (arg2), `r8` (arg3), `r9` (arg4), `[stack]` arg5.

* `0x8C031B` `mov r14,[rbp+0xfe0]` → **arg5** = contexto com arena: `[r14]` = base float, `[r14+0x18]` = offset bump (lido em `0x8C0335`, escrito em `0x8C0434`).
* `0x8C0350` laço 8×`0x80` + `0x8C03C4` (`movups [r10],xmm0`): copia **0x410 B** de `rdx`(arg2) para `rbp+0x750` → arg2 é o **descritor grande** (`0x8C03CD` lê `[rbp+0xb50]`=count e `0x8C03D7` lê `[rbp+0xb54]`=len).
* `0x8C03E5`/`0x8C03EC`/`0x8C03F2`: `[rbp+0x740]=count`, `[rbp+0x744]=len`, `[rbp+0x748]=4*len` → cabeçalho do descritor grande em `rbp+0x340`.
* `0x8C0402..0x8C0438`: preenche `[rbp+0x340 + i*8]` com fatias da arena (`r14`) avançando `len` amostras, alinhando o offset a 16 floats.
* `0x8C07D0` laço: copia os 0x410 B de `rbp+0x340` → `rbp+0xb60` (descritor de bandas usado nos dois MACs).
* `0x8C0840` laço: `0x1100(rcx=band[i], edx=len, r9d=0, xmm2=0)` → piso `max(x,0)` por banda.
* `0x8C086B`: copia **arg3** (`[rbp+0xfd0]`) → `rsp+0x30` (descritor pequeno).
* `0x8C0914..0x8C0995`: copia **arg1** (`r13`) → `rbp+0x340` (sobrescreve o cabeçalho grande; o grande já foi copiado para `0xb60`).
* `0x8C099C` **call #1**: `r8 = rsp+0x30` (**dst** = arg3), `rdx = rbp+0xb60` (src1 = bandas), `rcx = rbp+0x340` (src2 = arg1).
* `0x8C09A1`: `rax = [rbp+0xfd8]` = **arg4**; `0x8C09AF..0x8C0A14` copia arg4 → `rbp+0x340`.
* `0x8C0A20` laço: copia `rbp+0x750` → `rbp+0xb60` (nova cópia do descritor de bandas).
* `0x8C0A8C..0x8C0ADD`: copia **arg1** → `rsp+0x30`.
* `0x8C0AE5` **call #2**: `r8 = rbp+0x340` (**dst** = arg4), `rdx = rbp+0xb60` (bandas), `rcx = rsp+0x30` (arg1).

Portanto, o efeito dos dois MACs (provável pelo encadeamento de instruções, não pelo nome de nada):

```
arg3_planes += Σ_planos( band_planes * arg1_planes )     // 0x8C099C
arg1_planes += Σ_planos( band_planes * arg4_planes )     // 0x8C0AE5
```
`dst` dos MACs são **cópias de cabeçalho** dos descritores; a escrita cai nos buffers apontados pelos ponteiros (arena de arg5). Qual é a grandeza de cada descritor (curva? áudio? ganho?) → **NÃO PROVADO**.

---

## B) `0x8C3C20` — one-pole de duas passadas (forward/back)

Extensão `0x8C3C20..0x8C3DF1` (465 B), 109 instruções, 30 ops escalares, **zero chamadas**.

### B.1 Assinatura provada

| RVA | instrução | leitura |
|---|---|---|
| `0x8C3C26` | `movsxd rsi, [rcx+0x400]` | nº de planos (descritor **grande**) |
| `0x8C3C30` | `movsxd r10, [rcx+0x404]` | comprimento de cada plano |
| `0x8C3C37` | `mov rdi, rcx` | descritor base |
| `0x8C3C3A` | `test rsi,rsi` / `jle 0x8C3DEA` | sai se 0 planos |
| `0x8C3C60` | `mov rdx, [rdi + r11*8]` | `plano = desc->p[i]` |
| `0x8C3C66` | `movss xmm2, [rdx]` | **semente = x[0]** |
| `0x8C3C43` | `movss xmm3, [0x2079DB0]` | coeficiente `alpha = 0.1f` (constante única) |

### B.2 As 30 ops escalares (todas, com RVA)

**Passada direta, bloco desenrolado 4× (`0x8C3C90`–`0x8C3CE1`)**

| RVA | instrução | leitura |
|---|---|---|
| `0x8C3C9A` | `subss xmm0, xmm2` | `x[i] - y` |
| `0x8C3C9E` | `mulss xmm0, xmm3` | `* 0.1` |
| `0x8C3CA2` | `addss xmm2, xmm0` | `y += ...` |
| `0x8C3CAE` | `movss [rcx-8], xmm2` | **grava y in-place** em `x[i]` |
| `0x8C3CAA` | `subss xmm1, xmm2` | 2ª cópia do padrão |
| `0x8C3CB3` | `mulss xmm1, xmm3` | |
| `0x8C3CB7` | `addss xmm2, xmm1` | |
| `0x8C3CC4` | `movss [rcx-4], xmm2` | |
| `0x8C3CC0` | `subss xmm0, xmm2` | 3ª |
| `0x8C3CC9` | `mulss xmm0, xmm3` | |
| `0x8C3CCD` | `addss xmm2, xmm0` | |
| `0x8C3CD5` | `movss [rcx], xmm2` | |
| `0x8C3CD1` | `subss xmm1, xmm2` | 4ª |
| `0x8C3CD9` | `mulss xmm1, xmm3` | |
| `0x8C3CDD` | `addss xmm2, xmm1` | |
| `0x8C3CE1` | `movss [rcx+4], xmm2` | |

**Passada direta, cauda escalar (`0x8C3CF5`–`0x8C3D02`)**

| RVA | instrução | leitura |
|---|---|---|
| `0x8C3CFA` | `subss xmm0, xmm2` | idem, 1 elemento |
| `0x8C3CFE` | `mulss xmm0, xmm3` | |
| `0x8C3D02` | `addss xmm2, xmm0` | |
| `0x8C3D06` | `movss [rdx+rax*4], xmm2` | grava in-place |

**Passada reversa (`0x8C3D50`–`0x8C3DA8`)**

| RVA | instrução | leitura |
|---|---|---|
| `0x8C3D50` | `movss xmm0, [r8+8]` | carrega `x[k]` **de trás para frente** |
| `0x8C3D5C` | `subss xmm0, xmm2` | `x[k] - y` |
| `0x8C3D60` | `mulss xmm0, xmm3` | `* 0.1` |
| `0x8C3D64` | `addss xmm2, xmm0` | `y += ...` |
| `0x8C3D71` | `movss [r8+8], xmm2` | grava in-place |
| `0x8C3D6D`/`0x8C3D77`/`0x8C3D7B`/`0x8C3D89` | `subss`/`mulss`/`addss`/`movss` | 2ª cópia |
| `0x8C3D85`/`0x8C3D8F`/`0x8C3D93`/`0x8C3D9B` | idem | 3ª cópia |
| `0x8C3D97`/`0x8C3DA0`/`0x8C3DA4`/`0x8C3DA8` | idem | 4ª cópia |
| `0x8C3DAE` | `sub r8, 0x10` | anda 4 floats para trás (`0x8C3DB2 sub r9,1` / `jne`) |

**Passada reversa, cauda (`0x8C3DBD`–`0x8C3DD7`)**

| RVA | instrução | leitura |
|---|---|---|
| `0x8C3DC2` | `subss xmm0, xmm2` | |
| `0x8C3DC6` | `mulss xmm0, xmm3` | |
| `0x8C3DCA` | `addss xmm2, xmm0` | |
| `0x8C3DCE` | `movss [rdx+rcx*4], xmm2` | |
| `0x8C3DD7` | `jns 0x8C3DBD` | desce até o índice 0 |

Contagem: `subss` 4+1+4+1 = **10**, `mulss` **10**, `addss` **10** → 30. Nenhum outro op escalar no corpo.

### B.3 Pseudocódigo

```c
// 0x8C3C20(rcx = descritor grande)   -- in-place
for (i = 0; i < desc->n; i++) {              // 0x8C3C26, 0x8C3C60
    float* x = desc->p[i];                   // 0x8C3C60
    int    L = desc->len;                    // 0x8C3C30
    float  y = x[0];                         // 0x8C3C66
    for (k = 0; k < L; k++) {                // 0x8C3C90 (4×) + 0x8C3CF5
        y += (x[k] - y) * 0.1f;              // 0x8C3C9A / 0x8C3C9E / 0x8C3CA2
        x[k] = y;                            // 0x8C3CAE
    }
    // y == x[L-1] depois da passada direta
    for (k = L-2; k >= 0; k--) {             // 0x8C3D50 (4×) + 0x8C3DBD
        y += (x[k] - y) * 0.1f;              // 0x8C3D5C / 0x8C3D60 / 0x8C3D64
        x[k] = y;                            // 0x8C3D71
    }
}
```

### B.4 Veredito do alvo B

* **É um one-pole IIR de 1ª ordem** — `y += (x - y)*a` com **`a = 0.1f` fixo**, `0x2079DB0 = 0x3DCCCCCD` → **0.10000000149011612**.
* **É envelope follower com attack/release? NÃO.** Prova por instrução:
  * não existe `abs` (`andps` com `0x7FFFFFFF` ausente no corpo), não existe `maxss`/`minss`, nem `comiss`, nem seleção de coeficiente por ramo (`cmp`/`cmov` não aparecem antes do `mulss`);
  * o coeficiente é o **mesmo** `xmm3` nas duas passadas e em todos os 30 ops (`0x8C3C9E`, `0x8C3CB3`, `0x8C3CC9`, `0x8C3CD9`, `0x8C3CFE`, `0x8C3D60`, `0x8C3D77`, `0x8C3D8F`, `0x8C3DA0`, `0x8C3DC6`);
  * não há estado persistente entre chamadas: o "estado" (`xmm2`) é **semeado pela própria entrada** (`0x8C3C66` = `x[0]`) e a passada reversa é semeada pelo último valor da direta;
  * a operação é **in-place** (`0x8C3CAE`, `0x8C3D71`) e **bidirecional** (direta + reversa) ⇒ suavizador de defasagem ~zero, não seguidor de pico.
* **Entrada/saída**: o mesmo vetor (in-place), `desc->p[i][0..len-1]`, para `i < desc->n`.
* **Constante**: nenhuma outra; `0.1f` é a única constante lida no corpo.
* Chamadores: `0x8B7240` (dentro de `0x8B4268`) e `0x8C8FB0` (dentro de `0x8C5FD8`, cópia deslocada +0x11D70). Em `0x8B7240` o descritor passado é uma **cópia local** (`rbp+0x4110`, copiada de `rbp+0x830` em `0x8B71E0..0x8B723D`) ⇒ o resultado é uma versão suavizada paralela à original, não uma modificação do buffer de áudio. **Qual grandeza é suavizada (curva de ganho vs. sinal) → NÃO PROVADO.**

---

## C) `0x8C1440` — estagiador/orquestrador de bloco (7.800 B, 58 calls)

Perfil medido (`tools/scan_region.py`): 1.786 instruções, **2 `mulss`, 4 `subss`, 0 `addss`, 0 `divss`, 0 FMA**. Ou seja: **a conta não está aqui**; está nos thunks chamados.

### C.1 Assinatura (8 argumentos) — provada pela aritmética do quadro

```
0x8C144A  mov [rsp+8], rcx      ; home de arg1
0x8C1445  mov [rsp+0x10], rdx   ; home de arg2
0x8C1440  mov [rsp+0x18], r8    ; home de arg3
0x8C144F  push rbp / 0x8C1450 push rbx / 0x8C1451 push rsi
0x8C1452  lea rbp, [rsp - 0x13B0]   ; rbp = R - 0x13C8  (R = slot do retorno)
0x8C145A  mov eax, 0x14B0
0x8C145F  call 0x17978C0            ; sonda de pilha
0x8C1464  sub rsp, rax
```

Como **nenhuma** instrução grava `[rbp+0x13D0]`, `[rbp+0x13D8]`, `[rbp+0x13E0]`, `[rbp+0x13E8]` (varredura completa das 1.786 instruções), e como `rbp+0x13C8 == R`:

| slot | offset | = argumento |
|---|---|---|
| `rbp+0x13D0` | R+8 | **arg5** — ponteiro para a instância (`this`) |
| `rbp+0x13D8` | R+0x10 | **arg6** — descritor com `+0x404` = comprimento e array de ponteiros (`0x8C2DCD`/`0x8C2DD6`) |
| `rbp+0x13E0` | R+0x18 | **arg7** — ponteiro (buffer/descritor auxiliar) |
| `rbp+0x13E8` | R+0x20 | **arg8** — byte (flag) |

`arg2` (`rdx`→`rsi`) = descritor grande de bandas: `+0x400` = contagem, `+0x404` = amostras por banda.
`arg3` (`r8`→`rbx`) = arena: `[arg3]` = base float, `[arg3+0x18]` = offset bump.

### C.2 Mapa dos 58 `call` (destino + papel provado)

| destino | nº | RVAs | papel (prova) |
|---|---|---|---|
| `0x17978C0` | 1 | `0x8C145F` | sonda/alocação de pilha (`eax=0x14B0`; `sub rsp,rax` em `0x8C1464`). Identidade (`__chkstk`?) **NÃO PROVADA** — sem dissecção. |
| `0x8CAFD0` | 3 | `0x8C179A`, `0x8C17BE`, `0x8C17E2` | **bump allocator** da arena: lê `[rcx]`=base e `[rcx+0x18]`=offset, cria 2 fatias de `[rdx+0x10]` floats, grava `[rdx]`/`[rdx+8]` e alinha o offset a 16 floats (`0x8CAFD6`–`0x8CB03A`). Sem aritmética de sinal. |
| `0x10D0` | 12 | `0x8C1808`, `0x8C1838`, `0x8C187A`, `0x8C18BB`, `0x8C18FB`, `0x8C193A`, `0x8C197A`, `0x8C19BA`, `0x8C296B`, `0x8C29B7`, `0x8C29F2`, `0x8C2A37` | **memset**(rcx, n=edx de bytes→elementos) — `0x2F71 shl edx,2` + `call 0x1D2E9E0` em `0x2F7C`. Zera as fatias estagiadas (pares L/R: laço `cmp rbx,2`, `0x8C1814`). |
| `0x1580` | 5 | `0x8C1D28`, `0x8C1D4E`, `0x8C1E81`, `0x8C21D8`, `0x8C220E` | **MAC de descritores** `dst += src1*src2` (seção A; kernel `0x6CEBB`). |
| `0x1370` | 9 | `0x8C1DF0`, `0x8C1E3B`, `0x8C1EAB`, `0x8C22D0`, `0x8C22FB`, `0x8C298E`, `0x8C29CE`, `0x8C2A0E`, `0x8C2A4E` | **soma vetorial in-place** `dst[i] = src[i] + dst[i]` — impl `0xA120`: `0xA1A0 vmovss xmm0,[rcx+rdx*4]`, `0xA1A5 vaddss xmm1,xmm0,[rdi+rdx*4]`, `0xA1AA vmovss [rdi+rdx*4],xmm1`; assinatura 3 args (`test rcx`/`test rdi`/`test r8d` em `0xA128`/`0xA131`/`0xA13A`). |
| `0x1100` | 4 | `0x8C2393`, `0x8C23CD`, `0x8C240D`, `0x8C244D` | **clamp escalar com limite**: `r9d=0` → caminho `0x35D9` com `vmaxss` (`0x3640`, `0x3660`, `0x36C0`) = `x = max(x, bound)`; `r9d=4` → caminho `0x34AA` com `vminss` (`0x3500`, `0x3520`, `0x3580`). Aqui: `r9d=0`, `xmm2 = 1e-7` (`0x8C238D`/`0x8C2367`) ⇒ **piso 1e-7**. |
| `0x1550` | 4 | `0x8C2545`, `0x8C263D`, `0x8C273B`, `0x8C2828` | **divisão vetorial** `dst[i] = src1[i] / src2[i]` — impl `0xC560` → `0x63640`: `0x63775 vrcpps ymm0,ymm5`, `0x63782 vfnmadd213ps ymm3,ymm0,ymm4` (resíduo), `0x63791`/`0x63796` dois `vfmadd213ps` (Newton) + correção de zero/inf/denormal em `0x637BA..0x63889`. |
| `0x1220` | 4 | `0x8C2CE9`, `0x8C2DDD`, `0x8C30C9`, `0x8C31CA` | **escala in-place** `dst[i] *= xmm0` (fato já provado; usado aqui com `xmm0 = 1-g` em `0x8C2CCF`/`0x8C2DC8` e `0x8C30AF`/`0x8C31B6`). |
| `0x11F0` | 4 | `0x8C2DA7`, `0x8C2DF5`, `0x8C3196`, `0x8C31E0` | **FMA** `dst[i] = src[i]*xmm1 + dst[i]` — impl `0x5BC0`: `0x5C40 vmovss xmm0,[rcx+r10*4]`, `0x5C46 vfmadd213ss xmm0,xmm1,[r8+r10*4]`, `0x5C4C vmovss [r8+r10*4],xmm0`. |
| `0x61B790` | 8 | `0x8C1B2F`, `0x8C1B43`, `0x8C1F9E`, `0x8C1FB2`, `0x8C2B6A`, `0x8C2B7D`, `0x8C2ED3`, `0x8C2EE6` | **predicado** `bool f(ecx=código, edx=índice)`: cadeia `cmp ecx,1`…`cmp ecx,6` + `setne`/`seta`/`setbe` (`0x61B798`–`0x61B81x`). É a versão fora-de-linha do mesmo teste inline em `0x8C1ABD`–`0x8C1B69`. Semântica dos códigos **NÃO PROVADA**. |
| `0x1798F42` | 4 | `0x8C1BA0`, `0x8C2053`, `0x8C2BE2`, `0x8C2FBB` | **memset via tabela de thunks** (assinatura CRT: `rcx`=dst, `edx`=0, `r8d=0x3F8`; ver `0x8C1B86`–`0x8C1B9A`): zera `rbp+0x2A8..0x69F`. Identidade exata **NÃO PROVADA** (salta por `jmp [rip+…]` em `0x1798F42`). |

Soma: 1+3+12+5+9+4+4+4+4+8+4 = **58**.

### C.3 Offsets de estado (`[reg+disp]`, disp ≥ 0x100) — todos os acessos

Não existe **nenhuma escrita** em `[obj+disp ≥ 0x100]` neste corpo: todos os acessos abaixo são leituras (`mov`, `movsxd`, `movzx`, `cmp`). As únicas escritas de estado são `[arg3+0x18]` (bump da arena, disp < 0x100, em `0x8C154F`, `0x8C157F`, `0x8C15C9`… e dentro de `0x8CAFD0`) e os buffers apontados pelos descritores.

| base | disp | tipo | acessos (RVA) |
|---|---|---|---|
| `rdx` (arg2) | `+0x400` | i32 contagem | `0x8C1467` (`cmp …,2`; guarda `0x8C1474 jle 0x8C32AD`) |
| `rdx` (arg2) | `+0x404` | i32 comprimento | `0x8C14B0` |
| `rsi` (=arg2) | `+0x404` | i32 comprimento | `0x8C1582`, `0x8C15FB`, `0x8C167A`, `0x8C16F3`, `0x8C1787`, `0x8C179F`, `0x8C17C3`, `0x8C1B7F`, `0x8C283E`, `0x8C288A`, `0x8C28D6` (11×) |
| `r15` (descritor) | `+0x404` | i32 | `0x8C2032` |
| `rax` (descritor) | `+0x404` | i32 | `0x8C291F` |
| `rcx` (arg6) | `+0x404` | i32 | `0x8C2DCD`, `0x8C31BA` |
| `rdi` (descritor) | `+0x404` | i32 | `0x8C2BDB`, `0x8C2FB4` |
| `r8` / `rdx` (=arg5=inst) | `+0x2C38` | **ponteiro** p/ bloco de parâmetros | `0x8C19CF`, `0x8C19DF`, `0x8C19EF`, `0x8C19FF`, `0x8C1A0D`, `0x8C1A1B`, `0x8C1A64`, `0x8C2AB0` (8×) |
| `rax` (=`[[inst+0x2C38]]`) | `+0x2C`, `+0x30`, `+0x34`, `+0x38` | f32 (4 coeffs) | `0x8C19D6`, `0x8C19E6`, `0x8C19F6`, `0x8C1A06` |
| `rax` (=idem) | `+0x1BF` + `i*8` | u8 flags (i = 0..4) | `0x8C1A14` (i=0), `0x8C1A6E`, `0x8C2ABA` |
| `rax` (=idem) | `+0x1C7` | u8 flag | `0x8C1A22` |
| `[inst+0x10]` | — | ponteiro p/ `{begin,end}` de registros de 0x18 B | `0x8C1A77`, `0x8C2AC3` |
| registro `[r12]` / `[r12+8]` | +0 / +8 | i32 índice de banda / índice de plano | `0x8C1AB0`, `0x8C2AF0`, `0x8C2DC3`, `0x8C31B2`; avanço `add r12,0x18` em `0x8C2DFD` |

### C.4 Blocos que leem parâmetros (com a origem do ponteiro)

**C.4.1 Bloco de leitura única por bloco — `0x8C19C8`–`0x8C1A38` (o único ponto que toca `[inst+0x2C38]` fora do laço)**

```
0x8C19C8  mov  r8,  [rbp+0x13D0]      ; r8  = arg5 = inst
0x8C19CF  mov  rax, [r8+0x2C38]       ; rax = params*            (1ª de 8 leituras)
0x8C19D6  mov  eax, [rax+0x2C]        ; p0
0x8C19D9  mov  [rbp+0xC0], eax        ; guarda local (f32)
0x8C19E6  mov  eax, [rax+0x30]        ; p1
0x8C19E9  mov  [rbp+0xC4], eax
0x8C19F6  mov  eax, [rax+0x34]        ; p2
0x8C19F9  mov  [rbp+0xC8], eax
0x8C1A06  mov  eax, [rax+0x38]        ; p3
0x8C1A09  mov  [rsp+0x28], eax
0x8C1A14  movzx ecx, byte [rax+0x1BF]; flag por slot (i=0)
0x8C1A22  movzx edx, byte [rax+0x1C7]; flag global
0x8C1A2B..0x8C1A38: [rbp+0x13E8] = (cl == 0 && dl == 0)   ; arg8 é SOBRESCRITO
```

Onde esses valores são consumidos (prova de que são coeficientes de ganho):

```
0x8C2A70  movss xmm8,  [rbp+0xC0]     ; g0
0x8C2A79  movss xmm12, [rbp+0xC4]     ; g1
0x8C2A82  movss xmm13, [rbp+0xC8]     ; g2
0x8C2A8B  movss xmm14, [rsp+0x28]     ; g3
0x8C2CCF  subss xmm6, xmm8            ; xmm6 = 1.0 - g0        (xmm10=1.0 em 0x8C2A5C)
0x8C2DE6  movaps xmm1, xmm8  → 0x8C2DEA mulss xmm1, xmm11 (0.5)   ; g0*0.5
0x8C2F3F  movaps xmm6, xmm12          ; variante g1
0x8C2F50  movaps xmm6, xmm13          ; variante g2
0x8C2E9B  movaps xmm6, xmm14          ; variante g3
```

E o par de operações aplicado com o coeficiente escolhido:

```
0x8C2DB8  rcx = [rbp+0x13D8]          ; arg6 (descritor com +0x404 = len)
0x8C2DC3  rax = [r12+8]               ; índice de plano do registro de banda
0x8C2DC8  xmm0 = 1.0 - xmm8           ; (1 - g)
0x8C2DCD  edi = [rcx+0x404]           ; len
0x8C2DD6  rbx = [rcx + rax*8]         ; buffer alvo
0x8C2DDD  call 0x1220                 ; alvo *= (1 - g)
0x8C2DE6  xmm1 = g
0x8C2DEA  mulss xmm1, 0.5             ; g/2
0x8C2DF2  r8 = rbx                    ; mesmo buffer como dst
0x8C2DF5  call 0x11F0                 ; alvo += estagiado * (g/2)
```

**C.4.2 Filtro por slot (tabela estática) — `0x8C1A4D` e `0x8C1A60`–`0x8C1B74`**

```
0x8C1A4D  lea rax, [0x2014360]        ; int32[8] = {8, 9, 10, 6, 5, 0, 0, 0}
0x8C1A60  movsxd r9, [rax+rcx*4]      ; código do slot (5 iterações: 0x8C234D cmp rax,5)
0x8C1A64  rax = [r8+0x2C38]           ; params*
0x8C1A6E  movzx ecx, [rax+rcx*8+0x1BF] ; flag do slot
0x8C1AB0  r8d = [r13]                 ; índice lido do registro de banda
0x8C1AB4..0x8C1B69: predicado(código, índice)  → escolhe o caminho
```

O predicado inline (`0x8C1ABD`–`0x8C1B69`) é idêntico ao de `0x61B790`:
`código==0 → true`; `1 → idx!=10`; `2 → idx!=9`; `3 → !(9<=idx<=10)`; `4 → !(8<=idx<=10)`; `5 → !(16<=idx<=18)`; `6 → (4)&&(5)`; `7 → !(8<=idx<=9)`; outro → `idx == r9d`.

**C.4.3 Segundo laço (`0x8C2AA5`–`0x8C3220`)** — repete `0x8C2AB0 rax=[rdx+0x2C38]`, `0x8C2ABA` (flag do slot), `0x8C2AC3 rax=[rdx+0x10]` (lista de bandas) e aplica o par `0x1220`+`0x11F0` com o coeficiente selecionado (C.4.1).

### C.5 As 6 ops escalares do próprio corpo

| RVA | instrução | leitura |
|---|---|---|
| `0x8C2CCF` | `subss xmm6, xmm8` | `1.0 - g0` (xmm6 = 1.0 em `0x8C2CC4`, xmm10 = 1.0f em `0x8C2A5C`) |
| `0x8C2DC8` | `subss xmm0, xmm8` | `1.0 - g0` (variante do bloco de mistura) |
| `0x8C2DEA` | `mulss xmm1, xmm11` | `g0 * 0.5` (`xmm11 = 0.5f` em `0x8C2A67`) |
| `0x8C30AF` | `subss xmm7, xmm6` | `1.0 - g` (segunda metade do laço) |
| `0x8C31B6` | `subss xmm0, xmm6` | `1.0 - g` |
| `0x8C31D5` | `mulss xmm6, xmm11` | `g * 0.5` |

Nenhuma delas é a conta do detector: são o **coeficiente de mistura** (`1-g` no alvo, `g/2` no sinal estagiado) aplicado por `0x1220`/`0x11F0`.

---

## Constantes (bits)

| RVA | bits (`hex`) | valor | onde é usada |
|---|---|---|---|
| `0x2079DB0` | `0x3DCCCCCD` | `0.10000000149011612` | `0x8C3C43` (`alpha` do one-pole, seção B) |
| `0x2079CEC` | `0x33D6BF95` | `1.0000000116860974e-07` | `0x8C2367` (`xmm6`) → `xmm2` do clamp `0x1100` em `0x8C238D` |
| `0x2079F9C` | `0x3F800000` | `1.0` | `0x8C2A5C` (`xmm10`, base do `1.0 - g`) |
| `0x2079EA8` | `0x3F000000` | `0.5` | `0x8C2A67` (`xmm11`, fator `g/2`) |
| `0x1DF9DA0` | `0x3F800000` (vetor) | `1.0` | `0x6368F` — substitui divisor zero na divisão `0x63640` |
| `0x2014360` | — | `int32[8] = {8,9,10,6,5,0,0,0}` | `0x8C1A4D`, `0x8C2356`, `0x8C2AA5` (códigos de slot) |
| `0x21C7408` | — | `i32 = 4` | `0x1580`, índice do thunk IPP |
| `0x21C6488` | — | tabela de ponteiros | `0x1580`, entrada `0x199BCCE0` → RVA `0xCCE0` |
| `0x207A360` | `0x41200000` | `10.0` | **não referenciada** por `0x8CAE90`/`0x8C3C20`/`0x8C1440` (consta do enunciado; fica registrada, sem uso provado nesta região) |

---

## NÃO PROVADO (explícito)

1. **Domínio absoluto das grandezas nos descritores de `0x8CAE90`.** As instruções provam `float32` e ausência de `ln/exp/pow`; não provam se o valor é amplitude linear, magnitude de FFT ou ganho linearizado. Nenhum nome de parâmetro foi usado para decidir.
2. **Identidade de cada descritor em `0x8C02F0`** (arg1/arg2/arg3/arg4/arg5): o encadeamento dos dois MACs está provado (`arg3 += bandas*arg1`, `arg1 += bandas*arg4`), mas *qual* curva/parâmetro cada um representa não foi ligado a nenhum nome.
3. **Relação entre os dois layouts de descritor** (`count@+0x80` vs `count@+0x400`). Está provado que os dois formatos existem e são lidos nos offsets citados; a regra de quando cada um é usado fora destes três alvos não foi estabelecida.
4. **`0x17978C0`** — trata-se de sonda de pilha (`sub rsp,rax` logo depois), mas a função não foi dissecada; nome/identidade não provados.
5. **`0x1798F42`** — memset por tabela de saltos (`jmp [rip+…]`), consistente com `memset(dst,0,0x3F8)`, mas a tabela de destinos não foi resolvida; identidade não provada.
6. **`0x61B790`** — provado que devolve `bool` a partir de `(código, índice)` com uma cadeia fixa de comparações; **o significado dos códigos 0..7 e do índice não foi provado**.
7. **Índice de banda (`[registro]`, 0x18 B por registro)** — provado que é comparado com 8..18; não provado o que ele indexa (banda FFT? grupo?).
8. **Semântica do par `*= (1-g)` / `+= estagiado*(g/2)`** (`0x8C2DC8`–`0x8C2DF5`): a aritmética está provada; se é crossfade dry/wet, mix de detector ou recombinação de bandas **não está provado**.
9. **`g0..g3`** (`[params+0x2C/0x30/0x34/0x38]`) — provado que são 4 coeficientes f32 lidos uma vez por bloco e selecionados por código de slot (`0x8C2E9B`/`0x8C2F3F`/`0x8C2F50`/`0x8C2DB8`); **o mapeamento para nomes de parâmetro do plugin não foi feito**.
10. **Curva vs. áudio em `0x8C3C20`** — provado o filtro (one-pole `a=0.1`, duas passadas, in-place, semente nas bordas); não provado se o vetor suavizado é uma curva de ganho ou amostras de áudio. Só o chamador `0x8B7240` foi lido o suficiente para provar que recebe uma **cópia** do descritor.
11. **`0x8C1440`: papel de `arg7` (`rbp+0x13E0`)** — lido em `0x8C245B`, `0x8C2845`, `0x8C3226` e usado como descritor, mas não foi rastreado até o tipo.
12. **Guard `cmp [rdx+0x400],2 / jle return` (`0x8C1467`)** — provado o teste; não provado por que a função exige contagem > 2.

---

### Resumo (12 linhas)

1. `0x8CAE90` **não faz conta**: é adaptador de layout que chama o thunk `0x1580` → `0xCCE0` → `0x65EA0` → kernel `0x6CE80`.
2. O kernel é `dst += a*b` (`vfmadd213ps ymm1,ymm0,[r8]` em `0x6CEBB`, store em `0x6CEC4`): **MAC em float32 linear**, sem `ln/exp/pow/div`.
3. Papel dos args de `0x8CAE90`: `rcx`=descritor **destino** (`dst.p[i] += src1.p[i]*src2.p[i]`), `rdx`=fonte 1 (count `+0x400`), `r8`=fonte 2 (count `+0x80`), `len` de `[dst+0x84]`.
4. Três layouts provados: tudo planar (`0x8CAEF0`), fonte 1 planar + fonte 2 broadcast (`0x8CAF3B`), ambas broadcast (`0x8CAF7F`/`0x8CAF82`).
5. `0x8C02F0` usa isso 2× e o encadeamento fica `arg3 += bandas*arg1` (`0x8C099C`) e `arg1 += bandas*arg4` (`0x8C0AE5`).
6. `0x8C3C20` é **one-pole de 2 passadas** (`y += (x-y)*0.1f`, `0x8C3C9A/9E/A2`), in-place (`0x8C3CAE`), reversa semeada por `y[len-1]` (`0x8C3D5C..0x8C3D71`).
7. `0x8C3C20` **não é attack/release**: alpha único `0x3DCCCCCD = 0.1` (`0x2079DB0`), zero `abs`/`maxss`/`minss`/seleção de coeficiente.
8. `0x8C1440` (7.800 B, 58 calls) é **estagiador**: 3 alocações de arena (`0x8CAFD0`), 12 memsets (`0x10D0`), clamps, soma, MAC, divisão e mistura.
9. Mapa completo dos 58 calls na seção C.2: `0x10D0`×12, `0x1370`×9, `0x61B790`×8, `0x1580`×5, `0x1100`×4, `0x1550`×4, `0x1220`×4, `0x11F0`×4, `0x1798F42`×4, `0x8CAFD0`×3, `0x17978C0`×1.
10. Estado: nenhuma escrita em `[obj+disp≥0x100]`; leituras em `+0x400/+0x404` (descritores) e `[[inst+0x2C38]+0x2C/0x30/0x34/0x38, +0x1BF, +0x1C7]` (`0x8C19CF`–`0x8C1A22`).
11. Os 4 floats de parâmetro viram `g0..g3` e alimentam `alvo *= (1-g)` (`0x8C2DDD`) + `alvo += estagiado*(g/2)` (`0x8C2DF5`).
12. Aberto: domínio/nome das grandezas, identidade de `0x17978C0`/`0x1798F42`/`0x61B790`, mapeamento `g0..g3`→parâmetros, e se `0x8C3C20` suaviza curva ou áudio.

---

## Atualização 2026-11-25 — `0x1550`/`0x63640`

A linha da tabela acima ("dois `vfmadd213ps` (Newton)") descreve só o caminho de 8 lanes.
O laço de 16 lanes (`00063AF0`) refina o **recíproco** (`00063B24`/`00063B29`) e só então
multiplica por `num` (`00063B37`); as duas rotas **não** são equivalentes no ULP. Despacho
completo (cabeça/16/8/resto) em `checks/r_divisao_63640.md`.
