//! GERADO por `resonia/_ferramentas/gerar_param_table.py`. NAO EDITAR A MAO.
//!
//! Fonte: `RECURSOS_VALIDADOS_recuperados/parameter_table_143_params.json`
//! (SHA-256 do arquivo: 0d298b3f5c9104153fbc42a257b514dfe47d6d321fca6970086e5ae46bbdd376).
//! Tabela de 143 descritores em `0x238E9C0` (registros de 0x68 B), lida do dump 1.0.6
//! em 2026-11-25 (docs/engine/recursos-recuperados.md 2.4).
//!
//! Provado (2.4): ids 0..142, nomes, minimo, maximo, flags, ponteiros de callback.
//! `NAO PROVADO`: (a) que `default` seja o estado inicial gravado pelo motor (o JSON o chama
//! `initial_or_default_candidate`); (b) a curva normalizado<->valor de todo parametro cujo
//! callback `+72` nao e `0x3351A0` (ver `Curve`); (c) o significado das flags; (d) rotulos de
//! `Mode` (id 2) e `Band solo` (id 91): o formatador nao foi resolvido; (e) a classe `Kind`,
//! que e so a escolha de controle para o host/GUI (pelo formatador `+88`).

/// Controle exposto ao host/GUI. Derivado do formatador `+88` e dos limites; nao e prova de semantica.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    /// Contínuo.
    Float,
    /// 0/1 (formatador `0x335F40`).
    Bool,
    /// Inteiro discreto sem tabela de rótulos provada.
    Int,
    /// Inteiro com tabela de rótulos lida do dump.
    Enum(EnumTable),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum EnumTable {
    BandShape,
    StereoMode,
    Quality,
    BandChannels,
}

/// Curva normalizado<->valor.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Curve {
    /// `cb+72 = 0x3351A0`, `cb+80 = 0x3351E0`: (x-min)/(max-min) e inversa, PROVADO (2.4).
    Linear,
    /// Outro callback: curva NAO PROVADA. O host usa mapeamento linear provisório.
    NaoProvado,
}

#[derive(Clone, Copy, Debug)]
pub struct ParamSpec {
    pub id: u32,
    pub name: &'static str,
    pub min: f64,
    pub max: f64,
    /// `initial_or_default_candidate`: NAO PROVADO como estado inicial do motor.
    pub default: f64,
    pub flags: u64,
    pub kind: Kind,
    pub curve: Curve,
    /// RVAs (dump 1.0.6) dos 4 callbacks: valor->normalizado, normalizado->valor, formatador, parser.
    pub callbacks: [u32; 4],
}

/// Rótulos lidos do dump (tabela `band_shape`).
pub const BAND_SHAPE_LABELS: [&str; 8] = ["Low cut", "Low shelf", "Bell", "Bandpass", "Band reject", "Tilt", "High shelf", "High cut"];

/// Rótulos lidos do dump (tabela `stereo_mode`).
pub const STEREO_MODE_LABELS: [&str; 2] = ["L/R", "M/S"];

/// Rótulos lidos do dump (tabela `quality`). Rótulos de quality/band_channels: NAO reconferidos no 1.0.6 (INCERTO).
pub const QUALITY_LABELS: [&str; 3] = ["normal", "high", "ultra"];

/// Rótulos lidos do dump (tabela `band_channels`). Rótulos de quality/band_channels: NAO reconferidos no 1.0.6 (INCERTO).
pub const BAND_CHANNELS_LABELS: [&str; 20] = ["all channels", "all (-LFE)", "all (-C)", "all (-C -LFE)", "surr + ceil", "ceiling", "surround", "LCR", "L/R", "C", "LFE", "Lc/Rc", "Lw/Rw", "Ls/Rs", "Lss/Rss", "Lsr/Rsr", "Ltf/Rtf", "Ltm/Rtm", "Ltr/Rtr", "Cs"];

pub const PARAM_COUNT: usize = 143;

