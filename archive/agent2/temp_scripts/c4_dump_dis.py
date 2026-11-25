"""Desmonta o dump original logo apos os 12 je (0x277f56..0x277fdf)."""
import struct
from capstone import *
from pathlib import Path
DUMP = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin')
OFF = 0x277f40
SIZE = 0x180
b = DUMP.read_bytes()[OFF:OFF+SIZE]
print('bytes:', b.hex(' '))
md = Cs(CS_ARCH_X86, CS_MODE_64)
for ins in md.disasm(b, OFF):
    print('0x%x: %-28s %s' % (ins.address, ins.bytes.hex(' '), ins.mnemonic+' '+ins.op_str))
