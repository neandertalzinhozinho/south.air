import json, struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

A = Path(r'D:\PROJETOS\shadowFILES\analysis\startup_audit')
CAND = A / 'final_candidate_wrapperstub.vst3'


def sections(p):
    b = p.read_bytes()
    e = struct.unpack_from('<I', b, 0x3C)[0]
    nsec = struct.unpack_from('<H', b, e + 6)[0]
    optsz = struct.unpack_from('<H', b, e + 20)[0]
    st = e + 24 + optsz
    out = {}
    for i in range(nsec):
        o = st + i * 40
        nm = b[o:o + 8].rstrip(b'\x00').decode('latin-1')
        vsz, va, rsz, rptr = struct.unpack_from('<IIII', b, o + 8)
        out[nm] = (va, vsz, rptr, rsz)
    return b, out


b, secs = sections(CAND)


def read_rva(rva, n):
    for nm, (va, vsz, rptr, rsz) in secs.items():
        if va <= rva < va + max(vsz, rsz):
            off = rptr + (rva - va)
            return b[off:off + n]
    raise KeyError(hex(rva))


md = Cs(CS_ARCH_X86, CS_MODE_64)
for name, rva in [('normalizedParamToPlain', 0x3185e0), ('plainParamToNormalized', 0x318630),
                  ('getParamNormalized', 0x318680), ('setParamNormalized', 0x3186b0),
                  ('getParameterInfo', 0x318440), ('getParameterCount', 0x318420),
                  ('norm_cb_0x3351a0', 0x3351a0), ('norm_cb_0x3351e0', 0x3351e0)]:
    code = read_rva(rva, 48)
    print(f'\n=== {name} @0x{rva:X}  {code[:24].hex()}')
    for ins in md.disasm(code, rva):
        print(f'  0x{ins.address:X}: {ins.mnemonic} {ins.op_str}')
        if ins.address - rva > 30:
            break
