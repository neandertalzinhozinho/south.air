import json
import numpy as np
from pathlib import Path

ROOT = Path(r'D:\PROJETOS\shadowFILES')
C = ROOT / 'analysis/stage_reports/fase0/captures'
G = json.loads((ROOT / 'analysis/stage_reports/fase0/s3_final_gate.json').read_text(encoding='utf-8'))

bounds = {}
for region in ('data', 'data001', 'rdata01', 'text001'):
    A = [np.fromfile(C / f'A_r{i}_{region}.bin', dtype=np.uint8) for i in (1, 2, 3)]
    B = [np.fromfile(C / f'B_r{i}_{region}.bin', dtype=np.uint8) for i in (1, 2, 3)]
    va = ~((A[0] == A[1]) & (A[0] == A[2]))
    vb = ~((B[0] == B[1]) & (B[0] == B[2]))
    raw = (A[0] != B[0])
    lower = int((raw & ~(va | vb)).sum())
    upper = int((raw & ~va).sum())
    upper_b = int((raw & ~vb).sum())
    bounds[region] = {'lower_outside_both_floors': lower,
                      'upper_masking_only_oracle': upper,
                      'upper_masking_only_candidate': upper_b,
                      'raw': int(raw.sum())}
    G['regions'][region]['bounds'] = bounds[region]
    print(f'{region:<9} lower={lower:<6} upper(A)= {upper:<7} upper(B)= {upper_b:<7} raw={int(raw.sum())}')

# faixa de estado
G['declared_exclusions']['b_opaque_record'] = (
    '112 B em 0x5522FF..0x58DAE0: tokens de 8 bytes de alta entropia (dois dwords >= 0x01000000), '
    'com dwords repetidos aos pares nos vizinhos; mesma banda de estado que b_license_state; '
    'conteudo nao e reproduzivel por copia de dado')
G['declared_exclusions']['b_license_state'] = (
    'bloco de licenca/maquina 0x530000..0x538556: 8 strings presentes so no oraculo '
    '(iLok1/iLok2/iLok3/LicenseDb/LicenseDbRemote/IlokCloudRemote/iLok2Remote/iLok3Remote) + ImlIasm_; '
    'contadores 0x1e/0x1f vs 0x12/0; e .data001 0x8..0x2662 com o caminho TEMP em UTF-16 e id de maquina')
G['declared_exclusions']['state_band'] = (
    'todos os bytes b_* de .data caem em 0x52F7E0..0x58DAE0; .data001 0x8..0x2662; '
    'rdata01 0x440 e estrutural (TLS), nao estado')
G['declared_exclusions'].pop('a_image_pointer', None)
G['criteria']['limits_explicit'] = True
G['criteria']['lower_total'] = sum(b['lower_outside_both_floors'] for b in bounds.values())
G['criteria']['upper_total_oracle_floor'] = sum(b['upper_masking_only_oracle'] for b in bounds.values())
G['open_items'] = [
    'b_opaque_record (112 B) e nomeado por posicao e estatistica, nao por mecanismo: se S4 mostrar que '
    'o DSP depende desses tokens, a classe reabre',
    'c_unpopulated (92 B) e replayavel em principio: exige acrescentar a init que popula a cauda do '
    'registro de descritores de classe (0x5D45E0..0x5D4A50) a receita de inits',
]
(ROOT / 'analysis/stage_reports/fase0/s3_final_gate.json').write_text(json.dumps(G, indent=1), encoding='utf-8')
print('\ngate final:', (ROOT / 'analysis/stage_reports/fase0/s3_final_gate.json').stat().st_size, 'B')
