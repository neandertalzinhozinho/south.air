import re, pathlib
raw = pathlib.Path("checks/ghidra_H.txt").read_bytes()
s = raw.decode("utf-16", errors="replace") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8", errors="replace")
parts = re.split(r"===== FUNCTION (\S+) @ (0x[0-9a-f]+) size \d+ =====", s)
for i in range(1, len(parts), 3):
    addr, body = parts[i+1], parts[i+2].split("===== END ")[0]
    clean = "\n".join(ln.split("> ",1)[1] if "> " in ln else ln for ln in body.splitlines())
    pathlib.Path("checks/decomp/%s.c" % addr).write_text(clean, encoding="utf-8")
    print(addr, len(clean))
