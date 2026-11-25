import pefile, struct, math, collections, os

ROOT = r'D:\PROJETOS\shadowFILES'

def stats(tag, b):
    n = len(b)
    c = collections.Counter(b)
    ent = -sum((v / n) * math.log2(v / n) for v in c.values() if v)
    printable = sum(1 for x in b if 32 <= x < 127 or x in (9, 10, 13))
    zero = c.get(0, 0)
    print('%-26s %9d B  H=%.2f  impr=%.1f%%  zero=%.1f%%' % (tag, n, ent, 100.0 * printable / n, 100.0 * zero / n))

def sec_bytes(path, name):
    pe = pefile.PE(path, fast_load=True)
    for s in pe.sections:
        nm = s.Name.rstrip(b'\x00').decode('latin1')
        if nm == name:
            f = open(path, 'rb'); f.seek(s.PointerToRawData)
            b = f.read(s.SizeOfRawData); f.close()
            return b, s.Misc_VirtualSize, s.SizeOfRawData
    return None, 0, 0

pa = os.path.join(ROOT, r'analysis\host_reference\startup_capture\original_before_load.vst3')
A, Avs, Araw = sec_bytes(pa, '.data')
F, Fvs, Fraw = sec_bytes(os.path.join(ROOT, 'soothe3_unpacked_fixed.pe'), '.data')
U, Uvs, Uraw = sec_bytes(os.path.join(ROOT, r'analysis\startup_audit\final_candidate_uni46c.vst3'), '.data')
d = os.path.join(ROOT, 'soothe3_unpacked_mem.bin')
f = open(d, 'rb'); f.seek(0x217f000); D = f.read(0x5d8df8); f.close()

print('vsize/raw: A=0x%X/0x%X  fixed=0x%X/0x%X  uni46c=0x%X/0x%X' % (Avs, Araw, Fvs, Fraw, Uvs, Uraw))
stats('buildA .data (file)', A)
stats('fixed.pe .data', F)
stats('uni46c .data', U)
stats('dump .data', D)

print('\nidentidade:')
print('  fixed == dump : %s' % (F[:len(D)] == D[:len(F)]))
def eq(a, b):
    n = min(len(a), len(b)); dd = sum(1 for i in range(n) if a[i] != b[i])
    return dd, n
dd, n = eq(A, U); print('  buildA vs uni46c: %d/%d diferentes (%.4f%%)' % (dd, n, 100.0 * dd / n))
dd, n = eq(D, U); print('  dump   vs uni46c: %d/%d diferentes (%.4f%%)' % (dd, n, 100.0 * dd / n))

# bloco de 64 bytes em comum? procura alinhamento do dump dentro do arquivo A
print('\nprocurando o 1o bloco de 32 B do dump .data dentro do buildA .data:')
probe = D[:32]
idx = A.find(probe)
print('  D[0:32] em A -> %s' % (idx,))
for off in (0, 1000, 100000, 1000000, 2000000):
    p = D[off:off + 32]
    print('  D[%d:%d] em A -> %s' % (off, off + 32, A.find(p)))

# histograma de ponteiros com filtro canonico
w = len(D) // 8
vals = struct.unpack('<%dQ' % w, D[:w * 8])
ptr = [v for v in vals if 0x10000 <= v < 0x800000000000]
print('\nqwords=%d  no range canonico [64K,2^47)=%d' % (w, len(ptr)))
print('  <=0x00007FFF_FFFF (32-bit-ish): %d' % sum(1 for v in ptr if v < 0xFFFFF0FF))
print('  >=0x00000100_00000000 (>4GB):   %d' % sum(1 for v in ptr if v >= 0x100000000))

img_end = 0x82A4F00
best = []
for base in range(0x7F000000, 0x80000000, 0x10000):
    h = sum(1 for v in ptr[:60000] if 0 <= v - base < img_end)
    if h > 20:
        best.append((h, base))
best.sort(reverse=True)
print('  top bases 0x7F000000..0x80000000 (passo 64K):', [('0x%X' % b, h) for h, b in best[:5]])
