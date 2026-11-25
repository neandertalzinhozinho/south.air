import json, collections
from pathlib import Path
A = Path(r'D:\PROJETOS\shadowFILES\analysis\startup_audit')
d = json.loads((A / 'import_slot_ownership.json').read_text(encoding='utf-8'))
print('total', d['total_slots'], '| owned', d['owned']['count'], '| unowned', d['unowned']['count'])
print('\nmethod_notes:')
for n in d['method_notes']:
    print(' -', n)
print('\ncross_check:', json.dumps(d['cross_check'], indent=1)[:800])
own = d['owned']['slots']
uno = d['unowned']['slots']
print('\nowned sample:', json.dumps(own[:2], indent=1)[:700])
print('\nunowned sample:', json.dumps(uno[:3], indent=1)[:700])
# distribution of unowned by value being zero
def val(s):
    for k in ('value', 'slot_value', 'content', 'qword', 'bytes'):
        if k in s: return s[k]
    return None
print('\nunowned keys union:', sorted({k for s in uno for k in s}))
zc = collections.Counter()
for s in uno:
    v = s.get('value')
    zc['zero' if (v in (0, '0x0', '0', None)) else 'nonzero'] += 1
print('unowned zero/nonzero:', zc)
