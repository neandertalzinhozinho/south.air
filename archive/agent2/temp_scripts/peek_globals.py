import pefile, struct, sys
CAND = r'D:\PROJETOS\shadowFILES\analysis\startup_audit\final_candidate_wrapperstub.vst3'
ORAC = r'D:\PROJETOS\shadowFILES\analysis\host_reference\startup_capture\original_before_load.vst3'

def load(p):
    pe = pefile.PE(p, fast_load=True)
    return pe, pe.OPTIONAL_HEADER.ImageBase

def rva2off(pe, r):
    for s in pe.sections:
        va = s.VirtualAddress
        if va <= r < va + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (r - va)
    return None

def qwords(pe, rva, n=8):
    off = rva2off(pe, rva)
    if off is None:
        return None
    return [hex(struct.unpack('<Q', pe.__data__[off + 8 * i: off + 8 * i + 8])[0]) for i in range(n)]

pc, bc = load(CAND)
po, bo = load(ORAC)
print('image bases', hex(bc), hex(bo))
for rva in (0x21D0540, 0x26AFCF0, 0x21D0538, 0x26AFCE8, 0x26AFCF8):
    print(hex(rva))
    print('  cand', qwords(pc, rva, 4))
    print('  orac', qwords(po, rva, 4))
