//! Phase 4 oracle host: render a WAV through any VST3 (default: the installed
//! soothe3) so the port can be compared against the original.
//!
//! Usage: render-host <plugin.vst3|dll> <in.wav> <out.wav> [block]

#[path = "../host.rs"]
mod host;

use std::path::Path;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() < 3 {
        eprintln!("usage: render-host <plugin.vst3|dll> <in.wav> <out.wav> [block]");
        std::process::exit(2);
    }
    let plugin = Path::new(&args[0]);
    // Accept a bundle folder or the inner binary.
    let binary = if plugin.is_dir() {
        let name = plugin.file_name().unwrap().to_string_lossy().to_string();
        plugin.join("Contents").join("x86_64-win").join(name)
    } else {
        plugin.to_path_buf()
    };
    let block: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(512);
    match host::render_file(&binary, Path::new(&args[1]), Path::new(&args[2]), block) {
        Ok(r) => {
            println!(
                "rendered \"{}\": {} ch, {} Hz, {} blocks, latency {} samples -> {}",
                r.plugin, r.channels, r.sample_rate, r.blocks, r.latency_samples, args[2]
            );
        }
        Err(e) => {
            eprintln!("render failed: {e}");
            std::process::exit(1);
        }
    }
}
