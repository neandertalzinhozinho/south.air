//! Aplicativo Resonia: a mesma tela do plugin, em janela própria, e as ferramentas de linha
//! de comando (montar o bundle VST3, conferi-lo, listar parâmetros, teste de carga).
//!
//! NOVO na fase 2 da recuperação (25/11/2026). O `main.rs` recuperado (26 425 B, exato) está em
//! `_arquivo_heuristico/recuperados_exatos/main.rs`: ele tocava áudio com o DSP heurístico
//! antigo (cpal), ajustava esse DSP contra o plugin original (`--fit`, `--score`,
//! `--prove-superiority`, `--compare`, `--measure-original`) e por isso saiu do caminho de
//! áudio. Aqui o processamento passa SÓ pela ponte `engine_bridge` (hoje passa-direto).
//!
//!   southair-app                              abre a janela
//!   southair-app --process in.wav out.wav     processa um WAV pela ponte (sem janela)
//!   southair-app --screenshot out.png         desenha ~60 quadros, salva a imagem e sai
//!   southair-app --make-vst3 southair.dll dir  monta dir/South.air.vst3 (com moduleinfo.json) e confere
//!   southair-app --check-vst3 South.air.vst3    confere o bundle
//!   southair-app --inspect-vst3 South.air.vst3  carrega o plugin e lista os parâmetros
//!   southair-app --selftest-vst3 South.air.vst3 carrega o plugin, processa ruído e confere o passa-direto

use eframe::egui;
use southair::engine_bridge::EngineBridge;
use southair::param_table::{PARAMS, PARAM_COUNT};
use southair::ui;
use std::path::{Path, PathBuf};

#[cfg(windows)]
mod vst3host;
#[cfg(windows)]
mod vst3tool;

struct Source {
    sr: f32,
    ch: [Vec<f32>; 2],
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
    Ok(Source { sr: spec.sample_rate as f32, ch: [l, r] })
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

/// Processa o arquivo inteiro pela ponte, em blocos, descontando a latência que a ponte informar.
fn process_file(src: &Source, params: &[f64; PARAM_COUNT]) -> Result<([Vec<f32>; 2], u32, String), String> {
    let block = 1024;
    let mut bridge = EngineBridge::new();
    bridge.prepare(src.sr, block, 2).map_err(|e| e.to_string())?;
    for (i, v) in params.iter().enumerate() {
        bridge.set_param(i, *v);
    }
    let lat = bridge.latency_samples() as usize;
    eprintln!("engine: {} ({:?}), latency {} samples", bridge.status().engine_text(), bridge.engine_kind(), lat);
    let total = src.ch[0].len() + lat;
    let mut out = [Vec::with_capacity(total), Vec::with_capacity(total)];
    let (mut l, mut r) = (vec![0.0f32; block], vec![0.0f32; block]);
    let mut pos = 0;
    while pos < total {
        let n = block.min(total - pos);
        for i in 0..n {
            l[i] = src.ch[0].get(pos + i).copied().unwrap_or(0.0);
            r[i] = src.ch[1].get(pos + i).copied().unwrap_or(0.0);
        }
        {
            let mut chans: [&mut [f32]; 2] = [&mut l[..n], &mut r[..n]];
            bridge.process(&mut chans, None);
        }
        out[0].extend_from_slice(&l[..n]);
        out[1].extend_from_slice(&r[..n]);
        pos += n;
    }
    for o in out.iter_mut() {
        o.drain(..lat.min(o.len()));
    }
    Ok((out, bridge.latency_samples(), bridge.status().engine_text().to_string()))
}

fn default_params() -> [f64; PARAM_COUNT] {
    let mut p = [0.0; PARAM_COUNT];
    for (v, s) in p.iter_mut().zip(PARAMS.iter()) {
        *v = s.default;
    }
    p
}

/// Parâmetros da janela do aplicativo; repassa cada mudança à ponte.
struct AppAccess<'a> {
    values: &'a mut [f64; PARAM_COUNT],
    bridge: &'a mut EngineBridge,
}

