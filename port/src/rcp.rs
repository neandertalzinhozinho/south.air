//! Etapa M2 — recíproco `0x1C8530` → `0x29B260` transcrito bit a bit.
//!
//! Fonte: `checks/29b260.dis` (`0x29B260`–`0x29B9A0`, 1.856 B pelo `.pdata`),
//! `checks/29b9a0.dis` (lane especial) e `checks/s_reciproco_88e130.md`. Cada
//! passo cita o RVA. Nada aqui é estimado.
//!
//! ## Despacho (CPU path)
//!
//! `0x1C8530 movsxd rax,[0x21C7408]` (= `4` no dump) → `jmp [0x21C6AE8 + 8·4]`
//! = `[0x21C6B08]` = `0x19B78AC0` → `0x1C8AC0` (`endbr64; mov rax,[0x21C71D8];
//! jmp rax`) → `[0x21C71D8]` = `0x19C4B260` → **`0x29B260`** (base `0x199B0000`).
//! Os outros índices da tabela: `0..2` → `0x297EE0`, `3` → `0x299C60` (não lidos;
//! o dump fixou o índice `4`).
//!
//! ## Assinatura provada
//!
//! `rcx = src` (`0029B2A4 mov r14,rcx`), `rdx = dst` (`0029B298 mov r12,rdx`),
//! `r8d = n` (`0029B275 mov ebp,r8d`) → `dst[i] = 1/src[i]` aproximado. Em
//! `0x88E130` é in-place: `0088E31D movq rcx,xmm1` / `0088E327 mov rdx,rcx` /
//! `0088E32A movd r8d,xmm0` / `0088E32F call 0x1c8530`.
//!
//! ## Aritmética por lane (não depende de `n` nem de alinhamento)
//!
//! Lane **normal** (`0029B40E`..`0029B465`; cauda `0029B542`..`0029B558`):
//!
//! ```text
//! r0 = vrcpps(x)                       0029B40E / 0029B542
//! e  = 1 − x·r0     (FMA)              0029B442 vfnmadd231ps ymm8,ymm4,ymm12
//! r  = e·r0 + r0    (FMA)              0029B456 vfmadd213ps  ymm8,ymm12,ymm12
//! ```
//!
//! Lane **especial** — `t = (bits − 0x00800000) & 0x7FFFFFFF`, `t >s 0x7DFFE800`
//! (`0029B3DE vpsubd`, `0029B3EE vpand`, `0029B3FE vpcmpgtd`; constantes
//! `0x1ED0500`, `0x1ED04C0`, `0x1ED0540`), isto é `|x|` fora de
//! `[0x00800000, 0x7E7FE800]`: zero, denormal, `|x| > 0x7E7FE800`, ±inf, NaN.
//! A lane é refeita por `0x29B9A0` (`0029B756`/`0029B899`):
//! `r = 1.0f / x` (`0029B9B5 vdivss`, `1.0` de `0x1ED0620`) e
//! `status = (x == 0) ? 0x12 : 0` (`0029B9B0 vcmpeqss`, `0029B9C1 and eax,0x12`).
//! Com `status != 0` o binário grava `dst[i]`, chama `0x2D74A0` e relê `dst[i]`
//! (`0029B763`..`0029B7A4`); `0x2D74A0` é `endbr64; ret` (`002D74A0`/`002D74A4`),
//! então o valor fica `1/x = ±inf`.
//!
//! ## Despacho por `n`
//!
//! 1. Blocos de 32 (`ebx = n & ~31`, `0029B28C`), 4 vetores de 8
//!    (`0029B3C3`..`0029B4A3`), `vmovups` (sem exigência de alinhamento).
//! 2. Cauda em pedaços de `min(n − i, 8)` (`0029B500`..`0029B586`): carga
//!    mascarada (`0029B536 vmaskmovps`, máscara de `0x1ED0240 + 32·cnt`),
//!    padding `0.75` (`0029B53C vblendvps`, `0x1ED0600`), escrita mascarada
//!    (`0029B57E`, máscara de `0x1ED0380 + 32·cnt`).
//!
//! Não há cabeça de alinhamento: toda carga/escrita é `vmovups`/`vmaskmovps`.
//! Como a conta é por lane e o padding é descartado, o valor de cada lane não
//! depende de `n` nem do alinhamento — o despacho só decide **quais** lanes
//! passam por `0x29B9A0` (as especiais, em qualquer bloco).
//!
//! ## MXCSR
//!
//! `0029B355`..`0029B38D`: se `(mxcsr & 0xFFC0) != 0x1F80`, carrega
//! `(mxcsr & 0xFFFF003F) + 0x1F80` (arredondamento ao mais próximo, exceções
//! mascaradas, **FTZ = DAZ = 0**). Saída (`0029B59A`..`0029B5D0`): se trocou,
//! restaura o valor salvo; senão zera os flags `0..4` do valor corrente. O port
//! faz o mesmo ([`mxcsr_enter`]/[`mxcsr_leave`]), então FTZ/DAZ do host não
//! mudam o resultado. O x87 (`0029B328`..`0029B34B`, `0029B58C`..`0029B593`)
//! não é transcrito: nenhuma instrução x87 faz conta no corpo.
//!
//! ## Retorno
//!
//! `eax = r15d`: `0`, ou `0x12` se alguma lane foi `±0` (`0029B7A1`/`0029B8E0`);
//! `n <= 0` → `0xFFFFFFFA` (`0029B310`/`0029B971`); ponteiro nulo →
//! `0xFFFFFFF8` (`0029B319`/`0029B322`/`0029B90B`). `0x88E130` não lê `eax`
//! (`0088E334`..`0088E352`).
//!
//! ## `vrcpps`
//!
//! `_mm256_rcp_ps` é a mesma instrução do hardware em que o port roda. A tabela
//! de `vrcpps` não é fixada pela ISA (Intel ≠ AMD): bit a bit vale **na mesma
//! CPU** do oráculo (mesma ressalva de `crate::div`). Conferido contra a
//! sequência AVX/FMA do binário em `checks/j_rcp_avx.rs`.

