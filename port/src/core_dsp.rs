//! Etapa J - incremento 1: nucleo aritmetico provado (K + §8.2(b)).
//!
//! Fonte: `dumpsooth/nyx_soothe3_dump.bin`
//! SHA-256 `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C`.
//!
//! Regra: cada funcao aponta spec + RVA. Onde a transcricao nao fecha (ordem de soma
//! vetorial, implementacao de `powf`/`logf`/`expf`), o item fica marcado
//! `NAO EXTRAIDO` com o RVA onde a leitura parou - nunca aproximado.
//!
//! Compila com:
//! `rustc --edition 2021 --test checks/stage_j_core.rs -o stage_j_core_tests`

#![allow(clippy::excessive_precision)]

// ---------------------------------------------------------------------------
// Constantes lidas do dump (.rdata), com bytes
// ---------------------------------------------------------------------------

/// `0x2079F9C` bytes `00 00 80 3f`
pub const C_1_0: f32 = 1.0;
/// `0x207A360` bytes `00 00 20 41`
pub const C_10_0: f32 = 10.0;
/// `0x2079D88` bytes `cd cc 4c 3d`
pub const C_0_05: f32 = 0.05;
/// `0x207A3B0` bytes `00 00 a0 41`
pub const C_20_0: f32 = 20.0;
/// `0x207A474` bytes `00 00 70 42`
pub const C_60_0: f32 = 60.0;
/// `0x2079E18` bytes `00 00 80 3e`
pub const C_0_25: f32 = 0.25;
/// `0x207A67C` bytes `00 00 80 be`
pub const C_NEG_0_25: f32 = -0.25;
/// `0x207A188` bytes `00 00 00 40`
pub const C_2_0: f32 = 2.0;
/// `0x2079E54` bytes `fa 7e aa 3e`
pub const C_0_333_000_004_3: f32 = 0.3330000043;
/// `0x207A6AC` bytes (f32) `-1.099612832`
pub const C_NEG_1_099_612_832: f32 = -1.099612832;
/// `0x2079FC0` bytes (f32) `+1.099612832`
pub const C_1_099_612_832: f32 = 1.099612832;
/// `0x207A68C` bytes `67 66 e6 be`
pub const C_NEG_0_45: f32 = -0.45;
/// `0x207A2B8` = `4.0f` (expoente de F3)
pub const C_4_0: f32 = 4.0;
/// `0x2079D24` = `0.001f` (§8.2(b))
pub const C_0_001: f32 = 0.001;
/// `0x207A560` = `500.0f` (§8.2(b))
pub const C_500_0: f32 = 500.0;
/// `0x207A030` = `0x3FB99999A0000000` = `(double)0.1f` (§8.2(b))
pub const C_0_1_F64: f64 = 0.10000000149011612;

// ---------------------------------------------------------------------------
// Transcricoes literais dos stubs nao lidos ate o fim
//
// `NAO EXTRAIDO`: `0x1C9AA01` (powf), `0x1C9A9FB` (logf), `0x1C9A9D7` (expf).
// A ordem/implementacao internas dao o bit exato; `f32::powf`/`ln`/`exp` do Rust
// nao sao bit-identicas. Mantidas como funcoes separadas para troca futura.
// ---------------------------------------------------------------------------

/// `10^x` pelo import `powf` da UCRT (`api-ms-win-crt-math-l1-1-0.dll`).
///
/// Prova: `checks/thunk_map.txt` — `0x1C9AA01 -> IAT 0x1D8D818 powf`.
/// Nao ha kernel no dump: bit-exatidao = chamar a mesma UCRT.
/// `checks/j_crt_equiv.rs` confere 17.832.179 amostras sem 1 bit de diferenca
/// entre `f32::powf` e o `powf` importado.
#[inline]
pub fn powf_ipp(base: f32, exp: f32) -> f32 {
    base.powf(exp)
}

/// `ln(x)` pelo import `logf` da UCRT (`0x1C9A9FB -> IAT 0x1D8D808 logf`).
#[inline]
pub fn logf_ipp(x: f32) -> f32 {
    x.ln()
}

/// `exp(x)` pelo import `expf` da UCRT (`0x1C9A9D7 -> IAT 0x1D8D7F0 expf`).
#[inline]
pub fn expf_ipp(x: f32) -> f32 {
    x.exp()
}

