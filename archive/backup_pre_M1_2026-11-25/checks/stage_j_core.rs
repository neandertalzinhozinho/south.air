//! Testes da etapa J — o kernel vive em `port/src/core_dsp.rs` (fonte única).
//!
//! Este arquivo contém **apenas** os testes. O código testado é compartilhado
//! com o crate `soultree_port` via `#[path]`, então não há duas cópias.
//!
//! Extraído de `checks/.build/pre_port/stage_j_core.rs` por
//! `tools/extract_port_modules.py` (movido byte a byte, sem edição).
//!
//! Teste: `rustc --edition 2021 --test checks\stage_j_core.rs -o checks\.build\stage_j_core.exe`

#![allow(unused_imports)]

#[path = "../port/src/core_dsp.rs"]
mod core_dsp;

pub use core_dsp::*;

#[cfg(test)]
mod tests {
    use super::*;

    fn close(a: f32, b: f32, tol: f32) -> bool {
        (a - b).abs() <= tol
    }

    #[test]
    fn f1_mid_detail() {
        // detail = 0.5 -> dB = -50 -> 10^-2.5
        let g = f1_gain(0.5, 1.0);
        assert!(close(g, 10f32.powf(-2.5), 1e-6), "g={g}");
    }

    #[test]
    fn f1_clamps_detail() {
        // fora de [0,1] satura: detail=9 -> dB = -40 -> 10^-2
        let g = f1_gain(9.0, 1.0);
        assert!(close(g, 1e-2, 1e-7), "g={g}");
    }

    #[test]
    fn f1_apply_is_max() {
        let src = [0.1f32, 0.5, 0.9];
        let mut dst = [0.0f32; 3];
        f1_apply(&src, &mut dst, 0.5);
        assert_eq!(dst, [0.5, 0.5, 0.9]);
    }

    #[test]
    fn f3_scale_endpoints() {
        // x = 1 -> -0.25 - 0.25 = -0.5 ; x = 0 -> -0.25
        assert!(close(f3_scale(1.0), -0.5, 1e-7));
        assert!(close(f3_scale(0.0), -0.25, 1e-7));
    }

    #[test]
    fn f4_curve_endpoints() {
        // x = 0: com c = 1 -> exp(ln(7/3)) - 1/3 = 2.0
        //        com c = 0 -> exp(-1.099612832) - 1/3 = 0.0
        assert!(close(f4_curve(1.0, 0.0), 2.0, 1e-6), "c=1 -> {}", f4_curve(1.0, 0.0));
        assert!(close(f4_curve(0.0, 0.0), 0.0, 1e-6), "c=0 -> {}", f4_curve(0.0, 0.0));
    }

    #[test]
    fn one_pole_value() {
        // t/n = 1 -> x = 0.001*500 = 0.5 -> coef = 1 - 0.1^(1/0.5) = 0.99
        let c = one_pole_coef(48000.0, 48000);
        let want = 1.0 - C_0_1_F64.powf(2.0);
        assert!((c - want).abs() < 1e-12, "c={c} want={want}");
        assert!((c - 0.99).abs() < 1e-7, "c={c}");
    }

    #[test]
    fn dot32_fixed_bits() {
        // vetores de checks/j_dot32_avx.rs (saida do hardware AVX/FMA)
        let a: [f32; 32] = core::array::from_fn(|i| (i as f32 + 1.0) * 0.01);
        let b: [f32; 32] = core::array::from_fn(|i| 1.0 - (i as f32) * 0.03);
        assert_eq!(dot32(&a, &b).to_bits(), 0x4000_68db);
    }

    #[test]
    fn dot16_fixed_bits() {
        let a: [f32; 16] = core::array::from_fn(|i| (i as f32 + 1.0) * 0.07);
        let b: [f32; 16] = core::array::from_fn(|i| 0.5 + (i as f32) * 0.01);
        assert_eq!(dot16(&a, &b).to_bits(), 0x40b6_c8b4);
    }

    #[test]
    fn dot32_matches_sum_on_integers() {
        let a: [f32; 32] = core::array::from_fn(|i| i as f32);
        let b = [1.0f32; 32];
        assert_eq!(dot32(&a, &b), 496.0);
    }

    #[test]
    fn mac_matches_fma() {
        let mut d = [1.0f32, 2.0];
        mac_scalar_in_place(&mut d, &[3.0, 4.0], 0.5);
        assert_eq!(d, [1.0 + 3.0 * 0.5, 2.0 + 4.0 * 0.5]);
    }
}
