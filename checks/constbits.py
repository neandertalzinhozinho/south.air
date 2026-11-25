import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
for rva in (0x207A0D0,0x207A0E8,0x207A6B8,0x207A138,0x2079E20):
    v=struct.unpack_from("<Q",d,rva)[0]
    print(hex(rva), hex(v), repr(struct.unpack_from("<d",d,rva)[0]))
