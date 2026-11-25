import pefile, capstone
p = r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll'
pe = pefile.PE(p)
print('ImageBase', hex(pe.OPTIONAL_HEADER.ImageBase))
for s in pe.sections:
    print(s.Name.decode().rstrip('\0'), 'VA', hex(s.VirtualAddress), 'VS', hex(s.Misc_VirtualSize), 'raw', hex(s.PointerToRawData), hex(s.SizeOfRawData))

data = open(p,'rb').read()
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
for rva, size, label in [(0x61563f, 0x80, 'dump_71360 in DLL'), (0xf5977, 0x40, 'dump_6f360 call sites?'), (0x61d895, 0x40, 'dump_24140b in DLL')]:
    off = rva2off(rva)
    print(f'\n=== {label}: RVA {rva:#x} fileoff {off:#x} ===')
    b = data[off:off+size]
    print('raw:', ' '.join(f'{x:02x}' for x in b[:64]))
    for ins in md.disasm(b, pe.OPTIONAL_HEADER.ImageBase + rva):
        print(f'  +{ins.address - (pe.OPTIONAL_HEADER.ImageBase+rva):03x}: {ins.mnemonic:<8} {ins.op_str}')
