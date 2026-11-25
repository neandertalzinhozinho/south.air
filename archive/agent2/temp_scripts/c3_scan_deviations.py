"""C3 — reconstrutor da tabela de desvios rel32 que caem em zero-stubs."""
import bisect
import ctypes
import json
import re
from pathlib import Path

ROOT = Path(r'D:\PROJETOS\shadowFILES')
DLL = ROOT / 'analysis' / 'recovered_native' / 'testdll' / 'recovered_dsp_test.dll'
MAP = ROOT / 'analysis' / 'recovered_native' / 'testdll' / 'recovered_dsp_test.map'
DUMP = ROOT / 'soothe3_unpacked_mem.bin'
UNITS = ROOT / 'analysis' / 'recovered_native' / 'units'
OUT = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\c3_deviations.json')

lib = ctypes.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = ctypes.cast(lib._handle, ctypes.c_void_p).value
lib.RecoveredInit()

dump = DUMP.read_bytes()
mem = ctypes.string_at(BASE + 0x1000, 0x3260a8)
mem_r2 = ctypes.string_at(BASE + 0x328000, 0x365b1e)

# simbolos dump_<rva> -> rec_rva (objetos reais, nao support_asm)
syms = {}
for line in MAP.read_text(errors='replace').splitlines():
    m = re.match(r'\s*000[12]:[0-9a-f]+\s+dump_([0-9a-f]+)\s+0000000180([0-9a-f]+)\s+\S+\s+(\S+)', line)
    if not m or 'support_asm' in m.group(3):
        continue
    syms.setdefault(int(m.group(1), 16), []).append(int(m.group(2), 16))

# range table: (rec_start, rec_end, dump_start, dump_rva)
ranges = []
for rp in UNITS.glob('rva_*/roundtrip.json'):
    try:
        j = json.loads(rp.read_text())
        d = int(j['start'], 16)
        size = int(j['source_bytes'])
        cands = syms.get(d, [])
        rec = None
        for r in cands:
            off = r - 0x1000
            if 0 <= off <= len(mem) - 8 and mem[off:off + 8] == dump[d:d + 8]:
                rec = r
                break
        if rec is None and cands:
            rec = cands[0]
        if rec is not None:
            ranges.append((rec, rec + size, d))
    except Exception:
        pass
ranges.sort()
starts = [r[0] for r in ranges]


def dump_for(rec):
    i = bisect.bisect_right(starts, rec) - 1
    if i >= 0 and rec < ranges[i][1]:
        return ranges[i][2] + (rec - ranges[i][0])
    return None


by_dump = sorted(((d, rec, end) for rec, end, d in ranges), key=lambda x: x[0])
dump_starts = [x[0] for x in by_dump]


def rec_for(drva):
    i = bisect.bisect_right(dump_starts, drva) - 1
    if i >= 0:
        d, rec, end = by_dump[i]
        if drva < d + (end - rec):
            return rec + (drva - d)
    cands = syms.get(drva, [])
    return cands[0] if cands else None


STUB_LO, STUB_HI = 0x323659, 0x325fc0
results = []
for base_rva, blob in ((0x1000, mem), (0x328000, mem_r2)):
    for i in range(len(blob) - 6):
        op = blob[i]
        if op == 0x0F and 0x80 <= blob[i + 1] <= 0x8F:
            disp = int.from_bytes(blob[i + 2:i + 6], 'little', signed=True)
            width, opcode, rel_off = 6, f'0f{blob[i+1]:02x}', 2
        elif op in (0xE8, 0xE9):
            disp = int.from_bytes(blob[i + 1:i + 5], 'little', signed=True)
            width, opcode, rel_off = 5, f'{op:02x}', 1
        else:
            continue
        if not opcode.startswith('0f'):
            continue
        site = base_rva + i
        target = site + width + disp
        if not (STUB_LO <= target < STUB_HI):
            continue
        dsite = dump_for(site)
        if dsite is None:
            continue
        drel = int.from_bytes(dump[dsite + rel_off:dsite + rel_off + 4], 'little', signed=True)
        dtarget = dsite + width + drel
        rtarget = rec_for(dtarget)
        if rtarget is None or STUB_LO <= rtarget < STUB_HI:
            status, fix = 'unmapped', None
        else:
            status = 'fixable'
            fix = (rtarget - (site + width)).to_bytes(4, 'little', signed=True).hex()
        results.append({
            'opcode': opcode, 'site_rva': hex(site), 'dump_site': hex(dsite),
            'stub_target': hex(target), 'dump_target': hex(dtarget),
            'authentic_rva': hex(rtarget) if rtarget is not None else None,
            'status': status, 'fix_disp32': fix,
            'cur_disp': hex(disp & 0xFFFFFFFF),
        })

OUT.write_text(json.dumps(results, indent=2), encoding='utf-8')
print('ranges', len(ranges), 'total', len(results),
      'fixable', sum(r['status'] == 'fixable' for r in results))
for r in results:
    print(r['opcode'], r['site_rva'], r['dump_site'], '->', r['stub_target'],
          'dump->', r['dump_target'], 'auth->', r['authentic_rva'],
          r['status'], r['fix_disp32'])
