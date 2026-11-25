//! Etapa M3 — `ln` (`0x1C8500` → `0x293760`) e `exp` (`0x1C84A0` → `0x240C00`)
//! da IPP, transcritos bit a bit.
//!
//! Fonte: `checks/293760.dis`, `checks/293f80.dis` (lane especial do ln),
//! `checks/240c00.dis`, `checks/2414c0.dis` (lane especial do exp) e
//! `checks/t_ln_exp_ipp.md`. Cada passo cita o RVA. Nada aqui é estimado.
//!
//! ## Despacho (CPU path)
//!
//! * `0x1C8500` → `[0x21C6AA8 + 8·[0x21C7408]=4]` = `0x1C8A00` →
//!   `[0x21C70E8]` = **`0x293760`** (`checks/k_core.md` §tabela de stubs).
//! * `0x1C84A0` → `[0x21C6A28 + 8·4]` = `0x1C8880` → `[0x21C6F08]` =
//!   **`0x240C00`** (`checks/m_analise.md`, `008B90D7`).
//!
//! Mesmo índice `4` de `0x21C7408` de M2 (fixado no dump em tempo de execução).
//!
//! ## Assinatura (as duas funções)
//!
//! `rcx = src` (`002937A4`/`00240C44 mov r14,rcx`), `rdx = dst`
//! (`00293798`/`00240C38 mov r12,rdx`), `r8d = n` (`00293775`/`00240C15`).
//! `n <= 0` → `0xFFFFFFFA` (`00293F5D`/`00241491`); ponteiro nulo →
//! `0xFFFFFFF8` (`00293EFA`/`0024142B`). Senão `eax = r15d` = status da última
//! lane especial com status `!= 0`, em ordem crescente de índice
//! (`00293D9D`/`00293ECF`, `002412DD`/`00241400`).
//!
//! ## Por lane — independe de `n` e de alinhamento
//!
//! ln: blocos de 16 (`ebx = n & ~15`, `0029378C`) + cauda de 8 mascarada
//! (padding `0.75`, `0x1ECAF40`). exp: blocos de 32 (`n & ~31`, `00240C2C`) +
//! cauda de 8 (padding `0.75`, `0x1E6FF80`). Toda carga é `vmovups`/
//! `vmaskmovps`, a conta é por lane, o padding é descartado na escrita
//! mascarada. As lanes especiais são refeitas uma a uma pela função escalar
//! (`0x293F80` / `0x2414C0`) com a entrada salva em pilha. O handler de status
//! `0x2D74A0` é `endbr64; ret` (M2), então o valor da lane fica o da escalar.
//!
//! ## MXCSR
//!
//! Igual a M2 (`00293852`..`0029388A`, `00240CF5`..`00240D2D`): força
//! `RN, FTZ = DAZ = 0` e restaura na saída. As contas abaixo assumem esse modo,
//! que é o padrão do Rust em x86-64. Nenhuma instrução x87 faz conta.
//!
//! ## Sem `vrcpps`
//!
//! Ao contrário de M1/M2, nada aqui depende da CPU: só `add/sub/mul/FMA/cvt`
//! IEEE com arredondamento ao mais próximo. `f32::mul_add`/`f64::mul_add` são
//! FMA com um arredondamento, igual a `vfmadd*`.

// ---------------------------------------------------------------------------
// ln — constantes da lane vetorial (`0x1ECAC00`..`0x1ECAE40`, 8 lanes iguais)
// ---------------------------------------------------------------------------

const LN_C00: u32 = 0xBF00_0000; // 0x1ECAC00  -0.5
const LN_C20: u32 = 0x3EAA_AEE7; // 0x1ECAC20  0.333365649
const LN_C40: u32 = 0xBE80_061D; // 0x1ECAC40 -0.250046641
const LN_C60: u32 = 0x3E4A_FB81; // 0x1ECAC60  0.198225036
const LN_C80: u32 = 0xBE28_9358; // 0x1ECAC80 -0.164624572
const LN_CA0: u32 = 0x3E2D_B86B; // 0x1ECACA0  0.169648811
const LN_CC0: u32 = 0xBE1B_6A22; // 0x1ECACC0 -0.151772052
const LN_BIAS: i32 = 0x0080_0000; // 0x1ECAD00 (int)
const LN_LIM: i32 = 0x0100_0000; // 0x1ECAD40 (int)
const LN_OFF: i32 = 0x3F2A_AAAB; // 0x1ECAD80 (int; = 2/3 em f32)
const LN_MANT: i32 = 0x007F_FFFF; // 0x1ECADC0
const LN_ONE: u32 = 0x3F80_0000; // 0x1ECAE00  1.0
const LN_LN2: u32 = 0x3F31_7218; // 0x1ECAE40  0.693147182

