# Verificação das entregas K–O (2026-11-24)

Método: cada item abaixo foi reconferido **por mim** com desmontagem nova (Capstone sobre o
dump), lendo a janela citada. O que passou está marcado `OK` com a instrução; o que não foi
reconferido continua `A CONFERIR` e **não** entra em plano/spec como prova.

Fonte: `dumpsooth/nyx_soothe3_dump.bin`, SHA-256
`68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`.

---

## K — `checks/k_core.md` (49 KB)

| Claim | Verificação |
|---|---|
| F1: `state+4` lido cru como f32 | **OK** — `008B507C mov eax,[rax+4]`, `008B507F movd xmm1,eax` (bit-copy, não `cvtsi2ss`) |
| F1: clamps 0/1 e `20x-60` → dB | **OK** — `008B5083 maxss xmm1,xmm13`, `008B5088 minss xmm1,xmm11`, `008B508D mulss 20` (`0x207A3B0`), `008B5095 subss 60` (`0x207A474`) |
| F1: `10^(0.05·dB)` por `powf` | **OK** — `008B509D mulss xmm10` (0.05), `008B50A2 call 0x1C9AA01` (powf), `008B50B1 mulss xmm7,xmm6` |
| F2: `P = Σ buffer[k]·coef[32]`, `g = P·10^(−0.45)` | **OK (estrutura)** — `008B539B r8d=0x20`, `008B53AB rdx=0x2077680`, `008B53B2 call 0x1400`, `008B537C powf`, `008B53C6 mulss xmm6,xmm7` |
| F2: `0x1400` = produto escalar (`0xAC20` → `0x5F5C0`) | **OK** — `0x1400` lê `0x21C6288[4]` = `0x199BAC20` → `0xAC20`; corpo `0000AC46 call 0x5F5C0`; `0x5F5C0`: `vmulss xmm2,xmm1,[rcx+rax*4]` (`0005F646`/`0005F6E6`), `vaddss xmm0,xmm2,xmm0` (`0005F64E`/`0005F6EE`), `vfmadd231ps` (`0005F68D`), store `vmovss [r9],xmm0` (`0005F6F7`) ⇒ `out = Σ a[i]·b[i]` |
| F3: `s = −0.25 − 0.25·powf(state+4,4)` | **OK** — `008B6582 xmm1=4.0` (`0x207A2B8`), `008B658E call powf`, `008B6627 mulss 0.25`, `008B663E movss −0.25`, `008B6646 subss xmm6,xmm7`, `008B6659 call 0x1220` |
| F4: `exp(clamp(state+0)·(ln(2+1/3−x²)+1.0996)−1.0996) − 1/3` | **OK** — `008B7AFC 2.0`, `008B7B04 mulss x²`, `008B7B09 subss`, `008B7B0E addss 1/3` (`0x2079E54`), `008B7B16 logf` (`0x1C9A9FB`), `008B7B1B subss −1.0996` (`0x207A6AC`), `008B7B23-2D clamp`, `008B7B36 subss 1.0996` (`0x2079FC0`), `008B7B3E expf` (`0x1C9A9D7`), `008B7B4D subss 1/3` |
| F5: gate `[engine+0x48] > 2` | **OK** — `008B3FCC cmp qword [r13+0x48],2`, `008B3FD1 seta byte [rbp+0x4A20]` |
| F5: `0x8C3F10` sob o gate + dois `logf(powf(10,·))` | **OK** — `008B868B call 0x8C3F10`; `008B869C powf(10,−3)` (`0x207A6E4`), `008B86A1 logf`; `008B86BB powf`, `008B86C0 logf`; `008B86AF mulss −0.05` (`0x207A66C`) |
| `0x8C33D0` transcrição | **OK nas primitivas** — `0x11C0` → `0x50E0` (`vsubss/vsubps`, `00005186`/`000051AC`); `0x11F0` → `0x5BC0` (`vfmadd213ss`, `00005C46`); `0x1250` → `0x69C0` (`vminss xmm0,xmm0,xmm3`, `00006A65`); `0x1100` → `0x3480` (`vminps`, `00003520`). A leitura de `+0x400/+0x404` em `008C34BD`/`008C34C7` não foi relida linha a linha |
| Satélites `0x8AE6F0`, `0x8C3F10`, `0x8C42D0`, `0x8C32C0`, `0x8C3E00` | **OK** — `0x8AE6F0` (contínua além do `.pdata` em `008AE78F`): `memset` `008AE72A`, `memcpy` `008AE87C`/`008AE8A5`/`008AEA00` (`0x1798F36`), `0x86F170` `008AE968`, `0x10A0` ×2 `008AE984`/`008AE9A3`. `0x8C3F10`: `0x61B790` ×2 (`008C40A1`/`008C40B5`), `memset` `008C4123`, `0x10D0` `008C4225`. `0x8C42D0`: `0x1220` ×2 (`008C43D0`/`008C43E2`). `0x8C32C0` → `0x8CB040` (`008C33BD`); `0x8C3E00` → `0x8CB2F0` (`008C3EFD`) |

