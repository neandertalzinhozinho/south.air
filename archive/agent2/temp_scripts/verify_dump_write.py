import capstone
from pathlib import Path
DUMP = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
# dump has RVA == offset
with DUMP.open('rb') as f:
    f.seek(0x6f360)
    b=f.read(0x400)
ins=list(md.disasm(b,0x6f360))
print('instructions',len(ins))
for i in ins:
    if (i.mnemonic in ('mov','call','lea') and ('3' in i.op_str or 'r12' in i.op_str)) or 0x6f5d0 <= i.address <= 0x6f620:
        print(f'0x{i.address:x}: {i.bytes.hex():<18} {i.mnemonic:<8} {i.op_str}')
