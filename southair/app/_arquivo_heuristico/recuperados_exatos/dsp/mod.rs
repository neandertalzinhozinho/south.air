//! The audio engine: a short-time spectral processor that finds narrow peaks
//! (resonances) in the spectrum and turns them down dynamically, bin by bin.
//! Written from the behaviour described in MECHANICS.md.
//!
//! Layout mirrors the original engine:
//! `stft` (FFT/hop/overlap-add), `detect` (soft/hard thresholds, detail, gate),
//! `curve` (bands and the depth curve), `envelope` (attack/release),
//! `stereo` (link, balance, mid/side, sidechain) and `output` (gain, mix, delta).

mod curve;
mod detect;
mod envelope;
mod output;
mod stereo;
mod stft;

pub use curve::{
    attack_seconds, depth_curve, display_freq, release_seconds, set_tuning, tuning, Tuning, DISPLAY_MAX_HZ, DISPLAY_MIN_HZ,
    DISPLAY_POINTS,
};
pub use stft::MAX_CHANNELS;

use crate::settings::*;
use realfft::RealFftPlanner;
use stft::Stft;

/// FFT size used in low-latency mode (at 44.1/48 kHz).
pub const LOW_LATENCY_FFT: usize = 256;

/// What the screen shows: the incoming spectrum and the reduction being applied.
#[derive(Clone, Debug)]
pub struct Analysis {
    pub spectrum_db: Vec<f32>,
    pub reduction_db: Vec<f32>,
    pub max_reduction_now: f32,
    pub sidechain_level_db: f32,
    pub latency_samples: usize,
    pub sample_rate: f32,
}

impl Default for Analysis {
    fn default() -> Self {
        Self {
            spectrum_db: vec![-120.0; DISPLAY_POINTS],
            reduction_db: vec![0.0; DISPLAY_POINTS],
            max_reduction_now: 0.0,
            sidechain_level_db: -120.0,
            latency_samples: 0,
            sample_rate: 48000.0,
        }
    }
}

/// The whole effect: picks the engine for the chosen quality and mixes dry/wet.
pub struct Processor {
    sr: f32,
    engines: Vec<Stft>,
    active: usize,
    sizes: Vec<usize>,
    last_nch: usize,
}

impl Processor {
    pub fn new(sample_rate: f32) -> Self {
        let mult = ((sample_rate / 48000.0).round().max(1.0) as usize).next_power_of_two();
        let mut planner = RealFftPlanner::<f32>::new();
        let mut sizes: Vec<usize> = Quality::ALL.iter().map(|q| q.base_fft() * mult).collect();
        sizes.push(LOW_LATENCY_FFT * mult);
        let engines = sizes.iter().map(|&n| Stft::new(n, &mut planner)).collect();
        Self { sr: sample_rate, engines, active: 1, sizes, last_nch: 2 }
    }

    pub fn sample_rate(&self) -> f32 {
        self.sr
    }

    fn engine_index(s: &Settings) -> usize {
        if s.low_latency {
            4
        } else {
            Quality::ALL.iter().position(|q| *q == s.quality).unwrap_or(1)
        }
    }

    /// Delay the effect adds, in samples.
    pub fn latency_for(&self, s: &Settings) -> usize {
        self.sizes[Self::engine_index(s)]
    }

    pub fn reset(&mut self) {
        for e in &mut self.engines {
            e.reset();
        }
    }

    /// Process audio in place. `sidechain`, when given, feeds the detection instead
    /// of the main input (if sidechain is switched on).
    pub fn process(&mut self, channels: &mut [&mut [f32]], sidechain: Option<&[&mut [f32]]>, s: &Settings) {
        let idx = Self::engine_index(s);
        if idx != self.active {
            self.active = idx;
            self.engines[idx].reset();
        }
        let nch = channels.len().min(MAX_CHANNELS);
        if nch == 0 {
            return;
        }
        self.last_nch = nch;
        let len = channels[0].len();
        let sr = self.sr;
        let has_sc = sidechain.map(|sc| !sc.is_empty()).unwrap_or(false);
        let mix = if s.bypass { 0.0 } else { s.mix / 100.0 };
        let delta = s.delta && !s.bypass;
        let out_gain = if s.bypass {
            1.0
        } else {
            10f32.powf((s.output + s.out_trim) / 20.0)
        };
        let sc_listen = s.sidechain_listen && has_sc && !s.bypass;
        let e = &mut self.engines[idx];
        for i in 0..len {
            for ch in 0..MAX_CHANNELS {
                let x = if ch < nch { channels[ch][i] } else { channels[0][i] };
                let scx = match sidechain {
                    Some(sc) if !sc.is_empty() => {
                        let c = ch.min(sc.len() - 1);
                        sc[c].get(i).copied().unwrap_or(0.0)
                    }
                    _ => 0.0,
                };
                e.push_input(ch, x, scx);
            }
            for ch in 0..nch {
                let x = channels[ch][i];
                let dry = e.read_dry(ch, x);
                let wet = e.read_wet(ch);
                channels[ch][i] = if sc_listen {
                    e.sc_sample(ch) * out_gain
                } else {
                    output::mix_sample(dry, wet, mix, delta, s.wet_trim, out_gain)
                };
            }
            if e.advance() {
                e.process_frame(s, sr, nch, has_sc);
            }
        }
    }

