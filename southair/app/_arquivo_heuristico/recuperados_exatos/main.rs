//! Resonia desktop app: the same engine and screen as the plugin, with a built-in
//! test sound, WAV loading (drag a file onto the window), playback and export.
//!
//!   resonia-app [file.wav]                 open the window
//!   resonia-app --process in.wav out.wav   process a file without a window
//!   resonia-app --screenshot out.png       draw ~120 frames, save a picture, exit

use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use eframe::egui;
use resonia::dsp::{Analysis, Processor};
use resonia::settings::Settings;
use resonia::ui;
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};

#[cfg(windows)]
mod vst3tool;
#[cfg(windows)]
mod vst3host;
#[cfg(windows)]
mod equivalence;
#[cfg(windows)]
mod calibrate;

/// End the process without running library shutdown code (the original plugin's
/// copy protection crashes while Windows unloads it).
#[cfg(windows)]
fn hard_exit(code: u32) -> ! {
    use std::io::Write as _;
    let _ = std::io::stdout().flush();
    let _ = std::io::stderr().flush();
    extern "system" {
        fn GetCurrentProcess() -> *mut std::ffi::c_void;
        fn TerminateProcess(p: *mut std::ffi::c_void, code: u32) -> i32;
    }
    unsafe {
        TerminateProcess(GetCurrentProcess(), code);
    }
    std::process::exit(code as i32)
}

struct Source {
    name: String,
    sr: f32,
    /// stereo samples
    ch: [Vec<f32>; 2],
}

fn demo_source() -> Source {
    // Pink-ish noise, a harsh ringing peak near 3.2 kHz, a whistle near 6.3 kHz
    // and a low hum with harmonics: something with obvious resonances.
    let sr = 48000.0f32;
    let len = (sr * 8.0) as usize;
    let mut seed = 0x1234_5678u32;
    let mut rnd = || {
        seed ^= seed << 13;
        seed ^= seed >> 17;
        seed ^= seed << 5;
        (seed as f32 / u32::MAX as f32) * 2.0 - 1.0
    };
    let mut b = [0.0f32; 3];
    // resonant band-pass (biquad) at 3.2 kHz, Q 30
    let bp = |f: f32, q: f32| {
        let w = 2.0 * std::f32::consts::PI * f / sr;
        let alpha = w.sin() / (2.0 * q);
        let a0 = 1.0 + alpha;
        [alpha / a0, 0.0, -alpha / a0, -2.0 * w.cos() / a0, (1.0 - alpha) / a0]
    };
    let c = bp(3200.0, 30.0);
    let (mut x1, mut x2, mut y1, mut y2) = (0.0f32, 0.0f32, 0.0f32, 0.0f32);
    let mut l = Vec::with_capacity(len);
    let mut r = Vec::with_capacity(len);
    for i in 0..len {
        let t = i as f32 / sr;
        let w = rnd();
        b[0] = 0.997 * b[0] + 0.029 * w;
        b[1] = 0.985 * b[1] + 0.032 * w;
        b[2] = 0.950 * b[2] + 0.048 * w;
        let pink = (b[0] + b[1] + b[2] + 0.02 * w) * 0.9;
        let y = c[0] * w + c[1] * x1 + c[2] * x2 - c[3] * y1 - c[4] * y2;
        x2 = x1;
        x1 = w;
        y2 = y1;
        y1 = y;
        let env = 0.6 + 0.4 * (2.0 * std::f32::consts::PI * 0.5 * t).sin();
        let ring = y * 1.6 * env;
        let whistle = 0.05 * (2.0 * std::f32::consts::PI * (6300.0 + 40.0 * (6.0 * t).sin()) * t).sin();
        let hum: f32 = (1..6).map(|h| 0.04 / h as f32 * (2.0 * std::f32::consts::PI * 110.0 * h as f32 * t).sin()).sum();
        let s = pink * 0.5 + ring + whistle + hum;
        l.push(s * 0.8);
        r.push(s * 0.75 + rnd() * 0.01);
    }
    Source { name: "built-in test sound".into(), sr, ch: [l, r] }
}

