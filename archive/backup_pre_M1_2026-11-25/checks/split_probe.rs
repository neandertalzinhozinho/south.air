//! Sonda READ-ONLY de `0x895C0` (split CCS), caminho lento (`len >= 0x40000`).
//!
//! Chama o plugin carregado por RVA (nenhum patch/hook/injeção):
//!
//!   `0x895C0(buf, n/2, 1, tw50)`
//!
//! e grava `checks/.build/split<order>.bits` com SRC (antes), OUT (depois),
//! TW50 (n f32) e TW38 (tamanho medido).
//!
//! Build: rustc --edition 2021 -O checks\split_probe.rs -o checks\.build\split_probe.exe

use std::alloc::{alloc_zeroed, dealloc, Layout};
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;

#[repr(C)]
struct Mbi {
    base: usize,
    alloc_base: usize,
    alloc_protect: u32,
    partition_id: u16,
    _pad0: u16,
    region_size: usize,
    state: u32,
    protect: u32,
    typ: u32,
    _pad1: u32,
}

#[link(name = "kernel32")]
extern "system" {
    fn LoadLibraryW(name: *const u16) -> isize;
    fn FreeLibrary(h: isize) -> i32;
    fn VirtualQuery(addr: *const u8, buf: *mut Mbi, len: usize) -> usize;
}

type FnGetSize =
    unsafe extern "system" fn(i32, i32, i32, *mut i32, *mut i32, *mut i32) -> i32;
type FnInit = unsafe extern "system" fn(*mut *mut u8, i32, i32, i32, *mut u8, *mut u8) -> i32;
type FnSplit = unsafe extern "system" fn(*mut f32, i32, i32, *const f32);

const RVA_GETSIZE: usize = 0x4100;
const RVA_INIT: usize = 0x8840;
const RVA_SPLIT: usize = 0x895C0;

fn wide(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(Some(0)).collect()
}

struct Aligned {
    p: *mut u8,
    layout: Layout,
}

impl Aligned {
    fn new(bytes: usize) -> Aligned {
        let layout = Layout::from_size_align(bytes.max(64), 64).unwrap();
        let p = unsafe { alloc_zeroed(layout) };
        assert!(!p.is_null());
        Aligned { p, layout }
    }
}

impl Drop for Aligned {
    fn drop(&mut self) {
        unsafe { dealloc(self.p, self.layout) }
    }
}

struct Rng(u64);

impl Rng {
    fn next_u64(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545_F491_4F6C_DD1D)
    }
    fn f32(&mut self) -> f32 {
        let u = (self.next_u64() >> 40) as u32;
        (u as f32 / 8_388_608.0) - 1.0
    }
}

fn read_bits(addr: usize, count: usize) -> Vec<u32> {
    let mut out: Vec<u32> = Vec::with_capacity(count);
    let mut cur = addr;
    while out.len() < count {
        let mut mbi = Mbi {
            base: 0,
            alloc_base: 0,
            alloc_protect: 0,
            partition_id: 0,
            _pad0: 0,
            region_size: 0,
            state: 0,
            protect: 0,
            typ: 0,
            _pad1: 0,
        };
        let q = unsafe { VirtualQuery(cur as *const u8, &mut mbi, std::mem::size_of::<Mbi>()) };
        if q == 0 || mbi.state != 0x1000 {
            break;
        }
        let end = mbi.base.saturating_add(mbi.region_size);
        if end <= cur {
            break;
        }
        let avail = (end - cur) / 4;
        let take = avail.min(count - out.len());
        for i in 0..take {
            out.push(unsafe { *((cur + i * 4) as *const u32) });
        }
        cur += take * 4;
    }
    out.resize(count, 0);
    out
}

fn main() {
    let order: i32 = std::env::args()
        .nth(1)
        .map(|s| s.parse().unwrap())
        .unwrap_or(19);
    let dll = r"D:\PROJETOS\soultree\original\soothe3.vst3";
    let h = unsafe { LoadLibraryW(wide(dll).as_ptr()) };
    if h == 0 {
        eprintln!("LoadLibraryW falhou: {}", std::io::Error::last_os_error());
        std::process::exit(1);
    }
    let base = h as usize;

    let get_size: FnGetSize = unsafe { std::mem::transmute(base + RVA_GETSIZE) };
    let init: FnInit = unsafe { std::mem::transmute(base + RVA_INIT) };
    let split: FnSplit = unsafe { std::mem::transmute(base + RVA_SPLIT) };

    let (mut spec_size, mut init_size, mut buf_size) = (0i32, 0i32, 0i32);
    assert_eq!(
        unsafe { get_size(order, 8, 1, &mut spec_size, &mut init_size, &mut buf_size) },
        0
    );
    eprintln!("sizes: spec={spec_size} init={init_size} buf={buf_size}");
    let spec = Aligned::new(spec_size as usize);
    let initb = Aligned::new(init_size.max(1) as usize);
    let work = Aligned::new(buf_size.max(1) as usize);
    let mut spec_ptr: *mut u8 = std::ptr::null_mut();
    assert_eq!(
        unsafe { init(&mut spec_ptr, order, 8, 1, spec.p, initb.p) },
        0
    );

    let desc = unsafe { *(spec_ptr as *const u64).add(1) as usize };
    let wrapper = unsafe { *((desc + 0x18) as *const usize) };
    let ctx = unsafe { *((wrapper + 8) as *const usize) };
    let t_tw38 = unsafe { *((ctx + 0x38) as *const usize) };
    let t_tw50 = unsafe { *((ctx + 0x50) as *const usize) };
    let tw38_len = (t_tw50 - t_tw38) / 4;
    eprintln!("ctx=0x{ctx:x} tw38=0x{t_tw38:x} tw50=0x{t_tw50:x} tw38_len={tw38_len}");

    let n = 1usize << order;
    let len = (n / 2) as i32;
    let mut rng = Rng(0x1234_5678_9ABC_DEF0);
    let mut buf: Vec<f32> = (0..n + 2).map(|_| rng.f32()).collect();
    let src_bits: Vec<u32> = buf.iter().map(|v| v.to_bits()).collect();
    // Alinhamento 32 B: o vetor do Rust já garante 4 B; usamos buffer alinhado.
    let mut abuf = Aligned::new((n + 8) * 4);
    unsafe {
        let p = abuf.p as *mut f32;
        for i in 0..n + 2 {
            *p.add(i) = buf[i];
        }
        eprintln!("calling split len={len}");
        split(p, len, 1, t_tw50 as *const f32);
        eprintln!("split done");
        buf.clear();
        for i in 0..n + 2 {
            buf.push(*p.add(i));
        }
    }
    let out_bits: Vec<u32> = buf.iter().map(|v| v.to_bits()).collect();
    let tw50 = read_bits(t_tw50, n);
    let tw38 = read_bits(t_tw38, tw38_len);

    let mut txt = String::new();
    txt.push_str(&format!("# order={order} n={n}\n"));
    for (name, vals) in [
        ("SRC", src_bits),
        ("OUT", out_bits),
        ("TW38", tw38),
        ("TW50", tw50),
    ] {
        txt.push_str(name);
        txt.push('\n');
        for v in vals {
            txt.push_str(&format!("{v:08x}\n"));
        }
    }
    let path = format!("checks/.build/split{order}.bits");
    std::fs::write(&path, txt).unwrap();
    println!("escrito {path}");

    unsafe {
        FreeLibrary(h);
    }
}
