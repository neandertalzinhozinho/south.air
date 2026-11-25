import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
BASE=0x19000000
T0,T1=0x1000,0x1d8bb7d
# collect vtable runs >=5
runs=[];cur=[]
for o in range(0x1d8c000,0x2758000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    if T0<=v-BASE<T1:
        if not cur: cur=[o]
        cur.append(v)
    else:
        if len(cur)-1>=5: runs.append(cur[0])
        cur=[]
res=[]
for vt in runs:
    col=struct.unpack_from('<Q',d,vt-8)[0]-BASE
    if not (0x2180000<=col<0x2758000): continue
    sig,off,cd,pd=struct.unpack_from('<IIIi',d,col)
    if not (0x2180000<=pd<0x2758000): continue
    if d[pd:pd+4]!=b'.?AV' and d[pd:pd+4]!=b'.?AU': continue
    end=d.find(b'\0',pd)
    name=d[pd:end].decode(errors='replace')
    res.append((vt,col,name))
print('named vtables:',len(res))
for vt,col,name in res:
    print(hex(vt),hex(col),name)
