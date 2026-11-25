//! Etapa M2 - confere `port/src/rcp.rs` (transcrição de `0x29B260`) contra as
//! **mesmas instruções AVX2/FMA** executadas pelo hardware, bit a bit.
//!
//! Precedente: `checks/j_div_avx.rs` (M1). Não carrega o plugin, não executa código
//! do dump: o emulador abaixo é a sequência de `checks/29b260.dis` e
//! `checks/29b9a0.dis` reescrita com intrinsics, instrução por instrução (RVA em cada
//! linha), sobre ponteiros reais. As constantes e as tabelas de máscara são lidas
//! **do dump** (`dumpsooth/nyx_soothe3_dump.bin`, offset de arquivo = RVA) em tempo de
//! execução, e comparadas com as constantes do port.
//!
//! Veredito **estrito**: bits iguais em toda lane (inclusive NaN: sinal e payload) e
//! `eax` igual. Inclui MXCSR do chamador alterado (FTZ+DAZ+RZ) e três mutações de
//! controle que **têm** de ser detectadas.
//!
//! Compilar e rodar:
//! `rustc --edition 2021 -O checks/j_rcp_avx.rs -o checks/.build/j_rcp_avx.exe`
//! `checks/.build/j_rcp_avx.exe --exhaustive`  (todas as 2^32 entradas; fora do runner)
//! (`--test`: o mesmo conteúdo roda como `rcp_rs_matches_avx_fma_hardware`).

#![allow(dead_code)]
#![allow(deprecated)] // _mm_getcsr/_mm_setcsr: é exatamente vstmxcsr/vldmxcsr

#[path = "../port/src/rcp.rs"]
mod rcp;

use std::arch::x86_64::*;
use std::io::{Read, Seek, SeekFrom};

/// Constantes de `.rdata` lidas do dump.
struct Consts {
    sub: [u32; 8],     // 0x1ED0500
    abs: [u32; 8],     // 0x1ED04C0
    lim: [u32; 8],     // 0x1ED0540
    one: [u32; 8],     // 0x1ED05C0
    pad: [u32; 8],     // 0x1ED0600
    one_s: u32,        // 0x1ED0620
    ld_mask: [[u32; 8]; 9], // 0x1ED0240 + 32*cnt
    st_mask: [[u32; 8]; 9], // 0x1ED0380 + 32*cnt
}

fn dump_path() -> std::path::PathBuf {
    let here = std::path::Path::new(file!());
    let p = here.parent().unwrap().join("../dumpsooth/nyx_soothe3_dump.bin");
    if p.exists() {
        return p;
    }
    std::path::PathBuf::from(r"D:\PROJETOS\soultree FORK\dumpsooth\nyx_soothe3_dump.bin")
}

fn read_u32s(f: &mut std::fs::File, rva: u64, n: usize) -> Vec<u32> {
    f.seek(SeekFrom::Start(rva)).unwrap();
    let mut b = vec![0u8; 4 * n];
    f.read_exact(&mut b).unwrap();
    b.chunks(4).map(|c| u32::from_le_bytes([c[0], c[1], c[2], c[3]])).collect()
}

fn load_consts() -> Consts {
    let p = dump_path();
    let mut f = std::fs::File::open(&p).expect("dump");
    assert_eq!(f.metadata().unwrap().len(), 137_003_008, "tamanho do dump");
    let v8 = |f: &mut std::fs::File, rva| -> [u32; 8] { read_u32s(f, rva, 8).try_into().unwrap() };
    let mut ld_mask = [[0u32; 8]; 9];
    let mut st_mask = [[0u32; 8]; 9];
    for c in 0..9 {
        ld_mask[c] = v8(&mut f, 0x1ED0240 + 32 * c as u64);
        st_mask[c] = v8(&mut f, 0x1ED0380 + 32 * c as u64);
    }
    Consts {
        sub: v8(&mut f, 0x1ED0500),
        abs: v8(&mut f, 0x1ED04C0),
        lim: v8(&mut f, 0x1ED0540),
        one: v8(&mut f, 0x1ED05C0),
        pad: v8(&mut f, 0x1ED0600),
        one_s: read_u32s(&mut f, 0x1ED0620, 1)[0],
        ld_mask,
        st_mask,
        // tabela de despacho (conferida em run())
    }
}

