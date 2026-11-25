//! Etapa J4 — transcrição LITERAL dos kernels complexos da FFT do soothe3:
//! `0x8BFE0` (ordem 6), `0x8C280` (ordem 7), `0x1D69E00` (ordens 8..19,
//! genérico, incluindo `rdx > 0x800`) e do split CCS (`0x895C0`, rápido e lento).
//!
//! Nada aqui é "algoritmo equivalente": cada `V8` é um ymm e cada função é a
//! instrução AVX correspondente, na mesma ordem. `shuf`/`perm` reproduzem
//! `vshufps`/`vperm2f128`; `fma132`/`fma213`/`fnmadd231` usam `f32::mul_add`
//! (uma única arredondamento, como a FMA de hardware).
//!
//! ## Por que a ordem importa
//!
//! `vaddps`/`vsubps`/`vmulps`/`vfmadd` são exatamente as operações IEEE-754
//! de 32 bits com um arredondamento cada; o plugin foi medido nesta máquina e
//! a transcrição reproduz os bits (`j4_kernel6_bits` / `j4_chain_bits`).
//!
//! ## Cadeia em `0x72480` para ordem 6
//!
//! ```text
//! 0007258C call [0x1DFA358 + 6*8] = 0x8BFE0   kernel(src, dst)
//! 000725F6..00072617                          pack: dst0 = im+re, dst1 = re-im
//! 00072620 call 0x895C0(dst, n/2, 1, ctx+0x50) split CCS
//! 0007262E..0007263C                          dst[n] = dst[1], dst[1] = 0
//! ```
//!
//! ## `NÃO EXTRAÍDO`
//!
//! * o kernel `0x88300` (ordem > 0x13): inalcançável para o áudio do plugin
//!   (`N = round(256·fs/44100)` ≤ 1115 → ordem 11; `0007259B` só o chama com
//!   `r15d > 0x13`) e todo o corpo chama internos de IPP sem identidade lida;
//! * a geração das twiddles de `ctx+0x38`/`ctx+0x50` (`0x806E0`/`0x876E0`/`0x87AA0`)
//!   — as tabelas são medidas e fixadas nos goldens, mas não transcritas.
//!
//! As ordens 13..19 (`kernel_large`, `rdx > 0x800`) e o caminho lento de
//! `0x895C0` (`0000897A0`, `len >= 0x40000`) **estão transcritos** abaixo.
//!
//! Teste: `rustc --edition 2021 --test checks\j4_fft.rs -o checks\.build\j4_tests.exe`

#![allow(dead_code)]
#![allow(unused_assignments)]


type V8 = [f32; 8];

// ---------------------------------------------------------------------------
// Bits medidos (tabelas de constantes do kernel)
// ---------------------------------------------------------------------------

/// `0x1DFD120` (`vbroadcastf128`): `[0,-0,0,-0]` nos dois lanes.
/// `vmovsd`/`vbroadcastf128` em `0008C00F`, `0008C20C`, `000895D2`.
const MASK: V8 = [
    f32::from_bits(0x0000_0000),
    f32::from_bits(0x8000_0000),
    f32::from_bits(0x0000_0000),
    f32::from_bits(0x8000_0000),
    f32::from_bits(0x0000_0000),
    f32::from_bits(0x8000_0000),
    f32::from_bits(0x0000_0000),
    f32::from_bits(0x8000_0000),
];

/// `0x1DFD130` (`vbroadcastf128`, `0008C1AD`): `0.707106769` em oito lanes.
const CM: V8 = [f32::from_bits(0x3f35_04f3); 8];

macro_rules! v8 {
    ($($b:expr),* $(,)?) => {
        [$(f32::from_bits($b)),*]
    };
}

/// `0x1DFCFA0` (memória de `vmulps` em `0008C09C`).
const CA: V8 = v8!(
    0x0000_0000, 0x0000_0000, 0x3e47_c5c2, 0xbe47_c5c2, 0x3ec3_ef15, 0xbec3_ef15, 0x3f0e_39da,
    0xbf0e_39da,
);
/// `0x1DFCFC0`.
const CB: V8 = v8!(
    0x3f80_0000, 0x3f80_0000, 0x3f7b_14be, 0x3f7b_14be, 0x3f6c_835e, 0x3f6c_835e, 0x3f54_db31,
    0x3f54_db31,
);
/// `0x1DFCFE0`.
const CC: V8 = v8!(
    0x0000_0000, 0x0000_0000, 0x3ec3_ef15, 0xbec3_ef15, 0x3f35_04f3, 0xbf35_04f3, 0x3f6c_835e,
    0xbf6c_835e,
);
/// `0x1DFD000`.
const CD: V8 = v8!(
    0x3f80_0000, 0x3f80_0000, 0x3f6c_835e, 0x3f6c_835e, 0x3f35_04f3, 0x3f35_04f3, 0x3ec3_ef15,
    0x3ec3_ef15,
);
/// `0x1DFD020`.
const CE: V8 = v8!(
    0x0000_0000, 0x0000_0000, 0x3f0e_39da, 0xbf0e_39da, 0x3f6c_835e, 0xbf6c_835e, 0x3f7b_14be,
    0xbf7b_14be,
);
/// `0x1DFD040`.
const CF: V8 = v8!(
    0x3f80_0000, 0x3f80_0000, 0x3f54_db31, 0x3f54_db31, 0x3ec3_ef15, 0x3ec3_ef15, 0xbe47_c5c2,
    0xbe47_c5c2,
);
/// `0x1DFD060`.
const CG: V8 = v8!(
    0x3f35_04f3, 0xbf35_04f3, 0x3f54_db31, 0xbf54_db31, 0x3f6c_835e, 0xbf6c_835e, 0x3f7b_14be,
    0xbf7b_14be,
);
/// `0x1DFD080`.
const CH: V8 = v8!(
    0x3f35_04f3, 0x3f35_04f3, 0x3f0e_39da, 0x3f0e_39da, 0x3ec3_ef15, 0x3ec3_ef15, 0x3e47_c5c2,
    0x3e47_c5c2,
);
/// `0x1DFD0A0`.
const CI: V8 = v8!(
    0x3f80_0000, 0xbf80_0000, 0x3f6c_835e, 0xbf6c_835e, 0x3f35_04f3, 0xbf35_04f3, 0x3ec3_ef15,
    0xbec3_ef15,
);
/// `0x1DFD0C0`.
const CJ: V8 = v8!(
    0x0000_0000, 0x0000_0000, 0xbec3_ef15, 0xbec3_ef15, 0xbf35_04f3, 0xbf35_04f3, 0xbf6c_835e,
    0xbf6c_835e,
);
/// `0x1DFD0E0`.
const CK: V8 = v8!(
    0x3f35_04f3, 0xbf35_04f3, 0x3e47_c5c2, 0xbe47_c5c2, 0xbec3_ef15, 0x3ec3_ef15, 0xbf54_db31,
    0x3f54_db31,
);
/// `0x1DFD100`.
const CL: V8 = v8!(
    0xbf35_04f3, 0xbf35_04f3, 0xbf7b_14be, 0xbf7b_14be, 0xbf6c_835e, 0xbf6c_835e, 0xbf0e_39da,
    0xbf0e_39da,
);

// ---------------------------------------------------------------------------
// Instruções
// ---------------------------------------------------------------------------

#[inline(always)]
fn add(a: &V8, b: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = a[i] + b[i];
    }
    r
}

#[inline(always)]
fn sub(a: &V8, b: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = a[i] - b[i];
    }
    r
}

#[inline(always)]
fn mul(a: &V8, b: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = a[i] * b[i];
    }
    r
}

/// `vxorps` — XOR dos bits, não aritmética.
#[inline(always)]
fn xor(a: &V8, b: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = f32::from_bits(a[i].to_bits() ^ b[i].to_bits());
    }
    r
}

/// `vshufps ymm, ymm, ymm, imm` — por lane de 128 bits.
#[inline(always)]
fn shuf(a: &V8, b: &V8, imm: u32) -> V8 {
    let s = [
        (imm & 3) as usize,
        ((imm >> 2) & 3) as usize,
        ((imm >> 4) & 3) as usize,
        ((imm >> 6) & 3) as usize,
    ];
    let mut r = [0f32; 8];
    for lane in 0..2 {
        let base = lane * 4;
        r[base] = a[base + s[0]];
        r[base + 1] = a[base + s[1]];
        r[base + 2] = b[base + s[2]];
        r[base + 3] = b[base + s[3]];
    }
    r
}

/// `vperm2f128 ymm, ymm, ymm, imm`.
#[inline(always)]
fn perm(a: &V8, b: &V8, imm: u32) -> V8 {
    let pick = |sel: u32| -> [f32; 4] {
        match sel {
            0 => [a[0], a[1], a[2], a[3]],
            1 => [a[4], a[5], a[6], a[7]],
            2 => [b[0], b[1], b[2], b[3]],
            _ => [b[4], b[5], b[6], b[7]],
        }
    };
    let lo = pick(imm & 3);
    let hi = pick((imm >> 4) & 3);
    [lo[0], lo[1], lo[2], lo[3], hi[0], hi[1], hi[2], hi[3]]
}

/// `vfmadd132ps dst, src2, src3` → `dst = dst*src3 + src2`.
#[inline(always)]
fn fma132(dst: &V8, src2: &V8, src3: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = dst[i].mul_add(src3[i], src2[i]);
    }
    r
}

/// `vfmadd213ps dst, src2, src3` → `dst = src2*dst + src3`.
#[inline(always)]
fn fma213(dst: &V8, src2: &V8, src3: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = src2[i].mul_add(dst[i], src3[i]);
    }
    r
}

/// `vfnmadd231ps dst, src2, src3` → `dst = -(src2*src3) + dst`.
#[inline(always)]
fn fnmadd231(dst: &V8, src2: &V8, src3: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = (-src2[i]).mul_add(src3[i], dst[i]);
    }
    r
}

/// `vfmaddsub213ps dst, src1, src2` → `dst = src1*dst ∓ src2` (par subtrai, ímpar soma).
/// FMA verdadeiro (um único arredondamento).
#[inline(always)]
fn fmaaddsub213(dst: &V8, src1: &V8, src2: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = if i % 2 == 0 {
            src1[i].mul_add(dst[i], -src2[i])
        } else {
            src1[i].mul_add(dst[i], src2[i])
        };
    }
    r
}

/// `vfmaddsub231ps dst, src1, src2` → `dst = src1*src2 ∓ dst` (par subtrai, ímpar soma).
#[inline(always)]
fn fmaaddsub231(dst: &V8, src1: &V8, src2: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = if i % 2 == 0 {
            src1[i].mul_add(src2[i], -dst[i])
        } else {
            src1[i].mul_add(src2[i], dst[i])
        };
    }
    r
}

/// `vaddsubps a, b` → pares subtraem, ímpares somam.
#[inline(always)]
fn addsub(a: &V8, b: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = if i % 2 == 0 { a[i] - b[i] } else { a[i] + b[i] };
    }
    r
}

#[inline(always)]
fn load8(d: &[f32], i: usize) -> V8 {
    [d[i], d[i + 1], d[i + 2], d[i + 3], d[i + 4], d[i + 5], d[i + 6], d[i + 7]]
}

#[inline(always)]
fn store8(d: &mut [f32], i: usize, v: &V8) {
    d[i..i + 8].copy_from_slice(v);
}

#[inline(always)]
fn pair(d: &[f32], p: usize) -> (f32, f32) {
    (d[2 * p], d[2 * p + 1])
}

#[inline(always)]
fn store_pair(d: &mut [f32], p: usize, re: f32, im: f32) {
    d[2 * p] = re;
    d[2 * p + 1] = im;
}

#[inline(always)]
fn quad(d: &[f32], i: usize) -> [f32; 4] {
    [d[i], d[i + 1], d[i + 2], d[i + 3]]
}

// ---------------------------------------------------------------------------
// 0x8BFE0 — kernel complexo de 32 pontos (ordem 6), literal
// ---------------------------------------------------------------------------

/// Transcreve `0x8BFE0`..`0x8C27A`. `src` = 64 f32 (32 complexos intercalados),
/// `dst` = 64 f32. Todos os 8 ymm de saída são escritos.
///
/// RVAs das instruções-chave estão nos comentários.
pub fn kernel6(src: &[f32; 64], dst: &mut [f32; 64]) {
    let g = |j: usize| -> V8 { load8(src, j * 8) };
    let m = MASK;
    // 0008C006..0008C03C
    let mut y5 = g(0);
    let mut y1 = g(2);
    let mut y2 = m; // mask, reutilizado em 0008C1C0
    let mut y14 = add(&y5, &g(4));
    let mut y3 = add(&y1, &g(6));
    let mut y4 = sub(&y1, &g(6));
    let mut y15 = sub(&y5, &g(4));
    let mut y12 = add(&y14, &y3);
    y3 = sub(&y14, &y3);
    // 0008C040..0008C05A
    y14 = g(3);
    y5 = g(1);
    let mut y11 = add(&y14, &g(7));
    y1 = sub(&y5, &g(5));
    let mut y0 = shuf(&y4, &y4, 0xb1);
    y0 = xor(&y0, &y2);
    y4 = add(&y0, &y15);
    let mut y13 = sub(&y15, &y0);
    // 0008C06C..0008C093
    y0 = sub(&y14, &g(7));
    y15 = add(&y5, &g(5));
    y5 = xor(&shuf(&y0, &y0, 0xb1), &y2);
    y14 = add(&y15, &y11);
    y15 = sub(&y15, &y11);
    y0 = add(&y5, &y1);
    y1 = sub(&y1, &y5);
    // 0008C097..0008C0D1 (twiddles com vfmadd132ps)
    y11 = shuf(&y4, &y4, 0xb1);
    y5 = mul(&y11, &CA);
    y11 = shuf(&y3, &y3, 0xb1);
    y4 = fma132(&y4, &y5, &CB);
    y5 = mul(&y11, &CC);
    y11 = shuf(&y13, &y13, 0xb1);
    y3 = fma132(&y3, &y5, &CD);
    y5 = mul(&y11, &CE);
    y13 = fma132(&y13, &y5, &CF);
    // 0008C0DA..0008C102
    y5 = shuf(&y12, &y4, 0x44);
    y11 = shuf(&y12, &y4, 0xee);
    y4 = shuf(&y3, &y13, 0x44);
    y13 = shuf(&y3, &y13, 0xee);
    y3 = perm(&y5, &y4, 0x20);
    y5 = perm(&y5, &y4, 0x31);
    y4 = perm(&y11, &y13, 0x20);
    y11 = perm(&y11, &y13, 0x31);
    // 0008C108..0008C142
    y13 = shuf(&y0, &y0, 0xb1);
    y12 = mul(&y13, &CG);
    y13 = shuf(&y15, &y15, 0xb1);
    y0 = fma132(&y0, &y12, &CH);
    y12 = mul(&y13, &CI);
    y13 = shuf(&y1, &y1, 0xb1);
    y15 = fma132(&y15, &y12, &CJ);
    y12 = mul(&y13, &CK);
    y1 = fma132(&y1, &y12, &CL);
    // 0008C14B..0008C171
    y12 = shuf(&y14, &y0, 0x44);
    y13 = shuf(&y14, &y0, 0xee);
    y14 = shuf(&y15, &y1, 0x44);
    y0 = shuf(&y15, &y1, 0xee);
    y1 = perm(&y12, &y14, 0x20);
    y15 = perm(&y12, &y14, 0x31);
    y12 = perm(&y13, &y0, 0x20);
    y13 = perm(&y13, &y0, 0x31);
    // 0008C177..0008C197
    y0 = add(&y3, &y1);
    y14 = sub(&y3, &y1);
    y1 = add(&y5, &y15);
    y5 = sub(&y15, &y5);
    y15 = add(&y11, &y13);
    y13 = sub(&y13, &y11);
    y3 = add(&y4, &y12);
    y4 = sub(&y4, &y12);
    // 0008C19C..0008C1A9
    y12 = add(&y0, &y1);
    y0 = sub(&y0, &y1);
    y1 = add(&y3, &y15);
    y3 = sub(&y15, &y3);
    // 0008C1AD..0008C1CD
    y11 = CM;
    y13 = mul(&y11, &y13);
    y3 = shuf(&y3, &y3, 0xb1);
    y2 = xor(&y3, &y2);
    y3 = y4;
    y3 = fma132(&y3, &y13, &y11);
    y13 = fnmadd231(&y13, &y4, &y11);
    // 0008C1D2..0008C1F7
    y4 = add(&y12, &y1);
    y1 = sub(&y12, &y1);
    store8(dst, 0, &y4); // [rdx]
    store8(dst, 32, &y1); // [rdx+0x80]
    y1 = sub(&y0, &y2);
    y2 = add(&y2, &y0);
    y0 = add(&y14, &y3);
    store8(dst, 16, &y1); // [rdx+0x40]
    store8(dst, 48, &y2); // [rdx+0xc0]
    // 0008C1FF..0008C237
    y2 = sub(&y14, &y3);
    y3 = add(&y5, &y13);
    y5 = sub(&y13, &y5);
    y12 = MASK; // 0008C20C vbroadcastf128 [0x1DFD120]
    y4 = shuf(&y3, &y3, 0xb1);
    y11 = shuf(&y5, &y5, 0xb1);
    y13 = xor(&y4, &y12);
    y14 = xor(&y11, &y12);
    y15 = sub(&y0, &y13);
    y1 = add(&y13, &y0);
    y0 = sub(&y2, &y14);
    y2 = add(&y14, &y2);
    store8(dst, 8, &y15); // [rdx+0x20]
    store8(dst, 24, &y0); // [rdx+0x60]
    store8(dst, 40, &y2); // [rdx+0xa0]
    store8(dst, 56, &y1); // [rdx+0xe0]
}

