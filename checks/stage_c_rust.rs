// Tabela estatica reconstruida de 0x85E6C0 (jump table 0x85FFA0) + 0x563E40.
// Descriptor = 24 B: { i32 code; i32 pad; i64 idx; i32 kind; i32 pad }
#[repr(C)]
#[derive(Clone, Copy, Debug)]
pub struct BandDesc {
    pub code: i32,
    pub _pad0: i32,
    pub idx: i64,
    pub kind: i32,
    pub _pad1: i32,
}
const _: () = assert!(core::mem::size_of::<BandDesc>() == 24);

const EMPTY: &[BandDesc] = &[];

// caso 1 -> vetor 0x2754DB8 (1 elementos)
static CASE_01: &[BandDesc] = &[
    BandDesc { code: 9, _pad0: 0, idx: 0, kind: 1, _pad1: 0 },
];

// caso 2 -> vetor 0x2754BC8 (1 elementos)
static CASE_02: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
];

// caso 3 -> vetor 0x2754D80 (2 elementos)
static CASE_03: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
];

// caso 4 -> vetor 0x2754C88 (2 elementos)
static CASE_04: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 2, kind: 2, _pad1: 0 },
];

// caso 5 -> vetor 0x2754E40 (3 elementos)
static CASE_05: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 19, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
];

// caso 6 -> vetor 0x2754D48 (3 elementos)
static CASE_06: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 13, _pad0: 0, idx: 3, kind: 2, _pad1: 0 },
];

// caso 7 -> vetor 0x2754C00 (4 elementos)
static CASE_07: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 13, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
];

// caso 8 -> vetor 0x2754CD0 (4 elementos)
static CASE_08: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 13, _pad0: 0, idx: 3, kind: 2, _pad1: 0 },
    BandDesc { code: 19, _pad0: 0, idx: 5, kind: 1, _pad1: 0 },
];

// caso 9 -> vetor 0x2754BE0 (5 elementos)
static CASE_09: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 13, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 19, _pad0: 0, idx: 6, kind: 1, _pad1: 0 },
];

// caso 10 -> vetor 0x2754DD8 (4 elementos)
static CASE_10: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 3, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 5, kind: 2, _pad1: 0 },
];

// caso 11 -> vetor 0x2754CA8 (4 elementos)
static CASE_11: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 13, _pad0: 0, idx: 3, kind: 2, _pad1: 0 },
    BandDesc { code: 11, _pad0: 0, idx: 5, kind: 2, _pad1: 0 },
];

// caso 12 -> vetor 0x2754DF0 (5 elementos)
static CASE_12: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
];

// caso 13 -> vetor 0x2754E28 (5 elementos)
static CASE_13: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 13, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 11, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
];

// caso 14 -> vetor 0x2754D28 (5 elementos)
static CASE_14: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 13, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
];

// caso 15 -> vetor 0x2754C68 (6 elementos)
static CASE_15: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 13, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
    BandDesc { code: 18, _pad0: 0, idx: 8, kind: 2, _pad1: 0 },
];

// caso 16 -> vetor 0x2754E10 (5 elementos)
static CASE_16: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 3, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 5, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 7, kind: 2, _pad1: 0 },
];

// caso 17 -> vetor 0x2754CF0 (6 elementos)
static CASE_17: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 8, kind: 2, _pad1: 0 },
];

// caso 18 -> vetor 0x2754D98 (7 elementos)
static CASE_18: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 10, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
    BandDesc { code: 18, _pad0: 0, idx: 8, kind: 2, _pad1: 0 },
];

// caso 19 -> vetor 0x2754C40 (8 elementos)
static CASE_19: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 12, _pad0: 0, idx: 12, kind: 2, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 10, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
    BandDesc { code: 18, _pad0: 0, idx: 8, kind: 2, _pad1: 0 },
];

// caso 20 -> vetor 0x2754D10 (9 elementos)
static CASE_20: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 12, _pad0: 0, idx: 12, kind: 2, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 10, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
    BandDesc { code: 17, _pad0: 0, idx: 14, kind: 2, _pad1: 0 },
    BandDesc { code: 18, _pad0: 0, idx: 8, kind: 2, _pad1: 0 },
];

// caso 21 -> vetor 0x2754D68 (8 elementos)
static CASE_21: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 12, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 8, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 10, kind: 2, _pad1: 0 },
    BandDesc { code: 18, _pad0: 0, idx: 12, kind: 2, _pad1: 0 },
];

// caso 22 -> vetor 0x2754C20 (9 elementos)
static CASE_22: &[BandDesc] = &[
    BandDesc { code: 8, _pad0: 0, idx: 0, kind: 2, _pad1: 0 },
    BandDesc { code: 9, _pad0: 0, idx: 2, kind: 1, _pad1: 0 },
    BandDesc { code: 10, _pad0: 0, idx: 3, kind: 1, _pad1: 0 },
    BandDesc { code: 12, _pad0: 0, idx: 6, kind: 2, _pad1: 0 },
    BandDesc { code: 14, _pad0: 0, idx: 4, kind: 2, _pad1: 0 },
    BandDesc { code: 15, _pad0: 0, idx: 8, kind: 2, _pad1: 0 },
    BandDesc { code: 16, _pad0: 0, idx: 10, kind: 2, _pad1: 0 },
    BandDesc { code: 17, _pad0: 0, idx: 14, kind: 2, _pad1: 0 },
    BandDesc { code: 18, _pad0: 0, idx: 12, kind: 2, _pad1: 0 },
];

/// 0x85E6C0(case): case = dword [arg3+0] ou [arg3+8]; 0x85E6CE cmp ecx,0x16 / ja 0x85EBA7.
pub fn select_band_table(case: i32) -> &'static [BandDesc] {
    match case {
        1 => CASE_01,
        2 => CASE_02,
        3 => CASE_03,
        4 => CASE_04,
        5 => CASE_05,
        6 => CASE_06,
        7 => CASE_07,
        8 => CASE_08,
        9 => CASE_09,
        10 => CASE_10,
        11 => CASE_11,
        12 => CASE_12,
        13 => CASE_13,
        14 => CASE_14,
        15 => CASE_15,
        16 => CASE_16,
        17 => CASE_17,
        18 => CASE_18,
        19 => CASE_19,
        20 => CASE_20,
        21 => CASE_21,
        22 => CASE_22,
        _ => EMPTY, // caso 0 e > 0x16: 0x85EBA7 -> 0x2752208 (vector vazio)
    }
}
