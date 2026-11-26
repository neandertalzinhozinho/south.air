//! Fronteira entre o plugin Resonia e o motor de áudio.
//!
//! O plugin (lib.rs) e o aplicativo (main.rs) chamam **só** esta interface no caminho de
//! áudio.
//!
//! # Estado
//!
//! - **Sem `--features motor`**: PASSA-DIRETO, sem DSP (espaço reservado, anunciado na tela).
//! - **Com `--features motor`**: o motor é o código traduzido do dump (crates `lifted` +
//!   `lifted_extra`), rodando num emulador de CPU. A chamada é a provada bit a bit contra o
//!   soothe3 original (`checks/w_cadeia_m6.md` §5); a ponte só usa a API do motor e não mexe na
//!   aritmética dele (submódulo `motor`). O dump é lido **em tempo de execução** de
//!   `RESONIA_DUMP` (padrão `D:\PROJETOS\soultree FORK\dumpsooth\nyx_soothe3_dump.bin`). Sem o
//!   dump, ou se o motor der panic (ex.: caminho AVX-512 não traduzido), o plugin passa direto e
//!   a tela mostra o motivo.
//! - Desempenho: o motor emulado é ~2x mais lento que tempo real; a reprodução ao vivo
//!   engasga, o render/bounce offline funciona.
//!
//! # Latência
//!
//! Esta ponte **não** declara número próprio. `latency_samples()` devolve o que o motor informa
//! por `0x863020(handle)` (2304 a 48 kHz com os defaults; muda com os modos de uso, por isso é
//! relida a cada mudança de parâmetro). Sem motor: 0.
//!
//! # Parâmetros
//!
//! Índices 0..142 = ids da tabela de 143 descritores (`param_table.rs`). `set_param` recebe o
//! valor **simples** (unidades da tabela: dB, Hz, 0/1, inteiro de enum), nunca o normalizado.
//! A ponte converte para o normalizado do motor pelo callback `+0x48` da entrada da tabela do
//! dump (a mesma conversão do `m6_run`).

use crate::param_table::{PARAMS, PARAM_COUNT};
use std::sync::atomic::{AtomicU32, AtomicU8, Ordering};
use std::sync::{Arc, Mutex};

#[cfg(feature = "motor")]
mod motor;

/// Estado do motor, para a tela.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum EngineState {
    /// Compilado sem `--features motor`: passa-direto.
    NoMotorBuild = 0,
    /// Ainda não preparado (`prepare` não rodou).
    NotPrepared = 1,
    /// Motor ativo.
    Running = 2,
    /// Dump não encontrado/ilegível: passa-direto.
    DumpMissing = 3,
    /// `create` falhou ou o motor deu panic: passa-direto.
    Failed = 4,
}

/// Curva de redução enviada pelo motor (iface+0x20; nomes registrados por ele no create:
/// `reduction_curve_freq_points_lo/hi`, `reduction_curve_magnitudes_lo/hi`). Ganhos lineares
/// por canal (`mag_*[ch * n + k]`), nas frequências `freq_*` (Hz). Os dois estágios do motor
/// (FFT 4096 e 512) estão em série: a redução total é o produto.
#[derive(Clone, Default)]
pub struct Analysis {
    pub freq_lo: Vec<f32>,
    pub freq_hi: Vec<f32>,
    pub mag_lo: Vec<f32>,
    pub mag_hi: Vec<f32>,
    /// Incrementado a cada curva nova.
    pub seq: u64,
}

/// Estado do motor visível para a tela (compartilhado com a thread da GUI).
pub struct BridgeStatus {
    state: AtomicU8,
    latency: AtomicU32,
    detail: Mutex<String>,
    /// Editor aberto: o motor envia a curva de redução (iface+0x28 = 1, como o plugin original).
    pub editor_open: std::sync::atomic::AtomicBool,
    analysis: Mutex<Analysis>,
}

impl BridgeStatus {
    fn new() -> Self {
        Self {
            state: AtomicU8::new(0),
            latency: AtomicU32::new(0),
            detail: Mutex::new(String::new()),
            editor_open: std::sync::atomic::AtomicBool::new(false),
            analysis: Mutex::new(Analysis::default()),
        }
    }

