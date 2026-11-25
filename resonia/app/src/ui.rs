//! Tela do Resonia, compartilhada pela janela do plugin (lib.rs) e pelo aplicativo (main.rs).
//!
//! Layout no modelo pedido pelo usuário (2026-11-25):
//! - coluna da esquerda: marca, soft/hard e os knobs depth/detail/attack/release;
//! - coluna de controles: sidechain, stereo, tilt, scale;
//! - barra superior: estado do motor;
//! - gráfico de bandas com nós arrastáveis;
//! - barra inferior: bypass, delta, mix, out, quality e low latency.
//!
//! Paleta preta e laranja, própria do Resonia.
//!
//! Recursos usados de `resonia/RECURSOS_VALIDADOS_recuperados` (embutidos no binário):
//! - fontes CoFo Sans Regular/Medium;
//! - ícones SVG (fones, SC, liga/desliga, delta, lixeira, ajuda, formatos de banda, títulos de
//!   seção, "fast/slow");
//! - texturas PNG de knob (sombra e face).
//!
//! Ficam de fora as marcas de terceiros: logo, palavra "soothe" e o atlas PNG que traz essas
//! marcas.
//!
//! O que é só desenho:
//! - A curva do gráfico é ilustrativa, calculada dos parâmetros de banda: não é a resposta
//!   do motor, que ainda não expõe a curva de redução.
//! - "soft/hard" é o rótulo de exibição do parâmetro `Mode` (0/1), e "even" é a exibição de
//!   `Stereo focus` = 0,5. Nenhum dos dois foi conferido contra o binário.
//!
//! Fontes e ícones vêm de uma pasta ignorada pelo git, então só compila onde ela existe.

use crate::param_table::*;
use crate::params::enum_label;
use egui::{
    Align2, Color32, CornerRadius, FontFamily, FontId, Mesh, Pos2, Rect, Sense, Shape, Stroke, StrokeKind,
    TextureHandle, TextureOptions, Ui, Vec2,
};
use nih_plug_egui::egui;
use std::collections::HashMap;

pub const WIDTH: f32 = 1050.0;
pub const HEIGHT: f32 = 640.0;

// ---------------------------------------------------------------------------
// Paleta (preto e laranja)
// ---------------------------------------------------------------------------
mod pal {
    use super::Color32;
    pub const BG: Color32 = Color32::from_rgb(0x0b, 0x0b, 0x0d);
    pub const PANEL: Color32 = Color32::from_rgb(0x13, 0x13, 0x16);
    pub const PANEL_HI: Color32 = Color32::from_rgb(0x1b, 0x1b, 0x1f);
    pub const FIELD: Color32 = Color32::from_rgb(0x22, 0x22, 0x27);
    pub const FIELD_HOVER: Color32 = Color32::from_rgb(0x2b, 0x2b, 0x31);
    pub const EDGE: Color32 = Color32::from_rgb(0x2e, 0x2c, 0x2b);
    pub const TEXT: Color32 = Color32::from_rgb(0xf1, 0xea, 0xe3);
    pub const DIM: Color32 = Color32::from_rgb(0x95, 0x8b, 0x82);
    pub const FAINT: Color32 = Color32::from_rgb(0x55, 0x4f, 0x4a);
    pub const ORANGE: Color32 = Color32::from_rgb(0xff, 0x7a, 0x1a);
    pub const ORANGE_HI: Color32 = Color32::from_rgb(0xff, 0xa6, 0x4d);
    pub const ORANGE_LO: Color32 = Color32::from_rgb(0x9c, 0x45, 0x08);
    pub const PLOT_TOP: Color32 = Color32::from_rgb(0x1e, 0x15, 0x0f);
    pub const PLOT_MID: Color32 = Color32::from_rgb(0x15, 0x11, 0x0e);
    pub const FILL_TOP: Color32 = Color32::from_rgb(0x3a, 0x1d, 0x08);
    pub const FILL_BOT: Color32 = Color32::from_rgb(0x1a, 0x0e, 0x06);
    pub const GRID: Color32 = Color32::from_rgb(0x2a, 0x22, 0x1c);
    pub const CURVE: Color32 = Color32::from_rgb(0xff, 0xe2, 0xc4);
    pub const KNOB: Color32 = Color32::from_rgb(0x26, 0x25, 0x27);
    pub const TRACK: Color32 = Color32::from_rgb(0x2d, 0x2a, 0x28);
    /// Cor de cada nó de banda (1..8).
    pub const BAND: [Color32; 8] = [
        Color32::from_rgb(0xff, 0x4d, 0x2e),
        Color32::from_rgb(0xff, 0x8c, 0x1a),
        Color32::from_rgb(0xff, 0xc2, 0x3a),
        Color32::from_rgb(0xff, 0x6a, 0x7a),
        Color32::from_rgb(0xe8, 0xa8, 0x70),
        Color32::from_rgb(0xff, 0xd8, 0x8a),
        Color32::from_rgb(0xd9, 0x5f, 0x1e),
        Color32::from_rgb(0xff, 0xb0, 0x60),
    ];
}

// ---------------------------------------------------------------------------
// Recursos embutidos (RECURSOS_VALIDADOS_recuperados)
// ---------------------------------------------------------------------------
macro_rules! rec {
    ($p:literal) => {
        include_bytes!(concat!("../../RECURSOS_VALIDADOS_recuperados/", $p))
    };
}

const FONT_REGULAR: &[u8] = rec!("fontes/font_01ff1e30.ttf"); // CoFo Sans Regular
const FONT_MEDIUM: &[u8] = rec!("fontes/font_01fd02e0.ttf"); // CoFo Sans Medium

/// Ícones SVG: (nome, bytes). Cores do SVG são trocadas por branco na carga e tingidas na tela.
const SVGS: &[(&str, &[u8])] = &[
    ("headphones", rec!("svg/svg_020586d0.svg")),
    ("sc", rec!("svg/svg_02058940.svg")),
    ("power", rec!("svg/svg_0205ea20.svg")),
    ("delta", rec!("svg/svg_02060c20.svg")),
    ("trash", rec!("svg/svg_0205e890.svg")),
    ("help", rec!("svg/svg_020583e0.svg")),
    ("caret", rec!("svg/svg_0205ad60.svg")),
    ("updown", rec!("svg/svg_02061070.svg")),
    ("fastslow", rec!("svg/svg_02050f50.svg")),
    ("h_stereo", rec!("svg/svg_0205ae70.svg")),
    ("h_tilt", rec!("svg/svg_0205b500.svg")),
    ("h_scale", rec!("svg/svg_0205a720.svg")),
    // Formatos de banda, na ordem de BAND_SHAPE_LABELS.
    ("shape0", rec!("svg/svg_02061dc0.svg")),
    ("shape1", rec!("svg/svg_020615b0.svg")),
    ("shape2", rec!("svg/svg_02061410.svg")),
    ("shape3", rec!("svg/svg_02061980.svg")),
    ("shape4", rec!("svg/svg_02061f30.svg")),
    ("shape5", rec!("svg/svg_02061730.svg")),
    ("shape6", rec!("svg/svg_02061b70.svg")),
    ("shape7", rec!("svg/svg_02062120.svg")),
];

