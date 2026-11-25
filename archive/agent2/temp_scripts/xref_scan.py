import struct, time
from capstone import *
from capstone.x86 import *
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
START=0x1000; END=0x1cd6487
targets={
 0x2174d34:'GetPluginFactory str',
 0x238f24c:'Band1 frequency str',
 0x238f17c:'Band1 used str',
 0x1fbf810:'mode help',
 0x1fc0880:'quality help',
 0x1fbaf17:'FFTPACK license',
 0x1f77f90:'soothe3 pkg',
 0x1fbdca0:'updates url',
 0x2036650:'JuceVST3EditController',
 0x23ade18:'RTTI Soothe3AudioProcessor',
 0x2398570:'lambda rtti',
 0x1fc0dc0:'default preset str',
}
hits={}
entries=0; ins_count=0
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
t0=time.time()
for ins in md.disasm(d[START:END], START):
    ins_count+=1
    if ins.mnemonic in ('endbr64',): entries+=1
    if not ins.operands: continue
    for op in ins.operands:
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
            tgt=(ins.address+ins.size+op.mem.disp)&0xffffffffffffffff
            if tgt in targets:
                hits.setdefault(tgt,[]).append((ins.address,ins.mnemonic,ins.op_str))
print('instructions',ins_count,'endbr64',entries,'secs',round(time.time()-t0,1))
for t,n in targets.items():
    h=hits.get(t,[])
    print(n,hex(t),'xrefs',len(h),[(hex(a),m,o[:40]) for a,m,o in h[:5]])
