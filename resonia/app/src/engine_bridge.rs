//! Fronteira entre o plugin Resonia e o motor de áudio.
//!
//! O plugin (lib.rs) e o aplicativo (main.rs) chamam **só** esta interface no caminho de
//! áudio. O motor de verdade é o port Rust do DSP do soothe3 (`D:\PROJETOS\soultree FORK\port`,
//! crate `soultree_port`), que ainda não tem uma API de processamento de blocos: o `port`
//! fecha M1..M2 e o `pending::first_blocking()` ainda aponta para `0x293760` (ln, M3).
//!
//! # Estado atual: PASSA-DIRETO (bypass), sem DSP
//!
//! `EngineBridge::process` não altera o áudio. Isto **não** é um efeito: é um espaço
//! reservado, e o plugin anuncia isso em `engine_kind()` / na tela. Não há heurística aqui
//! (regra do `LEMBRAR DISSO.md`: o que não foi lido do dump não entra).
//!
//! Onde o motor entra: ver as marcas `// TODO motor: soultree_port` abaixo e a seção
//! "Plano de integração do port/" em `resonia/RECUPERACAO.md`.
//!
//! # Latência
//!
//! Esta ponte **não** declara número próprio. `latency_samples()` devolve o que a
//! implementação ativa informar: hoje 0 (passa-direto). O valor 2304 @ 48 kHz é do
//! build 1.0.5 e não está provado para o 1.0.6 (`docs/engine/recursos-recuperados.md` 2.1,
//! que registra o conflito documental); só entra quando o motor devolver o valor.
//!
//! # Parâmetros
//!
//! Índices 0..142 = ids da tabela de 143 descritores (`param_table.rs`). `set_param` recebe o
//! valor **simples** (unidades da tabela: dB, Hz, 0/1, inteiro de enum), nunca o normalizado.
//! A curva normalizado<->simples é linear só onde `Curve::Linear` (PROVADO); nos demais é
//! `NÃO PROVADO` e a conversão acontece fora da ponte (no host/GUI), não aqui.

use crate::param_table::{PARAMS, PARAM_COUNT};

/// Quem está processando de fato.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum EngineKind {
    /// Passa-direto: o áudio sai igual ao que entrou. Nenhum DSP.
    PassThrough,
    // TODO motor: soultree_port — `Soothe3Port` entra aqui quando a cadeia (M5/M6) existir.
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
}

impl Default for EngineBridge {
    fn default() -> Self {
        Self::new()
    }
}

impl EngineBridge {
    /// Nasce com os valores da tabela (`default`, NÃO PROVADO como estado inicial do motor).
    pub fn new() -> Self {
        let mut params = [0.0; PARAM_COUNT];
        for (p, spec) in params.iter_mut().zip(PARAMS.iter()) {
            *p = spec.default;
        }
        Self { config: None, params, kind: EngineKind::PassThrough }
    }

    /// Quem está processando (hoje sempre `PassThrough`).
    pub fn engine_kind(&self) -> EngineKind {
        self.kind
    }

    /// Versão do port ligado (só com `--features motor`).
    #[cfg(feature = "motor")]
    pub fn motor_port_version() -> &'static str {
        soultree_port::PORT_VERSION
    }

    /// Configura o motor. Pode alocar; chamar fora da thread de áudio.
    /// `max_block` é o maior bloco que `process` receberá; `channels` é o nº de canais principais.
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
        // TODO motor: soultree_port — criar/realocar o estado do motor para (sample_rate,
        // max_block, channels) e reaplicar `self.params` (índices 0..142).
        self.config = Some(Config { sample_rate, max_block, channels });
        Ok(())
    }

    /// Taxa de amostragem da última `prepare` bem-sucedida.
    pub fn sample_rate(&self) -> Option<f32> {
        self.config.map(|c| c.sample_rate)
    }

    /// Processa um bloco **no lugar**: `main[canal][amostra]`. Todos os canais têm o mesmo
    /// comprimento (<= `max_block`). `sidechain`, se existir, tem a mesma forma e não é alterado.
    ///
    /// Sem alocação nem bloqueio. Passa-direto: não toca nas amostras.
    pub fn process(&mut self, main: &mut [&mut [f32]], sidechain: Option<&[&[f32]]>) {
        let _ = sidechain;
        debug_assert!(
            self.config.map_or(true, |c| main.len() <= c.channels && main.iter().all(|ch| ch.len() <= c.max_block)),
            "bloco maior que o preparado"
        );
        // TODO motor: soultree_port — chamar a cadeia aqui, na ordem do binário (sem reordenar).
        // Passa-direto de propósito: nenhum DSP é feito nesta fase.
        let _ = main;
    }

    /// Latência atual em amostras, a que o host precisa compensar. 0 em passa-direto.
    /// TODO motor: soultree_port — devolver a latência informada pelo motor (não um número fixo).
    pub fn latency_samples(&self) -> u32 {
        0
    }

    /// Zera o estado interno (transporte parou/reposicionou). Mantém a configuração e os parâmetros.
    pub fn reset(&mut self) {
        // TODO motor: soultree_port — zerar rings/estados do motor.
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
        // TODO motor: soultree_port — encaminhar ao escritor de estado (`0x867D80`); a ordem de
        // aplicação e a origem de `rdx`/callback `[rdx+0x50]` são M4 (NÃO PROVADO).
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
        assert!(b.prepare(96_000.0, 64, 16).is_ok());
        assert_eq!(b.sample_rate(), Some(96_000.0));
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
        b.prepare(48_000.0, 256, 2).unwrap();
        b.set_param(94, 40.0); // Mix
        b.reset();
        assert_eq!(b.param(94), Some(40.0));
        assert_eq!(b.sample_rate(), Some(48_000.0));
    }

    #[cfg(feature = "motor")]
    #[test]
    fn motor_feature_links_the_port() {
        assert!(!EngineBridge::motor_port_version().is_empty());
    }
}
