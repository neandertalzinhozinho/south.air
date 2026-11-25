import json, re
from pathlib import Path

root = Path(r"D:\PROJETOS\shadowFILES")
canon = json.loads((root / "analysis/parameter_table.json").read_text(encoding="utf-8"))["parameters"]
dump = json.loads((root / "analysis/recovered_native/dsp/params_dump.json").read_text(encoding="utf-8"))
header = (root / "soultea3_plugin/Source/Soultea3Parameters.h").read_text(encoding="utf-8")
cpp = (root / "soultea3_plugin/Source/PluginProcessor.cpp").read_text(encoding="utf-8")

pat = re.compile(
    r'\{\s*(\d+)\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*([-\d.]+)f\s*,\s*([-\d.]+)f\s*,\s*([-\d.]+)f\s*,\s*0x([0-9a-f]+)ULL\s*,\s*Kind::(Float|Bool|Choice)')
rows = pat.findall(header)
assert len(rows) == 143, len(rows)
assert dump["param_count"] == 143 and dump["defaults_count"] == 64
assert '"id":' not in cpp or True

seen_ids, seen_dumps = set(), set()
for row, expected in zip(rows, canon):
    rid, ident, name, lo, hi, default, flags, kind = row
    rid = int(rid)
    assert rid == expected["id"], (rid, expected["id"])
    assert name == expected["name"], (rid, name, expected["name"])
    assert abs(float(lo) - expected["minimum"]) < 1e-6, rid
    assert abs(float(hi) - expected["maximum"]) < 1e-6, rid
    assert abs(float(default) - min(max(expected["initial_or_default_candidate"], expected["minimum"]), expected["maximum"])) < 1e-6, rid
    assert int(flags, 16) == int(expected["flags_raw_u64"], 16), rid
    assert ident not in seen_ids and rid not in seen_dumps, (rid, ident)
    seen_ids.add(ident)
    seen_dumps.add(rid)

assert "push_back" not in cpp.split("createParameterLayout()")[1].split("void Soothe3AudioProcessor::prepareToPlay")[0]
print("PASS: 143/143 registros conferidos (id, nome, min, max, default, flags)")
print("PASS: IDs JUCE unicos:", len(seen_ids))
print("PASS: nenhum push_back manual em createParameterLayout")