    /// Cópia da última curva de redução (vazia sem motor).
    pub fn analysis(&self) -> Option<Analysis> {
        let a = self.analysis.lock().ok()?;
        if a.freq_lo.is_empty() || a.mag_lo.is_empty() {
            return None;
        }
        Some(a.clone())
    }

    /// Chamado pela thread de áudio: nunca bloqueia (pula se a tela estiver lendo).
    #[allow(dead_code)]
    fn publish(&self, f: impl FnOnce(&mut Analysis)) {
        if let Ok(mut a) = self.analysis.try_lock() {
            f(&mut a);
        }
    }

    #[allow(dead_code)]
    fn set(&self, st: EngineState, detail: String) {
        if let Ok(mut d) = self.detail.lock() {
            *d = detail;
        }
        self.state.store(st as u8, Ordering::Release);
    }

    pub fn state(&self) -> EngineState {
        match self.state.load(Ordering::Acquire) {
            0 => EngineState::NoMotorBuild,
            1 => EngineState::NotPrepared,
            2 => EngineState::Running,
            3 => EngineState::DumpMissing,
            _ => EngineState::Failed,
        }
    }

    /// Latência em amostras informada pelo motor.
    pub fn latency(&self) -> u32 {
        self.latency.load(Ordering::Relaxed)
    }

    /// Texto curto do motor para o cabeçalho.
    pub fn engine_text(&self) -> &'static str {
        match self.state() {
            EngineState::NoMotorBuild => "none (pass-through, no DSP)",
            EngineState::NotPrepared => "not prepared (pass-through)",
            EngineState::Running => "engine (translated from binary, bit-exact)",
            EngineState::DumpMissing => "DUMP NOT FOUND - bypass (pass-through)",
            EngineState::Failed => "ENGINE ERROR - bypass (pass-through)",
        }
    }

    /// Aviso/detalhe: desempenho (motor ativo), caminho do dump ou mensagem do erro.
    pub fn detail(&self) -> String {
        match self.state() {
            EngineState::Running => "Null-test vs original: bit-identical (default at 44.1/48/96 kHz; low latency/high/ultra at 48 kHz). Ultra at 96 kHz may not keep up in real time.".to_string(),
            _ => self.detail.lock().map(|d| d.clone()).unwrap_or_default(),
        }
    }
}

/// Quem está processando de fato.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum EngineKind {
    /// Passa-direto: o áudio sai igual ao que entrou. Nenhum DSP.
    PassThrough,
    /// Motor traduzido (`lifted` + `lifted_extra`) ativo.
    Lifted,
}

/// Erros de `prepare`.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum PrepareError {
    /// Taxa de amostragem não finita ou <= 0.
    SampleRate,
    /// Bloco máximo igual a zero.
    BlockSize,
    /// Número de canais igual a zero ou acima de 16 (a tabela tem "Channel 1..16 enabled").
    Channels,
}

impl std::fmt::Display for PrepareError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(match self {
            PrepareError::SampleRate => "invalid sample rate",
            PrepareError::BlockSize => "invalid maximum block size",
            PrepareError::Channels => "invalid channel count (1..=16)",
        })
    }
}

impl std::error::Error for PrepareError {}

#[derive(Clone, Copy, Debug, PartialEq)]
struct Config {
    sample_rate: f32,
    max_block: usize,
    channels: usize,
}

/// Ponte para o motor. Construída uma vez; `prepare` a cada (re)ativação.
pub struct EngineBridge {
    config: Option<Config>,
    params: [f64; PARAM_COUNT],
    kind: EngineKind,
    status: Arc<BridgeStatus>,
    #[cfg(feature = "motor")]
    motor: Option<motor::SendMotor>,
}

impl Default for EngineBridge {
    fn default() -> Self {
        Self::new()
    }
}

impl EngineBridge {
    /// Nasce com os valores da tabela.
    pub fn new() -> Self {
        let mut params = [0.0; PARAM_COUNT];
        for (p, spec) in params.iter_mut().zip(PARAMS.iter()) {
            *p = spec.default;
        }
        let status = Arc::new(BridgeStatus::new());
        #[cfg(feature = "motor")]
        status.set(EngineState::NotPrepared, String::new());
        Self {
            config: None,
            params,
            kind: EngineKind::PassThrough,
            status,
            #[cfg(feature = "motor")]
            motor: None,
        }
    }

