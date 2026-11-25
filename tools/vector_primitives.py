"""Build a complete table of the IPP vector primitives used by the DSP.

Scans every .pdata function start in the low .text region, tests whether it is
an IPP dispatch thunk (jump-index global + dispatch table), follows the CFG of
the selected implementation and reports the float operations it performs.
The operation is read from the opcodes, never from a name.
"""
import struct
import sys
from collections import Counter, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM

d = re_lib.data()
BASE = 0x199B0000
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
ROOT = Path(__file__).resolve().parent.parent
PDATA_RVA = 0x2758000
PDATA_MAX = 0x5223000

FLOAT = {"mulss", "addss", "subss", "divss", "maxss", "minss", "sqrtss", "rcpss",
         "mulps", "addps", "subps", "divps", "maxps", "minps", "sqrtps", "rcpps",
         "fmadd132ss", "fmadd213ss", "fmadd231ss",
         "fmadd132ps", "fmadd213ps", "fmadd231ps",
         "fmsub132ss", "fmsub213ss", "fmsub231ss",
         "fmsub132ps", "fmsub213ps", "fmsub231ps",
         "fnmadd132ss", "fnmadd213ss", "fnmadd231ss",
         "fnmadd132ps", "fnmadd213ps", "fnmadd231ps"}
SKIP = {"xorps", "vxorps", "andps", "vandps", "shufps", "vshufps",
        "orps", "vorps", "blendps", "vblendps"}
COND = {"je", "jne", "jz", "jnz", "ja", "jae", "jb", "jbe", "jg", "jge",
        "jl", "jle", "jp", "jnp", "js", "jns", "jo", "jno", "jecxz", "jrcxz"}

STARTS = []
for i in range(0, PDATA_MAX, 12):
    b, e, u = struct.unpack_from("<III", d, PDATA_RVA + i)
    if b == 0 and e == 0:
        break
    if e > b:
        STARTS.append(b)


def u32(o):
    return struct.unpack_from("<I", d, o)[0]


def u64(o):
    return struct.unpack_from("<Q", d, o)[0]


def rip_target(ins):
    if "rip" not in ins.op_str:
        return None
    tail = ins.op_str.split("[rip")[1].split("]")[0].strip()
    sign = 1
    if tail.startswith("-"):
        sign, tail = -1, tail[1:].strip()
    elif tail.startswith("+"):
        tail = tail[1:].strip()
    try:
        return ins.address + ins.size + sign * int(tail, 16)
    except ValueError:
        return None


def resolve(t):
    ins = list(md.disasm(d[t:t + 0x20], t))
    if len(ins) < 3:
        return None
    g, tab = rip_target(ins[0]), rip_target(ins[1])
    if g is None or tab is None:
        return None
    if not (0x2000000 <= g < 0x2800000):
        return None
    if not (0x2000000 <= tab < 0x2800000):
        return None
    idx = u32(g)
    if idx > 64:
        return None
    ent = u64(tab + idx * 8)
    if not (BASE <= ent < BASE + 0x8300000):
        return None
    return idx, ent - BASE


def walk(entry, lo, hi):
    seen, order, todo = set(), [], deque([entry])
    while todo:
        pc = todo.popleft()
        while lo <= pc < hi and pc not in seen:
            seen.add(pc)
            one = list(md.disasm(d[pc:pc + 16], pc))
            if not one:
                break
            ins = one[0]
            order.append(ins)
            mn = ins.mnemonic
            if mn == "ret" or mn.startswith("ret"):
                break
            if mn.startswith("j"):
                if mn == "jmp":
                    if ins.operands and ins.operands[0].type == X86_OP_IMM:
                        todo.append(ins.operands[0].imm)
                    break
                if mn in COND:
                    if ins.operands and ins.operands[0].type == X86_OP_IMM:
                        todo.append(ins.operands[0].imm)
                    pc += ins.size
                    continue
                break
            pc += ins.size
    return order


def is_float(mn):
    return mn in FLOAT or (mn.startswith("v") and mn[1:] in FLOAT)


rows = []
for start in range(0x1000, 0x30000, 4):
    r = resolve(start)
    if r is None:
        continue
    idx, ent = r
    ins = walk(ent, ent - 0x40, ent + 0x800)
    c = Counter(i.mnemonic.replace("v", "", 1) if i.mnemonic.startswith("v") else i.mnemonic
                for i in ins if is_float(i.mnemonic) and i.mnemonic not in SKIP)
    sig = "+".join("%s%d" % (m, n) for m, n in c.most_common()) or "none"
    rows.append((start, idx, ent, len(ins), sig))

rows.sort()
lines = ["# IPP vector primitives reachable from the DSP core",
         "# thunk_rva  jump_index  impl_rva  insns  float_ops",
         ""]
for start, idx, ent, n, sig in rows:
    lines.append("0x%05X  idx=%d  impl=0x%05X  insns=%-4d  %s" % (start, idx, ent, n, sig))
text = "\n".join(lines)
(ROOT / "checks" / "vector_primitives.txt").write_text(text, encoding="utf-8")
print(text)
print()
print("total primitives:", len(rows))
