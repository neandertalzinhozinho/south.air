import struct,sys,argparse
sys.path.insert(0,r"D:\PROJETOS\soultree\tools")
d=open(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin","rb").read()
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
from capstone.x86 import X86_OP_MEM,X86_OP_IMM,X86_REG_RIP
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
lo=int(sys.argv[1],16); hi=int(sys.argv[2],16)
def rconst(t):
    for fmt in ("<f","<d"):
        try:
            v=struct.unpack_from(fmt,d,t)[0]
        except Exception: continue
        if fmt=="<f" and (abs(v)>1e-30 and abs(v)<1e30):
            return f"f32={v!r}"
        if fmt=="<d" and (abs(v)>1e-30 and abs(v)<1e30):
            return f"f64={v!r}"
    return ""
for ins in md.disasm(d[lo:hi],lo):
    extra=""
    for op in ins.operands:
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
            t=ins.address+ins.size+op.mem.disp
            nm={0x1d8c000:"" }
            extra+=f"  ; [{hex(t)}] {rconst(t)}"
    print(f"{ins.address:08X}  {ins.mnemonic:<8} {ins.op_str}{extra}")
