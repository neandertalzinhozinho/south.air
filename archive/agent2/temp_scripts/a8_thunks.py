import pefile
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

DLL=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
pe=pefile.PE(str(DLL)); B=pe.OPTIONAL_HEADER.ImageBase; raw=DLL.read_bytes()
md=Cs(CS_ARCH_X86,CS_MODE_64)
def show(rva,n=0x180):
    o=pe.get_offset_from_rva(rva)
    print(f'=== DLL {rva:#x} off {o:#x} ===')
    for i in md.disasm(raw[o:o+n],B+rva):
        print(f'{i.address-B:08x}  {i.bytes.hex():<20} {i.mnemonic} {i.op_str}')
for r in (0x3cea00,0x3ceb40,0x3cec00,0x3ced80):
    show(r,0x120)
