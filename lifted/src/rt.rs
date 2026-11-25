//! Runtime do código traduzido mecanicamente (M5): registradores, xmm de
//! 128 bits, flags e memória paginada. Cada instrução do binário vira uma
//! linha em `port/src/lifted/gen_*.rs` (gerado por `tools/lift/lift.py`), com o
//! RVA em comentário, na mesma ordem e com a mesma aritmética.
//!
//! - **Operações float:** usam intrinsics SSE (`_mm_add_ss` etc.), então o
//!   MXCSR corrente (arredondamento, FTZ/DAZ) vale como no hardware.
//! - **Imagem:** os endereços da imagem usam a base dos ponteiros de dado do
//!   dump (`0x199B0000`).
//!   - As páginas da imagem são lidas sob demanda de uma fonte só-leitura (o
//!     dump), com sobreposição copy-on-write para escritas em `.data`.
//!   - O conjunto de páginas tocadas é registrável, para congelar depois num
//!     blob embutido.

#![allow(clippy::all)]

use std::collections::HashMap;

pub const IMAGE_BASE: u64 = 0x199B_0000;
pub const IMAGE_SIZE: u64 = 0x0830_0000; // > 137.003.008 B
pub const HEAP_BASE: u64 = 0x0001_0000_0000;
pub const STACK_TOP: u64 = 0x0007_0000_0000;
pub const STACK_SIZE: u64 = 0x0040_0000; // 4 MiB

pub const RAX: usize = 0;
pub const RCX: usize = 1;
pub const RDX: usize = 2;
pub const RBX: usize = 3;
pub const RSP: usize = 4;
pub const RBP: usize = 5;
pub const RSI: usize = 6;
pub const RDI: usize = 7;
pub const R8: usize = 8;
pub const R9: usize = 9;

const PAGE: u64 = 4096;

thread_local! {
    /// RVA do último bloco básico iniciado (diagnóstico em mensagens de erro).
    pub static CUR: std::cell::Cell<u32> = const { std::cell::Cell::new(0) };
}

#[inline(always)]
pub fn set_cur(rva: u32) {
    CUR.with(|c| c.set(rva));
}

pub fn cur() -> u32 {
    CUR.with(|c| c.get())
}

/// Fonte só-leitura da imagem (bytes indexados por RVA).
pub trait ImageSource: Send {
    fn read_page(&self, rva: u64, out: &mut [u8; 4096]);
}

/// Dump inteiro em memória (`offset de arquivo = RVA`).
pub struct DumpImage(pub Vec<u8>);

impl ImageSource for DumpImage {
    fn read_page(&self, rva: u64, out: &mut [u8; 4096]) {
        let s = rva as usize;
        for (i, b) in out.iter_mut().enumerate() {
            *b = *self.0.get(s + i).unwrap_or(&0);
        }
    }
}

type Page = [u8; 4096];

/// Entradas do cache direto de páginas (endereço da página -> ponteiro).
const TLB: usize = 256;
/// Limite do índice de páginas do heap guardado em vetor (4 GiB); acima disso, mapa.
const HEAP_VEC_MAX: u64 = 1 << 20;
const STACK_LO: u64 = STACK_TOP - STACK_SIZE;

/// Memória emulada. Desempenho (não muda valores): páginas em vetores por região (imagem,
/// heap, pilha) com um cache direto `endereço de página -> ponteiro`; acessos de 1..16 bytes
/// dentro de uma página leem/escrevem direto, sem cópia por byte. As páginas são `Box` e
/// nunca são liberadas nem movidas, então os ponteiros do cache ficam válidos.
pub struct Mem {
    img: Vec<Option<Box<Page>>>,
    heap: Vec<Option<Box<Page>>>,
    stack: Vec<Option<Box<Page>>>,
    other: HashMap<u64, Box<Page>>,
    tlb_tag: [u64; TLB],
    tlb_ptr: [*mut Page; TLB],
    pub image: Option<Box<dyn ImageSource>>,
    /// Páginas da imagem lidas (RVA da página), para congelar.
    pub image_touched: std::collections::BTreeSet<u64>,
    pub heap_next: u64,
}

// Os ponteiros crus só apontam para páginas que o próprio `Mem` possui.
unsafe impl Send for Mem {}

impl Mem {
    pub fn new(image: Option<Box<dyn ImageSource>>) -> Mem {
        Mem {
            img: (0..IMAGE_SIZE / PAGE).map(|_| None).collect(),
            heap: Vec::new(),
            stack: (0..(STACK_TOP + PAGE - STACK_LO) / PAGE).map(|_| None).collect(),
            other: HashMap::new(),
            tlb_tag: [u64::MAX; TLB],
            tlb_ptr: [std::ptr::null_mut(); TLB],
            image,
            image_touched: Default::default(),
            heap_next: HEAP_BASE,
        }
    }

    #[inline(always)]
    fn page_ptr(&mut self, pa: u64) -> *mut Page {
        let i = ((pa >> 12) as usize) & (TLB - 1);
        if self.tlb_tag[i] == pa {
            return self.tlb_ptr[i];
        }
        let p = self.page_slow(pa);
        self.tlb_tag[i] = pa;
        self.tlb_ptr[i] = p;
        p
    }

