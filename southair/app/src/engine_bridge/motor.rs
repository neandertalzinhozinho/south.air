//! Motor traduzido (`lifted` + `lifted_extra`) atrás da ponte. Só existe com `--features motor`.
//!
//! Sequência provada bit a bit contra o soothe3 original (`checks/w_cadeia_m6.md` §3 e §5;
//! exemplo completo `lifted_extra/src/bin/m6_run.rs`):
//! 1. `register()`; `Cpu::new(Mem::new(ImageSource do dump))`; `Engine::new` (create `0x862E40`);
//! 2. os 143 parâmetros: plain -> normalizado pelo callback `+0x48` da entrada
//!    `IMAGE_BASE + 0x238E9C0 + 0x68*i`, e `set_param`;
//! 3. `0x863070(handle, 1, 1)`;
//! 4. latência: `0x863020(handle)`;
//! 5. process por bloco: `0x862F00(handle, rdx = SAÍDAS, r8 = ENTRADAS, r9 = 0, 5º arg = n)`.
//!
//! Nada aqui altera a aritmética do motor.

use crate::param_table::{PARAMS, PARAM_COUNT};
use soultree_lifted::api::{call_abi, Engine};
use soultree_lifted::rt::*;
use std::sync::{Arc, Mutex};

pub enum CreateError {
    /// Dump ausente/ilegível (mensagem com o caminho).
    DumpMissing(String),
    Failed(String),
}

/// Texto do payload de um panic.
pub fn panic_text(e: &Box<dyn std::any::Any + Send>) -> String {
    if let Some(s) = e.downcast_ref::<&str>() {
        (*s).to_string()
    } else if let Some(s) = e.downcast_ref::<String>() {
        s.clone()
    } else {
        "unknown panic".to_string()
    }
}

struct ArcImage(Arc<Vec<u8>>);

impl ImageSource for ArcImage {
    fn read_page(&self, rva: u64, out: &mut [u8; 4096]) {
        let s = rva as usize;
        for (i, b) in out.iter_mut().enumerate() {
            *b = *self.0.get(s + i).unwrap_or(&0);
        }
    }
}

const DEFAULT_DUMP: &str = r"D:\PROJETOS\soultree FORK\dumpsooth\nyx_soothe3_dump.bin";

/// Dump compartilhado entre instâncias (lido uma vez por processo; ~137 MB).
static DUMP: Mutex<Option<Arc<Vec<u8>>>> = Mutex::new(None);

pub fn dump_path() -> String {
    // SOUTHAIR_DUMP; RESONIA_DUMP (nome antigo) continua aceito.
    ["SOUTHAIR_DUMP", "RESONIA_DUMP"]
        .iter()
        .find_map(|k| std::env::var(k).ok().filter(|s| !s.is_empty()))
        .unwrap_or_else(|| DEFAULT_DUMP.to_string())
}

fn load_dump() -> Result<Arc<Vec<u8>>, CreateError> {
    let mut g = DUMP.lock().unwrap_or_else(|p| p.into_inner());
    if let Some(d) = g.as_ref() {
        return Ok(d.clone());
    }
    let path = dump_path();
    match std::fs::read(&path) {
        Ok(b) if b.len() >= 0x239_0000 => {
            let a = Arc::new(b);
            *g = Some(a.clone());
            Ok(a)
        }
        Ok(b) => Err(CreateError::DumpMissing(format!("dump too small ({} bytes): {path}", b.len()))),
        Err(e) => Err(CreateError::DumpMissing(format!("cannot read dump ({e}): {path} (set SOUTHAIR_DUMP)"))),
    }
}

pub struct Motor {
    e: Engine,
    ia: u64,
    oa: u64,
    ib: [u64; 2],
    ob: [u64; 2],
    cap: usize,
    lat: u32,
    /// Após um panic o estado emulado não é confiável: não chama destroy.
    pub poisoned: bool,
    /// Frequências (Hz) das curvas de redução, enviadas pelo motor no create (ids 0 e 1).
    pub freq_lo: Vec<f32>,
    pub freq_hi: Vec<f32>,
}

fn floats(b: &[u8]) -> Vec<f32> {
    b.chunks_exact(4).map(|c| f32::from_le_bytes([c[0], c[1], c[2], c[3]])).collect()
}

/// O emulador não é `Send` por causa do `Box<dyn ImageSource>`; aqui a fonte é um
/// `Arc<Vec<u8>>` (Send + Sync) e o resto do estado é dado puro, e o motor só é usado por uma
/// thread por vez (o host serializa initialize/process).
pub struct SendMotor(pub Motor);
unsafe impl Send for SendMotor {}

fn normalize(e: &mut Engine, i: usize, plain: f64) -> f64 {
    let ent = IMAGE_BASE + 0x238E9C0 + 0x68 * i as u64;
    let cb = (e.cpu.mem.r64(ent + 0x48) - IMAGE_BASE) as u32;
    e.cpu.r[RCX] = ent;
    e.cpu.x[1] = plain.to_bits() as u128;
    call_abi(&mut e.cpu, cb, &[]);
    f64::from_bits(e.cpu.x[0] as u64)
}

