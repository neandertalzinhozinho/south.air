import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
for o in range(0x2077480,0x2077620,16):
    raw=d[o:o+16]
    print(hex(o),raw.hex(),repr(raw))
