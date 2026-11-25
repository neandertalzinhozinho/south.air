//! M5 — tradução mecânica do miolo `0x8B3ED0` e do seu fecho de chamadas.
//!
//! `gen_engine.rs` é gerado por `tools/lift/lift.py` a partir do dump. Cada
//! instrução vira uma linha Rust, com o RVA, na mesma ordem e com a mesma
//! aritmética. `rt.rs` é o runtime (registradores, flags, memória);
//! `leaf.rs` tem as folhas não traduzidas (CRT, cópia/zero, `__chkstk`).
//! Prova e método: `checks/v_miolo_m5.md`.

pub mod api;
pub mod gen_engine;
pub mod leaf;
pub mod rt;
#[cfg(test)]
mod tests;

use rt::{Cpu, IMAGE_BASE};

/// Funções traduzidas num crate extra (`lifted_extra`), registradas em tempo de execução,
/// para iterar sem recompilar o crate base.
pub static EXTRA: std::sync::OnceLock<fn(u32) -> Option<fn(&mut Cpu)>> = std::sync::OnceLock::new();
pub static EXTRA_IMPORT: std::sync::OnceLock<fn(u32) -> Option<&'static str>> = std::sync::OnceLock::new();

/// Chama a função de RVA `rva`: traduzida se existir, senão folha.
pub fn call(c: &mut Cpu, rva: u32) {
    if let Some(f) = gen_engine::lifted(rva) {
        f(c);
        return;
    }
    if let Some(f) = EXTRA.get().and_then(|x| x(rva)) {
        f(c);
        return;
    }
    leaf::call(c, rva)
}

/// Chamada/salto indireto para um VA da imagem (base `0x199B0000`).
pub fn call_va(c: &mut Cpu, va: u64, site: u32) {
    if api::host_call(c, va, site) {
        return;
    }
    if va < IMAGE_BASE || va >= IMAGE_BASE + rt::IMAGE_SIZE {
        panic!("alvo indireto fora da imagem em 0x{site:X}: 0x{va:X}");
    }
    call(c, (va - IMAGE_BASE) as u32)
}
