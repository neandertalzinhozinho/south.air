import winreg, os, re

paths = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\oeksound_soothe3_is1",
         r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\oeksound_soothe3_is1"]
for pth in paths:
    try:
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pth)
    except OSError:
        continue
    print("==", pth)
    for i in range(winreg.QueryInfoKey(k)[1]):
        n, v, t = winreg.EnumValue(k, i)
        print(f"  {n} = {v}")

print("=== version hints in plugin ===")
p = r"D:\PROJETOS\shadowFILES\analysis\startup_audit\pace_free\final_candidate_uni46c.vst3"
blob = open(p, "rb").read()
for pat in [b"5.10.5", b"PACE Fusion", b"clientdb.v1.01", b"LicenseDaemonNeedsUpdate", b"EdenVersion"]:
    i, hits = 0, 0
    while hits < 3:
        i = blob.find(pat, i)
        if i < 0:
            break
        ctx = re.sub(rb"[^ -~]", b".", blob[max(0, i - 70):i + 90]).decode("latin1")
        print(f"  {pat.decode():<26} @{i:#x}  {ctx}")
        i += 1
        hits += 1
