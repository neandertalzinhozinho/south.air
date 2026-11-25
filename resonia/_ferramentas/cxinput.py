"""Grava a entrada (script JS) e a saida de chamadas Codex pelos timestamps dados (HH-MM-SS)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events  # noqa: E402

outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)
want = sys.argv[2:]
for e in events.codex_events():
    k = e["ts"][11:19].replace(":", "-")
    if e["ts"].startswith("2026-11-22") and k in want:
        with open(os.path.join(outdir, "in_" + k + ".js"), "w", encoding="utf-8", newline="\n") as w:
            w.write(e["input"] if isinstance(e["input"], str) else repr(e["input"]))
        with open(os.path.join(outdir, "out_" + k + ".txt"), "w", encoding="utf-8", newline="\n") as w:
            w.write(str(e["output"]))
        print(k, len(e["input"]))
