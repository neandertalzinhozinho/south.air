import json, collections
from pathlib import Path
rs = json.loads(Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\c3_deviations.json').read_text())
print('opcodes', collections.Counter(r['opcode'] for r in rs))
print('status', collections.Counter(r['status'] for r in rs))
print('\nUNMAPPED (logo adiante dos 12):')
for r in sorted([x for x in rs if x['status']=='unmapped'], key=lambda x:int(x['site_rva'],16))[:40]:
    print(' ', r)
print('\nall fixable near 0x460000-0x464000:')
for r in sorted([x for x in rs if x['status']=='fixable' and 0x460000<=int(x['site_rva'],16)<0x464000], key=lambda x:int(x['site_rva'],16)):
    print(' ', r['site_rva'], r['dump_site'], r['opcode'], r['dump_target'], r['authentic_rva'])
