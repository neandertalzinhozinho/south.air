import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
def q(rva): return struct.unpack_from("<Q",data,rva)[0]
v=q(0x21C6F08); print(hex(v),"rva",hex(v-0x199B0000))
