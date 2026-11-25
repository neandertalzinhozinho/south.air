//! Etapa M1 - confere `port/src/div.rs` (transcrição escalar de `0x63640`) contra as
//! **mesmas instruções AVX/FMA** executadas pelo hardware, bit a bit.
//!
//! Precedente: `checks/j_dot32_avx.rs`. Não carrega o plugin, não executa código do
//! dump: o emulador abaixo é a sequência de `checks/63640.dis` reescrita com
//! intrinsics, instrução por instrução (RVA em cada linha), sobre ponteiros reais
//! (o alinhamento de `dst` é lido do ponteiro, como em `0006366A and rdi,0x1c`).
//!
//! Compilar e rodar:
//! `rustc --edition 2021 -O checks/j_div_avx.rs -o checks/.build/j_div_avx.exe`
//! (ou `--test`: o mesmo conteúdo roda como `div_rs_matches_avx_fma_hardware`,
//! que é como `port/run_tests.ps1` o executa).
//!
//! Veredito: para toda lane cujo resultado **não** é NaN, os bits têm de ser iguais;
//! quando o resultado é NaN, os dois lados têm de ser NaN. O **sinal/payload** do NaN
//! não entra no veredito: depende da ordem de operandos que o LLVM escolhe para
//! `vmulps`/`vfmadd*`/`vfnmadd*` (comutativos para ele) — medido em 2026-11-25, o
//! próprio emulador dá payloads diferentes em `-O`, debug e `+fma` (ex.: `den` sNaN
//! `0x7FA00001` → `0xFFE00001` num build e `0x7FE00001` no outro). Por isso o payload
//! de NaN do port fica `NÃO PROVADO`; é contado à parte. No estágio o denominador é
//! clampado em `1e-7` e só vira NaN se a entrada já for NaN.

#![allow(dead_code)]

#[path = "../port/src/div.rs"]
mod div;

use std::arch::x86_64::*;

#[repr(C, align(64))]
struct Scratch([f32; 16]);

/// `fixup` do binário sobre bits (`000637C1`..`000637EC`).
#[inline]
fn fixup_bits(num: u32) -> u32 {
    let eax = num & 0x7fff_ffff; // 000637C8
    if (eax as i32) > 0x7f80_0000 || eax == 0 {
        0x7fbf_ffff // 000637EC
    } else {
        (num & 0x8000_0000).wrapping_add(0x7f80_0000) // 000637D8/000637DF
    }
}

/// Bloco **A** sobre o scratch (`s[0..8]` = den, `s[8..16]` = num), resultado em `s[0..8]`.
/// Cabeça `0006375E`..`000639F8`; resto `000640BA`..`0006432F` (mesma sequência).
#[target_feature(enable = "avx2,fma")]
unsafe fn block_a_scratch(s: *mut f32, one: __m256) {
    unsafe {
        let ymm2 = _mm256_loadu_ps(s); // 0006375E
        let zero = _mm256_setzero_ps(); // 00063766
        let ymm1 = _mm256_cmp_ps::<_CMP_EQ_OQ>(ymm2, zero); // 0006376A vcmpeqps
        let ymm5 = _mm256_blendv_ps(ymm2, one, ymm1); // 0006376F
        let ymm0 = _mm256_rcp_ps(ymm5); // 00063775
        let nz = _mm256_cmp_ps::<_CMP_NEQ_OQ>(ymm0, zero); // 00063779
        let ymm3 = _mm256_and_ps(ymm5, nz); // 0006377E
        let ymm3 = _mm256_fnmadd_ps(ymm0, ymm3, one); // 00063782 vfnmadd213ps ymm3,ymm0,ymm4
        let q0 = _mm256_mul_ps(ymm0, _mm256_loadu_ps(s.add(8))); // 00063787
        let q = _mm256_fmadd_ps(ymm3, q0, q0); // 00063791 vfmadd213ps ymm2,ymm3,ymm0
        let q = _mm256_fmadd_ps(ymm3, q, q0); // 00063796
        if _mm256_testz_ps(ymm1, ymm1) != 0 {
            _mm256_storeu_ps(s, q); // 000637A2
            return;
        }
        let mask = _mm256_movemask_ps(ymm1); // 000637AD
        for i in 0..8 {
            if mask & (1 << i) != 0 && (*s.add(i)).to_bits() == 0 {
                // 000637BA cmp dword [r13+4i],0
                *s.add(i) = f32::from_bits(fixup_bits((*s.add(8 + i)).to_bits()));
            }
        }
        let r = _mm256_blendv_ps(q, _mm256_loadu_ps(s), ymm1); // 000639F1
        _mm256_storeu_ps(s, r); // 000639F8
    }
}

