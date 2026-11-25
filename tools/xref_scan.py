"""Static direct-call xref scanner over .text of the flat dump.

Finds `call rel32` (E8), `call [rip+disp32]` (FF 15), and `jmp rel32` (E9)
whose target equals one of the requested RVAs.

Usage: py tools/xref_scan.py <hex-target> [<hex-target> ...]
"""
import sys
sys.path.insert(0, 'tools')
import re_lib

TEXT_RVA = 0x1000
TEXT_SIZE = 0x1CD5487

targets = set(int(a, 16) for a in sys.argv[1:])
if not targets:
    print('usage: py tools/xref_scan.py <hex-target> [...]')
    sys.exit(1)

d = re_lib.data()
text = d[TEXT_RVA:TEXT_RVA + TEXT_SIZE]
hits = {t: [] for t in targets}

i = 0
n = len(text)
while True:
    i = text.find(b'\xe8', i)
    if i < 0 or i + 5 > n:
        break
    disp = int.from_bytes(text[i + 1:i + 5], 'little', signed=True)
    tgt = TEXT_RVA + i + 5 + disp
    if tgt in targets:
        hits[tgt].append(('call', TEXT_RVA + i))
    i += 1

i = 0
while True:
    i = text.find(b'\xe9', i)
    if i < 0 or i + 5 > n:
        break
    disp = int.from_bytes(text[i + 1:i + 5], 'little', signed=True)
    tgt = TEXT_RVA + i + 5 + disp
    if tgt in targets:
        hits[tgt].append(('jmp', TEXT_RVA + i))
    i += 1

i = 0
while True:
    i = text.find(b'\xff\x15', i)
    if i < 0 or i + 6 > n:
        break
    disp = int.from_bytes(text[i + 2:i + 6], 'little', signed=True)
    tgt = TEXT_RVA + i + 6 + disp
    if tgt in targets:
        hits[tgt].append(('callm', TEXT_RVA + i))
    i += 1

for t in sorted(targets):
    lst = hits[t]
    print('target 0x%X : %d refs' % (t, len(lst)))
    seen = set()
    for kind, at in lst:
        f = re_lib.func_at(at)
        fs = ('func 0x%X size %d' % (f[0], f[1] - f[0])) if f else 'NOFUNC'
        key = (kind, f[0] if f else at)
        if key in seen:
            continue
        seen.add(key)
        print('   %-6s 0x%-9X  %s' % (kind, at, fs))
