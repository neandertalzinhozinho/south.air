#!/usr/bin/env python3
"""Map case index (0..22) of 0x85E6C0 to the returned descriptor-vector address.

Jump table at 0x85FFA0 (23 x i32 absolute RVA, base 0). For each case target we
follow the fast path until the first `lea rax,[rip+...]` and read the resolved
address printed by show_func.py.
"""
import re
import struct
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib

DIS = Path(r"D:\PROJETOS\soultree\checks\85e6c0.dis")


def main():
    d = re_lib.data()
    raw = DIS.read_bytes()
    enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
    lines = raw.decode(enc, errors="replace").splitlines()
    addr2line = {}
    order = []
    for line in lines:
        m = re.match(r"([0-9A-F]{8})\s+(.*)$", line)
        if m:
            addr2line[int(m.group(1), 16)] = line
            order.append(int(m.group(1), 16))
    order.sort()

    for idx in range(0x17):
        rel = struct.unpack_from("<i", d, 0x85FFA0 + 4 * idx)[0]
        target = rel & 0xFFFFFFFF
        found = None
        for a in order:
            if a < target:
                continue
            line = addr2line[a]
            if " lea " in line and re.search(r"lea\s+rax, \[rip", line):
                mm = re.search(r";\s*(0x[0-9A-F]+)", line)
                found = mm.group(1) if mm else "?"
                break
            if " ret" in line:
                break
        print("case %2d  target=0x%X  -> %s" % (idx, target, found))


main()
