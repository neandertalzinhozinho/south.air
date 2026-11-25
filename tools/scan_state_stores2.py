#!/usr/bin/env python3
"""State stores, filtered: no index register, report per function with all sites.

Also looks for functions that load a pointer from [x+0x2c38] and then store into
that same register at a small displacement (<=0x200).
"""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP

H1 = {0x54: "state+0x00", 0x58: "state+0x04", 0x7C: "state+0x28",
      0x90: "state+0x3c", 0xA0: "state+0x4c", 0xA6: "state+0x52"}
H2 = {0x00: "state+0x00", 0x04: "state+0x04", 0x28: "state+0x28",
      0x3C: "state+0x3c", 0x4C: "state+0x4c", 0x52: "state+0x52"}

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
d = re_lib.data()
lo, hi = 0x1000, 0x1CD6487

STOREPFX = ("mov", "vmov", "add", "sub", "and", "or", "xor", "mul", "div",
            "inc", "dec", "shl", "shr", "sar", "neg", "not", "pxor", "por",
            "pand", "vp", "cvt", "max", "min")


def is_store(ins):
    if not ins.operands:
        return False
    if ins.operands[0].type != X86_OP_MEM:
        return False
    m = ins.mnemonic
    if m in ("cmp", "test", "lea", "call", "jmp", "jmpq", "push", "pop"):
        return False
    # pure loads with memory destination are stores in ATT sense; capstone uses intel -> mem dest = store
    return True


hits = defaultdict(list)
state_flow = defaultdict(list)

for ins in md.disasm(d[lo:hi], lo):
    if not is_store(ins):
        continue
    op0 = ins.operands[0]
    base = op0.mem.base
    if base in (0, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP):
        continue
    if op0.mem.index != 0:
        continue
    disp = op0.mem.disp
    f = re_lib.func_at(ins.address)
    fn = f[0] if f else 0
    if disp in H1:
        hits[(fn, "H1")].append((ins.address, ins.mnemonic, ins.op_str, H1[disp]))
    if disp in H2:
        state_flow[fn].append((ins.address, ins.mnemonic, ins.op_str))

print("=== H1 non-indexed stores, grouped by function (any count) ===")
for (fn, _), sites in sorted(hits.items(), key=lambda kv: (-len(kv[1]), kv[0][0])):
    if len(sites) >= 1:
        print("\nfunction 0x%X (%d sites)" % (fn, len(sites)))
        for a, m, o, tag in sites:
            print("  %08X  %-8s %-42s ; %s" % (a, m, o, tag))

print("\n=== H2 non-indexed stores to 0x00/0x04/0x28/0x3c/0x4c/0x52, functions with >=2 ===")
for fn, sites in sorted(state_flow.items(), key=lambda kv: -len(kv[1])):
    if len(sites) >= 2:
        print("\nfunction 0x%X (%d sites)" % (fn, len(sites)))
        for a, m, o in sites:
            print("  %08X  %-8s %s" % (a, m, o))
