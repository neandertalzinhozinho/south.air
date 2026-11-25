//! Etapa M3 - confere `port/src/ippmath.rs` (transcrição de `0x293760` = ln e
//! `0x240C00` = exp da IPP) contra as **mesmas instruções AVX2/FMA** executadas
//! pelo hardware, bit a bit.
//!
//! Precedente: `checks/j_rcp_avx.rs` (M2). Não carrega o plugin, não executa código
//! do dump: o emulador abaixo é a sequência de `checks/293760.dis`,
//! `checks/293f80.dis`, `checks/240c00.dis` e `checks/2414c0.dis` reescrita com
//! intrinsics (RVA em cada linha). Constantes, máscaras e a tabela do ln são lidas
//! **do dump** em tempo de execução e comparadas com as do port.
//!
//! Veredito **estrito**: bits iguais em toda lane (inclusive NaN) e `eax` igual.
//! Inclui MXCSR do chamador alterado (FTZ+DAZ+RZ) e mutações de controle que
//! **têm** de ser detectadas.
//!
//! `rustc --edition 2021 -O -C target-feature=+fma checks/j_ln_exp_avx.rs -o checks/.build/j_ln_exp_avx.exe`
//! `checks/.build/j_ln_exp_avx.exe --exhaustive`  (2^32 entradas × 2 funções)

#![allow(dead_code)]
#![allow(deprecated)] // _mm_getcsr/_mm_setcsr = vstmxcsr/vldmxcsr

#[path = "../port/src/ippmath.rs"]
mod ippmath;

use std::arch::x86_64::*;
use std::io::{Read, Seek, SeekFrom};

fn dump_path() -> std::path::PathBuf {
    let here = std::path::Path::new(file!());
    let p = here.parent().unwrap().join("../dumpsooth/nyx_soothe3_dump.bin");
    if p.exists() {
        return p;
    }
    std::path::PathBuf::from(r"D:\PROJETOS\soultree FORK\dumpsooth\nyx_soothe3_dump.bin")
}

fn read_bytes(f: &mut std::fs::File, rva: u64, n: usize) -> Vec<u8> {
    f.seek(SeekFrom::Start(rva)).unwrap();
    let mut b = vec![0u8; n];
    f.read_exact(&mut b).unwrap();
    b
}

/// `.rdata` lido do dump: janelas cruas, endereçadas por RVA.
struct Mem {
    ln: Vec<u8>,  // 0x1ECA980 .. 0x1ECB610 (máscaras, consts, tabela, consts f64)
    ex: Vec<u8>,  // 0x1E6F940 .. 0x1E6FFE0
}
const LN_BASE: u64 = 0x1ECA980;
const EX_BASE: u64 = 0x1E6F940;

impl Mem {
    fn load() -> Mem {
        let mut f = std::fs::File::open(dump_path()).expect("dump");
        assert_eq!(f.metadata().unwrap().len(), 137_003_008, "tamanho do dump");
        Mem {
            ln: read_bytes(&mut f, LN_BASE, (0x1ECB610 - LN_BASE) as usize),
            ex: read_bytes(&mut f, EX_BASE, (0x1E6FFE0 - EX_BASE) as usize),
        }
    }
    fn lp(&self, rva: u64) -> *const u8 {
        self.ln[(rva - LN_BASE) as usize..].as_ptr()
    }
    fn ep(&self, rva: u64) -> *const u8 {
        self.ex[(rva - EX_BASE) as usize..].as_ptr()
    }
    fn lv(&self, rva: u64) -> __m256 {
        unsafe { _mm256_loadu_ps(self.lp(rva) as *const f32) }
    }
    fn ev(&self, rva: u64) -> __m256 {
        unsafe { _mm256_loadu_ps(self.ep(rva) as *const f32) }
    }
    fn lsd(&self, rva: u64) -> __m128d {
        unsafe { _mm_load_sd(self.lp(rva) as *const f64) }
    }
    fn ess(&self, rva: u64) -> __m128 {
        unsafe { _mm_load_ss(self.ep(rva) as *const f32) }
    }
    fn lu32(&self, rva: u64) -> u32 {
        unsafe { (self.lp(rva) as *const u32).read_unaligned() }
    }
    fn eu32(&self, rva: u64) -> u32 {
        unsafe { (self.ep(rva) as *const u32).read_unaligned() }
    }
}