#![allow(dead_code)]

/// `0x1ED0500` — subtraendo do teste de lane especial (`0029B3DE vpsubd`).
pub const SPECIAL_SUB: u32 = 0x0080_0000;
/// `0x1ED04C0` — máscara de valor absoluto (`0029B3EE vpand`).
pub const ABS_MASK: u32 = 0x7FFF_FFFF;
/// `0x1ED0540` — limite do `vpcmpgtd` com sinal (`0029B3FE`).
pub const SPECIAL_LIMIT: i32 = 0x7DFF_E800;
/// `0x1ED05C0` (vetor) e `0x1ED0620` (escalar de `0x29B9A0`): bits `0x3F800000`.
pub const ONE: f32 = f32::from_bits(0x3F80_0000);
/// `0x1ED0600` — padding das lanes fora da cauda (`0029B53C`): bits `0x3F400000`.
pub const PAD: f32 = f32::from_bits(0x3F40_0000);
/// `0029B9C1 and eax,0x12` — status de lane `±0`.
pub const STS_SING: i32 = 0x12;
/// `0029B971 mov eax,0xfffffffa` — `n <= 0`.
pub const STS_SIZE_ERR: i32 = 0xFFFF_FFFAu32 as i32;
/// `0029B90B mov eax,0xfffffff8` — ponteiro nulo.
pub const STS_NULL_PTR: i32 = 0xFFFF_FFF8u32 as i32;

/// Lane especial: `((bits − 0x00800000) & 0x7FFFFFFF) >s 0x7DFFE800`
/// (`0029B3DE`/`0029B3EE`/`0029B3FE`).
#[inline]
pub fn is_special(x: f32) -> bool {
    let t = x.to_bits().wrapping_sub(SPECIAL_SUB) & ABS_MASK;
    (t as i32) > SPECIAL_LIMIT
}

/// `vrcpps` em 8 lanes (`0029B40E`..`0029B41A`, `0029B542`).
#[cfg(target_arch = "x86_64")]
#[inline]
fn rcp8(x: &[f32; 8]) -> [f32; 8] {
    // SAFETY: os pontos de entrada checam `is_x86_feature_detected!("avx")`.
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
    panic!("0x29B260 usa vrcpps ymm: só existe em x86-64 com AVX");
}

