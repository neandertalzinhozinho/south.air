//! Calibration and proof: measure the original plugin once over a grid of settings
//! (cached in a file), then score Resonia's engine against those curves, and
//! compute quality numbers (precision, collateral change, latency, CPU) for both.

use crate::equivalence::{band_centres, gain_curve, measured_delay, signals, SR};
use crate::vst3host::Plugin;
use resonia::dsp::Processor;
use resonia::settings::*;
use std::fmt::Write as _;
use std::path::Path;
use std::time::Instant;

/// One measured setting: what to set on the original (by parameter title and text)
/// and the same thing on Resonia.
pub struct Case {
    pub label: &'static str,
    pub original: Vec<(&'static str, &'static str)>,
    pub ours: fn(&mut Settings),
}

pub fn cases() -> Vec<Case> {
    vec![
        Case { label: "default", original: vec![], ours: |_| {} },
        Case { label: "depth 2", original: vec![("Depth", "2.0")], ours: |s| s.depth = 2.0 },
        Case { label: "depth 8", original: vec![("Depth", "8.0")], ours: |s| s.depth = 8.0 },
        Case { label: "detail 2", original: vec![("Detail", "2.0")], ours: |s| s.detail = 2.0 },
        Case { label: "detail 8", original: vec![("Detail", "8.0")], ours: |s| s.detail = 8.0 },
        Case { label: "hard", original: vec![("Mode", "hard")], ours: |s| s.mode = Mode::Hard },
        Case { label: "max cut 3 dB", original: vec![("Max cut", "3.0")], ours: |s| s.max_reduction = 3.0 },
    ]
}

/// Parameters every case sets, so one case never leaks into the next.
const CONTROLLED: [&str; 4] = ["Depth", "Detail", "Mode", "Max cut"];

/// Resonance positions of the test signals (signal index -> Hz), used for the quality numbers.
fn resonances(signal: usize) -> &'static [f64] {
    match signal {
        0 => &[800.0, 3150.0, 6300.0],
        3 => &[2900.0],
        _ => &[],
    }
}

pub struct Measured {
    pub latency: usize,
    /// (case label, signal index) -> curve
    pub curves: Vec<(String, usize, Vec<f64>)>,
    pub cpu_ratio: f64,
}

fn param_value(p: &Plugin, title: &str, text: &str) -> Option<(u32, f64)> {
    let q = p.params.iter().find(|q| q.title.eq_ignore_ascii_case(title))?;
    // choice parameters: the step whose label is the text
    if q.steps > 0 {
        for k in 0..=q.steps {
            let x = k as f64 / q.steps as f64;
            if p.text_at(q.id, x).eq_ignore_ascii_case(text) {
                return Some((q.id, x));
            }
        }
    }
    let v = p.value_from_text(q.id, text).or_else(|| text.trim().parse::<f64>().ok().map(|x| (x / 10.0).clamp(0.0, 1.0)))?;
    Some((q.id, v))
}

/// Run the original over every case and signal and save the curves.
pub fn measure_original(path: &Path, cache: &Path) -> Result<String, String> {
    let sigs = signals();
    let mut p = Plugin::load(path)?;
    p.activate(SR, 512)?;
    let mut out = String::new();
    let mut log = String::new();
    let mut busy = 0.0f64;
    let mut audio = 0.0f64;
    for case in cases() {
        let mut values = Vec::new();
        for title in CONTROLLED {
            let wanted = case.original.iter().find(|(t, _)| *t == title).map(|(_, v)| *v);
            let q = p.params.iter().find(|q| q.title.eq_ignore_ascii_case(title)).cloned();
            let Some(q) = q else { continue };
            match wanted {
                Some(text) => match param_value(&p, title, text) {
                    Some(v) => values.push(v),
                    None => return Err(format!("the original did not accept {title} = {text}")),
                },
                None => values.push((q.id, q.default)),
            }
        }
        p.set_params(&values);
        p.run(&[vec![0.0; 48000], vec![0.0; 48000]])?;
        for (si, (_, _, x)) in sigs.iter().enumerate() {
            let t = Instant::now();
            let y = p.run(x)?;
            busy += t.elapsed().as_secs_f64();
            audio += x[0].len() as f64 / SR;
            let d = measured_delay(&x[0], &y[0], p.latency as usize);
            let c = gain_curve(&x[0], &y[0], d);
            let shown: Vec<String> = case.original.iter().map(|(t, _)| {
                let q = p.params.iter().find(|q| q.title.eq_ignore_ascii_case(t)).unwrap();
                let v = values.iter().find(|(id, _)| *id == q.id).unwrap().1;
                format!("{t}={}", p.text_at(q.id, v))
            }).collect();
            if si == 0 {
                let _ = writeln!(log, "measured '{}' [{}], delay {d}", case.label, shown.join(", "));
            }
            let _ = writeln!(out, "{}\t{}\t{}", case.label, si, c.iter().map(|v| format!("{v:.4}")).collect::<Vec<_>>().join(","));
        }
    }
    let _ = writeln!(out, "#latency\t{}", p.latency);
    let _ = writeln!(out, "#cpu\t{:.6}", busy / audio);
    std::fs::write(cache, out).map_err(|e| e.to_string())?;
    std::mem::forget(p);
    Ok(log)
}

