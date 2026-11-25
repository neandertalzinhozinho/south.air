import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
for rva in (0x207a030,0x2079d24,0x2077800,0x2077740,0x2077700,0x2077840):
    print(hex(rva),hex(struct.unpack_from("<Q",d,rva)[0]),repr(struct.unpack_from("<d",d,rva)[0]),repr(struct.unpack_from("<f",d,rva)[0]))
    print("  16 bytes:",d[rva:rva+16].hex())
