#!/usr/bin/env python3
"""Find candidate writers of the 24-byte band descriptor.

Signature sought (Stage C): a store of the discriminant `2` at descriptor+0x10,
where the descriptor pointer advances by 0x18. Prints every `mov dword ptr
[reg+0x10], 2` with the surrounding 6 instructions, filtered to functions that
also mention 0x18 near the site.

Read-only: scans the dump bytes, never touches a process.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

d = re_lib.data()

# unique function starts from .pdata (chain-aware fragments deduped by address)
starts = {}
for b, e, u in re_lib.funcs():
    starts.setdefault(b, e)

seen = set()
hits = []
for b, e in sorted(starts.items()):
    if not (0x1000 <= b < 0x1CD6487):
        continue
    insns = list(md.disasm(d[b:e], b))
    for i, ins in enumerate(insns):
        if ins.address in seen:
            continue
        seen.add(ins.address)
        if ins.mnemonic != "mov" or len(ins.operands) != 2:
            continue
        dst, src = ins.operands
        if dst.type != CS_OP_MEM or src.type != CS_OP_IMM:
            continue
        if dst.mem.disp != 0x10:
            continue
        if src.imm != 2:
            continue
        # look for 0x18 stride nearby
        lo = max(0, i - 40)
        hi = min(len(insns), i + 40)
        near = [x for x in insns[lo:hi] if "0x18" in x.op_str or "0x18" in x.mnemonic]
        hits.append((b, ins, near[:4]))

print(f"total mov [reg+0x10], 2 sites: {len(hits)}")
for b, ins, near in hits:
    print(f"\n=== func 0x{b:X} site 0x{ins.address:X}: {ins.mnemonic} {ins.op_str}")
    for x in near:
        print(f"    0x{x.address:X} {x.mnemonic} {x.op_str}")