impl ui::ParamAccess for AppAccess<'_> {
    fn get(&self, index: usize) -> f64 {
        self.values.get(index).copied().unwrap_or(0.0)
    }
    fn set(&mut self, index: usize, value: f64) {
        if let Some(slot) = self.values.get_mut(index) {
            *slot = value.clamp(PARAMS[index].min, PARAMS[index].max);
            self.bridge.set_param(index, value);
        }
    }
}

struct App {
    values: [f64; PARAM_COUNT],
    bridge: EngineBridge,
    ui_state: ui::UiState,
    screenshot: Option<PathBuf>,
    frames: u32,
    shot_sent: bool,
}

impl App {
    fn new(cc: &eframe::CreationContext, screenshot: Option<PathBuf>) -> Self {
        ui::setup_style(&cc.egui_ctx);
        let mut bridge = EngineBridge::new();
        let _ = bridge.prepare(48_000.0, 1024, 2);
        Self { values: default_params(), bridge, ui_state: ui::UiState::default(), screenshot, frames: 0, shot_sent: false }
    }
}

impl eframe::App for App {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        let st = self.bridge.status();
        let detail = st.detail();
        let info = ui::UiInfo {
            version: env!("CARGO_PKG_VERSION"),
            engine: st.engine_text(),
            latency_samples: self.bridge.latency_samples(),
            sample_rate: self.bridge.sample_rate(),
            analysis: st.analysis(),
            status: Some(if detail.is_empty() { "Standalone window: parameters only, no audio device." } else { detail.as_str() }),
        };
        if self.frames == 0 && self.screenshot.is_some() {
            if let Ok(v) = std::env::var("RESONIA_SHOT_VIEW") {
                self.ui_state.show_view(&v);
            }
        }
        let mut access = AppAccess { values: &mut self.values, bridge: &mut self.bridge };
        ui::draw(ctx, &mut access, &info, &mut self.ui_state);

