import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
def q(rva): return struct.unpack_from("<Q",data,rva)[0]
v=q(0x21C6A28+4*8); print("1C84A0 idx4 entry",hex(v),"rva",hex(v-0x199B0000))
# target funcs
for rva in (0x1C8A00,0x1C89E0,0x1C8A20):
    pass
