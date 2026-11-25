# NOTAS — achados técnicos do host (etapa I)

Este arquivo registra o que foi **medido** no binário `original/soothe3.vst3`
e no host, incluindo tentativas que falharam. Nada aqui é inferência
apresentada como certeza: quando é hipótese, está marcado como hipótese.

## 1. Entry point e carregamento

- O módulo exporta `GetPluginFactory` (RVA `+0x327A50`) e **não exporta**
  `DllGetClassObject` por nome. Por isso o host usa `GetPluginFactory`, que é
  o entry point padrão de um módulo VST3.
- Também existem exports `InitDll` / `ExitDll` (RVA `+0x325960` para ambos).
  O host **não** os chama: `LoadLibraryW` já executa o `DllMain` e todo o
  fluxo (factory → componente → process) funciona sem eles. Não foi testado
  chamá-los; a rota de dump repachado (`dumpsooth/soothe3_loadable.dll`) é
  sabidamente morta por crash no `DllMain` (§19.7 do plano).
- `LoadLibraryW` devolve base `0x180000000`, `SizeOfImage = 0x82A8000`.
- O `.text` em disco está **criptografado**: desmontar o arquivo diretamente
  mostra lixo. O código só fica legível depois de `LoadLibraryW`, lendo
  `string_at(base + RVA)` no processo.

## 2. Layout dos TUIDs (achado que destravou tudo)

O SDK compila com `COM_COMPATIBLE = 1` no Windows. Os TUIDs **não** são
little-endian por palavra de 32 bits nem big-endian por palavra: são o layout
**GUID/COM**:

```
Data1 = l1 em LE32
Data2 = parte alta de l2 (l2 >> 16) em LE16
Data3 = parte baixa de l2 (l2 & 0xFFFF) em LE16
Data4 = l3 e l4 em big-endian
```

É exatamente o que `INLINE_UID` de `funknown.h` expande. Evidência no binário
(desmontagem após carga): `initialize` consulta `IHostApplication` com os bytes
`cc 95 e5 58 2d db 69 49 8b 6a af 8c 36 a6 64 e5`, e o `queryInterface` compara
`IPluginBase` com `db 8d 88 22 6e 15 ae 45 83 58 b3 48 08 19 06 25`.

IIDs usados (bytes que funcionam):

| Interface | Bytes |
|---|---|
| `FUnknown` | `0000000000000000C000000000000046` |
| `IComponent` | `31ff31e8d5f20143928ebbee25697802` |
| `IAudioProcessor` | `993f0442dab73c45a569e79d9aaec33d` |
| `IHostApplication` | `cc95e5582ddb69498b6aaf8c36a664e5` |
| `IPluginBase` | `db8d88226e15ae458358b34808190625` |

Tentativas anteriores e erro exato:

- IIDs em **LE por palavra de 32 bits**: `createInstance` devolveu
  `E_NOINTERFACE (0x80004002)`.
- IIDs em **BE por palavra de 32 bits**: `createInstance(FUnknown)` passou, mas
  `queryInterface` devolvia `kResultFalse (S_FALSE)`.
- Causa raiz: layout GUID + IID errado de `IHostApplication`. Corrigido, tudo
  passou a devolver `S_OK`.

## 3. Classes da factory

`countClasses` devolve **3** (é uma contagem, não um HRESULT — o host agora
loga como número):

| Índice | CID (bytes de `getClassInfo`) | Categoria | Nome |
|---|---|---|---|
| 0 | `01EFCDAB8291EBFA4F656B5353746833` | `Audio Module Class` | `soothe3` |
| 1 | `01EFCDAB3412CDAB4F656B5353746833` | `Component Controller Class` | `soothe3` |
| 2 | `01EFCDABDEC00DF04F656B5353746833` | `Plugin Compatibility Class` | `soothe3` |

O CID é lido **verbatim** de `getClassInfo` (nada é hardcoded). O host escolhe
a categoria `Audio Module Class` e pede `IComponent` diretamente em
`createInstance` — devolve `S_OK`.

`getFactoryInfo`: `vendor='oeksound'`, `url=''`, `email=''`,
`flags=0x10` (`kUnicode`).

## 4. Vtables observadas

Endereços relativos à base do módulo (RVA), medidos após `LoadLibraryW`:

