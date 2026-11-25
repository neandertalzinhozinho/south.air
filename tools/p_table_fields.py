#!/usr/bin/env python3
"""Dump the 143 parameter descriptors at 0x238E9B0 (step 0x68) and the
qword fields at +0x00/+0x08/+0x50/+0x58/+0x60, resolved to RVAs."""
import sys
sys.path.insert(0, r"D:\PROJETOS\soultree\tools")
from re_lib import u32, u64, cstr, BASE

T = 0x238E9B0
STEP = 0x68
N = 143


def rva(p):
    if 0x199B0000 <= p < 0x199B0000 + 0x100000000:
        return p - BASE
    return None


def main():
    fields = [0x00, 0x08, 0x50, 0x58, 0x60]
    seen = {f: {} for f in fields}
    print(f"{'i':>3} {'+0x10':>6} {'name':<40} " + " ".join(f"+{f:02X}" for f in fields))
    for i in range(N):
        e = T + i * STEP
        idx = u32(e + 0x10)
        name = cstr(e + 0x14, 0x2C)
        vals = []
        for f in fields:
            q = u64(e + f)
            r = rva(q)
            s = f"{r:#x}" if r is not None else f"{q:#x}"
            vals.append(s)
            seen[f].setdefault(s, []).append(i)
        flag = "" if idx == i else "  <-- idx mismatch"
        print(f"{i:>3} {idx:>6} {name:<40} " + " ".join(f"{v:>10}" for v in vals) + flag)
    print("\n== distinct ==")
    for f in fields:
        print(f"+{f:02X}: {len(seen[f])} distinct")
        for v, ids in sorted(seen[f].items()):
            print(f"   {v:>10}  n={len(ids):<3} first={ids[:8]}")


if __name__ == "__main__":
    main()
