//! Validação do tradutor (M5): funções traduzidas mecanicamente × kernels já
//! provados à mão (J6, M1, M2, M3), bit a bit, com entradas aleatórias.
//! Precisam do dump em `dumpsooth/nyx_soothe3_dump.bin` (fonte das constantes).

use super::rt::*;
use std::sync::{Arc, OnceLock};

struct ArcImage(Arc<Vec<u8>>);
impl ImageSource for ArcImage {
    fn read_page(&self, rva: u64, out: &mut [u8; 4096]) {
        let s = rva as usize;
        for (i, b) in out.iter_mut().enumerate() {
            *b = *self.0.get(s + i).unwrap_or(&0);
        }
    }
}

fn dump() -> Arc<Vec<u8>> {
    static D: OnceLock<Arc<Vec<u8>>> = OnceLock::new();
    D.get_or_init(|| {
        let here = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
        let p = here.join("../dumpsooth/nyx_soothe3_dump.bin");
        let v = std::fs::read(&p).expect("dump");
        assert_eq!(v.len(), 137_003_008);
        Arc::new(v)
    })
    .clone()
}

pub fn new_cpu() -> Cpu {
    Cpu::new(Mem::new(Some(Box::new(ArcImage(dump())))))
}

/// Chama `rva` com o endereço de retorno sentinela e confere o `rsp` na volta.
pub fn invoke(c: &mut Cpu, rva: u32) {
    let sp = c.r[RSP];
    c.push(0xDEAD_BEEF);
    super::call(c, rva);
    assert_eq!(c.r[RSP], sp, "rsp desbalanceado após 0x{rva:X}");
}

fn lcg(s: &mut u64) -> u64 {
    *s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    *s
}

fn rnd(s: &mut u64, lo: f32, hi: f32) -> f32 {
    let u = (lcg(s) >> 40) as f32 / (1u64 << 24) as f32;
    lo + (hi - lo) * u
}

fn bits(v: &[f32]) -> Vec<u32> {
    v.iter().map(|x| x.to_bits()).collect()
}

#[test]
fn lifted_div_1550_matches_div_rs() {
    let mut s = 0x1550u64;
    for &n in &[1usize, 7, 8, 9, 16, 17, 31, 32, 33, 257, 513] {
        for off in [0u64, 4, 12, 28] {
            let mut c = new_cpu();
            let num: Vec<f32> = (0..n).map(|_| rnd(&mut s, -4.0, 4.0)).collect();
            let den: Vec<f32> = (0..n).map(|_| rnd(&mut s, 0.01, 3.0)).collect();
            let pn = c.mem.alloc(4 * n as u64 + 64);
            let pd = c.mem.alloc(4 * n as u64 + 64);
            let po = c.mem.alloc(4 * n as u64 + 64) + off;
            c.mem.write_f32s(pn, &num);
            c.mem.write_f32s(pd, &den);
            c.r[RCX] = pd; // den
            c.r[RDX] = pn; // num
            c.r[R8] = po; // dst
            c.r[R9] = n as u64;
            invoke(&mut c, 0x1550);
            let got = c.mem.read_f32s(po, n);
            let mut want = vec![0f32; n];
            soultree_port::div::div_block_mod32(&num, &den, &mut want, (po % 32) as usize);
            assert_eq!(bits(&got), bits(&want), "n={n} off={off}");
        }
    }
}

#[test]
fn lifted_ln_exp_rcp_match_ports() {
    let mut s = 0x2937u64;
    for &n in &[1usize, 5, 8, 15, 16, 17, 33, 100, 257] {
        let mut c = new_cpu();
        let x: Vec<f32> = (0..n).map(|_| rnd(&mut s, 1e-3, 50.0)).collect();
        let y: Vec<f32> = (0..n).map(|_| rnd(&mut s, -60.0, 60.0)).collect();
        let a = c.mem.alloc(4 * n as u64);
        let b = c.mem.alloc(4 * n as u64);
        // ln: 0x1C8500(src=rcx, dst=rdx, n=r8d)
        c.mem.write_f32s(a, &x);
        c.r[RCX] = a;
        c.r[RDX] = b;
        c.r[R8] = n as u64;
        invoke(&mut c, 0x1C8500);
        let mut w = vec![0f32; n];
        soultree_port::ippmath::ln_32f(&x, &mut w);
        assert_eq!(bits(&c.mem.read_f32s(b, n)), bits(&w), "ln n={n}");
        // exp: 0x1C84A0
        c.mem.write_f32s(a, &y);
        c.r[RCX] = a;
        c.r[RDX] = b;
        c.r[R8] = n as u64;
        invoke(&mut c, 0x1C84A0);
        soultree_port::ippmath::exp_32f(&y, &mut w);
        assert_eq!(bits(&c.mem.read_f32s(b, n)), bits(&w), "exp n={n}");
        // rcp: 0x1C8530 (in-place como em 0088E32F)
        c.mem.write_f32s(a, &x);
        c.r[RCX] = a;
        c.r[RDX] = a;
        c.r[R8] = n as u64;
        invoke(&mut c, 0x1C8530);
        soultree_port::rcp::inv_32f(&x, &mut w);
        assert_eq!(bits(&c.mem.read_f32s(a, n)), bits(&w), "rcp n={n}");
    }
}

#[test]
fn lifted_smoother_8c3c20_matches_engine() {
    let mut s = 0x8C3Cu64;
    for &(count, len) in &[(1usize, 1usize), (1, 2), (3, 17), (5, 257), (8, 64)] {
        let mut c = new_cpu();
        let desc = c.mem.alloc(0x410);
        let mut want = Vec::new();
        for k in 0..count {
            let v: Vec<f32> = (0..len).map(|_| rnd(&mut s, -1.0, 1.0)).collect();
            let p = c.mem.alloc(4 * len as u64);
            c.mem.write_f32s(p, &v);
            c.mem.w64(desc + 8 * k as u64, p);
            let mut w = v.clone();
            soultree_port::engine::smoother_fwd_back(&mut w);
            want.push((p, w));
        }
        c.mem.w32(desc + 0x400, count as u32);
        c.mem.w32(desc + 0x404, len as u32);
        c.r[RCX] = desc;
        invoke(&mut c, 0x8C3C20);
        for (p, w) in want {
            assert_eq!(bits(&c.mem.read_f32s(p, len)), bits(&w), "count={count} len={len}");
        }
    }
}
