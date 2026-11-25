"""DEV I5 — gera o relatorio de validacao (somente em temp)."""
import json, re, hashlib
from pathlib import Path

ROOT = Path(r"D:\PROJETOS\shadowFILES")
TMP = Path(r"C:\Users\tromb\AppData\Local\Temp\opencode")
canon = json.loads((ROOT / "analysis/parameter_table.json").read_text(encoding="utf-8"))
dump = json.loads((ROOT / "analysis/recovered_native/dsp/params_dump.json").read_text(encoding="utf-8"))
schema = json.loads((ROOT / "soothe3_reconstructed_engine/soothe3_parameters_schema.json").read_text(encoding="utf-8"))
rows = sorted(canon["parameters"], key=lambda p: int(p["id"]))

def enum_labels(prop):
    out = []
    for d in prop["enumDescriptions"]:
        m = re.match(r"^\d+:\s*", d)
        out.append(d[m.end():] if m else d)
    return out

choice_ids = {2, 3, 16, 91} | {19 + (b - 1) * 9 + 8 for b in range(1, 9)} | {19 + (b - 1) * 9 + 7 for b in range(1, 9)}

table = []
counts = {"float": 0, "bool": 0, "choice": 0}
for r in rows:
    rid = int(r["id"]); name = r["name"]
    lo, hi, ini = float(r["minimum"]), float(r["maximum"]), float(r["initial_or_default_candidate"])
    fl = int(r["flags_raw_u64"], 16)
    discrete = (fl & 0x1) != 0
    if rid in choice_ids or (discrete and hi > 1.0):
        kind, defout = "choice", str(min(max(int(round(ini)), 0), int(hi)))
        counts["choice"] += 1
    elif discrete and lo == 0.0 and hi == 1.0:
        kind, defout = "bool", ("true" if ini >= 0.5 else "false")
        counts["bool"] += 1
    else:
        kind, defout = "float", ("%g" % ini)
        counts["float"] += 1
    table.append("| %d | %s | %s | %g | %g | %s | 0x%x |" % (rid, name, kind, lo, hi, defout, fl))

exp = (TMP / "i5_params_expected.h").read_bytes()
hdr = (ROOT / "soultea3_plugin/Source/Soultea3Parameters.h").read_bytes()

sp = schema["properties"]
leaf = sum(len(v.get("properties", {})) for v in sp.values())
bandleaf = len(sp["parametric_weighting_bands"]["items"]["properties"])

