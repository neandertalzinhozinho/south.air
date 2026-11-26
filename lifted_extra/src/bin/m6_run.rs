//! M6/M7: roda o motor traduzido num WAV estéreo float32 e grava a saída.
//! Uso: m6_run <in.wav> <out.wav> [bloco=512]
use soultree_lifted::{api::Engine, rt::*};
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

fn read_wav(p: &str) -> (u32, Vec<Vec<f32>>) {
    let b = std::fs::read(p).expect("wav");
    let mut i = 12;
    let (mut fs, mut ch, mut fmt, mut bits) = (0u32, 0usize, 0u16, 0u16);
    let mut data = Vec::new();
    while i + 8 <= b.len() {
        let id = &b[i..i + 4];
        let sz = u32::from_le_bytes(b[i + 4..i + 8].try_into().unwrap()) as usize;
        if id == b"fmt " {
            fmt = u16::from_le_bytes([b[i + 8], b[i + 9]]);
            ch = u16::from_le_bytes([b[i + 10], b[i + 11]]) as usize;
            fs = u32::from_le_bytes(b[i + 12..i + 16].try_into().unwrap());
            bits = u16::from_le_bytes([b[i + 22], b[i + 23]]);
        } else if id == b"data" {
            data = b[i + 8..i + 8 + sz].to_vec();
        }
        i += 8 + sz + (sz & 1);
    }
    assert!(fmt == 3 && bits == 32, "só float32");
    let n = data.len() / 4 / ch;
    let mut out = vec![vec![0f32; n]; ch];
    for k in 0..n {
        for c in 0..ch {
            let o = 4 * (k * ch + c);
            out[c][k] = f32::from_le_bytes(data[o..o + 4].try_into().unwrap());
        }
    }
    (fs, out)
}

fn write_wav(p: &str, fs: u32, chans: &[Vec<f32>]) {
    let ch = chans.len();
    let n = chans[0].len();
    let mut data = Vec::with_capacity(4 * n * ch);
    for k in 0..n {
        for c in chans {
            data.extend_from_slice(&c[k].to_le_bytes());
        }
    }
    let mut h = Vec::new();
    h.extend_from_slice(b"RIFF");
    h.extend_from_slice(&(36 + data.len() as u32).to_le_bytes());
    h.extend_from_slice(b"WAVEfmt ");
    h.extend_from_slice(&16u32.to_le_bytes());
    h.extend_from_slice(&3u16.to_le_bytes());
    h.extend_from_slice(&(ch as u16).to_le_bytes());
    h.extend_from_slice(&fs.to_le_bytes());
    h.extend_from_slice(&(fs * 4 * ch as u32).to_le_bytes());
    h.extend_from_slice(&((4 * ch) as u16).to_le_bytes());
    h.extend_from_slice(&32u16.to_le_bytes());
    h.extend_from_slice(b"data");
    h.extend_from_slice(&(data.len() as u32).to_le_bytes());
    h.extend_from_slice(&data);
    std::fs::write(p, h).expect("gravar wav");
}

/// Carimbo de build (muda o hash do .exe quando o App Control bloqueia um binário).
const STAMP: Option<&str> = option_env!("M6_STAMP");