| Método | RVA |
|---|---|
| `IComponent::queryInterface` | `+0x322670` |
| `IComponent::initialize` | `+0x322740` |
| `IComponent::terminate` | `+0x322800` |
| `IComponent::getBusCount` | `+0x324100` |
| `IComponent::getBusInfo` | `+0x324130` |
| `IComponent::activateBus` | `+0x324280` |
| `IComponent::setActive` | `+0x322A00` |
| `IAudioProcessor::canProcessSampleSize` | `+0x324E50` |
| `IAudioProcessor::getLatencySamples` | `+0x324E90` |
| `IAudioProcessor::setupProcessing` | `+0x324EA0` |
| `IAudioProcessor::setProcessing` | `+0x324FD0` |
| `IAudioProcessor::getTailSamples` | `+0x324FF0` |
| `IAudioProcessor::process` | `+0x325070` |
| `IAudioProcessor::getBusArrangement` | `+0x324DE0` |
| `IPluginFactory::countClasses` | `+0x3267F0` |
| `IPluginFactory::getFactoryInfo` | `+0x326810` |
| `IPluginFactory::getClassInfo` | `+0x3268A0` |
| `IPluginFactory::createInstance` | `+0x326B10` |

`IAudioProcessor*` é `IComponent* + 8`: o objeto usa herança múltipla e o
segundo vtable pointer fica logo após o primeiro.

## 5. IHostApplication mínimo

`IComponent::initialize` chama de volta `queryInterface(IHostApplication)` no
contexto do host. Por isso o host implementa um objeto COM estático com:

- `queryInterface`: aceita `FUnknown` e `IHostApplication`; nega o resto com
  `E_NOINTERFACE`;
- `addRef`/`release`;
- `getName`: devolve a string UTF-16 `soultree-host-oracle`;
- `createInstance`: devolve `E_NOTIMPL`, porque o host não implementa
  `IMessage`/`IAttributeList`.

Nesta execução o plugin chamou apenas `queryInterface`; `getName` e
`createInstance` não foram chamados.

## 6. Buses

O componente declara:

| Direção | Índice | Nome | Tipo | Canais | Arranjo |
|---|---|---|---|---|---|
| entrada | 0 | `Main Input` | `kMain` | 2 | `0x3` (estéreo) |
| entrada | 1 | `Sidechain Input` | `kAux` | 2 | `0x3` (estéreo) |
| saída | 0 | `Output` | `kMain` | 2 | `0x3` (estéreo) |

`flags=0x1` (`kDefaultActive`) nos três. O host ativa explicitamente só os
buses de índice 0 e desativa o sidechain com `activateBus(..., false)`. No
`ProcessData`, o sidechain inativo vai com `numChannels = 0` e
`channelBuffers32 = null`, o que a spec permite.

## 7. Latência, tail e modo

- `getLatencySamples` = **2304** tanto a 48 kHz quanto a 44,1 kHz.
- `getTailSamples` = **0**.
- `canProcessSampleSize(kSample32)` = `S_OK`.
- `setupProcessing(kOffline, kSample32, 512, 48000)` = `S_OK`.
- `processContext = null` (opcional pela spec; sem transporte/tempo).
- `inputParameterChanges` e `outputParameterChanges` = `null`.

A latência **não** é compensada na gravação: o WAV de saída tem os primeiros
2304 samples praticamente nulos e o mesmo número de frames da entrada (o rabo
do plugin é 0, então não há o que rebobinar).

## 8. O plugin não é transparente no estado padrão

> **INVÁLIDO (2026-11-25):** as medições das §8–§9 foram feitas com o bug de (des)intercalação do
> laço de `process` (entrada L,R,L,R num canal; metade de cada bloco de saída sem escrita). A
> "dependência de bloco" e os lóbulos em `Fs/bloco` eram artefato do host. Corrigido em
> `host/src/main.rs`; ver `checks/w_cadeia_m6.md` §5.

O run canônico (`test/run4.log`, bloco 512) mostra, para um seno de 1 kHz:

- entrada: pico 0,5 / RMS −11,1 dBFS;
- saída: pico 0,532736 / RMS −15,7 dBFS;
- diferença crua saída−entrada: pico 0,855516 (−1,4 dBFS);
- diferença alinhada por 2304 samples (canal L): pico −1,4 dBFS,
  RMS −6,6 dBFS.

`test/analise.py` (janela de 16384 samples a partir de 12000, canal L):

- melhor atraso por correlação cruzada: 2568 samples, correlação 0,346;
- ganho escalar ótimo: 0,203 (−13,8 dB), resíduo RMS −14,2 dBFS.

A correlação baixa e o resíduo quase igual ao sinal mostram que a saída **não**
é uma cópia atrasada/escalada da entrada: o plugin está processando de fato.
Não use o "melhor atraso" da correlação como medida de latência — a latência
correta é a reportada, 2304.

## 9. Dependência do tamanho de bloco (importante para o oráculo)

O mesmo WAV renderizado com tamanhos de bloco diferentes produz saídas
diferentes. Medindo a projeção em 1 kHz e o resíduo (janela de 16384 samples a
partir de 12000, canal L):

