import struct, collections
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
IB=0x180000000
for target in [0x1fbf760, 0x1fc09c0, 0x2398570, 0x2174d34, 0x1fbaf17]:
    for fmt,val in [('<Q',target),('<Q',target+IB)]+([('<I',target)] if target<2**32 else []):
        b=struct.pack(fmt,val); idx=[];s=0
        while True:
            i=d.find(b,s)
            if i<0:break
            idx.append(i);s=i+1
        print(hex(target),fmt,hex(val),len(idx),[hex(i) for i in idx[:8]])
# count qwords in .rdata in 0x1b8... range
c=0;samples=[]
for o in range(0x1d8c000,0x217f000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    if 0x1b800000<=v<0x1c000000:
        c+=1
        if len(samples)<10: samples.append((hex(o),hex(v)))
print('rdata ptrs 0x1b8 range',c,samples)
# what are values in .rdata that point anywhere 0x1800...
c2=0;s2=[]
for o in range(0x1d8c000,0x217f000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    if 0x180000000<=v<0x1882a8000:
        c2+=1
        if len(s2)<8:s2.append((hex(o),hex(v)))
print('rdata normal VAs',c2,s2)
