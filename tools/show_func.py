#!/usr/bin/env python3
"""Show one function (chain-aware) with RIP-relative constants resolved.

Usage:  py tools/show_func.py 0x8C3C20 [--bytes N] [--calls]

Resolves, for every RIP-relative operand:
  * float32 / float64 / int32 / int64 value at the target
  * printable string
  * call targets mapped through checks/thunk_map.txt when present
"""
import argparse
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

ROOT = Path(__file__).resolve().parent.parent
PDATA_RVA = 0x2758000
PDATA_MAX = 0x5223000


def chain_extent(d, start):
    """Return (end, size) following UNW_FLAG_CHAININFO fragments."""
    entries = {}
    for i in range(0, PDATA_MAX, 12):
        b, e, u = struct.unpack_from("<III", d, PDATA_RVA + i)
        if b == 0 and e == 0:
            break
        if e > b:
            entries[b] = (e, u)
    if start not in entries:
        return None, 0
    e, u = entries[start]
    total, cur = e - start, e
    while cur in entries:
        e2, u2 = entries[cur]
        if (d[u2] >> 3) != 4:
            break
        total += e2 - cur
        cur = e2
    return cur, total


def thunk_names():
    out = {}
    p = ROOT / "checks" / "thunk_map.txt"
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        for i, tok in enumerate(parts):
            if tok.lower().startswith("0x") and i + 1 < len(parts):
                try:
                    out[int(tok, 16)] = parts[i + 1]
                except ValueError:
                    pass
                break
    return out


def scalar_at(d, t):
    """Best-effort decode of 8 bytes at t."""
    if t + 8 > len(d):
        return None
    raw = d[t:t + 8]
    f32 = struct.unpack_from("<f", raw, 0)[0]
    f64 = struct.unpack_from("<d", raw, 0)[0]
    i32 = struct.unpack_from("<i", raw, 0)[0]
    i64 = struct.unpack_from("<q", raw, 0)[0]
    bits = []
    if f32 == f32 and abs(f32) > 1e-30 and abs(f32) < 1e30:
        bits.append("f32=%.9g" % f32)
    if f64 == f64 and abs(f64) > 1e-30 and abs(f64) < 1e30:
        bits.append("f64=%.17g" % f64)
    if -1000000 < i32 < 1000000:
        bits.append("i32=%d" % i32)
    if abs(i64) < 100000000:
        bits.append("i64=%d" % i64)
    # printable?
    end = d.find(b"\0", t, t + 48)
    if end > t:
        chunk = d[t:end]
        if len(chunk) >= 2 and all(32 <= c < 127 for c in chunk):
            bits.append('"%s"' % chunk.decode("ascii"))
    return " ".join(bits) if bits else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rva", type=lambda s: int(s, 0))
    ap.add_argument("--bytes", type=lambda s: int(s, 0), default=None)
    ap.add_argument("--calls", action="store_true", help="only call instructions")
    args = ap.parse_args()

    d = re_lib.data()
    end, size = chain_extent(d, args.rva)
    if end is None:
        # fall back to next .pdata entry
        nxt = min([b for b in (struct.unpack_from("<I", d, PDATA_RVA + i * 12)[0]
                               for i in range(PDATA_MAX // 12)) if b > args.rva] or [args.rva + 0x400])
        end, size = nxt, nxt - args.rva
        print("# 0x%X is not a .pdata start; using next start 0x%X" % (args.rva, end))
    if args.bytes:
        end = args.rva + args.bytes
        size = args.bytes
    print("# function 0x%X..0x%X  size=%d" % (args.rva, end, size))

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    names = thunk_names()
    for ins in md.disasm(d[args.rva:end], args.rva):
        if args.calls and ins.mnemonic != "call":
            continue
        note = ""
        if ins.mnemonic == "call" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            t = ins.operands[0].imm
            if t in names:
                note = "   ; %s" % names[t]
            elif t in (0x1C84A0, 0x1C84D0, 0x1C8500, 0x1C8530):
                note = "   ; ipp-dispatch"
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                ann = re_lib.annotate_target(t)
                val = scalar_at(d, t)
                note = "   ; %s%s" % (ann, (" | " + val) if val else "")
        print("%08X  %-8s %s%s" % (ins.address, ins.mnemonic, ins.op_str, note))


if __name__ == "__main__":
    main()
