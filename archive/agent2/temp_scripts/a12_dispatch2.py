"""A12 part 2b: byte-exact scan of every `jmp qword ptr [reg+reg*8]` site."""
import json
import re
import struct
from pathlib import Path

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r'D:\PROJETOS\shadowFILES')
dump = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
pe = pefile.PE(str(ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
dll = pe.__data__
IB = pe.OPTIONAL_HEADER.ImageBase
MD = Cs(CS_ARCH_X86, CS_MODE_64)
MD.detail = True

syms = {}
for line in (ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.map').read_text(errors='replace').splitlines():
    m = re.match(r'\s*000[12]:[0-9a-f]+\s+(\S+)\s+([0-9a-fA-F]+)\s+\w', line)
    if m:
        syms[m.group(1)] = int(m.group(2), 16) - IB
rsyms = sorted((v, k) for k, v in syms.items())
rv = [x[0] for x in rsyms]


def nsym(r):
    import bisect
    i = bisect.bisect_right(rv, r) - 1
    return ('%s+0x%x' % (rsyms[i][1], r - rsyms[i][0])) if i >= 0 else '?+0x%x' % r


def dq(data, off):
    return struct.unpack_from('<Q', data, off)[0] if 0 <= off <= len(data) - 8 else None


def dd(data, off):
    return struct.unpack_from('<I', data, off)[0] if 0 <= off <= len(data) - 4 else None


def find_dispatchers(data, tag):
    out = []
    # FF /4 with SIB and index*8, REX.X/B variants: scan all 2..4 byte encodings
    for pat in (b'\x41\xff\x24\xc2', b'\x49\xff\x24\xc2', b'\xff\x24\xc2',
                b'\x42\xff\x24\xc2', b'\x4a\xff\x24\xc2', b'\x43\xff\x24\xd0'):
        i = 0
        while True:
            i = data.find(pat, i)
            if i < 0:
                break
            # decode previous 2 instructions at exact offsets (7+7 bytes)
            idx_slot = tbl = None
            win_start = max(0, i - 24)
            for ins in MD.disasm(data[win_start:i], (i - (i - win_start)) if tag == 'dump' else 0):
                pass
            # manual: look back 7 bytes for lea r10,[rip+disp32] (4c 8d 15)
            for off in (i - 7, i - 8, i - 6):
                if off >= 0 and data[off:off+3] == b'\x4c\x8d\x15':
                    tbl = off + 7 + struct.unpack_from('<i', data, off + 3)[0]
                    break
            for off in (i - 14, i - 15, i - 13):
                if off >= 0 and data[off:off+3] in (b'\x48\x63\x05', b'\x49\x63\x05'):
                    idx_slot = off + 7 + struct.unpack_from('<i', data, off + 3)[0]
                    break
            rec = {'addr': hex(i), 'pat': pat.hex(), 'idx_slot': hex(idx_slot) if idx_slot else None,
                   'table': hex(tbl) if tbl else None}
            if tag == 'dump':
                rec['idx'] = hex(dd(dump, idx_slot)) if idx_slot else None
                rec['slots'] = [hex(dq(dump, tbl + 8*k)) for k in range(8)] if tbl else []
            else:
                rva_i = i - (pe.get_offset_from_rva(0) - 0)  # not used
                off_i = i
                # find section containing file offset
                sec = None
                for s in pe.sections:
                    if s.PointerToRawData <= i < s.PointerToRawData + s.SizeOfRawData:
                        sec = s
                        break
                rva = (i - sec.PointerToRawData + sec.VirtualAddress) if sec else None
                rec['rva'] = hex(rva) if rva else None
                rec['sym'] = nsym(rva) if rva else '?'
                try:
                    rec['idx'] = hex(dd(dll, pe.get_offset_from_rva(idx_slot - IB))) if idx_slot else None
                except Exception:
                    rec['idx'] = None
                if tbl:
                    to = pe.get_offset_from_rva(tbl - IB)
                    rec['slots'] = [((hex(dq(dll, to + 8*k)) if dq(dll, to + 8*k) is not None else 'None')
                                     if to is not None else 'None') for k in range(8)]
                else:
                    rec['slots'] = []
            out.append(rec)
            i += 1
    return out

d = find_dispatchers(dll, 'dll')
u = find_dispatchers(dump, 'dump')
out = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\a12_dispatch2.json')
out.write_text(json.dumps({'dll': d, 'dump': u}, indent=1))
print('DLL dispatchers:', len(d), ' DUMP dispatchers:', len(u), 'wrote', out)
for tag, arr in (('DLL', d), ('DUMP', u)):
    print('\n===', tag, '===')
    for x in arr:
        print('%s %-28s idx_slot=%s idx=%s table=%s' % (x.get('rva') or x['addr'], x.get('sym', ''),
              x['idx_slot'], x.get('idx'), x['table']))
        if x['slots']:
            print('     slots:', ' '.join(x['slots']))
