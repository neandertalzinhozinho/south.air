import json
from pathlib import Path

p = Path(r"D:\PROJETOS\shadowFILES\analysis\startup_audit\uni46c_s3_gate.json")
d = json.loads(p.read_text(encoding="utf8"))

def shape(o, depth=0, key=""):
    pad = "  " * depth
    if isinstance(o, dict):
        print(f"{pad}{key}: dict[{len(o)}] keys={list(o)[:12]}")
        if depth < 2:
            for k in list(o)[:6]:
                shape(o[k], depth + 1, k)
    elif isinstance(o, list):
        print(f"{pad}{key}: list[{len(o)}]")
        if o and depth < 3:
            shape(o[0], depth + 1, "[0]")
    else:
        s = str(o)
        print(f"{pad}{key}: {type(o).__name__} = {s[:80]}")

shape(d)
