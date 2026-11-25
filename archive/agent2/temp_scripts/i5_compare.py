"""DEV I5 — comparador semantico independente do Soultea3Parameters.h do I1.

Parseia o header real e confere cada campo contra:
  - analysis/parameter_table.json (layout canonico, raw bytes decodificados)
  - params_dump.json (ids/nomes/count/defaults_count)
  - regra de tipo derivada de flags + faixa + enums do schema.
"""
import json
import re
import struct
from pathlib import Path

ROOT = Path(r"D:\PROJETOS\shadowFILES")
CANON = ROOT / "analysis/parameter_table.json"
DUMP = ROOT / "analysis/recovered_native/dsp/params_dump.json"
HEADER = ROOT / "soultea3_plugin/Source/Soultea3Parameters.h"
EXPECTED = Path(r"C:\Users\tromb\AppData\Local\Temp\opencode\i5_params_expected.h")

canon = json.loads(CANON.read_text(encoding="utf-8"))
dump = json.loads(DUMP.read_text(encoding="utf-8"))
rows = sorted(canon["parameters"], key=lambda p: int(p["id"]))

hdr = HEADER.read_text(encoding="utf-8") if HEADER.exists() else ""
issues = []

# --- constants -------------------------------------------------------------------
for token, want in [
    ("inline constexpr int kCount = 143;", None),
    ("inline constexpr int kLegacyCount = 56;", None),
    ("inline constexpr int kDumpDefaultsCount = 64;", None),
]:
    if token not in hdr:
        issues.append("missing constant: " + token)

# --- parse kSpecs -----------------------------------------------------------------
pat = re.compile(
    r'\{\s*(\d+),\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*([\d.eE+-]+)f,\s*([\d.eE+-]+)f,\s*([\d.eE+-]+)f,\s*'
    r'(0x[0-9a-fA-F]+)ULL,\s*Kind::(\w+),\s*(\w+|\w+),\s*(\d+),\s*(\d+),\s*([\d.eE+-]+)f,\s*([\d.eE+-]+)f,\s*"([^"]*)"\s*\}'
)
specs = pat.findall(hdr)
print("parsed specs:", len(specs))

counts = {"Float": 0, "Bool": 0, "Choice": 0}
field_bad = []
for s in specs:
    (rid, ident, name, lo, hi, dv, flags, kind, choices, nch, dch, interval, skew, label) = s
    rid = int(rid)
    if rid < 0 or rid >= len(rows):
        issues.append("spec dumpId out of range: %d" % rid)
        continue
    row = rows[rid]
    # posicao sequencial
    if rid != len(field_bad) + len([x for x in issues if x.startswith("spec")]) and False:
        pass
    exp_name = row["name"]
    exp_lo, exp_hi = float(row["minimum"]), float(row["maximum"])
    exp_flags = int(row["flags_raw_u64"], 16)
    got_lo, got_hi = float(lo), float(hi)
    got_flags = int(flags, 16)
    if name != exp_name:
        field_bad.append((rid, "name", name, exp_name))
    if abs(got_lo - exp_lo) > 1e-9:
        field_bad.append((rid, "min", got_lo, exp_lo))
    if abs(got_hi - exp_hi) > 1e-9:
        field_bad.append((rid, "max", got_hi, exp_hi))
    if got_flags != exp_flags:
        field_bad.append((rid, "flags", hex(got_flags), hex(exp_flags)))
    # tipo esperado (regra independente, derivada do dump)
    discrete = (exp_flags & 0x1) != 0
    choice_ids = {2, 3, 16, 91} | {19 + (b - 1) * 9 + 8 for b in range(1, 9)} | {19 + (b - 1) * 9 + 7 for b in range(1, 9)}
    if rid in choice_ids or (discrete and exp_hi > 1.0):
        exp_kind = "Choice"
    elif discrete and exp_lo == 0.0 and exp_hi == 1.0:
        exp_kind = "Bool"
    else:
        exp_kind = "Float"
    if kind != exp_kind:
        field_bad.append((rid, "kind", kind, exp_kind))
    if kind in counts:
        counts[kind] += 1
    # choice count coerente com faixa
    if kind == "Choice" and int(nch) != int(exp_hi) + 1:
        field_bad.append((rid, "choiceCount", nch, int(exp_hi) + 1))

print("counts:", counts)
print("field divergences:", len(field_bad))
for d in field_bad[:40]:
    print("  ", d)
print("constant/other issues:", len(issues))
for i in issues[:20]:
    print("  ", i)

# --- comparacao byte-a-byte com o esperado ----------------------------------------
exp_bytes = EXPECTED.read_bytes() if EXPECTED.exists() else b""
got_bytes = HEADER.read_bytes() if HEADER.exists() else b""
import hashlib
print("expected sha256:", hashlib.sha256(exp_bytes).hexdigest())
print("I1 header sha256:", hashlib.sha256(got_bytes).hexdigest())
print("BYTE IDENTICAL:", exp_bytes == got_bytes)
print("VERDICT:", "PASS" if (not field_bad and not issues and exp_bytes == got_bytes and len(specs) == 143) else "FAIL")
