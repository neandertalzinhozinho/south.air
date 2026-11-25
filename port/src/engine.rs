//! Etapa J6 — esqueleto G/H (detector, smoother, curvas e escalar de ganho).
//!
//! Fonte: `dumpsooth/nyx_soothe3_dump.bin` (SHA-256
//! `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`).
//!
//! Cada funcao abaixo aponta a instrucao + RVA. O que nao foi provado fica
//! marcado `NAO PROVADO` no comentario e **nao** e inventado.
//!
//! ## O que esta fechado aqui
//!
//! * `0x8C3C20` — smoother forward/backward, `a = 0.1f` (`checks/h_detector_ganho.md`
//!   §B.2, `008C3C90`/`008C3D50`);
//! * `0x8C0BD0` — detector de 2 planos `R = (P0²+P1²)/max(P0+P1, eps)` e
//!   `P_k = (1-g)·P_k + g·R` (`checks/h_primitivas_8c0bd0.md` §3.1);
//! * `0x8B68AB` — coeficiente do one-pole `1 − 0.1^(1/x)` (`checks/p_8b68ab.dis`);
//! * `0x88E130` — curva sigmoide `A^(1−σ)` (`checks/88e130.u8.dis`); o recíproco
//!   `0088E32F` (`0x1C8530` -> `0x29B260`) é `crate::rcp::inv_32f_in_place`,
//!   transcrito bit a bit em M2 (`checks/s_reciproco_88e130.md`);
//! * `0x882FC0` — par de curvas `A1^(1−σ1)·A2^(1−σ2)` (`checks/882fc0.u8.dis`);
//! * `0x8B5AF2`–`0x8B5CA7` — escalar de ganho `u·(y·v)` (ordem exata lida no dump).
//!
//! ## `NAO PROVADO` (nao implementado como se fosse verdade)
//!
//! * (M3, 2026-11-25) `0x293760` (`ln` da IPP) e `0x240C00` (`exp` da IPP) sairam
//!   daqui: `ipp_ln`/`ipp_exp` chamam `crate::ippmath`, transcrito bit a bit e
//!   conferido contra o hardware em `checks/j_ln_exp_avx.rs`. A IPP **difere** de
//!   `f32::ln`/`f32::exp` (ate alguns ulp), entao a troca muda bits das curvas.
//! * o significado fisico de `s0`, `A`, `A1`, `A2`, `k`, `G`; e a atribuicao
//!   grupo→coeficiente de §8.4.8 (`NAO EXTRAIDO`, sem tabela no codigo).
//!
//! `rustc --edition 2021 --test checks\stage_j_engine.rs -o checks\.build\j6.exe`

#![allow(dead_code)]
#![allow(clippy::excessive_precision)]

// ---------------------------------------------------------------------------
// Constantes lidas do dump
// ---------------------------------------------------------------------------

/// `0x2079CF0` = `2^-23` (`1.19209290e-7f`).
pub const EPS: f32 = 1.1920929e-7;
/// `0x2079DB0` = `0.1f` (smoother e `0x88E130`).
pub const C_0_1: f32 = 0.1;
/// `0x2079F9C` = `1.0f`.
pub const C_1_0: f32 = 1.0;
/// `0x2079EA8` = `0.5f`.
pub const C_0_5: f32 = 0.5;
/// `0x2079F38` = `0.800000012f`.
pub const C_0_8: f32 = 0.800000012;
/// `0x207A2D8` = `5.00000048f`.
pub const C_5_000_000_5: f32 = 5.0000005;
/// `0x207A00C` = `ln 4` = `1.38629436f`.
pub const C_LN4: f32 = 1.3862944;
/// `0x207A1E8` = `2.4000001f`.
pub const C_2_4: f32 = 2.4000001;
/// `0x207A1D0` / `0x207A6D4` = `±ln 10` = `±2.30258512f`.
pub const C_LN10: f32 = 2.3025851;
/// `0x207A360` = `10.0f`.
pub const C_10_0: f32 = 10.0;
/// `0x207A734` = `-24.0f`.
pub const C_NEG_24: f32 = -24.0;
/// `0x2079D88` = `0.05f`.
pub const C_0_05: f32 = 0.05;
/// `0x2079DE0` = `0.166666672f` (`1/6`).
pub const C_1_6: f32 = 0.166666672;
/// `0x207A020` = `log2(e)` = `1.44269502f`.
pub const C_LOG2E: f32 = 1.44269502;
/// `0x2079DBC` = `ln(10)/20` = `0.115129255f`.
pub const C_LN10_20: f32 = 0.115129255;
/// `0x207A690` = `-0.5f`.
pub const C_NEG_0_5: f32 = -0.5;
/// `0x207A560` = `500.0f` (curva A1 de `0x882FC0`).
pub const C_500_0: f32 = 500.0;
/// `0x207A5A8` = `2000.0f` (curva A2 de `0x882FC0`).
pub const C_2000_0: f32 = 2000.0;
/// `0x207A384` = `12.0f` (`k` das duas curvas de `0x882FC0`).
pub const C_12_0: f32 = 12.0;
/// `0x207A030` = `(double)0.1f` (`0x8B68AB`).
pub const C_0_1_F64: f64 = 0.10000000149011612;
/// `0x2079D24` = `0.001f`.
pub const C_0_001: f32 = 0.001;
/// `0x207A560` também é o `500.0f` do one-pole.
pub const C_500_0_ONE_POLE: f32 = 500.0;