const PNG_KNOB_SHADOW: &[u8] = rec!("png/png_02052850.png");
const PNG_KNOB_FACE: &[u8] = rec!("png/png_0204c060.png");

struct Assets {
    icons: HashMap<&'static str, TextureHandle>,
    knob_shadow: Option<TextureHandle>,
    knob_face: Option<TextureHandle>,
}

fn whiten_svg(src: &[u8]) -> Vec<u8> {
    // Toda cor de preenchimento/traço vira branco; a cor final vem do `tint` na tela.
    let s = String::from_utf8_lossy(src);
    let mut out = String::with_capacity(s.len());
    let mut rest: &str = &s;
    while let Some(i) = rest.find('#') {
        out.push_str(&rest[..i]);
        let after = &rest[i + 1..];
        let n = after.chars().take_while(|c| c.is_ascii_hexdigit()).count();
        if n == 3 || n == 6 || n == 8 {
            out.push_str("#ffffff");
            rest = &after[n..];
        } else {
            out.push('#');
            rest = after;
        }
    }
    out.push_str(rest);
    out.into_bytes()
}

fn raster_svg(ctx: &egui::Context, name: &str, src: &[u8], scale: f32) -> Option<TextureHandle> {
    use resvg::{tiny_skia, usvg};
    let data = whiten_svg(src);
    let tree = usvg::Tree::from_data(&data, &usvg::Options::default()).ok()?;
    let sz = tree.size();
    let (w, h) = ((sz.width() * scale).ceil() as u32, (sz.height() * scale).ceil() as u32);
    let mut pix = tiny_skia::Pixmap::new(w.max(1), h.max(1))?;
    resvg::render(&tree, tiny_skia::Transform::from_scale(scale, scale), &mut pix.as_mut());
    let img = egui::ColorImage::from_rgba_premultiplied([pix.width() as usize, pix.height() as usize], pix.data());
    Some(ctx.load_texture(format!("svg_{name}"), img, TextureOptions::LINEAR))
}

fn load_png(ctx: &egui::Context, name: &str, src: &[u8]) -> Option<TextureHandle> {
    let img = image::load_from_memory(src).ok()?.to_rgba8();
    let (w, h) = img.dimensions();
    let ci = egui::ColorImage::from_rgba_unmultiplied([w as usize, h as usize], img.as_raw());
    Some(ctx.load_texture(format!("png_{name}"), ci, TextureOptions::LINEAR))
}

impl Assets {
    fn load(ctx: &egui::Context) -> Assets {
        let mut icons = HashMap::new();
        for (name, bytes) in SVGS {
            if let Some(t) = raster_svg(ctx, name, bytes, 4.0) {
                icons.insert(*name, t);
            }
        }
        Assets {
            icons,
            knob_shadow: load_png(ctx, "knob_shadow", PNG_KNOB_SHADOW),
            knob_face: load_png(ctx, "knob_face", PNG_KNOB_FACE),
        }
    }
}

// ---------------------------------------------------------------------------
// Interface com o host / aplicativo
// ---------------------------------------------------------------------------

/// Leitura e escrita de parâmetros em valor simples (unidades da tabela). Cada `set` é um
/// gesto completo para o host (plugin) ou uma simples atribuição (aplicativo).
pub trait ParamAccess {
    fn get(&self, index: usize) -> f64;
    fn set(&mut self, index: usize, value: f64);
}

/// Informações do motor para a barra superior.
pub struct UiInfo<'a> {
    pub engine: &'a str,
    pub latency_samples: u32,
    pub sample_rate: Option<f32>,
    pub status: Option<&'a str>,
    /// Versão do plugin (`CARGO_PKG_VERSION`).
    pub version: &'a str,
}

#[derive(Clone, Copy, PartialEq, Eq, Default)]
pub enum Overlay {
    #[default]
    None,
    Settings,
    About,
}

/// Estado só da tela (não vai para o host).
pub struct UiState {
    /// Banda selecionada (0..8).
    pub band: Option<usize>,
    pub overlay: Overlay,
    /// Faixa do eixo de redução no gráfico (dB): 9, 18 ou 30.
    pub range_db: f32,
    assets: Option<Assets>,
}

impl Default for UiState {
    fn default() -> Self {
        UiState { band: None, overlay: Overlay::None, range_db: 9.0, assets: None }
    }
}

pub fn setup_style(ctx: &egui::Context) {
    let mut fonts = egui::FontDefinitions::default();
    fonts.font_data.insert("cofo".into(), egui::FontData::from_static(FONT_REGULAR).into());
    fonts.font_data.insert("cofo_med".into(), egui::FontData::from_static(FONT_MEDIUM).into());
    fonts.families.entry(FontFamily::Proportional).or_default().insert(0, "cofo".into());
    let mut med = vec!["cofo_med".to_string()];
    med.extend(fonts.families.get(&FontFamily::Proportional).cloned().unwrap_or_default());
    fonts.families.insert(FontFamily::Name("med".into()), med);
    ctx.set_fonts(fonts);

    let mut v = egui::Visuals::dark();
    v.panel_fill = pal::BG;
    v.window_fill = pal::PANEL;
    v.extreme_bg_color = pal::FIELD;
    v.faint_bg_color = pal::PANEL_HI;
    v.override_text_color = Some(pal::TEXT);
    v.selection.bg_fill = pal::ORANGE_LO;
    v.selection.stroke = Stroke::new(1.0_f32, pal::ORANGE);
    v.widgets.inactive.bg_fill = pal::FIELD;
    v.widgets.inactive.weak_bg_fill = pal::FIELD;
    v.widgets.hovered.bg_fill = pal::FIELD_HOVER;
    v.widgets.hovered.weak_bg_fill = pal::FIELD_HOVER;
    v.widgets.active.bg_fill = pal::ORANGE_LO;
    v.widgets.noninteractive.bg_stroke = Stroke::new(1.0_f32, pal::EDGE);
    v.window_stroke = Stroke::new(1.0_f32, pal::EDGE);
    ctx.set_visuals(v);
}

fn med(size: f32) -> FontId {
    FontId::new(size, FontFamily::Name("med".into()))
}
fn reg(size: f32) -> FontId {
    FontId::new(size, FontFamily::Proportional)
}

fn spec(index: usize) -> &'static ParamSpec {
    &PARAMS[index]
}

// ---------------------------------------------------------------------------
// Primitivas de desenho
// ---------------------------------------------------------------------------

