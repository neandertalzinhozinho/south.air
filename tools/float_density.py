import sys, csv, collections
sys.path.insert(0, r'tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64)

rows = list(csv.DictReader(open(r'docs/engine/functions.csv', encoding='utf-8')))
FOPS = set()
for base in ('add', 'sub', 'mul', 'div', 'min', 'max', 'sqrt', 'cmp'):
    for suf in ('ss', 'ps', 'sd', 'pd'):
        FOPS.add(base + suf)
        FOPS.add('v' + base + suf)
for extra in ('fmadd132ss', 'fmadd213ss', 'fmadd231ss', 'fmsub132ss', 'fmsub213ss',
              'fmsub231ss', 'fnmadd132ss', 'fnmadd213ss', 'fnmadd231ss',
              'fmadd132ps', 'fmadd213ps', 'fmadd231ps', 'fmsub132ps', 'fmsub213ps',
              'fmsub231ps', 'vfmadd132ps', 'vfmadd213ps', 'vfmadd231ps',
              'vfmadd132ss', 'vfmadd213ss', 'vfmadd231ss'):
    FOPS.add(extra)

res = []
for r in rows:
    a = int(r['rva'], 16)
    sz = int(r['size'])
    if sz < 48 or sz > 40000:
        continue
    if not (0x1000 <= a < 0x1CD5487):
        continue
    n = 0
    tot = 0
    for ins in md.disasm(d[a:a + sz], a):
        tot += 1
        if ins.mnemonic in FOPS:
            n += 1
    if n >= 8:
        res.append((n, n * 1000 // max(tot, 1), a, sz, tot))

res.sort(reverse=True)
print('%-6s %-5s %-10s %-7s %s' % ('fops', 'per1k', 'rva', 'size', 'insns'))
for n, dens, a, sz, tot in res[:70]:
    print('%-6d %-5d 0x%-8X %-7d %d' % (n, dens, a, sz, tot))
