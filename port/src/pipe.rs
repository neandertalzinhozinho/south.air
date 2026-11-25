//! Etapa J3 — camada de descritores e orquestração do núcleo.
//!
//! Transcreve **só o que está provado por instrução + RVA**:
//!
//! 1. descritor de arrays de `0x410 B` (`+0x000` `void*[128]`, `+0x400 i32 count`,
//!    `+0x404 i32 len`, `+0x408 i64 len*4`) e o alocador bump que o preenche;
//! 2. par de buffers do estagiador `{p0,p1,n,4n}` (`0x8CAFD0`);
//! 3. descritor de ring de `0x90 B` (write/read/len/nch) e a aritmética `(i+n)&(len-1)`;
//! 4. ordem da cadeia de `0x8AD2B0` (25 estágios, com os dois ramos de flag);
//! 5. lei de mistura de `0x8C1440`.
//!
//! O que **não** está provado fica marcado `NÃO EXTRAÍDO`/`NÃO PROVADO` com o RVA de
//! parada e **não** é implementado. Em particular: a semântica dos 16 buffers de
//! `0x8C1440` (só existência/contagem/alinhamento), o papel do miolo de `0x8B3ED0`
//! (5 faixas fechadas em K rodam sobre buffers cuja origem não foi atribuída) e o
//! interior de `0x8B8E70`/`0x8B9E40`/`0x8BA1B0`/`0x8BA7B0`/`0x8A1EE0`.
//!
//! `rustc --edition 2021 --test checks\stage_j_pipe.rs -o stage_j_pipe_tests`

#![allow(dead_code)]

use core::mem::size_of;

// ---------------------------------------------------------------------------
// 1. Descritor de arrays de 0x410 B
// ---------------------------------------------------------------------------

/// `+0x000..+0x3FF` = `void*[128]`; `+0x400 i32 count`; `+0x404 i32 len`;
/// `+0x408 i64 len*4`.
///
/// Prova (spec §8.4 / `checks/n_canal.md` §1.6):
/// - `008AD31B` zera `0x3F8` B a partir de `+0x8` (o ponteiro `+0x0` é zerado à parte);
/// - `008AD32A` grava `+0x400` (`count`), `008AD330` grava `+0x404` (`len`),
///   `008AD337` grava `+0x408` (`len*4`);
/// - cópia integral em 8×`0x80` (`008AD930..008AD981`) + cauda de 16 B
///   (`008C333B`, `008C33A3`) = `0x410`.
#[repr(C)]
pub struct Descr410 {
    pub ptr: [*mut f32; 128],
    pub count: i32,
    pub len: i32,
    pub stride: i64,
}

pub const DESCR410_BYTES: usize = 0x410;

impl Descr410 {
    /// Estado após o `memset` de `0x3F8` B: ponteiros nulos, cabeçalho zerado.
    pub fn zeroed() -> Self {
        Descr410 {
            ptr: [core::ptr::null_mut(); 128],
            count: 0,
            len: 0,
            stride: 0,
        }
    }
}

/// `align16` **em floats** (`eax = cursor + len`; `008C3510 and eax,0xf`;
/// `008C3513 sub`; `008C3516 add 0x10`; `008C351D cmove` quando já múltiplo).
#[inline]
pub fn align16_floats(x: i32) -> i32 {
    if x & 0xF == 0 {
        x
    } else {
        (x & !0xF).wrapping_add(0x10)
    }
}

/// Bloco 1 de `0x8C33D0`: aloca `count` ponteiros na arena e grava o cabeçalho.
///
/// ```
/// 008C34EE  edx = [r15+0x18]        ; cursor (floats)
/// 008C34F2  rax = [r15]             ; base
/// 008C34F8  ptr[i] = base + cursor*4
/// 008C34FC  eax = cursor + len
/// 008C3507..008C351D  cursor = align16(eax)
/// 008C3524  [r15+0x18] = cursor
/// ```
///
/// `base.len()` não é checado: a arena é externa (é o chamador quem a mantém).
/// Devolve o descritor e o cursor novo.
pub fn alloc_descr(base: *mut f32, cursor: i32, count: i32, len: i32) -> (Descr410, i32) {
    let mut d = Descr410::zeroed();
    d.count = count;
    d.len = len;
    d.stride = (len as i64) * 4;
    let mut cur = cursor;
    if count > 0 {
        for i in 0..(count as usize) {
            // SAFETY do chamador: a arena tem espaço para `cur + len` floats.
            d.ptr[i] = unsafe { base.add(cur as usize) };
            cur = align16_floats(cur.wrapping_add(len));
        }
    }
    (d, cur)
}

