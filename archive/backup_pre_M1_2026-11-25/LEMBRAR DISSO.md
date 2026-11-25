# LEMBRAR DISSO

> **ARQUIVO PERMANENTE. NÃO ALTERAR. NÃO "ATUALIZAR". NÃO CORRIGIR. NÃO APAGAR.**
> Escrito em 2026-11-22. Serve só para um agente novo entender, em 30 segundos, o que
> este projeto é. Se algo aqui conflitar com qualquer outro documento, **este vence**.
> O plano vivo é `PLANO_MOTOR_AUDIO.md`; este arquivo é a âncora.

---

## O objetivo, em uma frase

**Extrair o motor de áudio DSP do soothe3 a partir do dump e colocar esse mesmo motor
dentro do Resonia (VST3).**

Nada além disso. Não é "fazer um plugin parecido". Não é "um EQ dinâmico genérico".
É o DSP daquele binário, com a mesma aritmética, na mesma ordem, com os mesmos
coeficientes, rodando dentro do Resonia.

---

## De onde os dados vêm — e de onde NÃO vêm

| Papel | Caminho | Observação |
|---|---|---|
| **FONTE DE VERDADE** | `D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin` | dump descriptografado, 137.003.008 B, SHA-256 `68D30368936C738490F10A852304A5E67B7B4FDD563F62513C5A5BC81034F55C` |
| **O QUE O IDA ABRE** | `D:\PROJETOS\soultree\dumpsooth\soothe3_unpacked.dll` | o mesmo dump já convertido em PE válido, 19 seções, `ImageBase = 0x180000000`, `.pdata` com 30.859 funções |
| **NÃO É FONTE** | `original\soothe3.vst3` | o plugin empacotado em disco (47.500.552 B). O `.text` dele está **100% cifrado** (7.382 de 7.382 páginas diferentes do dump). Vale **zero** para extração |

**Toda constante, todo offset, todo RVA, toda fórmula sai do dump.** Se um número não
está no dump, ele não existe — vira `NÃO EXTRAÍDO` / `NÃO PROVADO`, e o trabalho para ali
naquele ponto.

O plugin original, quando muito, é um **black box que toca áudio** e serve para conferir
depois se o port bate. Ele nunca é fonte de coeficiente. Olhar para ele esperando achar
código é perda de tempo — o código dele está cifrado.

---

## Regras que não se negociam

1. **Zero estimativa.** Zero heurística. Zero "algoritmo equivalente".
   Se não foi lido do dump, não entra.
2. **Proibido inferir fórmula pelo nome do parâmetro.** `detect.rs`, `curve.rs`,
   `envelope.rs` não são prova de nada.
3. **Proibido ajustar até o null-test bater.** Se não bate, o coeficiente foi lido
   errado — volta pro dump, não para o osciloscópio.
4. **Indício não é prova.** String de licença de FFT no `.rdata` não prova FFT.
5. **Decompilado é leitura, não prova.** A prova é a instrução, com RVA.
6. **Nunca escrever no processo alvo.** Sem hook, sem patch de checksum, sem injeção.
   Só leitura: dump estático e, se preciso, processo somente-leitura.
7. **A entrega só conta com os 5 itens:** (a) endereço da função no dump,
   (b) pseudocódigo/desmontagem comentada, (c) constantes com RVA,
   (d) estruturas com offsets comprovados, (e) Rust com a mesma aritmética, na mesma
   ordem, com os mesmos coeficientes.

---

## Onde as coisas estão

| O quê | Onde |
|---|---|
| Plano vivo, com todas as seções e o histórico de erros | `PLANO_MOTOR_AUDIO.md` |
| Especificação do DSP (só entra o que tem RVA) | `docs/engine/dsp-spec.md` |
| Decompilados | `docs/engine/decomp/` — `808B3ED0.c` (Ghidra) e `ida_XXXXXXXX.c` (IDA 9.3) |
| Funções, params, RTTI, xrefs | `docs/engine/functions.csv`, `params.csv`, `rtti_classes.csv`, `xrefs.csv` |
| Banco do IDA que funciona | `C:\Users\tromb\AppData\Local\Temp\opencode\ida_pe\soothe3_pe.dll.i64` |
| Scripts de leitura | `tools/` |
| Logs de análise | `checks/` |

Banco do IDA: abrir **sempre** o PE normalizado (`ida_pe\soothe3_pe.dll`), nunca o dump
cru. `idat.exe -A -S"script.py" -L"log" "...\soothe3_pe.dll"`. Dentro do script,
`ida_auto.plan_and_wait(f.start_ea, f.end_ea)` antes de `decompile` — sem isso o
Hex-Rays devolve `JUMPOUT`. Nunca chamar `ida_auto.auto_wait()`.

---

## O que já está provado (não redescobrir)

- O DSP é **banco de filtros no domínio do tempo**, não FFT. A FFT do binário é da GUI.
- `N = 256` @ 44,1 kHz; `278` @ 48 kHz; `557` @ 96 kHz. Janela Hann em `0x877DD0`.
- Núcleo: `0x8B3ED0`, 20.209 B, 127 `call`, **zero FMA**.
- Cluster aritmético: `0x8BF5C0–0x8C4300`. Gêmeo: `0x8C5FD8`.
- `0x8C3C20` — one-pole ida-e-volta, `p += (x − p) * 0.1f`, volta começando em `length − 2`.
- `0x8C1440` — montagem/varredura de buffer com padding de 16 B e dispatch por tipo;
  **não** é kernel de filtro. Chamado 2× por bloco de dentro do núcleo.
- `0x879CF0` — curva de normalização `min((1/(x/a+1))^(1/3), 1)`. **Não** é espaçamento
  de bandas (hipótese refutada).
- Camada vetorial: 33 primitivas IPP, 45 chamadas no núcleo, resolvidas por opcode (§17).
  O recíproco do IPP **não** é `1.0/x`.

## O que ainda falta (é o trabalho)

1. Tipo de filtro por banda — `0x87BB60` → `0x882FC0`; `0x87E220` (`powf` 2.4 / −4.8).
2. Detector e lei de ganho — provavelmente em `0x8C02F0` / `0x8C0BD0`.
3. Struct de estado (`ctx+0x2C38`, `+0xBFF8`, `+0x5F8`, `+0x5ED0`) e o mapa dos 143 params.
4. Oráculo: WAV de referência do original, para o null-test.
5. Port Rust dentro do Resonia, com a mesma latência declarada ao host (2.304 amostras
   @ 48 kHz).

---

## Coisas que já deram errado (para não repetir)

- **Heurística.** Houve um `app/src/dsp/*` que "soava parecido". Não era entrega. Foi
  apagado junto com `app/`. Não recriar nada por intuição.
- **Hipótese de espaçamento de bandas.** Refutada por `0x879CF0`.
- **"O IDA está travado".** Era o arquivo errado: o lote abria um `.bin` de memória cru
  (136.990.720 B) em vez do PE (137.003.008 B). Com o PE, tudo decompila.
- **"O Ghidra foi desinstalado".** Falso. Está em `D:\TOOLS\ghidra_12.2_PUBLIC`.
- **"O plugin em disco serve para extrair".** Falso. `.text` cifrado, 100%.
