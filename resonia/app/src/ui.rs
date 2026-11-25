//! Tela do Resonia, compartilhada pela janela do plugin (lib.rs) e pelo aplicativo (main.rs).
//!
//! NOVA, escrita na fase 2 da recuperação (25/11/2026): layout e textos próprios, nenhum
//! asset de terceiros (nem SVG/PNG/HLSL do editor original, nem as fontes CoFo Sans; só as
//! fontes padrão do egui). Os controles são gerados a partir da tabela de 143 parâmetros
//! (`param_table.rs`). Não há gráfico de espectro nem de redução: isso depende do motor
//! (TODO motor: soultree_port — alimentar um painel de análise com o que o motor expuser).
//!
//! Tamanho da janela: 1050x621 é uma PISTA (docs/engine/recursos-recuperados.md 2.5), não provada.

use crate::param_table::*;
use crate::params::enum_label;
use egui::{Align2, Color32, CornerRadius, FontId, Pos2, Rect, Sense, Stroke, StrokeKind, Ui, Vec2};
use nih_plug_egui::egui;

pub const WIDTH: f32 = 1050.0;
pub const HEIGHT: f32 = 621.0;

const BACK: Color32 = Color32::from_rgb(0x14, 0x15, 0x18);
const PLOT: Color32 = Color32::from_rgb(0x1c, 0x1e, 0x23);
const GRID: Color32 = Color32::from_rgb(0x2c, 0x2f, 0x36);
const LABEL: Color32 = Color32::from_rgb(0x8f, 0x96, 0xa3);
const ACCENT: Color32 = Color32::from_rgb(0x4f, 0xc3, 0xa1);
const WARN: Color32 = Color32::from_rgb(0xf0, 0x8a, 0x3c);
const NODE_OFF: Color32 = Color32::from_rgb(0x55, 0x5a, 0x66);

/// Leitura e escrita de parâmetros em valor simples (unidades da tabela). Cada `set` é um
/// gesto completo para o host (plugin) ou uma simples atribuição (aplicativo).
pub trait ParamAccess {
    fn get(&self, index: usize) -> f64;
    fn set(&mut self, index: usize, value: f64);
}

/// Informações do motor para o cabeçalho.
pub struct UiInfo<'a> {
    /// Texto do estado do motor, por exemplo "nenhum (passa-direto)".
    pub engine: &'a str,
    pub latency_samples: u32,
    pub sample_rate: Option<f32>,
    pub status: Option<&'a str>,
}

#[derive(Clone, Copy, PartialEq, Eq, Default)]
pub enum Tab {
    #[default]
    General,
    Bands,
    Channels,
}

/// Estado só da tela (não vai para o host).
#[derive(Default)]
pub struct UiState {
    pub tab: Tab,
    /// Banda selecionada (0..8).
    pub band: usize,
    /// Banda sendo arrastada no gráfico.
    pub drag: Option<usize>,
}

pub fn setup_style(ctx: &egui::Context) {
    let mut v = egui::Visuals::dark();
    v.panel_fill = BACK;
    v.window_fill = BACK;
    v.extreme_bg_color = PLOT;
    v.override_text_color = Some(Color32::from_rgb(0xdd, 0xe0, 0xe6));
    ctx.set_visuals(v);
}

fn spec(index: usize) -> &'static ParamSpec {
    &PARAMS[index]
}

