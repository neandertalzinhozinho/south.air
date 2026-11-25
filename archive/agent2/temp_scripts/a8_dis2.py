from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

data = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
BASE = 0x18CC0000
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

def show(start, end):
    print(f'===== {start:#x} .. {end:#x} =====')
    for i in md.disasm(data[start:end], BASE + start):
        print(f'{i.address-BASE:08x}  {i.bytes.hex():<22} {i.mnemonic} {i.op_str}')

show(0x86390f, 0x863d00)
