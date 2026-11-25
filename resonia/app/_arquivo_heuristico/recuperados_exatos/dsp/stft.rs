//! The STFT engine: windowing, FFT, hop bookkeeping and overlap-add.

use super::curve::{self, Tuning};
use super::{detect, envelope, output, stereo};
use crate::settings::*;
use realfft::num_complex::Complex32;
use realfft::{ComplexToReal, RealFftPlanner, RealToComplex};
use std::sync::Arc;

pub const MAX_CHANNELS: usize = 2;

pub(crate) fn smooth_db(src: &[f32], prefix: &mut Vec<f64>, half_widths: &[usize], dst: &mut [f32]) {
    let n = src.len();
    prefix.clear();
    prefix.push(0.0);
    let mut acc = 0.0f64;
    for &v in src {
        acc += v as f64;
        prefix.push(acc);
    }
    for k in 0..n {
        let h = half_widths[k];
        let a = k.saturating_sub(h);
        let b = (k + h + 1).min(n);
        dst[k] = ((prefix[b] - prefix[a]) / (b - a) as f64) as f32;
    }
}

fn half_width_bins(k: usize, width_oct: f32) -> usize {
    let h = k as f32 * (2f32.powf(width_oct * 0.5) - 1.0);
    (h.round() as usize).max(1)
}

/// One STFT engine at a fixed FFT size.
pub(crate) struct Stft {
    pub(crate) n: usize,
    pub(crate) hop: usize,
    pub(crate) window: Vec<f32>,
    r2c: Arc<dyn RealToComplex<f32>>,
    c2r: Arc<dyn ComplexToReal<f32>>,
    pub(crate) in_fifo: Vec<Vec<f32>>,
    pub(crate) sc_fifo: Vec<Vec<f32>>,
    pub(crate) out_acc: Vec<Vec<f32>>,
    pub(crate) dry_ring: Vec<Vec<f32>>,
    pub(crate) ring_pos: usize,
    pub(crate) hop_pos: usize,
    time: Vec<f32>,
    pub(crate) spec: Vec<Vec<Complex32>>,
    pub(crate) sc_spec: Vec<Complex32>,
    scratch_fwd: Vec<Complex32>,
    scratch_inv: Vec<Complex32>,
    pub(crate) power: Vec<Vec<f32>>,
    pub(crate) sc_power: Vec<f32>,
    pub(crate) det_db: Vec<f32>,
    pub(crate) det_smooth: Vec<f32>,
    pub(crate) reference: Vec<f32>,
    pub(crate) target: Vec<f32>,
    pub(crate) reduction: Vec<Vec<f32>>,
    pub(crate) prefix: Vec<f64>,
    pub(crate) hw_ref: Vec<usize>,
    pub(crate) hw_det: Vec<usize>,
    pub(crate) bin_depth: Vec<f32>,
    pub(crate) bin_mult: Vec<f32>,
    pub(crate) bin_att: Vec<f32>,
    pub(crate) bin_rel: Vec<f32>,
    cached: Option<Settings>,
    /// Detection power averaged over time, per channel.
    pub(crate) det_state: Vec<Vec<f32>>,
    pub(crate) det_coef: f32,
    /// Detection power and its wide average, linear.
    pub(crate) det_lin: Vec<f32>,
    pub(crate) ref_lin: Vec<f32>,
    pub(crate) tuning: Tuning,
    pub(crate) display_spec: Vec<f32>,
    pub(crate) sc_level: f32,
}

impl Stft {
    pub(crate) fn new(n: usize, planner: &mut RealFftPlanner<f32>) -> Self {
        let bins = n / 2 + 1;
        let r2c = planner.plan_fft_forward(n);
        let c2r = planner.plan_fft_inverse(n);
        let scratch_fwd = r2c.make_scratch_vec();
        let scratch_inv = c2r.make_scratch_vec();
        let window = (0..n)
            .map(|i| 0.5 - 0.5 * (2.0 * std::f32::consts::PI * i as f32 / n as f32).cos())
            .collect();
        let ch = |len: usize| vec![vec![0.0f32; len]; MAX_CHANNELS];
        Self {
            n,
            hop: n / 4,
            window,
            r2c,
            c2r,
            in_fifo: ch(n),
            sc_fifo: ch(n),
            out_acc: ch(n),
            dry_ring: ch(n),
            ring_pos: 0,
            hop_pos: 0,
            time: vec![0.0; n],
            spec: vec![vec![Complex32::new(0.0, 0.0); bins]; MAX_CHANNELS],
            sc_spec: vec![Complex32::new(0.0, 0.0); bins],
            scratch_fwd,
            scratch_inv,
            power: ch(bins),
            sc_power: vec![0.0; bins],
            det_db: vec![0.0; bins],
            det_smooth: vec![0.0; bins],
            reference: vec![0.0; bins],
            target: vec![0.0; bins],
            reduction: ch(bins),
            prefix: Vec::with_capacity(bins + 1),
            hw_ref: vec![1; bins],
            hw_det: vec![1; bins],
            bin_depth: vec![0.0; bins],
            bin_mult: vec![1.0; bins],
            bin_att: vec![0.0; bins],
            bin_rel: vec![0.0; bins],
            cached: None,
            det_state: ch(bins),
            det_coef: 0.0,
            det_lin: vec![0.0; bins],
            ref_lin: vec![0.0; bins],
            tuning: Tuning::CALIBRATED,
            display_spec: vec![-120.0; curve::DISPLAY_POINTS],
            sc_level: -120.0,
        }
    }

