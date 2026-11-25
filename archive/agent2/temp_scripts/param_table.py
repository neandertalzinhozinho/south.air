import struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
for i in range(4):
    o=0x238e9b0+i*0x68
    print('=== entry',i,hex(o))
    print(d[o:o+0x68].hex(' '))
    for j in range(0,0x68,8):
        v=struct.unpack_from('<Q',d,o+j)[0]
        if v: print('  +%02x'%j, hex(v))
    # ascii
    print(' ascii:', ''.join(chr(c) if 32<=c<127 else '.' for c in d[o:o+0x68]))
