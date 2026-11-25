import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
for rva in (0x2037268,0x1CE51A0,0x3351A0,0x1CE5910,0x1CE5CB0,0x1CE5F40,0x1CC9170,0x1CE58F0,0x1CE5240,0x1CE5300,0x1CE51E0):
    b=d[rva:rva+32]
    print(hex(rva), b.hex(), repr(b))