// ---------------------------------------------------------------------------
// Math: imports da UCRT vs. implementacoes internas da IPP
// ---------------------------------------------------------------------------

/// `powf` da UCRT (`0x1C9AA01` -> IAT `0x1D8D818`). Equivalencia bit-a-bit
/// provada em `checks/j_crt_equiv.rs`.
#[inline]
pub fn powf_ucrt(base: f32, e: f32) -> f32 {
    base.powf(e)
}

/// `logf` da UCRT (`0x1C9A9FB` -> IAT `0x1D8D808`). Idem.
#[inline]
pub fn logf_ucrt(x: f32) -> f32 {
    x.ln()
}

/// `expf` da UCRT (`0x1C9A9D7` -> IAT `0x1D8D7F0`). Idem.
#[inline]
pub fn expf_ucrt(x: f32) -> f32 {
    x.exp()
}

/// `0x1C8500` -> impl `0x293760` (**ln da IPP**, nao `logf`).
/// M3: transcrito bit a bit em `crate::ippmath` (`checks/t_ln_exp_ipp.md`).
/// Por lane; o status (`eax`) nao e lido pelos chamadores do motor.
#[inline]
pub fn ipp_ln(x: f32) -> f32 {
    crate::ippmath::ln_lane(x).0
}

/// `0x1C84A0` -> impl `0x240C00` (**exp da IPP**, nao `expf`).
/// M3: transcrito bit a bit em `crate::ippmath` (`checks/t_ln_exp_ipp.md`).
#[inline]
pub fn ipp_exp(x: f32) -> f32 {
    crate::ippmath::exp_lane(x).0
}

#[inline]
pub fn clamp01(x: f32) -> f32 {
    // `maxss xmm1,xmm13` (0.0) / `minss xmm1,xmm11` (1.0)
    x.max(0.0).min(1.0)
}

// ---------------------------------------------------------------------------
// 0x8C3C20 — smoother forward/backward (a = 0.1f)
// ---------------------------------------------------------------------------

/// `0x8C3C20` (465 B, 0 chamadas). Por array:
///
/// ```text
/// 008C3C90  p = v[0]; for j: p += (v[j] - p)*0.1f; v[j] = p;
/// 008C3D50  for j = len-2..0: p += (v[j] - p)*0.1f; v[j] = p;
/// ```
pub fn smoother_fwd_back(v: &mut [f32]) {
    if v.is_empty() {
        return;
    }
    let mut p = v[0];
    for x in v.iter_mut() {
        p += (*x - p) * C_0_1; // mulss/subss/addss, sem FMA
        *x = p;
    }
    if v.len() >= 2 {
        let mut p = v[v.len() - 1];
        for j in (0..v.len() - 1).rev() {
            p += (v[j] - p) * C_0_1;
            v[j] = p;
        }
    }
}

// ---------------------------------------------------------------------------
// 0x8C0BD0 — detector de 2 planos (P0/P1) e mistura com g
// ---------------------------------------------------------------------------

