import sys, re
import pefile

p = r"D:\PROJETOS\shadowFILES\analysis\startup_audit\pace_free\final_candidate_uni46c.vst3"
pe = pefile.PE(p, fast_load=False)

want = ("Pipe", "DeviceIo", "NamedPipe", "CreateFile", "WaitNamedPipe", "ConnectNamedPipe",
        "TransactNamedPipe", "CallNamedPipe", "GetNamedPipe")
print("=== imported APIs matching pipe ===")
seen = set()
for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []):
    for imp in entry.imports:
        if not imp.name:
            continue
        n = imp.name.decode()
        if any(w.lower() in n.lower() for w in want):
            print(f"  {entry.dll.decode():<24} {n}")

print("=== exported functions (Eden/Pace) ===")
if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
    for sym in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if sym.name:
            n = sym.name.decode()
            if re.search(r"pace|eden|licen", n, re.I):
                print("  ", n)
else:
    print("  (no exports)")

print("=== strings: server-side / handler tokens ===")
blob = open(p, "rb").read()
pats = [b"TPaceNamedPipeServer", b"AuthorizationLiteHandler", b"AuthorizationLiteProcessor",
        b"LdLog_", b"LicenseDaemon", b"EdenVersion", b"licensedb", b"TPipeServer",
        b"TPacePipe", b"LicenseService", b"startLicenseDaemon", b"SpawnLicense"]
for pat in pats:
    idx = blob.find(pat)
    print(f"  {pat.decode():<32} {'FOUND @ %#x' % idx if idx >= 0 else 'absent'}")

print("=== .rdata strings containing 'Handler' near pace/eden ===")
for m in re.finditer(rb"[ -~]{6,160}", blob):
    s = m.group()
    if b"Handler" in s and (b"pace" in s.lower() or b"eden" in s.lower() or b"Licen" in s):
        print("  ", s.decode("latin1")[:150])
