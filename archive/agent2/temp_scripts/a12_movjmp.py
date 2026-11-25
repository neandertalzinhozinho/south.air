"""A12 part 3: exhaustive `mov r64,[rip+disp]; jmp r64` thunk scan (dump + DLL)."""
import json
import re
import struct
from pathlib import Path

import pefile

ROOT = Path(r'D:\PROJETOS\shadowFILES')
dump = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
pe = pefile.PE(str(ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
dll = pe.__data__
IB = pe.OPTIONAL_HEADER.ImageBase

# all REX.W mov r64,[rip+disp32] encodings: 48/49 8b /r with mod=00 rm=101
MOV_PREFIXES = [bytes([r, 0x8b, 0x05 | (k << 3)]) for r in (0x48, 0x49) for k in range(8)]
def jmp_enc(rex, reg):
    # jmp r/m64 = FF /4 ; reg 0-7 -> FF E0+reg ; r8-r15 -> 41 FF E0+(reg-8)
    if rex == 0x48:
        return bytes([0xff, 0xe0 | reg])
    return bytes([0x41, 0xff, 0xe0 | (reg & 7)])


def dq(data, off):
    return struct.unpack_from('<Q', data, off)[0] if 0 <= off <= len(data) - 8 else None


def scan(data, tag, start=0, end=None):
    end = end or len(data)
    out = []
    for pre in MOV_PREFIXES:
        rex, _, modrm = pre
        reg = (modrm >> 3) & 7
        expect_jmp = jmp_enc(rex, reg)
        i = start
        while True:
            i = data.find(pre, i, end)
            if i < 0:
                break
            disp = struct.unpack_from('<i', data, i + 3)[0]
            slot = i + 7 + disp
            # jmp must be within 12 bytes after the 7-byte mov
            found = None
            for j in range(i + 7, min(i + 19, end)):
                if data[j:j+2] == expect_jmp:
                    found = j
                    break
            if found is not None:
                v = dq(data, slot)
                out.append({'addr': hex(i), 'mov': pre.hex() + data[i+3:i+7].hex(),
                            'jmp': expect_jmp.hex(), 'jmp_at': hex(found),
                            'slot': hex(slot), 'value': hex(v) if v is not None else None})
            i += 1
    return out

u = scan(dump, 'dump', 0x1000, 0x1CD5800)
d = scan(dll, 'dll')
out = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\a12_movjmp.json')
out.write_text(json.dumps({'dump': u, 'dll': d}, indent=1))
print('DUMP mov-jmp thunks:', len(u), 'DLL mov-jmp thunks:', len(d), 'wrote', out)

for tag, arr in (('DUMP', u), ('DLL', d)):
    print('\n===', tag, 'mov r,[rip]; jmp r ===')
    for x in arr:
        print('%s  %-22s slot=%s value=%s  jmp@%s' %
              (x['addr'], x['mov'], x['slot'], x['value'], x['jmp_at']))
