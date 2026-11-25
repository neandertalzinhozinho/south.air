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
    let path = format!("checks/.build/j{order}_stage_rand.bits");
    let m = parse(&path);
    let n = 1usize << order;
    let src: Vec<f32> = m["SRC"].iter().map(|b| f32::from_bits(*b)).collect();
    let tw38: Vec<f32> = m["TW38"].iter().map(|b| f32::from_bits(*b)).collect();
    let tw50: Vec<f32> = m["TW50"].iter().map(|b| f32::from_bits(*b)).collect();
    let idx: Vec<u32> = m["IDX"].clone();
    let fwd = &m["FWD"];
    let got = fft::rfft_generic(&src, &tw38, &idx, &tw50, n);
    let mut bad = 0usize;
    for i in 0..n + 2 {
        if got[i].to_bits() != fwd[i] {
            if bad < 8 {
                println!(
                    "FWD[{i}] got {:08x} want {:08x}",
                    got[i].to_bits(),
                    fwd[i]
                );
            }
            bad += 1;
        }
    }
    println!("order {order}: FWD bad={bad} / {}", n + 2);
    println!(
        "split path = {}",
        if n / 2 >= 0x40000 { "slow" } else { "fast" }
    );
}