/// 8 lanes normais + máscara de especiais (bit `i` = lane `i`, `vmovmskps`
/// em `0029B41E`/`0029B560`).
fn lanes8(x: &[f32; 8]) -> ([f32; 8], u32) {
    let r0 = rcp8(x);
    let mut out = [0.0f32; 8];
    let mut mask = 0u32;
    for i in 0..8 {
        if is_special(x[i]) {
            mask |= 1 << i;
        }
        let e = (-x[i]).mul_add(r0[i], ONE); // 0029B442 vfnmadd231ps
        out[i] = e.mul_add(r0[i], r0[i]); // 0029B456 vfmadd213ps
    }
    (out, mask)
}

/// `0x29B9A0(&x, &r)`: `r = 1.0f / x` (`0029B9B5 vdivss`),
/// `eax = (x == 0) ? 0x12 : 0` (`0029B9B0`/`0029B9C1`).
#[inline]
pub fn special_lane(x: f32) -> (f32, i32) {
    let r = ONE / x;
    let st = if x == 0.0 { STS_SING } else { 0 };
    (r, st)
}

#[cfg(target_arch = "x86_64")]
fn stmxcsr() -> u32 {
    let mut v: u32 = 0;
    // SAFETY: `stmxcsr` só grava 4 bytes no endereço dado.
    unsafe {
        core::arch::asm!("stmxcsr [{p}]", p = in(reg) &mut v as *mut u32, options(nostack, preserves_flags));
    }
    v
}

#[cfg(target_arch = "x86_64")]
fn ldmxcsr(v: u32) {
    // SAFETY: valor com bits reservados (31..16) zerados, vindos do próprio MXCSR.
    // Sem `nomem`/`readonly`: o compilador não move cargas/escritas através dele.
    unsafe {
        core::arch::asm!("ldmxcsr [{p}]", p = in(reg) &v as *const u32, options(nostack, preserves_flags));
    }
}

/// `0029B355`..`0029B38D`. Devolve `(mxcsr salvo, trocou?)`.
#[cfg(target_arch = "x86_64")]
pub fn mxcsr_enter() -> (u32, bool) {
    let ecx = stmxcsr(); // 0029B355/0029B35E
    if ecx & 0xFFC0 == 0x1F80 {
        // 0029B367/0029B36D/0029B373
        (ecx, false)
    } else {
        ldmxcsr((ecx & 0xFFFF_003F).wrapping_add(0x1F80)); // 0029B37A/0029B380/0029B38D
        (ecx, true)
    }
}

/// `0029B59A`..`0029B5D0`.
#[cfg(target_arch = "x86_64")]
pub fn mxcsr_leave(saved: u32, changed: bool) {
    if changed {
        ldmxcsr(saved); // 0029B59F/0029B5A6
    } else {
        let edx = stmxcsr(); // 0029B5B1/0029B5BA
        if edx & 0x1F != 0 {
            ldmxcsr(edx & 0xFFFF_FFE0); // 0029B5C6/0029B5D0
        }
    }
}

