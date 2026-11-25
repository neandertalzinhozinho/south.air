//! Etapa J5 — caminho de canal e saida (N/O) em Rust.
//!
//! Fonte: `dumpsooth/nyx_soothe3_dump.bin` (SHA-256
//! `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`).
//!
//! Transcreve **so o que tem instrucao + RVA**:
//!
//! 1. os tres descritores de ring contiguos de `0x90 B` (base, `+0x90`, `+0x120`);
//! 2. a guarda de espaco e o avanco `(i + n) & (len - 1)`;
//! 3. o ganho unico do caminho de saida `gain = (float)arg2 / (float)arg3`
//!    (`008AD06B`..`008AD0B9`, `divss xmm6,xmm0`);
//! 4. `0x8BAA10` = zerar planos (`0x10D0` -> `0x2F60`, `memset 4*len`);
//! 5. `0x8BAB60` = `dst[i] += src[i] * gain`, via `0x11F0` -> `0x5BC0`
//!    (`00005C46 vfmadd213ss xmm0,xmm1,[r8+r10*4]`).
//!
//! `NAO EXTRAIDO` (com RVA de parada, nunca aproximado):
//!
//! * layout de `+0x08..+0x7F` do descritor de ring (`0x868840`); o codigo usa
//!   apenas `+0x00 plane`, `+0x80 write`, `+0x84 read`, `+0x88 len`, `+0x8C nch`;
//! * o mapeamento exato "qual buffer entra em `0x8BAB60`" dentro de `0x8ACC40`
//!   (a chamada esta em `008AD21D`, o argumento vem de listas montadas por
//!   `0x86F170`; a lista nao foi atribuida a A/B). Aqui o overlap-add e exposto
//!   como funcao pura sobre um descritor escolhido pelo chamador;
//! * a semantica de `nch > 1` no plano (`+0x00`): `0x8688B0` aloca `4*len`
//!   bytes para um descritor, mas `0x899940` percorre `[desc+0x8C]` canais
//!   (`00899C11`/`00899F21`). A ligacao plano->canais fica `NAO EXTRAIDA`;
//!   as funcoes abaixo tratam um plano mono por descritor.
//!
//! `rustc --edition 2021 --test checks\stage_j_chan.rs -o checks\.build\j5.exe`

#![allow(dead_code)]

use core::mem::size_of;

pub const RING_BYTES: usize = 0x90;
/// `00870790`/`00873D5D` empilham o literal `0x10000`; `008688CC` grava em `+0x88`.
pub const RING_LEN: i32 = 0x10000;

/// Descritor de ring de `0x90 B` (layout provado em `checks/o_saida.md` §8/§10.6).
#[repr(C)]
pub struct RingDesc {
    /// `+0x00` — `00868930 mov [rsi],rax` (plano alocado com `4*len` bytes).
    pub plane: *mut f32,
    /// `+0x08..+0x7F` — `NAO EXTRAIDO: 0x868840`.
    pub unknown: [u8; 0x78],
    /// `+0x80` — `008AD26C`/`008AD280`.
    pub write: i32,
    /// `+0x84` — `008ACCF7`/`008ACD0E`, `008ACC66`.
    pub read: i32,
    /// `+0x88` — `008688CC`, `008ACC75`.
    pub len: i32,
    /// `+0x8C` — `008688D4`.
    pub nch: i32,
}

impl RingDesc {
    /// Descritor com o comprimento de `0x8688B0` (`0x10000`). `plane` aponta para
    /// `len` floats (mono).
    pub fn new(plane: *mut f32) -> Self {
        RingDesc {
            plane,
            unknown: [0; 0x78],
            write: 0,
            read: 0,
            len: RING_LEN,
            nch: 1,
        }
    }

    /// `008ACC5D`..`008ACC82`: `disponivel = (write - read) & (len - 1)`.
    #[inline]
    pub fn available(&self) -> i32 {
        self.write.wrapping_sub(self.read) & (self.len - 1)
    }

    /// `008ACD06`..`008ACD0E` (desc A) e `008ACD6B`..`008ACD79` (desc B).
    #[inline]
    pub fn advance_read(&mut self, n: i32) {
        self.read = self.read.wrapping_add(n) & (self.len - 1);
    }

    /// `008AD278`..`008AD280`.
    #[inline]
    pub fn advance_write(&mut self, n: i32) {
        self.write = self.write.wrapping_add(n) & (self.len - 1);
    }

