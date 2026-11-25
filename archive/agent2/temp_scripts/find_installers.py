import os, re, fnmatch

roots = [r"C:\Users\tromb\Downloads", r"C:\Users\tromb\Desktop", r"C:\Users\tromb\Documents",
         r"C:\Windows\Temp", os.path.expandvars(r"%TEMP%"), r"C:\Windows\Installer",
         r"D:\PROJETOS\shadowFILES", r"C:\Program Files\Common Files\VST3", r"C:\Program Files (x86)",
         r"C:\Program Files"]
pat = re.compile(r"soothe|oeksound|pace|fusion|ldsvc|eden", re.I)
exts = {".exe", ".msi", ".pkg", ".zip", ".7z", ".dll", ".mst", ".cab"}
hits = []
for root in roots:
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root):
        if len(dp.split(os.sep)) > 12:
            dn[:] = []
            continue
        if dp.lower().startswith(r"d:\projetos\shadowfiles\analysis\tools"):
            dn[:] = []
            continue
        for f in fn:
            e = os.path.splitext(f)[1].lower()
            if e not in exts:
                continue
            if not pat.search(f):
                continue
            p = os.path.join(dp, f)
            try:
                sz = os.path.getsize(p)
            except OSError:
                continue
            hits.append((sz, p))
hits.sort(reverse=True)
for sz, p in hits[:40]:
    print(f"{sz:>12}  {p}")
print("total", len(hits))
