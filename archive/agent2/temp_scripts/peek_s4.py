import json
from pathlib import Path
d = json.loads(Path(r'D:\PROJETOS\shadowFILES\analysis\startup_audit\s4_surface_audit.json').read_text(encoding='utf-8'))
print('status:', d['status'])
print('\nconclusao:', d['conclusao'][:400])
print('\n--- metodo ---')
for k, v in d['metodo'].items():
    print(f'  {k} = {repr(v)[:300]}')
for sec in ('process', 'createView'):
    print(f'\n--- {sec} ---')
    for k, v in d[sec].items():
        print(f'  {k} = {repr(v)[:200]}')
print('\n--- runs ---')
for k, v in d['runs'].items():
    print(f'  {k}: {type(v).__name__} {len(v) if hasattr(v,"__len__") else ""}')
    if isinstance(v, dict):
        for kk, vv in list(v.items())[:8]:
            print(f'     {kk} = {repr(vv)[:120]}')
print('\n--- limitations ---')
for l in d['limitations']:
    print('  -', l[:220])
