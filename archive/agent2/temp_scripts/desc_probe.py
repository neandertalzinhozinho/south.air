import struct, re
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
base=0x238e9b0; stride=0x68
rows=[]; i=0
while True:
    o=base+i*stride
    if o+stride>0x2392600: break
    raw=d[o+0x14:o+0x14+0x2c]
    name=raw.split(b'\0')[0]
    if name and all(32<=c<127 for c in name) and len(name)>2:
        da=struct.unpack_from('<d',d,o+0x40)[0]
        db=struct.unpack_from('<d',d,o+0x48)[0]
        fl=struct.unpack_from('<Q',d,o+0x50)[0]
        rows.append((o,name.decode(),da,db,fl))
    i+=1
print('stride-aligned named entries:',len(rows))
for r in rows[:12]: print(hex(r[0]), r[1], r[2], r[3], hex(r[4]))
print('...')
for r in rows[-6:]: print(hex(r[0]), r[1], r[2], r[3], hex(r[4]))
