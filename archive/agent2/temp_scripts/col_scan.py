import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
BASE=0x19000000
cols={}
for o in range(0x2180000,0x2758000-24,4):
    sig,off,cd,pd=struct.unpack_from('<IIIi',d,o)
    if sig not in (0,1): continue
    if not (0x2180000<=pd<0x2758000-4): continue
    if d[pd:pd+4] not in (b'.?AV',b'.?AU'): continue
    end=d.find(b'\0',pd)
    if end<0 or end-pd>300: continue
    try: name=d[pd:end].decode('ascii')
    except: continue
    cols[o]=name
print('COLs:',len(cols))
found=[]
for o in range(0x1d8c000,0x2758000-8,8):
    v=struct.unpack_from('<Q',d,o)[0]
    r=v-BASE
    if r in cols:
        found.append((o+8,cols[r]))
print('vtables via COL:',len(found))
for vt,name in found[:80]:
    print(hex(vt),name)
