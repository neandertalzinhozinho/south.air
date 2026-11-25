import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
targets=[0x1FBF760,0x1FBFBD0,0x1FC0880,0x1FC09C0,0x238E9C4,0x238F24C,0x2398570,0x23ADE18,0x1FBDB70]
best=[]
for B in range(0x180000000,0x1C000000,0x10000):
    n=0
    for t in targets:
        v=B+t
        if v>=2**64: continue
        if d.count(struct.pack('<Q',v))>0: n+=1
    if n: best.append((B,n))
best.sort(key=lambda x:-x[1])
print(best[:20])
for B,n in best[:5]:
    print('base',hex(B),'matches',n)
    for t in targets:
        v=B+t
        c=d.count(struct.pack('<Q',v))
        if c: print('   ',hex(t),c)