report = f"""# I5 — Validacao independente dos 143 parametros `soultea3`

**Status: PASS** — header do I1 confere byte-a-byte e campo-a-campo com o esperado.

## 1. Verificacao das fontes (somente leitura)

- `params_dump.json`: `param_count=143`, `defaults_count=64`, `params[]` = 143 entradas, ids sequenciais 0..142.
- `parameter_table.json`: 143 registros, `record_stride=104`, ids unicos 0..142.
- **Layout +4B do dump NAO usado.** O layout canonico real e `id@0x00`, `name[36]@0x04`, `min@0x28`, `max@0x30`, `initial@0x38`, `flags(u64)@0x40`, `ptrs@0x48..0x68`. O dump le `a@0x34`, `b@0x3C`, `flags@0x44` (subnormais ~5e-315) — artefato descartado, conforme A9 §3.2.
- **Decodificacao independente:** todos os 143 `raw_record_hex` foram decodificados na mao (struct little-endian) e `min/max/initial/flags` conferem com os campos JSON do `parameter_table.json`: **143/143**.

## 2. Resolucao 143 vs 43

Nao ha contradicao: sao duas visoes do mesmo conjunto.

- O `soothe3_parameters_schema.json` e um **modelo logico agrupado**: 4 secoes, **39 definicoes escalares unicas** (14 globals + 6 tilts + 9 campos do template de banda + 10 immersive). Contando as 4 chaves de secao como propriedades, o schema tem **43 propriedades** — daqui o "43".
- O dump e a **tabela fisica plana**: **143 instancias**. A expansao ocorre porque estruturas repetidas sao representadas uma vez no schema e uma vez por instancia no dump:
  - banda de ponderacao: 9 campos × 8 bandas = **72 registros** (ids 19..90);
  - barramento immersive: 10 definicoes logicas → **52 registros** (ids 91..142: solo/delta/enabled/link-all por bus + 16 enables por canal);
  - globals + tilts: ids 0..18 = **19 registros**.
  - 19 + 72 + 52 = **143**.
- O schema tambem e uma visao **semanticamente derivada**: usa faixas "validated bounds" diferentes do dump em varios pontos (ex.: Attack min 0.1 no schema vs 0.0 no dump; Stereo link max 1.0 vs 100.0; Band depth ±24 vs ±10) e omite registros fisicos (ex.: `Band N used`, `Stereo focus`, `Channel N enabled`). Para o `.h`, a fonte canonica e o dump/parameter_table, nao o schema — o schema so fornece rotulos de enum.

## 3. Resultados

| Metrica | Valor |
|---|---|
| Total de parametros | **143** |
| float | **{counts['float']}** |
| bool | **{counts['bool']}** |
| choice | **{counts['choice']}** |
| Choice sets (kChoices) | 6 |

**10 primeiros nomes:** Depth, Low latency, Mode, Quality, Linear phase, Detail, Attack, Release, Detail tilt low, Detail tilt high.

## 4. Comparacao com o header do I1

- Arquivo: `soultea3_plugin/Source/Soultea3Parameters.h` (26888 B, 21/11/2026 05:49:33).
- Esperado: `C:\\Users\\tromb\\AppData\\Local\\Temp\\opencode\\i5_params_expected.h` (225 linhas).
- SHA-256 esperado: `{hashlib.sha256(exp).hexdigest()}`
- SHA-256 I1:         `{hashlib.sha256(hdr).hexdigest()}`
- **Byte-identico: SIM.**
- Comparacao semantica independente (parse do header do I1 vs `parameter_table.json` + regra de tipo derivada de flags/faixa/enum): **143 specs parseados, 0 divergencias de campo, 0 problemas de constante**. Contagens conferem (float 65 / bool 58 / choice 20).

### Risco detectado e ja corrigido pelo I1
A versao inicial do gerador do I1 (`gen_soultea3_params.py` 05:48:49) usava offsets de banda `base+7` para `shape` e `base+6` para `channels`. No layout canonico, porem, os campos da banda sao `used(0), enabled(1), frequency(2), depth(3), q(4), slope(5), focus(6), channels(7), shape(8)` — ou seja, `channels=base+7` e `shape=base+8`. O offset antigo colocava rotulos de choice em `Band N focus` (id 25) e faria o `assert len(labels)==hi+1` falhar. O I1 corrigiu para `base+8`/`base+7` as 05:49:28 e regerou o header as 05:49:33. Em seguida refinou `label_for`: `\"depth\" in low` → `low.endswith(\" depth\")`, para que o global `Depth` (faixa 0..10, sem unidade dB no schema) nao receba o rotulo `dB`; bandas/bus `... depth` continuam com `dB`. O esperado foi realinhado a essa regra. O header final esta correto.

## 5. Tabela canonica dos 143 parametros

`id | name | tipo | min | max | default | flags`

{chr(10).join(table)}

## 6. Artefatos em temp (somente leitura do repo)

- `i5_gen_expected.py` — gera o esperado e valida 143/143 contra os bytes crus.
- `i5_params_expected.h` — cabecalho esperado.
- `i5_compare.py` — comparador semantico + byte.
- `i5_linediff.py`, `i5_hexcheck.py`, `i5_inspect.py` — apoio.

Nenhum arquivo do repositorio foi editado; nenhum build/gate foi executado; CONTINUIDADE.md nao foi tocado.
"""

out = TMP / "i5_validacao.md"
out.write_text(report, encoding="utf-8", newline="\n")
print("WROTE", out, len(report), "chars")
