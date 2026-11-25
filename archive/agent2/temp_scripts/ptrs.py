import struct, collections
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
for td in [0x23ade18,0x23bc798,0x23bde08,0x23bf4f0]:
    print(hex(td), d[td-16:td].hex(' '), '->', hex(struct.unpack_from('<Q',d,td-16)[0]))
# distribution of 8-byte values in .data that look like pointers 0x1b8...
vals=collections.Counter()
for o in range(0x2180000,0x2758000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    hi=v>>40
    if hi: vals[hi]+=1
print('top high-40 bits:', [(hex(k),v) for k,v in vals.most_common(10)])
# check occurrences of byte pattern 0x1b8d75
pat=struct.pack('<I',0x1b8d7500)[:3]
print('1b8d75 count', d.count(b'\x1b\x8d\x75'))
