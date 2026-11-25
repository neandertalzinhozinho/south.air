#!/usr/bin/env python3
"""Per-function store scan in the DSP cluster (no linear sweep desync).

For every .pdata function starting in [lo,hi):
  disassemble function extent (chain-aware) and record stores whose memory operand
  has a non-stack base, no index, and disp in the state field set.
"""
import struct
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP

PDATA_RVA = 0x2758000
PDATA_MAX = 0x5223000

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

entries = {}
order = []
for i in range(0, PDATA_MAX, 12):
    b, e, u = struct.unpack_from("<III", d, PDATA_RVA + i)
    if b == 0 and e == 0:
        break
    if e > b:
        entries[b] = (e, u)
        order.append(b)
order.sort()


def extent(start):
    e, u = entries[start]
    total, cur = e - start, e
    while cur in entries:
        e2, u2 = entries[cur]
        if (d[u2] >> 3) != 4:
            break
        total += e2 - cur
        cur = e2
    return start, start + total


H1 = {0x54: "eng+0x54=state+0x00", 0x58: "eng+0x58=state+0x04",
      0x7C: "eng+0x7c=state+0x28", 0x90: "eng+0x90=state+0x3c",
      0xA0: "eng+0xa0=state+0x4c", 0xA6: "eng+0xa6=state+0x52"}
H2 = {0x00: "state+0x00", 0x04: "state+0x04", 0x28: "state+0x28",
      0x3C: "state+0x3c", 0x4C: "state+0x4c", 0x52: "state+0x52"}

lo, hi = 0x860000, 0x8F0000
res1 = defaultdict(list)
res2 = defaultdict(list)

for b in order:
    if not (lo <= b < hi):
        continue
    s, e = extent(b)
    if e - s > 0x20000:
        continue
    for ins in md.disasm(d[s:e], s):
        if not ins.operands:
            continue
        op0 = ins.operands[0]
        if op0.type != X86_OP_MEM:
            continue
        if op0.mem.base in (0, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP):
            continue
        if op0.mem.index != 0:
            continue
        if ins.mnemonic in ("cmp", "test", "lea", "push", "pop", "call", "jmp"):
            continue
        disp = op0.mem.disp
        if disp in H1:
            res1[b].append((ins.address, ins.mnemonic, ins.op_str, H1[disp]))
        if disp in H2:
            res2[b].append((ins.address, ins.mnemonic, ins.op_str, H2[disp]))

print("=== H1 (engine base) ===")
for b, sites in sorted(res1.items()):
    print("\nfunction 0x%X (%d)" % (b, len(sites)))
    for a, m, o, t in sites:
        print("  %08X  %-8s %-40s ; %s" % (a, m, o, t))

print("\n=== H2 (state base), functions with >=2 sites ===")
for b, sites in sorted(res2.items()):
    if len(sites) < 2:
        continue
    print("\nfunction 0x%X (%d)" % (b, len(sites)))
    for a, m, o, t in sites:
        print("  %08X  %-8s %-40s ; %s" % (a, m, o, t))