/// `0x8C0BD0`, por descritor com `+0x10 == 2` e por amostra
/// (`checks/h_primitivas_8c0bd0.md` §3.1):
///
/// ```text
/// sum2 = P0² + P1²                              (0x1190 + 0x1370)
/// sum  = P0 + P1                                (0x1370)
/// sum  = max(sum, 1.1920929e-7f)                (0x1100 modo 0)
/// R    = sum2 / sum                             (0x1550, dst = num/den)
/// P_k  = (1-g)·P_k + g·R                        (0x1220 + 0x11F0)
/// ```
///
/// Ordem de `P_k`: primeiro `P_k *= (1-g)` (`008C12B9`), depois
/// `P_k += R*g` com FMA (`008C1366`/`008C139C`). `R` usa os valores **originais**.
pub fn detector2_in_place(p0: &mut [f32], p1: &mut [f32], g: f32) {
    let one_minus_g = C_1_0 - g; // 008C12A4 subss
    for (a, b) in p0.iter_mut().zip(p1.iter_mut()) {
        let a0 = *a;
        let b0 = *b;
        let sum2 = a0 * a0 + b0 * b0; // 0x1190 / 0x1370
        let sum = (a0 + b0).max(EPS); // 0x1370 + 0x1100 (modo 0)
        let r = sum2 / sum; // 0x1550: rdx/rcx
        *a = r.mul_add(g, a0 * one_minus_g); // 008C1366, FMA
        *b = r.mul_add(g, b0 * one_minus_g); // 008C139C, FMA
    }
}

// ---------------------------------------------------------------------------
// 0x8B68AB — coeficiente do one-pole
// ---------------------------------------------------------------------------

/// `N = (float)(i64)[ctx+0x60]`
/// `x = ((float)[ctx+0x20] / N) * 0.001f * 500.0f`
///
/// M4 (2026-11-25, `checks/u_estado_m4.md`): `[ctx+0x20] = max(a/k, 44100)`
/// (`0087346D`/`008734C5`), com `a` = taxa do host e `k = max(1,
/// trunc((a+1)/44100))`; `[ctx+0x60] = [ctx+0x28] >> 1` = `N_ctx/2`
/// (`008769CA`..`008769D4`). O gate `[ctx+0x58]` só é `1` no ctx A
/// (`eng+0x5ED8`, `N_ctx = 2048`), então aqui `n = 1024` (medido de 32 a 192 kHz).
/// `coef = 1 − 0.1^(1/x)` em f64, resultado convertido para f32.
///
/// RVAs: `008B68BC`..`008B68E0` (conversao), `008B68F2` (`divss`),
/// `008B68F9`/`008B6901` (`0.001`/`500`), `008B6909 cvtps2pd`,
/// `008B690C divsd`, `008B6918 call pow`, `008B6932 subsd`, `008B6960 cvtpd2ps`.
pub fn one_pole_coef(t: f32, n: i64) -> f32 {
    let nf = n as f32;
    let x = (t / nf) * C_0_001 * C_500_0_ONE_POLE;
    let e = 1.0f64 / (x as f64);
    let p = C_0_1_F64.powf(e);
    (1.0f64 - p) as f32
}

// ---------------------------------------------------------------------------
// 0x88E130 — curva sigmoide A^(1-sigma)
// ---------------------------------------------------------------------------

