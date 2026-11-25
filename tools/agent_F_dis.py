#!/usr/bin/env python3
"""Print instruction stream of a range, filtered to interesting mnemonics."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

KEEP = None

for arg in sys.argv[1:]:
    rva_s, size_s = arg.split(":")
    rva, size = int(rva_s, 0), int(size_s, 0)
    print("=== 0x%X (%d bytes) ===" % (rva, size))
    for ins in md.disasm(d[rva:rva + size], rva):
        note = ""
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                note = "  ; -> 0x%X" % t
        print("%08X  %-14s %s%s" % (ins.address, ins.mnemonic, ins.op_str, note))