#[derive(Clone, Copy, PartialEq)]
enum Mutation {
    None,
    /// lanes especiais ficam com o resultado vrcpps+FMA (pula 0029B7AC/0029B67B)
    NoSpecial,
    /// não força o MXCSR (pula 0029B375..0029B38D)
    NoMxcsr,
}

/// `0x29B9A0(rcx = &x, rdx = &r)` (`0029B9A0`..`0029B9C4`).
#[target_feature(enable = "avx")]
unsafe fn emu_29b9a0(rcx: *const f32, rdx: *mut f32, one_s: u32) -> i32 {
    unsafe {
        let xmm2 = _mm_load_ss(rcx); // 0029B9A0
        let xmm3 = _mm_setzero_ps(); // 0029B9A4
        let xmm0 = _mm_castsi128_ps(_mm_cvtsi32_si128(one_s as i32)); // 0029B9A8
        let xmm4 = _mm_cmpeq_ss(xmm2, xmm3); // 0029B9B0
        let xmm1 = _mm_div_ss(xmm0, xmm2); // 0029B9B5
        let eax = _mm_cvtsi128_si32(_mm_castps_si128(xmm4)); // 0029B9B9
        _mm_store_ss(rdx, xmm1); // 0029B9BD
        eax & 0x12 // 0029B9C1
    }
}

#[inline]
unsafe fn ldv(a: &[u32; 8]) -> __m256i {
    unsafe { _mm256_loadu_si256(a.as_ptr() as *const __m256i) }
}

