import os

ROOT = r"D:\PROJETOS\shadowFILES"
big = []
zero = 0
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        p = os.path.join(dp, f)
        try:
            s = os.path.getsize(p)
        except OSError:
            continue
        if s == 0:
            zero += 1
        elif s > 300 * 1024 * 1024:
            big.append((s, p))
big.sort(reverse=True)
print("zero-byte files:", zero)
print("files >300MB (skipped by content scan):", len(big))
for s, p in big:
    print(f"  {s/1e6:8.1f} MB  {p}")