/// Núcleo sobre ponteiros (permite `src == dst`, como em `0088E32F`). Cada bloco
/// é lido inteiro antes de ser escrito, como no binário.
///
/// # Safety
/// `src` legível e `dst` gravável em `n` floats.
unsafe fn inv_raw(src: *const f32, dst: *mut f32, n: usize) -> i32 {
    let mut status = 0i32; // 0029B2B0 xor r15d,r15d
    let n32 = n & !31; // 0029B28C and ebx,0xffffffe0
    let mut i = 0usize;

    // --- Blocos de 32 (0029B3C0..0029B4A3) --------------------------------
    while i < n32 {
        let mut x = [0.0f32; 32];
        for k in 0..32 {
            x[k] = unsafe { *src.add(i + k) }; // 0029B3C3..0029B3D7
        }
        let mut r = [0.0f32; 32];
        let mut mask = 0u32;
        for q in 0..4 {
            let mut v = [0.0f32; 8];
            v.copy_from_slice(&x[8 * q..8 * q + 8]);
            let (o, m) = lanes8(&v);
            r[8 * q..8 * q + 8].copy_from_slice(&o);
            mask |= m << (8 * q); // 0029B46A..0029B47A
        }
        if mask != 0 {
            // 0029B7AC..0029B881: lanes 0..31 em ordem (0029B820 bt esi,edi)
            for k in 0..32 {
                if mask & (1 << k) != 0 {
                    let (v, st) = special_lane(x[k]); // 0029B899
                    r[k] = v;
                    if st != 0 {
                        status = st; // 0029B8E0 (0x2D74A0 é ret)
                    }
                }
            }
        }
        for k in 0..32 {
            unsafe { *dst.add(i + k) = r[k] }; // 0029B486..0029B49C
        }
        i += 32; // 0029B483
    }

    // --- Cauda em pedaços de 8 mascarados (0029B500..0029B586) -------------
    while i < n {
        let cnt = if n - i >= 8 { 8 } else { n - i }; // 0029B502..0029B50A
        let mut x = [PAD; 8]; // 0029B53C vblendvps com 0.75
        for k in 0..cnt {
            x[k] = unsafe { *src.add(i + k) }; // 0029B536 vmaskmovps
        }
        let (mut r, mask) = lanes8(&x);
        if mask != 0 {
            // 0029B67B..0029B73B: lanes 0..7 (0029B6C0 bt esi,ebx)
            for k in 0..8 {
                if mask & (1 << k) != 0 {
                    let (v, st) = special_lane(x[k]); // 0029B756
                    r[k] = v;
                    if st != 0 {
                        status = st; // 0029B7A1
                    }
                }
            }
        }
        for k in 0..cnt {
            unsafe { *dst.add(i + k) = r[k] }; // 0029B57E vmaskmovps
        }
        i += 8; // 0029B577
    }
    status
}

fn entry(n: usize) -> Option<i32> {
    assert!(
        std::is_x86_feature_detected!("avx"),
        "0x29B260 usa vrcpps ymm (AVX)"
    );
    assert!(n <= i32::MAX as usize, "0x29B260: r8d é i32");
    if n == 0 {
        Some(STS_SIZE_ERR) // 0029B30E/0029B310 jle → 0029B971
    } else {
        None
    }
}

/// `0x29B260(src, dst, n)`: `dst[i] ≈ 1/src[i]`. Devolve o `eax` do binário.
pub fn inv_32f(src: &[f32], dst: &mut [f32]) -> i32 {
    assert_eq!(src.len(), dst.len(), "0x29B260: src e dst com n diferente");
    if let Some(s) = entry(dst.len()) {
        return s;
    }
    let (saved, changed) = mxcsr_enter();
    // SAFETY: mesmos comprimentos, checados acima.
    let st = unsafe { inv_raw(src.as_ptr(), dst.as_mut_ptr(), dst.len()) };
    mxcsr_leave(saved, changed);
    st
}

/// `0x29B260(buf, buf, n)` — forma in-place usada em `0088E32F`.
pub fn inv_32f_in_place(buf: &mut [f32]) -> i32 {
    if let Some(s) = entry(buf.len()) {
        return s;
    }
    let (saved, changed) = mxcsr_enter();
    let p = buf.as_mut_ptr();
    // SAFETY: `src == dst` é o caso do binário; cada bloco é lido antes de escrito.
    let st = unsafe { inv_raw(p as *const f32, p, buf.len()) };
    mxcsr_leave(saved, changed);
    st
}

#[cfg(test)]
mod tests {
    use super::*;

    fn one(x: f32) -> f32 {
        let mut b = [x];
        inv_32f_in_place(&mut b);
        b[0]
    }

    #[test]
    fn special_test_bounds_are_the_dump_constants() {
        // [0x00800000, 0x7E7FE800] é normal, fora é especial (com e sem sinal).
        for s in [0u32, 0x8000_0000] {
            assert!(!is_special(f32::from_bits(s | 0x0080_0000)));
            assert!(!is_special(f32::from_bits(s | 0x7E7F_E800)));
            assert!(is_special(f32::from_bits(s | 0x7E7F_E801)));
            assert!(is_special(f32::from_bits(s | 0x007F_FFFF)));
            assert!(is_special(f32::from_bits(s)));
            assert!(is_special(f32::from_bits(s | 0x7F80_0000)));
            assert!(is_special(f32::from_bits(s | 0x7FC0_0000)));
        }
        assert!(!is_special(PAD), "padding 0.75 não pode ser especial");
    }

