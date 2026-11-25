import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
vals=[
 (0x3FD34413509F79FF,'log10(2) f64'),
 (0x3FE62E42FEFA39EF,'ln2 f64'),
 (0x3FF71547652B82FE,'1/ln2 f64'),
 (0x3E9A209B,'log10(2) f32'),
 (0x3F317218,'ln2 f32'),
 (0x3FB8AA3B,'log2(e) f32'),
 (0x3FF0000000000000,'1.0 f64'),
 (0x4000000000000000,'2.0 f64'),
 (0x4024000000000000,'10.0 f64'),
]
for v,name in vals:
    fmt='<Q' if v>0xffffffff else '<I'
    b=struct.pack(fmt,v); hits=[];s=0x1d8c000
    while True:
        i=d.find(b,s,0x217f000)
        if i<0:break
        hits.append(i);s=i+1
    print(name,hex(v),len(hits),[hex(h) for h in hits[:10]])
