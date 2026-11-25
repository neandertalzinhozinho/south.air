//! Esqueleto da cadeia de um bloco, na ordem **provada** por N.
//!
//! A ordem não é inventada aqui: vem de [`crate::pipe::chain_plan`], transcrita
//! de `checks/n_canal.md` §1.3 com os RVAs `008AD601` (núcleo), `008AD9FA`
//! (`0x8B8E70`, `f58 != 0`), `008ADC52` (`0x8B9E40`, `f58 == 0`), `008ADF9B`
//! (`0x8BA1B0`), `008AE096` (`0x8BA7B0`, `f52 != 0`), `008AE1AF` (`0x1010`),
//! `008AE55F` (`0x8BA8C0`) e `008AE5EC` (`0x8A1EE0`, `f52 != 0`).
//!
//! O miolo (`0x8B3ED0`) **não** está portado: J1–J6 são fragmentos provados,
//! não o motor. Por isso [`process_block`] devolve o primeiro gap bloqueante em
//! vez de produzir amostras — o null-test não pode "passar" com número estimado.

use crate::pending::{first_blocking, Gap};
use crate::pipe::{chain_plan, ChainFlags, Step};

/// Ordem de estágios de um bloco, com os ramos `f58`/`f52` e o atalho
/// `008ADC6B` → `008AE1C1` (`checks/n_canal.md` §1.3).
pub fn block_plan(flags: &ChainFlags, counts_equal: bool) -> Vec<Step> {
    chain_plan(flags, counts_equal)
}

/// Primeiro gap que impede um null-test válido (desde M1, `0x293760`; a
/// divisão `0x1550` -> `0x63640` está em `crate::div` e o recíproco
/// `0x1C8530` -> `0x29B260` de `0x88E130` em `crate::rcp`, M2).
pub fn blocking_gap() -> &'static Gap {
    first_blocking().expect("pending::GAPS sem gaps bloqueantes")
}

/// Ponto de entrada do motor completo — **ainda não implementado**.
///
/// Devolve `Err(gap)` enquanto existir gap bloqueante, com o RVA. Quando não
/// houver, entra em `panic!` explícito: não existe caminho silencioso que
/// devolva zeros como se fossem áudio do plugin.
pub fn process_block(_flags: &ChainFlags, _counts_equal: bool) -> Result<(), &'static Gap> {
    match first_blocking() {
        Some(g) => Err(g),
        None => panic!(
            "cadeia sem gap bloqueante, mas o miolo de 0x8B3ED0 ainda não foi portado"
        ),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::pipe::Step;

    fn flags(f58: bool, f52: bool, f51: bool, f59: bool) -> ChainFlags {
        ChainFlags { f58, f52, f51, f59 }
    }

    #[test]
    fn core_comes_before_analysis() {
        // §23.15-N: 008AD601 (núcleo) antes de 008AD9FA/008ADC52 (análise).
        let plan = block_plan(&flags(true, true, false, false), false);
        let core = plan.iter().position(|s| *s == Step::Core).unwrap();
        let analysis = plan
            .iter()
            .position(|s| matches!(s, Step::AnalysisStaged | Step::AnalysisPlain))
            .unwrap();
        assert!(core < analysis);
    }

    #[test]
    fn block_stops_at_first_gap_with_rva() {
        let err = process_block(&flags(true, false, false, false), false).unwrap_err();
        assert_eq!(err.rva, "0x293760");
        assert!(err.blocks_null_test);
    }
}