    #[test]
    fn normal_lane_is_rcp_plus_one_fma_step_not_ieee() {
        let xs = [1.0f32, 1.5, 3.0, 7.0, 1.0000001, 2.7182817, 12345.678, 1e30];
        let mut found_diff = false;
        for &x in &xs {
            let r0 = rcp8(&[x; 8])[0];
            let e = (-x).mul_add(r0, 1.0);
            let want = e.mul_add(r0, r0);
            assert_eq!(one(x).to_bits(), want.to_bits(), "x={x}");
            if one(x).to_bits() != (1.0f32 / x).to_bits() {
                found_diff = true;
            }
        }
        // A sequência não é a divisão IEEE em todo x (se fosse, o gap não existiria).
        let mut any = found_diff;
        for k in 0..4096u32 {
            let x = 1.0f32 + k as f32 / 4096.0;
            if one(x).to_bits() != (1.0f32 / x).to_bits() {
                any = true;
                break;
            }
        }
        assert!(any, "vrcpps+FMA deveria divergir de 1.0/x em algum x de [1,2)");
    }

    #[test]
    fn special_lanes_are_ieee_division() {
        assert_eq!(one(0.0), f32::INFINITY);
        assert_eq!(one(-0.0), f32::NEG_INFINITY);
        assert_eq!(one(f32::INFINITY).to_bits(), 0);
        assert_eq!(one(f32::NEG_INFINITY).to_bits(), 0x8000_0000);
        assert!(one(f32::NAN).is_nan());
        for bits in [0x0000_0001u32, 0x007F_FFFF, 0x7E7F_E801, 0x7F00_0000, 0x7F7F_FFFF] {
            let x = f32::from_bits(bits);
            assert_eq!(one(x).to_bits(), (1.0f32 / x).to_bits(), "{bits:08x}");
        }
    }

    #[test]
    fn status_is_0x12_only_for_zero_and_size_error_for_empty() {
        let mut v = [1.0f32, 2.0, 3.0];
        assert_eq!(inv_32f_in_place(&mut v), 0);
        let mut v = [1.0f32, 0.0, 3.0];
        assert_eq!(inv_32f_in_place(&mut v), STS_SING);
        let mut v = [f32::INFINITY; 40];
        assert_eq!(inv_32f_in_place(&mut v), 0);
        let mut v = [-0.0f32; 40];
        assert_eq!(inv_32f_in_place(&mut v), STS_SING);
        let mut e: [f32; 0] = [];
        assert_eq!(inv_32f_in_place(&mut e), STS_SIZE_ERR);
    }

    #[test]
    fn value_does_not_depend_on_n_or_block_position() {
        // Blocos de 32 e cauda de 8 com padding: a mesma lane dá os mesmos bits
        // em qualquer n e em qualquer posição.
        let base: Vec<f32> = (0..300).map(|i| 1.0 + i as f32 * 0.731).collect();
        let mut reference = base.clone();
        inv_32f_in_place(&mut reference);
        for n in 1..=80usize {
            for start in [0usize, 1, 3, 7, 31, 33, 100] {
                let src = &base[start..start + n];
                let mut dst = vec![0.0f32; n];
                inv_32f(src, &mut dst);
                for k in 0..n {
                    assert_eq!(dst[k].to_bits(), reference[start + k].to_bits(), "n={n} start={start} k={k}");
                }
            }
        }
    }

    #[test]
    fn in_place_equals_out_of_place() {
        let src: Vec<f32> = (0..77).map(|i| 0.5 + i as f32 * 1.37).collect();
        let mut a = vec![0.0f32; 77];
        inv_32f(&src, &mut a);
        let mut b = src.clone();
        inv_32f_in_place(&mut b);
        for k in 0..77 {
            assert_eq!(a[k].to_bits(), b[k].to_bits());
        }
    }

    #[test]
    fn mxcsr_is_restored() {
        let before = stmxcsr() & 0xFFC0;
        let mut v = [3.0f32; 9];
        inv_32f_in_place(&mut v);
        assert_eq!(stmxcsr() & 0xFFC0, before);
    }
}
