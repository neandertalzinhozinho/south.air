import hashlib
import json
from pathlib import Path

F2 = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2")
D = F2 / "dumps"


def by_event(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        if line.startswith("{"):
            e = json.loads(line)
            out.setdefault(e["event"], []).append(e)
    return out


c = by_event(F2 / "e_presets_cand.jsonl")
o = by_event(F2 / "e_presets_oracle.jsonl")

cs = c["program_states"][0]["states"]
os_ = o["program_states"][0]["states"]
print("programs", len(cs), len(os_))
print("probe IUnitInfo exposed:", c["unit_info_probe"][0]["exposed"], o["unit_info_probe"][0]["exposed"])
print("program param:", c["program_parameter"][0], "|", o["program_parameter"][0])

cn = [n["name"] for n in c["program_names"][0]["names"]]
on = [n["name"] for n in o["program_names"][0]["names"]]
print("names equal:", cn == on, "count", len(cn))

print("index values equal:", [s["current_program_index"] for s in cs] == [s["current_program_index"] for s in os_])
bad_idx = [(k, cs[k]["current_program_index"], os_[k]["current_program_index"])
           for k in range(len(cs)) if cs[k]["current_program_index"] != os_[k]["current_program_index"]]
print("index mismatches:", bad_idx)

bad_fnv = [k for k in range(len(cs)) if cs[k]["fnv64"] != os_[k]["fnv64"]]
print("fnv mismatches:", bad_fnv)

raw_bad = []
for k in range(len(cs)):
    pa, pb = D / f"cand.program_{k}.bin", D / f"oracle.program_{k}.bin"
    if hashlib.sha256(pa.read_bytes()).hexdigest() != hashlib.sha256(pb.read_bytes()).hexdigest():
        raw_bad.append((k, pa.stat().st_size, pb.stat().st_size))
print("raw sha mismatches:", raw_bad)

cb = c["program_param_bits"][0]["snapshots"]
ob = o["program_param_bits"][0]["snapshots"]
pbad = [k for k in range(len(cb)) if cb[k]["bits"] != ob[k]["bits"]]
print("param snapshot mismatches:", pbad)
print("unique param snapshots cand/oracle:",
      len({tuple(s["bits"]) for s in cb}), len({tuple(s["bits"]) for s in ob}))
print("unique state bytes cand/oracle:",
      len({s["fnv64"] for s in cs}), len({s["fnv64"] for s in os_}))

print()
for tag in ("cand", "oracle"):
    ev = by_event(F2 / f"e_presets_{tag}.jsonl")
    print(tag, "program_reload:", ev["program_reload"][0])
    for r in ev["program_audio"][0]["runs"]:
        print("   audio", r)
