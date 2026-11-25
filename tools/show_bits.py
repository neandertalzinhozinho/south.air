#!/usr/bin/env python3
"""Analisa checks/.build/j<order>_stage_<mode>.bits e imprime os nao-zeros."""
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


def as_f32(bits):
    return [struct.unpack("<f", struct.pack("<I", v))[0] for v in bits]


print(path.name)
for name in ("WS", "KD"):
    vals = as_f32(section(name))
    nz = [(i, round(v, 7)) for i, v in enumerate(vals) if abs(v) > 1e-9]
    print(f"{name}: {len(nz)} nao-zeros")
    print("   ", nz[:64])
