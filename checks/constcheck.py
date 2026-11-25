import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
for rva in (0x207A0D0,0x207A0E8,0x207A6B8,0x207A138,0x2079E20):
    v=struct.unpack_from("<d",d,rva)[0]
    print(hex(rva), repr(v))
for rva in (0x2079D88,0x207A360,0x2079CF0,0x207A020,0x207A248,0x207A1F8,0x207A5A8):
    v=struct.unpack_from("<f",d,rva)[0]
    print(hex(rva), repr(v), hex(struct.unpack_from("<I",d,rva)[0]))
