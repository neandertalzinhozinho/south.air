import os, fnmatch

roots = [os.path.expandvars(r"%TEMP%"), os.path.expandvars(r"%LOCALAPPDATA%"), os.path.expandvars(r"%APPDATA%"),
         r"C:\ProgramData", r"C:\Windows\Temp", r"C:\Program Files", r"C:\Program Files (x86)",
         r"C:\Users\tromb\Downloads", r"C:\Users\tromb\Desktop", r"C:\Users\tromb\Documents",
         r"D:\PROJETOS\shadowFILES", r"D:\\"]
pats = ["*ldsvc*", "*pace*.exe", "*eden*.exe", "ldsvc.exe"]
hits = []
seen_dirs = set()
for root in roots:
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root):
        if dp in seen_dirs:
            dn[:] = []
            continue
        seen_dirs.add(dp)
        if len(dp.split(os.sep)) > 14:
            dn[:] = []
        for f in fn:
            lf = f.lower()
            if any(fnmatch.fnmatch(lf, p) for p in pats):
                p = os.path.join(dp, f)
                try:
                    hits.append((os.path.getsize(p), p))
                except OSError:
                    pass
        if len(hits) > 50:
            break
for s, p in hits[:50]:
    print(s, p)
print('total', len(hits))
