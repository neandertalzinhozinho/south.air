import winreg, re

def scan(root, path):
    out = []
    try:
        k = winreg.OpenKey(root, path)
    except OSError:
        return out
    i = 0
    while True:
        try:
            name = winreg.EnumKey(k, i)
        except OSError:
            break
        i += 1
        try:
            sk = winreg.OpenKey(k, name)
        except OSError:
            continue
        vals = {}
        for v in ("ImagePath", "DisplayName", "Description", "ObjectName", "ServiceDll"):
            try:
                vals[v] = winreg.QueryValueEx(sk, v)[0]
            except OSError:
                pass
        try:
            params = winreg.OpenKey(sk, "Parameters")
            try:
                vals["ServiceDll"] = winreg.QueryValueEx(params, "ServiceDll")[0]
            except OSError:
                pass
        except OSError:
            pass
        blob = " ".join(str(x) for x in vals.values())
        if re.search(r"pace|eden|ldsvc|ilok|licen", blob, re.I) or re.search(r"pace|eden|ldsvc|ilok", name, re.I):
            out.append((name, vals))
    return out

for root, path in ((winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services"),):
    print(f"=== {path} ===")
    for name, vals in scan(root, path):
        print(name)
        for k, v in vals.items():
            print(f"    {k}: {v}")

print("=== uninstall entries (all, filtered) ===")
for path in (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
             r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"):
    try:
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except OSError:
        continue
    for i in range(winreg.QueryInfoKey(k)[0]):
        try:
            name = winreg.EnumKey(k, i)
            sk = winreg.OpenKey(k, name)
            dn = winreg.QueryValueEx(sk, "DisplayName")[0]
        except OSError:
            continue
        if re.search(r"pace|eden|oek|soothe|ilok", dn, re.I):
            print(f"  {dn}  [{name}]")