#[derive(Clone, Copy, PartialEq)]
enum Mutation {
    None,
    /// lanes especiais ficam com o resultado vetorial (pula a chamada escalar)
    NoSpecial,
    /// último FMA da lane vetorial vira mul+add (dois arredondamentos)
    SplitFma,
}

#[inline(always)]
fn ci(v: __m256) -> __m256i {
    unsafe { _mm256_castps_si256(v) }
}
#[inline(always)]
fn cf(v: __m256i) -> __m256 {
    unsafe { _mm256_castsi256_ps(v) }
}

// ---------------------------------------------------------------- ln vetorial
/// Uma metade de 8 lanes do bloco de `0x293760` (`002938F3`..`002939CF`).
/// Devolve `(y, máscara especial)`.
#[target_feature(enable = "avx2,fma")]
unsafe fn ln8(m: &Mem, x: __m256, mu: Mutation) -> (__m256, i32) {
    unsafe {
        let c8 = ci(m.lv(0x1ECAD00));
        let c7 = ci(m.lv(0x1ECAD40));
        let c6 = ci(m.lv(0x1ECAD80));
        let c5 = ci(m.lv(0x1ECADC0));
        let c4 = m.lv(0x1ECAE00);
        let v9 = _mm256_add_epi32(ci(x), c8); // 002938F8 vpaddd
        let v14 = _mm256_sub_epi32(ci(x), c6); // 002938FD vpsubd
        let v10 = _mm256_and_si256(v14, c5); // 00293901 vpand
        let v15 = _mm256_srai_epi32(v14, 23); // 00293905 vpsrad
        let v14 = _mm256_add_epi32(v10, c6); // 0029390B vpaddd
        let v13 = _mm256_cmpgt_epi32(c7, v9); // 00293918 vpcmpgtd
        let e = _mm256_cvtepi32_ps(v15); // 0029392B vcvtdq2ps
        let fr = _mm256_sub_ps(cf(v14), c4); // 00293930 vsubps
        let msk = _mm256_movemask_ps(cf(v13)); // 0029394A vmovmskps
        let mut p = _mm256_fmadd_ps(m.lv(0x1ECACC0), fr, m.lv(0x1ECACA0)); // 00293957
        p = _mm256_fmadd_ps(p, fr, m.lv(0x1ECAC80)); // 00293961
        p = _mm256_fmadd_ps(p, fr, m.lv(0x1ECAC60)); // 00293973
        p = _mm256_fmadd_ps(p, fr, m.lv(0x1ECAC40)); // 00293985
        p = _mm256_fmadd_ps(p, fr, m.lv(0x1ECAC20)); // 00293997
        p = _mm256_fmadd_ps(p, fr, m.lv(0x1ECAC00)); // 002939A9
        let r = _mm256_mul_ps(fr, p); // 002939B3
        let r = if mu == Mutation::SplitFma {
            _mm256_add_ps(_mm256_mul_ps(r, fr), fr)
        } else {
            _mm256_fmadd_ps(r, fr, fr) // 002939BD
        };
        let ln2 = m.lv(0x1ECAE40);
        let y = _mm256_fmadd_ps(e, ln2, r); // 002939CF
        (y, msk)
    }
}

