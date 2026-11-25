#!/usr/bin/env python3
"""Recover the static descriptor vectors built in 0x85E6C0 (README: PLANO §23.3).

Each `call 0x563e40` is a std::vector<Descriptor> constructor from an
initializer_list of 24-byte elements. The initializer list is built on the stack
of 0x85E6C0; the vector object lives in .data (0x2754xxx).

Frame mapping in 0x85E6C0: rsp = rbp - 0x110.
"""
import re
from pathlib import Path

DIS = Path(r"D:\PROJETOS\soultree\checks\85e6c0.dis")
RSP_FROM_RBP = 0x100


def rsp_off(op):
    m = re.search(r"\[(rsp|rbp)\s*([+-]\s*(?:0x)?[0-9a-fA-F]+)?\]", op)
    if not m:
        return None
    base = m.group(1)
    disp = int(m.group(2).replace(" ", ""), 16) if m.group(2) else 0
    return disp + (RSP_FROM_RBP if base == "rbp" else 0)


def main():
    raw = DIS.read_bytes()
    enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
    ins = []
    for line in raw.decode(enc, errors="replace").splitlines():
        if not line or line.startswith("#"):
            continue
        m = re.match(r"([0-9A-F]{8})\s+(\S+)\s+(.*)$", line)
        if m:
            ins.append((m.group(1), m.group(2), m.group(3)))

    for i, (a, mn, op) in enumerate(ins):
        if mn != "call" or not op.startswith("0x563e40"):
            continue
        vec = begin = end = None
        stores = []
        # region start = the mutex lock call that precedes the lazy construction
        start = 0
        for j in range(i - 1, max(0, i - 400), -1):
            if ins[j][1] == "call" and ins[j][2].startswith("0x17969e0"):
                start = j
                break
        for a2, m2, o2 in ins[start + 1:i]:
            if m2 == "lea" and o2.startswith("rcx") and "0x2754" in o2 and vec is None:
                vec = o2.split(";")[-1].strip()
            if m2 == "lea" and o2.startswith("rax,") and (
                    "[rsp" in o2 or "[rbp" in o2) and begin is None:
                begin = rsp_off(o2)
            if begin is not None and m2 == "lea" and o2.startswith("rdx,") and (
                    "[rsp" in o2 or "[rbp" in o2) and end is None:
                end = rsp_off(o2)
            if begin is not None and m2 == "mov" and " ptr [" in o2 and (
                    "dword" in o2 or "qword" in o2):
                mo = re.search(r"ptr \[[^\]]+\],\s*(-?0x[0-9a-fA-F]+|-?\d+)$", o2)
                off = rsp_off(o2)
                val = int(mo.group(1), 16) if mo else None
                stores.append((a2, off, val))

        print("CALL %s  vec=%s  begin=%s  end=%s" % (a, vec, begin, end))
        if begin is not None and end is not None:
            n = (end - begin) // 0x18
            print("   span 0x%X..0x%X = %d bytes, %d descriptors of 24 B"
                  % (begin, end, end - begin, (end - begin) // 0x18))
            elems = {}
            for a2, off, val in stores:
                if off is None or not (begin <= off < end):
                    continue
                rel = off - begin
                elems.setdefault(rel // 0x18, {})[rel % 0x18] = val
            for k in sorted(elems):
                d = elems[k]
                print("   desc[%d]  +0=%s  +8=%s  +0x10=%s   (%s)" % (
                    k, d.get(0), d.get(8), d.get(0x10),
                    ", ".join("%02X" % o for o in sorted(d))))


main()
