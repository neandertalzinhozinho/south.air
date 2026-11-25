//! Resonia, plugin VST3 (nih-plug).
//!
//! NOVO na fase 2 da recuperação (25/11/2026). O `lib.rs` final do projeto antigo não foi
//! recuperado por inteiro (só a versão da manhã de 21/11, arquivada em
//! `_arquivo_heuristico/recuperados_exatos/lib_fase_manha.rs`), e de qualquer forma ele ligava o
//! DSP heurístico antigo. Este arquivo só repete do antigo o que a versão da manhã mostra
//! (nome, id de classe VST3, subcategorias, layouts com sidechain) e liga o resto à ponte
//! [`engine_bridge`]: **nenhum DSP é chamado daqui**.

pub mod engine_bridge;
pub mod param_table;
pub mod params;
pub mod ui;

use engine_bridge::EngineBridge;
use nih_plug::prelude::*;
use nih_plug_egui::{create_egui_editor, EguiState};
use params::{ResoniaParams, Slot};
use std::num::NonZeroU32;
use std::sync::atomic::{AtomicU32, Ordering};
use std::sync::Arc;

/// Adaptador da tela sobre os parâmetros do host.
struct HostAccess<'a> {
    params: &'a ResoniaParams,
    setter: &'a ParamSetter<'a>,
}

impl ui::ParamAccess for HostAccess<'_> {
    fn get(&self, index: usize) -> f64 {
        self.params.plain(index)
    }
    fn set(&mut self, index: usize, value: f64) {
        self.params.set_with_gesture(self.setter, index, value);
    }
}

pub struct Resonia {
    params: Arc<ResoniaParams>,
    editor_state: Arc<EguiState>,
    bridge: EngineBridge,
    /// Último valor enviado à ponte, por índice (só envia quando muda).
    sent: Vec<f64>,
    /// Latência anunciada ao host (lida pela tela).
    latency: Arc<AtomicU32>,
}

impl Default for Resonia {
    fn default() -> Self {
        Self {
            params: Arc::new(ResoniaParams::default()),
            editor_state: EguiState::from_size(ui::WIDTH as u32, ui::HEIGHT as u32),
            bridge: EngineBridge::new(),
            sent: vec![f64::NAN; param_table::PARAM_COUNT],
            latency: Arc::new(AtomicU32::new(0)),
        }
    }
}

impl Resonia {
    /// Envia à ponte só os parâmetros que mudaram desde o último bloco.
    fn push_params(&mut self) {
        for i in 0..self.params.len() {
            let v = match self.params.slot(i) {
                Some(Slot::Float(p)) => p.value() as f64,
                Some(s) => s.plain(),
                None => continue,
            };
            if self.sent[i] != v {
                self.sent[i] = v;
                self.bridge.set_param(i, v);
            }
        }
    }
}

impl Plugin for Resonia {
    const NAME: &'static str = "Resonia";
    const VENDOR: &'static str = "Resonia";
    const URL: &'static str = "";
    const EMAIL: &'static str = "";
    const VERSION: &'static str = env!("CARGO_PKG_VERSION");

    const AUDIO_IO_LAYOUTS: &'static [AudioIOLayout] = &[
        AudioIOLayout {
            main_input_channels: NonZeroU32::new(2),
            main_output_channels: NonZeroU32::new(2),
            aux_input_ports: &[new_nonzero_u32(2)],
            aux_output_ports: &[],
            names: PortNames {
                layout: Some("Stereo"),
                main_input: None,
                main_output: None,
                aux_inputs: &["Sidechain"],
                aux_outputs: &[],
            },
        },
        AudioIOLayout {
            main_input_channels: NonZeroU32::new(1),
            main_output_channels: NonZeroU32::new(1),
            aux_input_ports: &[new_nonzero_u32(1)],
            aux_output_ports: &[],
            names: PortNames {
                layout: Some("Mono"),
                main_input: None,
                main_output: None,
                aux_inputs: &["Sidechain"],
                aux_outputs: &[],
            },
        },
    ];

    const SAMPLE_ACCURATE_AUTOMATION: bool = false;
    type SysExMessage = ();
    type BackgroundTask = ();

    fn params(&self) -> Arc<dyn Params> {
        self.params.clone()
    }

    fn editor(&mut self, _async_executor: AsyncExecutor<Self>) -> Option<Box<dyn Editor>> {
        let params = self.params.clone();
        let status = self.bridge.status();
        create_egui_editor(
            self.editor_state.clone(),
            ui::UiState::default(),
            |ctx, _| ui::setup_style(ctx),
            move |ctx, setter, state| {
                let detail = status.detail();
                let info = ui::UiInfo {
                    engine: status.engine_text(),
                    latency_samples: status.latency(),
                    sample_rate: None,
                    status: if detail.is_empty() { None } else { Some(detail.as_str()) },
                    version: env!("CARGO_PKG_VERSION"),
                };
                let mut access = HostAccess { params: &params, setter };
                ui::draw(ctx, &mut access, &info, state);
            },
        )
    }

    fn initialize(&mut self, layout: &AudioIOLayout, buffer_config: &BufferConfig, context: &mut impl InitContext<Self>) -> bool {
        let channels = layout.main_input_channels.map_or(2, |c| c.get() as usize);
        if self.bridge.prepare(buffer_config.sample_rate, buffer_config.max_buffer_size as usize, channels).is_err() {
            return false;
        }
        self.sent.iter_mut().for_each(|v| *v = f64::NAN);
        self.push_params();
        let lat = self.bridge.latency_samples();
        self.latency.store(lat, Ordering::Relaxed);
        context.set_latency_samples(lat);
        true
    }

    fn reset(&mut self) {
        self.bridge.reset();
    }

    fn process(&mut self, buffer: &mut Buffer, aux: &mut AuxiliaryBuffers, context: &mut impl ProcessContext<Self>) -> ProcessStatus {
        self.push_params();
        let lat = self.bridge.latency_samples();
        if lat != self.latency.load(Ordering::Relaxed) {
            self.latency.store(lat, Ordering::Relaxed);
            context.set_latency_samples(lat);
        }
        // O sidechain é entregue à ponte sem cópia; hoje ela o ignora (passa-direto).
        let _ = aux;
        self.bridge.process(buffer.as_slice(), None);
        // TODO motor: soultree_port — repassar `aux.inputs` como sidechain quando o motor o definir.
        ProcessStatus::Normal
    }
}

impl Vst3Plugin for Resonia {
    // Mesmo id de classe da versão da manhã (recuperada): 16 bytes ASCII.
    const VST3_CLASS_ID: [u8; 16] = *b"ResoniaSuppress1";
    const VST3_SUBCATEGORIES: &'static [Vst3SubCategory] = &[Vst3SubCategory::Fx, Vst3SubCategory::Eq, Vst3SubCategory::Dynamics];
}

nih_export_vst3!(Resonia);