// ---------------------------------------------------------------------------
// 2. Par de buffers do estagiador (0x8CAFD0)
// ---------------------------------------------------------------------------

/// Descritor de par do estagiador, `0x18 B`: `{p0@0, p1@8, n@0x10, 4n@0x14}`.
///
/// Prova: `008CAFE2 [rdx]=p0`, `008CB015 [rdx+8]=p1`; `n` lido em `008CAFDA`
/// de `[rdx+0x10]`; `4n` já está em `+0x14` (`NÃO EXTRAÍDO: quem grava +0x14`,
/// só o uso é provado).
#[repr(C)]
pub struct StageBuf {
    pub p0: *mut f32,
    pub p1: *mut f32,
    pub n: i32,
    pub n4: i32,
}

pub const STAGE_BUF_BYTES: usize = 0x18;

/// Alocador bump de `0x8CAFD0`: dois ponteiros consecutivos, cada avanço alinhado a 16.
///
/// ```
/// 008CAFD6  r8  = [rcx+0x18]          ; cursor
/// 008CAFDA  r10 = [rdx+0x10]          ; n (do descritor)
/// 008CAFDE  p0  = [rcx] + cursor*4
/// 008CAFE9..008CB007  cursor = align16(cursor+n)
/// 008CB00B..008CB015  p1 = base + cursor*4
/// 008CB019..008CB03A  cursor = align16(cursor+n)
/// ```
pub fn alloc_pair(
    base: *mut f32,
    cursor: i32,
    n: i32,
    n4: i32,
) -> (StageBuf, i32) {
    let p0 = unsafe { base.add(cursor as usize) };
    let mut cur = align16_floats(cursor.wrapping_add(n));
    let p1 = unsafe { base.add(cur as usize) };
    cur = align16_floats(cur.wrapping_add(n));
    (
        StageBuf {
            p0,
            p1,
            n,
            n4,
        },
        cur,
    )
}

/// `0x8C1440`: 16 buffers de `n` floats; 5 pares inline (`008C150F`..`008C1763`) e
/// 3 chamadas de `0x8CAFD0` (`008C179A`/`008C17BE`/`008C17E2`) → 5·2 + 3·2 = 16.
/// Zeroização: 16×`0x10D0` em `008C1800`..`008C19C6`.
pub const STAGE_BUFFERS: usize = 16;

/// Tabela `0x2014360` = `{8, 9, 10, 6, 5}` (lida em `008C1A4D`; bytes conferidos no dump).
pub const STAGE_GROUPS: [u8; 5] = [8, 9, 10, 6, 5];

/// Saída imediata de `0x8C1440`: `cmp dword [rdx+0x400], 2` / `jle`
/// (`008C1467`/`008C1474`) — com **count ≤ 2** não há estagiamento.
#[inline]
pub fn stage_returns_early(count: i32) -> bool {
    count <= 2
}

/// Enable do grupo `g`: `movzx ecx, byte [state + g*8 + 0x1BF]` (`008C1A6E`,
/// repetido em `008C2ABA`). `g` é o índice em `STAGE_GROUPS`.
#[inline]
pub fn group_enabled(state: &[u8], g: usize) -> bool {
    state[0x1BF + g * 8] != 0
}

