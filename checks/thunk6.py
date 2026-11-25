import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
def q(rva): return struct.unpack_from("<Q",data,rva)[0]
for slot in (0x1D8D808,0x1D8D818,0x1D8D540,0x1D8D890):
    v=q(slot)
    print(hex(slot),"->",hex(v),"rva",hex(v-0x199B0000) if v>0x199B0000 else hex(v))
