//! Depuracao: despeja o workspace apos a 1a e a 2a+3a passadas, para
//! comparar com o modelo Python (`tools/full_model.py`).
//!
//! Build: rustc --edition 2021 -O checks\j9_dbg.rs -o checks\.build\j9_dbg.exe

#[path = "j4_fft.rs"]
mod fft;

use fft::*;

fn dump(path: &str, d: &[f32]) {
    use std::io::Write;
    let mut s = String::new();
    for v in d {
        s.push_str(&format!("{:08x}\n", v.to_bits()));
    }
    std::fs::File::create(path)
        .and_then(|mut f| f.write_all(s.as_bytes()))
        .unwrap();
}

fn main() {
    let mut src = [0f32; 512];
    for i in 0..512 {
        src[i] = f32::from_bits(J9_SRC[i]);
    }
    let mut tw = [0f32; 512];
    for i in 0..512 {
        tw[i] = f32::from_bits(J9_TW38[i]);
    }

    let mut ws = vec![0f32; 512];
    kernel9_stage1(&src, &mut ws, &J9_IDX, &tw);
    dump("checks/.build/rust_ws1.bits", &ws);

    kernel9_stage2(&mut ws, &tw);
    dump("checks/.build/rust_ws2.bits", &ws);

    let mut dst = [0f32; 512];
    kernel9_final(&ws, &mut dst, &tw);
    dump("checks/.build/rust_kd.bits", &dst);
    println!("ok");
}
