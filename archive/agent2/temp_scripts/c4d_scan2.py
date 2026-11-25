"""C4d read-only scan v2: correct opcode classification + thunk slot analysis."""
import json, re, struct
from pathlib import Path

ROOT = Path(r'D:\PROJETOS\shadowFILES')
UNITS = ROOT / 'analysis/recovered_native/units'
DUMP = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
CAP = 0x18CC0000
SPAN = 0x82A5000

manifests = sorted(UNITS.glob('rva_*/roundtrip.json'))
defined, spans, info_by_start = set(), [], {}
for mf in manifests:
    try:
        info = json.loads(mf.read_text())
        s = int(info['start'], 16)
        e = int(info.get('end_exclusive', info.get('end', '0x0')), 16)
    except Exception:
        continue
    defined.add(f'dump_{s:x}'); spans.append((s, e, f'dump_{s:x}')); info_by_start[s] = (mf, info)
spans.sort()

def owner(rva):
    best = None
    for s, e, sym in spans:
        if s <= rva < e and (best is None or (e - s) < (best[1] - best[0])):
            best = (s, e, sym)
    return best

kinds, rows, nonbranch = {}, [], 0
for mf, info in info_by_start.values():
    s = int(info['start'], 16)
    for rel in info.get('relocations', []):
        if rel.get('type') != 4:
            continue
        cur = rel['offset']; tgt = int(rel['target_rva'], 16)
        ow = owner(tgt)
        if ow is None or ow[0] == tgt:
            continue
        b = DUMP[s + cur - 2:s + cur + 4]
        if len(b) < 6:
            continue
        if b[0] == 0x0F and 0x80 <= b[1] <= 0x8F:
            kind, doff = 'jcc_rel32', 2
        elif b[1] in (0xE8, 0xE9):
            kind, doff = ('call_rel32' if b[1] == 0xE8 else 'jmp_rel32'), 1
        else:
            nonbranch += 1
            continue
        kinds[kind] = kinds.get(kind, 0) + 1
        rows.append((kind, f'dump_{s:x}', cur - doff, doff, hex(tgt), ow[2], hex(tgt - ow[0])))

print('code spans:', len(spans))
print('BRANCH kinds:', kinds, 'total', len(rows), 'nonbranch rel32 skipped:', nonbranch)
for r in rows[:25]: print(r)

# thunks whose slot points into the capture range
th_cap, th_sys, th_other = [], 0, 0
for mf, info in info_by_start.values():
    s = int(info['start'], 16)
    txt = (mf.parent / 'dsp_entry.asm').read_text(errors='replace')
    sites = []
    for line in txt.splitlines():
        m = re.match(r'\s*jmp\s+qword\s+ptr\s*\[dump_([0-9a-fA-F]+)\]', line, re.I)
        if m: sites.append(('sym', int(m.group(1), 16)))
    for fx in info.get('rip_db_fixups', []):
        off = fx['offset']; b = DUMP[s + off:s + off + 3]
        if b[:2] == b'\xff\x25' or b == b'\x48\xff\x25':
            sites.append(('db', int(fx['target_rva'], 16)))
    for src, slot in sites:
        v = struct.unpack_from('<Q', DUMP, slot)[0] if slot + 8 <= len(DUMP) else 0
        if CAP <= v < CAP + SPAN:
            rva = v - CAP; ow = owner(rva)
            th_cap.append((src, f'dump_{s:x}', hex(slot), hex(v), hex(rva),
                            ow[2] if ow else '-', 'STUB' if ow and ow[0] != rva else 'OWNER'))
        elif 0x7FF000000000 <= v < 0x800000000000:
            th_sys += 1
        else:
            th_other += 1
print('thunks: capture-pointing', len(th_cap), 'system', th_sys, 'other', th_other)
for t in th_cap[:40]: print(t)