pub fn load_cache(cache: &Path) -> Result<Measured, String> {
    let text = std::fs::read_to_string(cache).map_err(|e| format!("{}: {e} (run --measure-original first)", cache.display()))?;
    let mut m = Measured { latency: 0, curves: Vec::new(), cpu_ratio: 0.0 };
    for line in text.lines() {
        let f: Vec<&str> = line.split('\t').collect();
        match f.as_slice() {
            ["#latency", v] => m.latency = v.parse().unwrap_or(0),
            ["#cpu", v] => m.cpu_ratio = v.parse().unwrap_or(0.0),
            [label, si, vals] => m.curves.push((label.to_string(), si.parse().unwrap_or(0), vals.split(',').filter_map(|v| v.parse().ok()).collect())),
            _ => {}
        }
    }
    Ok(m)
}

/// Run Resonia's engine (in this process, same code as the plugin) on one signal.
fn run_ours(s: &Settings, x: &[Vec<f32>; 2]) -> ([Vec<f32>; 2], usize, f64) {
    let mut p = Processor::new(SR as f32);
    let lat = p.latency_for(s);
    let mut warm = [vec![0.0f32; 512], vec![0.0f32; 512]];
    for _ in 0..90 {
        let [a, b] = &mut warm;
        let mut ch: [&mut [f32]; 2] = [&mut a[..], &mut b[..]];
        p.process(&mut ch, None, s);
    }
    let mut y = x.clone();
    let t = Instant::now();
    let [l, r] = &mut y;
    for (cl, cr) in l.chunks_mut(512).zip(r.chunks_mut(512)) {
        let mut ch: [&mut [f32]; 2] = [cl, cr];
        p.process(&mut ch, None, s);
    }
    (y, lat, t.elapsed().as_secs_f64())
}

fn correlation(a: &[f64], b: &[f64]) -> f64 {
    let n = a.len() as f64;
    let (ma, mb) = (a.iter().sum::<f64>() / n, b.iter().sum::<f64>() / n);
    let (mut ab, mut aa, mut bb) = (0.0, 0.0, 0.0);
    for (x, y) in a.iter().zip(b) {
        ab += (x - ma) * (y - mb);
        aa += (x - ma).powi(2);
        bb += (y - mb).powi(2);
    }
    if aa < 1e-9 || bb < 1e-9 {
        return 0.0;
    }
    ab / (aa * bb).sqrt()
}

/// Precision (mean cut at the known resonances, dB) and collateral change
/// (mean |change| away from them and on plain noise, dB) for one set of curves.
pub fn quality(curves: &dyn Fn(usize) -> Vec<f64>) -> (f64, f64) {
    let centres = band_centres();
    let mut prec = Vec::new();
    let mut coll = Vec::new();
    for si in [0usize, 3] {
        let c = curves(si);
        let res = resonances(si);
        for &f in res {
            let k = centres.iter().enumerate().min_by(|a, b| ((a.1 / f).ln().abs()).partial_cmp(&(b.1 / f).ln().abs()).unwrap()).unwrap().0;
            prec.push(-c[k]);
        }
        for (k, &fc) in centres.iter().enumerate() {
            if res.iter().all(|&f| (fc / f).log2().abs() > 0.5) {
                coll.push(c[k].abs());
            }
        }
    }
    let pink = curves(1);
    coll.extend(pink.iter().map(|v| v.abs()));
    let mean = |v: &Vec<f64>| v.iter().sum::<f64>() / v.len().max(1) as f64;
    (mean(&prec), mean(&coll))
}

