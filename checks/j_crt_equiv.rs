//! Etapa J - incremento 2: `powf`/`logf`/`expf` sao imports da UCRT no alvo.
//!
//! Prova no dump: `checks/thunk_map.txt`
//!   0x1C9A9D7 -> IAT 0x1D8D7F0  expf  [api-ms-win-crt-math-l1-1-0.dll]
//!   0x1C9A9FB -> IAT 0x1D8D808  logf  [api-ms-win-crt-math-l1-1-0.dll]
//!   0x1C9AA01 -> IAT 0x1D8D818  powf  [api-ms-win-crt-math-l1-1-0.dll]
//!
//! Logo nao ha kernel para portar: bit-exatidao exige chamar a **mesma** UCRT.
//! Este teste confere que `f32::powf`/`ln`/`exp` do Rust compilado para
//! `x86_64-pc-windows-msvc` produzem exatamente os mesmos bits que as funcoes
//! importadas da UCRT, no mesmo processo.
//!
//! `rustc -O checks/j_crt_equiv.rs -o j_crt_equiv && ./j_crt_equiv`

extern "C" {
    fn powf(base: f32, exp: f32) -> f32;
    fn logf(x: f32) -> f32;
    fn expf(x: f32) -> f32;
    fn fmaf(x: f32, y: f32, z: f32) -> f32;
}

fn bits(x: f32) -> u32 {
    x.to_bits()
}

fn main() {
    let mut bad = 0usize;
    let mut checked = 0usize;

    // powf: bases e expoentes usados no motor
    let bases = [10.0f32, 2.0, 0.1, 1.0, 0.25, 3.0, 7.0, 250.0, 0.3330000043];
    let exps = [
        -0.45f32, 0.05, 4.0, 1.0 / 3.0, -3.0, -0.05, 0.5, 2.4, -4.8, 0.0, 1.0,
    ];
    for &b in &bases {
        for &e in &exps {
            checked += 1;
            let a = b.powf(e);
            let c = unsafe { powf(b, e) };
            if bits(a) != bits(c) {
                bad += 1;
                println!("powf DIFF b={b:?} e={e:?} rust={:08x} crt={:08x}", bits(a), bits(c));
            }
        }
    }

    // logf / expf em varredura densa (inclui subnormais e valores grandes)
    let mut x = 1e-6f32;
    while x < 1.0e6 {
        checked += 2;
        if bits(x.ln()) != bits(unsafe { logf(x) }) {
            bad += 1;
            if bad < 12 {
                println!("logf DIFF x={x:e} rust={:08x} crt={:08x}", bits(x.ln()), bits(unsafe { logf(x) }));
            }
        }
        if bits(x.exp()) != bits(unsafe { expf(x) }) {
            bad += 1;
            if bad < 12 {
                println!("expf DIFF x={x:e} rust={:08x} crt={:08x}", bits(x.exp()), bits(unsafe { expf(x) }));
            }
        }
        x *= 1.0000031;
    }

    // fmaf: o alvo usa vfmadd (FMA); `mul_add` deve casar com fmaf
    let pairs = [
        (0.1f32, 0.2f32, 0.3f32),
        (1.0e30, 1.0e-30, -1.0),
        (0.3330000043, 2.5, 0.0),
        (-0.25, 3.0, 1.0),
    ];
    for &(a, b, c) in &pairs {
        checked += 1;
        if bits(a.mul_add(b, c)) != bits(unsafe { fmaf(a, b, c) }) {
            bad += 1;
            println!("fma DIFF {a:?}*{b:?}+{c:?}");
        }
    }

    println!("checked={checked} bad={bad}");
    assert_eq!(bad, 0, "divergencia Rust x UCRT: nao usar f32::* sem provar");
}
