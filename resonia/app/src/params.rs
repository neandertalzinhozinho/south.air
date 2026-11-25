//! Camada de parâmetros: os 143 descritores de `param_table.rs` expostos ao host (nih-plug).
//!
//! Nada aqui é DSP. Cada parâmetro nasce da tabela (nome, mínimo, máximo, padrão, tipo de
//! controle e rótulos de enum). Ids para o host: `p000`..`p142` (índice da tabela).
//!
//! `NÃO PROVADO` (ver `param_table.rs`): a curva normalizado<->valor de todo parâmetro cujo
//! `Curve` não seja `Linear`. O host usa aqui um mapeamento **linear provisório** para todos;
//! trocar por faixa/curva real é decisão da etapa M4, não desta camada.

use crate::param_table::*;
use nih_plug::prelude::*;
use std::sync::Arc;

/// Um parâmetro do host, na forma que a tabela pede.
pub enum Slot {
    Float(FloatParam),
    Int(IntParam),
    Bool(BoolParam),
}

impl Slot {
    /// Valor simples atual (unidades da tabela).
    pub fn plain(&self) -> f64 {
        match self {
            Slot::Float(p) => p.value() as f64,
            Slot::Int(p) => p.value() as f64,
            Slot::Bool(p) => {
                if p.value() {
                    1.0
                } else {
                    0.0
                }
            }
        }
    }

    fn ptr(&self) -> ParamPtr {
        match self {
            Slot::Float(p) => p.as_ptr(),
            Slot::Int(p) => p.as_ptr(),
            Slot::Bool(p) => p.as_ptr(),
        }
    }
}

/// Rótulo de enum da tabela, ou `None` se o valor está fora da tabela.
pub fn enum_label(table: EnumTable, v: i32) -> Option<&'static str> {
    let labels: &[&str] = match table {
        EnumTable::BandShape => &BAND_SHAPE_LABELS,
        EnumTable::StereoMode => &STEREO_MODE_LABELS,
        EnumTable::Quality => &QUALITY_LABELS,
        EnumTable::BandChannels => &BAND_CHANNELS_LABELS,
    };
    usize::try_from(v).ok().and_then(|i| labels.get(i).copied())
}

/// Grupo do host: bandas ficam em "Band N"; grupos de canais em "Channels".
fn group_of(spec: &ParamSpec) -> String {
    let n = spec.name;
    if let Some(rest) = n.strip_prefix("Band ") {
        if let Some((num, _)) = rest.split_once(' ') {
            if num.chars().all(|c| c.is_ascii_digit()) {
                return format!("Band {num}");
            }
        }
    }
    if spec.id >= 98 {
        return "Channels".to_string();
    }
    String::new()
}

fn make_slot(spec: &ParamSpec) -> Slot {
    match spec.kind {
        Kind::Float => {
            let unit = if spec.name.ends_with("frequency") { " Hz" } else { "" };
            // Casas decimais só para exibição (não é prova de nada).
            let span = spec.max - spec.min;
            let dec: usize = if span >= 1000.0 { 0 } else if span >= 50.0 { 1 } else { 2 };
            FloatParam::new(spec.name, spec.default as f32, FloatRange::Linear { min: spec.min as f32, max: spec.max as f32 })
                .with_unit(unit)
                .with_value_to_string(Arc::new(move |v| format!("{:.*}", dec, v)))
                .into_slot()
        }
        Kind::Int => IntParam::new(spec.name, spec.default as i32, IntRange::Linear { min: spec.min as i32, max: spec.max as i32 }).into_slot(),
        Kind::Enum(t) => IntParam::new(spec.name, spec.default as i32, IntRange::Linear { min: spec.min as i32, max: spec.max as i32 })
            .with_value_to_string(Arc::new(move |v| enum_label(t, v).map(str::to_string).unwrap_or_else(|| v.to_string())))
            .into_slot(),
        Kind::Bool => {
            let b = BoolParam::new(spec.name, spec.default >= 0.5);
            // "Bypass" (id 97) é o parâmetro de bypass do host.
            let b = if spec.name == "Bypass" { b.make_bypass() } else { b };
            b.into_slot()
        }
    }
}

trait IntoSlot {
    fn into_slot(self) -> Slot;
}
impl IntoSlot for FloatParam {
    fn into_slot(self) -> Slot {
        Slot::Float(self)
    }
}
impl IntoSlot for IntParam {
    fn into_slot(self) -> Slot {
        Slot::Int(self)
    }
}
impl IntoSlot for BoolParam {
    fn into_slot(self) -> Slot {
        Slot::Bool(self)
    }
}

