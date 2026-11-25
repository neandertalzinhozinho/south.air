//! Etapa Q — `0x8C1440` transcrito: estagiador de 5 grupos + mistura.
//!
//! Fonte: `checks/q_8c1440_buffers.md` (leitura FECHADA em 2026-11-25) e
//! `checks/8c1440.u8.dis` (`0x8C1440`–`0x8C32B7`). Cada passo abaixo cita o
//! RVA. O que **não** está provado fica no doc e não é estimado.
//!
//! ## Estrutura provada
//!
//! 1. **Guarda** (`008C1467`/`008C1474`): `count = [t+0x400]`; `count <= 2` →
//!    retorno imediato, nada é estagiado (`pipe::stage_returns_early`).
//! 2. **16 buffers** zerados (`008C1800`–`008C19C6`), `n = [t+0x404]`.
//! 3. **Passagem A** (`008C1A58`–`008C2361`): para cada grupo `g` de
//!    `STAGE_GROUPS = {8,9,10,6,5}` e cada registro de banda de `0x18 B`
//!    (`+0x00 sel`, `+0x08 first_buf`, `+0x10 nch`), acumula
//!    `par 0/2/4/6 += ch²` (`0x1580`, FMA) e `par 1/3/5/7 += ch` (`0x1370`).
//!    O par depende da **rota** ([`route_for`]), não do índice do grupo.
//! 4. **Clamp** (`008C2367`/`008C2393`/`008C23CD`/`008C240D`/`008C244D`):
//!    `0x1100(r9d=0, xmm2=1.00000001e-07f)` nos pares **ímpares**
//!    (`1/3/5/7`) — `x = max(x, CLAMP_MIN)`, `vmaxss` em `00003640`.
//! 5. **Quatro divisões** (`008C2545`/`008C263D`/`008C273B`/`008C2828`):
//!    `new1=par0/par1`, `T1=par2/par3`, `T2=par4/par5`, `T3=par6/par7`.
//! 6. **Quatro somas** (`008C28B1`–`008C2A5A`): `A/B/C/D` = soma dos 2 canais
//!    de `new1/T1/T2/T3` (zero + `0x1370` duas vezes).
//! 7. **Passagem B** (`008C2AA5`–`008C3201`): `ch ← (1-g)·ch + g·D` por
//!    canal quando `nch == 2`; quando `nch != 2` (mono) usa só
//!    `buffers[first_buf]`, `src` = soma `A/B/C/D` e coeficiente `g·0.5`
//!    (`008C2DEA`/`008C31D5`) — implementado por `pipe::mix_lane`, provado em
//!    `checks/q_8c1440_buffers.md` §4.
//!
//! ## Gaps (não estimados)
//!
//! * **Divisão `0x1550` → `0xC560` → `0x63640`**: não é `vdivps`; é `vrcpps`
//!   + dois Newton (`00063775`, `00063782`, `00063791`, `00063796`) com
//!   correção de zero/inf/denormal (`000637BA`..`00063889`). O port usa a
//!   divisão exata, que difere no ULP do caminho vetorial. `pending::GAPS`
//!   registra `0x63640` como primeiro bloqueante.
//! * Nome/unidade dos quatro coeficientes (`state+0x2C/0x30/0x34/0x38`) e a
//!   faixa válida de `g`: `NÃO PROVADO` (docs, §9).
//! * `nch > 2` habilitado: o binário usa só `buffers[first_buf]` e escreve
//!   **nos dois** canais do par (`008C1E61`–`008C1E8D`); desabilitado com
//!   `nch ∉ {1,2}` não acumula (`008C21E9`/`008C22E1`). Transcrito como está;
//!   a razão depende de quem escreve `rec->nch`.
//!
//! `cargo test --lib stage::` (testes no próprio módulo, rodados por
//! `port/run_tests.ps1`).

#![allow(dead_code)]

use crate::pipe::{mix_lane, stage_returns_early, STAGE_GROUPS};

/// Piso do denominador: `1.00000001e-07f` = bits `0x33D6BF95`
/// (`0x2079CEC`, carregado em `008C2367`, usado como `xmm2` do `0x1100` em
/// `008C238D`).
pub const CLAMP_MIN: f32 = f32::from_bits(0x33D6BF95);

