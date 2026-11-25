# host — host VST3 somente leitura (oráculo da etapa I)

Programa mínimo em Rust que carrega `original/soothe3.vst3`, inicializa o
componente de áudio pela API padrão do VST3, processa um WAV de entrada em
blocos e grava um WAV **float32 estéreo** com a saída bruta do plugin.

Não há injeção, hook, patch ou alteração do plugin. O host apenas:

1. `LoadLibraryW` no `.vst3` (que é uma DLL PE);
2. `GetProcAddress("GetPluginFactory")` e chamada da factory;
3. enumeração das classes e escolha da categoria `Audio Module Class`;
4. `createInstance` → `IComponent` + `queryInterface(IAudioProcessor)`;
5. `initialize` → `setupProcessing` → `setActive(true)` → `setProcessing(true)`;
6. `process` bloco a bloco;
7. `setProcessing(false)` → `setActive(false)` → `terminate` → `release`.

O host **não usa** `DllGetClassObject`: esse símbolo não é exportado pelo
módulo. O entry point VST3 exportado é `GetPluginFactory`, que é o caminho
usado aqui.

## Requisitos

- Windows x64.
- Rust stable com toolchain `x86_64-pc-windows-msvc` (testado com 1.100.0).
- Nenhuma dependência externa: só `std` e FFI crua de `kernel32`.
- Nenhuma rede: `cargo build --release --offline` funciona.

## Compilar

```powershell
cd host
cargo build --release --offline
```

São gerados dois binários:

- `target/release/host.exe` — o host;
- `target/release/gen_sine.exe` — gerador do WAV de teste.

## Gerar o WAV de teste

Seno de 1 kHz, 48 kHz, 1 s, estéreo, com amplitudes diferentes por canal
(L = 0,5 e R = 0,25) para detectar troca de canais:

```powershell
.\target\release\gen_sine.exe test\seno_1k_48k_1s.wav
```

## Rodar

```powershell
.\target\release\host.exe ..\original\soothe3.vst3 test\seno_1k_48k_1s.wav test\out_soothe3.wav
```

Uso completo:

```
host <plugin.vst3> <in.wav> <out.wav> [blocos]
```

- `blocos` é o tamanho do bloco em frames (padrão **512**).
- Entrada aceita: PCM 8/16/24/32 ou float 32/64, 44,1 kHz ou 48 kHz, mono ou
  estéreo (mono é duplicado; >2 canais usam os dois primeiros).
- Saída: WAV `WAVE_FORMAT_IEEE_FLOAT`, 32 bits, estéreo, **mesmo número de
  frames da entrada**. A latência do plugin **não** é compensada: o WAV é a
  saída bruta, incluindo os 2304 samples de atraso no início.

Cada chamada COM é registrada com ordem, endereço da função, RVA relativo ao
módulo e HRESULT simbólico. Se um passo falhar, o programa aborta antes de
gravar e imprime o HRESULT exato. Ele também se recusa a gravar se a saída for
silêncio absoluto com entrada não silenciosa, ou se contiver NaN/Inf.

## Resultado verificado (48 kHz, bloco 512)

Log completo: `test/run4.log`. Resumo:

```
vendor='oeksound' flags=0x10 (kUnicode)
3 classes: Audio Module Class / Component Controller Class / Plugin Compatibility Class
classe escolhida: 'soothe3' cid=01EFCDAB8291EBFA4F656B5353746833
createInstance(IComponent) = S_OK
queryInterface(IAudioProcessor) = S_OK
initialize(hostContext) = S_OK
buses: 2 entradas (0 = Main Input kMain 2ch, 1 = Sidechain Input kAux 2ch),
       1 saída (Output kMain 2ch)
getLatencySamples = 2304
getTailSamples = 0
setupProcessing(kOffline, kSample32, 512, 48000) = S_OK
setActive(true) = S_OK
setProcessing(true) = S_OK
94 blocos processados, todos S_OK
frames: 48000 de 48000
saída: 48000 frames, 2 canais, 48000 Hz, float32 (384056 bytes)
pico -5,5 dBFS, RMS -15,7 dBFS
diferença crua saída−entrada: pico -1,4 dBFS
diferença alinhada por 2304 samples: pico -1,4 dBFS, RMS -6,6 dBFS
```

Também testado em 44,1 kHz (`test/run_44k1.log`): 44100 frames, 87 blocos,
latência reportada 2304, saída gravada com 44100 frames.

**Importante:** no estado padrão (sem preset) o plugin **não é transparente**.
Um seno de 1 kHz é atenuado e sofre modulação. Portanto o null-test da etapa I
deve comparar **saída do plugin × reconstrução**, ambos renderizados pelo mesmo
host com o **mesmo tamanho de bloco**, e não saída × entrada. Ver `NOTAS.md`.

## Estado/preset

Esta versão **não** carrega `.vstpreset` nem chama `setState`/`getState`.
O plugin roda no estado padrão de fábrica. Também não há controlador, automação
de parâmetros, `processContext` nem suporte a outros tamanhos de amostra/taxa.
Ver a lista completa em `NOTAS.md`.

## Arquivos

```
host/
  Cargo.toml
  src/main.rs            host (FFI, vtables, WAV, log)
  src/bin/gen_sine.rs    gerador do WAV de teste
  test/seno_1k_48k_1s.wav
  test/out_soothe3.wav   saída do run4
  test/run4.log          log do run 48 kHz
  test/seno_1k_44k1_1s.wav  entrada secundária (44,1 kHz)
  test/out_44k1.wav      saída do run 44,1 kHz
  test/run_44k1.log      log do run 44,1 kHz
  test/analise.py        comparação entrada×saída (atraso, ganho, resíduo)
  NOTAS.md               achados técnicos e limites
```

`test/analise.py` é opcional (usa só a biblioteca padrão do Python):

```powershell
py test\analise.py test\seno_1k_48k_1s.wav test\out_soothe3.wav
```