/// `0x293F80(rcx=&x, rdx=&y) -> eax` com SSE2/FMA escalar.
#[target_feature(enable = "avx2,fma")]
unsafe fn emu_293f80(m: &Mem, x: f32) -> (f32, i32) {
    unsafe {
        let b = x.to_bits();
        if (b >> 16) & 0x7f80 == 0x7f80 {
            // 002941D2
            if (b >> 24) & 0x80 == 0x80 && b & 0x7fffff == 0 {
                let z = m.lsd(0x1ECB5A8); // 002941F9
                let q = _mm_div_sd(z, z); // 00294206
                return (_mm_cvtss_f32(_mm_cvtsd_ss(_mm_setzero_ps(), q)), 0x13);
            }
            let v = _mm_set_ss(x);
            return (_mm_cvtss_f32(_mm_mul_ss(v, v)), 0); // 002941E3
        }
        let mut x2 = _mm_cvtss_sd(_mm_setzero_pd(), _mm_set_ss(x)); // 00293FA9
        let mut r8: i32 = 0;
        if (_mm_cvtsd_f64(x2).to_bits() >> 48) as u32 & 0x7ff0 == 0 {
            x2 = _mm_mul_sd(x2, m.lsd(0x1ECB5A0)); // 00293FC1
            r8 = -60; // 00293FC9
        }
        let x3 = m.lsd(0x1ECB5A8);
        if _mm_comigt_sd(x2, x3) == 0 {
            // 0029418E vucomisd ; jp ; je
            if _mm_ucomieq_sd(x2, x3) == 1 {
                let one = m.lsd(0x1ECB5B0);
                let sgn = _mm_loadu_pd(m.lp(0x1ECB5F0) as *const f64);
                let n1 = _mm_xor_pd(one, sgn); // 002941B9
                let q = _mm_div_sd(n1, x3); // 002941C1
                return (_mm_cvtss_f32(_mm_cvtsd_ss(_mm_setzero_ps(), q)), 0x12);
            }
            let q = _mm_div_sd(x3, x3); // 00294196
            return (_mm_cvtss_f32(_mm_cvtsd_ss(_mm_setzero_ps(), q)), 0x13);
        }
        let x1 = m.lsd(0x1ECB600); // 00293FE7
        let z = _mm_sub_sd(x2, x1); // 00293FEF
        let az = f64::from_bits(_mm_cvtsd_f64(z).to_bits() & 0x7fff_ffff_ffff_ffff); // 00293FF9
        if _mm_comigt_sd(_mm_set_sd(az), m.lsd(0x1ECB598)) == 0 {
            // 0029413A
            let mut p = _mm_fmadd_sd(m.lsd(0x1ECB5E8), z, m.lsd(0x1ECB5E0));
            let z2 = _mm_mul_sd(z, z); // 0029414B
            p = _mm_fmadd_sd(p, z, m.lsd(0x1ECB5D8));
            p = _mm_fmadd_sd(p, z, m.lsd(0x1ECB5D0));
            p = _mm_fmadd_sd(p, z, m.lsd(0x1ECB5C8));
            p = _mm_fmadd_sd(p, z, m.lsd(0x1ECB5C0));
            p = _mm_fmadd_sd(p, z, m.lsd(0x1ECB5B8));
            p = _mm_fmadd_sd(p, z2, z); // 0029417C
            return (_mm_cvtss_f32(_mm_cvtsd_ss(_mm_setzero_ps(), p)), 0);
        }
        let t = _mm_cvtsd_f64(x2).to_bits();
        let r9 = (((t >> 48) as u32 & 0xffff_800f) + 0x3ff0) & 0xffff; // 0029401C..0029402E
        let mb = (t & 0x0000_ffff_ffff_ffff) | ((r9 as u64) << 48); // 00294035
        let ecx = (((t >> 48) as u32) & 0x7ff0) >> 4; // 00294029..00294041
        let e = r8 + ecx as i32 - 0x3ff; // 00294060
        let x0 = _mm_cvtsi32_sd(_mm_setzero_pd(), e); // 00294068
        let x2 = _mm_set_sd(f64::from_bits(mb));
        let x5 = m.lsd(0x1ECB580);
        let x4 = _mm_add_sd(x2, m.lsd(0x1ECB588)); // 00294052
        let r10 = (_mm_cvtsd_f64(x4).to_bits() as u32) & 0x7f; // 0029406D/00294079
        let tb = 0x1ECAF60 + 24 * r10 as u64; // r11 = 3*r10, ·8
        let x4 = _mm_fmadd_sd(m.lsd(0x1ECB578), x0, m.lsd(tb + 8)); // 0029408F
        let x0 = _mm_fmadd_sd(x0, x5, m.lsd(tb + 0x10)); // 00294099
        let x3 = m.lsd(tb); // 002940A3
        let s = m.lsd(0x1ECB590);
        let x5 = _mm_sub_sd(_mm_add_sd(x2, s), s); // 002940AD..002940C1
        let x2 = _mm_sub_sd(x2, x5); // 002940C9
        let x5 = _mm_fmsub_sd(x5, x3, x1); // 002940CD
        let x3 = _mm_mul_sd(x3, x2); // 002940D2
        let x4 = _mm_add_sd(x4, x5); // 002940D6
        let x1 = _mm_add_sd(x5, x3); // 002940E2
        let x0 = _mm_add_sd(x3, x0); // 002940E6
        let mut p = _mm_fmadd_sd(m.lsd(0x1ECB5E8), x1, m.lsd(0x1ECB5E0)); // 002940EA
        p = _mm_fmadd_sd(p, x1, m.lsd(0x1ECB5D8));
        p = _mm_fmadd_sd(p, x1, m.lsd(0x1ECB5D0));
        p = _mm_fmadd_sd(p, x1, m.lsd(0x1ECB5C8));
        p = _mm_fmadd_sd(p, x1, m.lsd(0x1ECB5C0));
        p = _mm_fmadd_sd(p, x1, m.lsd(0x1ECB5B8)); // 00294117
        let x1 = _mm_mul_sd(x1, x1); // 00294120
        let p = _mm_fmadd_sd(p, x1, x0); // 00294124
        let y = _mm_add_sd(x4, p); // 00294129
        (_mm_cvtss_f32(_mm_cvtsd_ss(_mm_setzero_ps(), y)), 0) // 0029412D
    }
}