    /// Estado compartilhado para a tela.
    pub fn status(&self) -> Arc<BridgeStatus> {
        self.status.clone()
    }

    /// Quem está processando.
    pub fn engine_kind(&self) -> EngineKind {
        self.kind
    }

    /// Configura o motor. Pode alocar e ler o dump (lento: segundos); chamar fora da thread de
    /// áudio. `max_block` é o maior bloco que `process` receberá; `channels` é o nº de canais.
    pub fn prepare(&mut self, sample_rate: f32, max_block: usize, channels: usize) -> Result<(), PrepareError> {
        if !sample_rate.is_finite() || sample_rate <= 0.0 {
            return Err(PrepareError::SampleRate);
        }
        if max_block == 0 {
            return Err(PrepareError::BlockSize);
        }
        if channels == 0 || channels > 16 {
            return Err(PrepareError::Channels);
        }
        self.config = Some(Config { sample_rate, max_block, channels });
        #[cfg(feature = "motor")]
        {
            self.motor = None; // destrói o anterior
            self.kind = EngineKind::PassThrough;
            self.status.latency.store(0, Ordering::Relaxed);
            let params = self.params;
            let r = std::panic::catch_unwind(|| motor::create(sample_rate, max_block, &params));
            match r {
                Ok(Ok(m)) => {
                    self.status.latency.store(m.latency(), Ordering::Relaxed);
                    let (fl, fh) = (m.freq_lo.clone(), m.freq_hi.clone());
                    if let Ok(mut a) = self.status.analysis.lock() {
                        *a = Analysis { freq_lo: fl, freq_hi: fh, ..Default::default() };
                    }
                    self.motor = Some(motor::SendMotor(m));
                    self.kind = EngineKind::Lifted;
                    self.status.set(EngineState::Running, String::new());
                }
                Ok(Err(motor::CreateError::DumpMissing(msg))) => self.status.set(EngineState::DumpMissing, msg),
                Ok(Err(motor::CreateError::Failed(msg))) => self.status.set(EngineState::Failed, msg),
                Err(e) => self.status.set(EngineState::Failed, format!("engine panic in create: {}", motor::panic_text(&e))),
            }
        }
        Ok(())
    }

    /// Taxa de amostragem da última `prepare` bem-sucedida.
    pub fn sample_rate(&self) -> Option<f32> {
        self.config.map(|c| c.sample_rate)
    }

    /// Falha do motor: passa direto até o próximo `prepare`.
    #[cfg(feature = "motor")]
    fn fail(&mut self, what: &str, e: Box<dyn std::any::Any + Send>) {
        if let Some(m) = self.motor.as_mut() {
            m.0.poisoned = true;
        }
        self.motor = None;
        self.kind = EngineKind::PassThrough;
        self.status.latency.store(0, Ordering::Relaxed);
        self.status.set(EngineState::Failed, format!("engine panic in {what}: {}", motor::panic_text(&e)));
    }

    /// Processa um bloco **no lugar**: `main[canal][amostra]`. Todos os canais têm o mesmo
    /// comprimento (<= `max_block`). `sidechain`, se existir, tem a mesma forma e não é alterado.
    ///
    /// Sem motor, ou com o motor em falha: passa-direto, não toca nas amostras. O sidechain é
    /// ignorado (o caminho provado usa `r9 = 0`).
    /// Editor aberto ou fechado (o motor só envia a curva de redução com o editor aberto).
    pub fn set_editor_open(&self, open: bool) {
        self.status.editor_open.store(open, Ordering::Relaxed);
    }

