#!/usr/bin/env python3
"""Gera checks/fft_golden.rs a partir dos dumps de checks/.build/fft_<o>_<sig>.bits.

Os dumps sao produzidos por checks/fft_probe.rs, que chama a FFT interna do
proprio plugin (read-only) por RVA: 0x4100 (getSize), 0x8840 (init), 0x20E0
(fwd), 0x7B40 (inv). Nada aqui e estimado: sao bits medidos.
"""
import pathlib

ORDERS = (6, 7, 8, 9)
SIGS = ("impulse", "cos", "ramp")

root = pathlib.Path(__file__).resolve().parent.parent
build = root / "checks" / ".build"

out = []
out.append("// Vetores-ouro MEDIDOS da FFT interna do soothe3 (nao estimados).")
out.append("//")
out.append("// Fonte: `checks/fft_probe.rs`, que carrega `original/soothe3.vst3` com")
out.append("// `LoadLibraryW` (sem patch/hook/injecao) e chama, por RVA, o mesmo trio que o")
out.append("// audio chama: `0x4100` getSize (thunk 0x1130), `0x8840` init (thunk 0x12B0),")
out.append("// `0x20E0` fwd (thunk 0x1010) e `0x7B40` inv (thunk 0x1280).")
out.append("//")
out.append("// flag = 8 (IPP_FFT_NODIV_BY_ANY, `cmp esi,8 je 0x7245C`), hint = 1.")
out.append("// Para cada caso: bits de `src` (n f32) e de `dst` (n+2 f32) devolvidos por")
out.append("// `fwd`. `dst` e o layout provado: `n/2+1` pares (re,im) intercalados em ordem")
out.append("// natural; par 0 = (DC, 0); par n/2 = (Nyquist, 0).")
out.append("")

for o in ORDERS:
    for s in SIGS:
        p = build / f"fft_{o}_{s}.bits"
        lines = [l.strip() for l in p.read_text().splitlines() if l.strip()]
        assert lines[0].startswith("# order=")
        i = lines.index("SRC")
        j = lines.index("DST")
        k = lines.index("BACK")
        src = lines[i + 1:j]
        dst = lines[j + 1:k]
        back = lines[k + 1:]
        n = 1 << o
        assert len(src) == n, (o, s, len(src))
        assert len(dst) == n + 2, (o, s, len(dst))
        assert len(back) == n + 2, (o, s, len(back))
        out.append(f"pub static FFT{o}_{s.upper()}_SRC: [u32; {n}] = [")
        for k2 in range(0, n, 8):
            out.append("    " + " ".join("0x" + b + "," for b in src[k2:k2 + 8]))
        out.append("];")
        out.append(f"pub static FFT{o}_{s.upper()}_DST: [u32; {n + 2}] = [")
        for k2 in range(0, n + 2, 8):
            out.append("    " + " ".join("0x" + b + "," for b in dst[k2:k2 + 8]))
        out.append("];")
        out.append(f"pub static FFT{o}_{s.upper()}_BACK: [u32; {n + 2}] = [")
        for k2 in range(0, n + 2, 8):
            out.append("    " + " ".join("0x" + b + "," for b in back[k2:k2 + 8]))
        out.append("];")
        out.append("")

(root / "checks" / "fft_golden.rs").write_text("\n".join(out) + "\n", encoding="utf-8")
print("escrito", root / "checks" / "fft_golden.rs")
