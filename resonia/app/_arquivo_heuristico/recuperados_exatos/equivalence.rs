//! Equivalence test: the same test signals through the original plugin and through
//! Resonia, both loaded as VST3 plugins, then their gain changes compared band by band.

use crate::vst3host::Plugin;
use realfft::RealFftPlanner;
use std::fmt::Write as _;
use std::path::Path;

pub const SR: f64 = 48000.0;
const SECONDS: f64 = 6.0;
const BLOCK: usize = 512;
const FFT: usize = 4096;
/// Analysis starts after this, so both plugins have settled.
const SKIP_SECONDS: f64 = 2.0;

struct Rng(u32);
impl Rng {
    fn next(&mut self) -> f32 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 17;
        self.0 ^= self.0 << 5;
        (self.0 as f32 / u32::MAX as f32) * 2.0 - 1.0
    }
}

fn biquad_bp(x: &[f32], f: f32, q: f32) -> Vec<f32> {
    let w = 2.0 * std::f32::consts::PI * f / SR as f32;
    let alpha = w.sin() / (2.0 * q);
    let a0 = 1.0 + alpha;
    let (b0, b2, a1, a2) = (alpha / a0, -alpha / a0, -2.0 * w.cos() / a0, (1.0 - alpha) / a0);
    let (mut x1, mut x2, mut y1, mut y2) = (0.0f32, 0.0f32, 0.0f32, 0.0f32);
    x.iter()
        .map(|&v| {
            let y = b0 * v + b2 * x2 - a1 * y1 - a2 * y2;
            x2 = x1;
            x1 = v;
            y2 = y1;
            y1 = y;
            y
        })
        .collect()
}

fn pink(len: usize, seed: u32) -> Vec<f32> {
    let mut r = Rng(seed);
    let mut b = [0.0f32; 3];
    (0..len)
        .map(|_| {
            let w = r.next();
            b[0] = 0.997 * b[0] + 0.029 * w;
            b[1] = 0.985 * b[1] + 0.032 * w;
            b[2] = 0.950 * b[2] + 0.048 * w;
            (b[0] + b[1] + b[2] + 0.02 * w) * 0.9
        })
        .collect()
}

/// The test signals: name, description, stereo samples.
pub fn signals() -> Vec<(&'static str, &'static str, [Vec<f32>; 2])> {
    let len = (SR * SECONDS) as usize;
    let mono = |v: Vec<f32>| [v.clone(), v];
    let mut out = Vec::new();

    // 1: noise with narrow resonances
    let n = pink(len, 7);
    let mut r = Rng(99);
    let white: Vec<f32> = (0..len).map(|_| r.next()).collect();
    let ring1 = biquad_bp(&white, 3150.0, 30.0);
    let ring2 = biquad_bp(&white, 800.0, 15.0);
    let res: Vec<f32> = (0..len)
        .map(|i| {
            let t = i as f32 / SR as f32;
            0.35 * n[i] + 1.2 * ring1[i] + 0.6 * ring2[i] + 0.04 * (2.0 * std::f32::consts::PI * 6300.0 * t).sin()
        })
        .collect();
    out.push(("resonant noise", "pink noise + ringing peaks at 800 Hz, 3.15 kHz and a 6.3 kHz whistle", mono(res)));

    // 2: plain pink noise (no resonances: should be left mostly alone in soft mode)
    let p: Vec<f32> = pink(len, 3).iter().map(|v| v * 0.5).collect();
    out.push(("pink noise", "broadband pink noise, no resonances", mono(p)));

    // 3: a steady tone over quiet noise
    let q = pink(len, 11);
    let tone: Vec<f32> = (0..len)
        .map(|i| 0.25 * (2.0 * std::f32::consts::PI * 1000.0 * i as f32 / SR as f32).sin() + 0.01 * q[i])
        .collect();
    out.push(("1 kHz tone", "steady 1 kHz sine at -12 dBFS over -40 dB noise", mono(tone)));

    // 4: a voice-like harmonic tone with a harsh formant
    let mut r2 = Rng(5);
    let voice: Vec<f32> = (0..len)
        .map(|i| {
            let t = i as f32 / SR as f32;
            let f0 = 180.0 * (1.0 + 0.01 * (2.0 * std::f32::consts::PI * 5.0 * t).sin());
            let mut v = 0.0;
            for h in 1..60 {
                let f = f0 * h as f32;
                if f > 18000.0 {
                    break;
                }
                // formants at 700 Hz and 2.9 kHz (harsh), falling spectrum
                let g = 1.0 / h as f32 * (1.0 + 2.5 * (-((f - 700.0) / 250.0).powi(2)).exp() + 6.0 * (-((f - 2900.0) / 180.0).powi(2)).exp());
                v += g * (2.0 * std::f32::consts::PI * f * t + h as f32).sin();
            }
            0.08 * v + 0.003 * r2.next()
        })
        .collect();
    out.push(("harsh voice", "180 Hz harmonic tone with a strong narrow formant at 2.9 kHz", mono(voice)));
    out
}

