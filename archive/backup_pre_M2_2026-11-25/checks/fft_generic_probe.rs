//! Sonda READ-ONLY do kernel genérico `0x1D69E00` (ordens 8..19).
//!
//! Chama, por RVA, direto no plugin carregado (`LoadLibraryW`; nenhum
//! patch/hook/injeção):
//!
//!   `0x1D69E00(src, dst, n/2, tw38, idx30, workspace)`
//!   `0x20E0(src, dst, spec, work)`            (referência)
//!
//! e grava em `checks/.build/j9_stage.bits`:
//!
//!   SRC  n f32      entrada determinística
//!   KD   n f32      saída do kernel sozinho
//!   FWD  n+2 f32    saída de `0x20E0`
//!   IDX  76 u32     tabela de índices (`ctx+0x30`, primeiros 64 dwords)
//!   TW38 512 f32    twiddles do kernel (`ctx+0x38`, 0x800 bytes)
//!   TW50 2n f32     twiddles do split (`ctx+0x50`)
//!
//! Build: rustc --edition 2021 -O checks\fft_generic_probe.rs -o checks\.build\fft_generic_probe.exe

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
type FnXform = unsafe extern "system" fn(*const f32, *mut f32, *mut u8, *mut u8) -> i32;
/// `0x1D69E00`: (src, dst, n/2, tw38, idx30, workspace) — 5º/6º na pilha.
type FnKernelGeneric = unsafe extern "system" fn(
    *const f32,
    *mut f32,
    i32,
    *const u8,
    *const u8,
    *mut u8,
);

const RVA_GETSIZE: usize = 0x4100;
const RVA_INIT: usize = 0x8840;
const RVA_FWD: usize = 0x20E0;
const RVA_KERNEL_GENERIC: usize = 0x1D69E00;

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