    pub(crate) fn bins(&self) -> usize {
        self.n / 2 + 1
    }

    pub(crate) fn reset(&mut self) {
        for v in self
            .in_fifo
            .iter_mut()
            .chain(self.sc_fifo.iter_mut())
            .chain(self.out_acc.iter_mut())
            .chain(self.dry_ring.iter_mut())
            .chain(self.reduction.iter_mut())
            .chain(self.det_state.iter_mut())
        {
            v.iter_mut().for_each(|x| *x = 0.0);
        }
        self.ring_pos = 0;
        self.hop_pos = 0;
        self.display_spec.iter_mut().for_each(|x| *x = -120.0);
    }

    /// Per-bin tables that only change when settings change.
    fn update_tables(&mut self, s: &Settings, sr: f32) {
        if self.cached.as_ref() == Some(s) {
            return;
        }
        let bins = self.bins();
        let frames_per_sec = sr / self.hop as f32;
        let t = curve::tuning();
        for k in 0..bins {
            let f = k as f32 * sr / self.n as f32;
            let (d, m) = curve::depth_curve(s, f);
            self.bin_depth[k] = d;
            self.bin_mult[k] = if f < 20.0 { 0.0 } else { m };
            let detail = (s.detail / DETAIL.max * curve::tilt_factor(f, s.detail_lo, s.detail_hi)).clamp(0.0, 1.0);
            let w_det = t.detail_w0 * (t.detail_w10 / t.detail_w0).powf(detail);
            self.hw_det[k] = half_width_bins(k, w_det).min(bins / 2);
            self.hw_ref[k] = half_width_bins(k, t.ref_width_oct).max(3).min(bins / 2);
            let att = curve::attack_seconds(s.attack_ms, &t) * curve::tilt_factor(f, s.attack_lo, s.attack_hi);
            let rel = curve::release_seconds(s.release_ms, &t) * curve::tilt_factor(f, s.release_lo, s.release_hi);
            self.bin_att[k] = (-1.0 / (att.max(1e-4) * frames_per_sec)).exp();
            self.bin_rel[k] = (-1.0 / (rel.max(1e-4) * frames_per_sec)).exp();
        }
        self.det_coef = if t.det_smooth_ms > 0.0 { (-1.0 / (t.det_smooth_ms / 1000.0 * frames_per_sec)).exp() } else { 0.0 };
        self.tuning = t;
        self.cached = Some(s.clone());
    }

    /// Write one input sample into the sliding window at the current hop position.
    pub(crate) fn push_input(&mut self, ch: usize, x: f32, sc: f32) {
        let w = self.n - self.hop + self.hop_pos;
        self.in_fifo[ch][w] = x;
        self.sc_fifo[ch][w] = sc;
    }

    /// Read the delayed dry sample for this channel.
    pub(crate) fn read_dry(&mut self, ch: usize, x: f32) -> f32 {
        let dry = self.dry_ring[ch][self.ring_pos];
        self.dry_ring[ch][self.ring_pos] = x;
        dry
    }

    /// Read the next overlap-added wet sample.
    pub(crate) fn read_wet(&self, ch: usize) -> f32 {
        self.out_acc[ch][self.hop_pos]
    }

    pub(crate) fn sc_sample(&self, ch: usize) -> f32 {
        let w = self.n - self.hop + self.hop_pos;
        self.sc_fifo[ch.min(MAX_CHANNELS - 1)][w]
    }

    /// Advance the hop; returns true when a new frame must be processed.
    pub(crate) fn advance(&mut self) -> bool {
        self.ring_pos = (self.ring_pos + 1) % self.n;
        self.hop_pos += 1;
        if self.hop_pos == self.hop {
            self.hop_pos = 0;
            true
        } else {
            false
        }
    }

