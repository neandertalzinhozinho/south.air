import json

d = json.load(open(r"D:\PROJETOS\shadowFILES\analysis\parameter_table.json", encoding="utf-8"))
ps = sorted(d["parameters"], key=lambda p: int(p["id"]))
for p in ps:
    print("%3d|%-34s|min=%9g|max=%9g|init=%9g|%s" % (
        p["id"], p["name"], p["minimum"], p["maximum"],
        p["initial_or_default_candidate"], p["flags_raw_u64"]))