// --------------------------------------------------------------- exp vetorial
/// 8 lanes de `0x240C00` (`00240D96`..`00240F0D`; cauda `0024102E`..`00241078`).
#[target_feature(enable = "avx2,fma")]
unsafe fn exp8(m: &Mem, x: __m256, mu: Mutation) -> (__m256, i32) {
    unsafe {
        let sh = m.ev(0x1E6FC00);
        let t = _mm256_fmadd_ps(m.ev(0x1E6FBC0), x, sh); // 00240D96
        let k = _mm256_sub_ps(t, sh); // 00240DAA
        let a = _mm256_and_ps(x, m.ev(0x1E6FE80)); // 00240DCA
        let sp = _mm256_cmpgt_epi32(ci(a), ci(m.ev(0x1E6FEC0))); // 00240DD3
        let msk = _mm256_movemask_ps(cf(sp)); // 00240DD7
        let ti = _mm256_slli_epi32(ci(t), 23); // 00240DE0
        let r = _mm256_fnmadd_ps(m.ev(0x1E6FC40), k, x); // 00240E2B
        let r = _mm256_fnmadd_ps(k, m.ev(0x1E6FC80), r); // 00240E4F
        let mut p = _mm256_fmadd_ps(m.ev(0x1E6FE40), r, m.ev(0x1E6FE00)); // 00240E75
        p = _mm256_fmadd_ps(p, r, m.ev(0x1E6FDC0)); // 00240E91
        p = _mm256_fmadd_ps(p, r, m.ev(0x1E6FD80)); // 00240EAD
        p = _mm256_fmadd_ps(p, r, m.ev(0x1E6FD40)); // 00240EC9
        p = if mu == Mutation::SplitFma {
            _mm256_add_ps(_mm256_mul_ps(p, r), m.ev(0x1E6FD00))
        } else {
            _mm256_fmadd_ps(p, r, m.ev(0x1E6FD00)) // 00240EE5
        };
        (cf(_mm256_add_epi32(ti, ci(p))), msk) // 00240F00 vpaddd
    }
}

