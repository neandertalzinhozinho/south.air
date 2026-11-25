#[path = "j4_fft.rs"]
mod fft;

use std::collections::HashMap;

fn parse(path: &str) -> HashMap<String, Vec<u32>> {
    let s = std::fs::read_to_string(path).unwrap();
    let mut map = HashMap::new();
    let mut cur = String::new();
    let mut vals: Vec<u32> = Vec::new();
    for line in s.lines() {
        if line.starts_with("# ") {
            continue;
        }
        if line.len() >= 8 && line.chars().all(|c| c.is_ascii_hexdigit()) {
            vals.push(u32::from_str_radix(line, 16).unwrap());
        } else if !line.is_empty() {
            if !cur.is_empty() {
                map.insert(cur.clone(), std::mem::take(&mut vals));
            }
            cur = line.to_string();
        }
    }
    if !cur.is_empty() {
        map.insert(cur, vals);
    }
    map
}

fn main() {
    let order: usize = std::env::args().nth(1).unwrap().parse().unwrap();
    let m = parse(&format!("checks/.build/split{order}.bits"));
    let n = 1usize << order;
    let mut d: Vec<f32> = m["SRC"].iter().map(|b| f32::from_bits(*b)).collect();
    let tw: Vec<f32> = m["TW50"].iter().map(|b| f32::from_bits(*b)).collect();
    let out = &m["OUT"];
    let mode = std::env::args().nth(2).unwrap_or_else(|| "auto".to_string());
    if mode == "fast" {
        fft::split_ccs_fast(&mut d, n / 2, &tw);
    } else {
        fft::split_ccs(&mut d, n / 2, &tw);
    }
    let mut bad = 0usize;
    for i in 0..n + 2 {
        if d[i].to_bits() != out[i] {
            if bad < 12 {
                println!("OUT[{i}] got {:08x} want {:08x}", d[i].to_bits(), out[i]);
            }
            bad += 1;
        }
    }
    if let Ok(p) = std::env::var("FFT_DUMP") {
        let mut txt = String::new();
        for v in &d[..n + 2] {
            txt.push_str(&format!("{:08x}\n", v.to_bits()));
        }
        std::fs::write(p, txt).unwrap();
    }
    let mut maxerr = 0f64;
    let mut maxrel = 0f64;
    for i in 0..n + 2 {
        let want = f32::from_bits(out[i]) as f64;
        let got = d[i] as f64;
        let e = (got - want).abs();
        if e > maxerr {
            maxerr = e;
        }
        let rel = e / want.abs().max(1e-9);
        if rel > maxrel {
            maxrel = rel;
        }
    }
    println!(
        "split direct order {order} mode={mode}: bad={bad} / {} maxerr={maxerr:.3e} maxrel={maxrel:.3e}",
        n + 2
    );
}
