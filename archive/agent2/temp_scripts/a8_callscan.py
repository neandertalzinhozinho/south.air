import pefile
from pathlib import Path
DLL=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
pe=pefile.PE(str(DLL)); B=pe.OPTIONAL_HEADER.ImageBase; raw=DLL.read_bytes()
TARGET=0x444814  # dump_238800 in DLL
for s in pe.sections:
    if not (s.Characteristics & 0x20000000):  # IMAGE_SCN_MEM_EXECUTE
        continue
    start=s.VirtualAddress; end=start+max(s.Misc_VirtualSize,s.SizeOfRawData)
    off=s.PointerToRawData
    blob=raw[off:off+(end-start)]
    for i,b in enumerate(blob):
        if b==0xE8 and i+5<=len(blob):
            import struct
            rel=struct.unpack_from('<i',blob,i+1)[0]
            if start+i+5+rel==TARGET:
                print(f'call at DLL {start+i:#x} -> {TARGET:#x}, retaddr {start+i+5:#x}, section {s.Name}')
        elif b==0xE9 and i+5<=len(blob):
            rel=struct.unpack_from('<i',blob,i+1)[0]
            if start+i+5+rel==TARGET:
                print(f'jmp  at DLL {start+i:#x} -> {TARGET:#x}, section {s.Name}')