/// Índice do coeficiente em [`StageState::g`]: `state+0x2C` (`008C2A70`).
pub const COEF_ENABLED: usize = 0;
/// `state+0x30` (`008C2A79`), rota `tipo 8/9` desabilitado.
pub const COEF_GROUP89: usize = 1;
/// `state+0x34` (`008C2A82`), rota `tipo 6` desabilitado.
pub const COEF_GROUP6: usize = 2;
/// `state+0x38` (`008C2A8B`), rota `tipo 5` desabilitado.
pub const COEF_GROUP5: usize = 3;

/// Registro de banda de `0x18 B` (`008C1A60`, `008C1AB0`).
///
/// `+0x00 sel`, `+0x08 first_buf`, `+0x10 nch`; os canais do registro são
/// `track->buffers[first_buf .. first_buf+nch]` (`008C1D18`/`008C1E61`).
#[derive(Clone, Copy, Debug)]
pub struct BandRec {
    pub sel: u8,
    pub first_buf: u32,
    pub nch: u32,
}

/// Estado lido uma vez por bloco.
#[derive(Clone, Copy, Debug)]
pub struct StageState {
    /// `state[0x1BF + 8g]` (`008C1A6E`/`008C2ABA`); `g` indexa `STAGE_GROUPS`.
    pub enable: [bool; 5],
    /// `state+0x2C`, `+0x30`, `+0x34`, `+0x38`, carregados em
    /// `008C2A70`/`008C2A79`/`008C2A82`/`008C2A8B`.
    pub g: [f32; 4],
}

/// Entrada do estágio.
pub struct StageInput<'a> {
    /// `n = [t+0x404]` (`008C2032`, `008C2BDB`).
    pub n: usize,
    /// `count = [t+0x400]`; `<= 2` não estagia (`008C1467`).
    pub count: i32,
    /// Registros de cada grupo (`g = 0..5`), na ordem em que aparecem.
    pub groups: [&'a [BandRec]; 5],
    pub state: StageState,
    /// `[rbp+0x13E8] != 0` ⇔ `state[0x1BF] == 0 && state[0x1C7] == 0`
    /// (`008C1A14`–`008C1A38`, `008C1FFE`, `008C2F2E`): grupos 0 e 1 ambos
    /// desabilitados.
    pub flag_13e8: bool,
}

/// Rota provada do registro — decide par de acumulação (`passagem A`),
/// divisor (`new1/T1/T2/T3`) e coeficiente (passagem B).
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Route {
    /// `enable != 0`, qualquer `tipo`: `new1` / soma `A` / `+0x2C`
    /// (`008C1D28`, `008C2CC4`).
    Enabled,
    /// `enable == 0`, `tipo 8/9`, `sel == tipo` **e** flag: `T1` / `B` / `+0x30`
    /// (`008C1FFE`, `008C2F3F`).
    Group89,
    /// `enable == 0`, `tipo 6`, `h(4) && !h(5)`: `T2` / `C` / `+0x34`
    /// (`008C1F91`–`008C1FC4`, `008C2F50`).
    Group6,
    /// `enable == 0`, `tipo 5`, `sel ∈ {0x10,0x11,0x12}`: `T3` / `D` / `+0x38`
    /// (`008C1F2B`–`008C1F32`, `008C2E9B`).
    Group5,
}

impl Route {
    /// Índice da divisão `0..4` (`new1/T1/T2/T3`).
    pub const fn division(self) -> usize {
        match self {
            Route::Enabled => 0,
            Route::Group89 => 1,
            Route::Group6 => 2,
            Route::Group5 => 3,
        }
    }

    /// Par `Σch²` da passagem A (o par `Σch` é `+1`): `0/2/4/6`.
    pub const fn sq_pair(self) -> usize {
        self.division() * 2
    }

    pub const fn coef(self) -> usize {
        match self {
            Route::Enabled => COEF_ENABLED,
            Route::Group89 => COEF_GROUP89,
            Route::Group6 => COEF_GROUP6,
            Route::Group5 => COEF_GROUP5,
        }
    }
}

