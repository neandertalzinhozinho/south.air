#!/usr/bin/env python3
"""Emit the case -> descriptor-vector -> descriptor table for Stage C (0x85E6C0)."""
import json
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib

BASE = Path(r"D:\PROJETOS\soultree")

txt = (BASE / "checks" / "desc_vectors.txt").read_bytes().decode("utf-16", errors="replace")
vecs = {}
cur = None
for line in txt.splitlines():
    m = re.search(r"vec=(0x2754[0-9A-F]+)", line)
    if m:
        cur = m.group(1)
        vecs[cur] = []
        continue
    m = re.search(r"desc\[(\d+)\]\s+\+0=(\d+)\s+\+8=(\d+)\s+\+0x10=(\d+)", line)
    if m and cur:
        vecs[cur].append([int(m.group(i)) for i in (2, 3, 4)])

d = re_lib.data()
lines = (BASE / "checks" / "85e6c0.dis").read_bytes().decode("utf-16", errors="replace").splitlines()
addr = {}
for l in lines:
    if re.match(r"[0-9A-F]{8}\s", l):
        addr[int(l[:8], 16)] = l
order = sorted(addr)

EMPTY = "0x2752208"


def vec_for_case(i):
    t = struct.unpack_from("<i", d, 0x85FFA0 + 4 * i)[0] & 0xFFFFFFFF
    for a in order:
        if a < t:
            continue
        l = addr[a]
        m = re.search(r"lea\s+rax, \[rip.*;\s*(0x[0-9A-F]+)", l)
        if m:
            return m.group(1)
        if " ret" in l:
            return EMPTY
    return EMPTY


rows = []
for i in range(23):
    v = vec_for_case(i)
    rows.append({"case": i, "vec": v, "desc": vecs.get(v, [])})

(BASE / "checks" / "stage_c_table.json").write_text(json.dumps(rows, indent=1))
for r in rows:
    print("case %2d %s %s" % (r["case"], r["vec"], r["desc"]))
