import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
base=0x238E9B0
for i in range(3):
    o=base+i*0x68
    raw=d[o:o+0x68]
    print("entry",i,hex(o))
    print(" hex:",raw.hex())
    print(" ascii:",repr(raw))
