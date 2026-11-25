//! Sonda READ-ONLY das PEÇAS da FFT, para transcrever sem inferência.
//!
//! Chama, por RVA, direto no plugin carregado com `LoadLibraryW` (nenhum
//! patch/hook/injeção), as três peças que `0x72480` encadeia para ordem 6:
//!
//!   `0x8BFE0`  kernel complexo de 32 pontos: (src, dst) -> void
//!   pack       inline em `0x725F6`..`0x72617`
//!   `0x895C0`  split CCS: (buf, len, r8d, table) -> void
//!
//! Grava bits medidos em `checks/.build/j4_stage.bits` e confere que a cadeia
//! manual reproduz bit a bit o que `0x20E0` (fwd) devolve.
//!
//! Build: rustc --edition 2021 -O checks\fft_stage_probe.rs -o checks\.build\fft_stage_probe.exe

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
type FnInit =
    unsafe extern "system" fn(*mut *mut u8, i32, i32, i32, *mut u8, *mut u8) -> i32;
type FnXform = unsafe extern "system" fn(*const f32, *mut f32, *mut u8, *mut u8) -> i32;
type FnKernel = unsafe extern "system" fn(*const f32, *mut f32);
type FnSplit = unsafe extern "system" fn(*mut f32, i32, i32, *const u8);

const RVA_GETSIZE: usize = 0x4100;
const RVA_INIT: usize = 0x8840;
const RVA_FWD: usize = 0x20E0;
const RVA_KERNEL6: usize = 0x8BFE0;
const RVA_KERNEL7: usize = 0x8C280;
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

/// xorshift64* determinístico: bits reprodutíveis sem depender de rand.
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
        // [-1, 1) com 24 bits de mantissa, sempre normal.
        let u = (self.next_u64() >> 40) as u32; // 24 bits
        (u as f32 / 8_388_608.0) - 1.0
    }
}

