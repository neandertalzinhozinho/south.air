//! Attack/release smoothing of the per-bin reduction.

/// Move `reduction` toward `target` (already scaled by shape multiplier and
/// channel balance), clamped to `max` dB, using per-bin attack/release factors.
pub(crate) fn apply(reduction: &mut [f32], target: &[f32], mult: &[f32], gain: f32, att: &[f32], rel: &[f32], max: f32) {
    for k in 0..reduction.len() {
        let t = (target[k] * mult[k] * gain).min(max);
        let r = &mut reduction[k];
        let a = if t > *r { att[k] } else { rel[k] };
        *r = t + (*r - t) * a;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn converges_to_target() {
        let mut r = [0.0f32; 4];
        let target = [6.0f32; 4];
        let mult = [1.0f32; 4];
        let att = [0.5f32; 4];
        let rel = [0.5f32; 4];
        for _ in 0..40 {
            apply(&mut r, &target, &mult, 1.0, &att, &rel, 24.0);
        }
        for v in r {
            assert!((v - 6.0).abs() < 1e-3, "got {v}");
        }
    }
}
