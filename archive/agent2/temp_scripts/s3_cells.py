import json
from pathlib import Path

d = json.loads(Path(r"D:\PROJETOS\shadowFILES\analysis\startup_audit\uni46c_s3_gate.json").read_text(encoding="utf8"))
cells = d["cells"]
print("cells", len(cells))
from collections import Counter
print("kinds", Counter(c["kind"] for c in cells))
for c in cells[:6]:
    print(json.dumps(c)[:300])
print("---- cells with boolean false:", sum(1 for c in cells if not c["new_equal_oracle_all_runs_on_reference_stable_bytes"]))
for name, s in d["sections"].items():
    print(f"== {name}: rva={s['rva']} baseline_diff={s['baseline_constant_different_bytes']} "
          f"regressed={s['regressed_bytes']} improved={s['improved_bytes']} "
          f"regr_rvas={len(s['regression_rvas'])} cap_sha={s['fresh_capture_sha256'][:16]}")
    print("   semantic_heap_qwords:", s["semantic_heap_qwords"])
print("vector:", json.dumps(d["vector_0x26b39c0"])[:400])
