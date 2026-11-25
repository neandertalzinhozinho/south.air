//! Gaps explícitos do port — `NÃO EXTRAÍDO` / `NÃO PROVADO`, com o RVA de parada.
//!
//! Lista consolidada no `PLANO_MOTOR_AUDIO.md` §25 (2026-11-24) e §23.15.
//! Nenhum item aqui é estimado: `blocks_null_test` diz se o null-test
//! **plugin × port** pode passar sem fechar o gap. O que não bloqueia fica
//! registrado para não virar "esquecido", mas não consome sessão.

/// Situação da leitura no dump.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Status {
    /// Instrução não lida até o fim; não há transcrição.
    NaoExtraido,
    /// Instrução lida, mas a identidade/semântica não está fechada.
    NaoProvado,
    /// Leitura fechada (instrução a instrução), falta transcrever no port.
    NaoTranscrito,
}

/// Um gap do port.
#[derive(Clone, Copy, Debug)]
pub struct Gap {
    /// Identificador curto (para a mensagem de erro).
    pub id: &'static str,
    /// RVA onde a leitura parou.
    pub rva: &'static str,
    /// Situação.
    pub status: Status,
    /// `true` se o null-test não pode ser considerado válido sem fechar este gap.
    pub blocks_null_test: bool,
    /// O que exatamente falta (sem interpretação).
    pub note: &'static str,
}

/// Todos os gaps conhecidos, do mais bloqueante para o menos.
pub const GAPS: &[Gap] = &[
    // M1 (2026-11-25): a divisão 0x1550 -> 0x63640 saiu daqui — transcrita em
    // port/src/div.rs, usada por stage.rs, conferida contra hardware em
    // checks/j_div_avx.rs. O resíduo de M1 é o gap "identidade de E" abaixo.
    // M3 (2026-11-25): ln 0x293760 e exp 0x240C00 da IPP saíram daqui —
    // transcritos em port/src/ippmath.rs, usados por engine.rs (ipp_ln/ipp_exp),
    // conferidos contra hardware em checks/j_ln_exp_avx.rs (exaustivo 2^32);
    // sem vrcpps, então bit a bit em qualquer CPU (checks/t_ln_exp_ipp.md).
    // M2 (2026-11-25): o recíproco 0x1C8530 -> 0x29B260 de 0x88E130 saiu daqui —
    // transcrito em port/src/rcp.rs, usado por engine.rs (0088E32F), conferido
    // contra hardware em checks/j_rcp_avx.rs (checks/s_reciproco_88e130.md).
    // Resíduo: vrcpps é bit a bit só na CPU do oráculo (mesma ressalva de M1).
    Gap {
        id: "campo de sample rate (identidade de r13 / [ctx+0x60])",
        rva: "0x8B68AB (008B68BC)",
        status: Status::NaoProvado,
        blocks_null_test: true,
        note: "r13 = arg1 de 0x8B3ED0 (008B3F14); [ctx+0x60] é qword; 'sample rate' \
               não provado — o port hoje só roda em 48 kHz",
    },
    Gap {
        id: "identidade do objeto E de 0x864410 e do arg4 de 0x8634A0 (n e alinhamento da divisão)",
        rva: "0x864410 (0086453D) / 0x862E40 (00862E68)",
        status: Status::NaoProvado,
        blocks_null_test: true,
        note: "M1: dst & 0x1c = 0 nas 4 divisões é provado dentro de 0x8C1440 (cursor align16) \
               e na base [E+0x30] escrita por 0x868B50 (00868B98/00868B9C, 64 B) a partir de \
               0x8634A0 (00863563); n = [X+0x40] = 257 vale para arg4 = 48000 \
               (div::stage_division_len). Falta a instrução que ligue o E de 0x864410 \
               (despacho indireto) ao objeto de 0x8634A0 — hoje só coincidem os offsets \
               +0x10/+0x2C/+0x30/+0x5F8 — e a identidade de arg4 (= (float)xmm2 de 0x862E40) \
               como taxa de amostragem (M4)",
    },
    Gap {
        id: "callback [rdx+0x50] do descritor de runtime",
        rva: "00867E10",
        status: Status::NaoProvado,
        blocks_null_test: true,
        note: "call indireto; provado que não é campo +0x50 da tabela 0x238E9B0. \
               Só bloqueia se o caminho default passar por ele",
    },
    Gap {
        id: "packing da FFT: RToPerm/RToPack e construtor de [spec]==7",
        rva: "0xBD40 (0000BDCC/0000BDE0)",
        status: Status::NaoProvado,
        blocks_null_test: false,
        note: "o caminho de áudio foi medido como CCS (n/2+1 pares, ordem natural); \
               falta só o nome do packing da IPP",
    },
    Gap {
        id: "instância de linear phase",
        rva: "0x87E0B0",
        status: Status::NaoExtraido,
        blocks_null_test: false,
        note: "default é minimum phase; nenhum FIR localizado no caminho lido",
    },
    Gap {
        id: "identidade de 0x86F170",
        rva: "0x86F170",
        status: Status::NaoProvado,
        blocks_null_test: false,
        note: "mecânica provada (dois descritores de 0x18 B, deslocamento 4*[sub+0x88]); \
               nome/identidade não",
    },
    Gap {
        id: "kernel 0x88300 (ordem > 0x13)",
        rva: "0x88300",
        status: Status::NaoExtraido,
        blocks_null_test: false,
        note: "inalcançável para o áudio: N = round(256*fs/44100) <= 1115 -> ordem 11; \
               só é chamado com r15d > 0x13 (0007259B/000725A1..000725AE)",
    },
    Gap {
        id: "geradores de twiddle (0x806E0/0x876E0/0x87AA0)",
        rva: "0x806E0",
        status: Status::NaoExtraido,
        blocks_null_test: false,
        note: "tabelas medidas nos goldens; geração não transcrita",
    },
    Gap {
        id: "corpo de 0x72180 (ctx da FFT)",
        rva: "0x72180",
        status: Status::NaoExtraido,
        blocks_null_test: false,
        note: "só os campos usados pelo caminho de áudio foram lidos",
    },
];

