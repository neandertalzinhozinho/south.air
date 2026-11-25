#!/usr/bin/env python3
"""Small helpers for static analysis of the soothe3 dump (flat RVA layout)."""
import struct
from pathlib import Path

DUMP = Path(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin")
BASE = 0x199B0000  # runtime base used by absolute pointers in .data/.rdata
IMAGE_BASE = 0x180000000
PDATA_RVA = 0x2758000
PDATA_MAX = 0x5223000

_data = None


def data() -> bytes:
    global _data
    if _data is None:
        _data = DUMP.read_bytes()
    return _data


def u32(o): return struct.unpack_from("<I", data(), o)[0]
def i32(o): return struct.unpack_from("<i", data(), o)[0]
def u64(o): return struct.unpack_from("<Q", data(), o)[0]


def functions():
    """[(begin, end, unwind)] as RVAs."""
    out = []
    d = data()
    for i in range(0, PDATA_MAX, 12):
        b, e, u = struct.unpack_from("<III", d, PDATA_RVA + i)
        if b == 0 and e == 0:
            break
        if e > b:
            out.append((b, e, u))
    return out


_FUNCS = None


def funcs():
    global _FUNCS
    if _FUNCS is None:
        _FUNCS = functions()
    return _FUNCS


def func_at(rva: int):
    for b, e, u in funcs():
        if b <= rva < e:
            return b, e, u
    return None


def cstr(rva: int, maxlen: int = 200) -> str:
    d = data()
    end = d.find(b"\0", rva, rva + maxlen)
    if end < 0:
        end = rva + maxlen
    return d[rva:end].decode("latin-1", errors="replace")


def printable_at(rva: int, n: int = 24) -> bool:
    chunk = data()[rva:rva + n]
    return len(chunk) > 0 and sum(32 <= c < 127 for c in chunk) / len(chunk) > 0.85


def annotate_target(t: int) -> str:
    """Describe a RIP-relative target."""
    d = data()
    for name, lo, hi in [
        (".text", 0x1000, 0x1CD6487),
        ("IPPCODE", 0x1CD7000, 0x1CD7000 + 0xB4B7D),
        (".rdata", 0x1D8C000, 0x1D8C000 + 0x3F2D38),
        (".data", 0x217F000, 0x217F000 + 0x5D8DD8),
        (".pdata", 0x2758000, 0x2758000 + 0x5223000),
    ]:
        if lo <= t < hi:
            sec = name
            break
    else:
        return f"0x{t:X}"
    if sec in (".rdata", ".data") and printable_at(t):
        return f"0x{t:X} [{sec}] \"{cstr(t, 64)}\""
    return f"0x{t:X} [{sec}]"


def disasm_function(rva: int, max_ins: int = 4000):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP
    f = func_at(rva)
    if not f:
        print(f"0x{rva:X}: not inside a known function")
        return
    b, e, u = f
    print(f"function 0x{b:X}..0x{e:X} size={e-b} unwind=0x{u:X} (requested 0x{rva:X})")
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    n = 0
    for ins in md.disasm(data()[b:e], b):
        note = ""
        if ins.operands:
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    t = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                    note = "   ; " + annotate_target(t)
        print(f"  {ins.address:08X}: {ins.mnemonic:8s} {ins.op_str}{note}")
        n += 1
        if n >= max_ins:
            print("  ... (truncated)")
            break


def callers(target_rva: int, limit: int = 200):
    """Find direct call/jmp rel32 to target (E8/E9) in code."""
    d = data()
    out = []
    lo, hi = 0x1000, 0x1CD6487
    for i in range(lo, hi - 5):
        if d[i] in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", d, i + 1)[0]
            tgt = i + 5 + rel
            if tgt == target_rva:
                f = func_at(i)
                out.append((i, f[0] if f else None))
                if len(out) >= limit:
                    break
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        disasm_function(int(sys.argv[1], 0))
