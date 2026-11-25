//! Testes da etapa J — o kernel vive em `port/src/fft_kernels.rs` (fonte única).
//!
//! Este arquivo contém **apenas** os testes. O código testado é compartilhado
//! com o crate `soultree_port` via `#[path]`, então não há duas cópias.
//!
//! Extraído de `checks/.build/pre_port/j4_fft.rs` por
//! `tools/extract_port_modules.py` (movido byte a byte, sem edição).
//!
//! Teste: `rustc --edition 2021 --test checks\j4_fft.rs -o checks\.build\j4_fft.exe`

#![allow(unused_imports)]

#[path = "../port/src/fft_kernels.rs"]
mod fft_kernels;

pub use fft_kernels::*;

include!("j4_golden_6.rs");
include!("j4_golden_7.rs");
include!("fft_golden.rs");
include!("j8_golden.rs");
include!("j9_golden.rs");
include!("j10_golden.rs");
include!("j11_golden.rs");
include!("j12_golden.rs");

#[cfg(test)]
mod tests {
    use super::*;

    fn f(bits: u32) -> f32 {
        f32::from_bits(bits)
    }

    fn to_f32(bits: &[u32]) -> Vec<f32> {
        bits.iter().map(|b| f(*b)).collect()
    }

    #[test]
    fn kernel6_is_bit_exact() {
        let src_bits: [u32; 64] = J6_SRC;
        let mut src = [0f32; 64];
        for i in 0..64 {
            src[i] = f(src_bits[i]);
        }
        let mut dst = [0f32; 64];
        kernel6(&src, &mut dst);
        let mut bad = 0;
        for i in 0..64 {
            let want = f(J6_KD[i]);
            if dst[i].to_bits() != want.to_bits() {
                bad += 1;
                println!(
                    "  KD[{i}] got {:08x} {:+.9e}  want {:08x} {:+.9e}",
                    dst[i].to_bits(),
                    dst[i],
                    want.to_bits(),
                    want
                );
            }
        }
        assert_eq!(bad, 0, "kernel6 divergiu em {bad} de 64 floats");
    }

    #[test]
    fn full_chain_is_bit_exact() {
        let src_bits: [u32; 64] = J6_SRC;
        let mut src = [0f32; 64];
        for i in 0..64 {
            src[i] = f(src_bits[i]);
        }
        let tw = to_f32(&J6_TW);
        let got = rfft6(&src, &tw);
        let mut bad = 0;
        for i in 0..66 {
            let want = f(J6_FWD[i]);
            if got[i].to_bits() != want.to_bits() {
                bad += 1;
                println!(
                    "  FWD[{i}] got {:08x} {:+.9e}  want {:08x} {:+.9e}",
                    got[i].to_bits(),
                    got[i],
                    want.to_bits(),
                    want
                );
            }
        }
        assert_eq!(bad, 0, "cadeia divergiu em {bad} de 66 floats");
    }

    /// Confirma que o pack/split não depende da ordem da leitura: os três
    /// estágios sozinhos têm de casar com o que o plugin gravou.
    #[test]
    fn measured_sections_are_consistent() {
        // FWD e MAN vêm de caminhos diferentes no probe (fwd vs manual);
        // o probe já checou 0 diffs, e aqui os dois arrays precisam ser iguais.
        for i in 0..66 {
            assert_eq!(J6_MAN[i], J6_FWD[i], "MAN != FWD em [{i}]");
        }
    }

    /// A saída é CCS de ordem natural: bins 0 e n/2 reais, pares intercalados.
    #[test]
    fn layout_is_ccs_pairs() {
        let tw = to_f32(&J6_TW);
        let src_bits: [u32; 64] = J6_SRC;
        let mut src = [0f32; 64];
        for i in 0..64 {
            src[i] = f(src_bits[i]);
        }
        let d = rfft6(&src, &tw);
        assert_eq!(d[1].to_bits(), 0f32.to_bits(), "Im(DC)");
        assert_eq!(d[65].to_bits(), 0f32.to_bits(), "Im(Nyquist)");
    }

    /// Prova de ponta a ponta: o port de ordem 6 reproduz bit a bit os três
    /// vetores-ouro medidos por `checks/fft_probe.rs` (`checks/fft_golden.rs`),
    /// que vêm de `0x20E0` (fwd) sobre entradas reais reais (impulso, cosseno e
    /// rampa), não do caminho manual.
    #[test]
    fn order6_matches_probe_golden() {
        let tw = to_f32(&J6_TW);
        let cases: [(&str, [u32; 64], [u32; 66]); 3] = [
            ("impulse", FFT6_IMPULSE_SRC, FFT6_IMPULSE_DST),
            ("cos", FFT6_COS_SRC, FFT6_COS_DST),
            ("ramp", FFT6_RAMP_SRC, FFT6_RAMP_DST),
        ];
        for (name, src_bits, want_bits) in cases {
            let mut src = [0f32; 64];
            for i in 0..64 {
                src[i] = f(src_bits[i]);
            }
            let got = rfft6(&src, &tw);
            let mut bad = 0;
            for i in 0..66 {
                if got[i].to_bits() != want_bits[i] {
                    bad += 1;
                    if bad <= 4 {
                        println!(
                            "  {name}[{i}] got {:08x} {:+.9e}  want {:08x} {:+.9e}",
                            got[i].to_bits(),
                            got[i],
                            want_bits[i],
                            f(want_bits[i])
                        );
                    }
                }
            }
            assert_eq!(bad, 0, "{name}: {bad} de 66 floats divergiram");
        }
    }