#[inline]
pub fn clamp_unit(x: f32) -> f32 {
    // maxss xmm1,xmm13 (0.0) / minss xmm1,xmm11 (1.0): 008B5083/008B5088 e 008B7B28/008B7B2D
    x.max(0.0).min(1.0)
}

// ---------------------------------------------------------------------------
// Primitivas de buffer (spec §9 / §17.2), com o modo provado
// ---------------------------------------------------------------------------

/// `0x1220` -> impl `0x2300`: `dst[i] *= s` in place.
/// Prova: spec §8.2(g) F3 (`008B6659 call 0x1220`) e §10.4 (`0000232B call 0x1D2E460`).
pub fn scale_in_place(dst: &mut [f32], s: f32) {
    for v in dst.iter_mut() {
        *v *= s;
    }
}

/// `0x11F0` -> impl `0x5BC0`: `dst[i] += src[i] * s`
/// Prova: `00005C46 vfmadd213ss xmm0, xmm1, [r8+r10*4]` (spec §8.2(g), `0x8C33D0`).
pub fn mac_scalar_in_place(dst: &mut [f32], src: &[f32], s: f32) {
    for (d, a) in dst.iter_mut().zip(src.iter()) {
        *d = a.mul_add(s, *d); // FMA, como 00005C46
    }
}

/// `0x1250` -> impl `0x69C0`: `dst[i] = min/max(src[i], scalar)`.
///
/// `mode` = 5o argumento na pilha. Provado em `PLANO_MOTOR_AUDIO.md` §17.2:
/// `4` -> min (`00006A65 vminss`), `0` -> max.
/// Prova de ordem dos argumentos: `00006A60 vmovss xmm0,[rcx+rbx*4]` (fonte) e
/// `00006A69 vmovss [rdx+rbx*4],xmm0` (destino).
pub fn clip_scalar(src: &[f32], dst: &mut [f32], scalar: f32, mode: u32) {
    match mode {
        4 => {
            for (d, s) in dst.iter_mut().zip(src.iter()) {
                *d = (*s).min(scalar); // 00006A65 vminss
            }
        }
        0 => {
            for (d, s) in dst.iter_mut().zip(src.iter()) {
                *d = (*s).max(scalar);
            }
        }
        other => panic!("0x69C0: modo {other} nao provado"),
    }
}

// ---------------------------------------------------------------------------
// F1 - ganho dB->linear a partir de `state+4` (spec §8.2(g))
// ---------------------------------------------------------------------------

/// `g = 10^(0.05*(20*clamp(detail,0,1) - 60)) * m`
///
/// RVAs: `008B507C` (leitura crua de `state+4`), `008B5083`/`008B5088` (clamp),
/// `008B508D` (`*20`), `008B5095` (`-60`), `008B509D` (`*0.05`),
/// `008B50A2` (powf), `008B50B1` (`*M`).
pub fn f1_gain(detail: f32, m: f32) -> f32 {
    let x = clamp_unit(detail);
    let db = x * C_20_0 - C_60_0; // mulss/subss
    let lin = powf_ipp(C_10_0, db * C_0_05);
    lin * m
}

/// Aplicacao de F1: `dst[i] = max(src[i], g)`.
///
/// RVAs: `008B51B8 mov [rsp+0x20],0` (modo 0 = max), `008B51BD call 0x1250`.
/// `NAO EXTRAIDO`: por que a aplicacao e `max` (limite inferior) - a semantica do
/// parametro "Detail" nao esta provada; a operacao, sim.
pub fn f1_apply(src: &[f32], dst: &mut [f32], g: f32) {
    clip_scalar(src, dst, g, 0);
}

// ---------------------------------------------------------------------------
// F2 - produto escalar de 32 taps (spec §8.2(g))
// ---------------------------------------------------------------------------

