//! Testes da etapa J — o kernel vive em `port/src/pipe.rs` (fonte única).
//!
//! Este arquivo contém **apenas** os testes. O código testado é compartilhado
//! com o crate `soultree_port` via `#[path]`, então não há duas cópias.
//!
//! Extraído de `checks/.build/pre_port/stage_j_pipe.rs` por
//! `tools/extract_port_modules.py` (movido byte a byte, sem edição).
//!
//! Teste: `rustc --edition 2021 --test checks\stage_j_pipe.rs -o checks\.build\stage_j_pipe.exe`

#![allow(unused_imports)]

#[path = "../port/src/pipe.rs"]
mod pipe;

pub use pipe::*;

use core::mem::size_of;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn descr410_is_0x410_bytes() {
        assert_eq!(size_of::<Descr410>(), DESCR410_BYTES);
        assert_eq!(DESCR410_BYTES, 0x410);
        assert_eq!(size_of::<StageBuf>(), STAGE_BUF_BYTES);
        assert_eq!(size_of::<RingDesc>(), RING_BYTES);
    }

    #[test]
    fn align16_matches_008c3507() {
        assert_eq!(align16_floats(0), 0);
        assert_eq!(align16_floats(16), 16);
        assert_eq!(align16_floats(17), 32);
        assert_eq!(align16_floats(31), 32);
        assert_eq!(align16_floats(32), 32);
        assert_eq!(align16_floats(33), 48);
    }

    #[test]
    fn alloc_descr_walks_arena_in_16_float_steps() {
        let mut arena = vec![0.0f32; 256];
        let base = arena.as_mut_ptr();
        let (d, cur) = alloc_descr(base, 0, 3, 17);
        assert_eq!(d.count, 3);
        assert_eq!(d.len, 17);
        assert_eq!(d.stride, 68);
        // 008C34F8: ptr[i] = base + cursor*4, cursor avança align16(17)=32
        unsafe {
            assert_eq!(d.ptr[0], base.add(0));
            assert_eq!(d.ptr[1], base.add(32));
            assert_eq!(d.ptr[2], base.add(64));
        }
        assert_eq!(cur, 96);
        // count = 0: nenhum ponteiro, cursor intacto (008C34E9 jle)
        let (d0, cur0) = alloc_descr(base, 40, 0, 17);
        assert_eq!(cur0, 40);
        assert_eq!(d0.ptr[0], core::ptr::null_mut());
    }

    #[test]
    fn alloc_pair_matches_008cafd0() {
        let mut arena = vec![0.0f32; 256];
        let base = arena.as_mut_ptr();
        let (b, cur) = alloc_pair(base, 0, 17, 68);
        unsafe {
            assert_eq!(b.p0, base.add(0));
            assert_eq!(b.p1, base.add(32));
        }
        assert_eq!(b.n, 17);
        assert_eq!(b.n4, 68);
        assert_eq!(cur, 64);
        // terceiro par (segunda chamada de 0x8CAFD0) continua do cursor
        let (b2, cur2) = alloc_pair(base, cur, 16, 64);
        unsafe {
            assert_eq!(b2.p0, base.add(64));
            assert_eq!(b2.p1, base.add(80));
        }
        assert_eq!(cur2, 96);
    }

    #[test]
    fn stage_constants() {
        assert_eq!(STAGE_BUFFERS, 16);
        assert_eq!(STAGE_GROUPS, [8, 9, 10, 6, 5]);
        assert!(stage_returns_early(2));
        assert!(!stage_returns_early(3));
    }

    #[test]
    fn group_enable_reads_state_1bf_plus_8g() {
        let mut state = vec![0u8; 0x400];
        state[0x1BF] = 1;
        state[0x1BF + 8 * 4] = 1;
        assert!(group_enabled(&state, 0));
        assert!(!group_enabled(&state, 1));
        assert!(group_enabled(&state, 4));
    }

    #[test]
    fn mix_law_endpoints_and_midpoint() {
        // nch == 2 (008C2BAE/008C2BB4): alvo (1-g), MAC g
        // g = 0: dst *= 1; dst += staged*0  -> intacto
        let staged = [1.0f32, -2.0, 3.0, -4.0];
        let mut dst = [10.0f32, 20.0, -30.0, 40.0];
        mix_lane(&mut dst, &staged, 0.0, 2);
        assert_eq!(dst, [10.0, 20.0, -30.0, 40.0]);

        // g = 1: dst *= 0; dst += staged  -> staged
        let mut dst = [10.0f32, 20.0, -30.0, 40.0];
        mix_lane(&mut dst, &staged, 1.0, 2);
        assert_eq!(dst, staged);

        // g = 0.25: (dst*0.75) + staged*0.25
        let mut dst = [4.0f32];
        mix_lane(&mut dst, &[8.0], 0.25, 2);
        assert_eq!(dst, [4.0 * 0.75 + 8.0 * 0.25]);
    }

    #[test]
    fn mix_mono_halves_only_the_staged_term() {
        // nch != 2: alvo (1-g), MAC g*0.5 (008C2DC8 / 008C2DEA)
        assert_eq!(mix_coeffs(0.0, 1), (1.0, 0.0));
        assert_eq!(mix_coeffs(0.0, 2), (1.0, 0.0));
        assert_eq!(mix_coeffs(0.5, 2), (0.5, 0.5));
        assert_eq!(mix_coeffs(0.5, 1), (0.5, 0.25));
        // a soma dos dois coeficientes NÃO é 1 no mono: 1-0.5+0.25 = 0.75
        let mut dst = [4.0f32];
        mix_lane(&mut dst, &[8.0], 0.5, 1);
        assert_eq!(dst, [4.0 * 0.5 + 8.0 * 0.25]);
    }

    #[test]
    fn ring_wraps_with_len_mask() {
        let mut plane = vec![0.0f32; RING_LEN as usize];
        let mut ring = RingDesc::new(plane.as_mut_ptr(), 2);
        assert_eq!(ring.len, 0x10000);
        assert_eq!(ring.nch, 2);
        // (w - r) & (len-1) atravessa o zero
        ring.write = 10;
        ring.read = 0xFFF8;
        assert_eq!(ring.available(), 18);
        // read avança e dá a volta
        ring.read = 0xFFF0;
        ring.advance_read(0x20);
        assert_eq!(ring.read, 0x10);
        // write idem
        ring.write = 0xFFF0;
        ring.advance_write(0x20);
        assert_eq!(ring.write, 0x10);
    }

    #[test]
    fn chain_order_full_with_both_flags() {
        let f = ChainFlags {
            f58: true,
            f52: true,
            f51: false,
            f59: false,
        };
        let got = chain_plan(&f, false);
        assert_eq!(
            got,
            vec![
                Step::Probe,
                Step::ZeroDescr(0),
                Step::ZeroDescr(1),
                Step::ZeroDescr(2),
                Step::Core,
                Step::ZeroDescr(3),
                Step::ZeroDescr(4),
                Step::CopyPre,
                Step::AnalysisStaged,
                Step::Fill,
                Step::DescrBuild(13),
                Step::PtrCopy(14),
                Step::Bands1,
                Step::DescrBuild(16),
                Step::PtrCopy(17),
                Step::Bands2,
                Step::Fft,
                Step::DescrBuild(20),
                Step::PtrCopy(21),
                Step::Copy1520,
                Step::Finish,
                Step::MixAlt,
            ]
        );
    }

    #[test]
    fn chain_branch_f58_false_uses_8b9e40() {
        let f = ChainFlags {
            f58: false,
            f52: false,
            ..Default::default()
        };
        let got = chain_plan(&f, false);
        assert!(got.contains(&Step::AnalysisPlain));
        assert!(!got.contains(&Step::AnalysisStaged));
        assert!(!got.contains(&Step::Bands2));
        assert!(!got.contains(&Step::MixAlt));
        assert_eq!(*got.last().unwrap(), Step::Finish);
    }

    #[test]
    fn chain_shortcut_skips_8_to_19() {
        let f = ChainFlags {
            f58: true,
            f52: true,
            f51: false,
            f59: false,
        };
        assert!(chain_takes_shortcut(&f, true));
        let got = chain_plan(&f, true);
        for skipped in [
            Step::CopyPre,
            Step::AnalysisStaged,
            Step::Fill,
            Step::DescrBuild(13),
            Step::Bands1,
            Step::Bands2,
            Step::Fft,
        ] {
            assert!(!got.contains(&skipped), "não deveria conter {skipped:?}");
        }
        assert_eq!(*got.last().unwrap(), Step::MixAlt);
        // com f51 ou f59 ligados o atalho não é tomado (008ADC6F/008ADC7E)
        assert!(!chain_takes_shortcut(
            &ChainFlags {
                f51: true,
                ..f
            },
            true
        ));
        assert!(!chain_takes_shortcut(
            &ChainFlags {
                f59: true,
                ..f
            },
            true
        ));
        assert!(!chain_takes_shortcut(&f, false));
    }
}