    #[inline(never)]
    fn page_slow(&mut self, pa: u64) -> *mut Page {
        if pa >= IMAGE_BASE && pa < IMAGE_BASE + IMAGE_SIZE {
            let idx = ((pa - IMAGE_BASE) / PAGE) as usize;
            if self.img[idx].is_none() {
                let rva = pa - IMAGE_BASE;
                let mut p = Box::new([0u8; 4096]);
                match &self.image {
                    Some(img) => img.read_page(rva, &mut p),
                    None => panic!("leitura da imagem sem fonte: RVA 0x{rva:X}"),
                }
                self.image_touched.insert(rva);
                self.img[idx] = Some(p);
            }
            return &mut **self.img[idx].as_mut().unwrap() as *mut Page;
        }
        if pa >= STACK_LO && pa < STACK_TOP + PAGE {
            let idx = ((pa - STACK_LO) / PAGE) as usize;
            return &mut **self.stack[idx].get_or_insert_with(|| Box::new([0u8; 4096])) as *mut Page;
        }
        if pa >= HEAP_BASE && pa < STACK_TOP + PAGE {
            let idx = (pa - HEAP_BASE) / PAGE;
            if idx < HEAP_VEC_MAX {
                let idx = idx as usize;
                if idx >= self.heap.len() {
                    self.heap.resize_with(idx + 1, || None);
                }
                return &mut **self.heap[idx].get_or_insert_with(|| Box::new([0u8; 4096])) as *mut Page;
            }
            return &mut **self.other.entry(pa).or_insert_with(|| Box::new([0u8; 4096])) as *mut Page;
        }
        panic!("acesso fora das regiões conhecidas: 0x{pa:X} (bloco 0x{:X})", cur());
    }

    #[inline]
    fn page(&mut self, addr: u64) -> &mut Page {
        let p = self.page_ptr(addr & !(PAGE - 1));
        unsafe { &mut *p }
    }

    /// Leitura de `N` bytes; caminho direto quando não cruza página.
    #[inline(always)]
    fn rd<const N: usize>(&mut self, a: u64) -> [u8; N] {
        let off = (a & (PAGE - 1)) as usize;
        if off + N <= PAGE as usize {
            let p = self.page_ptr(a & !(PAGE - 1));
            unsafe { std::ptr::read_unaligned((p as *const u8).add(off) as *const [u8; N]) }
        } else {
            let mut b = [0u8; N];
            self.read(a, &mut b);
            b
        }
    }

    #[inline(always)]
    fn wr<const N: usize>(&mut self, a: u64, v: [u8; N]) {
        let off = (a & (PAGE - 1)) as usize;
        if off + N <= PAGE as usize {
            let p = self.page_ptr(a & !(PAGE - 1));
            unsafe { std::ptr::write_unaligned((p as *mut u8).add(off) as *mut [u8; N], v) }
        } else {
            self.write(a, &v);
        }
    }

    pub fn read(&mut self, addr: u64, out: &mut [u8]) {
        let mut a = addr;
        let mut i = 0;
        while i < out.len() {
            let off = (a & (PAGE - 1)) as usize;
            let n = (out.len() - i).min(PAGE as usize - off);
            let p = self.page(a);
            out[i..i + n].copy_from_slice(&p[off..off + n]);
            i += n;
            a += n as u64;
        }
    }

    pub fn write(&mut self, addr: u64, data: &[u8]) {
        let mut a = addr;
        let mut i = 0;
        while i < data.len() {
            let off = (a & (PAGE - 1)) as usize;
            let n = (data.len() - i).min(PAGE as usize - off);
            let p = self.page(a);
            p[off..off + n].copy_from_slice(&data[i..i + n]);
            i += n;
            a += n as u64;
        }
    }

    #[inline(always)]
    pub fn r8(&mut self, a: u64) -> u8 {
        self.rd::<1>(a)[0]
    }
    #[inline(always)]
    pub fn r16(&mut self, a: u64) -> u16 {
        u16::from_le_bytes(self.rd(a))
    }
    #[inline(always)]
    pub fn r32(&mut self, a: u64) -> u32 {
        u32::from_le_bytes(self.rd(a))
    }
    #[inline(always)]
    pub fn r64(&mut self, a: u64) -> u64 {
        u64::from_le_bytes(self.rd(a))
    }
    #[inline(always)]
    pub fn r128(&mut self, a: u64) -> u128 {
        u128::from_le_bytes(self.rd(a))
    }
    #[inline(always)]
    pub fn w8(&mut self, a: u64, v: u8) {
        self.wr(a, [v]);
    }
    #[inline(always)]
    pub fn w16(&mut self, a: u64, v: u16) {
        self.wr(a, v.to_le_bytes());
    }
    #[inline(always)]
    pub fn w32(&mut self, a: u64, v: u32) {
        self.wr(a, v.to_le_bytes());
    }
    #[inline(always)]
    pub fn w64(&mut self, a: u64, v: u64) {
        self.wr(a, v.to_le_bytes());
    }
    #[inline(always)]
    pub fn w128(&mut self, a: u64, v: u128) {
        self.wr(a, v.to_le_bytes());
    }

    /// Bump allocator do heap emulado (alinhamento 64).
    pub fn alloc(&mut self, size: u64) -> u64 {
        let a = (self.heap_next + 63) & !63;
        self.heap_next = a + size.max(1);
        assert!(self.heap_next < STACK_TOP - STACK_SIZE, "heap emulado esgotado");
        a
    }

