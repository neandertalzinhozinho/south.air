import struct
from pathlib import Path

CAND = Path(r'D:\PROJETOS\shadowFILES\analysis\startup_audit\final_candidate_wrapperstub.vst3')
ORA = Path(r'D:\PROJETOS\shadowFILES\analysis\host_reference\startup_capture\original_before_load.vst3')


def sections(p):
    b = p.read_bytes()
    e = struct.unpack_from('<I', b, 0x3C)[0]
    nsec = struct.unpack_from('<H', b, e + 6)[0]
    optsz = struct.unpack_from('<H', b, e + 20)[0]
    opt = e + 24
    magic = struct.unpack_from('<H', b, opt)[0]
    pe32plus = magic == 0x20b
    ddoff = opt + (112 if pe32plus else 96)
    imgbase = struct.unpack_from('<Q' if pe32plus else '<I', b, opt + (24 if pe32plus else 28))[0]
    st = opt + optsz
    out = []
    for i in range(nsec):
        o = st + i * 40
        name = b[o:o + 8].rstrip(b'\x00').decode('latin-1')
        vsz, va, rsz, rptr = struct.unpack_from('<IIII', b, o + 8)
        out.append(dict(name=name, va=va, vsz=vsz, rptr=rptr, rsz=rsz,
                        file=b[rptr:rptr + max(vsz, rsz)]))
    return b, imgbase, out


def find(secs, name):
    return next(s for s in secs if s['name'] == name)


cb, cbase, cs = sections(CAND)
ob, obase, os_ = sections(ORA)
print('candidate base', hex(cbase), 'sections', len(cs))
print('oracle base', hex(obase), 'sections', len(os_))
for s in cs:
    if s['name'] in ('.imports', '.rdata', '.inits', '.tlsstub'):
        print(f"  {s['name']:10s} va=0x{s['va']:X} vsz=0x{s['vsz']:X} rsz=0x{s['rsz']:X}")
for s in os_:
    if s['name'] in ('.rdata', '.data'):
        print(f"  ORACLE {s['name']:10s} va=0x{s['va']:X} vsz=0x{s['vsz']:X}")

imp = find(cs, '.imports')
rda = find(os_, '.rdata')
print('\n.oracle .rdata va', hex(rda['va']), 'cand .imports va', hex(imp['va']))
n = min(0x2000, imp['rsz'])
o_slice = rda['file'][:n]          # oracle .rdata start = 0x1d8c000
c_slice = imp['file'][:n]
eq = sum(1 for i in range(0, n, 8) if o_slice[i:i + 8] == c_slice[i:i + 8])
print(f'\n{n} bytes / {n//8} qwords | equal {eq} | differ {n//8 - eq}')
zeroc = sum(1 for i in range(0, n, 8) if c_slice[i:i + 8] == b'\x00' * 8)
zeroo = sum(1 for i in range(0, n, 8) if o_slice[i:i + 8] == b'\x00' * 8)
print(f'candidate zero qwords {zeroc} | oracle zero qwords {zeroo}')
print('\nfirst 24 differing qwords:')
k = 0
for i in range(0, n, 8):
    a, b2 = o_slice[i:i + 8], c_slice[i:i + 8]
    if a != b2:
        k += 1
        if k <= 24:
            print(f'  .rdata+0x{i:05X} (rva 0x{rda["va"]+i:X})  oracle={a.hex()}  cand={b2.hex()}  '
                  f'o={int.from_bytes(a,"little"):#x} c={int.from_bytes(b2,"little"):#x}')
print('total differing', k)