        // --screenshot: desenha alguns quadros, depois salva a imagem da janela
        if let Some(path) = self.screenshot.clone() {
            self.frames += 1;
            if self.frames >= 60 && !self.shot_sent {
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
    println!("South.air by NDERTAL labs");
    println!();
    println!("usage:");
    println!("  southair-app                               open the window");
    println!("  southair-app --process in.wav out.wav      run a WAV file through the engine bridge");
    println!("  southair-app --screenshot out.png          save a picture of the window and exit");
    println!("  southair-app --make-vst3 southair.dll dir   build dir/South.air.vst3 (with moduleinfo.json) and check it");
    println!("  southair-app --check-vst3 South.air.vst3     check the bundle");
    println!("  southair-app --inspect-vst3 South.air.vst3   load the plugin and list its parameters");
    println!("  southair-app --selftest-vst3 South.air.vst3  load the plugin, process noise, check pass-through");
}

#[cfg(windows)]
fn selftest(bundle: &Path) -> Result<Vec<String>, String> {
    let mut out = Vec::new();
    let mut p = vst3host::Plugin::load(bundle)?;
    out.push(format!("ok  loaded            {} ({} parameters)", p.name(), p.params.len()));
    if p.params.len() != PARAM_COUNT {
        return Err(format!("expected {PARAM_COUNT} parameters, plugin has {}", p.params.len()));
    }
    for (q, s) in p.params.iter().zip(PARAMS.iter()) {
        if q.title != s.name {
            return Err(format!("parameter {} is '{}', table says '{}'", s.id, q.title, s.name));
        }
    }
    out.push("ok  parameters        143 names match the table".to_string());
    p.activate(48_000.0, 512)?;
    out.push(format!("ok  activated         latency reported: {} samples", p.latency));
    // ruído determinístico (xorshift), 1 s, estéreo
    let mut x: u32 = 0x1234_5678;
    let mut next = || {
        x ^= x << 13;
        x ^= x >> 17;
        x ^= x << 5;
        (x as f32 / u32::MAX as f32) * 1.6 - 0.8
    };
    let n = 48_000;
    let input = [(0..n).map(|_| next()).collect::<Vec<f32>>(), (0..n).map(|_| next()).collect::<Vec<f32>>()];
    let output = p.run(&input)?;
    let lat = p.latency as usize;
    if lat != 0 {
        // Motor ativo (latência > 0): a saída é processada, não é cópia da entrada.
        let mut peak = 0f32;
        let mut finite = true;
        for c in 0..2 {
            for i in lat..n {
                finite &= output[c][i].is_finite();
                peak = peak.max(output[c][i].abs());
            }
        }
        if !finite || peak == 0.0 {
            return Err(format!("engine output is silent or not finite (peak {peak})"));
        }
        out.push(format!("ok  engine output     processed audio, peak {peak:.4}, latency {lat} samples (pass-through check skipped)"));
        return Ok(out);
    }
    let mut bad = 0usize;
    for c in 0..2 {
        for i in lat..n {
            if output[c][i].to_bits() != input[c][i - lat].to_bits() {
                bad += 1;
            }
        }
    }
    if bad != 0 {
        return Err(format!("{bad} samples differ from the input (pass-through expected)"));
    }
    out.push(format!("ok  pass-through      {} samples x 2 channels bit-identical to the input", n - lat));
    Ok(out)
}

fn hard_exit_if_windows(code: i32) -> ! {
    use std::io::Write as _;
    let _ = std::io::stdout().flush();
    let _ = std::io::stderr().flush();
    std::process::exit(code)
}

/// Carimbo de build (só muda o hash do .exe; contorno do Smart App Control, os error 4551).
const BUILD_STAMP: Option<&str> = option_env!("RESONIA_STAMP");

fn main() {
    let _ = BUILD_STAMP;
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut screenshot = None;
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
            #[cfg(windows)]
            "--make-vst3" => {
                let (Some(dll), Some(out)) = (args.get(i + 1), args.get(i + 2)) else {
                    eprintln!("--make-vst3 needs the built plugin library and an output folder");
                    std::process::exit(2);
                };
                match vst3tool::make_bundle(Path::new(dll), Path::new(out), "South.air", env!("CARGO_PKG_VERSION"))
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
            #[cfg(windows)]
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
            #[cfg(windows)]
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
            #[cfg(windows)]
            "--selftest-vst3" => {
                let Some(b) = args.get(i + 1) else {
                    eprintln!("--selftest-vst3 needs a .vst3 bundle folder");
                    std::process::exit(2);
                };
                match selftest(Path::new(b)) {
                    Ok(lines) => {
                        lines.iter().for_each(|l| println!("{l}"));
                        hard_exit_if_windows(0)
                    }
                    Err(e) => {
                        eprintln!("self-test failed: {e}");
                        hard_exit_if_windows(1)
                    }
                }
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
                let (data, lat, kind_text) = match process_file(&src, &default_params()) {
                    Ok(d) => d,
                    Err(e) => {
                        eprintln!("{e}");
                        std::process::exit(1);
                    }
                };
                if let Err(e) = write_wav(Path::new(out), src.sr, &data) {
                    eprintln!("{e}");
                    std::process::exit(1);
                }
                println!("processed {} samples at {} Hz through the engine bridge ({}, latency {} samples compensated) -> {}", data[0].len(), src.sr, kind_text, lat, out);
                return;
            }
            other => {
                eprintln!("unknown option {other}");
                usage();
                std::process::exit(2);
            }
        }
        i += 1;
    }

    let mut vp = egui::ViewportBuilder::default()
        .with_title("South.air")
        .with_inner_size([ui::WIDTH, ui::HEIGHT])
        .with_min_inner_size([900.0, 560.0]);
    if screenshot.is_some() {
        vp = vp.with_active(false);
        #[cfg(windows)]
        {
            vp = vp.with_window_level(egui::WindowLevel::AlwaysOnBottom);
        }
    }
    let options = eframe::NativeOptions { viewport: vp, run_and_return: true, ..Default::default() };
    let shot = screenshot.clone();
    if let Err(e) = eframe::run_native("South.air", options, Box::new(move |cc| Ok(Box::new(App::new(cc, shot))))) {
        eprintln!("could not open the window: {e}");
        std::process::exit(1);
    }
}
