# M4 — identidades de estado: sample rate, `[ctx+0x60]`, objeto `E` e callback `[rdx+0x50]` (2026-11-25)

Fonte: dump `dumpsooth/nyx_soothe3_dump.bin`, onde o offset de arquivo é o RVA
e os ponteiros de dado usam VA na base `0x199B0000`.

- **Prova por instrução:** desmontagens novas em `checks/867d80_m4.dis`,
  `checks/3351e0.dis`, `3358f0.dis`, `335300.dis`, `335470.dis`, `335670.dis` e
  `335830.dis`, mais as já existentes `873440.dis`, `86a8c0.dis`, `8634a0.dis`,
  `862e40.dis` e `8ad2b0.dis`.
- **Ferramentas novas** (só leem o dump): `tools/find_callers.py`,
  `tools/find_refs_va.py` e `tools/gen_param_entries.py`.
- **Medição:** feita no processo somente-leitura do host com
  `host.exe` + `SOULTREE_PROBE=1` (§5).

## 1. Cadeia do sample rate (instrução)

```
0x861DB0 (create do descritor do motor; ponteiro em 0x2392718 = [0x23926F0+0x28])
  xmm1 (double) → xmm6 (00861DE0) ; xmm6 = maxsd(xmm6, 0.0) (008624EE)
  call 0x862E40 com xmm2 = xmm6 (00862DF6 / 00862E01)
0x862E40: new 0xC1A8 ; xmm3 = cvtsd2ss xmm2 (00862E68) ; call 0x8634A0 (00862E72)
          devolve handle: [h]=objeto, [h+8]=0x862EF0, [h+0x10]=0x862F00, … [h+0x50]=0x863070
0x8634A0 (this = engine): [eng+0x28] = a (0086352B)
          k = max(1, trunc((a + 1)·(1/44100)))  → [eng+0x2C] (00863531..00863552)
          call 0x86A8C0(rcx = eng+0x5ED0, xmm3 = a / k) (0086398C..008639E3)
0x86A8C0: ctx A = this+8      ← 0x873440(..., xmm3, arg5 = 0x800, arg6 = 1) (0086A913..0086A92B)
          ctx B = this+0x2C50 ← 0x873440(..., xmm3, arg5 = 0x100, arg6 = 0) (0086A935..0086A961)
0x873440 (construtor do ctx):
  [ctx+0x20] = max(xmm3, 44100.0f)                (0087346D / 008734C5)
  [ctx+0x28] = N = trunc([ctx+0x20]·(1/44100))·arg5 (008734CA..00873513)
  [ctx+0x38] = 2N ; [ctx+0x40] = N+1             (00873517..00873525)
  [ctx+0x58] = [ctx+0x59] = arg6 (gate)          (00873554 / 00873557)
  [ctx+0x60] = N>>2 (00873561), depois SOBRESCRITO:
  [ctx+0x60] = [ctx+0x28] >> 1 = N/2             (008769CA..008769D4)
```

O descritor `0x23926F0` tem estes campos:
`{+0x08: 0x238E9C0 (entradas de parâmetro), +0x10: 0x8F = 143, +0x18: 0x23923E0, +0x20: 0x40, +0x28: create 0x861DB0}`.

Ele entra no plugin pelo construtor do `Soothe3AudioProcessor`:

- vtable `0x2037A58` (`00344DA6`);
- `lea rdx, [0x23926F8]` (`00344DD6`) e depois `0x336E20`, que grava
  `[W+0x70] = 0x23926F8` (`00336EA6`), com `W = processor+0xE40` (vtable `0x2037178`).

A chamada de `create` com o `sampleRate` do host passa por código ofuscado do
wrapper (`0x861DB0` tem predicados opacos e `jmp r13`). Por isso esse elo foi
fechado por **medição** (§5), não por instrução.

## 2. `r13` de `0x8B3ED0` e `[ctx+0x60]`

- `0x8AD2B0` (`008AD4F9 mov rcx,[rdi+8]`) chama `0x8B3ED0` em `008AD601`, e
  `0x8B3ED0` faz `008B3F14 mov r13, rcx`.
- `r13` lê `+0x2BC8`/`+0x2C38`, campos que só o construtor `0x873440` grava
  (`00873E87`/`00873F06`).
- Em `0x8B68AB`:
  - o gate é `[r13+0x58]`, e só o ctx A tem `1`;
  - a entrada é `[r13+0x20]` = taxa efetiva do ctx;
  - o divisor é `[r13+0x60]` = **N/2 = 1024**. **Não** é sample rate; o rótulo
    anterior estava errado.

Na fórmula de `one_pole_coef`, isso vira
`x = (fs_ctx / (N/2))·0.001·500`, com `fs_ctx = max(a/k, 44100)`.

## 3. Objeto `E` de `0x864410` (resíduo de M1)

`[h+0x10] = 0x862F00` (`00862E9B`) é `mov rcx,[rcx]; jmp 0x864410`. Então o `E`
de `0x864410` é `[handle]`, isto é, o objeto que `0x8634A0` construiu.

- **Medido:** `[h]` é o objeto com `+0x28 = taxa` e `+0x5ED0` com os dois ctx.
- **Fecha o resíduo de M1:** `arg4` de `0x8634A0` é a taxa do host, e `n = 257`
  a 48 kHz vale porque `k = 1` e `N_B = 256`.

## 4. Callback `[rdx+0x50]` do setter `0x867D80`

- **Caminho do `rdx`:**
  - `0x33A630` é o slot 1 da vtable `0x2037178`;
  - nele, `rdx = [[W+0x70]] + idx·0x68 = 0x238E9C0 + idx·0x68`
    (`0033A642`..`0033A654`);
  - a chamada é `[W+0x30](rcx = [W+0x68] = handle, rdx, xmm2 = (double)valor)`;
  - `[W+0x30]` foi **medido** igual a `0x862EF0`, que faz `rcx = [rcx]`,
    `cvtsd2ss xmm2` e `jmp 0x867D80`.
