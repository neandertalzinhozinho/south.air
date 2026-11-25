import json
from pathlib import Path
t = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
for i in range(1, 4):
    d = json.loads((t / f'c3_patch12_report_{i}.json').read_text())
    bad = [p for p in d['patches'] if p['after'].replace(' ', '') != p['expected']]
    print('run', i, 'phase', d['phase'], 'patches', len(d['patches']), 'bad', len(bad))
    print(' ', [(p['je_rva'], p['after'], p['authentic_rva']) for p in d['patches']])
