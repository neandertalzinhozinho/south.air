import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
BASE=0x19000000
T0,T1=0x1000,0x1d8bb7d
runs=[];cur=[]
for o in range(0x1d8c000,0x2758000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    r=v-BASE
    if T0<=r<T1:
        if not cur: cur=[o]
        cur.append(v)
    else:
        if len(cur)-1>=5: runs.append(cur)
        cur=[]
if len(cur)-1>=5: runs.append(cur)
print('vtable runs>=5:',len(runs))
for r in runs[:40]:
    print('at',hex(r[0]),'n',len(r)-1,'targets',[hex((x-BASE)) for x in r[1:6]])
