# RETOMADA — ARQUIVO SUPERADO (não usar para trabalho)

> **Obsoleto desde 2026-11-23.** Este era o resumo curto de 2026-11-22 que mandava
> continuar a etapa **D0** (`0x8B2C30`). D0 fechou em 2026-11-23 (FIR de 32 taps) e,
> depois dela, A–P **e** I também fecharam. Seguir este arquivo produz retrabalho.
>
> Conteúdo original preservado em
> `archive/PROMPT_RETOMADA_4000.obsoleto-2026-11-22.md` — congelado, só histórico.

## Use estes

| Papel | Arquivo |
|---|---|
| Estado real e ordem das etapas | `PROMPT_RETOMADA.md` (sincronizado 2026-11-24) |
| Fonte de verdade | `PLANO_MOTOR_AUDIO.md` §23.12/§23.15/§25 |
| Especificação técnica | `docs/engine/dsp-spec.md` |
| Âncora do projeto | `LEMBRAR DISSO.md` (congelado) |

## Estado em 2026-11-24 (para não reabrir o que já está provado)

Fechadas com instrução + RVA: D0, A, B, C, D1, E, F, G, H, K, L, M, N, O, P, I e §24
(FFT no caminho de áudio; `0x20E0` direta, `0x7B40` inversa).

**J (port Rust) fechado:** J1/J2 (`checks/stage_j_core.rs`, 10 testes), J3
(`checks/stage_j_pipe.rs`, 12), J4 (`checks/j4_fft.rs`, 13 — ordens 8..19 e split `0x895C0`
rápido/lento bit a bit), J5 (`checks/stage_j_chan.rs`, 7) e J6 (`checks/stage_j_engine.rs`, 8).
**J0 (2026-11-25):** os kernels passaram a viver em `port/src/` (fonte única; os testes em
`checks/` apontam com `#[path]`); runner `powershell -File port\run_tests.ps1` = 57 J + 6
port, 0 falhas.

Falta o null-test plugin × port com alinhamento **2304** e o mesmo bloco. Ele depende de
fechar, nesta ordem: transcrever `0x8C1440` no port (leitura fechada em 2026-11-25,
`checks/q_8c1440_buffers.md`), `0x293760`/`0x240C00` (ln/exp bit a bit), recíproco de
`0x88E130`, sample rate (`[ctx+0x60]`) e então o port completo. `0x88300` e os geradores de
twiddle ficam `NÃO EXTRAÍDO` — fora do caminho de áudio (`PLANO_MOTOR_AUDIO.md` §24.5-(3)).
Ver `PROMPT_RETOMADA.md`.
