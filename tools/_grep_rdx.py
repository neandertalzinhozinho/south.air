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
    args = m.group(3)
    if 0x01D6A18B <= a <= 0x01D6AD25 and ("rdx" in args or "edx" in args):
        print(l.strip())
