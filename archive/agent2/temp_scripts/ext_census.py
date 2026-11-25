import os, collections

ROOT = r"D:\PROJETOS\shadowFILES"
counts = collections.Counter()
sizes = collections.Counter()
examples = {}
interesting = {".msi", ".mst", ".cab", ".pkg", ".iso", ".img", ".vhd", ".vhdx", ".7z", ".rar",
               ".zip", ".tar", ".gz", ".exe", ".dll", ".sys", ".ocx", ".scr", ".msix", ".appx"}
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        e = os.path.splitext(f)[1].lower()
        counts[e] += 1
        try:
            sizes[e] += os.path.getsize(os.path.join(dp, f))
        except OSError:
            pass
        if e in interesting and e not in examples:
            examples[e] = os.path.join(dp, f)
print("=== interesting extensions present ===")
for e in sorted(interesting):
    if counts[e]:
        print(f"  {e:<7} count={counts[e]:<6} bytes={sizes[e]:<14} e.g. {examples[e]}")
    else:
        print(f"  {e:<7} count=0")
print("=== all extensions (top 20 by count) ===")
for e, c in counts.most_common(20):
    print(f"  {e or '(none)':<10} {c}")
