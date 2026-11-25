"""Gera Soultea3Parameters.h a partir dos 143 registros canonicos.

Fontes (somente leitura):
  analysis/recovered_native/dsp/params_dump.json   -> ids/nomes/count (layout +4B, nao usar a/b/flags)
  analysis/parameter_table.json                    -> min/max/initial/flags canonicos (@0x28/@0x30/@0x38/@0x40)
  soothe3_reconstructed_engine/soothe3_parameters_schema.json -> rotulos de enum

Saida: soultea3_plugin/Source/Soultea3Parameters.h
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"D:\PROJETOS\shadowFILES")
DUMP = ROOT / "analysis/recovered_native/dsp/params_dump.json"
CANON = ROOT / "analysis/parameter_table.json"
SCHEMA = ROOT / "soothe3_reconstructed_engine/soothe3_parameters_schema.json"
OUT = ROOT / "soultea3_plugin/Source/Soultea3Parameters.h"
EXPECTED_COUNT = 143


def cstr(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def slug(value: str) -> str:
    out = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return out or "unnamed"


# --- carrega e valida as tres fontes -------------------------------------------------
dump = json.loads(DUMP.read_text(encoding="utf-8"))
canon = json.loads(CANON.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

assert int(dump["param_count"]) == EXPECTED_COUNT, dump["param_count"]
assert len(dump["params"]) == EXPECTED_COUNT
assert len(canon["parameters"]) == EXPECTED_COUNT
assert len(set(p["id"] for p in canon["parameters"])) == EXPECTED_COUNT

dump_by_id = {int(p["id"]): p for p in dump["params"]}
rows = sorted(canon["parameters"], key=lambda p: int(p["id"]))
for row in rows:
    rid = int(row["id"])
    assert rid in dump_by_id, rid
    assert dump_by_id[rid]["name"] == row["name"], (rid, dump_by_id[rid]["name"], row["name"])

# Rotulos de enum do schema (usados apenas para Choice; valores numericos vem do dump).
def schema_prop(section: str, key: str):
    return schema["properties"][section]["properties"][key]

def enum_labels(prop):
    out = []
    for description in prop["enumDescriptions"]:
        match = re.match(r"^\d+:\s*", description)
        out.append(description[match.end():] if match else description)
    return out


mode_labels = ["Soft", "Hard"]
quality_labels = enum_labels(schema_prop("engine_globals", "Quality"))
stereo_mode_labels = enum_labels(schema_prop("immersive_and_surround_bus", "Stereo mode"))
band_item_props = schema["properties"]["parametric_weighting_bands"]["items"]["properties"]
band_shape_labels = enum_labels({"enumDescriptions": band_item_props["shape"]["enumDescriptions"]})
band_channel_labels = enum_labels({"enumDescriptions": band_item_props["channels"]["enumDescriptions"]})
band_solo_labels = ["Off"] + [f"Band {b}" for b in range(1, 9)]

# IDs historicos still consumidos por PluginEditor.cpp / syncParametersToEngine().
# mapa: dump id -> ID JUCE antigo (evita duplicata e mantem UI/engine funcionando).
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
assert len(legacy) == 56, len(legacy)  # 10 globais + 6 tilts + 8 bandas x 5 = 56 push_back antigos
assert all(rid < EXPECTED_COUNT for rid in legacy)

# Choice explicito por id dump; demais seguem a regra de flags.
choice_overrides: dict[int, list[str]] = {
    2: mode_labels,
    3: quality_labels,
    16: stereo_mode_labels,
    91: band_solo_labels,
}
for band in range(1, 9):
    choice_overrides[19 + (band - 1) * 9 + 8] = band_shape_labels
    nch = int(rows[19 + (band - 1) * 9 + 7]["maximum"])
    choice_overrides[19 + (band - 1) * 9 + 7] = (
        band_channel_labels + [f"Channel {i}" for i in range(len(band_channel_labels), nch + 1)]
    )

# --- monta as tabelas deChoice e os registros ----------------------------------------
choice_sets: list[tuple[str, list[str]]] = []
choice_symbol: dict[tuple[str, ...], str] = {}


def choice_sym(labels: list[str]) -> str:
    key = tuple(labels)
    if key not in choice_symbol:
        symbol = "kChoices" + str(len(choice_sets))
        choice_sets.append((symbol, labels))
        choice_symbol[key] = symbol
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


lines: list[str] = []
ids_seen: set[str] = set()
counts = {"Float": 0, "Bool": 0, "Choice": 0}
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
        labels = choice_overrides.get(rid)
        if labels is None:
            n = int(hi) + 1
            labels = [str(i) for i in range(n)]
        assert len(labels) == int(hi) + 1, (rid, name, len(labels), hi)
        default_index = min(max(int(round(init)), 0), len(labels) - 1)
        sym = choice_sym(labels)
        extra = f"{sym}, {len(labels)}, {default_index}"
        interval, skew = 1.0, 1.0
        init_out = float(default_index)
        label = ""
    elif discrete and lo == 0.0 and hi == 1.0:
        kind = "Bool"
        extra = "nullptr, 0, 0"
        interval, skew = 1.0, 1.0
        init_out = 1.0 if init >= 0.5 else 0.0
        label = ""
    else:
        kind = "Float"
        extra = "nullptr, 0, 0"
        interval = 1.0 if "frequency" in name.lower() else interval_for(lo, hi)
        skew = 0.3 if "frequency" in name.lower() else 1.0
        init_out = init
        label = label_for(name)

    ident = legacy.get(rid, f"sp{rid:03d}_{slug(name)}")
    assert ident not in ids_seen, ident
    ids_seen.add(ident)
    counts[kind] += 1

    def f(value: float) -> str:
        text = repr(float(value))
        if "." not in text and "e" not in text:
            text += ".0"
        return text + "f"

    lines.append(
        "    { %3d, %-32s, %-46s, %s, %s, %s, 0x%xULL, Kind::%s, %s, %s, %s, %s }," % (
            rid, cstr(ident), cstr(name), f(lo), f(hi), f(init_out),
            flags, kind, extra, f(interval), f(skew), cstr(label)))

# --- escreve o header ---------------------------------------------------------------
choice_lines: list[str] = []
for sym, labels in choice_sets:
    choice_lines.append(f"inline constexpr const char* const {sym}[] = {{")
    for chunk_start in range(0, len(labels), 8):
        choice_lines.append("    " + ", ".join(cstr(x) for x in labels[chunk_start:chunk_start + 8]) + ",")
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
print("wrote", OUT)
print("count", EXPECTED_COUNT, counts)
print("legacy ids", len(legacy), "choice sets", len(choice_sets))
print("examples:", [(r["id"], r["name"]) for r in rows[:6]])