/// `0x63640` emulado: `rcx = den`, `rdx = num`, `r8 = dst`, `r9d = n`.
#[target_feature(enable = "avx2,fma")]
unsafe fn emu_63640(den: *const f32, num: *const f32, dst: *mut f32, n: i32) {
    unsafe {
        let one = _mm256_loadu_ps([1.0f32; 8].as_ptr()); // 0006368F ymm4 = [0x1DF9DA0]
        let mut sc = Scratch([0.0; 16]);
        let s = sc.0.as_mut_ptr(); // 0006365E..00063666 r13 = (rsp+0xaf) & ~0x3f
        let (mut rcx, mut rbp, mut r8, mut r9d) = (den, num, dst, n);
        let mut edi = (dst as usize & 0x1c) as i32; // 0006366A

        // --- cabeça ---------------------------------------------------------
        if edi != 0 {
            // 00063697/00063699
            edi >>= 2; // 0006369F
            edi = 8 - edi; // 000636A2/000636A4
            _mm256_storeu_ps(s, one); // 000636AA
            _mm256_storeu_ps(s.add(8), one); // 000636B0
            if edi >= r9d {
                edi = r9d; // 000636A7/000636B6 cmovge
            }
            let r10 = edi as isize; // 000636BA
            for i in 0..r10.max(0) {
                // 000636C0..00063757 (h < 8 => laço escalar)
                *s.offset(i) = *rcx.offset(i);
                *s.offset(8 + i) = *rbp.offset(i);
            }
            block_a_scratch(s, one);
            for i in 0..r10.max(0) {
                *r8.offset(i) = *s.offset(i); // 000639FE..00063A4F
            }
            r9d -= edi; // 00063A51
            rcx = rcx.offset(r10); // 00063A54
            rbp = rbp.offset(r10); // 00063A58
            r8 = r8.offset(r10); // 00063A5D
        }

        // --- laço de 16, aritmética B --------------------------------------
        let n16 = r9d >> 4; // 00063A67 sar
        let zero = _mm256_setzero_ps(); // 00063AA1
        for _ in 0..n16.max(0) {
            let mut y7 = _mm256_loadu_ps(rcx); // 00063AC0
            let mut y6 = _mm256_loadu_ps(rcx.add(8)); // 00063AC6
            let y5 = _mm256_cmp_ps::<_CMP_EQ_OQ>(y7, zero); // 00063ACD
            let y3 = _mm256_cmp_ps::<_CMP_EQ_OQ>(y6, zero); // 00063AD2
            let any = _mm256_or_ps(y5, y3); // 00063AD7
            let mut dl = false;
            if _mm256_testz_ps(any, any) == 0 {
                y7 = _mm256_blendv_ps(y7, one, y5); // 00063AE2
                dl = true; // 00063AE8
                y6 = _mm256_blendv_ps(y6, one, y3); // 00063AEA
            }
            let y0 = _mm256_rcp_ps(y7); // 00063AF0
            let y1 = _mm256_rcp_ps(y6); // 00063AF4
            let y9 = _mm256_cmp_ps::<_CMP_EQ_OQ>(y0, zero); // 00063AF8
            let y10 = _mm256_cmp_ps::<_CMP_EQ_OQ>(y1, zero); // 00063AFD
            let z = _mm256_or_ps(y9, y10); // 00063B02
            if _mm256_testz_ps(z, z) == 0 {
                y7 = _mm256_andnot_ps(y9, y7); // 00063B0E
                y6 = _mm256_andnot_ps(y10, y6); // 00063B12
            }
            let e7 = _mm256_fnmadd_ps(y0, y7, one); // 00063B16 vfnmadd213ps ymm7,ymm0,ymm4
            let e6 = _mm256_fnmadd_ps(y1, y6, one); // 00063B1B
            let r = _mm256_fmadd_ps(e7, y0, y0); // 00063B24 vfmadd213ps ymm8,ymm7,ymm0
            let r = _mm256_fmadd_ps(e7, r, y0); // 00063B29
            let h = _mm256_fmadd_ps(e6, y1, y1); // 00063B32
            let mut q7 = _mm256_mul_ps(r, _mm256_loadu_ps(rbp)); // 00063B37
            let h = _mm256_fmadd_ps(e6, h, y1); // 00063B3D
            let mut q0 = _mm256_mul_ps(h, _mm256_loadu_ps(rbp.add(8))); // 00063B42
            if dl {
                // 00063B49
                let mask = (_mm256_movemask_ps(y3) << 8) | _mm256_movemask_ps(y5); // 00063B51..00063B5C
                _mm256_storeu_ps(s, zero); // 00063B5E
                _mm256_storeu_ps(s.add(8), zero); // 00063B64
                for i in 0..16 {
                    if mask & (1 << i) != 0 && (*rcx.add(i)).to_bits() == 0 {
                        // 00063B6F cmp dword [r15+rdi],0
                        *s.add(i) = f32::from_bits(fixup_bits((*rbp.add(i)).to_bits()));
                    }
                }
                q7 = _mm256_blendv_ps(q7, _mm256_loadu_ps(s), y5); // 00063FB3
                q0 = _mm256_blendv_ps(q0, _mm256_loadu_ps(s.add(8)), y3); // 00063FBC
            }
            _mm256_storeu_ps(r8, q7); // 00063FCB
            _mm256_storeu_ps(r8.add(8), q0); // 00063FD6
            rcx = rcx.add(16); // 00063FC6
            rbp = rbp.add(16); // 00063FD1
            r8 = r8.add(16); // 00063FDD
        }

        // --- bloco de 8, aritmética A (000643DD..0006468D) -----------------
        if r9d & 8 != 0 {
            // 0006400D
            let y3 = _mm256_loadu_ps(rcx); // 000643DD
            let y5 = _mm256_loadu_ps(rbp); // 000643E3
            _mm256_storeu_ps(s, y3); // 000643E8
            _mm256_storeu_ps(s.add(8), y5); // 000643EE
            let z = _mm256_setzero_ps(); // 000643F4
            let y1 = _mm256_cmp_ps::<_CMP_EQ_OQ>(y3, z); // 000643F8
            let y2 = _mm256_blendv_ps(y3, one, y1); // 000643FD
            let r0 = _mm256_rcp_ps(y2); // 00064403
            let nz = _mm256_cmp_ps::<_CMP_NEQ_OQ>(r0, z); // 00064407
            let q0 = _mm256_mul_ps(r0, y5); // 0006440C
            let d = _mm256_and_ps(y2, nz); // 00064410
            let e = _mm256_fnmadd_ps(r0, d, one); // 00064414 vfnmadd213ps ymm2,ymm3,ymm4
            let q = _mm256_fmadd_ps(e, q0, q0); // 0006441D
            let mut q = _mm256_fmadd_ps(e, q, q0); // 00064422
            if _mm256_testz_ps(y1, y1) == 0 {
                let mask = _mm256_movemask_ps(y1); // 00064439
                for i in 0..8 {
                    if mask & (1 << i) != 0 && (*s.add(i)).to_bits() == 0 {
                        // 00064442
                        *s.add(i) = f32::from_bits(fixup_bits((*s.add(8 + i)).to_bits()));
                    }
                }
                q = _mm256_blendv_ps(q, _mm256_loadu_ps(s), y1); // 0006466D
            }
            _mm256_storeu_ps(s, q); // 0006442E / 00064674
            _mm256_storeu_ps(r8, q); // 0006467A
            rcx = rcx.add(8); // 00064681
            rbp = rbp.add(8); // 00064685
            r8 = r8.add(8); // 00064689
        }

        // --- resto 1..7, aritmética A (0006401A..0006438F) -----------------
        let rem = r9d & 7; // 0006401A
        if rem != 0 {
            _mm256_storeu_ps(s, one); // 00064024
            _mm256_storeu_ps(s.add(8), one); // 0006402A
            for i in 0..rem as usize {
                // 00064036..000640B8
                *s.add(i) = *rcx.add(i);
                *s.add(8 + i) = *rbp.add(i);
            }
            block_a_scratch(s, one); // 000640BA..0006432F
            for i in 0..rem as usize {
                *r8.add(i) = *s.add(i); // 0006433C..0006438F
            }
        }
    }
}