/// Lei de mistura de `0x8C1440`, por buffer:
///
/// ```
/// 008C2A5C  xmm10 = 1.0                  ; constante 0x2079F9C
/// 008C2A70  xmm8  = f32 [state+0x2C]     ; g  (lido em 008C19D9)
/// 008C2CC4  xmm6  = xmm10 - xmm8         ; 1 - g
/// 008C2CE0  call 0x1220(dst_i, n, 1-g)   ; dst *= 1-g
/// 008C2D90  call 0x11F0(staged_i, dst_i, n, g)  ; dst += staged*g
/// ```
///
/// `0x1220` → `0x6160` (multiplicar, `vmulps` em `00006220`) e `0x11F0` →
/// `0x5BC0` — **MAC com FMA**: `00005C46 vfmadd213ss xmm0,xmm1,[r8+...]` e
/// `00005C85 vfmadd213ps ymm2,ymm0,[r8+...]`, isto é
/// `dst = src*alpha + dst` com **um** arredondamento. Por isso o segundo
/// laço usa [`f32::mul_add`]; `dst + src*alpha` com dois arredondamentos
/// divergiria no ULP.
///
/// **Correção 2026-11-24 (era "g/2 no estéreo").** O `×0,5` não é o caminho estéreo:
/// - `nch == 2` (`008C2BAE cmp [r12+0x10],2` / `008C2BB4 jne`; idem `008C2F88`/`008C2F8D`):
///   o laço por canal usa `g` **inteiro** (`008C2D90..008C2DB4`, `008C3180..008C31A3`);
/// - `nch != 2` vai a `008C2DB8`/`008C31A7`: alvo `1-g` (`008C2DC8 subss`) e **MAC `g·0,5`**
///   (`008C2DEA mulss xmm1,xmm11`, `xmm11 = 0,5` em `008C2A67`, constante `0x2079EA8`).
///
/// **Correção 2026-11-25.** `dst` = buffers de canal do registro; `staged` = **resultado da
/// divisão** (`new1/T1/T2/T3`, isto é `Σregistros ch² / Σregistros ch`), não um buffer de
/// entrada. No caminho mono o `staged` recebido já é `A/B/C/D` = soma dos 2 canais do
/// resultado, e é por isso que o `×0,5` existe só ali. O portão `cmp edi,2`
/// (`008C2D79`/`008C3169`) é redundante: `edi = [rbp+0x6A0]` é a contagem de ponteiros do
/// descritor local, fixada em `2` (`008C2C0B`/`008C2FE4`) porque o bloco já está no ramo
/// `nch == 2`.
pub fn mix_coeffs(g: f32, nch: i32) -> (f32, f32) {
    if nch == 2 {
        (1.0f32 - g, g)
    } else {
        (1.0f32 - g, g * 0.5)
    }
}

pub fn mix_lane(dst: &mut [f32], staged: &[f32], g: f32, nch: i32) {
    let (a, b) = mix_coeffs(g, nch);
    for d in dst.iter_mut() {
        *d *= a; // 0x1220: vmulps, um arredondamento
    }
    for (d, s) in dst.iter_mut().zip(staged.iter()) {
        *d = s.mul_add(b, *d); // 0x11F0: vfmadd213ps (00005C85)
    }
}

// ---------------------------------------------------------------------------
// 3. Descritor de ring de 0x90 B
// ---------------------------------------------------------------------------

/// Três descritores contíguos de `0x90 B` (base, `base+0x90`, `base+0x120`).
///
/// Campos provados (`checks/o_saida.md` §10.6):
/// `+0x00 f32* plane` (`00868930`), `+0x80 i32 write` (`008AD26C`/`008AD280`),
/// `+0x84 i32 read` (`008ACCF7`/`008ACD0E`), `+0x88 i32 len` (`008688CC`,
/// `0x10000` em `00870790`/`00873D5D`), `+0x8C i32 nch` (`008688D4`).
///
/// `+0x08..+0x7F` = `NÃO EXTRAÍDO` (`0x868840`, que inicializa o descritor).
#[repr(C)]
pub struct RingDesc {
    pub plane: *mut f32,
    pub unknown: [u8; 0x78],
    pub write: i32,
    pub read: i32,
    pub len: i32,
    pub nch: i32,
}

pub const RING_BYTES: usize = 0x90;
/// Comprimento fixo do ring (`00870790`/`00873D5D` empilham o literal `0x10000`,
/// gravado em `+0x88` por `008688CC`).
pub const RING_LEN: i32 = 0x10000;

impl RingDesc {
    pub fn new(plane: *mut f32, nch: i32) -> Self {
        RingDesc {
            plane,
            unknown: [0; 0x78],
            write: 0,
            read: 0,
            len: RING_LEN,
            nch,
        }
    }

    /// `008ACC5D`..`008ACC82`: `avail = (write - read) & (len-1)` (32 bits).
    #[inline]
    pub fn available(&self) -> i32 {
        self.write.wrapping_sub(self.read) & (self.len - 1)
    }

    /// `008ACD06`..`008ACD0E` e `008AD26C`..`008AD280`: `i = (i + n) & (len-1)`.
    #[inline]
    pub fn advance_read(&mut self, n: i32) {
        self.read = self.read.wrapping_add(n) & (self.len - 1);
    }

    #[inline]
    pub fn advance_write(&mut self, n: i32) {
        self.write = self.write.wrapping_add(n) & (self.len - 1);
    }
}

