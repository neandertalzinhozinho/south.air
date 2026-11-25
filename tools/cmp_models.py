#!/usr/bin/env python3
"""Compara celula a celula os dois modelos de pass2."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rank_pass2 as A  # noqa: E402
import recover_pass1 as B  # noqa: E402

bad = 0
worst = 0.0
for i in range(64):
    e = [0.0] * 64
    e[i] = 1.0
    a = A.p2(e)
    b = B.pass2_block(e)
    for r in range(64):
        d = abs(a[r] - b[r])
        if d > 1e-12:
            bad += 1
            worst = max(worst, d)
            if bad <= 10:
                print(f"col {i} linha {r}: rank_pass2={a[r]:.9f} recover={b[r]:.9f}")
print("diferencas:", bad, "pior:", worst)
print("tw iguais:", A.tw == B.tw, "len", len(A.tw), len(B.tw))
for k in range(24):
    if A.tw[k] != B.tw[k]:
        print("tw difere", k, A.tw[k], B.tw[k])
