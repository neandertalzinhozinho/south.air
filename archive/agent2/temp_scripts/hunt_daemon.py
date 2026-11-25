import os, re, sys

root = r"D:\PROJETOS\shadowFILES"
name_pat = re.compile(r"ldsvc|eden|pace", re.I)
skip_dirs = {".git", "node_modules", "rustup", "s5_toolchain", "JUCE", ".venv", "build"}

named = []
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d.lower() not in skip_dirs]
    for f in fn:
        if name_pat.search(f):
            p = os.path.join(dp, f)
            try:
                named.append((os.path.getsize(p), p))
            except OSError:
                pass
named.sort(reverse=True)
print("=== filename hits ===")
for s, p in named[:60]:
    print(f"{s:>12}  {p}")
print("total", len(named))

print("=== content hits (TPaceNamedPipeServer / LicensedEden) ===")
needles = [b"TPaceNamedPipeServer", b"com.paceap.eden", b"LdLog_"]
found = []
scanned = 0
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d.lower() not in skip_dirs]
    for f in fn:
        p = os.path.join(dp, f)
        try:
            if os.path.getsize(p) > 80_000_000:
                continue
            with open(p, "rb") as fh:
                blob = fh.read()
        except OSError:
            continue
        scanned += 1
        for n in needles:
            if n in blob:
                found.append((n.decode(), p, len(blob)))
                break
print("scanned", scanned)
for n, p, sz in found[:60]:
    print(f"{sz:>12}  [{n}]  {p}")
print("total", len(found))