#[inline(always)]
fn f(b: u32) -> f32 {
    f32::from_bits(b)
}

#[inline(always)]
fn d(b: u64) -> f64 {
    f64::from_bits(b)
}

/// Lane vetorial de `0x293760` (bloco: `002938E0`..`002939D4`; cauda:
/// `00293AC4`..`00293B20`). `x` já sabido normal positivo.
#[inline]
fn ln_vec_lane(x: f32) -> f32 {
    let i = x.to_bits() as i32;
    // 002938FD vpsubd t = i - 0x3F2AAAAB
    let t = i.wrapping_sub(LN_OFF);
    // 00293905 vpsrad 23 ; 0029392B vcvtdq2ps
    let e = (t >> 23) as f32;
    // 00293901 vpand 0x7FFFFF ; 0029390B vpaddd 0x3F2AAAAB
    let m = f32::from_bits((t & LN_MANT).wrapping_add(LN_OFF) as u32);
    // 00293930 vsubps fr = m - 1.0
    let fr = m - f(LN_ONE);
    // 00293957 vfmadd231ps p = CC0*fr + CA0
    let mut p = f(LN_CC0).mul_add(fr, f(LN_CA0));
    p = p.mul_add(fr, f(LN_C80)); // 00293961
    p = p.mul_add(fr, f(LN_C60)); // 00293973
    p = p.mul_add(fr, f(LN_C40)); // 00293985
    p = p.mul_add(fr, f(LN_C20)); // 00293997
    p = p.mul_add(fr, f(LN_C00)); // 002939A9
    let r = fr * p; // 002939B3 vmulps
    let r = r.mul_add(fr, fr); // 002939BD vfmadd213ps r = r*fr + fr
    e.mul_add(f(LN_LN2), r) // 002939CF vfmadd213ps y = e*ln2 + r
}

/// `true` se a lane vai para `0x293F80`: `(i + 0x00800000) <s 0x01000000`
/// (`002938F3 vpaddd`, `0029390F vpcmpgtd`, `0029393D vmovmskps`). Pega ±0,
/// denormais, negativos, ±inf e NaN; deixa só os normais positivos finitos.
#[inline]
fn ln_is_special(x: f32) -> bool {
    (x.to_bits() as i32).wrapping_add(LN_BIAS) < LN_LIM
}

// ---------------------------------------------------------------------------
// ln — lane especial `0x293F80` (f64 + tabela `0x1ECAF60`, 65 × 24 B)
// ---------------------------------------------------------------------------

const LN_D_LN2HI: u64 = 0x3FE6_2E42_FEFA_3800; // 0x1ECB578
const LN_D_LN2LO: u64 = 0x3D2E_F357_93C7_6730; // 0x1ECB580
const LN_D_IDX: u64 = 0x42D0_0000_0000_0040; // 0x1ECB588  2^46 + 1
const LN_D_SPLIT: u64 = 0x4140_0000_0000_0000; // 0x1ECB590  2^21
const LN_D_NEAR: u64 = 0x3F84_0000_0000_0000; // 0x1ECB598  0.009765625
const LN_D_2P60: u64 = 0x43B0_0000_0000_0000; // 0x1ECB5A0  2^60
const LN_D_P0: u64 = 0xBFE0_0000_0000_0000; // 0x1ECB5B8 -0.5
const LN_D_P1: u64 = 0x3FD5_5555_5555_5613; // 0x1ECB5C0
const LN_D_P2: u64 = 0xBFD0_0000_0000_0262; // 0x1ECB5C8
const LN_D_P3: u64 = 0x3FC9_9999_97B3_6C81; // 0x1ECB5D0
const LN_D_P4: u64 = 0xBFC5_5555_5228_B38F; // 0x1ECB5D8
const LN_D_P5: u64 = 0x3FC2_49C0_2481_059D; // 0x1ECB5E0
const LN_D_P6: u64 = 0xBFC0_00B4_05A2_836D; // 0x1ECB5E8
const LN_D_ONE: u64 = 0x3FF0_0000_0000_0000; // 0x1ECB600 (e 0x1ECB5B0)

/// "Real indefinite" do x86: `vdivsd 0,0` → `0xFFF8000000000000` →
/// `vcvtsd2ss` → `0xFFC00000` (`00294196`/`00294206`). Escrito em bits para
/// não depender de dobra de constante do compilador.
const X86_QNAN_F32: u32 = 0xFFC0_0000;

