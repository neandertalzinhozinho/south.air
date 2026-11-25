//! Sonda READ-ONLY da FFT interna do soothe3 (IPP embutida estaticamente).
//!
//! Nao patcheia, nao hooka, nao injeta: so `LoadLibraryW` (como o host) e
//! chamadas por RVA nas funcoes internas, que sao exatamente as mesmas que o
//! audio usa:
//!
//!   0x4100  getSize(order, flag, hint, &specSize, &initSize, &bufSize) -> st
//!           (thunk 0x1130; chamado por 0x6166A2)
//!   0x8840  init(&spec, order, flag, hint, specBuf, initBuf) -> st
//!           (thunk 0x12B0; chamado por 0x6166DE)
//!   0x20E0  fwd(src, dst, spec, buf) -> st      (thunk 0x1010)
//!   0x7B40  inv(src, dst, spec, buf) -> st      (thunk 0x1280)
//!
//! O proposito e fixar o LAYOUT de bins e vetores-ouro bit-exatos para
//! `checks/stage_j_fft.rs`, sem inferir de nome de parametro.
//!
//! Build: rustc --edition 2021 checks\fft_probe.rs -O -o checks\.build\fft_probe.exe

use std::alloc::{alloc_zeroed, dealloc, Layout};
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;
use std::ptr;

#[link(name = "kernel32")]
extern "system" {
    fn LoadLibraryW(name: *const u16) -> isize;
    fn FreeLibrary(h: isize) -> i32;
}

type FnGetSize =
    unsafe extern "system" fn(i32, i32, i32, *mut i32, *mut i32, *mut i32) -> i32;
type FnInit =
    unsafe extern "system" fn(*mut *mut u8, i32, i32, i32, *mut u8, *mut u8) -> i32;
type FnXform = unsafe extern "system" fn(*const f32, *mut f32, *mut u8, *mut u8) -> i32;

const RVA_GETSIZE: usize = 0x4100;
const RVA_INIT: usize = 0x8840;
const RVA_FWD: usize = 0x20E0;
const RVA_INV: usize = 0x7B40;

struct Buf {
    p: *mut u8,
    layout: Layout,
}

impl Buf {
    fn new(bytes: usize) -> Buf {
        let layout = Layout::from_size_align(bytes.max(64), 64).unwrap();
        let p = unsafe { alloc_zeroed(layout) };
        assert!(!p.is_null());
        Buf { p, layout }
    }
    fn f32(&self) -> *mut f32 {
        self.p as *mut f32
    }
}

impl Drop for Buf {
    fn drop(&mut self) {
        unsafe { dealloc(self.p, self.layout) }
    }
}

fn wide(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(Some(0)).collect()
}