fn load_wav(path: &Path) -> Result<Source, String> {
    let mut rd = hound::WavReader::open(path).map_err(|e| format!("cannot open {}: {e}", path.display()))?;
    let spec = rd.spec();
    let chans = spec.channels.max(1) as usize;
    let samples: Vec<f32> = match spec.sample_format {
        hound::SampleFormat::Float => rd.samples::<f32>().map(|s| s.unwrap_or(0.0)).collect(),
        hound::SampleFormat::Int => {
            let scale = 1.0 / (1u64 << (spec.bits_per_sample.max(1) - 1)) as f32;
            rd.samples::<i32>().map(|s| s.unwrap_or(0) as f32 * scale).collect()
        }
    };
    let frames = samples.len() / chans;
    if frames == 0 {
        return Err(format!("{} has no audio", path.display()));
    }
    let mut l = Vec::with_capacity(frames);
    let mut r = Vec::with_capacity(frames);
    for f in 0..frames {
        l.push(samples[f * chans]);
        r.push(samples[f * chans + (chans > 1) as usize]);
    }
    let name = path.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();
    Ok(Source { name, sr: spec.sample_rate as f32, ch: [l, r] })
}

/// Process a whole file with the given settings, delay removed. Returns the peak reduction seen.
fn process_file(src: &Source, s: &Settings) -> ([Vec<f32>; 2], f32) {
    let mut proc = Processor::new(src.sr);
    let lat = proc.latency_for(s);
    let total = src.ch[0].len() + lat;
    let mut out = [Vec::with_capacity(total), Vec::with_capacity(total)];
    let mut a = Analysis::default();
    let mut peak = 0.0f32;
    let block = 1024;
    let mut pos = 0;
    let mut l = vec![0.0f32; block];
    let mut r = vec![0.0f32; block];
    while pos < total {
        let n = block.min(total - pos);
        for i in 0..n {
            l[i] = src.ch[0].get(pos + i).copied().unwrap_or(0.0);
            r[i] = src.ch[1].get(pos + i).copied().unwrap_or(0.0);
        }
        {
            let mut chans: [&mut [f32]; 2] = [&mut l[..n], &mut r[..n]];
            proc.process(&mut chans, None, s);
        }
        proc.copy_analysis(&mut a, s);
        peak = peak.max(a.max_reduction_now);
        out[0].extend_from_slice(&l[..n]);
        out[1].extend_from_slice(&r[..n]);
        pos += n;
    }
    for o in out.iter_mut() {
        o.drain(..lat.min(o.len()));
    }
    (out, peak)
}

fn write_wav(path: &Path, sr: f32, ch: &[Vec<f32>; 2]) -> Result<(), String> {
    let spec = hound::WavSpec { channels: 2, sample_rate: sr as u32, bits_per_sample: 32, sample_format: hound::SampleFormat::Float };
    let mut w = hound::WavWriter::create(path, spec).map_err(|e| format!("cannot write {}: {e}", path.display()))?;
    for i in 0..ch[0].len() {
        w.write_sample(ch[0][i]).map_err(|e| e.to_string())?;
        w.write_sample(ch[1][i]).map_err(|e| e.to_string())?;
    }
    w.finalize().map_err(|e| e.to_string())
}

fn export_path(src_path: &Path) -> PathBuf {
    let stem = src_path.file_stem().map(|s| s.to_string_lossy().to_string()).unwrap_or_else(|| "audio".into());
    src_path.with_file_name(format!("{stem}_resonia.wav"))
}

/// Live playback through the default output device.
struct Player {
    _stream: cpal::Stream,
}