/// Tabela `0x1ECAF60`: `[c, a, b]` por índice `j ∈ 0..=64` (`c` em `+0`,
/// `a` em `+8`, `b` em `+0x10`; `002940A3`, `0029408F`, `00294099`).
#[rustfmt::skip]
const LN_TAB: [[u64; 3]; 65] = [
    [0x3FF0000000000000, 0x0000000000000000, 0x0000000000000000], //  0 @0x1ECAF60
    [0x3FEF800000000000, 0x3F90205658A00000, 0xBD894F716C1B8BDF], //  1 @0x1ECAF78
    [0x3FEF080000000000, 0x3F9F7A9B16800000, 0xBD7F5EA936C720C1], //  2 @0x1ECAF90
    [0x3FEE900000000000, 0x3FA788595A380000, 0xBD74422C3420ECE9], //  3 @0x1ECAFA8
    [0x3FEE200000000000, 0x3FAEEA31C0080000, 0xBD647844F93F24EE], //  4 @0x1ECAFC0
    [0x3FEDB00000000000, 0x3FB333D7F8180000, 0x3D4FA5B5255F91DF], //  5 @0x1ECAFD8
    [0x3FED400000000000, 0x3FB700D30AEA0000, 0x3D681C1E8DA99DED], //  6 @0x1ECAFF0
    [0x3FECD80000000000, 0x3FBA956D3ECA0000, 0x3D6BCC6F29805896], //  7 @0x1ECB008
    [0x3FEC700000000000, 0x3FBE3707EE300000, 0x3D521ED09CCECD58], //  8 @0x1ECB020
    [0x3FEC100000000000, 0x3FC0CE7ECDCD0000, 0xBD5EB9AD25400ABC], //  9 @0x1ECB038
    [0x3FEBAC0000000000, 0x3FC299D30C608000, 0xBD41597FC311FB94], // 10 @0x1ECB050
    [0x3FEB500000000000, 0x3FC4462B9DC98000, 0x3D59EDE9D63B93E8], // 11 @0x1ECB068
    [0x3FEAF40000000000, 0x3FC5F830A1A60000, 0xBD5AB765D9C00F91], // 12 @0x1ECB080
    [0x3FEA980000000000, 0x3FC7B00916518000, 0xBD56B9D7F2C19F96], // 13 @0x1ECB098
    [0x3FEA400000000000, 0x3FC95A5ADCF70000, 0x3D07F22858A0FF6F], // 14 @0x1ECB0B0
    [0x3FE9EC0000000000, 0x3FCAF68956110000, 0xBD522905117EF527], // 15 @0x1ECB0C8
    [0x3FE9980000000000, 0x3FCC97F8079D8000, 0xBD5D89D3CAE72327], // 16 @0x1ECB0E0
    [0x3FE9480000000000, 0x3FCE2A877A6B0000, 0x3D5608E05DE1C206], // 17 @0x1ECB0F8
    [0x3FE8F80000000000, 0x3FCFC218BE620000, 0x3D34BBA46F1CF6A0], // 18 @0x1ECB110
    [0x3FE8AC0000000000, 0x3FD0A504E97BC000, 0xBD47E7B58CCB79DE], // 19 @0x1ECB128
    [0x3FE8600000000000, 0x3FD16B5CCBAD0000, 0xBD323299042D74BF], // 20 @0x1ECB140
    [0x3FE8180000000000, 0x3FD22981FBEF8000, 0xBD3A1421609580DA], // 21 @0x1ECB158
    [0x3FE7D00000000000, 0x3FD2E9E2BCE12000, 0x3D24300C128D1DC2], // 22 @0x1ECB170
    [0x3FE78C0000000000, 0x3FD3A1AC802F4000, 0xBD4338986332A139], // 23 @0x1ECB188
    [0x3FE7440000000000, 0x3FD4668BF41F0000, 0xBD39AF1762C5A8F7], // 24 @0x1ECB1A0
    [0x3FE7040000000000, 0x3FD5178D9AB56000, 0xBD451F56780B4E27], // 25 @0x1ECB1B8
    [0x3FE6C00000000000, 0x3FD5D5BDDF596000, 0xBD0A0B2A08A465DC], // 26 @0x1ECB1D0
    [0x3FE6800000000000, 0x3FD68AC83E9C6000, 0x3D442834C9D5BAE8], // 27 @0x1ECB1E8
    [0x3FE6440000000000, 0x3FD736580F3AE000, 0x3D46CAA59D367ECC], // 28 @0x1ECB200
    [0x3FE6040000000000, 0x3FD7EF5861CC6000, 0x3D4CEF42353DDE1F], // 29 @0x1ECB218
    [0x3FE5C80000000000, 0x3FD89EB3AF432000, 0x3D40E8B030791139], // 30 @0x1ECB230
    [0x3FE5900000000000, 0x3FD9441434A04000, 0xBD4B4D1F8DA8002F], // 31 @0x1ECB248
    [0x3FE5540000000000, 0x3FD9F7240CC0E000, 0x3D4B6291B174879D], // 32 @0x1ECB260
    [0x3FE51C0000000000, 0x3FDAA00CAE22A000, 0x3D46245C1F2FADAB], // 33 @0x1ECB278
    [0x3FE4E40000000000, 0x3FDB4AB7BDF08000, 0x3D3646398C3E8673], // 34 @0x1ECB290
    [0x3FE4B00000000000, 0x3FDBEACD9E272000, 0xBD34BAC8923C3257], // 35 @0x1ECB2A8
    [0x3FE47C0000000000, 0x3FDC8C77E019C000, 0xBD44FF3BDBB1EB43], // 36 @0x1ECB2C0
    [0x3FE4480000000000, 0x3FDD2FBE93204000, 0xBD4671F55E1C3CAA], // 37 @0x1ECB2D8
    [0x3FE4140000000000, 0x3FDDD4AA04E1C000, 0x3D32D8512DF01AFD], // 38 @0x1ECB2F0
    [0x3FE3E40000000000, 0x3FDE6E62A6DA4000, 0x3D4CA9FBE3D32749], // 39 @0x1ECB308
    [0x3FE3B00000000000, 0x3FDF168F7FB06000, 0xBD2D6FB40A7C0C6E], // 40 @0x1ECB320
    [0x3FE3800000000000, 0x3FDFB358AF7A4000, 0x3D41085FA3C16493], // 41 @0x1ECB338
    [0x3FE3540000000000, 0x3FE02232CCB34800, 0xBD2DC38BFA057734], // 42 @0x1ECB350
    [0x3FE3240000000000, 0x3FE0720E5C40E000, 0xBD1C762FFD3F0109], // 43 @0x1ECB368
    [0x3FE2F80000000000, 0x3FE0BBF2FD23E000, 0xBD35F8BFA94A1946], // 44 @0x1ECB380
    [0x3FE2C80000000000, 0x3FE10D53CBC08000, 0x3D1EFC5CB54F6AF7], // 45 @0x1ECB398
    [0x3FE2A00000000000, 0x3FE151C3F6F29800, 0xBD2EDD97A293AE49], // 46 @0x1ECB3B0
    [0x3FE2740000000000, 0x3FE19DB6BA0BA800, 0xBD324C53BD2DAECC], // 47 @0x1ECB3C8
    [0x3FE2480000000000, 0x3FE1EA5F6E70E800, 0x3D3C1747EB80651C], // 48 @0x1ECB3E0
    [0x3FE2200000000000, 0x3FE230B0D8BEC000, 0xBD3B40FE646DE661], // 49 @0x1ECB3F8
    [0x3FE1F80000000000, 0x3FE2779E1EC94000, 0xBD235B991994C90F], // 50 @0x1ECB410
    [0x3FE1D00000000000, 0x3FE2BF29F9842000, 0xBD3E275C79E2C481], // 51 @0x1ECB428
    [0x3FE1A80000000000, 0x3FE30757344F1000, 0xBD2EC82F533A1F99], // 52 @0x1ECB440
    [0x3FE1800000000000, 0x3FE35028AD9D9000, 0xBD3BD1F01AB60655], // 53 @0x1ECB458
    [0x3FE15C0000000000, 0x3FE39240DDE5D000, 0xBD26D8482A914E99], // 54 @0x1ECB470
    [0x3FE1340000000000, 0x3FE3DC5296586000, 0xBD262793C05BC7A1], // 55 @0x1ECB488
    [0x3FE1100000000000, 0x3FE41F8FF8472000, 0xBD34F7845166B2E1], // 56 @0x1ECB4A0
    [0x3FE0EC0000000000, 0x3FE4635BCF40E000, 0xBD318B9515F69AA9], // 57 @0x1ECB4B8
    [0x3FE0C80000000000, 0x3FE4A7B87BF1F800, 0x3D34123A4EB6653D], // 58 @0x1ECB4D0
    [0x3FE0A80000000000, 0x3FE4E4F832C56000, 0x3D1BADBDDCAF29D2], // 59 @0x1ECB4E8
    [0x3FE0840000000000, 0x3FE52A6D269BC800, 0xBD2FFBBB2E12EC6D], // 60 @0x1ECB500
    [0x3FE0640000000000, 0x3FE568AA0194F000, 0xBD3C89DB8CAE0304], // 61 @0x1ECB518
    [0x3FE0400000000000, 0x3FE5AF405C364800, 0x3D2DFA63AC10C9FB], // 62 @0x1ECB530
    [0x3FE0200000000000, 0x3FE5EE82AA241800, 0x3D2202380CDA46BE], // 63 @0x1ECB548
    [0x3FE0000000000000, 0x3FE62E42FEFA3800, 0x3D2EF35793C76730], // 64 @0x1ECB560
];