fn lcg(state: &mut u64) -> u64 {
    *state = state
        .wrapping_mul(6364136223846793005)
        .wrapping_add(1442695040888963407);
    *state
}

const SPECIAL: [u32; 18] = [
    0x0000_0000, // +0
    0x8000_0000, // -0
    0x0000_0001, // menor denormal
    0x007f_ffff, // maior denormal
    0x0080_0000, // MIN_POSITIVE
    0x7f7f_ffff, // f32::MAX (vrcpps -> 0)
    0x7e80_0000, // 2^126
    0x7e00_0000, // 2^125
    0x7f80_0000, // +inf
    0xff80_0000, // -inf
    0x7fc0_0000, // qNaN
    0x7fa0_0001, // sNaN
    0x33d6_bf95, // CLAMP_MIN do estágio (1e-7)
    0x3f80_0000, // 1.0
    0xbf80_0000, // -1.0
    0x4040_0000, // 3.0
    0x4b18_9680, // 1e7
    0x0040_0000, // denormal
];

/// den positivo no domínio do estágio (`>= 1e-7`) na maior parte; às vezes especial.
fn rand_val(state: &mut u64, special_rate: u64) -> f32 {
    let r = lcg(state);
    if (r >> 56) % 100 < special_rate {
        return f32::from_bits(SPECIAL[((r >> 32) as usize) % SPECIAL.len()]);
    }
    // expoente amplo: [2^-24, 2^40), sinal aleatório
    let mant = ((r >> 8) & 0x7f_ffff) as u32;
    let exp = 103 + ((r >> 40) % 64) as u32;
    let sign = ((r >> 50) & 1) as u32;
    f32::from_bits((sign << 31) | (exp << 23) | mant)
}

