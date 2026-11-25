//! Etapa M4 — conversão normalizado → plain do setter `0x867D80` (`00867E10
//! call [rdx+0x50]`), transcrita bit a bit.
//!
//! Fonte: `checks/867d80_m4.dis`, `checks/3351e0.dis`, `checks/3358f0.dis`,
//! `checks/335300.dis`, `checks/335470.dis`, `checks/335670.dis`,
//! `checks/335830.dis` e `checks/u_estado_m4.md`.
//!
//! ## Identidade de `rdx` (PROVADO: instrução + medição somente-leitura)
//!
//! - **Por instrução:**
//!   - `0x33A630` (slot 1 da vtable `0x2037178`, subobjeto `W = processor+0xE40`)
//!     faz `rdx = [[W+0x70]] + idx·0x68` (`0033A642`..`0033A654`) e chama
//!     `[W+0x30]` com `rcx = [W+0x68]` (`0033A657`..`0033A65F`).
//!   - `[W+0x70]` = `0x23926F8` (`00344DD6` → `00336EA6`), e
//!     `[0x23926F8]` = `0x238E9C0`.
//! - **Por medição** (host somente-leitura, `SOULTREE_PROBE=1`):
//!   - `[W+0x30]` = `0x862EF0`;
//!   - `0x862EF0` faz `rcx = [rcx]` e `cvtsd2ss xmm2`, depois `jmp 0x867D80`.
//!
//! Logo, no setter, `rdx` é a entrada `0x238E9C0 + i·0x68` e `[rdx+0x50]` é o
//! callback daquela entrada ([`crate::param_entries::ENTRIES`]).
//!
//! A refutação anterior (P2) tinha lido a tabela com base `0x238E9B0`, deslocada
//! em `0x10`.
//!
//! ## Chamada
//!
//! `xmm1 = (double)norm` (`00867E00 cvtps2pd`), `rcx = rdx` (`00867DAE`).
//! O retorno vem em `xmm0` como `double` e vira `float` em `00867E1A`.
//!
//! ## Matemática da UCRT
//!
//! `log` = `0x1C9A9EF`, `exp` = `0x1C9A9D1`, `pow` = `0x1C9A5AD` (todos
//! `api-ms-win-crt-math`) e `round` = `[0x1D8D7C0]` (IAT índice 6). No
//! `x86_64-pc-windows-msvc`, `f64::ln/exp/powf` do Rust chamam essas mesmas
//! funções da UCRT em tempo de execução. `round` é exato por definição.

/// `maxsd a, b` (`a > b ? a : b`; NaN ou igualdade devolve `b`).
#[inline(always)]
fn maxsd(a: f64, b: f64) -> f64 {
    if a > b { a } else { b }
}

/// `minsd a, b` (`a < b ? a : b`; NaN ou igualdade devolve `b`).
#[inline(always)]
fn minsd(a: f64, b: f64) -> f64 {
    if a < b { a } else { b }
}

/// Seleção por `cmov` comum aos callbacks, por exemplo `003351F6..00335226`:
/// `p = (x >= 0) ? &x : &0`, depois `(x <= 1 ou NaN) ? p : &1`.
#[inline(always)]
fn sel01(x: f64) -> f64 {
    let p = if x >= 0.0 { x } else { 0.0 };
    if x > 1.0 { 1.0 } else { p }
}

/// Família do callback `+0x50`.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Curve {
    /// `0x3351E0`: `t·(max−min) + min`.
    Linear,
    /// `0x3358F0`: `x >= 0.5 ? 1 : 0`.
    Bool,
    /// `0x335300`: inteiro arredondado.
    Int,
    /// `0x335470`: log com deslocamento 150.
    LogOff150,
    /// `0x335670`: log com centro `[e+0x38]` em `t = 0.5`.
    LogSkew,
    /// `0x335830`: log puro.
    Log,
}

impl Curve {
    pub fn from_rva(rva: u32) -> Option<Curve> {
        Some(match rva {
            0x3351E0 => Curve::Linear,
            0x3358F0 => Curve::Bool,
            0x335300 => Curve::Int,
            0x335470 => Curve::LogOff150,
            0x335670 => Curve::LogSkew,
            0x335830 => Curve::Log,
            _ => return None,
        })
    }
}

/// Uma entrada `0x238E9C0 + i·0x68` (campos usados pelos callbacks).
#[derive(Clone, Copy, Debug)]
pub struct Entry {
    pub min: f64,    // +0x28
    pub max: f64,    // +0x30
    pub center: f64, // +0x38
    pub curve: Curve, // +0x50
}

