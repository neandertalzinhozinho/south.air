#!/usr/bin/env python3
"""Compara os dois algoritmos de posto no modelo de pass2 e mede o composto."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import recover_pass1 as R  # noqa: E402


def mat(fn, dim):
    M = [[0.0] * dim for _ in range(dim)]
    for i in range(dim):
        e = [0.0] * dim
        e[i] = 1.0
        out = fn(e)
        for r in range(dim):
            M[r][i] = out[r]
    return M


def rank_fwd(M, tol=1e-9):
    A = [row[:] for row in M]
    n, m = len(A), len(A[0])
    rank = 0
    piv = []
    for c in range(m):
        p = max(range(rank, n), key=lambda r: abs(A[r][c]))
        if abs(A[p][c]) < tol:
            continue
        A[rank], A[p] = A[p], A[rank]
        pv = A[rank][c]
        for r in range(rank + 1, n):
            f = A[r][c] / pv
            if f:
                for k in range(c, m):
                    A[r][k] -= f * A[rank][k]
        piv.append(c)
        rank += 1
    return rank, [c for c in range(m) if c not in piv]


def rank_gj(M, tol=1e-9):
    A = [row[:] for row in M]
    n, m = len(A), len(A[0])
    r = 0
    for c in range(m):
        p = max(range(r, n), key=lambda i: abs(A[i][c]))
        if abs(A[p][c]) < tol:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0.0:
                f = A[i][c]
                A[i] = [A[i][k] - f * A[r][k] for k in range(m)]
        r += 1
        if r == n:
            break
    return r


M2 = mat(R.pass2_block, 64)
print("pass2 fwd:", rank_fwd(M2))
print("pass2 gj :", rank_gj(M2), "/ 64")
M3 = mat(R.pass3a_block, 128)
print("pass3a fwd:", rank_fwd(M3)[0], "/ 128")
MC = R.build_matrix()
print("composto fwd:", rank_fwd(MC))
