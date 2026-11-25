#!/usr/bin/env python3
"""Rank do modelo da 2a passada (transcricao literal)."""
import pathlib
import struct
import sys

mode = sys.argv[1] if len(sys.argv) > 1 else "imp"
lines = [l.strip() for l in (pathlib.Path(__file__).resolve().parent.parent / "checks" / ".build" / f"j9_stage_{mode}.bits").read_text().splitlines() if l.strip()]
NAMES = ("SRC", "KD", "WS", "FWD", "IDX", "TW38", "TW50")


def sec(n):
    i = lines.index(n)
    out = []
    for l in lines[i + 1:]:
        if l in NAMES:
            break
        out.append(int(l, 16))
    return out


def f32(v):
    return struct.unpack("<f", struct.pack("<I", v))[0]


tw = [f32(v) for v in sec("TW38")]


def dup4(off):
    v = tw[off // 4:off // 4 + 4]
    return v + v


def ld(d, o):
    i = o // 4
    return d[i:i + 8]


def perm(a, b, imm):
    return a[:4] + b[:4] if imm == 0x20 else a[4:] + b[4:]


def p2(block):
    t8, t9, t10, t11, t12, t13 = [dup4(o) for o in (0, 0x10, 0x20, 0x30, 0x40, 0x50)]
    y0 = ld(block, 0x40)
    y15 = perm(y0, ld(block, 0xc0), 0x20)
    y14 = perm(y0, ld(block, 0xc0), 0x31)
    y0 = [t8[i] * y15[i] for i in range(8)]
    y1 = [t8[i] * y14[i] for i in range(8)]
    y0 = [-t9[i] * y14[i] + y0[i] for i in range(8)]
    y1 = [t9[i] * y15[i] + y1[i] for i in range(8)]
    y4 = ld(block, 0x60)
    y15b = perm(y4, ld(block, 0xe0), 0x20)
    y14b = perm(y4, ld(block, 0xe0), 0x31)
    y4 = [t12[i] * y15b[i] for i in range(8)]
    y5 = [t12[i] * y14b[i] for i in range(8)]
    y4 = [-t13[i] * y14b[i] + y4[i] for i in range(8)]
    y5 = [t13[i] * y15b[i] + y5[i] for i in range(8)]
    y2 = ld(block, 0x20)
    y15c = perm(y2, ld(block, 0xa0), 0x20)
    y14c = perm(y2, ld(block, 0xa0), 0x31)
    y2 = [t10[i] * y15c[i] for i in range(8)]
    y3 = [t10[i] * y14c[i] for i in range(8)]
    y2 = [-t11[i] * y14c[i] + y2[i] for i in range(8)]
    y3 = [t11[i] * y15c[i] + y3[i] for i in range(8)]
    y7 = ld(block, 0x00)
    y6 = perm(y7, ld(block, 0x80), 0x20)
    y7 = perm(y7, ld(block, 0x80), 0x31)
    y14d = [y0[i] + y4[i] for i in range(8)]
    y0 = [y0[i] - y4[i] for i in range(8)]
    y15d = [y1[i] + y5[i] for i in range(8)]
    y1 = [y1[i] - y5[i] for i in range(8)]
    y4d = [y6[i] + y2[i] for i in range(8)]
    y6 = [y6[i] - y2[i] for i in range(8)]
    y5d = [y7[i] + y3[i] for i in range(8)]
    y7 = [y7[i] - y3[i] for i in range(8)]
    y2d = [y4d[i] + y14d[i] for i in range(8)]
    y4d = [y4d[i] - y14d[i] for i in range(8)]
    y14e = [y6[i] + y1[i] for i in range(8)]
    y6 = [y6[i] - y1[i] for i in range(8)]
    out = [0.0] * 64
    out[0:8] = perm(y2d, y14e, 0x20)
    out[32:40] = perm(y2d, y14e, 0x31)
    out[16:24] = perm(y4d, y6, 0x20)
    out[48:56] = perm(y4d, y6, 0x31)
    y3u = [y5d[i] + y15d[i] for i in range(8)]
    y5u = [y5d[i] - y15d[i] for i in range(8)]
    y15u = [y7[i] - y0[i] for i in range(8)]
    y7u = [y7[i] + y0[i] for i in range(8)]
    out[8:16] = perm(y3u, y15u, 0x20)
    out[40:48] = perm(y3u, y15u, 0x31)
    out[24:32] = perm(y5u, y7u, 0x20)
    out[56:64] = perm(y5u, y7u, 0x31)
    return out


M = [[0.0] * 64 for _ in range(64)]
for i in range(64):
    e = [0.0] * 64
    e[i] = 1.0
    c = p2(e)
    for r in range(64):
        M[r][i] = c[r]

if __name__ == "__main__":
    A = [row[:] for row in M]
    rank = 0
    piv = []
    for c in range(64):
        p = max(range(rank, 64), key=lambda r: abs(A[r][c]))
        if abs(A[p][c]) < 1e-9:
            continue
        A[rank], A[p] = A[p], A[rank]
        pv = A[rank][c]
        for r in range(rank + 1, 64):
            f = A[r][c] / pv
            if f:
                for k in range(c, 64):
                    A[r][k] -= f * A[rank][k]
        piv.append(c)
        rank += 1
    print("rank do modelo de pass2:", rank, "de 64")
    print("colunas sem pivo:", [c for c in range(64) if c not in piv])
