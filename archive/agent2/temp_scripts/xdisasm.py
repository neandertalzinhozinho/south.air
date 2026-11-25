import pefile, capstone, sys
p = r'D:\PROJETOS\shadowFILES\analysis\startup_audit\final_candidate_wrapperstub.vst3'
pe = pefile.PE(p, fast_load=True)
image_base = pe.OPTIONAL_HEADER.ImageBase
rva = int(sys.argv[1], 16)
n = int(sys.argv[2]) if len(sys.argv) > 2 else 1200

def rva2off(r):
    for s in pe.sections:
        va = s.VirtualAddress
        if va <= r < va + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (r - va)
    return None

off = rva2off(rva)
data = pe.__data__[off:off+n]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = False
for ins in md.disasm(data, image_base + rva):
    print(f'0x{ins.address-image_base:08x}  {ins.mnemonic:<8} {ins.op_str}')
