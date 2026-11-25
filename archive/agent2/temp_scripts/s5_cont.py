import json
from pathlib import Path

F1 = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase1')
c = [json.loads(l) for l in open(F1 / 's5_params_wrapperstub.jsonl', encoding='utf-8') if l.startswith('{')]
c = [e for e in c if e['event'] == 'parameter']
for p in c:
    if p['stepCount'] == 0:
        print(f"{p['index']:3d} {p['title']:20s} {[s['text'] for s in p['string_samples']]}")