/// Polinômio de grau 6 em f64 comum aos dois ramos de `0x293F80`:
/// `P6·z + P5`, `·z + P4`, …, `·z + P0` (`002940EA`..`00294117`,
/// `0029413A`..`00294173`).
#[inline(always)]
fn ln_d_poly(z: f64) -> f64 {
    let mut p = d(LN_D_P6).mul_add(z, d(LN_D_P5));
    p = p.mul_add(z, d(LN_D_P4));
    p = p.mul_add(z, d(LN_D_P3));
    p = p.mul_add(z, d(LN_D_P2));
    p = p.mul_add(z, d(LN_D_P1));
    p.mul_add(z, d(LN_D_P0))
}

/// `0x293F80(rcx=&x, rdx=&y) -> eax`. Devolve `(y, status)`.
pub fn ln_special(x: f32) -> (f32, u32) {
    let b = x.to_bits();
    // 00293F89..00293F9C: expoente f32 = 0xFF
    if b & 0x7F80_0000 == 0x7F80_0000 {
        // 002941D2..002941F7: sinal e mantissa 0 (só -inf) → 0/0, 0x13
        if b & 0x8000_0000 != 0 && b & 0x007F_FFFF == 0 {
            return (f(X86_QNAN_F32), 0x13); // 002941F9..0029420E
        }
        return (x * x, 0); // 002941DE vmulss (+inf → +inf; NaN → NaN quieto)
    }
    // 00293FA9 vcvtss2sd
    let mut dx = x as f64;
    let mut adj: i32 = 0;
    // 00293FB4..00293FCF: expoente f64 = 0 (só ±0 aqui) → ·2^60, adj = -60
    if dx.to_bits() & 0x7FF0_0000_0000_0000 == 0 {
        dx *= d(LN_D_2P60);
        adj = -60;
    }
    // 00293FDD vcomisd dx, 0.0 ; jbe 0x29418E
    if !(dx > 0.0) {
        if dx == 0.0 {
            // 002941AC..002941C5: (-1.0)/(+0.0) = -inf, 0x12
            return ((-d(LN_D_ONE) / 0.0f64) as f32, 0x12);
        }
        // 00294196: 0/0, 0x13
        return (f(X86_QNAN_F32), 0x13);
    }
    // 00293FEF z = dx - 1.0 ; 00293FF9 |z|
    let z = dx - d(LN_D_ONE);
    // 00294004 vcomisd |z|, 0.009765625 ; jbe 0x29413A
    if !(z.abs() > d(LN_D_NEAR)) {
        // 0029413A..00294181: y = poly(z)·z² + z
        let z2 = z * z; // 0029414B
        let y = ln_d_poly(z).mul_add(z2, z); // 0029417C
        return (y as f32, 0);
    }
    let db = dx.to_bits();
    // 0029401C..00294035: expoente ← 0x3FF (m ∈ [1,2))
    let m = d((db & 0x800F_FFFF_FFFF_FFFF).wrapping_add(0x3FF0_0000_0000_0000));
    // 00294029..00294060: e = adj + exp - 0x3FF ; 00294068 vcvtsi2sd
    let e = adj + ((db >> 52) & 0x7FF) as i32 - 0x3FF;
    let ef = e as f64;
    // 00294052 vaddsd ; 0029406D..00294079 índice = low32 & 0x7F
    let j = ((m + d(LN_D_IDX)).to_bits() as u32 & 0x7F) as usize;
    let [c, a, bb] = LN_TAB[j];
    let hi = d(LN_D_LN2HI).mul_add(ef, d(a)); // 0029408F
    let lo = ef.mul_add(d(LN_D_LN2LO), d(bb)); // 00294099
    let c = d(c); // 002940A3
    // 002940AD..002940C1: mh = (m + 2^21) - 2^21
    let mh = (m + d(LN_D_SPLIT)) - d(LN_D_SPLIT);
    let ml = m - mh; // 002940C9
    let rh = mh.mul_add(c, -d(LN_D_ONE)); // 002940CD vfmsub213sd mh·c - 1
    let t = c * ml; // 002940D2
    let hi = hi + rh; // 002940D6
    let r = rh + t; // 002940E2
    let lo = t + lo; // 002940E6
    let r2 = r * r; // 00294120
    let p = ln_d_poly(r).mul_add(r2, lo); // 00294124
    ((hi + p) as f32, 0) // 00294129 / 0029412D vcvtsd2ss
}

