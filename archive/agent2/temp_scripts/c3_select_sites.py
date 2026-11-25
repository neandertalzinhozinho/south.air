import json
from pathlib import Path
p = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\c3_deviations.json')
rs = json.loads(p.read_text())
sel = [r for r in rs if 0x460650 <= int(r['site_rva'], 16) <= 0x460700 and r['status'] == 'fixable']
sel.sort(key=lambda r: int(r['site_rva'], 16))
print('count', len(sel))
for r in sel:
    print(r['site_rva'], r['dump_site'], 'cur', r['cur_disp'], 'fix', r['fix_disp32'],
          'auth', r['authentic_rva'])
