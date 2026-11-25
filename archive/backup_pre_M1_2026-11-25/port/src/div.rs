//! Etapa M1 — divisão `0x1550` → `0x63640` transcrita bit a bit.
//!
//! Fonte: `checks/63640.dis` (`0x63640`–`0x646C0`, 1.006 linhas) e
//! `checks/r_divisao_63640.md`. Cada passo cita o RVA. O que não está provado
//! continua marcado no doc — aqui não há estimativa.
//!
//! ## Assinatura provada
//!
//! `rcx = den`, `rdx = num`, `r8 = dst`, `r9d = n` → `dst[i] = num[i] / den[i]`
//! (`00063676 mov rbp,rdx`, `00063787 vmulps`, `00063B37 vmulps`).
//!
//! ## Duas aritméticas (não são a mesma conta)
//!
//! As duas calculam a **série geométrica truncada** `q0·(1+e+e²)` com FMA, mas
//! partem de pontos diferentes e por isso diferem no ULP:
//!
//! * **A — 8 lanes** (cabeça, bloco de 8 e resto): refina o **quociente**
//!   `q0 = r0·num` (`00063787`, `000640E3`, `0006440C`) e depois
//!   `q = q·e + q0` duas vezes (`00063791`/`00063796`, `000640ED`/`000640F2`,
//!   `0006441D`/`00064422`).
//! * **B — 16 lanes**: refina o **recíproco** `r0 → r0·(1+e+e²)`
//!   (`00063B24`/`00063B29`, addend sempre `r0`) e multiplica no fim
//!   (`00063B37`/`00063B42`).
//!
//! `e = 1 − d·r0` é calculado **uma vez** por lane e reutilizado
//! (`vfnmadd213ps` em `00063782`/`00063B16`/`000640DE`/`00064414`). Não é
//! Newton de verdade (`(1+e)²` seria `1+2e+e²`): é a série truncada, erro
//! `O(e³)`.
//!
//! ## Despacho (ordem provada)
//!
//! 1. **Cabeça** `h = min(8 − ((dst & 0x1c) >> 2), n)` (`0006366A`–`000636B6`):
//!    preenche um scratch de 16 floats com `1.0` (`000636AA`/`000636B0`), copia
//!    `h` de `den`/`num` (`000636E0`–`00063757`), roda **A** e copia `h` de
//!    volta (`00063A20`–`00063A4F`). Só executa se `dst & 0x1c != 0`
//!    (`00063697`/`00063699`).
//! 2. `n16 = (n − h) >> 4` (`00063A67`), laço **B** de 16 (`00063AC0`–`00063FE9`).
//! 3. `(n − h) & 8` (`0006400D`), bloco de 8 **A** (`000643DD`–`0006468D`);
//!    o bloco recalcula `den'` localmente (`000643F8`/`000643FD`).
//! 4. `(n − h) & 7` (`0006401A`), resto 1..7 **A** com padding `1.0`
//!    (`00064024`–`0006438F`).
//!
//! ## Correção de `den == 0` (`fixup`)
//!
//! Quando `den == 0` o lane é substituído (`vcmpeqps` + `vblendvps` em
//! `0006376A`/`0006376F`, `00063ACD`–`00063AEA`, `000640C6`/`000640CB`,
//! `000643F8`/`000643FD`): `den' = 1.0` para o recíproco e o resultado vira
//! `fixup(num)` — `sign(num) | 0x7F800000` (∓inf) para `num` finito ≠ 0 ou
//! infinito, e `0x7FBFFFFF` para `num == 0` ou NaN (`000637C1`–`000637EC`).
//!
//! **Quirk transcrito:** o teste do fixup é `cmp dword ptr [scratch], 0`
//! (`000637BA`, `00063B6F`, `00064442`, `00064112`), que só casa com `+0.0`.
//! `−0.0` casa no `vcmpeqps` (que é IEEE, `−0.0 == +0.0`) mas **não** no
//! `cmp`, então o lane não é reescrito e o blend devolve o que estava no
//! scratch: `−0.0` na cabeça/bloco 8/resto, e `+0.0` no laço de 16 (o scratch é
//! zerado em `00063B5E`/`00063B64`). No estágio isso é inalcançável: o
//! denominador é clampado em `1e-7` (`stage::CLAMP_MIN`).
//!
//! ## Alinhamento
//!
//! A cabeça existe porque `dst` pode não estar num bloco de 32 B. No estágio o
//! destino é a arena, **64 B alinhada** (prova em `checks/r_divisao_63640.md`
//! §5: `0x868B50` faz `(p+0x40) & ~0x3f`), logo `dst & 0x1c == 0` e a cabeça
//! nunca roda. [`div_block_mod32`] recebe esse valor explicitamente; o
//! [`div_block`] genérico o lê do ponteiro.
//!
//! ## `vrcpps`
//!
//! `00063775`/`00063AF0`/`000640D1`/`00064403` são `vrcpps ymm`, não
//! `vdivps`. O port chama a intrinsic `_mm256_rcp_ps` (mesma tabela de 12 bits
//! do hardware, lane a lane; o `ymm` é duas metades de 128 bits com a mesma
//! tabela). O resultado é determinístico nesta CPU e é o único caminho para o
//! bit a bit — não há reimplementação portátil equivalente.

