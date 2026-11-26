//! Tela do South.air (NDERTAL labs), compartilhada pela janela do plugin (lib.rs) e pelo
//! aplicativo (main.rs).
//!
//! Identidade e layout: `southair/South.air-Redesign-Kit` (referência
//! `assets/reference/southair-ui-reference.png`, tokens `design-system/tokens.css`):
//! - coluna da esquerda: símbolo Fuji, wordmark, versão, soft/hard e os knobs
//!   depth/detail/attack/release;
//! - coluna de controles: stereo (L/R, M/S, link, focus), tilt (detail/attack/release), max cut,
//!   wet trim;
//! - barra superior: sidechain, fones, estado do motor, ajuda e configurações;
//! - gráfico de bandas com nós arrastáveis;
//! - barra inferior: bypass, delta, mix, out, quality e low latency.
//!
//! Redesign só visual: os mesmos parâmetros, os mesmos gestos e a mesma ponte com o motor.
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
// Paleta South.air (tokens do kit: design-system/tokens.css)
// ---------------------------------------------------------------------------
mod pal {
    use super::Color32;
    pub const BG: Color32 = Color32::from_rgb(0x10, 0x0e, 0x0e); // --sa-background
    pub const PANEL: Color32 = Color32::from_rgb(0x14, 0x14, 0x14); // --sa-panel
    pub const PANEL_HI: Color32 = Color32::from_rgb(0x1a, 0x1a, 0x1b); // --sa-surface
    pub const FIELD: Color32 = Color32::from_rgb(0x20, 0x21, 0x23); // --sa-control
    pub const FIELD_HOVER: Color32 = Color32::from_rgb(0x29, 0x2a, 0x2d);
    pub const EDGE: Color32 = Color32::from_rgb(0x2b, 0x2b, 0x2d); // --sa-border
    pub const TEXT: Color32 = Color32::from_rgb(0xe3, 0xe3, 0xe2); // --sa-text-primary
    pub const DIM: Color32 = Color32::from_rgb(0xa1, 0xa1, 0xa2); // --sa-text-secondary
    pub const FAINT: Color32 = Color32::from_rgb(0x68, 0x68, 0x6b); // --sa-text-muted
    pub const ORANGE: Color32 = Color32::from_rgb(0xf3, 0x6d, 0x03); // --sa-orange
    pub const ORANGE_HI: Color32 = Color32::from_rgb(0xfa, 0x86, 0x03); // --sa-orange-active
    pub const ORANGE_LO: Color32 = Color32::from_rgb(0xa5, 0x4d, 0x05); // --sa-orange-deep
    pub const GLOW: Color32 = Color32::from_rgb(0x52, 0x23, 0x04); // --sa-orange-glow
    pub const SOFT: Color32 = Color32::from_rgb(0xfb, 0xa4, 0x5a); // --sa-orange-soft
    pub const PLOT_TOP: Color32 = Color32::from_rgb(0x13, 0x11, 0x11);
    pub const PLOT_MID: Color32 = Color32::from_rgb(0x12, 0x10, 0x10);
    pub const FILL_TOP: Color32 = Color32::from_rgb(0x5c, 0x29, 0x06);
    pub const FILL_BOT: Color32 = Color32::from_rgb(0x16, 0x11, 0x0f);
    pub const GRID: Color32 = Color32::from_rgb(0x29, 0x27, 0x27); // --sa-graph-grid
    pub const CURVE: Color32 = ORANGE;
    pub const KNOB: Color32 = Color32::from_rgb(0x1c, 0x1c, 0x1e);
    pub const TRACK: Color32 = Color32::from_rgb(0x2b, 0x2b, 0x2d);
    /// Cor de cada nó de banda (1..8): família laranja do kit.
    pub const BAND: [Color32; 8] = [ORANGE, ORANGE_HI, SOFT, ORANGE, ORANGE_HI, SOFT, ORANGE, ORANGE_HI];
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

/// Símbolo South.air (Monte Fuji e sol nascente), do kit de redesign; carregado nas cores
/// originais.
const SVG_LOGO: &[u8] = include_bytes!("../../South.air-Redesign-Kit/assets/brand/southair-mark.svg");

struct Assets {
    icons: HashMap<&'static str, TextureHandle>,
    knob_shadow: Option<TextureHandle>,
    knob_face: Option<TextureHandle>,
    logo: Option<TextureHandle>,
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
    raster_svg_data(ctx, name, &whiten_svg(src), scale)
}

/// Filtro trilinear com mipmaps: as texturas (SVG rasterizado em escala alta, PNG) são
/// reduzidas na tela; sem mipmap a GPU pula texels e a borda fica serrilhada.
fn smooth_tex() -> TextureOptions {
    let mut o = TextureOptions::LINEAR;
    o.mipmap_mode = Some(egui::TextureFilter::Linear);
    o
}

fn raster_svg_data(ctx: &egui::Context, name: &str, data: &[u8], scale: f32) -> Option<TextureHandle> {
    use resvg::{tiny_skia, usvg};
    let tree = usvg::Tree::from_data(data, &usvg::Options::default()).ok()?;
    let sz = tree.size();
    let (w, h) = ((sz.width() * scale).ceil() as u32, (sz.height() * scale).ceil() as u32);
    let mut pix = tiny_skia::Pixmap::new(w.max(1), h.max(1))?;
    resvg::render(&tree, tiny_skia::Transform::from_scale(scale, scale), &mut pix.as_mut());
    let img = egui::ColorImage::from_rgba_premultiplied([pix.width() as usize, pix.height() as usize], pix.data());
    Some(ctx.load_texture(format!("svg_{name}"), img, smooth_tex()))
}

fn load_png(ctx: &egui::Context, name: &str, src: &[u8]) -> Option<TextureHandle> {
    let img = image::load_from_memory(src).ok()?.to_rgba8();
    let (w, h) = img.dimensions();
    let ci = egui::ColorImage::from_rgba_unmultiplied([w as usize, h as usize], img.as_raw());
    Some(ctx.load_texture(format!("png_{name}"), ci, smooth_tex()))
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
            logo: raster_svg_data(ctx, "logo", SVG_LOGO, 3.0),
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
    /// Curva de redução enviada pelo motor (só com o editor aberto e o motor ativo).
    pub analysis: Option<crate::engine_bridge::Analysis>,
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
    /// Redução exibida por coluna de pixel (dB, <= 0), suavizada no tempo.
    red: Vec<f32>,
    preset: PresetUi,
}

/// Estado da aba de presets (barra superior).
struct PresetUi {
    /// Preset carregado por último e os valores dele (para o indicador de alterado).
    name: String,
    reference: Vec<(usize, f64)>,
    /// Lista de presets do usuário (lida do disco ao abrir o menu e após salvar/apagar).
    list: Option<Vec<String>>,
    menu: bool,
    /// Caixa de "save as" aberta, com o texto digitado.
    save_as: Option<String>,
    /// "delete" pede um segundo clique antes de apagar o arquivo.
    confirm_delete: bool,
    /// Retângulo da barra (âncora do menu), do último quadro.
    anchor: Rect,
    msg: Option<String>,
}

impl Default for UiState {
    fn default() -> Self {
        UiState {
            band: None,
            overlay: Overlay::None,
            range_db: 9.0,
            assets: None,
            red: Vec::new(),
            preset: PresetUi {
                name: crate::presets::DEFAULT_NAME.to_string(),
                reference: crate::presets::defaults(),
                list: None,
                menu: false,
                save_as: None,
                confirm_delete: false,
                anchor: Rect::NOTHING,
                msg: None,
            },
        }
    }
}

impl UiState {
    /// Só para conferência por screenshot (`RESONIA_SHOT_VIEW` no aplicativo): abre um painel.
    pub fn show_view(&mut self, v: &str) {
        match v {
            "settings" => self.overlay = Overlay::Settings,
            "about" => self.overlay = Overlay::About,
            "presets" => self.preset.menu = true,
            _ => {}
        }
    }