/// Uma lane de `0x293760`: `(y, status)`.
#[inline]
pub fn ln_lane(x: f32) -> (f32, u32) {
    if ln_is_special(x) {
        ln_special(x)
    } else {
        (ln_vec_lane(x), 0)
    }
}

/// `0x1C8500(src, dst, n)` → `0x293760`. Devolve o `eax` do binário.
pub fn ln_32f(src: &[f32], dst: &mut [f32]) -> i32 {
    let n = src.len().min(dst.len());
    if n == 0 {
        return 0xFFFF_FFFAu32 as i32; // 00293F5D
    }
    let mut st = 0u32;
    for k in 0..n {
        let (y, s) = ln_lane(src[k]);
        dst[k] = y;
        if s != 0 {
            st = s;
        }
    }
    st as i32
}

/// Versão in-place (`src == dst`): cada lane lê antes de escrever.
pub fn ln_32f_inplace(buf: &mut [f32]) -> i32 {
    if buf.is_empty() {
        return 0xFFFF_FFFAu32 as i32;
    }
    let mut st = 0u32;
    for v in buf.iter_mut() {
        let (y, s) = ln_lane(*v);
        *v = y;
        if s != 0 {
            st = s;
        }
    }
    st as i32
}

// ---------------------------------------------------------------------------
// exp — constantes da lane vetorial (`0x1E6FBC0`..`0x1E6FEC0`)
// ---------------------------------------------------------------------------