/// Entrada do parâmetro `i`, de [`crate::param_entries::ENTRIES`].
pub fn entry(i: usize) -> Entry {
    let (_, f, cb) = crate::param_entries::ENTRIES[i];
    Entry {
        min: f64::from_bits(f[0]),
        max: f64::from_bits(f[1]),
        center: f64::from_bits(f[2]),
        curve: Curve::from_rva(cb[1]).expect("callback +0x50 fora das 6 famílias"),
    }
}

/// `[rdx+0x50](rcx = e, xmm1 = x) -> xmm0`.
pub fn to_plain(e: &Entry, x: f64) -> f64 {
    match e.curve {
        Curve::Linear => {
            let span = e.max - e.min; // 00335218/0033521D
            let t = minsd(maxsd(sel01(x), 0.0), 1.0); // 0033522A/0033522E
            t * span + e.min // 00335232 mulsd / 00335236 addsd
        }
        Curve::Bool => {
            if x >= 0.5 { 1.0 } else { 0.0 } // 003358F0 comisd 0.5 ; jae
        }
        Curve::Int => {
            let lo = e.min.round() as i32; // 00335320 round / 00335326 cvttsd2si
            let hi = e.max.round() as i32; // 0033532F / 00335335
            let n = hi.wrapping_sub(lo); // 00335339
            if n <= 0 {
                return lo as f64; // 0033533F / 003353A1
            }
            let v = (n as f64 * sel01(x)).round(); // 0033537B..00335387
            ((v as i32).wrapping_add(lo)) as f64 // 0033538D..003353A1
        }
        Curve::LogOff150 => {
            let l0 = (e.min + 150.0).ln(); // 00335481..003354CE
            let l1 = (e.max + 150.0).ln(); // 003354D6..003354E3
            let d = l1 - l0; // 003354E8
            let t = minsd(maxsd(sel01(x), 0.0), 1.0); // 00335501/00335505
            (d * t + l0).exp() - 150.0 // 0033550A..00335517
        }
        Curve::LogSkew => {
            let lmin = e.min.ln(); // 003356CB
            let a = e.center.ln() - e.min.ln(); // 003356EA..003356FC
            let b = e.max.ln() - e.min.ln(); // 00335705..00335717
            let r = a / b; // 0033571B
            let s = r.ln() * -1.4426950408889634; // 00335722/00335727 [0x207A6C8]
            let p = minsd(maxsd(sel01(x).powf(s), 0.0), 1.0); // 00335736..00335748
            let span = e.max.ln() - lmin; // 0033574D/00335752
            (p * span + lmin).exp() // 00335757/0033575B ; 00335786 jmp exp
        }
        Curve::Log => {
            let l0 = e.min.ln(); // 00335886
            let d = e.max.ln() - l0; // 00335893/00335898
            let t = minsd(maxsd(sel01(x), 0.0), 1.0); // 003358B1/003358B5
            (d * t + l0).exp() // 003358BA/003358BE ; 003358E5 jmp exp
        }
    }
}

/// Valor que o setter `0x867D80` passa adiante: `(float)callback((double)norm)`
/// (`00867E00` / `00867E1A`). Aqui `norm` já está limitado pelo próprio setter
/// (`00867DC2`..`00867DF7`).
pub fn plain_f32(i: usize, norm: f32) -> f32 {
    to_plain(&entry(i), norm as f64) as f32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_entry_has_known_curve() {
        for i in 0..143 {
            let _ = entry(i);
        }
    }

    #[test]
    fn family_counts_match_dump() {
        let mut c = [0usize; 6];
        for i in 0..143 {
            c[entry(i).curve as usize] += 1;
        }
        // Linear 43, Bool 43, Int 35, LogOff150 8, LogSkew 8, Log 6
        assert_eq!(c, [43, 43, 35, 8, 8, 6]);
    }

    #[test]
    fn endpoints_and_center() {
        for i in 0..143 {
            let e = entry(i);
            match e.curve {
                Curve::Linear | Curve::Log | Curve::LogOff150 | Curve::LogSkew => {
                    let y0 = to_plain(&e, 0.0);
                    let y1 = to_plain(&e, 1.0);
                    assert!((y0 - e.min).abs() <= 1e-9 * e.min.abs().max(1.0), "i={i} y0={y0}");
                    assert!((y1 - e.max).abs() <= 1e-9 * e.max.abs().max(1.0), "i={i} y1={y1}");
                }
                _ => {}
            }
            if e.curve == Curve::LogSkew {
                let yc = to_plain(&e, 0.5);
                assert!((yc - e.center).abs() <= 1e-9 * e.center, "i={i} yc={yc}");
            }
        }
    }

    #[test]
    fn select_semantics() {
        assert_eq!(sel01(f64::NAN), 0.0);
        assert_eq!(sel01(-3.0), 0.0);
        assert_eq!(sel01(7.0), 1.0);
        assert_eq!(maxsd(-0.0, 0.0).to_bits(), 0.0f64.to_bits());
    }
}