// ---------------------------------------------------------------------------
// 0x895C0 — split CCS, caminho rápido (len < 0x40000)
// ---------------------------------------------------------------------------

/// Transcreve o laço `0x89600`..`0x89757` de `0x895C0` para `len < 0x40000`
/// (o caso do áudio: `len = n/2`; ordem 9 → 256).
///
/// `d` = `n+2` floats; `len = n/2`; `tw` = tabela de `ctx+0x50` (pares f32).
pub fn split_ccs(d: &mut [f32], len: usize, tw: &[f32]) {
    if len >= 0x40000 {
        // 000895E0 cmp r10d,0x40000 / 000895E7 jge 0x89768
        return split_ccs_slow(d, len, tw);
    }
    split_ccs_fast(d, len, tw)
}

/// Laço rápido (`00089600`..`00089757`), `len < 0x40000`.
pub fn split_ccs_fast(d: &mut [f32], len: usize, tw: &[f32]) {
    assert!(len > 0);
    assert!(d.len() >= 2 * len + 2);
    let m = MASK;
    let mut low = 1usize; // r8 = buf+8 bytes = par 1
    let mut high = len - 8; // rcx = buf + len*8 - 0x40
    let mut t = 0usize; // r9 avança 0x40 B (16 f32) por iteração
    let mut eax = 0i32;
    while eax < len as i32 {
        // ---- primeira metade ----
        let a2 = pair(d, low + 1); // 00089600 [r8+8]
        let a4 = pair(d, low + 3); // 0008960E [r8+0x18]
        let a1 = pair(d, low); // 00089614 [r8]
        let a3 = pair(d, low + 2); // 00089619 [r8+0x10]
        let h6 = quad(d, 2 * (high + 6)); // 00089609 [rcx+0x30]
        let xmm2 = [a2.0, a2.1, a1.0, a1.1];
        let xmm6 = [a4.0, a4.1, a3.0, a3.1];
        let h4 = quad(d, 2 * (high + 4)); // 00089623 [rcx+0x20]
        let mut y4 = [h6[0], h6[1], h6[2], h6[3], h4[0], h4[1], h4[2], h4[3]];
        let y3 = xor(&y4, &m); // 0008962F
        let y6 = [xmm2[0], xmm2[1], xmm2[2], xmm2[3], xmm6[0], xmm6[1], xmm6[2], xmm6[3]];
        let y5 = sub(&y6, &y3); // 0008963D
        let t0 = quad(tw, t); // 0008962A [r9]
        let t1 = quad(tw, t + 4); // 00089645 [r9+0x10]
        let y4t = [t0[0], t0[1], t0[2], t0[3], t1[0], t1[1], t1[2], t1[3]];
        let mut y2 = shuf(&y4t, &y4t, 0xa0); // 0008964C
        let mut y1 = shuf(&y4t, &y4t, 0xf5); // 00089651
        y2 = xor(&y2, &m); // 00089656
        y4 = xor(&y6, &m); // 0008965A
        let mut y6s = shuf(&y5, &y5, 0xb1); // 0008965E
        y6s = mul(&y2, &y6s); // 00089663
        let b8 = pair(d, low + 7); // 00089667 [r8+0x38]
        y1 = fma213(&y1, &y5, &y6s); // 0008966D
        let b6 = pair(d, low + 5); // 00089672 [r8+0x28]
        let y6o = add(&y3, &y1); // 00089678
        let y3o = addsub(&y4, &y1); // 0008967C
        let h2 = quad(d, 2 * (high + 2)); // 00089680 [rcx+0x10]
        let p4 = pair(d, low + 4); // 00089685 [r8+0x20]
        let p6 = pair(d, low + 6); // 0008968B [r8+0x30]
        let x1 = [b6.0, b6.1, p4.0, p4.1]; // 00089685 vmovhps
        let x5 = [b8.0, b8.1, p6.0, p6.1]; // 0008968B vmovhps
        let y2b = [x1[0], x1[1], x1[2], x1[3], x5[0], x5[1], x5[2], x5[3]];
        let h0 = quad(d, 2 * high); // 0008969F [rcx]
        let y5b = [h2[0], h2[1], h2[2], h2[3], h0[0], h0[1], h0[2], h0[3]];
        // 000896A5..000896C4 — stores permutados
        store_pair(d, low + 1, y6o[0], y6o[1]);
        store_pair(d, low, y6o[2], y6o[3]);
        store_pair(d, low + 3, y6o[4], y6o[5]);
        store_pair(d, low + 2, y6o[6], y6o[7]);
        let y1b = xor(&y5b, &m); // 000896CA
        let y6b = sub(&y2b, &y1b); // 000896CE
        // 000896D2..000896D9
        store_pair(d, high + 4, y3o[4], y3o[5]);
        store_pair(d, high + 5, y3o[6], y3o[7]);
        store_pair(d, high + 6, y3o[0], y3o[1]);
        store_pair(d, high + 7, y3o[2], y3o[3]);

        // ---- segunda metade ----
        let t2 = quad(tw, t + 8); // 000896DE [r9+0x20]
        let t3 = quad(tw, t + 12); // 000896E8 [r9+0x30]
        let y3t = [t2[0], t2[1], t2[2], t2[3], t3[0], t3[1], t3[2], t3[3]];
        let mut y4c = shuf(&y3t, &y3t, 0xa0); // 000896F3
        let mut y5c = shuf(&y3t, &y3t, 0xf5); // 000896F8
        y4c = xor(&y4c, &m); // 000896FD
        let y3c = xor(&y2b, &m); // 00089701
        let mut y2c = shuf(&y6b, &y6b, 0xb1); // 00089705
        y2c = mul(&y4c, &y2c); // 0008970A
        y5c = fma213(&y5c, &y6b, &y2c); // 0008970E
        let y1c = add(&y1b, &y5c); // 00089713
        let y3d = addsub(&y3c, &y5c); // 00089717
        // 0008971B..0008973B
        store_pair(d, low + 4, y1c[2], y1c[3]);
        store_pair(d, low + 5, y1c[0], y1c[1]);
        store_pair(d, low + 7, y1c[4], y1c[5]);
        store_pair(d, low + 6, y1c[6], y1c[7]);
        // 00089745..0008974A
        store_pair(d, high + 2, y3d[0], y3d[1]);
        store_pair(d, high + 3, y3d[2], y3d[3]);
        store_pair(d, high, y3d[4], y3d[5]);
        store_pair(d, high + 1, y3d[6], y3d[7]);

        low += 8;
        high -= 8;
        t += 16;
        eax += 0x10; // 00089606
    }
}

/// Caminho lento de `0x895C0` (`00089768`..`000899AC`), para `len >= 0x40000`
/// (ordem 19 → `len = n/2 = 262144`). Processa a tabela em blocos de `0x800`
/// pares; cada bloco aplica o twiddle de bloco `tw[0x800 + 2·block]` (par
/// `(cos,−sin)`) e repete a tabela `tw[0..0x800)` dentro do bloco (16 f32 por
/// iteração). Os valores do lado "high" entram escalados por `0.5`
/// (`00089768 vbroadcastf128`, `[0x1DFC7C0] = 0.5`), por isso o resultado é
/// equivalente ao caminho rápido, mas com a metade em dobro somada no fim.
pub fn split_ccs_slow(d: &mut [f32], len: usize, tw: &[f32]) {
    assert!(len >= 0x40000);
    assert!(d.len() >= 2 * len + 2);
    let m = MASK;
    let half: V8 = [0.5f32; 8];
    let mut low = 1usize; // r8 = buf+8 (par)
    let mut high = len - 8; // rcx = buf + len*8 - 0x40 (par)
    let mut block = 0usize; // 0008978E edx
    while block * 0x800 < len {
        // 000897A0..000897C0: twiddle de bloco, (w0,w1) → broadcast
        let bw0 = tw[0x800 + 2 * block];
        let bw1 = tw[0x800 + 2 * block + 1];
        let y5: V8 = [bw0; 8]; // vshufps 0xa0 (por lane de 128 b → broadcast)
        let y6b: V8 = [bw1; 8]; // vshufps 0xf5
        let mut r11 = 0usize; // floats em tw (000897A4 r11 = r9)
        let mut ebp = 0usize;
        while ebp < 0x800 {
            // ===== 1ª metade (000897E0..0008986E) =====
            let a2 = pair(d, low + 1); // 000897E0 [r8+8]
            let a1 = pair(d, low); // 000897E9 [r8]
            let xmm7 = [a2.0, a2.1, a1.0, a1.1];
            let h6 = quad(d, 2 * (high + 6)); // 000897EE [rcx+0x30]
            let a4 = pair(d, low + 3); // 000897F3 [r8+0x18]
            let a3 = pair(d, low + 2); // 000897F9 [r8+0x10]
            let xmm2 = [a4.0, a4.1, a3.0, a3.1];
            let y4 = [xmm7[0], xmm7[1], xmm7[2], xmm7[3], xmm2[0], xmm2[1], xmm2[2], xmm2[3]];
            let h4 = quad(d, 2 * (high + 4)); // 00089811 [rcx+0x20]
            let y7i = [h6[0], h6[1], h6[2], h6[3], h4[0], h4[1], h4[2], h4[3]];
            let t = mul(&half, &y7i); // 00089818
            let mut y8 = half;
            let mut y7 = xor(&t, &m); // 0008981C
            y8 = fmaaddsub213(&y8, &y4, &t); // 00089820 vfmaddsub213ps
            y7 = fma231(&y7, &y4, &half); // 00089825

            let tw0 = quad(tw, r11); // 0008982A [r11]
            let tw1 = quad(tw, r11 + 4); // 00089833 [r11+0x10]
            let y3 = [tw0[0], tw0[1], tw0[2], tw0[3], tw1[0], tw1[1], tw1[2], tw1[3]];
            let y2 = shuf(&y3, &y3, 0xb1); // 0008983A
            let mut y4b = mul(&y6b, &y2); // 0008983F
            y4b = fmaaddsub231(&y4b, &y3, &y5); // 00089843
            let y2b = shuf(&y4b, &y4b, 0xa0); // 00089848
            let y3b = shuf(&y4b, &y4b, 0xf5); // 0008984D
            let mut y4c = xor(&y2b, &m); // 00089852
            let y2c = shuf(&y8, &y8, 0xb1); // 00089856
            y4c = mul(&y4c, &y2c); // 0008985C
            y8 = fma213(&y8, &y3b, &y4c); // 00089860
            let y2d = add(&y7, &y8); // 00089865
            let y7b = xor(&y7, &m); // 0008986A
            let y7c = addsub(&y7b, &y8); // 0008986E

            // ===== 2ª metade, leituras (00089873..000898A4) =====
            let b6 = pair(d, low + 5); // 00089873 [r8+0x28]
            let p4 = pair(d, low + 4); // 00089879 [r8+0x20]
            let b8 = pair(d, low + 7); // 0008987F [r8+0x38]
            let p6 = pair(d, low + 6); // 00089885 [r8+0x30]
            let y3c = [b6.0, b6.1, p4.0, p4.1, b8.0, b8.1, p6.0, p6.1];
            let h2 = quad(d, 2 * (high + 2)); // 00089895 [rcx+0x10]
            let h0 = quad(d, 2 * high); // 0008989E [rcx]
            let y8i = [h2[0], h2[1], h2[2], h2[3], h0[0], h0[1], h0[2], h0[3]];
            let y8s = mul(&half, &y8i); // 000898A4
            let mut y4d = half; // 000898D5
            let mut y2 = xor(&y8s, &m); // 000898D9
            y4d = fmaaddsub213(&y4d, &y3c, &y8s); // 000898DD
            y2 = fma231(&y2, &y3c, &half); // 000898E2

            // ===== stores da 1ª metade (000898A9..000898E7) =====
            store_pair(d, low + 1, y2d[0], y2d[1]);
            store_pair(d, low, y2d[2], y2d[3]);
            store_pair(d, low + 3, y2d[4], y2d[5]);
            store_pair(d, low + 2, y2d[6], y2d[7]);
            store_pair(d, high + 4, y7c[4], y7c[5]);
            store_pair(d, high + 5, y7c[6], y7c[7]);
            store_pair(d, high + 6, y7c[0], y7c[1]);
            store_pair(d, high + 7, y7c[2], y7c[3]);

            // ===== 2ª metade, twiddle e butterfly (000898EC..00089935) =====
            let tw2 = quad(tw, r11 + 8); // 000898EC [r11+0x20]
            let tw3 = quad(tw, r11 + 12); // 000898F6 [r11+0x30]
            let y3d = [tw2[0], tw2[1], tw2[2], tw2[3], tw3[0], tw3[1], tw3[2], tw3[3]];
            r11 += 16; // 000898FD add r11,0x40
            let y8e = shuf(&y3d, &y3d, 0xb1); // 00089901
            let mut y7d = mul(&y6b, &y8e); // 00089906
            y7d = fmaaddsub231(&y7d, &y3d, &y5); // 0008990B
            let y8f = shuf(&y7d, &y7d, 0xa0); // 00089910
            let mut y3e = xor(&y8f, &m); // 00089915
            let y8g = shuf(&y4d, &y4d, 0xb1); // 00089919
            y3e = mul(&y3e, &y8g); // 0008991E
            let y7e = shuf(&y7d, &y7d, 0xf5); // 00089923
            y4d = fma213(&y4d, &y7e, &y3e); // 00089928
            let y8h = add(&y2, &y4d); // 0008992D
            let y2b2 = xor(&y2, &m); // 00089931
            let y7f = addsub(&y2b2, &y4d); // 00089935

            // ===== stores da 2ª metade (00089939..00089969) =====
            store_pair(d, low + 5, y8h[0], y8h[1]);
            store_pair(d, low + 4, y8h[2], y8h[3]);
            store_pair(d, low + 7, y8h[4], y8h[5]);
            store_pair(d, low + 6, y8h[6], y8h[7]);
            store_pair(d, high + 2, y7f[0], y7f[1]);
            store_pair(d, high + 3, y7f[2], y7f[3]);
            store_pair(d, high, y7f[4], y7f[5]);
            store_pair(d, high + 1, y7f[6], y7f[7]);

            low += 8; // 00089960 add r8,0x40
            high -= 8; // 0008996F add rcx,-0x40
            ebp += 0x10; // 000897E6
        }
        block += 1; // 0008997F
    }
}

