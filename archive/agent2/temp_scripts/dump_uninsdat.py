import re

p = r"C:\ProgramData\oeksound\soothe3\unins000.dat"
blob = open(p, "rb").read()
print("size", len(blob))
print("--- ascii strings >=4 ---")
for m in re.finditer(rb"[ -~]{4,200}", blob):
    print(m.group().decode("latin1"))
print("--- utf16 strings >=4 ---")
for m in re.finditer(rb"(?:[ -~]\x00){4,200}", blob):
    print(m.group().decode("utf-16-le", "ignore"))
