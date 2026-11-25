//! Resonia: a dynamic resonance smoother, as a VST3 plugin.

pub mod dsp;
pub mod settings;
pub mod ui;

use dsp::{Analysis, Processor};
use nih_plug::prelude::*;
use nih_plug_egui::{create_egui_editor, EguiState};
use settings::*;
use std::sync::{Arc, Mutex};

#[derive(Params)]
pub struct BandParams {
    #[id = "on"]
    pub enabled: BoolParam,
    #[id = "shape"]
    pub shape: EnumParam<BandShape>,
    #[id = "freq"]
    pub freq: FloatParam,
    #[id = "depth"]
    pub depth: FloatParam,
    #[id = "q"]
    pub q: FloatParam,
}

#[derive(Params)]
pub struct ResoniaParams {
    #[persist = "editor-state"]
    pub editor_state: Arc<EguiState>,
    #[id = "mode"]
    pub mode: EnumParam<Mode>,
    #[id = "depth"]
    pub depth: FloatParam,
    #[id = "detail"]
    pub detail: FloatParam,
    #[id = "attack"]
    pub attack: FloatParam,
    #[id = "release"]
    pub release: FloatParam,
    #[id = "maxcut"]
    pub max_reduction: FloatParam,
    #[id = "dtl_lo"]
    pub detail_lo: FloatParam,
    #[id = "dtl_hi"]
    pub detail_hi: FloatParam,
    #[id = "att_lo"]
    pub attack_lo: FloatParam,
    #[id = "att_hi"]
    pub attack_hi: FloatParam,
    #[id = "rel_lo"]
    pub release_lo: FloatParam,
    #[id = "rel_hi"]
    pub release_hi: FloatParam,
    #[id = "mix"]
    pub mix: FloatParam,
    #[id = "wettrim"]
    pub wet_trim: FloatParam,
    #[id = "output"]
    pub output: FloatParam,
    #[id = "delta"]
    pub delta: BoolParam,
    #[id = "midside"]
    pub mid_side: BoolParam,
    #[id = "link"]
    pub link: FloatParam,
    #[id = "balance"]
    pub balance: FloatParam,
    #[id = "lowlat"]
    pub low_latency: BoolParam,
    #[id = "quality"]
    pub quality: EnumParam<Quality>,
    #[id = "sc"]
    pub sidechain: BoolParam,
    #[id = "sclisten"]
    pub sidechain_listen: BoolParam,
    #[id = "bypass"]
    pub bypass: BoolParam,
    #[id = "range"]
    pub graph_range: FloatParam,
    #[nested(array, group = "Band")]
    pub bands: [BandParams; NUM_BANDS],
}

fn fparam(r: &FRange) -> FloatParam {
    let range = if r.log {
        FloatRange::Skewed { min: r.min, max: r.max, factor: FloatRange::skew_factor(-1.5) }
    } else {
        FloatRange::Linear { min: r.min, max: r.max }
    };
    let rr = *r;
    FloatParam::new(r.name, r.default, range)
        .with_unit(r.unit)
        .with_value_to_string(Arc::new(move |v| format!("{:.*}", rr.decimals, v)))
}

fn tilt(name: &str) -> FloatParam {
    FloatParam::new(name.to_string(), TILT.default, FloatRange::Linear { min: TILT.min, max: TILT.max })
        .with_unit(TILT.unit)
        .with_value_to_string(Arc::new(|v| format!("{:.0}", v)))
}

