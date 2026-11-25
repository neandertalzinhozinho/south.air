import pefile, sys, os, hashlib, struct

PE_PATH  = r"D:\PROJETOS\shadowFILES\analysis\host_reference\startup_capture\original_before_load.vst3"
DUMP_PATH= r"D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin"

RVAS = [0x863170, 0x8637d0, 0x86ec10, 0x72180, 0x1d2e9e0]

def dump_pe(path, label):
    print("="*100)
    print(f"[{label}] {path}")
    print(f"size = {os.path.getsize(path):,} bytes (0x{os.path.getsize(path):X})")
    pe = pefile.PE(path, fast_load=False)
    print(f"Machine=0x{pe.FILE_HEADER.Machine:X}  Characteristics=0x{pe.FILE_HEADER.Characteristics:X}")
    print(f"ImageBase=0x{pe.OPTIONAL_HEADER.ImageBase:X}  EntryPoint=0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:X}  SectionAlignment=0x{pe.OPTIONAL_HEADER.SectionAlignment:X}  FileAlignment=0x{pe.OPTIONAL_HEADER.FileAlignment:X}")
    print(f"SizeOfImage=0x{pe.OPTIONAL_HEADER.SizeOfImage:X}  SizeOfHeaders=0x{pe.OPTIONAL_HEADER.SizeOfHeaders:X}")
    print(f"NumberOfSections={pe.FILE_HEADER.NumberOfSections}")
    print("-"*100)
    print(f"{'Name':<12} {'VirtAddr':>12} {'VirtSize':>12} {'RawPtr':>12} {'RawSize':>12} {'RVA==Raw?':>10} {'Chars':>10}")
    for s in pe.sections:
        name = s.Name.rstrip(b'\0').decode('latin1')
        print(f"{name:<12} 0x{s.VirtualAddress:08X}  0x{s.Misc_VirtualSize:08X}  0x{s.PointerToRawData:08X}  0x{s.SizeOfRawData:08X}  {str(s.VirtualAddress==s.PointerToRawData):>10}  0x{s.Characteristics:08X}")
    return pe

pe = dump_pe(PE_PATH, "PE")
dpe = dump_pe(DUMP_PATH, "DUMP")

pe_data = pe.__data__
dump_data = dpe.__data__

print("="*100)
print("RVA BYTE COMPARISON (PE uses get_offset_from_rva; DUMP uses flat offset = RVA)")
print("="*100)
for rva in RVAS:
    print("-"*100)
    print(f"RVA 0x{rva:X}")
    try:
        pe_off = pe.get_offset_from_rva(rva)
        pe_bytes = pe_data[pe_off:pe_off+32]
        print(f"  PE   file_off=0x{pe_off:X} : {pe_bytes.hex(' ')}")
    except Exception as e:
        pe_off = None
        pe_bytes = b''
        print(f"  PE   get_offset_from_rva FAILED: {e}")
    dump_bytes = dump_data[rva:rva+32]
    print(f"  DUMP flat_off=0x{rva:X}     : {dump_bytes.hex(' ')}")
    # also get dump via PE section mapping, to see whether header maps it differently
    try:
        d_off = dpe.get_offset_from_rva(rva)
        db2 = dump_data[d_off:d_off+32]
        print(f"  DUMP pe_mapped_off=0x{d_off:X}: {db2.hex(' ')}  (equal to flat? {db2==dump_bytes})")
    except Exception as e:
        print(f"  DUMP pe_mapped_off FAILED: {e}")
    # search first 16 dump bytes inside PE file
    needle = dump_bytes[:16]
    positions = []
    start = 0
    while True:
        idx = pe_data.find(needle, start)
        if idx == -1:
            break
        positions.append(idx)
        start = idx + 1
        if len(positions) > 20: break
    print(f"  search 16 dump bytes in PE -> offsets: {[hex(p) for p in positions[:20]]} (count={len(positions)})")
    # search dump bytes in dump itself beyond the RVA
    positions2 = []
    start = 0
    while True:
        idx = dump_data.find(needle, start)
        if idx == -1: break
        positions2.append(idx)
        start = idx + 1
        if len(positions2) > 10: break
    print(f"  search 16 dump bytes in DUMP -> offsets: {[hex(p) for p in positions2[:10]]}")

print("="*100)
print("GLOBAL SEARCH: do dump bytes for factory appear anywhere in PE raw section data?")
print("="*100)
for rva in RVAS:
    needle = dump_data[rva:rva+16]
    hit = pe_data.find(needle)
    print(f"  RVA 0x{rva:X} needle={needle.hex(' ')} -> PE offset {hex(hit) if hit>=0 else 'NOT FOUND'}")

print("="*100)
print("HEADER FIRST BYTES")
print("="*100)
print("  PE   [0:64] :", pe_data[:64].hex(' '))
print("  DUMP [0:64] :", dump_data[:64].hex(' '))
print("  PE MZ/PE sig:", pe_data[:2], pe_data[pe_data.find(b'PE\0\0'):pe_data.find(b'PE\0\0')+4] if pe_data.find(b'PE\0\0')>=0 else None)
print("  DUMP MZ/PE sig:", dump_data[:2], dump_data[dump_data.find(b'PE\0\0'):dump_data.find(b'PE\0\0')+4] if dump_data.find(b'PE\0\0')>=0 else None)
print("  DUMP PE header offset:", hex(struct.unpack_from('<I', dump_data, 0x3c)[0]))
