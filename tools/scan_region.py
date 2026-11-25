#!/usr/bin/env python3
"""Chain-aware arithmetic scan of one RVA window.

Different from tools/find_kernels.py: that one trusts the .pdata size in
functions.csv, which is a *fragment* for functions that are split across
UNW_FLAG_CHAININFO entries (0x8B3ED0 is 49 B in the CSV and 20.209 B real).
Here every body is expanded with show_func.chain_extent(), instructions are
de-duplicated by address (chains overlap), and only then counted.

Usage:  py tools/scan_region.py 0x8A0000 0x8E0000 [top_n]
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from show_func import chain_extent
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parent.parent
PDATA_RVA = 0x2758000
PDATA_MAX = 0x5223000

MUL = {"mulss", "vmulss", "mulps", "vmulps"}
ADD = {"addss", "vaddss", "addps", "vaddps"}
SUB = {"subss", "vsubss", "subps", "vsubps"}
DIV = {"divss", "vdivss", "divps", "vdivps"}
FMA = {"vfmadd132ss", "vfmadd213ss", "vfmadd231ss", "vfmadd132ps", "vfmadd213ps",
       "vfmadd231ps", "vfmadd132sd", "vfmadd213sd", "vfmadd231sd",
       "vfmsub132ss", "vfmsub213ss", "vfmsub231ss"}


def main():
    lo = int(sys.argv[1], 16)
    hi = int(sys.argv[2], 16)
    top = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    d = re_lib.data()
    starts = []
    for i in range(0, PDATA_MAX, 12):
        b, e, u = struct.unpack_from("<III", d, PDATA_RVA + i)
        if b == 0 and e == 0:
            break
        if lo <= b < hi and e > b:
            starts.append(b)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    seen = set()
    rows = []
    tot_fma = tot_mul = tot_add = tot_sub = tot_div = 0
    for s in starts:
        end, size = chain_extent(d, s)
        if not end:
            continue
        n = {"mul": 0, "add": 0, "sub": 0, "div": 0, "fma": 0, "call": 0}
        uniq = 0
        for ins in md.disasm(d[s:end], s):
            if ins.address in seen:
                continue
            seen.add(ins.address)
            uniq += 1
            m = ins.mnemonic
            if m in MUL:
                n["mul"] += 1
            elif m in ADD:
                n["add"] += 1
            elif m in SUB:
                n["sub"] += 1
            elif m in DIV:
                n["div"] += 1
            elif m in FMA:
                n["fma"] += 1
            elif m == "call":
                n["call"] += 1
        tot_fma += n["fma"]
        tot_mul += n["mul"]
        tot_add += n["add"]
        tot_sub += n["sub"]
        tot_div += n["div"]
        arith = n["mul"] + n["add"] + n["sub"] + n["div"] + 2 * n["fma"]
        if arith:
            rows.append((arith, s, size, uniq, n))

    print("window 0x%X-0x%X  .pdata starts: %d  unique insns: %d" %
          (lo, hi, len(starts), len(seen)))
    print("TOTAL  fma=%d  mul=%d  add=%d  sub=%d  div=%d" %
          (tot_fma, tot_mul, tot_add, tot_sub, tot_div))
    rows.sort(reverse=True)
    print("%-11s %7s %6s %5s %5s %5s %5s %5s %6s" %
          ("rva", "size", "insns", "fma", "mul", "add", "sub", "div", "call"))
    for arith, s, size, uniq, n in rows[:top]:
        print("0x%08X %7d %6d %5d %5d %5d %5d %5d %6d" %
              (s, size, uniq, n["fma"], n["mul"], n["add"], n["sub"], n["div"], n["call"]))


if __name__ == "__main__":
    main()