impl Default for ResoniaParams {
    fn default() -> Self {
        let bands = default_bands();
        Self {
            editor_state: EguiState::from_size(ui::WIDTH as u32, ui::HEIGHT as u32),
            mode: EnumParam::new("Mode", Mode::Soft),
            depth: fparam(&DEPTH),
            detail: fparam(&DETAIL),
            attack: fparam(&ATTACK),
            release: fparam(&RELEASE),
            max_reduction: fparam(&MAX_RED),
            detail_lo: tilt("Detail tilt low"),
            detail_hi: tilt("Detail tilt high"),
            attack_lo: tilt("Attack tilt low"),
            attack_hi: tilt("Attack tilt high"),
            release_lo: tilt("Release tilt low"),
            release_hi: tilt("Release tilt high"),
            mix: fparam(&MIX),
            wet_trim: fparam(&WET_TRIM),
            output: fparam(&OUTPUT),
            delta: BoolParam::new("Delta", false),
            mid_side: BoolParam::new("Mid/Side", false),
            link: fparam(&LINK),
            balance: fparam(&BALANCE),
            low_latency: BoolParam::new("Low latency", false),
            quality: EnumParam::new("Quality", Quality::Normal),
            sidechain: BoolParam::new("Sidechain", false),
            sidechain_listen: BoolParam::new("Sidechain listen", false),
            bypass: BoolParam::new("Bypass", false).make_bypass(),
            graph_range: fparam(&GRAPH_RANGE),
            bands: [0, 1, 2, 3, 4, 5].map(|i| {
                let b = bands[i];
                let n = i + 1;
                BandParams {
                    enabled: BoolParam::new(format!("Band {n} on"), b.enabled),
                    shape: EnumParam::new(format!("Band {n} shape"), b.shape),
                    freq: FloatParam::new(
                        format!("Band {n} frequency"),
                        b.freq,
                        FloatRange::Skewed { min: BAND_FREQ.min, max: BAND_FREQ.max, factor: FloatRange::skew_factor(-2.0) },
                    )
                    .with_unit(" Hz")
                    .with_value_to_string(formatters::v2s_f32_hz_then_khz(2))
                    .with_string_to_value(formatters::s2v_f32_hz_then_khz()),
                    depth: FloatParam::new(format!("Band {n} depth"), b.depth, FloatRange::Linear { min: BAND_DEPTH.min, max: BAND_DEPTH.max })
                        .with_value_to_string(formatters::v2s_f32_rounded(1)),
                    q: FloatParam::new(
                        format!("Band {n} Q"),
                        b.q,
                        FloatRange::Skewed { min: BAND_Q.min, max: BAND_Q.max, factor: FloatRange::skew_factor(-1.0) },
                    )
                    .with_value_to_string(formatters::v2s_f32_rounded(2)),
                }
            }),
        }
    }
}

/// Read every parameter into the plain settings the engine and the screen use.
pub fn settings_from_params(p: &ResoniaParams) -> Settings {
    let mut bands = default_bands();
    for (b, bp) in bands.iter_mut().zip(p.bands.iter()) {
        *b = BandSettings {
            enabled: bp.enabled.value(),
            shape: bp.shape.value(),
            freq: bp.freq.value(),
            depth: bp.depth.value(),
            q: bp.q.value(),
        };
    }
    Settings {
        mode: p.mode.value(),
        depth: p.depth.value(),
        detail: p.detail.value(),
        attack_ms: p.attack.value(),
        release_ms: p.release.value(),
        max_reduction: p.max_reduction.value(),
        detail_lo: p.detail_lo.value(),
        detail_hi: p.detail_hi.value(),
        attack_lo: p.attack_lo.value(),
        attack_hi: p.attack_hi.value(),
        release_lo: p.release_lo.value(),
        release_hi: p.release_hi.value(),
        mix: p.mix.value(),
        wet_trim: p.wet_trim.value(),
        output: p.output.value(),
        delta: p.delta.value(),
        mid_side: p.mid_side.value(),
        link: p.link.value(),
        balance: p.balance.value(),
        low_latency: p.low_latency.value(),
        quality: p.quality.value(),
        sidechain: p.sidechain.value(),
        sidechain_listen: p.sidechain_listen.value(),
        bypass: p.bypass.value(),
        graph_range: p.graph_range.value(),
        bands,
    }
}

macro_rules! sync {
    ($setter:expr, $param:expr, $old:expr, $new:expr) => {
        if $old != $new {
            $setter.begin_set_parameter(&$param);
            $setter.set_parameter(&$param, $new);
            $setter.end_set_parameter(&$param);
        }
    };
}

