import struct, math, collections, sys

p = r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d = open(p, 'rb').read()
IMAGEBASE = 0x180000000
SIZE = len(d)

def u16(o): return struct.unpack_from('<H', d, o)[0]
def u32(o): return struct.unpack_from('<I', d, o)[0]
def u64(o): return struct.unpack_from('<Q', d, o)[0]

print('filesize == SizeOfImage:', hex(SIZE))

# section table
pe_off = u32(0x3c)
num = u16(pe_off + 6)
opt = u16(pe_off + 20)
sect = pe_off + 24 + opt
print('sections', num)
secs = []
for i in range(num):
    off = sect + i*40
    name = d[off:off+8].rstrip(b'\0').decode(errors='replace')
    vsize, va, rawsize, rawptr = struct.unpack_from('<IIII', d, off+8)
    secs.append((name, va, vsize, rawptr, rawsize))
    print(f'{name:10s} rva={hex(va)} vsize={hex(vsize)} rawptr={hex(rawptr)} rawsize={hex(rawsize)}')

def rva2off(rva):
    return rva  # flat virtual dump hypothesis

# entropy of virtual regions
def entropy(off, n):
    chunk = d[off:off+n]
    if not chunk: return 0
    c = collections.Counter(chunk)
    m = len(chunk)
    return -sum((v/m)*math.log2(v/m) for v in c.values())

for name, va, vsize, rawptr, rawsize in secs:
    if name in ('.text', 'IPPCODE', '.rdata', '.data', '.text001', '.guard', '.proxy'):
        print('entropy VA-layout', name, round(entropy(va, min(vsize, 8_000_000)), 3))

# exports at dir 0
dd = pe_off + 24 + opt
exp_rva, exp_size = struct.unpack_from('<II', d, dd)
print('export dir rva', hex(exp_rva), 'size', hex(exp_size))
if exp_rva and exp_rva < SIZE:
    eo = exp_rva
    def rd(rva): return rva
    chars, ts, major, minor, name_rva, base, nfunc, nname, funcs_rva, names_rva, ords_rva = struct.unpack_from('<IIHHIIIIII', d, eo)
    print('base', base, 'nfunc', nfunc, 'nname', nname)
    names = []
    for i in range(min(nname, 300)):
        nr = u32(names_rva + 4*i)
        end = d.index(b'\0', nr)
        names.append(d[nr:end].decode(errors='replace'))
    print('exports:', names[:40], '... total', len(names))
    for i in range(min(nfunc, 10)):
        print(' func', i, hex(u32(funcs_rva + 4*i) + IMAGEBASE))

# imports dir 1
imp_rva, imp_size = struct.unpack_from('<II', d, dd + 8)
print('import dir rva', hex(imp_rva), 'size', hex(imp_size))
if imp_rva and imp_rva < SIZE:
    o = imp_rva
    while True:
        ilt, ts, fwd, nm, iat = struct.unpack_from('<IIIII', d, o)
        if not (ilt or nm): break
        end = d.index(b'\0', nm)
        dll = d[nm:end].decode(errors='replace')
        names = []
        t = ilt or iat
        while True:
            v = u64(t)
            if v == 0: break
            if v & 0x8000000000000000:
                names.append('ord%d' % (v & 0xffff))
            else:
                no = (v & 0x7fffffff) + 2
                e = d.index(b'\0', no)
                names.append(d[no:e].decode(errors='replace'))
            t += 8
        print(' ', dll, len(names), names[:6])
        o += 20