fn vgrad(painter: &egui::Painter, rect: Rect, top: Color32, bottom: Color32) {
    let mut m = Mesh::default();
    m.colored_vertex(rect.left_top(), top);
    m.colored_vertex(rect.right_top(), top);
    m.colored_vertex(rect.right_bottom(), bottom);
    m.colored_vertex(rect.left_bottom(), bottom);
    m.add_triangle(0, 1, 2);
    m.add_triangle(0, 2, 3);
    painter.add(Shape::mesh(m));
}

fn icon(painter: &egui::Painter, a: &Assets, name: &str, center: Pos2, height: f32, tint: Color32) {
    if let Some(t) = a.icons.get(name) {
        let s = t.size_vec2();
        let w = height * s.x / s.y.max(1.0);
        let r = Rect::from_center_size(center, Vec2::new(w, height));
        painter.image(t.id(), r, Rect::from_min_max(Pos2::ZERO, Pos2::new(1.0, 1.0)), tint);
    }
}

fn fmt_val(index: usize, v: f64) -> String {
    let s = spec(index);
    match index {
        92 if v >= 23.95 => "off".into(),
        92 => format!("{:.1} dB", v),
        93 | 95 => format!("{:.1} dB", v),
        17 | 94 => format!("{:.0} %", v),
        18 if (v - 0.5).abs() < 0.005 => "even".into(),
        _ => {
            if s.name.ends_with("frequency") {
                if v >= 1000.0 { format!("{:.2}k", v / 1000.0) } else { format!("{:.0}", v) }
            } else {
                format!("{:.1}", v)
            }
        }
    }
}

/// Arraste vertical/horizontal sobre `resp` altera o parâmetro; duplo clique volta ao padrão.
fn drag_param(ui: &Ui, p: &mut dyn ParamAccess, index: usize, resp: &egui::Response, px_full: f32) {
    let s = spec(index);
    if resp.double_clicked() {
        p.set(index, s.default);
        return;
    }
    if resp.dragged() {
        let d = resp.drag_delta();
        let fine = ui.input(|i| i.modifiers.shift);
        let k = if fine { 0.15 } else { 1.0 };
        let px = (d.x - d.y) as f64;
        if px != 0.0 {
            let v = if s.name.ends_with("frequency") {
                p.get(index) * 2f64.powf(px / 60.0 * k)
            } else {
                p.get(index) + px / px_full as f64 * (s.max - s.min) * k
            };
            p.set(index, v.clamp(s.min, s.max));
        }
    }
}

/// Caixa de valor (arrastável).
fn value_box(ui: &mut Ui, p: &mut dyn ParamAccess, index: usize, rect: Rect) {
    let resp = ui.interact(rect, egui::Id::new(("vbox", index)), Sense::click_and_drag());
    drag_param(ui, p, index, &resp, 240.0);
    let fill = if resp.hovered() || resp.dragged() { pal::FIELD_HOVER } else { pal::FIELD };
    let painter = ui.painter();
    painter.rect_filled(rect, CornerRadius::same(4), fill);
    if resp.dragged() {
        painter.rect_stroke(rect, CornerRadius::same(4), Stroke::new(1.0_f32, pal::ORANGE), StrokeKind::Inside);
    }
    painter.text(rect.center(), Align2::CENTER_CENTER, fmt_val(index, p.get(index)), reg(13.0), pal::TEXT);
    resp.on_hover_text(spec(index).name);
}

/// Knob rotativo com arco laranja; rótulo acima e caixa de valor abaixo.
fn knob(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, index: usize, center: Pos2, r: f32, label: &str, label_dy: f32) {
    let s = spec(index);
    let painter = ui.painter().clone();
    painter.text(Pos2::new(center.x, center.y - r - 14.0 - label_dy), Align2::CENTER_CENTER, label, reg(15.0), pal::TEXT);

    let rect = Rect::from_center_size(center, Vec2::splat(r * 2.0 + 10.0));
    let resp = ui.interact(rect, egui::Id::new(("knob", index)), Sense::click_and_drag());
    drag_param(ui, p, index, &resp, 260.0);

    let v = p.get(index);
    let t = ((v - s.min) / (s.max - s.min)).clamp(0.0, 1.0) as f32;
    let a0 = std::f32::consts::PI * 0.75;
    let sweep = std::f32::consts::PI * 1.5;
    let arc = |from: f32, to: f32, rad: f32| -> Vec<Pos2> {
        let n = 48;
        (0..=n)
            .map(|i| {
                let ang = from + (to - from) * i as f32 / n as f32;
                center + Vec2::new(ang.cos(), ang.sin()) * rad
            })
            .collect()
    };
    // Sombra (PNG recuperado), tingida de preto, por baixo de tudo.
    if let Some(sh) = &a.knob_shadow {
        let rr = Rect::from_center_size(center + Vec2::new(0.0, r * 0.08), Vec2::splat(r * 2.3));
        painter.image(sh.id(), rr, Rect::from_min_max(Pos2::ZERO, Pos2::new(1.0, 1.0)), Color32::from_black_alpha(170));
    }
    let ring = r + 4.0;
    let w = (r * 0.12).clamp(3.0, 7.0);
    painter.add(Shape::line(arc(a0, a0 + sweep, ring), Stroke::new(w, pal::TRACK)));
    painter.add(Shape::line(arc(a0, a0 + sweep * t, ring), Stroke::new(w, pal::ORANGE)));

    painter.circle_filled(center, r, pal::KNOB);
    // Face: textura PNG recuperada (gradiente escuro) mapeada num disco.
    if let Some(face) = &a.knob_face {
        let mut m = Mesh::with_texture(face.id());
        let n = 64u32;
        m.vertices.push(egui::epaint::Vertex { pos: center, uv: Pos2::new(0.5, 0.5), color: Color32::from_white_alpha(255) });
        for i in 0..=n {
            let ang = i as f32 / n as f32 * std::f32::consts::TAU;
            let d = Vec2::new(ang.cos(), ang.sin());
            m.vertices.push(egui::epaint::Vertex {
                pos: center + d * (r - 1.0),
                uv: Pos2::new(0.5 + d.x * 0.5, 0.5 + d.y * 0.5),
                color: Color32::WHITE,
            });
        }
        for i in 1..=n {
            m.add_triangle(0, i, i + 1);
        }
        painter.add(Shape::mesh(m));
    }
    painter.circle_stroke(center, r, Stroke::new(1.0_f32, Color32::from_rgb(0x3a, 0x37, 0x35)));
    let ang = a0 + sweep * t;
    let dir = Vec2::new(ang.cos(), ang.sin());
    painter.line_segment([center + dir * r * 0.45, center + dir * r * 0.85], Stroke::new((r * 0.08).max(2.0), pal::ORANGE_HI));
    if resp.hovered() || resp.dragged() {
        painter.circle_stroke(center, r + 1.0, Stroke::new(1.0_f32, pal::ORANGE_LO));
    }

    let vb = Rect::from_center_size(Pos2::new(center.x, center.y + r + 22.0), Vec2::new(54.0, 22.0));
    value_box(ui, p, index, vb);
}

