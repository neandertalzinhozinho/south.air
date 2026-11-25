import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
vals32={0x40C90FDB:'2pi f32',0x40490FDB:'pi f32',0x3F000000:'0.5 f32',0x3F800000:'1.0 f32',0x42C80000:'100.0 f32',0x447A0000:'1000.0 f32'}
vals64={0x401921FB54442D18:'2pi f64',0x400921FB54442D18:'pi f64',0x3FE0000000000000:'0.5 f64',0x3FF0000000000000:'1.0 f64'}
for v,name in vals32.items():
    b=struct.pack('<I',v); hits=[];s=0x1d8c000
    while True:
        i=d.find(b,s,0x217f000)
        if i<0:break
        hits.append(i);s=i+1
    print(name,hex(v),len(hits),[hex(h) for h in hits[:12]])
for v,name in vals64.items():
    b=struct.pack('<Q',v); hits=[];s=0x1d8c000
    while True:
        i=d.find(b,s,0x217f000)
        if i<0:break
        hits.append(i);s=i+1
    print(name,hex(v),len(hits),[hex(h) for h in hits[:12]])
