import os
roots = [r"C:\Program Files", r"C:\Program Files (x86)", r"C:\ProgramData",
         os.path.expandvars(r"%LOCALAPPDATA%"), os.path.expandvars(r"%APPDATA%"),
         r"C:\Windows\System32", r"D:\PROJETOS\shadowFILES"]
pat = ("ldsvc", "paceld", "eden", "pace")
hits = []
for root in roots:
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d.lower() not in ("cache", "temp", "tmp", "winsxs", "node_modules", ".git", ".venv")]
        for f in fn:
            lf = f.lower()
            if any(p in lf for p in pat):
                p = os.path.join(dp, f)
                try:
                    hits.append((os.path.getsize(p), p))
                except OSError:
                    pass
    if len(hits) > 200:
        break
for s, p in hits[:80]:
    print(s, p)
print("total", len(hits))
