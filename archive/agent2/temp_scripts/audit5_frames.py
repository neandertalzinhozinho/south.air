"""Agente 5 — auditoria de frames das 1325 unidades reextraidas (SOMENTE LEITURA)."""
import bisect
import datetime
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r'D:\PROJETOS\shadowFILES')
UNITS = ROOT / 'analysis/recovered_native/units'
CLOSURE = ROOT / 'analysis/recovered_native/dsp/dependency_build.json'
DUMP = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
MD = Cs(CS_ARCH_X86, CS_MODE_64)

closure = json.loads(CLOSURE.read_text())
cl_by_start = {int(r['start'], 16): r for r in closure}
starts = set(cl_by_start)

units = {}
for mf in sorted(UNITS.glob('rva_*/roundtrip.json')):
    try:
        d = json.loads(mf.read_text())
    except Exception:
        continue
    s = int(d['start'], 16)
    e = int(d.get('end_exclusive') or d['end'], 16)
    units[s] = {
        'rva': s, 'end': e, 'dir': mf.parent,
        'mftime': mf.stat().st_mtime,
        'bidem': bool(d.get('byte_identical')),
    }

reext = [u for u in units.values()
         if datetime.datetime.fromtimestamp(u['mftime']).strftime('%Y-%m-%d %H') == '2026-11-21 03']
reext.sort(key=lambda u: u['rva'])
print('unidades reextraidas (mtime 21/11 03h):', len(reext))

# ---------- extracao de frames com capstone ----------
IMM_RE = re.compile(r'0x([0-9a-fA-F]+)|(\d+)h?|([0-9]+)')

def imm_of(op):
    m = re.search(r'0x([0-9a-fA-F]+)', op)
    if m:
        return int(m.group(1), 16)
    m = re.search(r'\b([0-9a-fA-F]+)h\b', op)
    if m:
        return int(m.group(1), 16)
    m = re.search(r'\b(\d+)\b', op)
    if m:
        return int(m.group(1), 10)
    return None

def scan(code, base, full=False):
    """Retorna (subs, adds, leas, max_rsp_disp, nins)."""
    subs, adds, leas = [], [], []
    maxdisp = -1
    n = 0
    for ins in MD.disasm(code, base):
        n += 1
        op = ins.op_str
        if ins.mnemonic == 'sub' and op.startswith('rsp'):
            v = imm_of(op.split(',', 1)[-1])
            if v is not None:
                subs.append((ins.address - base, v, ins.bytes.hex(), ins.mnemonic + ' ' + op))
        elif ins.mnemonic == 'add' and op.startswith('rsp'):
            v = imm_of(op.split(',', 1)[-1])
            if v is not None:
                adds.append((ins.address - base, v, ins.bytes.hex(), ins.mnemonic + ' ' + op))
        elif ins.mnemonic == 'lea' and op.startswith('rsp'):
            v = imm_of(op)
            if v is not None:
                leas.append((ins.address - base, v, ins.bytes.hex(), ins.mnemonic + ' ' + op))
        if 'rsp' in op and '[' in op:
            for mm in re.finditer(r'\[rsp\s*([+-])\s*(0x[0-9a-fA-F]+|[0-9a-fA-F]+h|\d+)', op):
                v = imm_of(mm.group(2))
                if v is not None and mm.group(1) == '+':
                    maxdisp = max(maxdisp, v)
    return subs, adds, leas, maxdisp, n

def unit_frames(u, window=96, full=False):
    s, e = u['rva'], u['end']
    code = DUMP[s:e]
    if full or len(code) <= window * 2:
        subs, adds, leas, mx, n = scan(code, s)
        head, tail = code[:window], code[max(0, len(code) - window):]
    else:
        subs, adds, leas, mx, n = scan(code[:window], s), None, None, None, None
        h = scan(code[:window], s)
        t = scan(code[len(code) - window:], e - window)
        subs = h[0] + [(a + len(code) - window, v, b, txt) for a, v, b, txt in t[0]]
        adds = h[1] + [(a + len(code) - window, v, b, txt) for a, v, b, txt in t[1]]
        leas = h[2] + [(a + len(code) - window, v, b, txt) for a, v, b, txt in t[2]]
        mx = max(h[3], t[3])
        n = len(code)
        head, tail = h, t
    frame = subs[0][1] if subs else (leas[0][1] if leas else None)
    epilogue = adds[-1][1] if adds else None
    return {'subs': subs, 'adds': adds, 'leas': leas, 'maxdisp': mx,
            'frame': frame, 'epi': epilogue, 'bytes': code, 'n': n}

# frames de todas as unidades (cabecalho/calda) para comparacao com vizinhos
allframes = {}
for u in units.values():
    allframes[u['rva']] = unit_frames(u)

# ---------- vizinhos por sobreposicao ----------
sorted_starts = sorted(units)
def overlapping(u, maxn=200):
    s, e = u['rva'], u['end']
    i = bisect.bisect_left(sorted_starts, s)
    out = []
    # para tras enquanto unf possivel começar antes e terminar depois de s
    j = i - 1
    while j >= 0 and len(out) < maxn:
        v = units[sorted_starts[j]]
        if v['end'] <= s:
            break
        if v['rva'] != s:
            out.append(v)
        j -= 1
    j = i
    while j < len(sorted_starts) and len(out) < maxn:
        v = units[sorted_starts[j]]
        if v['rva'] >= e:
            break
        if v['rva'] != s:
            out.append(v)
        j += 1
    return out

# ---------- referencias stale dump_base+delta ----------
STALE_RE = re.compile(r'\bdump_([0-9a-fA-F]+)\s*\+\s*0?([0-9a-fA-F]+)h?\b')

