import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
for v in [0x19000000+0x1fbf760,0x19000000+0x1fc09c0,0x19000000+0x2398570,0x19000000+0x1d8c000]:
    print(hex(v), d.count(struct.pack('<Q',v)), d.count(struct.pack('<I',v & 0xffffffff)))
# check 32-bit refs to string RVAs too
for v in [0x1fbf760,0x1fc09c0]:
    print('rva32',hex(v),'count',d.count(struct.pack('<I',v)))
