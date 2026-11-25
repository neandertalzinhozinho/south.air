import sys, struct
sys.path.insert(0, r'tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

TEXT_LO, TEXT_HI = 0x1000, 0x1CD5487

targets = set()
for a in sys.argv[1:]:
    targets.add(int(a, 16))

found = {t: [] for t in targets}

# linear sweep; capstone handles most, skip data by requiring valid insn
addr = TEXT_LO
end = TEXT_HI
while addr < end:
    chunk = d[addr:addr + 0x400]
    consumed = 0
    for ins in md.disasm(chunk, addr):
        consumed += ins.size
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                tgt = ins.address + ins.size + op.mem.disp
                if tgt in found:
                    found[tgt].append((ins.address, ins.mnemonic, ins.op_str))
        # stop at ret/int3 to resync occasionally
    if consumed == 0:
        consumed = 1
    addr += consumed

for t in sorted(found):
    print('target 0x%X : %d rip-refs' % (t, len(found[t])))
    for a, m, o in found[t][:40]:
        print('   0x%X  %-8s %s' % (a, m, o))
