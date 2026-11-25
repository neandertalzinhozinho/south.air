import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
BASE=0x199b0000
T0,T1=0x1000,0x1d8bb7d
for vt in [0x2050B90,0x2050A40,0x2050CA0,0x2050530,0x2050740,0x20506B0,0x2050610,0x20507E0,0x20509D0,0x20508F0]:
    entries=[]
    o=vt
    while True:
        v=struct.unpack_from('<Q',d,o)[0]
        r=v-BASE
        if not (T0<=r<T1): break
        entries.append(r); o+=8
    print(hex(vt),'entries',len(entries),'first',[hex(x) for x in entries[:6]])
