import hashlib
import json
import struct
from pathlib import Path

root = Path(r'D:\PROJETOS\shadowFILES')
dump = (root / 'soothe3_unpacked_mem.bin').read_bytes()
dsp = root / 'analysis/recovered_native/dsp'
m = json.loads((dsp / 'roundtrip.json').read_text())
start = int(m['start'], 16)
end = int(m['end_exclusive'], 16)
body = dump[start:end]
assert hashlib.sha256(body).hexdigest() == m['original_sha256']
leaf = dump[0x868840:0x8688bb]
assert len(leaf) == 123

local = [(0x868840, 0x3500, leaf)]
for i, rva in enumerate((0x2079d2c, 0x2079fa4, 0x207a190, 0x207a6b0, 0x207a774)):
    local.append((rva, 0x3600 + 4 * i, dump[rva:rva + 4]))
payload = b''.join(p for _, _, p in local)

relocs = [(r['offset'], int(r['target_rva'], 16), r['type']) for r in m['relocations']]
externals = sorted(int(k, 16) for k in m['external_targets'])
local_rvas = {r[0] for r in local}
missing = [r for r in externals if r not in local_rvas]

unwind = []
for info in (0x2126d2c, 0x2126d40, 0x2126d84):
    head = 4 + 4 * ((dump[info + 2] + 1) // 2)
    unwind.append(dump[info:info + head])


def arr(name, data, typ='std::uint8_t', per=16):
    lines = [f'inline constexpr {typ} {name}[] = {{']
    for i in range(0, len(data), per):
        chunk = data[i:i + per]
        vals = ', '.join(f'0x{b:02x}' if isinstance(b, int) else str(b) for b in chunk)
        lines.append('    ' + vals + (',' if i + per < len(data) else ''))
    lines.append('};')
    return '\n'.join(lines)


def structs(name, rows, fields):
    lines = [f'struct {name} {{ {fields} }};', f'inline constexpr {name} {name}s[] = {{']
    for row in rows:
        lines.append('    { ' + ', '.join(f'0x{v:x}' if isinstance(v, int) else str(v) for v in row) + ' },')
    lines.append('};')
    return '\n'.join(lines)


out = []
out.append('// Generated from analysis/recovered_native/dsp/roundtrip.json and soothe3_unpacked_mem.bin.')
out.append('// Do not edit by hand. The body is the byte-identical slice [0x864740,0x867925).')
out.append('#pragma once')
out.append('#include <cstdint>')
out.append('')
out.append('namespace soultea3::validated_dsp::data {')
out.append('')
out.append(f'inline constexpr std::uint32_t kStartRva = 0x{start:x};')
out.append(f'inline constexpr std::uint32_t kEndRva = 0x{end:x};')
out.append(f'inline constexpr std::uint32_t kBodySize = {len(body)};')
out.append(f'inline constexpr const char* kBodySha256 = "{m["original_sha256"]}";')
out.append(f'inline constexpr std::uint32_t kUnresolvedCount = {len(missing)};')
out.append('')
out.append(arr('kBody', body))
out.append('')
out.append(structs('Relocation', relocs, 'std::uint32_t offset; std::uint32_t targetRva; std::uint32_t type;'))
out.append('')
out.append(structs('LocalTarget', [(r, o, len(p)) for r, o, p in local],
                  'std::uint32_t targetRva; std::uint16_t offset; std::uint16_t size;'))
out.append('')
out.append(arr('kLocalPayload', payload))
out.append('')
for i, blob in enumerate(unwind):
    out.append(arr(f'kUnwind{i}', blob))
out.append('')
out.append('inline constexpr std::uint32_t kUnwindLo[3] = { 0x864740, 0x8649d2, 0x867917 };')
out.append('inline constexpr std::uint32_t kUnwindHi[3] = { 0x8649d2, 0x867917, 0x867925 };')
out.append('inline constexpr std::uint32_t kUnwindInfo[3] = { 0x2126d2c, 0x2126d40, 0x2126d84 }; // provenance only')
out.append('')
unresolved_bytes = b''.join(struct.pack('<I', v) for v in missing)
out.append(arr('kUnresolvedTargets', unresolved_bytes))
out.append('static_assert(sizeof(kUnresolvedTargets) == 4 * kUnresolvedCount);')
out.append('')
out.append('} // namespace soultea3::validated_dsp::data')
out.append('')

p = root / 'soothe3_reconstructed_engine/Soultea3ValidatedDSPData.h'
p.write_text('\n'.join(out), encoding='ascii')
print('wrote', p, 'bytes', p.stat().st_size, 'body', len(body), 'relocs', len(relocs), 'missing', len(missing))
print('missing', ', '.join(hex(x) for x in missing))