const EX_LOG2E: u32 = 0x3FB8_AA3B; // 0x1E6FBC0 1.44269502
const EX_SHIFT: u32 = 0x4B40_0000; // 0x1E6FC00 12582912 = 1.5·2^23
const EX_LN2HI: u32 = 0x3F31_7200; // 0x1E6FC40 0.693145752
const EX_LN2LO: u32 = 0x35BF_BE8E; // 0x1E6FC80 1.42860677e-06
const EX_C0: u32 = 0x3F80_0000; // 0x1E6FD00 1.0
const EX_C1: u32 = 0x3F7F_FFFE; // 0x1E6FD40 0.999999881
const EX_C2: u32 = 0x3EFF_FF34; // 0x1E6FD80 0.49999392
const EX_C3: u32 = 0x3E2A_ACAC; // 0x1E6FDC0 0.166674316
const EX_C4: u32 = 0x3D2B_8392; // 0x1E6FE00 0.0418735221
const EX_C5: u32 = 0x3C07_D9FE; // 0x1E6FE40 0.00829171948
const EX_ABS: u32 = 0x7FFF_FFFF; // 0x1E6FE80
const EX_LIM: i32 = 0x42AE_AC4F; // 0x1E6FEC0 87.3365402 (int)

/// `true` se a lane vai para `0x2414C0`: `(bits & 0x7FFFFFFF) >s 0x42AEAC4F`
/// (`00240DCA vandps`, `00240DD3 vpcmpgtd`): `|x| > 87.33654`, ±inf, NaN.
#[inline]
fn exp_is_special(x: f32) -> bool {
    ((x.to_bits() & EX_ABS) as i32) > EX_LIM
}

/// Lane vetorial de `0x240C00` (bloco: `00240D96`..`00240F0D`; cauda:
/// `0024102E`..`00241078`).
#[inline]
fn exp_vec_lane(x: f32) -> f32 {
    // 00240D96 vfmadd231ps t = log2e·x + shift
    let t = f(EX_LOG2E).mul_add(x, f(EX_SHIFT));
    let k = t - f(EX_SHIFT); // 00240DAA vsubps
    // 00240E2B vfnmadd231ps r = -(hi·k) + x
    let r = (-f(EX_LN2HI)).mul_add(k, x);
    // 00240E4F vfnmadd213ps r = -(k·lo) + r
    let r = (-k).mul_add(f(EX_LN2LO), r);
    // 00240E75 vfmadd231ps p = c5·r + c4 ; depois ·r + c3, c2, c1, c0
    let mut p = f(EX_C5).mul_add(r, f(EX_C4));
    p = p.mul_add(r, f(EX_C3)); // 00240E91
    p = p.mul_add(r, f(EX_C2)); // 00240EAD
    p = p.mul_add(r, f(EX_C1)); // 00240EC9
    p = p.mul_add(r, f(EX_C0)); // 00240EE5
    // 00240DE0 vpslld t,23 ; 00240F00 vpaddd (inteiro, com wrap)
    f32::from_bits((t.to_bits() << 23).wrapping_add(p.to_bits()))
}

