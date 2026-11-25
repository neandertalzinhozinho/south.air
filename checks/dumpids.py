import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
for o in range(0x1FB6A80,0x1FB6B80,16):
    print(hex(o),repr(d[o:o+16]))
print("----")
for o in range(0x1FBF0C0,0x1FBF1B0,16):
    print(hex(o),repr(d[o:o+16]))
