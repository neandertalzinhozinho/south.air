import json, collections
from pathlib import Path
A = Path(r'D:\PROJETOS\shadowFILES\analysis\startup_audit')
d = json.loads((A / 'import_slot_ownership.json').read_text(encoding='utf-8'))
print('top keys:', list(d)[:20])
for k, v in d.items():
    if isinstance(v, list):
        print(f'{k}: list[{len(v)}] first={repr(v[0])[:200] if v else None}')
    elif isinstance(v, dict):
        print(f'{k}: dict[{len(v)}] keys={list(v)[:8]}')
    else:
        print(f'{k} = {repr(v)[:200]}')