    /// Fatia linear `[write, write+n)` com volta no fim do ring.
    /// A mascara `len-1` e a mesma de `008ACD0A`/`008AD27A`.
    #[inline]
    pub fn write_span(&mut self, n: i32) -> (&mut [f32], &mut [f32]) {
        let len = self.len as usize;
        let w = (self.write as usize) & (len - 1);
        debug_assert!(n >= 0 && (n as usize) <= len);
        let n = n as usize;
        // SAFETY: `plane` tem `len` floats; os dois pedacos sao disjuntos.
        let base = unsafe { core::slice::from_raw_parts_mut(self.plane, len) };
        if w + n <= len {
            (&mut base[w..w + n], &mut [])
        } else {
            let (a, b) = base.split_at_mut(w);
            (&mut b[..len - w], &mut a[..n - (len - w)])
        }
    }
}

/// `0x8BAA10` -> `0x10D0` -> `0x2F60`: `memset(plane, 0, 4*len)`.
///
/// Prova: `008BAAA5 call 0x10D0` com `edx = [rbp+0x34]`; `0x2F60` faz `shl edx,2`
/// (`002F71`) e `call 0x1D2E9E0` (`memset`).
pub fn zero_planes(planes: &mut [&mut [f32]]) {
    for p in planes {
        for v in p.iter_mut() {
            *v = 0.0;
        }
    }
}

/// `0x8BAB60` -> `0x11F0` -> `0x5BC0`: `dst[i] += src[i] * gain`.
///
/// Prova da ordem: `00005C40 vmovss xmm0,[rcx+r10*4]` (src), `00005C46
/// vfmadd213ss xmm0,xmm1,[r8+r10*4]` (dst) e `00005C4C vmovss [r8+r10*4],xmm0`.
/// `xmm1` = ganho (`008BAB86 movaps xmm6,xmm2`, repassado em `008BABD2`).
pub fn accumulate_with_gain(dst: &mut [f32], src: &[f32], gain: f32) {
    for (d, s) in dst.iter_mut().zip(src.iter()) {
        *d = s.mul_add(gain, *d); // FMA unico, como 00005C46
    }
}

/// `008AD06B`..`008AD0B9`: `gain = (float)n / (float)m`.
///
/// O binario converte `rsi`/`rdi` (inteiros de 64 bits assinados) com `cvtsi2ss`
/// e faz `divss xmm6,xmm0`. O caminho negativo (`008AD086`/`008AD0AA`) e o
/// trabalho de conversao u64->f32; a aritmetica final e uma divisao f32.
#[inline]
pub fn overlap_gain(n: i64, m: i64) -> f32 {
    (n as f32) / (m as f32)
}

/// `0x8ACC40`, ordem provada dos efeitos (sem atribuir qual lista entra no MAC):
///
/// ```text
/// 008ACC5D..008ACC88  se available(A) < n -> false (008AD288)
/// 008ACD06..008ACD0E  read(A) = (read(A) + n) & (len-1)
/// 008ACD6B..008ACD79  read(B) = (read(B) + n) & (len-1)
/// 008AD049            zero dos planos de saida (0x8BAA10)
/// 008AD0B9            gain = n/m
/// 008AD21D            para cada canal: dst += src*gain (0x8BAB60)
/// 008AD278..008AD280  write(out) = (write(out) + n) & (len-1)
/// ```
///
/// `src` e o bloco que o chamador escolheu para o overlap-add; qual dos dois
/// rings alimenta esse bloco e `NAO EXTRAIDO` (parada `008AD21D`).
pub fn push_overlap_block(
    out: &mut RingDesc,
    a: &mut RingDesc,
    b: &mut RingDesc,
    src: &[f32],
    n: i32,
    m: i32,
) -> bool {
    if a.available() < n {
        return false;
    }
    a.advance_read(n);
    b.advance_read(n);
    let gain = overlap_gain(n as i64, m as i64);
    let (head, tail) = out.write_span(n);
    for v in head.iter_mut() {
        *v = 0.0;
    }
    for v in tail.iter_mut() {
        *v = 0.0;
    }
    // 0x8BAB60 e chamado por canal; a lista de canais nao foi atribuida.
    let mut off = 0usize;
    accumulate_with_gain(head, &src[off..off + head.len()], gain);
    off += head.len();
    accumulate_with_gain(tail, &src[off..off + tail.len()], gain);
    out.advance_write(n);
    true
}

/// Banco dos tres descritores contiguos: `out @ +0x00`, `A @ +0x90`, `B @ +0x120`.
/// `0x878200` inicializa exatamente tres descritores de `0x90 B`
/// (`008782F5`/`00878306`/`0087830D`).
#[repr(C)]
pub struct RingBank {
    pub out: RingDesc,
    pub a: RingDesc,
    pub b: RingDesc,
}

pub const RING_BANK_BYTES: usize = RING_BYTES * 3;

// ---------------------------------------------------------------------------
// Testes
// ---------------------------------------------------------------------------

