#!/usr/bin/env python3
"""Recupera a 1a passada de 0x1D69E00 para varios modos e valida reprojetando."""
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import recover_pass1 as R  # noqa: E402

NAMES = ("SRC", "KD", "WS", "FWD", "IDX", "TW38", "TW50")
root = pathlib.Path(__file__).resolve().parent.parent


def load(mode):
    p = root / "checks" / ".build" / f"j9_stage_{mode}.bits"
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


def f32(v):
    return struct.unpack("<f", struct.pack("<I", v))[0]


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


def forward(p1):
    out = [0.0] * 512
    for b in range(4):
        out[b * 128:b * 128 + 128] = R.composite_block128(p1[b * 128:b * 128 + 128])
    return out


modes = sys.argv[1:] or ["imp", "e1", "e2", "e3", "e4", "e8", "e16", "e32"]
for mode in modes:
    d = load(mode)
    ws = [f32(v) for v in d["WS"]]
    p1 = recover(d["WS"])
    # erro de reprojecao
    fw = forward(p1)
    err = max(abs(fw[i] - ws[i]) for i in range(512))
    nz = [(i, round(v, 5)) for i, v in enumerate(p1) if abs(v) > 1e-5]
    print(f"{mode:5s} reproj_err={err:.3e} pass1_nz={len(nz)} {nz[:10]}")
