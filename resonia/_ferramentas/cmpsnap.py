"""Compara um trecho de snapshot Codex (linhas a..b do .txt extraido) com um arquivo (linhas c..).

Uso: py -I cmpsnap.py <snap.txt> <a> <b> <arquivo> <c>
Imprime IGUAL ou as primeiras diferencas. Compara com LF (CRLF normalizado).
"""
import sys

snapf, a, b, fil, c = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
S = open(snapf, encoding="utf-8").read().split("\n")[a - 1:b]
F = open(fil, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
F = F[c - 1:c - 1 + len(S)]
diffs = [(i, x, y) for i, (x, y) in enumerate(zip(S, F)) if x.rstrip() != y.rstrip()]
if len(F) < len(S):
    print("ARQUIVO CURTO: %d < %d" % (len(F), len(S)))
if not diffs:
    print("IGUAL (%d linhas; arquivo linhas %d..%d)" % (len(S), c, c + len(S) - 1))
else:
    print("DIFERENCAS: %d de %d" % (len(diffs), len(S)))
    for i, x, y in diffs[:8]:
        print("  arq linha %d\n    snap: %r\n    arq : %r" % (c + i, x[:160], y[:160]))
