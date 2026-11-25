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
    Gap {
        id: "divisão do estagiador 0x1550 -> 0x63640 (vrcpps + Newton)",
        rva: "0x1550 -> 0x63640",
        status: Status::NaoTranscrito,
        blocks_null_test: true,
        note: "o estágio 0x8C1440 está transcrito em port/src/stage.rs, mas as 4 divisões \
               (008C2545/008C263D/008C273B/008C2828) não são vdivps: 0x63640 tem DUAS \
               aritméticas — 16 lanes refinam o recíproco (00063B24/00063B29) e multiplicam \
               no fim (00063B37); 8 lanes refinam o quociente (00063791/00063796) — e o \
               despacho depende de n e do alinhamento de dst (cabeça 00063697, 16 em \
               00063A67, 8 em 0006400D, resto 0006401A). n = [X+0x40] = N+1 é ímpar. Ver \
               checks/r_divisao_63640.md; falta transcrever e provar N/alinhamento",
    },
    Gap {
        id: "ln da IPP vs f32::ln (bit a bit)",
        rva: "0x293760",
        status: Status::NaoProvado,
        blocks_null_test: true,
        note: "curvas J6 são matematicamente equivalentes; falta provar bit-exatidão no \
               domínio alcançável (mesmo método de checks/j_crt_equiv.rs)",
    },
    Gap {
        id: "exp da IPP vs f32::exp (bit a bit)",
        rva: "0x240C00",
        status: Status::NaoProvado,
        blocks_null_test: true,
        note: "idem ln; afeta F4 e o par logf(powf(10, .)) de F5",
    },
    Gap {
        id: "recíproco vetorial de 0x88E130",
        rva: "0x1C8530 -> 0x29B260",
        status: Status::NaoProvado,
        blocks_null_test: true,
        note: "difere de 1.0/x no ULP; transcrever a sequência (determinística) fecha",
    },
    Gap {
        id: "campo de sample rate (identidade de r13 / [ctx+0x60])",
        rva: "0x8B68AB (008B68BC)",
        status: Status::NaoProvado,
        blocks_null_test: true,
        note: "r13 = arg1 de 0x8B3ED0 (008B3F14); [ctx+0x60] é qword; 'sample rate' \
               não provado — o port hoje só roda em 48 kHz",
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
    fn first_blocking_is_the_stage_division() {
        // Ordem deliberada: o gap que muda o sinal grosseiramente vem primeiro.
        let g = first_blocking().expect("há gaps bloqueantes");
        assert_eq!(g.rva, "0x1550 -> 0x63640");
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
        assert!(l.starts_with("NÃO TRANSCRITO: "));
        assert!(l.contains("0x63640"));
    }
}