/// Band centres (1/6 octave, 63 Hz .. 16 kHz).
pub fn band_centres() -> Vec<f64> {
    (0..=48).map(|k| 63.0 * 2f64.powf(k as f64 / 6.0)).filter(|f| *f <= 16500.0).collect()
}

fn band_powers(x: &[f32]) -> Vec<f64> {
    let mut planner = RealFftPlanner::<f32>::new();
    let fft = planner.plan_fft_forward(FFT);
    let win: Vec<f32> = (0..FFT).map(|i| 0.5 - 0.5 * (2.0 * std::f32::consts::PI * i as f32 / FFT as f32).cos()).collect();
    let mut acc = vec![0.0f64; FFT / 2 + 1];
    let mut buf = vec![0.0f32; FFT];
    let mut spec = fft.make_output_vec();
    let mut pos = 0;
    let mut frames = 0;
    while pos + FFT <= x.len() {
        for i in 0..FFT {
            buf[i] = x[pos + i] * win[i];
        }
        let _ = fft.process(&mut buf, &mut spec);
        for (a, c) in acc.iter_mut().zip(&spec) {
            *a += c.norm_sqr() as f64;
        }
        frames += 1;
        pos += FFT / 2;
    }
    let bin_hz = SR / FFT as f64;
    band_centres()
        .iter()
        .map(|&f| {
            let lo = (f / 2f64.powf(1.0 / 12.0) / bin_hz).floor() as usize;
            let hi = ((f * 2f64.powf(1.0 / 12.0) / bin_hz).ceil() as usize).min(FFT / 2);
            acc[lo.max(1)..=hi.max(lo.max(1))].iter().sum::<f64>() / frames.max(1) as f64
        })
        .collect()
}

/// Gain change per band in dB (negative = cut), after removing the plugin's latency.
pub fn gain_curve(input: &[f32], output: &[f32], latency: usize) -> Vec<f64> {
    let start = (SKIP_SECONDS * SR) as usize;
    let end = input.len().saturating_sub(latency);
    let a = &input[start..end];
    let b = &output[start + latency..end + latency];
    band_powers(a).iter().zip(band_powers(b)).map(|(pi, po)| 10.0 * ((po + 1e-20) / (pi + 1e-20)).log10()).collect()
}

/// Find the delay (in samples) that best lines the output up with the input.
pub fn measured_delay(input: &[f32], output: &[f32], hint: usize) -> usize {
    let start = (SKIP_SECONDS * SR) as usize;
    let n = 8192;
    let mut best = (hint, f64::MIN);
    let lo = hint.saturating_sub(2048);
    for d in lo..hint + 2048 {
        if start + d + n > output.len() {
            break;
        }
        let mut c = 0.0f64;
        for i in 0..n {
            c += input[start + i] as f64 * output[start + d + i] as f64;
        }
        if c > best.1 {
            best = (d, c);
        }
    }
    best.0
}

fn correlation(a: &[f64], b: &[f64]) -> f64 {
    let n = a.len() as f64;
    let ma = a.iter().sum::<f64>() / n;
    let mb = b.iter().sum::<f64>() / n;
    let (mut sab, mut saa, mut sbb) = (0.0, 0.0, 0.0);
    for (x, y) in a.iter().zip(b) {
        sab += (x - ma) * (y - mb);
        saa += (x - ma).powi(2);
        sbb += (y - mb).powi(2);
    }
    if saa < 1e-9 || sbb < 1e-9 {
        return f64::NAN;
    }
    sab / (saa * sbb).sqrt()
}

pub struct RunResult {
    pub latency_reported: u32,
    pub latency_measured: usize,
    pub curves: Vec<Vec<f64>>,
}

