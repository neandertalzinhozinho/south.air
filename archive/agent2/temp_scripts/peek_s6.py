import json
from pathlib import Path

P = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\dsp\deps_exercised_r3.json')
d = json.loads(P.read_text(encoding='utf-8'))
print('scope:', d['scope'])
print('gate_passed:', d['gate_passed'])
print('counts:', d['exercitadas_contagem'], d['bloqueadas_harness_contagem'])
print('\n-- routinas (primeira) --')
print(json.dumps(d['routines'][0], indent=1)[:900])
print('\n-- campos de cada routina --')
print(sorted({k for r in d['routines'] for k in r}))
print('\n-- diagnostico_lacunas_alcancabilidade --')
print(json.dumps(d['diagnostico_lacunas_alcancabilidade'], indent=1)[:1500])
print('\n-- configurations_used --')
for c in d['configurations_used']:
    print('  ', json.dumps(c)[:160])
