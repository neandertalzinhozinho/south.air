"""Enumerate every MSVC RTTI class in the flat dump.

Layout (x64):
  TypeDescriptor : void* pVFTable; void* spare; char name[]   (name starts +16)
  CompleteObjectLocator (24 bytes):
      u32 signature(=1); u32 offset; u32 cdOffset;
      u32 pTypeDescriptor; u32 pClassDescriptor; u32 pSelf
  vtable[-8] holds (COL + ABS_BASE)

Writes docs/engine/rtti_classes.csv: vtable_rva, class_name, col_rva
"""
import sys, struct, csv, os
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib

d = re_lib.data()
BASE = 0x199B0000
RD_LO, RD_HI = 0x1D80000, 0x2760000   # .rdata/.data span
TEXT_HI = 0x1D8BB7D

def u32(o): return struct.unpack_from('<I', d, o)[0]

# 1. collect TypeDescriptors
td = {}
for prefix in (b'.?AV', b'.?AU', b'.?AW'):
    s = 0
    while True:
        n = d.find(prefix, s)
        if n < 0:
            break
        s = n + 1
        start = n - 16
        if start < 0:
            continue
        name = re_lib.cstr(n, 300)
        if not name or len(name) < 4:
            continue
        td[start] = name

print(f'type descriptors: {len(td)}')

# 2. find COLs referencing them
cols = {}
lo = RD_LO & ~3
seg = d[lo:RD_HI]
for i, (v,) in enumerate(struct.iter_unpack('<I', seg)):
    if v not in td:
        continue
    col = lo + i * 4 - 12          # pTypeDescriptor sits at COL+12
    if col < 0 or u32(col) != 1:
        continue
    cd = u32(col + 16)
    if not (RD_LO <= cd < RD_HI):
        continue
    cols[col] = td[v]

print(f'COLs: {len(cols)}')

# 3. resolve vtable from COL reference
rows = []
for col, name in cols.items():
    vt = None
    pat = struct.pack('<Q', col + BASE)
    p = d.find(pat, RD_LO)
    if p >= 0 and (p + 8) < RD_HI:
        vt = p + 8
    rows.append((vt, name, col))

found = sum(1 for r in rows if r[0] is not None)
print(f'vtables resolved: {found}/{len(rows)}')

out = r'D:\PROJETOS\soultree\docs\engine\rtti_classes.csv'
os.makedirs(os.path.dirname(out), exist_ok=True)
rows.sort(key=lambda r: (r[1] or '', r[0] or 0))
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['vtable_rva', 'class_name', 'col_rva'])
    for vt, name, col in rows:
        w.writerow([f'0x{vt:X}' if vt else '', name, f'0x{col:X}'])

if len(sys.argv) > 1:
    needle = sys.argv[1].lower()
    for vt, name, col in rows:
        if needle in name.lower():
            print(f'  0x{vt:X}' if vt else '  -        ', name)
