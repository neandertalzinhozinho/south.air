# M6 — cadeia completa pela API do motor (2026-11-25, em andamento)

O motor inteiro foi traduzido mecanicamente a partir das entradas da API (`checks/v_miolo_m5.md`):
`lifted/src/gen_engine.rs`, com 437 funções e 111.559 instruções. O driver está em
`lifted/src/api.rs`. Daqui em diante, o oráculo (`host`, somente leitura) é a referência.

## 1. API do motor (instrução + medição)

O handle é devolvido por `0x862E40` (`00862E77..00862EE1`). Cada campo é um ponteiro de função:

| Campo do handle | Função | Papel |
|---|---|---|
| `+0x00` | — | `engine` (objeto de `0x8634A0`) |
| `+0x08` | `0x862EF0` | setter: `rcx = [rcx]`, `cvtsd2ss xmm2`, `jmp 0x867D80` |
| `+0x10` | `0x862F00` | process: `rcx = [rcx]`, `jmp 0x864410` |
| `+0x18` | `0x862F10` | `0x8689D0(engine, 1)` + `xchg [engine+0x4A], 1` |
| `+0x20` | `0x862F40` | ainda não lido |
| `+0x28` | `0x863020` | ainda não lido |
| `+0x50` | `0x863070` | ainda não lido |

### Create: `0x862E40(rcx = iface, rdx = config, xmm2 = taxa double)`

- **`iface`:** é uma interface do plugin, gravada em `[engine+0]` (`008634CD`). Funções medidas
  no oráculo:
  - `+0x18` = `0x338A60`: registra uma saída com nome, e o retorno é ignorado (`00863574..`);
  - `+0x20` = `0x338A80`: envia dados;
  - `+0x28` = `0x338BA0`: `movzx eax, byte [[iface]+0x94]`, **medido 0**.
- **Consequência da flag 0:** o `process` não chama `+0x20` (`00866730..00866735`,
  `0086733A`). No port, o stub de `+0x28` devolve 0, e `+0x20` vira `panic` se for chamado.
- **`config`:** **medida** no oráculo como dado estático `0x23923E0` (campo `+0x18` do
  descritor `0x23926F0`). Conteúdo: `{2,2,2,2,2,1,1,1,1,1,1,0,3,3,3,3,…}`.
  - `[cfg]` e `[cfg+8]` passam por `0x56B140` e dão `[eng+0x10] = 2` (entrada) e
    `[eng+0x14] = 2` (saída), também medidos.

### Process: `0x862F00(handle, rdx = in[], r8 = out[], r9 = 0, [rsp+0x28] = n)`

- `rdx[0..[eng+0x10])` é copiado para `[rbp+0x930]` (`00864518..0086453B`);
- `r8[0..[eng+0x10])` é copiado para `[rbp+0x7F0]` (`008645B4..008645EB`);
- com `r9 = 0`, `0x868510` monta a saída a partir de `[rbp+0x7F0]` (`00864617..0086462D`);
- o `n` vem do quinto argumento (`00864495 mov rbx,[rbp+0x3380]`).

`NÃO PROVADO`: o papel exato de `r8` quando `r9 ≠ 0` (sidechain?), e a sequência de chamadas que
o plugin faz por bloco (wrapper ofuscado). Isso será checado pelo null-test (M7).

## 2. Pendente

- Rodar `create` e `process` traduzidos (`lifted/src/bin/m6_run.rs`) e tratar o que parar
  (`NÃO SUPORTADO`/folhas).
- Estado inicial: comparar o estado `engine+0x54` do motor traduzido logo após o `create` com o
  medido no oráculo (`p0 = 0.5`, `p21 = 100`, …), para decidir se o plugin chama o setter com
  defaults.

## 3. Execução do motor traduzido (2026-11-25)

- **Estruturas `lifted/` e `lifted_extra/`:**
  - base com 691 funções;
  - extra com 72 funções descobertas em execução por `tools/lift/iterate_extra.sh`;
  - o extra inclui os kernels de FFT por ponteiro, a init da FFT, os geradores de twiddle, os
    handlers do setter e os callbacks plain↔norm.
- **Estáticos do dump:** o dump traz os estáticos já inicializados, apontando para o heap do
  processo original. A emulação reinicializa cada um na primeira vez:
  - `_Init_thread_header` `0x17969E0` vira handler e força `*guard = -1`;
  - o epoch TLS começa em `INT_MIN`, como no MSVC (o guard do dump `[0x2754C5C]` vale
    `0x80000018`).
- **`create` + defaults + flag `0x863070(h,1,1)`:** o estado do `engine[0..0x600]` fica
  **idêntico** ao do oráculo, a menos de ponteiros.
- **Latência pela API (`0x863020`) = 2304**, igual ao oráculo.
- **Ordem real dos buffers do `process`**, medida:
  `0x862F00(handle, rdx = SAÍDAS, r8 = ENTRADAS, r9 = sidechain/0, [rsp+0x28] = n)`. Com `r8 = 0`,
  a saída é 0; com `r8 = sinal`, a saída processada sai em `rdx` e `r8` fica intacto. Isso
  corrige a §1.
- **Seno 1 kHz a 48 kHz, 12000 amostras:**
  - o motor traduzido produz áudio, e **o início coincide com o plugin (amostra 1024)**;
  - no 1º bloco após o início, o pico é 0,487 no port e 0,484 no plugin.
- **Null-test ainda não fecha:**
  - o plugin oscila por bloco (0,506 / 0,465 / 0,462 / 0,521 …, pico 0,532);
  - o port decresce suave (0,441 → 0,387);
  - há 2106 amostras bit-iguais em 24000, quase todas zeros do início.
