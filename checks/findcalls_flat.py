import re, struct, sys

DUMP = r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin"
d = open(DUMP, "rb").read()
targets = {int(a, 16): [] for a in sys.argv[1:]}
for m in re.finditer(b"\xe8", d):
    i = m.start()
    if i + 5 > len(d):
        break
    rel = struct.unpack_from("<i", d, i + 1)[0]
    t = i + 5 + rel
    if t in targets:
        targets[t].append(i)
for t, v in targets.items():
    print(hex(t), [hex(x) for x in v])
