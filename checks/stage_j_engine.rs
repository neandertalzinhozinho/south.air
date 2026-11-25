//! Testes da etapa J — o kernel vive em `port/src/engine.rs` (fonte única).
//!
//! Este arquivo contém **apenas** os testes. O código testado é compartilhado
//! com o crate `soultree_port` via `#[path]`, então não há duas cópias.
//!
//! Extraído de `checks/.build/pre_port/stage_j_engine.rs` por
//! `tools/extract_port_modules.py` (movido byte a byte, sem edição).
//!
//! Teste: `rustc --edition 2021 --test checks\stage_j_engine.rs -o checks\.build\stage_j_engine.exe`

#![allow(unused_imports)]

#[path = "../port/src/engine.rs"]
mod engine;

pub use engine::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn smoother_keeps_constant_and_spreads_impulse() {
        let mut v = [0.7f32; 8];
        smoother_fwd_back(&mut v);
        for x in v {
            assert!((x - 0.7).abs() < 1e-7, "constante mudou: {x}");
        }
        let mut imp = [0.0f32; 8];
        imp[0] = 1.0;
        smoother_fwd_back(&mut imp);
        // as duas passadas espalham o impulso para os dois lados
        assert!(imp[0] > 0.0);
        assert!(imp[1] > 0.0);
        assert!(imp[7] > 0.0);
        assert!(imp[0] > imp[7]);
    }

    #[test]
    fn detector_matches_power_mean_identities() {
        // P1 = 0 e P0 > 0 -> R = P0; P0 fica (1-g)P0+gP0 e P1 vira g*P0
        let mut p0 = [2.0f32, 4.0];
        let mut p1 = [0.0f32, 0.0];
        detector2_in_place(&mut p0, &mut p1, 0.25);
        assert_eq!(p0, [2.0, 4.0]);
        assert_eq!(p1, [0.5, 1.0]);

        // P0 == P1 -> R = P0; ambos intactos
        let mut p0 = [3.0f32];
        let mut p1 = [3.0f32];
        detector2_in_place(&mut p0, &mut p1, 0.5);
        assert_eq!(p0, [3.0]);
        assert_eq!(p1, [3.0]);

        // P0 = -P1 -> denominador cai em eps e R fica enorme (sem clamp superior)
        let mut p0 = [1.0f32];
        let mut p1 = [-1.0f32];
        detector2_in_place(&mut p0, &mut p1, 0.5);
        let r = 2.0f32 / EPS;
        assert_eq!(p0[0], r.mul_add(0.5, 1.0 * 0.5));
        assert_eq!(p1[0], r.mul_add(0.5, -1.0 * 0.5));
        assert!(r > 1.0e7);
    }

    #[test]
    fn one_pole_endpoints_and_monotonicity() {
        // t = 0 -> x = 0 -> 1/x = inf -> 0.1^inf = 0 -> coef = 1
        assert_eq!(one_pole_coef(0.0, 48000), 1.0);
        // t muito grande -> x grande -> 0.1^(1/x) -> 1 -> coef -> 0
        let c = one_pole_coef(1.0e15, 48000);
        assert!(c >= 0.0 && c < 1.0e-5, "coef={c}");
        // monotonicamente decrescente em t (t grande o bastante para sair de 1.0)
        let a = one_pole_coef(1.0e6, 48000);
        let b = one_pole_coef(1.0e7, 48000);
        assert!(a > b, "a={a} b={b}");
    }

    #[test]
    fn shelf_k_zero_is_unity() {
        let mut dst = [0.0f32, 5.0, -3.0];
        shelf_curve_in_place(&mut dst, None, 500.0, 0.0, 42.0);
        assert_eq!(dst, [1.0, 1.0, 1.0]);
    }

    #[test]
    fn shelf_center_has_zero_db_and_ends_are_monotone() {
        // v = A, G = 0 -> sigma = 1/2 -> exp(0) = 1
        let mut dst = [500.0f32];
        shelf_curve_in_place(&mut dst, None, 500.0, 12.0, 0.0);
        assert!((dst[0] - 1.0).abs() < 2e-6, "centro={}", dst[0]);

        // com G > 0 a curva cresce com v (sigma cresce), com G < 0 decresce
        let small = [1.0f32];
        let big = [10000.0f32];
        let mut cs = small;
        let mut cb = big;
        shelf_curve_in_place(&mut cs, None, 500.0, 12.0, 24.0);
        shelf_curve_in_place(&mut cb, None, 500.0, 12.0, 24.0);
        assert!(cb[0] > cs[0]);
        let mut cs = small;
        let mut cb = big;
        shelf_curve_in_place(&mut cs, None, 500.0, 12.0, -24.0);
        shelf_curve_in_place(&mut cb, None, 500.0, 12.0, -24.0);
        assert!(cb[0] < cs[0]);
    }

    #[test]
    fn shelf_pair_composes_two_curves_in_order() {
        // Aplica curva1 (A interno 500) e curva2 (A interno 2000) e confere que o
        // resultado e o produto na ordem das duas chamadas de 0x1340.
        let probe = [500.0f32, 2000.0, 10.0];
        let a1 = 500.0f32;
        let a2 = 2000.0f32;

        let l1 = a1.max(EPS).log10();
        let mut c1 = vec![0.0f32; probe.len()];
        shelf_curve_in_place(&mut c1, Some(&probe), C_500_0, C_12_0, -20.0 * l1);
        let s1 = powf_ucrt(C_10_0, C_0_5 * l1);
        for v in c1.iter_mut() {
            *v *= s1;
        }
        let l2 = a2.max(EPS).log10();
        let mut c2 = vec![0.0f32; probe.len()];
        shelf_curve_in_place(&mut c2, Some(&probe), C_2000_0, C_12_0, -20.0 * l2);
        let s2 = powf_ucrt(C_10_0, C_0_5 * l2);
        for v in c2.iter_mut() {
            *v *= s2;
        }

        let mut dst = [1.0f32; 3];
        shelf_pair_apply(&mut dst, &probe, a1, a2);
        for i in 0..3 {
            let want = c1[i] * c2[i];
            assert!(
                (dst[i] - want).abs() / want < 1e-6,
                "i={i} got={} want={want}",
                dst[i]
            );
        }
        // v = A2 = 2000 -> sigma2 = 1/2 -> curva2 = sqrt(2000)
        assert!((c2[1] - 2000.0f32.sqrt()).abs() / 44.72 < 1e-5);
    }

    #[test]
    fn gain_scale_matches_closed_form() {
        // s0 = 0 -> T = 0, y = exp(-ln10)-0.1 (residuo de arredondamento) e u*v finito
        let z = band_gain_scale(0.0, 1.0);
        assert!(z.abs() < 1e-8, "scale(0,1)={z}");
        // a = 1, s0 = 1: u = 2, y = 10^2.4, v = 10^-1.2 -> 2*10^1.2
        let got = band_gain_scale(1.0, 1.0);
        let want = 2.0f32 * C_10_0.powf(1.2);
        assert!((got - want).abs() / want < 1e-3, "got={got} want={want}");
    }

    #[test]
    fn roughness_flags_small_variation() {
        assert_eq!(roughness_mean(&[1.0f32; 8]), Some(0.0));
        assert_eq!(roughness_mean(&[0.0, 1.0, 0.0, 1.0]), None);
        assert!(roughness_mean(&[]).is_none());
    }
}
