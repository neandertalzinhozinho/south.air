import json, struct, collections
from pathlib import Path

A = Path(r'D:\PROJETOS\shadowFILES\analysis\startup_audit')
CAND = A / 'final_candidate_wrapperstub.vst3'
ORA = Path(r'D:\PROJETOS\shadowFILES\analysis\host_reference\startup_capture\original_before_load.vst3')
own = json.loads((A / 'import_slot_ownership.json').read_text(encoding='utf-8'))
unowned = {int(s['rva'], 16): s for s in own['unowned']['slots']}
owned = {int(s['rva'], 16): s for s in own['owned']['slots']}


def section_window(p, name, off, n):
    b = p.read_bytes()
    e = struct.unpack_from('<I', b, 0x3C)[0]
    nsec = struct.unpack_from('<H', b, e + 6)[0]
    optsz = struct.unpack_from('<H', b, e + 20)[0]
    st = e + 24 + optsz
    for i in range(nsec):
        o = st + i * 40
        nm = b[o:o + 8].rstrip(b'\x00').decode('latin-1')
        vsz, va, rsz, rptr = struct.unpack_from('<IIII', b, o + 8)
        if nm == name:
            return b[rptr + off:rptr + off + n], va + off
    raise KeyError(name)


N = 0x2000
ow, _ = section_window(ORA, '.rdata', 0, N)
cw, _ = section_window(CAND, '.rdata', 0, N)

rows = []
for i in range(0, N, 8):
    rva = 0x1d8c000 + i
    o = int.from_bytes(ow[i:i + 8], 'little')
    c = int.from_bytes(cw[i:i + 8], 'little')
    rows.append((rva, o, c))

def classify(rva):
    return 'owned' if rva in owned else ('unowned' if rva in unowned else 'undescribed')

for group in ('owned', 'unowned', 'undescribed'):
    g = [r for r in rows if classify(r[0]) == group]
    eq = sum(1 for _, o, c in g if o == c)
    o_zero = sum(1 for _, o, _ in g if o == 0)
    c_zero = sum(1 for _, _, c in g if c == 0)
    print(f'{group:12s} n={len(g):4d} equal={eq:4d} differ={len(g)-eq:4d} oracle_zero={o_zero:4d} cand_zero={c_zero:4d}')

print('\n--- unowned slots, oracle vs candidate ---')
diffs = [(r, o, c) for r, o, c in rows if classify(r) == 'unowned' and o != c]
print('differing unowned:', len(diffs))
for rva, o, c in diffs[:30]:
    print(f'  0x{rva:X}  o={o:#018x}  c={c:#018x}  callers={len(unowned[rva].get("callers") or [])}')

print('\n--- unowned where oracle nonzero ---')
onz = [r for r in rows if classify(r[0]) == 'unowned' and r[1] != 0]
print('count', len(onz))
for rva, o, c in onz[:15]:
    print(f'  0x{rva:X}  o={o:#018x}  c={c:#018x}')

# callers summary across the whole unowned set
caller_slots = {rva: (s.get('callers') or []) for rva, s in unowned.items()}
print('\nunowned slots with callers:', sum(1 for v in caller_slots.values() if v))
for rva, cl in caller_slots.items():
    if cl:
        print(f'  0x{rva:X}: {len(cl)} callers -> {cl[:4]}')
