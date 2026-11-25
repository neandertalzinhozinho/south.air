#!/usr/bin/env python3
"""Resume os nao-zeros de WS/KD de um .bits e compara KD com a DFT exata."""
import cmath
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


def ranges(idxs):
    if not idxs:
        return "[]"
    out = []
    a = b = idxs[0]
    for i in idxs[1:]:
        if i == b + 1:
            b = i
        else:
            out.append(f"{a}" if a == b else f"{a}..{b}")
            a = b = i
    out.append(f"{a}" if a == b else f"{a}..{b}")
    return "[" + ", ".join(out) + "]"


src = as_f32(section("SRC"))
kd = as_f32(section("KD"))
ws = as_f32(section("WS"))
n = len(src)

print(f"{path.name}  n={n}")
for name, vals in (("WS", ws), ("KD", kd)):
    nz = [i for i, v in enumerate(vals) if abs(v) > 1e-9]
    print(f"{name}: {len(nz)} nz  {ranges(nz)}")
    print(f"    valores unicos: {sorted(set(round(v, 6) for v in vals if abs(v) > 1e-9))[:8]}")

# DFT exata da entrada (intercalada como pares complexos? ou real?)
x = [complex(v, 0.0) for v in src]
N = len(x)
dft = [sum(x[t] * cmath.exp(-2j * cmath.pi * k * t / N) for t in range(N)) for k in range(N // 2 + 1)]

for label, cand in (
    ("KD[2k]+iKD[2k+1]", [complex(kd[2 * k], kd[2 * k + 1]) for k in range(N // 2)]),
):
    errs = [abs(cand[k] - dft[k]) for k in range(N // 2)]
    print(f"{label} vs DFT: max err {max(errs):.3e}  (err em k=0..5: "
          + ", ".join(f"{e:.2e}" for e in errs[:6]) + ")")