/// Um controle genérico para o parâmetro `index`, conforme o `Kind` da tabela.
fn control(ui: &mut Ui, p: &mut dyn ParamAccess, index: usize) {
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
            let shown = enum_label(t, v).unwrap_or("?");
            ui.horizontal(|ui| {
                ui.label(s.name);
                egui::ComboBox::from_id_salt(("enum", index)).selected_text(shown).show_ui(ui, |ui| {
                    for i in (s.min as i32)..=(s.max as i32) {
                        let name = enum_label(t, i).unwrap_or("?");
                        ui.selectable_value(&mut v, i, name);
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
            let log = s.name.ends_with("frequency");
            ui.horizontal(|ui| {
                ui.label(s.name);
                // `logarithmic` é só a escolha de arraste da tela (a curva do host é NÃO PROVADA).
                ui.add(egui::Slider::new(&mut v, s.min..=s.max).logarithmic(log).max_decimals(3));
            });
            if (v - cur).abs() > f64::EPSILON {
                p.set(index, v);
            }
        }
    }
}

fn section(ui: &mut Ui, title: &str, ids: &[usize], p: &mut dyn ParamAccess) {
    ui.group(|ui| {
        ui.set_min_width(300.0);
        ui.colored_label(LABEL, title);
        for &i in ids {
            control(ui, p, i);
        }
    });
}

fn general(ui: &mut Ui, p: &mut dyn ParamAccess) {
    ui.horizontal_top(|ui| {
        ui.vertical(|ui| {
            section(ui, "Dynamics", &[0, 5, 6, 7, 92], p);
            section(ui, "Tilt", &[8, 9, 10, 11, 12, 13], p);
        });
        ui.vertical(|ui| {
            section(ui, "Output", &[94, 93, 95, 96, 97], p);
            section(ui, "Processing", &[1, 2, 3, 4], p);
        });
        ui.vertical(|ui| {
            section(ui, "Stereo", &[16, 17, 18], p);
            section(ui, "Sidechain", &[14, 15], p);
            section(ui, "Solo", &[91], p);
        });
    });
}

const BAND_BASE: usize = 19;
const BAND_STRIDE: usize = 9;
const NUM_BANDS: usize = 8;
const F_MIN: f64 = 20.0;
const F_MAX: f64 = 20000.0;
const D_RANGE: f64 = 10.0;

fn band_id(band: usize, field: usize) -> usize {
    BAND_BASE + band * BAND_STRIDE + field
}

fn freq_to_x(f: f64) -> f32 {
    ((f.clamp(F_MIN, F_MAX) / F_MIN).ln() / (F_MAX / F_MIN).ln()) as f32
}

fn x_to_freq(x: f32) -> f64 {
    F_MIN * (F_MAX / F_MIN).powf(x.clamp(0.0, 1.0) as f64)
}

fn bands(ui: &mut Ui, p: &mut dyn ParamAccess, st: &mut UiState) {
    let size = Vec2::new(ui.available_width().min(WIDTH - 40.0), 250.0);
    let (rect, _) = ui.allocate_exact_size(size, Sense::hover());
    let painter = ui.painter_at(rect);
    painter.rect_filled(rect, CornerRadius::same(4), PLOT);
    for f in [50.0, 100.0, 200.0, 500.0, 1000.0, 2000.0, 5000.0, 10000.0] {
        let x = rect.left() + freq_to_x(f) * rect.width();
        painter.line_segment([Pos2::new(x, rect.top()), Pos2::new(x, rect.bottom())], Stroke::new(1.0_f32, GRID));
        let txt = if f >= 1000.0 { format!("{}k", f / 1000.0) } else { format!("{f}") };
        painter.text(Pos2::new(x + 2.0, rect.bottom() - 2.0), Align2::LEFT_BOTTOM, txt, FontId::proportional(10.0), LABEL);
    }
    let y0 = rect.center().y;
    painter.line_segment([Pos2::new(rect.left(), y0), Pos2::new(rect.right(), y0)], Stroke::new(1.0_f32, GRID));

    let to_pos = |freq: f64, depth: f64| {
        Pos2::new(
            rect.left() + freq_to_x(freq) * rect.width(),
            rect.center().y - (depth.clamp(-D_RANGE, D_RANGE) / D_RANGE) as f32 * (rect.height() * 0.5 - 8.0),
        )
    };
    let mut hit: Option<usize> = None;
    for b in 0..NUM_BANDS {
        let on = p.get(band_id(b, 0)) >= 0.5 && p.get(band_id(b, 1)) >= 0.5;
        let pos = to_pos(p.get(band_id(b, 2)), p.get(band_id(b, 3)));
        let sel = st.band == b;
        let color = if on { ACCENT } else { NODE_OFF };
        painter.circle_filled(pos, if sel { 8.0 } else { 6.0 }, color);
        painter.circle_stroke(pos, if sel { 8.0 } else { 6.0 }, Stroke::new(1.0_f32, Color32::BLACK));
        painter.text(pos, Align2::CENTER_CENTER, format!("{}", b + 1), FontId::proportional(9.0), Color32::BLACK);
        let r = ui.interact(Rect::from_center_size(pos, Vec2::splat(18.0)), egui::Id::new(("node", b)), Sense::click_and_drag());
        if r.clicked() || r.drag_started() {
            st.band = b;
        }
        if r.dragged() {
            hit = Some(b);
        }
    }
    if let (Some(b), Some(ptr)) = (hit, ui.input(|i| i.pointer.interact_pos())) {
        let x = (ptr.x - rect.left()) / rect.width();
        let depth = (-(ptr.y - rect.center().y) / (rect.height() * 0.5 - 8.0)) as f64 * D_RANGE;
        p.set(band_id(b, 2), x_to_freq(x));
        p.set(band_id(b, 3), depth.clamp(-D_RANGE, D_RANGE));
    }
    painter.rect_stroke(rect, CornerRadius::same(4), Stroke::new(1.0_f32, GRID), StrokeKind::Inside);

    ui.add_space(6.0);
    ui.horizontal(|ui| {
        for b in 0..NUM_BANDS {
            if ui.selectable_label(st.band == b, format!("Band {}", b + 1)).clicked() {
                st.band = b;
            }
        }
    });
    ui.add_space(4.0);
    let b = st.band.min(NUM_BANDS - 1);
    ui.horizontal_top(|ui| {
        ui.vertical(|ui| {
            for f in [0, 1, 7, 8] {
                control(ui, p, band_id(b, f));
            }
        });
        ui.vertical(|ui| {
            for f in [2, 3, 4, 5, 6] {
                control(ui, p, band_id(b, f));
            }
        });
    });
}

fn channels(ui: &mut Ui, p: &mut dyn ParamAccess) {
    ui.horizontal_top(|ui| {
        for (name, ids) in [
            ("L/R", [98usize, 99, 100, 101, 102]),
            ("Center", [103, 104, 105, 106, 107]),
            ("LFE", [108, 109, 110, 111, 112]),
            ("Surround", [113, 114, 115, 116, 117]),
            ("Ceiling", [118, 119, 120, 121, 122]),
        ] {
            ui.vertical(|ui| section(ui, name, &ids, p));
        }
    });
    ui.horizontal_top(|ui| {
        ui.vertical(|ui| section(ui, "Links", &[123, 124, 125, 126], p));
        ui.vertical(|ui| section(ui, "Channels 1-8", &[127, 128, 129, 130, 131, 132, 133, 134], p));
        ui.vertical(|ui| section(ui, "Channels 9-16", &[135, 136, 137, 138, 139, 140, 141, 142], p));
    });
}

/// Desenha a tela inteira.
pub fn draw(ctx: &egui::Context, p: &mut dyn ParamAccess, info: &UiInfo, st: &mut UiState) {
    egui::CentralPanel::default().show(ctx, |ui| {
        ui.horizontal(|ui| {
            ui.heading("Resonia");
            ui.add_space(16.0);
            ui.colored_label(WARN, format!("engine: {}", info.engine));
            ui.add_space(12.0);
            ui.colored_label(LABEL, format!("latency: {} samples", info.latency_samples));
            if let Some(sr) = info.sample_rate {
                ui.colored_label(LABEL, format!("{} Hz", sr));
            }
        });
        if let Some(s) = info.status {
            ui.colored_label(LABEL, s);
        }
        ui.separator();
        ui.horizontal(|ui| {
            ui.selectable_value(&mut st.tab, Tab::General, "General");
            ui.selectable_value(&mut st.tab, Tab::Bands, "Bands");
            ui.selectable_value(&mut st.tab, Tab::Channels, "Channels");
        });
        ui.add_space(6.0);
        egui::ScrollArea::vertical().auto_shrink([false, false]).show(ui, |ui| match st.tab {
            Tab::General => general(ui, p),
            Tab::Bands => bands(ui, p, st),
            Tab::Channels => channels(ui, p),
        });
    });
}
