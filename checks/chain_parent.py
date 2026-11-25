import struct, sys
d = open(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin", "rb").read()
PD = 0x2758000
want = int(sys.argv[1], 16)
ents = []
for i in range(0, 0x5223000, 12):
    b, e, u = struct.unpack_from("<III", d, PD + i)
    if b == 0 and e == 0:
        break
    if e > b:
        ents.append((b, e, u))
for b, e, u in ents:
    if b <= want < e:
        print("direct:", hex(b), hex(e), hex(u))
# chain: unwind info at u, flags in low 3 bits; if (flags>>3)==4 chained
for b, e, u in ents:
    fl = d[u]
    if (fl >> 3) != 4:
        continue
    cb, ce, cu = struct.unpack_from("<III", d, u + 4)
    if cb == want:
        print("chain parent:", hex(b), hex(e), "chained:", hex(cb), hex(ce))