    pub fn copy_analysis(&self, a: &mut Analysis, s: &Settings) {
        let e = &self.engines[self.active];
        a.spectrum_db.copy_from_slice(&e.display_spec);
        a.max_reduction_now = e.reduction_display(self.last_nch, self.sr, &mut a.reduction_db);
        a.sidechain_level_db = e.sc_level;
        a.latency_samples = self.latency_for(s);
        a.sample_rate = self.sr;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn run(s: &Settings, input: &[f32]) -> (Vec<f32>, usize) {
        let mut p = Processor::new(48000.0);
        let lat = p.latency_for(s);
        let mut l = input.to_vec();
        let mut r = input.to_vec();
        for (cl, cr) in l.chunks_mut(512).zip(r.chunks_mut(512)) {
            let mut ch: [&mut [f32]; 2] = [cl, cr];
            p.process(&mut ch, None, s);
        }
        (l, lat)
    }

    #[test]
    fn transparent_at_zero_depth() {
        // The real default preset includes a low cut at 100 Hz and a high cut at
        // 16 kHz; transparency is tested with every band disabled.
        let mut s = Settings { depth: 0.0, ..Settings::default() };
        for b in &mut s.bands {
            b.enabled = false;
            b.used = false;
        }
        let x: Vec<f32> = (0..48000).map(|i| (i as f32 * 0.05).sin() * 0.5 + (i as f32 * 0.31).sin() * 0.2).collect();
        let (y, lat) = run(&s, &x);
        for i in (lat + 4096)..x.len() {
            assert!((y[i] - x[i - lat]).abs() < 1e-3, "sample {i}: {} vs {}", y[i], x[i - lat]);
        }
    }

    #[test]
    fn cuts_a_resonance() {
        // white noise plus a loud sine: the sine should come out quieter
        let mut seed = 1u32;
        let x: Vec<f32> = (0..96000)
            .map(|i| {
                seed = seed.wrapping_mul(1664525).wrapping_add(1013904223);
                let n = (seed >> 8) as f32 / (1u32 << 24) as f32 - 0.5;
                n * 0.2 + 0.5 * (2.0 * std::f32::consts::PI * 3000.0 * i as f32 / 48000.0).sin()
            })
            .collect();
        let s = Settings::default();
        let (y, lat) = run(&s, &x);
        let tone = |v: &[f32]| {
            let (mut c, mut q) = (0.0f32, 0.0f32);
            for (i, x) in v.iter().enumerate() {
                let a = 2.0 * std::f32::consts::PI * 3000.0 * i as f32 / 48000.0;
                c += x * a.cos();
                q += x * a.sin();
            }
            (c * c + q * q).sqrt() / v.len() as f32
        };
        let before = tone(&x[48000 - lat..96000 - lat]);
        let after = tone(&y[48000..96000]);
        let cut_db = 20.0 * (before / after).log10();
        assert!(cut_db > 3.0, "only {cut_db} dB cut");
    }

    #[test]
    fn latency_is_reported() {
        let p = Processor::new(48000.0);
        let s = Settings::default();
        assert_eq!(p.latency_for(&s), Quality::Normal.base_fft());
        let ll = Settings { low_latency: true, ..Settings::default() };
        assert_eq!(p.latency_for(&ll), LOW_LATENCY_FFT);
        let eco = Settings { quality: Quality::Eco, ..Settings::default() };
        assert_eq!(p.latency_for(&eco), Quality::Eco.base_fft());
    }

    #[test]
    fn eight_bands() {
        assert_eq!(NUM_BANDS, 8);
        assert_eq!(Settings::default().bands.len(), 8);
    }
}
