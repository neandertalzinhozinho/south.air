import difflib
import hashlib
from pathlib import Path

D = Path(r"D:\PROJETOS\shadowFILES\analysis\stage_reports\fase2\dumps")


def toks(data):
    # split into printable runs and single bytes, enough to see structure
    out, cur = [], bytearray()
    for b in data:
        if 32 <= b < 127:
            cur.append(b)
        else:
            if cur:
                out.append(bytes(cur))
                cur = bytearray()
            out.append(bytes([b]))
    if cur:
        out.append(bytes(cur))
    return out


for k in (39, 45, 52):
    a = (D / f"cand.program_{k}.bin").read_bytes()
    b = (D / f"oracle.program_{k}.bin").read_bytes()
    print(f"--- program {k}: cand {len(a)} B sha {hashlib.sha256(a).hexdigest()[:16]} | "
          f"oracle {len(b)} B sha {hashlib.sha256(b).hexdigest()[:16]}")
    sa, sb = toks(a), toks(b)
    sm = difflib.SequenceMatcher(a=sa, b=sb, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        ca = b"".join(sa[i1:i2])
        cb = b"".join(sb[j1:j2])
        print(f"  {tag}: cand[{i1}:{i2}]={ca!r} oracle[{j1}:{j2}]={cb!r}")
print()
# identical program (control): 0
a = (D / "cand.program_0.bin").read_bytes()
b = (D / "oracle.program_0.bin").read_bytes()
print("program 0 equal:", a == b, len(a), len(b))
print("program 0 printable:", bytes(c for c in a if 32 <= c < 127)[:400])