// ---------------------------------------------------------------------------
// 0x8C280 — kernel complexo de 64 pontos (ordem 7), literal
// ---------------------------------------------------------------------------

macro_rules! kc {
    ($($b:expr),* $(,)?) => {
        [$(f32::from_bits($b)),*]
    };
}

const KC140: V8 = kc!(0x0000_0000, 0x0000_0000, 0x3dc8_bd36, 0xbdc8_bd36, 0x3e47_c5c2, 0xbe47_c5c2, 0x3e94_a031, 0xbe94_a031);
const KC160: V8 = kc!(0x3f80_0000, 0x3f80_0000, 0x3f7e_c46d, 0x3f7e_c46d, 0x3f7b_14be, 0x3f7b_14be, 0x3f74_fa0b, 0x3f74_fa0b);
const KC180: V8 = kc!(0x0000_0000, 0x0000_0000, 0x3e47_c5c2, 0xbe47_c5c2, 0x3ec3_ef15, 0xbec3_ef15, 0x3f0e_39da, 0xbf0e_39da);
const KC1A0: V8 = kc!(0x3f80_0000, 0x3f80_0000, 0x3f7b_14be, 0x3f7b_14be, 0x3f6c_835e, 0x3f6c_835e, 0x3f54_db31, 0x3f54_db31);
const KC1C0: V8 = kc!(0x0000_0000, 0x0000_0000, 0x3e94_a031, 0xbe94_a031, 0x3f0e_39da, 0xbf0e_39da, 0x3f45_e403, 0xbf45_e403);
const KC1E0: V8 = kc!(0x3f6c_835e, 0x3f6c_835e, 0x3f61_c598, 0x3f61_c598, 0x3f54_db31, 0x3f54_db31, 0x3f45_e403, 0x3f45_e403);
const KC200: V8 = kc!(0x3f80_0000, 0x3f80_0000, 0x3f74_fa0b, 0x3f74_fa0b, 0x3f54_db31, 0x3f54_db31, 0x3f22_6799, 0x3f22_6799);
const KC220: V8 = kc!(0x3f35_04f3, 0x3f35_04f3, 0x3f0e_39da, 0x3f0e_39da, 0x3ec3_ef15, 0x3ec3_ef15, 0x3e47_c5c2, 0x3e47_c5c2);
const KC240: V8 = kc!(0x3ec3_ef15, 0xbec3_ef15, 0x3ef1_5aea, 0xbef1_5aea, 0x3f0e_39da, 0xbf0e_39da, 0x3f22_6799, 0xbf22_6799);
const KC260: V8 = kc!(0x3f35_04f3, 0xbf35_04f3, 0x3f54_db31, 0xbf54_db31, 0x3f6c_835e, 0xbf6c_835e, 0x3f7b_14be, 0xbf7b_14be);
const KC280: V8 = kc!(0x3f6c_835e, 0xbf6c_835e, 0x3f7e_c46d, 0xbf7e_c46d, 0x3f7b_14be, 0xbf7b_14be, 0x3f61_c598, 0xbf61_c598);
const KC2A0: V8 = kc!(0x3ec3_ef15, 0x3ec3_ef15, 0x3dc8_bd36, 0x3dc8_bd36, 0xbe47_c5c2, 0xbe47_c5c2, 0xbef1_5aea, 0xbef1_5aea);
const KC2C0: V8 = kc!(0x3f80_0000, 0xbf80_0000, 0x3f6c_835e, 0xbf6c_835e, 0x3f35_04f3, 0xbf35_04f3, 0x3ec3_ef15, 0xbec3_ef15);
const KC2E0: V8 = kc!(0x3f6c_835e, 0xbf6c_835e, 0x3f22_6799, 0xbf22_6799, 0x3e47_c5c2, 0xbe47_c5c2, 0xbe94_a031, 0x3e94_a031);
const KC300: V8 = kc!(0x3f35_04f3, 0xbf35_04f3, 0x3e47_c5c2, 0xbe47_c5c2, 0xbec3_ef15, 0x3ec3_ef15, 0xbf54_db31, 0x3f54_db31);
const KC320: V8 = kc!(0x3ec3_ef15, 0xbec3_ef15, 0xbe94_a031, 0x3e94_a031, 0xbf54_db31, 0x3f54_db31, 0xbf7e_c46d, 0x3f7e_c46d);
const KC340: V8 = kc!(0x0000_0000, 0x0000_0000, 0xbec3_ef15, 0xbec3_ef15, 0xbf35_04f3, 0xbf35_04f3, 0xbf6c_835e, 0xbf6c_835e);
const KC360: V8 = kc!(0xbec3_ef15, 0xbec3_ef15, 0xbf45_e403, 0xbf45_e403, 0xbf7b_14be, 0xbf7b_14be, 0xbf74_fa0b, 0xbf74_fa0b);
const KC380: V8 = kc!(0xbf35_04f3, 0xbf35_04f3, 0xbf7b_14be, 0xbf7b_14be, 0xbf6c_835e, 0xbf6c_835e, 0xbf0e_39da, 0xbf0e_39da);
const KC3A0: V8 = kc!(0xbf6c_835e, 0xbf6c_835e, 0xbf74_fa0b, 0xbf74_fa0b, 0xbf0e_39da, 0xbf0e_39da, 0x3dc8_bd36, 0x3dc8_bd36);

/// `vshufps ymm_dst, ymm_a, ymm_b, imm` com dois vetores distintos.
#[inline(always)]
fn shuf2(a: &V8, b: &V8, imm: u32) -> V8 {
    shuf(a, b, imm)
}

/// Transcreve `0x8C280`..`0x8C961` (64 pontos complexos = os 128 f32 de uma
/// ordem 7 real). `r13` é a área de rascunho empilhada: `s[k]` = `[r13+0x20k]`.
///
/// Não lê `r8`/`r9`/`r11` (conferido: nenhuma ocorrência no desmonte), então
/// é chamável como `(src, dst)` só.
pub fn kernel7(src: &[f32; 128], dst: &mut [f32; 128]) {
    let g = |j: usize| -> V8 { load8(src, j * 8) };
    let z = [0f32; 8];
    let mut y0 = z;
    let mut y1 = z;
    let mut y2 = z;
    let mut y3 = z;
    let mut y4 = z;
    let mut y5 = z;
    let mut y6 = z;
    let mut y7 = z;
    let mut y8 = z;
    let mut y9 = z;
    let mut y10 = z;
    let mut y11 = z;
    let mut y12 = z;
    let mut y13 = z;
    let mut y14 = z;
    let mut y15 = z;
    let mut s = [z; 10];

    // 0008C2EC..0008C356
    y6 = g(14);
    y10 = CM; // vbroadcastf128 [0x1DFD3C0]
    y2 = g(0);
    y3 = g(2);
    y7 = g(12);
    y13 = sub(&y6, &g(6));
    y15 = add(&y2, &g(8));
    y8 = sub(&y3, &g(10));
    y5 = add(&y7, &g(4));
    y1 = add(&y6, &g(6));
    y0 = add(&y3, &g(10));
    y11 = sub(&y2, &g(8));
    y9 = sub(&y7, &g(4));
    y14 = sub(&y1, &y0);
    y3 = add(&y0, &y1);
    y12 = mul(&y10, &y13);
    y2 = MASK; // vbroadcastf128 [0x1DFD3D0]
    y13 = add(&y15, &y5);
    y15 = sub(&y15, &y5);
    y7 = add(&y13, &y3);
    y5 = y8;
    y5 = fma132(&y5, &y12, &y10);
    y12 = fnmadd231(&y12, &y8, &y10);
    y8 = sub(&y13, &y3);
    y4 = shuf(&y14, &y14, 0xb1);
    y6 = xor(&y4, &y2);
    y3 = sub(&y15, &y6);
    y13 = add(&y6, &y15);
    y15 = add(&y9, &y12);
    y9 = sub(&y12, &y9);
    y6 = add(&y11, &y5);
    y11 = sub(&y11, &y5);
    s[0] = y13; // [r13]
    y1 = shuf(&y9, &y9, 0xb1);
    y13 = xor(&y1, &y2);
    y4 = sub(&y11, &y13);
    y11 = add(&y13, &y11);
    // 0008C3C6..0008C410
    y13 = g(3);
    y9 = g(15);
    s[2] = y11; // [r13+0x40]
    y11 = g(13);
    y1 = add(&y13, &g(11));
    y13 = sub(&y13, &g(11));
    y12 = shuf(&y15, &y15, 0xb1);
    y0 = xor(&y12, &y2);
    y5 = sub(&y6, &y0);
    y14 = add(&y0, &y6);
    y15 = add(&y11, &g(5));
    y6 = g(1);
    s[1] = y14; // [r13+0x20]
    y14 = add(&y9, &g(7));
    y12 = add(&y6, &g(9));
    y0 = sub(&y6, &g(9));
    y6 = sub(&y11, &g(5));
    y11 = sub(&y9, &g(7));
    y9 = mul(&y10, &y11);
    y11 = add(&y12, &y15);
    y15 = sub(&y12, &y15);
    y12 = add(&y1, &y14);
    y1 = sub(&y14, &y1);
    y1 = shuf(&y1, &y1, 0xb1);
    y14 = xor(&y1, &y2);
    y1 = y13;
    y1 = fma132(&y1, &y9, &y10);
    y9 = fnmadd231(&y9, &y13, &y10);
    y10 = add(&y11, &y12);
    y11 = sub(&y11, &y12);
    y12 = sub(&y15, &y14);
    y15 = add(&y14, &y15);
    y13 = add(&y0, &y1);
    y14 = sub(&y0, &y1);
    y0 = add(&y6, &y9);
    y9 = sub(&y9, &y6);
    y6 = shuf(&y0, &y0, 0xb1);
    y1 = shuf(&y9, &y9, 0xb1);
    y6 = xor(&y6, &y2);
    y2 = xor(&y1, &y2);
    // 0008C4A6..0008C4BB
    y0 = shuf2(&y7, &y5, 0x44);
    y1 = shuf2(&y7, &y5, 0xee);
    y5 = shuf2(&y3, &y4, 0x44);
    y7 = perm(&y0, &y5, 0x20);
    y3 = shuf2(&y3, &y4, 0xee);
    s[3] = y7; // [r13+0x60]
    y7 = s[2];
    y9 = sub(&y13, &y6);
    y6 = add(&y6, &y13);
    y13 = sub(&y14, &y2);
    y2 = add(&y2, &y14);
    y14 = s[0];
    y4 = perm(&y0, &y5, 0x31);
    y5 = perm(&y1, &y3, 0x20);
    y3 = perm(&y1, &y3, 0x31);
    y1 = s[1];
    y0 = shuf2(&y8, &y7, 0x44);
    y8 = shuf2(&y8, &y7, 0xee);
    y7 = shuf2(&y14, &y1, 0x44);
    y1 = shuf2(&y14, &y1, 0xee);
    y14 = perm(&y0, &y7, 0x20);
    y7 = perm(&y0, &y7, 0x31);
    y0 = perm(&y8, &y1, 0x20);
    y8 = perm(&y8, &y1, 0x31);
    y1 = shuf(&y5, &y5, 0xb1);
    s[4] = y14; // [r13+0x80]
    y14 = mul(&y1, &KC140);
    y5 = fma132(&y5, &y14, &KC160);
    s[5] = y5; // [r13+0xa0]
    y5 = shuf(&y4, &y4, 0xb1);
    y5 = mul(&y5, &KC180);
    y4 = fma132(&y4, &y5, &KC1A0);
    s[6] = y4; // [r13+0xc0]
    y4 = shuf(&y3, &y3, 0xb1);
    y5 = mul(&y4, &KC1C0);
    y4 = KC1E0;
    y3 = fma132(&y3, &y5, &KC200);
    y5 = KC220;
    s[7] = y3; // [r13+0xe0]
    y3 = KC240;
    y1 = shuf(&y0, &y0, 0xb1);
    y14 = mul(&y1, &y3);
    y0 = fma213(&y0, &y4, &y14);
    y14 = KC260;
    s[8] = y0; // [r13+0x100]
    y0 = shuf(&y7, &y7, 0xb1);
    y1 = mul(&y0, &y14);
    y0 = KC280;
    y7 = fma213(&y7, &y5, &y1);
    y1 = KC2A0;
    s[9] = y7; // [r13+0x120]
    y7 = shuf(&y8, &y8, 0xb1);
    y7 = mul(&y7, &y0);
    y8 = fma213(&y8, &y1, &y7);
    y7 = shuf(&y9, &y9, 0xb1);
    y3 = mul(&y7, &y3);
    y9 = fma213(&y9, &y4, &y3);
    y4 = shuf(&y12, &y12, 0xb1);
    y7 = mul(&y4, &y14);
    y12 = fma213(&y12, &y5, &y7);
    y5 = shuf(&y13, &y13, 0xb1);
    y0 = mul(&y5, &y0);
    y13 = fma213(&y13, &y1, &y0);
    y1 = shuf(&y11, &y11, 0xb1);
    y14 = mul(&y1, &KC2C0);
    y4 = shuf(&y2, &y2, 0xb1);
    y7 = shuf(&y15, &y15, 0xb1);
    y1 = shuf(&y6, &y6, 0xb1);
    y3 = mul(&y4, &KC2E0);
    y5 = mul(&y7, &KC300);
    y0 = mul(&y1, &KC320);
    y11 = fma132(&y11, &y14, &KC340);
    y2 = fma132(&y2, &y3, &KC360);
    y15 = fma132(&y15, &y5, &KC380);
    y6 = fma132(&y6, &y0, &KC3A0);
    // 0008C684..0008C6D7
    y3 = s[7];
    y14 = shuf2(&y10, &y9, 0x44);
    y9 = shuf2(&y10, &y9, 0xee);
    y10 = shuf2(&y12, &y13, 0x44);
    y13 = shuf2(&y12, &y13, 0xee);
    y12 = shuf2(&y11, &y2, 0x44);
    y2 = shuf2(&y11, &y2, 0xee);
    y11 = shuf2(&y15, &y6, 0x44);
    y7 = perm(&y14, &y10, 0x20);
    y0 = perm(&y14, &y10, 0x31);
    y4 = perm(&y9, &y13, 0x20);
    y10 = perm(&y9, &y13, 0x31);
    y13 = shuf2(&y15, &y6, 0xee);
    y1 = perm(&y12, &y11, 0x20);
    y15 = perm(&y12, &y11, 0x31);
    // 0008C6DD..0008C7D2
    y12 = s[3];
    y5 = add(&y10, &y3);
    y10 = sub(&y10, &y3);
    y3 = CM;
    y6 = perm(&y2, &y13, 0x20);
    y11 = perm(&y2, &y13, 0x31);
    y2 = add(&y12, &y7);
    y12 = sub(&y12, &y7);
    y7 = s[5];
    y13 = add(&y4, &y7);
    y9 = sub(&y7, &y4);
    y4 = s[6];
    y7 = mul(&y3, &y10);
    y10 = add(&y13, &y5);
    y14 = add(&y0, &y4);
    y5 = sub(&y5, &y13);
    y0 = sub(&y0, &y4);
    y4 = add(&y2, &y14);
    y2 = sub(&y2, &y14);
    y13 = MASK;
    y14 = shuf(&y5, &y5, 0xb1);
    y5 = xor(&y14, &y13);
    y14 = y9;
    y14 = fma132(&y14, &y7, &y3);
    y7 = fnmadd231(&y7, &y9, &y3);
    y9 = add(&y4, &y10);
    y3 = sub(&y4, &y10);
    y4 = sub(&y2, &y5);
    y5 = add(&y5, &y2);
    y13 = sub(&y12, &y14);
    store8(dst, 0, &y9); // [rdx]
    store8(dst, 64, &y3); // [rdx+0x100]
    store8(dst, 32, &y4); // [rdx+0x80]
    store8(dst, 96, &y5); // [rdx+0x180]
    // 0008C797..0008C7F4
    y10 = s[4];
    y9 = add(&y12, &y14);
    y12 = add(&y0, &y7);
    y0 = sub(&y7, &y0);
    y5 = MASK;
    y7 = shuf(&y12, &y12, 0xb1);
    y12 = shuf(&y0, &y0, 0xb1);
    y3 = xor(&y12, &y5);
    y0 = xor(&y7, &y5);
    y4 = sub(&y13, &y3);
    y13 = add(&y3, &y13);
    y2 = sub(&y9, &y0);
    y9 = add(&y0, &y9);
    y5 = add(&y10, &y1);
    store8(dst, 80, &y13); // [rdx+0x140]
    store8(dst, 16, &y2); // [rdx+0x40]
    store8(dst, 112, &y9); // [rdx+0x1c0]
    store8(dst, 48, &y4); // [rdx+0xc0]
    // 0008C7FC..0008C895
    y13 = sub(&y10, &y1);
    y1 = s[8];
    y3 = MASK;
    y9 = add(&y6, &y1);
    y12 = sub(&y1, &y6);
    y1 = add(&y11, &y8);
    y8 = sub(&y11, &y8);
    y6 = s[9];
    y11 = CM;
    y4 = add(&y9, &y1);
    y0 = add(&y15, &y6);
    y9 = sub(&y1, &y9);
    y7 = sub(&y15, &y6);
    y15 = add(&y5, &y0);
    y6 = mul(&y11, &y8);
    y8 = sub(&y5, &y0);
    y2 = shuf(&y9, &y9, 0xb1);
    y5 = xor(&y2, &y3);
    y10 = y12;
    y10 = fma132(&y10, &y6, &y11);
    y6 = fnmadd231(&y6, &y12, &y11);
    y11 = add(&y15, &y4);
    y15 = sub(&y15, &y4);
    y4 = sub(&y8, &y5);
    y8 = add(&y5, &y8);
    y0 = add(&y13, &y10);
    y1 = sub(&y13, &y10);
    y13 = add(&y7, &y6);
    y7 = sub(&y6, &y7);
    store8(dst, 8, &y11); // [rdx+0x20]
    store8(dst, 72, &y15); // [rdx+0x120]
    store8(dst, 40, &y4); // [rdx+0xa0]
    store8(dst, 104, &y8); // [rdx+0x1a0]
    // 0008C8AD..0008C8F0
    y14 = MASK;
    y6 = shuf(&y13, &y13, 0xb1);
    y12 = shuf(&y7, &y7, 0xb1);
    y6 = xor(&y6, &y14);
    y7 = xor(&y12, &y14);
    y2 = sub(&y0, &y6);
    y5 = add(&y6, &y0);
    y3 = sub(&y1, &y7);
    y4 = add(&y7, &y1);
    store8(dst, 24, &y2); // [rdx+0x60]
    store8(dst, 56, &y3); // [rdx+0xe0]
    store8(dst, 88, &y4); // [rdx+0x160]
    store8(dst, 120, &y5); // [rdx+0x1e0]
}

