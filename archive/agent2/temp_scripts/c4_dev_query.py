import json
from pathlib import Path
p = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\c3_deviations.json')
rs = json.loads(p.read_text())
print('total', len(rs), 'keys', list(rs[0].keys()))
sel = [r for r in rs if 0x460600 <= int(r['site_rva'],16) <= 0x460800]
sel.sort(key=lambda r: int(r['site_rva'],16))
print('in window', len(sel))
for r in sel:
    print(r['site_rva'], r.get('dump_site'), 'cur',r.get('cur_disp'),
          'fix',r.get('fix_disp32'),'auth',r.get('authentic_rva'),
          'status',r.get('status'),'stub?',r.get('cur_target_rva'))
