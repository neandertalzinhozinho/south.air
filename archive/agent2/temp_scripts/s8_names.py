import json
from pathlib import Path

p = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase3\s8_bundle_names.jsonl")
raw = p.read_bytes()
text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8", errors="replace")
ev = {}
for line in text.splitlines():
    if line.startswith("{"):
        e = json.loads(line)
        ev.setdefault(e["event"], []).append(e)
print("events", list(ev))
print("program param", ev["program_parameter"][0])
names = ev["program_names"][0]["names"]
b = ev["program_param_bits"][0]["snapshots"]
print("names", len(names), names[:2])
print("snapshots", len(b), "params each", len(b[0]["bits"]), "unique", len({tuple(s["bits"]) for s in b}))

# compare against the E evidence for the loose module
for line in open(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2\e_presets_cand.jsonl", encoding="utf-8"):
    if '"program_name' in line or '"program_param_bits"' in line:
        e = json.loads(line)
        if e["event"] == "program_names":
            print("names equal to loose-module E run:", [n["name"] for n in e["names"]] == [n["name"] for n in names])
        else:
            print("snapshots equal to loose-module E run:",
                  [s["bits"] for s in e["snapshots"]] == [s["bits"] for s in b])
