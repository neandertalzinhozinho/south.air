#!/usr/bin/env python3
"""Modelo LITERAL da 1a passada de 0x1D69E00 (01D69EAC..01D6A16A).

Compara `pass1(src)` com a pass1 recuperada por inversao de pass2+pass3a
(tools/recover_pass1.py) para varios impulsos e para entrada aleatoria.
"""
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import recover_pass1 as R  # noqa: E402

NAMES = ("SRC", "KD", "WS", "FWD", "IDX", "TW38", "TW50")
ROOT = pathlib.Path(__file__).resolve().parent.parent
NEG_EVEN = [0x80000000 if i % 2 == 0 else 0 for i in range(8)]


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


def shuf4(a, b, imm):
    r = []
    for lane in (0, 4):
        r += [a[lane + (imm & 3)], a[lane + ((imm >> 2) & 3)],
              b[lane + ((imm >> 4) & 3)], b[lane + ((imm >> 6) & 3)]]
    return r


def unpcklpd(a, b):
    """`vunpcklpd` = intercala as palavras de 64 bits BAIXAS de cada lane.

    Nao e intercalacao de floats: por lane pega os floats {0,1} de cada
    operando -> [a0,a1,b0,b1 | a4,a5,b4,b5].
    """
    return [a[0], a[1], b[0], b[1], a[4], a[5], b[4], b[5]]


def unpckhpd(a, b):
    """`vunpckhpd` = palavras de 64 bits ALTAS de cada lane: {2,3} de cada."""
    return [a[2], a[3], b[2], b[3], a[6], a[7], b[6], b[7]]


def mul_i(v):
    """vshufps 0xb1 seguido de xor NEG_EVEN (multiplica por i)."""
    w = shuf4(v, v, 0xB1)
    bits = [struct.unpack("<I", struct.pack("<f", x))[0] for x in w]
    bits = [b ^ NEG_EVEN[i] for i, b in enumerate(bits)]
    return [struct.unpack("<f", struct.pack("<I", b))[0] for b in bits]


def swap_pairs(v):
    """vshufps 0xb1 puro (sem xor)."""
    return shuf4(v, v, 0xB1)


def neg_even(v):
    """vxorps com NEG_EVEN: nega as lanes pares."""
    bits = [struct.unpack("<I", struct.pack("<f", x))[0] for x in v]
    bits = [b ^ NEG_EVEN[i] for i, b in enumerate(bits)]
    return [struct.unpack("<f", struct.pack("<I", b))[0] for b in bits]


def butterfly(a, b, c, d):
    # 01D69EC0..01D69ED5: so `a-b` leva vshufps 0xb1; so `c-d` leva vxorps NEG_EVEN.
    t0 = [a[i] + b[i] for i in range(8)]
    t4 = swap_pairs([a[i] - b[i] for i in range(8)])
    t2 = [c[i] + d[i] for i in range(8)]
    t5 = neg_even([c[i] - d[i] for i in range(8)])
    X1 = [t0[i] + t2[i] for i in range(8)]
    X0 = [t0[i] - t2[i] for i in range(8)]
    Y1 = [t4[i] + t5[i] for i in range(8)]
    Y0 = [t4[i] - t5[i] for i in range(8)]
    p2 = unpcklpd(X1, Y1)
    p3 = unpckhpd(X1, Y1)
    p5 = unpcklpd(X0, Y0)
    p4 = unpckhpd(X0, Y0)
    return {
        "O1": shuf4(p2, p5, 0xCC),
        "O2": shuf4(p2, p5, 0x99),
        "O3": shuf4(p3, p4, 0xCC),
        "O4": shuf4(p3, p4, 0x99),
    }


def ld(src, off):
    """off em BYTES."""
    i = off // 4
    return src[i:i + 8]


def st(ws, off, v):
    i = off // 4
    ws[i:i + 4] = v


def _store_group(ws, r13, r14, off, o, rbp):
    st(ws, r13 + off + 0x00, o["O1"][0:4])
    st(ws, r13 + off + 0x10, o["O2"][0:4])
    st(ws, r14 + off + 0x00, o["O1"][4:8])
    st(ws, r14 + off + 0x10, o["O2"][4:8])
    st(ws, r13 + off + rbp * 4 + 0x00, o["O3"][0:4])
    st(ws, r13 + off + rbp * 4 + 0x10, o["O4"][0:4])
    st(ws, r14 + off + rbp * 4 + 0x00, o["O3"][4:8])
    st(ws, r14 + off + rbp * 4 + 0x10, o["O4"][4:8])


def pass1_model(src, idx):
    rbp = 0x100
    ws = [0.0] * 512
    r13 = 0
    r14 = 0x200
    base = 0
    cur = 16
    while True:
        def rd(d):
            return ld(src, base + d * 4)

        # Ordem real do corpo (01D69EAC..01D6A167):
        #  BF-A: le base+{0,256,128,384}   -> grava em 16i+0..7  (regioes 0..3)
        #  BF-B: le base+{64,320,192,448}  -> grava em 16i+8..15
        #  BF-C: le base+{8,136,264,392}   -> grava em 16i+64..71
        #  BF-D: le base+{72,328,200,456}  -> grava em 16i+72..79
        oa = butterfly(rd(0), rd(256), rd(128), rd(384))
        _store_group(ws, r13, r14, 0x00, oa, rbp)

        ob = butterfly(rd(64), rd(320), rd(192), rd(448))
        _store_group(ws, r13, r14, 0x20, ob, rbp)

        oc = butterfly(rd(8), rd(264), rd(136), rd(392))
        _store_group(ws, r13 + rbp, r14 + rbp, 0x00, oc, rbp)

        od = butterfly(rd(72), rd(328), rd(200), rd(456))
        _store_group(ws, r13 + rbp, r14 + rbp, 0x20, od, rbp)

        r13 += 0x40
        r14 += 0x40

        idx_val = idx[cur]
        cur += 16
        base = idx_val * 8 * 4   # idx*8 floats * 4 bytes
        if base == 0:
            break

    return ws


def main():
    M = R.build_matrix()
    Mi = R.inv(M)

    def recover(ws_u32):
        ws = [f32(v) for v in ws_u32]
        p1 = [0.0] * 512
        for b in range(4):
            x = ws[b * 128:b * 128 + 128]
            y = [sum(Mi[r][c] * x[c] for c in range(128)) for r in range(128)]
            p1[b * 128:b * 128 + 128] = y
        return p1

    modes = sys.argv[1:] or ["imp", "e1", "e2", "e3", "e4", "e8", "e16", "e32", "rand"]
    for mode in modes:
        d = load(mode)
        src = [f32(v) for v in d["SRC"]]
        idx = d["IDX"]
        got = pass1_model(src, idx)
        want = recover(d["WS"])
        err = max(abs(got[i] - want[i]) for i in range(512))
        nzg = [(i, round(v, 4)) for i, v in enumerate(got) if abs(v) > 1e-5]
        print(f"{mode:5s} max|modelo-recuperado|={err:.3e}  modelo_nz={len(nzg)} {nzg[:8]}")


if __name__ == "__main__":
    main()
