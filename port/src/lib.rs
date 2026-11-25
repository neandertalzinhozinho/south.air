//! Port Rust do motor DSP do soothe3 — **fonte única** dos kernels provados.
//!
//! Fonte: `dumpsooth/nyx_soothe3_dump.bin`
//! SHA-256 `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`.
//!
//! ## Regra
//!
//! Cada função aponta instrução + RVA. O que não foi lido do dump **não** é
//! estimado: fica em [`pending`] com o RVA de parada, e a cadeia
//! ([`chain`]) para no primeiro gap que bloqueia o null-test.
//!
//! ## Origem dos módulos
//!
//! Os módulos foram extraídos byte a byte de `checks/` por
//! `tools/extract_port_modules.py`, que mantém os testes no lugar:
//!
//! | Módulo | Etapa | Kernel provado |
//! |---|---|---|
//! | [`core_dsp`] | J1/J2 | F1..F4, gate de F5, one-pole, dot16/dot32 (`0x5F5C0`) |
//! | [`pipe`] | J3 | descritor `0x410 B`, par `0x18 B`, ring `0x90 B`, `chain_plan` |
//! | [`fft_layout`] | J4 (contrato) | tabela ordem→kernel, layout CCS |
//! | [`fft_kernels`] | J4 | `0x8BFE0`, `0x8C280`, `0x1D69E00`, split `0x895C0` |
//! | [`chan`] | J5 | ring/ganho `arg2/arg3`, `0x8BAA10`/`0x8BAB60` |
//! | [`engine`] | J6 | smoother, detector, one-pole, curvas, ganho `u·(y·v)` |
//! | [`stage`] | Q | `0x8C1440`: 5 grupos, `Σch²/Σch`, 4 divisões, mistura |
//! | [`div`] | M1 | `0x1550` → `0x63640`: despacho cabeça/16/8/resto, aritméticas A/B |
//! | [`rcp`] | M2 | `0x1C8530` → `0x29B260`: `vrcpps` + 1 passo FMA, lanes especiais `1/x`, MXCSR |
//!
//! `checks/<arquivo>.rs` aponta para o mesmo arquivo com
//! `#[path = "../port/src/<modulo>.rs"]`, então teste e biblioteca nunca
//! divergem. Rode `port/run_tests.ps1`.

#![allow(clippy::excessive_precision)]
#![allow(dead_code)]

pub mod chain;
#[allow(unused_imports)]
pub mod chan;
pub mod core_dsp;
pub mod div;
pub mod engine;
pub mod fft_kernels;
pub mod fft_layout;
pub mod pending;
#[allow(unused_imports)]
pub mod pipe;
pub mod rcp;
pub mod stage;

/// Versão do port, para carimbar o WAV do null-test.
pub const PORT_VERSION: &str = "0.0.0-j1j6+q+m1+m2";
