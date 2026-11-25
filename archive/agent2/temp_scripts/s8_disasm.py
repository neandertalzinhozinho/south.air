import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = r"D:\PROJETOS\shadowFILES\analysis\startup_audit\final_candidate.vst3"
pe = pefile.PE(P, fast_load=True)
data = open(P, "rb").read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
base = pe.OPTIONAL_HEADER.ImageBase

for rva in (0x30D310, 0xC76730, 0x30D330):
    off = pe.get_offset_from_rva(rva)
    print(f"=== rva {rva:#x} rva->file {off:#x} va {base + rva:#x}")
    code = data[off:off + 120]
    n = 0
    for ins in md.disasm(code, base + rva):
        print(f"   {ins.address - base:#010x}  {ins.mnemonic:8s} {ins.op_str}")
        n += 1
        if n >= 22:
            break
    print()
