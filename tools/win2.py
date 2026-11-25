import struct,sys
sys.path.insert(0,r"D:\PROJETOS\soultree\tools")
d=open(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin","rb").read()
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
from capstone.x86 import X86_OP_MEM,X86_OP_IMM,X86_REG_RIP
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
fs=int(sys.argv[1],16); lo=int(sys.argv[2],16); hi=int(sys.argv[3],16)
fe=int(sys.argv[4],16) if len(sys.argv)>4 else lo+0x400
def val(t):
    try: f=struct.unpack_from("<f",d,t)[0]
    except Exception: return ""
    try: dd=struct.unpack_from("<d",d,t)[0]
    except Exception: dd=None
    s=f"  ; [0x{t:X}]"
    if abs(f)>1e-30 and abs(f)<1e30: s+=f" f32={f!r}"
    if dd is not None and abs(dd)>1e-30 and abs(dd)<1e30: s+=f" f64={dd!r}"
    return s
for ins in md.disasm(d[fs:fe],fs):
    if lo<=ins.address<hi:
        extra=""
        for op in ins.operands:
            if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
                extra+=val(ins.address+ins.size+op.mem.disp)
        print(f"{ins.address:08X}  {ins.mnemonic:<8} {ins.op_str}{extra}")
