import json
from pathlib import Path
p = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase1\s4_lifecycle_wrapperstub.json')
d = json.loads(p.read_text(encoding='utf-8'))
print('contract:', d['contract'], '| plugin:', Path(d['plugin']).name)
print('inits:', d['init_routines'], '| module:', d['module'])
print('classes:', d['class_count'], [c['name'] for c in (d['classes_tested'] or [])])
print('init_errors_in_capture:', d['init_errors_in_capture'])
print('\n%-15s %-32s %-8s %s' % ('MODE', 'EXIT x3', 'DET', 'LAST STAGE'))
for m, e in d['teardown_experiments'].items():
    print('%-15s %-32s %-8s %s' % (m, ','.join(e['exit_codes']), e['deterministic'], e['reached_last_stage']))
print('\nEVIDENCE:', json.dumps(d['evidence'], indent=2)[:1800])
print('\nVERDICT:', json.dumps(d['verdict'], indent=2)[:2000])
