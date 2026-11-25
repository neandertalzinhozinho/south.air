#!/usr/bin/env python3
"""Gera checks/j<order>_golden.rs a partir de checks/.build/j<order>_stage_<modo>.bits.

O arquivo de bits vem de checks/fft_generic_probe.rs, que chama o plugin
(read-only) por RVA: kernel 0x1D69E00 e fwd 0x20E0, sobre entrada deterministica.

Uso: py -3 tools/gen_j9_golden.py 9 [rand|imp|eN]
"""
import pathlib
import sys

order = int(sys.argv[1]) if len(sys.argv) > 1 else 9
mode = sys.argv[2] if len(sys.argv) > 2 else "rand"
root = pathlib.Path(__file__).resolve().parent.parent
src = root / "checks" / ".build" / f"j{order}_stage_{mode}.bits"
lines = [l.strip() for l in src.read_text().splitlines() if l.strip()]
assert lines[0].startswith(f"# order={order}"), lines[0]

NAMES = ("SRC", "KD", "WS", "FWD", "IDX", "TW38", "TW50")


def section(name):
    i = lines.index(name)
    out = []
    for l in lines[i + 1:]:
        if l in NAMES:
            break
        out.append(int(l, 16))
    return out


sec = {n: section(n) for n in NAMES}
n = 1 << order
assert len(sec["SRC"]) == n and len(sec["KD"]) == n, (len(sec["SRC"]), len(sec["KD"]))
assert len(sec["FWD"]) == n + 2
assert len(sec["WS"]) == n
assert len(sec["IDX"]) == n // 8 + 16, len(sec["IDX"])
assert len(sec["TW50"]) == 2 * n
assert len(sec["TW38"]) == (0x400 << (order - 8)) // 4, len(sec["TW38"])

out = []
out.append(f"// Vetores-ouro MEDIDOS do kernel generico 0x1D69E00, ordem {order}.")
out.append("//")
out.append("// Fonte: checks/fft_generic_probe.rs (LoadLibraryW, read-only) chamando")
out.append(f"//   0x1D69E00(src, dst, {n // 2}, tw38, idx30, ws) -> KD ({n} f32)")
out.append(f"//   0x20E0 (fwd do plugin)                      -> FWD ({n + 2} f32)")
out.append(f"// IDX  = {len(sec['IDX'])} u32 de ctx+0x30 (até o 0 sentinela, n/8+16);")
out.append(f"// TW38 = {len(sec['TW38'])} f32 de ctx+0x38 (tw50_ptr - tw38_ptr);")
out.append(f"// TW50 = {2 * n} f32 de ctx+0x50 (twiddles do split).")
out.append("")

for name, arr in (
    ("SRC", sec["SRC"]),
    ("KD", sec["KD"]),
    ("WS", sec["WS"]),
    ("FWD", sec["FWD"]),
    ("IDX", sec["IDX"]),
    ("TW38", sec["TW38"]),
    ("TW50", sec["TW50"]),
):
    sym = f"J{order}_{name}"
    out.append(f"pub static {sym}: [u32; {len(arr)}] = [")
    for k in range(0, len(arr), 8):
        out.append("    " + " ".join("0x%08x," % v for v in arr[k:k + 8]))
    out.append("];")
    out.append("")

dst = root / "checks" / f"j{order}_golden.rs"
dst.write_text("\n".join(out) + "\n", encoding="utf-8")
print("escrito", dst)
