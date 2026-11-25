import json
from pathlib import Path

R = Path(r'D:\PROJETOS\shadowFILES\analysis\startup_audit')

def peek(name, depth=2, maxk=40):
    p = R / name
    d = json.loads(p.read_text(encoding='utf-8'))
    print(f'\n########## {name}  ({p.stat().st_size} B)')
    def walk(o, pre='', lvl=0):
        if lvl > depth: return
        if isinstance(o, dict):
            for i, (k, v) in enumerate(o.items()):
                if i >= maxk:
                    print(f'{pre}  ... ({len(o)-maxk} chaves)'); break
                if isinstance(v, (dict, list)):
                    n = len(v)
                    print(f'{pre}{k}: <{type(v).__name__} {n}>')
                    if isinstance(v, dict): walk(v, pre + '  ', lvl + 1)
                    elif v and not isinstance(v[0], (dict, list)):
                        print(f'{pre}   {v[:8]}')
                    elif v: walk(v[0], pre + '   ', lvl + 1)
                else:
                    print(f'{pre}{k} = {repr(v)[:110]}')
    walk(d)

for n in ('s4_lifecycle_audit.json', 's5_controller_dependency.json',
          'import_slot_ownership.json', 's5_enumerated_params.json'):
    try: peek(n)
    except Exception as e: print(f'\n{n}: ERRO {e}')