fn hexbits(x: f32) -> String {
    format!("{:08x}", x.to_bits())
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let order: i32 = args.get(1).map(|s| s.parse().unwrap()).unwrap_or(9);
    let sig: String = args.get(2).cloned().unwrap_or_else(|| "impulse".into());

    let dll = r"D:\PROJETOS\soultree\original\soothe3.vst3";
    let h = unsafe { LoadLibraryW(wide(dll).as_ptr()) };
    if h == 0 {
        eprintln!("LoadLibraryW falhou: {}", std::io::Error::last_os_error());
        std::process::exit(1);
    }
    let base = h as usize;
    println!("modulo base = 0x{base:x} (rva 0x{order:x} pedido: order={order})");

    let get_size: FnGetSize = unsafe { std::mem::transmute(base + RVA_GETSIZE) };
    let init: FnInit = unsafe { std::mem::transmute(base + RVA_INIT) };
    let fwd: FnXform = unsafe { std::mem::transmute(base + RVA_FWD) };
    let inv: FnXform = unsafe { std::mem::transmute(base + RVA_INV) };

    let (mut spec_size, mut init_size, mut buf_size) = (0i32, 0i32, 0i32);
    let st = unsafe { get_size(order, 8, 1, &mut spec_size, &mut init_size, &mut buf_size) };
    println!(
        "getSize(order={order}, flag=8, hint=1) -> st={st} spec={spec_size} init={init_size} buf={buf_size}"
    );
    if st != 0 || spec_size <= 0 || init_size < 0 || buf_size < 0 {
        eprintln!("getSize recusou; parando");
        std::process::exit(2);
    }

    let spec = Buf::new(spec_size as usize);
    let initb = Buf::new((init_size.max(1)) as usize);
    let work = Buf::new((buf_size.max(1)) as usize);

    let mut spec_ptr: *mut u8 = ptr::null_mut();
    let st = unsafe {
        init(
            &mut spec_ptr,
            order,
            8,
            1,
            spec.p,
            initb.p,
        )
    };
    println!("init -> st={st} spec_ptr=0x{:x} (base+0x{:x})", spec_ptr as usize, spec_ptr as usize - base);
    if st != 0 || spec_ptr.is_null() {
        eprintln!("init recusou; parando");
        std::process::exit(3);
    }
    unsafe {
        let d = spec_ptr as *const u32;
        println!("spec[0] (magic) = {}", *d);
        let q = spec_ptr as *const u64;
        println!("spec[8] (inner) = 0x{:x}", *q.add(1));
        let inner = *q.add(1) as *const u8;
        let iq = inner as *const u64;
        println!("inner[0] = 0x{:x}  inner[8] = 0x{:x}  inner[0x18] = 0x{:x}",
                 *iq, *iq.add(1), *iq.add(3));
        let w = *iq.add(3) as *const u8;
        let wq = w as *const u64;
        println!("wrapper[0] = {}  wrapper[8] = 0x{:x}", *(w as *const u32), *wq.add(1));
        println!("wrapper[+0x18] = 0x{:x}  wrapper[+0x20] = 0x{:x}  wrapper[+0x28] = 0x{:x}",
                 *wq.add(3) - base as u64, *wq.add(4) - base as u64, *wq.add(5) - base as u64);
        println!("wrapper[+0x30] = 0x{:x}  wrapper[+0x38] = 0x{:x}  wrapper[+0x40] = 0x{:x}",
                 *wq.add(6) - base as u64, *wq.add(7) - base as u64, *wq.add(8) - base as u64);
        let c = *wq.add(1) as *const u32;
        let cq = c as *const u64;
        println!("ctx[0] = {} (magic)", *c);
        println!("ctx[+4] order = {}  ctx[+8] = {}  ctx[+0xc] = {}",
                 *(c as *const i32).add(1), *c.add(2), *c.add(3));
        println!("ctx[+0x10] = f32 {} (bits {})",
                 *(cq.add(2) as *const f32), hexbits(*(cq.add(2) as *const f32)));
        println!("ctx[+0x14] = {}  ctx[+0x18] = 0x{:x}  ctx[+0x1c] = {}",
                 *c.add(5), *cq.add(3), *c.add(7));
        println!("ctx[+0x30] = 0x{:x}  ctx[+0x38] = 0x{:x}  ctx[+0x50] = 0x{:x}  ctx[+0x58] = 0x{:x}",
                 *cq.add(6), *cq.add(7), *cq.add(10), *cq.add(11));
    }

    let n: usize = 1usize << order; // comprimento real da FFT
    println!("n = {n}");

    let mut src = vec![0f32; n];
    match sig.as_str() {
        "impulse" => src[0] = 1.0,
        "dc" => src.iter_mut().for_each(|s| *s = 1.0),
        "cos" => {
            for (i, s) in src.iter_mut().enumerate() {
                *s = (2.0 * std::f64::consts::PI * 3.0 * i as f64 / n as f64).cos() as f32;
            }
        }
        "ramp" => {
            for (i, s) in src.iter_mut().enumerate() {
                *s = ((i as f32) / (n as f32) - 0.5) * 2.0;
            }
        }
        other => panic!("sinal desconhecido: {other}"),
    }

    let mut dst = vec![0f32; n + 2];
    let st = unsafe { fwd(src.as_ptr(), dst.as_mut_ptr(), spec_ptr, work.p) };
    println!("fwd -> st={st}");
    if st != 0 {
        eprintln!("fwd falhou; parando");
        std::process::exit(4);
    }

    let show = (16).min(dst.len());
    println!("--- fwd dst[0..{show}] = n/2+2 primeiros floats ---");
    for i in 0..show {
        println!("  dst[{i:4}] = {:+.9e}  bits {}", dst[i], hexbits(dst[i]));
    }
    println!("--- cauda ---");
    for i in 0..show.min(6) {
        let j = dst.len() - 1 - i;
        println!("  dst[{j:4}] = {:+.9e}  bits {}", dst[j], hexbits(dst[j]));
    }
    let mut nz = Vec::new();
    for (i, v) in dst.iter().enumerate() {
        if *v != 0.0 {
            nz.push((i, *v));
        }
    }
    println!("nao-zero: {} de {} floats", nz.len(), dst.len());
    for (i, v) in nz.iter().take(16) {
        println!("   [{i}] = {v:+.9e}");
    }

    // round-trip: inv(fwd(x)) deve dar x*n (flag 8 = sem divisao da IPP)
    let mut back = vec![0f32; n + 2];
    let st = unsafe { inv(dst.as_ptr(), back.as_mut_ptr(), spec_ptr, work.p) };
    println!("inv -> st={st}");
    if st == 0 {
        let mut maxerr = 0f32;
        let mut maxerr_scaled = 0f32;
        for i in 0..n {
            let e = (back[i] - src[i]).abs();
            let es = (back[i] - src[i] * n as f32).abs();
            if e > maxerr {
                maxerr = e;
            }
            if es > maxerr_scaled {
                maxerr_scaled = es;
            }
        }
        println!("inv: max|back-x| = {maxerr:.9e}   max|back-x*n| = {maxerr_scaled:.9e}");
        for i in 0..8.min(n) {
            println!("  back[{i}] = {:+.9e} bits {}   x*n = {:+.9e} bits {}",
                     back[i], hexbits(back[i]), src[i] * n as f32, hexbits(src[i] * n as f32));
        }
    }

    // Dump reproduzivel: bits de src e dst para alimentar o teste Rust.
    {
        let mut txt = String::new();
        txt.push_str(&format!("# order={order} sig={sig} n={n}\n"));
        txt.push_str("SRC\n");
        for v in &src {
            txt.push_str(&format!("{:08x}\n", v.to_bits()));
        }
        txt.push_str("DST\n");
        for v in &dst {
            txt.push_str(&format!("{:08x}\n", v.to_bits()));
        }
        txt.push_str("BACK\n");
        for v in &back {
            txt.push_str(&format!("{:08x}\n", v.to_bits()));
        }
        let path = format!("checks/.build/fft_{order}_{sig}.bits");
        std::fs::write(&path, txt).unwrap();
        println!("dump escrito em {path}");
    }

    unsafe {
        FreeLibrary(h);
    }
}
