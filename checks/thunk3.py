import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
def q(rva): return struct.unpack_from("<Q",data,rva)[0]
for rva in (0x21C70E8,0x21C7110,0x21C7138):
    v=q(rva); print(hex(rva),hex(v),"rva",hex(v-0x199B0000) if v>0x199B0000 else "")
