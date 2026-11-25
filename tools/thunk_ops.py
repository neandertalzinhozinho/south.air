"""Classify the vector thunks by the float instructions they actually execute.

For each thunk RVA: resolve the IPP dispatch (index 4), disassemble the entry
region linearly, and report every distinct float mnemonic with a sample
instruction. No name-based guessing: the operation comes from the opcode.
"""
import struct
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = re_lib.data()
BASE = 0x199B0000
md = Cs(CS_ARCH_X86, CS_MODE_64)
ROOT = Path(__file__).resolve().parent.parent

FLOAT = {
    "mulss", "addss", "subss", "divss", "maxss", "minss", "sqrtss", "rcpss",
    "mulps", "addps", "subps", "divps", "maxps", "minps", "sqrtps", "rcpps",
    "andps", "andnps", "orps", "xorps", "blendps", "shufps", "cmpps", "cmpss",
    "vfmadd132ss", "vfmadd213ss", "vfmadd231ss",
    "vfmadd132ps", "vfmadd213ps", "vfmadd231ps",
    "vfmsub132ss", "vfmsub213ss", "vfmsub231ss",
    "vfmsub132ps", "vfmsub213ps", "vfmsub231ps",
    "vfnmadd132ss", "vfnmadd213ss", "vfnmadd231ss",
    "vfnmadd132ps", "vfnmadd213ps", "vfnmadd231ps",
}


def is_float(mn):
    return mn in FLOAT or (mn.startswith("v") and mn[1:] in FLOAT)


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
    idx = u32(g)
    ent = u64(tab + idx * 8)
    return idx, ent - BASE


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
    ins = list(md.disasm(d[ent:ent + 0x600], ent))
    c = Counter(i.mnemonic for i in ins if is_float(i.mnemonic))
    sample = {}
    for i in ins:
        if is_float(i.mnemonic) and i.mnemonic not in sample:
            sample[i.mnemonic] = "0x%X %s %s" % (i.address, i.mnemonic, i.op_str)
    out.append("0x%04X -> 0x%X   idx=%d  insns=%d" % (t, ent, idx, len(ins)))
    if not c:
        out.append("        no float op in first 0x600 bytes")
    for m, n in c.most_common():
        out.append("        %-10s x%-3d  %s" % (m, n, sample[m]))
    out.append("")

text = "\n".join(out)
(ROOT / "checks" / "thunk_ops.txt").write_text(text, encoding="utf-8")
print(text)
