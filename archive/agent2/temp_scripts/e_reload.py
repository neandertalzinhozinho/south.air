import json
from pathlib import Path

F2 = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2")
D = F2 / "dumps"


def lines(path):
    raw = Path(path).read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16").splitlines()
    return raw.decode("utf-8", errors="replace").splitlines()


def names(path):
    for line in lines(path):
        if line.startswith("{") and '"program_names"' in line:
            return [n["name"] for n in json.loads(line)["names"]]
    return []


o = names(F2 / "e_presets_oracle.jsonl")
print("oracle[1:] == sorted(oracle[1:]):", o[1:] == sorted(o[1:]))
print("oracle sorted head:", sorted(o[1:])[:4], "actual head:", o[1:5])


def load(data):
    text = data.decode("utf-8", errors="replace")
    return json.loads(text[: text.rfind("}") + 1])


for tag in ("cand", "oracle"):
    src = load((D / f"{tag}.program_reload_source.bin").read_bytes())
    aft = load((D / f"{tag}.program_reload_after.bin").read_bytes())
    print(f"\n{tag}: source idx={src.get('current_program_index')} "
          f"after idx={aft.get('current_program_index')}")
    for key in sorted(set(src) | set(aft)):
        if src.get(key) != aft.get(key):
            a, b = src.get(key), aft.get(key)
            if isinstance(a, dict) and isinstance(b, dict):
                dd = [x for x in a if a[x] != b.get(x)]
                print(f"   {key} differs in {dd}")
                for x in dd[:5]:
                    print(f"      {x}: src={json.dumps(a[x])[:80]} after={json.dumps(b.get(x))[:80]}")
            else:
                print(f"   {key}: src={json.dumps(a)[:120]} after={json.dumps(b)[:120]}")