| blocos | RMS da janela | amplitude 1 kHz | vs entrada | resíduo RMS | lóbulos laterais |
|---|---|---|---|---|---|
| 64 | −13,03 dBFS | 0,22625 | −6,9 dB | −16,17 dBFS | a cada 750 Hz |
| 512 | −13,70 dBFS | 0,10129 | −13,9 dB | −14,26 dBFS | a cada 93,75 Hz |
| 1024 | −13,75 dBFS | 0,13556 | −11,3 dB | −14,82 dBFS | a cada 46,875 Hz |
| 4096 | −14,10 dBFS | 0,10049 | −13,9 dB | −14,71 dBFS | a cada 11,7 Hz |
| 48000 | −12,72 dBFS | 0,27971 | −5,0 dB | −18,45 dBFS | sem lóbulos |

O espaçamento dos lóbulos é exatamente `Fs / blocos` (750 = 48000/64,
93,75 = 48000/512, etc.). Com um único bloco de 48000, o tom sai limpo em
1 kHz, atenuado cerca de 5 dB.

Interpretação: o componente de áudio adapta seu comportamento **por chamada de
`process`**, e essa adaptação gera modulação no rate do bloco. O host passa os
mesmos samples em qualquer chunking (o `pos` avança exatamente por `n`), então
a diferença vem de dentro do plugin, não da montagem dos buffers. Não foi
possível, só por inspeção do host, provar qual parámetro interno faz isso.

Consequência prática: **o null-test precisa fixar o tamanho de bloco** e usá-lo
igual nos dois lados. O padrão do host é 512. Não compare renders feitos com
blocos diferentes.

## 10. Determinismo

Duas execuções idênticas (bloco 512) produziram WAVs com o mesmo SHA-256:

```
1218c801a5e61a7591dce500c40a166e8598532666ae5b7808816899b42be67b
```

Ou seja, não há ruído/uninitialized memory visível: a renderização é
determinística neste ambiente.

## 11. O que NÃO está implementado

- `setState` / `getState` e carregamento de `.vstpreset` — o plugin roda no
  estado padrão de fábrica. Não há parâmetro de preset na CLI.
- Controlador (`Component Controller Class`), parâmetros, automação,
  `IParameterChanges`.
- `processContext`, `IEventList`, transporte/tempo.
- `InitDll` / `ExitDll`.
- Taxas diferentes de 44,1 e 48 kHz (o host aborta antes de carregar o plugin).
- Sample size diferente de 32-bit float.
- Mais de 2 canais, sidechain alimentado, múltiplos buses principais.
- Compensação de latência e flush de tail (tail reportado = 0).

## 12. Observações de execução

- Em um caminho de falha de uma tentativa antiga, o processo terminou com
  `0xC0000409` (`STATUS_STACK_BUFFER_OVERRUN`/fail-fast) depois do `fail()`.
  Não foi reproduzido no caminho de sucesso: os runs válidos (48 kHz, 44,1 kHz
  e os tamanhos de bloco testados) saíram com código 0.
- `setProcessing(false)`, `setActive(false)` e `terminate` devolvem `S_OK`.
- `release` do componente chama de volta `IHostApplication::release`; o
  objeto de host é estático e termina com `refs=1` (a referência inicial),
  o que é esperado.
- `FreeLibrary` devolve ok depois de todos os `release`.
- O log é UTF-8; a exibição no console do PowerShell pode mostrar acentos
  quebrados por causa da code page, mas os bytes gravados em `run4.log` são
  UTF-8 válidos.


## 13. Modo de sonda somente-leitura (M4, 2026-11-25)

Com `SOULTREE_PROBE=1`, o host:

1. roda `probe_state` depois do `process`;
2. varre por `VirtualQuery` as regiões privadas RW do **próprio processo**;
3. acha o `Soothe3AudioProcessor` pela vtable `base+0x2037A58`;
4. imprime `W = obj+0xE40`, `[W+0x28/0x30/0x68/0x70]`, o struct handle, `engine = [handle]`,
   `[eng+0x28/0x2C]`, o estado `engine+0x54` e os dois ctx (`eng+0x5ED8`, `eng+0x8B20`).

Só lê: não escreve, não instala hook e não injeta nada. No modo de sonda, a restrição de taxa
(44,1/48 kHz) é liberada para medir 32k..192k. O resultado está em `checks/u_estado_m4.md` §5.

Ambiente: o Windows App Control às vezes bloqueia um `host.exe` recém-compilado
("Permission denied"/`os error 4551`). Uma mudança mínima no código e a recompilação gera
outro hash e resolve.
