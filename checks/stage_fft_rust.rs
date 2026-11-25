//! Espelho Rust do que ficou PROVADO sobre o par FFT/IPP usado pelo áudio
//! (PLANO §24.4; spec §18.6). Cada item aponta para instrução + RVA.
//!
//! O que NÃO está aqui: as borboletas / twiddles. A implementação concreta do
//! kernel não foi lida (`NÃO EXTRAÍDO`); os símbolos IPP foram linkados
//! estaticamente sem nomes. Este módulo reproduz **só** o contrato provado:
//! validação de spec (magic 7), despacho forward/inverse, e a escala 1/n.
#![allow(dead_code)]

/// Códigos de retorno observados em `0x20E0`/`0x7B40` (RVA de cada `mov eax,imm`).
pub const IPP_STS_OK: i32 = 0;
pub const IPP_STS_NULL_PTR: i32 = -8; // 0xFFFFFFF8 @ 0x21B9 / 0x7C1A
pub const IPP_STS_CONTEXT_MATCH: i32 = -13; // 0xFFFFFFF3 @ 0x20FF / 0x7B5F
pub const IPP_STS_BAD_ARG: i32 = -2; // 0xFFFFFFFE @ 0x2189 / 0x7BEA

/// Descritor empilhado pelo wrapper antes de chamar a vtable interna.
/// `00002130 mov qword ptr [rsp+0x30], 0x36` (fwd) /
/// `00007B90 mov qword ptr [rsp+0x30], 0x36` (inv).
pub const INNER_CTX_QWORD: u64 = 0x36;

/// Cabeçalho comum de `IppsFFTSpec_*` como o binário o lê — só os campos usados:
/// `[+0]` = magic (comparado com 7), `[+8]` = ponteiro para o objeto interno.
/// Prova: `000020FA cmp dword ptr [rax],7`; `0000211B mov rcx,[rax+8]`.
#[repr(C)]
pub struct IppSpec {
    pub magic: i32,     // +0x00, deve ser 7
    pub _pad: i32,      // +0x04 (não lido pelo wrapper)
    pub inner: *mut Inner, // +0x08
}

/// Objeto interno. `[+0x18]` pode ser um descritor alternativo com `[+0]==3`;
/// `[+0]`/`[+8]` formam a vtable usada no caminho genérico.
#[repr(C)]
pub struct Inner {
    pub vtable: *const InnerVtbl, // +0x00  (chamado em 0x214A como [rcx])
    pub _pad: *const u8,          // +0x08
    pub _pad2: *const u8,         // +0x10
    pub alt: *const AltDesc,      // +0x18  (`mov rax,[rcx+0x18]` @ 0x211F)
}

/// Vtable do caminho genérico: slot 0 = forward, slot 8 = inverse.
/// Prova: `0000214A call qword ptr [rcx]` vs `00007BAA call qword ptr [rcx+8]`.
#[repr(C)]
pub struct InnerVtbl {
    pub fwd: unsafe extern "C" fn(*mut Inner, *const f32, *mut f32, *mut u64, *mut u8) -> i32,
    pub inv: unsafe extern "C" fn(*mut Inner, *const f32, *mut f32, *mut u64, *mut u8) -> i32,
}

/// Descritor alternativo: `[+0]==3`, `[+8]` e `[+0x18]`/`[+0x20]` são funções.
/// Prova: `00002128 cmp dword ptr [rax],3`; `000021B1 call qword ptr [rax+0x18]`;
/// `00007C12 call qword ptr [rax+0x20]`.
#[repr(C)]
pub struct AltDesc {
    pub kind: i32,                // +0x00 == 3
    pub _pad: i32,
    pub data: *const u8,          // +0x08 -> r8
    pub _pad2: u64,               // +0x10
    pub fwd: usize,               // +0x18
    pub inv: usize,               // +0x20
}

unsafe fn dispatch(
    src: *const f32,
    dst: *mut f32,
    spec: *const IppSpec,
    buf: *mut u8,
) -> i32 {
    if spec.is_null() {
        return IPP_STS_NULL_PTR; // 0x20F1 test rax,rax / 0x21B9
    }
    if (*spec).magic != 7 {
        return IPP_STS_CONTEXT_MATCH; // 0x20FA cmp dword ptr [rax],7 / 0x20FF
    }
    if src.is_null() || dst.is_null() {
        return IPP_STS_NULL_PTR; // 0x2109 / 0x2112
    }
    let inner = (*spec).inner; // 0x211B
    let alt = (*inner).alt; // 0x211F
    if !alt.is_null() && (*alt).kind == 3 {
        // 0x2128: caminho "descritor alternativo" (slot +0x18 fwd / +0x20 inv)
        // corpo NÃO EXTRAÍDO
        unimplemented!("alt path @ 0x21A7/0x7C08 — corpo NÃO EXTRAÍDO");
    }
    let vt = (*inner).vtable; // [rcx]
    let mut ctx = [INNER_CTX_QWORD, 0u64]; // 0x2130/0x2142
    ((*vt).fwd)(inner, src, dst, ctx.as_mut_ptr(), buf) // 0x214A
}

