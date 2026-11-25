"""DEV I5 — gerador INDEPENDENTE do cabecalho esperado dos 143 parametros.

SOMENTE LEITURA das fontes. Saida: i5_params_expected.h (temp), NAO toca o repo.

Validacao independente aplicada ANTES de gerar:
  - param_count / defaults_count / ids / nomes do params_dump.json cruzados com
    analysis/parameter_table.json (layout canonico, NAO o +4B do dump).
  - Cada raw_record_hex e decodificado na mao (min@0x28, max@0x30, init@0x38,
    flags@0x40) e comparado aos campos JSON -> 143/143.

O formato de saida espelha o contrato publicado pelo I1
(temp/gen_soultea3_params.py) para que a comparacao byte-a-byte seja possivel.
"""
from __future__ import annotations

import json
import re
import struct
from pathlib import Path

ROOT = Path(r"D:\PROJETOS\shadowFILES")
DUMP = ROOT / "analysis/recovered_native/dsp/params_dump.json"
CANON = ROOT / "analysis/parameter_table.json"
SCHEMA = ROOT / "soothe3_reconstructed_engine/soothe3_parameters_schema.json"
OUT = Path(r"C:\Users\tromb\AppData\Local\Temp\opencode\i5_params_expected.h")
EXPECTED_COUNT = 143