**Correção material ao item (f):** K marca a semântica de `0x293760` (alvo de `0x1C8500`) como
`NÃO PROVADO`. Está **errado**: o corpo carrega `ln 2` = `0.693147182` de `0x1ECAE40` em três
pontos (`002939C7`, `00293A3B`, `00293D0D`) e os coeficientes da série de `ln(1+x)`
(`0x1ECAC20..0x1ECAE00`: `0.333365649`, `−0.250046641`, `0.198225036`, `−0.164624572`,
`0.169648811`, `−0.151772052`). Mantém-se a identificação **`0x1C8500` = ln** (spec §10.4).

## L — `checks/l_filtro.md` (22 KB)

| Claim | Verificação |
|---|---|
| `+0x80` do descritor é **contagem** comparada com 1, não flag booleana | **OK** — `008832C1 cmp eax,1` (eax de `[rsi+0x80]` via `movd`), `008832D0 jne`; idem `00883371`/`00883374` |
| `0x87BB60` = multiplicação de curva de ganho no domínio espectral (sem recursão por amostra) | **OK (negativa)** — varredura completa chain-aware (`show_func.py`, 1.641 linhas, 8.136 B): exatamente **23** ops float (`5 mulss, 5 subss, 4 addss, 4 maxss, 4 minss, 1 divss`), todas escalares em registrador nos clusters `0087BBF0`–`0087BCAE`, `0087CAA0`–`0087CC28`, `0087D030`; nenhuma acumulação float com operando de memória indexado. Não há `a1/a2` nem histórico por amostra |
| `0x1100` modo 4 = `min`, modo 0 = `max` | **A CONFERIR** (spec §17 já tem a assinatura; modo não relido aqui) |
| `0x87E220` = clamp `[10^−4.8, 10^2.4]` | **A CONFERIR** — constantes `0x207A1E8`=2.4 e `0x207A6F0`=−4.8 citadas |

## M — `checks/m_analise.md` (21 KB)

| Claim | Verificação |
|---|---|
| Nº de bandas é runtime; produtor `[engine+8]` | **OK com correção** — é `008AD310 mov rbx,[rax+0x48]` (o `.md` cita `008AD314`, que é `mov [rbp+0x11b0],rsi`). `008AD301 mov rax,[rcx+8]`; `008AD30C mov r15,[rax+0x40]` |
| Contagem lida em `0x8B8E70` | **OK** — `008B8F61 movsxd r12,[rbp+0x1090]`, `008B8F57 movsxd r14,[rbp+0x1094]` |
| "Sem magnitude/potência, sem dBFS, sem tilt" | **PARCIAL** — negativa ampla; sustenta-se no mapa de `call` (20 sítios) relido pelo agente, não por mim |
| `0x8BA7B0` vs `0x8A1EE0`: 9 bytes diferem, flag = 5º arg | **A CONFERIR** |

## N — `checks/n_canal.md` (22 KB)

| Claim | Verificação |
|---|---|
| Ordem: núcleo **antes** das análises | **OK** — `008AD601 call 0x8B3ED0`; depois `008AD9FA call 0x8B8E70`, `008ADC52 call 0x8B9E40`, `008ADF9B call 0x8BA1B0`, `008AE096 call 0x8BA7B0`, `008AE5EC call 0x8A1EE0` |
| `0x8C1440`/`0x8C0BD0` rodam **dentro** do núcleo | **OK** — já provado em H: `008B605C/606E` e `008B80DC/80EE` |
| Ramos por `[state+0x58]` e `[state+0x52]` | **A CONFERIR** (byte lido no ramo de `0x8AD75B`, não relido por mim) |
| Modelo de objetos (`X=[engine+8]`, `+0x40`/`+0x48`) | **PARCIAL** — `[rax+0x40]`/`[rax+0x48]` confirmados em `008AD30C/310`; resto não relido |

## O — `checks/o_saida.md` (28 KB)

| Claim | Verificação |
|---|---|
| `0x899940` não tem aritmética de estéreo (0 float) | **OK (contagem)** — 0 `*ss/±ss` no corpo de 2.412 B; os 8 `call` são cópia/despacho |
| Único peso numérico: `gain = arg2/arg3` | **OK (sítio)** — `008AD0B9 divss xmm6,xmm0`, com `008AD0AA cvtsi2ss` e `008AD0B3 mov ecx,[rbp+0x5F0]`; loop único `008AD0E0` |
| Ring: `w/r/len` em `+0x110/+0x114/+0x118`, `len=0x10000`, avanço `(r+n)&(len−1)` | **OK** — `008ACC5D/66/75/7E/82/85`, `008ACD06-0E`, `008ACD6B-79` |
| Lei de estéreo (link/focus/mid/side) | **NÃO PROVADA** — o `.md` também a marca assim; candidatos `byte[ctx+0x51]` e flags `ctx+0x2C40..0x2C45` |