/// Botão segmentado de dois estados (bool/enum de 2 valores).
fn segmented(ui: &mut Ui, p: &mut dyn ParamAccess, index: usize, rect: Rect, labels: [&str; 2]) {
    let painter = ui.painter().clone();
    painter.rect_filled(rect, CornerRadius::same(11), pal::FIELD);
    let cur = (p.get(index).round() as i32).clamp(0, 1) as usize;
    for (i, lab) in labels.iter().enumerate() {
        let r = Rect::from_min_size(
            Pos2::new(rect.left() + rect.width() * 0.5 * i as f32, rect.top()),
            Vec2::new(rect.width() * 0.5, rect.height()),
        );
        let resp = ui.interact(r, egui::Id::new(("seg", index, i)), Sense::click());
        if resp.clicked() {
            p.set(index, i as f64);
        }
        let on = cur == i;
        if on {
            painter.rect_filled(r.shrink(2.0), CornerRadius::same(9), pal::ORANGE);
        }
        let col = if on { pal::BG } else if resp.hovered() { pal::TEXT } else { pal::DIM };
        painter.text(r.center(), Align2::CENTER_CENTER, *lab, reg(14.0), col);
    }
}

/// Alternador redondo com rótulo (bypass, delta, low latency...).
fn pill_toggle(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, index: usize, rect: Rect, label: &str, glyph: Option<&str>) {
    let resp = ui.interact(rect, egui::Id::new(("pill", index)), Sense::click());
    if resp.clicked() {
        p.set(index, if p.get(index) >= 0.5 { 0.0 } else { 1.0 });
    }
    let on = p.get(index) >= 0.5;
    let painter = ui.painter();
    let fill = if on { pal::ORANGE_LO } else if resp.hovered() { pal::FIELD_HOVER } else { pal::FIELD };
    painter.rect_filled(rect, CornerRadius::same(11), fill);
    let c = Pos2::new(rect.left() + 13.0, rect.center().y);
    match glyph {
        Some(g) => icon(painter, a, g, c, 11.0, if on { pal::ORANGE_HI } else { pal::DIM }),
        None => {
            painter.circle_stroke(c, 5.5, Stroke::new(1.3_f32, if on { pal::ORANGE_HI } else { pal::DIM }));
            if on {
                painter.circle_filled(c, 3.0, pal::ORANGE_HI);
            }
        }
    }
    painter.text(Pos2::new(rect.left() + 24.0, rect.center().y), Align2::LEFT_CENTER, label, reg(14.0), if on { pal::TEXT } else { pal::DIM });
}

/// Botão quadrado com ícone (alternador de parâmetro bool).
fn icon_toggle(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, index: usize, rect: Rect, glyph: &str, h: f32) {
    let resp = ui.interact(rect, egui::Id::new(("itg", index)), Sense::click());
    if resp.clicked() {
        p.set(index, if p.get(index) >= 0.5 { 0.0 } else { 1.0 });
    }
    let on = p.get(index) >= 0.5;
    let painter = ui.painter();
    painter.rect_filled(rect, CornerRadius::same(6), if on { pal::ORANGE_LO } else if resp.hovered() { pal::FIELD_HOVER } else { pal::FIELD });
    icon(painter, a, glyph, rect.center(), h, if on { pal::ORANGE_HI } else { pal::DIM });
    resp.on_hover_text(spec(index).name);
}

// ---------------------------------------------------------------------------
// Bandas e gráfico
// ---------------------------------------------------------------------------

const BAND_BASE: usize = 19;
const BAND_STRIDE: usize = 9;
const NUM_BANDS: usize = 8;
const F_MIN: f64 = 20.0;
const F_MAX: f64 = 20000.0;
const D_RANGE: f64 = 10.0;

fn band_id(band: usize, field: usize) -> usize {
    BAND_BASE + band * BAND_STRIDE + field
}
fn freq_to_t(f: f64) -> f32 {
    ((f.clamp(F_MIN, F_MAX) / F_MIN).ln() / (F_MAX / F_MIN).ln()) as f32
}
fn t_to_freq(t: f32) -> f64 {
    F_MIN * (F_MAX / F_MIN).powf(t.clamp(0.0, 1.0) as f64)
}

/// Curva ILUSTRATIVA de uma banda (unidades de "depth"; cortes caem para -inf).
fn band_shape(shape: i32, f: f64, fc: f64, depth: f64, q: f64, slope: f64) -> f64 {
    let o = (f / fc).log2();
    let bell = (-(o * o) * (q.max(0.1) * 1.6)).exp();
    let s = |x: f64| 1.0 / (1.0 + (-x).exp());
    match shape {
        0 => -40.0 * s(-o * (1.0 + slope) * 2.0) * 1.0, // low cut
        1 => depth * s(-o * 3.0),                        // low shelf
        2 => depth * bell,                               // bell
        3 => depth * bell - depth.abs() * 0.15 * (1.0 - bell),
        4 => -depth.abs() * bell,                        // band reject
        5 => depth * (o / 4.0).clamp(-1.0, 1.0),          // tilt
        6 => depth * s(o * 3.0),                         // high shelf
        7 => -40.0 * s(o * (1.0 + slope) * 2.0),         // high cut
        _ => 0.0,
    }
}

fn band_on(p: &dyn ParamAccess, b: usize) -> bool {
    p.get(band_id(b, 0)) >= 0.5
}
fn is_cut(shape: i32) -> bool {
    shape == 0 || shape == 7
}