    pub fn read_f32s(&mut self, a: u64, n: usize) -> Vec<f32> {
        (0..n).map(|i| f32::from_bits(self.r32(a + 4 * i as u64))).collect()
    }
    pub fn write_f32s(&mut self, a: u64, v: &[f32]) {
        for (i, x) in v.iter().enumerate() {
            self.w32(a + 4 * i as u64, x.to_bits());
        }
    }
}

pub struct Cpu {
    pub r: [u64; 16],
    pub x: [u128; 16],
    /// Metade alta (bits 255:128) dos ymm. Instruções SSE legadas preservam;
    /// VEX.128 zera; VEX.256 escreve.
    pub y: [u128; 16],
    pub zf: bool,
    pub sf: bool,
    pub cf: bool,
    pub of: bool,
    pub pf: bool,
    pub mem: Mem,
    /// Contador de instruções executadas (diagnóstico).
    pub icount: u64,
    /// Flag de direção (std/cld) para `rep movs/stos`.
    pub df: bool,
    /// Guards de inicialização estática já vistos nesta emulação (`0x17969E0`).
    pub static_guards: std::collections::HashSet<u64>,
    /// `gs:[0x58]` (ThreadLocalStoragePointer) emulado: array de ponteiros para blocos
    /// TLS zerados, alocado sob demanda.
    pub tls: u64,
    /// RVA do bloco básico corrente (diagnóstico).
    pub cur: u32,
    /// Perfil opcional: RVA do bloco -> (execuções, instruções). Ligado por `prof_on()`.
    pub prof: Option<Box<HashMap<u32, (u64, u64)>>>,
}

impl Cpu {
    pub fn new(mem: Mem) -> Cpu {
        let mut c = Cpu {
            r: [0; 16],
            x: [0; 16],
            y: [0; 16],
            zf: false,
            sf: false,
            cf: false,
            of: false,
            pf: false,
            mem,
            icount: 0,
            df: false,
            static_guards: Default::default(),
            tls: 0,
            cur: 0,
            prof: None,
        };
        c.r[RSP] = STACK_TOP - 0x100;
        c
    }

    /// Leitura de `gs:[disp]` (TEB). Só `0x58` (TLS) é emulado; o resto para.
    /// Entrada de bloco básico (emitida por `tools/lift/lift.py`): RVA corrente, contador de
    /// instruções do bloco e perfil opcional. Não toca registradores, flags nem memória.
    #[inline(always)]
    pub fn blk(&mut self, rva: u32, n: u64) {
        self.cur = rva;
        self.icount += n;
        if self.prof.is_some() {
            self.prof_hit(rva, n);
        }
    }

    #[inline(never)]
    fn prof_hit(&mut self, rva: u32, n: u64) {
        let e = self.prof.as_mut().unwrap().entry(rva).or_insert((0, 0));
        e.0 += 1;
        e.1 += n;
    }

    pub fn prof_on(&mut self) {
        self.prof = Some(Box::default());
    }

    pub fn gs_read(&mut self, disp: u64, site: u32) -> u64 {
        match disp {
            0x58 => {
                if self.tls == 0 {
                    let arr = self.mem.alloc(64 * 8);
                    for i in 0..64u64 {
                        let blk = self.mem.alloc(0x1000);
                        // _Init_thread_epoch (TLS +0x10) começa em INT_MIN num processo novo
                        // (os guards do dump, ex. [0x2754C5C] = 0x80000018, comparam com ele).
                        self.mem.w32(blk + 0x10, 0x8000_0000);
                        self.mem.w64(arr + 8 * i, blk);
                    }
                    self.tls = arr;
                }
                self.tls
            }
            _ => panic!("gs:[0x{disp:X}] não emulado em 0x{site:X}"),
        }
    }

    #[inline]
    pub fn push(&mut self, v: u64) {
        self.r[RSP] = self.r[RSP].wrapping_sub(8);
        let sp = self.r[RSP];
        self.mem.w64(sp, v);
    }
    #[inline]
    pub fn pop(&mut self) -> u64 {
        let sp = self.r[RSP];
        let v = self.mem.r64(sp);
        self.r[RSP] = sp.wrapping_add(8);
        v
    }

    // ---- registradores parciais ----
    #[inline]
    pub fn g8(&self, i: usize) -> u8 {
        self.r[i] as u8
    }
    #[inline]
    pub fn g16(&self, i: usize) -> u16 {
        self.r[i] as u16
    }
    #[inline]
    pub fn g32(&self, i: usize) -> u32 {
        self.r[i] as u32
    }
    #[inline]
    pub fn s8(&mut self, i: usize, v: u8) {
        self.r[i] = (self.r[i] & !0xFF) | v as u64;
    }
    #[inline]
    pub fn s16(&mut self, i: usize, v: u16) {
        self.r[i] = (self.r[i] & !0xFFFF) | v as u64;
    }
    #[inline]
    pub fn s32(&mut self, i: usize, v: u32) {
        self.r[i] = v as u64; // escrita de 32 bits zera a metade alta
    }

    // ---- flags ----
    #[inline]
    #[inline(always)]
    fn parity(v: u64) -> bool {
        (v as u8).count_ones() % 2 == 0
    }