// ---------------------------------------------------------------------------
// Cadeia de 0x72480 para ordem 6
// ---------------------------------------------------------------------------

/// `000725F6`..`00072617`: combina DC e Nyquist na posição do par 0.
pub fn pack_dc_nyq(d: &mut [f32]) {
    let re = d[0];
    let im = d[1];
    d[0] = im + re; // 0007260B vaddss xmm0, xmm2, xmm1
    d[1] = re - im; // 0007260F vsubss xmm3, xmm1, xmm2
}

/// Caminho completo de `0x72480` para ordem 6 (flag 8, `ctx+8 == 0`).
pub fn rfft6(src: &[f32; 64], tw: &[f32]) -> [f32; 66] {
    let mut d = [0f32; 66];
    let mut k = [0f32; 64];
    kernel6(src, &mut k);
    d[..64].copy_from_slice(&k);
    pack_dc_nyq(&mut d);
    split_ccs(&mut d, 32, tw);
    let t = d[1];
    d[64] = t; // 00072631 dst[n] = dst[1]
    d[65] = 0.0; // 00072637
    d[1] = 0.0; // 0007263C
    d
}

/// Caminho completo de `0x72480` para ordem 7 (flag 8, `ctx+8 == 0`).
/// `0007258C` chama `0x8C280`; o resto é o mesmo código de `000725F6`.
pub fn rfft7(src: &[f32; 128], tw: &[f32]) -> [f32; 130] {
    let mut d = [0f32; 130];
    let mut k = [0f32; 128];
    kernel7(src, &mut k);
    d[..128].copy_from_slice(&k);
    pack_dc_nyq(&mut d);
    split_ccs(&mut d, 64, tw);
    let t = d[1];
    d[128] = t;
    d[129] = 0.0;
    d[1] = 0.0;
    d
}

// ---------------------------------------------------------------------------
// 0x1D69E00 — kernel genérico, caminho do áudio (rdx = n/2 = 0x100, ordem 9)
// ---------------------------------------------------------------------------
//
// `000725C7 mov r8d,r14d` passa `1 << (order-1)` = 256 = n/2; com `rdx <= 0x800`
// (`01D6A17E`/`01D6A185`) o código salta para `01D6B03A`, e a cadeia
// `01D6B22F..01D6B243` manda `rdx == 0x100` para `01D6B8C9`. Depois de uma
// passada em `01D6B8C9` o teste `01D6BB7D cmp r11,4 / jg` cai em `01D6BB87`
// (última passada) e o epílogo é `01D6C0E7`. Nada aqui é estimado: cada linha
// é uma instrução de `checks/.build/1d69e00_full.dis`.

/// `0x797B680` (`vxorps` em `01D69ED5`, `01D69F94`, `01D6A043`):
/// `[-0.0, +0.0, -0.0, +0.0, -0.0, +0.0, -0.0, +0.0]`.
const NEG_EVEN: V8 = [
    f32::from_bits(0x8000_0000),
    f32::from_bits(0x0000_0000),
    f32::from_bits(0x8000_0000),
    f32::from_bits(0x0000_0000),
    f32::from_bits(0x8000_0000),
    f32::from_bits(0x0000_0000),
    f32::from_bits(0x8000_0000),
    f32::from_bits(0x0000_0000),
];

/// `0x797B640` (lido no dump): `0.7071068286895752` (`0x3f3504f4`) × 8.
const F8P: V8 = [f32::from_bits(0x3f35_04f4); 8];

/// `0x797B660` (lido no dump): `-0.7071068286895752` (`0xbf3504f4`) × 8.
const F8N: V8 = [f32::from_bits(0xbf35_04f4); 8];

/// `vfmadd231ps dst, a, b` → `dst = a*b + dst`.
#[inline(always)]
fn fma231(dst: &V8, a: &V8, b: &V8) -> V8 {
    let mut r = [0f32; 8];
    for i in 0..8 {
        r[i] = a[i].mul_add(b[i], dst[i]);
    }
    r
}

/// `vunpcklps a, b` (por lane de 128 bits): `[a0,b0,a1,b1]`.
#[inline(always)]
fn unpcklps(a: &V8, b: &V8) -> V8 {
    [a[0], b[0], a[1], b[1], a[4], b[4], a[5], b[5]]
}

/// `vunpckhps a, b` (por lane de 128 bits): `[a2,b2,a3,b3]`.
#[inline(always)]
fn unpckhps(a: &V8, b: &V8) -> V8 {
    [a[2], b[2], a[3], b[3], a[6], b[6], a[7], b[7]]
}

/// `vmovupd`/`vmovups` de 32 B, deslocamento em BYTES.
#[inline(always)]
fn ld(d: &[f32], off: usize) -> V8 {
    let i = off / 4;
    [d[i], d[i + 1], d[i + 2], d[i + 3], d[i + 4], d[i + 5], d[i + 6], d[i + 7]]
}

/// `vmovupd`/`vmovups` de 32 B.
#[inline(always)]
fn st(d: &mut [f32], off: usize, v: &V8) {
    let i = off / 4;
    d[i..i + 8].copy_from_slice(v);
}

/// `vextractf128 [mem], ymm, lane` (16 B em `mem`, lane só escolhe a metade).
#[inline(always)]
fn st_lane(d: &mut [f32], off: usize, v: &V8, lane: usize) {
    let i = off / 4;
    d[i..i + 4].copy_from_slice(&v[4 * lane..4 * lane + 4]);
}

/// `vmovaps xmm` + `vinsertf128 ymm, ymm, xmm, 1` (duplica a lane baixa).
#[inline(always)]
fn dup4(d: &[f32], off: usize) -> V8 {
    let i = off / 4;
    [d[i], d[i + 1], d[i + 2], d[i + 3], d[i], d[i + 1], d[i + 2], d[i + 3]]
}