fn graph(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, st: &mut UiState, rect: Rect) {
    // Fundo primeiro: o que for registrado depois (faixa, nós, inspetor) fica por cima.
    let bg = ui.interact(rect, egui::Id::new("graph_bg"), Sense::click());
    let painter = ui.painter_at(rect);
    vgrad(&painter, Rect::from_min_max(rect.min, Pos2::new(rect.max.x, rect.top() + rect.height() * 0.42)), pal::PLOT_TOP, pal::PLOT_MID);
    let y0 = rect.top() + rect.height() * 0.42;
    // Região de processamento abaixo da linha de 0 (sem dados do motor: área lisa).
    vgrad(&painter, Rect::from_min_max(Pos2::new(rect.left(), y0), rect.max), pal::FILL_TOP, pal::FILL_BOT);

    for f in [100.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0, 16000.0] {
        let x = rect.left() + freq_to_t(f) * rect.width();
        painter.line_segment([Pos2::new(x, rect.top() + 20.0), Pos2::new(x, rect.bottom())], Stroke::new(1.0_f32, pal::GRID));
        let txt = if f >= 1000.0 { format!("{}k", f / 1000.0) } else { format!("{f}") };
        painter.text(Pos2::new(x, rect.top() + 9.0), Align2::CENTER_CENTER, txt, reg(13.0), pal::DIM);
    }
    // Eixo de redução à direita.
    let below = rect.bottom() - y0;
    for i in 1..=3 {
        let db = st.range_db * i as f32 / 3.0;
        let y = y0 + below * (i as f32 / 3.0) * 0.92;
        painter.line_segment([Pos2::new(rect.left(), y), Pos2::new(rect.right(), y)], Stroke::new(1.0_f32, pal::GRID));
        if i < 3 {
            // a última marca é mostrada pelo próprio seletor de faixa
            painter.text(Pos2::new(rect.right() - 6.0, y - 8.0), Align2::RIGHT_CENTER, format!("-{:.0}", db), reg(12.0), pal::DIM);
        }
    }
    // Seletor da faixa (9/18/30 dB).
    let rr = Rect::from_min_size(Pos2::new(rect.right() - 46.0, rect.bottom() - 28.0), Vec2::new(40.0, 20.0));
    let rresp = ui.interact(rr, egui::Id::new("range"), Sense::click());
    if rresp.clicked() {
        st.range_db = match st.range_db as i32 { 9 => 18.0, 18 => 30.0, _ => 9.0 };
    }
    painter.rect_filled(rr, CornerRadius::same(4), pal::FIELD);
    painter.text(Pos2::new(rr.left() + 14.0, rr.center().y), Align2::CENTER_CENTER, format!("-{:.0}", st.range_db), reg(12.0), pal::TEXT);
    {
        let c = Pos2::new(rr.right() - 10.0, rr.center().y + 1.0);
        painter.add(Shape::convex_polygon(vec![c + Vec2::new(-4.0, -3.0), c + Vec2::new(4.0, -3.0), c + Vec2::new(0.0, 3.0)], pal::DIM, Stroke::NONE));
    }

    // Curva (ilustrativa).
    let px_per_unit = (rect.height() * 0.36) / D_RANGE as f32;
    let n = rect.width() as usize;
    let mut pts = Vec::with_capacity(n + 1);
    for i in 0..=n {
        let t = i as f32 / n as f32;
        let f = t_to_freq(t);
        let mut v = 0.0;
        for b in 0..NUM_BANDS {
            if !band_on(p, b) || p.get(band_id(b, 1)) < 0.5 {
                continue;
            }
            v += band_shape(
                p.get(band_id(b, 8)).round() as i32,
                f,
                p.get(band_id(b, 2)),
                p.get(band_id(b, 3)),
                p.get(band_id(b, 4)),
                p.get(band_id(b, 5)),
            );
        }
        let y = (y0 - v as f32 * px_per_unit).clamp(rect.top() + 20.0, rect.bottom() + 4.0);
        pts.push(Pos2::new(rect.left() + t * rect.width(), y));
    }
    painter.add(Shape::line(pts, Stroke::new(2.0_f32, pal::CURVE)));

    // Nós.
    let to_pos = |p: &dyn ParamAccess, b: usize| {
        let shape = p.get(band_id(b, 8)).round() as i32;
        let x = rect.left() + freq_to_t(p.get(band_id(b, 2))) * rect.width();
        let y = if is_cut(shape) { y0 } else { y0 - p.get(band_id(b, 3)).clamp(-D_RANGE, D_RANGE) as f32 * px_per_unit };
        Pos2::new(x, y)
    };
    let mut over_node = false;
    for b in 0..NUM_BANDS {
        if !band_on(p, b) {
            continue;
        }
        let pos = to_pos(p, b);
        let shape = p.get(band_id(b, 8)).round() as i32;
        let hit = Rect::from_center_size(pos, Vec2::new(22.0, 28.0));
        let resp = ui.interact(hit, egui::Id::new(("node", b)), Sense::click_and_drag());
        if resp.hovered() || resp.dragged() {
            over_node = true;
        }
        if resp.clicked() || resp.drag_started() {
            st.band = Some(b);
        }
        if resp.double_clicked() {
            p.set(band_id(b, 0), 0.0); // remove a banda
            st.band = None;
            continue;
        }
        if resp.dragged() {
            if let Some(ptr) = ui.input(|i| i.pointer.interact_pos()) {
                p.set(band_id(b, 2), t_to_freq((ptr.x - rect.left()) / rect.width()));
                if !is_cut(shape) {
                    let d = ((y0 - ptr.y) / px_per_unit) as f64;
                    p.set(band_id(b, 3), d.clamp(-D_RANGE, D_RANGE));
                }
            }
        }
        if resp.hovered() {
            let sc = ui.input(|i| i.smooth_scroll_delta.y);
            if sc != 0.0 {
                let q = (p.get(band_id(b, 4)) * (1.0 + sc as f64 * 0.004)).clamp(0.1, 10.0);
                p.set(band_id(b, 4), q);
            }
        }
        let enabled = p.get(band_id(b, 1)) >= 0.5;
        let col = if enabled { pal::BAND[b] } else { pal::FAINT };
        let sel = st.band == Some(b);
        if is_cut(shape) {
            let r = Rect::from_center_size(pos, Vec2::new(if sel { 12.0 } else { 10.0 }, 26.0));
            painter.rect_filled(r, CornerRadius::same(5), col);
            painter.rect_stroke(r, CornerRadius::same(5), Stroke::new(1.5_f32, pal::BG), StrokeKind::Outside);
        } else {
            let r = if sel { 8.5 } else { 7.0 };
            painter.circle_filled(pos, r, col);
            painter.circle_stroke(pos, r, Stroke::new(1.5_f32, Color32::WHITE));
        }
        if resp.hovered() || resp.dragged() {
            let f = p.get(band_id(b, 2));
            let txt = format!("{}  {} Hz  {:+.1}", b + 1, if f >= 1000.0 { format!("{:.2}k", f / 1000.0) } else { format!("{:.0}", f) }, p.get(band_id(b, 3)));
            painter.text(pos + Vec2::new(0.0, -22.0), Align2::CENTER_CENTER, txt, reg(12.0), pal::TEXT);
        }
    }

    // Clique duplo no vazio: nova banda (bell) na posição.
    if bg.double_clicked() && !over_node {
        if let (Some(ptr), Some(b)) = (bg.interact_pointer_pos(), (0..NUM_BANDS).find(|&b| !band_on(p, b))) {
            p.set(band_id(b, 0), 1.0);
            p.set(band_id(b, 1), 1.0);
            p.set(band_id(b, 8), 2.0);
            p.set(band_id(b, 2), t_to_freq((ptr.x - rect.left()) / rect.width()));
            p.set(band_id(b, 3), (((y0 - ptr.y) / px_per_unit) as f64).clamp(-D_RANGE, D_RANGE));
            st.band = Some(b);
        }
    } else if bg.clicked() && !over_node {
        st.band = None;
    }

    // Inspetor da banda selecionada.
    if let Some(b) = st.band.filter(|&b| band_on(p, b)) {
        band_inspector(ui, a, p, st, b, Rect::from_min_size(Pos2::new(rect.left() + 10.0, rect.bottom() - 74.0), Vec2::new(560.0, 64.0)));
    }
}

