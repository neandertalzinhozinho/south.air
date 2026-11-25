"""Agente 5 — validacao somente-leitura: hashes, closure, objs faltantes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(r'D:\PROJETOS\shadowFILES')
UNITS = ROOT / 'analysis/recovered_native/units'
CLOSURE = ROOT / 'analysis/recovered_native/dsp/dependency_build.json'
DUMP = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()

closure = json.loads(CLOSURE.read_text())
print('closure records:', len(closure))
print('closure passed:', sum(1 for r in closure if r.get('status') == 'passed'))
print('closure byte_identical True:', sum(1 for r in closure if r.get('byte_identical')))
print('closure gaps:', sum(1 for r in closure if 'gap filler' in r.get('assembler_output', '')))

recs = []
for mf in sorted(UNITS.glob('rva_*/roundtrip.json')):
    try:
        d = json.loads(mf.read_text())
    except Exception:
        continue
    s = int(d['start'], 16)
    e = int(d.get('end_exclusive') or d['end'], 16)
    orig = DUMP[s:e]
    oh = d.get('original_sha256')
    ah = d.get('assembled_at_original_rva_sha256')
    actual_oh = hashlib.sha256(orig).hexdigest()
    recs.append({
        'dir': mf.parent.name, 'rva': s, 'end': e, 'len': len(orig),
        'oh': oh, 'ah': ah, 'bidem': bool(d.get('byte_identical')),
        'oh_ok': oh == actual_oh, 'ah_ok': ah == actual_oh,
        'rt_ok': d.get('instruction_count', 0) >= 0,
        'mtime': mf.stat().st_mtime,
    })

print('roundtrip.json total:', len(recs))
print('byte_identical True:', sum(1 for r in recs if r['bidem']))
print('byte_identical False:', sum(1 for r in recs if not r['bidem']))
print('original_sha256 bate dump:', sum(1 for r in recs if r['oh_ok']))
print('assembled_sha256 bate dump:', sum(1 for r in recs if r['ah_ok']))
print('oh == ah:', sum(1 for r in recs if r['oh'] == r['ah']))

# objs faltantes segundo compile_missing_objs.py
starts_ok = {int(r['start'], 16) for r in closure
             if r.get('status') == 'passed' and r.get('byte_identical')}
missing = [r for r in recs if r['rva'] in starts_ok and r['bidem']
           and (UNITS / r['dir'] / 'dsp_entry.asm').exists()
           and not (UNITS / r['dir'] / 'dsp_entry.obj').exists()]
print('compile_missing_objs alvos (somente leitura):', len(missing))
for r in missing[:10]:
    print('  ', hex(r['rva']))

# 1325 reextraidos (mtime 2026-11-21 03)
import datetime
reext = [r for r in recs if datetime.datetime.fromtimestamp(r['mtime']).strftime('%Y-%m-%d %H') == '2026-11-21 03']
print('reextraidos (mtime 21/11 03h):', len(reext))
print('  byte_identical:', sum(1 for r in reext if r['bidem']))
print('  original_sha256 ok:', sum(1 for r in reext if r['oh_ok']))
print('  assembled_sha256 ok:', sum(1 for r in reext if r['ah_ok']))
print('  bytes_dump_total:', sum(r['len'] for r in reext))
