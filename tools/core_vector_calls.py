"""Count which vector primitives the core orchestrator actually calls.

Reads docs/engine/decomp/808B3ED0.c and tallies FUN_1800010xx/11xx/12xx/13xx/15xx
calls, then joins with checks/vector_primitives.txt to print the op for each.
"""
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ops = {}
for line in (ROOT / "checks" / "vector_primitives.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"0x([0-9A-F]+)\s+idx=\d+\s+impl=0x([0-9A-F]+)\s+insns=\d+\s+(\S+)", line)
    if m:
        ops[int(m.group(1), 16)] = (m.group(2), m.group(3))

calls = Counter()
for src in (ROOT / "docs" / "engine" / "decomp" / "808B3ED0.c",):
    text = src.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"FUN_18000(1[0-9A-F]{3})\(", text):
        calls[int(m.group(1), 16)] += 1

lines = ["# vector primitives called by 0x8B3ED0 (core orchestrator)", ""]
total = 0
for rva, n in sorted(calls.items(), key=lambda kv: -kv[1]):
    impl, sig = ops.get(rva, ("?", "not-a-primitive"))
    lines.append("0x%05X  x%-3d  impl=0x%05X  %s" % (rva, n, int(impl, 16) if impl != "?" else 0, sig))
    total += n
lines.append("")
lines.append("total vector calls in 0x8B3ED0: %d" % total)
text = "\n".join(lines)
(ROOT / "checks" / "core_vector_calls.txt").write_text(text, encoding="utf-8")
print(text)