/// `0x2414C0(rcx=&x, rdx=&y) -> eax` com SSE/FMA escalar.
#[target_feature(enable = "avx2,fma")]
unsafe fn emu_2414c0(m: &Mem, x: f32) -> (f32, i32) {
    unsafe {
        let b = x.to_bits();
        if (b >> 16) & 0x7f80 == 0x7f80 {
            if (b >> 24) & 0x80 == 0x80 && b & 0x7fffff == 0 {
                return (f32::from_bits(0), 0); // 002416FB mov [rdx],eax (=0)
            }
            let v = _mm_set_ss(x);
            return (_mm_cvtss_f32(_mm_mul_ss(v, v)), 0); // 002416E5
        }
        let x0 = _mm_set_ss(x);
        if _mm_comilt_ss(m.ess(0x1E6FFA0), x0) == 1 {
            // 002414F3 jb
            let fm = m.ess(0x1E6FFA8);
            return (_mm_cvtss_f32(_mm_mul_ss(fm, fm)), 0xc); // 002416BA
        }
        if _mm_comilt_ss(x0, m.ess(0x1E6FFA4)) == 1 {
            let tn = m.ess(0x1E6FFD4);
            return (_mm_cvtss_f32(_mm_mul_ss(tn, tn)), 0x11); // 00241698
        }
        let below = _mm_comilt_ss(x0, m.ess(0x1E6FFD0)) == 1; // 00241513 / 002415AE
        let x1 = _mm_mul_ss(x0, m.ess(0x1E6FFAC)); // 0024150B
        let x5 = m.ess(0x1E6FFB0);
        let x3 = _mm_add_ss(x1, x5); // 0024152F
        let r8 = (_mm_cvtss_f32(x3).to_bits() as u16) as i16 as i32; // 0024153F movsx
        let kf = _mm_sub_ss(x3, x5); // 00241545
        let x4 = _mm_mul_ss(kf, m.ess(0x1E6FFB4)); // 00241555
        let x1 = _mm_sub_ss(x0, x4); // 00241563
        let x2 = _mm_mul_ss(kf, m.ess(0x1E6FFB8)); // 00241567
        let r = _mm_sub_ss(x1, x2); // 00241577
        let one = m.ess(0x1E6FFBC);
        let mut p = _mm_fmadd_ss(m.ess(0x1E6FFC0), r, m.ess(0x1E6FFC4)); // 00241583
        p = _mm_fmadd_ss(p, r, m.ess(0x1E6FFC8)); // 0024158C
        p = _mm_fmadd_ss(p, r, m.ess(0x1E6FFCC)); // 00241595
        p = _mm_fmadd_ss(p, r, one); // 0024159E
        p = _mm_fmadd_ss(p, r, one); // 002415A3
        // dword [rsp+0x2C]: low word 0 (002414EF), high word escrito abaixo
        let sc = |e8: u32| _mm_castsi128_ps(_mm_cvtsi32_si128(((e8 & 0xff) << 23) as i32));
        if below {
            // 0024163C..00241677
            let y = _mm_mul_ss(_mm_mul_ss(p, sc((r8 - 0x45) as u32)), m.ess(0x1E6FFD8));
            return (_mm_cvtss_f32(y), 0x11);
        }
        let ecx = (r8 + 0x7f) as u32; // 002415B4
        if ecx <= 0xfe {
            return (_mm_cvtss_f32(_mm_mul_ss(p, sc(ecx))), 0); // 002415D1
        }
        let y = _mm_mul_ss(_mm_mul_ss(p, sc((r8 + 0x7e) as u32)), m.ess(0x1E6FFDC)); // 0024160F/00241621
        (_mm_cvtss_f32(y), 0)
    }
}

// ------------------------------------------------- função inteira (ln ou exp)
#[derive(Clone, Copy, PartialEq)]
enum Fun {
    Ln,
    Exp,
}