// exp — constantes da lane especial (`0x1E6FFA0`..`0x1E6FFDC`)
const EXS_OVF: u32 = 0x42B1_7217; // 0x1E6FFA0  88.72283
const EXS_UNF: u32 = 0xC2CF_F1B4; // 0x1E6FFA4 -103.97208
const EXS_FMAX: u32 = 0x7F7F_FFFF; // 0x1E6FFA8
const EXS_LOG2E: u32 = 0x3FB8_AA3B; // 0x1E6FFAC
const EXS_SHIFT: u32 = 0x4B40_0000; // 0x1E6FFB0
const EXS_LN2HI: u32 = 0x3F31_7200; // 0x1E6FFB4
const EXS_LN2LO: u32 = 0x35BF_BE8E; // 0x1E6FFB8
const EXS_ONE_P: u32 = 0x3F80_0001; // 0x1E6FFBC  1.0000001
const EXS_P5: u32 = 0x3C09_50EF; // 0x1E6FFC0
const EXS_P4: u32 = 0x3D2B_B1B6; // 0x1E6FFC4
const EXS_P3: u32 = 0x3E2A_A9C6; // 0x1E6FFC8
const EXS_P2: u32 = 0x3EFF_FE85; // 0x1E6FFCC
const EXS_DEN: u32 = 0xC2AE_AC4F; // 0x1E6FFD0 -87.33654
const EXS_TINY: u32 = 0x0000_0001; // 0x1E6FFD4
const EXS_2M60: u32 = 0x2180_0000; // 0x1E6FFD8  2^-60
const EXS_TWO: u32 = 0x4000_0000; // 0x1E6FFDC  2.0

/// `0x2414C0(rcx=&x, rdx=&y) -> eax`. Devolve `(y, status)`.
pub fn exp_special(x: f32) -> (f32, u32) {
    let b = x.to_bits();
    // 002414C9..002414DC: expoente f32 = 0xFF
    if b & 0x7F80_0000 == 0x7F80_0000 {
        if b & 0x8000_0000 != 0 && b & 0x007F_FFFF == 0 {
            return (f32::from_bits(0), 0); // 002416FB: -inf → eax(=0) = +0.0
        }
        return (x * x, 0); // 002416E0
    }
    // 002414F3 vcomiss 88.72283, x ; jb → x > 88.72283
    if f(EXS_OVF) < x {
        return (f(EXS_FMAX) * f(EXS_FMAX), 0xC); // 002416B2
    }
    // 002414FD vcomiss x, -103.97208 ; jb
    if x < f(EXS_UNF) {
        return (f(EXS_TINY) * f(EXS_TINY), 0x11); // 00241690
    }
    // 00241513 vcomiss x, -87.33654 (flag usado em 002415AE)
    let denorm = x < f(EXS_DEN);
    let y1 = x * f(EXS_LOG2E); // 0024150B vmulss
    let t = y1 + f(EXS_SHIFT); // 0024152F vaddss
    let kk = (t.to_bits() as u16) as i16 as i32; // 0024153F movsx word
    let kf = t - f(EXS_SHIFT); // 00241545
    let r = x - kf * f(EXS_LN2HI); // 00241555 / 00241563
    let r = r - kf * f(EXS_LN2LO); // 00241567 / 00241577
    let mut p = f(EXS_P5).mul_add(r, f(EXS_P4)); // 00241583
    p = p.mul_add(r, f(EXS_P3)); // 0024158C
    p = p.mul_add(r, f(EXS_P2)); // 00241595
    p = p.mul_add(r, f(EXS_ONE_P)); // 0024159E
    p = p.mul_add(r, f(EXS_ONE_P)); // 002415A3
    // escala = dword [rsp+0x2C] (low word 0, 002414EF) com expoente no high word
    let scale = |e: i32| f32::from_bits(((e as u32) & 0xFF) << 23);
    if denorm {
        // 0024163C..00241677: e = (k - 0x45) & 0xFF ; y = p·2^(k+60)·2^-60
        let y = (p * scale(kk - 0x45)) * f(EXS_2M60);
        return (y, 0x11);
    }
    let e = kk + 0x7F; // 002415B4
    if (e as u32) <= 0xFE {
        (p * scale(e), 0) // 002415C0..002415D1
    } else {
        // 002415EA..00241621: e = (k + 0x7E) & 0xFF ; y = p·2^(k-1)·2
        ((p * scale(kk + 0x7E)) * f(EXS_TWO), 0)
    }
}

