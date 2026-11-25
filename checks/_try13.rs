#[path = "j4_fft.rs"]
mod fft;

include!("j13_golden.rs");

fn main() {
    let n = 1usize << 13;
    let src: Vec<f32> = J13_SRC.iter().map(|b| f32::from_bits(*b)).collect();
    let tw: Vec<f32> = J13_TW38.iter().map(|b| f32::from_bits(*b)).collect();
    let mut ws = vec![0f32; n];
    let mut dst = vec![0f32; n + 2];
    fft::kernel_generic(&src, &mut ws, &mut dst, &J13_IDX, &tw, n);
    let mut bad = 0;
    for i in 0..n {
        if dst[i].to_bits() != J13_KD[i] {
            if bad < 5 {
                println!("dst[{i}] = {:08x} want {:08x}", dst[i].to_bits(), J13_KD[i]);
            }
            bad += 1;
        }
    }
    println!("bad={bad} / {n}");

    let mut ws_bad = 0;
    for i in 0..n {
        if ws[i].to_bits() != J13_WS[i] {
            if ws_bad < 5 {
                println!("ws[{i}] = {:08x} want {:08x}", ws[i].to_bits(), J13_WS[i]);
            }
            ws_bad += 1;
        }
    }
    println!("ws_bad={ws_bad} / {n}");
}
