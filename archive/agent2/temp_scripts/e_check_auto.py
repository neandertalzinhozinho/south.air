import json
from pathlib import Path

F2 = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2")

def by_event(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        if line.startswith("{"):
            e = json.loads(line)
            out.setdefault(e["event"], []).append(e)
    return out

res = {}
for scen in ("baseline", "a", "b", "c", "d"):
    res[scen] = {}
    for b in ("cand", "oracle"):
        ev = by_event(F2 / f"e_automation_{scen}_{b}.jsonl")
        runs = {r["tag"]: r for r in ev["run"]}
        r = runs.get(scen)
        res[scen][b] = r
        print(f"{scen:9s} {b:6s} fnv={r['fnv64']} peak={r['stats']['peak']:.9f} "
              f"nz={r['stats']['nonzero']} applied={json.dumps(r['automation_applied'])[:90]}")
    print()

print("cand == oracle per scenario:",
      {s: res[s]["cand"]["fnv64"] == res[s]["oracle"]["fnv64"] for s in res})
print("distinct hashes among scenarios (cand):",
      {res[s]["cand"]["fnv64"] for s in res})
print("baseline vs a/b/c/d differ (cand):",
      {s: res[s]["cand"]["fnv64"] != res["baseline"]["cand"]["fnv64"] for s in ("a", "b", "c", "d")})
