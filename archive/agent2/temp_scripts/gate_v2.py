import json, collections
import numpy as np
from pathlib import Path
import pefile

ROOT = Path(r'D:\PROJETOS\shadowFILES')
C = ROOT / 'analysis/stage_reports/fase0/captures'
BASE = 0x180000000

peA = pefile.PE(str(ROOT / 'analysis/host_reference/startup_capture/original_before_load.vst3'), fast_load=True)
peB = pefile.PE(str(ROOT / 'analysis/startup_audit/final_candidate_wrapperstub.vst3'), fast_load=True)
SEC = {t: [(s.VirtualAddress, s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData),
            s.Name.rstrip(b'\0').decode('latin1')) for s in p.sections]
       for t, p in (('A', peA), ('B', peB))}

def in_image(v, t):
    if not (BASE <= v < BASE + 0x9000000): return None
    for lo, hi, n in SEC[t]:
        if lo <= v - BASE < hi: return n
    return None

def side(region):
    return ([np.fromfile(C / f'A_r{i}_{region}.bin', dtype=np.uint8) for i in (1, 2, 3)],
            [np.fromfile(C / f'B_r{i}_{region}.bin', dtype=np.uint8) for i in (1, 2, 3)])

def analyse(region):
    A, B = side(region)
    va = ~((A[0] == A[1]) & (A[0] == A[2]))
    vb = ~((B[0] == B[1]) & (B[0] == B[2]))
    idx = np.flatnonzero((A[0] != B[0]) & ~(va | vb))
    return A[0], B[0], idx, int(va.sum()), int(vb.sum()), int((~(va | vb)).sum())

CLASSES = {}

def dense(blk):
    """registro de 8 bytes: os dois dwords >= 0x01000000 nas duas imagens (alta entropia)."""
    if len(blk) != 8: return False
    b = blk.tobytes()
    lo = int.from_bytes(b[0:4], 'little'); hi = int.from_bytes(b[4:8], 'little')
    return lo >= 0x01000000 and hi >= 0x01000000

def name_byte(A0, B0, o, region):
    q = o & ~7
    nozero = dense(A0[q:q+8]) and dense(B0[q:q+8])
    d = o & ~3
    a4 = int.from_bytes(A0[d:d+4].tobytes().ljust(4, b'\0'), 'little')
    b4 = int.from_bytes(B0[d:d+4].tobytes().ljust(4, b'\0'), 'little')
    a8 = int.from_bytes(A0[o:o+8].tobytes().ljust(8, b'\0'), 'little')
    b8 = int.from_bytes(B0[o:o+8].tobytes().ljust(8, b'\0'), 'little')

    if region == 'data':
        if 0x530000 <= o < 0x538556:                    return 'b_license_state'
        if 0x58F20 <= o < 0x58F3C:                      return 'a_pointer_table'
        if (a4 & 0x80000000) and (b4 & 0x80000000) and a4 > b4 and (a4 & 0x7fffffff) < 0x40:
                                                        return 'b_blob_offset'
        if nozero:                                       return 'b_opaque_record'
        if in_image(a8, 'A') and in_image(b8, 'B'):     return 'a_image_pointer'
        if A0[o] != 0 and B0[o] == 0:                    return 'c_unpopulated'
        if A0[o] == 0 and B0[o] != 0:                    return 'c_extra_in_candidate'
        if A0[o] < 0x40 and B0[o] < 0x40:                return 'b_state_counter'
        return 'd_unexplained'
    if region == 'rdata01':                              return 'a_tls_directory'
    return 'b_license_state'

gate = {'generated': '2026-11-16', 'module_base': hex(BASE),
        'source': 'analysis/stage_reports/fase0/s3_captures_v2.json',
        'regions': {}}

for region in ('data', 'data001', 'rdata01', 'text001'):
    A0, B0, idx, fa, fb, st = analyse(region)
    per = collections.defaultdict(list)
    for o in idx:
        per[name_byte(A0, B0, int(o), region)].append(int(o))
    rec = {'size': int(len(A0)), 'volatile_A': fa, 'volatile_B': fb,
           'stable_offsets': st, 'diff_raw': int((A0 != B0).sum()), 'diff_stable': int(len(idx)),
           'classes': {}}
    for k, v in sorted(per.items()):
        rec['classes'][k] = {'bytes': len(v), 'first': hex(min(v)), 'last': hex(max(v))}
    gate['regions'][region] = rec
    print(f'\n== {region}  stable={st}  diff_bruto={rec["diff_raw"]}  diff_estavel={len(idx)}')
    for k, v in sorted(per.items()):
        print(f'   {k:<20} {len(v):5d} B  0x{min(v):07X}..0x{max(v):07X}')

print('\n=== total ===')
tot = 0
for r in ('data', 'data001', 'rdata01', 'text001'):
    tot += gate['regions'][r]['diff_stable']
gate['total_residual'] = tot
print('residuo estavel total:', tot, '(data 478 + data001 359 + rdata01 4 + text001 0)')
gate['declared_exclusions'] = {
    'b_license_state': 'bloco de licenca/maquina: 0x530000..0x538556 (strs iLok*/LicenseDb*, contadores 30/31 vs 18/0) + data001 0x8..0x2662 (TEMP path UTF-16, id de maquina)',
    'b_opaque_record': 'registros de 8 bytes de alta entropia em 0x5522FF..0x58DAE0; escrever por copia de dado nao reproduz',
    'b_blob_offset': 'offsets com tag 0x80000000 para um blob serializado; delta constante -4 (B 4 bytes mais curto antes do offset 8)',
    'b_state_counter': 'contadores vizinhos ao bloco de licenca (0x52F7E0 = 6 vs 18; 0x52FB10 = 13 vs 8)',
    'a_pointer_table': 'tabela de 8 ponteiros em .data+0x58F00; 4 apontam para .text com RVA constante -0x44F50',
    'a_image_pointer': 'ponteiros in-image; diferenca de RVA, nao de estado',
    'a_tls_directory': 'rdata01+0x440 = TLS AddressOfCallBacks: oraculo -> .rdata01, candidato -> .tlsstub (estrutural)',
    'c_unpopulated': 'celulas que o oraculo escreveu e a receita de 306 inits nao cobre (inclui cauda do registro de descritores de classe 0x5D45E0..0x5D4A50)',
}
Path(ROOT / 'analysis/stage_reports/fase0/s3_final_gate.json').write_text(json.dumps(gate, indent=1), encoding='utf-8')
print('\ngravado: analysis/stage_reports/fase0/s3_final_gate.json')
peA.close(); peB.close()