    pub fn process(&mut self, main: &mut [&mut [f32]], sidechain: Option<&[&[f32]]>) {
        let _ = sidechain;
        #[cfg(feature = "motor")]
        if let Some(m) = self.motor.as_mut() {
            let st = &self.status;
            let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| m.0.process(main, st)));
            if let Err(e) = r {
                self.fail("process", e);
            }
        }
        #[cfg(not(feature = "motor"))]
        let _ = main;
    }

    /// Latência atual em amostras, a que o host precisa compensar. 0 em passa-direto.
    /// Com motor: o último valor lido de `0x863020` (relido a cada mudança de parâmetro).
    pub fn latency_samples(&self) -> u32 {
        self.status.latency()
    }

    /// Zera o estado interno (transporte parou/reposicionou). Mantém a configuração e os parâmetros.
    pub fn reset(&mut self) {
        #[cfg(feature = "motor")]
        if let Some(m) = self.motor.as_mut() {
            if let Err(e) = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| m.0.reset())) {
                self.fail("reset", e);
            }
        }
    }

    /// Define o parâmetro `index` (0..=142) em valor simples. O valor é limitado a [min, max]
    /// da tabela; NaN é ignorado. Índice inválido devolve `false`.
    pub fn set_param(&mut self, index: usize, plain: f64) -> bool {
        let Some(spec) = PARAMS.get(index) else {
            return false;
        };
        if plain.is_nan() {
            return false;
        }
        let v = plain.clamp(spec.min, spec.max);
        self.params[index] = v;
        #[cfg(feature = "motor")]
        if let Some(m) = self.motor.as_mut() {
            match std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                m.0.set_param(index, v);
                m.0.latency()
            })) {
                Ok(lat) => self.status.latency.store(lat, Ordering::Relaxed),
                Err(e) => self.fail("set_param", e),
            }
        }
        true
    }

    /// Último valor simples definido para `index`.
    pub fn param(&self, index: usize) -> Option<f64> {
        self.params.get(index).copied()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[cfg(not(feature = "motor"))]
    #[test]
    fn passthrough_is_bit_exact() {
        let mut b = EngineBridge::new();
        b.prepare(48_000.0, 512, 2).unwrap();
        let mut l: Vec<f32> = (0..512).map(|i| ((i * 37) % 101) as f32 * 0.01 - 0.5).collect();
        let mut r: Vec<f32> = l.iter().map(|x| -x * 0.5).collect();
        let (l0, r0) = (l.clone(), r.clone());
        let mut chans: [&mut [f32]; 2] = [&mut l[..], &mut r[..]];
        b.process(&mut chans, None);
        assert_eq!(l.iter().map(|x| x.to_bits()).collect::<Vec<_>>(), l0.iter().map(|x| x.to_bits()).collect::<Vec<_>>());
        assert_eq!(r.iter().map(|x| x.to_bits()).collect::<Vec<_>>(), r0.iter().map(|x| x.to_bits()).collect::<Vec<_>>());
    }

    #[cfg(not(feature = "motor"))]
    #[test]
    fn latency_is_zero_without_engine() {
        let mut b = EngineBridge::new();
        assert_eq!(b.latency_samples(), 0);
        b.prepare(44_100.0, 128, 1).unwrap();
        assert_eq!(b.latency_samples(), 0);
        assert_eq!(b.engine_kind(), EngineKind::PassThrough);
    }

    #[test]
    fn prepare_rejects_bad_arguments() {
        let mut b = EngineBridge::new();
        assert_eq!(b.prepare(0.0, 64, 2), Err(PrepareError::SampleRate));
        assert_eq!(b.prepare(f32::NAN, 64, 2), Err(PrepareError::SampleRate));
        assert_eq!(b.prepare(48_000.0, 0, 2), Err(PrepareError::BlockSize));
        assert_eq!(b.prepare(48_000.0, 64, 0), Err(PrepareError::Channels));
        assert_eq!(b.prepare(48_000.0, 64, 17), Err(PrepareError::Channels));
        assert_eq!(b.sample_rate(), None);
    }

    #[test]
    fn params_start_at_table_defaults_and_clamp() {
        let mut b = EngineBridge::new();
        assert_eq!(b.param(0), Some(5.0)); // Depth
        assert_eq!(b.param(21), Some(100.0)); // Band 1 frequency
        assert_eq!(b.param(143), None);
        assert!(b.set_param(0, 99.0));
        assert_eq!(b.param(0), Some(10.0));
        assert!(b.set_param(22, -99.0)); // Band 1 depth, min -10
        assert_eq!(b.param(22), Some(-10.0));
        assert!(!b.set_param(143, 1.0));
        assert!(!b.set_param(0, f64::NAN));
        assert_eq!(b.param(0), Some(10.0));
    }

    #[test]
    fn reset_keeps_params_and_config() {
        let mut b = EngineBridge::new();
        b.set_param(94, 40.0); // Mix
        b.reset();
        assert_eq!(b.param(94), Some(40.0));
    }
}