/// Primeiro gap que impede um null-test válido.
pub fn first_blocking() -> Option<&'static Gap> {
    GAPS.iter().find(|g| g.blocks_null_test)
}

/// Gaps que não bloqueiam o null-test (registro, não trabalho pendente).
pub fn non_blocking() -> impl Iterator<Item = &'static Gap> {
    GAPS.iter().filter(|g| !g.blocks_null_test)
}

/// Formata um gap como `NÃO EXTRAÍDO: <id> (<rva>)`.
pub fn label(g: &Gap) -> String {
    let s = match g.status {
        Status::NaoExtraido => "NÃO EXTRAÍDO",
        Status::NaoProvado => "NÃO PROVADO",
        Status::NaoTranscrito => "NÃO TRANSCRITO",
    };
    format!("{s}: {} ({})", g.id, g.rva)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_gap_has_rva_and_note() {
        for g in GAPS {
            assert!(!g.rva.is_empty(), "{} sem RVA", g.id);
            assert!(!g.note.is_empty(), "{} sem nota", g.id);
        }
    }

    #[test]
    fn first_blocking_is_the_sample_rate() {
        // M3 fechou ln/exp da IPP (port/src/ippmath.rs); o primeiro bloqueante
        // passa a ser o campo de sample rate (M4).
        let g = first_blocking().expect("há gaps bloqueantes");
        assert_eq!(g.rva, "0x8B68AB (008B68BC)");
    }

    #[test]
    fn ipp_ln_exp_are_no_longer_gaps() {
        for g in GAPS {
            assert!(!g.rva.contains("0x293760"), "{} ainda lista 0x293760", g.id);
            assert!(!g.rva.contains("0x240C00"), "{} ainda lista 0x240C00", g.id);
        }
    }

    #[test]
    fn stage_division_is_no_longer_a_gap() {
        for g in GAPS {
            assert!(!g.rva.contains("0x63640"), "{} ainda lista 0x63640", g.id);
        }
    }

    #[test]
    fn reciprocal_of_88e130_is_no_longer_a_gap() {
        // M2: 0x1C8530 -> 0x29B260 está em port/src/rcp.rs.
        for g in GAPS {
            assert!(!g.rva.contains("0x29B260"), "{} ainda lista 0x29B260", g.id);
            assert!(!g.id.contains("recíproco"), "{} ainda lista o recíproco", g.id);
        }
    }

    #[test]
    fn out_of_audio_items_do_not_block() {
        for g in GAPS {
            if g.rva == "0x88300" || g.rva == "0x806E0" || g.rva == "0x72180" {
                assert!(!g.blocks_null_test, "{} não deveria bloquear", g.id);
            }
        }
    }

    #[test]
    fn label_carries_status_and_rva() {
        let g = first_blocking().unwrap();
        let l = label(g);
        assert!(l.starts_with("NÃO PROVADO: "));
        assert!(l.contains("0x8B68AB"));
    }
}
