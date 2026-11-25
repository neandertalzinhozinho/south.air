#[cfg(target_arch = "x86_64")]
use std::arch::x86_64::*;

fn main() {
    #[cfg(target_arch = "x86_64")]
    unsafe {
        let a = _mm256_setr_ps(1., 2., 3., 4., 5., 6., 7., 8.);
        let b = _mm256_setr_ps(1., 1., 1., 1., 1., 1., 1., 1.);
        let c = _mm256_setr_ps(10., 10., 10., 10., 10., 10., 10., 10.);
        let mut o = [0f32; 8];
        _mm256_storeu_ps(o.as_mut_ptr(), _mm256_fmaddsub_ps(a, b, c));
        println!("fmaddsub(a,b,c) [a*b -/+ c]: {o:?}");
        _mm256_storeu_ps(o.as_mut_ptr(), _mm256_fmaddsub_ps(a, b, c));
        // 213 form: dst=a, src1=b, src2=c  -> a*b -/+ c (same as above args)
        _mm256_storeu_ps(o.as_mut_ptr(), _mm256_addsub_ps(a, c));
        println!("addsub(a,c) [a -/+ c]: {o:?}");
        let d = _mm256_setr_ps(100., 100., 100., 100., 100., 100., 100., 100.);
        _mm256_storeu_ps(o.as_mut_ptr(), _mm256_fmaddsub_ps(a, b, d));
        println!("fmaddsub(a,b,d) [a*b -/+ d]: {o:?}");
    }
}
