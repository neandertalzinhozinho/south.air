# P — sobras de bit-exatidão (leitura própria, 2026-11-24)

Regra: cada item traz instrução + RVA. O que não fechou está em `NÃO PROVADO` com o RVA onde a
cadeia para. Nada aqui é estimativa.

---

## P1 — `ctx+0x5F8` e `ctx+0x5ED0`: não são ponteiros, são subobjetos embutidos

**Conclusão provada:** os dois endereços são objetos construídos *in place* na base do motor;
não existe "store de um ponteiro" nesses offsets.

| Fato | Instrução / RVA |
|---|---|
| construção do objeto em `engine+0x5F8` | `008638D6 lea rcx,[r14+0x5f8]` → `00863929 call 0x86a4e0` |
| construção do objeto em `engine+0x5ED0` | `00863994 lea rcx,[r14+0x5ed0]` → `008639E3 call 0x86a8c0` |
| `r14` = base do motor | `008634CA`/`00864057` (`r14 = rcx`, devolvido em `rax`) — já provado em G |
| destruição dos dois | `00862F89 lea rcx,[rbx+0x5ed0]` + `00862F90 call 0x863140`; `00862F95 lea rcx,[rbx+0x5f8]` + `00862F9C call 0x863140` |
| `rbx` = motor no destruidor | `00862F4A mov rbx,[rcx]` |

**Tamanho mínimo do subobjeto:** o destruidor `0x863140` zera ponteiros em `+0x58C0`
(`00863149`, `00863165`) e `+0x58A8` (`00863170`, `00863193`) e chama `0x8631C0` em `+0x2C50`
(`0086318C`). Logo cada instância tem **≥ 0x58C8 bytes**. O layout encaixa:
`0x5F8 + 0x58C8 = 0x5EC0`, e o outro objeto começa em `0x5ED0`.

**Seleção em `0x8774A0`** (caminho de saída):

```
008774AC  cmp  byte ptr [rax], 0        ; rax = [rcx] = flag do motor
008774AF  je   0x8774e6
008774BD  add  rcx, 0x5ed0              ; rcx = [rbx+0x10] + 0x5ED0
008774DB  call 0x880640                 ; caminho A
...
008774EA  add  rcx, 0x5f8               ; rcx = [rbx+0x10] + 0x5F8
008774F1  call 0x868730
0087751C  call 0x881050                 ; caminho B
```

**Os dois construtores diferem no modo de `0x873440`:** ambos chamam `0x873440`, mas
`0x86A8C0` passa `byte[rsp+0x28]=1` e `dword[rsp+0x20]=0x800` (`0086A91E`, `0086A923`), enquanto
o outro passa `0`/`0x100` (ver `0086A954`, `0086A959` no par). Os dois corpos têm 980 B e
diferem (comparação linha a linha em `checks/86a4e0.dis` vs `86a8c0.dis`). Qual dos dois modos
corresponde a `+0x5F8` vs `+0x5ED0` está na tabela acima.
**`NÃO PROVADO`:** o significado funcional dos dois modos (0x800 vs 0x100) — não inferir.

Artefatos: `checks/862f40.dis`, `checks/8634a0.dis`, `checks/8774a0.dis`, `checks/86a4e0.dis`,
`checks/86a8c0.dis`, `checks/863140.dis`, `checks/868730.dis`.

---

## P2 — callback `[rdx+0x50]` do setter `0x867D80`: é ponteiro de código, e **não** é campo da tabela `0x238E9B0`

**Provado no setter:**

```
00867D98  movsd xmm6, [rdx+0x28]     ; min (f64)
00867DBA  movsd xmm7, [rdx+0x30]     ; max (f64)
00867DFC  mov   rax, [rdx+0x50]      ; ponteiro de código
00867E10  call  rax                  ; callback(valor normalizado em xmm0 double)
00867E50  mov   eax, [rsi]           ; rsi = rdx → índice do parâmetro
```

