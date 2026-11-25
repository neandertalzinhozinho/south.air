import json
from pathlib import Path
A = Path(r'D:\PROJETOS\shadowFILES\analysis')

def show(name, maxlen=1400):
    p = A / name
    if not p.exists():
        print(f'\n### {name}: MISSING'); return
    b = p.read_bytes()
    print(f'\n### {name} ({len(b)} B)')
    try:
        d = json.loads(b.decode('utf-8'))
    except Exception as e:
        print('  not json:', e); print(b[:400].decode('utf-8', 'replace')); return
    if isinstance(d, dict):
        for k, v in d.items():
            s = repr(v)
            print(f'  {k}: {s[:maxlen]}')
    else:
        print(f'  list[{len(d)}]')
        print('  ', repr(d[:3])[:maxlen])

for n in ('stage_reports/S5.json', 'submit/S5.json', 'startup_audit/s5_enumerated_params.json',
          'parameter_table.json', 'startup_audit/s5_controller_rootcause.json'):
    show(n)
