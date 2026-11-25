import struct, collections
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
TXT=(0x1000,0x1cd6487); DATA=(0x217f000,0x2758dd8); RD=(0x1d8c000,0x217f000)
cands=[0x19000000,0x180000000,0x1b800000,0x1a000000,0x1b000000,0x19800000,0x190c0000]
for B in cands:
    t=dta=rd=0;tot=0
    for o in range(0x1d8c000,0x217f000,8):
        v=struct.unpack_from('<Q',d,o)[0]
        if v>0x10000:
            tot+=1
            r=v-B
            if TXT[0]<=r<TXT[1]: t+=1
            elif DATA[0]<=r<DATA[1]: dta+=1
            elif RD[0]<=r<RD[1]: rd+=1
    print(hex(B),'text',t,'data',dta,'rdata',rd,'of',tot)
