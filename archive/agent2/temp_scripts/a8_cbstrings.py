from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

data=Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
BASE=0x18CC0000
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True

for i in md.disasm(data[0x8637d0:0x8639c4], BASE+0x8637d0):
    if i.mnemonic in ('lea','call') and 'rip' in i.op_str:
        # compute target for lea
        if i.mnemonic=='lea':
            import re
            m=re.search(r'\[rip ([-+]) (0x[0-9a-f]+)\]',i.op_str)
            if m:
                d=int(m.group(2),16)*(-1 if m.group(1)=='-' else 1)
                t=i.address+i.size+d-BASE
                s=data[t:t+80].split(b'\x00')[0]
                print(f'{i.address-BASE:#x}: lea -> dump {t:#x}  str={s[:60]!r}')
    if i.mnemonic=='call' and i.op_str.startswith('qword ptr [r15'):
        print(f'{i.address-BASE:#x}: {i.mnemonic} {i.op_str}   bytes={i.bytes.hex()}')