fn main() {
    let _ = STAMP;
    register();
    let a: Vec<String> = std::env::args().collect();
    let block: usize = a.get(3).map(|s| s.parse().unwrap()).unwrap_or(512);
    let (fs, input) = read_wav(&a[1]);
    let here = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let dump = Arc::new(std::fs::read(here.join("../dumpsooth/nyx_soothe3_dump.bin")).expect("dump"));
    let cpu = Cpu::new(Mem::new(Some(Box::new(ArcImage(dump)))));
    let t0 = std::time::Instant::now();
    let mut e = Engine::new(cpu, fs as f64);
    // M6_ANALYSIS: habilitado já antes dos defaults, para ver o que o setter envia.
    if std::env::var("M6_ANALYSIS").is_ok() {
        e.cpu.analysis = true;
    }
    eprintln!("create ok: handle=0x{:X} in={} out={} icount={} ({:?})", e.handle, e.n_in, e.n_out, e.cpu.icount, t0.elapsed());
    // Como o plugin faz depois do create (estado medido no oráculo, checks/w_cadeia_m6.md §4):
    // 1) para cada parâmetro i: norm = callback +0x48 (plain->norm) aplicado ao default +0x38,
    //    e o setter 0x862EF0 com esse valor;
    // 2) 0x863070(handle, edx=1, r8d=1) -> [eng+0x235] = 1 (medido [0x234..0x237] = 0,1,0,0).
    if std::env::var("M6_NO_DEFAULTS").is_err() {
        for i in 0..143u64 {
            let ent = IMAGE_BASE + 0x238E9C0 + 0x68 * i;
            let plain = f64::from_bits(e.cpu.mem.r64(ent + 0x38));
            let cb = (e.cpu.mem.r64(ent + 0x48) - IMAGE_BASE) as u32;
            e.cpu.r[RCX] = ent;
            e.cpu.x[1] = plain.to_bits() as u128;
            soultree_lifted::api::call_abi(&mut e.cpu, cb, &[]);
            let norm = f64::from_bits(e.cpu.x[0] as u64);
            e.set_param(i as usize, norm);
        }
        e.cpu.r[RCX] = e.handle;
        e.cpu.r[RDX] = 1;
        e.cpu.r[R8] = 1;
        soultree_lifted::api::call_abi(&mut e.cpu, 0x863070, &[]);
        eprintln!("defaults aplicados (icount={})", e.cpu.icount);
    }
    // M6_SET="i=norm,i=norm": parâmetros normalizados aplicados depois dos defaults
    // (ex.: "1=1" liga Low latency, entrada 1 da tabela 0x238E9C0).
    if let Ok(s) = std::env::var("M6_SET") {
        for kv in s.split(',').filter(|x| !x.is_empty()) {
            let (k, v) = kv.split_once('=').expect("M6_SET: i=valor");
            e.set_param(k.trim().parse().unwrap(), v.trim().parse().unwrap());
        }
        e.cpu.r[RCX] = e.handle;
        soultree_lifted::api::call_abi(&mut e.cpu, 0x863020, &[]);
        eprintln!("M6_SET={s}: latência (0x863020) = {}", e.cpu.r[RAX] as u32 as i32);
    }
    // process = 0x862F00(handle, rdx = saídas, r8 = entradas, r9 = 0 (sem sidechain), [rsp+0x28] = n).
    // Medido no motor traduzido: com r8 = sinal e rdx = buffer, a saída processada sai em rdx e
    // r8 fica intacto; com r8 = 0 a saída é 0 (checks/w_cadeia_m6.md §1).
    // M6_ANALYSIS=1: iface+0x28 responde habilitado (editor aberto); lista registros e envios.
    let analysis = std::env::var("M6_ANALYSIS").is_ok();
    if analysis {
        for (id, d) in &e.cpu.sent {
            let f: Vec<f32> = d.chunks(4).map(|b| f32::from_le_bytes([b[0], b[1], b[2], b[3]])).collect();
            eprintln!("envio antes do process: id={id} n={} primeiros={:?} últimos={:?}", f.len(), &f[..f.len().min(5)], &f[f.len().saturating_sub(3)..]);
        }
        e.cpu.sent.clear();
        e.cpu.analysis = true;
        for (id, name, r9) in &e.cpu.registered {
            eprintln!("registro iface+0x18: id={id} nome={name:?} r9={r9}");
        }
    }
    let mut blk_no = 0usize;
    let mut hist: std::collections::BTreeMap<u32, (usize, usize, usize)> = Default::default();
    if std::env::var("M6_PROF").is_ok() {
        e.cpu.prof_on();
    }
    let n = input[0].len();
    let mut out = vec![vec![0f32; n]; e.n_out];
    let ia = e.cpu.mem.alloc(64);
    let oa = e.cpu.mem.alloc(64);
    let mut ib = Vec::new();
    let mut ob = Vec::new();
    for ch in 0..2u64 {
        let i = e.cpu.mem.alloc(4 * block as u64 + 64);
        let o = e.cpu.mem.alloc(4 * block as u64 + 64);
        e.cpu.mem.w64(ia + 8 * ch, i);
        e.cpu.mem.w64(oa + 8 * ch, o);
        ib.push(i);
        ob.push(o);
    }
    let mut pos = 0;
    while pos < n {
        let m = block.min(n - pos);
        for ch in 0..2 {
            e.cpu.mem.write_f32s(ib[ch], &input[ch][pos..pos + m]);
            e.cpu.mem.write_f32s(ob[ch], &vec![0f32; m]);
        }
        let mode = std::env::var("M6_MODE").unwrap_or_default();
        e.cpu.r[RCX] = e.handle;
        e.cpu.r[RDX] = oa;
        e.cpu.r[R8] = ia;
        e.cpu.r[R9] = 0;
        if mode == "resend" || mode == "resend_f" {
            // hipótese: o wrapper reenvia os parâmetros a cada process
            for i in 0..143u64 {
                let ent = IMAGE_BASE + 0x238E9C0 + 0x68 * i;
                let plain = f64::from_bits(e.cpu.mem.r64(ent + 0x38));
                let cb = (e.cpu.mem.r64(ent + 0x48) - IMAGE_BASE) as u32;
                e.cpu.r[RCX] = ent;
                e.cpu.x[1] = plain.to_bits() as u128;
                soultree_lifted::api::call_abi(&mut e.cpu, cb, &[]);
                let norm = f64::from_bits(e.cpu.x[0] as u64);
                e.set_param(i as usize, norm);
            }
            if mode == "resend_f" {
                e.cpu.r[RCX] = e.handle;
                e.cpu.r[RDX] = 1;
                e.cpu.r[R8] = 1;
                soultree_lifted::api::call_abi(&mut e.cpu, 0x863070, &[]);
            }
            e.cpu.r[RCX] = e.handle;
            e.cpu.r[RDX] = oa;
            e.cpu.r[R8] = ia;
            e.cpu.r[R9] = 0;
        }
        if mode == "f10" {
            e.cpu.r[RCX] = e.handle;
            soultree_lifted::api::call_abi(&mut e.cpu, 0x862F10, &[]);
            e.cpu.r[RCX] = e.handle;
            e.cpu.r[RDX] = oa;
            e.cpu.r[R8] = ia;
            e.cpu.r[R9] = 0;
        }
        if mode == "sc" {
            e.cpu.r[R9] = ia; // sidechain = entrada
        }
        if mode == "inplace" {
            for ch in 0..2 {
                let v = e.cpu.mem.read_f32s(ib[ch], m);
                e.cpu.mem.write_f32s(ob[ch], &v);
            }
        }
        // M6_N: n passado ao motor por bloco (hipótese do wrapper); o resto da saída fica 0
        let nn: usize = std::env::var("M6_N").ok().and_then(|v| v.parse().ok()).unwrap_or(m).min(m);
        soultree_lifted::api::call_abi(&mut e.cpu, 0x862F00, &[nn as u64]);
        if analysis {
            for (id, d) in &e.cpu.sent {
                let ent = hist.entry(*id).or_insert((0usize, usize::MAX, 0usize));
                ent.0 += 1;
                ent.1 = ent.1.min(blk_no);
                ent.2 = d.len() / 4;
                if (*id == 0 || *id == 1 || *id == 4) && ent.0 == 1 {
                    let f: Vec<f32> = d.chunks(4).map(|b| f32::from_le_bytes([b[0], b[1], b[2], b[3]])).collect();
                    eprintln!("id={id} n={} primeiros={:?} últimos={:?}", f.len(), &f[..f.len().min(5)], &f[f.len().saturating_sub(3)..]);
                }
            }
            if blk_no < 3 || blk_no == 40 {
                for (id, d) in &e.cpu.sent {
                    let f: Vec<f32> = d.chunks(4).map(|b| f32::from_le_bytes([b[0], b[1], b[2], b[3]])).collect();
                    let mx = f.iter().cloned().fold(f32::MIN, f32::max);
                    let mn = f.iter().cloned().fold(f32::MAX, f32::min);
                    eprintln!("bloco {blk_no}: envio id={id} n={} min={mn:.4} max={mx:.4} primeiros={:?}", f.len(), &f[..f.len().min(6)]);
                }
            }
            e.cpu.sent.clear();
        }
        blk_no += 1;
        for ch in 0..e.n_out {
            let v = e.cpu.mem.read_f32s(ob[ch], m);
            out[ch][pos..pos + m].copy_from_slice(&v);
        }
        pos += m;
    }
    if analysis {
        for (id, (k, first, n)) in &hist {
            eprintln!("envios id={id}: {k} vezes, primeiro bloco {first}, n={n}");
        }
    }
    eprintln!("processado: {n} frames, icount={} ({:?})", e.cpu.icount, t0.elapsed());
    if let Some(p) = e.cpu.prof.take() {
        // Perfil por bloco: "RVA execuções instruções" (agrupar por função com o gen_*.rs).
        let mut v: Vec<_> = p.into_iter().collect();
        v.sort_by(|a, b| b.1 .1.cmp(&a.1 .1));
        let path = std::env::var("M6_PROF").unwrap();
        let txt: String = v.iter().map(|(r, (k, n))| format!("{r:X} {k} {n}
")).collect();
        std::fs::write(&path, txt).expect("M6_PROF");
        eprintln!("perfil gravado em {path}");
    }
    if let Ok(p) = std::env::var("M6_DUMP") {
        let eng = e.engine_ptr();
        let mut buf = vec![0u8; 0x600];
        e.cpu.mem.read(eng, &mut buf);
        std::fs::write(&p, &buf).expect("dump do estado");
        eprintln!("engine[0..0x600] gravado em {p}");
    }
    write_wav(&a[2], fs, &out);
}
