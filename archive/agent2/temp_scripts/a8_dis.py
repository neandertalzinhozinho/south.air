import sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

DUMP = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin')
data = DUMP.read_bytes()
BASE = 0x18CC0000
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

def dis(rva, count=80, maxbytes=0x800):
    print(f'===== dump RVA {rva:#x} (VA {BASE+rva:#x}) =====')
    raw = data[rva:rva+maxbytes]
    for i in md.disasm(raw, BASE + rva):
        print(f'{i.address - BASE:08x}  {i.bytes.hex():<20} {i.mnemonic} {i.op_str}')
        count -= 1
        if count <= 0:
            break

for a in sys.argv[1:]:
    rva = int(a, 0)
    dis(rva)