**Contradição material com a leitura anterior de §3:** na tabela `0x238E9B0` (passo `0x68`), o
campo `+0x50` **não é ponteiro**: varrendo as 143 entradas (`tools/p_table_fields.py` →
`checks/p_table_fields.txt`) os valores distintos são `0`, `1`, `0x101`, `0x10001`. Além disso
`+0x28`/`+0x30` da tabela caem **dentro do nome** (`+0x14` + `char[0x2C]`), não são `f64`
min/max.

Logo o descritor que chega em `rdx` ao setter é **outra estrutura**, não a entrada de
`0x238E9B0`. O mapa índice→offset de G continua válido (o switch usa `[rdx]` e a numeração
0..142 com os mesmos cortes), mas o **elo descritor-de-runtime ↔ linha da tabela** é
`NÃO PROVADO`.

**`NÃO PROVADO`:** identidade do callback e quem monta o descritor de runtime. A cadeia para em
`00867E10` (call indireto): não há valor estático a resolver sem a instância viva.

Tabela de campos por entrada (`checks/p_table_fields.txt`): `+0x00` = 15 ponteiros distintos,
`+0x08` = 8, `+0x58` = 6, `+0x60` = 6 (todos em `0x319xxx`/`0x335xxx`/`0x336xxx`).
Exceção: **índice 0** tem `+0x00 = 0x2037268` e `+0x08 = 0x3` (não é ponteiro de código) —
registro de tipo diferente. `NÃO PROVADO` o motivo.

---

## P3 — bloco one-pole de `0x8B68AB`: onde está a taxa de amostragem (campo provado, identidade não)

Transcrição com RVA (`checks/p_8b68ab.dis`):

```
008B68AB  cmp  byte ptr [r13+0x58], 0     ; gate
008B68BC  mov  rcx, [r13+0x60]            ; inteiro 64 bits
008B68C8  cvtsi2ss xmm1, rcx              ; (com caminho para negativo em 008B68CF-008B68E0)
008B68E4  movss xmm0, [r13+0x20]          ; entrada tipo-tempo (f32)
008B68F2  divss xmm0, xmm1                ; / [r13+0x60]
008B68F9  mulss xmm0, [0x2079D24]         ; 0.001f
008B6901  mulss xmm0, [0x207A560]         ; 500.0f
008B6909  cvtps2pd xmm0, xmm0
008B690C  divsd xmm1, xmm0                ; 1.0 / x
008B6910  movsd xmm0, [0x207A030]         ; 0.1 (double)
008B6918  call  0x1c9a5ad                 ; pow (double)
008B6932  subsd xmm6, xmm0                ; 1 - pow(0.1, 1/x)   (xmm6 = 1.0 de 0x207A138)
```

**Provado:** o divisor é `(float)(int64)[r13+0x60]`; a entrada é `[r13+0x20]`; o gate é o byte
`[r13+0x58]`; as constantes são `0x2079D24`=0.001f, `0x207A560`=500.0f, `0x207A030`=0.1f64,
`0x207A138`=1.0f64.

**`NÃO PROVADO`:** identidade de `r13` e, portanto, se `[r13+0x60]` é a taxa de amostragem. A
aritmética `(t / fs) * 0.001 * 500` **não é dimensionalmente** `t·fs/1000`; nomear `[r13+0x60]`
de "sample rate" seria inferência. A cadeia de `r13` pertence ao bloco K (proveniência de
registrador dentro de `0x8B3ED0`) e fica lá.

---

## Resumo do que P fechou / não fechou

