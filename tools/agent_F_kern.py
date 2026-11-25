#!/usr/bin/env python3
"""Dump pointer values and count arithmetic mnemonics in a function body."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = re_lib.data()
BASE = 0x199B0000
md = Cs(CS_ARCH_X86, CS_MODE_64)

for t in (0x21C6F08, 0x21C6F30, 0x21C6F58, 0x21C6F80):
    v = re_lib.u64(t)
    print("ptr @0x%X = 0x%X -> RVA 0x%X" % (t, v, v - BASE if v > BASE else v))

for rva, size in ((0x4BC0, 0x1E0), (0x1C8880, 0x30), (0x240C00, 0x600),
                  (0x2F60, 0x30), (0x5BC0, 0x140), (0x6160, 0x1C0),
                  (0x7B40, 0x30), (0xCCE0, 0x30), (0x20E0, 0x30)):
    c = Counter()
    for ins in md.disasm(d[rva:rva + size], rva):
        c[ins.mnemonic] += 1
    print("0x%X: %s" % (rva, dict(c)))