#![allow(dead_code)]

/// Bits do NaN de fixup (`000637EC`, `000639E4`, …): `0x7FBFFFFF`.
pub const FIXUP_NAN: u32 = 0x7FBF_FFFF;

/// `fixup(num)` — `000637C1`–`000637EC` (idêntico em `00063B76`, `00064119`,
/// `00064449`).
///
/// `|num| > 0x7F800000` (NaN) ou `num == ±0.0` → [`FIXUP_NAN`]; senão
/// `sign(num) | 0x7F800000` (∓inf, incluindo `num` já infinito).
#[inline]
pub fn fixup(num: f32) -> f32 {
    let bits = num.to_bits();
    let mag = bits & 0x7FFF_FFFF;
    if mag > 0x7F80_0000 || mag == 0 {
        f32::from_bits(FIXUP_NAN)
    } else {
        f32::from_bits((bits & 0x8000_0000) | 0x7F80_0000)
    }
}

/// `vrcpps` em 8 lanes (`00063775`, `00063AF0`, `000640D1`, `00064403`).
#[cfg(target_arch = "x86_64")]
#[inline]
fn rcp8(x: &[f32; 8]) -> [f32; 8] {
    // SAFETY: todo entry point checa `is_x86_feature_detected!("avx")`.
    unsafe { rcp8_avx(x) }
}

#[cfg(target_arch = "x86_64")]
#[target_feature(enable = "avx")]
unsafe fn rcp8_avx(x: &[f32; 8]) -> [f32; 8] {
    use core::arch::x86_64::{_mm256_loadu_ps, _mm256_rcp_ps, _mm256_storeu_ps};
    unsafe {
        let v = _mm256_loadu_ps(x.as_ptr());
        let r = _mm256_rcp_ps(v);
        let mut out = [0.0f32; 8];
        _mm256_storeu_ps(out.as_mut_ptr(), r);
        out
    }
}

#[cfg(not(target_arch = "x86_64"))]
fn rcp8(_x: &[f32; 8]) -> [f32; 8] {
    panic!("0x63640 usa vrcpps ymm: só existe em x86-64 com AVX");
}

/// `den' = blend(den, 1.0, den == 0)` (`0006376F`, `00063AE2`, `000640CB`,
/// `000643FD`). `vcmpeqps` é IEEE: `−0.0` também casa; NaN não.
#[inline]
fn blend_den(den: f32) -> f32 {
    if den == 0.0 {
        1.0
    } else {
        den
    }
}

/// `nz = (r0 != 0)` do `vcmpneq_oqps` (`00063779`, `00063AF8`, `000640D5`,
/// `00064407`): falso para NaN e para `±0.0`.
#[inline]
fn rcp_nonzero(r0: f32) -> bool {
    !r0.is_nan() && r0 != 0.0
}

/// `d = den' & mask` (`vandps` em `0006377E`/`000640DA`,
/// `vandnps` em `00063B0E`/`00063B12`).
#[inline]
fn masked_den(denp: f32, nz: bool) -> f32 {
    if nz {
        denp
    } else {
        0.0
    }
}