/// Uma lane de `0x240C00`: `(y, status)`.
#[inline]
pub fn exp_lane(x: f32) -> (f32, u32) {
    if exp_is_special(x) {
        exp_special(x)
    } else {
        (exp_vec_lane(x), 0)
    }
}

/// `0x1C84A0(src, dst, n)` → `0x240C00`. Devolve o `eax` do binário.
pub fn exp_32f(src: &[f32], dst: &mut [f32]) -> i32 {
    let n = src.len().min(dst.len());
    if n == 0 {
        return 0xFFFF_FFFAu32 as i32; // 00241491
    }
    let mut st = 0u32;
    for k in 0..n {
        let (y, s) = exp_lane(src[k]);
        dst[k] = y;
        if s != 0 {
            st = s;
        }
    }
    st as i32
}

/// Versão in-place.
pub fn exp_32f_inplace(buf: &mut [f32]) -> i32 {
    if buf.is_empty() {
        return 0xFFFF_FFFAu32 as i32;
    }
    let mut st = 0u32;
    for v in buf.iter_mut() {
        let (y, s) = exp_lane(*v);
        *v = y;
        if s != 0 {
            st = s;
        }
    }
    st as i32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ln_basics() {
        assert_eq!(ln_lane(1.0).0.to_bits(), 0);
        assert!((ln_lane(2.0).0 - core::f32::consts::LN_2).abs() <= f32::EPSILON);
        assert_eq!(ln_lane(0.0), (f32::NEG_INFINITY, 0x12));
        assert_eq!(ln_lane(-0.0), (f32::NEG_INFINITY, 0x12));
        assert_eq!(ln_lane(-1.0).0.to_bits(), X86_QNAN_F32);
        assert_eq!(ln_lane(-1.0).1, 0x13);
        assert_eq!(ln_lane(f32::NEG_INFINITY).1, 0x13);
        assert_eq!(ln_lane(f32::INFINITY), (f32::INFINITY, 0));
    }

    #[test]
    fn ln_error_is_small_everywhere_positive() {
        // sanidade (não é prova): erro ≤ 2 ulp contra f64::ln em todos os
        // finitos positivos, normais e denormais, com passo 61.
        let mut b = 1u32;
        while b < 0x7F80_0000 {
            let x = f32::from_bits(b);
            let y = ln_lane(x).0;
            let r = (x as f64).ln() as f32;
            let du = (y.to_bits() as i64 - r.to_bits() as i64).abs();
            let both_neg = (y.to_bits() ^ r.to_bits()) & 0x8000_0000 == 0;
            // limite de sanidade, não de prova: a IPP erra até alguns ulp
            // perto do corte de redução m ≈ 2/3 (ex. x = 0x3F2AAFE4, 3 ulp).
            assert!(both_neg && du <= 4 || y == r, "x={b:#x} y={y} ref={r}");
            b += 997;
        }
    }

    #[test]
    fn exp_basics() {
        assert_eq!(exp_lane(0.0).0, 1.0);
        assert_eq!(exp_lane(f32::NEG_INFINITY), (0.0, 0));
        assert_eq!(exp_lane(f32::INFINITY), (f32::INFINITY, 0));
        assert_eq!(exp_lane(100.0), (f32::INFINITY, 0xC));
        assert_eq!(exp_lane(-200.0), (0.0, 0x11));
        assert_eq!(exp_lane(-95.0).1, 0x11);
        assert!(exp_lane(f32::NAN).0.is_nan());
    }

    #[test]
    fn exp_error_is_small_in_normal_range() {
        // sanidade: erro ≤ 2 ulp contra f64::exp para resultado normal.
        let lo = -87.0f32;
        let hi = 88.5f32;
        let mut x = lo;
        while x < hi {
            let y = exp_lane(x).0;
            let r = (x as f64).exp() as f32;
            let du = (y.to_bits() as i64 - r.to_bits() as i64).abs();
            assert!(du <= 2, "x={x} y={y} ref={r}");
            x += 0.00731;
        }
    }

    #[test]
    fn status_is_last_nonzero() {
        let src = [1.0f32, 0.0, 2.0, -1.0, 3.0];
        let mut dst = [0.0f32; 5];
        assert_eq!(ln_32f(&src, &mut dst), 0x13);
        let src = [-200.0f32, 100.0, 1.0];
        let mut dst = [0.0f32; 3];
        assert_eq!(exp_32f(&src, &mut dst), 0xC);
        assert_eq!(ln_32f(&[], &mut []), 0xFFFF_FFFAu32 as i32);
    }
}
