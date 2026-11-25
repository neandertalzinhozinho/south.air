from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

data = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
BASE=0x18CC0000

pats = {
 'mov r9d,801': bytes.fromhex('41b901080000'),
 'mov r8d,801': bytes.fromhex('41b801080000'),
 'mov r10d,801': bytes.fromhex('41ba01080000'),
 'mov ecx,801': bytes.fromhex('b901080000'),
 'mov edx,801': bytes.fromhex('ba01080000'),
 'mov esi,801': bytes.fromhex('be01080000'),
 'mov edi,801': bytes.fromhex('bf01080000'),
 'mov r9d,808': bytes.fromhex('41b908080000'),
 'mov ecx,808': bytes.fromhex('b908080000'),
 'mov edx,808': bytes.fromhex('ba08080000'),
 'cmp ? 801 imm32': bytes.fromhex('8108010800'),
}
md=Cs(CS_ARCH_X86,CS_MODE_64)
for name,pat in pats.items():
    hits=[]; start=0
    while True:
        i=data.find(pat,start)
        if i<0: break
        hits.append(i); start=i+1
        if len(hits)>=200: break
    print(f'=== {name}: {len(hits)} hits ===')
    for h in hits[:30]:
        ins=list(md.disasm(data[max(0,h-6):h+len(pat)+6], BASE+h-6))
        txt='; '.join(f'{x.mnemonic} {x.op_str}' for x in ins)
        print(f'{h:#x}: {txt}')