/// `0x88E130(dst, src, A, k, G)`, ramo geral (`0088E1D8`..`0088E3E5`).
///
/// O binario aplica passadas vetoriais sobre o buffer inteiro, nesta ordem:
///
/// ```text
/// 0088E1DF  A1   = max(A, eps)
/// 0088E208/11 invA = 1.0f / A1                  (divss)
/// 0088E1E7  ks   = k * 0.166666672f
/// 0088E233  dst <- src  (se src->flag@0x80 == 1)
/// 0088E256  dst += eps
/// 0088E275  dst *= invA
/// 0088E298  dst  = ln(dst)                      (IPP ln)
/// 0088E29D  dst *= 1.44269502f                  (log2(e))
/// 0088E2B3  ks   = -ks
/// 0088E2D0  dst *= ks
/// 0088E2EE  dst  = exp(dst)                     (IPP exp)
/// 0088E311  dst += 1.0f
/// 0088E32F  dst  = rcp(dst)                     (0x29B260: vrcpps + 1 passo FMA)
/// 0088E352  dst += -0.5f
/// 0088E376  dst *= G
/// 0088E399  dst *= 0.115129255f
/// 0088E3B7  dst  = exp(dst)                     (IPP exp)
/// ```
///
/// Com `sigma = 1/(1+exp(-(k/6)·log2((v+eps)/A1)))` o resultado e
/// `exp(G·0.115129255·(sigma-0.5))` por amostra. `k == 0` cai no ramo
/// constante (`0088E144`..`0088E1C2`): `dst[i] = 1.0f`.
///
/// `src` = `None` usa `dst` como fonte (equivale a `src->flag != 1`).
pub fn shelf_curve_in_place(dst: &mut [f32], src: Option<&[f32]>, a: f32, k: f32, gain_db: f32) {
    if k.abs() <= EPS {
        // ramo constante: dst <- src (se flag), dst *= 0, dst += 1
        if let Some(s) = src {
            dst.copy_from_slice(s);
        }
        for v in dst.iter_mut() {
            *v = C_1_0; // 0x1220 com 0.0 e 0x12E0 com 1.0
        }
        return;
    }
    let a1 = a.max(EPS); // 0088E1DF maxss
    let inv_a = C_1_0 / a1; // 0088E208 divss
    let ks = -(k * C_1_6); // 0088E1E7, negado em 0088E2B3
    if let Some(s) = src {
        dst.copy_from_slice(s); // 0088E233 (0x10A0)
    }
    for v in dst.iter_mut() {
        *v += EPS; // 0088E256 (0x12E0)
        *v *= inv_a; // 0088E275 (0x1220)
        *v = ipp_ln(*v); // 0088E298
        *v *= C_LOG2E; // 0088E29D..0088E2AB
        *v *= ks; // 0088E2D0
        *v = ipp_exp(*v); // 0088E2EE
        *v += C_1_0; // 0088E311
    }
    // 0088E32F call 0x1C8530 -> 0x29B260, in-place (rcx = rdx), M2: crate::rcp.
    // O status (eax) não é lido por 0x88E130 (0088E334..0088E352).
    crate::rcp::inv_32f_in_place(dst);
    for v in dst.iter_mut() {
        *v += C_NEG_0_5; // 0088E352
        *v *= gain_db; // 0088E376
        *v *= C_LN10_20; // 0088E399
        *v = ipp_exp(*v); // 0088E3B7
    }
}

// ---------------------------------------------------------------------------
// 0x882FC0 — duas curvas aplicadas como multiplicacao de buffers
// ---------------------------------------------------------------------------

/// `0x882FC0`: bloco 1 (`00883054`..`00883112`) e bloco 2 (`0088315E`..`00883212`).
///
/// ```text
/// bw1 = -20.0f * log10f(A1)                    ; 00883054/0088307D
/// curve1 = f88E130(probe, A=500.0f,  k=12.0f, G=bw1)   ; 008830E7
/// curve1 *= powf(10.0f, 0.5f*log10f(A1))       ; 008830EC/00883107/00883112
/// bw2 = -20.0f * log10f(A2)                    ; bloco 2, A=2000.0f
/// curva2 = idem
/// ```
///
/// Aplicacao (`00883217`..`008833B6`): `0x1340(curve, dst, n)` duas vezes, ou
/// seja `dst[i] = dst[i] * curve1[i]` e depois `* curve2[i]`, cada uma com seu
/// arredondamento.
///
/// `probe` e o bloco `b` copiado por `0x882FC0` e usado como fonte das curvas
/// quando `b->flag@0x80 == 1`. `NAO PROVADO`: se essa flag vale 1 nos dois sitios
/// de `0x87BB60` (`0087C231`/`0087C4DA`); aqui `probe` e sempre a fonte.
pub fn shelf_pair_apply(dst: &mut [f32], probe: &[f32], a1: f32, a2: f32) {
    let l1 = a1.max(EPS).log10(); // log10f da UCRT
    let bw1 = -20.0f32 * l1; // 0088307D
    let mut c1 = vec![0.0f32; probe.len()];
    shelf_curve_in_place(&mut c1, Some(probe), C_500_0, C_12_0, bw1);
    let s1 = powf_ucrt(C_10_0, C_0_5 * l1); // 008830EC/00883107
    for v in c1.iter_mut() {
        *v *= s1; // 00883112 (0x1220)
    }

    let l2 = a2.max(EPS).log10();
    let bw2 = -20.0f32 * l2;
    let mut c2 = vec![0.0f32; probe.len()];
    shelf_curve_in_place(&mut c2, Some(probe), C_2000_0, C_12_0, bw2);
    let s2 = powf_ucrt(C_10_0, C_0_5 * l2);
    for v in c2.iter_mut() {
        *v *= s2;
    }

    for i in 0..dst.len() {
        dst[i] *= c1[i]; // 008832E4 (0x1340)
        dst[i] *= c2[i]; // 008833A9 (0x1340)
    }
}