fn start_player(src: Arc<Source>, settings: Arc<Mutex<Settings>>, analysis: Arc<Mutex<Analysis>>) -> Result<Player, String> {
    let host = cpal::default_host();
    let dev = host.default_output_device().ok_or("no audio output device found")?;
    let cfg = dev.default_output_config().map_err(|e| e.to_string())?;
    if cfg.sample_format() != cpal::SampleFormat::F32 {
        return Err(format!("audio device format {:?} is not supported", cfg.sample_format()));
    }
    let out_ch = cfg.channels() as usize;
    let dev_sr = cfg.sample_rate().0 as f32;
    let mut proc = Processor::new(dev_sr);
    let step = src.sr / dev_sr;
    let mut pos = 0.0f64;
    let mut l = vec![0.0f32; 8192];
    let mut r = vec![0.0f32; 8192];
    let mut current = settings.lock().map(|s| s.clone()).unwrap_or_default();
    let stream = dev
        .build_output_stream(
            &cfg.into(),
            move |data: &mut [f32], _| {
                if let Ok(s) = settings.try_lock() {
                    if *s != current {
                        current = s.clone();
                    }
                }
                let frames = (data.len() / out_ch).min(l.len());
                let len = src.ch[0].len();
                for i in 0..frames {
                    let p = pos as usize % len;
                    l[i] = src.ch[0][p];
                    r[i] = src.ch[1][p];
                    pos += step as f64;
                    if pos >= len as f64 {
                        pos -= len as f64;
                    }
                }
                {
                    let mut chans: [&mut [f32]; 2] = [&mut l[..frames], &mut r[..frames]];
                    proc.process(&mut chans, None, &current);
                }
                if let Ok(mut a) = analysis.try_lock() {
                    proc.copy_analysis(&mut a, &current);
                }
                for i in 0..frames {
                    for c in 0..out_ch {
                        data[i * out_ch + c] = if c % 2 == 0 { l[i] } else { r[i] };
                    }
                }
                for x in data[frames * out_ch..].iter_mut() {
                    *x = 0.0;
                }
            },
            |e| eprintln!("audio error: {e}"),
            None,
        )
        .map_err(|e| e.to_string())?;
    stream.play().map_err(|e| e.to_string())?;
    Ok(Player { _stream: stream })
}

struct App {
    settings: Settings,
    shared_settings: Arc<Mutex<Settings>>,
    analysis: Arc<Mutex<Analysis>>,
    ui_state: ui::UiState,
    source: Arc<Source>,
    source_path: Option<PathBuf>,
    /// engine used to animate the screen while nothing is playing
    preview: Processor,
    preview_pos: usize,
    player: Option<Player>,
    status: String,
    screenshot: Option<PathBuf>,
    frames: u32,
    shot_sent: bool,
}

impl App {
    fn new(cc: &eframe::CreationContext, source: Source, path: Option<PathBuf>, screenshot: Option<PathBuf>) -> Self {
        ui::setup_style(&cc.egui_ctx);
        // the desktop app opens on a preset so the band nodes are visible with the test sound
        let settings = resonia::settings::factory_presets()[1].1.clone();
        let preview = Processor::new(source.sr);
        Self {
            shared_settings: Arc::new(Mutex::new(settings.clone())),
            settings,
            analysis: Arc::new(Mutex::new(Analysis::default())),
            ui_state: ui::UiState { preset: 1, ..Default::default() },
            status: format!("Source: {}  (drag a WAV file onto the window to load it)", source.name),
            source: Arc::new(source),
            source_path: path,
            preview,
            preview_pos: 0,
            player: None,
            screenshot,
            frames: 0,
            shot_sent: false,
        }
    }

    fn set_source(&mut self, src: Source, path: Option<PathBuf>) {
        self.player = None;
        self.preview = Processor::new(src.sr);
        self.preview_pos = 0;
        self.status = format!("Source: {}", src.name);
        self.source = Arc::new(src);
        self.source_path = path;
    }

    fn advance_preview(&mut self, dt: f32) {
        let n = ((dt.clamp(0.005, 0.05)) * self.source.sr) as usize;
        let len = self.source.ch[0].len();
        let mut l = Vec::with_capacity(n);
        let mut r = Vec::with_capacity(n);
        for i in 0..n {
            let p = (self.preview_pos + i) % len;
            l.push(self.source.ch[0][p]);
            r.push(self.source.ch[1][p]);
        }
        self.preview_pos = (self.preview_pos + n) % len;
        let mut chans: [&mut [f32]; 2] = [&mut l[..], &mut r[..]];
        self.preview.process(&mut chans, None, &self.settings);
        if let Ok(mut a) = self.analysis.lock() {
            self.preview.copy_analysis(&mut a, &self.settings);
        }
    }