unsafe fn dispatch_inv(
    src: *const f32,
    dst: *mut f32,
    spec: *const IppSpec,
    buf: *mut u8,
) -> i32 {
    // idêntico a `dispatch`; muda apenas o slot: `0x7BAA call [rcx+8]`
    if spec.is_null() {
        return IPP_STS_NULL_PTR;
    }
    if (*spec).magic != 7 {
        return IPP_STS_CONTEXT_MATCH; // 0x7B5A / 0x7B5F
    }
    if src.is_null() || dst.is_null() {
        return IPP_STS_NULL_PTR;
    }
    let inner = (*spec).inner;
    let alt = (*inner).alt;
    if !alt.is_null() && (*alt).kind == 3 {
        unimplemented!("alt path @ 0x7C08 — corpo NÃO EXTRAÍDO");
    }
    let vt = (*inner).vtable;
    let mut ctx = [INNER_CTX_QWORD, 0u64];
    ((*vt).inv)(inner, src, dst, ctx.as_mut_ptr(), buf) // 0x7BAA
}

/// Tradução de código interno -> status público (0x215B..0x2187, idêntica em 0x7BBC..0x7BE8).
pub fn translate_internal(code: i32) -> i32 {
    if code == 0 {
        return 0;
    }
    if code == 7 {
        return IPP_STS_BAD_ARG; // 0x215B cmp rax,7 -> 0x2189
    }
    let t = code & !2;
    if t == 1 {
        return IPP_STS_NULL_PTR; // 0x2161..0x216C
    }
    if code == 5 {
        return IPP_STS_NULL_PTR; // 0x216E
    }
    if code == 2 {
        return IPP_STS_CONTEXT_MATCH; // 0x2174 -> 0x2193
    }
    let d = code.wrapping_sub(100);
    if d <= 2 {
        return 0; // 0x217F..0x2187
    }
    IPP_STS_BAD_ARG // 0x2189
}

/// Um passo do estágio espectral de `0x8B2680`, na ordem provada das chamadas.
/// `n` = `[stage+0x18]` (`008B2753 movsxd r15,dword [rax+0x18]`).
pub struct StageStep {
    pub n: usize,
}

impl StageStep {
    /// FFT direta -> multiplicação espectral -> FFT inversa -> escala 1/n.
    ///
    /// Ordem exata do binário:
    ///   008B28D6 call 0x1010  (forward)
    ///   008B28F6 call 0x1520  (mul espectral, em 0xBD40)
    ///   008B290F call 0x1280  (inverse, em 0x7B40)
    ///   008B2929 call 0x1220  (scale 1/n)
    ///
    /// `bins = n/2 + 1` (`008B28AA shr rdi,1`; `008B28AD inc rdi`).
    pub fn hop(&self) -> usize {
        self.n / 2
    }

    pub fn bins(&self) -> usize {
        self.n / 2 + 1
    }

    /// `xmm0 = 1.0f / (float)n` — `008B272F movss xmm7,[0x2079F9C]` (1.0),
    /// `008B291C cvtdq2ps xmm1,n`, `008B2925 divss xmm0,xmm1`.
    pub fn inv_scale(&self) -> f32 {
        1.0f32 / self.n as f32
    }
}

/// Multiplicação complexa in-place com checagem de sobreposição — `0xBD40`.
/// Elementos de 8 B: par interleaved (re,im) (`vmovsd`, `vmovshdup`, `vshufps 0xb1`,
/// `vfmaddsub213ps` em 0xBDE0..0xBDFD). `count` = número de pares.
pub fn mul_complex_inplace(coef: &[f32], data: &mut [f32], count: usize) {
    assert_eq!(coef.len(), count * 2);
    assert_eq!(data.len(), count * 2);
    for k in 0..count {
        let cr = coef[2 * k];
        let ci = coef[2 * k + 1];
        let dr = data[2 * k];
        let di = data[2 * k + 1];
        data[2 * k] = dr * cr - di * ci;
        data[2 * k + 1] = dr * ci + di * cr;
    }
}