/// `0x29B260(rcx = src, rdx = dst, r8d = n)` com intrinsics.
#[target_feature(enable = "avx2,fma,bmi2,popcnt")]
unsafe fn emu_29b260(c: &Consts, r14: *const f32, r12: *mut f32, n: i32, m: Mutation) -> i32 {
    unsafe {
        let ebp = n as u32; // 0029B275
        let ebx = ebp & 0xffff_ffe0; // 0029B281/0029B28C
        let mut r15d: i32 = 0; // 0029B2B0
        if n <= 0 {
            return 0xffff_fffau32 as i32; // 0029B310 -> 0029B971
        }
        if r14.is_null() || r12.is_null() {
            return 0xffff_fff8u32 as i32; // 0029B319/0029B322 -> 0029B90B
        }
        // x87 0029B328..0029B34B: não há conta x87 no corpo; não emulado.
        let ecx = _mm_getcsr(); // 0029B355
        let mut dl2 = false;
        if (ecx & 0xffc0) != 0x1f80 && m != Mutation::NoMxcsr {
            _mm_setcsr((ecx & 0xffff_003f).wrapping_add(0x1f80)); // 0029B37A..0029B38D
            dl2 = true; // 0029B377 add dl,2
        }
        let mut eax: u32 = 0; // 0029B396
        if ebx != 0 {
            let ymm3 = ldv(&c.sub); // 0029B3A0
            let ymm2 = ldv(&c.abs); // 0029B3A8
            let ymm1 = ldv(&c.lim); // 0029B3B0
            let ymm0 = _mm256_castsi256_ps(ldv(&c.one)); // 0029B3B8
            loop {
                let r8 = eax as usize; // 0029B3C0
                let ymm4 = _mm256_loadu_ps(r14.add(r8)); // 0029B3C3
                let ymm7 = _mm256_loadu_ps(r14.add(r8 + 8)); // 0029B3C9
                let ymm6 = _mm256_loadu_ps(r14.add(r8 + 16)); // 0029B3D0
                let ymm5 = _mm256_loadu_ps(r14.add(r8 + 24)); // 0029B3D7
                let s = |v: __m256| _mm256_and_si256(_mm256_sub_epi32(_mm256_castps_si256(v), ymm3), ymm2); // 0029B3DE..0029B3FA
                let g8 = _mm256_cmpgt_epi32(s(ymm4), ymm1); // 0029B3FE
                let g9 = _mm256_cmpgt_epi32(s(ymm7), ymm1); // 0029B402
                let g10 = _mm256_cmpgt_epi32(s(ymm6), ymm1); // 0029B406
                let g11 = _mm256_cmpgt_epi32(s(ymm5), ymm1); // 0029B40A
                let ymm12 = _mm256_rcp_ps(ymm4); // 0029B40E
                let ymm13 = _mm256_rcp_ps(ymm7); // 0029B412
                let ymm14 = _mm256_rcp_ps(ymm6); // 0029B416
                let ymm15 = _mm256_rcp_ps(ymm5); // 0029B41A
                let esi0 = _mm256_movemask_ps(_mm256_castsi256_ps(g8)) as u32; // 0029B41E
                let edi = _mm256_movemask_ps(_mm256_castsi256_ps(g9)) as u32; // 0029B423
                let r10d = _mm256_movemask_ps(_mm256_castsi256_ps(g10)) as u32; // 0029B428
                let r11d = _mm256_movemask_ps(_mm256_castsi256_ps(g11)) as u32; // 0029B42D
                let mut ymm8 = _mm256_fnmadd_ps(ymm4, ymm12, ymm0); // 0029B442 vfnmadd231ps
                let mut ymm9 = _mm256_fnmadd_ps(ymm7, ymm13, ymm0); // 0029B447
                let mut ymm10 = _mm256_fnmadd_ps(ymm6, ymm14, ymm0); // 0029B44C
                let mut ymm11 = _mm256_fnmadd_ps(ymm5, ymm15, ymm0); // 0029B451
                ymm8 = _mm256_fmadd_ps(ymm12, ymm8, ymm12); // 0029B456 vfmadd213ps ymm8,ymm12,ymm12
                ymm9 = _mm256_fmadd_ps(ymm13, ymm9, ymm13); // 0029B45B
                ymm10 = _mm256_fmadd_ps(ymm14, ymm10, ymm14); // 0029B460
                ymm11 = _mm256_fmadd_ps(ymm15, ymm11, ymm15); // 0029B465
                let esi = esi0 | (edi << 8) | (r10d << 16) | (r11d << 24); // 0029B46A..0029B47A
                if esi != 0 && m != Mutation::NoSpecial {
                    // 0029B7AC..0029B7E5: x em [r13+0xc0..], r em [r13+0x40..]
                    let mut xs = [0.0f32; 32];
                    let mut rs = [0.0f32; 32];
                    _mm256_storeu_ps(xs.as_mut_ptr(), ymm4);
                    _mm256_storeu_ps(xs.as_mut_ptr().add(8), ymm7);
                    _mm256_storeu_ps(xs.as_mut_ptr().add(16), ymm6);
                    _mm256_storeu_ps(xs.as_mut_ptr().add(24), ymm5);
                    _mm256_storeu_ps(rs.as_mut_ptr(), ymm8);
                    _mm256_storeu_ps(rs.as_mut_ptr().add(8), ymm9);
                    _mm256_storeu_ps(rs.as_mut_ptr().add(16), ymm10);
                    _mm256_storeu_ps(rs.as_mut_ptr().add(24), ymm11);
                    for e in 0..32u32 {
                        // 0029B820 bt esi,edi
                        if (esi >> e) & 1 != 0 {
                            let st = emu_29b9a0(xs.as_ptr().add(e as usize), rs.as_mut_ptr().add(e as usize), c.one_s); // 0029B899
                            if st != 0 {
                                let idx = (eax + e) as usize; // 0029B8A5
                                *r12.add(idx) = rs[e as usize]; // 0029B8AA
                                // 0029B8D3 call 0x2D74A0 = endbr64; ret
                                rs[e as usize] = *r12.add(idx); // 0029B8D8/0029B8E3
                                r15d = st; // 0029B8E0
                            }
                        }
                    }
                    ymm8 = _mm256_loadu_ps(rs.as_ptr()); // 0029B84E
                    ymm9 = _mm256_loadu_ps(rs.as_ptr().add(8)); // 0029B854
                    ymm10 = _mm256_loadu_ps(rs.as_ptr().add(16)); // 0029B85A
                    ymm11 = _mm256_loadu_ps(rs.as_ptr().add(24)); // 0029B863
                }
                eax += 0x20; // 0029B483
                _mm256_storeu_ps(r12.add(r8), ymm8); // 0029B486
                _mm256_storeu_ps(r12.add(r8 + 8), ymm9); // 0029B48E
                _mm256_storeu_ps(r12.add(r8 + 16), ymm10); // 0029B495
                _mm256_storeu_ps(r12.add(r8 + 24), ymm11); // 0029B49C
                if eax >= ebx {
                    break; // 0029B48C/0029B4A3 jb
                }
            }
        }
        // Cauda 0029B4A9..0029B586
        if eax < ebp {
            let mut r8d: i32 = -(eax as i32); // 0029B4A9/0029B4AC
            let ymm4 = ldv(&c.sub); // 0029B4B7
            let r9: u64 = 0xffff_ffff; // 0029B4BF
            let ymm3 = ldv(&c.abs); // 0029B4C9
            let ymm2 = ldv(&c.lim); // 0029B4D1
            let ymm1 = _mm256_castsi256_ps(ldv(&c.one)); // 0029B4D9
            let ymm0 = _mm256_castsi256_ps(ldv(&c.pad)); // 0029B4E1
            loop {
                let edi = eax as usize; // 0029B500
                let mut b = (ebp as i32).wrapping_add(r8d) as u32; // 0029B502
                if b >= 8 {
                    b = 8; // 0029B507/0029B50A cmovae
                }
                let shift = (0x20u32.wrapping_sub(b)) as u64; // 0029B50E/0029B510
                // 0029B513 shrx rsi,r9,rbx: r9 >> (rbx & 63) (sem intrinsic em Rust)
                let esi_mask = ((r9 >> (shift & 63)) & 0xffff_ffff) as u32;
                let r13_0 = esi_mask; // 0029B518 mov [r13],esi
                let mut rbx = (_popcnt32((esi_mask & 0xff) as i32) as usize) * 32; // 0029B51E..0029B528
                let ymm6m = ldv(&c.ld_mask[rbx / 32]); // 0029B52C
                let ymm5 = _mm256_maskload_ps(r14.add(edi), ymm6m); // 0029B536
                let ymm5 = _mm256_blendv_ps(ymm0, ymm5, _mm256_castsi256_ps(ymm6m)); // 0029B53C
                let ymm10 = _mm256_rcp_ps(ymm5); // 0029B542
                let ymm7 = _mm256_sub_epi32(_mm256_castps_si256(ymm5), ymm4); // 0029B546
                let ymm8 = _mm256_and_si256(ymm7, ymm3); // 0029B54A
                let mut ymm6 = _mm256_fnmadd_ps(ymm10, ymm5, ymm1); // 0029B54E/0029B552 vfnmadd231ps ymm6,ymm10,ymm5
                ymm6 = _mm256_fmadd_ps(ymm10, ymm6, ymm10); // 0029B557 vfmadd213ps ymm6,ymm10,ymm10
                let ymm9 = _mm256_cmpgt_epi32(ymm8, ymm2); // 0029B55C
                let esi = _mm256_movemask_ps(_mm256_castsi256_ps(ymm9)) as u32; // 0029B560
                if esi != 0 && m != Mutation::NoSpecial {
                    // 0029B67B..0029B73B
                    let mut xs = [0.0f32; 8];
                    let mut rs = [0.0f32; 8];
                    _mm256_storeu_ps(xs.as_mut_ptr(), ymm5); // 0029B67B
                    _mm256_storeu_ps(rs.as_mut_ptr(), ymm6); // 0029B684
                    for k in 0..8u32 {
                        if (esi >> k) & 1 != 0 {
                            // 0029B6C0 bt esi,ebx
                            let st = emu_29b9a0(xs.as_ptr().add(k as usize), rs.as_mut_ptr().add(k as usize), c.one_s); // 0029B756
                            if st != 0 {
                                let idx = (eax + k) as usize; // 0029B766
                                *r12.add(idx) = rs[k as usize]; // 0029B76B
                                // 0029B794 call 0x2D74A0 = ret
                                rs[k as usize] = *r12.add(idx); // 0029B799/0029B7A4
                                r15d = st; // 0029B7A1
                            }
                        }
                    }
                    rbx = (_popcnt32((r13_0 & 0xff) as i32) as usize) * 32; // 0029B6CC..0029B737
                    ymm6 = _mm256_loadu_ps(rs.as_ptr()); // 0029B6E9
                }
                let ymm5s = ldv(&c.st_mask[rbx / 32]); // 0029B56D
                eax += 8; // 0029B577
                r8d -= 8; // 0029B57A
                _mm256_maskstore_ps(r12.add(edi), ymm5s, ymm6); // 0029B57E
                if eax >= ebp {
                    break; // 0029B584/0029B586 jb
                }
            }
        }
        // 0029B58C fnclex (x87); MXCSR 0029B59A..0029B5D0
        if dl2 {
            _mm_setcsr(ecx); // 0029B59F/0029B5A6
        } else {
            let edx = _mm_getcsr(); // 0029B5B1
            if edx & 0x1f != 0 {
                _mm_setcsr(edx & 0xffff_ffe0); // 0029B5C6/0029B5D0
            }
        }
        r15d // 0029B5FC
    }
}