/// `e = 1 − d·r0` — `vfnmadd213ps` (`00063782`, `00063B16`, `000640DE`,
/// `00064414`). FMA, uma única arredondagem.
#[inline]
fn residual(d: f32, r0: f32) -> f32 {
    (-d).mul_add(r0, 1.0)
}

/// **A** — 8 lanes, refina o quociente (`00063787`–`00063796`,
/// `000640E3`–`000640F2`, `0006440C`–`00064422`).
fn lanes_a(den: &[f32; 8], num: &[f32; 8]) -> [f32; 8] {
    let mut denp = [0.0f32; 8];
    for i in 0..8 {
        denp[i] = blend_den(den[i]);
    }
    let r0 = rcp8(&denp);
    let mut out = [0.0f32; 8];
    for i in 0..8 {
        let d = masked_den(denp[i], rcp_nonzero(r0[i]));
        let e = residual(d, r0[i]);
        let q0 = r0[i] * num[i]; // vmulps, não FMA
        let q = q0.mul_add(e, q0);
        out[i] = q.mul_add(e, q0);
    }
    out
}

/// **B** — 8 lanes (metade de um bloco de 16), refina o recíproco
/// (`00063B20`–`00063B42`).
fn lanes_b8(den: &[f32; 8], num: &[f32; 8]) -> [f32; 8] {
    let mut denp = [0.0f32; 8];
    for i in 0..8 {
        denp[i] = blend_den(den[i]);
    }
    let r0 = rcp8(&denp);
    let mut out = [0.0f32; 8];
    for i in 0..8 {
        let d = masked_den(denp[i], rcp_nonzero(r0[i]));
        let e = residual(d, r0[i]);
        let r1 = r0[i].mul_add(e, r0[i]);
        let r2 = r1.mul_add(e, r0[i]);
        out[i] = r2 * num[i]; // vmulps no fim
    }
    out
}

/// **B** — 16 lanes: duas metades independentes (`00063AF0`/`00063AF4`).
fn lanes_b16(den: &[f32; 16], num: &[f32; 16]) -> [f32; 16] {
    let mut lo_d = [0.0f32; 8];
    let mut lo_n = [0.0f32; 8];
    let mut hi_d = [0.0f32; 8];
    let mut hi_n = [0.0f32; 8];
    lo_d.copy_from_slice(&den[..8]);
    lo_n.copy_from_slice(&num[..8]);
    hi_d.copy_from_slice(&den[8..]);
    hi_n.copy_from_slice(&num[8..]);
    let lo = lanes_b8(&lo_d, &lo_n);
    let hi = lanes_b8(&hi_d, &hi_n);
    let mut out = [0.0f32; 16];
    out[..8].copy_from_slice(&lo);
    out[8..].copy_from_slice(&hi);
    out
}

/// Aplica o fixup de `den == 0` sobre `q` (`000637AD`–`000639F8`,
/// `00063B49`–`00063FBC`, `00064109`–`0006432F`, `00064439`–`00064674`).
///
/// `neg_zero_as_positive` reproduz o quirk do scratch: no laço de 16 ele é
/// zerado (`00063B5E`/`00063B64`), então `−0.0` vira `+0.0`; nos outros blocos
/// o scratch ainda contém o `den`, então `−0.0` permanece `−0.0`.
fn apply_fixup(den: &[f32], num: &[f32], q: &mut [f32], neg_zero_as_positive: bool) {
    for i in 0..q.len() {
        if den[i] == 0.0 {
            q[i] = if den[i].to_bits() == 0 {
                fixup(num[i])
            } else if neg_zero_as_positive {
                0.0
            } else {
                den[i]
            };
        }
    }
}

/// `dst[i] = num[i] / den[i]` — `0x63640` com o alinhamento lido do ponteiro
/// (`r8 & 0x1c` em `0006366A`).
pub fn div_block(num: &[f32], den: &[f32], dst: &mut [f32]) {
    let mod32 = dst.as_ptr() as usize & 0x1c;
    div_block_mod32(num, den, dst, mod32);
}