fn main() {
    let order: i32 = std::env::args()
        .nth(1)
        .map(|s| s.parse().unwrap())
        .unwrap_or(6);
    // 0007258C: ordem <= 7 usa a tabela 0x1DFA358; 6 -> 0x8BFE0, 7 -> 0x8C280.
    let rva_kernel = match order {
        6 => RVA_KERNEL6,
        7 => RVA_KERNEL7,
        _ => panic!("kernel de ordem {order} ainda NAO EXTRAIDO"),
    };

    let dll = r"D:\PROJETOS\soultree\original\soothe3.vst3";
    let h = unsafe { LoadLibraryW(wide(dll).as_ptr()) };
    if h == 0 {
        eprintln!("LoadLibraryW falhou: {}", std::io::Error::last_os_error());
        std::process::exit(1);
    }
    let base = h as usize;

    let get_size: FnGetSize = unsafe { std::mem::transmute(base + RVA_GETSIZE) };
    let init: FnInit = unsafe { std::mem::transmute(base + RVA_INIT) };
    let fwd: FnXform = unsafe { std::mem::transmute(base + RVA_FWD) };
    let kernel: FnKernel = unsafe { std::mem::transmute(base + rva_kernel) };
    let split: FnSplit = unsafe { std::mem::transmute(base + RVA_SPLIT) };

    let (mut spec_size, mut init_size, mut buf_size) = (0i32, 0i32, 0i32);
    let st = unsafe { get_size(order, 8, 1, &mut spec_size, &mut init_size, &mut buf_size) };
    assert_eq!(st, 0);
    let spec = Aligned::new(spec_size as usize);
    let initb = Aligned::new(init_size.max(1) as usize);
    let work = Aligned::new(buf_size.max(1) as usize);
    let mut spec_ptr: *mut u8 = std::ptr::null_mut();
    let st = unsafe { init(&mut spec_ptr, order, 8, 1, spec.p, initb.p) };
    assert_eq!(st, 0);

    // spec+8 = descritor; descritor+0x18 = wrapper; wrapper+8 = ctx.
    let desc = unsafe { *(spec_ptr as *const u64).add(1) as usize };
    let wrapper = unsafe { *((desc + 0x18) as *const usize) };
    let ctx = unsafe { *((wrapper + 8) as *const usize) };
    let table = unsafe { *((ctx + 0x50) as *const usize) };
    println!("base=0x{base:x} ctx=0x{ctx:x} table(ctx+0x50)=0x{table:x}");

    let n = 1usize << order;

    // ---- twiddles do split: 0x100 bytes medidos ----
    let mut tw = Vec::new();
    for i in 0..(2 * n) {
        let v = unsafe { *(table as *const u32).add(i) };
        tw.push(v);
    }

    // ---- input determinístico ----
    let mut rng = Rng(0x0123_4567_89AB_CDEF);
    let src: Vec<f32> = (0..n).map(|_| rng.f32()).collect();

    // ---- kernel puro ----
    let mut kd = vec![0f32; n + 2];
    unsafe { kernel(src.as_ptr(), kd.as_mut_ptr()) };
    let kd_bits: Vec<u32> = kd[..n].iter().map(|v| v.to_bits()).collect();

    // ---- cadeia manual: kernel -> pack -> split -> move ----
    let mut man = vec![0f32; n + 2];
    unsafe { kernel(src.as_ptr(), man.as_mut_ptr()) };
    let pack = |d: &mut [f32]| {
        let re = d[0];
        let im = d[1];
        d[0] = im + re; // 0007260B vaddss xmm0,xmm2,xmm1
        d[1] = re - im; // 0007260F vsubss xmm3,xmm1,xmm2
    };
    pack(&mut man);
    unsafe { split(man.as_mut_ptr(), (n / 2) as i32, 1, table as *const u8) };
    if n != 1 {
        let t = man[1];
        man[n] = t;
        man[n + 1] = 0.0;
        man[1] = 0.0;
    }
    let man_bits: Vec<u32> = man.iter().map(|v| v.to_bits()).collect();

    // ---- referência: fwd do plugin ----
    let mut dst = vec![0f32; n + 2];
    let st = unsafe { fwd(src.as_ptr(), dst.as_mut_ptr(), spec_ptr, work.p) };
    assert_eq!(st, 0);
    let dst_bits: Vec<u32> = dst.iter().map(|v| v.to_bits()).collect();

    let diff = man_bits
        .iter()
        .zip(dst_bits.iter())
        .filter(|(a, b)| a != b)
        .count();
    println!("cadeia manual == fwd? diffs = {diff} de {}", dst_bits.len());
    for i in 0..dst_bits.len() {
        if man_bits[i] != dst_bits[i] {
            println!(
                "  [{i}] manual {:08x} {:+.9e}  fwd {:08x} {:+.9e}",
                man_bits[i],
                f32::from_bits(man_bits[i]),
                dst_bits[i],
                f32::from_bits(dst_bits[i])
            );
        }
    }

    // ---- arquivo de bits ----
    let mut txt = String::new();
    txt.push_str(&format!("# order={order} n={n} chain_diffs={diff}\n"));
    txt.push_str("SRC\n");
    for v in &src {
        txt.push_str(&format!("{:08x}\n", v.to_bits()));
    }
    txt.push_str("KD\n");
    for v in &kd_bits {
        txt.push_str(&format!("{v:08x}\n"));
    }
    txt.push_str("MAN\n");
    for v in &man_bits {
        txt.push_str(&format!("{v:08x}\n"));
    }
    txt.push_str("FWD\n");
    for v in &dst_bits {
        txt.push_str(&format!("{v:08x}\n"));
    }
    txt.push_str("TW\n");
    for v in &tw {
        txt.push_str(&format!("{v:08x}\n"));
    }
    let path = format!("checks/.build/j4_stage_{order}.bits");
    std::fs::write(&path, txt).unwrap();
    println!("escrito {path} (TW = {} u32 de ctx+0x50, 2*n)", tw.len());

    unsafe {
        FreeLibrary(h);
    }
}
