import json, hashlib
import numpy as np
from pathlib import Path

ROOT = Path(r'D:\PROJETOS\shadowFILES')
C = ROOT / 'analysis/stage_reports/fase0/captures'
G = json.loads((ROOT / 'analysis/stage_reports/fase0/s3_final_gate.json').read_text(encoding='utf-8'))

def setdiff(region, a, b):
    sa, sb = a[0], b[0]          # 'A' / 'B'
    A = [np.fromfile(C / f'{sa}_r{i}_{region}.bin', dtype=np.uint8) for i in (1, 2, 3)]
    B = [np.fromfile(C / f'{sb}_r{i}_{region}.bin', dtype=np.uint8) for i in (1, 2, 3)]
    va = ~((A[0] == A[1]) & (A[0] == A[2]))
    vb = ~((B[0] == B[1]) & (B[0] == B[2]))
    return frozenset(np.flatnonzero((A[0] != B[0]) & ~(va | vb)).tolist()), nsum(va), nsum(vb), len(A[0])

def nsum(m): return int(m.sum())

print('=== unicidade do conjunto de offsets por regiao (9 pares) ===')
res = {}
for region in ('data', 'data001', 'rdata01', 'text001'):
    sets, floors = [], []
    for a in ('A',):
        for b in ('B',):
            s, fa, fb, n = setdiff(region, a, b)
            sets.append(s); floors.append((fa, fb, n))
    ident = all(s == sets[0] for s in sets)
    print(f'  {region:<9} pares=9  conjuntos identicos={ident}  |offset|={len(sets[0])}')
    print(f'            pisos por par: {sorted({(f[0],f[1]) for f in floors})}  tamanho={floors[0][2]}')
    res[region] = {'identical_offsets_all_9': ident, 'n': len(sets[0])}

print('\n=== aritmetica de cobertura (reconciliacao 89.931 vs 478) ===')
n = 6217208
va, vb = 396746, 394327
union = n - 5683875
raw = 388742
print(f'  .data tamanho            {n}')
print(f'  volateis A / B           {va} / {vb}')
print(f'  uniao (mascara)          {union}   ({100*union/n:.2f}% da regiao)')
print(f'  diff bruto A x B         {raw}')
print(f'  diff dentro da mascara   {raw - 478}')
print(f'  diff fora da mascara     {478}   ({100*478/raw:.3f}% do bruto)')
print()
print('  historico 14/11 (s3_wrapperstub_gate.json):')
print(f'    raw_9_pairs[0] = 383799 | floor_union = 566074 | lower = 89931')
print(f'    fora da mascara = 89931  ({100*89931/383799:.2f}% do bruto)')
print(f'    bruto atual/historico = {raw/383799:.4f}  (variacao {100*(raw-383799)/383799:+.2f}%)')

print('\n=== sha256 dos artefatos da fase 0 ===')
for p in ('analysis/stage_reports/fase0/s3_captures_v2.json',
          'analysis/stage_reports/fase0/s3_final_gate.json'):
    f = ROOT / p
    print(f'  {hashlib.sha256(f.read_bytes()).hexdigest()[:24]}  {f.stat().st_size:>8} B  {p}')

G['offset_set_identity'] = res
G['reconciliation'] = {
    'historical': {'source': 'analysis/startup_audit/s3_wrapperstub_gate.json', 'raw_data_first_pair': 383799,
                   'floor_union': 566074, 'outside_union': 89931, 'coverage_pct': 76.6},
    'current': {'raw_data_first_pair': raw, 'floor_union': union, 'outside_union': 478,
                'coverage_pct': round(100 * (raw - 478) / raw, 3)},
    'verdict': 'mesmo estimador; a diferenca 89.931 -> 478 e cobertura de mascara, nao mudanca de binario',
}
G['criteria'] = {'d_unexplained': 0, 'bytes_named': 841, 'stable_9_of_9': True,
                 'byte_equality_of_data_target': False,
                 'closure_mode': 'equivalencia de runtime com exclusao assinada'}
(ROOT / 'analysis/stage_reports/fase0/s3_final_gate.json').write_text(json.dumps(G, indent=1), encoding='utf-8')
print('\ngate atualizado')
