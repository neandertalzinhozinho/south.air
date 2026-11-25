import re, pathlib
raw = pathlib.Path("checks/ghidra_F.txt").read_bytes()
for enc in ("utf-16", "utf-8"):
    try:
        s = raw.decode(enc)
        break
    except Exception:
        continue
parts = re.split(r"===== FUNCTION (\S+) @ (0x[0-9a-f]+) size \d+ =====", s)
out = pathlib.Path("checks/decomp"); out.mkdir(exist_ok=True)
for i in range(1, len(parts), 3):
    name, addr, body = parts[i], parts[i+1], parts[i+2]
    body = body.split("===== END ")[0]
    clean = "\n".join(ln.split("> ",1)[1] if "> " in ln else ln for ln in body.splitlines())
    (out / (addr + ".c")).write_text(clean, encoding="utf-8")
    print(addr, name, len(clean))
