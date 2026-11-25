#[path = "j4_fft.rs"]
mod fft;

use std::collections::HashMap;

fn parse(path: &str) -> HashMap<String, Vec<u32>> {
    let s = std::fs::read_to_string(path).unwrap();
    let mut map = HashMap::new();
    let mut cur = String::new();
    let mut vals: Vec<u32> = Vec::new();
    for line in s.lines() {
        if let Some(rest) = line.strip_prefix("# ") {
            let _ = rest;
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
    let mode = std::env::args().nth(2).unwrap_or_else(|| "rand".to_string());
    let path = format!("checks/.build/j{order}_stage_{mode}.bits");
    let m = parse(&path);
    let n = 1usize << order;
    let src: Vec<f32> = m["SRC"].iter().map(|b| f32::from_bits(*b)).collect();
    let kd: Vec<u32> = m["KD"].clone();
    let ws_gold: Vec<u32> = m["WS"].clone();
    let idx: Vec<u32> = m["IDX"].clone();
    let tw: Vec<f32> = m["TW38"].iter().map(|b| f32::from_bits(*b)).collect();

    let mut ws = vec![0f32; n];
    let mut dst = vec![0f32; n + 2];
    fft::kernel_generic(&src, &mut ws, &mut dst, &idx, &tw, n);

    let mut bad = 0usize;
    for i in 0..n {
        if dst[i].to_bits() != kd[i] {
            if bad < 6 {
                println!("dst[{i}] = {:08x} want {:08x}", dst[i].to_bits(), kd[i]);
            }
            bad += 1;
        }
    }
    println!("order {order}: dst bad={bad} / {n}");
    let mut wbad = 0usize;
    for i in 0..n {
        if ws[i].to_bits() != ws_gold[i] {
            if wbad < 6 {
                println!("ws[{i}] = {:08x} want {:08x}", ws[i].to_bits(), ws_gold[i]);
            }
            wbad += 1;
        }
    }
    println!("order {order}: ws bad={wbad} / {n}");
    if wbad > 0 {
        let first = (0..n).find(|&i| ws[i].to_bits() != ws_gold[i]).unwrap();
        let mut regions = [0usize; 64];
        for i in 0..n {
            if ws[i].to_bits() != ws_gold[i] {
                regions[(i * 64 / n).min(63)] += 1;
            }
        }
        println!("first ws mismatch at {first}; regions: {:?}", &regions[..]);
    }
    if let Ok(p) = std::env::var("FFT_DUMP") {
        let mut txt = String::new();
        for v in &dst[..n] {
            txt.push_str(&format!("{:08x}\n", v.to_bits()));
        }
        std::fs::write(p, txt).unwrap();
    }
}
