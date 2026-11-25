//! Etapa J2 - ordem de soma de `0x5F5C0` (produto escalar) para `n = 16` e `n = 32`.
//!
//! Prova da ordem (dump, `checks/p_dot_full.dis`):
//!   0005F680  vmovups ymm2,[r10+r11*4]      ; b[0..8]   (r11=0) / b[16..24] (r11=16)
//!   0005F686  vmovups ymm3,[r10+r11*4+0x20] ; b[8..16]  / b[24..32]
//!   0005F68D  vfmadd231ps ymm1, ymm2, [rcx+r11*4]
//!   0005F693  vfmadd231ps ymm0, ymm3, [rcx+r11*4+0x20]
//!   0005F6A3  vaddps ymm0, ymm1, ymm0
//!   0005F6A7  vextractf128 xmm1, ymm0, 1
//!   0005F6AD  vaddps xmm2, xmm0, xmm1
//!   0005F6B1  vmovhlps xmm3, xmm2, xmm2
//!   0005F6B5  vaddps xmm4, xmm2, xmm3
//!   0005F6B9  vshufps xmm5, xmm4, xmm4, 0xf5
//!   0005F6BE  vaddss xmm0, xmm4, xmm5
//!
//! `n = 32` e `n = 16` caem em `0005F705` (`and r8d,~15`) sem prefixo escalar:
//! `n = 16` -> 1 iteracao do laco; `n = 32` -> 2 iteracoes.
//!
//! Este programa confere a emulacao escalar contra as **mesmas instrucoes AVX/FMA**
//! executadas por hardware, bit a bit. Compilar com:
//! `rustc -O -C target-feature=+avx2,+fma checks/j_dot32_avx.rs -o j_dot32_avx`

use std::arch::x86_64::*;

/// Emulacao escalar, na ordem exata do binario (FMA separado do `vaddps`).
pub fn dot_scalar(a: &[f32], b: &[f32], n: usize) -> f32 {
    assert!(n == 16 || n == 32, "0x5F5C0: n={n} NAO EXTRAIDO");
    let mut acc0 = [0f32; 8]; // ymm1
    let mut acc1 = [0f32; 8]; // ymm0
    let chunks = n / 16;
    for c in 0..chunks {
        for i in 0..8 {
            acc0[i] = b[c * 16 + i].mul_add(a[c * 16 + i], acc0[i]); // vfmadd231ps
        }
        for i in 0..8 {
            acc1[i] = b[c * 16 + 8 + i].mul_add(a[c * 16 + 8 + i], acc1[i]);
        }
    }
    let mut l = [0f32; 8];
    for i in 0..8 {
        l[i] = acc0[i] + acc1[i]; // vaddps ymm0, ymm1, ymm0
    }
    let x2 = [l[0] + l[4], l[1] + l[5], l[2] + l[6], l[3] + l[7]]; // vaddps xmm2
    let x4 = [x2[0] + x2[2], x2[1] + x2[3]]; // vmovhlps + vaddps
    x4[0] + x4[1] // vshufps 0xf5 + vaddss
}

#[target_feature(enable = "avx2,fma")]
unsafe fn dot_avx(a: &[f32], b: &[f32], n: usize) -> f32 {
    let mut acc0 = _mm256_setzero_ps(); // ymm1
    let mut acc1 = _mm256_setzero_ps(); // ymm0
    let chunks = n / 16;
    for c in 0..chunks {
        let base = c * 16;
        let b0 = _mm256_loadu_ps(b.as_ptr().add(base));
        let a0 = _mm256_loadu_ps(a.as_ptr().add(base));
        acc0 = _mm256_fmadd_ps(b0, a0, acc0);
        let b1 = _mm256_loadu_ps(b.as_ptr().add(base + 8));
        let a1 = _mm256_loadu_ps(a.as_ptr().add(base + 8));
        acc1 = _mm256_fmadd_ps(b1, a1, acc1);
    }
    let s = _mm256_add_ps(acc0, acc1); // 0005F6A3
    let hi = _mm256_extractf128_ps(s, 1); // 0005F6A7
    let lo = _mm256_castps256_ps128(s);
    let x2 = _mm_add_ps(lo, hi); // 0005F6AD
    let x3 = _mm_movehl_ps(x2, x2); // 0005F6B1
    let x4 = _mm_add_ps(x2, x3); // 0005F6B5
    let x5 = _mm_shuffle_ps::<0xf5>(x4, x4); // 0005F6B9
    _mm_cvtss_f32(_mm_add_ss(x4, x5)) // 0005F6BE
}

fn lcg(state: &mut u64) -> u64 {
    *state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    *state
}

/// f32 aleatorio em [-1,1] a partir de 24 bits (mantem exatidao previsivel).
fn rand_f32(state: &mut u64) -> f32 {
    let v = ((lcg(state) >> 40) as i32 - (1 << 23)) as f32 / (1 << 23) as f32;
    v
}

fn main() {
    let mut seed = 0x1234_5678_9abc_def0u64;
    let mut bad = 0usize;
    let mut total = 0usize;
    let mut naive_bad = 0usize;

    for n in [16usize, 32] {
        for _ in 0..200_000 {
            let mut a = vec![0f32; n];
            let mut b = vec![0f32; n];
            for i in 0..n {
                a[i] = rand_f32(&mut seed);
                b[i] = rand_f32(&mut seed);
            }
            let s = dot_scalar(&a, &b, n);
            let v = unsafe { dot_avx(&a, &b, n) };
            total += 1;
            if s.to_bits() != v.to_bits() {
                bad += 1;
                if bad < 8 {
                    println!(
                        "DIFF n={n} scalar={:08x} avx={:08x}",
                        s.to_bits(),
                        v.to_bits()
                    );
                }
            }
            // referencia ingenua: soma sequencial com FMA (nao e a ordem do alvo)
            let mut naive = 0.0f32;
            for i in 0..n {
                naive = a[i].mul_add(b[i], naive);
            }
            if naive.to_bits() != v.to_bits() {
                naive_bad += 1;
            }
        }
    }

    // Vetores fixos para embutir como teste em stage_j_core.rs
    let a32: [f32; 32] = core::array::from_fn(|i| (i as f32 + 1.0) * 0.01);
    let b32: [f32; 32] = core::array::from_fn(|i| 1.0 - (i as f32) * 0.03);
    let a16: [f32; 16] = core::array::from_fn(|i| (i as f32 + 1.0) * 0.07);
    let b16: [f32; 16] = core::array::from_fn(|i| 0.5 + (i as f32) * 0.01);
    println!("fixo32 bits={:08x} scalar={:?}", dot_scalar(&a32, &b32, 32).to_bits(), dot_scalar(&a32, &b32, 32));
    println!("fixo16 bits={:08x} scalar={:?}", dot_scalar(&a16, &b16, 16).to_bits(), dot_scalar(&a16, &b16, 16));

    println!("total={total} bad={bad} naive_difere={naive_bad}");
    assert_eq!(bad, 0, "emulacao escalar divergiu do hardware AVX/FMA");
}
