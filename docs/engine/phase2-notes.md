# Fase 2 — funções identificadas (endereço, tamanho, papel, confiança)

Base de ponteiros `0x199B0000`. Tamanhos vêm do `.pdata`
(`docs/engine/functions.csv`). Confiança: **alta** = provado por RTTI/string;
**média** = padrão de chamada/assinatura; **baixa** = candidato.

| RVA | Tamanho | Papel provável | Confiança | Evidência |
|---|---:|---|---|---|
| `0x2037A58` | — | vtable `Soothe3AudioProcessor` | alta | COL `0x2095B50` → `0x23ADE08` |
| `0x2036E48` | — | vtable `kali::JUCEAudioProcessor<visualisation_data,8>` | alta | COL `0x2096FE0` → `0x23AC970` |
| `0x34C3C0` | 33 | `Soothe3AudioProcessor::getName` → `"soothe3"` | alta | string em `0x1C2BC08` |
| `0x350F20` | 9682 | candidato a `processBlock` | média | maior slot; args de áudio; corpo obfuscado |
| `0x34F970` | 5538 | candidato a `prepareToPlay`/`process` | baixa | 2º maior slot |
| `0x48A440` | 105 | programa/tail length | média | slot 5 da vtable |
| `0x48B980` | 68 | consulta de barramento (`[this+0xD8]`, `[this+0x10C]`) | média | slot 11 |
| `0x48B8E0` | 68 | par do anterior | média | slot 12 |
| `0x61BF30` | 6151 | `MainComponent` ctor (UI) | alta | grava vtable `0x2050B90` (`.?AUMainComponent@@`) |
| `0x66A710` | — | layout de parâmetros ("low latency", "minimum phase", "quality", "mix") | alta | strings referenciadas |
| `0x661EC0` | — | builder da tabela de parâmetros (chama `0x32AEC0` 65×) | média | xrefs |
| `0x17280` | — | kernel SIMD PFFFT | média | padrão + licença FFTPACK |
| `0x17380` | — | kernel SIMD PFFFT | média | idem |
| `0x17820` | — | kernel SIMD PFFFT | média | idem |
| `0x238E9B0` | 143×0x68 | tabela de descritores de parâmetros | alta | `params.csv` |

## Como reproduzir

```powershell
py tools\rtti_name.py 0x2037A58 0x2036E48
py tools\vtable_dump.py 0x2037A58
py tools\ctor_vtables.py 0x61BF30
py tools\summarize_func.py 0x350F20
```

## Pendências (para fechar a Fase 2/3)

1. Desobfuscar `0x350F20` (opaque predicates) para confirmar `processBlock`.
2. Seguir as chamadas indiretas (`call qword ptr [rax+0xNN]`) até a classe de STFT.
3. Localizar as constantes de tamanho de FFT por `Quality` (procurar `0x400/0x800/0x1000/0x2000`
   perto de `0x66A710`).
