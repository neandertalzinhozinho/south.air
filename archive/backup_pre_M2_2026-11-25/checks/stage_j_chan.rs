//! Testes da etapa J — o kernel vive em `port/src/chan.rs` (fonte única).
//!
//! Este arquivo contém **apenas** os testes. O código testado é compartilhado
//! com o crate `soultree_port` via `#[path]`, então não há duas cópias.
//!
//! Extraído de `checks/.build/pre_port/stage_j_chan.rs` por
//! `tools/extract_port_modules.py` (movido byte a byte, sem edição).
//!
//! Teste: `rustc --edition 2021 --test checks\stage_j_chan.rs -o checks\.build\stage_j_chan.exe`

#![allow(unused_imports)]

#[path = "../port/src/chan.rs"]
mod chan;

pub use chan::*;

use core::mem::size_of;

#[cfg(test)]
mod tests {
    use super::*;

    fn bank() -> (Vec<f32>, RingBank) {
        let mut arena = vec![0.0f32; (RING_LEN as usize) * 3];
        let p = arena.as_mut_ptr();
        let bank = RingBank {
            out: RingDesc::new(p),
            a: RingDesc::new(unsafe { p.add(RING_LEN as usize) }),
            b: RingDesc::new(unsafe { p.add(2 * RING_LEN as usize) }),
        };
        (arena, bank)
    }

    #[test]
    fn descr_is_0x90_and_layout_offsets_match() {
        assert_eq!(size_of::<RingDesc>(), RING_BYTES);
        assert_eq!(size_of::<RingBank>(), RING_BANK_BYTES);
        assert_eq!(core::mem::offset_of!(RingDesc, write), 0x80);
        assert_eq!(core::mem::offset_of!(RingDesc, read), 0x84);
        assert_eq!(core::mem::offset_of!(RingDesc, len), 0x88);
        assert_eq!(core::mem::offset_of!(RingDesc, nch), 0x8C);
        assert_eq!(core::mem::offset_of!(RingBank, a), 0x90);
        assert_eq!(core::mem::offset_of!(RingBank, b), 0x120);
    }

    #[test]
    fn gain_is_arg2_over_arg3_in_f32() {
        // 008AD0B9 divss xmm6,xmm0
        assert_eq!(overlap_gain(512, 1024), 0.5);
        assert_eq!(overlap_gain(0, 7), 0.0);
        // 3/7 em f32 e o mesmo bit pattern da conversao+divisao
        assert_eq!(overlap_gain(3, 7), 3.0f32 / 7.0f32);
    }

    #[test]
    fn available_and_advance_match_mask_arithmetic() {
        let (mut arena, mut bank) = bank();
        let d = &mut bank.a;
        d.write = 10;
        d.read = 0xFFF8;
        assert_eq!(d.available(), 18);
        d.read = 0xFFF0;
        d.advance_read(0x20);
        assert_eq!(d.read, 0x10);
        d.write = 0xFFF0;
        d.advance_write(0x20);
        assert_eq!(d.write, 0x10);
        arena[0] = 1.0;
    }

    #[test]
    fn guard_false_leaves_indices_untouched() {
        let (_arena, mut bank) = bank();
        bank.a.write = 0;
        bank.a.read = 0; // available = 0 < n
        bank.b.read = 7;
        bank.out.write = 3;
        let src = [1.0f32; 8];
        assert!(!push_overlap_block(
            &mut bank.out,
            &mut bank.a,
            &mut bank.b,
            &src,
            8,
            16
        ));
        assert_eq!(bank.a.read, 0);
        assert_eq!(bank.a.write, 0);
        assert_eq!(bank.b.read, 7);
        assert_eq!(bank.out.write, 3);
    }

    #[test]
    fn push_zeros_then_adds_scaled_block_and_advances() {
        let (_arena, mut bank) = bank();
        bank.a.write = 16;
        bank.a.read = 0;
        bank.b.write = 16;
        bank.b.read = 4;
        bank.out.write = RING_LEN - 4; // escreve atravessando o fim
        let src = [2.0f32, 4.0, 6.0, 8.0, 10.0, 12.0];
        assert!(push_overlap_block(
            &mut bank.out,
            &mut bank.a,
            &mut bank.b,
            &src,
            6,
            12
        ));
        // gain = 6/12 = 0.5
        assert_eq!(bank.a.read, 6);
        assert_eq!(bank.b.read, 10);
        assert_eq!(bank.out.write, 2);
        let out = unsafe { core::slice::from_raw_parts(bank.out.plane, RING_LEN as usize) };
        assert_eq!(out[RING_LEN as usize - 4], 1.0);
        assert_eq!(out[RING_LEN as usize - 3], 2.0);
        assert_eq!(out[RING_LEN as usize - 2], 3.0);
        assert_eq!(out[RING_LEN as usize - 1], 4.0);
        assert_eq!(out[0], 5.0);
        assert_eq!(out[1], 6.0);
    }

    #[test]
    fn accumulate_uses_single_fma_rounding() {
        let src = [3.0000002f32, -1.5, 0.25];
        let init = [0.1f32, 1e-8, -7.0];
        let mut dst = init;
        accumulate_with_gain(&mut dst, &src, 0.33333334);
        for i in 0..src.len() {
            assert_eq!(dst[i], src[i].mul_add(0.33333334, init[i]));
        }
        // a forma com dois arredondamentos nao e usada
        let mut naive = [0.1f32];
        accumulate_with_gain(&mut naive, &[3.0000002], 0.33333334);
        assert_eq!(naive[0], 3.0000002f32.mul_add(0.33333334, 0.1f32));
    }

    #[test]
    fn zero_planes_clears_every_plane() {
        let mut p0 = [1.0f32; 4];
        let mut p1 = [2.0f32; 4];
        zero_planes(&mut [&mut p0, &mut p1]);
        assert_eq!(p0, [0.0; 4]);
        assert_eq!(p1, [0.0; 4]);
    }
}
