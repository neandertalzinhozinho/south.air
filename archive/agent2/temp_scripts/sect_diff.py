import pefile, os

ROOT = r'D:\PROJETOS\shadowFILES'
A = os.path.join(ROOT, r'analysis\host_reference\startup_capture\original_before_load.vst3')
U = os.path.join(ROOT, r'analysis\startup_audit\final_candidate_uni46c.vst3')

def load(p):
    pe = pefile.PE(p, fast_load=True)
    d = {}
    for s in pe.sections:
        nm = s.Name.rstrip(b'\x00').decode('latin1')
        f = open(p, 'rb'); f.seek(s.PointerToRawData)
        d[nm] = (s.VirtualAddress, s.Misc_VirtualSize, s.SizeOfRawData, f.read(s.SizeOfRawData))
        f.close()
    ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    return pe, d, ep

pa, a, epa = load(A)
pu, u, epu = load(U)
print('entry: buildA=0x%X  uni46c=0x%X  %s' % (epa, epu, 'IGUAL' if epa == epu else 'DIFERENTE'))
print('checksum: 0x%X vs 0x%X' % (pa.OPTIONAL_HEADER.CheckSum, pu.OPTIONAL_HEADER.CheckSum))
print()
print('%-10s %-24s %-24s %s' % ('secao', 'buildA vsize/raw', 'uni46c vsize/raw', 'bytes diferentes'))
for nm in a:
    va_a, vs_a, r_a, b_a = a[nm]
    if nm in u:
        va_u, vs_u, r_u, b_u = u[nm]
        n = min(len(b_a), len(b_u))
        dd = sum(1 for i in range(n) if b_a[i] != b_u[i])
        pct = 100.0 * dd / n if n else 0.0
        flag = 'IGUAL' if dd == 0 and len(b_a) == len(b_u) else '%.2f%%' % pct
        print('%-10s %8X/%-8X %8X/%-8X %s' % (nm, vs_a, r_a, vs_u, r_u, flag))
    else:
        print('%-10s AUSENTE no uni46c (%d B raw)' % (nm, r_a))
extra = [k for k in u if k not in a]
print('secoes novas no uni46c:', extra)
print('relocs: buildA=%d uni46c=%d' % (
    pa.OPTIONAL_HEADER.DATA_DIRECTORY[5].Size, pu.OPTIONAL_HEADER.DATA_DIRECTORY[5].Size))
print('tls dir: buildA != 0 -> %s | uni46c != 0 -> %s' % (
    pa.OPTIONAL_HEADER.DATA_DIRECTORY[9].VirtualAddress,
    pu.OPTIONAL_HEADER.DATA_DIRECTORY[9].VirtualAddress))
