import re, pathlib

lines = pathlib.Path(r"D:\PROJETOS\soultree\checks\.build\1d69e00_full.dis").read_text(
    encoding="utf-8", errors="replace"
).splitlines()
pat = re.compile(r"^([0-9A-F]{8})\s+(\S+)\s*(.*)$")
for l in lines:
    m = pat.match(l.strip())
    if not m:
        continue
    a = int(m.group(1), 16)
    op, args = m.group(2), m.group(3)
    if 0x01D69E91 <= a <= 0x01D6A18B:
        if op.startswith("mov") or op.startswith("shl") or op.startswith("shr") or op.startswith("sar"):
            pass
        if re.search(r"\brdx\b|\bedx\b", args):
            print(l.strip())
