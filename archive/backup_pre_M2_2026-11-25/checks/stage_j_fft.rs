//! Testes da etapa J — o kernel vive em `port/src/fft_layout.rs` (fonte única).
//!
//! Este arquivo contém **apenas** os testes. O código testado é compartilhado
//! com o crate `soultree_port` via `#[path]`, então não há duas cópias.
//!
//! Extraído de `checks/.build/pre_port/stage_j_fft.rs` por
//! `tools/extract_port_modules.py` (movido byte a byte, sem edição).
//!
//! Teste: `rustc --edition 2021 --test checks\stage_j_fft.rs -o checks\.build\stage_j_fft.exe`

#![allow(unused_imports)]

#[path = "../port/src/fft_layout.rs"]
mod fft_layout;

pub use fft_layout::*;

include!("fft_golden.rs");


// ---------------------------------------------------------------------------
// Casos medidos
// ---------------------------------------------------------------------------

pub struct Case {
    pub order: u32,
    pub sig: &'static str,
    pub src: &'static [u32],
    pub dst: &'static [u32],
    pub back: &'static [u32],
}

pub static CASES: &[Case] = &[
    Case { order: 6, sig: "impulse", src: &FFT6_IMPULSE_SRC, dst: &FFT6_IMPULSE_DST, back: &FFT6_IMPULSE_BACK },
    Case { order: 6, sig: "cos", src: &FFT6_COS_SRC, dst: &FFT6_COS_DST, back: &FFT6_COS_BACK },
    Case { order: 6, sig: "ramp", src: &FFT6_RAMP_SRC, dst: &FFT6_RAMP_DST, back: &FFT6_RAMP_BACK },
    Case { order: 7, sig: "impulse", src: &FFT7_IMPULSE_SRC, dst: &FFT7_IMPULSE_DST, back: &FFT7_IMPULSE_BACK },
    Case { order: 7, sig: "cos", src: &FFT7_COS_SRC, dst: &FFT7_COS_DST, back: &FFT7_COS_BACK },
    Case { order: 7, sig: "ramp", src: &FFT7_RAMP_SRC, dst: &FFT7_RAMP_DST, back: &FFT7_RAMP_BACK },
    Case { order: 8, sig: "impulse", src: &FFT8_IMPULSE_SRC, dst: &FFT8_IMPULSE_DST, back: &FFT8_IMPULSE_BACK },
    Case { order: 8, sig: "cos", src: &FFT8_COS_SRC, dst: &FFT8_COS_DST, back: &FFT8_COS_BACK },
    Case { order: 8, sig: "ramp", src: &FFT8_RAMP_SRC, dst: &FFT8_RAMP_DST, back: &FFT8_RAMP_BACK },
    Case { order: 9, sig: "impulse", src: &FFT9_IMPULSE_SRC, dst: &FFT9_IMPULSE_DST, back: &FFT9_IMPULSE_BACK },
    Case { order: 9, sig: "cos", src: &FFT9_COS_SRC, dst: &FFT9_COS_DST, back: &FFT9_COS_BACK },
    Case { order: 9, sig: "ramp", src: &FFT9_RAMP_SRC, dst: &FFT9_RAMP_DST, back: &FFT9_RAMP_BACK },
];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn golden_shape_and_dispatch_table() {
        for c in CASES {
            let n = 1usize << c.order;
            assert_eq!(c.src.len(), n, "{} ordem {}", c.sig, c.order);
            assert_eq!(c.dst.len(), n + 2);
            assert_eq!(c.back.len(), n + 2);
            // O audio roda com flag 8 -> ctx+8 = 0.
            let k = kernel_for(c.order, 0);
            match c.order {
                6 => assert_eq!(k, 0x8BFE0),
                7 => assert_eq!(k, 0x8C280),
                8 | 9 => assert_eq!(k, KERNEL_8_19),
                _ => {}
            }
        }
        // A tabela alternativa tem que ser diferente nos slots especializados.
        assert_ne!(kernel_for(6, 0), kernel_for(6, 1));
        assert_eq!(kernel_for(6, 1), 0x8B3A0);
        assert_eq!(kernel_for(5, 0), 0x8BEE0);
        assert_eq!(kernel_for(4, 0), 0x8A6C0);
        assert_eq!(kernel_for(20, 0), KERNEL_GT19);
        // Slots do wrapper medidos no plugin:
        assert_eq!(WRAP_FWD, 0x72480);
        assert_eq!(WRAP_INV, 0x726A0);
        // Desc generico (so usado se o marcador != 3):
        assert_eq!(GENERIC_FWD, 0x6F6A0);
        assert_eq!(GENERIC_INV, 0x6F760);
    }

    #[test]
    fn golden_dc_and_nyquist_are_real() {
        for c in CASES {
            let d = to_f32(c.dst);
            let n = 1usize << c.order;
            assert_eq!(d[1], 0.0, "Im(DC) != 0 em {} ordem {}", c.sig, c.order);
            assert_eq!(d[n + 1], 0.0, "Im(Nyq) != 0 em {} ordem {}", c.sig, c.order);
            assert_eq!(c.dst[1], 0);
            assert_eq!(c.dst[n + 1], 0);
        }
    }

    #[test]
    fn golden_impulse_is_flat_spectrum() {
        for c in CASES.iter().filter(|c| c.sig == "impulse") {
            let d = to_f32(c.dst);
            let n = 1usize << c.order;
            for k in 0..=n / 2 {
                let (re, im) = bin(&d, k);
                assert_eq!(re, 1.0, "Re bin {k} ordem {}", c.order);
                assert_eq!(im, 0.0, "Im bin {k} ordem {}", c.order);
            }
        }
    }

    #[test]
    fn golden_cos_peak_is_bin_3() {
        for c in CASES.iter().filter(|c| c.sig == "cos") {
            let d = to_f32(c.dst);
            let n = 1usize << c.order;
            let mut best = (0usize, -1.0f32);
            for k in 0..=n / 2 {
                let (re, im) = bin(&d, k);
                let m = (re * re + im * im).sqrt();
                if m > best.1 {
                    best = (k, m);
                }
            }
            assert_eq!(best.0, 3, "ordem {}", c.order);
            // Entrada e cos(2*pi*3*i/n) em f32; pico teorico = n/2 (a menos de
            // arredondamento f32 da propria entrada/FFT).
            let peak = bin(&d, 3).0;
            let want = (n / 2) as f32;
            assert!(
                (peak - want).abs() <= 2e-3 * want,
                "Re do pico, ordem {}: {peak} vs {want}",
                c.order
            );
        }
    }

    /// Prova que o layout medido e `X[k] = sum_i x[i] exp(-2*pi*i*k*i/n)` para
    /// `k = 0..n/2`, pares intercalados em ordem natural. DFT em f64 aqui e
    /// **apenas conferente**, nao e o port.
    #[test]
    fn golden_layout_is_natural_order_dft() {
        let two_pi = std::f64::consts::TAU;
        for c in CASES {
            let x: Vec<f64> = to_f32(c.src).iter().map(|v| *v as f64).collect();
            let d = to_f32(c.dst);
            let n = x.len();
            let mut worst = 0.0f64;
            for k in 0..=n / 2 {
                let mut sr = 0.0f64;
                let mut si = 0.0f64;
                for (i, xi) in x.iter().enumerate() {
                    let a = -two_pi * (k as f64) * (i as f64) / (n as f64);
                    sr += xi * a.cos();
                    si += xi * a.sin();
                }
                let (re, im) = bin(&d, k);
                let scale = sr.hypot(si).max(1.0);
                let err = ((re as f64 - sr).abs() + (im as f64 - si).abs()) / scale;
                if err > worst {
                    worst = err;
                }
            }
            // A FFT f32 erra ~1e-6 relativo; 2e-5 cobre com folga.
            assert!(
                worst < 2e-5,
                "layout nao bate com DFT natural: {} ordem {} (erro rel {:.3e})",
                c.sig,
                c.order,
                worst
            );
        }
    }

    #[test]
    fn golden_roundtrip_gain_is_n() {
        for c in CASES {
            let x = to_f32(c.src);
            let b = to_f32(c.back);
            let n = x.len();
            let nf = n as f32;
            if c.sig == "impulse" {
                // Medido: bits identicos a x*n para o impulso.
                for i in 0..n {
                    assert_eq!(b[i].to_bits(), (x[i] * nf).to_bits(), "impulso [{}]", i);
                }
            } else {
                let mut worst = 0.0f32;
                for i in 0..n {
                    worst = worst.max((b[i] - x[i] * nf).abs());
                }
                assert!(worst < 2.5e-4, "round-trip {} ordem {}: {:.3e}", c.sig, c.order, worst);
            }
            // A inversa nao devolve os dois floats extras como amostras.
            assert_eq!(b.len(), n + 2);
        }
    }

    /// A escala `1/n` e do chamador (`008B291C`..`008B2929`), nao da IPP:
    /// a IPP com flag 8 devolve `x*n`, entao o ganho medido do par e `n`.
    #[test]
    fn scaling_is_caller_side() {
        let c = CASES.iter().find(|c| c.order == 9 && c.sig == "impulse").unwrap();
        let b = to_f32(c.back);
        assert_eq!(b[0], 512.0);
        // 1/n sobre isso devolve 1.0 em f32.
        let s = 1.0f32 / 512.0f32;
        assert_eq!(b[0] * s, 1.0);
        assert_eq!(INNER_CTX_QWORD, 0x36);
        assert_eq!(SPEC_MAGIC, 7);
        assert_eq!(CTX_MAGIC, 6);
        assert_eq!(WRAPPER_MARKER, 3);
        assert_eq!(FLAG_NODIV, 8);
        assert_eq!(HINT, 1);
    }
}
