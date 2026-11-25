import json, collections, hashlib
import numpy as np
from pathlib import Path
import pefile

ROOT = Path(r'D:\PROJETOS\shadowFILES')
C = ROOT / 'analysis/stage_reports/fase0/captures'
BASE = 0x180000000

A_pe = pefile.PE(str(ROOT / 'analysis/host_reference/startup_capture/original_before_load.vst3'), fast_load=True)
secs = [(s.VirtualAddress, s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData),
         s.Name.rstrip(b'\0').decode('latin1')) for s in A_pe.sections]

def in_image(v):
    if not (BASE <= v < BASE + 0x9000000):
        return None
    rva = v - BASE
    for lo, hi, n in secs:
        if lo <= rva < hi:
            return n
    return None

def load(region):
    A = [np.fromfile(C / f'A_r{i}_{region}.bin', dtype=np.uint8) for i in (1, 2, 3)]
    B = [np.fromfile(C / f'B_r{i}_{region}.bin', dtype=np.uint8) for i in (1, 2, 3)]
    return A, B

def stable_diff(region):
    A, B = load(region)
    va = ~((A[0] == A[1]) & (A[0] == A[2]))
    vb = ~((B[0] == B[1]) & (B[0] == B[2]))
    stable = ~(va | vb)
    idx = np.flatnonzero((A[0] != B[0]) & (stable) if region != 'data' else (A[0] != B[0]) & (stable))
    st = int(stable.sum())
    return A[0], B[0], idx, st, av if False else None

out = {'generated': '2026-11-16', 'base': hex(BASE), 'method': {}, 'regions': {}}

for region in ('data', 'data001', 'rdata01', 'text001'):
    A, B = load(region)
    va = ~((A[0] == A[1]) & (A[0] == A[2]))
    vb = ~((B[0] == B[1]) & (B[0] == B[2]))
    stable = ~(va | vb)
    idx = np.flatnonzero((A[0] != B[0]) & stable)
    A0, B0 = A[0], B[0]
    cls = {}
    detail = []
    for o in idx:
        o = int(o)
        s16 = o & ~0xF
        blk_a = A0[s16:s16+16].tobytes(); blk_b = B0[s16:s16+16].tobytes()
        a4 = int.from_bytes(A0[o & ~3:(o & ~3)+4].tobytes().ljust(4, b'\0'), 'little')
        b4 = int.from_bytes(B0[o & ~3:(o & ~3)+4].tobytes().ljust(4, b'\0'), 'little')
        a8 = int.from_bytes(A0[o:o+8].tobytes().ljust(8, b'\0'), 'little')
        b8 = int.from_bytes(B0[o:o+8].tobytes().ljust(8, b'\0'), 'little')
        se_a, se_b = in_image(a8), in_image(b8)

        if region == 'data' and 0x530000 <= o < 0x538556:
            k = 'b_license_state'
        elif 0 not in blk_a and 0 not in blk_b and len(set(blk_a)) >= 12 and len(set(blk_b)) >= 12:
            k = 'b_opaque_blob'
        elif se_a and se_b:
            k = 'a_image_pointer'
        elif a8 == 0 and b8 == 0 and a4 == b4 + 4 and (a4 & 0x80000000):
            k = 'b_offset_minus4'
        elif a4 == b4 + 4 and (a4 & 0x80000000) and abs(a4 - b4) == 4:
            k = 'b_offset_minus4'
        elif B0[o] == 0 and A0[o] != 0:
            k = 'c_unpopulated'
        elif A0[o] == 0 and B0[o] != 0:
            k = 'c_extra_in_candidate'
        else:
            k = 'd_unexplained'
        cls.setdefault(k, []).append(o)
        if k == 'd_unexplained':
            detail.append({'offset': hex(o), 'a': A0[o:o+8].tobytes().hex(), 'b': B0[o:o+8].tobytes().hex()})

    out['regions'][region] = {
        'volatile_A': int(va.sum()), 'volatile_B': int(vb.sum()),
        'stable_offsets': int(stable.sum()),
        'diff_stable': int(len(idx)),
        'classes': {k: {'bytes': len(v), 'first': hex(min(v)), 'last': hex(max(v))}
                    for k, v in sorted(cls.items())},
        'unexplained': detail[:40],
    }
    print(f'\n== {region}: {len(idx)} bytes estaveis-diferentes ==')
    for k, v in sorted(cls.items()):
        print(f'   {k:<22} {len(v):5d} B   0x{min(v):07X} .. 0x{max(v):07X}')
    for d in detail[:8]:
        print(f'      D  {d}')

# .data001 / .rdata01 detalhe
A1 = [np.fromfile(C / f'A_r{i}_data001.bin', dtype=np.uint8) for i in (1,2,3)]
B1 = [np.fromfile(C / f'B_r{i}_data001.bin', dtype=np.uint8) for i in (1,2,3)]
va = ~((A1[0]==A1[1]) & (A1[0]==A1[2])); vb = ~((B1[0]==B1[1]) & (B1[0]==B1[2]))
i1 = np.flatnonzero((A1[0]!=B1[0]) & ~(va|vb))
print(f'\n== data001 {len(i1)} bytes: 0x{int(i1[0]):X}..0x{int(i1[-1]):X} | A nonzero={int((A1[0][i1]!=0).sum())} B nonzero={int((B1[0][i1]!=0).sum())}')
print('   blocos com A!=0,B==0:', int(((A1[0][i1]!=0)&(B1[0][i1]==0)).sum()), '| A==0,B!=0:', int(((A1[0][i1]==0)&(B1[0][i1]!=0)).sum()))

Ar = np.fromfile(C / 'A_r1_rdata01.bin', dtype=np.uint8); Br = np.fromfile(C / 'B_r1_rdata01.bin', dtype=np.uint8)
print(f'\n== rdata01 0x440: A=0x{int.from_bytes(Ar[0x440:0x448].tobytes(),"little"):X} -> {in_image(int.from_bytes(Ar[0x440:0x448].tobytes(),"little"))}')
print(f'                B=0x{int.from_bytes(Br[0x440:0x448].tobytes(),"little"):X} -> {in_image(int.from_bytes(Br[0x440:0x448].tobytes(),"little"))}')

Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\gate_classes.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
A_pe.close()
print('\nok')
