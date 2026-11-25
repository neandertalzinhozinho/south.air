import sys, struct
sys.path.insert(0, r'tools')
import re_lib

d = re_lib.data()

def u32(o): return struct.unpack_from('<I', d, o)[0]
def cstr(o):
    e = d.index(b'\x00', o)
    return d[o:e].decode('latin-1')

def ok_rva(x):
    return 0x1000 <= x < 0x82A8000

rows = []
o = 0x2174EFC
while True:
    name, iat, intt, z1, z2 = struct.unpack_from('<IIIII', d, o)
    if name == 0 and iat == 0 and intt == 0:
        break
    try:
        dll = cstr(name)
    except Exception:
        o += 0x14
        continue
    if intt and ok_rva(intt):
        k = 0
        while True:
            ent = u32(intt + 4 * k)
            if ent == 0:
                break
            if not ok_rva(ent):
                break
            try:
                nm = cstr(ent + 2)
            except Exception:
                break
            if all(32 <= ord(c) < 127 for c in nm):
                rows.append((dll, nm, iat + 8 * k))
            k += 1
    o += 0x14

print('total imports:', len(rows))
with open(r'checks\import_map.txt', 'w', encoding='utf-8') as f:
    for dll, nm, slot in rows:
        f.write('0x%X  %-46s %s\n' % (slot, nm, dll))

for dll, nm, slot in rows:
    if 'crt-math' in dll:
        print('0x%X  %-24s %s' % (slot, nm, dll))