def cstr(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_") or "unnamed"


def f(value: float) -> str:
    text = repr(float(value))
    if "." not in text and "e" not in text:
        text += ".0"
    return text + "f"


def enum_labels(prop: dict) -> list[str]:
    out = []
    for desc in prop["enumDescriptions"]:
        m = re.match(r"^\d+:\s*", desc)
        out.append(desc[m.end():] if m else desc)
    return out


# ---- carrega fontes --------------------------------------------------------------
dump = json.loads(DUMP.read_text(encoding="utf-8"))
canon = json.loads(CANON.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

assert int(dump["param_count"]) == EXPECTED_COUNT
assert len(dump["params"]) == EXPECTED_COUNT
assert len(canon["parameters"]) == EXPECTED_COUNT
assert len(set(p["id"] for p in canon["parameters"])) == EXPECTED_COUNT

dump_by_id = {int(p["id"]): p for p in dump["params"]}
rows = sorted(canon["parameters"], key=lambda p: int(p["id"]))

# ---- verificacao independenta: raw bytes vs JSON canonico ------------------------
hex_ok = 0
for row in rows:
    rid = int(row["id"])
    drow = dump_by_id[rid]
    assert drow["name"] == row["name"], (rid, drow["name"], row["name"])
    raw = bytes.fromhex(row["raw_record_hex"])
    assert len(raw) == 104, (rid, len(raw))
    assert struct.unpack_from("<I", raw, 0x00)[0] == rid
    assert raw[0x04:0x04+36].split(b"\0")[0].decode("ascii") == row["name"]
    mn = struct.unpack_from("<d", raw, 0x28)[0]
    mx = struct.unpack_from("<d", raw, 0x30)[0]
    ini = struct.unpack_from("<d", raw, 0x38)[0]
    fl = struct.unpack_from("<Q", raw, 0x40)[0]
    assert mn == float(row["minimum"]), (rid, mn, row["minimum"])
    assert mx == float(row["maximum"]), (rid, mx, row["maximum"])
    assert ini == float(row["initial_or_default_candidate"]), (rid, ini, row["initial_or_default_candidate"])
    assert fl == int(row["flags_raw_u64"], 16), (rid, fl, row["flags_raw_u64"])
    hex_ok += 1
assert hex_ok == EXPECTED_COUNT

# ---- rotulos de enum do schema ---------------------------------------------------
def sp(section: str, key: str):
    return schema["properties"][section]["properties"][key]

mode_labels = ["Soft", "Hard"]
quality_labels = enum_labels(sp("engine_globals", "Quality"))
stereo_labels = enum_labels(sp("immersive_and_surround_bus", "Stereo mode"))
band_item = schema["properties"]["parametric_weighting_bands"]["items"]["properties"]
band_shape_labels = enum_labels({"enumDescriptions": band_item["shape"]["enumDescriptions"]})
band_chan_labels = enum_labels({"enumDescriptions": band_item["channels"]["enumDescriptions"]})
solo_labels = ["Off"] + [f"Band {b}" for b in range(1, 9)]

# ---- IDs JUCE legados preservados (contrato I1) ----------------------------------
legacy: dict[int, str] = {
    0: "depth", 2: "mode", 5: "detail", 6: "attack", 7: "release",
    8: "detail_tilt_low", 9: "detail_tilt_high",
    10: "attack_tilt_low", 11: "attack_tilt_high",
    12: "release_tilt_low", 13: "release_tilt_high",
    92: "max_cut", 94: "mix", 95: "out_trim", 96: "delta", 97: "bypass",
}
for band in range(1, 9):
    base = 19 + (band - 1) * 9
    legacy[base + 1] = f"band_{band}_enabled"
    legacy[base + 2] = f"band_{band}_freq"
    legacy[base + 3] = f"band_{band}_depth"
    legacy[base + 4] = f"band_{band}_q"
    legacy[base + 8] = f"band_{band}_shape"
assert len(legacy) == 56

# ---- Choice por id (contrato I1) -------------------------------------------------
choice_overrides: dict[int, list[str]] = {
    2: mode_labels, 3: quality_labels, 16: stereo_labels, 91: solo_labels,
}
for band in range(1, 9):
    base = 19 + (band - 1) * 9
    choice_overrides[base + 8] = band_shape_labels
    nch = int(rows[base + 7]["maximum"])
    choice_overrides[base + 7] = band_chan_labels + [
        f"Channel {i}" for i in range(len(band_chan_labels), nch + 1)
    ]

choice_sets: list[tuple[str, list[str]]] = []
choice_symbol: dict[tuple[str, ...], str] = {}


def choice_sym(labels: list[str]) -> str:
    key = tuple(labels)
    if key not in choice_symbol:
        sym = "kChoices" + str(len(choice_sets))
        choice_sets.append((sym, labels))
        choice_symbol[key] = sym
    return choice_symbol[key]


def label_for(name: str) -> str:
    low = name.lower()
    if "frequency" in low:
        return "Hz"
    if low in ("max cut", "wet trim", "out trim") or low.endswith(" depth"):
        return "dB"
    if low in ("mix", "stereo link", "link all") or low.startswith("group link"):
        return "%"
    return ""


def interval_for(lo: float, hi: float) -> float:
    span = hi - lo
    if span <= 1.0:
        return 0.001
    if span <= 10.0:
        return 0.01
    if span <= 100.0:
        return 0.1
    return 1.0


# ---- monta registros -------------------------------------------------------------
lines: list[str] = []
ids_seen: set[str] = set()
counts = {"Float": 0, "Bool": 0, "Choice": 0}
canonical_list = []

for row in rows:
    rid = int(row["id"])
    name = str(row["name"])
    lo = float(row["minimum"])
    hi = float(row["maximum"])
    init = float(row["initial_or_default_candidate"])
    flags = int(row["flags_raw_u64"], 16)
    assert hi > lo, (rid, name)
    init = min(max(init, lo), hi)

    discrete = (flags & 0x1) != 0
    if rid in choice_overrides or (discrete and hi > 1.0):
        kind = "Choice"
        labels = choice_overrides.get(rid) or [str(i) for i in range(int(hi) + 1)]
        assert len(labels) == int(hi) + 1, (rid, name, len(labels), hi)
        default_index = min(max(int(round(init)), 0), len(labels) - 1)
        sym = choice_sym(labels)
        extra = f"{sym}, {len(labels)}, {default_index}"
        interval, skew, init_out, label = 1.0, 1.0, float(default_index), ""
    elif discrete and lo == 0.0 and hi == 1.0:
        kind = "Bool"
        extra = "nullptr, 0, 0"
        interval, skew = 1.0, 1.0
        init_out, label = (1.0 if init >= 0.5 else 0.0), ""
    else:
        kind = "Float"
        extra = "nullptr, 0, 0"
        interval = 1.0 if "frequency" in name.lower() else interval_for(lo, hi)
        skew = 0.3 if "frequency" in name.lower() else 1.0
        init_out, label = init, label_for(name)

    ident = legacy.get(rid, f"sp{rid:03d}_{slug(name)}")
    assert ident not in ids_seen, ident
    ids_seen.add(ident)
    counts[kind] += 1
    canonical_list.append((rid, ident, name, kind, lo, hi, init_out, flags))

    lines.append(
        "    { %3d, %-32s, %-46s, %s, %s, %s, 0x%xULL, Kind::%s, %s, %s, %s, %s }," % (
            rid, cstr(ident), cstr(name), f(lo), f(hi), f(init_out),
            flags, kind, extra, f(interval), f(skew), cstr(label)))

# ---- cabecalho ------------------------------------------------------------------
choice_lines: list[str] = []
for sym, labels in choice_sets:
    choice_lines.append(f"inline constexpr const char* const {sym}[] = {{")
    for start in range(0, len(labels), 8):
        choice_lines.append("    " + ", ".join(cstr(x) for x in labels[start:start + 8]) + ",")
    choice_lines.append("};")
    choice_lines.append("")

header = f"""#pragma once

// -----------------------------------------------------------------------------
// AUTO-GENERATED by temp/gen_soultea3_params.py -- NAO EDITAR A MAO.
// Fonte canonica: analysis/parameter_table.json (143 registros, stride 104),
//   min@0x28 / max@0x30 / initial@0x38 / flags@0x40.
// Cross-check: analysis/recovered_native/dsp/params_dump.json (param_count=143,
//   defaults_count=64). O layout +4B do dump (a@0x34/b@0x3c/flags@0x44) NAO e usado.
// Rotulos de enum: soothe3_reconstructed_engine/soothe3_parameters_schema.json.
// IDs JUCE: os 56 IDs historicos usados por PluginEditor.cpp/syncParametersToEngine
//   sao preservados (mapeados 1:1 pelo id do dump); os demais usam sp<id>_<nome>.
// Tipos: Float / Bool / Choice, decididos pelos bits de flags + faixa + overrides
//   de enum documentados no schema.
// -----------------------------------------------------------------------------

#include <cstdint>

namespace soultea3 {{
namespace params {{

enum class Kind : std::uint8_t {{ Float, Bool, Choice }};

struct Spec {{
    int dumpId;                 // id do registro no dump (0..142)
    const char* id;             // ID estavel usado no APVTS
    const char* name;           // nome exato do registro canonico
    float minValue;
    float maxValue;
    float defaultValue;
    std::uint64_t flags;        // flags cruzas do registro canonico (@0x40)
    Kind kind;
    const char* const* choices; // nao-nulo somente para Choice
    int choiceCount;
    int defaultChoice;
    float interval;
    float skew;
    const char* label;
}};

{chr(10).join(choice_lines)}
inline constexpr int kCount = {EXPECTED_COUNT};
inline constexpr int kLegacyCount = {len(legacy)};
inline constexpr int kDumpDefaultsCount = {int(dump['defaults_count'])};
inline constexpr const char* kCanonicalSource = "analysis/parameter_table.json";
inline constexpr const char* kDumpSource = "analysis/recovered_native/dsp/params_dump.json";

inline constexpr Spec kSpecs[kCount] = {{
{chr(10).join(lines)}
}};

inline const Spec* findByDumpId(int dumpId) noexcept {{
    if (dumpId < 0 || dumpId >= kCount) return nullptr;
    return &kSpecs[dumpId];
}}

}} // namespace params
}} // namespace soultea3
"""
OUT.write_text(header, encoding="utf-8", newline="\n")
print("WROTE", OUT)
print("TOTAL", EXPECTED_COUNT, counts)
print("FIRST10", [r[2] for r in canonical_list[:10]])
print("CHOICE_SETS", len(choice_sets))
print("HEX_VERIFIED", hex_ok, "/", EXPECTED_COUNT)
