import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
# function starts
starts=set()
for i in range(0,0x5223000,12):
    b,e,u=struct.unpack_from('<III',d,0x2758000+i)
    if b==0 and e==0: break
    starts.add(b)
print('starts',len(starts))
ptrs=[]
for o in range(0x1d8c000,0x2758000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    if 0x19000000<=v<0x1c000000:
        ptrs.append(v)
print('ptrs in range',len(ptrs))
best=[]
for B in range(0x19000000,0x1b000000,0x1000):
    n=sum(1 for v in ptrs if (v-B) in starts)
    if n: best.append((n,B))
best.sort(reverse=True)
print(best[:15])
for n,B in best[:3]:
    print(hex(B),n,'/',len(ptrs))
