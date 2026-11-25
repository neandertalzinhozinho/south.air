import re, struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
def s(off, n=160):
    e=d.index(b'\0', off)
    return d[off:min(e,off+n)].decode(errors='replace')
for off in [0x1fbf775,0x1fbf9d5,0x1fbfbea,0x1fc09d8,0x1fc0de7,0x2174d34,0x1fc01f0,0x1fbf810,0x1fc0710,0x1fc0848,0x1fc0880,0x2038408,0x2398585]:
    print(hex(off), repr(s(off)))
print('--- GetPluginFactory context ---')
print(d[0x2174d00:0x2174e00].hex(' '))
print('--- class ids near strings ---')
for m in re.finditer(b'Resonia', d):
    print('resonia', hex(m.start()))
# search UTF-16 soothe
for m in re.finditer('soothe'.encode('utf-16le'), d):
    print('utf16 soothe', hex(m.start()))
