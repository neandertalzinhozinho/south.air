import re, struct, sys

d = open(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin", "rb").read()
want = [int(a, 16) for a in sys.argv[1:]]
hits = {w: [] for w in want}
for m in re.finditer(b"\xff\x15", d):
    i = m.start()
    if i + 6 > len(d):
        break
    disp = struct.unpack_from("<i", d, i + 2)[0]
    t = i + 6 + disp
    if t in hits:
        hits[t].append(i)
for t, v in hits.items():
    print(hex(t), len(v), [hex(x) for x in v[:40]])
