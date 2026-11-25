//! Etapa J4 — contrato da FFT interna usada pelo audio do soothe3.
//!
//! Tudo abaixo tem instrucao + RVA. Onde a matematica do kernel nao foi lida,
//! esta escrito `NAO EXTRAIDO` — nada aqui infere de nome de parametro.
//!
//! ## Cadeia de despacho (provada)
//!
//! ```text
//! stage (0x619EA0, +0x18 = n)
//!   +0 -> config  (0x6165A0): config+0 = flag (8), config+8 = spec
//!   +8 -> state   (0x6165A0): state+0  = pBuffer
//!                              state+8  = specBuf
//!                              state+0x10 = initBuf
//!                              state+0x18 = n (comprimento, multiplo de 8)
//!   +0x18 = n
//! ```
//!
//! `0x8B2680` chama `0x1010` (fwd) com
//! `rcx=src`, `rdx=dst`, `r8=[[stage]+8]` (spec), `r9=[[stage+8]]` (pBuffer):
//! `008B28C8`/`008B28CC`/`008B28CF`/`008B28D2`. A inversa `0x1280` em
//! `008B290F` com os mesmos dois.
//!
//! `0x20E0` (fwd) e `0x7B40` (inv) sao wrappers identicos exceto o slot:
//!
//! | passo | fwd `0x20E0` | inv `0x7B40` |
//! |---|---|---|
//! | valida tag 7 | `000020FA cmp dword ptr [rax],7` | `00007B5A` |
//! | `rcx = [spec+8]` (descritor) | `0000211B` | `00007B7B` |
//! | `rax = [descritor+0x18]` | `0000211F` | `00007B7F` |
//! | se `dword [rax]==3` -> caminho especial | `00002128`/`0000212B` | `00007B88`/`00007B8B` |
//! | especial: `r8=[rax+8]`, `call [rax+0x18]` | `000021AD`/`000021B1` | `00007C0E`/`00007C12` |
//! | generico: `call [rcx]` / `call [rcx+8]` | `0000214A` | `00007BAA` |
//!
//! ## Quem grava o que (medido no proprio plugin, ver `checks/fft_probe.rs`)
//!
//! * `spec+0` = 7 (`000088C2 mov dword ptr [r13],7`).
//! * `spec+8` = descritor = `spec+0x10` (`000089A0 mov [r13+8],r15`). O
//!   descritor e o bloco de `0x340` B zerado em `000004BF`/`0x75FC0` e
//!   preenchido por `0x70480` (via `0x69C80`); `desc[0]=0x6F6A0` e
//!   `desc[8]=0x6F760` sao os kernels **genericos**, gravados por `0x6F360`
//!   em `0006F603`/`0006F608` (chamado por `0x6FF80` a partir de `0000899B`).
//! * `desc+0x18` = objeto "wrapper": `0006F5E5 mov dword ptr [r12],3` e
//!   `0006F5ED mov [r14+0x18],r12`. Ele guarda em `+0x18..+0x40` os kernels
//!   especializados (`0006F502..0006F51B` para a via radix-2/4 e
//!   `0006F5C7..0006F5E0` para a via mista).
//! * `wrapper+8` = ctx (o objeto de `0x72180`, magic 6 em `000721??`); o
//!   wrapper repassa `r8 = [wrapper+8]` ao kernel.
//!
//! ## Kernel por ordem (medido: `checks/.build/fft_*.bits`)
//!
//! Com `flag = 8` o ctx recebe `ctx+8 = 0` (`0x7245C..0x72470`), e e esse
//! campo que `0x72480` testa em `00072552 cmp dword ptr [rsi+8],0` para
//! escolher a tabela `0x1DFA358` (ordens 5..7) / `0x1DFA2F8` (ordens 0..4).
//! Ordem >= 8 vai para `0x1D69E00` (`0007259B`/`000725D6`); ordem > 0x13 vai
//! para `0x88300` (`000725A1`).
//!
//! | ordem | kernel (ctx+8 == 0) | fonte |
//! |---|---|---|
//! | 0..4 | `0x1DFA2F8[ordem]` | `0007257C`/`0007258C` |
//! | 5..7 | `0x1DFA358[ordem]` | `00072552`/`0007257C`/`0007258C` |
//! | 6 | `0x8BFE0` (FFT complexa de 32 pontos, unrolled) | tabela |
//! | 7 | `0x8C280` (FFT complexa de 64 pontos) | tabela |
//! | 8..0x13 | `0x1D69E00` (generica, com twiddles em `ctx+0x30`/`ctx+0x38`) | `000725D6` |
//! | >0x13 | `0x88300` | `000725AE` |
//!
//! A transformada e **real -> complexa** com `n` amostras reais e saida de
//! `n/2+1` pares `(re,im)` intercalados em ordem natural (medido; ver
//! `golden_layout` abaixo). `flag = 8` nao aplica escala
//! (`000088EC cmp edi,8 / je 0x8986`), e o chamador multiplica por `1/n`
//! depois da inversa (`008B2914..008B2929`, `xmm0 = 1.0/n`).
//!
//! ## `NAO EXTRAIDO` (parada com RVA)
//!
//! * Corpo/aritmetica dos kernels `0x1D69E00`, `0x8BFE0`, `0x8C280`.
//! * `0x895C0` (split real/complexo pos-FFT complexa), `0x72180` (ctx),
//!   `0x80640`/`0x806E0`/`0x876E0`/`0x87AA0` (twiddles).
//!
//! Build/teste: `rustc --edition 2021 --test checks\stage_j_fft.rs -o checks\.build\stage_j_fft_tests.exe`