    /// Ordem 7: kernel `0x8C280` sozinho contra o que o plugin devolveu.
    #[test]
    fn kernel7_is_bit_exact() {
        let mut src = [0f32; 128];
        for i in 0..128 {
            src[i] = f(J7_SRC[i]);
        }
        let mut dst = [0f32; 128];
        kernel7(&src, &mut dst);
        let mut bad = 0;
        for i in 0..128 {
            let want = f(J7_KD[i]);
            if dst[i].to_bits() != want.to_bits() {
                bad += 1;
                if bad <= 4 {
                    println!(
                        "  KD7[{i}] got {:08x} {:+.9e}  want {:08x} {:+.9e}",
                        dst[i].to_bits(),
                        dst[i],
                        want.to_bits(),
                        want
                    );
                }
            }
        }
        assert_eq!(bad, 0, "kernel7 divergiu em {bad} de 128 floats");
    }

    #[test]
    fn order7_chain_is_bit_exact() {
        let mut src = [0f32; 128];
        for i in 0..128 {
            src[i] = f(J7_SRC[i]);
        }
        let tw = to_f32(&J7_TW);
        let got = rfft7(&src, &tw);
        let mut bad = 0;
        for i in 0..130 {
            let want = f(J7_FWD[i]);
            if got[i].to_bits() != want.to_bits() {
                bad += 1;
                if bad <= 4 {
                    println!(
                        "  FWD7[{i}] got {:08x} {:+.9e}  want {:08x} {:+.9e}",
                        got[i].to_bits(),
                        got[i],
                        want.to_bits(),
                        want
                    );
                }
            }
        }
        assert_eq!(bad, 0, "cadeia ordem 7 divergiu em {bad} de 130 floats");
    }

    #[test]
    fn order7_matches_probe_golden() {
        let tw = to_f32(&J7_TW);
        let cases: [(&str, [u32; 128], [u32; 130]); 3] = [
            ("impulse", FFT7_IMPULSE_SRC, FFT7_IMPULSE_DST),
            ("cos", FFT7_COS_SRC, FFT7_COS_DST),
            ("ramp", FFT7_RAMP_SRC, FFT7_RAMP_DST),
        ];
        for (name, src_bits, want_bits) in cases {
            let mut src = [0f32; 128];
            for i in 0..128 {
                src[i] = f(src_bits[i]);
            }
            let got = rfft7(&src, &tw);
            let mut bad = 0;
            for i in 0..130 {
                if got[i].to_bits() != want_bits[i] {
                    bad += 1;
                }
            }
            assert_eq!(bad, 0, "{name}: {bad} de 130 floats divergiram");
        }
    }

    /// Isola as passadas 1+2+3a: compara o workspace intermediário com o do plugin.
    #[test]
    fn kernel9_workspace_matches() {
        let mut src = [0f32; 512];
        for i in 0..512 {
            src[i] = f(J9_SRC[i]);
        }
        let tw38 = to_f32(&J9_TW38);
        let mut ws = vec![0f32; 512];
        kernel9_stages12(&src, &mut ws, &J9_IDX, &tw38);
        let mut bad = 0;
        for i in 0..512 {
            if ws[i].to_bits() != J9_WS[i] {
                bad += 1;
                if bad <= 6 {
                    println!(
                        "  WS[{i}] got {:08x} {:+.9e}  want {:08x} {:+.9e}",
                        ws[i].to_bits(),
                        ws[i],
                        J9_WS[i],
                        f(J9_WS[i])
                    );
                }
            }
        }
        assert_eq!(bad, 0, "workspace divergiu em {bad} de 512 floats");
    }

    /// Ordem 9: kernel genérico `0x1D69E00` sozinho contra o que o plugin devolveu.
    #[test]
    fn kernel9_is_bit_exact() {
        let mut src = [0f32; 512];
        for i in 0..512 {
            src[i] = f(J9_SRC[i]);
        }
        let tw38 = to_f32(&J9_TW38);
        let idx = J9_IDX;
        let mut ws = vec![0f32; 512];
        let mut dst = [0f32; 512];
        kernel9(&src, &mut ws, &mut dst, &idx, &tw38);
        let mut bad = 0;
        for i in 0..512 {
            let want = f(J9_KD[i]);
            if dst[i].to_bits() != want.to_bits() {
                bad += 1;
                if bad <= 6 {
                    println!(
                        "  KD9[{i}] got {:08x} {:+.9e}  want {:08x} {:+.9e}",
                        dst[i].to_bits(),
                        dst[i],
                        want.to_bits(),
                        want
                    );
                }
            }
        }
        assert_eq!(bad, 0, "kernel9 divergiu em {bad} de 512 floats");
    }

