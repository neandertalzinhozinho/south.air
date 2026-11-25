import hashlib
import json
from pathlib import Path

F2 = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2")
D = F2 / "dumps"


def by_event(path):
    ev = [json.loads(l) for l in open(path, encoding="utf-8") if l.startswith("{")]
    out = {}
    for e in ev:
        out.setdefault(e["event"], []).append(e)
    return out


c = by_event(F2 / "e_presets_cand.jsonl")
o = by_event(F2 / "e_presets_oracle.jsonl")
cs = c["program_states"][0]["states"]
os_ = o["program_states"][0]["states"]
diff = [k for k in range(len(cs)) if cs[k]["fnv64"] != os_[k]["fnv64"]]
print("per-program state fnv differences:", len(diff), diff[:20])
print("sizes cand", sorted({s['bytes'] for s in cs}), "oracle", sorted({s['bytes'] for s in os_}))

cbits = c["program_param_bits"][0]["snapshots"]
obits = o["program_param_bits"][0]["snapshots"]
pbad = [k for k in range(len(cbits)) if cbits[k]["bits"] != obits[k]["bits"]]
print("per-program param snapshot differences:", len(pbad), pbad[:20])

# raw bytes of the dumps
sbad = []
for k in range(len(cs)):
    pc = D / f"cand.program_{k}.bin"
    po = D / f"oracle.program_{k}.bin"
    if pc.exists() and po.exists():
        if hashlib.sha256(pc.read_bytes()).hexdigest() != hashlib.sha256(po.read_bytes()).hexdigest():
            sbad.append(k)
print("raw state byte differences:", len(sbad), sbad[:20])
print("first differing state dump sizes",
      (D / f"cand.program_{sbad[0]}.bin").stat().st_size if sbad else None,
      (D / f"oracle.program_{sbad[0]}.bin").stat().st_size if sbad else None)