// ---------------------------------------------------------------------------
// 4. Ordem da cadeia de 0x8AD2B0
// ---------------------------------------------------------------------------

/// Flags de decisão lidas em `0x8AD2B0` (`checks/n_canal.md` §1.4).
#[derive(Clone, Copy, Debug, Default)]
pub struct ChainFlags {
    /// `byte[[X+0x2C38]+0x58]` — `008AD76B`/`008AD7A1`: 1 → `0x8B8E70`, 0 → `0x8B9E40`.
    pub f58: bool,
    /// `byte[[X+0x2C38]+0x52]` — `008ADFAB`/`008AE56F`: liga `0x8BA7B0` e `0x8A1EE0`.
    pub f52: bool,
    /// `byte[[X+0x2C38]+0x51]` — `008ADC78`: parte do atalho.
    pub f51: bool,
    /// `byte[X+0x59]` — `008ADC6B`: parte do atalho.
    pub f59: bool,
}

/// O atalho `008ADC84 mov r15b,1` / `008ADC87 jmp 0x8AE1C1` salta de `008ADC8C`
/// direto para o `call 0x619D90` (`008AE1EC`), pulando os estágios 8–19.
#[inline]
pub fn chain_takes_shortcut(flags: &ChainFlags, counts_equal: bool) -> bool {
    !flags.f59 && !flags.f51 && counts_equal
}

/// Estágios na ordem em que `0x8AD2B0` os executa (`checks/n_canal.md` §1.3).
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Step {
    /// (1) sonda de pilha de `008AD2B0`.
    Probe,
    /// (2)(3)(4)(6)(7) descritor de arena zerado (`memset 0x3F8`).
    ZeroDescr(u8),
    /// (5) `008AD601 call 0x8B3ED0` — o único núcleo.
    Core,
    /// (8)(10) `0x8AE650` — cópia de estruturas antes da análise.
    CopyPre,
    /// (9) `008AD9FA call 0x8B8E70` [f58 != 0].
    AnalysisStaged,
    /// (11) `008ADC52 call 0x8B9E40` [f58 == 0].
    AnalysisPlain,
    /// (12) `0x10D0` preenche N buffers de comprimento `[rbp+0xD94]`.
    Fill,
    /// (13)(16)(20) monta descritor de `0x410 B`.
    DescrBuild(u8),
    /// (14)(17)(21) copia a lista de ponteiros.
    PtrCopy(u8),
    /// (15) `008ADF9B call 0x8BA1B0`.
    Bands1,
    /// (18) `008AE096 call 0x8BA7B0` [f52 != 0].
    Bands2,
    /// (19) `008AE1AF call 0x1010` (FFT direta) em laço.
    Fft,
    /// (22)(23) `0x1520` (laço se contagens iguais, único se `edx == 1`).
    Copy1520,
    /// (24) `008AE55F call 0x8BA8C0`.
    Finish,
    /// (25) `008AE5EC call 0x8A1EE0` [f52 != 0].
    MixAlt,
}

/// Sequência provada, incluindo os dois ramos de flag e o atalho.
pub fn chain_plan(flags: &ChainFlags, counts_equal: bool) -> Vec<Step> {
    let mut v = vec![Step::Probe];
    v.extend_from_slice(&[
        Step::ZeroDescr(0),
        Step::ZeroDescr(1),
        Step::ZeroDescr(2),
        Step::Core,
        Step::ZeroDescr(3),
        Step::ZeroDescr(4),
    ]);
    if !chain_takes_shortcut(flags, counts_equal) {
        v.push(Step::CopyPre);
        v.push(if flags.f58 {
            Step::AnalysisStaged
        } else {
            Step::AnalysisPlain
        });
        v.push(Step::Fill);
        v.push(Step::DescrBuild(13));
        v.push(Step::PtrCopy(14));
        v.push(Step::Bands1);
        if flags.f52 {
            v.push(Step::DescrBuild(16));
            v.push(Step::PtrCopy(17));
            v.push(Step::Bands2);
        }
        v.push(Step::Fft);
    }
    v.push(Step::DescrBuild(20));
    v.push(Step::PtrCopy(21));
    v.push(Step::Copy1520);
    v.push(Step::Finish);
    if flags.f52 {
        v.push(Step::MixAlt);
    }
    v
}

// ---------------------------------------------------------------------------
// Testes
// ---------------------------------------------------------------------------