fn main() {
    run();
}

/// Mesmo conteúdo de `main`, para o runner (`rustc --test`) executar de fato.
#[test]
fn div_rs_matches_avx_fma_hardware() {
    run();
}

fn run() {
    assert!(
        is_x86_feature_detected!("avx2") && is_x86_feature_detected!("fma"),
        "precisa de AVX2/FMA"
    );
    let mut seed = 0x0063_640d_1550_c560u64;
    let mut lanes = 0usize;
    let mut bad = 0usize;
    let mut nan_lanes = 0usize;
    let mut nan_payload_diff = 0usize;
    let mut calls = 0usize;
    let mut head_calls = 0usize;

    let mut ns: Vec<usize> = (1..=80).collect();
    ns.extend_from_slice(&[255, 256, 257, 258, 513]);

    for &n in &ns {
        for off_bytes in (0..32).step_by(4) {
            for round in 0..60 {
                let special = if round % 3 == 0 { 25 } else { 0 };
                let den: Vec<f32> = (0..n).map(|_| rand_val(&mut seed, special)).collect();
                let num: Vec<f32> = (0..n).map(|_| rand_val(&mut seed, special)).collect();

                let mut a = vec![0.0f32; n + 16];
                let base = a.as_ptr() as usize;
                let start = ((32 - base % 32) % 32 + off_bytes) / 4;
                let mut b = vec![0.0f32; n + 16];
                let base_b = b.as_ptr() as usize;
                let start_b = ((32 - base_b % 32) % 32 + off_bytes) / 4;
                assert_eq!(a[start..].as_ptr() as usize & 0x1c, off_bytes);
                assert_eq!(b[start_b..].as_ptr() as usize & 0x1c, off_bytes);

                unsafe {
                    emu_63640(den.as_ptr(), num.as_ptr(), a.as_mut_ptr().add(start), n as i32);
                }
                div::div_block(&num, &den, &mut b[start_b..start_b + n]);
                calls += 1;
                if off_bytes != 0 {
                    head_calls += 1;
                }

                for i in 0..n {
                    let (x, y) = (a[start + i], b[start_b + i]);
                    lanes += 1;
                    if x.is_nan() {
                        nan_lanes += 1;
                    }
                    if x.to_bits() != y.to_bits() {
                        if x.is_nan() && y.is_nan() {
                            nan_payload_diff += 1;
                            continue;
                        }
                        bad += 1;
                        if bad <= 10 {
                            println!(
                                "DIFF n={n} off={off_bytes} i={i} den={:08x} num={:08x} hw={:08x} port={:08x}",
                                den[i].to_bits(),
                                num[i].to_bits(),
                                x.to_bits(),
                                y.to_bits()
                            );
                        }
                    }
                }
            }
        }
    }

    // Domínio do estágio: n = 257 (48 kHz, `div::stage_division_len(48000.0)`), dst alinhado.
    let n = div::stage_division_len(48000.0) as usize;
    let mut stage_bad = 0usize;
    for _ in 0..2000 {
        let den: Vec<f32> = (0..n)
            .map(|_| {
                let v = rand_val(&mut seed, 0).abs();
                if v < f32::from_bits(0x33d6_bf95) {
                    f32::from_bits(0x33d6_bf95)
                } else {
                    v
                }
            })
            .collect();
        let num: Vec<f32> = (0..n).map(|_| rand_val(&mut seed, 0).abs()).collect();
        let mut a = vec![0.0f32; n + 16];
        let start = ((32 - a.as_ptr() as usize % 32) % 32) / 4;
        let mut b = vec![0.0f32; n];
        unsafe {
            emu_63640(den.as_ptr(), num.as_ptr(), a.as_mut_ptr().add(start), n as i32);
        }
        div::div_block_mod32(&num, &den, &mut b, 0);
        for i in 0..n {
            lanes += 1;
            if a[start + i].to_bits() != b[i].to_bits() {
                stage_bad += 1;
            }
        }
    }

    println!(
        "calls={calls} (com cabeça: {head_calls}) lanes={lanes} bad={bad} stage_n={n} stage_bad={stage_bad} \
         lanes_NaN={nan_lanes} payload_NaN_difere={nan_payload_diff} (fora do veredito)"
    );
    assert_eq!(bad, 0, "port/src/div.rs divergiu do hardware AVX/FMA");
    assert_eq!(stage_bad, 0, "port/src/div.rs divergiu no domínio do estágio");
}