/// 1ª passada de `0x1D69E00` (`01D69EAC`..`01D6A16A`), genérica por ordem.
/// `src` = `n` f32; `ws` = `n` f32 (workspace de `4n` bytes); `r_bytes = n/2`
/// (bytes); `idx` = tabela de `ctx+0x30` (lida em `01D6A04B` a cada 0x40 B,
/// até o `0` sentinela); `tw` não é usada nesta passada.
pub fn kernel_stage1(src: &[f32], ws: &mut [f32], idx: &[u32], _tw: &[f32], r_bytes: usize) {
    let r = r_bytes; // rbp = rdx = n/2, em BYTES (0x100 para ordem 9)

    // ================= 1ª passada: 01D69EAC..01D6A16A =================
    let mut rbx = 0usize; // byte em src
    let mut r10 = 2 * r;
    let mut r13 = 0usize; // byte em ws
    let mut r14 = 2 * r;
    let mut tab = 16usize; // idx[16], idx[32], ...
    loop {
        // ---- bloco A: grupos pares, metade de baixo → pares, 0x00..0x20
        let mut y4 = ld(src, rbx);
        let mut y1 = ld(src, rbx + 4 * r);
        let mut y5 = ld(src, r10);
        let mut y3 = ld(src, r10 + 4 * r);
        let mut y0 = add(&y4, &y1); // 01D69EC0
        y4 = sub(&y4, &y1); // 01D69EC4
        y4 = shuf(&y4, &y4, 0xb1); // 01D69EC8
        let mut y2 = add(&y5, &y3); // 01D69ECD
        y5 = sub(&y5, &y3); // 01D69ED1
        y5 = xor(&y5, &NEG_EVEN); // 01D69ED5
        let y14 = ld(src, rbx + 0x20); // 01D69EDD
        let y15 = ld(src, r10 + 0x20); // 01D69EE2
        let y11 = ld(src, rbx + 4 * r + 0x20); // 01D69EE8
        let y13 = ld(src, r10 + 4 * r + 0x20); // 01D69EEE
        rbx += r; // 01D69EF5
        r10 += r; // 01D69EF9
        y1 = add(&y0, &y2); // 01D69EFD
        y0 = sub(&y0, &y2); // 01D69F01
        y3 = add(&y4, &y5); // 01D69F05
        y4 = sub(&y4, &y5); // 01D69F09
        y2 = shuf(&y1, &y3, 0x44); // 01D69F0D vunpcklpd
        y3 = shuf(&y1, &y3, 0xee); // 01D69F11 vunpckhpd
        y5 = shuf(&y0, &y4, 0x44); // 01D69F15
        y4 = shuf(&y0, &y4, 0xee); // 01D69F19
        y1 = shuf(&y2, &y5, 0xcc); // 01D69F1D
        y2 = shuf(&y2, &y5, 0x99); // 01D69F22
        st_lane(ws, r13, &y1, 0); // 01D69F27
        st_lane(ws, r13 + 0x10, &y2, 0); // 01D69F2E
        st_lane(ws, r14, &y1, 1); // 01D69F35
        st_lane(ws, r14 + 0x10, &y2, 1); // 01D69F3B
        let y0b = shuf(&y3, &y4, 0xcc); // 01D69F42
        let y3b = shuf(&y3, &y4, 0x99); // 01D69F47
        st_lane(ws, r13 + 4 * r, &y0b, 0); // 01D69F4C
        st_lane(ws, r13 + 4 * r + 0x10, &y3b, 0); // 01D69F54
        st_lane(ws, r14 + 4 * r, &y0b, 1); // 01D69F5C
        st_lane(ws, r14 + 4 * r + 0x10, &y3b, 1); // 01D69F63

        // ---- bloco A2: grupos ímpares, metade de baixo → pares, 0x20..0x40
        let mut z8 = ld(src, rbx); // 01D69F6B
        let mut z6 = ld(src, rbx + 4 * r); // 01D69F6F
        let mut z9 = ld(src, r10); // 01D69F74
        let mut z7 = ld(src, r10 + 4 * r); // 01D69F79
        let mut z0 = add(&z8, &z6); // 01D69F7F
        let mut z4 = sub(&z8, &z6); // 01D69F83
        z4 = shuf(&z4, &z4, 0xb1); // 01D69F87
        let mut z2 = add(&z9, &z7); // 01D69F8C
        let mut z5 = sub(&z9, &z7); // 01D69F90
        z5 = xor(&z5, &NEG_EVEN); // 01D69F94
        z8 = ld(src, rbx + 0x20); // 01D69F9C
        z9 = ld(src, r10 + 0x20); // 01D69FA1
        z6 = ld(src, rbx + 4 * r + 0x20); // 01D69FA7
        z7 = ld(src, r10 + 4 * r + 0x20); // 01D69FAD
        let mut z1 = add(&z0, &z2); // 01D69FB4
        z0 = sub(&z0, &z2); // 01D69FB8
        let mut z3 = add(&z4, &z5); // 01D69FBC
        z4 = sub(&z4, &z5); // 01D69FC0
        z2 = shuf(&z1, &z3, 0x44); // 01D69FC4
        z3 = shuf(&z1, &z3, 0xee); // 01D69FC8
        z5 = shuf(&z0, &z4, 0x44); // 01D69FCC
        z4 = shuf(&z0, &z4, 0xee); // 01D69FD0
        let z0b = shuf(&z3, &z4, 0xcc); // 01D69FD4
        let z3b = shuf(&z3, &z4, 0x99); // 01D69FD9
        st_lane(ws, r14 + 4 * r + 0x20, &z0b, 1); // 01D69FDE
        st_lane(ws, r14 + 4 * r + 0x30, &z3b, 1); // 01D69FE6
        st_lane(ws, r13 + 4 * r + 0x20, &z0b, 0); // 01D69FEE
        st_lane(ws, r13 + 4 * r + 0x30, &z3b, 0); // 01D69FF6
        let z1b = shuf(&z2, &z5, 0xcc); // 01D69FFE
        let z2b = shuf(&z2, &z5, 0x99); // 01D6A003
        st_lane(ws, r14 + 0x20, &z1b, 1); // 01D6A008
        st_lane(ws, r14 + 0x30, &z2b, 1); // 01D6A00F
        st_lane(ws, r13 + 0x20, &z1b, 0); // 01D6A016
        st_lane(ws, r13 + 0x30, &z2b, 0); // 01D6A01D
        r13 += r; // 01D6A024
        r14 += r; // 01D6A027

        // ---- bloco B: grupos pares, metade de cima → ímpares, 0x00..0x20
        y0 = add(&y14, &y11); // 01D6A02A
        y4 = sub(&y14, &y11); // 01D6A02F
        y4 = shuf(&y4, &y4, 0xb1); // 01D6A034
        y2 = add(&y15, &y13); // 01D6A039
        y5 = sub(&y15, &y13); // 01D6A03E
        y5 = xor(&y5, &NEG_EVEN); // 01D6A043
        rbx = (idx[tab] as usize) * 32; // 01D6A04B..01D6A056
        tab += 16; // 01D6A052
        r10 = rbx + 2 * r; // 01D6A05A
        y1 = add(&y0, &y2); // 01D6A05E
        y0 = sub(&y0, &y2); // 01D6A062
        y3 = add(&y4, &y5); // 01D6A066
        y4 = sub(&y4, &y5); // 01D6A06A
        y2 = shuf(&y1, &y3, 0x44); // 01D6A06E
        y3 = shuf(&y1, &y3, 0xee); // 01D6A072
        y5 = shuf(&y0, &y4, 0x44); // 01D6A076
        y4 = shuf(&y0, &y4, 0xee); // 01D6A07A
        y1 = shuf(&y2, &y5, 0xcc); // 01D6A07E
        y2 = shuf(&y2, &y5, 0x99); // 01D6A083
        st_lane(ws, r13, &y1, 0); // 01D6A088
        st_lane(ws, r13 + 0x10, &y2, 0); // 01D6A08F
        st_lane(ws, r14, &y1, 1); // 01D6A096
        st_lane(ws, r14 + 0x10, &y2, 1); // 01D6A09C
        y0 = shuf(&y3, &y4, 0xcc); // 01D6A0A3
        y3 = shuf(&y3, &y4, 0x99); // 01D6A0A8
        st_lane(ws, r13 + 4 * r, &y0, 0); // 01D6A0AD
        st_lane(ws, r13 + 4 * r + 0x10, &y3, 0); // 01D6A0B5
        st_lane(ws, r14 + 4 * r, &y0, 1); // 01D6A0BD
        st_lane(ws, r14 + 4 * r + 0x10, &y3, 1); // 01D6A0C4

        // ---- bloco C: grupos ímpares, metade de cima → ímpares, 0x20..0x40
        z0 = add(&z8, &z6); // 01D6A0CC
        z4 = sub(&z8, &z6); // 01D6A0D0
        z4 = shuf(&z4, &z4, 0xb1); // 01D6A0D4
        z2 = add(&z9, &z7); // 01D6A0D9
        z5 = sub(&z9, &z7); // 01D6A0DD
        z5 = xor(&z5, &NEG_EVEN); // 01D6A0E1
        z1 = add(&z0, &z2); // 01D6A0E9
        z0 = sub(&z0, &z2); // 01D6A0ED
        z3 = add(&z4, &z5); // 01D6A0F1
        z4 = sub(&z4, &z5); // 01D6A0F5
        z2 = shuf(&z1, &z3, 0x44); // 01D6A0F9
        z3 = shuf(&z1, &z3, 0xee); // 01D6A0FD
        z5 = shuf(&z0, &z4, 0x44); // 01D6A101
        z4 = shuf(&z0, &z4, 0xee); // 01D6A105
        let z0c = shuf(&z3, &z4, 0xcc); // 01D6A109
        let z3c = shuf(&z3, &z4, 0x99); // 01D6A10E
        st_lane(ws, r14 + 4 * r + 0x20, &z0c, 1); // 01D6A113
        st_lane(ws, r14 + 4 * r + 0x30, &z3c, 1); // 01D6A11B
        st_lane(ws, r13 + 4 * r + 0x20, &z0c, 0); // 01D6A123
        st_lane(ws, r13 + 4 * r + 0x30, &z3c, 0); // 01D6A12B
        let z1c = shuf(&z2, &z5, 0xcc); // 01D6A133
        let z2c = shuf(&z2, &z5, 0x99); // 01D6A138
        st_lane(ws, r14 + 0x20, &z1c, 1); // 01D6A13D
        st_lane(ws, r14 + 0x30, &z2c, 1); // 01D6A144
        st_lane(ws, r13 + 0x20, &z1c, 0); // 01D6A14B
        st_lane(ws, r13 + 0x30, &z2c, 0); // 01D6A152

        r13 -= r; // 01D6A159
        r14 -= r; // 01D6A15C
        r13 += 0x40; // 01D6A15F
        r14 += 0x40; // 01D6A163
        if rbx == 0 {
            break; // 01D6A167 cmp rbx,r12 / 01D6A16A jne
        }
    }

    // ================= 2ª passada: 01D6B03A..01D6B20C =================
}

/// Um passo radix-4 da 3ª passada (`01D6B901..01D6BA0B`), no lugar.
///
/// `o` e `tb` em BYTES. As 8 entradas (`o+{0x00,0x20,0x80,0xa0,0x100,0x120,
/// 0x180,0x1a0}`) são lidas antes de qualquer escrita, então o passo pode ser
/// feito no lugar (o conjunto lido é igual ao conjunto escrito).
fn pass3a_step(d: &mut [f32], o: usize, tw: &[f32], tb: usize, r10: usize) {
    let t1 = ld(tw, tb); // 01D6B908
    let t2 = ld(tw, tb + 0x20); // 01D6B913
    let t3 = ld(tw, tb + 0x40); // 01D6B963
    let t4 = ld(tw, tb + 0x60); // 01D6B96F
    let t5 = ld(tw, tb + 0x80); // 01D6B932
    let t6 = ld(tw, tb + 0xa0); // 01D6B941

    // C: o + 2*r10 (re) / +0x20 (im)
    let c_re = ld(d, o + 2 * r10); // 01D6B901
    let c_im = ld(d, o + 2 * r10 + 0x20); // 01D6B90C
    let mut y0 = mul(&t1, &c_re); // 01D6B918
    let mut y1 = mul(&t1, &c_im); // 01D6B91D
    y0 = fnmadd231(&y0, &t2, &c_im); // 01D6B921
    y1 = fma231(&y1, &t2, &c_re); // 01D6B926

    // D: o + 3*r10
    let d_re = ld(d, o + 3 * r10); // 01D6B92B
    let d_im = ld(d, o + 3 * r10 + 0x20); // 01D6B93A
    let mut y9 = mul(&t5, &d_re); // 01D6B949
    let mut y10 = mul(&t5, &d_im); // 01D6B94E
    y9 = fnmadd231(&y9, &t6, &d_im); // 01D6B952
    y10 = fma231(&y10, &t6, &d_re); // 01D6B957

    // B: o + r10
    let b_re = ld(d, o + r10); // 01D6B95C
    let b_im = ld(d, o + r10 + 0x20); // 01D6B968
    let mut y2 = mul(&t3, &b_re); // 01D6B974
    let mut y3 = mul(&t3, &b_im); // 01D6B979
    y2 = fnmadd231(&y2, &t4, &b_im); // 01D6B97D
    y3 = fma231(&y3, &t4, &b_re); // 01D6B982

    let y4 = add(&y9, &y0); // 01D6B98E
    let y0 = sub(&y0, &y9); // 01D6B992
    let y5 = add(&y10, &y1); // 01D6B997
    let y1 = sub(&y1, &y10); // 01D6B99B

    // X0: o
    let x0re = ld(d, o); // 01D6B9A0
    let y6 = sub(&x0re, &y2); // 01D6B9A6
    let y2b = add(&x0re, &y2); // 01D6B9AA
    st(d, o, &add(&y2b, &y4)); // 01D6B9AE/01D6B9B2
    st(d, o + 2 * r10, &sub(&y2b, &y4)); // 01D6B9B8/01D6B9BC

    let x0im = ld(d, o + 0x20); // 01D6B9C3
    let y4b = sub(&x0im, &y3); // 01D6B9C9
    let y3b = add(&x0im, &y3); // 01D6B9CD
    st(d, o + 0x20, &add(&y3b, &y5)); // 01D6B9D1/01D6B9D5
    st(d, o + 2 * r10 + 0x20, &sub(&y3b, &y5)); // 01D6B9DB/01D6B9DF

    st(d, o + r10, &add(&y6, &y1)); // 01D6B9E6/01D6B9EA
    st(d, o + 3 * r10, &sub(&y6, &y1)); // 01D6B9F1/01D6B9F5
    st(d, o + r10 + 0x20, &sub(&y4b, &y0)); // 01D6B9FC/01D6BA00
    st(d, o + 3 * r10 + 0x20, &add(&y4b, &y0)); // 01D6BA07/01D6BA0B
}

/// 2ª passada de `0x1D69E00` (`01D6B03A..01D6B20C`): radix-4 com twiddles
/// sobre o workspace, no lugar. `rdx = n/2` em bytes; o laço roda
/// `[rsp+8] = rdx/16` decrementado de 2 → `rdx/32` iterações de 0x100 B.
pub fn pass2(ws: &mut [f32], tw: &[f32], rdx: usize) {
    let mut p = 0usize; // r13
    let stp = 0x20usize; // r10 = 4 << 3
    let rax = 0x60usize; // r10*3
                         // 01D6B05D..01D6B098: 6 xmm duplicados para as duas lanes
    let t8 = dup4(tw, 0x00);
    let t9 = dup4(tw, 0x10);
    let t10 = dup4(tw, 0x20);
    let t11 = dup4(tw, 0x30);
    let t12 = dup4(tw, 0x40);
    let t13 = dup4(tw, 0x50);
    for _ in 0..(rdx / 32) {
        let mut y0 = ld(ws, p + 2 * stp); // 01D6B09E
        let y15 = perm(&y0, &ld(ws, p + 2 * stp + 0x80), 0x20); // 01D6B0A5
        let y14 = perm(&y0, &ld(ws, p + 2 * stp + 0x80), 0x31); // 01D6B0B0
        y0 = mul(&t8, &y15); // 01D6B0BB
        let mut y1 = mul(&t8, &y14); // 01D6B0C0
        y0 = fnmadd231(&y0, &t9, &y14); // 01D6B0C5
        y1 = fma231(&y1, &t9, &y15); // 01D6B0CA
        let mut y4 = ld(ws, p + rax); // 01D6B0CF
        let y15b = perm(&y4, &ld(ws, p + rax + 0x80), 0x20); // 01D6B0D6
        let y14b = perm(&y4, &ld(ws, p + rax + 0x80), 0x31); // 01D6B0E1
        y4 = mul(&t12, &y15b); // 01D6B0EC
        let mut y5 = mul(&t12, &y14b); // 01D6B0F1
        y4 = fnmadd231(&y4, &t13, &y14b); // 01D6B0F6
        y5 = fma231(&y5, &t13, &y15b); // 01D6B0FB
        let mut y2 = ld(ws, p + stp); // 01D6B100
        let y15c = perm(&y2, &ld(ws, p + stp + 0x80), 0x20); // 01D6B107
        let y14c = perm(&y2, &ld(ws, p + stp + 0x80), 0x31); // 01D6B112
        y2 = mul(&t10, &y15c); // 01D6B11D
        let mut y3 = mul(&t10, &y14c); // 01D6B122
        y2 = fnmadd231(&y2, &t11, &y14c); // 01D6B127
        y3 = fma231(&y3, &t11, &y15c); // 01D6B12C
        let mut y7 = ld(ws, p); // 01D6B131
        let mut y6 = perm(&y7, &ld(ws, p + 0x80), 0x20); // 01D6B137
        y7 = perm(&y7, &ld(ws, p + 0x80), 0x31); // 01D6B141
        let y14d = add(&y0, &y4); // 01D6B14B
        y0 = sub(&y0, &y4); // 01D6B14F
        let y15d = add(&y1, &y5); // 01D6B153
        y1 = sub(&y1, &y5); // 01D6B157
        let mut y4d = add(&y6, &y2); // 01D6B15B
        y6 = sub(&y6, &y2); // 01D6B15F
        let y5d = add(&y7, &y3); // 01D6B163
        y7 = sub(&y7, &y3); // 01D6B167
        let y2d = add(&y4d, &y14d); // 01D6B16B
        y4d = sub(&y4d, &y14d); // 01D6B170
        let y14e = add(&y6, &y1); // 01D6B175
        y6 = sub(&y6, &y1); // 01D6B179
        st(ws, p, &perm(&y2d, &y14e, 0x20)); // 01D6B17D/01D6B183
        st(ws, p + 0x80, &perm(&y2d, &y14e, 0x31)); // 01D6B189/01D6B18F
        st(ws, p + 2 * stp, &perm(&y4d, &y6, 0x20)); // 01D6B198/01D6B19E
        st(ws, p + 2 * stp + 0x80, &perm(&y4d, &y6, 0x31)); // 01D6B1A5/01D6B1AB
        let y3u = add(&y5d, &y15d); // 01D6B1B5
        let y5u = sub(&y5d, &y15d); // 01D6B1BA
        let y15u = sub(&y7, &y0); // 01D6B1BF
        let y7u = add(&y7, &y0); // 01D6B1C3
        st(ws, p + stp, &perm(&y3u, &y15u, 0x20)); // 01D6B1C7/01D6B1CD
        st(ws, p + stp + 0x80, &perm(&y3u, &y15u, 0x31)); // 01D6B1D4/01D6B1DA
        st(ws, p + rax, &perm(&y5u, &y7u, 0x20)); // 01D6B1E4/01D6B1EA
        st(ws, p + rax + 0x80, &perm(&y5u, &y7u, 0x31)); // 01D6B1F1/01D6B1F7
        p += 0x100; // 01D6B201
    }
}

