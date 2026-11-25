import json
w = json.load(open(r'D:\PROJETOS\shadowFILES\analysis\startup_audit\init_order_plus_tables.json', encoding='utf-8'))
u = json.load(open(r'D:\PROJETOS\shadowFILES\analysis\startup_audit\uni46c_build_plan.json', encoding='utf-8'))

def rvas(seq):
    out = []
    for e in seq:
        v = e['rva'] if isinstance(e, dict) else e
        out.append(int(v, 16) if isinstance(v, str) else int(v))
    return out

wr = rvas(w)
ur = rvas(u['full_order_rvas'])
print('wrapperstub', len(wr), 'uni46c', len(ur))
sw, su = set(wr), set(ur)
print('only in wrapperstub:', [hex(x) for x in sorted(sw - su)])
print('only in uni46c:', len(su - sw), [hex(x) for x in sorted(su - sw)][:40])
# order comparison for common prefix
n = 0
for a, b in zip(wr, ur):
    if a != b:
        break
    n += 1
print('common prefix', n)
print('wr[%d:%d]' % (n, n + 8), [hex(x) for x in wr[n:n + 8]])
print('ur[%d:%d]' % (n, n + 8), [hex(x) for x in ur[n:n + 8]])