/// `0x293760` / `0x240C00` (`src`, `dst`, `n`) — despacho por bloco
/// (ln: 16; exp: 32), cauda de 8 com máscaras do dump e padding `0.75`,
/// lanes especiais em ordem crescente, MXCSR forçado/restaurado.
#[target_feature(enable = "avx2,fma,bmi2,popcnt")]
unsafe fn emu(m: &Mem, fun: Fun, src: *const f32, dst: *mut f32, n: i32, mu: Mutation) -> i32 {
    unsafe {
        if n <= 0 {
            return 0xFFFF_FFFAu32 as i32;
        }
        if src.is_null() || dst.is_null() {
            return 0xFFFF_FFF8u32 as i32;
        }
        // 00293852..0029388A / 00240CF5..00240D2D
        let saved = _mm_getcsr();
        let changed = saved & 0xffc0 != 0x1f80;
        if changed {
            _mm_setcsr((saved & 0xffff_003f) + 0x1f80);
        }
        let (blk, padrva, ldm, stm) = match fun {
            Fun::Ln => (16usize, 0x1ECAF40u64, 0x1ECA980u64, 0x1ECAAC0u64),
            Fun::Exp => (32usize, 0x1E6FF80u64, 0x1E6F940u64, 0x1E6FA80u64),
        };
        let vec8 = |x: __m256| -> (__m256, i32) {
            match fun {
                Fun::Ln => ln8(m, x, mu),
                Fun::Exp => exp8(m, x, mu),
            }
        };
        let scal = |p: *const f32| -> (f32, i32) {
            match fun {
                Fun::Ln => emu_293f80(m, *p),
                Fun::Exp => emu_2414c0(m, *p),
            }
        };
        let mp = |rva: u64| match fun {
            Fun::Ln => m.lp(rva),
            Fun::Exp => m.ep(rva),
        };
        let n = n as usize;
        let mut st: i32 = 0;
        let full = n & !(blk - 1);
        let mut i = 0usize;
        while i < full {
            // bloco inteiro: calcula todas as metades, depois refaz as especiais
            let mut ys = [_mm256_setzero_ps(); 4];
            let mut mask: u32 = 0;
            for h in 0..blk / 8 {
                let (y, k) = vec8(_mm256_loadu_ps(src.add(i + 8 * h)));
                ys[h] = y;
                mask |= (k as u32) << (8 * h);
            }
            let mut tmp = [0.0f32; 32];
            for h in 0..blk / 8 {
                _mm256_storeu_ps(tmp.as_mut_ptr().add(8 * h), ys[h]);
            }
            if mu != Mutation::NoSpecial {
                for l in 0..blk {
                    if mask >> l & 1 == 1 {
                        let (y, s) = scal(src.add(i + l));
                        tmp[l] = y;
                        if s != 0 {
                            st = s; // 0x2D74A0 = ret
                        }
                    }
                }
            }
            std::ptr::copy_nonoverlapping(tmp.as_ptr(), dst.add(i), blk);
            i += blk;
        }
        while i < n {
            let cnt = (n - i).min(8);
            let lm = _mm256_loadu_ps(mp(ldm + 32 * cnt as u64) as *const f32);
            let xm = _mm256_maskload_ps(src.add(i), ci(lm)); // vmaskmovps
            let pad = _mm256_loadu_ps(mp(padrva) as *const f32);
            let x = _mm256_blendv_ps(pad, xm, lm); // vblendvps
            let (y, k) = vec8(x);
            let mut tmp = [0.0f32; 8];
            _mm256_storeu_ps(tmp.as_mut_ptr(), y);
            if mu != Mutation::NoSpecial {
                for l in 0..8 {
                    if (k as u32) >> l & 1 == 1 {
                        let xv = [x; 1];
                        let xs = &*(xv.as_ptr() as *const [f32; 8]);
                        let (yv, s) = scal(&xs[l] as *const f32);
                        tmp[l] = yv;
                        if s != 0 {
                            st = s;
                        }
                    }
                }
            }
            let sm = _mm256_loadu_ps(mp(stm + 32 * cnt as u64) as *const f32);
            _mm256_maskstore_ps(dst.add(i), ci(sm), _mm256_loadu_ps(tmp.as_ptr()));
            i += 8;
        }
        // 00293B4C.. / 002410A1..
        if changed {
            _mm_setcsr(saved);
        } else {
            let c = _mm_getcsr();
            if c & 0x1f != 0 {
                _mm_setcsr(c & 0xffff_ffe0);
            }
        }
        st
    }
}

// -------------------------------------------------------------------- testes
fn check_consts(m: &Mem) {
    // máscaras 0..8 (ld e st) de ln e exp
    for (base, getter) in [(0x1ECA980u64, 0), (0x1ECAAC0, 0), (0x1E6F940, 1), (0x1E6FA80, 1)] {
        for cnt in 0..9u64 {
            for l in 0..8u64 {
                let rva = base + 32 * cnt + 4 * l;
                let v = if getter == 0 { m.lu32(rva) } else { m.eu32(rva) };
                assert_eq!(v, if l < cnt { 0xffff_ffff } else { 0 }, "mascara {rva:#x}");
            }
        }
    }
    // spot-check de constantes do port contra o dump
    assert_eq!(m.lu32(0x1ECAE40), 0x3F31_7218);
    assert_eq!(m.lu32(0x1ECAD80), 0x3F2A_AAAB);
    assert_eq!(m.lu32(0x1ECAF40), 0x3F40_0000);
    assert_eq!(m.eu32(0x1E6FBC0), 0x3FB8_AA3B);
    assert_eq!(m.eu32(0x1E6FEC0), 0x42AE_AC4F);
    assert_eq!(m.eu32(0x1E6FF80), 0x3F40_0000);
    assert_eq!(m.eu32(0x1E6FFBC), 0x3F80_0001);
    // despacho: [0x21C7408]=4 ; 0x21C6AA8[4] / 0x21C6A28[4] ; [0x21C70E8] / [0x21C6F08]
    let mut f = std::fs::File::open(dump_path()).unwrap();
    let q = |f: &mut std::fs::File, rva| u64::from_le_bytes(read_bytes(f, rva, 8).try_into().unwrap());
    assert_eq!(q(&mut f, 0x21C7408) as u32, 4, "ippJumpIndex");
    assert_eq!(q(&mut f, 0x21C6AA8 + 32), 0x199B_0000 + 0x1C8A00, "0x21C6AA8[4]");
    assert_eq!(q(&mut f, 0x21C70E8), 0x199B_0000 + 0x293760, "[0x21C70E8]");
    assert_eq!(q(&mut f, 0x21C6A28 + 32), 0x199B_0000 + 0x1C8880, "0x21C6A28[4]");
    assert_eq!(q(&mut f, 0x21C6F08), 0x199B_0000 + 0x240C00, "[0x21C6F08]");
}

