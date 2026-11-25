#!/usr/bin/env python3
"""Extract (index, name) from the parameter registration sequence in 0x8634A0.

Registration pattern (proved by disassembly):
    lea r8,[rip+X]      ; name string
    mov/lea edx, idx    ; parameter index
    mov rcx, r15
    call qword ptr [r15+0x18]
"""
import re
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "checks" / "8634a0.dis"
raw = p.read_bytes()
if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
    txt = raw.decode("utf-16", errors="replace")
else:
    txt = raw.decode("utf-8", errors="replace")
lines = txt.splitlines()

R13 = 1
pending = None
idx = None
r13 = R13
out = []

for line in lines:
    m = re.match(r"^([0-9A-F]{8})\s+(\S+)\s+(.*)$", line)
    if not m:
        continue
    a, mn, ops = m.group(1), m.group(2), m.group(3)

    # index assignments
    if mn == "xor" and ops.replace(" ", "") == "edx,edx":
        idx = 0
        continue
    mm = re.match(r"edx, \[r13 \+ (0x[0-9A-Fa-f]+|\d+)\]", ops)
    if mm:
        idx = int(mm.group(1), 0) + r13
        continue
    if re.match(r"edx, r13d$", ops):
        idx = r13
        continue
    mm = re.match(r"edx, (0x[0-9A-Fa-f]+|\d+)$", ops)
    if mm:
        idx = int(mm.group(1), 0)
        continue

    if mn == "lea" and ops.startswith("r8, [rip"):
        names = re.findall(r'"([^"]*)"', line)
        pending = names[0] if names else None
        continue

    if mn == "call" and "r15 + 0x18" in ops:
        if pending and idx is not None:
            out.append((idx, pending, a))
        pending = None

for i, nm, a in sorted(out):
    print("%4d  0x%s  %s" % (i, a, nm))
print("total", len(out))