/// Send what the screen changed back to the host.
fn apply_changes(setter: &ParamSetter, p: &ResoniaParams, o: &Settings, n: &Settings) {
    sync!(setter, p.mode, o.mode, n.mode);
    sync!(setter, p.depth, o.depth, n.depth);
    sync!(setter, p.detail, o.detail, n.detail);
    sync!(setter, p.attack, o.attack_ms, n.attack_ms);
    sync!(setter, p.release, o.release_ms, n.release_ms);
    sync!(setter, p.max_reduction, o.max_reduction, n.max_reduction);
    sync!(setter, p.detail_lo, o.detail_lo, n.detail_lo);
    sync!(setter, p.detail_hi, o.detail_hi, n.detail_hi);
    sync!(setter, p.attack_lo, o.attack_lo, n.attack_lo);
    sync!(setter, p.attack_hi, o.attack_hi, n.attack_hi);
    sync!(setter, p.release_lo, o.release_lo, n.release_lo);
    sync!(setter, p.release_hi, o.release_hi, n.release_hi);
    sync!(setter, p.mix, o.mix, n.mix);
    sync!(setter, p.wet_trim, o.wet_trim, n.wet_trim);
    sync!(setter, p.output, o.output, n.output);
    sync!(setter, p.delta, o.delta, n.delta);
    sync!(setter, p.mid_side, o.mid_side, n.mid_side);
    sync!(setter, p.link, o.link, n.link);
    sync!(setter, p.balance, o.balance, n.balance);
    sync!(setter, p.low_latency, o.low_latency, n.low_latency);
    sync!(setter, p.quality, o.quality, n.quality);
    sync!(setter, p.sidechain, o.sidechain, n.sidechain);
    sync!(setter, p.sidechain_listen, o.sidechain_listen, n.sidechain_listen);
    sync!(setter, p.bypass, o.bypass, n.bypass);
    sync!(setter, p.graph_range, o.graph_range, n.graph_range);
    for ((bp, ob), nb) in p.bands.iter().zip(o.bands.iter()).zip(n.bands.iter()) {
        sync!(setter, bp.enabled, ob.enabled, nb.enabled);
        sync!(setter, bp.shape, ob.shape, nb.shape);
        sync!(setter, bp.freq, ob.freq, nb.freq);
        sync!(setter, bp.depth, ob.depth, nb.depth);
        sync!(setter, bp.q, ob.q, nb.q);
    }
}

pub struct Resonia {
    params: Arc<ResoniaParams>,
    processor: Option<Processor>,
    analysis: Arc<Mutex<Analysis>>,
    latency: usize,
}

impl Default for Resonia {
    fn default() -> Self {
        Self {
            params: Arc::new(ResoniaParams::default()),
            processor: None,
            analysis: Arc::new(Mutex::new(Analysis::default())),
            latency: 0,
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
        let analysis = self.analysis.clone();
        create_egui_editor(
            self.params.editor_state.clone(),
            ui::UiState::default(),
            |ctx, _| ui::setup_style(ctx),
            move |ctx, setter, state| {
                let snapshot = analysis.lock().map(|a| a.clone()).unwrap_or_default();
                let old = settings_from_params(&params);
                let mut new = old.clone();
                ui::draw(ctx, &mut new, &snapshot, state, None, &mut |_| {});
                apply_changes(setter, &params, &old, &new);
                ctx.request_repaint();
            },
        )
    }

    fn initialize(&mut self, _layout: &AudioIOLayout, buffer_config: &BufferConfig, context: &mut impl InitContext<Self>) -> bool {
        let proc = Processor::new(buffer_config.sample_rate);
        let s = settings_from_params(&self.params);
        self.latency = proc.latency_for(&s);
        context.set_latency_samples(self.latency as u32);
        self.processor = Some(proc);
        true
    }

    fn reset(&mut self) {
        if let Some(p) = &mut self.processor {
            p.reset();
        }
    }

    fn process(&mut self, buffer: &mut Buffer, aux: &mut AuxiliaryBuffers, context: &mut impl ProcessContext<Self>) -> ProcessStatus {
        let Some(proc) = &mut self.processor else {
            return ProcessStatus::Normal;
        };
        let s = settings_from_params(&self.params);
        let lat = proc.latency_for(&s);
        if lat != self.latency {
            self.latency = lat;
            context.set_latency_samples(lat as u32);
        }
        let sc = aux.inputs.get_mut(0).map(|b| b.as_slice_immutable());
        proc.process(buffer.as_slice(), sc, &s);
        if let Ok(mut a) = self.analysis.try_lock() {
            proc.copy_analysis(&mut a, &s);
        }
        ProcessStatus::Normal
    }
}

impl Vst3Plugin for Resonia {
    const VST3_CLASS_ID: [u8; 16] = *b"ResoniaSuppress1";
    const VST3_SUBCATEGORIES: &'static [Vst3SubCategory] = &[Vst3SubCategory::Fx, Vst3SubCategory::Eq, Vst3SubCategory::Dynamics];
}

nih_export_vst3!(Resonia);
