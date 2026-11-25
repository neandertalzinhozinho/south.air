import pefile
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
pe = pefile.PE(str(DLL))
BASE = pe.OPTIONAL_HEADER.ImageBase
raw = DLL.read_bytes()
md = Cs(CS_ARCH_X86, CS_MODE_64)

def off(rva):
    return pe.get_offset_from_rva(rva)

def show(rva, n=48):
    print(f'===== DLL RVA {rva:#x} (VA {BASE+rva:#x}, off {off(rva):#x}) =====')
    b = raw[off(rva):off(rva)+n]
    for i in md.disasm(b, BASE+rva):
        print(f'{i.address-BASE:08x}  {i.bytes.hex():<22} {i.mnemonic} {i.op_str}')

for r in [0x444c30, 0x45aca0, 0x45ad20, 0x45ad60]:
    show(r, 0x50)
