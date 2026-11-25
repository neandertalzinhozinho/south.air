#!/usr/bin/env python3
"""Cadeia completa (pass1..pass3b) de 0x1D69E00, comparada com o KD medido.

O KD do plugin e a verdade (CFFT de n/2 sobre pares intercalados). Se a cadeia
bater com KD para entrada aleatoria, todas as 4 passadas estao certas.
"""
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pass1_model as P1  # noqa: E402
import recover_pass1 as R  # noqa: E402

NAMES = ("SRC", "KD", "WS", "FWD", "IDX", "TW38", "TW50")
ROOT = pathlib.Path(__file__).resolve().parent.parent


def f32(v):
    return struct.unpack("<f", struct.pack("<I", v))[0]


def load(mode):
    p = ROOT / "checks" / ".build" / f"j9_stage_{mode}.bits"
    lines = [l.strip() for l in p.read_text().splitlines() if l.strip()]
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


def ld(buf, off):
    i = off // 4
    return buf[i:i + 8]


def st(buf, off, v):
    i = off // 4
    buf[i:i + 8] = v


def perm(a, b, imm):
    return a[:4] + b[:4] if imm == 0x20 else a[4:] + b[4:]


def unpcklps(a, b):
    return [a[0], b[0], a[1], b[1], a[4], b[4], a[5], b[5]]


def unpckhps(a, b):
    return [a[2], b[2], a[3], b[3], a[6], b[6], a[7], b[7]]


def cmul(t1, t2, re, im):
    """(t1 + i t2) * (re + i im), como vfnmadd/vfmadd: re' = t1*re - t2*im, im' = t1*im + t2*re."""
    r = [t1[i] * re[i] - t2[i] * im[i] for i in range(8)]
    m = [t1[i] * im[i] + t2[i] * re[i] for i in range(8)]
    return r, m


def pass2_all(ws):
    out = [0.0] * 512
    for p in range(0, 512 * 4, 0x100):
        out[p // 4:p // 4 + 64] = R.pass2_block(ws[p // 4:p // 4 + 64])
    return out


def pass3a_all(ws, tw):
    d = ws[:]
    for outer in range(4):
        base = outer * 0x200
        for i in range(2):
            R.p3a_step(d, base + i * 0x40, 0x60 + i * 0xc0)
    return d


def pass3b(ws, tw):
    dst = [0.0] * 512
    r10 = 0x200
    rax = 0x600
    r12 = 0
    r13 = 0
    rbx = 0x1E0
    for _ in range(8):
        a_re = ld(ws, r12 + 0x400)
        a_im = ld(ws, r12 + 0x420)
        t1 = ld(tw, rbx + 0x00)
        t2 = ld(tw, rbx + 0x20)
        are, aim = cmul(t1, t2, a_re, a_im)
        d_re = ld(ws, r12 + 0x600)
        d_im = ld(ws, r12 + 0x620)
        t5 = ld(tw, rbx + 0x80)
        t6 = ld(tw, rbx + 0xA0)
        dre, dim = cmul(t5, t6, d_re, d_im)
        b_re = ld(ws, r12 + 0x200)
        b_im = ld(ws, r12 + 0x220)
        t3 = ld(tw, rbx + 0x40)
        t4 = ld(tw, rbx + 0x60)
        bre, bim = cmul(t3, t4, b_re, b_im)
        rbx += 0xC0

        y4 = [dre[i] + are[i] for i in range(8)]
        y0 = [are[i] - dre[i] for i in range(8)]
        y5 = [dim[i] + aim[i] for i in range(8)]
        y1 = [aim[i] - dim[i] for i in range(8)]

        x0re = ld(ws, r12 + 0x00)
        y6 = [x0re[i] - bre[i] for i in range(8)]
        y2 = [x0re[i] + bre[i] for i in range(8)]
        o0 = [y2[i] + y4[i] for i in range(8)]
        o1 = [y2[i] - y4[i] for i in range(8)]

        x0im = ld(ws, r12 + 0x20)
        y4b = [x0im[i] - bim[i] for i in range(8)]
        y3 = [x0im[i] + bim[i] for i in range(8)]
        o2 = [y3[i] + y5[i] for i in range(8)]
        o3 = [y3[i] - y5[i] for i in range(8)]

        o4 = [y6[i] + y1[i] for i in range(8)]
        o5 = [y6[i] - y1[i] for i in range(8)]
        o6 = [y4b[i] - y0[i] for i in range(8)]
        o7 = [y4b[i] + y0[i] for i in range(8)]

        for src_a, src_b, off in ((o0, o2, 0x000), (o4, o6, 0x200),
                                  (o1, o3, 0x400), (o5, o7, 0x600)):
            i1 = unpcklps(src_a, src_b)
            i2 = unpckhps(src_a, src_b)
            st(dst, r13 + off, perm(i1, i2, 0x20))
            st(dst, r13 + off + 0x20, perm(i1, i2, 0x31))
        r12 += 0x40
        r13 += 0x40
    return dst


def full_model(src, tw, idx):
    ws = P1.pass1_model(src, idx)
    ws = pass2_all(ws)
    ws = pass3a_all(ws, tw)
    return pass3b(ws, tw), ws


def main():
    modes = sys.argv[1:] or ["rand", "imp", "e1", "e8"]
    for mode in modes:
        d = load(mode)
        src = [f32(v) for v in d["SRC"]]
        kd = [f32(v) for v in d["KD"]]
        ws_meas = [f32(v) for v in d["WS"]]
        tw = [f32(v) for v in d["TW38"]]
        idx = d["IDX"]
        got, ws3a = full_model(src, tw, idx)
        err_kd = max(abs(got[i] - kd[i]) for i in range(512))
        err_ws = max(abs(ws3a[i] - ws_meas[i]) for i in range(512))
        # erro relativo grosseiro
        scale = max(1e-9, max(abs(x) for x in kd))
        print(f"{mode:5s} max|modelo-KD|={err_kd:.3e} (rel {err_kd/scale:.2e})  "
              f"max|ws3a-WS|={err_ws:.3e}")


if __name__ == "__main__":
    main()