fn lcg(state: &mut u64) -> u64 {
    *state = state
        .wrapping_mul(6364136223846793005)
        .wrapping_add(1442695040888963407);
    *state
}

const SPECIAL: [u32; 30] = [
    0x0000_0000, 0x8000_0000, // ±0
    0x0000_0001, 0x8000_0001, 0x007f_ffff, 0x807f_ffff, 0x0040_0000, // denormais
    0x0080_0000, 0x8080_0000, // ±MIN_POSITIVE (normal)
    0x7e7f_e7ff, 0x7e7f_e800, 0x7e7f_e801, 0xfe7f_e800, 0xfe7f_e801, // limite 0x1ED0540
    0x7e80_0000, 0x7f00_0000, 0x7f7f_ffff, 0xff7f_ffff, // 1/x denormal ou tiny
    0x7f80_0000, 0xff80_0000, // ±inf
    0x7fc0_0000, 0xffc0_0000, 0x7fa0_0001, 0xffa0_0001, 0x7fc1_2345, // NaN q/s, sinais
    0x3f80_0000, 0xbf80_0000, 0x3f40_0000, 0x4040_0000, 0x4b18_9680, // 1, -1, 0.75, 3, 1e7
];

/// Valor de teste: 0 = bits aleatórios (domínio inteiro), 1 = especiais,
/// 2 = domínio de 0088E32F (`1 + exp(.)`, isto é `x >= 1`, inclusive +inf).
fn val(state: &mut u64, kind: u32) -> f32 {
    let r = lcg(state);
    match kind {
        0 => f32::from_bits((r >> 32) as u32),
        1 => f32::from_bits(SPECIAL[((r >> 32) as usize) % SPECIAL.len()]),
        _ => {
            let e = f32::from_bits(((r >> 33) as u32) & 0x7fff_ffff); // >= 0, pode ser inf/NaN
            if e.is_nan() { 1.0 + 1.0 } else { 1.0f32 + e }
        }
    }
}