/// Score Resonia against the cached original curves. Returns the report text and the
/// overall average difference (dB per band).
pub fn score(cache: &Path, verbose: bool) -> Result<(String, f64), String> {
    let m = load_cache(cache)?;
    let sigs = signals();
    let mut rep = String::new();
    let mut total = 0.0f64;
    let mut count = 0.0f64;
    let mut ours_curves: Vec<(String, usize, Vec<f64>)> = Vec::new();
    let mut busy = 0.0;
    let mut audio = 0.0;
    let mut our_latency = 0;
    let _ = writeln!(rep, "| setting | signal | similarity | avg diff dB | deepest cut original | deepest cut Resonia |\n|---|---|---|---|---|---|");
    let centres = band_centres();
    for case in cases() {
        let mut s = Settings::default();
        (case.ours)(&mut s);
        for (si, (name, _, x)) in sigs.iter().enumerate() {
            let Some((_, _, orig)) = m.curves.iter().find(|(l, i, _)| l == case.label && *i == si) else { continue };
            let (y, lat, t) = run_ours(&s, x);
            busy += t;
            audio += x[0].len() as f64 / SR;
            our_latency = lat;
            let c = gain_curve(&x[0], &y[0], lat);
            let mad = orig.iter().zip(&c).map(|(a, b)| (a - b).abs()).sum::<f64>() / c.len() as f64;
            total += mad;
            count += 1.0;
            let (ai, amin) = orig.iter().enumerate().fold((0, f64::MAX), |m, (i, v)| if *v < m.1 { (i, *v) } else { m });
            let (bi, bmin) = c.iter().enumerate().fold((0, f64::MAX), |m, (i, v)| if *v < m.1 { (i, *v) } else { m });
            let _ = writeln!(
                rep,
                "| {} | {name} | {:.2} | {mad:.2} | {amin:.1} dB @ {:.0} Hz | {bmin:.1} dB @ {:.0} Hz |",
                case.label,
                correlation(orig, &c),
                centres[ai],
                centres[bi]
            );
            ours_curves.push((case.label.to_string(), si, c));
        }
    }
    let avg = total / count.max(1.0);
    let get = |set: &Vec<(String, usize, Vec<f64>)>, si: usize| set.iter().find(|(l, i, _)| l == "default" && *i == si).map(|v| v.2.clone()).unwrap_or_default();
    let (po, co) = quality(&|si| get(&m.curves, si));
    let (pr, cr) = quality(&|si| get(&ours_curves, si));
    let sel_o = po / co.max(1e-3);
    let sel_r = pr / cr.max(1e-3);
    let cpu_r = busy / audio;
    // A single favourable number is not proof. The gate requires the 1% gain
    // in selectivity without trading away precision, transparency, or latency.
    const SUPERIORITY_MARGIN: f64 = 0.01;
    let selectivity_gain = (sel_r / sel_o.max(1e-9)) - 1.0;
    let precision_regression = pr + 1e-9 < po;
    let collateral_regression = cr > co + 1e-9;
    let latency_regression = our_latency > m.latency;
    let superior = selectivity_gain >= SUPERIORITY_MARGIN
        && !precision_regression
        && !collateral_regression
        && !latency_regression;
    let _ = writeln!(rep, "\nAverage difference over every setting and signal: **{avg:.2} dB per band**.\n");
    let _ = writeln!(rep, "## Quality at default settings\n");
    let _ = writeln!(rep, "| measure | original | Resonia | Resonia vs original |\n|---|---|---|---|");
    let pct = |a: f64, b: f64, higher_better: bool| {
        let d = if higher_better { (b - a) / a.abs().max(1e-9) } else { (a - b) / a.abs().max(1e-9) } * 100.0;
        format!("{d:+.1} % {}", if d >= 1.0 { "better" } else if d <= -1.0 { "worse" } else { "same" })
    };
    let _ = writeln!(rep, "| precision: mean cut at the known resonances | {po:.2} dB | {pr:.2} dB | {} |", pct(po, pr, true));
    let _ = writeln!(rep, "| collateral: mean change away from them and on plain noise | {co:.3} dB | {cr:.3} dB | {} |", pct(co, cr, false));
    let _ = writeln!(rep, "| selectivity: precision / collateral | {sel_o:.1} | {sel_r:.1} | {} |", pct(sel_o, sel_r, true));
    let lo = m.latency as f64 / SR * 1000.0;
    let lr = our_latency as f64 / SR * 1000.0;
    let _ = writeln!(rep, "| latency | {lo:.1} ms | {lr:.1} ms | {} |", pct(lo, lr, false));
    let _ = writeln!(
        rep,
        "| CPU time per second of audio | {:.2} ms | {:.2} ms | {} |",
        m.cpu_ratio * 1000.0,
        cpu_r * 1000.0,
        pct(m.cpu_ratio, cpu_r, false)
    );
    let _ = writeln!(rep, "\n## Superiority gate\n");
    let _ = writeln!(rep, "Target: at least **1.0%** more selectivity (precision / collateral), with no regression in precision, collateral change, or latency.");
    let _ = writeln!(rep, "- selectivity gain: {:+.2}%", selectivity_gain * 100.0);
    let _ = writeln!(rep, "- precision regression: {}", if precision_regression { "FAIL" } else { "PASS" });
    let _ = writeln!(rep, "- collateral regression: {}", if collateral_regression { "FAIL" } else { "PASS" });
    let _ = writeln!(rep, "- latency regression: {}", if latency_regression { "FAIL" } else { "PASS" });
    let _ = writeln!(rep, "- **VERDICT: {}**", if superior { "PASS — measured audio-engine superiority" } else { "FAIL — superiority is not proven" });
    let _ = writeln!(rep, "\nThe original's CPU time includes the test host's plugin calls; Resonia's is measured in-process with the same block size, so CPU is indicative only.");
    if verbose {
        let _ = writeln!(rep, "\n## Curves (default setting)\n\n| band Hz | signal | original | Resonia |\n|---|---|---|---|");
        for si in 0..sigs.len() {
            let a = get(&m.curves, si);
            let b = get(&ours_curves, si);
            for (k, f) in centres.iter().enumerate() {
                let _ = writeln!(rep, "| {f:.0} | {} | {:+.2} | {:+.2} |", sigs[si].0, a[k], b[k]);
            }
        }
    }
    Ok((rep, avg))
}

