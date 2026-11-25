import os, re

pat = re.compile(r"soothe|oeksound", re.I)
skip = {"shadowfiles", "juce", "node_modules"}
hits = []
for root in ("D:\\", "E:\\"):
    if not os.path.isdir(root):
        continue
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d.lower() not in skip and not d.startswith("$")]
        if dp.count(os.sep) > 6:
            dn[:] = []
        for f in fn:
            if pat.search(f):
                p = os.path.join(dp, f)
                try:
                    hits.append((os.path.getsize(p), p))
                except OSError:
                    pass
hits.sort(reverse=True)
for s, p in hits[:30]:
    print(f"{s:>14}  {p}")
print("total", len(hits))
