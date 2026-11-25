"""Aplica os patches Codex de sucesso (02:14:06 calibrate.rs, 02:14:21 main.rs) sobre o replay.

Uso: py -I montar_patch.py <replay_dir> <patches_dir> <saida_dir>
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import applypatch as ap  # noqa: E402

rdir, pdir, odir = sys.argv[1:4]
os.makedirs(odir, exist_ok=True)
jobs = [
    ("src_calibrate.rs@01-56-26.txt", "in_02-14-06.js", "calibrate.rs", 18458),
    ("src_main.rs@01-56-30.txt", "in_02-14-21.js", "main.rs", 26425),
]
for base, pj, name, final_size in jobs:
    text = open(os.path.join(rdir, base), encoding="utf-8", newline="").read()
    patch = ap.extract_patch(open(os.path.join(pdir, pj), encoding="utf-8").read())
    secs = ap.sections(patch)
    for path, chunks in secs.items():
        if not path.endswith("\\" + name):
            print(pj, "secao para", path, "com", len(chunks), "bloco(s):",
                  [[t for t, _ in c] for c in chunks], "(ignorada aqui)")
            continue
        text, rep = ap.apply(text, chunks)
        print(name, rep)
    lf = len(text.encode("utf-8"))
    crlf = len(text.replace("\n", "\r\n").encode("utf-8"))
    print(name, "bytes LF=%d CRLF=%d esperado=%d -> %s" % (
        lf, crlf, final_size, "LF" if lf == final_size else ("CRLF" if crlf == final_size else "NAO BATE")))
    with open(os.path.join(odir, name), "w", encoding="utf-8", newline="") as w:
        w.write(text)
