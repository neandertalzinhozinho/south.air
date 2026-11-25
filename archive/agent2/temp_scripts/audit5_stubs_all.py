"""Agente 5 — varredura: simbolos dump_* que caem em zero-stub na DLL (SOMENTE LEITURA)."""
import json
import re
from pathlib import Path

import pefile

ROOT = Path(r'D:\PROJETOS\shadowFILES')
DLL = ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.dll'
MAP = DLL.with_suffix('.map')
DUMP = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
CL = ROOT / 'analysis/recovered_native/dsp/dependency_build.json'
closure = json.loads(CL.read_text())
starts = sorted({int(r['start'], 16) for r in closure if r.get('byte_identical')})
print('closure unicas:', len(starts))

pe = pefile.PE(str(DLL), fast_load=False)
data = DLL.read_bytes()
def off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None

sym = {}
for ln in MAP.open(encoding='utf-8', errors='replace'):
    m = re.match(r'^\s*\d{4}:[0-9a-fA-F]{8}\s+([0-9a-fA-F]{8}h)?\s+(\S+)\s+([0-9a-fA-F]{16})', ln)
    if m and int(m.group(3), 16) >= 0x180000000:
        sym[m.group(2)] = int(m.group(3), 16) - 0x180000000

STUBS = {
    b'\x0f\x28\xc0\x33\xc0\xc3': 'xorps xmm0,xmm0; xor eax,eax; ret',
    b'\x0f\x57\xc0\x33\xc0\xc3': 'xorps xmm6,xmm6; xor eax,eax; ret',
    b'\x33\xc0\xc3': 'xor eax,eax; ret',
    b'\x31\xc0\xc3': 'xor eax,eax; ret(31)',
}
hits = []
sem_simbolo = 0
for s in starts:
    n = f'dump_{s:x}'
    if n not in sym:
        sem_simbolo += 1
        continue
    a = sym[n]
    o = off(a)
    if o is None:
        continue
    b = data[o:o + 12]
    orig = DUMP[s:s + 12]
    for pat, desc in STUBS.items():
        if b.startswith(pat) and not orig.startswith(pat):
            hits.append((s, a, desc, b[:12].hex(), orig[:12].hex()))
            break
print('dump_* sem simbolo no map:', sem_simbolo)
print('dump_* que apontam p/ zero-stub com original DIFERENTE:', len(hits))
for h in sorted(hits):
    print(f"  RVA_orig={h[0]:#x} DLL_rva={h[1]:#x} stub='{h[2]}' dll={h[3]} orig={h[4]}")