/// `0x63640` com `dst_mod32 = dst & 0x1c` explícito.
///
/// No estágio o destino é a arena de 64 B (`dst_mod32 = 0`), então a cabeça
/// não roda — passe `0` mesmo que o `Vec` do port não esteja alinhado; o valor
/// que importa é o do binário, provado em `checks/r_divisao_63640.md` §5.
pub fn div_block_mod32(num: &[f32], den: &[f32], dst: &mut [f32], dst_mod32: usize) {
    assert_eq!(num.len(), dst.len(), "0x63640: num e dst com n diferente");
    assert_eq!(den.len(), dst.len(), "0x63640: den e dst com n diferente");
    assert!(
        std::is_x86_feature_detected!("avx"),
        "0x63640 usa vrcpps ymm (AVX)"
    );

    let n = dst.len();
    let mut off = 0usize;

    // --- Cabeça (00063697..00063A5D) -------------------------------------
    let mod32 = dst_mod32 & 0x1c;
    if mod32 != 0 {
        let mut h = 8 - (mod32 >> 2); // 0006369F..000636A4
        if h >= n {
            h = n; // 000636A7/000636B6 cmovge
        }
        if h > 0 {
            // Scratch de 16 floats com padding 1.0 (000636AA/000636B0).
            let mut sd = [1.0f32; 8];
            let mut sn = [1.0f32; 8];
            sd[..h].copy_from_slice(&den[..h]);
            sn[..h].copy_from_slice(&num[..h]);
            let mut q = lanes_a(&sd, &sn);
            apply_fixup(&sd, &sn, &mut q, false);
            dst[..h].copy_from_slice(&q[..h]);
        }
        off = h; // 00063A51 sub r9d,edi
    }

    // --- Laço de 16, aritmética B (00063A61..00063FE9) -------------------
    let n16 = (n - off) >> 4;
    for _ in 0..n16 {
        let mut d = [0.0f32; 16];
        let mut m = [0.0f32; 16];
        d.copy_from_slice(&den[off..off + 16]);
        m.copy_from_slice(&num[off..off + 16]);
        let mut q = lanes_b16(&d, &m);
        apply_fixup(&d, &m, &mut q, true);
        dst[off..off + 16].copy_from_slice(&q);
        off += 16;
    }

    let rem = n - off; // == (n - h) & 15

    // --- Bloco de 8, aritmética A (0006400D..0006468D) -------------------
    if rem & 8 != 0 {
        let mut d = [0.0f32; 8];
        let mut m = [0.0f32; 8];
        d.copy_from_slice(&den[off..off + 8]);
        m.copy_from_slice(&num[off..off + 8]);
        let mut q = lanes_a(&d, &m);
        apply_fixup(&d, &m, &mut q, false);
        dst[off..off + 8].copy_from_slice(&q);
        off += 8;
    }

    // --- Resto 1..7, aritmética A (0006401A..0006438F) -------------------
    let n7 = (n - off) & 7;
    if n7 != 0 {
        let mut sd = [1.0f32; 8];
        let mut sn = [1.0f32; 8];
        sd[..n7].copy_from_slice(&den[off..off + n7]);
        sn[..n7].copy_from_slice(&num[off..off + n7]);
        let mut q = lanes_a(&sd, &sn);
        apply_fixup(&sd, &sn, &mut q, false);
        dst[off..off + n7].copy_from_slice(&q[..n7]);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// `rcp` de um valor: `vrcpps` é lane a lane, então replicar não muda a lane 0.
    fn rcp1(x: f32) -> f32 {
        rcp8(&[x; 8])[0]
    }

    /// A de um lane (`00063787`–`00063796`).
    fn a1(den: f32, num: f32) -> f32 {
        lanes_a(&[den; 8], &[num; 8])[0]
    }

    /// B de um lane (`00063B20`–`00063B42`).
    fn b1(den: f32, num: f32) -> f32 {
        lanes_b8(&[den; 8], &[num; 8])[0]
    }

    /// Buffer com `dst.as_ptr() & 0x1c == off_bytes` (`off_bytes` múltiplo de 4,
    /// `< 32`). Devolve o `Vec` dono e o índice de início.
    fn buf_with_mod32(n: usize, off_bytes: usize) -> (Vec<f32>, usize) {
        let v = vec![0.0f32; n + 32];
        let base = v.as_ptr() as usize;
        let pad = (32 - base % 32) % 32;
        let start = (pad + off_bytes) / 4;
        (v, start)
    }

    #[test]
    fn mod32_from_pointer_matches_the_parameter() {
        for off in [0usize, 4, 8, 12, 16, 20, 24, 28] {
            let (v, start) = buf_with_mod32(64, off);
            assert_eq!(v[start..].as_ptr() as usize & 0x1c, off, "off {off}");
        }
    }

    #[test]
    fn aligned_dst_never_runs_the_head() {
        // dst & 0x1c == 0 → 00063699 pula para 00063A61: tudo é B no laço de 16.
        let n = 16;
        let (mut v, start) = buf_with_mod32(n, 0);
        let num: Vec<f32> = (0..n).map(|i| 1.0 + i as f32 * 0.37).collect();
        let den: Vec<f32> = (0..n).map(|i| 0.11 + i as f32 * 0.73).collect();
        div_block(&num, &den, &mut v[start..start + n]);
        for i in 0..n {
            assert_eq!(
                v[start + i],
                b1(den[i], num[i]),
                "lane {i} deveria ser B (laço de 16)"
            );
        }
    }

    #[test]
    fn head_uses_a_for_the_partial_lane_count() {
        // dst & 0x1c == 16 → h = 8 - 4 = 4 (0006369F..000636B6).
        let n = 16;
        let (mut v, start) = buf_with_mod32(n, 16);
        let num: Vec<f32> = (0..n).map(|i| 1.0 + i as f32 * 0.37).collect();
        let den: Vec<f32> = (0..n).map(|i| 0.11 + i as f32 * 0.73).collect();
        div_block(&num, &den, &mut v[start..start + n]);
        for i in 0..4 {
            assert_eq!(v[start + i], a1(den[i], num[i]), "lane {i} é cabeça (A)");
        }
        for i in 4..16 {
            assert_eq!(
                v[start + i],
                b1(den[i], num[i]),
                "lane {i} é laço de 16 (B)"
            );
        }
    }

    #[test]
    fn head_h1_when_dst_is_28_mod_32() {
        let n = 20;
        let (mut v, start) = buf_with_mod32(n, 28);
        let num: Vec<f32> = (0..n).map(|i| 2.0 + i as f32).collect();
        let den: Vec<f32> = (0..n).map(|i| 1.0 + i as f32 * 0.5).collect();
        div_block(&num, &den, &mut v[start..start + n]);
        assert_eq!(v[start], a1(den[0], num[0]));
        // 1 cabeça + 16 laço + 3 resto.
        for i in 1..17 {
            assert_eq!(v[start + i], b1(den[i], num[i]), "lane {i} é B");
        }
        for i in 17..20 {
            assert_eq!(v[start + i], a1(den[i], num[i]), "lane {i} é resto (A)");
        }
    }

    #[test]
    fn tail_after_16_loop_is_8_plus_remainder() {
        // n = 16 + 8 + 3: laço B, bloco 8 A, resto 3 A (0006400D/0006401A).
        let n = 27;
        let (mut v, start) = buf_with_mod32(n, 0);
        let num: Vec<f32> = (0..n).map(|i| 3.0 + i as f32 * 0.21).collect();
        let den: Vec<f32> = (0..n).map(|i| 0.7 + i as f32 * 0.13).collect();
        div_block(&num, &den, &mut v[start..start + n]);
        for i in 0..16 {
            assert_eq!(v[start + i], b1(den[i], num[i]), "lane {i} é B");
        }
        for i in 16..24 {
            assert_eq!(v[start + i], a1(den[i], num[i]), "lane {i} é bloco 8 (A)");
        }
        for i in 24..27 {
            assert_eq!(v[start + i], a1(den[i], num[i]), "lane {i} é resto (A)");
        }
    }

    #[test]
    fn n_below_16_is_all_remainder_a() {
        for n in 1..16usize {
            let (mut v, start) = buf_with_mod32(n, 0);
            let num: Vec<f32> = (0..n).map(|i| 1.0 + i as f32).collect();
            let den: Vec<f32> = (0..n).map(|i| 0.3 + i as f32).collect();
            div_block(&num, &den, &mut v[start..start + n]);
            for i in 0..n {
                assert_eq!(v[start + i], a1(den[i], num[i]), "n {n} lane {i}");
            }
        }
    }

    #[test]
    fn zero_denominator_uses_fixup() {
        // den = +0.0 → fixup(num) (000637C1..000637EC).
        assert_eq!(fixup(1.0), f32::INFINITY);
        assert_eq!(fixup(-1.0), f32::NEG_INFINITY);
        assert_eq!(fixup(f32::INFINITY), f32::INFINITY);
        assert_eq!(fixup(f32::NEG_INFINITY), f32::NEG_INFINITY);
        assert_eq!(fixup(0.0).to_bits(), FIXUP_NAN);
        assert_eq!(fixup(-0.0).to_bits(), FIXUP_NAN);
        assert_eq!(fixup(f32::NAN).to_bits(), FIXUP_NAN);

        for n in [1usize, 8, 16, 17] {
            let (mut v, start) = buf_with_mod32(n, 0);
            let num: Vec<f32> = (0..n).map(|i| if i % 2 == 0 { 2.0 } else { -3.0 }).collect();
            let den = vec![0.0f32; n];
            div_block(&num, &den, &mut v[start..start + n]);
            for i in 0..n {
                assert_eq!(v[start + i], fixup(num[i]), "n {n} lane {i}");
            }
        }
    }

    #[test]
    fn negative_zero_is_the_transcribed_scratch_quirk() {
        // Resto/cabeça/bloco 8: o scratch guarda o den, então −0.0 fica −0.0.
        let (mut v, start) = buf_with_mod32(1, 0);
        div_block(&[5.0], &[-0.0], &mut v[start..start + 1]);
        assert_eq!(v[start].to_bits(), (-0.0f32).to_bits());

        // Laço de 16: o scratch é zerado (00063B5E/00063B64) → +0.0.
        let (mut v, start) = buf_with_mod32(16, 0);
        div_block(&[5.0; 16], &[-0.0; 16], &mut v[start..start + 16]);
        for i in 0..16 {
            assert_eq!(v[start + i].to_bits(), 0, "lane {i}");
        }
    }

    #[test]
    fn a_and_b_differ_in_the_ulp() {
        // As duas aritméticas não são a mesma conta; o despacho escolhe qual
        // roda. Se fossem iguais, a cabeça não precisaria existir.
        let dens = [3.0f32, 7.0, 1e-7, 1e7, 0.1, 1234.5678];
        let nums = [1.0f32, 3.0, 7.0, 0.1, 1e-7, 1e7, 12345.678];
        let mut found = None;
        for &d in &dens {
            for &m in &nums {
                if a1(d, m).to_bits() != b1(d, m).to_bits() {
                    found = Some((d, m, a1(d, m), b1(d, m)));
                    break;
                }
            }
            if found.is_some() {
                break;
            }
        }
        let (d, m, qa, qb) = found.expect("A e B deveriam divergir em algum par");
        assert_eq!(qa.to_bits() != qb.to_bits(), true, "d={d} m={m} a={qa} b={qb}");
    }

    #[test]
    fn quotient_is_within_a_few_ulp_of_exact_division() {
        let dens = [3.0f32, 7.0, 1e-7, 1e7, 0.1, 1234.5678, 0.5, 2.0];
        let nums = [1.0f32, 3.0, 7.0, 0.1, 1e-7, 1e7, 12345.678];
        for &d in &dens {
            for &m in &nums {
                let exact = m / d;
                let got = a1(d, m);
                let tol = exact.abs() * 4.0 * f32::EPSILON;
                assert!(
                    (got - exact).abs() <= tol,
                    "d={d} m={m} got={got} exact={exact}"
                );
            }
        }
    }

    #[test]
    fn rcp_is_never_nan_for_positive_denominator() {
        // O caminho do estágio: den >= 1e-7 > 0, então nz é sempre verdadeiro.
        for x in [1e-7f32, 1.0, 3.0, 1e7, f32::MAX, f32::MIN_POSITIVE] {
            let r = rcp1(x);
            assert!(!r.is_nan() && r != 0.0, "rcp({x}) = {r}");
        }
    }

    #[test]
    fn empty_slice_is_a_noop() {
        let mut v: [f32; 0] = [];
        div_block(&[], &[], &mut v);
    }
}
