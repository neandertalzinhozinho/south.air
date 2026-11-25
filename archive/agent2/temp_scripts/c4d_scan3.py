"""C4d read-only scan v3: closure-only, matching build_recovered_dsp_dll.collect()."""
import json, re, struct
from pathlib import Path

ROOT = Path(r'D:\PROJETOS\shadowFILES')
UNITS = ROOT / 'analysis/recovered_native/units'
ENTRY = ROOT / 'analysis/recovered_native/dsp'
DUMP = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
CAP, SPAN = 0x18CC0000, 0x82A5000
SHIM = {0x1797024, 0x1796c60, 0x1796d10, 0x1796ca4, 0x1797488, 0x314fe0}
closure = json.loads((ENTRY / 'dependency_build.json').read_text())
dirs = [UNITS / f"rva_{r['start'][2:]}" for r in closure
        if r.get('status') == 'passed' and r.get('byte_identical')
        and int(r['start'], 16) not in SHIM]
defined, spans, infos = set(), [], {}
for d in dirs:
    mf = d / 'roundtrip.json'
    if not mf.exists(): continue
    try:
        info = json.loads(mf.read_text()); s = int(info['start'], 16)
        e = int(info.get('end_exclusive', info.get('end', '0x0')), 16)
    except Exception: continue
    defined.add(f'dump_{s:x}'); spans.append((s, e, f'dump_{s:x}')); infos[s] = (d, info)
spans.sort()

def owner(rva):
    best = None
    for s, e, sym in spans:
        if s <= rva < e and (best is None or (e - s) < (best[1] - best[0])): best = (s, e, sym)
    return best

kinds, rows = {}, []
for s, (d, info) in infos.items():
    for rel in info.get('relocations', []):
        if rel.get('type') != 4: continue
        cur, tgt = rel['offset'], int(rel['target_rva'], 16)
        ow = owner(tgt)
        if ow is None or ow[0] == tgt: continue
        if info.get('external_targets', {}).get(hex(tgt)) != 'PROC': continue
        b = DUMP[s + cur - 2:s + cur + 4]
        if len(b) < 6: continue
        if b[0] == 0x0F and 0x80 <= b[1] <= 0x8F: kind, doff = 'jcc', 2
        elif b[1] in (0xE8, 0xE9): kind, doff = ('call' if b[1] == 0xE8 else 'jmp'), 1
        else: continue
        kinds[kind] = kinds.get(kind, 0) + 1
        rows.append((kind, f'dump_{s:x}', cur - doff, doff, hex(tgt), ow[2], hex(tgt - ow[0])))
print('closure units:', len(infos), 'defined:', len(defined), 'proc-stub symbols expected:', len({r[4] for r in rows}))
print('kinds:', kinds, 'total sites:', len(rows))
for r in rows[:25]: print(r)

th = []
for s, (d, info) in infos.items():
    txt = (d / 'dsp_entry.asm').read_text(errors='replace')
    sites = []
    for line in txt.splitlines():
        m = re.match(r'\s*jmp\s+qword\s+ptr\s*\[dump_([0-9a-fA-F]+)\]', line, re.I)
        if m: sites.append(('sym', int(m.group(1), 16)))
    for fx in info.get('rip_db_fixups', []):
        off = fx['offset']; b = DUMP[s + off:s + off + 3]
        if b[:2] == b'\xff\x25' or b == b'\x48\xff\x25': sites.append(('db', int(fx['target_rva'], 16)))
    for src, slot in sites:
        v = struct.unpack_from('<Q', DUMP, slot)[0] if slot + 8 <= len(DUMP) else 0
        if CAP <= v < CAP + SPAN:
            rva = v - CAP; ow = owner(rva)
            th.append((src, f'dump_{s:x}', hex(slot), hex(rva), ow[2] if ow else '-',
                       'STUB' if ow and ow[0] != rva else 'OWNER'))
print('capture-pointing thunks:', len(th))
for t in th[:30]: print(t)
