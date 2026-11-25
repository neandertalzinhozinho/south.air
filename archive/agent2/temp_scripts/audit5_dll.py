"""Agente 5 — auditoria pefile da DLL atual + stubs (SOMENTE LEITURA)."""
import re
from collections import Counter
from pathlib import Path

import pefile

ROOT = Path(r'D:\PROJETOS\shadowFILES')
DLL = ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.dll'
MAP = DLL.with_suffix('.map')
SUP = ROOT / 'analysis/recovered_native/testdll/support.asm'

data = DLL.read_bytes()
print('DLL:', DLL.name, 'size:', len(data))
pe = pefile.PE(str(DLL), fast_load=False)
print('PE valid parse: YES')
print('machine:', hex(pe.FILE_HEADER.Machine), 'is_dll:', bool(pe.FILE_HEADER.Characteristics & 0x2000))
print('sections:', pe.FILE_HEADER.NumberOfSections, 'imagebase:', hex(pe.OPTIONAL_HEADER.ImageBase))
print('SizeOfImage:', hex(pe.OPTIONAL_HEADER.SizeOfImage), 'EntryPoint RVA:', hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
print('checksum in header:', hex(pe.OPTIONAL_HEADER.CheckSum), 'computed:', hex(pe.generate_checksum()))

# exports
exp = []
for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
    exp.append((hex(e.address), e.name.decode('ascii', 'replace') if e.name else None, e.ordinal))
print('exports count:', len(exp))
for e in exp[:25]:
    print('  exp', e)

# imports
impdll, impsyms = [], 0
for d in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', []):
    dllname = d.dll.decode('ascii', 'replace')
    impdll.append((dllname, len(d.imports)))
    impsyms += len(d.imports)
print('import dlls:', len(impdll), 'import symbols:', impsyms)
for x in impdll:
    print('  imp', x)

# secoes executaveis: bytes 0xCC
EXEC = 0x20000000  # IMAGE_SCN_MEM_EXECUTE
CODE = 0x00000020
execsecs = []
for s in pe.sections:
    flags = s.Characteristics
    if not (flags & EXEC):
        continue
    b = s.get_data()
    n_cc = b.count(0xCC)
    # runs
    runs = []
    pos = 0
    while True:
        i = b.find(b'\xcc', pos)
        if i < 0:
            break
        j = i
        while j < len(b) and b[j] == 0xCC:
            j += 1
        runs.append((j - i, s.VirtualAddress + i))
        pos = j
    runs.sort(reverse=True)
    execsecs.append({
        'name': s.Name.rstrip(b'\0').decode('ascii', 'replace'),
        'rva': s.VirtualAddress, 'raw': s.SizeOfRawData, 'vs': s.Misc_VirtualSize,
        'flags': hex(flags), 'cc': n_cc, 'runs': len(runs),
        'runs16': sum(1 for r in runs if r[0] >= 16),
        'runs32': sum(1 for r in runs if r[0] >= 32),
        'runs64': sum(1 for r in runs if r[0] >= 64),
        'longest': runs[:5],
        'data': b,
    })
print('\nsecoes executaveis:', len(execsecs))
for s in execsecs:
    print(f"  {s['name']:<16} RVA={s['rva']:#x} raw={s['raw']:#x} vs={s['vs']:#x} flags={s['flags']} "
          f"CC={s['cc']} runs={s['runs']} >=16:{s['runs16']} >=32:{s['runs32']} >=64:{s['runs64']} "
          f"top={[(hex(a), n) for n, a in s['longest']]}")
tot_cc = sum(s['cc'] for s in execsecs)
tot_runs16 = sum(s['runs16'] for s in execsecs)
print('TOTAL CC em exec:', tot_cc, 'runs>=16:', tot_runs16)

# stub pattern na DLL: procurar sequencias curtas repetidas tipicas de zero-stub
# exemplos: xorps xmm0,xmm0 / xor eax,eax / ret  => 0f 28 c0 31 c0 c3
#           xor eax,eax / ret                    => 31 c0 c3
for pat, label in [(b'\x0f\x28\xc0\x31\xc0\xc3', 'xorps;xor eax,eax;ret'),
                   (b'\x31\xc0\xc3', 'xor eax,eax;ret'),
                   (b'\x33\xc0\xc3', 'xor eax,eax;ret(33)'),
                   (b'\xc3', 'ret')]:
    c = 0
    for s in execsecs:
        b = s['data']
        p = 0
        while True:
            i = b.find(pat, p)
            if i < 0:
                break
            c += 1
            p = i + 1
    print(f'padrao {label} ({pat.hex()}): {c}')

# support.asm: contar PROCs e stub zeros
stub_names = []
proc_names = []
stub_re = re.compile(r'^\s*([A-Za-z_$][\w$@]*)\s+PROC\b', re.I)
with SUP.open('r', encoding='utf-8', errors='replace') as f:
    lines = []
    for ln in f:
        lines.append(ln)
        if len(lines) > 7:
            lines.pop(0)
        m = stub_re.match(ln)
        if m:
            nm = m.group(1)
            proc_names.append(nm)
            body = ''.join(lines[-4:]).lower()
            if 'xorps' in body and 'ret' in body and ('xor eax,eax' in body.replace(' ', '') or 'xoreax' in body.replace(' ', '')):
                stub_names.append(nm)
print('support.asm PROCs:', len(proc_names), 'zero-stubs(xorps+xor+ret):', len(stub_names))
print('  exemplos stub:', stub_names[:5])
print('  exemplos PROC:', proc_names[:5])

# .map: symbol -> endereco. Verificar quantos dump_* caem em zero-stub na DLL
sym = {}
sym_re = re.compile(r'^\s*\d{4}:[0-9a-fA-F]{8}\s+([0-9a-fA-F]{8}h)?\s+(\S+)\s+([0-9a-fA-F]{16})')
with MAP.open('r', encoding='utf-8', errors='replace') as f:
    for ln in f:
        m = sym_re.match(ln)
        if not m:
            continue
        name = m.group(2)
        addr = int(m.group(3), 16)
        if addr >= pe.OPTIONAL_HEADER.ImageBase:
            sym[name] = addr - pe.OPTIONAL_HEADER.ImageBase
print('map symbols:', len(sym), 'dump_*:', sum(1 for n in sym if n.startswith('dump_')))

def rva2data(rva, n=16):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
            off = s.PointerToRawData + (rva - s.VirtualAddress)
            if off + n <= len(data):
                return data[off:off + n]
            return data[off:]
    return b''

stub_hits = []
for n, rva in sorted(sym.items()):
    if not n.startswith('dump_'):
        continue
    b = rva2data(rva, 8)
    if b[:6] == b'\x0f\x28\xc0\x31\xc0\xc3' or b[:3] in (b'\x31\xc0\xc3', b'\x33\xc0\xc3'):
        stub_hits.append((n, hex(rva), b.hex()))
print('dump_* symbols em zero-stub na DLL:', len(stub_hits))
for h in stub_hits[:12]:
    print('  ', h)