fn run_all(p: &mut Plugin, sigs: &[(&str, &str, [Vec<f32>; 2])], settings: &[(u32, f64)]) -> Result<RunResult, String> {
    p.set_params(settings);
    // a short warm-up so parameter changes and smoothing have settled
    let warm = [vec![0.0f32; 48000], vec![0.0f32; 48000]];
    p.run(&warm)?;
    let mut curves = Vec::new();
    let mut lat_measured = 0;
    for (_, _, x) in sigs {
        let y = p.run(x)?;
        let lat = p.latency as usize;
        let d = measured_delay(&x[0], &y[0], lat);
        lat_measured = d;
        curves.push(gain_curve(&x[0], &y[0], d));
    }
    Ok(RunResult { latency_reported: p.latency, latency_measured: lat_measured, curves })
}

/// A number from a parameter's display text, with its unit applied ("4.0 kHz" -> 4000).
fn parse_number(s: &str) -> Option<f64> {
    let s = s.trim();
    let t: String = s.chars().take_while(|c| c.is_ascii_digit() || *c == '.' || *c == '-' || *c == '+').collect();
    let v: f64 = t.parse().ok()?;
    let unit = s[t.len()..].trim().to_lowercase();
    Some(if unit.starts_with("khz") { v * 1000.0 } else { v })
}

/// Same-named controls: set Resonia's to the values the original shows.
fn matched_settings(orig: &Plugin, ours: &Plugin) -> (Vec<(u32, f64)>, Vec<String>) {
    let mut set = Vec::new();
    let mut notes = Vec::new();
    for q in &ours.params {
        let title = q.title.to_lowercase();
        let Some(o) = orig.params.iter().find(|o| o.title.to_lowercase() == title) else { continue };
        let Some(num) = parse_number(&o.default_text) else { continue };
        let Some(v) = ours.value_from_text(q.id, &format!("{num}")) else { continue };
        // only when both show the same unit and Resonia can reach the value
        let unit = |text: &str, fallback: &str| {
            let t = text.trim();
            let n: String = t.chars().take_while(|c| c.is_ascii_digit() || *c == '.' || *c == '-' || *c == '+').collect();
            let u = t[n.len()..].trim().to_lowercase().replace("khz", "hz");
            if u.is_empty() { fallback.trim().to_lowercase() } else { u }
        };
        let ours_text = ours.text_at(q.id, v);
        let same_unit = unit(&o.default_text, &o.units) == unit(&ours_text, &q.units);
        let reached = parse_number(&ours_text).map(|x| (x - num).abs() <= 0.02 * num.abs().max(1.0)).unwrap_or(false);
        if same_unit && reached {
            set.push((q.id, v));
            notes.push(format!("{} = {} (original shows \"{}\")", q.title, ours_text, o.default_text));
        } else {
            notes.push(format!("{}: not matched — original shows \"{}\", Resonia's scale differs (would be \"{}\")", q.title, o.default_text, ours_text));
        }
    }
    (set, notes)
}

fn fmt_curve_row(f: f64, a: f64, b: f64) -> String {
    let label = if f >= 1000.0 { format!("{:.1}k", f / 1000.0) } else { format!("{:.0}", f) };
    format!("| {label} | {a:+.2} | {b:+.2} | {:+.2} |", b - a)
}

