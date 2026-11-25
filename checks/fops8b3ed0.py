import struct,sys
sys.path.insert(0,r"D:\PROJETOS\soultree\tools")
d=open(r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin","rb").read()
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
want={"mulss","addss","subss","maxss","minss","divss","sqrtss","andps","xorps","cmpltss","cmpgtss","cmpless","cmpgess"}
seen=set()
for ins in md.disasm(d[0x8B3ED0:0x8B8DC1],0x8B3ED0):
    if ins.mnemonic in want:
        print(f"0x{ins.address:08X} {ins.mnemonic} {ins.op_str}")
