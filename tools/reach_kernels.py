"""Rank the functions REACHABLE from the DSP core by float-arithmetic density.

Reachability comes from docs/engine/xrefs.csv (call edges) starting at the core
0x8B3ED0 and its twin 0x8C5FD8.  Arithmetic density comes from disassembly.

This is the filter that separates DSP kernels from buffer plumbing: a wrapper
allocates and copies, a kernel multiplies.

Usage: py -3 tools/reach_kernels.py [maxdepth] [top_n]
"""
import csv, struct, sys, math
from collections import defaultdict, deque
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

DUMP = r'D:\PROJETOS\soultree\dumpsooth\soothe3_unpacked.dll'
FUNCS = r'D:\PROJETOS\soultree\docs\engine\functions.csv'
XREFS = r'D:\PROJETOS\soultree\docs\engine\xrefs.csv'
ROOTS = [0x8B3ED0, 0x8C5FD8]
MAXDEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 40
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 50

edges = defaultdict(set)
with open(XREFS, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['kind'] != 'call':
            continue
        try:
            edges[int(r['func'], 16)].add(int(r['target'], 16))
        except ValueError:
            pass

seen = set()
q = deque((r, 0) for r in ROOTS)
while q:
    n, d = q.popleft()
    if n in seen:
        continue
    seen.add(n)
    if d >= MAXDEPTH:
        continue
    for m in edges.get(n, ()):
        if m not in seen:
            q.append((m, d + 1))
print('reachable functions from %s: %d' % ([hex(x) for x in ROOTS], len(seen)))

data = open(DUMP, 'rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

FP_MUL = {'mulsd', 'mulss', 'vmulsd', 'vmulss', 'mulps', 'mulpd', 'vmulps', 'vmulpd'}
FP_ADD = {'addsd', 'addss', 'vaddsd', 'vaddss', 'addps', 'addpd', 'vaddps', 'vaddpd'}
FP_SUB = {'subsd', 'subss', 'vsubsd', 'vsubss', 'subps', 'subpd', 'vsubps', 'vsubpd'}
FP_DIV = {'divsd', 'divss', 'vdivsd', 'vdivss', 'divps', 'divpd'}
FMA = {'vfmadd132ss', 'vfmadd213ss', 'vfmadd231ss', 'vfmadd132sd', 'vfmadd213sd',
       'vfmadd231sd', 'vfmadd132ps', 'vfmadd213ps', 'vfmadd231ps',
       'vfmsub132ss', 'vfmsub213ss', 'vfmsub231ss', 'vfnmadd132ss', 'vfnmadd213ss'}
CONST = {'movss', 'movsd', 'vmovss', 'vmovsd'}


def plausible(b):
    v = struct.unpack('<f', b)[0]
    if v != v or math.isinf(v):
        return False
    a = abs(v)
    return a == 0.0 or 1e-8 <= a <= 1e8


sizes = {}
with open(FUNCS, newline='', encoding='utf-8') as f:
    for r in csv.reader(f):
        if r and r[0].startswith('0x'):
            try:
                sizes[int(r[0], 16)] = int(r[2])
            except (ValueError, IndexError):
                pass

rows = []
for rva in seen:
    size = sizes.get(rva)
    if not size or size <= 8 or size > 8000 or rva + size > len(data):
        continue
    body = data[rva:rva + size]
    nmul = nadd = nsub = ndiv = nfma = nconst = ncall = nrip = 0
    for ins in md.disasm(body, rva):
        m = ins.mnemonic
        if m in FP_MUL:
            nmul += 1
        elif m in FP_ADD:
            nadd += 1
        elif m in FP_SUB:
            nsub += 1
        elif m in FP_DIV:
            ndiv += 1
        elif m in FMA:
            nfma += 1
        elif m == 'call':
            ncall += 1
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                tgt = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                if 0 < tgt < len(data) - 4:
                    nrip += 1
                    if m in CONST and plausible(data[tgt:tgt + 4]):
                        nconst += 1
    arith = nmul + nadd + nsub + ndiv + 2 * nfma
    if arith == 0:
        continue
    score = arith * 3 + nconst * 6 + nfma * 4 - ncall * 2 + nrip
    rows.append((score, rva, size, nmul, nadd, nsub, ndiv, nfma, nconst, nrip, ncall))

rows.sort(reverse=True)
print('with arithmetic: %d' % len(rows))
print('%-10s %-6s %4s %4s %4s %4s %4s %6s %5s %5s  %s' %
      ('rva', 'size', 'mul', 'add', 'sub', 'div', 'fma', 'fconst', 'ripf', 'call', 'score'))
for s, rva, size, a, b, c, d, fm, fc, rl, cl in rows[:TOP]:
    print('0x%08X %-6d %4d %4d %4d %4d %4d %6d %5d %5d  %d' %
          (rva, size, a, b, c, d, fm, fc, rl, cl, s))
