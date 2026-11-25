import json
from pathlib import Path

D = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2\dumps")


def load(data):
    text = data.decode("utf-8", errors="replace")
    end = text.rfind("}")
    return json.loads(text[: end + 1]), text[end + 1:]


for k in (38, 39, 45, 52, 53):
    a = (D / f"cand.program_{k}.bin").read_bytes()
    b = (D / f"oracle.program_{k}.bin").read_bytes()
    ja, ta = load(a)
    jb, tb = load(b)
    print(f"--- program {k}: cand {len(a)}B oracle {len(b)}B equal={a == b} tail_cand={ta!r} tail_orc={tb!r}")
    for key in sorted(set(ja) | set(jb)):
        va, vb = ja.get(key, "<missing>"), jb.get(key, "<missing>")
        if va != vb:
            print(f"   {key}: cand={json.dumps(va)[:300]}")
            print(f"   {' ' * len(key)}  orc={json.dumps(vb)[:300]}")
        elif isinstance(va, list) and va and isinstance(va[0], dict):
            for i, (ea, eb) in enumerate(zip(va, vb)):
                if ea != eb:
                    diffkeys = [x for x in ea if ea.get(x) != eb.get(x)]
                    print(f"   {key}[{i}] differs in {diffkeys}")
                    for x in diffkeys:
                        print(f"       {x}: cand={json.dumps(ea.get(x))[:150]} orc={json.dumps(eb.get(x))[:150]}")
