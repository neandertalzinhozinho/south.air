import json
from pathlib import Path

D = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2\dumps")


def summary(data):
    s = json.loads(data.decode("utf-8", errors="replace"))
    return s


for k in (38, 39, 45, 52, 53):
    a = (D / f"cand.program_{k}.bin").read_bytes()
    b = (D / f"oracle.program_{k}.bin").read_bytes()
    print(f"--- program {k}: cand {len(a)}B oracle {len(b)}B equal={a == b}")
    try:
        ja, jb = summary(a), summary(b)
    except Exception as exc:
        print("   json parse failed:", exc)
        continue
    keys = sorted(set(ja) | set(jb))
    for key in keys:
        va, vb = ja.get(key, "<missing>"), jb.get(key, "<missing>")
        if va != vb:
            def brief(v):
                if isinstance(v, list):
                    return f"list[{len(v)}] first={json.dumps(v[0])[:120] if v else None} last={json.dumps(v[-1])[:120] if v else None}"
                return json.dumps(v)[:200]
            print(f"   {key}: cand={brief(va)}")
            print(f"   {' ' * len(key)}  orc={brief(vb)}")
        elif isinstance(va, list) and va and isinstance(va[0], dict):
            # check per-element differences anyway
            for i, (ea, eb) in enumerate(zip(va, vb)):
                if ea != eb:
                    diffkeys = [x for x in ea if ea.get(x) != eb.get(x)]
                    print(f"   {key}[{i}] differs in {diffkeys}")
                    for x in diffkeys:
                        print(f"       {x}: cand={json.dumps(ea.get(x))[:120]} orc={json.dumps(eb.get(x))[:120]}")
