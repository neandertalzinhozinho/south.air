import sys, struct
sys.path.insert(0, r'tools')
import re_lib

d = re_lib.data()

def u16(o): return struct.unpack_from('<H', d, o)[0]
def u32(o): return struct.unpack_from('<I', d, o)[0]
def u64(o): return struct.unpack_from('<Q', d, o)[0]
def cstr(o):
    e = d.index(b'\x00', o)
    return d[o:e].decode('latin-1')

IMP_RVA = 0x79CF76C
IAT_LO, IAT_HI = 0x1D8D000, 0x1D8E000

rows = []
o = IMP_RVA
while True:
    oft = u32(o + 0x00)
    name = u32(o + 0x0C)
    ft = u32(o + 0x10)
    if oft == 0 and name == 0 and ft == 0:
        break
    dll = cstr(name)
    t = oft if oft else ft
    iat = ft
    k = 0
    while True:
        ent = u64(t + 8 * k)
        if ent == 0:
            break
        slot = iat + 8 * k
        if ent & 0x8000000000000000:
            rows.append((dll, 'ord#%d' % (ent & 0xffff), slot, None))
        else:
            hint = u16(ent)
            nm = cstr(ent + 2)
            rows.append((dll, nm, slot, hint))
        k += 1
    o += 0x14

print('total imports:', len(rows))
for dll, nm, slot, hint in rows:
    print('0x%X  %-40s %s' % (slot, nm, dll))