pub static PARAMS: [ParamSpec; PARAM_COUNT] = [
    ParamSpec { id: 0, name: "Depth", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 1, name: "Low latency", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 2, name: "Mode", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Int, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336900, 0x319170] },
    ParamSpec { id: 3, name: "Quality", min: 0.0, max: 2.0, default: 0.0, flags: 0x101, kind: Kind::Enum(EnumTable::Quality), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3369A0, 0x319170] },
    ParamSpec { id: 4, name: "Linear phase", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 5, name: "Detail", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 6, name: "Attack", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 7, name: "Release", min: 0.0, max: 10.0, default: 3.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 8, name: "Detail tilt low", min: 0.1, max: 10.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335790, 0x335830, 0x335D10, 0x335CB0] },
    ParamSpec { id: 9, name: "Detail tilt high", min: 0.1, max: 10.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335790, 0x335830, 0x335D10, 0x335CB0] },
    ParamSpec { id: 10, name: "Attack tilt low", min: 0.1, max: 10.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335790, 0x335830, 0x335D10, 0x335CB0] },
    ParamSpec { id: 11, name: "Attack tilt high", min: 0.1, max: 10.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335790, 0x335830, 0x335D10, 0x335CB0] },
    ParamSpec { id: 12, name: "Release tilt low", min: 0.1, max: 10.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335790, 0x335830, 0x335D10, 0x335CB0] },
    ParamSpec { id: 13, name: "Release tilt high", min: 0.1, max: 10.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335790, 0x335830, 0x335D10, 0x335CB0] },
    ParamSpec { id: 14, name: "Sidechain", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 15, name: "Sidechain listen", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 16, name: "Stereo mode", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::StereoMode), curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x3367D0, 0x336830] },
    ParamSpec { id: 17, name: "Stereo link", min: 0.0, max: 100.0, default: 100.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335CF0, 0x335CB0] },
    ParamSpec { id: 18, name: "Stereo focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 19, name: "Band 1 used", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 20, name: "Band 1 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 21, name: "Band 1 frequency", min: 20.0, max: 20000.0, default: 100.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x3353B0, 0x335470, 0x335D80, 0x335DE0] },
    ParamSpec { id: 22, name: "Band 1 depth", min: -10.0, max: 10.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 23, name: "Band 1 q", min: 0.1, max: 10.0, default: 0.707, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335550, 0x335670, 0x335910, 0x335CB0] },
    ParamSpec { id: 24, name: "Band 1 slope", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 25, name: "Band 1 focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 26, name: "Band 1 channels", min: 0.0, max: 19.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandChannels), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336610, 0x319170] },
    ParamSpec { id: 27, name: "Band 1 shape", min: 0.0, max: 7.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandShape), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3366A0, 0x336700] },
    ParamSpec { id: 28, name: "Band 2 used", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 29, name: "Band 2 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 30, name: "Band 2 frequency", min: 20.0, max: 20000.0, default: 4000.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x3353B0, 0x335470, 0x335D80, 0x335DE0] },
    ParamSpec { id: 31, name: "Band 2 depth", min: -10.0, max: 10.0, default: 2.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 32, name: "Band 2 q", min: 0.1, max: 10.0, default: 0.707, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335550, 0x335670, 0x335910, 0x335CB0] },
    ParamSpec { id: 33, name: "Band 2 slope", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 34, name: "Band 2 focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 35, name: "Band 2 channels", min: 0.0, max: 19.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandChannels), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336610, 0x319170] },
    ParamSpec { id: 36, name: "Band 2 shape", min: 0.0, max: 7.0, default: 2.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandShape), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3366A0, 0x336700] },
    ParamSpec { id: 37, name: "Band 3 used", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 38, name: "Band 3 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 39, name: "Band 3 frequency", min: 20.0, max: 20000.0, default: 16000.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x3353B0, 0x335470, 0x335D80, 0x335DE0] },
    ParamSpec { id: 40, name: "Band 3 depth", min: -10.0, max: 10.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 41, name: "Band 3 q", min: 0.1, max: 10.0, default: 0.707, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335550, 0x335670, 0x335910, 0x335CB0] },
    ParamSpec { id: 42, name: "Band 3 slope", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 43, name: "Band 3 focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 44, name: "Band 3 channels", min: 0.0, max: 19.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandChannels), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336610, 0x319170] },
    ParamSpec { id: 45, name: "Band 3 shape", min: 0.0, max: 7.0, default: 7.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandShape), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3366A0, 0x336700] },
    ParamSpec { id: 46, name: "Band 4 used", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 47, name: "Band 4 enabled", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 48, name: "Band 4 frequency", min: 20.0, max: 20000.0, default: 1000.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x3353B0, 0x335470, 0x335D80, 0x335DE0] },
    ParamSpec { id: 49, name: "Band 4 depth", min: -10.0, max: 10.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 50, name: "Band 4 q", min: 0.1, max: 10.0, default: 0.707, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335550, 0x335670, 0x335910, 0x335CB0] },
    ParamSpec { id: 51, name: "Band 4 slope", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 52, name: "Band 4 focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 53, name: "Band 4 channels", min: 0.0, max: 19.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandChannels), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336610, 0x319170] },
    ParamSpec { id: 54, name: "Band 4 shape", min: 0.0, max: 7.0, default: 2.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandShape), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3366A0, 0x336700] },
    ParamSpec { id: 55, name: "Band 5 used", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 56, name: "Band 5 enabled", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 57, name: "Band 5 frequency", min: 20.0, max: 20000.0, default: 1000.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x3353B0, 0x335470, 0x335D80, 0x335DE0] },
    ParamSpec { id: 58, name: "Band 5 depth", min: -10.0, max: 10.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 59, name: "Band 5 q", min: 0.1, max: 10.0, default: 0.707, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335550, 0x335670, 0x335910, 0x335CB0] },
    ParamSpec { id: 60, name: "Band 5 slope", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 61, name: "Band 5 focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 62, name: "Band 5 channels", min: 0.0, max: 19.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandChannels), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336610, 0x319170] },
    ParamSpec { id: 63, name: "Band 5 shape", min: 0.0, max: 7.0, default: 2.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandShape), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3366A0, 0x336700] },
    ParamSpec { id: 64, name: "Band 6 used", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 65, name: "Band 6 enabled", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 66, name: "Band 6 frequency", min: 20.0, max: 20000.0, default: 1000.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x3353B0, 0x335470, 0x335D80, 0x335DE0] },
    ParamSpec { id: 67, name: "Band 6 depth", min: -10.0, max: 10.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 68, name: "Band 6 q", min: 0.1, max: 10.0, default: 0.707, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335550, 0x335670, 0x335910, 0x335CB0] },
    ParamSpec { id: 69, name: "Band 6 slope", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 70, name: "Band 6 focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 71, name: "Band 6 channels", min: 0.0, max: 19.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandChannels), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336610, 0x319170] },
    ParamSpec { id: 72, name: "Band 6 shape", min: 0.0, max: 7.0, default: 2.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandShape), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3366A0, 0x336700] },
    ParamSpec { id: 73, name: "Band 7 used", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 74, name: "Band 7 enabled", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 75, name: "Band 7 frequency", min: 20.0, max: 20000.0, default: 1000.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x3353B0, 0x335470, 0x335D80, 0x335DE0] },
    ParamSpec { id: 76, name: "Band 7 depth", min: -10.0, max: 10.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 77, name: "Band 7 q", min: 0.1, max: 10.0, default: 0.707, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335550, 0x335670, 0x335910, 0x335CB0] },
    ParamSpec { id: 78, name: "Band 7 slope", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 79, name: "Band 7 focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 80, name: "Band 7 channels", min: 0.0, max: 19.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandChannels), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336610, 0x319170] },
    ParamSpec { id: 81, name: "Band 7 shape", min: 0.0, max: 7.0, default: 2.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandShape), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3366A0, 0x336700] },
    ParamSpec { id: 82, name: "Band 8 used", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 83, name: "Band 8 enabled", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x335F40, 0x319170] },
    ParamSpec { id: 84, name: "Band 8 frequency", min: 20.0, max: 20000.0, default: 1000.0, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x3353B0, 0x335470, 0x335D80, 0x335DE0] },
    ParamSpec { id: 85, name: "Band 8 depth", min: -10.0, max: 10.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 86, name: "Band 8 q", min: 0.1, max: 10.0, default: 0.707, flags: 0x0, kind: Kind::Float, curve: Curve::NaoProvado, callbacks: [0x335550, 0x335670, 0x335910, 0x335CB0] },
    ParamSpec { id: 87, name: "Band 8 slope", min: 0.0, max: 10.0, default: 5.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335910, 0x335CB0] },
    ParamSpec { id: 88, name: "Band 8 focus", min: 0.0, max: 1.0, default: 0.5, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335F70, 0x336080] },
    ParamSpec { id: 89, name: "Band 8 channels", min: 0.0, max: 19.0, default: 0.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandChannels), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336610, 0x319170] },
    ParamSpec { id: 90, name: "Band 8 shape", min: 0.0, max: 7.0, default: 2.0, flags: 0x1, kind: Kind::Enum(EnumTable::BandShape), curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x3366A0, 0x336700] },
    ParamSpec { id: 91, name: "Band solo", min: 0.0, max: 8.0, default: 0.0, flags: 0x101, kind: Kind::Int, curve: Curve::NaoProvado, callbacks: [0x335240, 0x335300, 0x336A50, 0x319170] },
    ParamSpec { id: 92, name: "Max cut", min: 0.0, max: 24.0, default: 24.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335E40, 0x335EC0] },
    ParamSpec { id: 93, name: "Wet trim", min: -18.0, max: 18.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335E00, 0x335CB0] },
    ParamSpec { id: 94, name: "Mix", min: 0.0, max: 100.0, default: 100.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335CF0, 0x335CB0] },
    ParamSpec { id: 95, name: "Out trim", min: -18.0, max: 18.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335E00, 0x335CB0] },
    ParamSpec { id: 96, name: "Delta", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 97, name: "Bypass", min: 0.0, max: 1.0, default: 0.0, flags: 0x10001, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 98, name: "LR depth", min: 0.0, max: 1.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335D10, 0x335CB0] },
    ParamSpec { id: 99, name: "LR enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 100, name: "LR solo", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 101, name: "LR delta", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 102, name: "LR link all", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 103, name: "Center depth", min: 0.0, max: 1.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335D10, 0x335CB0] },
    ParamSpec { id: 104, name: "Center enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 105, name: "Center solo", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 106, name: "Center delta", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 107, name: "Center link all", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 108, name: "LFE depth", min: 0.0, max: 1.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335D10, 0x335CB0] },
    ParamSpec { id: 109, name: "LFE enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 110, name: "LFE solo", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 111, name: "LFE delta", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 112, name: "LFE link all", min: 0.0, max: 1.0, default: 0.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 113, name: "Surround depth", min: 0.0, max: 1.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335D10, 0x335CB0] },
    ParamSpec { id: 114, name: "Surround enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 115, name: "Surround solo", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 116, name: "Surround delta", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 117, name: "Surround link all", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 118, name: "Ceiling depth", min: 0.0, max: 1.0, default: 1.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335D10, 0x335CB0] },
    ParamSpec { id: 119, name: "Ceiling enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 120, name: "Ceiling solo", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 121, name: "Ceiling delta", min: 0.0, max: 1.0, default: 0.0, flags: 0x101, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 122, name: "Ceiling link all", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 123, name: "Link all", min: 0.0, max: 100.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335CF0, 0x335CB0] },
    ParamSpec { id: 124, name: "Group link LCR", min: 0.0, max: 100.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335CF0, 0x335CB0] },
    ParamSpec { id: 125, name: "Group link surround", min: 0.0, max: 100.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335CF0, 0x335CB0] },
    ParamSpec { id: 126, name: "Group link ceiling", min: 0.0, max: 100.0, default: 0.0, flags: 0x0, kind: Kind::Float, curve: Curve::Linear, callbacks: [0x3351A0, 0x3351E0, 0x335CF0, 0x335CB0] },
    ParamSpec { id: 127, name: "Channel 1 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 128, name: "Channel 2 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 129, name: "Channel 3 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 130, name: "Channel 4 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 131, name: "Channel 5 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 132, name: "Channel 6 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 133, name: "Channel 7 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 134, name: "Channel 8 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 135, name: "Channel 9 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 136, name: "Channel 10 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 137, name: "Channel 11 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 138, name: "Channel 12 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 139, name: "Channel 13 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 140, name: "Channel 14 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 141, name: "Channel 15 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
    ParamSpec { id: 142, name: "Channel 16 enabled", min: 0.0, max: 1.0, default: 1.0, flags: 0x1, kind: Kind::Bool, curve: Curve::NaoProvado, callbacks: [0x3358F0, 0x3358F0, 0x335F40, 0x319170] },
];