/// Predicado de participação `h(tipo, sel)` — árvore recomposta em
/// `008C1AB0`–`008C1B6E` (habilitado), `008C1EE4`–`008C1F43` (desabilitado)
/// e `008C2AF0`–`008C2BA8` (passagem B), idêntica a `0x61B790`.
///
/// `tipo 0` participa sempre (`008C1AB4` → `008C1B74`), mas nunca ocorre: a
/// tabela é `{8,9,10,6,5}`.
pub fn participates(tipo: u8, sel: u8) -> bool {
    match tipo {
        0 => true,
        1 => sel != 0xA,                        // 008C1AC3
        2 => sel != 9,                          // 008C1AD5
        3 => sel.wrapping_sub(9) > 1,           // 008C1AE7
        4 => sel.wrapping_sub(8) > 2,           // 008C1B14
        5 => sel.wrapping_sub(0x10) <= 2,       // 008C1AFF
        6 => participates(4, sel) && !participates(5, sel), // 008C1B2F/008C1B43
        7 => sel.wrapping_sub(8) <= 1,          // 008C1B57
        _ => sel == tipo,                       // 008C1B66 / 008C1FDB
    }
}

/// Rota do registro, ou `None` quando ele não acumula nem mistura.
///
/// Ramo habilitado (`008C1A8F`): só o predicado. Ramo desabilitado
/// (`008C1EBE`): `tipo 8/9` exige `sel == tipo` **e** flag (`008C1FFE`);
/// `tipo 6` exige `h(4) && !h(5)`; `tipo 5` exige `sel ∈ {0x10,0x11,0x12}`
/// (`008C1F2B`); `tipo 0xA` desabilitado nunca (`008C1FDB`–`008C1FF1`).
pub fn route_for(enabled: bool, tipo: u8, sel: u8, flag_13e8: bool) -> Option<Route> {
    if enabled {
        if participates(tipo, sel) {
            Some(Route::Enabled)
        } else {
            None
        }
    } else if (tipo == 8 || tipo == 9) && sel == tipo && flag_13e8 {
        Some(Route::Group89)
    } else if tipo == 6 && participates(4, sel) && !participates(5, sel) {
        Some(Route::Group6)
    } else if tipo == 5 && participates(5, sel) {
        Some(Route::Group5)
    } else {
        None
    }
}

/// `0x1100` modo 0 (`r9d = 0`, `00003498` → `000035D9`): `x = max(x, bound)`,
/// `vmaxss xmm0, xmm2, [buf]` (`00003640`). `bound` é finito (`1e-7`), então o
/// único caso especial que sobra é NaN, que o `vmaxss` devolve como NaN — o
/// `if x <` preserva isso.
#[inline]
pub fn clamp_min(x: f32, bound: f32) -> f32 {
    if x < bound {
        bound
    } else {
        x
    }
}

