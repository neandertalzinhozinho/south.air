#!/usr/bin/env python3
"""Linear-sweep text disassembler that resyncs after undecodable bytes.

Usage: py -3 tools/lsweep.py <lo> <hi> <regex-on-opstr> [limit]
"""
import re
import sys

sys.path.insert(0, r'tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64


def sweep(lo, hi, pattern, limit=200):
    d = re_lib.data()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    rx = re.compile(pattern)
    out = []
    pos = lo
    while pos < hi:
        chunk = d[pos:pos + 0x1000]
        got = False
        for ins in md.disasm(chunk, pos):
            got = True
            if rx.search(ins.op_str) or rx.search(ins.mnemonic + ' ' + ins.op_str):
                out.append((ins.address, ins.mnemonic, ins.op_str))
                if len(out) >= limit:
                    return out
            pos = ins.address + ins.size
        if not got:
            pos += 1
    return out


if __name__ == '__main__':
    lo = int(sys.argv[1], 0)
    hi = int(sys.argv[2], 0)
    pat = sys.argv[3]
    lim = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    for a, m, o in sweep(lo, hi, pat, lim):
        print('%08X  %-9s %s' % (a, m, o))