fn lcg(s: &mut u64) -> u64 {
    *s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    *s
}

const SPECIAL: [u32; 26] = [
    0x0000_0000, 0x8000_0000, 0x0000_0001, 0x007f_ffff, 0x8000_0001, 0x0080_0000,
    0x3f80_0000, 0xbf80_0000, 0x3f2a_aaab, 0x3f2a_aaaa, 0x3f80_0001, 0x3f7f_ffff,
    0x7f7f_ffff, 0x7f80_0000, 0xff80_0000, 0x7fc0_0000, 0xffc0_0000, 0x7fa0_0001,
    0x42ae_ac4f, 0x42ae_ac50, 0xc2ae_ac50, 0x42b1_7217, 0x42b1_7218, 0xc2cf_f1b4,
    0xc2cf_f1b5, 0xc2b0_0000,
];

fn val(s: &mut u64, kind: u32) -> f32 {
    let r = lcg(s);
    match kind {
        0 => f32::from_bits((r >> 32) as u32),
        1 => f32::from_bits(SPECIAL[((r >> 32) as usize) % SPECIAL.len()]),
        _ => ((r >> 40) as f32 / (1u64 << 24) as f32 - 0.5) * 220.0, // [-110, 110]
    }
}

fn port_call(fun: Fun, x: &[f32], y: &mut [f32]) -> i32 {
    match fun {
        Fun::Ln => ippmath::ln_32f(x, y),
        Fun::Exp => ippmath::exp_32f(x, y),
    }
}

fn compare(m: &Mem, fun: Fun, x: &[f32], mu: Mutation, csr: Option<u32>) -> (usize, bool) {
    let n = x.len();
    let mut hw = vec![0.0f32; n];
    let mut po = vec![0.0f32; n];
    let saved = unsafe { _mm_getcsr() };
    if let Some(v) = csr {
        unsafe { _mm_setcsr(v) };
    }
    let sh = unsafe { emu(m, fun, x.as_ptr(), hw.as_mut_ptr(), n as i32, mu) };
    let after = unsafe { _mm_getcsr() };
    unsafe { _mm_setcsr(saved) };
    let sp = port_call(fun, x, &mut po);
    let csr_ok = csr.map_or(true, |v| after & 0xffc0 == v & 0xffc0);
    let mut bad = (0..n).filter(|&i| hw[i].to_bits() != po[i].to_bits()).count();
    if sh != sp {
        bad += 1;
    }
    (bad, csr_ok)
}

