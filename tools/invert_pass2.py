#!/usr/bin/env python3
"""Modela a 2a passada de 0x1D69E00 (01D6B09E..01D6B20C) e INVERTE-a para
recuperar a saida verdadeira da 1a passada a partir do WS medido.

Sem numpy: aritmetica em float64 e eliminacao de Gauss propria.
"""
import pathlib
import struct
import sys

order = int(sys.argv[1]) if len(sys.argv) > 1 else 9
mode = sys.argv[2] if len(sys.argv) > 2 else "imp"
root = pathlib.Path(__file__).resolve().parent.parent
path = root / "checks" / ".build" / f"j{order}_stage_{mode}.bits"
lines = [l.strip() for l in path.read_text().splitlines() if l.strip()]
NAMES = ("SRC", "KD", "WS", "FWD", "IDX", "TW38", "TW50")


def section(name):
    i = lines.index(name)
    out = []
    for l in lines[i + 1:]:
        if l in NAMES:
            break
        out.append(int(l, 16))
    return out


def f32(v):
    return struct.unpack("<f", struct.pack("<I", v))[0]


ws = [f32(v) for v in section("WS")]
tw = [f32(v) for v in section("TW38")]
n = len(ws)


def ld(d, off):
    i = off // 4
    return d[i:i + 8]


def perm(a, b, imm):
    if imm == 0x20:
        return a[:4] + b[:4]
    if imm == 0x31:
        return a[4:] + b[4:]
    raise ValueError(imm)


def dup4(off):
    v = tw[off // 4:off // 4 + 4]
    return v + v


def pass2_block(block):
    t8, t9, t10, t11, t12, t13 = (dup4(0x00), dup4(0x10), dup4(0x20),
                                  dup4(0x30), dup4(0x40), dup4(0x50))

    y0 = ld(block, 0x40)
    y15 = perm(y0, ld(block, 0x40 + 0x80), 0x20)
    y14 = perm(y0, ld(block, 0x40 + 0x80), 0x31)
    y0 = [t8[i] * y15[i] for i in range(8)]
    y1 = [t8[i] * y14[i] for i in range(8)]
    y0 = [-t9[i] * y14[i] + y0[i] for i in range(8)]
    y1 = [t9[i] * y15[i] + y1[i] for i in range(8)]

    y4 = ld(block, 0x60)
    y15b = perm(y4, ld(block, 0x60 + 0x80), 0x20)
    y14b = perm(y4, ld(block, 0x60 + 0x80), 0x31)
    y4 = [t12[i] * y15b[i] for i in range(8)]
    y5 = [t12[i] * y14b[i] for i in range(8)]
    y4 = [-t13[i] * y14b[i] + y4[i] for i in range(8)]
    y5 = [t13[i] * y15b[i] + y5[i] for i in range(8)]

    y2 = ld(block, 0x20)
    y15c = perm(y2, ld(block, 0x20 + 0x80), 0x20)
    y14c = perm(y2, ld(block, 0x20 + 0x80), 0x31)
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
    out[0x00:0x20] = perm(y2d, y14e, 0x20)
    out[0x80:0xa0] = perm(y2d, y14e, 0x31)
    out[0x40:0x60] = perm(y4d, y6, 0x20)
    out[0xc0:0xe0] = perm(y4d, y6, 0x31)

    y3u = [y5d[i] + y15d[i] for i in range(8)]
    y5u = [y5d[i] - y15d[i] for i in range(8)]
    y15u = [y7[i] - y0[i] for i in range(8)]
    y7u = [y7[i] + y0[i] for i in range(8)]
    out[0x20:0x40] = perm(y3u, y15u, 0x20)
    out[0xa0:0xc0] = perm(y3u, y15u, 0x31)
    out[0x60:0x80] = perm(y5u, y7u, 0x20)
    out[0xe0:0x100] = perm(y5u, y7u, 0x31)
    return out


def solve(M, b):
    """Gauss com pivoteamento parcial."""
    n = len(b)
    A = [row[:] + [b[i]] for i, row in enumerate(M)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / pv
            if f:
                for k in range(c, n + 1):
                    A[r][k] -= f * A[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = A[r][n] - sum(A[r][k] * x[k] for k in range(r + 1, n))
        x[r] = s / A[r][r]
    return x


M = [[0.0] * 64 for _ in range(64)]
for i in range(64):
    e = [0.0] * 64
    e[i] = 1.0
    col = pass2_block(e)
    for r in range(64):
        M[r][i] = col[r]

for b in range(0, n, 64):
    x = solve(M, ws[b:b + 64])
    nz = [(i, round(v, 6)) for i, v in enumerate(x) if abs(v) > 1e-6]
    print(f"bloco {b//64}: pass1 -> {len(nz)} nz {nz[:16]}")