// ---------------------------------------------------------------------------
// 0x8B5AF2..0x8B5CA7 — escalar de ganho u*(y*v)
// ---------------------------------------------------------------------------

/// Ordem exata lida em `checks/giant_8b3ed0.dis`:
///
/// ```text
/// T = clamp((s0 - 0.8f)*5.0f, 0, 1)                        ; 008B5B36/46/6B
/// x = clamp((1.0f - 0.5f*A)*T, 0, 1)                       ; 008B5B21/42/6F/74
/// u = expf(x * ln4)                                        ; 008B5B79/84
/// y = expf((logf(powf(10,2.4)+0.1) + ln10)*clamp01(s0) - ln10) - 0.1f
///                                                          ; 008B5B89..008B5BD5
/// e = (clamp01(A*A) * -24.0f) * 0.05f                      ; 008B5BDD/5BF0/5BF8
/// v = powf(10, e)                                          ; 008B5BFD
/// scale = u * (y * v)                                      ; 008B5C02/008B5C8A
/// ```
///
/// A versao anterior da spec escrevia `u·y·v`; a instrucao e `y*v` primeiro
/// (`008B5C02 mulss xmm7,xmm0`) e `u*(y*v)` depois (`008B5C8A`).
pub fn band_gain_scale(s0: f32, a: f32) -> f32 {
    let t = clamp01((s0 - C_0_8) * C_5_000_000_5);
    let x = clamp01((C_1_0 - C_0_5 * a) * t);
    let u = expf_ucrt(x * C_LN4); // 008B5B84

    let p = powf_ucrt(C_10_0, C_2_4); // 008B5B99
    let l = logf_ucrt(p + C_0_1); // 008B5B9E/5BA6
    let l = (l + C_LN10) * clamp01(s0) - C_LN10; // 5BAB/5BBD/5BC1
    let y = expf_ucrt(l) - C_0_1; // 008B5BC9/5BD5

    let e = (clamp01(a * a) * C_NEG_24) * C_0_05; // 008B5BDD/5BF0/5BF8
    let v = powf_ucrt(C_10_0, e); // 008B5BFD

    u * (y * v) // 008B5C02 / 008B5C8A
}

// ---------------------------------------------------------------------------
// 8.2(a) — rugosidade media de um array de banda
// ---------------------------------------------------------------------------

/// `008B4E20`..`008B4FAC`: media em f64 de `|v[k]-v[k-1]| / (v[k-1]+1e-7)`.
/// Se `m < 0.001` (comparacao em f64) devolve `Some(m)` — o chamador escala o
/// array por `m` (`008B4FA7 call 0x1220`); senao `None`.
///
/// `n = [r13+0x40] >> 2` (`008B4E29`/`008B4E31`) e o numero de floats.
pub fn roughness_mean(v: &[f32]) -> Option<f32> {
    if v.is_empty() {
        return None;
    }
    let mut prev = v[0];
    let mut acc = 0.0f64;
    for &x in &v[1..] {
        let diff = (x - prev) as f64;
        acc += diff.abs() / (prev as f64 + 1e-7); // 008B4E8B..008B4F23
        prev = x;
    }
    let m = (acc / v.len() as f64) as f32; // 008B4F88 divss (acumulado/n)
    if (m as f64) < 0.001 {
        Some(m)
    } else {
        None
    }
}

// ---------------------------------------------------------------------------
// Testes
// ---------------------------------------------------------------------------