/// Run the comparison and write a Markdown report. Returns a short summary.
pub fn compare(original: &Path, ours: &Path, report: &Path) -> Result<String, String> {
    let sigs = signals();
    let mut o = Plugin::load(original).map_err(|e| format!("original: {e}"))?;
    let mut r = Plugin::load(ours).map_err(|e| format!("Resonia: {e}"))?;
    o.activate(SR, BLOCK).map_err(|e| format!("original: {e}"))?;
    r.activate(SR, BLOCK).map_err(|e| format!("Resonia: {e}"))?;

    let ro = run_all(&mut o, &sigs, &[])?;
    let rr_default = run_all(&mut r, &sigs, &[])?;
    let (matched, notes) = matched_settings(&o, &r);
    let rr_matched = if matched.is_empty() { None } else { Some(run_all(&mut r, &sigs, &matched)?) };

    let centres = band_centres();
    let mut md = String::new();
    let _ = writeln!(md, "# Equivalence test: {} vs {}\n", o.name(), r.name());
    let _ = writeln!(md, "Both plugins loaded as VST3 in the same test host, {} Hz, stereo, blocks of {BLOCK}. Each signal is {SECONDS} s; the first {SKIP_SECONDS} s are skipped so both have settled. Output is lined up with the input using each plugin's delay, then the power change is measured in 1/6-octave bands (negative = cut).\n", SR);
    let _ = writeln!(md, "| | original | Resonia |\n|---|---|---|");
    let _ = writeln!(md, "| reported latency | {} samples | {} samples |", ro.latency_reported, rr_default.latency_reported);
    let _ = writeln!(md, "| measured delay | {} samples | {} samples |\n", ro.latency_measured, rr_default.latency_measured);

    let _ = writeln!(md, "## The original's parameters (as it reports them)\n");
    let _ = writeln!(md, "| id | name | default | at 0 | at 1 | steps | units |\n|---|---|---|---|---|---|---|");
    for p in &o.params {
        let _ = writeln!(md, "| {} | {} | {} | {} | {} | {} | {} |", p.id, p.title, p.default_text, p.min_text, p.max_text, p.steps, p.units);
    }
    if !notes.is_empty() {
        let _ = writeln!(md, "\n## Resonia set to the original's default values\n");
        for n in &notes {
            let _ = writeln!(md, "- {n}");
        }
    }

    let mut summary = String::new();
    let _ = writeln!(summary, "latency: original {} / Resonia {} samples", ro.latency_reported, rr_default.latency_reported);
    let mut runs = vec![("Resonia at its own defaults", &rr_default)];
    if let Some(m) = rr_matched.as_ref() {
        runs.push(("Resonia set to the original's values", m));
    }
    let _ = writeln!(md, "\n## Summary\n\n| signal | compared with | similarity | avg diff dB | deepest cut original | deepest cut Resonia |\n|---|---|---|---|---|---|");
    for (label, run) in &runs {
        let _ = writeln!(summary, "-- {label}");
        for (si, (name, _, _)) in sigs.iter().enumerate() {
            let a = &ro.curves[si];
            let b = &run.curves[si];
            let corr = correlation(a, b);
            let mad = a.iter().zip(b.iter()).map(|(x, y)| (x - y).abs()).sum::<f64>() / a.len() as f64;
            let (ai, amin) = a.iter().enumerate().fold((0, f64::MAX), |m, (i, v)| if *v < m.1 { (i, *v) } else { m });
            let (bi, bmin) = b.iter().enumerate().fold((0, f64::MAX), |m, (i, v)| if *v < m.1 { (i, *v) } else { m });
            let _ = writeln!(md, "| {name} | {label} | {corr:.2} | {mad:.2} | {amin:.1} dB @ {:.0} Hz | {bmin:.1} dB @ {:.0} Hz |", centres[ai], centres[bi]);
            let _ = writeln!(summary, "{name:>15}: similarity {corr:.2}, avg diff {mad:.2} dB, deepest cut orig {amin:.1} dB @ {:.0} Hz / Resonia {bmin:.1} dB @ {:.0} Hz", centres[ai], centres[bi]);
        }
    }
    let _ = writeln!(md, "\nSimilarity is the correlation of the two gain curves (1 = same shape, 0 = unrelated); avg diff is the mean absolute difference per band.");
    let ours = *runs.last().map(|r| &r.1).unwrap();
    let label = runs.last().map(|r| r.0).unwrap();
    for (si, (name, desc, _)) in sigs.iter().enumerate() {
        let a = &ro.curves[si];
        let b = &ours.curves[si];
        let corr = correlation(a, b);
        let mad = a.iter().zip(b).map(|(x, y)| (x - y).abs()).sum::<f64>() / a.len() as f64;
        let (ai, amin) = a.iter().enumerate().fold((0, f64::MAX), |m, (i, v)| if *v < m.1 { (i, *v) } else { m });
        let (bi, bmin) = b.iter().enumerate().fold((0, f64::MAX), |m, (i, v)| if *v < m.1 { (i, *v) } else { m });
        let _ = writeln!(md, "\n## {name}\n\n{desc}. Compared with: {label}.\n");
        let _ = writeln!(md, "- deepest cut: original {amin:.2} dB at {:.0} Hz, Resonia {bmin:.2} dB at {:.0} Hz", centres[ai], centres[bi]);
        let _ = writeln!(md, "- shape similarity (correlation of the two curves): {corr:.2}");
        let _ = writeln!(md, "- average difference: {mad:.2} dB per band\n");
        let _ = writeln!(md, "| band Hz | original dB | Resonia dB | difference |\n|---|---|---|---|");
        for (k, f) in centres.iter().enumerate() {
            let _ = writeln!(md, "{}", fmt_curve_row(*f, a[k], b[k]));
        }
    }
    std::fs::write(report, md).map_err(|e| format!("cannot write report: {e}"))?;
    // The original's copy protection aborts the process when its module is shut down
    // and unloaded, so it stays loaded until the program exits.
    std::mem::forget(o);
    Ok(summary)
}
