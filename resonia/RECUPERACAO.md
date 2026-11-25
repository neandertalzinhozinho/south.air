# Recuperação do código-fonte do Resonia e preparo para o motor (25/11/2026)

Duas fases. A fase 1 (recuperação) já tinha parte do trabalho gravado em `app\` quando esta
retomada começou (as ferramentas de `_ferramentas\` e as montagens de `_ferramentas\analise\montado`
e `...\replay2`). Esta retomada **conferiu** esse material, testou `minised.py`, e fez a fase 2.
Nada fora de `resonia\` foi alterado. Nenhum git commit. Nada foi instalado no sistema nem copiado
para pastas de plugins.

## Fase 1 — recuperação

### Descoberta central (continua valendo)
O projeto antigo tem uma lacuna sem registro (21/11 10:03Z até 22/11 01:37Z) em que um agente
sem log reestruturou tudo (`dsp.rs` virou `dsp/*`, apareceram `host.rs`, `bin/render_host.rs`).
Por isso o estado final = snapshot completo mais recente + edições posteriores; o replay "pela
frente" só vale para a fase manhã.

### Passos do §7 antigo, estado real
1. `replay.py`: existe e roda; log em `_ferramentas\analise\replay2\_log.txt`. Todos os Write/Edit
   conferem com `originalFile`/`structuredPatch` e Reads (hunks "OK", Reads "conteudo IGUAL"),
   exceto: `dsp\curve.rs` 01:54:19 (sem base, arquivo da lacuna; coberto pelo snapshot) e
   `lib.rs` 01:55:17 (DIVERGE(9): base da lacuna, expected). Nenhum comando dos registros é executado.
2. `minised.py`: testado por `_ferramentas\testar_minised.py` (5 casos, TUDO OK): sed 01:54:26
   (curve.rs, saída idêntica ao registro), 01:54:41 (troca de `use` do stft), `132i\`, `257,262s` ERE
   e `93,94c\` (os dois últimos sobre texto sintético com a forma do comando registrado). Limite:
   não implementa `-n`/`p`; não testado o `sed -n 90,98p` de 10:02:15 (ui.rs da manhã não é reconstruído).
3. Snapshots Codex (`extrair_snap.py`, desfaz mojibake cp1252→UTF-8): tamanhos conferidos contra o §2 antigo.
4. Patches Codex 02:14:06 (calibrate.rs) e 02:14:21 (main.rs) aplicados com conferência de contexto
   (`montar_patch.py`); 02:24:31 (ui.rs) não aplicado porque o ui.rs recuperável é parcial e foi descartado
   (abaixo). O de 02:13:37 falhou no log original e foi ignorado.
5–6. Montagem e gravação em `app\`: ver tabela. Sem stub inventado para o que falta.

### Estado por arquivo (tamanho final conhecido = `Get-ChildItem` de 02:28:53Z)

Todos os "exato" têm tamanho em bytes igual ao do registro, conteúdo comparado com `cmp` contra a
montagem, EOL = LF. Ficam em `app\_arquivo_heuristico\recuperados_exatos\` (os DSP heurísticos, ver fase 2),
exceto `vst3host.rs`, `vst3tool.rs`, `make_vst3.cmd`, que seguem ativos.

| Arquivo | Estado | Bytes | Verificação |
|---|---|---:|---|
| src/vst3tool.rs | exato (Write 09:56:52 + sed 01:38:31) | 11937 | tamanho = registro; **ativo** |
| src/vst3host.rs | exato (Write + 3 Edits) | 26859 | tamanho = registro; **ativo** |
| make_vst3.cmd | exato (versão manhã; lacuna pode ter mudado) | 513 | Write len; **ativo** |
| src/calibrate.rs | exato (snapshot 02:12:59 + patch 02:14:06) | 18458 | tamanho = registro; arquivado |
| src/equivalence.rs | exato (snapshot 02:28:59) | 15498 | tamanho = registro; arquivado |
| src/main.rs (antigo) | exato (replay + patch 02:14:21) | 26425 | tamanho = registro; arquivado (`main.rs`) |
| src/dsp/{curve,detect,envelope,mod,stft}.rs | exato | 5387/2406/998/8090/12007 | tamanhos = registro; arquivados |
| src/bin/render_host.rs | exato | 1338 | arquivado |
| Cargo.toml (antigo) | exato no conteúdo (743 B); EOL LF presumido | 743 | substituído (fase 2) |
| src/lib.rs | **só a versão da manhã** (13125 B, exata para a manhã); final (14726 B) **não recuperado** | — | `lib_fase_manha.rs` |
| src/settings.rs (13164 B) | **não reconstruído** (decisão abaixo) | — | — |
| src/ui.rs (31658 B) | **não reconstruído** (parcial: só linhas ~1–452 + patch; decisão abaixo) | — | — |
| src/host.rs (16667 B) | **ausente**: só 30 linhas + fragmentos | — | — |
| src/dsp/output.rs (1284 B), src/dsp/stereo.rs (1653 B) | **ausentes**: o conteúdo nunca aparece nos registros | — | — |
| Cargo.lock | **ausente** (nunca lido por inteiro). O `app\Cargo.lock` atual foi **gerado** pelo cargo na fase 2 | — | — |
| MECHANICS.md, mechanics.json | não recuperados (só versão da manhã; fora do escopo do build) | — | — |

Decisão sobre `ui.rs`/`settings.rs`: a leitura anterior dos registros indicou que o conteúdo recuperável
vinha com textos, endereços e valores copiados de um produto comercial de terceiros e imitava a tela dele; além
disso era parcial. Não foi reconstruído. A tela atual é nova (fase 2).

**Arquivos NOVOS escritos por engano numa tentativa anterior**, sem origem nos registros (`output.rs`,
`stereo.rs`, `host.rs`-substituto, `settings.rs`, `ui.rs` antigos): contrariam a regra "sem stub inventado".
Foram movidos para `app\_arquivo_heuristico\descartados_NOVOS\` (não compilados, só para rastreio; podem ser apagados).

### Build/test da fase 1 (estado real, antes da fase 2)
`cargo build --offline` em `resonia\app`, com os recuperados + NOVOS e sem `lib.rs`:
`error: failed to parse manifest ... can't find library resonia, rename file to src/lib.rs or specify lib.path`.
Sem `lib.rs` final, `output.rs`, `stereo.rs`, `host.rs` e `Cargo.lock` recuperados, a árvore antiga **não compila**
e não é reconstruível sem invenção. Isso é a lacuna registrada; a fase 2 não a contorna reescrevendo o DSP.

## Fase 2 — preparo para o motor

### O que mudou
- O DSP heurístico (`dsp/*`) e as ferramentas que o calibravam contra o plugin original
  (`calibrate`, `equivalence`, `--fit/--score/--prove-superiority/--compare/--measure-original`, `render_host`)
  saíram do caminho de áudio e estão em `app\_arquivo_heuristico\` (**não compilado**).
- Novo `src/engine_bridge.rs`: única interface de áudio. Hoje **passa-direto** (`// TODO motor: soultree_port`).
- Novo `src/param_table.rs`, **gerado** por `_ferramentas\gerar_param_table.py` a partir de
  `RECURSOS_VALIDADOS_recuperados\parameter_table_143_params.json` (SHA-256 no cabeçalho do arquivo).
- Novo `src/params.rs`: 143 parâmetros nih-plug (`Params` implementado à mão), ids de host `p000`..`p142`.
- Novo `src/lib.rs` (plugin), `src/ui.rs` (tela gerada a partir da tabela), `src/main.rs` (janela + ferramentas).
- `Cargo.toml`: removidos `cpal`, `realfft`; `soultree_port = { path = "../../port", optional = true }` atrás da
  feature `motor`. Sem a feature, o `port\` não entra no build.
- Mantidos: `vst3tool.rs`, `vst3host.rs`, `make_vst3.cmd`.

### Assinatura de `engine_bridge`
```rust
pub struct EngineBridge;
pub enum EngineKind { PassThrough }
pub enum PrepareError { SampleRate, BlockSize, Channels }          // canais 1..=16
impl EngineBridge {
    pub fn new() -> Self;                                          // params = default da tabela (NÃO PROVADO como estado inicial)
    pub fn engine_kind(&self) -> EngineKind;
    pub fn prepare(&mut self, sample_rate: f32, max_block: usize, channels: usize) -> Result<(), PrepareError>;
    pub fn sample_rate(&self) -> Option<f32>;
    pub fn process(&mut self, main: &mut [&mut [f32]], sidechain: Option<&[&[f32]]>); // no lugar, sem alocar
    pub fn latency_samples(&self) -> u32;                          // 0 em passa-direto; nunca número fixo inventado
    pub fn reset(&mut self);
    pub fn set_param(&mut self, index: usize, plain: f64) -> bool; // 0..=142, valor simples, clamp [min,max], NaN ignorado
    pub fn param(&self, index: usize) -> Option<f64>;
    #[cfg(feature = "motor")] pub fn motor_port_version() -> &'static str;
}
```

### Parâmetros (o que é provado e o que não é)
Fonte e provas: `docs/engine/recursos-recuperados.md` §2.4/§3. Marcado `NÃO PROVADO` no código
(`param_table.rs`, `params.rs`):
- `Curve::Linear` só onde `cb+72=0x3351A0` e `cb+80=0x3351E0` (provado); `Curve::NaoProvado` nos outros 100 parâmetros
  (frequência, Q, tilt, bandas discretas, bools...). O host usa mapeamento **linear provisório** para todos.
- `default` = `initial_or_default_candidate`: não é estado inicial provado.
- `Kind` (Float/Bool/Int/Enum) é só escolha de controle pelo formatador `+88`; rótulos de `Mode` (id 2) e `Band solo`
  (id 91) não resolvidos (mostrados como inteiro); rótulos de `quality` e `band_channels` não reconferidos no 1.0.6.
- Unidade " Hz" só em "* frequency"; demais sem unidade (não provadas). Log-slider de frequência na tela é só conveniência de arraste.
- Bypass (id 97) é marcado como bypass do host; o passa-direto atual não depende disso.

### Latência
Declarada ao host = `bridge.latency_samples()` = **0** (sem motor). 2304 @ 48 kHz é do build 1.0.5 e não está provado
no 1.0.6 (conflito documental em `recursos-recuperados.md` 2.1). Só entra quando o motor informar.

### GUI
Janela 1050×621 (pista, não provada). Nenhum SVG/PNG/HLSL/fonte do material recuperado foi empacotado; só fontes padrão
do egui. Abas General/Bands/Channels geradas da tabela; nós de banda arrastáveis (freq/depth). Sem espectro nem curva de
redução (dependem do motor). Captura: `app\target\release\resonia-app.exe --screenshot x.png` (conferida, 1050×621).

### Resultado real de build/test (fase 2)
- `cargo build --offline`: **ok** (só warnings: dead code em `vst3host.rs`, inferência `f32` do egui, corrigida em `ui.rs`).
- `cargo test --offline`: **9 passed, 0 failed** (`engine_bridge`: passa-direto bit a bit, latência 0, `prepare` com
  argumentos inválidos, defaults/clamp, reset; `params`: 143 ids sequenciais dentro da faixa, pontos conferidos, rótulos
  de enum, 143 ids de host únicos e defaults).
- `cargo test --offline --features motor`: **10 passed** (compila e liga `soultree_port`; só lê `PORT_VERSION`).
- `make_vst3.cmd` (release): **ok** → `app\dist\Resonia.vst3` (3 828 224 B) + `moduleinfo.json`; `--check-vst3`: ok
  (1 classe, CID `5265736F6E6961537570707265737331`, 2 entradas incl. sidechain, 1 saída).
- `resonia-app --selftest-vst3 dist\Resonia.vst3` (carrega a DLL em processo, 143 parâmetros): nomes = tabela;
  latência reportada 0; **48 000 amostras × 2 canais bit-idênticas à entrada**.
- Não verificado: carga em DAW real; edição/automação no host; `--process` com WAV; consumo de CPU.

## Plano de integração do `port/`

O motor ainda não tem API de blocos; hoje o `port` fecha M1/M2 e `pending::first_blocking()` = `0x293760` (M3). Quando a
cadeia (M5/M6) existir, o encaixe é **só** em `app\src\engine_bridge.rs`:

1. Ativar: `cargo build --features motor` (a dependência `soultree_port = { path = "../../port", optional = true }` já está
   no `Cargo.toml`). Se o `port` virar workspace/ganhar dependências, rodar sem `--offline` uma vez para atualizar o `Cargo.lock`.
2. `EngineKind`: acrescentar `Soothe3Port` e guardar o estado do motor em `EngineBridge` (campo `#[cfg(feature = "motor")]`).
3. `prepare` (marca `TODO motor` 1): criar/realocar o estado para `(sample_rate, max_block, channels)`, reaplicar `self.params`.
   `sample_rate` do motor é a identidade `[ctx+0x60]` (M4, hoje NÃO PROVADA).
4. `set_param` (marca 3): encaminhar `(index, plain)` ao escritor `0x867D80`. O motor espera o valor após o callback `[rdx+0x50]`
   (M4); se o motor quiser normalizado, a conversão correta usa `Curve::Linear` onde provado e **nenhuma conversão inventada**
   onde `Curve::NaoProvado` — resolver essas curvas antes (M4) ou passar o plain e deixar o motor converter.
5. `process` (marca 2): chamar a cadeia na ordem do binário, in-place; passar `sidechain` (o plugin hoje entrega `None`:
   em `lib.rs`/`Resonia::process` trocar por `aux.inputs`, marca `TODO motor`).
6. `latency_samples` (marca 4): devolver a latência informada pelo motor; `lib.rs` já anuncia ao host em `initialize` e a cada
   bloco se mudar. Conferir contra o oráculo (`host\` + `original\soothe3.vst3` 1.0.6, bloco 512, alinhamento 2304) em M7.
7. `reset`: zerar rings/estados. 
8. Tela: trocar o texto "none (pass-through, no DSP)" (`UiInfo.engine` em `lib.rs` e `main.rs`) por `engine_kind()`; alimentar
   um painel de análise com o que o motor expuser (`ui.rs` não tem espectro).
9. Testes: `engine_bridge::tests::passthrough_is_bit_exact` deve ser trocado/estendido pelo null-test (M7), e
   `--selftest-vst3` deixa de esperar passa-direto.

## Lacunas conhecidas
`lib.rs` final, `settings.rs`, `ui.rs`, `host.rs`, `dsp/output.rs`, `dsp/stereo.rs`, `Cargo.lock`, `MECHANICS.md`/`mechanics.json`
não foram recuperados (ver tabela). Nada foi inventado para substituí-los na recuperação; o que existe de novo é a camada da
fase 2 acima, rotulada como NOVA.
