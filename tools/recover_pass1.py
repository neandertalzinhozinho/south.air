#!/usr/bin/env python3
"""Recupera a saida VERDADEIRA da 1a passada de 0x1D69E00 invertendo o mapa
medido (passada 2 + passada 3a) sobre o WS lido do plugin.

Modelos transcritos de checks/.build/1d69e00_full.dis:
  passada 2 : 01D6B03A..01D6B20C  (radix-8, bloco de 64 floats)
  passada 3a: 01D6B8C9..01D6BA2C  (radix-4 in place, bloco de 128 floats,
                                   twiddles reiniciados em tw+0 a cada outer)
Uso: py -3 tools/recover_pass1.py [modo]
"""
import pathlib
import struct
import sys

mode = sys.argv[1] if len(sys.argv) > 1 else "imp"
root = pathlib.Path(__file__).resolve().parent.parent
path = root / "checks" / ".build" / f"j9_stage_{mode}.bits"
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


ws_meas = [f32(v) for v in section("WS")]
tw = [f32(v) for v in section("TW38")]
N = 512


def ld(d, off):
    i = off // 4
    return d[i:i + 8]


def st(d, off, v):
    i = off // 4
    d[i:i + 8] = v


def perm(a, b, imm):
    return a[:4] + b[:4] if imm == 0x20 else a[4:] + b[4:]


def pass2_block(block):
    """block: lista de 64 floats. Transcricao de 01D6B09E..01D6B1F7."""
    def dup4(off):
        v = tw[off // 4:off // 4 + 4]
        return v + v

    t8, t9, t10, t11, t12, t13 = [dup4(o) for o in (0x00, 0x10, 0x20, 0x30, 0x40, 0x50)]

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


def pass2(ws):
    out = [0.0] * N
    for p in range(0, N * 4, 0x100):
        out[p // 4:p // 4 + 64] = pass2_block(ws[p // 4:p // 4 + 64])
    return out


def p3a_step(d, o, tb):
    """Radix-4 in place em 01D6B901..01D6BA0B. `o` e `tb` em BYTES."""
    t1, t2 = ld(tw, tb + 0x00), ld(tw, tb + 0x20)
    t3, t4 = ld(tw, tb + 0x40), ld(tw, tb + 0x60)
    t5, t6 = ld(tw, tb + 0x80), ld(tw, tb + 0xa0)

    c_re, c_im = ld(d, o + 0x100), ld(d, o + 0x120)
    y0 = [t1[i] * c_re[i] for i in range(8)]
    y1 = [t1[i] * c_im[i] for i in range(8)]
    y0 = [-t2[i] * c_im[i] + y0[i] for i in range(8)]
    y1 = [t2[i] * c_re[i] + y1[i] for i in range(8)]

    d_re, d_im = ld(d, o + 0x180), ld(d, o + 0x1a0)
    y9 = [t5[i] * d_re[i] for i in range(8)]
    y10 = [t5[i] * d_im[i] for i in range(8)]
    y9 = [-t6[i] * d_im[i] + y9[i] for i in range(8)]
    y10 = [t6[i] * d_re[i] + y10[i] for i in range(8)]

    b_re, b_im = ld(d, o + 0x80), ld(d, o + 0xa0)
    y2 = [t3[i] * b_re[i] for i in range(8)]
    y3 = [t3[i] * b_im[i] for i in range(8)]
    y2 = [-t4[i] * b_im[i] + y2[i] for i in range(8)]
    y3 = [t4[i] * b_re[i] + y3[i] for i in range(8)]

    y4 = [y9[i] + y0[i] for i in range(8)]
    y0 = [y0[i] - y9[i] for i in range(8)]
    y5 = [y10[i] + y1[i] for i in range(8)]
    y1 = [y1[i] - y10[i] for i in range(8)]

    y7 = ld(d, o + 0x00)
    y6 = [y7[i] - y2[i] for i in range(8)]
    y2 = [y7[i] + y2[i] for i in range(8)]
    st(d, o + 0x00, [y2[i] + y4[i] for i in range(8)])
    st(d, o + 0x100, [y2[i] - y4[i] for i in range(8)])

    y7 = ld(d, o + 0x20)
    y4 = [y7[i] - y3[i] for i in range(8)]
    y3 = [y7[i] + y3[i] for i in range(8)]
    st(d, o + 0x20, [y3[i] + y5[i] for i in range(8)])
    st(d, o + 0x120, [y3[i] - y5[i] for i in range(8)])

    st(d, o + 0x80, [y6[i] + y1[i] for i in range(8)])
    st(d, o + 0x180, [y6[i] - y1[i] for i in range(8)])
    st(d, o + 0xa0, [y4[i] - y0[i] for i in range(8)])
    st(d, o + 0x1a0, [y4[i] + y0[i] for i in range(8)])


def pass3a_block(ws):
    """Cada bloco de 128 floats (0x200 B) e independente: base=0, 2 passos.

    A base de twiddle vem de `rcx = rbx` em 01D6B216, depois de `add rbx,0x60`
    em 01D6B212; e reiniciada a cada outer em 01D6B8FA.
    """
    d = ws[:]
    for i in range(2):
        p3a_step(d, i * 0x40, 0x60 + i * 0xc0)
    return d


def composite_block128(x):
    """ws_apos_1 -> ws_apos_3a, para um bloco de 128 floats."""
    tmp = [0.0] * 128
    for k in range(2):
        tmp[64 * k:64 * k + 64] = pass2_block(x[64 * k:64 * k + 64])
    return pass3a_block(tmp)


def inv(M):
    n = len(M)
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        if abs(A[p][c]) < 1e-12:
            raise SystemExit(f"matriz singular na coluna {c}")
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [v / pv for v in A[c]]
        for r in range(n):
            if r != c and A[r][c]:
                f = A[r][c]
                A[r] = [A[r][k] - f * A[c][k] for k in range(2 * n)]
    return [row[n:] for row in A]


# --- matriz composta por bloco de 128 floats ---
def build_matrix():
    M = [[0.0] * 128 for _ in range(128)]
    for i in range(128):
        e = [0.0] * 128
        e[i] = 1.0
        col = composite_block128(e)
        for r in range(128):
            M[r][i] = col[r]
    return M


def main():
    M = build_matrix()
    Mi = inv(M)

    p1 = [0.0] * N
    for b in range(4):
        x = [ws_meas[b * 128 + r] for r in range(128)]
        y = [sum(Mi[r][c] * x[c] for c in range(128)) for r in range(128)]
        p1[b * 128:b * 128 + 128] = y

    nz = [(i, round(v, 6)) for i, v in enumerate(p1) if abs(v) > 1e-6]
    print(f"{path.name}: 1a passada recuperada -> {len(nz)} nao-zeros")
    print(nz[:64])


if __name__ == "__main__":
    main()
