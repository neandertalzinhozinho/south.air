#!/usr/bin/env python3
"""Extract function boundaries from the soothe3 dump's .pdata and the parameter
name table from .data.

Outputs:
  docs/engine/functions.csv  (rva, va, size, section, endbr64)
  docs/engine/params.csv     (name, rva, value_a, value_b, flags)

Run from the repository root after tools/normalize_dump.py (same file is fine).
"""
import csv
import struct
from pathlib import Path

DUMP = Path(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin")
OUT = Path(r"D:\PROJETOS\soultree\docs\engine")
IMAGE_BASE = 0x180000000
PDATA_RVA, PDATA_MAX = 0x2758000, 0x5223000
PARAM_RVA, PARAM_END, PARAM_STRIDE = 0x238E9B0, 0x2392600, 0x68

SECTIONS = [
    (".text", 0x1000, 0x1CD6487),
    ("IPPCODE", 0x1CD7000, 0x1CD7000 + 0xB4B7D),
    (".rdata", 0x1D8C000, 0x1D8C000 + 0x3F2D38),
    (".data", 0x217F000, 0x217F000 + 0x5D8DD8),
    (".pdata", 0x2758000, 0x2758000 + 0x5223000),
]


def section_of(rva: int) -> str:
    for name, lo, hi in SECTIONS:
        if lo <= rva < hi:
            return name
    return "?"


def main() -> None:
    data = DUMP.read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)

    rows = []
    for i in range(0, PDATA_MAX, 12):
        begin, end, unwind = struct.unpack_from("<III", data, PDATA_RVA + i)
        if begin == 0 and end == 0:
            break
        if end <= begin:
            continue
        endbr = data[begin:begin + 4] == b"\xf3\x0f\x1e\xfa"
        rows.append((begin, begin + IMAGE_BASE, end - begin, section_of(begin), int(endbr), unwind))

    with (OUT / "functions.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rva", "va", "size", "section", "endbr64", "unwind_rva"])
        for rva, va, size, sec, endbr, unwind in rows:
            w.writerow([f"0x{rva:X}", f"0x{va:X}", size, sec, endbr, f"0x{unwind:X}"])
    print(f"functions.csv: {len(rows)} functions")
    by_sec = {}
    for _, _, _, sec, _, _ in rows:
        by_sec[sec] = by_sec.get(sec, 0) + 1
    print("  by section:", by_sec)

    params = []
    slot = 0
    while PARAM_RVA + slot * PARAM_STRIDE + PARAM_STRIDE <= PARAM_END:
        o = PARAM_RVA + slot * PARAM_STRIDE
        raw = data[o + 0x14:o + 0x14 + 0x2C]
        name = raw.split(b"\0")[0]
        if name and all(32 <= c < 127 for c in name) and len(name) > 2:
            a = struct.unpack_from("<d", data, o + 0x40)[0]
            b = struct.unpack_from("<d", data, o + 0x48)[0]
            flags = struct.unpack_from("<Q", data, o + 0x50)[0]
            params.append((name.decode(), o, a, b, flags))
        slot += 1

    with (OUT / "params.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "rva", "value_a", "value_b", "flags"])
        for name, o, a, b, flags in params:
            w.writerow([name, f"0x{o:X}", a, b, f"0x{flags:X}"])
    print(f"params.csv: {len(params)} parameter names")
    print(f"  first: {params[0][0]}  last: {params[-1][0]}")


if __name__ == "__main__":
    main()
