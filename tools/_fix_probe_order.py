import pathlib

p = pathlib.Path(r"D:\PROJETOS\soultree\checks\fft_generic_probe.rs")
d = p.read_bytes()
s = d.decode("utf-8-sig")
try:
    s2 = s.encode("latin-1").decode("utf-8")
    print("recovered latin1 roundtrip")
    s = s2
except Exception as e:
    print("no roundtrip:", e)

old = 'assert!((8..=12).contains(&order), "s\u00f3 8..12 (rdx = n/2 <= 0x800)");'
new = 'assert!((8..=19).contains(&order), "ordens 8..19 (rdx pode passar de 0x800)");'
print("found old assert:", old in s)
s = s.replace(old, new)
p.write_text(s, encoding="utf-8", newline="\n")
print([l for l in s.splitlines() if "assert!((8" in l])
