files = [r"D:\PROJETOS\shadowFILES\analysis\startup_audit\soothe3_unpacked_fixed.i64",
         r"D:\PROJETOS\shadowFILES\soothe3_unpacked_fixed.pe.id1"]
targets = [b"TPaceNamedPipeServer", b"LDsvc", b"LdLog_", b"PaceLicenseService", b"FusionSetup",
           b"PACE Fusion Setup", b"PaceEden", b"paceap.com"]
CH = 16 << 20
for p in files:
    print("==", p)
    hits = {t: 0 for t in targets}
    with open(p, "rb") as fh:
        carry = b""
        while True:
            c = fh.read(CH)
            if not c:
                break
            buf = carry + c
            for t in targets:
                n = buf.count(t)
                if n:
                    hits[t] += n
            carry = buf[-128:]
    for t in targets:
        print(f"   {t.decode():<22} {hits[t]}")
