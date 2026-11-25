"""Summarize a function: direct calls and float constants (RIP-relative).

Usage: py tools/func_summary.py
Edit FUNCS below or pass start:size pairs on the command line.
"""
import sys, struct
sys.path.insert(0, 'tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_OP_IMM

d = re_lib.data()
B = 0x199B0000

FUNCS = [
    ('0x8774A0', 0x8774A0, 135),
    ('0x881050', 0x881050, 969),
    ('0x889BB0', 0x889BB0, 4720),
    ('0x899940', 0x899940, 2388),
    ('0x8ACC40', 0x8ACC40, 1605),
    ('0x8AD2B0', 0x8AD2B0, 5013),
    ('0x8B3ED0', 0x8B3ED0, 20209),
    ('0x8615D0', 0x8615D0, 1326),
    ('0x6CE80', 0x6CE80, 425),
    ('0x9BA0', 0x9BA0, 407),
    ('0x7D9550', 0x7D9550, 288),
]

if len(sys.argv) > 1:
    FUNCS = []
    for a in sys.argv[1:]:
        s, sz = a.split(':')
        FUNCS.append((s, int(s, 16), int(sz, 16)))

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

for name, start, size in FUNCS:
    code = d[start:start + size]
    calls = {}
    floats = {}
    for ins in md.disasm(code, start):
        if ins.mnemonic == 'call':
            op = ins.operands[0]
            tgt = None
            if op.type == X86_OP_IMM:
                tgt = op.imm
            elif op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                tgt = ins.address + ins.size + op.mem.disp
            if tgt is not None:
                f = re_lib.func_at(tgt)
                fs = f[0] if f else tgt
                calls.setdefault(fs, 0)
                calls[fs] += 1
        # float constants loaded via RIP
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                addr = ins.address + ins.size + op.mem.disp
                if 0 <= addr and addr + 4 <= len(d):
                    v = struct.unpack_from('<f', d, addr)[0]
                    if v == v and abs(v) < 1e9 and v != 0.0:
                        floats.setdefault(round(v, 9), 0)
                        floats[round(v, 9)] += 1
    print('=== %s  size %d ===' % (name, size))
    print('  calls:')
    for t, n in sorted(calls.items(), key=lambda kv: -kv[1]):
        f = re_lib.func_at(t)
        sz = (f[1] - f[0]) if f else 0
        print('    0x%-9X x%-4d size %-6d' % (t, n, sz))
    print('  float consts (RIP):')
    for v, n in sorted(floats.items(), key=lambda kv: -kv[1])[:24]:
        print('    %-16.9g x%d' % (v, n))
    print()
