"""C4 — int3 no callback (Rip==site) arma TF; single-step ate o AV."""
import ctypes as C
import json, struct
from ctypes import wintypes as W
from pathlib import Path

TMP=Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
DLL=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
DEV=json.loads((TMP/'c3_deviations.json').read_text())
SITES=sorted([r for r in DEV if 0x460650<=int(r['site_rva'],16)<=0x460700 and r['status']=='fixable'],
             key=lambda r:int(r['site_rva'],16))
LOG=TMP/'c4_trace_cb2.log'; LOG.write_text('',encoding='utf-8')
k32=C.WinDLL('kernel32',use_last_error=True)
k32.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,W.DWORD,C.POINTER(W.DWORD)]
k32.VirtualProtect.restype=W.BOOL
k32.AddVectoredExceptionHandler.argtypes=[W.ULONG,C.c_void_p]
k32.AddVectoredExceptionHandler.restype=C.c_void_p

class ER(C.Structure):
    _fields_=[('code',W.DWORD),('flags',W.DWORD),('rec',C.c_void_p),
              ('addr',C.c_void_p),('n',W.DWORD),('u',W.DWORD),('info',C.c_void_p*15)]
class CTX(C.Structure):
    _fields_=[(n,C.c_uint64) for n in ('P1','P2','P3','P4','P5','P6')]+[
        ('flags',C.c_uint32),('mxcsr',C.c_uint32)]+[
        (n,C.c_uint16) for n in ('cs','ds','es','fs','gs','ss')]+[
        ('eflags',C.c_uint32)]+[
        (n,C.c_uint64) for n in ('dr0','dr1','dr2','dr3','dr6','dr7')]+[
        (n,C.c_uint64) for n in ('rax','rcx','rdx','rbx','rsp','rbp','rsi','rdi',
                                 'r8','r9','r10','r11','r12','r13','r14','r15','rip')]
class EP(C.Structure):
    _fields_=[('er',C.POINTER(ER)),('ctx',C.POINTER(CTX))]

BASE=[0]; N=[0]; TRACE=[0]; ARM=[0]; ORIG=[b'']
def rd(a):
    try: return struct.unpack('<Q',C.string_at(a,8))[0]
    except Exception: return 0

def handler(arg):
    p=C.cast(arg,C.POINTER(EP)).contents
    er,c=p.er.contents,p.ctx.contents
    code=er.code&0xffffffff
    if code==0x80000003:
        site=c.rip
        if site==ARM[0]:
            C.memmove(site,C.create_string_buffer(ORIG[0],1),1)
            c.rip=site
            c.eflags |= 0x100
            TRACE[0]=1
            with LOG.open('a',encoding='utf-8') as f:
                f.write('ARM site=%#x orig=%s rsp=%#x\n'%(site,ORIG[0].hex(),c.rsp)); f.flush()
            return 1
        with LOG.open('a',encoding='utf-8') as f:
            f.write('INT3 other site=%#x step=%d\n'%(site,N[0])); f.flush()
        c.rip=site+1
        if TRACE[0]: c.eflags |= 0x100
        return 1
    if code==0x80000004 and TRACE[0]:
        N[0]+=1
        if N[0]<25000:
            with LOG.open('a',encoding='utf-8') as f:
                f.write('STEP %d rip=%#x rsp=%#x rax=%#x rcx=%#x rdx=%#x rbx=%#x '
                        'rsi=%#x rdi=%#x r8=%#x r9=%#x r10=%#x [rsp]=%#x [rsp-8]=%#x\n'%(
                    N[0],c.rip,c.rsp,c.rax,c.rcx,c.rdx,c.rbx,c.rsi,c.rdi,c.r8,c.r9,c.r10,
                    rd(c.rsp),rd(c.rsp-8)))
                if N[0]%500==0: f.flush()
        c.eflags |= 0x100
        return 1
    if code==0xc0000005:
        with LOG.open('a',encoding='utf-8') as f:
            f.write('AV rip=%#x rsp=%#x [rsp]=%#x [rsp-8]=%#x info0=%#x steps=%d\n'%(
                c.rip,c.rsp,rd(c.rsp),rd(c.rsp-8),er.info[0] or 0,N[0]))
        return 0
    return 0

CB=C.CFUNCTYPE(C.c_long,C.c_void_p)(handler)
k32.AddVectoredExceptionHandler(1,C.cast(CB,C.c_void_p))

lib=C.CDLL(str(DLL)); lib.RecoveredInit.restype=None
BASE[0]=C.cast(lib._handle,C.c_void_p).value
lib.RecoveredInit()
for r in SITES:
    s=BASE[0]+int(r['site_rva'],16)+2; old=W.DWORD()
    assert k32.VirtualProtect(C.c_void_p(s),4,0x40,C.byref(old))
    C.memmove(s,C.create_string_buffer(bytes.fromhex(r['fix_disp32']),4),4)
    bk=W.DWORD(); assert k32.VirtualProtect(C.c_void_p(s),4,old.value,C.byref(bk))

calls=[0]
def cb_reg(a,b,c_,d): calls[0]+=1; return 1
def cb_evt(a): calls[0]+=1; return 1
f1=C.CFUNCTYPE(C.c_int,C.c_void_p,C.c_int,C.c_void_p,C.c_int)(cb_reg)
f2=C.CFUNCTYPE(C.c_int,C.c_void_p)(cb_evt)
host=(C.c_ubyte*0x80)()
for off,fn in ((0x18,f1),(0x20,f2)):
    C.memmove(C.byref(host,off),C.byref(C.c_void_p(C.cast(fn,C.c_void_p).value)),8)
cfg=(C.c_int32*64)(*([5]*64))
lib.Audio_863170.restype=C.c_void_p
lib.Audio_863170.argtypes=[C.c_void_p,C.c_void_p,C.c_double]

addr=C.cast(f1,C.c_void_p).value
old=W.DWORD()
assert k32.VirtualProtect(C.c_void_p(addr),1,0x40,C.byref(old))
ARM[0]=addr; ORIG[0]=C.string_at(addr,1)
C.memmove(addr,C.create_string_buffer(b'\xcc',1),1)
bk=W.DWORD(); assert k32.VirtualProtect(C.c_void_p(addr),1,old.value,C.byref(bk))
with LOG.open('a',encoding='utf-8') as f:
    f.write('PATCH cb %#x orig=%s\n'%(addr,ORIG[0].hex()))

ret=lib.Audio_863170(C.byref(host),C.byref(cfg),48000.0)
print('returned',hex(ret) if ret else 'NULL','steps',N[0])