    #[inline(always)]
    pub fn fl_logic(&mut self, res: u64, bits: u32) {
        let m = mask(bits);
        let r = res & m;
        self.zf = r == 0;
        self.sf = (r >> (bits - 1)) & 1 == 1;
        self.cf = false;
        self.of = false;
        self.pf = Self::parity(r);
    }

    #[inline(always)]
    pub fn fl_add(&mut self, a: u64, b: u64, bits: u32) -> u64 {
        let m = mask(bits);
        let (a, b) = (a & m, b & m);
        let r = a.wrapping_add(b) & m;
        let sb = 1u64 << (bits - 1);
        self.zf = r == 0;
        self.sf = r & sb != 0;
        self.cf = if bits == 64 { a.checked_add(b).is_none() } else { a + b > m };
        self.of = ((a ^ r) & (b ^ r) & sb) != 0;
        self.pf = Self::parity(r);
        r
    }

    #[inline(always)]
    pub fn fl_sub(&mut self, a: u64, b: u64, bits: u32) -> u64 {
        let m = mask(bits);
        let (a, b) = (a & m, b & m);
        let r = a.wrapping_sub(b) & m;
        let sb = 1u64 << (bits - 1);
        self.zf = r == 0;
        self.sf = r & sb != 0;
        self.cf = a < b;
        self.of = ((a ^ b) & (a ^ r) & sb) != 0;
        self.pf = Self::parity(r);
        r
    }

    /// inc/dec preservam CF.
    #[inline(always)]
    pub fn fl_incdec(&mut self, a: u64, inc: bool, bits: u32) -> u64 {
        let cf = self.cf;
        let r = if inc { self.fl_add(a, 1, bits) } else { self.fl_sub(a, 1, bits) };
        self.cf = cf;
        r
    }

    /// comiss/comisd/ucomis*: ZF,PF,CF; OF=SF=0.
    #[inline(always)]
    pub fn fl_comi(&mut self, unordered: bool, lt: bool, eq: bool) {
        self.of = false;
        self.sf = false;
        if unordered {
            self.zf = true;
            self.pf = true;
            self.cf = true;
        } else {
            self.zf = eq;
            self.pf = false;
            self.cf = lt;
        }
    }

    // condições
    #[inline]
    pub fn c_e(&self) -> bool {
        self.zf
    }
    #[inline]
    pub fn c_a(&self) -> bool {
        !self.cf && !self.zf
    }
    #[inline]
    pub fn c_ae(&self) -> bool {
        !self.cf
    }
    #[inline]
    pub fn c_b(&self) -> bool {
        self.cf
    }
    #[inline]
    pub fn c_be(&self) -> bool {
        self.cf || self.zf
    }
    #[inline]
    pub fn c_l(&self) -> bool {
        self.sf != self.of
    }
    #[inline]
    pub fn c_ge(&self) -> bool {
        self.sf == self.of
    }
    #[inline]
    pub fn c_le(&self) -> bool {
        self.zf || self.sf != self.of
    }
    #[inline]
    pub fn c_g(&self) -> bool {
        !self.zf && self.sf == self.of
    }
    #[inline]
    pub fn c_s(&self) -> bool {
        self.sf
    }
    #[inline]
    pub fn c_p(&self) -> bool {
        self.pf
    }
}

#[inline]
pub fn mask(bits: u32) -> u64 {
    if bits == 64 { u64::MAX } else { (1u64 << bits) - 1 }
}

// ---------------------------------------------------------------------------
// SSE: operações escalares sobre o u128 do registrador, pelas intrinsics (MXCSR
// corrente vale, como no hardware).
// ---------------------------------------------------------------------------

pub mod sse {
    use std::arch::x86_64::*;

    #[inline]
    pub fn ps(v: u128) -> __m128 {
        unsafe { std::mem::transmute(v) }
    }
    #[inline]
    pub fn pd(v: u128) -> __m128d {
        unsafe { std::mem::transmute(v) }
    }
    #[inline]
    pub fn ui(v: __m128i) -> u128 {
        unsafe { std::mem::transmute(v) }
    }
    #[inline]
    pub fn si(v: u128) -> __m128i {
        unsafe { std::mem::transmute(v) }
    }
    #[inline]
    pub fn ups(v: __m128) -> u128 {
        unsafe { std::mem::transmute(v) }
    }
    #[inline]
    pub fn upd(v: __m128d) -> u128 {
        unsafe { std::mem::transmute(v) }
    }

    macro_rules! ss2 {
        ($name:ident, $intr:ident) => {
            #[inline]
            pub fn $name(a: u128, b: u128) -> u128 {
                unsafe { ups($intr(ps(a), ps(b))) }
            }
        };
    }
    macro_rules! sd2 {
        ($name:ident, $intr:ident) => {
            #[inline]
            pub fn $name(a: u128, b: u128) -> u128 {
                unsafe { upd($intr(pd(a), pd(b))) }
            }
        };
    }
    ss2!(addss, _mm_add_ss);
    ss2!(subss, _mm_sub_ss);
    ss2!(mulss, _mm_mul_ss);
    ss2!(divss, _mm_div_ss);
    ss2!(minss, _mm_min_ss);
    ss2!(maxss, _mm_max_ss);
    ss2!(addps, _mm_add_ps);
    ss2!(subps, _mm_sub_ps);
    ss2!(mulps, _mm_mul_ps);
    ss2!(divps, _mm_div_ps);
    ss2!(minps, _mm_min_ps);
    ss2!(maxps, _mm_max_ps);
    sd2!(addsd, _mm_add_sd);
    sd2!(subsd, _mm_sub_sd);
    sd2!(mulsd, _mm_mul_sd);
    sd2!(divsd, _mm_div_sd);
    sd2!(minsd, _mm_min_sd);
    sd2!(maxsd, _mm_max_sd);
    sd2!(addpd, _mm_add_pd);
    sd2!(mulpd, _mm_mul_pd);
    sd2!(subpd, _mm_sub_pd);
    sd2!(divpd, _mm_div_pd);