    #[test]
    fn order9_chain_is_bit_exact() {
        let mut src = [0f32; 512];
        for i in 0..512 {
            src[i] = f(J9_SRC[i]);
        }
        let tw38 = to_f32(&J9_TW38);
        let tw50 = to_f32(&J9_TW50);
        let got = rfft9(&src, &tw38, &J9_IDX, &tw50);
        let mut bad = 0;
        for i in 0..514 {
            let want = f(J9_FWD[i]);
            if got[i].to_bits() != want.to_bits() {
                bad += 1;
                if bad <= 6 {
                    println!(
                        "  FWD9[{i}] got {:08x} {:+.9e}  want {:08x} {:+.9e}",
                        got[i].to_bits(),
                        got[i],
                        want.to_bits(),
                        want
                    );
                }
            }
        }
        assert_eq!(bad, 0, "cadeia ordem 9 divergiu em {bad} de 514 floats");
    }

    #[test]
    fn order9_matches_probe_golden() {
        let tw38 = to_f32(&J9_TW38);
        let tw50 = to_f32(&J9_TW50);
        let cases: [(&str, [u32; 512], [u32; 514]); 3] = [
            ("impulse", FFT9_IMPULSE_SRC, FFT9_IMPULSE_DST),
            ("cos", FFT9_COS_SRC, FFT9_COS_DST),
            ("ramp", FFT9_RAMP_SRC, FFT9_RAMP_DST),
        ];
        for (name, src_bits, want_bits) in cases {
            let mut src = [0f32; 512];
            for i in 0..512 {
                src[i] = f(src_bits[i]);
            }
            let got = rfft9(&src, &tw38, &J9_IDX, &tw50);
            let mut bad = 0;
            for i in 0..514 {
                if got[i].to_bits() != want_bits[i] {
                    bad += 1;
                }
            }
            assert_eq!(bad, 0, "{name}: {bad} de 514 floats divergiram");
        }
    }

    fn check_generic_order(
        order: usize,
        src_bits: &[u32],
        kd_bits: &[u32],
        ws_bits: &[u32],
        fwd_bits: &[u32],
        idx: &[u32],
        tw38: &[u32],
        tw50: &[u32],
    ) {
        let n = 1usize << order;
        let src = to_f32(src_bits);
        let tw = to_f32(tw38);
        let mut ws = vec![0f32; n];
        let mut dst = vec![0f32; n];
        kernel_generic(&src, &mut ws, &mut dst, idx, &tw, n);

        let mut bad = 0;
        for i in 0..n {
            if dst[i].to_bits() != kd_bits[i] {
                bad += 1;
                if bad <= 6 {
                    println!(
                        "  ord{order} KD[{i}] got {:08x} want {:08x}",
                        dst[i].to_bits(),
                        kd_bits[i]
                    );
                }
            }
        }
        assert_eq!(bad, 0, "ordem {order}: KD divergiu em {bad}/{n}");

        let mut bad = 0;
        for i in 0..n {
            if ws[i].to_bits() != ws_bits[i] {
                bad += 1;
                if bad <= 6 {
                    println!(
                        "  ord{order} WS[{i}] got {:08x} want {:08x}",
                        ws[i].to_bits(),
                        ws_bits[i]
                    );
                }
            }
        }
        assert_eq!(bad, 0, "ordem {order}: WS divergiu em {bad}/{n}");

        let tw50f = to_f32(tw50);
        let got = rfft_generic(&src, &tw, idx, &tw50f, n);
        let mut bad = 0;
        for i in 0..n + 2 {
            if got[i].to_bits() != fwd_bits[i] {
                bad += 1;
                if bad <= 6 {
                    println!(
                        "  ord{order} FWD[{i}] got {:08x} want {:08x}",
                        got[i].to_bits(),
                        fwd_bits[i]
                    );
                }
            }
        }
        assert_eq!(bad, 0, "ordem {order}: FWD divergiu em {bad}/{}", n + 2);
    }

    #[test]
    fn orders_8_10_11_12_are_bit_exact() {
        check_generic_order(9, &J9_SRC, &J9_KD, &J9_WS, &J9_FWD, &J9_IDX, &J9_TW38, &J9_TW50);
        check_generic_order(8, &J8_SRC, &J8_KD, &J8_WS, &J8_FWD, &J8_IDX, &J8_TW38, &J8_TW50);
        check_generic_order(
            10, &J10_SRC, &J10_KD, &J10_WS, &J10_FWD, &J10_IDX, &J10_TW38, &J10_TW50,
        );
        check_generic_order(
            11, &J11_SRC, &J11_KD, &J11_WS, &J11_FWD, &J11_IDX, &J11_TW38, &J11_TW50,
        );
        check_generic_order(
            12, &J12_SRC, &J12_KD, &J12_WS, &J12_FWD, &J12_IDX, &J12_TW38, &J12_TW50,
        );
    }
}
