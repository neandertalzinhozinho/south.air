import pefile, math, os, struct
from collections import Counter

PE_PATH  = r"D:\PROJETOS\shadowFILES\analysis\host_reference\startup_capture\original_before_load.vst3"
DUMP_PATH= r"D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin"
pe = pefile.PE(PE_PATH, fast_load=False)
dpe = pefile.PE(DUMP_PATH, fast_load=False)
P, D = pe.__data__, dpe.__data__

def ent(b):
    if not b: return 0.0
    c = Counter(b); n = len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

print("DATA DIRECTORIES (PE vs DUMP) - index, VA, Size")
for i in range(16):
    a = pe.OPTIONAL_HEADER.DATA_DIRECTORY[i]
    b = dpe.OPTIONAL_HEADER.DATA_DIRECTORY[i]
    same = (a.VirtualAddress==b.VirtualAddress and a.Size==b.Size)
    print(f"  dir[{i:2}] PE=0x{a.VirtualAddress:08X}/0x{a.Size:08X}  DUMP=0x{b.VirtualAddress:08X}/0x{b.Size:08X}  same={same}")

print("\nSECTION SHIFT: bytes IDA-as-PE would read at RVA vs true flat-dump bytes at RVA")
for s in pe.sections:
    name = s.Name.rstrip(b'\0').decode('latin1')
    va, raw, rs, vs = s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData, s.Misc_VirtualSize
    print(f"  {name:<10} VA=0x{va:08X} RawPtr=0x{raw:08X} shift(VA-RawPtr)=0x{va-raw:08X} ({va-raw}) VirtualSize=0x{vs:X} RawSize=0x{rs:X}")

print("\nENTROPY / CONTENT COMPARISON PER SECTION (first min(VirtualSize,0x40000) bytes)")
for s in pe.sections:
    name = s.Name.rstrip(b'\0').decode('latin1')
    va, raw, rs, vs = s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData, s.Misc_VirtualSize
    n = min(vs, 0x40000, rs)
    disk = P[raw:raw+n]
    # memory image: flat offset == RVA
    mem  = D[va:va+n]
    # what IDA-as-PE would copy into VA
    ida  = D[raw:raw+n]
    print(f"  {name:<10} n=0x{n:X} H(disk)={ent(disk):.3f} H(mem@RVA)={ent(mem):.3f} equal={disk==mem} "
          f"H(ida-shifted)={ent(ida):.3f} equal(disk,ida)={disk==ida}")

print("\nZERO-FILL / SIZE ACCOUNTING")
tot_vs = sum(s.Misc_VirtualSize for s in pe.sections)
tot_rs = sum(s.SizeOfRawData for s in pe.sections)
print(f"  sum VirtualSize = 0x{tot_vs:X} ({tot_vs:,})  sum RawSize = 0x{tot_rs:X} ({tot_rs:,})  diff = {tot_vs-tot_rs:,}")
print(f"  PE file size = {os.path.getsize(PE_PATH):,}  DUMP file size = {os.path.getsize(DUMP_PATH):,}  SizeOfImage = 0x{pe.OPTIONAL_HEADER.SizeOfImage:X}")

print("\nVERIFY FLAT-IMAGE HYPOTHESIS: header bytes at dump offset 0 should equal PE header bytes")
print("  header[0:0x600] identical:", P[:0x600]==D[:0x600])
print("  PE[0x600:0x610]:", P[0x600:0x610].hex(' '), " DUMP[0x1000:0x1010]:", D[0x1000:0x1010].hex(' '))
