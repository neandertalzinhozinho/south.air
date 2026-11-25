import json, collections
import numpy as np
from pathlib import Path
import pefile

ROOT = Path(r'D:\PROJETOS\shadowFILES')
C = ROOT / 'analysis/stage_reports/fase0/captures'
BASE = 0x180000000

peA = pefile.PE(str(ROOT / 'analysis/host_reference/startup_capture/original_before_load.vst3'), fast_load=True)
peB = pefile.PE(str(ROOT / 'analysis/startup_audit/final_candidate_wrapperstub.vst3'), fast_load=True)
def sections(pe):
    return [(s.VirtualAddress, s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData),
             s.Name.rstrip(b'\0').decode('latin1')) for s in pe.sections]
SEC_A, SEC_B = sections(peA), sections(peB)

def in_image(v, secs):
    if not (BASE <= v < BASE + 0x9000000): return None
    rva = v - BASE
    for lo, hi, n in secs:
        if lo <= rva < hi: return n
    return None

def caps(region):
    return ([np.fromfile(C / f'A_r{i}_{region}.bin', dtype=np.uint8) for i in (1,2,3)],
            [np.fromfile(C / f'B_r{i}_{region}.bin', dtype=np.uint8) for i in (1,2,3)])

def stable_idx(region):
    A, B = caps(region)
    va = ~((A[0]==A[1]) & (A[0]==A[2]))
    vb = ~((B[0]==B[1]) & (B[0]==B[2]))
    stable = ~(va|vb)
    return A[0], B[0], np.flatnonzero((A[0]!=B[0]) & stable), int(va.sum()), int(vb.sum()), int(stable.sum())

gate = {'generated': '2026-11-16', 'module_base': hex(BASE), 'regions': {}}
tot = collections.Counter()
resid = []

A0, B0, idx, fa, fb, st = stable_idx('data')
classes = {}
for o in idx:
    o = int(o); s16 = o & ~0xF
    ba = A0[s16:s16+16].tobytes(); bb = B0[s16:s16+16].tobytes()
    d = o & ~3
    a4 = int.from_bytes(A0[d:d+4].tobytes().ljust(4,b'\0'),'little')
    b4 = int.from_bytes(B0[d:d+4].tobytes().ljust(4,b'\0'),'little')
    a8 = int.from_bytes(A0[o:o+8].tobytes().ljust(8,b'\0'),'little')
    b8 = int.from_bytes(B0[o:o+8].tobytes().ljust(8,b'\0'),'little')
    sa, sb = in_image(a8, SEC_A), in_image(b8, SEC_B)
    if 0x530000 <= o < 0x538556:
        k = 'b_license_state'
    elif 0x58F20 <= o < 0x58F3C:
        k = 'a_pointer_shift'
    elif 0 not in ba and 0 not in bb and len(set(ba)) >= 12 and len(set(bb)) >= 12:
        k = 'b_opaque_blob'
    elif sa and sb:
        k = 'a_image_pointer'
    elif a4 == b4 + 4 and (a4 & 0x80000000):
        k = 'b_offset_minus4'
    elif B0[o] == 0 and A0[o] != 0:
        k = 'c_unpopulated'
    elif A0[o] == 0 and B0[o] != 0:
        k = 'c_extra_in_candidate'
    else:
        k = 'd_unexplained'
        resid.append({'region':'data','offset':hex(o),'a':A0[o:o+8].tobytes().hex(),'b':B0[o:o+8].tobytes().hex()})
    classes.setdefault(k, []).append(o)

print('=== .data 478 bytes por classe ===')
for k, v in sorted(classes.items()):
    print(f'  {k:<22} {len(v):5d} B  {sorted({hex(x>>16<<16) for x in v})}')
    tot[k] += len(v)
print('\nresiduo d em .data:', len(resid))
for r in resid: print('  ', r)

gate['regions']['data'] = {
    'size': int(len(A0)), 'volatile_A': fa, 'volatile_B': fb, 'stable': st,
    'diff_raw': int((A0!=B0).sum()), 'diff_stable': int(len(idx)),
    'classes': {k: {'bytes': len(v), 'windows': sorted({x>>16 for x in v})} for k, v in sorted(classes.items())},
}

# data001
A0, B0, idx, fa, fb, st = stable_idx('data001')
d1 = {'unpopulated': int(((A0[idx]!=0)&(B0[idx]==0)).sum()),
      'extra': int(((A0[idx]==0)&(B0[idx]!=0)).sum()),
      'other': int(((A0[idx]!=0)&(B0[idx]!=0)).sum())}
print('\n=== .data001 359 bytes ===', d1, '| faixa 0x%X..0x%X' % (int(idx[0]), int(idx[-1])))
gate['regions']['data001'] = {'size': int(len(A0)), 'volatile_A': fa, 'volatile_B': fb, 'stable': st,
                              'diff_raw': int((A0!=B0).sum()), 'diff_stable': int(len(idx)), 'breakdown': d1}
a_str = bytes(A0[0x1640:0x1680]).split(b'\0')[0]
print('  string unica em A em +0x1640:', a_str)

# rdata01
A0, B0, idx, fa, fb, st = stable_idx('rdata01')
va = int.from_bytes(A0[0x440:0x448].tobytes(),'little'); vb = int.from_bytes(B0[0x440:0x448].tobytes(),'little')
print('\n=== .rdata01 4 bytes em 0x440 ===')
print('  A 0x%X -> secao %s' % (va, in_image(va, SEC_A)))
print('  B 0x%X -> secao %s' % (vb, in_image(vb, SEC_B)))
print('  RVA do campo: 0x79CC440 (TLS AddressOfCallBacks)')
gate['regions']['rdata01'] = {'size': int(len(A0)), 'volatile_A': fa, 'volatile_B': fb, 'stable': st,
                              'diff_stable': int(len(idx)),
                              'classes': {'a_tls_directory_structural': int(len(idx))},
                              'a_value': hex(va), 'b_value': hex(vb),
                              'a_section': in_image(va, SEC_A), 'b_section': in_image(vb, SEC_B)}

A0, B0, idx, fa, fb, st = stable_idx('text001')
gate['regions']['text001'] = {'size': int(len(A0)), 'diff_stable': int(len(idx))}
print('\n=== .text001 === 0 bytes')

print('\n=== total ===')
ad = sum(len(v) for v in classes.values())
print('  .data %d + .data001 359 + .rdata01 4 + .text001 0 = %d' % (ad, ad + 363))
print('  por classe:', dict(tot))

gate['totals'] = {'data': ad, 'data001': 359, 'rdata01': 4, 'text001': 0, 'all': ad + 363}
gate['residual_unexplained'] = resid
Path(ROOT / 'analysis/stage_reports/fase0/s3_final_gate.json').write_text(json.dumps(gate, indent=1), encoding='utf-8')
print('\ngravado: analysis/stage_reports/fase0/s3_final_gate.json')
peA.close(); peB.close()