/// `0x1400` = stub IPP -> `0xAC20` -> `0x5F5C0`, `out = sum a[i]*b[i]`.
///
/// Prova: `0005F646 vmulss`, `0005F64E vaddss`, `0005F68D vfmadd231ps`,
/// store `0005F6F7`.
///
/// Ordem **bit-exata** para `n = 16` e `n = 32` (os dois valores usados pelo núcleo:
/// `008B539B r8d=0x20`, `008B6807`/`008B6828 r8d=0x10`), transcrita de
/// `0005F680`..`0005F6BE`:
/// - dois acumuladores de 8 lanes: `acc0 += b[k..k+8]*a[k..k+8]` com
///   `k = 0,16,...`; `acc1 += b[k+8..k+16]*a[k+8..k+16]` (`0005F68D`/`0005F693`);
/// - `L[i] = acc0[i] + acc1[i]` (`0005F6A3`);
/// - `x2 = [L0+L4, L1+L5, L2+L6, L3+L7]` (`0005F6AD`);
/// - `x4_0 = x2[0]+x2[2]`, `x4_1 = x2[1]+x2[3]` (`0005F6B1`/`0005F6B5` `vmovhlps`);
/// - resultado `= x4_0 + x4_1` (`0005F6B9` `vshufps 0xf5` + `0005F6BE vaddss`).
///
/// `checks/j_dot32_avx.rs` compara esta emulação com as mesmas instruções AVX/FMA
/// em hardware: **400.000** casos, `bad=0`.
pub fn dot_ipp(a: &[f32], b: &[f32], n: usize) -> f32 {
    assert!(n == 16 || n == 32, "0x5F5C0: n={n} NAO EXTRAIDO");
    let mut acc0 = [0.0f32; 8];
    let mut acc1 = [0.0f32; 8];
    for c in 0..(n / 16) {
        for i in 0..8 {
            acc0[i] = b[c * 16 + i].mul_add(a[c * 16 + i], acc0[i]); // 0005F68D
            acc1[i] = b[c * 16 + 8 + i].mul_add(a[c * 16 + 8 + i], acc1[i]); // 0005F693
        }
    }
    let mut l = [0.0f32; 8];
    for i in 0..8 {
        l[i] = acc0[i] + acc1[i]; // 0005F6A3
    }
    let x2 = [l[0] + l[4], l[1] + l[5], l[2] + l[6], l[3] + l[7]]; // 0005F6AD
    let x4 = [x2[0] + x2[2], x2[1] + x2[3]]; // 0005F6B1/0005F6B5
    x4[0] + x4[1] // 0005F6B9/0005F6BE
}

/// `n = 32` (F2, `008B539B`).
#[inline]
pub fn dot32(a: &[f32; 32], b: &[f32; 32]) -> f32 {
    dot_ipp(a, b, 32)
}

/// `n = 16` (`008B6807`/`008B6828`).
#[inline]
pub fn dot16(a: &[f32; 16], b: &[f32; 16]) -> f32 {
    dot_ipp(a, b, 16)
}

/// Referência **não** bit-exata (soma sequencial). Serve só para mostrar que a ordem
/// importa: em 400.000 casos aleatórios ela divergiu do alvo em **298.626**.
pub fn dot32_naive(a: &[f32; 32], b: &[f32; 32]) -> f32 {
    let mut acc = 0.0f32;
    for i in 0..32 {
        acc = a[i].mul_add(b[i], acc);
    }
    acc
}

/// F2 por buffer: `buf *= dot(buffer, coef32) * 10^(-0.45)`.
///
/// RVAs: `008B537C` (powf de `-0.45`), `008B539B` (`n = 0x20`),
/// `008B53AB` (tabela `0x2077680`), `008B53B2` (dot), `008B53C6` (`*w`),
/// `008B545B` (`0x1160` = `buf *= g`).
pub fn f2_apply(buf: &mut [f32; 32], coef: &[f32; 32]) {
    let w = powf_ipp(C_10_0, C_NEG_0_45);
    let p = dot32(buf, coef); // bit-exato (ordem de 0005F680..0005F6BE)
    let g = p * w;
    for v in buf.iter_mut() {
        *v *= g;
    }
}

// ---------------------------------------------------------------------------
// F3 - par 0.25 / -0.25 com x^4 (spec §8.2(g))
// ---------------------------------------------------------------------------

/// `s = -0.25 - 0.25 * powf(detail, 4)`
///
/// RVAs: `008B6627 mulss 0.25`, `008B663E movss -0.25`, `008B6646 subss`,
/// `008B6582`/`008B658E` (powf com expoente 4), `008B6659` (`0x1220`).
pub fn f3_scale(detail: f32) -> f32 {
    let p = powf_ipp(detail, C_4_0);
    C_NEG_0_25 - C_0_25 * p
}