/// Uma chamada do port (in-place ou não) e do emulador; conta diferenças.
fn compare_call(
    c: &Consts,
    x: &[f32],
    src_off: usize,
    dst_off: usize,
    in_place: bool,
    m: Mutation,
    csr: Option<u32>,
) -> (usize, usize, bool) {
    let n = x.len();
    // buffers com alinhamento controlado (offset em bytes mod 32)
    let mk = |off: usize| -> (Vec<f32>, usize) {
        let v = vec![0.0f32; n + 32];
        let base = v.as_ptr() as usize;
        ((v), ((32 - base % 32) % 32 + off) / 4)
    };
    let (mut hs, hs0) = mk(src_off);
    let (mut hd, hd0) = mk(dst_off);
    hs[hs0..hs0 + n].copy_from_slice(x);
    let (mut pd, pd0) = mk(dst_off);
    let (mut ps, ps0) = mk(src_off);
    ps[ps0..ps0 + n].copy_from_slice(x);

    let saved = unsafe { _mm_getcsr() };
    if let Some(v) = csr {
        unsafe { _mm_setcsr(v) };
    }
    let (st_hw, st_port);
    let (hw, port): (Vec<f32>, Vec<f32>);
    unsafe {
        if in_place {
            let p = hs.as_mut_ptr().add(hs0);
            st_hw = emu_29b260(c, p, p, n as i32, m);
            st_port = rcp::inv_32f_in_place(&mut ps[ps0..ps0 + n]);
        } else {
            st_hw = emu_29b260(c, hs.as_ptr().add(hs0), hd.as_mut_ptr().add(hd0), n as i32, m);
            st_port = rcp::inv_32f(&ps[ps0..ps0 + n], &mut pd[pd0..pd0 + n]);
        }
    }
    let csr_after = unsafe { _mm_getcsr() };
    unsafe { _mm_setcsr(saved) };
    let csr_ok = csr.map_or(true, |v| (csr_after & 0xffc0) == (v & 0xffc0));
    if in_place {
        hw = hs[hs0..hs0 + n].to_vec();
        port = ps[ps0..ps0 + n].to_vec();
    } else {
        hw = hd[hd0..hd0 + n].to_vec();
        port = pd[pd0..pd0 + n].to_vec();
        assert_eq!(&ps[ps0..ps0 + n].iter().map(|v| v.to_bits()).collect::<Vec<_>>(),
                   &x.iter().map(|v| v.to_bits()).collect::<Vec<_>>(), "port alterou src");
    }
    let mut bad = 0usize;
    let mut nan = 0usize;
    for i in 0..n {
        if hw[i].is_nan() {
            nan += 1;
        }
        if hw[i].to_bits() != port[i].to_bits() {
            bad += 1;
        }
    }
    if st_hw != st_port {
        bad += 1;
    }
    (bad, nan, csr_ok)
}