    #[inline]
    pub fn sqrtss(a: u128, b: u128) -> u128 {
        unsafe { ups(_mm_sqrt_ss(_mm_move_ss(ps(a), ps(b)))) }
    }
    #[inline]
    pub fn sqrtsd(a: u128, b: u128) -> u128 {
        unsafe { upd(_mm_sqrt_sd(pd(a), pd(b))) }
    }
    /// cvtss2sd dst, src: low f64 = (double)src.f32[0]; resto de dst preservado.
    #[inline]
    pub fn cvtss2sd(dst: u128, src: u128) -> u128 {
        unsafe { upd(_mm_cvtss_sd(pd(dst), ps(src))) }
    }
    #[inline]
    pub fn cvtsd2ss(dst: u128, src: u128) -> u128 {
        unsafe { ups(_mm_cvtsd_ss(ps(dst), pd(src))) }
    }
    #[inline]
    pub fn cvtps2pd(src: u128) -> u128 {
        unsafe { upd(_mm_cvtps_pd(ps(src))) }
    }
    #[inline]
    pub fn cvtpd2ps(src: u128) -> u128 {
        unsafe { ups(_mm_cvtpd_ps(pd(src))) }
    }
    #[inline]
    pub fn cvtdq2ps(src: u128) -> u128 {
        unsafe { ups(_mm_cvtepi32_ps(si(src))) }
    }
    #[inline]
    pub fn cvtdq2pd(src: u128) -> u128 {
        unsafe { upd(_mm_cvtepi32_pd(si(src))) }
    }
    #[inline]
    pub fn cvttps2dq(src: u128) -> u128 {
        unsafe { ui(_mm_cvttps_epi32(ps(src))) }
    }
    #[inline]
    pub fn cvtps2dq(src: u128) -> u128 {
        unsafe { ui(_mm_cvtps_epi32(ps(src))) }
    }
    #[inline]
    pub fn cvtsi2ss32(dst: u128, v: i32) -> u128 {
        unsafe { ups(_mm_cvtsi32_ss(ps(dst), v)) }
    }
    #[inline]
    pub fn cvtsi2ss64(dst: u128, v: i64) -> u128 {
        unsafe { ups(_mm_cvtsi64_ss(ps(dst), v)) }
    }
    #[inline]
    pub fn cvtsi2sd32(dst: u128, v: i32) -> u128 {
        unsafe { upd(_mm_cvtsi32_sd(pd(dst), v)) }
    }
    #[inline]
    pub fn cvtsi2sd64(dst: u128, v: i64) -> u128 {
        unsafe { upd(_mm_cvtsi64_sd(pd(dst), v)) }
    }
    #[inline]
    pub fn cvttss2si32(v: u128) -> i32 {
        unsafe { _mm_cvttss_si32(ps(v)) }
    }
    #[inline]
    pub fn cvttss2si64(v: u128) -> i64 {
        unsafe { _mm_cvttss_si64(ps(v)) }
    }
    #[inline]
    pub fn cvttsd2si32(v: u128) -> i32 {
        unsafe { _mm_cvttsd_si32(pd(v)) }
    }
    #[inline]
    pub fn cvttsd2si64(v: u128) -> i64 {
        unsafe { _mm_cvttsd_si64(pd(v)) }
    }
    #[inline]
    pub fn cvtss2si32(v: u128) -> i32 {
        unsafe { _mm_cvtss_si32(ps(v)) }
    }
    #[inline]
    pub fn cvtsd2si32(v: u128) -> i32 {
        unsafe { _mm_cvtsd_si32(pd(v)) }
    }

    /// (unordered, lt, eq) de comiss.
    #[inline]
    pub fn cmp_ss(a: u128, b: u128) -> (bool, bool, bool) {
        let x = f32::from_bits(a as u32);
        let y = f32::from_bits(b as u32);
        (x.is_nan() || y.is_nan(), x < y, x == y)
    }
    #[inline]
    pub fn cmp_sd(a: u128, b: u128) -> (bool, bool, bool) {
        let x = f64::from_bits(a as u64);
        let y = f64::from_bits(b as u64);
        (x.is_nan() || y.is_nan(), x < y, x == y)
    }