#![allow(dead_code)]


// ---------------------------------------------------------------------------
// Constantes provadas (RVA ao lado)
// ---------------------------------------------------------------------------

/// `000088C2 mov dword ptr [r13],7` / `000020FA cmp dword ptr [rax],7`.
pub const SPEC_MAGIC: u32 = 7;
/// Magic do ctx de `0x72180` (medido: `ctx[0] == 6`).
pub const CTX_MAGIC: u32 = 6;
/// `00002128 cmp dword ptr [rax],3` — marcador do wrapper de kernels.
pub const WRAPPER_MARKER: u32 = 3;
/// Contexto empilhado pelos wrappers antes de chamar o kernel:
/// `00002130 mov qword ptr [rsp+0x30],0x36` (fwd) / `00007B90` (inv).
pub const INNER_CTX_QWORD: u64 = 0x36;
/// Flag usado pelo audio: `000088EC cmp edi,8` / `je 0x8986` (sem escala na IPP).
pub const FLAG_NODIV: u32 = 8;
/// Hint usado pelo audio: `0x6166C8 mov r9d,1` antes de `call 0x12b0`.
pub const HINT: u32 = 1;

/// Wrapper de kernels (marker 3) e slots observados por `checks/fft_probe.rs`.
pub const WRAPPER_FWD_SLOT: usize = 0x18; // `000021B1 call qword ptr [rax+0x18]`
pub const WRAPPER_INV_SLOT: usize = 0x20; // `00007C12 call qword ptr [rax+0x20]`
pub const WRAPPER_CTX_SLOT: usize = 0x08; // `000021AD mov r8,[rax+8]`

/// `desc[0]`/`desc[8]` genericos (`0006F603`/`0006F608`).
pub const GENERIC_FWD: u32 = 0x6F6A0;
pub const GENERIC_INV: u32 = 0x6F760;

/// Kernels especializados do wrapper para a via escolhida em `0x6F360`.
/// `0006F502..0006F51B` (ordens 8..0x13 usam `+0x18` fwd e `+0x20` inv).
pub const WRAP_FWD: u32 = 0x72480;
pub const WRAP_INV: u32 = 0x726A0;
pub const WRAP_28: u32 = 0x72A40;
pub const WRAP_30: u32 = 0x72E20;
pub const WRAP_38: u32 = 0x73440;
pub const WRAP_40: u32 = 0x735E0;

/// Tabela de kernels com `ctx+8 == 0` (o caso do audio).
pub const TAB_LE4_CTX8_0: [u32; 5] = [0x101A0, 0x21920, 0x21940, 0x8A5E0, 0x8A6C0];
pub const TAB_5_7_CTX8_0: [u32; 8] = [
    0x8A980, 0x22500, 0x22520, 0x8B0E0, 0x8B160, 0x8BEE0, 0x8BFE0, 0x8C280,
];
/// Tabela alternativa (`ctx+8 != 0`); o audio nao usa, fica registrada para
/// conferir o `cmp dword ptr [rsi+8],0` de `00072552`.
pub const TAB_LE4_CTX8_1: [u32; 5] = [0x20C00, 0x20C20, 0x20C60, 0x899C0, 0x89AC0];
pub const TAB_5_7_CTX8_1: [u32; 8] = [
    0x8A980, 0x22500, 0x22520, 0x8B0E0, 0x8B160, 0x8B260, 0x8B3A0, 0x8B660,
];
pub const KERNEL_8_19: u32 = 0x1D69E00;
pub const KERNEL_GT19: u32 = 0x88300;

// ---------------------------------------------------------------------------
// Layout
// ---------------------------------------------------------------------------

/// `bins = n/2+1` (`008B28AA`/`008B28AD`); saida tem `n+2` floats.
pub fn bins(n: usize) -> usize {
    n / 2 + 1
}

/// Par `(re,im)` do bin `k` no buffer real->complexo.
/// Medido: bin 0 em `dst[0..2]`, bin 1 em `dst[2..4]`, ..., bin `n/2` em
/// `dst[n..n+2]` (ver `golden_layout_*`).
pub fn bin(dst: &[f32], k: usize) -> (f32, f32) {
    assert_eq!(dst.len(), 2 * (bins((dst.len() - 2) as usize)));
    (dst[2 * k], dst[2 * k + 1])
}

pub fn f(bits: u32) -> f32 {
    f32::from_bits(bits)
}

pub fn to_f32(bits: &[u32]) -> Vec<f32> {
    bits.iter().map(|b| f32::from_bits(*b)).collect()
}

/// Resolve o kernel para `(order, ctx8)` conforme `0x72480` (RVAs na doc acima).
pub fn kernel_for(order: u32, ctx8: u32) -> u32 {
    if order > 0x13 {
        return KERNEL_GT19; // 000725A1 / 000725AE
    }
    if order > 7 {
        return KERNEL_8_19; // 0007259B / 000725D6
    }
    if order <= 4 {
        if ctx8 == 0 {
            TAB_LE4_CTX8_0[order as usize]
        } else {
            TAB_LE4_CTX8_1[order as usize]
        }
    } else if ctx8 == 0 {
        TAB_5_7_CTX8_0[order as usize] // 00072552 je + 0007257C
    } else {
        TAB_5_7_CTX8_1[order as usize]
    }
}

// ---------------------------------------------------------------------------
// Testes
// ---------------------------------------------------------------------------