- **No setter:**
  - `[rdx+0x28]`/`[rdx+0x30]` = min/max, em `double`;
  - o normalizado é limitado em `00867DC2..00867DF7`;
  - `00867DFC mov rax,[rdx+0x50]`, `00867E00 xmm1 = (double)norm`,
    `00867E10 call rax`, e o resultado vira `float` em `00867E1A`.
- **Correção de P2:** a refutação anterior leu a tabela com base `0x238E9B0`,
  deslocada em `0x10`. Com a base `0x238E9C0`, o campo `+0x50` das 143 entradas
  é código e cai em 6 famílias:

| RVA | n | Fórmula (`t = clamp(x)` pela seleção `cmov` + `maxsd`/`minsd`) |
|---|---|---|
| `0x3351E0` | 43 | `t·(max−min) + min` |
| `0x3358F0` | 43 | `x ≥ 0.5 ? 1 : 0` |
| `0x335300` | 35 | `lo + trunc(round(n·t))`, `lo/hi = trunc(round(min/max))`, `n ≤ 0 → lo` |
| `0x335470` | 8 | `exp((ln(max+150) − ln(min+150))·t + ln(min+150)) − 150` |
| `0x335670` | 8 | `exp(clamp(t^(−log2 r))·(ln max − ln min) + ln min)`, `r = (ln c − ln min)/(ln max − ln min)`, `c = [e+0x38]` |
| `0x335830` | 6 | `exp((ln max − ln min)·t + ln min)` |

Imports usados (`checks/thunk_map.txt` e o OFT): `log` `0x1C9A9EF`, `exp`
`0x1C9A9D1`, `pow` `0x1C9A5AD` e `round` `[0x1D8D7C0]`, todos da UCRT.

O port está em `port/src/params.rs`. As entradas (min, max, `+0x38` e
callbacks) estão em `port/src/param_entries.rs`, gerado do dump.

## 5. Medição somente-leitura (`host`, `SOULTREE_PROBE=1`)

O modo de sonda do `host` funciona assim:

1. depois do `process`, varre a memória privada RW do **próprio processo** por
   `VirtualQuery`;
2. acha o processor pela vtable `base+0x2037A58`;
3. lê `W = obj+0xE40`, `[W+0x68]` (handle), `engine = [handle]`, os dois ctx e o
   estado `engine+0x54`.

Não há escrita, hook nem injeção.

**Taxas do host** (as outras taxas foram liberadas só no modo de sonda; o resto
é igual em todas):

| fs do host | `[eng+0x28]` | `k` | `ctx+0x20` |
|---|---|---|---|
| 32000 | 44100 | 1 | 44100 |
| 44100 | 44100 | 1 | 44100 |
| 48000 | 48000 | 1 | 48000 |
| 88200 | 88200 | 2 | 44100 |
| 96000 | 96000 | 2 | 48000 |
| 192000 | 192000 | 4 | 48000 |

- **ctx A:** `N = 2048`, `N+1 = 2049`, `[+0x60] = 1024`, gate `1`.
- **ctx B:** `N = 256`, `N+1 = 257`, `[+0x60] = 128`, gate `0`.
- A 32 kHz, o motor recebe `a = 44100`: há um clamp a montante, no código
  ofuscado do create.
- **N não muda com fs.** A taxa interna fica em 44,1/48 kHz por decimação `k`.
  Isso **refuta** "N = 278 @48k / 557 @96k" da âncora (ver §23.14).

**Elos medidos:**
- `[W] = 0x2037178`;
- `[W+0x30] = 0x862EF0`, `[W+0x70] = 0x23926F8`, `[[W+0x70]] = 0x238E9C0`;
- handle: `+8 = 0x862EF0`, `+0x10 = 0x862F00`, `+0x18 = 0x862F10`,
  `+0x20 = 0x862F40`, `+0x28 = 0x863020`, `+0x50 = 0x863070`.

**Estado padrão, a 48 kHz** (`engine+0x54`, offsets do `checks/param_map.txt`):
- campos que guardam o valor do callback (`xmm6`): `p8..p13 = 1.0`,
  `p21 = 100.0` e `p25 = 0.5`, iguais ao `+0x38` de cada entrada;
- campos que guardam o normalizado (`xmm8`): `p0 = 0.5` (5/10), `p7 = 0.3`
  (3/10), `p17 = 1.0` e `p18 = 0.5`;
- campos derivados: `p23 = 2·asinh(1/(2·0.707))/ln2 = 1.9002` e
  `p24 = exp(ln6 + 0.5·(ln128 − ln6)) = 27.71`.

Conclusão: **`+0x38` da entrada é o valor plain default**.

## 6. Resíduo `NÃO PROVADO`

- **Elo host → `create`:** a chamada de `0x861DB0` com o `sampleRate` do host
  está em código ofuscado. Ela está fechada por medição, sem prova por instrução.
- **Clamp a 44100 em 32 kHz:** medido, mas a instrução que faz o clamp não foi
  localizada.
- **Outros chamadores de `[W+0x30]`:** foi conferido só o `0x33A630`; não
  enumerei todos.
- **Callbacks sem conferência dinâmica:** comparar `[rdx+0x50]` com o port
  valor a valor exige mandar parameter changes pelo host (fica para M6). Por
  enquanto há a transcrição e a consistência dos defaults (§5).
- **Callbacks `+0x48`/`+0x58`/`+0x60`** (plain→norm e texto): não lidos, porque
  não estão no caminho de áudio.