| Item de P (§23.15–P) | Estado |
|---|---|
| 1. store de `ctx+0x5F8`/`ctx+0x5ED0` | **FECHADO**: subobjetos embutidos, construtores `0x86A4E0`/`0x86A8C0` em `00863929`/`008639E3`, destruidor `0x863140` via `00862F90`/`00862F9C` |
| 2. callback `[rdx+0x50]` | **NÃO PROVADO**: é call indireto (`00867E10`); provado que não vem de `+0x50` da tabela `0x238E9B0` |
| 3. 16 buffers de `0x8C1440` | **FECHADO em 2026-11-25** (`q_8c1440_buffers.md`; §7d) |
| 4. sample rate em `0x8B68AB` | **PARCIAL**: campo `[r13+0x60]` e aritmética provados; identidade de `r13` `NÃO PROVADA` |
| 5. sabor da FFT | pendente |
| 6. linear phase | pendente |
| 7. `0x1400` / `0x86F170` | em execução pelo agente K |


---

## Segunda rodada de P (2026-11-24) - fechamento com RVA

### 7a. `0x86F340` e `0x860B90` - clones espelhados (PROVADO)

Desmontagem completa em `checks/p_86f340.dis` e `checks/p_860b90.dis`. Sao **83 instrucoes
cada**; a comparacao instrucao a instrucao da **21 linhas diferentes**, todas por alocacao de
registrador ou deslocamento de branch, **exceto o sentido dos argumentos**:

| | `0x86F340` | `0x860B90` |
|---|---|---|
| arg1 (`rcx`) | **fonte** | **destino** |
| arg2 (`rdx`) | **destino** | **fonte** |

Prova: `0x86F340` le `eax=[rcx+8]` (`0086F346`) e escreve `[rdx+8]` (`0086F35A`), `[rdx]=0`
(`0086F36E`), `[rdx+0xC]=r9d` (`0086F371`), `[rdx+0x10]=4*r9d` (`0086F375`). `0x860B90` faz o
inverso: `[rcx]=rdx` (`00860BA5`), `[rcx+0xC]=r9d` (`00860B9E`), `eax=[rdx+8]` (`00860BAA`),
`[rcx+8]=eax` (`00860BB2`), `[rcx+0x10]=4*r9d` (`00860BC5`).

Nucleo comum (provado nos dois): copia `n = [fonte+8]` qwords de `fonte` para `destino`,
somando `4*arg3` a cada qword - `paddq xmm0,xmm2` com `xmm2 = 4*arg3` (`0086F39C`-`0086F3F7`,
`0086F3FF`, `0086F404`-`0086F422`) e cauda escalar `add rdx,r9` / `mov [rax-8],rdx`
(`0086F460`-`0086F473`). O laco cobre o descritor **inteiro** a partir do indice 0.

Efeito mecanico: `dst_qword[i] = src_qword[i] + 4*arg3` para `i < [src+8]`, com cabecalho
`{0 @0, n @8, arg4 @0xC, 4*arg4 @0x10}`. **`NAO PROVADO`:** identidade/nome (deslocamento de
ponteiros de descritor; nao ha prova de que seja FFT).

### 7b. `0x86F170` - composicao dos dois clones (PROVADO mecanicamente)

`checks/p_86f170.dis` (457 B). Entradas e saidas provadas:

```
sub = [rcx+8]            ; 0086F18C
len = [rcx+0x18]         ; 0086F192
n   = [rcx]              ; 0086F1B2
d   = [sub+0x88]         ; 0086F1A8
esi = len - d + arg3     ; 0086F1A2 / 0086F1AF
monta descritor temporario [rbp-0x50]:
   [0]=0, [8]=n, [0xC]=d, [0x10]=4*d
   copia n ponteiros de [rcx+0x10]      ; 0086F1D7-0086F202
se esi > 0: 0x86F340(tmp -> out0, arg3 = len, arg4 = arg3_orig - esi)   ; 0086F210
senao:      0x860B90(out1 <- tmp, arg3 = 0,  arg4 = esi)                ; 0086F271
saida = 0x30 B em rdx: descritor0 @+0x00, descritor1 @+0x18             ; 0086F283-0086F29D
```

Resultado: **dois descritores de 0x18 B de cabecalho + lista**, o primeiro com os ponteiros
deslocados de `4*d` e o segundo sem deslocamento. Chamado por `0x8AE6F0` em `008AE968`.
**`NAO PROVADO`:** identidade (candidato: divisor de descritor para dois consumidores, mas o
nome seria inferencia).

