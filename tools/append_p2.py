# -*- coding: utf-8 -*-
import io

p = r'D:\PROJETOS\soultree\checks\p_extras.md'
s = io.open(p, encoding='utf-8').read()

add = """

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

### 7d. 16 buffers de `0x8C1440` - `NAO EXTRAIDO` (semantica)

O bloco H ja provou existencia, contagem e layout (spec §8.4; plano §23.15-(g)): 5 pares
inline + 3 chamadas de `0x8CAFD0` (2 cada) + 16 `0x10D0` de zeragem. O que falta e o **papel
DSP de cada buffer**. Nao ha, no codigo, nome nem tabela que associe buffer a coeficiente:
a atribuicao seria inferencia. Fica `NAO EXTRAIDO: 0x8C1440` (mapa semantico dos 16 buffers).

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
"""

io.open(p, 'w', encoding='utf-8', newline='\n').write(s + add)
print('appended', len(add))
