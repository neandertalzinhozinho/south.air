"""Agente 5 — v3: frames vs vizinhos + stubs reais na DLL (SOMENTE LEITURA)."""
import bisect
import datetime
import json
import re
from collections import Counter
from pathlib import Path

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r'D:\PROJETOS\shadowFILES')
UNITS = ROOT / 'analysis/recovered_native/units'
CL = ROOT / 'analysis/recovered_native/dsp'
DUMP = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
DLL = ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.dll'
MAP = ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.map'
MD = Cs(CS_ARCH_X86, CS_MODE_64)
closure = json.loads((CL / 'dependency_build.json').read_text())
starts = {int(r['start'], 16) for r in closure if r.get('byte_identical')}

meta = {}
for mf in UNITS.glob('rva_*/roundtrip.json'):
    d = json.loads(mf.read_text())
    s = int(d['start'], 16); e = int(d.get('end_exclusive') or d['end'], 16)
    meta[s] = {'dir': mf.parent, 'start': s, 'end': e, 'mtime': mf.stat().st_mtime,
               'bidem': bool(d.get('byte_identical'))}

def in_window(t):
    dt = datetime.datetime.fromtimestamp(t)
    return dt.strftime('%Y-%m-%d') == '2026-11-21' and (
        dt.hour == 3 and (dt.minute == 2 and dt.second >= 13 or dt.minute in (3, 4, 5, 6)
                          or dt.minute == 7 and dt.second <= 57))
reext = sorted([u for u in meta.values() if in_window(u['mtime'])], key=lambda x: x['start'])

def frame(s, e, scan=96):
    b = DUMP[s:e]
    off = 0
    while off < len(b) and b[off] == 0xCC:
        off += 1
    first = None
    last_add = None
    for ins in MD.disasm(b[off:off + scan], s + off):
        if ins.mnemonic == 'sub' and ins.op_str.startswith('rsp'):
            m = re.search(r'0x([0-9a-fA-F]+)|([0-9a-fA-F]+)h', ins.op_str)
            if m:
                v = int(m.group(1), 16) if m.group(1) else int(m.group(2), 16)
                if first is None:
                    first = (v, ins.bytes.hex(), ins.address - s)
    # calda: procura add rsp nos ultimos 64 bytes nao-CC
    tail = bytearray(b[-64:])
    toff = len(tail) - 1
    while toff >= 0 and tail[toff] == 0xCC:
        toff -= 1
    tb = bytes(tail[:toff + 1])
    for ins in MD.disasm(tb, e - len(tb)):
        if ins.mnemonic == 'add' and ins.op_str.startswith('rsp'):
            m = re.search(r'0x([0-9a-fA-F]+)|([0-9a-fA-F]+)h', ins.op_str)
            if m:
                v = int(m.group(1), 16) if m.group(1) else int(m.group(2), 16)
                last_add = (v, ins.bytes.hex())
    return first, last_add, b[:16].hex(), b[-16:].hex()

F = {}
for s, u in meta.items():
    F[s] = frame(u['start'], u['end'])

sorted_starts = sorted(meta)
def neigh(u, maxn=300):
    s, e = u['start'], u['end']
    out = []
    i = bisect.bisect_left(sorted_starts, s)
    j = i - 1
    while j >= 0 and len(out) < maxn:
        v = meta[sorted_starts[j]]
        if v['end'] <= s: break
        if v['start'] != s: out.append(v)
        j -= 1
    j = i
    while j < len(sorted_starts) and len(out) < maxn:
        v = meta[sorted_starts[j]]
        if v['start'] >= e: break
        if v['start'] != s: out.append(v)
        j += 1
    return out

rows = []
for u in reext:
    s = u['start']
    cf, ca, cb, ct = F[s]
    if not cf:
        continue
    ns = []
    for v in neigh(u):
        vf = F[v['start']][0]
        if vf:
            ns.append((abs(vf[0] - cf[0]), v['start'], vf[0], v['end'] - v['start']))
    ns.sort(reverse=True)
    rows.append({
        'rva': s, 'size': u['end'] - s, 'frame': cf[0], 'fbytes': cf[1],
        'epi': ca[0] if ca else None, 'epibytes': ca[1] if ca else None,
        'cb': cb, 'ct': ct, 'neigh': ns[:5], 'nneigh': len(ns),
        'maxdelta': ns[0][0] if ns else None,
        'common': Counter(x[2] for x in ns).most_common(3),
    })
