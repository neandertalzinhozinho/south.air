import re, sys, pathlib

path = pathlib.Path(r"D:\PROJETOS\soultree\checks\.build\1d69e00_full.dis")
lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

ins = {}
order = []
for l in lines:
    m = re.match(r"^([0-9A-F]{8})\s+(\S+)\s*(.*)$", l.strip())
    if m:
        a = int(m.group(1), 16)
        ins[a] = (m.group(2), m.group(3).strip())
        order.append(a)

def seq(start, end):
    out = []
    for a in order:
        if start <= a <= end:
            op, args = ins[a]
            out.append(op)
    return out

def show(start, end, name):
    s = seq(start, end)
    print(f"{name}: {len(s)} insns, mnemonics:", " ".join(s[:12]), "...")

# blocks to compare
pairs = [
    ("A1EB", 0x01D6A1EB, 0x01D6A3E8),
    ("B03A", 0x01D6B03A, 0x01D6B225),
    ("A3E9", 0x01D6A3E9, 0x01D6A6AE),
    ("B249", 0x01D6B249, 0x01D6B89D),
    ("A6B0", 0x01D6A6B0, 0x01D6AD24),
    ("B8C9", 0x01D6B8C9, 0x01D6BB86),
    ("AD25", 0x01D6AD25, 0x01D6B039),
    ("BB87", 0x01D6BB87, 0x01D6BD18),
]
for name, s, e in pairs:
    show(s, e, name)
