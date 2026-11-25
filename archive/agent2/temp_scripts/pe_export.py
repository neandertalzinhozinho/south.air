import pefile, re, sys, collections

p = r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
pe = pefile.PE(p, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DEBUG'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])

print('=== EXPORTS ===')
if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
    for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        print(hex(e.address), e.name.decode() if e.name else e.ordinal)
else:
    print('none')

print('=== IMPORTS ===')
if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    for m in pe.DIRECTORY_ENTRY_IMPORT:
        print(m.dll.decode(), len(m.imports))
else:
    print('none')

print('=== DEBUG ===')
if hasattr(pe, 'DIRECTORY_ENTRY_DEBUG'):
    for d in pe.DIRECTORY_ENTRY_DEBUG:
        print(d.entry, getattr(d.entry, 'PdbFileName', None), getattr(d.entry, 'Signature_Data', None))
else:
    print('none')

print('=== RESOURCES ===')
if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
    for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        print(t.name, t.id)
else:
    print('none')

# grep printable strings in full file, report interesting keywords
kw = [b'soothe', b'GetPluginFactory', b'Soothe', b'FXP', b'vst3', b'VST3', b'PACE', b'parameter', b'Bypass', b'Depth', b'Detail', b'Attack', b'Release', b'Mix', b'Quality', b'band', b'Bell', b'sidechain', b'oversampl', b'linear', b'notch']
data = open(p,'rb').read()
print('=== KEYWORD HITS ===')
for k in kw:
    idxs = [m.start() for m in re.finditer(re.escape(k), data)]
    print(k.decode(errors='replace'), len(idxs), [hex(i) for i in idxs[:6]])
