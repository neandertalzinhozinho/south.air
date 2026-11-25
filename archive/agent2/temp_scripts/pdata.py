import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
base=0x2758000
entries=[]
for i in range(0,0x5223000,12):
    b,e,u=struct.unpack_from('<III',d,base+i)
    if b==0 and e==0: break
    entries.append((b,e,u))
print('pdata entries',len(entries))
print('first',[(hex(b),hex(e),hex(u)) for b,e,u in entries[:5]])
print('last',[(hex(b),hex(e),hex(u)) for b,e,u in entries[-5:]])
# check zero-run after
z=0
for i in range(base, base+0x5223000):
    if d[i]!=0: z+=1
print('nonzero bytes in .pdata virtual range',z)
# code size coverage
cov=sum(e-b for b,e,u in entries)
print('covered code bytes',hex(cov),'text size',hex(0x1cd5487))
