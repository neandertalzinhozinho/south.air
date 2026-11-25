import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
IB=0x180000000
td=0x23ade18
for fmt,val in [('<I',td),('<Q',td),('<Q',td+IB),('<I',td-16),('<Q',td-16)]:
    b=struct.pack(fmt,val)
    idx=[];s=0
    while True:
        i=d.find(b,s)
        if i<0:break
        idx.append(i);s=i+1
    print(fmt,hex(val),len(idx),[hex(i) for i in idx[:20]])
print('bytes around td-32:',d[td-32:td+48].hex(' '))
# scan possible COL where pTypeDescriptor field (offset +12) equals td, signature arbitrary small
cnt=0
for o in range(0x2180000,0x2758000-24,4):
    sig=struct.unpack_from('<I',d,o)[0]
    if sig<=2:
        ptd=struct.unpack_from('<I',d,o+12)[0]
        if ptd==td:
            print('COL cand',hex(o),d[o:o+24].hex(' '));cnt+=1
print('cands',cnt)
