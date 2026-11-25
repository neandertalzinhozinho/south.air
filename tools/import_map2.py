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

# descriptor containing Name -> api-ms-win-crt-math-l1-1-0.dll
seed = 0x2175050 - 0x0C
start = seed
while start >= 0x1D8C000:
    if u32(start) == 0 and u32(start + 0x0C) == 0 and u32(start + 0x10) == 0 and u32(start + 0x04) == 0 and u32(start + 0x08) == 0:
        break
    start -= 0x14
start += 0x14

rows = []
o = start
while True:
    oft, ts, fc, name, ft = struct.unpack_from('<IIIII', d, o)
    if oft == 0 and name == 0 and ft == 0:
        break
    dll = cstr(name)
    t = oft if oft else ft
    k = 0
    while True:
        ent = u64(t + 8 * k)
        if ent == 0:
            break
        slot = ft + 8 * k
        if ent & 0x8000000000000000:
            rows.append((dll, 'ord#%d' % (ent & 0xffff), slot))
        else:
            rows.append((dll, cstr(ent + 2), slot))
        k += 1
    o += 0x14

print('descriptor start 0x%X' % start)
print('total imports:', len(rows))
with open(r'checks\import_map.txt', 'w') as f:
    for dll, nm, slot in rows:
        line = '0x%X  %-46s %s' % (slot, nm, dll)
        f.write(line + '\n')
        print(line)
