//! Sonda READ-ONLY das TABELAS da FFT que `0x1D69E00` consome.
//!
//! Chama o plugin (LoadLibraryW; nenhum patch/hook) e imprime:
//!   ctx+0x30 (ponteiro) -> dwords   (tabela de indices da 1a passada)
//!   ctx+0x38 (ponteiro) -> floats   (twiddles)
//!   ctx+0x50/+0x58      -> floats   (twiddles do split)
//!
//! Build: rustc --edition 2021 -O checks\fft_tables_probe.rs -o checks\.build\fft_tables_probe.exe

use std::alloc::{alloc_zeroed, dealloc, Layout};
use std::ffi::OsStr;
use std::os::windows::ffi::OsStrExt;

#[link(name = "kernel32")]
extern "system" {
    fn LoadLibraryW(name: *const u16) -> isize;
    fn FreeLibrary(h: isize) -> i32;
}

type FnGetSize =
    unsafe extern "system" fn(i32, i32, i32, *mut i32, *mut i32, *mut i32) -> i32;
type FnInit = unsafe extern "system" fn(*mut *mut u8, i32, i32, i32, *mut u8, *mut u8) -> i32;

const RVA_GETSIZE: usize = 0x4100;
const RVA_INIT: usize = 0x8840;

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

fn main() {
    let order: i32 = std::env::args()
        .nth(1)
        .map(|s| s.parse().unwrap())
        .unwrap_or(9);

    let dll = r"D:\PROJETOS\soultree\original\soothe3.vst3";
    let h = unsafe { LoadLibraryW(wide(dll).as_ptr()) };
    if h == 0 {
        eprintln!("LoadLibraryW falhou: {}", std::io::Error::last_os_error());
        std::process::exit(1);
    }
    let base = h as usize;
    let get_size: FnGetSize = unsafe { std::mem::transmute(base + RVA_GETSIZE) };
    let init: FnInit = unsafe { std::mem::transmute(base + RVA_INIT) };

    let (mut a, mut b, mut c) = (0i32, 0i32, 0i32);
    assert_eq!(unsafe { get_size(order, 8, 1, &mut a, &mut b, &mut c) }, 0);
    let spec = Aligned::new(a as usize);
    let initb = Aligned::new(b.max(1) as usize);
    let mut spec_ptr: *mut u8 = std::ptr::null_mut();
    assert_eq!(
        unsafe { init(&mut spec_ptr, order, 8, 1, spec.p, initb.p) },
        0
    );

    let desc = unsafe { *(spec_ptr as *const u64).add(1) as usize };
    let wrapper = unsafe { *((desc + 0x18) as *const usize) };
    let ctx = unsafe { *((wrapper + 8) as *const usize) };
    println!("order={order} ctx=0x{ctx:x}");

    let fields: [(usize, &str); 6] = [
        (0x30, "tabela idx (dwords)"),
        (0x38, "twiddles gen"),
        (0x50, "twiddles split"),
        (0x58, "tabela 0x58"),
        (0x18, "workspace size"),
        (0x10, "escala"),
    ];
    for (off, name) in fields {
        let v = unsafe { *((ctx + off) as *const u64) };
        println!("ctx+0x{off:02x} = 0x{v:x}   ({name})");
    }

    // tamanho do workspace e da escala
    let ws = unsafe { *((ctx + 0x18) as *const i64) };
    println!("workspace = {ws} bytes");

    let t_idx = unsafe { *((ctx + 0x30) as *const usize) };
    let t_tw = unsafe { *((ctx + 0x38) as *const usize) };
    let t_sp = unsafe { *((ctx + 0x50) as *const usize) };

    println!("\n== ctx+0x30 (dwords) ==");
    for row in 0..32 {
        let mut s = String::new();
        for col in 0..8 {
            let v = unsafe { *((t_idx + (row * 8 + col) * 4) as *const u32) };
            s.push_str(&format!("{:5} ", v as i32));
        }
        println!("{row:3}: {s}");
    }

    let n = 1usize << order;
    println!("\n== ctx+0x38 (f32), n/2 = {} ==", n / 2);
    for row in 0..(n / 32).max(1) {
        let mut s = String::new();
        for col in 0..8 {
            let v = unsafe { *((t_tw + (row * 8 + col) * 4) as *const f32) };
            s.push_str(&format!("{:+.7e} ", v));
        }
        println!("{row:3}: {s}");
    }

    println!("\n== ctx+0x50 (f32), n/2 = {} ==", n / 2);
    for row in 0..(n / 32).max(1) {
        let mut s = String::new();
        for col in 0..8 {
            let v = unsafe { *((t_sp + (row * 8 + col) * 4) as *const f32) };
            s.push_str(&format!("{:+.7e} ", v));
        }
        println!("{row:3}: {s}");
    }

    unsafe {
        FreeLibrary(h);
    }
}
