//! Depuração do process traduzido: monta a chamada a 0x862F00 à mão e inspeciona os buffers.
use soultree_lifted::{api::*, rt::*};
use soultree_lifted_extra::register;
use std::sync::Arc;

struct ArcImage(Arc<Vec<u8>>);
impl ImageSource for ArcImage {
    fn read_page(&self, rva: u64, out: &mut [u8; 4096]) {
        let s = rva as usize;
        for (i, b) in out.iter_mut().enumerate() {
            *b = *self.0.get(s + i).unwrap_or(&0);
        }
    }
}

const STAMP: Option<&str> = option_env!("M6_STAMP");

fn main() {
    let _ = STAMP;
    register();
    let here = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let dump = Arc::new(std::fs::read(here.join("../dumpsooth/nyx_soothe3_dump.bin")).expect("dump"));
    let cpu = Cpu::new(Mem::new(Some(Box::new(ArcImage(dump)))));
    let mut e = Engine::new(cpu, 48000.0);
    for i in 0..143u64 {
        let ent = IMAGE_BASE + 0x238E9C0 + 0x68 * i;
        let plain = f64::from_bits(e.cpu.mem.r64(ent + 0x38));
        let cb = (e.cpu.mem.r64(ent + 0x48) - IMAGE_BASE) as u32;
        e.cpu.r[RCX] = ent;
        e.cpu.x[1] = plain.to_bits() as u128;
        call_abi(&mut e.cpu, cb, &[]);
        let norm = f64::from_bits(e.cpu.x[0] as u64);
        e.set_param(i as usize, norm);
    }
    e.cpu.r[RCX] = e.handle;
    e.cpu.r[RDX] = 1;
    e.cpu.r[R8] = 1;
    call_abi(&mut e.cpu, 0x863070, &[]);
    // latência pela API (0x863020)
    e.cpu.r[RCX] = e.handle;
    call_abi(&mut e.cpu, 0x863020, &[]);
    eprintln!("latência (0x863020) = {}", e.cpu.r[RAX] as u32 as i32);

    let n = 512usize;
    let ia = e.cpu.mem.alloc(64);
    let oa = e.cpu.mem.alloc(64);
    let mut ins = Vec::new();
    let mut outs = Vec::new();
    for ch in 0..2u64 {
        let i = e.cpu.mem.alloc(4 * n as u64);
        let o = e.cpu.mem.alloc(4 * n as u64);
        e.cpu.mem.w64(ia + 8 * ch, i);
        e.cpu.mem.w64(oa + 8 * ch, o);
        ins.push(i);
        outs.push(o);
    }
    let mut tot_in = 0f64;
    let mut tot_out = 0f64;
    for blk in 0..24 {
        for ch in 0..2 {
            let v: Vec<f32> = (0..n)
                .map(|k| 0.5 * ((2.0 * std::f64::consts::PI * 1000.0 * ((blk * n + k) as f64) / 48000.0).sin()) as f32)
                .collect();
            e.cpu.mem.write_f32s(ins[ch], &v);
            e.cpu.mem.write_f32s(outs[ch], &v); // hipótese: r8 = entrada
        }
        e.cpu.r[RCX] = e.handle;
        e.cpu.r[RDX] = ia;
        e.cpu.r[R8] = oa;
        e.cpu.r[R9] = 0;
        call_abi(&mut e.cpu, 0x862F00, &[n as u64]);
        let i0 = e.cpu.mem.read_f32s(ins[0], n);
        let o0 = e.cpu.mem.read_f32s(outs[0], n);
        if blk == 10 { eprintln!("rdx[0][0..4]={:?} r8[0][0..4]={:?}", &i0[..4], &o0[..4]); }
        let pi = i0.iter().fold(0f32, |m, x| m.max(x.abs()));
        let po = o0.iter().fold(0f32, |m, x| m.max(x.abs()));
        tot_in += pi as f64;
        tot_out += po as f64;
        eprintln!("bloco {blk:2}: pico in(depois)={pi:.6} out={po:.6} envios_host={}", SENDS.load(std::sync::atomic::Ordering::Relaxed));
    }
    eprintln!("soma picos in={tot_in:.3} out={tot_out:.3}");
}