/// Lê `count` dwords de `addr` sem tocar página não commitada.
/// O que não estiver mapeado vira 0 (sentinela para o kernel).
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
        .unwrap_or(9);
    assert!((8..=19).contains(&order), "ordens 8..19 (rdx pode passar de 0x800)");

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
    let kernel: FnKernelGeneric = unsafe { std::mem::transmute(base + RVA_KERNEL_GENERIC) };

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
    let t_idx = unsafe { *((ctx + 0x30) as *const usize) };
    let t_tw38 = unsafe { *((ctx + 0x38) as *const usize) };
    let t_tw50 = unsafe { *((ctx + 0x50) as *const usize) };
    let ws_size = unsafe { *((ctx + 0x18) as *const i64) } as usize;
    let tw38_len = (t_tw50 - t_tw38) / 4;
    println!(
        "order={order} base=0x{base:x} ctx=0x{ctx:x} idx=0x{t_idx:x} tw38=0x{t_tw38:x} \
         tw50=0x{t_tw50:x} ws={ws_size} tw38_len={tw38_len}"
    );

    let n = 1usize << order;

    let mut rng = Rng(0x0F1E_2D3C_4B5A_6978);
    let mode = std::env::args().nth(2).unwrap_or_else(|| "rand".to_string());
    let mut src: Vec<f32> = (0..n).map(|_| rng.f32()).collect();
    if mode == "imp" {
        src = vec![0f32; n];
        src[0] = 1.0;
    } else if let Some(k) = mode.strip_prefix('e') {
        let k: usize = k.parse().unwrap();
        src = vec![0f32; n];
        src[k] = 1.0;
    }

    // O áudio chama com src == dst (`000725BD mov rcx,rdx` / `000725C4 mov rdx,rbx`);
    // assim `r9` (workspace) NÃO é trocado por `dst` (`01D69E80..01D69E8E`) e o
    // workspace que passamos continua sendo o usado — dá para lê-lo no fim.
    let mut kd = vec![0f32; n + 2];
    kd[..n].copy_from_slice(&src);
    eprintln!("calling kernel rdx={}", n / 2);
    unsafe {
        kernel(
            kd.as_ptr(),
            kd.as_mut_ptr(),
            (n / 2) as i32,
            t_tw38 as *const u8,
            t_idx as *const u8,
            work.p,
        )
    };
    let kd_bits: Vec<u32> = kd[..n].iter().map(|v| v.to_bits()).collect();
    eprintln!("kernel done");
    let ws_bits: Vec<u32> = (0..n)
        .map(|i| unsafe { *((work.p as *const f32).add(i)) }.to_bits())
        .collect();

    let mut dst = vec![0f32; n + 2];
    eprintln!("calling fwd");
    assert_eq!(
        unsafe { fwd(src.as_ptr(), dst.as_mut_ptr(), spec_ptr, work.p) },
        0
    );
    eprintln!("fwd done");
    let dst_bits: Vec<u32> = dst.iter().map(|v| v.to_bits()).collect();

    // A 1ª passada lê `idx[16], idx[32], …` em passos de 16 dwords e para no 0
    // sentinela. Os 16 primeiros dwords são lixo/zero e NÃO indicam o fim.
    // Ela roda `n/128` iterações, então a tabela tem `n/8 + 16` dwords.
    // Lemos com `VirtualQuery` para nunca tocar página não commitada (o crash
    // 0xC0000005 na ordem 19 vinha de ler além da alocação); o que faltar é 0.
    let idx_len = n / 8 + 16;
    let mut idx: Vec<u32> = Vec::with_capacity(idx_len);
    let mut addr = t_idx;
    while idx.len() < idx_len {
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
        let q = unsafe {
            VirtualQuery(
                addr as *const u8,
                &mut mbi,
                std::mem::size_of::<Mbi>(),
            )
        };
        if q == 0 || mbi.state != 0x1000 {
            break; // MEM_COMMIT
        }
        let end = mbi.base.saturating_add(mbi.region_size);
        if end <= addr {
            break;
        }
        let avail = (end - addr) / 4;
        let take = avail.min(idx_len - idx.len());
        for i in 0..take {
            idx.push(unsafe { *((addr + i * 4) as *const u32) });
        }
        addr += take * 4;
    }
    idx.resize(idx_len, 0); // o que não foi lido conta como sentinela 0
    let sentinel = (16..idx.len()).step_by(16).find(|&i| idx[i] == 0);
    eprintln!(
        "idx read: {} entries, sentinel at idx[{:?}]",
        idx.len(),
        sentinel
    );
    // `ctx+0x38` é a tabela do kernel e `ctx+0x50` a do split; o tamanho da
    // primeira é `tw50_ptr - tw38_ptr` (por ordem: 0x400/0x800/0x1000/0x2000/
    // 0x8000 B para as ordens 8/9/10/11/12).
    let tw38_len = (t_tw50 - t_tw38) / 4;
    eprintln!("reading tw38 len={tw38_len} @0x{t_tw38:x}");
    let tw38 = read_bits(t_tw38, tw38_len);
    eprintln!("tw38 ok");
    // Para ordens >= 17 a tabela do split não tem 2n floats alocados
    // (leitura de 2n sai da página → 0xC0000005); ler n é o que o split consome.
    let tw50_len = if order >= 17 { n } else { 2 * n };
    eprintln!("reading tw50 len={tw50_len}");
    let tw50 = read_bits(t_tw50, tw50_len);
    eprintln!("tw read: tw38={} tw50={}", tw38.len(), tw50.len());

    let mut txt = String::new();
    txt.push_str(&format!("# order={order} n={n}\n"));
    for (name, vals) in [
        ("SRC", src.iter().map(|v| v.to_bits()).collect::<Vec<_>>()),
        ("KD", kd_bits),
        ("WS", ws_bits),
        ("FWD", dst_bits),
        ("IDX", idx),
        ("TW38", tw38),
        ("TW50", tw50),
    ] {
        txt.push_str(name);
        txt.push('\n');
        for v in vals {
            txt.push_str(&format!("{v:08x}\n"));
        }
    }
    let path = format!("checks/.build/j{order}_stage_{mode}.bits");
    std::fs::write(&path, txt).unwrap();
    println!("escrito {path}");

    unsafe {
        FreeLibrary(h);
    }
}
