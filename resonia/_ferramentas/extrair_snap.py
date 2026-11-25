"""Extrai arquivos completos de snapshots Codex por faixa de linhas e confere o tamanho.

Uso: py -I extrair_snap.py <snap_dir> <saida_dir>
"""
import os
import sys

snapd, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
# (nome, snapshot, primeira linha, ultima linha, bytes finais conhecidos ou None)
JOBS = [
    ("dsp_mod.rs", "02-28-59", 342, 576, 8090),
    ("dsp_curve.rs", "02-29-14", 60, 201, 5387),
    ("dsp_detect.rs", "02-29-14", 5, 59, 2406),
    ("render_host.rs", "02-29-06", 340, 377, 1338),
    ("Cargo.toml", "02-28-59", 577, 603, None),
    ("Cargo.toml.0212", "02-12-53", 552, 578, None),
    ("equivalence.rs", "02-28-59", 5, 341, 15498),
]
for name, sn, a, b, size in JOBS:
    L = open(os.path.join(snapd, sn + ".txt"), encoding="utf-8").read().split("\n")[a - 1:b]
    while L and L[-1].strip() == "":
        L.pop()
    t = "\n".join(L) + "\n"
    lf = len(t.encode())
    crlf = len(t.replace("\n", "\r\n").encode())
    verdict = "?" if size is None else ("LF" if lf == size else ("CRLF" if crlf == size else "NAO BATE"))
    print("%-16s linhas=%d LF=%d CRLF=%d esperado=%s -> %s" % (name, len(L), lf, crlf, size, verdict))
    open(os.path.join(out, name), "w", encoding="utf-8", newline="").write(
        t if verdict != "CRLF" else t.replace("\n", "\r\n"))