    fn export(&mut self) {
        let path = self.source_path.clone().map(|p| export_path(&p)).unwrap_or_else(|| {
            std::env::current_dir().unwrap_or_default().join("test_sound_resonia.wav")
        });
        let (out, peak) = process_file(&self.source, &self.settings);
        self.status = match write_wav(&path, self.source.sr, &out) {
            Ok(()) => format!("Saved {} (peak cut {:.1} dB)", path.display(), peak),
            Err(e) => format!("Export failed: {e}"),
        };
    }
}

impl eframe::App for App {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // dropped files
        let dropped: Vec<PathBuf> = ctx.input(|i| i.raw.dropped_files.iter().filter_map(|f| f.path.clone()).collect());
        if let Some(p) = dropped.into_iter().next() {
            match load_wav(&p) {
                Ok(src) => self.set_source(src, Some(p)),
                Err(e) => self.status = e,
            }
        }

        if self.player.is_none() {
            let dt = ctx.input(|i| i.stable_dt);
            self.advance_preview(if self.screenshot.is_some() { 0.03 } else { dt });
        }
        let snapshot = self.analysis.lock().map(|a| a.clone()).unwrap_or_default();

        let mut play_clicked = false;
        let mut export_clicked = false;
        let playing = self.player.is_some();
        let before = self.settings.clone();
        let status = self.status.clone();
        ui::draw(ctx, &mut self.settings, &snapshot, &mut self.ui_state, Some(&status), &mut |ui| {
            ui.add_space(8.0);
            if ui.add(egui::Button::new(if playing { "■ stop" } else { "▶ play" }).selected(playing)).on_hover_text("Play the sound through the effect.").clicked() {
                play_clicked = true;
            }
            if ui.button("export").on_hover_text("Save the processed sound as a new WAV file.").clicked() {
                export_clicked = true;
            }
        });
        if self.settings != before {
            if let Ok(mut s) = self.shared_settings.lock() {
                *s = self.settings.clone();
            }
        }

        if play_clicked {
            if self.player.is_some() {
                self.player = None;
            } else {
                match start_player(self.source.clone(), self.shared_settings.clone(), self.analysis.clone()) {
                    Ok(p) => {
                        self.player = Some(p);
                        self.status = format!("Playing: {}", self.source.name);
                    }
                    Err(e) => self.status = format!("Cannot play: {e}"),
                }
            }
        }
        if export_clicked {
            self.export();
        }

        // --screenshot: draw about 120 frames, then save the window's picture
        if let Some(path) = self.screenshot.clone() {
            self.frames += 1;
            if self.frames >= 120 && !self.shot_sent {
                ctx.send_viewport_cmd(egui::ViewportCommand::Screenshot(egui::UserData::default()));
                self.shot_sent = true;
            }
            let shot = ctx.input(|i| {
                i.raw.events.iter().find_map(|e| match e {
                    egui::Event::Screenshot { image, .. } => Some(image.clone()),
                    _ => None,
                })
            });
            if let Some(img) = shot {
                let [w, h] = img.size;
                let bytes: Vec<u8> = img.pixels.iter().flat_map(|c| c.to_array()).collect();
                let result = image::RgbaImage::from_raw(w as u32, h as u32, bytes)
                    .ok_or_else(|| "bad image".to_string())
                    .and_then(|im| im.save(&path).map_err(|e| e.to_string()));
                match result {
                    Ok(()) => println!("saved screenshot to {}", path.display()),
                    Err(e) => {
                        eprintln!("could not save screenshot: {e}");
                        std::process::exit(1);
                    }
                }
                ctx.send_viewport_cmd(egui::ViewportCommand::Close);
            }
        }
        ctx.request_repaint();
    }
}