print('reextraidas:', len(reext), 'com frame detectado:', len(rows))
print('sem frame detectado:', len(reext) - len(rows))
print('sub_inicial != add_final (amostra limitada 64B calda):',
      sum(1 for r in rows if r['epi'] is not None and r['epi'] != r['frame']))
print('distribuicao maxdelta vs vizinhos:', Counter(r['maxdelta'] for r in rows).most_common(20))
rows2 = sorted(rows, key=lambda r: (-(r['maxdelta'] or -1), -r['size'], r['rva']))
print('\n===== TOP 20: MAIOR DIFERENCA DE FRAME VS VIZINHOS SOBREPOSTOS =====')
for r in rows2[:20]:
    print(f"\nRVA {r['rva']:#x} size={r['size']:#x} frame={r['frame']:#x} ({r['fbytes']}) "
          f"epi={r['epi'] and hex(r['epi'])} ({r['epibytes']}) maxdelta={r['maxdelta']:#x} nneigh={r['nneigh']}")
    print(f"  bytes_ini={r['cb']} bytes_fim={r['ct']} frames_vizinhos={r['common']}")
    for d, nrva, nf, nsize in r['neigh'][:3]:
        print(f"  VIZ {nrva:#x} size={nsize:#x} frame={nf:#x} delta={d:#x}")

# ------- stubs vs unidades reais na DLL -------
print('\n===== STUBS vs UNIDADES REAIS NA DLL =====')
pe = pefile.PE(str(DLL), fast_load=False)
data = DLL.read_bytes()
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None
def dllbytes(rva, n=24):
    o = rva2off(rva)
    return data[o:o + n] if o is not None else b''
sym = {}
for ln in MAP.open(encoding='utf-8', errors='replace'):
    m = re.match(r'^\s*\d{4}:[0-9a-fA-F]{8}\s+([0-9a-fA-F]{8}h)?\s+(\S+)\s+([0-9a-fA-F]{16})', ln)
    if m and int(m.group(3), 16) >= 0x180000000:
        sym[m.group(2)] = int(m.group(3), 16) - 0x180000000
STUBPAT = b'\x0f\x28\xc0\x33\xc0\xc3'  # xorps xmm0,xmm0; xor eax,eax; ret
print('DLL: ocorrencias de 0f28c033c0c3 (stub xorps/xor/ret):', data.count(STUBPAT))
print('DLL: ocorrencias de 33c0c3:', data.count(b'\x33\xc0\xc3'))
# 152 records novos vs bak_p1_cookie = promocao de orfaos
bak = json.loads((CL / 'dependency_build.json.bak_p1_cookie').read_text())
old = {int(r['start'], 16) for r in bak}
new = sorted(starts - old)
print('records novos vs bak_p1_cookie:', len(new))
prom = {'real': 0, 'stub': 0, 'sem_simbolo': 0, 'outro': 0}
examples = {'stub': [], 'outro': [], 'real': []}
for s in new:
    nm = f'dump_{s:x}'
    if nm not in sym:
        prom['sem_simbolo'] += 1; continue
    rva = sym[nm]
    b = dllbytes(rva, 16)
    orig = DUMP[s:s + 16]
    if b[:6] == STUBPAT:
        prom['stub'] += 1
        if len(examples['stub']) < 8: examples['stub'].append((hex(s), hex(rva), b.hex()))
    elif b[:12] == orig[:12]:
        prom['real'] += 1
        if len(examples['real']) < 5: examples['real'].append((hex(s), hex(rva), b.hex()))
    else:
        prom['outro'] += 1
        if len(examples['outro']) < 10: examples['outro'].append((hex(s), hex(rva), b.hex(), orig[:12].hex()))
print('promovidos (152) na DLL:', prom)
for k, v in examples.items():
    for x in v:
        print(' ', k, x)
