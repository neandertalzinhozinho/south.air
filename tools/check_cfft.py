#!/usr/bin/env python3
"""Testa a hipotese: 0x1D69E00 = FFT complexa de tamanho m=n/2 sobre pares
intercalados (re=src[2t], im=src[2t+1]), saida intercalada em ordem natural."""
import cmath
import pathlib
import struct
import sys

order = int(sys.argv[1]) if len(sys.argv) > 1 else 9
mode = sys.argv[2] if len(sys.argv) > 2 else "rand"
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


src = as_f32(section("SRC"))
kd = as_f32(section("KD"))
n = len(src)
m = n // 2

z = [complex(src[2 * t], src[2 * t + 1]) for t in range(m)]
Z = [
    sum(z[t] * cmath.exp(-2j * cmath.pi * k * t / m) for t in range(m))
    for k in range(m)
]

err = [abs(complex(kd[2 * k], kd[2 * k + 1]) - Z[k]) for k in range(m)]
mx = max(err)
print(f"{path.name}: m={m}  max |KD - FFT| = {mx:.3e}   media = {sum(err)/m:.3e}")
print("  err k=0..7:", ", ".join(f"{e:.2e}" for e in err[:8]))
print("  KD[0..7]  :", [f"{kd[i]:+.6f}" for i in range(8)])
print("  FFT[0..3] :", [f"{Z[i].real:+.6f}{Z[i].imag:+.6f}i" for i in range(4)])
