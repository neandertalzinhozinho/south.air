import json
from pathlib import Path

F2 = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2")
for b in ("cand", "oracle"):
    ev = [json.loads(l) for l in open(F2 / f"e_presets_{b}.jsonl", encoding="utf-8") if l.startswith("{")]
    by = {}
    for e in ev:
        by.setdefault(e["event"], []).append(e)
    states = by["program_states"][0]["states"]
    fnvs = [s["fnv64"] for s in states]
    lens = {s["bytes"] for s in states}
    print(b, "programs", len(states), "unique_state_hashes", len(set(fnvs)), "state_sizes", lens)
    names = [n["name"] for n in by["program_names"][0]["names"]]
    print(" names", len(names), names[:5], "...", names[-2:])
    snaps = by["program_param_bits"][0]["snapshots"]
    print(" unique_param_snapshots", len({tuple(s["bits"]) for s in snaps}))
    print(" statuses", sorted({s["status"] for s in states}),
          "readback_sample", [round(s["readback"], 6) for s in states[:5]])
