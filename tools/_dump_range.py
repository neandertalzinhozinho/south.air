import re, pathlib, sys

lines = pathlib.Path(r"D:\PROJETOS\soultree\checks\.build\1d69e00_full.dis").read_text(encoding="utf-8", errors="replace").splitlines()
ins = []
for l in lines:
    m = re.match(r"^([0-9A-F]{8})\s+(\S+)\s*(.*)$", l.strip())
    if m:
        ins.append((int(m.group(1), 16), m.group(2), m.group(3).strip()))

a, b = int(sys.argv[1], 16), int(sys.argv[2], 16)
for x in ins:
    if a <= x[0] <= b:
        print(f"{x[0]:08X} {x[1]:10s} {x[2]}")