fn usage() {
    println!("Resonia - dynamic resonance smoother");
    println!();
    println!("usage:");
    println!("  resonia-app [file.wav]                 open the window (optionally with a WAV file)");
    println!("  resonia-app --process in.wav out.wav   process a WAV file with the default settings");
    println!("  resonia-app --screenshot out.png       save a picture of the window and exit");
    println!("  resonia-app --make-vst3 resonia.dll dir   build dir/Resonia.vst3 (with moduleinfo.json) and check it");
    println!("  resonia-app --check-vst3 Resonia.vst3  load the plugin and check the bundle");
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut screenshot = None;
    let mut input = None;
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "-h" | "--help" => {
                usage();
                return;
            }
            "--screenshot" => {
                let Some(p) = args.get(i + 1) else {
                    eprintln!("--screenshot needs a file name");
                    std::process::exit(2);
                };
                screenshot = Some(PathBuf::from(p));
                i += 1;
            }
            "--make-vst3" => {
                let (Some(dll), Some(out)) = (args.get(i + 1), args.get(i + 2)) else {
                    eprintln!("--make-vst3 needs the built plugin library and an output folder");
                    std::process::exit(2);
                };
                match vst3tool::make_bundle(Path::new(dll), Path::new(out), "Resonia", env!("CARGO_PKG_VERSION"))
                    .and_then(|b| vst3tool::check_bundle(&b).map(|lines| (b, lines)))
                {
                    Ok((b, lines)) => {
                        println!("built {}", b.display());
                        lines.iter().for_each(|l| println!("{l}"));
                    }
                    Err(e) => {
                        eprintln!("VST3 bundle failed: {e}");
                        std::process::exit(1);
                    }
                }
                return;
            }
            "--inspect-vst3" => {
                let Some(b) = args.get(i + 1) else {
                    eprintln!("--inspect-vst3 needs a .vst3 bundle folder");
                    std::process::exit(2);
                };
                match vst3host::Plugin::load(Path::new(b)) {
                    Ok(p) => {
                        println!("{}: {} parameters", p.name(), p.params.len());
                        for q in &p.params {
                            println!(
                                "{:>10}  {:<28} default {:<14} min {:<14} max {:<14} steps {} units '{}' flags {}",
                                q.id, q.title, q.default_text, q.min_text, q.max_text, q.steps, q.units, q.flags
                            );
                        }
                    }
                    Err(e) => {
                        eprintln!("could not open the plugin: {e}");
                        std::process::exit(1);
                    }
                }
                return;
            }
            "--measure-original" => {
                let Some(b) = args.get(i + 1) else {
                    eprintln!("--measure-original needs the original .vst3 bundle");
                    std::process::exit(2);
                };
                let cache = args.get(i + 2).map(PathBuf::from).unwrap_or_else(|| PathBuf::from("equivalence/original-curves.tsv"));
                match calibrate::measure_original(Path::new(b), &cache) {
                    Ok(log) => {
                        print!("{log}");
                        println!("saved {}", cache.display());
                        hard_exit(0);
                    }
                    Err(e) => {
                        eprintln!("measurement failed: {e}");
                        hard_exit(1);
                    }
                }
            }
            "--fit" => {
                let rounds = args.get(i + 1).and_then(|r| r.parse().ok()).unwrap_or(4);
                match calibrate::fit(Path::new("equivalence/original-curves.tsv"), rounds) {
                    Ok(t) => println!("{t}"),
                    Err(e) => {
                        eprintln!("fit failed: {e}");
                        std::process::exit(1);
                    }
                }
                return;
            }
            "--score" => {
                let cache = args.get(i + 1).map(PathBuf::from).unwrap_or_else(|| PathBuf::from("equivalence/original-curves.tsv"));
                let report = args.get(i + 2).map(PathBuf::from);
                match calibrate::score(&cache, report.is_some()) {
                    Ok((text, avg)) => {
                        if let Some(r) = report {
                            let head = "# Resonia vs the original: measured\n\nThe original was measured once in the test host (`--measure-original`) over the settings below; Resonia's engine runs the same test signals with the same settings. Curves are the power change in 1/6-octave bands, after removing each one's delay. Similarity: correlation of the curves (1 = same shape). Avg diff: mean absolute difference per band.\n\n";
                            if let Err(e) = std::fs::write(&r, format!("{head}{text}")) {
                                eprintln!("cannot write {}: {e}", r.display());
                            }
                        }
                        println!("{text}");
                        println!("overall avg diff {avg:.3} dB");
                    }
                    Err(e) => {
                        eprintln!("scoring failed: {e}");
                        std::process::exit(1);
                    }
                }
                return;
            }
            "--prove-superiority" => {
                let cache = args.get(i + 1).map(PathBuf::from).unwrap_or_else(|| PathBuf::from("equivalence/original-curves.tsv"));
                let report = args.get(i + 2).map(PathBuf::from).unwrap_or_else(|| PathBuf::from("equivalence/superiority-report.md"));
                match calibrate::prove_superiority(&cache, &report) {
                    Ok((text, true)) => println!("{text}"),
                    Ok((text, false)) => {
                        eprintln!("{text}");
                        std::process::exit(1);
                    }
                    Err(e) => {
                        eprintln!("superiority test failed: {e}");
                        std::process::exit(1);
                    }
                }
                return;
            }
            "--compare" => {
                let (Some(a), Some(b)) = (args.get(i + 1), args.get(i + 2)) else {
                    eprintln!("--compare needs two .vst3 bundles: the original and Resonia");
                    std::process::exit(2);
                };
                let out = args.get(i + 3).map(PathBuf::from).unwrap_or_else(|| PathBuf::from("equivalence-report.md"));
                let code = match equivalence::compare(Path::new(a), Path::new(b), &out) {
                    Ok(summary) => {
                        println!("{summary}\nreport written to {}", out.display());
                        0
                    }
                    Err(e) => {
                        eprintln!("comparison failed: {e}");
                        1
                    }
                };
                // The original's copy protection crashes the process while Windows unloads
                // it at exit, so end without running library shutdown code.
                use std::io::Write as _;
                let _ = std::io::stdout().flush();
                let _ = std::io::stderr().flush();
                extern "system" {
                    fn GetCurrentProcess() -> *mut std::ffi::c_void;
                    fn TerminateProcess(p: *mut std::ffi::c_void, code: u32) -> i32;
                }
                unsafe {
                    TerminateProcess(GetCurrentProcess(), code);
                }
                return;
            }
            "--check-vst3" => {
                let Some(b) = args.get(i + 1) else {
                    eprintln!("--check-vst3 needs a .vst3 bundle folder");
                    std::process::exit(2);
                };
                match vst3tool::check_bundle(Path::new(b)) {
                    Ok(lines) => lines.iter().for_each(|l| println!("{l}")),
                    Err(e) => {
                        eprintln!("VST3 check failed: {e}");
                        std::process::exit(1);
                    }
                }
                return;
            }
            "--process" => {
                let (Some(inp), Some(out)) = (args.get(i + 1), args.get(i + 2)) else {
                    eprintln!("--process needs an input and an output file");
                    std::process::exit(2);
                };
                let src = match load_wav(Path::new(inp)) {
                    Ok(s) => s,
                    Err(e) => {
                        eprintln!("{e}");
                        std::process::exit(1);
                    }
                };
                let s = Settings::default();
                let (data, peak) = process_file(&src, &s);
                if let Err(e) = write_wav(Path::new(out), src.sr, &data) {
                    eprintln!("{e}");
                    std::process::exit(1);
                }
                println!("processed {} samples at {} Hz, peak cut {:.1} dB -> {}", data[0].len(), src.sr, peak, out);
                return;
            }
            other if other.starts_with('-') => {
                eprintln!("unknown option {other}");
                usage();
                std::process::exit(2);
            }
            other => input = Some(PathBuf::from(other)),
        }
        i += 1;
    }

    let (source, path) = match &input {
        Some(p) => match load_wav(p) {
            Ok(s) => (s, Some(p.clone())),
            Err(e) => {
                eprintln!("{e}");
                (demo_source(), None)
            }
        },
        None => (demo_source(), None),
    };

    let mut vp = egui::ViewportBuilder::default()
        .with_title("Resonia")
        .with_inner_size([ui::WIDTH, ui::HEIGHT + 24.0])
        .with_min_inner_size([900.0, 560.0])
        .with_drag_and_drop(true);
    if screenshot.is_some() {
        vp = vp.with_active(false);
        #[cfg(windows)]
        {
            vp = vp.with_window_level(egui::WindowLevel::AlwaysOnBottom);
        }
    }
    let options = eframe::NativeOptions { viewport: vp, run_and_return: true, ..Default::default() };
    let shot = screenshot.clone();
    if let Err(e) = eframe::run_native("Resonia", options, Box::new(move |cc| Ok(Box::new(App::new(cc, source, path, shot))))) {
        eprintln!("could not open the window: {e}");
        std::process::exit(1);
    }
}