- **O motor traduzido é invariante ao tamanho de bloco:** blocos 64…4096 dão saída idêntica. O
  plugin depende do bloco, com lóbulos em `Fs/bloco` (`host/NOTAS.md` §9). Logo, **a diferença
  está no wrapper do plugin** (`processBlock` `0x350F20`, ofuscado), que faz algo a cada chamada
  além de chamar o motor.
- **Hipóteses testadas e descartadas:** sidechain = entrada; in-place; reenviar parâmetros a cada
  bloco; outro tamanho de bloco no motor.
- **Desempenho:** cerca de 0,5 s para 0,25 s de áudio, ou seja, **~2× mais lento que tempo
  real**.

## 4. Próximo passo de M7

Ler o `processBlock` do plugin (`0x350F20`, slot 6 da vtable `0x2037A58`) e o `0x3426A0`
(`this+0xE40`) para saber o que o wrapper faz por chamada. Candidatos: smoothing de parâmetro no
lado JUCE (`[W+0x30]` por bloco), mix dry/wet com o atraso, ou uma chamada ao motor com outro
argumento. O código é ofuscado (predicados opacos); a alternativa é traduzir o wrapper também.

## 5. M7 — NULL-TEST FECHADO (2026-11-25)

**O problema estava no oráculo, não no motor.** O host da etapa I tinha um bug de
(des)intercalação no laço de `process` (`host/src/main.rs`):

- a entrada fazia `in_l[..n] = samples[pos*2 .. pos*2+n]`, ou seja, o plugin recebia L,R,L,R…
  num canal só;
- a saída fazia `total[pos*2 .. pos*2+n] = out_l[..n]` e depois `out_r` deslocado 1, o que
  deixava metade de cada bloco sem escrita.

Daí vinham os 255 zeros por bloco de 512, a "dependência do tamanho de bloco" e os lóbulos em
`Fs/bloco` de `host/NOTAS.md` §8–§9. **Os WAVs de oráculo gerados antes de 2026-11-25 estão
errados.** Com a correção (intercalar e desintercalar por amostra):

| Sinal | fs | Bloco | Resultado (motor traduzido × soothe3 original) |
|---|---|---|---|
| Seno 1 kHz, 0,25 s | 48000 | 512 | **24000/24000 bit-iguais**, offset 0, `max|dif| = 0` |
| Ruído + senos, 1 s | 48000 | 512 | **96000/96000**, `max|dif| = 0` |
| Ruído + senos, 1 s | 48000 | 64 | **96000/96000** |
| Ruído + senos, 1 s | 48000 | 4096 | **96000/96000** |
| Ruído + senos, 1 s | 44100 | 512 | **88200/88200** |
| Ruído + senos, 1 s | 96000 | 512 | **192000/192000** (offset 0) |

- **Chamada usada no motor traduzido:** `create` (`0x862E40`, config `0x23923E0`), os 143
  defaults pelo setter (normalizado pelo callback `+0x48`), `0x863070(h,1,1)`, e depois
  `process` (`0x862F00`, `rdx = saídas`, `r8 = entradas`, `r9 = 0`) por bloco. A latência
  reportada é 2304 nos dois lados.
- **Ressalvas:**
  - o resultado vale na CPU do oráculo, porque `vrcpps`/`vrsqrtps` usam o hardware;
  - os caminhos AVX-512 não foram traduzidos e param com o RVA se forem executados;
  - o motor ainda lê as constantes do dump em tempo de execução;
  - o desempenho é ~2× mais lento que tempo real.

## 6. Desempenho do motor traduzido (2026-11-25)

Todas as mudanças são só de runtime e codegen; a aritmética e a ordem das instruções não
mudam. Depois de cada rodada, o null-test contra o soothe3 original segue **bit a bit** nas
5 configurações da §5. Nos modos low latency, high e ultra, a saída é idêntica à da rodada
anterior.

| Rodada (commit) | Mudança | 1 s a 48 kHz, padrão | Ultra |
|---|---|---|---|
| base (`8144e0f`) | `HashMap` de páginas, cópia por byte | 1,55 s | — |
| `a2f4d4f` | páginas em vetores e cache direto; despacho de blocos denso; chamadas diretas | ~0,25 s | ~0,93 s |
| `52c67d4` | AVX2/FMA habilitados no compilador; intrinsics inline | ~0,21 s | ~0,73 s |
| `0bb9844` | cache (tag, ponteiro) unificado; caminhos frios fora de linha; flags mortas eliminadas | ~0,20 s | ~0,58 s (melhor de 6) |

- **Latência pela API (`0x863020`):**
  - padrão = 2304;
  - **Low latency** (parâmetro 1 = 1) = **0**.
- **Custo relativo, em instruções executadas por 1 s de áudio:**
  - padrão: 103 M;
  - low latency: 270 M;
  - high (parâmetro 3 = 0,5): 197 M;
  - ultra (parâmetro 3 = 1): 384 M;
  - 96 kHz, padrão: 324 M.
- **Ferramentas:**
  - `M6_SET="i=norm,…"` aplica parâmetros depois dos defaults;
  - `M6_PROF=<arquivo>` grava o perfil por bloco (RVA, execuções, instruções);
  - `lifted_extra/.cargo/config.toml` e `resonia/app/.cargo/config.toml` ligam
    `+avx2,+fma`.
- **Pendente:** a validação bit a bit dos modos low latency, high e ultra contra o oráculo
  ainda não foi feita (o host oráculo roda só com os defaults).
