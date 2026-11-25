import json
from pathlib import Path

F2 = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2")

def ev(name):
    out = {}
    for line in open(F2 / name, encoding="utf-8"):
        if line.startswith("{"):
            e = json.loads(line)
            out.setdefault(e["event"], []).append(e)
    return out

c = ev("e_presets_cand.jsonl")["program_names"][0]["names"]
o = ev("e_presets_oracle.jsonl")["program_names"][0]["names"]
for a, b in zip(c, o):
    if a["name"] != b["name"] or a["status"] != b["status"] or a["t"] != b["t"]:
        print(a["k"], "cand:", repr(a["name"]), a["status"], a["t"],
              "| oracle:", repr(b["name"]), b["status"], b["t"])
