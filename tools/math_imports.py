import sys, struct
sys.path.insert(0, r'tools')
import re_lib

d = re_lib.data()

def u32(o): return struct.unpack_from('<I', d, o)[0]
def u64(o): return struct.unpack_from('<Q', d, o)[0]
def cstr(o):
    e = d.index(b'\x00', o)
    return d[o:e].decode('latin-1')

MATH_INT = 0x2176878
MATH_IAT = 0x1D8D790

names = []
o = MATH_INT
while True:
    ent = u32(o)
    if ent == 0:
        break
    names.append(cstr(ent + 2))
    o += 8

print('math imports:', len(names))
for k, nm in enumerate(names):
    print('  k=%2d  IAT 0x%X  %s' % (k, MATH_IAT + 8 * k, nm))

with open(r'checks\math_imports.txt', 'w', encoding='utf-8') as f:
    for k, nm in enumerate(names):
        f.write('k=%2d  IAT 0x%X  %s\n' % (k, MATH_IAT + 8 * k, nm))
