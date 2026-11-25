import sys, struct
sys.path.insert(0, r'tools')
import re_lib

d = re_lib.data()

def u32(o): return struct.unpack_from('<I', d, o)[0]
def i32(o): return struct.unpack_from('<i', d, o)[0]
def cstr(o):
    e = d.index(b'\x00', o)
    return d[o:e].decode('latin-1')

DESC = 0x2174EFC
STRIDE = 0x14

descs = []
for i in range(400):
    o = DESC + i * STRIDE
    name, iat, intt = u32(o), u32(o + 4), u32(o + 8)
    if name == 0 and iat == 0 and intt == 0:
        break
    descs.append((cstr(name) if 0x1000 < name < len(d) else '?', iat, intt))

# names(INT of desc i) pair with IAT of desc i+1
iat_names = {}   # slot -> (name, dll)
for i in range(len(descs) - 1):
    dll, iat, intt = descs[i]
    ndll, niat, nintt = descs[i + 1]
    if not (0x1000 < intt < len(d)):
        continue
    names = []
    j = intt
    while True:
        ent = u32(j)
        if ent == 0 or len(names) > 5000:
            break
        names.append(cstr(ent + 2) if 0x1000 < ent < len(d) else None)
        j += 8
    for k, nm in enumerate(names):
        if nm:
            iat_names[niat + 8 * k] = (nm, ndll)

# scan for FF 25 thunks
thunks = {}
i = 0x1000
end = 0x1CD5487
needle = b'\xff\x25'
while True:
    j = d.find(needle, i, end)
    if j < 0:
        break
    disp = i32(j + 2)
    tgt = j + 6 + disp
    if tgt in iat_names:
        thunks[j] = (tgt, iat_names[tgt])
    i = j + 1

print('resolved thunks:', len(thunks))
with open(r'checks\thunk_map.txt', 'w', encoding='utf-8') as f:
    for a in sorted(thunks):
        tgt, (nm, dll) = thunks[a]
        f.write('0x%X -> IAT 0x%X  %s  [%s]\n' % (a, tgt, nm, dll))

# quick check of requested ones
for a in (0x1C9A5AD, 0x1C84A0, 0x1C8500, 0x1C8530, 0x1C9A9C5, 0x1C9AA01):
    print('0x%X ->' % a, thunks.get(a, 'NOT A NAMED THUNK'))