fn run() {
    assert!(
        is_x86_feature_detected!("avx2") && is_x86_feature_detected!("fma")
            && is_x86_feature_detected!("bmi2") && is_x86_feature_detected!("popcnt"),
        "precisa de AVX2/FMA/BMI2/POPCNT"
    );
    let m = Mem::load();
    check_consts(&m);
    let host_csr = 0x1f80 | 0x8000 | 0x0040 | 0x6000; // FTZ + DAZ + RZ
    let mut seed = 0x0029_3760_0024_0c00u64;
    let mut ns: Vec<usize> = (1..=70).collect();
    ns.extend_from_slice(&[255, 256, 257, 513]);
    for fun in [Fun::Ln, Fun::Exp] {
        let (mut lanes, mut bad, mut csr_bad, mut m_sp, mut m_fma) = (0usize, 0usize, 0usize, 0usize, 0usize);
        for &n in &ns {
            for round in 0..9u32 {
                let kind = round % 3;
                let x: Vec<f32> = (0..n).map(|_| val(&mut seed, kind)).collect();
                let csr = if round == 4 { Some(host_csr) } else { None };
                let (b, ok) = compare(&m, fun, &x, Mutation::None, csr);
                bad += b;
                lanes += n;
                if !ok {
                    csr_bad += 1;
                }
                if kind == 1 {
                    m_sp += compare(&m, fun, &x, Mutation::NoSpecial, None).0;
                }
                if kind == 2 {
                    m_fma += compare(&m, fun, &x, Mutation::SplitFma, None).0;
                }
            }
        }
        // diferença IEEE (informativa): IPP × f32::ln / f32::exp no mesmo lote
        let mut libm = 0usize;
        for _ in 0..200 {
            let x: Vec<f32> = (0..257).map(|_| val(&mut seed, 2).abs() + 1e-3).collect();
            let mut y = vec![0.0f32; 257];
            port_call(fun, &x, &mut y);
            for i in 0..257 {
                let r = if fun == Fun::Ln { x[i].ln() } else { (x[i] - 55.0).exp() };
                let yy = if fun == Fun::Ln { y[i] } else {
                    let mut z = [0.0f32]; port_call(fun, &[x[i] - 55.0], &mut z); z[0]
                };
                if yy.to_bits() != r.to_bits() {
                    libm += 1;
                }
            }
        }
        let name = if fun == Fun::Ln { "ln 0x293760" } else { "exp 0x240C00" };
        println!(
            "{name}: lanes={lanes} bad={bad} mxcsr_nao_restaurado={csr_bad} | mutacoes: \
             sem_especial={m_sp} fma_partido={m_fma} | difere_de_f32::libm={libm}/51400"
        );
        assert_eq!(bad, 0, "{name}: ippmath.rs divergiu do hardware AVX2/FMA");
        assert_eq!(csr_bad, 0);
        assert!(m_sp > 0, "{name}: mutação sem especial não detectada");
        assert!(m_fma > 0, "{name}: mutação FMA partido não detectada");
    }
}

fn exhaustive() {
    let m = Mem::load();
    check_consts(&m);
    const CH: usize = 4096;
    let mut x = vec![0.0f32; CH];
    let mut hw = vec![0.0f32; CH];
    let mut po = vec![0.0f32; CH];
    for fun in [Fun::Ln, Fun::Exp] {
        let (mut bad, mut nan, mut libm) = (0u64, 0u64, 0u64);
        let mut first = Vec::new();
        for chunk in 0..(1u64 << 32) / CH as u64 {
            let base = chunk * CH as u64;
            for i in 0..CH {
                x[i] = f32::from_bits((base + i as u64) as u32);
            }
            let sh = unsafe { emu(&m, fun, x.as_ptr(), hw.as_mut_ptr(), CH as i32, Mutation::None) };
            let sp = port_call(fun, &x, &mut po);
            if sh != sp {
                bad += 1;
            }
            for i in 0..CH {
                if hw[i].is_nan() {
                    nan += 1;
                }
                let r = if fun == Fun::Ln { x[i].ln() } else { x[i].exp() };
                if r.to_bits() != hw[i].to_bits() && !(r.is_nan() && hw[i].is_nan()) {
                    libm += 1;
                }
                if hw[i].to_bits() != po[i].to_bits() {
                    bad += 1;
                    if first.len() < 10 {
                        first.push((x[i].to_bits(), hw[i].to_bits(), po[i].to_bits()));
                    }
                }
            }
        }
        for (a, h, p) in &first {
            println!("DIFF x={a:08x} hw={h:08x} port={p:08x}");
        }
        let name = if fun == Fun::Ln { "ln" } else { "exp" };
        println!("EXAUSTIVO {name}: 2^32 entradas, bad={bad}, NaN={nan}, difere_de_libm={libm}");
        assert_eq!(bad, 0);
    }
}

fn main() {
    if std::env::args().any(|a| a == "--exhaustive") {
        exhaustive();
    } else {
        run();
    }
}

#[test]
fn ln_exp_rs_match_avx_fma_hardware() {
    run();
}