    pub(crate) fn process_frame(&mut self, s: &Settings, sr: f32, nch: usize, has_sc: bool) {
        let n = self.n;
        let bins = self.bins();
        let scale = 4.0 / n as f32; // full-scale sine at a bin centre reads 0 dB
        self.update_tables(s, sr);

        for ch in 0..nch {
            for i in 0..n {
                self.time[i] = self.in_fifo[ch][i] * self.window[i];
            }
            let _ = self.r2c.process_with_scratch(&mut self.time, &mut self.spec[ch], &mut self.scratch_fwd);
        }
        if nch == 2 && s.mid_side {
            stereo::to_mid_side(&mut self.spec, bins);
        }
        for ch in 0..nch {
            for k in 0..bins {
                self.power[ch][k] = self.spec[ch][k].norm_sqr() * scale * scale;
            }
        }
        let use_sc = s.sidechain && has_sc;
        if has_sc {
            self.sc_power.iter_mut().for_each(|p| *p = 0.0);
            for ch in 0..MAX_CHANNELS {
                for i in 0..n {
                    self.time[i] = self.sc_fifo[ch][i] * self.window[i];
                }
                let _ = self.r2c.process_with_scratch(&mut self.time, &mut self.sc_spec, &mut self.scratch_fwd);
                for k in 0..bins {
                    self.sc_power[k] += self.sc_spec[k].norm_sqr() * scale * scale / MAX_CHANNELS as f32;
                }
            }
            let total: f32 = self.sc_power.iter().sum();
            self.sc_level = 10.0 * (total + 1e-12).log10();
        }

        // display spectrum (average of the channels, smoothed in time)
        for i in 0..curve::DISPLAY_POINTS {
            let pos = curve::display_freq(i) * n as f32 / sr;
            let bin = pos.floor() as usize;
            if bin + 1 >= bins {
                self.display_spec[i] = -120.0;
                continue;
            }
            let frac = pos - bin as f32;
            let mut p = 0.0;
            for ch in 0..nch {
                p += self.power[ch][bin] * (1.0 - frac) + self.power[ch][bin + 1] * frac;
            }
            let db = 10.0 * (p / nch as f32 + 1e-12).log10();
            self.display_spec[i] = if db > self.display_spec[i] { db } else { 0.8 * self.display_spec[i] + 0.2 * db };
        }

        let link = (s.link / 100.0).clamp(0.0, 1.0);
        for ch in 0..nch {
            detect::fill_target(self, s, ch, nch, use_sc, link);
            let bal = stereo::balance_gain(ch, nch, s.balance);
            envelope::apply(
                &mut self.reduction[ch],
                &self.target,
                &self.bin_mult,
                bal,
                &self.bin_att,
                &self.bin_rel,
                if s.max_reduction >= MAX_RED.max { f32::INFINITY } else { s.max_reduction },
            );
        }

        // apply the gains (lightly smoothed across neighbouring bins)
        let wet_trim = 10f32.powf(s.wet_trim / 20.0);
        for ch in 0..nch {
            output::apply_gains(&mut self.spec[ch], &self.reduction[ch], wet_trim);
        }
        if nch == 2 && s.mid_side {
            stereo::from_mid_side(&mut self.spec, bins);
        }
        let norm = 1.0 / (n as f32 * 1.5); // inverse FFT scale and Hann² overlap sum at hop n/4
        for ch in 0..nch {
            self.spec[ch][0].im = 0.0;
            self.spec[ch][bins - 1].im = 0.0;
            let _ = self.c2r.process_with_scratch(&mut self.spec[ch], &mut self.time, &mut self.scratch_inv);
            let acc = &mut self.out_acc[ch];
            acc.copy_within(self.hop.., 0);
            for x in acc[n - self.hop..].iter_mut() {
                *x = 0.0;
            }
            for i in 0..n {
                acc[i] += self.time[i] * self.window[i] * norm;
            }
        }
        for ch in 0..MAX_CHANNELS {
            self.in_fifo[ch].copy_within(self.hop.., 0);
            self.sc_fifo[ch].copy_within(self.hop.., 0);
        }
    }

    pub(crate) fn reduction_display(&self, nch: usize, sr: f32, out: &mut [f32]) -> f32 {
        let bins = self.bins();
        let mut peak = 0.0f32;
        for (i, o) in out.iter_mut().enumerate() {
            let bin = (curve::display_freq(i) * self.n as f32 / sr).round() as usize;
            let mut r = 0.0f32;
            if bin < bins {
                for ch in 0..nch {
                    r = r.max(self.reduction[ch][bin]);
                }
            }
            *o = r;
            peak = peak.max(r);
        }
        peak
    }
}
