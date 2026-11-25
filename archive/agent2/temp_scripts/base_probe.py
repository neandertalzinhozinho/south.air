import pefile, struct, collections, hashlib, os

ROOT = r'D:\PROJETOS\shadowFILES'
fixed = os.path.join(ROOT, 'soothe3_unpacked_fixed.pe')
pe_f = pefile.PE(fixed, fast_load=True)
secs = [(s.Name.rstrip(b'\x00').decode('latin1'), s.VirtualAddress, s.Misc_VirtualSize,
         s.PointerToRawData, s.SizeOfRawData) for s in pe_f.sections]
image_end = max(va + vs for _, va, vs, _, _ in secs)
print('image_end = 0x%X (%.1f MB)' % (image_end, image_end / 1048576))
print('sections:', [(n, hex(va), hex(vs)) for n, va, vs, _, _ in secs])

DUMP = os.path.join(ROOT, 'soothe3_unpacked_mem.bin')
f = open(DUMP, 'rb')
dva, dvs = 0x217f000, 0x5d8df8
f.seek(dva)
raw = f.read(dvs)
print('dump .data lido: %d B' % len(raw))

w = len(raw) // 8
vals = struct.unpack('<%dQ' % w, raw[:w * 8])
nz = [v for v in vals if v]
big = [v for v in nz if v >= 0x100000000]
print('palavras=%d  nao_zero=%d (%.2f%%)  >=4GB=%d (%.2f%% de nz)' %
      (w, len(nz), 100.0 * len(nz) / w, len(big), 100.0 * len(big) / max(1, len(nz))))

c = collections.Counter(v >> 26 for v in big)
print('top buckets de 64MB (inicio, contagem, %):')
for b, k in c.most_common(8):
    print('   0x%X0000000  %7d  %.1f%%' % (b * 4, k, 100.0 * k / len(big)))

print('min=0x%X  max=0x%X' % (min(big), max(big)))

sample = big[:300000]
def hits(base):
    h = 0
    for v in sample:
        r = v - base
        if 0 <= r < image_end:
            for n, va, vs, _, _ in secs:
                if va <= r < va + vs:
                    h += 1
                    break
    return h

cands = {
    '0x180000000 (header)': 0x180000000,
    '0x18CC0000 (doc)': 0x18CC0000,
    '0x18000000 (doc-1nibble)': 0x18000000,
    '0x206800000 (tls hint V1)': 0x206800000,
    '0x206800000-? tls-C158': 0x2068C158 - 0xC158,
}
mn = min(big)
for k in range(0, 4):
    cands['min-0x%X' % (k * 0x1000)] = (mn & ~0xFFFF) - k * 0x1000
cands['min&~0xFFFFF'] = mn & ~0xFFFFF

print('--- teste de base (amostra=%d palavras) ---' % len(sample))
for name in sorted(cands, key=lambda n: -hits(cands[n])):
    print('   %-28s 0x%X  hits=%d (%.1f%%)' % (name, cands[name], hits(cands[name]), 100.0 * hits(cands[name]) / len(sample)))

# comparacao de bytes: dump .data vs build A file .data
pa = os.path.join(ROOT, r'analysis\host_reference\startup_capture\original_before_load.vst3')
pea = pefile.PE(pa, fast_load=True)
dA = None
for s in pea.sections:
    nm = s.Name.rstrip(b'\x00').decode('latin1')
    if nm == '.data':
        dA = (s.Misc_VirtualSize, s.SizeOfRawData, s.PointerToRawData)
        print('.data buildA: vsize=0x%X raw=0x%X ptr=0x%X' % dA)
fa = open(pa, 'rb'); fa.seek(dA[2]); rawA = fa.read(dA[1]); fa.close()

n_raw = min(len(rawA), len(raw))
diff_raw = sum(1 for i in range(n_raw) if rawA[i] != raw[i])
print('dump .data[0:%d] vs buildA .data raw: %d bytes diferentes (%.2f%%)' % (n_raw, diff_raw, 100.0 * diff_raw / n_raw))

# tail do dump vs tail do fixed.pe
for s in pe_f.sections:
    nm = s.Name.rstrip(b'\x00').decode('latin1')
    if nm == '.data':
        pf, pr = s.PointerToRawData, s.SizeOfRawData
ff = open(fixed, 'rb'); ff.seek(pf + pr); tailF = ff.read(dvs - pr); ff.close()
tailD = raw[pr:]
print('tail len: dump=%d fixed=%d' % (len(tailD), len(tailF)))
n = min(len(tailD), len(tailF))
dl = sum(1 for i in range(n) if tailD[i] != tailF[i])
print('tail dump vs tail fixed.pe: %d bytes diferentes (%.2f%%)' % (dl, 100.0 * dl / n))
print('tail fixed sha=%s  tail dump sha=%s' % (hashlib.sha256(tailF).hexdigest()[:16], hashlib.sha256(tailD).hexdigest()[:16]))
print('tail dump nao-zero: %d de %d' % (sum(1 for b in tailD if b), len(tailD)))
f.close()
