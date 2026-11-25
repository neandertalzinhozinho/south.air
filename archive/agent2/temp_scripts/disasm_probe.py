import capstone, struct, sys

DUMP = r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin'
BASE = 0x180000000
f = open(DUMP, 'rb')
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True

def dump(rva, size, label):
    f.seek(rva)
    data = f.read(size)
    print(f'\n===== {label}: RVA 0x{rva:x} .. 0x{rva+size:x} ({size} bytes) =====')
    for ins in md.disasm(data, BASE + rva):
        raw = ' '.join(f'{x:02x}' for x in ins.bytes)
        extra = ''
        if ins.mnemonic in ('call','jmp','je','jne','ja','jb','jbe','jae','jg','jl','jge','jle','js','jns','jo','jno','jp','jnp','jz','jnz','loop','jrcxz','jecxz'):
            # compute target
            op = ins.operands[0]
            if op.type == capstone.x86.X86_OP_IMM:
                extra = f'  ; target=0x{op.imm - BASE:x} (VA 0x{op.imm:x})'
        print(f'  0x{ins.address-BASE:06x}:  {raw:<24} {ins.mnemonic:<8} {ins.op_str}{extra}')

for rva, size, label in [
    (0x6f360, 0x300, 'caller_6f360'),
    (0x71360, 0x100, 'inner_71360'),
    (0x71400, 0x60,  'inner_71400 (entry)'),
    (0x715c0, 0x100, 'callee_715c0 (entry, AV at +0x5f=0x7161f)'),
    (0x241400, 0x80, 'interior_24140b area'),
]:
    dump(rva, size, label)
