//! Peak detection: soft (relative) and hard (absolute) thresholds, detail
//! smoothing, time averaging of the detection and the quiet-bin gate.
//! The constants come from `Tuning`, fitted to measurements of the original.

use super::stereo;
use super::stft::{smooth_db, Stft};
use crate::settings::{Mode, Settings};

/// Fill `e.target` (positive dB of wanted reduction) for one channel.
pub(crate) fn fill_target(e: &mut Stft, s: &Settings, ch: usize, nch: usize, use_sc: bool, link: f32) {
    let bins = e.bins();
    let t = e.tuning;
    let a = e.det_coef;
    for k in 0..bins {
        let p = if use_sc {
            e.sc_power[k]
        } else {
            stereo::linked_power(&e.power, ch, k, nch, link)
        };
        // average the detection over time, so plain noise reads steadier than it is per frame
        let st = &mut e.det_state[ch][k];
        *st = p + (*st - p) * a;
        e.det_lin[k] = *st;
        e.det_db[k] = 10.0 * (*st + 1e-12).log10();
    }
    smooth_db(&e.det_db, &mut e.prefix, &e.hw_det, &mut e.det_smooth);
    match s.mode {
        Mode::Soft => {
            // surroundings: blend of the dB average and the power average
            smooth_db(&e.det_db, &mut e.prefix, &e.hw_ref, &mut e.reference);
            if t.ref_linear > 0.0 {
                smooth_db(&e.det_lin, &mut e.prefix, &e.hw_ref, &mut e.ref_lin);
                for k in 0..bins {
                    let lin_db = 10.0 * (e.ref_lin[k] + 1e-12).log10();
                    e.reference[k] += (lin_db - e.reference[k]) * t.ref_linear;
                }
            }
            for k in 0..bins {
                let excess = (e.det_smooth[k] - e.reference[k] - t.knee_db).max(0.0);
                let excess = excess / (1.0 + excess / t.sat_db.max(1e-3));
                // quiet bins (noise floor) are left alone
                let gate = ((e.det_smooth[k] + 100.0) / 20.0).clamp(0.0, 1.0);
                let depth = (e.bin_depth[k] / 10.0).max(0.0).powf(t.depth_exp);
                e.target[k] = excess * t.gain * depth * gate;
            }
        }
        Mode::Hard => {
            for k in 0..bins {
                let thr = t.hard_thr0 - t.hard_thr_per_depth * e.bin_depth[k];
                let over = (e.det_smooth[k] - thr).max(0.0);
                e.target[k] = if e.bin_depth[k] > 0.0 { over * t.hard_slope } else { 0.0 };
            }
        }
    }
}
