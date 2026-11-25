import sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

p = sys.argv[1]
targets = [int(x, 16) for x in sys.argv[2:]]
pe = pefile.PE(p, fast_load=True)
data = open(p, 'rb').read()

secs = [(s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         s.Name.rstrip(b'\0').decode()) for s in pe.sections]
tv, tvs, traw, trs, _ = next(s for s in secs if s[4] == '.text')
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

text = data[traw:traw + trs]
found = {}
for ins in md.disasm(text, tv):
    if ins.mnemonic != 'lea' or len(ins.operands) != 2:
        continue
    mem = ins.operands[1]
    if mem.type != 3:
        continue
    if 'rip' not in ins.op_str:
        continue
    addr = ins.address + ins.size + mem.mem.disp
    for t in targets:
        if addr == t:
            found.setdefault(t, []).append(ins.address)

for t in targets:
    print(f"{t:#x}: {[hex(x) for x in found.get(t, [])]}")