def stale_refs(u):
    asm = u['dir'] / 'dsp_entry.asm'
    if not asm.exists():
        return []
    txt = asm.read_text(errors='replace')
    out = []
    for m in STALE_RE.finditer(txt):
        tgt = int(m.group(1), 16) + int(m.group(2), 16)
        if tgt in starts:
            out.append((tgt, m.group(0), m.start()))
    return out

# frame completo das unidades reextraidas (para maxdisp / sub multiple)
fullframes = {u['rva']: unit_frames(u, full=True) for u in reext}

rows = []
for u in reext:
    s = u['rva']
    fr = fullframes[s]
    neigh = overlapping(u)
    nd = []
    for v in neigh:
        vf = allframes[v['rva']]
        if vf['frame'] is not None and fr['frame'] is not None:
            nd.append((abs(vf['frame'] - fr['frame']), v['rva'], vf['frame'],
                       v['end'] - v['rva']))
    nd.sort(reverse=True)
    sr = stale_refs(u)
    sr_frames = []
    for tgt, text, pos in sr:
        if tgt in allframes:
            tf = allframes[tgt]['frame']
            if tf is not None and fr['frame'] is not None:
                sr_frames.append((abs(tf - fr['frame']), tgt, tf, text,
                                  allframes[tgt]['bytes'][:16].hex()))
    sr_frames.sort(reverse=True)
    subvals = sorted({x[1] for x in fr['subs']})
    addvals = sorted({x[1] for x in fr['adds']})
    mismatch = (fr['frame'] is not None and fr['epi'] is not None
                and fr['frame'] != fr['epi'])
    overdisp = fr['maxdisp'] - fr['frame'] if (fr['maxdisp'] >= 0 and fr['frame']) else -1
    score = (max([x[0] for x in sr_frames], default=0) * 4
             + (0x100 if mismatch else 0)
             + max([x[0] for x in nd], default=0)
             + (overdisp if overdisp > 0 else 0)
             + (0x40 if len(subvals) > 1 else 0))
    rows.append({
        'rva': s, 'end': u['end'], 'size': u['end'] - s,
        'frame': fr['frame'], 'epi': fr['epi'], 'subs': subvals, 'adds': addvals,
        'sub_first': fr['subs'][0] if fr['subs'] else None,
        'add_last': fr['adds'][-1] if fr['adds'] else None,
        'maxdisp': fr['maxdisp'], 'overdisp': overdisp,
        'neigh': nd[:4], 'nneigh': len(neigh),
        'stale': sr[:4], 'nstale': len(sr), 'stale_frames': sr_frames[:4],
        'mismatch': mismatch, 'score': score,
        'bytes': fr['bytes'][:24].hex(),
        'bytes_end': fr['bytes'][-24:].hex(),
        'bidem': u['bidem'],
        'actual_oh_ok': hashlib.sha256(DUMP[s:u['end']]).hexdigest() ==
                        json.loads((u['dir'] / 'roundtrip.json').read_text()).get('original_sha256'),
    })

rows.sort(key=lambda r: (-r['score'], -r['nstale'], r['rva']))
print('com byte_identical=True:', sum(1 for r in rows if r['bidem']))
print('com original_sha256 ok:', sum(1 for r in rows if r['actual_oh_ok']))
print('com frame identificado:', sum(1 for r in rows if r['frame'] is not None))
print('com prologo/epilogo sub vs add differentes:', sum(1 for r in rows if r['mismatch']))
print('com refs stale (dump_x+delta p/ start exato):', sum(1 for r in rows if r['nstale']))
print('com max[rsp+disp] acima do frame:', sum(1 for r in rows if r['overdisp'] > 0))
print('distribuicao frames (top 15):', Counter(r['frame'] for r in rows).most_common(15))
print('distribuicao deltas vizinhos (top 15):',
      Counter(x[0] for r in rows for x in r['neigh']).most_common(15))
print('distribuicao deltas stale (top 15):',
      Counter(x[0] for r in rows for x in r['stale_frames']).most_common(15))

print('\n===== TOP 20 MAIS SUSPEITAS =====')
for r in rows[:20]:
    print(f"\nRVA {r['rva']:#010x} size={r['size']} score={r['score']:#x} "
          f"frame={r['frame'] and hex(r['frame'])} epi={r['epi'] and hex(r['epi'])} "
          f"mismatch={r['mismatch']} overdisp={r['overdisp']} nstale={r['nstale']} nneigh={r['nneigh']}")
    print(f"  subs={[hex(x) for x in r['subs'][:8]]} adds={[hex(x) for x in r['adds'][:8]]} maxdisp={r['maxdisp']:#x}")
    print(f"  bytes_ini={r['bytes']} bytes_fim={r['bytes_end']}")
    if r['stale_frames']:
        for d, tgt, tf, text, tb in r['stale_frames'][:2]:
            print(f"  STALE -> {tgt:#x} frame={tf and hex(tf)} delta={d:#x} ref='{text}' tgtbytes={tb}")
    elif r['stale']:
        for tgt, text, pos in r['stale'][:2]:
            print(f"  STALE -> {tgt:#x} (sem frame) ref='{text}'")
    if r['neigh']:
        for d, nrva, nf, nsize in r['neigh'][:2]:
            print(f"  VIZINHO {nrva:#x} size={nsize} frame={nf and hex(nf)} delta={d:#x}")

#dump completo para arquivo temporario (fora do repo)
out = ROOT.parent.parent  # apenas referencia
import pickle
with open(r'C:\Users\tromb\AppData\Local\Temp\opencode\audit5_frames_rows.pkl', 'wb') as f:
    pickle.dump(rows, f)