    #[inline]
    pub fn shufps(a: u128, b: u128, imm: u8) -> u128 {
        let la = lanes32(a);
        let lb = lanes32(b);
        from32([
            la[(imm & 3) as usize],
            la[((imm >> 2) & 3) as usize],
            lb[((imm >> 4) & 3) as usize],
            lb[((imm >> 6) & 3) as usize],
        ])
    }
    #[inline]
    pub fn pshufd(a: u128, imm: u8) -> u128 {
        let l = lanes32(a);
        from32([
            l[(imm & 3) as usize],
            l[((imm >> 2) & 3) as usize],
            l[((imm >> 4) & 3) as usize],
            l[((imm >> 6) & 3) as usize],
        ])
    }
    #[inline]
    pub fn unpcklps(a: u128, b: u128) -> u128 {
        let (x, y) = (lanes32(a), lanes32(b));
        from32([x[0], y[0], x[1], y[1]])
    }
    #[inline]
    pub fn unpckhps(a: u128, b: u128) -> u128 {
        let (x, y) = (lanes32(a), lanes32(b));
        from32([x[2], y[2], x[3], y[3]])
    }
    #[inline]
    pub fn lanes32(v: u128) -> [u32; 4] {
        [v as u32, (v >> 32) as u32, (v >> 64) as u32, (v >> 96) as u32]
    }
    #[inline]
    pub fn from32(l: [u32; 4]) -> u128 {
        l[0] as u128 | (l[1] as u128) << 32 | (l[2] as u128) << 64 | (l[3] as u128) << 96
    }
    #[inline]
    pub fn lanes64(v: u128) -> [u64; 2] {
        [v as u64, (v >> 64) as u64]
    }
    #[inline]
    pub fn from64(l: [u64; 2]) -> u128 {
        l[0] as u128 | (l[1] as u128) << 64
    }
}

// ---------------------------------------------------------------------------
// AVX/FMA por metades de 128 bits (resultado por lane idêntico ao ymm).
// ---------------------------------------------------------------------------
pub mod avx {
    use super::sse::*;
    use std::arch::x86_64::*;

