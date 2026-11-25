import sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

p, rva = sys.argv[1], int(sys.argv[2], 16)
back = int(sys.argv[3]) if len(sys.argv) > 3 else 200
fwd = int(sys.argv[4]) if len(sys.argv) > 4 else 96

pe = pefile.PE(p, fast_load=True)
data = open(p, 'rb').read()
secs = [(s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]


def rva2off(r):
    for va, vs, raw, rs in secs:
        if va <= r < va + max(vs, rs):
            return raw + (r - va)
    return None


start = rva - back
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
chunk = data[rva2off(start):rva2off(rva) + fwd]
for ins in md.disasm(chunk, start):
    mark = '   <<<< HERE' if ins.address == rva else ''
    print(f'{ins.address:#010x}  {ins.bytes.hex():<24} {ins.mnemonic:<8} {ins.op_str}{mark}')
