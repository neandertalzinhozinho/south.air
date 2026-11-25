//! gen_sine — gera o WAV de teste do oráculo (seno 1 kHz, 48 kHz, 1 s, estéreo).
//!
//! Uso:
//!   gen_sine <out.wav> [freq_hz] [taxa_hz] [segundos] [pico_L] [pico_R]
//!
//! Padrões: 1000 Hz, 48000 Hz, 1.0 s, pico L = 0.5, pico R = 0.25.
//! Os canais têm amplitudes diferentes **de propósito**: se o host trocar os
//! canais, o teste aparece na hora.
//!
//! Saída: WAV float32 (WAVE_FORMAT_IEEE_FLOAT), 2 canais.

use std::env;
use std::fs;

fn main() {
    let a: Vec<String> = env::args().collect();
    if a.len() < 2 {
        eprintln!("uso: gen_sine <out.wav> [freq_hz] [taxa_hz] [segundos] [pico_L] [pico_R]");
        std::process::exit(2);
    }
    let out = &a[1];
    let freq: f64 = a.get(2).and_then(|s| s.parse().ok()).unwrap_or(1000.0);
    let rate: u32 = a.get(3).and_then(|s| s.parse().ok()).unwrap_or(48000);
    let secs: f64 = a.get(4).and_then(|s| s.parse().ok()).unwrap_or(1.0);
    let pl: f32 = a.get(5).and_then(|s| s.parse().ok()).unwrap_or(0.5);
    let pr: f32 = a.get(6).and_then(|s| s.parse().ok()).unwrap_or(0.25);

    let frames = (secs * rate as f64).round() as usize;
    let channels: u16 = 2;
    let data_bytes = (frames * channels as usize * 4) as u32;

    let mut buf: Vec<u8> = Vec::with_capacity(58 + data_bytes as usize);
    buf.extend_from_slice(b"RIFF");
    buf.extend_from_slice(&(36u32 + 4 + data_bytes).to_le_bytes());
    buf.extend_from_slice(b"WAVE");

    buf.extend_from_slice(b"fmt ");
    buf.extend_from_slice(&16u32.to_le_bytes());
    buf.extend_from_slice(&3u16.to_le_bytes()); // IEEE float
    buf.extend_from_slice(&channels.to_le_bytes());
    buf.extend_from_slice(&rate.to_le_bytes());
    buf.extend_from_slice(&(rate * 8).to_le_bytes()); // byte rate (2 ch * 4 B)
    buf.extend_from_slice(&8u16.to_le_bytes()); // block align
    buf.extend_from_slice(&32u16.to_le_bytes()); // bits

    buf.extend_from_slice(b"fact");
    buf.extend_from_slice(&4u32.to_le_bytes());
    buf.extend_from_slice(&(frames as u32).to_le_bytes());

    buf.extend_from_slice(b"data");
    buf.extend_from_slice(&data_bytes.to_le_bytes());

    let two_pi = std::f64::consts::TAU;
    for n in 0..frames {
        let ph = two_pi * freq * (n as f64) / (rate as f64);
        let s = ph.sin() as f32;
        buf.extend_from_slice(&(s * pl).to_le_bytes());
        buf.extend_from_slice(&(s * pr).to_le_bytes());
    }

    if let Err(e) = fs::write(out, &buf) {
        eprintln!("erro ao gravar {out}: {e}");
        std::process::exit(1);
    }
    println!(
        "gravado {out}: {frames} frames, {rate} Hz, {channels} canais, {freq} Hz, {secs} s, pico L={pl} R={pr}"
    );
}
