import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
BASE=0x19000000
for lo,hi,label in [(0x238E000,0x2393000,'param table'),(0x1FBF000,0x1FC2000,'help strings'),(0x2398000,0x23B0000,'rtti block'),(0x1D8C000,0x1D92000,'rdata start')]:
    hits=[]
    for o in range(0,len(d)-8,8):
        v=struct.unpack_from('<Q',d,o)[0]
        r=v-BASE
        if lo<=r<hi:
            hits.append((o,r))
    print(label,'hits',len(hits),[(hex(o),hex(r)) for o,r in hits[:10]])
