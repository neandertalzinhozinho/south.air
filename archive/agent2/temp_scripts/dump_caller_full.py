import capstone
from pathlib import Path
DUMP=Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
with DUMP.open('rb') as f:
    f.seek(0x6f360); b=f.read(0x2d0)
for i in md.disasm(b,0x6f360):
    mark=''
    if i.mnemonic in ('call','jmp') or (i.mnemonic=='mov' and 'r12' in i.op_str and '3' in i.op_str):
        mark='  <<<'
    print(f'0x{i.address:x}: {i.bytes.hex():<20} {i.mnemonic:<8} {i.op_str}{mark}')