    #[target_feature(enable = "fma")]
    unsafe fn fmadd_ps_(a: __m128, b: __m128, c: __m128) -> __m128 {
        _mm_fmadd_ps(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fmadd_ss_(a: __m128, b: __m128, c: __m128) -> __m128 {
        _mm_fmadd_ss(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fmsub_ps_(a: __m128, b: __m128, c: __m128) -> __m128 {
        _mm_fmsub_ps(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fnmadd_ps_(a: __m128, b: __m128, c: __m128) -> __m128 {
        _mm_fnmadd_ps(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fnmadd_ss_(a: __m128, b: __m128, c: __m128) -> __m128 {
        _mm_fnmadd_ss(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fmsub_ss_(a: __m128, b: __m128, c: __m128) -> __m128 {
        _mm_fmsub_ss(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fmadd_sd_(a: __m128d, b: __m128d, c: __m128d) -> __m128d {
        _mm_fmadd_sd(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fnmadd_sd_(a: __m128d, b: __m128d, c: __m128d) -> __m128d {
        _mm_fnmadd_sd(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fmsub_sd_(a: __m128d, b: __m128d, c: __m128d) -> __m128d {
        _mm_fmsub_sd(a, b, c)
    }

    /// a·b + c (packed, 4 lanes)
    pub fn fmadd_ps(a: u128, b: u128, c: u128) -> u128 {
        unsafe { ups(fmadd_ps_(ps(a), ps(b), ps(c))) }
    }
    pub fn fmsub_ps(a: u128, b: u128, c: u128) -> u128 {
        unsafe { ups(fmsub_ps_(ps(a), ps(b), ps(c))) }
    }
    pub fn fnmadd_ps(a: u128, b: u128, c: u128) -> u128 {
        unsafe { ups(fnmadd_ps_(ps(a), ps(b), ps(c))) }
    }
    /// lane 0 = a0·b0 + c0; lanes 1..3 de a.
    pub fn fmadd_ss(a: u128, b: u128, c: u128) -> u128 {
        unsafe { ups(fmadd_ss_(ps(a), ps(b), ps(c))) }
    }
    pub fn fmsub_ss(a: u128, b: u128, c: u128) -> u128 {
        unsafe { ups(fmsub_ss_(ps(a), ps(b), ps(c))) }
    }
    pub fn fnmadd_ss(a: u128, b: u128, c: u128) -> u128 {
        unsafe { ups(fnmadd_ss_(ps(a), ps(b), ps(c))) }
    }
    pub fn fmadd_sd(a: u128, b: u128, c: u128) -> u128 {
        unsafe { upd(fmadd_sd_(pd(a), pd(b), pd(c))) }
    }
    /// -(a·b + c) com um arredondamento: FMA com o sinal invertido (exato).
    pub fn fnmsub_ss(a: u128, b: u128, c: u128) -> u128 {
        fmadd_ss(a, b, c) ^ 0x8000_0000u128
    }
    pub fn fnmsub_ps(a: u128, b: u128, c: u128) -> u128 {
        fmadd_ps(a, b, c) ^ 0x8000_0000_8000_0000_8000_0000_8000_0000u128
    }
    pub fn fnmsub_sd(a: u128, b: u128, c: u128) -> u128 {
        fmadd_sd(a, b, c) ^ 0x8000_0000_0000_0000u128
    }
    pub fn fnmadd_sd(a: u128, b: u128, c: u128) -> u128 {
        unsafe { upd(fnmadd_sd_(pd(a), pd(b), pd(c))) }
    }
    pub fn fmsub_sd(a: u128, b: u128, c: u128) -> u128 {
        unsafe { upd(fmsub_sd_(pd(a), pd(b), pd(c))) }
    }
    /// vblendvps por metade: lane de b onde o bit de sinal de m é 1.
    pub fn blendv_ps(a: u128, b: u128, m: u128) -> u128 {
        let (a, b, m) = (lanes32(a), lanes32(b), lanes32(m));
        let mut r = [0u32; 4];
        for i in 0..4 {
            r[i] = if m[i] >> 31 == 1 { b[i] } else { a[i] };
        }
        from32(r)
    }
    pub fn broadcast32(v: u32) -> u128 {
        from32([v, v, v, v])
    }
    pub fn rcp_ps(a: u128) -> u128 {
        unsafe { ups(_mm_rcp_ps(ps(a))) }
    }
    pub fn cmp_ps(a: u128, b: u128, pred: u8) -> u128 {
        let (x, y) = (lanes32(a), lanes32(b));
        let mut r = [0u32; 4];
        for i in 0..4 {
            let (p, q) = (f32::from_bits(x[i]), f32::from_bits(y[i]));
            let un = p.is_nan() || q.is_nan();
            let t = match pred & 0x1F {
                0 | 0x10 => !un && p == q,          // EQ_OQ / EQ_OS
                1 | 0x11 => !un && p < q,           // LT
                2 | 0x12 => !un && p <= q,          // LE
                3 | 0x13 => un,                      // UNORD
                4 | 0x14 => un || p != q,           // NEQ_UQ
                5 | 0x15 => un || !(p < q),         // NLT
                6 | 0x16 => un || !(p <= q),        // NLE
                7 | 0x17 => !un,                     // ORD
                0x0C | 0x1C => !un && p != q,       // NEQ_OQ / NEQ_OS
                0x0D | 0x1D => !un && p >= q,       // GE_OS / GE_OQ
                0x0E | 0x1E => !un && p > q,        // GT_OS / GT_OQ
                0x09 | 0x19 => un || p < q,         // NGE
                0x0A | 0x1A => un || p <= q,        // NGT
                _ => panic!("predicado vcmpps 0x{pred:X} não suportado"),
            };
            r[i] = if t { u32::MAX } else { 0 };
        }
        from32(r)
    }
}

// ---------------------------------------------------------------------------
// Inteiros por lane (32 bits) e conversões VEX, por metade de 128 bits.
// ---------------------------------------------------------------------------
pub mod ilane {
    use super::sse::{from32, from64, lanes32, lanes64};
    pub fn map2(a: u128, b: u128, f: impl Fn(u32, u32) -> u32) -> u128 {
        let (x, y) = (lanes32(a), lanes32(b));
        from32([f(x[0], y[0]), f(x[1], y[1]), f(x[2], y[2]), f(x[3], y[3])])
    }
    pub fn paddd(a: u128, b: u128) -> u128 {
        map2(a, b, |p, q| p.wrapping_add(q))
    }
    pub fn psubd(a: u128, b: u128) -> u128 {
        map2(a, b, |p, q| p.wrapping_sub(q))
    }
    pub fn pcmpeqd(a: u128, b: u128) -> u128 {
        map2(a, b, |p, q| if p == q { u32::MAX } else { 0 })
    }
    pub fn pcmpgtd(a: u128, b: u128) -> u128 {
        map2(a, b, |p, q| if (p as i32) > (q as i32) { u32::MAX } else { 0 })
    }
    pub fn pslld(a: u128, n: u64) -> u128 {
        if n > 31 { 0 } else { map2(a, 0, |p, _| p << n) }
    }
    pub fn psrld(a: u128, n: u64) -> u128 {
        if n > 31 { 0 } else { map2(a, 0, |p, _| p >> n) }
    }
    pub fn psrad(a: u128, n: u64) -> u128 {
        let n = n.min(31);
        map2(a, 0, |p, _| ((p as i32) >> n) as u32)
    }
    pub fn punpcklqdq(a: u128, b: u128) -> u128 {
        from64([lanes64(a)[0], lanes64(b)[0]])
    }
    pub fn punpckhqdq(a: u128, b: u128) -> u128 {
        from64([lanes64(a)[1], lanes64(b)[1]])
    }
    pub fn punpckldq(a: u128, b: u128) -> u128 {
        let (x, y) = (lanes32(a), lanes32(b));
        from32([x[0], y[0], x[1], y[1]])
    }
    pub fn punpckhdq(a: u128, b: u128) -> u128 {
        let (x, y) = (lanes32(a), lanes32(b));
        from32([x[2], y[2], x[3], y[3]])
    }
    pub fn movmskps(lo: u128, hi: u128, n: usize) -> u64 {
        let mut m = 0u64;
        for i in 0..n {
            let v = if i < 4 { lanes32(lo)[i] } else { lanes32(hi)[i - 4] };
            m |= ((v >> 31) as u64) << i;
        }
        m
    }
    /// `vrsqrtps`: aproximação do hardware (como `vrcpps`, bit a bit só na mesma CPU).
    pub fn rsqrt_ps(a: u128) -> u128 {
        use std::arch::x86_64::*;
        unsafe { super::sse::ups(_mm_rsqrt_ps(super::sse::ps(a))) }
    }
}

pub fn get_mxcsr() -> u32 {
    #[allow(deprecated)]
    unsafe {
        std::arch::x86_64::_mm_getcsr()
    }
}

pub fn set_mxcsr(v: u32) {
    #[allow(deprecated)]
    unsafe {
        std::arch::x86_64::_mm_setcsr(v)
    }
}

// ---------------------------------------------------------------------------
// Double/FMA-pd, addsub, permps, TLS (gs:[0x58]).
// ---------------------------------------------------------------------------
pub mod avxd {
    use super::sse::*;
    use std::arch::x86_64::*;
    #[target_feature(enable = "fma")]
    unsafe fn fmadd_pd_(a: __m128d, b: __m128d, c: __m128d) -> __m128d {
        _mm_fmadd_pd(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fmsub_pd_(a: __m128d, b: __m128d, c: __m128d) -> __m128d {
        _mm_fmsub_pd(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fnmadd_pd_(a: __m128d, b: __m128d, c: __m128d) -> __m128d {
        _mm_fnmadd_pd(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fmaddsub_ps_(a: __m128, b: __m128, c: __m128) -> __m128 {
        _mm_fmaddsub_ps(a, b, c)
    }
    #[target_feature(enable = "fma")]
    unsafe fn fmsubadd_ps_(a: __m128, b: __m128, c: __m128) -> __m128 {
        _mm_fmsubadd_ps(a, b, c)
    }
    pub fn fmadd_pd(a: u128, b: u128, c: u128) -> u128 {
        unsafe { upd(fmadd_pd_(pd(a), pd(b), pd(c))) }
    }
    pub fn fmsub_pd(a: u128, b: u128, c: u128) -> u128 {
        unsafe { upd(fmsub_pd_(pd(a), pd(b), pd(c))) }
    }
    pub fn fnmadd_pd(a: u128, b: u128, c: u128) -> u128 {
        unsafe { upd(fnmadd_pd_(pd(a), pd(b), pd(c))) }
    }
    pub fn fmaddsub_ps(a: u128, b: u128, c: u128) -> u128 {
        unsafe { ups(fmaddsub_ps_(ps(a), ps(b), ps(c))) }
    }
    pub fn fmsubadd_ps(a: u128, b: u128, c: u128) -> u128 {
        unsafe { ups(fmsubadd_ps_(ps(a), ps(b), ps(c))) }
    }
    pub fn addsub_ps(a: u128, b: u128) -> u128 {
        unsafe { ups(_mm_addsub_ps(ps(a), ps(b))) }
    }
    pub fn addsub_pd(a: u128, b: u128) -> u128 {
        unsafe { upd(_mm_addsub_pd(pd(a), pd(b))) }
    }
    pub fn hadd_pd(a: u128, b: u128) -> u128 {
        unsafe { upd(_mm_hadd_pd(pd(a), pd(b))) }
    }
    pub fn hadd_ps(a: u128, b: u128) -> u128 {
        unsafe { ups(_mm_hadd_ps(ps(a), ps(b))) }
    }
    pub fn max_pd(a: u128, b: u128) -> u128 {
        unsafe { upd(_mm_max_pd(pd(a), pd(b))) }
    }
    pub fn min_pd(a: u128, b: u128) -> u128 {
        unsafe { upd(_mm_min_pd(pd(a), pd(b))) }
    }
    pub fn sqrt_sd(a: u128, b: u128) -> u128 {
        unsafe { upd(_mm_sqrt_sd(pd(a), pd(b))) }
    }
    pub fn sqrt_ps(a: u128) -> u128 {
        unsafe { ups(_mm_sqrt_ps(ps(a))) }
    }
    pub fn sqrt_pd(a: u128) -> u128 {
        unsafe { upd(_mm_sqrt_pd(pd(a))) }
    }
    /// cvtps2pd de 4 floats (256 bits de saída) a partir de 128 bits.
    pub fn cvtps2pd_256(a: u128) -> (u128, u128) {
        let l = lanes32(a);
        let f = |x: u32| (f32::from_bits(x) as f64).to_bits();
        (from64([f(l[0]), f(l[1])]), from64([f(l[2]), f(l[3])]))
    }
    /// cvtpd2ps de 4 doubles (256 bits de entrada) para 128 bits.
    pub fn cvtpd2ps_256(lo: u128, hi: u128) -> u128 {
        unsafe {
            let a = _mm_cvtpd_ps(pd(lo));
            let b = _mm_cvtpd_ps(pd(hi));
            ups(_mm_movelh_ps(a, b))
        }
    }
    /// vpermps (8 lanes): r[i] = src[idx[i] & 7].
    pub fn permps(idx_lo: u128, idx_hi: u128, s_lo: u128, s_hi: u128) -> (u128, u128) {
        let s = [lanes32(s_lo), lanes32(s_hi)].concat();
        let i = [lanes32(idx_lo), lanes32(idx_hi)].concat();
        let r: Vec<u32> = (0..8).map(|k| s[(i[k] & 7) as usize]).collect();
        (from32([r[0], r[1], r[2], r[3]]), from32([r[4], r[5], r[6], r[7]]))
    }
    pub fn moveldup(a: u128) -> u128 {
        let l = lanes32(a);
        from32([l[0], l[0], l[2], l[2]])
    }
    pub fn movehdup(a: u128) -> u128 {
        let l = lanes32(a);
        from32([l[1], l[1], l[3], l[3]])
    }
}
