import pefile, capstone
from pathlib import Path
p=pefile.PE(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64); md.detail=True
def dis(rva,n):
    o=p.get_offset_from_rva(rva); b=bytes(p.__data__[o:o+n])
    for i in md.disasm(b,rva):
        print(f'0x{i.address:x}: {i.bytes.hex():<20} {i.mnemonic:<10} {i.op_str}')
print('=== caller dump_6f360 @0xf5977 ===')
dis(0xf5977,0x400)
