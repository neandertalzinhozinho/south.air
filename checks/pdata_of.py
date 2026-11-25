import struct, sys
d = open(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin", "rb").read()
PD = 0x2758000
addr = int(sys.argv[1], 16)
best = None
for i in range(0, 0x5223000, 12):
    b, e, u = struct.unpack_from("<III", d, PD + i)
    if b == 0 and e == 0:
        break
    if e > b and b <= addr < e:
        best = (b, e, u)
print(sys.argv[1], "->", None if not best else (hex(best[0]), hex(best[1]), hex(best[2])))
