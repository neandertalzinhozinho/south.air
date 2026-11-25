import json
from pathlib import Path

F2 = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2")


def lines(path):
    raw = Path(path).read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16").splitlines()
    return raw.decode("utf-8", errors="replace").splitlines()


def names(path):
    for line in lines(path):
        if line.startswith("{") and '"program_names"' in line:
            e = json.loads(line)
            return [n["name"] for n in e["names"]]
    return []


def bits(path):
    for line in lines(path):
        if line.startswith("{") and '"program_param_bits"' in line:
            e = json.loads(line)
            return [tuple(s["bits"]) for s in e["snapshots"]]
    return []


c = names(F2 / "e_presets_cand.jsonl")
o = names(F2 / "e_presets_oracle.jsonl")
i = names(F2 / "e_names_installed.jsonl")
print("counts", len(c), len(o), len(i))
print("set(cand)==set(oracle):", sorted(c) == sorted(o))
print("set(installed)==set(oracle):", sorted(i) == sorted(o))
print("cand == oracle order:", c == o)
print("installed == oracle order:", i == o)
print("installed == cand order:", i == c)
print()
print("k  cand                          oracle                        installed")
for k in range(69):
    print(f"{k:2d} {c[k][:29]:29s} {o[k][:29]:29s} {i[k][:29]:29s}")

bc = bits(F2 / "e_presets_cand.jsonl")
bo = bits(F2 / "e_presets_oracle.jsonl")
bi = bits(F2 / "e_names_installed.jsonl")
print()
print("param bits cand==oracle:", bc == bo, "count", len(bc), len(bo))
print("param bits installed==oracle:", bi == bo, "count", len(bi))
if bi and bo and bi != bo:
    print("differing k:", [k for k in range(min(len(bi), len(bo))) if bi[k] != bo[k]][:20])
