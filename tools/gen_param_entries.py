"""Gera port/src/param_entries.rs a partir do dump (só leitura).
Entradas de parâmetro: base 0x238E9C0 (= [0x23926F8], descritor do motor 0x23926F0),
passo 0x68, 143 entradas ([0x2392700] = 0x8F). Campos lidos: +0x00 (u32 índice),
+0x28 min, +0x30 max, +0x38 centro (f64, bits), +0x48/+0x50/+0x58/+0x60 callbacks (RVA)."""
import struct
d = open(r'dumpsooth/nyx_soothe3_dump.bin', 'rb').read()
VA = 0x199B0000
assert struct.unpack_from('<Q', d, 0x23926F8)[0] - VA == 0x238E9C0
assert struct.unpack_from('<Q', d, 0x2392700)[0] == 0x8F
out = ['//! GERADO por tools/gen_param_entries.py a partir do dump (não editar à mão).',
       '//! Entradas `0x238E9C0 + i·0x68`, i = 0..143 (M4, checks/u_estado_m4.md).', '',
       '/// `[idx(+0), min(+0x28), max(+0x30), centro(+0x38)]` (f64 em bits) e callbacks RVA',
       '/// `[+0x48, +0x50, +0x58, +0x60]`.',
       '#[rustfmt::skip]',
       'pub const ENTRIES: [(u32, [u64; 3], [u32; 4]); 143] = [']
for i in range(143):
    e = 0x238E9C0 + i * 0x68
    idx = struct.unpack_from('<I', d, e)[0]
    f = struct.unpack_from('<3Q', d, e + 0x28)
    cb = [struct.unpack_from('<Q', d, e + o)[0] - VA for o in (0x48, 0x50, 0x58, 0x60)]
    out.append(f'    ({idx}, [0x{f[0]:016X}, 0x{f[1]:016X}, 0x{f[2]:016X}], [0x{cb[0]:X}, 0x{cb[1]:X}, 0x{cb[2]:X}, 0x{cb[3]:X}]), // {i} @0x{e:X}')
out.append('];')
open('port/src/param_entries.rs', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('ok', 143)
