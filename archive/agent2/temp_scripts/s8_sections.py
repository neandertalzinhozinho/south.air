import pefile

P = r"D:\PROJETOS\shadowFILES\analysis\startup_audit\final_candidate.vst3"
p = pefile.PE(P, fast_load=True)
print("entry", hex(p.OPTIONAL_HEADER.AddressOfEntryPoint), "base", hex(p.OPTIONAL_HEADER.ImageBase))
for s in p.sections:
    name = s.Name.rstrip(b"\x00").decode(errors="replace")
    print(f"{name:12s} va={s.VirtualAddress:#x} vs={s.Misc_VirtualSize:#x} "
          f"raw={s.SizeOfRawData:#x} exec={bool(s.Characteristics & 0x20000000)}")

for rva in (3199760, 13068080, 3199792, 3206416, 3199680, 3199728):
    where = None
    for s in p.sections:
        lo, hi = s.VirtualAddress, s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData)
        if lo <= rva < hi:
            name = s.Name.rstrip(b"\x00").decode(errors="replace")
            where = f"{name} exec={bool(s.Characteristics & 0x20000000)} +{rva - lo:#x}"
    print(f"rva {rva:>9d} {rva:#010x} -> {where}")
