#!/usr/bin/env python3
"""Compara os vetores de checks/j9_golden.rs com o .bits medido (modo rand)."""
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAMES = ("SRC", "KD", "WS", "FWD", "IDX", "TW38", "TW50")


def golden(name):
    txt = (ROOT / "checks" / "j9_golden.rs").read_text()
    m = re.search(r"pub static " + name + r": \[u32; (\d+)\] = \[(.*?)\];", txt, re.S)
    if not m:
        return None
    n = int(m.group(1))
    vals = [int(x, 16) for x in re.findall(r"0x[0-9a-fA-F]+", m.group(2))]
    assert len(vals) == n, (name, len(vals), n)
    return vals


def measured(mode):
    lines = [l.strip() for l in (ROOT / "checks" / ".build" / f"j9_stage_{mode}.bits").read_text().splitlines() if l.strip()]
    out = {}
    for nm in NAMES:
        i = lines.index(nm)
        vals = []
        for l in lines[i + 1:]:
            if l in NAMES:
                break
            vals.append(int(l, 16))
        out[nm] = vals
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "rand"
    d = measured(mode)
    for nm in ("SRC", "KD", "WS", "FWD", "IDX", "TW38", "TW50"):
        g = golden("J9_" + nm)
        m = d[nm]
        if g is None:
            print(f"{nm}: sem golden")
            continue
        if len(g) != len(m):
            print(f"{nm}: tamanho golden={len(g)} medido={len(m)}")
            continue
        bad = [i for i in range(len(g)) if g[i] != m[i]]
        print(f"{nm}: len={len(g)} diffs={len(bad)}" + (f" primeiros={bad[:6]}" if bad else ""))


if __name__ == "__main__":
    main()
