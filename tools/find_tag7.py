#!/usr/bin/env python3
"""Find `mov dword ptr [<mem>], 7` writes in the image (candidate IPP spec tag)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib

d = re_lib.data()
LO, HI = 0x1000, 0x1CD5487
PAT = b"\x07\x00\x00\x00"


def modrm_len(modrm, has_sib_ok=True):
    mod = modrm >> 6
    rm = modrm & 7
    n = 0
    if mod != 3 and rm == 4:
        n += 1  # sib
    if mod == 1:
        n += 1
    elif mod == 2:
        n += 4
    elif mod == 0 and rm == 5:
        n += 4
    return n


hits = []
i = LO
while True:
    j = d.find(PAT, i, HI)
    if j < 0:
        break
    for s in range(max(LO, j - 12), j - 3):
        if d[s] != 0xC7:
            continue
        m = d[s + 1]
        if (m >> 3) & 7 != 0:
            continue
        if s + 1 + 1 + modrm_len(m) + 4 == j:
            hits.append(s)
            break
    i = j + 1

print("candidates", len(hits))
PC = []
for k in hits:
    # region check: IPP code island or general text
    print("0x%X  %s" % (k, d[k:k + 10].hex(" ")))