/// Run the full comparison as a release gate. A failed result is intentionally
/// distinguishable from an informational score so automation cannot claim a win.
pub fn prove_superiority(cache: &Path, report: &Path) -> Result<(String, bool), String> {
    let (text, _) = score(cache, true)?;
    std::fs::write(report, &text).map_err(|e| format!("cannot write {}: {e}", report.display()))?;
    let passed = text.contains("**VERDICT: PASS — measured audio-engine superiority**");
    Ok((format!("{}\nreport written to {}", if passed { "superiority gate: PASS" } else { "superiority gate: FAIL" }, report.display()), passed))
}

/// Average difference (dB per band) between Resonia and the cached original over
/// every case and signal, with the engine's current tuning. Runs cases in parallel.
fn objective(m: &Measured, sigs: &[(&'static str, &'static str, [Vec<f32>; 2])]) -> f64 {
    let cs = cases();
    let jobs: Vec<(usize, usize)> = (0..cs.len()).flat_map(|c| (0..sigs.len()).map(move |s| (c, s))).collect();
    let results: Vec<f64> = std::thread::scope(|scope| {
        let handles: Vec<_> = jobs
            .iter()
            .map(|&(ci, si)| {
                let case = &cs[ci];
                let x = &sigs[si].2;
                scope.spawn(move || {
                    let Some((_, _, orig)) = m.curves.iter().find(|(l, i, _)| l == case.label && *i == si) else { return f64::NAN };
                    let mut s = Settings::default();
                    (case.ours)(&mut s);
                    let (y, lat, _) = run_ours(&s, x);
                    let c = gain_curve(&x[0], &y[0], lat);
                    orig.iter().zip(&c).map(|(a, b)| (a - b).abs()).sum::<f64>() / c.len() as f64
                })
            })
            .collect();
        handles.into_iter().map(|h| h.join().unwrap_or(f64::NAN)).collect()
    });
    let v: Vec<f64> = results.into_iter().filter(|x| x.is_finite()).collect();
    v.iter().sum::<f64>() / v.len().max(1) as f64
}

