import os

ROOT = r"D:\PROJETOS\shadowFILES"
targets = [b"TPaceNamedPipeServer", b"LdLog_", b"LDsvc.exe", b"librustc", b"5.10.5.4734",
           b"PaceLicenseService", b"LicenseSupport", b"PaceFusion", b"FusionSetup",
           b"PaceEdenService", b"eden licensed daemon"]
CH = 8 << 20
res = {t: [] for t in targets}
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        p = os.path.join(dp, f)
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        if sz == 0 or sz > 300 * 1024 * 1024:
            continue
        try:
            with open(p, "rb") as fh:
                carry = b""
                while True:
                    c = fh.read(CH)
                    if not c:
                        break
                    buf = carry + c
                    for t in targets:
                        if t in buf:
                            res[t].append(p)
                    carry = buf[-128:]
        except OSError:
            pass

for t in targets:
    uniq = sorted(set(res[t]))
    print(f"--- {t.decode()} : {len(uniq)} file(s)")
    for p in uniq[:12]:
        print("     ", p)