---

## Conclusões que entram como prova

1. **K**: as cinco faixas estão transcritas e conferidas nas instruções-chave; `0x1400` e
   `0x8C33D0` e os satélites ainda exigem leitura minha.
2. **L**: o `+0x80` é contagem de ponteiros (não flag) — prova fechada. A conclusão "sem filtro
   temporal em `0x87BB60`" é plausível e coerente com 0 ops por amostra, mas fica **PARCIAL**
   até a varredura completa do corpo.
3. **M**: número de bandas é runtime; corrigir o RVA `008AD314` → `008AD310`.
4. **N**: a ordem "análise → núcleo" está **refutada**; núcleo vem primeiro.
5. **O**: não há lei de estéreo em `0x899940`; o ganho de overlap-add é uma divisão única.

**Pendência de verificação (minha):** corpo completo de `0x87BB60` (fechado na 2ª rodada),
modos de `0x1100` (fechados), diffs `0x8BA7B0`/`0x8A1EE0` (fechados), ramos de `0x8AD2B0`
(pendente).

---

## Segunda rodada — pendências residuais (2026-11-24)

### 1. Cabeçalho de B em `0x8C33D0`: `+0x400/+0x404`

```
008C34BD  movsxd rsi, [rbp+0x744]     ; = B+0x404 (len), lido da cópia de B em [rbp+0x340]
008C34C7  movsxd r12, [rbp+0x740]     ; = B+0x400 (count)
```

`B` é o descritor de `0x410 B` que `0x8B3ED0` monta na pilha em `[rbp+0x1050]`
(`008B6A16 lea rdx,[rbp+0x1050]`, chamada em `008B6A7E`). O formato `ptr[128] + header
{2,N,N*4}` já está provado (H, spec §8.4).

**NÃO é `0x8C32C0` que escreve esse header:** `0x8C32C0` *copia* A e B para a pilha
(`008C32E7`–`008C33A3`) e escreve o resultado em `arg1+0x1A0`
(`008C33A6 lea r8,[rcx+0x1a0]`, `008C33BD call 0x8CB040`), sem tocar `B+0x400`.

**`NÃO PROVADO`:** quem preenche `[rbp+0x1050]+0x400/+0x404` antes de `008B6A7E`. A cadeia
para em `008B6A16` (o descritor já está montado quando é passado).

### 2. `0x8BA7B0` vs `0x8A1EE0` — diff fechado

Comparação instrução a instrução (60 instruções cada, `checks/p_8a1ee0.dis` vs
`checks/m_8ba7b0.dis`): **3 diferenças totais**, sendo 2 deslocamentos de branch
(`008BA7D0` vs `008A1F00`, `008BA840` vs `008A1F70`) e **uma** diferença semântica:

```
008BA80?  mov byte ptr [rsp+0x20], 1        ; 0x8BA7B0
008A1FC9  mov byte ptr [rsp+0x20], r10b     ; 0x8A1EE0, com r10 = 0 (contador do laço de 8)
```

Portanto o único parâmetro que difere é o **5º argumento (byte na pilha)** passado a
`0x8B35A0`: `1` em `0x8BA7B0`, `0` em `0x8A1EE0` (o `r10b` vale 0 porque o laço
`008A1FBD sub r10,1 / 008A1FC1 jne` termina com `r10 = 0`). Não é um valor vindo do
chamador — é constante em cada função.

### 3. `r13` em `0x8B68AB` = **argumento 1 de `0x8B3ED0`**

```
008B3F14  mov r13, rcx          ; r13 = arg1 do núcleo (o mesmo objeto lido em [r13+0x2C38])
```

Logo `[r13+0x58]` (gate, `cmp byte`) e `[r13+0x60]` (divisor, lido como `qword` inteiro 64
bits em `008B68BC`) são **campos do objeto de contexto**, não do bloco de estado
(`state = [ctx+0x2C38]`). **`NÃO PROVADO`:** que `[ctx+0x60]` seja a taxa de amostragem; a
aritmética é `(t / [ctx+0x60]) · 0.001 · 500`, o que não é dimensionalmente `t·fs/1000`.

### 4. `0x86F170` (chamado por `0x8AE6F0` em `008AE968`)

457 B; chama `0x86F340` em `0086F210`/`0086F2E0` e `0x860B90` em `0086F271`.
**`NÃO PROVADO`:** identidade funcional.

### 5. Modos de `0x1100` (`0x3480`)

`00003520 vminps ymm1, ymm0, [rcx+r9*4]` + `0000352D vmovups [rcx+r9*4], ymm1` —
`dst[i] = min(bound, dst[i])`. O mapeamento numérico **já estava provado** em
`PLANO_MOTOR_AUDIO.md` §17.2: `r9d==4` → min, `r9d==0` → max (`0x3495 test r9d,r9d;
je 0x35D9`). Fica **FECHADO**.
