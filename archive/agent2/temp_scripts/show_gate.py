import json
from pathlib import Path
g = json.loads(Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0\s3_final_gate.json').read_text(encoding='utf-8'))
print('lower total:', g['criteria']['lower_total'], '| upper total:', g['criteria']['upper_total_oracle_floor'])
print('d:', g['criteria']['d_unexplained'], '| bytes nomeados:', g['criteria']['bytes_named'])
for r, v in g['regions'].items():
    print(' %-9s res=%-5d lower=%-5d upper=%-6d classes=%s' %
          (r, v['diff_stable'], v['bounds']['lower_outside_both_floors'],
           v['bounds']['upper_masking_only_oracle'], list(v['classes'])))
print('\nopen_items:')
for i in g['open_items']:
    print('  -', i)
