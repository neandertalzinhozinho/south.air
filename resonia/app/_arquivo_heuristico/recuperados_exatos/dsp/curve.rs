//! The depth curve: how the bands shape the processing across the spectrum,
//! plus the frequency points and constants used by the graph.

use crate::settings::*;

/// Points drawn on the frequency graph (log-spaced 20 Hz .. 20 kHz).
pub const DISPLAY_POINTS: usize = 240;
pub const DISPLAY_MIN_HZ: f32 = 20.0;
pub const DISPLAY_MAX_HZ: f32 = 20000.0;
/// The engine's constants. Their values are fitted to measurements of the original
/// plugin (`resonia-app --fit`, see MECHANICS.md); `TUNING` lets the fitter try others.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Tuning {
    /// Width of the "surroundings" a peak is compared against (soft mode), octaves.
    pub ref_width_oct: f32,
    /// 0 = surroundings averaged in dB, 1 = averaged as power (tones stand out less).
    pub ref_linear: f32,
    /// Detection smoothing width at Detail 0 and 10, octaves.
    pub detail_w0: f32,
    pub detail_w10: f32,
    /// How far (dB) a peak may stick out before it is touched.
    pub knee_db: f32,
    /// Cut in dB per dB of excess at depth 10.
    pub gain: f32,
    /// Cut grows as (depth/10)^depth_exp.
    pub depth_exp: f32,
    /// Excess above this many dB is compressed (cut = e / (1 + e/sat)).
    pub sat_db: f32,
    /// Detection power is averaged over this long, ms (steadies plain noise).
    pub det_smooth_ms: f32,
    /// Attack time at attack 5, ms, and its ratio per 5 steps of the knob.
    pub attack_ms_at_5: f32,
    pub attack_span: f32,
    /// Release time at release 3, ms, and its ratio per 5 steps of the knob.
    pub release_ms_at_3: f32,
    pub release_span: f32,
    /// Hard mode: threshold (dBFS per bin) = hard_thr0 - hard_thr_per_depth * depth.
    pub hard_thr0: f32,
    pub hard_thr_per_depth: f32,
    /// Hard mode: dB of cut per dB over the threshold.
    pub hard_slope: f32,
}

impl Tuning {
    pub const CALIBRATED: Tuning = Tuning {
        ref_width_oct: 1.0,
        ref_linear: 0.0,
        detail_w0: 0.5,
        detail_w10: 1.0 / 48.0,
        knee_db: 1.5,
        gain: 1.0,
        depth_exp: 1.0,
        sat_db: 1000.0,
        det_smooth_ms: 0.0,
        attack_ms_at_5: 5.0,
        attack_span: 4.0,
        release_ms_at_3: 50.0,
        release_span: 4.0,
        hard_thr0: -12.0,
        hard_thr_per_depth: 5.0,
        hard_slope: 0.75,
    };
}

pub static TUNING: std::sync::RwLock<Tuning> = std::sync::RwLock::new(Tuning::CALIBRATED);

pub fn tuning() -> Tuning {
    TUNING.read().map(|t| *t).unwrap_or(Tuning::CALIBRATED)
}

pub fn set_tuning(t: Tuning) {
    if let Ok(mut g) = TUNING.write() {
        *g = t;
    }
}

/// Attack knob (0..10) to seconds.
pub fn attack_seconds(a: f32, t: &Tuning) -> f32 {
    t.attack_ms_at_5 * t.attack_span.powf((a - 5.0) / 5.0) / 1000.0
}
/// Release knob (0..10) to seconds.
pub fn release_seconds(r: f32, t: &Tuning) -> f32 {
    t.release_ms_at_3 * t.release_span.powf((r - 3.0) / 5.0) / 1000.0
}

pub fn display_freq(i: usize) -> f32 {
    let t = i as f32 / (DISPLAY_POINTS - 1) as f32;
    DISPLAY_MIN_HZ * (DISPLAY_MAX_HZ / DISPLAY_MIN_HZ).powf(t)
}

/// How the depth curve (bands) changes the processing at frequency `f`:
/// returns (effective depth 0..20, on/off multiplier 0..1).
pub fn depth_curve(s: &Settings, f: f32) -> (f32, f32) {
    let mut depth = s.depth;
    let mut mult = 1.0f32;
    for b in s.bands.iter().filter(|b| b.enabled) {
        let x = (f.max(1.0) / b.freq).log2();
        // bandwidth in octaves from Q, widened/narrowed by the band slope
        let bw = (2.0 * (1.0 / (2.0 * b.q)).asinh() / std::f32::consts::LN_2).max(0.05) * b.slope.max(0.05);
        let bell = (-(x / (bw * 0.6)).powi(2)).exp();
        let k = 2.0 + 2.0 * b.q; // shelf / cut steepness
        match b.shape {
            BandShape::Bell => depth += b.depth * bell,
            BandShape::LowShelf => depth += b.depth / (1.0 + (x * k).exp()),
            BandShape::HighShelf => depth += b.depth / (1.0 + (-x * k).exp()),
            BandShape::Tilt => depth += b.depth * (x / 4.0).clamp(-2.5, 2.5),
            BandShape::LowCut => mult *= 1.0 / (1.0 + (-x * k * 2.0).exp()),
            BandShape::HighCut => mult *= 1.0 / (1.0 + (x * k * 2.0).exp()),
            BandShape::Bandpass => mult *= bell,
            BandShape::BandReject => mult *= 1.0 - bell,
        }
    }
    (depth.clamp(DEPTH.min, DEPTH.max), mult.clamp(0.0, 1.0))
}

/// Tilt scaling: a multiplier (1.0x = none) that acts gradually under 500 Hz and above 2 kHz.
pub(crate) fn tilt_factor(f: f32, lo: f32, hi: f32) -> f32 {
    let wl = ((TILT_LOW_HZ / f.max(1.0)).log2() / (TILT_LOW_HZ / 20.0).log2()).clamp(0.0, 1.0);
    let wh = ((f / TILT_HIGH_HZ).log2() / (20000.0 / TILT_HIGH_HZ).log2()).clamp(0.0, 1.0);
    lo.max(0.01).powf(wl) * hi.max(0.01).powf(wh)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn zero_depth_is_flat() {
        // Neutral band set: the real default preset has a low/high cut, which is
        // not flat even at depth 0.
        let mut s = Settings { depth: 0.0, ..Settings::default() };
        for b in &mut s.bands {
            b.enabled = false;
            b.used = false;
        }
        for i in 0..DISPLAY_POINTS {
            let (d, m) = depth_curve(&s, display_freq(i));
            assert!(d.abs() < 1e-6, "depth {} at {}", d, display_freq(i));
            assert!((m - 1.0).abs() < 1e-6);
        }
    }
}
