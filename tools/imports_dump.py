import sys, struct
sys.path.insert(0, r'tools')
import re_lib

d = re_lib.data()

def u32(o): return struct.unpack_from('<I', d, o)[0]
def u64(o): return struct.unpack_from('<Q', d, o)[0]
def cstr(o):
    e = d.index(b'\x00', o)
    return d[o:e].decode('latin-1')

DESC = 0x2174EFC
STRIDE = 0x14

rows = []
for i in range(400):
    o = DESC + i * STRIDE
    name, iat, intt = u32(o), u32(o + 4), u32(o + 8)
    if name == 0 and iat == 0 and intt == 0:
        break
    nm = cstr(name) if 0x1000 < name < len(d) else '?'
    rows.append((i, o, nm, iat, intt))

print('descriptors:', len(rows))
for r in rows:
    print('%3d off=0x%X dll=%-22s IAT=0x%X INT=0x%X' % r)

print()
print('--- INT name lists ---')
for r in rows:
    i, o, nm, iat, intt = r
    if not (0x1000 < intt < len(d)):
        continue
    names = []
    j = intt
    while True:
        ent = u32(j)
        if ent == 0 or len(names) > 4000:
            break
        if 0x1000 < ent < len(d):
            names.append(cstr(ent + 2))
        else:
            names.append('<bad 0x%X>' % ent)
        j += 8
    print('desc %d %s INT=0x%X count=%d first=%s' % (i, nm, intt, len(names), names[:6]))
