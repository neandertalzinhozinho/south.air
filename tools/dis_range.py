import struct, sys

sys.path.insert(0, r"D:\PROJETOS\soultree\tools")
d = open(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin", "rb").read()
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
fs = int(sys.argv[1], 16)
hi = int(sys.argv[2], 16)
out = sys.argv[3]


def val(t):
    try:
        return struct.unpack_from("<f", d, t)[0]
    except Exception:
        return None


lines = []
for ins in md.disasm(d[fs:hi], fs):
    extra = ""
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            t = ins.address + ins.size + op.mem.disp
            f = val(t)
            extra += f"  ; [0x{t:X}]" + (f" f32={f!r}" if f is not None else "")
    lines.append(f"{ins.address:08X}  {ins.mnemonic:<10} {ins.op_str}{extra}")

open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(len(lines), "linhas ->", out)
