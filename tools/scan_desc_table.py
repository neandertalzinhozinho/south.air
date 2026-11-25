#!/usr/bin/env python3
"""Look for a static table of 24-byte descriptor records in .data/.rdata.

Record (proved read layout, spec 18.4): +0 i32 A, +8 i32 index, +0x10 i32 type.
A run = >=3 consecutive records with plausible fields.
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib

d = re_lib.data()
REGIONS = [(".rdata", 0x1D8C000, 0x1D8C000 + 0x3F2D38),
           (".data", 0x217F000, 0x217F000 + 0x5D8DD8)]


def plausible(o):
    a, _p0, idx, _p1, typ, _p2 = struct.unpack_from("<6i", d, o)
    return (1 <= typ <= 40) and (0 <= idx < 0x1000) and (-0x10000 <= a <= 0x10000)


for name, lo, hi in REGIONS:
    best = []
    o = lo
    while o < hi - 24 * 3:
        if plausible(o) and plausible(o + 24) and plausible(o + 48):
            start = o
            n = 3
            while o + n * 24 < hi - 24 and plausible(o + n * 24):
                n += 1
            recs = [struct.unpack_from("<6i", d, start + k * 24) for k in range(min(n, 8))]
            best.append((n, start, recs))
            o = start + n * 24
        else:
            o += 4
    best.sort(reverse=True)
    print(f"\n### {name}: {len(best)} runs")
    for n, start, recs in best[:8]:
        print(f"  run {n} @ 0x{start:X}")
        for r in recs:
            print(f"    {r[0]:>8} pad={r[1]:>8} idx={r[2]:>4} pad={r[3]:>4} type={r[4]:>3} pad={r[5]}")
