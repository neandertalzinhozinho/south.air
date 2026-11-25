import json
from pathlib import Path

d = json.loads(Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\dsp\deps_exercised_r3.json')
               .read_text(encoding='utf-8'))
for k, v in d['diagnostico_lacunas_alcancabilidade'].items():
    print(f'\n### {k}  ({len(v.get("rvas", []))} rvas)')
    print('  causa:', v.get('causa_bloqueio_harness', '')[:400])
    print('  extras:', {kk: vv for kk, vv in v.items() if kk not in ('descricao', 'rvas', 'causa_bloqueio_harness')} if len(v) > 3 else '')
print('\n=== 20 bloqueadas ===')
for r in d['routines']:
    if r['bloqueado_harness']:
        print(f"{r['rva']:>10s} size={r['size_bytes']:5d} {r['como'][:95]}")
        print(f"{'':>10s} min: {r['configuracao_minima_necessaria'][:130]}")
print('\n=== 19 exercitadas (resumo) ===')
ex = [r for r in d['routines'] if not r['bloqueado_harness']]
print('amostras total', sum(r['amostras'] for r in ex), '| erro max', max(r['erro_max'] for r in ex),
      '| external_count>0:', sum(1 for r in ex if r['external_count']))
print('byte_identical_build all:', all(r['byte_identical_build'] for r in d['routines']))
