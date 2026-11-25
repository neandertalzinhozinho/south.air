import struct, json
from pathlib import Path
root = Path(r'D:\PROJETOS\shadowFILES')
data = (root / 'soothe3_unpacked_mem.bin').read_bytes()
pd = json.loads((root / 'analysis/recovered_native/dsp/params_dump.json').read_text())
for i in (0, 1, 50):
    off = 0x238e9c0 + i * 104
    raw = data[off:off + 104]
    print('=== id', i, pd['params'][i]['name'])
    for o in range(0, 104, 4):
        print(f'  0x{o:02x}: {raw[o:o+4].hex()}  u32=0x{struct.unpack_from("<I",raw,o)[0]:08x}  f32={struct.unpack_from("<f",raw,o)[0]:.6g}')
    print('  ddd@0x28(40) =', struct.unpack_from('<ddd', raw, 40))
    print('  ddd@0x34(52) =', struct.unpack_from('<ddd', raw, 52))
    print('  pd a=', pd['params'][i]['a'], 'bits=', hex(struct.unpack('<Q', struct.pack('<d', pd['params'][i]['a']))[0]))
    print('  pd b=', pd['params'][i]['b'], 'bits=', hex(struct.unpack('<Q', struct.pack('<d', pd['params'][i]['b']))[0]))
    print('  pd flags=', pd['params'][i]['flags'])