    /// Descarta as texturas carregadas (recarregadas no próximo quadro, no contexto atual).
    pub fn reset_assets(&mut self) {
        self.assets = None;
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
    v.widgets.active.weak_bg_fill = pal::FIELD_HOVER;
    v.widgets.noninteractive.bg_stroke = Stroke::new(1.0_f32, pal::EDGE);
    v.widgets.inactive.bg_stroke = Stroke::new(1.0_f32, pal::EDGE);
    v.widgets.hovered.bg_stroke = Stroke::new(1.0_f32, pal::ORANGE_LO);
    v.widgets.active.bg_stroke = Stroke::new(1.0_f32, pal::ORANGE);
    v.widgets.open.bg_stroke = Stroke::new(1.0_f32, pal::ORANGE_LO);
    v.widgets.open.weak_bg_fill = pal::FIELD;
    for w in [&mut v.widgets.noninteractive, &mut v.widgets.inactive, &mut v.widgets.hovered, &mut v.widgets.active, &mut v.widgets.open] {
        w.corner_radius = CornerRadius::same(8);
    }
    v.window_corner_radius = CornerRadius::same(14);
    v.menu_corner_radius = CornerRadius::same(10);
    v.window_stroke = Stroke::new(1.0_f32, pal::EDGE);
    ctx.set_visuals(v);
}

/// Transição suave (egui anima e repinta sozinho até chegar ao alvo).
fn anim(ui: &Ui, id: impl std::hash::Hash, target: f32, secs: f32) -> f32 {
    ui.ctx().animate_value_with_time(egui::Id::new(("anim", id)), target, secs)
}

fn mix(a: Color32, b: Color32, t: f32) -> Color32 {
    let t = t.clamp(0.0, 1.0);
    let l = |x: u8, y: u8| (x as f32 + (y as f32 - x as f32) * t).round() as u8;
    Color32::from_rgba_unmultiplied(l(a.r(), b.r()), l(a.g(), b.g()), l(a.b(), b.b()), l(a.a(), b.a()))
}

fn med(size: f32) -> FontId {
    FontId::new(size, FontFamily::Name("med".into()))
}
fn reg(size: f32) -> FontId {
    FontId::new(size, FontFamily::Proportional)
}

/// Wordmark `South.air`: "South." em branco gelo e "air" em laranja, inclinado (kit: fonte da
/// marca em itálico; aqui CoFo Sans Medium com a inclinação do egui).
fn wordmark(size: f32) -> egui::text::LayoutJob {
    let mut job = egui::text::LayoutJob::default();
    for (txt, col) in [("South.", pal::TEXT), ("air", pal::ORANGE)] {
        job.append(
            txt,
            0.0,
            egui::TextFormat { font_id: med(size), color: col, italics: true, extra_letter_spacing: -0.5, ..Default::default() },
        );
    }
    job
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
    value_box_ex(ui, p, index, rect, false);
}

/// `accent`: contorno e texto laranja (campo de destaque, como o mix da referência).
fn value_box_ex(ui: &mut Ui, p: &mut dyn ParamAccess, index: usize, rect: Rect, accent: bool) {
    let resp = ui.interact(rect, egui::Id::new(("vbox", index)), Sense::click_and_drag());
    drag_param(ui, p, index, &resp, 240.0);
    let h = anim(ui, ("vbh", index), if resp.hovered() || resp.dragged() { 1.0 } else { 0.0 }, 0.12);
    let d = anim(ui, ("vbd", index), if resp.dragged() { 1.0 } else { 0.0 }, 0.12);
    let painter = ui.painter();
    let cr = CornerRadius::same(8);
    painter.rect_filled(rect, cr, mix(pal::FIELD, pal::FIELD_HOVER, h));
    let edge = if accent { pal::ORANGE } else { mix(pal::EDGE, pal::ORANGE, d) };
    painter.rect_stroke(rect, cr, Stroke::new(1.0_f32, edge), StrokeKind::Inside);
    let col = if accent { pal::ORANGE_HI } else { pal::TEXT };
    painter.text(rect.center(), Align2::CENTER_CENTER, fmt_val(index, p.get(index)), reg(14.0), col);
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
    let t_target = ((v - s.min) / (s.max - s.min)).clamp(0.0, 1.0) as f32;
    // Arraste responde na hora; mudanças vindas de fora (automação, duplo clique) deslizam.
    let t = if resp.dragged() {
        ui.ctx().animate_value_with_time(egui::Id::new(("anim", ("knob", index))), t_target, 0.0)
    } else {
        anim(ui, ("knob", index), t_target, 0.10)
    };
    let a0 = std::f32::consts::PI * 0.75;
    let sweep = std::f32::consts::PI * 1.5;
    let arc = |from: f32, to: f32, rad: f32| -> Vec<Pos2> {
        let n = 96;
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
    let ring = r + 3.0;
    let w = (r * 0.11).clamp(3.5, 7.0);
    painter.add(Shape::line(arc(a0, a0 + sweep, ring), Stroke::new(w, pal::TRACK)));
    painter.add(Shape::line(arc(a0, a0 + sweep * t, ring), Stroke::new(w, pal::ORANGE)));

    painter.circle_filled(center, r, pal::KNOB);
    // Face: textura PNG recuperada (gradiente escuro) mapeada num disco.
    if let Some(face) = &a.knob_face {
        let mut m = Mesh::with_texture(face.id());
        let n = 64u32;
        m.vertices.push(egui::epaint::Vertex { pos: center, uv: Pos2::new(0.5, 0.5), color: Color32::from_gray(95) });
        for i in 0..=n {
            let ang = i as f32 / n as f32 * std::f32::consts::TAU;
            let d = Vec2::new(ang.cos(), ang.sin());
            m.vertices.push(egui::epaint::Vertex {
                pos: center + d * (r - 1.0),
                uv: Pos2::new(0.5 + d.x * 0.5, 0.5 + d.y * 0.5),
                color: Color32::from_gray(95), // face escurecida (kit: knob grafite)
            });
        }
        for i in 1..=n {
            m.add_triangle(0, i, i + 1);
        }
        painter.add(Shape::mesh(m));
    }
    painter.circle_stroke(center, r, Stroke::new(1.0_f32, Color32::from_rgb(0x30, 0x30, 0x33)));
    let ang = a0 + sweep * t;
    let dir = Vec2::new(ang.cos(), ang.sin());
    let ind = Stroke::new((r * 0.06).clamp(2.0, 3.5), pal::ORANGE);
    painter.line_segment([center + dir * r * 0.52, center + dir * r * 0.86], ind);
    let hv = anim(ui, ("knobh", index), if resp.hovered() || resp.dragged() { 1.0 } else { 0.0 }, 0.15);
    if hv > 0.01 {
        painter.circle_stroke(center, r + 1.0, Stroke::new(1.0_f32, mix(Color32::TRANSPARENT, pal::ORANGE_LO, hv)));
    }
    // Valor dentro do knob (referência South.air); o knob inteiro arrasta e o duplo clique volta
    // ao padrão, como antes na caixa de valor.
    let fs = (r * 0.3).clamp(13.0, 19.0);
    painter.text(Pos2::new(center.x, center.y + r * 0.42), Align2::CENTER_CENTER, fmt_val(index, v), reg(fs), pal::TEXT);
    resp.on_hover_text(s.name);
}

/// Botão segmentado de dois estados (bool/enum de 2 valores).
fn segmented(ui: &mut Ui, p: &mut dyn ParamAccess, index: usize, rect: Rect, labels: [&str; 2]) {
    let painter = ui.painter().clone();
    let rad = (rect.height() * 0.5) as u8;
    painter.rect_filled(rect, CornerRadius::same(rad), pal::PANEL_HI);
    painter.rect_stroke(rect, CornerRadius::same(rad), Stroke::new(1.0_f32, pal::EDGE), StrokeKind::Inside);
    let cur = (p.get(index).round() as i32).clamp(0, 1) as usize;
    let pos = anim(ui, ("seg", index), cur as f32, 0.15);
    let hl = Rect::from_min_size(Pos2::new(rect.left() + rect.width() * 0.5 * pos, rect.top()), Vec2::new(rect.width() * 0.5, rect.height()));
    painter.rect_filled(hl.shrink(2.0), CornerRadius::same(rad.saturating_sub(2)), pal::ORANGE);
    for (i, lab) in labels.iter().enumerate() {
        let r = Rect::from_min_size(
            Pos2::new(rect.left() + rect.width() * 0.5 * i as f32, rect.top()),
            Vec2::new(rect.width() * 0.5, rect.height()),
        );
        let resp = ui.interact(r, egui::Id::new(("seg", index, i)), Sense::click());
        if resp.clicked() {
            p.set(index, i as f64);
        }
        let near = 1.0 - (pos - i as f32).abs().min(1.0);
        let hov = anim(ui, ("segh", index, i), if resp.hovered() { 1.0 } else { 0.0 }, 0.12);
        let col = mix(mix(pal::DIM, pal::TEXT, hov), pal::BG, near);
        painter.text(r.center(), Align2::CENTER_CENTER, *lab, if near > 0.5 { med(15.0) } else { reg(15.0) }, col);
    }
}

/// Alternador redondo com rótulo (bypass, delta, low latency...).
fn pill_toggle(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, index: usize, rect: Rect, label: &str, glyph: Option<&str>) {
    let resp = ui.interact(rect, egui::Id::new(("pill", index)), Sense::click());
    if resp.clicked() {
        p.set(index, if p.get(index) >= 0.5 { 0.0 } else { 1.0 });
    }
    let on = anim(ui, ("pill", index), if p.get(index) >= 0.5 { 1.0 } else { 0.0 }, 0.15);
    let hov = anim(ui, ("pillh", index), if resp.hovered() { 1.0 } else { 0.0 }, 0.12);
    let painter = ui.painter();
    // Kit: inativo grafite com borda sutil; ativo laranja com texto escuro.
    let cr = CornerRadius::same(10);
    painter.rect_filled(rect, cr, mix(mix(pal::PANEL_HI, pal::FIELD_HOVER, hov), pal::ORANGE, on));
    painter.rect_stroke(rect, cr, Stroke::new(1.0_f32, mix(pal::EDGE, pal::ORANGE_HI, on)), StrokeKind::Inside);
    let c = Pos2::new(rect.left() + 17.0, rect.center().y);
    let off_glyph = if glyph == Some("power") { pal::ORANGE } else { pal::TEXT };
    let gcol = mix(off_glyph, pal::BG, on);
    match glyph {
        Some(g) => icon(painter, a, g, c, 13.0, gcol),
        None => {
            painter.circle_stroke(c, 7.0, Stroke::new(1.4_f32, gcol));
            if on > 0.01 {
                painter.circle_filled(c, 3.5 * on, pal::BG);
            }
        }
    }
    painter.text(Pos2::new(rect.left() + 31.0, rect.center().y), Align2::LEFT_CENTER, label, reg(15.0), mix(pal::TEXT, pal::BG, on));
}

/// Botão quadrado com ícone (alternador de parâmetro bool).
fn icon_toggle(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, index: usize, rect: Rect, glyph: &str, h: f32) {
    let resp = ui.interact(rect, egui::Id::new(("itg", index)), Sense::click());
    if resp.clicked() {
        p.set(index, if p.get(index) >= 0.5 { 0.0 } else { 1.0 });
    }
    let on = anim(ui, ("itg", index), if p.get(index) >= 0.5 { 1.0 } else { 0.0 }, 0.15);
    let hov = anim(ui, ("itgh", index), if resp.hovered() { 1.0 } else { 0.0 }, 0.12);
    let painter = ui.painter();
    let cr = CornerRadius::same(8);
    painter.rect_filled(rect, cr, mix(mix(pal::FIELD, pal::FIELD_HOVER, hov), pal::ORANGE, on));
    painter.rect_stroke(rect, cr, Stroke::new(1.0_f32, mix(pal::EDGE, pal::ORANGE_HI, on)), StrokeKind::Inside);
    icon(painter, a, glyph, rect.center(), h, mix(pal::DIM, pal::BG, on));
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

fn graph(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, st: &mut UiState, info: &UiInfo, rect: Rect) {
    // Fundo primeiro: o que for registrado depois (faixa, nós, inspetor) fica por cima.
    let bg = ui.interact(rect, egui::Id::new("graph_bg"), Sense::click());
    let painter = ui.painter_at(rect);
    vgrad(&painter, Rect::from_min_max(rect.min, Pos2::new(rect.max.x, rect.top() + rect.height() * 0.42)), pal::PLOT_TOP, pal::PLOT_MID);
    let y0 = rect.top() + rect.height() * 0.42;
    reduction_fill(&painter, st, info, rect, y0);

    // Faixa dos rótulos de frequência acima da área do gráfico (referência South.air).
    painter.rect_filled(Rect::from_min_max(rect.min, Pos2::new(rect.max.x, rect.top() + 26.0)), CornerRadius::ZERO, pal::BG);
    for f in [100.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0, 16000.0] {
        let x = rect.left() + freq_to_t(f) * rect.width();
        painter.line_segment([Pos2::new(x, rect.top() + 26.0), Pos2::new(x, rect.bottom())], Stroke::new(1.0_f32, pal::GRID));
        let txt = if f >= 1000.0 { format!("{}k", f / 1000.0) } else { format!("{f}") };
        painter.text(Pos2::new(x, rect.top() + 13.0), Align2::CENTER_CENTER, txt, reg(14.0), pal::TEXT);
    }
    painter.line_segment([Pos2::new(rect.left(), rect.top() + 26.0), Pos2::new(rect.right(), rect.top() + 26.0)], Stroke::new(1.0_f32, pal::EDGE));
    {
        let ym = (rect.top() + 26.0 + y0) * 0.5;
        painter.line_segment([Pos2::new(rect.left(), ym), Pos2::new(rect.right(), ym)], Stroke::new(1.0_f32, pal::GRID));
    }
    // Eixo de redução à direita.
    let below = rect.bottom() - y0;
    for i in 1..=3 {
        let db = st.range_db * i as f32 / 3.0;
        let y = y0 + below * (i as f32 / 3.0) * 0.92;
        painter.line_segment([Pos2::new(rect.left(), y), Pos2::new(rect.right(), y)], Stroke::new(1.0_f32, pal::GRID));
        if i < 3 {
            // a última marca é mostrada pelo próprio seletor de faixa
            painter.text(Pos2::new(rect.right() - 8.0, y - 10.0), Align2::RIGHT_CENTER, format!("-{:.0}", db), reg(13.0), pal::DIM);
        }
    }
    // Seletor da faixa (9/18/30 dB).
    let rr = Rect::from_min_size(Pos2::new(rect.right() - 50.0, rect.bottom() - 30.0), Vec2::new(44.0, 22.0));
    let rresp = ui.interact(rr, egui::Id::new("range"), Sense::click());
    if rresp.clicked() {
        st.range_db = match st.range_db as i32 { 9 => 18.0, 18 => 30.0, _ => 9.0 };
    }
    let rh = anim(ui, "rangeh", if rresp.hovered() { 1.0 } else { 0.0 }, 0.12);
    painter.rect_filled(rr, CornerRadius::same(6), mix(pal::PANEL_HI, pal::FIELD_HOVER, rh));
    painter.rect_stroke(rr, CornerRadius::same(6), Stroke::new(1.0_f32, pal::EDGE), StrokeKind::Inside);
    painter.text(Pos2::new(rr.left() + 16.0, rr.center().y), Align2::CENTER_CENTER, format!("-{:.0}", st.range_db), reg(13.0), pal::TEXT);
    {
        let c = Pos2::new(rr.right() - 10.0, rr.center().y + 1.0);
        painter.add(Shape::convex_polygon(vec![c + Vec2::new(-4.0, -3.0), c + Vec2::new(4.0, -3.0), c + Vec2::new(0.0, 3.0)], pal::TEXT, Stroke::NONE));
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
        let y = (y0 - v as f32 * px_per_unit).clamp(rect.top() + 26.0, rect.bottom() + 4.0);
        pts.push(Pos2::new(rect.left() + t * rect.width(), y));
    }
    painter.add(Shape::line(pts, Stroke::new(2.5_f32, pal::CURVE)));

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
        let grow = anim(ui, ("node", b), if sel || resp.hovered() || resp.dragged() { 1.0 } else { 0.0 }, 0.12);
        if is_cut(shape) {
            let r = Rect::from_center_size(pos, Vec2::new(10.0 + 2.0 * grow, 24.0 + 2.0 * grow));
            painter.rect_filled(r, CornerRadius::same(5), col);
            painter.rect_stroke(r, CornerRadius::same(5), Stroke::new(1.5_f32, pal::BG), StrokeKind::Outside);
        } else {
            let r = 7.5 + 1.8 * grow;
            if grow > 0.01 {
                painter.circle_filled(pos, r + 5.0 * grow, mix(Color32::TRANSPARENT, Color32::from_rgba_unmultiplied(0xf3, 0x6d, 0x03, 40), grow));
            }
            painter.circle_filled(pos, r, col);
            painter.circle_stroke(pos, r, Stroke::new(2.0_f32, Color32::from_rgb(0xfb, 0xe9, 0xdc)));
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

/// Interpolação linear de `ys` (um canal) nas frequências `xs` (espaçamento uniforme).
fn interp(xs: &[f32], ys: &[f32], f: f32) -> f32 {
    if xs.len() < 2 || ys.len() < xs.len() {
        return 1.0;
    }
    let n = xs.len();
    let step = xs[1] - xs[0];
    if step <= 0.0 {
        return 1.0;
    }
    let pos = ((f - xs[0]) / step).clamp(0.0, (n - 1) as f32);
    let i0 = pos.floor() as usize;
    let i1 = (i0 + 1).min(n - 1);
    let fr = pos - i0 as f32;
    ys[i0] + (ys[i1] - ys[i0]) * fr
}

/// Área de redução, como o `reductionCurveFragmentShader` recuperado: curva interpolada
/// linearmente, preenchida abaixo com gradiente vertical topo->base. Dados: ganhos que o motor
/// envia (estágios lo e hi em série; canal com mais redução). Sem dados: área lisa em 0 dB.
fn reduction_fill(painter: &egui::Painter, st: &mut UiState, info: &UiInfo, rect: Rect, y0: f32) {
    let cols = rect.width().max(1.0) as usize;
    if st.red.len() != cols + 1 {
        st.red = vec![0.0; cols + 1];
    }
    if let Some(an) = &info.analysis {
        let (nl, nh) = (an.freq_lo.len(), an.freq_hi.len());
        let chans_lo = if nl > 0 { an.mag_lo.len() / nl } else { 0 };
        let chans_hi = if nh > 0 { an.mag_hi.len() / nh } else { 0 };
        for i in 0..=cols {
            let f = t_to_freq(i as f32 / cols as f32) as f32;
            let mut g = 1.0f32;
            for ch in 0..chans_lo.max(chans_hi).max(1) {
                let lo = if ch < chans_lo { interp(&an.freq_lo, &an.mag_lo[ch * nl..(ch + 1) * nl], f) } else { 1.0 };
                let hi = if ch < chans_hi { interp(&an.freq_hi, &an.mag_hi[ch * nh..(ch + 1) * nh], f) } else { 1.0 };
                g = g.min(lo * hi);
            }
            let db = 20.0 * g.max(1e-6).log10();
            let old = st.red[i];
            // queda rápida, retorno mais lento (só exibição)
            let k = if db < old { 0.55 } else { 0.18 };
            st.red[i] = old + (db.min(0.0) - old) * k;
        }
    } else {
        st.red.iter_mut().for_each(|v| *v *= 0.8);
    }
    let below = (rect.bottom() - y0) * 0.92;
    let colr = |y: f32| mix(pal::FILL_TOP, pal::FILL_BOT, (y - y0) / (rect.bottom() - y0));
    let mut m = Mesh::default();
    let mut edge = Vec::with_capacity(cols + 1);
    for i in 0..=cols {
        let x = rect.left() + i as f32 / cols as f32 * rect.width();
        let y = (y0 + (-st.red[i] / st.range_db) * below).clamp(y0, rect.bottom());
        edge.push(Pos2::new(x, y));
        m.colored_vertex(Pos2::new(x, y), colr(y));
        m.colored_vertex(Pos2::new(x, rect.bottom()), pal::FILL_BOT);
        if i > 0 {
            let b = (2 * i) as u32;
            m.add_triangle(b - 2, b - 1, b);
            m.add_triangle(b - 1, b + 1, b);
        }
    }
    painter.add(Shape::mesh(m));
    // Contorno discreto da redução, para a variação ficar legível sob a curva laranja.
    painter.add(Shape::line(edge, Stroke::new(1.2_f32, Color32::from_rgba_unmultiplied(0xfb, 0xa4, 0x5a, 110))));
}

fn band_inspector(ui: &mut Ui, a: &Assets, p: &mut dyn ParamAccess, st: &mut UiState, b: usize, rect: Rect) {
    let painter = ui.painter().clone();
    painter.rect_filled(rect, CornerRadius::same(10), Color32::from_rgba_unmultiplied(0x14, 0x14, 0x14, 240));
    painter.rect_stroke(rect, CornerRadius::same(10), Stroke::new(1.0_f32, pal::EDGE), StrokeKind::Inside);
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
        painter.rect_filled(r, CornerRadius::same(6), if on { pal::ORANGE } else if resp.hovered() { pal::FIELD_HOVER } else { pal::FIELD });
        icon(&painter, a, &format!("shape{s}"), r.center(), 12.0, if on { pal::BG } else { pal::DIM });
        resp.on_hover_text(BAND_SHAPE_LABELS[s]);
    }
    // Ativa / remove.
    let er = Rect::from_min_size(Pos2::new(rect.right() - 70.0, rect.top() + 4.0), Vec2::new(26.0, 22.0));
    icon_toggle(ui, a, p, band_id(b, 1), er, "power", 12.0);
    let tr = Rect::from_min_size(Pos2::new(rect.right() - 38.0, rect.top() + 4.0), Vec2::new(26.0, 22.0));
    let tresp = ui.interact(tr, egui::Id::new(("trash", b)), Sense::click());
    painter.rect_filled(tr, CornerRadius::same(6), if tresp.hovered() { pal::FIELD_HOVER } else { pal::FIELD });
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
    // Cabe na janela do plugin (margem de 24 px) e rola nos dois eixos se faltar espaço.
    let screen = ctx.screen_rect();
    let size = Vec2::new((screen.width() - 48.0).min(960.0), screen.height() - 70.0);
    let section = |ui: &mut Ui, title: &str| {
        ui.add_space(6.0);
        ui.label(egui::RichText::new(title).font(med(14.0)).color(pal::ORANGE));
        ui.add_space(2.0);
    };
    let mut open = true;
    egui::Window::new("settings")
        .open(&mut open)
        .collapsible(false)
        .resizable(false)
        .fixed_size(size)
        .anchor(Align2::CENTER_CENTER, Vec2::new(0.0, 10.0))
        .show(ctx, |ui| {
            ui.spacing_mut().slider_width = 110.0;
            ui.spacing_mut().item_spacing.y = 5.0;
            egui::ScrollArea::both().auto_shrink([false, false]).show(ui, |ui| {
                ui.columns(3, |cols| {
                    // 1: processamento, links, canais
                    let c = &mut cols[0];
                    section(c, "processing");
                    for i in [4usize, 91] {
                        generic_control(c, p, i);
                    }
                    section(c, "links");
                    for i in [123usize, 124, 125, 126] {
                        generic_control(c, p, i);
                    }
                    section(c, "channels");
                    egui::Grid::new("chan_grid").spacing(Vec2::new(10.0, 4.0)).show(c, |ui| {
                        for i in 127..=142usize {
                            let mut b = p.get(i) >= 0.5;
                            if ui.checkbox(&mut b, format!("{}", i - 126)).changed() {
                                p.set(i, if b { 1.0 } else { 0.0 });
                            }
                            if (i - 126) % 4 == 0 {
                                ui.end_row();
                            }
                        }
                    });
                    // 2: L/R, center, LFE
                    let c = &mut cols[1];
                    for (name, ids) in [("L/R", [98usize, 99, 100, 101, 102]), ("center", [103, 104, 105, 106, 107]), ("LFE", [108, 109, 110, 111, 112])] {
                        section(c, name);
                        for i in ids {
                            generic_control(c, p, i);
                        }
                    }
                    // 3: surround, ceiling, canais por banda
                    let c = &mut cols[2];
                    for (name, ids) in [("surround", [113usize, 114, 115, 116, 117]), ("ceiling", [118, 119, 120, 121, 122])] {
                        section(c, name);
                        for i in ids {
                            generic_control(c, p, i);
                        }
                    }
                    section(c, "bands (channels)");
                    for b in 0..NUM_BANDS {
                        generic_control(c, p, band_id(b, 7));
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
            ui.label(wordmark(26.0));
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

// ---------------------------------------------------------------------------
// Presets (barra superior)
// ---------------------------------------------------------------------------

fn preset_modified(p: &dyn ParamAccess, ps: &PresetUi) -> bool {
    ps.reference.iter().any(|&(i, v)| (p.get(i) - v).abs() > 1e-6 * (1.0 + v.abs()))
}

/// Carrega o preset pelos mesmos `set` dos controles (só os valores que mudam).
fn apply_preset(p: &mut dyn ParamAccess, ps: &mut PresetUi, name: &str) {
    match crate::presets::load(name) {
        Some(vals) => {
            for &(i, v) in &vals {
                if (p.get(i) - v).abs() > 1e-9 {
                    p.set(i, v);
                }
            }
            ps.name = name.to_string();
            ps.reference = vals;
            ps.msg = None;
        }
        None => ps.msg = Some(format!("cannot read preset \"{name}\"")),
    }
}

fn save_preset(p: &dyn ParamAccess, ps: &mut PresetUi, name: &str) {
    match crate::presets::save(name, |i| p.get(i)) {
        Ok(()) => {
            ps.name = name.to_string();
            ps.reference = crate::presets::defaults().into_iter().map(|(i, _)| (i, p.get(i))).collect();
            ps.list = None;
            ps.msg = None;
        }
        Err(e) => ps.msg = Some(format!("save failed: {e}")),
    }
}

/// Embutido primeiro, depois os do usuário.
fn preset_names(ps: &mut PresetUi) -> Vec<String> {
    if ps.list.is_none() {
        ps.list = Some(crate::presets::list());
    }
    let mut v = vec![crate::presets::DEFAULT_NAME.to_string()];
    v.extend(ps.list.iter().flatten().cloned());
    v
}

/// Botão pequeno arredondado com realce suave no hover; devolve a resposta.
fn bar_button(ui: &mut Ui, id: &str, r: Rect) -> egui::Response {
    let resp = ui.interact(r, egui::Id::new(("pbtn", id)), Sense::click());
    let h = anim(ui, ("pbtnh", id), if resp.hovered() { 1.0 } else { 0.0 }, 0.12);
    if h > 0.01 {
        ui.painter().rect_filled(r, CornerRadius::same(7), mix(Color32::TRANSPARENT, pal::FIELD_HOVER, h));
    }
    resp
}

fn chevron(painter: &egui::Painter, c: Pos2, left: bool, col: Color32) {
    let s = if left { 1.0 } else { -1.0 };
    let st = Stroke::new(1.8_f32, col);
    painter.line_segment([c + Vec2::new(2.5 * s, -5.0), c + Vec2::new(-2.5 * s, 0.0)], st);
    painter.line_segment([c + Vec2::new(-2.5 * s, 0.0), c + Vec2::new(2.5 * s, 5.0)], st);
}

/// Aba de presets: anterior/próximo, nome (com `*` laranja quando alterado; clique abre a
/// lista) e "save".
fn preset_bar(ui: &mut Ui, _a: &Assets, p: &mut dyn ParamAccess, st: &mut UiState, r: Rect) {
    let ps = &mut st.preset;
    ps.anchor = r;
    let painter = ui.painter().clone();
    let cr = CornerRadius::same((r.height() * 0.5) as u8);
    let menu_t = anim(ui, "pmenu", if ps.menu { 1.0 } else { 0.0 }, 0.15);
    painter.rect_filled(r, cr, pal::PANEL_HI);
    painter.rect_stroke(r, cr, Stroke::new(1.0_f32, mix(pal::EDGE, pal::ORANGE_LO, menu_t)), StrokeKind::Inside);

    // anterior / próximo
    let step = |ps: &mut PresetUi, p: &mut dyn ParamAccess, d: i32| {
        let names = preset_names(ps);
        let cur = names.iter().position(|n| *n == ps.name).map(|i| i as i32).unwrap_or(0);
        let n = names.len() as i32;
        let next = names[((cur + d) % n + n) as usize % n as usize].clone();
        apply_preset(p, ps, &next);
    };
    let pr = Rect::from_center_size(Pos2::new(r.left() + 20.0, r.center().y), Vec2::new(28.0, 24.0));
    let nr = Rect::from_center_size(Pos2::new(r.left() + 50.0, r.center().y), Vec2::new(28.0, 24.0));
    let presp = bar_button(ui, "prev", pr);
    let nresp = bar_button(ui, "next", nr);
    chevron(&painter, pr.center(), true, if presp.hovered() { pal::TEXT } else { pal::DIM });
    chevron(&painter, nr.center(), false, if nresp.hovered() { pal::TEXT } else { pal::DIM });
    if presp.clicked() {
        step(ps, p, -1);
    }
    if nresp.clicked() {
        step(ps, p, 1);
    }
    presp.on_hover_text("previous preset");
    nresp.on_hover_text("next preset");

    // save
    let sr = Rect::from_min_max(Pos2::new(r.right() - 64.0, r.top() + 4.0), Pos2::new(r.right() - 6.0, r.bottom() - 4.0));
    let sresp = bar_button(ui, "save", sr);
    let modified = preset_modified(p, ps);
    painter.text(sr.center(), Align2::CENTER_CENTER, "save", reg(14.0), if sresp.hovered() { pal::TEXT } else if modified { pal::ORANGE_HI } else { pal::DIM });
    if sresp.clicked() {
        if ps.name == crate::presets::DEFAULT_NAME {
            ps.save_as = Some(String::new());
        } else {
            let n = ps.name.clone();
            save_preset(p, ps, &n);
        }
        ps.menu = false;
    }
    sresp.on_hover_text("save preset");

    // nome
    let name_r = Rect::from_min_max(Pos2::new(nr.right() + 6.0, r.top() + 3.0), Pos2::new(sr.left() - 6.0, r.bottom() - 3.0));
    let nresp = ui.interact(name_r, egui::Id::new("preset_name"), Sense::click());
    let h = anim(ui, "pnameh", if nresp.hovered() || ps.menu { 1.0 } else { 0.0 }, 0.12);
    if h > 0.01 {
        painter.rect_filled(name_r, CornerRadius::same(10), mix(Color32::TRANSPARENT, pal::FIELD, h));
    }
    if nresp.clicked() {
        ps.menu = !ps.menu;
        ps.confirm_delete = false;
        ps.list = None;
    }
    let mut job = egui::text::LayoutJob::default();
    let (label, col) = match &ps.msg {
        Some(m) => (m.clone(), pal::ORANGE_HI),
        None => (ps.name.clone(), pal::TEXT),
    };
    job.append(&label, 0.0, egui::TextFormat { font_id: med(15.0), color: col, ..Default::default() });
    if modified && ps.msg.is_none() {
        job.append(" *", 0.0, egui::TextFormat { font_id: med(15.0), color: pal::ORANGE, ..Default::default() });
    }
    let g = painter.layout_job(job);
    let w = g.size().x;
    let tx = name_r.center().x - (w + 16.0) * 0.5;
    painter.galley(Pos2::new(tx, name_r.center().y - g.size().y * 0.5), g, pal::TEXT);
    // seta do menu (gira quando aberto)
    let c = Pos2::new(tx + w + 12.0, name_r.center().y);
    let k = 1.0 - 2.0 * menu_t;
    painter.add(Shape::convex_polygon(
        vec![c + Vec2::new(-4.0, -2.5 * k), c + Vec2::new(4.0, -2.5 * k), c + Vec2::new(0.0, 2.5 * k)],
        if nresp.hovered() || ps.menu { pal::TEXT } else { pal::DIM },
        Stroke::NONE,
    ));
}

/// Menu da lista de presets e caixa "save as".
fn preset_popups(ctx: &egui::Context, p: &mut dyn ParamAccess, st: &mut UiState) {
    let ps = &mut st.preset;
    if ps.menu {
        let names = preset_names(ps);
        let width = 280.0;
        let pos = Pos2::new(ps.anchor.center().x - width * 0.5, ps.anchor.bottom() + 6.0);
        let mut chosen: Option<String> = None;
        let mut action: Option<&str> = None;
        let is_default = ps.name == crate::presets::DEFAULT_NAME;
        let area = egui::Area::new(egui::Id::new("preset_menu")).order(egui::Order::Foreground).fixed_pos(pos).show(ctx, |ui| {
            egui::Frame::NONE
                .fill(pal::PANEL)
                .stroke(Stroke::new(1.0_f32, pal::EDGE))
                .corner_radius(CornerRadius::same(12))
                .inner_margin(egui::Margin::same(6))
                .shadow(egui::epaint::Shadow { offset: [0, 6], blur: 18, spread: 0, color: Color32::from_black_alpha(140) })
                .show(ui, |ui| {
                    ui.set_width(width - 12.0);
                    ui.style_mut().spacing.button_padding = Vec2::new(10.0, 5.0);
                    ui.style_mut().override_font_id = Some(reg(14.0));
                    ui.with_layout(egui::Layout::top_down_justified(egui::Align::LEFT), |ui| {
                        egui::ScrollArea::vertical().max_height(320.0).show(ui, |ui| {
                            for n in &names {
                                if ui.selectable_label(*n == ps.name, n.as_str()).clicked() {
                                    chosen = Some(n.clone());
                                }
                            }
                        });
                        ui.separator();
                        if ui.selectable_label(false, "save as…").clicked() {
                            action = Some("save_as");
                        }
                        let del = if ps.confirm_delete { format!("confirm: delete \"{}\"", ps.name) } else { "delete".to_string() };
                        if ui.add_enabled(!is_default, egui::SelectableLabel::new(false, del)).clicked() {
                            action = Some("delete");
                        }
                        if ui.selectable_label(false, "open presets folder").clicked() {
                            action = Some("folder");
                        }
                    });
                });
        });
        if let Some(n) = chosen {
            apply_preset(p, ps, &n);
            ps.menu = false;
        }
        match action {
            Some("save_as") => {
                ps.save_as = Some(if is_default { String::new() } else { ps.name.clone() });
                ps.menu = false;
            }
            Some("delete") if ps.confirm_delete => {
                let n = ps.name.clone();
                match crate::presets::delete(&n) {
                    Ok(()) => {
                        ps.list = None;
                        // volta ao embutido, sem mexer nos controles: o som atual fica como "alterado"
                        ps.name = crate::presets::DEFAULT_NAME.to_string();
                        ps.reference = crate::presets::defaults();
                    }
                    Err(e) => ps.msg = Some(format!("delete failed: {e}")),
                }
                ps.confirm_delete = false;
                ps.menu = false;
            }
            Some("delete") => ps.confirm_delete = true,
            Some("folder") => {
                if let Some(d) = crate::presets::dir() {
                    let _ = std::fs::create_dir_all(&d);
                    let _ = std::process::Command::new("explorer").arg(&d).spawn();
                }
                ps.menu = false;
            }
            _ => {}
        }
        // Clique fora do menu e da barra fecha.
        let outside = ctx.input(|i| {
            i.pointer.any_pressed() && i.pointer.interact_pos().map_or(false, |q| !area.response.rect.contains(q) && !ps.anchor.contains(q))
        });
        if outside {
            ps.menu = false;
            ps.confirm_delete = false;
        }
    }

    if let Some(mut text) = ps.save_as.take() {
        let mut open = true;
        let mut done: Option<bool> = None;
        egui::Window::new("save preset")
            .open(&mut open)
            .collapsible(false)
            .resizable(false)
            .anchor(Align2::CENTER_TOP, Vec2::new(0.0, 70.0))
            .show(ctx, |ui| {
                let te = ui.add(egui::TextEdit::singleline(&mut text).desired_width(260.0).hint_text("preset name").font(reg(15.0)));
                te.request_focus();
                let enter = ui.input(|i| i.key_pressed(egui::Key::Enter));
                let clean = crate::presets::sanitize(&text);
                if !clean.is_empty() && ps.list.iter().flatten().any(|n| n.eq_ignore_ascii_case(&clean)) {
                    ui.colored_label(pal::ORANGE_HI, "a preset with this name exists: it will be replaced");
                }
                ui.add_space(4.0);
                ui.horizontal(|ui| {
                    if ui.button("save").clicked() || enter {
                        done = Some(true);
                    }
                    if ui.button("cancel").clicked() || ui.input(|i| i.key_pressed(egui::Key::Escape)) {
                        done = Some(false);
                    }
                });
            });
        match done {
            Some(true) => {
                let n = crate::presets::sanitize(&text);
                if n.is_empty() {
                    ps.save_as = Some(text);
                } else {
                    save_preset(&*p, ps, &n);
                }
            }
            Some(false) => {}
            None => {
                if open {
                    ps.save_as = Some(text);
                }
            }
        }
    }
}

/// Desenha a tela inteira.
pub fn draw(ctx: &egui::Context, p: &mut dyn ParamAccess, info: &UiInfo, st: &mut UiState) {
    if st.assets.is_none() {
        st.assets = Some(Assets::load(ctx));
    }
    let assets = st.assets.take().unwrap();
    if info.analysis.is_some() {
        ctx.request_repaint_after(std::time::Duration::from_millis(16));
    }
    let a = &assets;

    egui::CentralPanel::default().frame(egui::Frame::NONE.fill(pal::BG)).show(ctx, |ui| {
        let full = ui.max_rect();
        let painter = ui.painter().clone();

        // Medidas tiradas da referência do kit (1618×972) na escala da janela (×0,66).
        const TOP_H: f32 = 48.0;
        const BOT_H: f32 = 58.0;

        // ---------------- coluna esquerda ----------------
        let left = Rect::from_min_size(full.min, Vec2::new(216.0, full.height()));
        vgrad(&painter, left, pal::PANEL_HI, pal::PANEL);
        painter.line_segment([left.right_top(), left.right_bottom()], Stroke::new(1.0_f32, pal::EDGE));
        let lx = left.center().x;
        // Símbolo (SVG do kit) e wordmark.
        if let Some(t) = &a.logo {
            let w = 150.0;
            let h = w * t.size_vec2().y / t.size_vec2().x.max(1.0);
            let r = Rect::from_min_size(Pos2::new(lx - w * 0.5, left.top() - 6.0), Vec2::new(w, h));
            painter.image(t.id(), r, Rect::from_min_max(Pos2::ZERO, Pos2::new(1.0, 1.0)), Color32::WHITE);
        }
        {
            let g = painter.layout_job(wordmark(34.0));
            let pos = Pos2::new(lx - g.size().x * 0.5, left.top() + 84.0);
            painter.galley(pos, g, pal::TEXT);
        }
        painter.text(Pos2::new(left.right() - 26.0, left.top() + 132.0), Align2::RIGHT_CENTER, format!("v{}", info.version), reg(14.0), pal::DIM);

        segmented(ui, p, 2, Rect::from_center_size(Pos2::new(lx, left.top() + 162.0), Vec2::new(150.0, 26.0)), ["soft", "hard"]);
        knob(ui, a, p, 0, Pos2::new(lx, left.top() + 272.0), 56.0, "depth", 0.0);
        knob(ui, a, p, 5, Pos2::new(lx, left.top() + 404.0), 32.0, "detail", 0.0);
        painter.line_segment(
            [Pos2::new(left.left() + 22.0, left.top() + 458.0), Pos2::new(left.right() - 22.0, left.top() + 458.0)],
            Stroke::new(1.0_f32, pal::EDGE),
        );
        let ar_y = left.top() + 540.0;
        knob(ui, a, p, 6, Pos2::new(left.left() + 60.0, ar_y), 28.0, "attack", 0.0);
        knob(ui, a, p, 7, Pos2::new(left.right() - 60.0, ar_y), 28.0, "release", 0.0);

        // ---------------- coluna de controles ----------------
        let mid = Rect::from_min_max(Pos2::new(left.right() + 1.0, full.top() + TOP_H), Pos2::new(left.right() + 115.0, full.bottom() - BOT_H));
        painter.rect_filled(mid, CornerRadius::ZERO, pal::PANEL);
        painter.line_segment([mid.right_top(), mid.right_bottom()], Stroke::new(1.0_f32, pal::EDGE));
        let cx = mid.center().x;
        let y0 = full.top();
        let label = |y: f32, t: &str| {
            painter.text(Pos2::new(cx, y0 + y), Align2::CENTER_CENTER, t, reg(15.0), pal::TEXT);
        };

        segmented(ui, p, 16, Rect::from_center_size(Pos2::new(cx, y0 + 94.0), Vec2::new(92.0, 26.0)), ["L/R", "M/S"]);
        label(128.0, "link");
        value_box(ui, p, 17, Rect::from_center_size(Pos2::new(cx, y0 + 152.0), Vec2::new(80.0, 24.0)));
        label(188.0, "focus");
        // focus: barra deslizante + valor
        {
            let r = Rect::from_center_size(Pos2::new(cx, y0 + 207.0), Vec2::new(80.0, 6.0));
            let resp = ui.interact(r.expand2(Vec2::new(0.0, 7.0)), egui::Id::new("focusbar"), Sense::click_and_drag());
            if resp.double_clicked() {
                p.set(18, spec(18).default);
            } else if resp.dragged() || resp.clicked() {
                if let Some(ptr) = resp.interact_pointer_pos() {
                    p.set(18, (((ptr.x - r.left()) / r.width()) as f64).clamp(0.0, 1.0));
                }
            }
            let fx = anim(ui, "focusx", p.get(18) as f32, if resp.dragged() { 0.0 } else { 0.10 });
            let x = r.left() + fx * r.width();
            painter.rect_filled(r, CornerRadius::same(3), pal::TRACK);
            // Kit: trilha grafite, progresso e thumb laranja.
            painter.rect_filled(Rect::from_min_max(r.min, Pos2::new(x, r.max.y)), CornerRadius::same(3), pal::ORANGE);
            let fh = anim(ui, "focush", if resp.hovered() || resp.dragged() { 1.0 } else { 0.0 }, 0.12);
            painter.circle_filled(Pos2::new(x, r.center().y), 7.0 + fh, pal::ORANGE_HI);
            value_box(ui, p, 18, Rect::from_center_size(Pos2::new(cx, y0 + 231.0), Vec2::new(80.0, 24.0)));
        }

        for (k, (lab, lo)) in [("detail", 8usize), ("attack", 10), ("release", 12)].iter().enumerate() {
            let y = 268.0 + k as f32 * 52.0;
            label(y, lab);
            value_box(ui, p, *lo, Rect::from_center_size(Pos2::new(cx - 20.0, y0 + y + 24.0), Vec2::new(38.0, 24.0)));
            value_box(ui, p, *lo + 1, Rect::from_center_size(Pos2::new(cx + 20.0, y0 + y + 24.0), Vec2::new(38.0, 24.0)));
        }

        label(436.0, "max cut");
        value_box(ui, p, 92, Rect::from_center_size(Pos2::new(cx, y0 + 460.0), Vec2::new(86.0, 24.0)));
        label(494.0, "wet trim");
        value_box(ui, p, 93, Rect::from_center_size(Pos2::new(cx, y0 + 518.0), Vec2::new(86.0, 24.0)));

        // ---------------- barra superior ----------------
        let right = Rect::from_min_max(Pos2::new(mid.right() + 1.0, full.top()), full.max);
        let top = Rect::from_min_max(Pos2::new(mid.left(), full.top()), Pos2::new(full.right(), full.top() + TOP_H));
        painter.rect_filled(top, CornerRadius::ZERO, pal::BG);
        painter.line_segment([top.left_bottom(), top.right_bottom()], Stroke::new(1.0_f32, pal::EDGE));
        // Sidechain e fones: botões quadrados acima da coluna de controles.
        icon_toggle(ui, a, p, 14, Rect::from_center_size(Pos2::new(cx - 20.0, top.center().y), Vec2::new(32.0, 30.0)), "sc", 11.0);
        icon_toggle(ui, a, p, 15, Rect::from_center_size(Pos2::new(cx + 20.0, top.center().y), Vec2::new(32.0, 30.0)), "headphones", 14.0);
        let status = Rect::from_min_max(Pos2::new(right.left() + 6.0, top.top() + 8.0), Pos2::new(top.right() - 84.0, top.bottom() - 8.0));
        // Aba de presets (o estado do motor e a latência ficam no "?" / about).
        preset_bar(ui, a, p, st, status);
        // Ajuda (sobre) e configurações.
        let round_btn = |ui: &mut Ui, id: &str, c: Pos2| {
            let b = Rect::from_center_size(c, Vec2::splat(30.0));
            let resp = ui.interact(b, egui::Id::new(id), Sense::click());
            let h = anim(ui, ("rbh", id), if resp.hovered() { 1.0 } else { 0.0 }, 0.12);
            painter.circle_filled(b.center(), 15.0, mix(pal::PANEL_HI, pal::FIELD_HOVER, h));
            painter.circle_stroke(b.center(), 15.0, Stroke::new(1.0_f32, mix(pal::EDGE, pal::ORANGE_LO, h)));
            (b, resp)
        };
        let (hb, hresp) = round_btn(ui, "help", Pos2::new(top.right() - 62.0, top.center().y));
        icon(&painter, a, "help", hb.center(), 13.0, pal::TEXT);
        if hresp.clicked() {
            st.overlay = if st.overlay == Overlay::About { Overlay::None } else { Overlay::About };
        }
        let (sb, sresp) = round_btn(ui, "settings", Pos2::new(top.right() - 26.0, top.center().y));
        // engrenagem desenhada (o ícone de engrenagem não está entre os recursos recuperados)
        for k in 0..8 {
            let ang = k as f32 * std::f32::consts::PI / 4.0;
            let d = Vec2::new(ang.cos(), ang.sin());
            painter.line_segment([sb.center() + d * 5.5, sb.center() + d * 8.5], Stroke::new(2.6_f32, pal::TEXT));
        }
        painter.circle_stroke(sb.center(), 5.5, Stroke::new(2.0_f32, pal::TEXT));
        painter.circle_filled(sb.center(), 2.0, pal::TEXT);
        if sresp.clicked() {
            st.overlay = if st.overlay == Overlay::Settings { Overlay::None } else { Overlay::Settings };
        }

        // ---------------- gráfico ----------------
        let g = Rect::from_min_max(Pos2::new(right.left(), top.bottom() + 1.0), Pos2::new(right.right(), full.bottom() - BOT_H));
        graph(ui, a, p, st, info, g);

        // ---------------- barra inferior ----------------
        let bot = Rect::from_min_max(Pos2::new(mid.left(), full.bottom() - BOT_H), full.max);
        painter.rect_filled(bot, CornerRadius::ZERO, pal::PANEL);
        painter.line_segment([bot.left_top(), bot.right_top()], Stroke::new(1.0_f32, pal::EDGE));
        let by = bot.center().y;
        let bx = bot.left();
        let sep = |x: f32| {
            painter.line_segment([Pos2::new(bx + x, by - 16.0), Pos2::new(bx + x, by + 16.0)], Stroke::new(1.0_f32, pal::EDGE));
        };
        pill_toggle(ui, a, p, 97, Rect::from_min_size(Pos2::new(bx + 16.0, by - 15.0), Vec2::new(94.0, 30.0)), "bypass", Some("power"));
        pill_toggle(ui, a, p, 96, Rect::from_min_size(Pos2::new(bx + 120.0, by - 15.0), Vec2::new(80.0, 30.0)), "delta", Some("delta"));
        sep(216.0);
        painter.text(Pos2::new(bx + 262.0, by), Align2::RIGHT_CENTER, "mix", reg(15.0), pal::DIM);
        value_box_ex(ui, p, 94, Rect::from_min_size(Pos2::new(bx + 270.0, by - 15.0), Vec2::new(72.0, 30.0)), true);
        painter.text(Pos2::new(bx + 382.0, by), Align2::RIGHT_CENTER, "out", reg(15.0), pal::DIM);
        value_box(ui, p, 95, Rect::from_min_size(Pos2::new(bx + 390.0, by - 15.0), Vec2::new(72.0, 30.0)));
        sep(480.0);

        // quality
        painter.text(Pos2::new(bx + 545.0, by), Align2::RIGHT_CENTER, "quality", reg(15.0), pal::DIM);
        let qr = Rect::from_min_size(Pos2::new(bx + 553.0, by - 15.0), Vec2::new(116.0, 30.0));
        let mut q = p.get(3).round() as i32;
        let before = q;
        let mut qui = ui.new_child(egui::UiBuilder::new().max_rect(qr));
        qui.spacing_mut().interact_size.y = 30.0;
        qui.spacing_mut().button_padding = Vec2::new(10.0, 6.0);
        qui.style_mut().override_font_id = Some(reg(15.0));
        egui::ComboBox::from_id_salt("quality")
            .width(112.0)
            .selected_text(QUALITY_LABELS.get(q as usize).copied().unwrap_or("?"))
            .show_ui(&mut qui, |ui| {
                for (i, l) in QUALITY_LABELS.iter().enumerate() {
                    ui.selectable_value(&mut q, i as i32, *l);
                }
            });
        if q != before {
            p.set(3, q as f64);
        }
        sep(686.0);
        pill_toggle(ui, a, p, 1, Rect::from_min_size(Pos2::new(bot.right() - 134.0, by - 15.0), Vec2::new(122.0, 30.0)), "low latency", None);
    });

    preset_popups(ctx, p, st);
    match st.overlay {
        Overlay::Settings => settings_overlay(ctx, p, st),
        Overlay::About => about_overlay(ctx, info, st),
        Overlay::None => {}
    }
    st.assets = Some(assets);
}
