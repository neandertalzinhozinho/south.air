import struct, collections
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
T0,T1=0x180001000,0x181cd5487
arr=[]
runs=[]
cur=[]
for o in range(0x1d8c000,0x217f000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    if T0<=v<T1:
        if not cur: cur=[o]
        cur.append(v)
    else:
        if len(cur)-1>=4: runs.append(cur)
        cur=[]
print('vtable-like runs:',len(runs))
for r in runs[:15]:
    print('at',hex(r[0]),'n',len(r)-1,'firsts',[hex(x) for x in r[1:6]])
# also 32-bit pointers
runs32=[]
for o in range(0x1d8c000,0x217f000,4):
    v=struct.unpack_from('<I',d,o)[0]
    if T0<=v<T1:
        runs32.append((o,v))
print('32-bit code ptrs:',len(runs32), [ (hex(o),hex(v)) for o,v in runs32[:10] ])