fn band_inspector(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, st: &mut UiState, b: usize, rect: Rect) {
    let painter = ui.painter().clone();
    painter.rect_filled(rect, CornerRadius::same(8), Color32::from_rgba_unmultiplied(0x0b, 0x0b, 0x0d, 235));
    painter.rect_stroke(rect, CornerRadius::same(8), Stroke::new(1.0_f32, pal::BAND[b]), StrokeKind::Inside);
    painter.text(Pos2::new(rect.left() + 12.0, rect.top() + 14.0), Align2::LEFT_CENTER, format!("band {}", b + 1), med(13.0), pal::BAND[b]);
    // Formatos (ícones recuperados).
    let cur = p.get(band_id(b, 8)).round() as i32;
    for s in 0..8 {
        let r = Rect::from_min_size(Pos2::new(rect.left() + 70.0 + s as f32 * 30.0, rect.top() + 4.0), Vec2::new(26.0, 22.0));
        let resp = ui.interact(r, egui::Id::new(("shape", b, s)), Sense::click());
        if resp.clicked() {
            p.set(band_id(b, 8), s as f64);
        }
        let on = cur == s as i32;
        painter.rect_filled(r, CornerRadius::same(4), if on { pal::ORANGE_LO } else if resp.hovered() { pal::FIELD_HOVER } else { pal::FIELD });
        icon(&painter, a, &format!("shape{s}"), r.center(), 12.0, if on { pal::ORANGE_HI } else { pal::DIM });
        resp.on_hover_text(BAND_SHAPE_LABELS[s]);
    }
    // Ativa / remove.
    let er = Rect::from_min_size(Pos2::new(rect.right() - 70.0, rect.top() + 4.0), Vec2::new(26.0, 22.0));
    icon_toggle(ui, a, p, band_id(b, 1), er, "power", 12.0);
    let tr = Rect::from_min_size(Pos2::new(rect.right() - 38.0, rect.top() + 4.0), Vec2::new(26.0, 22.0));
    let tresp = ui.interact(tr, egui::Id::new(("trash", b)), Sense::click());
    painter.rect_filled(tr, CornerRadius::same(4), if tresp.hovered() { pal::FIELD_HOVER } else { pal::FIELD });
    icon(&painter, a, "trash", tr.center(), 12.0, pal::DIM);
    if tresp.clicked() {
        p.set(band_id(b, 0), 0.0);
        st.band = None;
        return;
    }
    // Campos.
    let fields = [(2usize, "freq"), (3, "depth"), (4, "q"), (5, "slope"), (6, "focus")];
    for (k, (f, lab)) in fields.iter().enumerate() {
        let x = rect.left() + 12.0 + k as f32 * 108.0;
        painter.text(Pos2::new(x, rect.top() + 46.0), Align2::LEFT_CENTER, *lab, reg(12.0), pal::DIM);
        value_box(ui, p, band_id(b, *f), Rect::from_min_size(Pos2::new(x + 40.0, rect.top() + 35.0), Vec2::new(60.0, 22.0)));
    }
}

// ---------------------------------------------------------------------------
// Painéis sobrepostos (configurações / sobre)
// ---------------------------------------------------------------------------

fn generic_control(ui: &mut Ui, p: &mut dyn ParamAccess, index: usize) {
    let s = spec(index);
    let cur = p.get(index);
    match s.kind {
        Kind::Bool => {
            let mut b = cur >= 0.5;
            if ui.checkbox(&mut b, s.name).changed() {
                p.set(index, if b { 1.0 } else { 0.0 });
            }
        }
        Kind::Enum(t) => {
            let mut v = cur.round() as i32;
            ui.horizontal(|ui| {
                ui.label(s.name);
                egui::ComboBox::from_id_salt(("enum", index)).selected_text(enum_label(t, v).unwrap_or("?")).show_ui(ui, |ui| {
                    for i in (s.min as i32)..=(s.max as i32) {
                        ui.selectable_value(&mut v, i, enum_label(t, i).unwrap_or("?"));
                    }
                });
            });
            if v != cur.round() as i32 {
                p.set(index, v as f64);
            }
        }
        Kind::Int => {
            let mut v = cur.round() as i32;
            ui.horizontal(|ui| {
                ui.label(s.name);
                ui.add(egui::Slider::new(&mut v, (s.min as i32)..=(s.max as i32)).integer());
            });
            if v != cur.round() as i32 {
                p.set(index, v as f64);
            }
        }
        Kind::Float => {
            let mut v = cur;
            ui.horizontal(|ui| {
                ui.label(s.name);
                ui.add(egui::Slider::new(&mut v, s.min..=s.max).max_decimals(2));
            });
            if (v - cur).abs() > f64::EPSILON {
                p.set(index, v);
            }
        }
    }
}

fn settings_overlay(ctx: &egui::Context, p: &mut dyn ParamAccess, st: &mut UiState) {
    let mut open = true;
    egui::Window::new("settings")
        .open(&mut open)
        .collapsible(false)
        .resizable(false)
        .fixed_size(Vec2::new(860.0, 440.0))
        .anchor(Align2::CENTER_CENTER, Vec2::ZERO)
        .show(ctx, |ui| {
            egui::ScrollArea::vertical().show(ui, |ui| {
                ui.horizontal_top(|ui| {
                    ui.vertical(|ui| {
                        ui.colored_label(pal::ORANGE, "processing");
                        for i in [4usize, 91] {
                            generic_control(ui, p, i);
                        }
                        ui.add_space(8.0);
                        ui.colored_label(pal::ORANGE, "links");
                        for i in [123usize, 124, 125, 126] {
                            generic_control(ui, p, i);
                        }
                    });
                    ui.add_space(16.0);
                    for (name, ids) in [
                        ("L/R", [98usize, 99, 100, 101, 102]),
                        ("center", [103, 104, 105, 106, 107]),
                        ("LFE", [108, 109, 110, 111, 112]),
                    ] {
                        ui.vertical(|ui| {
                            ui.colored_label(pal::ORANGE, name);
                            for i in ids {
                                generic_control(ui, p, i);
                            }
                        });
                    }
                });
                ui.separator();
                ui.horizontal_top(|ui| {
                    for (name, ids) in [("surround", [113usize, 114, 115, 116, 117]), ("ceiling", [118, 119, 120, 121, 122])] {
                        ui.vertical(|ui| {
                            ui.colored_label(pal::ORANGE, name);
                            for i in ids {
                                generic_control(ui, p, i);
                            }
                        });
                    }
                    ui.vertical(|ui| {
                        ui.colored_label(pal::ORANGE, "channels");
                        ui.horizontal_wrapped(|ui| {
                            for i in 127..=142usize {
                                let mut b = p.get(i) >= 0.5;
                                if ui.checkbox(&mut b, format!("{}", i - 126)).changed() {
                                    p.set(i, if b { 1.0 } else { 0.0 });
                                }
                            }
                        });
                    });
                });
                ui.separator();
                ui.colored_label(pal::ORANGE, "bands (channels)");
                ui.horizontal_wrapped(|ui| {
                    for b in 0..NUM_BANDS {
                        generic_control(ui, p, band_id(b, 7));
                    }
                });
            });
        });
    if !open {
        st.overlay = Overlay::None;
    }
}