/// Fit the engine's constants to the original by coordinate search; prints progress and
/// returns the best tuning found as Rust source for `Tuning::CALIBRATED`.
pub fn fit(cache: &Path, rounds: usize) -> Result<String, String> {
    use resonia::dsp::{set_tuning, tuning, Tuning};
    let m = load_cache(cache)?;
    let sigs = signals();
    let mut best = tuning();
    set_tuning(best);
    let mut best_score = objective(&m, &sigs);
    println!("start: {best_score:.4} dB");
    type Field = (&'static str, fn(&mut Tuning) -> &mut f32, f32, f32, bool);
    // (name, field, lower bound, upper bound, multiplicative steps?)
    let fields: Vec<Field> = vec![
        ("gain", |t| &mut t.gain, 0.01, 10.0, true),
        ("depth_exp", |t| &mut t.depth_exp, 0.2, 6.0, true),
        ("knee_db", |t| &mut t.knee_db, 0.0, 30.0, false),
        ("sat_db", |t| &mut t.sat_db, 0.5, 1000.0, true),
        ("ref_width_oct", |t| &mut t.ref_width_oct, 0.1, 4.0, true),
        ("ref_linear", |t| &mut t.ref_linear, 0.0, 1.0, false),
        ("detail_w0", |t| &mut t.detail_w0, 0.02, 3.0, true),
        ("detail_w10", |t| &mut t.detail_w10, 0.005, 1.0, true),
        ("det_smooth_ms", |t| &mut t.det_smooth_ms, 0.0, 2000.0, false),
        ("attack_ms_at_5", |t| &mut t.attack_ms_at_5, 0.5, 500.0, true),
        ("release_ms_at_3", |t| &mut t.release_ms_at_3, 2.0, 3000.0, true),
        ("hard_thr0", |t| &mut t.hard_thr0, -80.0, 20.0, false),
        ("hard_thr_per_depth", |t| &mut t.hard_thr_per_depth, 0.0, 12.0, false),
        ("hard_slope", |t| &mut t.hard_slope, 0.01, 2.0, true),
    ];
    let mut step = 1.0f32;
    for round in 0..rounds {
        let mut improved = false;
        for (name, get, lo, hi, mult) in &fields {
            let cur = *get(&mut best);
            let candidates: Vec<f32> = if *mult {
                let r = 2f32.powf(step);
                vec![cur * r, cur / r, cur * r.sqrt(), cur / r.sqrt()]
            } else {
                let span = (hi - lo) * 0.15 * step;
                let base = if cur == 0.0 && *lo == 0.0 { span } else { span };
                vec![cur + base, cur - base, cur + base * 0.4, cur - base * 0.4]
            };
            for c in candidates {
                let c = c.clamp(*lo, *hi);
                if (c - cur).abs() < 1e-6 {
                    continue;
                }
                let mut t = best;
                *get(&mut t) = c;
                set_tuning(t);
                let sc = objective(&m, &sigs);
                if sc + 1e-4 < best_score {
                    best_score = sc;
                    best = t;
                    improved = true;
                    println!("round {round} {name} = {c:.4}: {sc:.4} dB");
                }
            }
            set_tuning(best);
        }
        if !improved {
            step *= 0.5;
            println!("round {round}: no change, step {step}");
            if step < 0.05 {
                break;
            }
        }
    }
    set_tuning(best);
    Ok(format!("best: {best_score:.4} dB\n{best:#?}"))
}
