import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
base=0x238E9B0
def q(o): return struct.unpack_from("<Q",d,o)[0]
def dd(o): return struct.unpack_from("<d",d,o)[0]
def f32(o): return struct.unpack_from("<f",d,o)[0]
for i in [0,1,2,94]:
    o=base+i*0x68
    print("entry",i,hex(o))
    for off in range(0,0x68,8):
        raw=d[o+off:o+off+8]
        print(f"  +0x{off:02x} {raw.hex()} q={q(o+off):#x} d={dd(o+off)!r} f={f32(o+off)!r}")
print("after table", hex(base+143*0x68))
print(d[base+143*0x68:base+143*0x68+0x40].hex())
print("before", d[base-0x20:base].hex())
