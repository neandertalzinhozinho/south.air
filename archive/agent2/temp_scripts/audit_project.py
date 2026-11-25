import os, re, sys, json, zipfile

ROOT = r"D:\PROJETOS\shadowFILES"
OUT = r"C:\Users\tromb\AppData\Local\Temp\opencode\full_audit.txt"

name_re = re.compile(r"ldsvc|pace|eden|fusion|oeksound|ilok", re.I)
soothe_re = re.compile(r"soothe", re.I)
arch_ext = {".exe", ".msi", ".mst", ".cab", ".pkg", ".zip", ".7z", ".rar", ".iso", ".img", ".tar", ".gz", ".bz2", ".xz", ".dll", ".sys", ".dat", ".bin"}

markers = [b"LDsvc", b"LDSvc", b"ldsvc.exe", b"PACE Fusion", b"TPaceNamedPipeServer",
           b"PACE Anti-Piracy", b"com.paceap.eden.licensed", b"paceap.com/LicenseSupport",
           b"FusionSetup", b"PaceLicenseService"]
pe_magic = b"MZ"

files = 0
total_bytes = 0
name_hits = []
arch_hits = []
big = []
content_hits = []
errors = []
scanned_bytes = 0
scanned_files = 0

CHUNK = 8 << 20
OVERLAP = 128

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as log:
    log.write(f"ROOT {ROOT}\n")
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            p = os.path.join(dp, f)
            try:
                st = os.stat(p)
            except OSError as e:
                errors.append((p, repr(e)))
                continue
            files += 1
            total_bytes += st.st_size
            base = f
            if name_re.search(base):
                name_hits.append((st.st_size, p))
            ext = os.path.splitext(base)[1].lower()
            if ext in arch_ext and st.st_size > 256 * 1024:
                arch_hits.append((st.st_size, p))
            if st.st_size > 1_000_000:
                big.append((st.st_size, p))
            # content scan
            if st.st_size == 0 or st.st_size > 300 * 1024 * 1024:
                continue
            try:
                with open(p, "rb") as fh:
                    head = fh.read(2)
                    fh.seek(0)
                    first = True
                    carry = b""
                    while True:
                        chunk = fh.read(CHUNK)
                        if not chunk:
                            break
                        buf = carry + chunk
                        for mk in markers:
                            idx = buf.find(mk)
                            while idx >= 0:
                                content_hits.append((p, mk.decode("latin1"), idx))
                                idx = buf.find(mk, idx + 1)
                        carry = buf[-OVERLAP:]
                        scanned_bytes += len(chunk)
                    scanned_files += 1
            except OSError as e:
                errors.append((p, repr(e)))

    name_hits.sort(reverse=True)
    arch_hits.sort(reverse=True)
    big.sort(reverse=True)

    log.write(f"\nSTATS files={files} bytes={total_bytes} scanned_files={scanned_files} scanned_bytes={scanned_bytes}\n")
    log.write(f"ERRORS {len(errors)}\n")
    for p, e in errors[:20]:
        log.write(f"  ERR {p} {e}\n")

    log.write(f"\n=== NAME MATCHES (ldsvc|pace|eden|fusion|oeksound|ilok) : {len(name_hits)} ===\n")
    for s, p in name_hits:
        log.write(f"{s:>14}  {p}\n")

    log.write(f"\n=== ARCHIVES/BINARIES >256KB : {len(arch_hits)} (top 60) ===\n")
    for s, p in arch_hits[:60]:
        log.write(f"{s:>14}  {p}\n")

    log.write(f"\n=== FILES >1MB : {len(big)} (top 40) ===\n")
    for s, p in big[:40]:
        log.write(f"{s:>14}  {p}\n")

    log.write(f"\n=== CONTENT MARKER HITS : {len(content_hits)} ===\n")
    for p, mk, off in content_hits[:200]:
        log.write(f"  [{mk}] @{off:#x}  {p}\n")

    log.write("\n=== ZIP INSPECTION ===\n")
    for s, p in arch_hits:
        if not p.lower().endswith(".zip"):
            continue
        try:
            z = zipfile.ZipFile(p)
            names = z.namelist()
            interesting = [n for n in names if name_re.search(n)]
            log.write(f"  ZIP {p} entries={len(names)} interesting={interesting[:10]}\n")
        except Exception as e:
            log.write(f"  ZIP {p} FAILED {e!r}\n")

print(open(OUT, encoding="utf-8").read()[:6000])
print("....")
print("FULL LOG:", OUT)