fn main() {
    if std::env::args().any(|a| a == "--exhaustive") {
        exhaustive();
    } else {
        run();
    }
}

#[test]
fn rcp_rs_matches_avx_fma_hardware() {
    run();
}

fn check_consts(c: &Consts) {
    let all = |a: &[u32; 8], v: u32| a.iter().all(|&x| x == v);
    assert!(all(&c.sub, rcp::SPECIAL_SUB), "0x1ED0500");
    assert!(all(&c.abs, rcp::ABS_MASK), "0x1ED04C0");
    assert!(all(&c.lim, rcp::SPECIAL_LIMIT as u32), "0x1ED0540");
    assert!(all(&c.one, rcp::ONE.to_bits()), "0x1ED05C0");
    assert!(all(&c.pad, rcp::PAD.to_bits()), "0x1ED0600");
    assert_eq!(c.one_s, rcp::ONE.to_bits(), "0x1ED0620");
    for cnt in 0..9 {
        for l in 0..8 {
            let want = if l < cnt { 0xffff_ffff } else { 0 };
            assert_eq!(c.ld_mask[cnt][l], want, "0x1ED0240 cnt={cnt} lane={l}");
            assert_eq!(c.st_mask[cnt][l], want, "0x1ED0380 cnt={cnt} lane={l}");
        }
    }
    // Despacho: [0x21C7408] = 4, [0x21C6AE8 + 8*4] -> 0x1C8AC0, [0x21C71D8] -> 0x29B260.
    let mut f = std::fs::File::open(dump_path()).unwrap();
    assert_eq!(read_u32s(&mut f, 0x21C7408, 1)[0], 4, "ippJumpIndex");
    assert_eq!(read_u32s(&mut f, 0x21C6B08, 2), vec![0x19B7_8AC0, 0], "tabela 0x21C6AE8[4]");
    assert_eq!(read_u32s(&mut f, 0x21C71D8, 2), vec![0x19C4_B260, 0], "[0x21C71D8]");
}