/// `0x8C1440` completo: passagem A, clamp, quatro divisões, quatro somas e
/// passagem B. `bufs` é `track->buffers`; os registros indexam por
/// `first_buf`.
///
/// **Divisão:** aqui é a divisão IEEE exata; o binário chama `0x1550` →
/// `0x63640` (`vrcpps` + Newton). É o gap bloqueante registrado em
/// `pending::GAPS` (`0x63640`), não uma diferença ignorada.
pub fn process(input: &StageInput<'_>, bufs: &mut [Vec<f32>]) {
    if stage_returns_early(input.count) {
        return; // 008C1467 cmp [rdx+0x400],2 / 008C1474 jle
    }
    let n = input.n;

    // 8 pares × 2 canais, zerados por 0x10D0 em 008C1800..008C19C6.
    let mut acc: [[Vec<f32>; 2]; 8] = std::array::from_fn(|_| [vec![0.0; n], vec![0.0; n]]);

    // --- Passagem A: acumulação (008C1A58..008C2361) ---------------------
    for (g, recs) in input.groups.iter().enumerate() {
        let tipo = STAGE_GROUPS[g];
        let enabled = input.state.enable[g];
        for rec in recs.iter() {
            let Some(route) = route_for(enabled, tipo, rec.sel, input.flag_13e8) else {
                continue; // 008C1E09 / 008C2311
            };
            // `nch == 2` → um buffer por canal (008C1D18/008C1D20).
            // `nch != 2` habilitado → só buffers[first_buf], escrito nos dois
            // canais (008C1E61..008C1E8D). Desabilitado aceita só `nch == 1`
            // (008C21E9/008C22E1); `nch > 2` não acumula.
            let src_idx = match rec.nch {
                2 => [rec.first_buf as usize, rec.first_buf as usize + 1],
                _ if enabled || rec.nch == 1 => [rec.first_buf as usize; 2],
                _ => continue,
            };
            let sq_pair = route.sq_pair();
            for c in 0..2 {
                let src = &bufs[src_idx[c]];
                debug_assert_eq!(src.len(), n, "buffer menor que n");
                let (head, tail) = acc.split_at_mut(sq_pair + 1);
                let sq = &mut head[sq_pair][c];
                let lin = &mut tail[0][c];
                for i in 0..n {
                    // 0x1580: dst = a*b + dst, FMA (008C1D28/008C1E81/008C200F/008C1F59/008C1F60)
                    sq[i] = src[i].mul_add(src[i], sq[i]);
                    // 0x1370: dst += src (008C1DF0/008C1EAB/008C1F70/008C201D/008C2021)
                    lin[i] += src[i];
                }
            }
        }
    }

    // --- Clamp dos denominadores: pares 1/3/5/7 (008C2367..008C244D) -----
    for pair in [1usize, 3, 5, 7] {
        for lane in acc[pair].iter_mut() {
            for x in lane.iter_mut() {
                *x = clamp_min(*x, CLAMP_MIN);
            }
        }
    }

    // --- Quatro divisões (008C2545/008C263D/008C273B/008C2828) -----------
    let mut div: [[Vec<f32>; 2]; 4] = std::array::from_fn(|_| [vec![0.0; n], vec![0.0; n]]);
    for k in 0..4 {
        for c in 0..2 {
            for i in 0..n {
                div[k][c][i] = acc[2 * k][c][i] / acc[2 * k + 1][c][i];
            }
        }
    }

    // --- Somas A/B/C/D = 2 canais de new1/T1/T2/T3 (008C28B1..008C2A5A) --
    let mut sum: [Vec<f32>; 4] = std::array::from_fn(|_| vec![0.0; n]);
    for k in 0..4 {
        for i in 0..n {
            // 0x10D0 zera, depois dois 0x1370: (0 + lane0) + lane1.
            let mut s = 0.0f32;
            s += div[k][0][i];
            s += div[k][1][i];
            sum[k][i] = s;
        }
    }

    // --- Passagem B: mistura (008C2AA5..008C3201) -------------------------
    for (g, recs) in input.groups.iter().enumerate() {
        let tipo = STAGE_GROUPS[g];
        let enabled = input.state.enable[g];
        for rec in recs.iter() {
            let Some(route) = route_for(enabled, tipo, rec.sel, input.flag_13e8) else {
                continue; // 008C2DFD / 008C31ED
            };
            let k = route.division();
            let coef = input.state.g[route.coef()];
            let first = rec.first_buf as usize;
            if rec.nch == 2 {
                // dst = canais do registro (008C2C30/008C2D20); src = divisão.
                let (head, tail) = bufs.split_at_mut(first + 1);
                mix_lane(&mut head[first], &div[k][0], coef, 2);
                mix_lane(&mut tail[0], &div[k][1], coef, 2);
            } else {
                // 008C2DB8/008C31A7: só buffers[first_buf]; src = soma;
                // coeficiente g*0.5 (008C2DEA/008C31D5).
                mix_lane(&mut bufs[first], &sum[k], coef, 1);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const N: usize = 4;

    fn rec(sel: u8, first_buf: u32, nch: u32) -> BandRec {
        BandRec {
            sel,
            first_buf,
            nch,
        }
    }

    /// Estado com só a rota pedida ligada (`g = 1`, as outras `g = 0`).
    fn state_with(enable: [bool; 5], coef: usize) -> StageState {
        let mut g = [0.0f32; 4];
        g[coef] = 1.0;
        StageState { enable, g }
    }

    fn input<'a>(
        count: i32,
        groups: [&'a [BandRec]; 5],
        state: StageState,
        flag: bool,
    ) -> StageInput<'a> {
        StageInput {
            n: N,
            count,
            groups,
            state,
            flag_13e8: flag,
        }
    }

    fn bufs_of(values: &[f32]) -> Vec<Vec<f32>> {
        values.iter().map(|v| vec![*v; N]).collect()
    }

    #[test]
    fn count_le_2_does_not_stage() {
        // 008C1467/008C1474: count <= 2 → retorno imediato.
        let groups: [&[BandRec]; 5] = [&[], &[], &[], &[], &[]];
        let st = state_with([true, false, false, false, false], COEF_ENABLED);
        let inp = input(2, groups, st, false);
        let mut bufs = bufs_of(&[1.0, 1.0]);
        process(&inp, &mut bufs);
        assert_eq!(bufs[0], vec![1.0; N]);
        assert_eq!(bufs[1], vec![1.0; N]);
    }

    #[test]
    fn one_record_is_identity_when_dyadic() {
        // D = ch²/ch = ch para ch = 3.0 (exato); g = 1 → ch ← D.
        let recs = [rec(8, 0, 2)];
        let groups: [&[BandRec]; 5] = [&recs, &[], &[], &[], &[]];
        let st = state_with([true, false, false, false, false], COEF_ENABLED);
        let inp = input(3, groups, st, false);
        let mut bufs = bufs_of(&[3.0, 3.0]);
        process(&inp, &mut bufs);
        assert_eq!(bufs[0], vec![3.0; N]);
        assert_eq!(bufs[1], vec![3.0; N]);
    }

    #[test]
    fn two_records_use_power_weighted_mean() {
        // (1² + 3²)/(1 + 3) = 2.5 (008C2545 new1).
        let recs = [rec(8, 0, 2), rec(8, 2, 2)];
        let groups: [&[BandRec]; 5] = [&recs, &[], &[], &[], &[]];
        let st = state_with([true, false, false, false, false], COEF_ENABLED);
        let inp = input(3, groups, st, false);
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&inp, &mut bufs);
        for b in bufs.iter() {
            assert_eq!(b, &vec![2.5; N]);
        }
    }

    #[test]
    fn odd_pairs_are_clamped_to_clamp_min() {
        // Σch² = 2 e Σch = 0 → denominador vira CLAMP_MIN (008C2393).
        let recs = [rec(8, 0, 2), rec(8, 2, 2)];
        let groups: [&[BandRec]; 5] = [&recs, &[], &[], &[], &[]];
        let st = state_with([true, false, false, false, false], COEF_ENABLED);
        let inp = input(3, groups, st, false);
        let mut bufs = bufs_of(&[1.0, 1.0, -1.0, -1.0]);
        // Antes: denominador seria 0 (inf). Depois: 2 / CLAMP_MIN.
        let expected = 2.0f32 / CLAMP_MIN;
        assert!(expected.is_finite());
        process(&inp, &mut bufs);
        for b in bufs.iter() {
            assert_eq!(b, &vec![expected; N]);
        }
    }

    #[test]
    fn tipo10_enabled_participates_only_with_sel_10() {
        let recs_ok = [rec(10, 0, 2), rec(10, 2, 2)];
        let groups: [&[BandRec]; 5] = [&[], &[], &recs_ok, &[], &[]];
        let st = state_with([false, false, true, false, false], COEF_ENABLED);
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&input(3, groups, st, false), &mut bufs);
        for b in bufs.iter() {
            assert_eq!(b, &vec![2.5; N]);
        }

        // sel != 10 (008C1B66: sel == tipo) → não participa.
        let recs_bad = [rec(11, 0, 2), rec(11, 2, 2)];
        let groups: [&[BandRec]; 5] = [&[], &[], &recs_bad, &[], &[]];
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&input(3, groups, st, false), &mut bufs);
        assert_eq!(bufs[0], vec![1.0; N]);
        assert_eq!(bufs[2], vec![3.0; N]);
    }

    #[test]
    fn tipo10_disabled_never_mixes() {
        // 008C1FDB–008C1FF1: al = 0 incondicional para tipo 0xA.
        let recs = [rec(10, 0, 2), rec(10, 2, 2)];
        let groups: [&[BandRec]; 5] = [&[], &[], &recs, &[], &[]];
        let st = state_with([false, false, false, false, false], COEF_ENABLED);
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&input(3, groups, st, true), &mut bufs);
        assert_eq!(bufs[0], vec![1.0; N]);
        assert_eq!(bufs[2], vec![3.0; N]);
    }

    #[test]
    fn mono_uses_half_gain_over_channel_sum() {
        // tipo 9 desabilitado, sel = 9, nch = 1, flag = 1 → T1/B/+0x30.
        // D = 2.5, B = 2*2.5 = 5; ch ← 0·ch + (g/2)·B = 2.5 (008C2DEA).
        let recs = [rec(9, 0, 1), rec(9, 1, 1)];
        let groups: [&[BandRec]; 5] = [&[], &recs, &[], &[], &[]];
        let st = state_with([false, false, false, false, false], COEF_GROUP89);
        let mut bufs = bufs_of(&[1.0, 3.0]);
        process(&input(3, groups, st, true), &mut bufs);
        assert_eq!(bufs[0], vec![2.5; N]);
        assert_eq!(bufs[1], vec![2.5; N]);
    }

    #[test]
    fn group89_disabled_requires_flag() {
        let recs = [rec(9, 0, 2), rec(9, 2, 2)];
        let groups: [&[BandRec]; 5] = [&[], &recs, &[], &[], &[]];
        let st = state_with([false, false, false, false, false], COEF_GROUP89);
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&input(3, groups, st, false), &mut bufs);
        assert_eq!(bufs[0], vec![1.0; N]);
        assert_eq!(bufs[2], vec![3.0; N]);
    }

    #[test]
    fn tipo5_disabled_requires_sel_16_to_18() {
        let st = state_with([false, false, false, false, false], COEF_GROUP5);
        for sel in [16u8, 17, 18] {
            let recs = [rec(sel, 0, 2), rec(sel, 2, 2)];
            let groups: [&[BandRec]; 5] = [&[], &[], &[], &[], &recs];
            let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
            process(&input(3, groups, st, false), &mut bufs);
            for b in bufs.iter() {
                assert_eq!(b, &vec![2.5; N], "sel {sel} deveria misturar");
            }
        }
        for sel in [15u8, 19] {
            let recs = [rec(sel, 0, 2), rec(sel, 2, 2)];
            let groups: [&[BandRec]; 5] = [&[], &[], &[], &[], &recs];
            let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
            process(&input(3, groups, st, false), &mut bufs);
            assert_eq!(bufs[0], vec![1.0; N], "sel {sel} não deveria misturar");
        }
    }

    #[test]
    fn tipo5_enabled_requires_sel_16_to_18() {
        let st = state_with([false, false, false, false, true], COEF_ENABLED);
        let ok = [rec(16, 0, 2), rec(16, 2, 2)];
        let groups: [&[BandRec]; 5] = [&[], &[], &[], &[], &ok];
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&input(3, groups, st, false), &mut bufs);
        for b in bufs.iter() {
            assert_eq!(b, &vec![2.5; N]);
        }

        let bad = [rec(19, 0, 2), rec(19, 2, 2)];
        let groups: [&[BandRec]; 5] = [&[], &[], &[], &[], &bad];
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&input(3, groups, st, false), &mut bufs);
        assert_eq!(bufs[0], vec![1.0; N]);
    }

    #[test]
    fn tipo6_disabled_skips_sel_16_to_18() {
        // h(4) && !h(5): sel 7 participa, sel 16 não (008C1F91..008C1FC4).
        let st = state_with([false, false, false, false, false], COEF_GROUP6);
        let ok = [rec(7, 0, 2), rec(7, 2, 2)];
        let groups: [&[BandRec]; 5] = [&[], &[], &[], &ok, &[]];
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&input(3, groups, st, false), &mut bufs);
        for b in bufs.iter() {
            assert_eq!(b, &vec![2.5; N]);
        }

        let bad = [rec(16, 0, 2), rec(16, 2, 2)];
        let groups: [&[BandRec]; 5] = [&[], &[], &[], &bad, &[]];
        let mut bufs = bufs_of(&[1.0, 1.0, 3.0, 3.0]);
        process(&input(3, groups, st, false), &mut bufs);
        assert_eq!(bufs[0], vec![1.0; N]);
    }

    #[test]
    fn disabled_multi_channel_record_does_not_accumulate() {
        // nch = 3 no ramo desabilitado: a passagem A não acumula
        // (008C21E9/008C22E1), mas a passagem B só testa nch == 2
        // (008C2F88/008C2F8D) e mistura com a soma vazia → 0. A assimetria é
        // do binário; está transcrita, não "corrigida".
        let recs = [rec(9, 0, 3), rec(9, 3, 3)];
        let groups: [&[BandRec]; 5] = [&[], &recs, &[], &[], &[]];
        let st = state_with([false, false, false, false, false], COEF_GROUP89);
        let mut bufs = bufs_of(&[1.0, 1.0, 1.0, 3.0, 3.0, 3.0]);
        process(&input(3, groups, st, true), &mut bufs);
        assert_eq!(bufs[0], vec![0.0; N]);
        assert_eq!(bufs[3], vec![0.0; N]);
    }
}
