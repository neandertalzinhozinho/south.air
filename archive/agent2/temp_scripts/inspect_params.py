import json, collections
from pathlib import Path

root = Path(r"D:\PROJETOS\shadowFILES")
d = json.loads((root / "analysis/parameter_table.json").read_text(encoding="utf-8"))
p = d["parameters"]
print("count", len(p))
print("flags histogram:")
for k, v in sorted(collections.Counter(x["flags_raw_u64"] for x in p).items()):
    print(" ", k, v)
print()
print("id | name | min | max | init | flags")
for x in p:
    print("%3d | %-46s | %10.5g %10.5g %10.5g | %s" % (
        x["id"], x["name"][:46], x["minimum"], x["maximum"],
        x["initial_or_default_candidate"], x["flags_raw_u64"]))
print()
print("interpretation keys:", list(d.get("interpretation", {}).keys()) if isinstance(d.get("interpretation"), dict) else type(d.get("interpretation")))
print(json.dumps(d.get("interpretation"), indent=2, ensure_ascii=False)[:5000])