pub fn create(sample_rate: f32, max_block: usize, params: &[f64; PARAM_COUNT]) -> Result<Motor, CreateError> {
    let dump = load_dump()?;
    soultree_lifted_extra::register();
    let cpu = Cpu::new(Mem::new(Some(Box::new(ArcImage(dump)))));
    let mut e = Engine::new(cpu, sample_rate as f64);
    if e.handle == 0 || e.n_in < 2 || e.n_out < 2 {
        return Err(CreateError::Failed(format!("create returned handle=0x{:X} in={} out={}", e.handle, e.n_in, e.n_out)));
    }
    for i in 0..PARAMS.len() {
        let norm = normalize(&mut e, i, params[i]);
        e.set_param(i, norm);
    }
    e.cpu.r[RCX] = e.handle;
    e.cpu.r[RDX] = 1;
    e.cpu.r[R8] = 1;
    call_abi(&mut e.cpu, 0x863070, &[]);

    let cap = max_block.max(1);
    let ia = e.cpu.mem.alloc(64);
    let oa = e.cpu.mem.alloc(64);
    let mut ib = [0; 2];
    let mut ob = [0; 2];
    for ch in 0..2u64 {
        let i = e.cpu.mem.alloc(4 * cap as u64 + 64);
        let o = e.cpu.mem.alloc(4 * cap as u64 + 64);
        e.cpu.mem.w64(ia + 8 * ch, i);
        e.cpu.mem.w64(oa + 8 * ch, o);
        ib[ch as usize] = i;
        ob[ch as usize] = o;
    }
    // Envios do create: pontos de frequência das curvas (ids 0 = lo, 1 = hi).
    let (mut freq_lo, mut freq_hi) = (Vec::new(), Vec::new());
    for (id, d) in e.cpu.sent.drain(..) {
        match id {
            0 => freq_lo = floats(&d),
            1 => freq_hi = floats(&d),
            _ => {}
        }
    }
    let mut m = Motor { e, ia, oa, ib, ob, cap, lat: 0, poisoned: false, freq_lo, freq_hi };
    m.refresh_latency();
    Ok(m)
}

impl Motor {
    fn refresh_latency(&mut self) {
        self.e.cpu.r[RCX] = self.e.handle;
        call_abi(&mut self.e.cpu, 0x863020, &[]);
        self.lat = self.e.cpu.r[RAX] as u32;
    }

    pub fn latency(&self) -> u32 {
        self.lat
    }

    /// `plain` em unidades da tabela; a conversão para normalizado é a do motor.
    pub fn set_param(&mut self, index: usize, plain: f64) {
        let norm = normalize(&mut self.e, index, plain);
        self.e.set_param(index, norm);
        self.refresh_latency();
    }

    pub fn reset(&mut self) {
        self.e.cpu.r[RCX] = self.e.handle;
        call_abi(&mut self.e.cpu, 0x862F10, &[]);
    }

    /// Processa no lugar. Estéreo: canais 0 e 1. Mono: o canal 0 vai aos dois lados e volta o
    /// lado esquerdo. Canais acima do segundo passam direto.
    pub fn process(&mut self, main: &mut [&mut [f32]], st: &super::BridgeStatus) {
        if main.is_empty() {
            return;
        }
        // Editor aberto: iface+0x28 responde 1 e o motor envia a curva de redução. O áudio não
        // muda (null-test com e sem envio: idêntico byte a byte).
        self.e.cpu.analysis = st.editor_open.load(std::sync::atomic::Ordering::Relaxed);
        let len = main[0].len();
        let mono = main.len() == 1;
        let mut pos = 0;
        while pos < len {
            let m = self.cap.min(len - pos);
            for ch in 0..2 {
                let src = if mono { &main[0] } else { &main[ch] };
                self.e.cpu.mem.write_f32s(self.ib[ch], &src[pos..pos + m]);
            }
            self.e.cpu.r[RCX] = self.e.handle;
            self.e.cpu.r[RDX] = self.oa;
            self.e.cpu.r[R8] = self.ia;
            self.e.cpu.r[R9] = 0;
            call_abi(&mut self.e.cpu, 0x862F00, &[m as u64]);
            let outs = if mono { 1 } else { 2 };
            for ch in 0..outs {
                let v = self.e.cpu.mem.read_f32s(self.ob[ch], m);
                main[ch][pos..pos + m].copy_from_slice(&v);
            }
            pos += m;
        }
        // Última curva enviada neste bloco (ids 2 = lo, 3 = hi); o resto é descartado.
        let (mut lo, mut hi) = (None, None);
        for (id, d) in self.e.cpu.sent.drain(..) {
            match id {
                2 => lo = Some(d),
                3 => hi = Some(d),
                _ => {}
            }
        }
        if lo.is_some() || hi.is_some() {
            st.publish(|a| {
                if let Some(d) = lo {
                    a.mag_lo = floats(&d);
                }
                if let Some(d) = hi {
                    a.mag_hi = floats(&d);
                }
                a.seq += 1;
            });
        }
    }
}

impl Drop for Motor {
    fn drop(&mut self) {
        if self.poisoned {
            return;
        }
        // destroy = 0x862F40(handle); um panic aqui não pode derrubar o host.
        let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            self.e.cpu.r[RCX] = self.e.handle;
            call_abi(&mut self.e.cpu, 0x862F40, &[]);
        }));
    }
}