/// Os 143 parâmetros do plugin, na ordem da tabela.
pub struct ResoniaParams {
    slots: Vec<Slot>,
}

impl Default for ResoniaParams {
    fn default() -> Self {
        Self { slots: PARAMS.iter().map(make_slot).collect() }
    }
}

impl ResoniaParams {
    pub fn slot(&self, index: usize) -> Option<&Slot> {
        self.slots.get(index)
    }

    pub fn len(&self) -> usize {
        self.slots.len()
    }

    pub fn is_empty(&self) -> bool {
        self.slots.is_empty()
    }

    /// Valor simples do parâmetro `index`.
    pub fn plain(&self, index: usize) -> f64 {
        self.slots.get(index).map_or(0.0, Slot::plain)
    }

    /// Escreve o valor simples via `setter` (gesto completo begin/set/end).
    pub fn set_with_gesture(&self, setter: &ParamSetter, index: usize, plain: f64) {
        match self.slots.get(index) {
            Some(Slot::Float(p)) => {
                setter.begin_set_parameter(p);
                setter.set_parameter(p, plain as f32);
                setter.end_set_parameter(p);
            }
            Some(Slot::Int(p)) => {
                setter.begin_set_parameter(p);
                setter.set_parameter(p, plain.round() as i32);
                setter.end_set_parameter(p);
            }
            Some(Slot::Bool(p)) => {
                setter.begin_set_parameter(p);
                setter.set_parameter(p, plain >= 0.5);
                setter.end_set_parameter(p);
            }
            None => {}
        }
    }
}

// SAFETY: `param_map` devolve ponteiros para os elementos do `Vec` interno, que nunca é
// redimensionado depois de criado; o wrapper do nih-plug guarda o `Arc<ResoniaParams>`.
unsafe impl Params for ResoniaParams {
    fn param_map(&self) -> Vec<(String, ParamPtr, String)> {
        self.slots.iter().zip(PARAMS.iter()).map(|(s, spec)| (format!("p{:03}", spec.id), s.ptr(), group_of(spec))).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn table_has_143_sequential_ids_inside_range() {
        assert_eq!(PARAMS.len(), 143);
        for (i, p) in PARAMS.iter().enumerate() {
            assert_eq!(p.id as usize, i);
            assert!(p.min <= p.default && p.default <= p.max, "{}: default fora da faixa", p.name);
            assert!(!p.name.is_empty());
        }
    }

    #[test]
    fn spot_checks_against_the_table() {
        assert_eq!(PARAMS[0].name, "Depth");
        assert_eq!((PARAMS[0].min, PARAMS[0].max, PARAMS[0].default), (0.0, 10.0, 5.0));
        assert_eq!(PARAMS[21].name, "Band 1 frequency");
        assert_eq!((PARAMS[21].min, PARAMS[21].max, PARAMS[21].default), (20.0, 20000.0, 100.0));
        assert_eq!(PARAMS[97].name, "Bypass");
        assert_eq!(PARAMS[142].name, "Channel 16 enabled");
        assert_eq!(PARAMS[27].kind, Kind::Enum(EnumTable::BandShape));
        assert_eq!(PARAMS[0].curve, Curve::Linear);
        assert_eq!(PARAMS[21].curve, Curve::NaoProvado);
    }

    #[test]
    fn enum_labels() {
        assert_eq!(enum_label(EnumTable::BandShape, 2), Some("Bell"));
        assert_eq!(enum_label(EnumTable::StereoMode, 1), Some("M/S"));
        assert_eq!(enum_label(EnumTable::BandChannels, 19), Some("Cs"));
        assert_eq!(enum_label(EnumTable::Quality, 3), None);
        assert_eq!(enum_label(EnumTable::Quality, -1), None);
    }

    #[test]
    fn host_map_has_143_unique_ids_and_defaults() {
        let p = ResoniaParams::default();
        let map = p.param_map();
        assert_eq!(map.len(), 143);
        let mut ids: Vec<&str> = map.iter().map(|(id, _, _)| id.as_str()).collect();
        ids.sort_unstable();
        ids.dedup();
        assert_eq!(ids.len(), 143);
        for (i, spec) in PARAMS.iter().enumerate() {
            assert!((p.plain(i) - spec.default).abs() < 1e-4, "{}: {} != {}", spec.name, p.plain(i), spec.default);
        }
        assert_eq!(map[27].2, "Band 1");
        assert_eq!(map[100].2, "Channels");
        assert_eq!(map[0].2, "");
    }
}
