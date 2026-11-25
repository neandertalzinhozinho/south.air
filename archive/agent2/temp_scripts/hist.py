import struct, collections
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
hist=collections.Counter(); ex={}
for o in range(0x1d8c000,0x217f000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    if 0x10000000<=v<0x40000000:
        b=v>>24
        hist[b]+=1; ex.setdefault(b,(hex(o),hex(v)))
for b,c in hist.most_common(20):
    print(hex(b<<24),c,ex[b])
for v in [0x1d87f760,0x1ba43b48,0x1b8d7518]:
    print(hex(v),'count',d.count(struct.pack('<Q',v)))
# histogram of lower 32-bit for high-value qwords
