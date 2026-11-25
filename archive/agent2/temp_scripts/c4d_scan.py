"""C4d read-only scan: classify REL32 relocations whose target is a code interior.

No repo writes, no build, no gate. Prints counts and sample rows.
"""
import json, re, struct
from pathlib import Path

ROOT = Path(r'D:\PROJETOS\shadowFILES')
UNITS = ROOT / 'analysis/recovered_native/units'
DUMP = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
CAP = 0x18CC0000
SPAN = 0x82A5000

manifests = sorted(UNITS.glob('rva_*/roundtrip.json'))
defined = set()
spans = []
info_by_start = {}
for mf in manifests:
    try:
        info = json.loads(mf.read_text())
        s = int(info['start'], 16)
        e = int(info.get('end_exclusive', info.get('end', '0x0')), 16)
    except Exception:
        continue
    defined.add(f'dump_{s:x}')
    spans.append((s, e, f'dump_{s:x}'))
    info_by_start[s] = (mf, info)
spans.sort()

def owner(rva):
    best = None
    for s, e, sym in spans:
        if s <= rva < e and (best is None or (e - s) < (best[1] - best[0])):
            best = (s, e, sym)
    return best

rows = []
kinds = {}
for mf, info in info_by_start.values():
    s = int(info['start'], 16)
    for rel in info.get('relocations', []):
        if rel.get('type') != 4:
            continue
        cur = rel['offset']
        tgt = int(rel['target_rva'], 16)
        ow = owner(tgt)
        if ow is None or ow[0] == tgt:
            continue
        # target is code interior, symbol dump_<tgt> is only a stub
        op = DUMP[s + cur - 2:s + cur]
        if len(op) == 2 and op[0] == 0x0F and 0x80 <= op[1] <= 0x8F:
            kind = 'jcc_rel32'
        elif len(op) == 2 and op[0] in (0xE8, 0xE9):
            kind = 'call_rel32' if op[0] == 0xE8 else 'jmp_rel32'
        else:
            kind = 'other_' + op.hex()
        kinds[kind] = kinds.get(kind, 0) + 1
        rows.append((kind, f'dump_{s:x}', cur, hex(tgt), ow[2], hex(tgt - ow[0])))

print('code spans:', len(spans), 'defined symbols:', len(defined))
print('kinds:', kinds)
print('total suspicious rel32:', len(rows))
for r in rows[:40]:
    print(r)

# thunks: jmp qword ptr [rip+disp] via rip_db_fixups or symbolic ASM
th = []
for mf, info in info_by_start.values():
    s = int(info['start'], 16)
    asm = mf.parent / 'dsp_entry.asm'
    txt = asm.read_text(errors='replace') if asm.exists() else ''
    # symbolic
    for line in txt.splitlines():
        m = re.match(r'\s*jmp\s+qword\s+ptr\s*\[dump_([0-9a-fA-F]+)\]', line, re.I)
        if m:
            slot = int(m.group(1), 16)
            v = struct.unpack_from('<Q', DUMP, slot)[0] if slot + 8 <= len(DUMP) else 0
            th.append(('sym', f'dump_{s:x}', hex(slot), hex(v),
                       hex(v - CAP) if CAP <= v < CAP + SPAN else '-'))
    # raw DB with rip_db_fixups
    for fx in info.get('rip_db_fixups', []):
        off = fx['offset']
        b = DUMP[s + off:s + off + 3]
        if b[:2] == b'\xff\x25' or b == b'\x48\xff\x25':
            slot = int(fx['target_rva'], 16)
            v = struct.unpack_from('<Q', DUMP, slot)[0] if slot + 8 <= len(DUMP) else 0
            th.append(('db', f'dump_{s:x}', hex(slot), hex(v),
                       hex(v - CAP) if CAP <= v < CAP + SPAN else '-'))
print('thunk sites total:', len(th))
for t in th[:30]:
    print(t)
