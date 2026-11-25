import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
base=0x238E9B0
N=143
def q(o): return struct.unpack_from("<Q",d,o)[0]
def f64(o): return struct.unpack_from("<d",d,o)[0]
for i in range(N):
    o=base+i*0x68
    p1=q(o); p2=q(o+8); kind=struct.unpack_from("<I",d,o+0x10)[0]
    name=d[o+0x14:o+0x14+0x40].split(b"\x00")[0].decode("latin1")
    va=f64(o+0x58); vb=f64(o+0x60)
    tail1=q(o+0x50); tail2=q(o+0x58) if False else None
    flags=struct.unpack_from("<I",d,o+0x54)[0]
    e1=q(o+0x68-0x18); e2=q(o+0x68-0x10)
    print(f"{i:3d} {hex(o)} p1={hex(p1)} p2={hex(p2)} kind={kind} flags={flags:#x} va={va:g} vb={vb:g} {name!r} t1={hex(e1)} t2={hex(e2)}")