/// Aplicacao de F3: `buf *= s` (`008B6659 call 0x1220`).
pub fn f3_apply(buf: &mut [f32], detail: f32) {
    scale_in_place(buf, f3_scale(detail));
}

// ---------------------------------------------------------------------------
// F4 - curva log/exp sobre `state+4` (spec §8.2(g))
// ---------------------------------------------------------------------------

/// `y = exp(c*(ln(2 - x^2 + 0.3330000043) + 1.099612832) - 1.099612832) - 0.3330000043`
/// com `c = clamp(state+0,0,1)` e `x = state+4`.
///
/// RVAs: `008B7AFC` (`2.0`), `008B7B04` (`x*x`), `008B7B09` (`2-x^2`),
/// `008B7B0E` (`+1/3`), `008B7B16` (logf), `008B7B1B` (`+1.0996`),
/// `008B7B23`-`008B7B2D` (clamp de `state+0`), `008B7B32` (`*c`),
/// `008B7B36` (`-1.0996`), `008B7B3E` (expf), `008B7B4D` (`-1/3`).
pub fn f4_curve(c: f32, x: f32) -> f32 {
    let inner = logf_ipp(C_2_0 - x * x + C_0_333_000_004_3) - C_NEG_1_099_612_832;
    let y = expf_ipp(clamp_unit(c) * inner - C_1_099_612_832);
    y - C_0_333_000_004_3
}

/// Aplicacao de F4: `buf *= curva` (`008B7BD9 call 0x1220`).
pub fn f4_apply(buf: &mut [f32], c: f32, x: f32) {
    scale_in_place(buf, f4_curve(c, x));
}

// ---------------------------------------------------------------------------
// F5 - gate e dois log(pow(10,.)) (spec §8.2(g)) - PARCIAL
// ---------------------------------------------------------------------------

/// Gate de F5: `byte[engine+0x48] > 2`.
/// Prova: `008B3FCC cmp qword [r13+0x48],2`; `008B3FD1 seta byte [rbp+0x4A20]`.
#[inline]
pub fn f5_gate(engine_48: u64) -> bool {
    engine_48 > 2
}

/// As duas conversoes de F5: `ln(10^-3)` e `ln(10^(-0.05*v))`.
/// Prova: `008B869C powf(10,-3)` (`0x207A6E4`), `008B86A1 logf`; `008B86BB powf`,
/// `008B86C0 logf`; `008B86AF mulss -0.05` (`0x207A66C`).
/// `NAO EXTRAIDO`: o consumidor de `0x8BFCB0`/`0x8BFD30` sob o gate e a ordem
/// exata da composicao (`008B86A6`..`008B86D0`) - parada em `008B86D0`.
pub fn f5_ln_pair(v: f32) -> (f32, f32) {
    let a = logf_ipp(powf_ipp(C_10_0, -3.0));
    let b = logf_ipp(powf_ipp(C_10_0, -0.05 * v));
    (a, b)
}

// ---------------------------------------------------------------------------
// §8.2(b) - coeficiente de one-pole a partir de um tempo
// ---------------------------------------------------------------------------

/// `coef = 1 - 0.1^(1/x)`, `x = ((t / n) * 0.001) * 500`.
///
/// RVAs: `008B68AB`/`008B68B6` (gate `[ctx+0x58]`), `008B68BC` (`N` como `qword`
/// inteiro -> `cvtsi2ss`), `008B68E4`..`008B6901` (`/N`, `*0.001`, `*500`),
/// `008B6918` (`pow` double), `008B6932` (subtracao de 1.0).
/// `r13` = arg1 de `0x8B3ED0` (`008B3F14`), logo `t = [ctx+0x20]` e `n = [ctx+0x60]`
/// sao campos do **contexto**; "sample rate" nao provado.
pub fn one_pole_coef(t: f32, n: i64) -> f64 {
    let n_f = n as f32;
    let x = (t / n_f) * C_0_001 * C_500_0;
    1.0 - C_0_1_F64.powf(1.0 / x as f64)
}

// ---------------------------------------------------------------------------
// Testes (formulas fechadas; tolerancia porque powf/log/exp sao do host)
// ---------------------------------------------------------------------------