/// Estágio de 16 pontos (`01D6B8C9..01D6BA2C`): `r11` blocos de
/// `r10_in/8` passos radix-4 cada, no lugar. `r10_in` é o valor de `[rsp]`
/// (`0x10` na 1ª chamada, `0x80` depois do laço radix-8). Devolve o `rbx`
/// final (`mov rcx, rbx` em `01D6BA2C`).
pub fn stage16(
    ws: &mut [f32],
    tw: &[f32],
    rcx: usize,
    r10_in: usize,
    n_in: usize,
) -> usize {
    let r10 = r10_in << 3; // 01D6B8E5
    let rax = 3 * r10; // 01D6B8E9
    let mut r11 = n_in >> 2; // 01D6B8C9
    let mut r13 = 0usize; // 01D6B8D9
    let mut tb_last = rcx;
    while r11 > 0 {
        let mut tb = rcx; // 01D6B8FA `mov rbx, rcx`
        let mut cnt = r10_in; // 01D6B8FD `mov r12, [rsp]`
        while cnt > 0 {
            pass3a_step(ws, r13, tw, tb, r10);
            tb += 0xc0; // 01D6B987
            r13 += 0x40; // 01D6BA12
            cnt -= 8; // 01D6BA16
        }
        r13 += rax; // 01D6BA20
        r11 -= 1; // 01D6BA23
        tb_last = tb;
    }
    tb_last
}

/// 2ª e 3ª passadas de `0x1D69E00` para a ordem 9 (`01D6B03A..01D6B20C` e
/// `01D6B8C9..01D6BA2C`). Ao final, `ws` é exatamente o workspace que o
/// plugin entrega à 4ª passada.
pub fn kernel9_stage2(ws: &mut [f32], tw: &[f32]) {
    pass2(ws, tw, 0x100);
    let _ = stage16(ws, tw, 0x60, 0x10, 0x10);
}

/// Passada final de `0x1D69E00` (`01D6BB87..01D6BD14`): lê o workspace e
/// escreve `dst` em ordem natural. Separada para poder comparar o estado
/// intermediário do workspace com o do plugin.
pub fn kernel9_final(ws: &[f32], dst: &mut [f32], tw: &[f32]) {
    {
        let stp = 0x200usize; // r10 = 64 << 3
        let rax = 0x600usize; // r10*3
        let mut r12 = 0usize; // ws
        let mut q = 0usize; // dst
        // `rcx` em 01D6BB6D recebe `rbx` do fim da 3ª passada = tw+0x60+0x180
        // (4 blocos × 2 passos, mas o twiddle só avança dentro do último
        // bloco: reinicia em 01D6B8FA e avança 2×0xc0). Base = tw+0x1e0.
        let mut tb = 0x1e0usize;
        for _ in 0..8 {
            let mut y8 = ld(ws, r12 + 2 * stp); // 01D6BBA3
            let t1 = ld(tw, tb); // 01D6BBA9
            let mut y6 = ld(ws, r12 + 2 * stp + 0x20); // 01D6BBAD
            let t2 = ld(tw, tb + 0x20); // 01D6BBB4
            let mut y0 = mul(&t1, &y8); // 01D6BBB9
            let mut y1 = mul(&t1, &y6); // 01D6BBBE
            y0 = fnmadd231(&y0, &t2, &y6); // 01D6BBC2
            y1 = fma231(&y1, &t2, &y8); // 01D6BBC7
            y8 = ld(ws, r12 + rax); // 01D6BBCC
            let t5 = ld(tw, tb + 0x80); // 01D6BBD2
            y6 = ld(ws, r12 + rax + 0x20); // 01D6BBDA
            let t6 = ld(tw, tb + 0xa0); // 01D6BBE1
            let mut y9 = mul(&t5, &y8); // 01D6BBE9
            let mut y10 = mul(&t5, &y6); // 01D6BBEE
            y9 = fnmadd231(&y9, &t6, &y6); // 01D6BBF2
            y10 = fma231(&y10, &t6, &y8); // 01D6BBF7
            y8 = ld(ws, r12 + stp); // 01D6BBFC
            let t3 = ld(tw, tb + 0x40); // 01D6BC02
            y6 = ld(ws, r12 + stp + 0x20); // 01D6BC07
            let t4 = ld(tw, tb + 0x60); // 01D6BC0E
            let mut y2 = mul(&t3, &y8); // 01D6BC13
            let mut y3 = mul(&t3, &y6); // 01D6BC18
            y2 = fnmadd231(&y2, &t4, &y6); // 01D6BC1C
            y3 = fma231(&y3, &t4, &y8); // 01D6BC21
            tb += 0xc0; // 01D6BC26
            let y4 = add(&y9, &y0); // 01D6BC2D
            y0 = sub(&y0, &y9); // 01D6BC31
            let y5 = add(&y10, &y1); // 01D6BC36
            y1 = sub(&y1, &y10); // 01D6BC3A
            let mut y7 = ld(ws, r12); // 01D6BC3F
            y6 = sub(&y7, &y2); // 01D6BC45
            let mut y2b = add(&y7, &y2); // 01D6BC49
            let y8b = add(&y2b, &y4); // 01D6BC4D
            y2b = sub(&y2b, &y4); // 01D6BC51
            y7 = ld(ws, r12 + 0x20); // 01D6BC55
            let mut y4b = sub(&y7, &y3); // 01D6BC5C
            let mut y3b = add(&y7, &y3); // 01D6BC60
            let y7c = add(&y3b, &y5); // 01D6BC64
            y3b = sub(&y3b, &y5); // 01D6BC68
            let y5c = add(&y6, &y1); // 01D6BC6C
            y6 = sub(&y6, &y1); // 01D6BC70
            let y1b = sub(&y4b, &y0); // 01D6BC74
            y4b = add(&y4b, &y0); // 01D6BC78
            let a0 = unpcklps(&y8b, &y7c); // 01D6BC7C
            let a1 = unpckhps(&y8b, &y7c); // 01D6BC80
            st(dst, q, &perm(&a0, &a1, 0x20)); // 01D6BC84/01D6BC8A
            st(dst, q + 0x20, &perm(&a0, &a1, 0x31)); // 01D6BC90/01D6BC96
            let b0 = unpcklps(&y5c, &y1b); // 01D6BC9C
            let b1 = unpckhps(&y5c, &y1b); // 01D6BCA0
            st(dst, q + stp, &perm(&b0, &b1, 0x20)); // 01D6BCA4/01D6BCAA
            st(dst, q + stp + 0x20, &perm(&b0, &b1, 0x31)); // 01D6BCB1/01D6BCB7
            let c0 = unpcklps(&y2b, &y3b); // 01D6BCBE
            let c1 = unpckhps(&y2b, &y3b); // 01D6BCC2
            st(dst, q + 2 * stp, &perm(&c0, &c1, 0x20)); // 01D6BCC6/01D6BCCC
            st(dst, q + 2 * stp + 0x20, &perm(&c0, &c1, 0x31)); // 01D6BCD3/01D6BCD9
            let d0 = unpcklps(&y6, &y4b); // 01D6BCE0
            let d1 = unpckhps(&y6, &y4b); // 01D6BCE4
            st(dst, q + rax, &perm(&d0, &d1, 0x20)); // 01D6BCE8/01D6BCEE
            st(dst, q + rax + 0x20, &perm(&d0, &d1, 0x31)); // 01D6BCF5/01D6BCFB
            r12 += 0x40; // 01D6BD02
            q += 0x40; // 01D6BD06
        }
    }
}

/// Corpo radix-8 de `01D6B28C..01D6B55F` (workspace, no lugar).
/// `r12`/`r13`/`r10`/`rax`/`tb` em BYTES; `r13` é um ponteiro de `ws`
/// (aqui passado relativo ao início) e `tb` = `rbx` na tabela `tw`.
fn radix8_body_inplace(
    ws: &mut [f32],
    r12: usize,
    r13: usize,
    r10: usize,
    rax: usize,
    tw: &[f32],
    tb: usize,
) {
    let mut y2 = ld(ws, r12 + r10 * 2); // 01D6B28C
    let mut y1 = ld(tw, tb + 0x40); // 01D6B292
    let mut y0 = mul(&y1, &y2); // 01D6B297
    let mut y8 = ld(ws, r12 + r10 * 2 + 0x20); // 01D6B29B
    y1 = mul(&y1, &y8); // 01D6B2A2
    let mut y9 = ld(tw, tb + 0x60); // 01D6B2A7
    y0 = fnmadd231(&y0, &y9, &y8); // 01D6B2AC
    y1 = fma231(&y1, &y9, &y2); // 01D6B2B1
    let mut y4 = ld(ws, r12 + rax); // 01D6B2B6
    let mut y3 = ld(tw, tb + 0x140); // 01D6B2BC
    let mut y14 = mul(&y3, &y4); // 01D6B2C4
    let mut y10 = ld(ws, r12 + rax + 0x20); // 01D6B2C8
    let mut y6 = mul(&y3, &y10); // 01D6B2CF
    let mut y11 = ld(tw, tb + 0x160); // 01D6B2D4
    y14 = fnmadd231(&y14, &y11, &y10); // 01D6B2DC
    y6 = fma231(&y6, &y11, &y4); // 01D6B2E1
    y2 = add(&y14, &y0); // 01D6B2E6
    y0 = sub(&y0, &y14); // 01D6B2EA
    y3 = add(&y6, &y1); // 01D6B2EF
    y1 = sub(&y1, &y6); // 01D6B2F3
    y6 = ld(ws, r12 + r10); // 01D6B2F7
    let mut y5 = ld(tw, tb + 0xc0); // 01D6B2FD
    y4 = mul(&y5, &y6); // 01D6B305
    let mut y12 = ld(ws, r12 + r10 + 0x20); // 01D6B309
    y5 = mul(&y5, &y12); // 01D6B310
    let mut y13 = ld(tw, tb + 0xe0); // 01D6B315
    y4 = fnmadd231(&y4, &y13, &y12); // 01D6B31D
    y5 = fma231(&y5, &y13, &y6); // 01D6B322
    y8 = ld(ws, r13); // 01D6B327
    let mut y7 = ld(tw, tb); // 01D6B32D
    y6 = mul(&y7, &y8); // 01D6B331
    y14 = ld(ws, r13 + 0x20); // 01D6B336
    y7 = mul(&y7, &y14); // 01D6B33C
    let mut y15 = ld(tw, tb + 0x20); // 01D6B341
    y6 = fnmadd231(&y6, &y15, &y14); // 01D6B346
    y7 = fma231(&y7, &y15, &y8); // 01D6B34B
    y10 = ld(ws, r13 + r10); // 01D6B350
    y12 = ld(tw, tb + 0x100); // 01D6B357
    y14 = mul(&y12, &y10); // 01D6B35F
    y9 = ld(ws, r13 + r10 + 0x20); // 01D6B364
    y12 = mul(&y12, &y9); // 01D6B36B
    y13 = ld(tw, tb + 0x120); // 01D6B370
    y14 = fnmadd231(&y14, &y13, &y9); // 01D6B378
    y12 = fma231(&y12, &y13, &y10); // 01D6B37D
    y8 = add(&y14, &y6); // 01D6B382
    y6 = sub(&y6, &y14); // 01D6B386
    y9 = add(&y12, &y7); // 01D6B38B
    y7 = sub(&y7, &y12); // 01D6B38F
    y12 = ld(ws, r13 + r10 * 2); // 01D6B394
    y11 = ld(tw, tb + 0x80); // 01D6B39B
    y10 = mul(&y11, &y12); // 01D6B3A3
    y14 = ld(ws, r13 + r10 * 2 + 0x20); // 01D6B3A8
    y11 = mul(&y11, &y14); // 01D6B3AF
    y15 = ld(tw, tb + 0xa0); // 01D6B3B4
    y10 = fnmadd231(&y10, &y15, &y14); // 01D6B3BC
    y11 = fma231(&y11, &y15, &y12); // 01D6B3C1
    y12 = ld(ws, r13 + rax); // 01D6B3C6
    y13 = ld(tw, tb + 0x180); // 01D6B3CD
    y12 = mul(&y13, &y12); // 01D6B3D5
    y14 = ld(ws, r13 + rax + 0x20); // 01D6B3DA
    y13 = mul(&y13, &y14); // 01D6B3E1
    y15 = ld(tw, tb + 0x1a0); // 01D6B3E6
    y12 = fnmadd231(&y12, &y15, &y14); // 01D6B3EE
    y13 = fma231(&y13, &y15, &ld(ws, r13 + rax)); // 01D6B3F3

    y14 = ld(ws, r12); // 01D6B401
    y15 = sub(&y14, &y4); // 01D6B407
    y14 = add(&y4, &y14); // 01D6B40B
    y4 = sub(&y14, &y2); // 01D6B410
    y2 = add(&y2, &y14); // 01D6B414
    y14 = sub(&y10, &y12); // 01D6B419
    y12 = add(&y12, &y10); // 01D6B41E
    y10 = sub(&y11, &y13); // 01D6B423
    y13 = add(&y13, &y11); // 01D6B428
    y11 = sub(&y8, &y12); // 01D6B42D
    y12 = add(&y12, &y8); // 01D6B432
    y8 = sub(&y15, &y1); // 01D6B437
    y15 = add(&y15, &y1); // 01D6B43B
    y1 = sub(&y9, &y13); // 01D6B43F
    y13 = add(&y13, &y9); // 01D6B444
    y9 = sub(&y2, &y12); // 01D6B449
    y2 = add(&y2, &y12); // 01D6B44E
    st(ws, r12, &y2); // 01D6B453
    y2 = ld(ws, r12 + 0x20); // 01D6B459
    y12 = sub(&y2, &y5); // 01D6B460
    y5 = add(&y5, &y2); // 01D6B464
    y2 = sub(&y6, &y10); // 01D6B468
    y6 = add(&y6, &y10); // 01D6B46D
    y6 = mul(&y6, &F8P); // 01D6B472
    y2 = mul(&y2, &F8N); // 01D6B47A
    y10 = sub(&y7, &y14); // 01D6B482
    y10 = mul(&y10, &F8P); // 01D6B487
    y7 = add(&y7, &y14); // 01D6B48F
    y7 = mul(&y7, &F8N); // 01D6B494
    y14 = sub(&y5, &y3); // 01D6B49C
    y3 = add(&y3, &y5); // 01D6B4A0
    y5 = add(&y12, &y0); // 01D6B4A4
    y12 = sub(&y12, &y0); // 01D6B4A8
    y0 = sub(&y3, &y13); // 01D6B4AC
    y3 = add(&y3, &y13); // 01D6B4B1
    st(ws, r12 + 0x20, &y3); // 01D6B4B6
    st(ws, r13, &y9); // 01D6B4BD
    st(ws, r13 + 0x20, &y0); // 01D6B4C3
    y0 = sub(&y10, &y6); // 01D6B4C9
    y6 = add(&y6, &y10); // 01D6B4CD
    y9 = add(&y7, &y2); // 01D6B4D2
    y2 = sub(&y2, &y7); // 01D6B4D6
    y3 = add(&y4, &y1); // 01D6B4DA
    st(ws, r12 + r10 * 2, &y3); // 01D6B4DE
    y13 = sub(&y14, &y11); // 01D6B4E4
    st(ws, r12 + r10 * 2 + 0x20, &y13); // 01D6B4E9
    y3 = sub(&y4, &y1); // 01D6B4F0
    st(ws, r13 + r10 * 2, &y3); // 01D6B4F4
    y13 = add(&y14, &y11); // 01D6B4FB
    st(ws, r13 + r10 * 2 + 0x20, &y13); // 01D6B500
    y3 = add(&y15, &y6); // 01D6B507
    st(ws, r12 + r10, &y3); // 01D6B50B
    y13 = add(&y12, &y0); // 01D6B511
    st(ws, r12 + r10 + 0x20, &y13); // 01D6B515
    y3 = sub(&y15, &y6); // 01D6B51C
    st(ws, r13 + r10, &y3); // 01D6B520
    y13 = sub(&y12, &y0); // 01D6B527
    st(ws, r13 + r10 + 0x20, &y13); // 01D6B52B
    y3 = add(&y8, &y2); // 01D6B532
    st(ws, r12 + rax, &y3); // 01D6B536
    y13 = add(&y5, &y9); // 01D6B53C
    st(ws, r12 + rax + 0x20, &y13); // 01D6B541
    y3 = sub(&y8, &y2); // 01D6B548
    st(ws, r13 + rax, &y3); // 01D6B54C
    y13 = sub(&y5, &y9); // 01D6B553
    st(ws, r13 + rax + 0x20, &y13); // 01D6B558
}

