import pefile, math, collections, sys

p = sys.argv[1] if len(sys.argv) > 1 else r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
pe = pefile.PE(p, fast_load=True)
print('Machine', hex(pe.FILE_HEADER.Machine), 'Chars', hex(pe.FILE_HEADER.Characteristics))
print('ImageBase', hex(pe.OPTIONAL_HEADER.ImageBase), 'Entry', hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
print('SizeOfImage', hex(pe.OPTIONAL_HEADER.SizeOfImage), 'FileAlign', hex(pe.OPTIONAL_HEADER.FileAlignment), 'SectAlign', hex(pe.OPTIONAL_HEADER.SectionAlignment))
for s in pe.sections:
    d = s.get_data()
    ent = 0.0
    if d:
        cnt = collections.Counter(d)
        n = len(d)
        ent = -sum((c/n)*math.log2(c/n) for c in cnt.values())
    print(f"{s.Name.rstrip(chr(0).encode()).decode(errors='replace'):10s} VA={hex(pe.OPTIONAL_HEADER.ImageBase+s.VirtualAddress)} vsize={hex(s.Misc_VirtualSize)} raw={hex(s.SizeOfRawData)} off={hex(s.PointerToRawData)} ent={ent:.2f}")
print('dirs:')
for i, d in enumerate(pe.OPTIONAL_HEADER.DATA_DIRECTORY):
    if d.VirtualAddress:
        print(i, hex(d.VirtualAddress), hex(d.Size))
