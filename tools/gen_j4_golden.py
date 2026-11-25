#!/usr/bin/env python3
"""Gera checks/j4_golden_<order>.rs a partir de checks/.build/j4_stage_<order>.bits.

O arquivo de bits vem de checks/fft_stage_probe.rs, que chama o plugin
(read-only) por RVA: kernel (0x8BFE0 / 0x8C280), split 0x895C0 e fwd 0x20E0,
sobre uma entrada deterministica (xorshift). Nada aqui e estimado.

Uso: py -3 tools/gen_j4_golden.py 6
     py -3 tools/gen_j4_golden.py 7
"""
import pathlib
import sys

order = int(sys.argv[1]) if len(sys.argv) > 1 else 6
root = pathlib.Path(__file__).resolve().parent.parent
src = root / "checks" / ".build" / f"j4_stage_{order}.bits"
lines = [l.strip() for l in src.read_text().splitlines() if l.strip()]
assert lines[0].startswith(f"# order={order}"), lines[0]

NAMES = ("SRC", "KD", "MAN", "FWD", "TW")


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
assert len(sec["SRC"]) == n, (len(sec["SRC"]), n)
assert len(sec["KD"]) == n, (len(sec["KD"]), n)
assert len(sec["MAN"]) == n + 2 and len(sec["FWD"]) == n + 2
assert len(sec["TW"]) >= 2 * n

out = []
out.append(f"// Vetores-ouro MEDIDOS das pecas da FFT de ordem {order} (nao estimados).")
out.append("//")
out.append("// Fonte: checks/fft_stage_probe.rs (LoadLibraryW, read-only) chamando")
out.append("//   0x8BFE0 (ordem 6) ou 0x8C280 (ordem 7)  -> KD (n f32)")
out.append("//   0x725F6 pack + 0x895C0 split + move     -> MAN (n+2 f32)")
out.append("//   0x20E0 (fwd do plugin)                  -> FWD (n+2 f32)")
out.append("// TW = 2*n u32 lidos de ctx+0x50 (tabela de twiddles do split).")
out.append("")

for name, arr in (("SRC", sec["SRC"]), ("KD", sec["KD"]),
                  ("MAN", sec["MAN"]), ("FWD", sec["FWD"]),
                  ("TW", sec["TW"])):
    sym = f"J{order}_{name}"
    out.append(f"pub static {sym}: [u32; {len(arr)}] = [")
    for k in range(0, len(arr), 8):
        out.append("    " + " ".join("0x%08x," % v for v in arr[k:k + 8]))
    out.append("];")
    out.append("")

dst = root / "checks" / f"j4_golden_{order}.rs"
dst.write_text("\n".join(out) + "\n", encoding="utf-8")
print("escrito", dst)
