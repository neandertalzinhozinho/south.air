"""Fecho de chamadas dentro do cluster DSP (0x860000..0x8D2000) a partir de RVAs dados.
Funções fora do cluster viram folhas (listadas). Só leitura do dump.
Uso: py tools/cluster_closure.py 0x864410 [...]"""
import struct, collections, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
d = open(r'dumpsooth/nyx_soothe3_dump.bin', 'rb').read()
pe = struct.unpack_from('<I', d, 0x3c)[0]
exc, sz = struct.unpack_from('<II', d, pe + 24 + 112 + 24)
fe = {}
for i in range(sz // 12):
    b, e, u = struct.unpack_from('<III', d, exc + 12 * i)
    fe[b] = e
GIANT = {0x8B3ED0: 20209, 0x8C5C40: 20209}
LO, HI = 0x860000, 0x8D2000
md = Cs(CS_ARCH_X86, CS_MODE_64)
def end_of(f):
    if f in GIANT: return f + GIANT[f]
    return fe.get(f, f + 0x200)
def closure(roots):
    seen, leaves, todo, mn = {}, collections.Counter(), list(roots), collections.Counter()
    while todo:
        f = todo.pop()
        if f in seen: continue
        if not (LO <= f < HI): leaves[f] += 1; continue
        e = end_of(f); n = 0
        for x in md.disasm(d[f:e], f):
            n += 1; mn[x.mnemonic] += 1
            if x.mnemonic in ('call', 'jmp'):
                try:
                    t = int(x.op_str, 16)
                    if x.mnemonic == 'call' or not (f <= t < e): todo.append(t)
                except ValueError:
                    leaves[f'ind@{x.address:X}'] += 1
        seen[f] = n
    return seen, leaves, mn
if __name__ == '__main__':
    roots = [int(a, 16) for a in sys.argv[1:]]
    seen, leaves, mn = closure(roots)
    print('funcs', len(seen), 'instr', sum(seen.values()), 'mnem', len(mn))
    print('folhas', sorted(k if isinstance(k, str) else hex(k) for k in leaves))
    print('mnem', sorted(mn))