/// Laço de níveis radix-8 (`01D6B249..01D6B585`), no lugar. Devolve o `rcx`
/// final (`mov rcx, rbx` em `01D6B582`). `r10_in` = `[rsp]` (0x10 nas
/// chamadas que chegam do despacho).
pub fn radix8_levels(
    ws: &mut [f32],
    tw: &[f32],
    rcx: usize,
    r10_in: usize,
    n_in: usize,
) -> usize {
    let r10 = r10_in << 3; // 01D6B262
    let rax = 3 * r10; // 01D6B266
    let mut r11 = n_in >> 3; // 01D6B249
    let mut r12 = 0usize; // 01D6B256 `mov r12, r9`
    let mut r13 = r12 + r10 * 4; // 01D6B26A
    let mut tb_last = rcx;
    while r11 > 0 {
        let mut tb = rcx; // 01D6B289 `mov rbx, rcx`
        let mut a = r12;
        let mut b = r13;
        let end = a + r10; // 01D6B282/01D6B286 `lea rdi, [r10+r12]`
        while a != end {
            radix8_body_inplace(ws, a, b, r10, rax, tw, tb);
            tb += 0x1c0; // 01D6B3FA
            a += 0x40; // 01D6B55F
            b += 0x40; // 01D6B563
        }
        r12 = b + rax; // 01D6B570 `lea r12, [r13+rax]`
        r13 = r12 + r10 * 4; // 01D6B575
        r11 -= 1; // 01D6B579
        tb_last = tb;
    }
    tb_last
}

/// Estágio radix-8 final (`01D6BD19..01D6BD14`): lê o workspace e escreve
/// `dst` em ordem natural (blocos intercalados com `vextractf128`/`vperm2f128`).
pub fn radix8_final(
    ws: &mut [f32],
    dst: &mut [f32],
    tw: &[f32],
    rcx: usize,
    r10_in: usize,
) {
    let r10 = r10_in << 3; // 01D6BD27
    let rax = 3 * r10; // 01D6BD2B
    let mut r12 = 0usize; // 01D6BD1D `mov r12, r9`
    let mut r13 = r12 + r10 * 4; // 01D6BD2F
    let mut r14 = 0usize; // 01D6BD20 `mov r14, rsi`
    let mut r15 = r14 + r10 * 4; // 01D6BD33
    let end = r12 + r10; // 01D6BD37/01D6BD3B
    let mut tb = rcx; // 01D6BD3E `mov rbx, rcx`
    while r12 != end {
        let mut y2 = ld(ws, r12 + r10 * 2); // 01D6BD41
        let mut y1 = ld(tw, tb + 0x40); // 01D6BD47
        let mut y0 = mul(&y1, &y2); // 01D6BD4C
        let mut y8 = ld(ws, r12 + r10 * 2 + 0x20); // 01D6BD50
        y1 = mul(&y1, &y8); // 01D6BD57
        let mut y9 = ld(tw, tb + 0x60); // 01D6BD5C
        y0 = fnmadd231(&y0, &y9, &y8); // 01D6BD61
        y1 = fma231(&y1, &y9, &y2); // 01D6BD66
        let mut y4 = ld(ws, r12 + rax); // 01D6BD6B
        let mut y3 = ld(tw, tb + 0x140); // 01D6BD71
        let mut y14 = mul(&y3, &y4); // 01D6BD79
        let mut y10 = ld(ws, r12 + rax + 0x20); // 01D6BD7D
        let mut y6 = mul(&y3, &y10); // 01D6BD84
        let mut y11 = ld(tw, tb + 0x160); // 01D6BD89
        y14 = fnmadd231(&y14, &y11, &y10); // 01D6BD91
        y6 = fma231(&y6, &y11, &y4); // 01D6BD96
        y2 = add(&y14, &y0); // 01D6BD9B
        y0 = sub(&y0, &y14); // 01D6BD9F
        y3 = add(&y6, &y1); // 01D6BDA4
        y1 = sub(&y1, &y6); // 01D6BDA8
        y6 = ld(ws, r12 + r10); // 01D6BDAC
        let mut y5 = ld(tw, tb + 0xc0); // 01D6BDB2
        y4 = mul(&y5, &y6); // 01D6BDBA
        let mut y12 = ld(ws, r12 + r10 + 0x20); // 01D6BDBE
        y5 = mul(&y5, &y12); // 01D6BDC5
        let mut y13 = ld(tw, tb + 0xe0); // 01D6BDCA
        y4 = fnmadd231(&y4, &y13, &y12); // 01D6BDD2
        y5 = fma231(&y5, &y13, &y6); // 01D6BDD7
        y8 = ld(ws, r13); // 01D6BDDC
        let mut y7 = ld(tw, tb); // 01D6BDE2
        y6 = mul(&y7, &y8); // 01D6BDE6
        y14 = ld(ws, r13 + 0x20); // 01D6BDEB
        y7 = mul(&y7, &y14); // 01D6BDF1
        let mut y15 = ld(tw, tb + 0x20); // 01D6BDF6
        y6 = fnmadd231(&y6, &y15, &y14); // 01D6BDFB
        y7 = fma231(&y7, &y15, &y8); // 01D6BE00
        y10 = ld(ws, r13 + r10); // 01D6BE05
        y12 = ld(tw, tb + 0x100); // 01D6BE0C
        y14 = mul(&y12, &y10); // 01D6BE14
        y9 = ld(ws, r13 + r10 + 0x20); // 01D6BE19
        y12 = mul(&y12, &y9); // 01D6BE20
        y13 = ld(tw, tb + 0x120); // 01D6BE25
        y14 = fnmadd231(&y14, &y13, &y9); // 01D6BE2D
        y12 = fma231(&y12, &y13, &y10); // 01D6BE32
        y8 = add(&y14, &y6); // 01D6BE37
        y6 = sub(&y6, &y14); // 01D6BE3B
        y9 = add(&y12, &y7); // 01D6BE40
        y7 = sub(&y7, &y12); // 01D6BE44
        y12 = ld(ws, r13 + r10 * 2); // 01D6BE49
        y11 = ld(tw, tb + 0x80); // 01D6BE50
        y10 = mul(&y11, &y12); // 01D6BE58
        y14 = ld(ws, r13 + r10 * 2 + 0x20); // 01D6BE5D
        y11 = mul(&y11, &y14); // 01D6BE64
        y15 = ld(tw, tb + 0xa0); // 01D6BE69
        y10 = fnmadd231(&y10, &y15, &y14); // 01D6BE71
        y11 = fma231(&y11, &y15, &y12); // 01D6BE76
        y12 = ld(ws, r13 + rax); // 01D6BE7B
        y13 = ld(tw, tb + 0x180); // 01D6BE82
        y12 = mul(&y13, &y12); // 01D6BE8A
        y14 = ld(ws, r13 + rax + 0x20); // 01D6BE8F
        y13 = mul(&y13, &y14); // 01D6BE96
        y15 = ld(tw, tb + 0x1a0); // 01D6BE9B
        y12 = fnmadd231(&y12, &y15, &y14); // 01D6BEA3
        y13 = fma231(&y13, &y15, &ld(ws, r13 + rax)); // 01D6BEA8
        tb += 0x1c0; // 01D6BEAF

        y14 = ld(ws, r12); // 01D6BEB6
        y15 = sub(&y14, &y4); // 01D6BEBC
        y14 = add(&y4, &y14); // 01D6BEC0
        y4 = sub(&y14, &y2); // 01D6BEC5
        y2 = add(&y2, &y14); // 01D6BEC9
        y14 = sub(&y10, &y12); // 01D6BECE
        y12 = add(&y12, &y10); // 01D6BED3
        y10 = sub(&y11, &y13); // 01D6BED8
        y13 = add(&y13, &y11); // 01D6BEDD
        y11 = sub(&y8, &y12); // 01D6BEE2
        y12 = add(&y12, &y8); // 01D6BEE7
        y8 = sub(&y15, &y1); // 01D6BEEC
        st(ws, r12, &y8); // 01D6BEF0
        y15 = add(&y15, &y1); // 01D6BEF6
        y1 = sub(&y9, &y13); // 01D6BEFA
        y13 = add(&y13, &y9); // 01D6BEFF
        y9 = sub(&y2, &y12); // 01D6BF04
        y2 = add(&y2, &y12); // 01D6BF09
        y8 = ld(ws, r12 + 0x20); // 01D6BF0E
        y12 = sub(&y8, &y5); // 01D6BF15
        y5 = add(&y5, &y8); // 01D6BF19
        y8 = sub(&y6, &y10); // 01D6BF1E
        y6 = add(&y6, &y10); // 01D6BF23
        y6 = mul(&y6, &F8P); // 01D6BF28
        y8 = mul(&y8, &F8N); // 01D6BF30
        y10 = sub(&y7, &y14); // 01D6BF38
        y10 = mul(&y10, &F8P); // 01D6BF3D
        y7 = add(&y7, &y14); // 01D6BF45
        y7 = mul(&y7, &F8N); // 01D6BF4A
        y14 = sub(&y5, &y3); // 01D6BF52
        y3 = add(&y3, &y5); // 01D6BF56
        y5 = add(&y12, &y0); // 01D6BF5A
        y12 = sub(&y12, &y0); // 01D6BF5E
        y0 = sub(&y3, &y13); // 01D6BF62
        y3 = add(&y3, &y13); // 01D6BF67
        y13 = unpcklps(&y2, &y3); // 01D6BF6C
        y3 = unpckhps(&y2, &y3); // 01D6BF70
        y2 = ld(ws, r12); // 01D6BF74
        st_lane(dst, r14, &y13, 0); // 01D6BF7A
        st_lane(dst, r14 + 0x10, &y3, 0); // 01D6BF80
        st_lane(dst, r14 + 0x20, &y13, 1); // 01D6BF87
        st_lane(dst, r14 + 0x30, &y3, 1); // 01D6BF8E
        y13 = unpcklps(&y9, &y0); // 01D6BF95
        y9 = unpckhps(&y9, &y0); // 01D6BF99
        y0 = perm(&y13, &y9, 0x20); // 01D6BF9D
        y13 = perm(&y13, &y9, 0x31); // 01D6BFA3
        st(dst, r15, &y0); // 01D6BFA9
        st(dst, r15 + 0x20, &y13); // 01D6BFAE
        y0 = sub(&y10, &y6); // 01D6BFB4
        y6 = add(&y6, &y10); // 01D6BFB8
        y9 = add(&y7, &y8); // 01D6BFBD
        y8 = sub(&y8, &y7); // 01D6BFC2
        y3 = add(&y4, &y1); // 01D6BFC6
        y13 = sub(&y14, &y11); // 01D6BFCA
        y7 = unpcklps(&y3, &y13); // 01D6BFCF
        y3 = unpckhps(&y3, &y13); // 01D6BFD4
        y13 = perm(&y7, &y3, 0x20); // 01D6BFD9
        y3 = perm(&y7, &y3, 0x31); // 01D6BFDF
        st(dst, r14 + r10 * 2, &y13); // 01D6BFE5
        st(dst, r14 + r10 * 2 + 0x20, &y3); // 01D6BFEB
        y3 = sub(&y4, &y1); // 01D6BFF2
        y13 = add(&y14, &y11); // 01D6BFF6
        y7 = unpcklps(&y3, &y13); // 01D6BFFB
        y3 = unpckhps(&y3, &y13); // 01D6C000
        y13 = perm(&y7, &y3, 0x20); // 01D6C005
        y3 = perm(&y7, &y3, 0x31); // 01D6C00B
        st(dst, r15 + r10 * 2, &y13); // 01D6C011
        st(dst, r15 + r10 * 2 + 0x20, &y3); // 01D6C017
        y3 = add(&y15, &y6); // 01D6C01E
        y13 = add(&y12, &y0); // 01D6C022
        y7 = unpcklps(&y3, &y13); // 01D6C026
        y3 = unpckhps(&y3, &y13); // 01D6C02B
        y13 = perm(&y7, &y3, 0x20); // 01D6C030
        y3 = perm(&y7, &y3, 0x31); // 01D6C036
        st(dst, r14 + r10, &y13); // 01D6C03C
        st(dst, r14 + r10 + 0x20, &y3); // 01D6C042
        y3 = sub(&y15, &y6); // 01D6C049
        y13 = sub(&y12, &y0); // 01D6C04D
        y7 = unpcklps(&y3, &y13); // 01D6C051
        y3 = unpckhps(&y3, &y13); // 01D6C056
        y13 = perm(&y7, &y3, 0x20); // 01D6C05B
        y3 = perm(&y7, &y3, 0x31); // 01D6C061
        st(dst, r15 + r10, &y13); // 01D6C067
        st(dst, r15 + r10 + 0x20, &y3); // 01D6C06D
        y3 = add(&y2, &y8); // 01D6C074
        y13 = add(&y5, &y9); // 01D6C079
        y7 = unpcklps(&y3, &y13); // 01D6C07E
        y3 = unpckhps(&y3, &y13); // 01D6C083
        y13 = perm(&y7, &y3, 0x20); // 01D6C088
        y3 = perm(&y7, &y3, 0x31); // 01D6C08E
        st(dst, r14 + rax, &y13); // 01D6C094
        st(dst, r14 + rax + 0x20, &y3); // 01D6C09A
        y3 = sub(&y2, &y8); // 01D6C0A1
        y13 = sub(&y5, &y9); // 01D6C0A6
        y7 = unpcklps(&y3, &y13); // 01D6C0AB
        y3 = unpckhps(&y3, &y13); // 01D6C0B0
        y13 = perm(&y7, &y3, 0x20); // 01D6C0B5
        y3 = perm(&y7, &y3, 0x31); // 01D6C0BB
        st(dst, r15 + rax, &y13); // 01D6C0C1
        st(dst, r15 + rax + 0x20, &y3); // 01D6C0C7

        r12 += 0x40; // 01D6C0CE
        r13 += 0x40; // 01D6C0D2
        r14 += 0x40; // 01D6C0D6
        r15 += 0x40; // 01D6C0DA
    }
}

