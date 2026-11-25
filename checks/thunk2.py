import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
def q(rva): return struct.unpack_from("<Q",data,rva)[0]
for tab in (0x21C6AA8,):
    for i in range(0,12):
        v=q(tab+i*8)
        print(hex(tab+i*8),hex(v), "rva",hex(v-0x199B0000) if v>0x199B0000 else "")