### 7c. Sabor da FFT - exclusoes provadas, nome ainda `NAO PROVADO`

Fatos novos, todos com RVA:

- `n = [estagio+0x18]` (`008B2753 movsxd r15,[rax+0x18]`).
- mascara de posicao `n/2-1`: `008B275A shr rbx,1` + `008B275D lea rax,[rbx-1]` +
  `008B2761 test [rsi+0x140],rax`.
- `bins = n/2+1`: `008B28AA shr rdi,1` + `008B28AD inc rdi`; passado a `0x1520` em
  `008B28E2 mov r8d,edi`.
- inversa com `n`: `008B291F mov r8d,r15d`; escala `1/n` em `008B291C cvtdq2ps` /
  `008B2925 divss` / `008B2929 call 0x1220`.
- `0xBD40` percorre **todos** os bins a partir de 0 (`0000BDCC xor r10d,r10d`,
  `0000BDE0 vmovsd xmm3,[rdx+r10*8]`), 8 B por bin (par complexo interleaved), sem tratar o
  par 0 como DC/Nyquist.

Consequencia: o packing DC/Nyquist do **CCS** esta **excluido** para o par 0. `RToPerm` vs
`RToPack` (ordem dos bins) **continua `NAO PROVADO`** - distinguir exigiria ler quem monta o
espectro do filtro (a mesma ordem e aplicada dos dois lados, entao a ordem e transparente).
Construtor de `[spec]==7`: segue `NAO PROVADO` (§24.5).

### 7d. 16 buffers de `0x8C1440` - **FECHADO em 2026-11-25** (`q_8c1440_buffers.md`)

> **Correcao 2026-11-25.** Esta secao ficou desatualizada. A leitura instrucao a instrucao
> esta em `checks/q_8c1440_buffers.md`: pares 0/2/4/6 = `Sigma ch^2`, pares 1/3/5/7 =
> `Sigma ch` (unicos clampados), as 4 divisoes escrevem em alocacao nova (`new1/T1/T2/T3`),
> `A/B/C/D` somam os 2 canais, e o coeficiente e escolhido por `(enable, al, flag, tipo)`:
> `enable -> +0x2C`, `tipo 8/9 -> +0x30`, `tipo 6 -> +0x34`, `tipo 5 -> +0x38`, `tipo 10 ->
> nunca`. Resta `NAO PROVADO` so o nome/unidade dos 4 coeficientes, a faixa de `g`, a
> intencao musical e `nch > 2`.

O bloco H ja provou existencia, contagem e layout (spec §8.4; plano §23.15-(g)): 5 pares
inline + 3 chamadas de `0x8CAFD0` (2 cada) + 8 sitios de `0x10D0` em laco de 2 = 16 buffers.

### 7e. Linear phase - `NAO EXTRAIDO` como instancia; ganho e zero-fase por construcao

- `0x87DB30` (410 instrucoes, **0 ops float**) so despacha: `0x8833F0` (`0087DC3B`),
  `0x882DE0` (`0087DD8E`), `0x1340` x2 (`0087DE86`/`0087DEA9`, multiplicacao espectral),
  `0x1C8530` (`0087E0B0`, IPP) e `0x1220` (`0087E1E9`).
- `0x877D90` (37 B) so escreve flags: `byte[ctx+0x2BC8]=1` (`00877D92`) e
  `byte[ctx+0x2BB8+i]=1` (`00877DB2`) para `i < [ctx+0x48]`.
- Nao ha historico por amostra nem FIR nesses consumidores; o ganho entra como multiplicacao
  real de bins complexos (`0x1340` em `0087DE86`/`0087DEA9`), logo **fase zero** no estagio de
  ganho.

Uma instancia separada de FIR linear-phase **nao foi localizada** no caminho lido:
`NAO EXTRAIDO` (parada em `0x87E0B0`).