/// Estágio radix-4 final (`01D6BB87..01D6BD14`): lê o workspace e escreve
/// `dst` em ordem natural. `r10_in` = `[rsp]` (0x40/0x80/0x200 conforme a
/// ordem); o laço roda `r10_in/8` iterações.
pub fn radix4_final(
    ws: &[f32],
    dst: &mut [f32],
    tw: &[f32],
    rcx: usize,
    r10_in: usize,
) {
    let r10 = r10_in << 3; // 01D6BB98
    let rax = 3 * r10; // 01D6BB9C
    let mut r11 = r10_in; // 01D6BB95
    let mut r12 = 0usize; // 01D6BB8B `mov r12, r9`
    let mut r13 = 0usize; // 01D6BB8E `mov r13, rsi`
    let mut tb = rcx; // 01D6BBA0 `mov rbx, rcx`
    while r11 > 0 {
        let mut y8 = ld(ws, r12 + r10 * 2); // 01D6BBA3
        let mut y1 = ld(tw, tb); // 01D6BBA9
        let mut y6 = ld(ws, r12 + r10 * 2 + 0x20); // 01D6BBAD
        let mut y7 = ld(tw, tb + 0x20); // 01D6BBB4
        let mut y0 = mul(&y1, &y8); // 01D6BBB9
        y1 = mul(&y1, &y6); // 01D6BBBE
        y0 = fnmadd231(&y0, &y7, &y6); // 01D6BBC2
        y1 = fma231(&y1, &y7, &y8); // 01D6BBC7
        y8 = ld(ws, r12 + rax); // 01D6BBCC
        let y5 = ld(tw, tb + 0x80); // 01D6BBD2
        y6 = ld(ws, r12 + rax + 0x20); // 01D6BBDA
        y7 = ld(tw, tb + 0xa0); // 01D6BBE1
        let mut y9 = mul(&y5, &y8); // 01D6BBE9
        let mut y10 = mul(&y5, &y6); // 01D6BBEE
        y9 = fnmadd231(&y9, &y7, &y6); // 01D6BBF2
        y10 = fma231(&y10, &y7, &y8); // 01D6BBF7
        y8 = ld(ws, r12 + r10); // 01D6BBFC
        let mut y3 = ld(tw, tb + 0x40); // 01D6BC02
        y6 = ld(ws, r12 + r10 + 0x20); // 01D6BC07
        y7 = ld(tw, tb + 0x60); // 01D6BC0E
        let mut y2 = mul(&y3, &y8); // 01D6BC13
        y3 = mul(&y3, &y6); // 01D6BC18
        y2 = fnmadd231(&y2, &y7, &y6); // 01D6BC1C
        y3 = fma231(&y3, &y7, &y8); // 01D6BC21
        tb += 0xc0; // 01D6BC26
        let y4 = add(&y9, &y0); // 01D6BC2D
        y0 = sub(&y0, &y9); // 01D6BC31
        let y5b = add(&y10, &y1); // 01D6BC36
        y1 = sub(&y1, &y10); // 01D6BC3A
        y7 = ld(ws, r12); // 01D6BC3F
        y6 = sub(&y7, &y2); // 01D6BC45
        let y2b = add(&y7, &y2); // 01D6BC49
        let y8b = add(&y2b, &y4); // 01D6BC4D
        let y2c = sub(&y2b, &y4); // 01D6BC51
        y7 = ld(ws, r12 + 0x20); // 01D6BC55
        let mut y4b = sub(&y7, &y3); // 01D6BC5C
        let mut y3b = add(&y7, &y3); // 01D6BC60
        let y7c = add(&y3b, &y5b); // 01D6BC64
        y3b = sub(&y3b, &y5b); // 01D6BC68
        let y5c = add(&y6, &y1); // 01D6BC6C
        y6 = sub(&y6, &y1); // 01D6BC70
        let y1b = sub(&y4b, &y0); // 01D6BC74
        y4b = add(&y4b, &y0); // 01D6BC78
        let a0 = unpcklps(&y8b, &y7c); // 01D6BC7C
        let a1 = unpckhps(&y8b, &y7c); // 01D6BC80
        st(dst, r13, &perm(&a0, &a1, 0x20)); // 01D6BC84/01D6BC8A
        st(dst, r13 + 0x20, &perm(&a0, &a1, 0x31)); // 01D6BC90/01D6BC96
        let b0 = unpcklps(&y5c, &y1b); // 01D6BC9C
        let b1 = unpckhps(&y5c, &y1b); // 01D6BCA0
        st(dst, r13 + r10, &perm(&b0, &b1, 0x20)); // 01D6BCA4/01D6BCAA
        st(dst, r13 + r10 + 0x20, &perm(&b0, &b1, 0x31)); // 01D6BCB1/01D6BCB7
        let c0 = unpcklps(&y2c, &y3b); // 01D6BCBE
        let c1 = unpckhps(&y2c, &y3b); // 01D6BCC2
        st(dst, r13 + r10 * 2, &perm(&c0, &c1, 0x20)); // 01D6BCC6/01D6BCCC
        st(dst, r13 + r10 * 2 + 0x20, &perm(&c0, &c1, 0x31)); // 01D6BCD3/01D6BCD9
        let d0 = unpcklps(&y6, &y4b); // 01D6BCE0
        let d1 = unpckhps(&y6, &y4b); // 01D6BCE4
        st(dst, r13 + rax, &perm(&d0, &d1, 0x20)); // 01D6BCE8/01D6BCEE
        st(dst, r13 + rax + 0x20, &perm(&d0, &d1, 0x31)); // 01D6BCF5/01D6BCFB
        r12 += 0x40; // 01D6BD02
        r13 += 0x40; // 01D6BD06
        r11 -= 8; // 01D6BD0A
    }
}

/// Caminho `rdx > 0x800` (`01D6A18B..01D6AD24` + final `01D6AD6A..01D6B035`),
/// usado pelas ordens 13..19.
///
/// O laço externo fatia `n/2` em blocos de `0x800` (complexos); cada bloco
/// (`0x1000` floats) é processado pelo mesmo "descascamento" (peeling):
/// 2ª passada radix-8 (`01D6A1EB`), depois estágios radix-4 (`01D6A3E9`) ou,
/// quando `r10 == 0x10` e `rdx & 0x55555555 == 0`, radix-8 (`01D6A6B0`);
/// `r10` cresce ×4 (radix-4) ou ×8 (radix-8) e `[rsp+0x28]` divide por 4 ou 8.
/// Terminado o bloco, `r9` avança `0x4000` B e `rcx` volta ao início dos
/// twiddles. Ao fim, o laço `01D6AD77` roda estágios radix-4 (`stage16`) sobre
/// o array inteiro até `[rsp+0x28] == 4`, e então `radix4_final` (`01D6BB87`).
pub fn kernel_large(ws: &mut [f32], dst: &mut [f32], tw: &[f32], rdx: usize) {
    let mask = rdx & 0x5555_5555; // 01D6A1CF
    let mut remaining = rdx; // [rsp+0x30]
    let mut chunk = 0usize; // r9 (floats)
    let mut rcx = 0usize; // rcx (bytes em tw)
    let mut r10 = 4usize; // [rsp+0x10]
    let mut r11 = 0x200usize; // [rsp+0x18] = 0x800 >> 2
    let mut sub28 = rdx >> 2; // [rsp+0x20]/[rsp+0x28]
    loop {
        loop {
            if r10 == 4 {
                // 01D6A1EB: 2ª passada do bloco (64 × 0x100 B = 0x4000 B)
                pass2(&mut ws[chunk..], tw, 0x800);
                rcx += 0x60; // 01D6A3C3
                r10 = 0x10; // 01D6A3CA
                sub28 >>= 2; // 01D6A3D6
                r11 = 0x80; // [rsp+8] = 0x200 >> 2
                continue;
            }
            if r11 < 4 {
                break; // 01D6A1C5/01D6A1C9
            }
            if mask != 0 {
                let n_in = r11;
                rcx = stage16(&mut ws[chunk..], tw, rcx, r10, n_in); // 01D6A3E9
                r10 <<= 2; // 01D6A694
                sub28 >>= 2; // 01D6A69D
                r11 = n_in >> 2; // 01D6A6A6
            } else if r10 == 0x10 {
                let n_in = r11;
                rcx = radix8_levels(&mut ws[chunk..], tw, rcx, r10, n_in); // 01D6A6B0
                r10 <<= 3; // 01D6AD09
                sub28 >>= 3; // 01D6AD12
                r11 = n_in >> 3; // 01D6AD1B
            } else {
                let n_in = r11;
                rcx = stage16(&mut ws[chunk..], tw, rcx, r10, n_in); // 01D6A3E9
                r10 <<= 2;
                sub28 >>= 2;
                r11 = n_in >> 2;
            }
        }
        remaining -= 0x800; // 01D6AD2A
        if remaining == 0 {
            break;
        }
        chunk += 0x1000; // 01D6AD47 `r9 += 0x4000` (B)
        rcx = 0; // 01D6AD3C/01D6AD41
        r10 = 4; // 01D6AD5B
        r11 = 0x200; // 01D6AD60
        sub28 = rdx >> 2; // 01D6AD51/01D6AD56
    }
    // 01D6AD6A: r9 volta à base; 01D6AD77: estágios radix-4 finais.
    if std::env::var_os("FFT_DBG").is_some() {
        eprintln!("chunks={} rcx_f={} r10f={} sub28={}", chunk / 0x1000, rcx, r10, sub28);
    }
    let mut r11f = sub28;
    let mut r10f = r10;
    let mut rcx_f = rcx;
    if std::env::var_os("FFT_V1").is_some() {
        rcx_f = 0;
    }
    if std::env::var_os("FFT_V2").is_some() {
        r10f = 0x10;
    }
    while r11f != 4 {
        let n_in = r11f;
        rcx_f = stage16(ws, tw, rcx_f, r10f, n_in); // 01D6ADB9
        r10f <<= 2; // 01D6B028
        r11f = n_in >> 2;
    }
    if std::env::var_os("FFT_V4").is_some() {
        rcx_f = stage16(ws, tw, rcx_f, r10f, 0x10);
        r10f <<= 2;
    }
    radix4_final(ws, dst, tw, rcx_f, r10f); // 01D6BB87
}

/// `0x1D69E00` genérico para as ordens 8..19.
///
/// Fluxo literal: 1ª passada → despacho `01D6A17E` (`cmp rdx,0x800`).
/// Para `rdx <= 0x800` (ordens 8..12): 2ª passada e despacho `01D6B225`.
/// As ordens 8/9/10/11/12 passam, respectivamente, por `01D6BD19`
/// (radix-8 final), `01D6B8C9` (16 pontos → radix-4),
/// `01D6B249`→`01D6BB87`, `01D6B249`→`01D6BD19` e
/// `01D6B249`→`01D6B8C9`→`01D6BB87`.
/// Para `rdx > 0x800` (ordens 13..19) → `kernel_large` (`01D6A18B`).
pub fn kernel_generic(
    src: &[f32],
    ws: &mut [f32],
    dst: &mut [f32],
    idx: &[u32],
    tw: &[f32],
    n: usize,
) {
    let rdx = n / 2; // rdx = n/2 (bytes; ver 01D69E91 `mov rbp, rdx`)
    kernel_stage1(src, ws, idx, tw, rdx);
    if rdx > 0x800 {
        // 01D6A17E `cmp rdx,0x800` / 01D6A185 `jle 01D6B03A`
        kernel_large(ws, dst, tw, rdx); // 01D6A18B..01D6B035
        return;
    }
    pass2(ws, tw, rdx);
    let r10 = 0x10usize; // 01D6B219
    let r11 = rdx / 16; // 01D6B220
    let rcx = 0x60usize; // 01D6B212/01D6B216
    if r11 == 4 {
        radix4_final(ws, dst, tw, rcx, r10);
    } else if r11 == 8 {
        radix8_final(ws, dst, tw, rcx, r10);
    } else if r11 == 0x10 {
        let rcx2 = stage16(ws, tw, rcx, r10, r11);
        radix4_final(ws, dst, tw, rcx2, r10 << 2); // 01D6BB70/01D6BB74
    } else {
        // 01D6B249: laço radix-8 e re-despacho em 01D6B89E.
        let rcx2 = radix8_levels(ws, tw, rcx, r10, r11);
        let r10b = r10 << 3; // 01D6B8A2
        let r11b = rdx / 128; // 01D6B8A6 `[rsp+8]` após `shr r11,3`
        if r11b == 4 {
            radix4_final(ws, dst, tw, rcx2, r10b);
        } else if r11b == 8 {
            radix8_final(ws, dst, tw, rcx2, r10b);
        } else {
            // `r11b == 0x10` (ordem 12) → 16 pontos e depois radix-4.
            let rcx3 = stage16(ws, tw, rcx2, r10b, r11b);
            radix4_final(ws, dst, tw, rcx3, r10b << 2); // 01D6BB70/01D6BB74
        }
    }
}

/// `0x1D69E00` completo (as três passadas), para ordem 9.
pub fn kernel9(src: &[f32], ws: &mut [f32], dst: &mut [f32], idx: &[u32], tw: &[f32]) {
    kernel9_stages12(src, ws, idx, tw);
    kernel9_final(ws, dst, tw);
}

/// Passadas 1 e 2 (o que o plugin deixa no workspace antes da última passada).
pub fn kernel9_stages12(src: &[f32], ws: &mut [f32], idx: &[u32], tw: &[f32]) {
    kernel_stage1(src, ws, idx, tw, 0x100);
    kernel9_stage2(ws, tw);
}

/// Caminho completo de `0x72480` para ordem 9 (flag 8, `ctx+8 == 0`).
pub fn rfft9(src: &[f32; 512], tw38: &[f32], idx: &[u32], tw50: &[f32]) -> [f32; 514] {
    let mut ws = vec![0f32; 512];
    let mut buf = [0f32; 512];
    kernel9(src, &mut ws, &mut buf, idx, tw38);
    let mut d = [0f32; 514];
    d[..512].copy_from_slice(&buf);
    pack_dc_nyq(&mut d);
    split_ccs(&mut d, 256, tw50);
    let t = d[1];
    d[512] = t;
    d[513] = 0.0;
    d[1] = 0.0;
    d
}

/// Caminho completo de `0x72480` para qualquer ordem 8..12 (`flag 8`,
/// `ctx+8 == 0`): kernel genérico + pack + split + `dst[n]=dst[1]`.
pub fn rfft_generic(
    src: &[f32],
    tw38: &[f32],
    idx: &[u32],
    tw50: &[f32],
    n: usize,
) -> Vec<f32> {
    let mut ws = vec![0f32; n];
    let mut buf = vec![0f32; n];
    kernel_generic(src, &mut ws, &mut buf, idx, tw38, n);
    let mut d = vec![0f32; n + 2];
    d[..n].copy_from_slice(&buf);
    pack_dc_nyq(&mut d);
    split_ccs(&mut d, n / 2, tw50);
    let t = d[1];
    d[n] = t;
    d[n + 1] = 0.0;
    d[1] = 0.0;
    d
}

// ---------------------------------------------------------------------------
// Testes
// ---------------------------------------------------------------------------

