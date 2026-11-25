import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
lo,hi=0x1d8c000,0x217f000
found=[]
for n in (256,512,1024,2048,4096,8192,16384):
    step=4
    for o in range(lo,hi-n*4,step):
        if o%4: continue
        a=struct.unpack_from('<%df'%n,d,o)
        if a[0]>0.01 or a[-1]>0.01: continue
        if max(a)>1.05 or min(a)<-0.01: continue
        # symmetry check
        ok=sum(1 for i in range(0,n//2, max(1,n//64)) if abs(a[i]-a[n-1-i])<0.02)
        tot=len(range(0,n//2,max(1,n//64)))
        if ok/tot>0.9 and a[n//2]>0.9:
            found.append((o,n,a[n//2]))
print('window candidates',len(found))
for o,n,m in found[:30]: print(hex(o),n,round(m,3))
