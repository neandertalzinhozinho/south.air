"""Reachability-based float-op classification of the IPP vector thunks.

Starts at the dispatch entry, walks the CFG (fallthrough + direct jumps,
stopping at ret / indirect jumps) and reports the float operations that are
actually reachable. This avoids both .pdata fragment gaps and neighbour bleed.
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
        "jl", "jle", "jp", "jnp", "js", "jns", "jo", "jno", "jecxz",
        "jrcxz"}


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
    return u32(g), u64(tab + u32(g) * 8) - BASE


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
                    tgt = ins.operands[0]
                    if tgt.type == X86_OP_IMM:
                        todo.append(tgt.imm)
                    break
                if mn in COND:
                    tgt = ins.operands[0]
                    if tgt.type == X86_OP_IMM:
                        todo.append(tgt.imm)
                    pc += ins.size
                    continue
                break
            if mn == "call":
                pc += ins.size
                continue
            pc += ins.size
    return order


def is_float(mn):
    return mn in FLOAT or (mn.startswith("v") and mn[1:] in FLOAT)


THUNKS = [0x1010, 0x1040, 0x1070, 0x10A0, 0x10D0, 0x1100, 0x1160, 0x1190,
          0x11C0, 0x11F0, 0x1220, 0x1250, 0x1280, 0x12B0, 0x12E0, 0x1310,
          0x1340, 0x1370, 0x13A0, 0x1580, 0x15B0]

out = []
for t in THUNKS:
    r = resolve(t)
    if r is None:
        out.append("0x%04X  <unparsed>" % t)
        continue
    idx, ent = r
    ins = walk(ent, ent - 0x40, ent + 0x800)
    c = Counter(i.mnemonic for i in ins if is_float(i.mnemonic) and i.mnemonic not in SKIP)
    sample = {}
    for i in ins:
        if is_float(i.mnemonic) and i.mnemonic not in SKIP and i.mnemonic not in sample:
            sample[i.mnemonic] = "0x%X %s %s" % (i.address, i.mnemonic, i.op_str)
    out.append("0x%04X -> entry 0x%X  reachable=%d insns" % (t, ent, len(ins)))
    if not c:
        out.append("        (no arithmetic float op reachable)")
    for m, n in c.most_common():
        out.append("        %-10s x%-3d  %s" % (m, n, sample[m]))
    out.append("")

text = "\n".join(out)
(ROOT / "checks" / "thunk_ops.txt").write_text(text, encoding="utf-8")
print(text)
