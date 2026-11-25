import capstone
from pathlib import Path
D=Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
with D.open('rb') as f:
    for rva,n,label in ((0x715c00,0x40,'dump_715c0 prologue'),(0x6f3b0,0x60,'path A setup'),(0x6f4ae,0x30,'path B setup'),(0x6f5e0,0x10,'magic-3 write')):
        f.seek(rva); b=f.read(n)
        print('===',label,'@0x%x ==='%rva)
        for i in md.disasm(b,rva):
            print(f'  0x{i.address:x}: {i.bytes.hex():<18} {i.mnemonic} {i.op_str}')
