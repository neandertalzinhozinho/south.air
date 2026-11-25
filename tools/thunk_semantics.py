"""Resolve the IPP-style dispatch thunks used by the DSP core and describe the
implementation that index 4 actually selects.

Writes checks/thunk_semantics.txt and prints a short summary.
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
    return idx, tab, ent, (ent - BASE if BASE <= ent < BASE + 0x8300000 else None)


# thunks actually called by the core / cluster / 0x879CF0
THUNKS = [0x1010, 0x1040, 0x1070, 0x10A0, 0x10D0, 0x1100, 0x1160, 0x1190,
          0x11C0, 0x11F0, 0x1220, 0x1250, 0x1280, 0x12B0, 0x12E0, 0x1310,
          0x1340, 0x1370, 0x13A0, 0x1580, 0x15B0]

FLOAT = {"mulss", "addss", "subss", "divss", "maxss", "minss", "sqrtss",
         "mulps", "addps", "subps", "divps", "rcpps", "rsqrtss",
         "vfmadd132ss", "vfmadd213ss", "vfmadd231ss",
         "vfmadd132ps", "vfmadd213ps", "vfmadd231ps",
         "vfmsub132ss", "vfmsub213ss", "vfmsub231ss",
         "vfmsub132ps", "vfmsub213ps", "vfmsub231ps",
         "vrcpps", "vrsqrtss"}

out = []
for t in THUNKS:
    r = resolve(t)
    if r is None:
        out.append("thunk 0x%X  <no parse>" % t)
        continue
    idx, tab, ent, rva = r
    out.append("thunk 0x%-5X idx=%d tab=0x%X entry=0x%X rva=%s"
               % (t, idx, tab, ent, ("0x%X" % rva) if rva is not None else "external"))
    if rva is None:
        continue
    # walk up to 0x400 bytes or until a ret
    ins = []
    for i in md.disasm(d[rva:rva + 0x400], rva):
        ins.append(i)
        if i.mnemonic == "ret":
            break
    c = Counter(i.mnemonic for i in ins if i.mnemonic in FLOAT)
    out.append("    insns=%d  float=%s" % (len(ins), dict(c) if c else "{}"))
    for i in ins[:10]:
        out.append("      %08X  %-9s %s" % (i.address, i.mnemonic, i.op_str))
    out.append("")

(ROOT / "checks" / "thunk_semantics.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out[:40]))
print("...")
print("full ->", ROOT / "checks" / "thunk_semantics.txt")
