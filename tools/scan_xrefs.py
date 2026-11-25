#!/usr/bin/env python3
"""Scan every .pdata function and record direct calls and RIP-relative data refs.

Writes docs/engine/xrefs.csv with columns:
  func, insn, kind (call|rip), target, target_section, target_text
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import re_lib

OUT = Path(r"D:\PROJETOS\soultree\docs\engine\xrefs.csv")
SECTIONS = [
    (".text", 0x1000, 0x1CD6487),
    ("IPPCODE", 0x1CD7000, 0x1CD7000 + 0xB4B7D),
    (".rdata", 0x1D8C000, 0x1D8C000 + 0x3F2D38),
    (".data", 0x217F000, 0x217F000 + 0x5D8DD8),
    (".pdata", 0x2758000, 0x2758000 + 0x5223000),
    ("loader", 0x79CD000, 0x79CD000 + 0x125A),
]


def sec_of(t: int) -> str:
    for name, lo, hi in SECTIONS:
        if lo <= t < hi:
            return name
    return "?"


def main() -> None:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP

    d = re_lib.data()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    funcs = re_lib.funcs()
    for idx, (b, e, _u) in enumerate(funcs):
        for ins in md.disasm(d[b:e], b):
            if ins.mnemonic in ("call", "jmp") and ins.operands:
                op = ins.operands[0]
                if op.type == 2 and op.imm:
                    t = op.imm & 0xFFFFFFFFFFFFFFFF
                    if 0x1000 <= t < 0x1D8BB7D:
                        rows.append((b, ins.address, "call", t, sec_of(t), ""))
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                    txt = ""
                    if sec_of(t) in (".rdata", ".data") and re_lib.printable_at(t):
                        txt = re_lib.cstr(t, 80)
                    rows.append((b, ins.address, "rip", t, sec_of(t), txt))
        if idx % 5000 == 0:
            print(f"  {idx}/{len(funcs)} functions, {len(rows)} rows", flush=True)

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["func", "insn", "kind", "target", "target_section", "target_text"])
        for r in rows:
            w.writerow([f"0x{r[0]:X}", f"0x{r[1]:X}", r[2], f"0x{r[3]:X}", r[4], r[5]])
    print(f"wrote {OUT} with {len(rows)} rows")


if __name__ == "__main__":
    main()