fn about_overlay(ctx: &egui::Context, info: &UiInfo, st: &mut UiState) {
    let mut open = true;
    egui::Window::new("about")
        .open(&mut open)
        .collapsible(false)
        .resizable(false)
        .anchor(Align2::CENTER_CENTER, Vec2::ZERO)
        .show(ctx, |ui| {
            ui.label(egui::RichText::new("Resonia").font(med(26.0)).color(pal::ORANGE));
            ui.label(format!("version {}", info.version));
            ui.add_space(6.0);
            ui.label(format!("engine: {}", info.engine));
            ui.label(format!("latency: {} samples", info.latency_samples));
            if let Some(sr) = info.sample_rate {
                ui.label(format!("sample rate: {sr} Hz"));
            }
            if let Some(s) = info.status {
                ui.add_space(6.0);
                ui.colored_label(pal::DIM, s);
            }
            ui.add_space(6.0);
            ui.colored_label(pal::DIM, "graph: double-click adds a band, double-click a node removes it, wheel = q, shift = fine.");
        });
    if !open {
        st.overlay = Overlay::None;
    }
}

// ---------------------------------------------------------------------------
// Tela
// ---------------------------------------------------------------------------

/// Desenha a tela inteira.
pub fn draw(ctx: &egui::Context, p: &mut dyn ParamAccess, info: &UiInfo, st: &mut UiState) {
    if st.assets.is_none() {
        st.assets = Some(Assets::load(ctx));
    }
    let assets = st.assets.take().unwrap();
    let a = &assets;

    egui::CentralPanel::default().frame(egui::Frame::NONE.fill(pal::BG)).show(ctx, |ui| {
        let full = ui.max_rect();
        let painter = ui.painter().clone();

        // ---------------- coluna esquerda ----------------
        let left = Rect::from_min_size(full.min, Vec2::new(200.0, full.height()));
        vgrad(&painter, left, pal::PANEL_HI, pal::PANEL);
        painter.text(Pos2::new(left.left() + 22.0, left.top() + 34.0), Align2::LEFT_CENTER, "Resonia", med(36.0), pal::ORANGE);
        painter.text(Pos2::new(left.right() - 26.0, left.top() + 62.0), Align2::RIGHT_CENTER, info.version, reg(13.0), pal::DIM);

        segmented(ui, p, 2, Rect::from_center_size(Pos2::new(left.center().x, left.top() + 100.0), Vec2::new(108.0, 26.0)), ["soft", "hard"]);
        knob(ui, a, p, 0, Pos2::new(left.center().x, left.top() + 210.0), 58.0, "depth", 0.0);
        knob(ui, a, p, 5, Pos2::new(left.center().x, left.top() + 370.0), 30.0, "detail", 0.0);
        let ar_y = left.top() + 520.0;
        // "fast/slow" (SVG recuperado) logo acima de cada knob de tempo.
        for x in [left.left() + 52.0, left.right() - 52.0] {
            icon(&painter, a, "fastslow", Pos2::new(x, ar_y - 31.0), 18.0, pal::DIM);
        }
        knob(ui, a, p, 6, Pos2::new(left.left() + 52.0, ar_y), 24.0, "attack", 14.0);
        knob(ui, a, p, 7, Pos2::new(left.right() - 52.0, ar_y), 24.0, "release", 14.0);

        // ---------------- coluna de controles ----------------
        let mid = Rect::from_min_size(Pos2::new(left.right() + 2.0, full.top()), Vec2::new(100.0, full.height() - 44.0));
        painter.rect_filled(mid, CornerRadius::ZERO, pal::PANEL);
        let cx = mid.center().x;
        icon_toggle(ui, a, p, 14, Rect::from_center_size(Pos2::new(cx - 18.0, mid.top() + 22.0), Vec2::new(32.0, 26.0)), "sc", 11.0);
        icon_toggle(ui, a, p, 15, Rect::from_center_size(Pos2::new(cx + 18.0, mid.top() + 22.0), Vec2::new(32.0, 26.0)), "headphones", 14.0);

        icon(&painter, a, "h_stereo", Pos2::new(cx, mid.top() + 62.0), 11.0, pal::ORANGE);
        segmented(ui, p, 16, Rect::from_center_size(Pos2::new(cx, mid.top() + 88.0), Vec2::new(84.0, 24.0)), ["L/R", "M/S"]);
        painter.text(Pos2::new(cx, mid.top() + 118.0), Align2::CENTER_CENTER, "link", reg(14.0), pal::TEXT);
        value_box(ui, p, 17, Rect::from_center_size(Pos2::new(cx, mid.top() + 140.0), Vec2::new(78.0, 22.0)));
        painter.text(Pos2::new(cx, mid.top() + 170.0), Align2::CENTER_CENTER, "focus", reg(14.0), pal::TEXT);
        // focus: barra deslizante + valor
        {
            let r = Rect::from_center_size(Pos2::new(cx, mid.top() + 190.0), Vec2::new(78.0, 8.0));
            let resp = ui.interact(r.expand2(Vec2::new(0.0, 6.0)), egui::Id::new("focusbar"), Sense::click_and_drag());
            if resp.double_clicked() {
                p.set(18, spec(18).default);
            } else if resp.dragged() || resp.clicked() {
                if let Some(ptr) = resp.interact_pointer_pos() {
                    p.set(18, (((ptr.x - r.left()) / r.width()) as f64).clamp(0.0, 1.0));
                }
            }
            painter.rect_filled(r, CornerRadius::same(4), pal::FIELD);
            let x = r.left() + p.get(18) as f32 * r.width();
            painter.line_segment([Pos2::new(r.center().x, r.top()), Pos2::new(r.center().x, r.bottom())], Stroke::new(1.0_f32, pal::FAINT));
            painter.circle_filled(Pos2::new(x, r.center().y), 6.0, pal::ORANGE);
            value_box(ui, p, 18, Rect::from_center_size(Pos2::new(cx, mid.top() + 214.0), Vec2::new(78.0, 22.0)));
        }

        icon(&painter, a, "h_tilt", Pos2::new(cx, mid.top() + 252.0), 11.0, pal::ORANGE);
        for (k, (lab, lo)) in [("detail", 8usize), ("attack", 10), ("release", 12)].iter().enumerate() {
            let y = mid.top() + 276.0 + k as f32 * 52.0;
            painter.text(Pos2::new(cx, y), Align2::CENTER_CENTER, *lab, reg(14.0), pal::TEXT);
            value_box(ui, p, *lo, Rect::from_center_size(Pos2::new(cx - 20.0, y + 21.0), Vec2::new(38.0, 22.0)));
            value_box(ui, p, *lo + 1, Rect::from_center_size(Pos2::new(cx + 20.0, y + 21.0), Vec2::new(38.0, 22.0)));
        }

        icon(&painter, a, "h_scale", Pos2::new(cx, mid.top() + 440.0), 11.0, pal::ORANGE);
        painter.text(Pos2::new(cx, mid.top() + 462.0), Align2::CENTER_CENTER, "max cut", reg(14.0), pal::TEXT);
        value_box(ui, p, 92, Rect::from_center_size(Pos2::new(cx, mid.top() + 484.0), Vec2::new(78.0, 22.0)));
        painter.text(Pos2::new(cx, mid.top() + 514.0), Align2::CENTER_CENTER, "wet trim", reg(14.0), pal::TEXT);
        value_box(ui, p, 93, Rect::from_center_size(Pos2::new(cx, mid.top() + 536.0), Vec2::new(78.0, 22.0)));

        // ---------------- barra superior ----------------
        let right = Rect::from_min_max(Pos2::new(mid.right() + 2.0, full.top()), full.max);
        let top = Rect::from_min_size(right.min, Vec2::new(right.width(), 44.0));
        painter.rect_filled(top, CornerRadius::ZERO, pal::PANEL);
        let status = Rect::from_min_size(Pos2::new(top.left() + 12.0, top.top() + 8.0), Vec2::new(top.width() - 110.0, 28.0));
        painter.rect_filled(status, CornerRadius::same(6), pal::FIELD);
        painter.circle_filled(Pos2::new(status.left() + 14.0, status.center().y), 4.0, if info.latency_samples > 0 || info.engine.contains("bit") { pal::ORANGE } else { pal::FAINT });
        painter.text(
            Pos2::new(status.left() + 26.0, status.center().y),
            Align2::LEFT_CENTER,
            format!("{}   ·   latency {} samples{}", info.engine, info.latency_samples, info.sample_rate.map(|s| format!("   ·   {s} Hz")).unwrap_or_default()),
            reg(13.0),
            pal::TEXT,
        );
        // Ajuda (sobre) e configurações.
        let hb = Rect::from_center_size(Pos2::new(top.right() - 70.0, top.center().y), Vec2::new(28.0, 28.0));
        let hresp = ui.interact(hb, egui::Id::new("help"), Sense::click());
        painter.rect_filled(hb, CornerRadius::same(14), if hresp.hovered() { pal::FIELD_HOVER } else { pal::FIELD });
        icon(&painter, a, "help", hb.center(), 13.0, pal::TEXT);
        if hresp.clicked() {
            st.overlay = if st.overlay == Overlay::About { Overlay::None } else { Overlay::About };
        }
        let sb = Rect::from_center_size(Pos2::new(top.right() - 34.0, top.center().y), Vec2::new(28.0, 28.0));
        let sresp = ui.interact(sb, egui::Id::new("settings"), Sense::click());
        painter.rect_filled(sb, CornerRadius::same(14), if sresp.hovered() { pal::FIELD_HOVER } else { pal::FIELD });
        // engrenagem desenhada (o ícone de engrenagem não está entre os recursos recuperados)
        for k in 0..8 {
            let ang = k as f32 * std::f32::consts::PI / 4.0;
            let d = Vec2::new(ang.cos(), ang.sin());
            painter.line_segment([sb.center() + d * 5.0, sb.center() + d * 8.5], Stroke::new(2.4_f32, pal::TEXT));
        }
        painter.circle_stroke(sb.center(), 5.0, Stroke::new(2.0_f32, pal::TEXT));
        if sresp.clicked() {
            st.overlay = if st.overlay == Overlay::Settings { Overlay::None } else { Overlay::Settings };
        }

        // ---------------- gráfico ----------------
        let g = Rect::from_min_max(Pos2::new(right.left(), top.bottom()), Pos2::new(right.right(), full.bottom() - 44.0));
        graph(ui, a, p, st, g);

        // ---------------- barra inferior ----------------
        let bot = Rect::from_min_max(Pos2::new(mid.left(), full.bottom() - 44.0), full.max);
        painter.rect_filled(bot, CornerRadius::ZERO, pal::PANEL);
        let by = bot.center().y;
        pill_toggle(ui, a, p, 97, Rect::from_min_size(Pos2::new(bot.left() + 10.0, by - 13.0), Vec2::new(92.0, 26.0)), "bypass", Some("power"));
        pill_toggle(ui, a, p, 96, Rect::from_min_size(Pos2::new(bot.left() + 110.0, by - 13.0), Vec2::new(80.0, 26.0)), "delta", Some("delta"));
        painter.text(Pos2::new(bot.left() + 262.0, by), Align2::RIGHT_CENTER, "mix", reg(14.0), pal::DIM);
        value_box(ui, p, 94, Rect::from_min_size(Pos2::new(bot.left() + 270.0, by - 12.0), Vec2::new(76.0, 24.0)));
        painter.text(Pos2::new(bot.left() + 384.0, by), Align2::RIGHT_CENTER, "out", reg(14.0), pal::DIM);
        value_box(ui, p, 95, Rect::from_min_size(Pos2::new(bot.left() + 392.0, by - 12.0), Vec2::new(76.0, 24.0)));

        // quality
        painter.text(Pos2::new(bot.right() - 300.0, by), Align2::RIGHT_CENTER, "quality", reg(14.0), pal::DIM);
        let qr = Rect::from_min_size(Pos2::new(bot.right() - 292.0, by - 12.0), Vec2::new(116.0, 24.0));
        let mut q = p.get(3).round() as i32;
        let before = q;
        let mut qui = ui.new_child(egui::UiBuilder::new().max_rect(qr));
        egui::ComboBox::from_id_salt("quality")
            .width(110.0)
            .selected_text(QUALITY_LABELS.get(q as usize).copied().unwrap_or("?"))
            .show_ui(&mut qui, |ui| {
                for (i, l) in QUALITY_LABELS.iter().enumerate() {
                    ui.selectable_value(&mut q, i as i32, *l);
                }
            });
        if q != before {
            p.set(3, q as f64);
        }
        pill_toggle(ui, a, p, 1, Rect::from_min_size(Pos2::new(bot.right() - 160.0, by - 13.0), Vec2::new(150.0, 26.0)), "low latency", None);
    });

    match st.overlay {
        Overlay::Settings => settings_overlay(ctx, p, st),
        Overlay::About => about_overlay(ctx, info, st),
        Overlay::None => {}
    }
    st.assets = Some(assets);
}