fn run() {
    assert!(
        is_x86_feature_detected!("avx2") && is_x86_feature_detected!("fma")
            && is_x86_feature_detected!("bmi2") && is_x86_feature_detected!("popcnt"),
        "precisa de AVX2/FMA/BMI2/POPCNT"
    );
    let c = load_consts();
    check_consts(&c);

    let mut seed = 0x0029_b260_1c85_30d1u64;
    let mut ns: Vec<usize> = (1..=80).collect();
    ns.extend_from_slice(&[255, 256, 257, 258, 513]);
    let host_csr = 0x1f80 | 0x8000 | 0x0040 | 0x6000; // FTZ + DAZ + RC = zero

    let (mut calls, mut lanes, mut bad, mut nan, mut csr_bad) = (0usize, 0usize, 0usize, 0usize, 0usize);
    let (mut mut_nospecial, mut mut_nomxcsr, mut mut_ieee) = (0usize, 0usize, 0usize);
    for &n in &ns {
        for src_off in (0..32).step_by(4) {
            for dst_off in [0usize, 4, 12, 28] {
                for round in 0..6u32 {
                    let kind = round % 3;
                    let x: Vec<f32> = (0..n).map(|_| val(&mut seed, kind)).collect();
                    let in_place = round >= 3;
                    let csr = if round == 4 { Some(host_csr) } else { None };
                    let (b, k, ok) = compare_call(&c, &x, src_off, dst_off, in_place, Mutation::None, csr);
                    bad += b;
                    nan += k;
                    lanes += n;
                    calls += 1;
                    if !ok {
                        csr_bad += 1;
                    }
                    if b != 0 && bad <= 10 {
                        println!("DIFF n={n} src_off={src_off} dst_off={dst_off} round={round} bad={b}");
                    }
                    // Mutações de controle (têm de ser detectadas).
                    if kind == 1 {
                        mut_nospecial += compare_call(&c, &x, src_off, dst_off, false, Mutation::NoSpecial, None).0;
                        mut_nomxcsr += compare_call(&c, &x, src_off, dst_off, false, Mutation::NoMxcsr, Some(host_csr)).0;
                    }
                }
            }
        }
    }
    // Mutação IEEE: 1.0/x em toda lane contra o port, no domínio de 0088E32F.
    for _ in 0..2000 {
        let x: Vec<f32> = (0..257).map(|_| val(&mut seed, 2)).collect();
        let mut p = x.clone();
        rcp::inv_32f_in_place(&mut p);
        for i in 0..x.len() {
            if (1.0f32 / x[i]).to_bits() != p[i].to_bits() {
                mut_ieee += 1;
            }
        }
    }
    println!(
        "calls={calls} lanes={lanes} bad={bad} lanes_NaN={nan} (estrito, inclui payload) \
         mxcsr_nao_restaurado={csr_bad} | mutacoes: sem_especial={mut_nospecial} \
         sem_mxcsr={mut_nomxcsr} ieee_1/x={mut_ieee}"
    );
    assert_eq!(bad, 0, "port/src/rcp.rs divergiu do hardware AVX2/FMA");
    assert_eq!(csr_bad, 0, "MXCSR do chamador não foi restaurado");
    assert!(mut_nospecial > 0, "mutação sem lane especial não detectada");
    assert!(mut_nomxcsr > 0, "mutação sem MXCSR não detectada");
    assert!(mut_ieee > 0, "mutação 1.0/x não detectada");
}

/// Todas as 2^32 entradas, em chamadas de 4096 (blocos de 32), port × emulador.
fn exhaustive() {
    let c = load_consts();
    check_consts(&c);
    const CH: usize = 4096;
    let mut x = vec![0.0f32; CH];
    let mut hw = vec![0.0f32; CH];
    let mut port = vec![0.0f32; CH];
    let (mut bad, mut nan, mut special, mut ieee_diff) = (0u64, 0u64, 0u64, 0u64);
    let mut first = Vec::new();
    for chunk in 0..(1u64 << 32) / CH as u64 {
        let base = chunk * CH as u64;
        for i in 0..CH {
            x[i] = f32::from_bits((base + i as u64) as u32);
        }
        let st_hw = unsafe { emu_29b260(&c, x.as_ptr(), hw.as_mut_ptr(), CH as i32, Mutation::None) };
        let st_port = rcp::inv_32f(&x, &mut port);
        if st_hw != st_port {
            bad += 1;
        }
        for i in 0..CH {
            if hw[i].is_nan() {
                nan += 1;
            }
            if rcp::is_special(x[i]) {
                special += 1;
            } else if hw[i].to_bits() != (1.0f32 / x[i]).to_bits() {
                ieee_diff += 1;
            }
            if hw[i].to_bits() != port[i].to_bits() {
                bad += 1;
                if first.len() < 10 {
                    first.push((x[i].to_bits(), hw[i].to_bits(), port[i].to_bits()));
                }
            }
        }
    }
    for (a, h, p) in &first {
        println!("DIFF x={a:08x} hw={h:08x} port={p:08x}");
    }
    println!(
        "exaustivo: 2^32 entradas, bad={bad} lanes_NaN={nan} lanes_especiais={special} \
         normais_diferentes_de_1/x={ieee_diff}"
    );
    assert_eq!(bad, 0);
}
