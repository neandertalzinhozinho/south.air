import re
from pathlib import Path

p = Path(r"D:\PROJETOS\shadowFILES\analysis\startup_audit\pace_free\final_candidate_uni46c.vst3")
blob = p.read_bytes()

pat = re.compile(rb"[ -~]{6,200}")
sym = re.compile(rb"Authorization\w*|sendEncryptedCommand\w*|SvIf|Processor|Handler|presult|_result")

hits = []
for m in pat.finditer(blob):
    s = m.group()
    if sym.search(s) and (b"eden" in s or b"Authoriz" in s or b"sendEnc" in s):
        hits.append((m.start(), s.decode("latin1")))

seen = set()
print(f"=== {len(hits)} raw, unique below ===")
for off, s in hits:
    if s in seen:
        continue
    seen.add(s)
    print(f"{off:#010x}  {s}")
