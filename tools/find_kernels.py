"""Rank functions by scalar-float arithmetic density.

Evidence-grade filter: finds the DSP kernels instead of reading wrappers.
For every .pdata function it disassembles the body and counts
  - fp mul/add/sub/div (scalar + packed)
  - FMA
  - RIP-relative loads of 4-byte values that decode to plausible float constants
  - call count
Score favours arithmetic and penalises call-heavy buffer plumbing.

Usage: py -3 tools/find_kernels.py [max_size] [top_n]
"""
import csv, struct, sys, math
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP

DUMP = r'D:\PROJETOS\soultree\dumpsooth\soothe3_unpacked.dll'
FUNCS = r'D:\PROJETOS\soultree\docs\engine\functions.csv'
MAX_SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 40

data = open(DUMP, 'rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

FP_MUL = {'mulsd', 'mulss', 'mulsd', 'vmulsd', 'vmulss', 'mulps', 'mulpd', 'vmulps', 'vmulpd'}
FP_ADD = {'addsd', 'addss', 'vaddsd', 'vaddss', 'addps', 'addpd', 'vaddps', 'vaddpd'}
FP_SUB = {'subsd', 'subss', 'vsubsd', 'vsubss', 'subps', 'subpd', 'vsubps', 'vsubpd'}
FP_DIV = {'divsd', 'divss', 'vdivsd', 'vdivss', 'divps', 'divpd'}
FMA = {'vfmadd132ss', 'vfmadd213ss', 'vfmadd231ss', 'vfmadd132sd', 'vfmadd213sd',
       'vfmadd231sd', 'vfmadd132ps', 'vfmadd213ps', 'vfmadd231ps',
       'vfmsub132ss', 'vfmsub213ss', 'vfmsub231ss'}
CONST = {'movss', 'movsd', 'vmovss', 'vmovsd'}


def plausible_float(b):
    v = struct.unpack('<f', b)[0]
    if v != v or math.isinf(v):
        return False
    a = abs(v)
    return a == 0.0 or 1e-8 <= a <= 1e8


rows = []
with open(FUNCS, newline='', encoding='utf-8') as f:
    for r in csv.reader(f):
        if not r or not r[0].startswith('0x'):
            continue
        try:
            rva = int(r[0], 16)
            size = int(r[2])
        except (ValueError, IndexError):
            continue
        if size <= 8 or size > MAX_SIZE:
            continue
        if rva + size > len(data):
            continue
        body = data[rva:rva + size]
        nmul = nadd = nsub = ndiv = nfma = nconst = ncall = nloadfloat = 0
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
            elif m in ('call', 'jmp') and not m == 'jmp':
                ncall += 1
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    tgt = (ins.address + ins.size + op.mem.disp) & 0xFFFFFFFFFFFFFFFF
                    if 0 < tgt < len(data) - 4:
                        nloadfloat += 1
                        if m in CONST and plausible_float(data[tgt:tgt + 4]):
                            nconst += 1
        arith = nmul + nadd + nsub + ndiv + 2 * nfma
        if arith == 0:
            continue
        # penalise call-heavy plumbing, reward constants and fma
        score = arith * 3 + nconst * 6 + nfma * 4 - ncall * 2 + nloadfloat
        rows.append((score, rva, size, nmul, nadd, nsub, ndiv, nfma, nconst, nloadfloat, ncall))

rows.sort(reverse=True)
print('candidates:', len(rows))
print('%-10s %-6s %5s %5s %5s %5s %5s %6s %6s %5s  %s' %
      ('rva', 'size', 'mul', 'add', 'sub', 'div', 'fma', 'fconst', 'ripf', 'call', 'score'))
for s, rva, size, a, b, c, d, fm, fc, rl, cl in rows[:TOP]:
    print('0x%08X %-6d %5d %5d %5d %5d %5d %6d %6d %5d  %d' %
          (rva, size, a, b, c, d, fm, fc, rl, cl, s))
