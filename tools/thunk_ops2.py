"""Precise float-op classification of the IPP vector thunks.

Uses .pdata (chain-aware, same logic as show_func.py) so each function is
disassembled exactly within its own bounds - no bleed into neighbours.
"""
import bisect
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
PDATA_RVA = 0x2758000
PDATA_MAX = 0x5223000

FLOAT = {"mulss", "addss", "subss", "divss", "maxss", "minss", "sqrtss", "rcpss",
         "mulps", "addps", "subps", "divps", "maxps", "minps", "sqrtps", "rcpps",
         "andps", "andnps", "orps", "xorps", "shufps", "cmpps", "cmpss",
         "fmadd132ss", "fmadd213ss", "fmadd231ss",
         "fmadd132ps", "fmadd213ps", "fmadd231ps",
         "fmsub132ss", "fmsub213ss", "fmsub231ss",
         "fmsub132ps", "fmsub213ps", "fmsub231ps",
         "fnmadd132ss", "fnmadd213ss", "fnmadd231ss",
         "fnmadd132ps", "fnmadd213ps", "fnmadd231ps"}

ENTRIES = {}
for i in range(0, PDATA_MAX, 12):
    b, e, u = struct.unpack_from("<III", d, PDATA_RVA + i)
    if b == 0 and e == 0:
        break
    if e > b:
        ENTRIES[b] = (e, u)
STARTS = sorted(ENTRIES)


def extent(start):
    e, u = ENTRIES[start]
    total, cur = e - start, e
    while cur in ENTRIES:
        e2, u2 = ENTRIES[cur]
        if (d[u2] >> 3) != 4:
            break
        total += e2 - cur
        cur = e2
    return cur, total


def owner(rva):
    i = bisect.bisect_right(STARTS, rva) - 1
    return STARTS[i] if i >= 0 else rva


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
    return u32(g), u64(tab + u32(g) * 8) - BASE


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
    start = owner(ent)
    end, size = extent(start)
    ins = list(md.disasm(d[start:end], start))
    c = Counter(i.mnemonic for i in ins if is_float(i.mnemonic))
    c.pop("xorps", None)
    c.pop("vxorps", None)
    c.pop("andps", None)
    c.pop("vandps", None)
    c.pop("shufps", None)
    c.pop("vshufps", None)
    sample = {}
    for i in ins:
        if is_float(i.mnemonic) and i.mnemonic not in sample:
            sample[i.mnemonic] = "0x%X %s %s" % (i.address, i.mnemonic, i.op_str)
    out.append("0x%04X -> entry 0x%X  fn 0x%X..0x%X (%d B)  insns=%d"
               % (t, ent, start, end, size, len(ins)))
    if not c:
        out.append("        (no arithmetic float op)")
    for m, n in c.most_common():
        out.append("        %-10s x%-3d  %s" % (m, n, sample[m]))
    out.append("")

text = "\n".join(out)
(ROOT / "checks" / "thunk_ops.txt").write_text(text, encoding="utf-8")
print(text)
