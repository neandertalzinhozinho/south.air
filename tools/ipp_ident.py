import sys, struct, collections
sys.path.insert(0, r'tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = re_lib.data()
BASE = 0x199B0000
md = Cs(CS_ARCH_X86, CS_MODE_64)

def u32(o): return struct.unpack_from('<I', d, o)[0]
def i32(o): return struct.unpack_from('<i', d, o)[0]
def u64(o): return struct.unpack_from('<Q', d, o)[0]


def rip_target(ins):
    if 'rip' not in ins.op_str:
        return None
    tail = ins.op_str.split('[rip')[1].split(']')[0].strip()
    sign = 1
    if tail.startswith('-'):
        sign = -1
        tail = tail[1:].strip()
    elif tail.startswith('+'):
        tail = tail[1:].strip()
    if not tail:
        return None
    try:
        return ins.address + ins.size + sign * int(tail, 16)
    except ValueError:
        return None


def resolve(t):
    ins = list(md.disasm(d[t:t + 0x20], t))
    gaddr = rip_target(ins[0])
    tab = rip_target(ins[1])
    idx = u32(gaddr)
    ent = u64(tab + idx * 8)
    return ent - BASE


def func_end(start, limit=0x3000):
    for ins in md.disasm(d[start:start + limit], start):
        if ins.mnemonic in ('ret',):
            return ins.address + ins.size - start
    return limit


TH = [0x1010, 0x1040, 0x1070, 0x10A0, 0x10D0, 0x1100, 0x1130, 0x1160, 0x1190,
      0x11C0, 0x11F0, 0x1220, 0x1250, 0x1280, 0x12B0, 0x12E0, 0x1310, 0x1340,
      0x1370, 0x13A0, 0x13D0, 0x1400, 0x1430, 0x1460, 0x1490, 0x14C0, 0x14F0,
      0x1520, 0x1550, 0x1580, 0x15B0, 0x1C84A0, 0x1C8500, 0x1C8530, 0x1C8560,
      0x1C8590, 0x1C85C0, 0x1C85F0, 0x1C8620, 0x1C8650, 0x1C8680, 0x1C86B0,
      0x1C86E0, 0x1C8710, 0x1C8740]

VEC = ('vmulps', 'vaddps', 'vsubps', 'vdivps', 'vmaxps', 'vminps', 'vcmpps',
       'vrsqrtps', 'vrcpps', 'vsqrtps', 'vfmadd', 'vfmsub', 'vfnmadd', 'vfnmsub',
       'mulps', 'addps', 'subps', 'divps', 'maxps', 'minps', 'cmpps', 'rsqrtps',
       'rcpps', 'sqrtps', 'vmulss', 'vaddss', 'vsubss', 'vdivss', 'vmaxss',
       'vminss', 'vsqrtss', 'mulss', 'addss', 'subss', 'divss', 'maxss',
       'minss', 'sqrtss', 'vfmadd132ps', 'vfmadd213ps', 'vfmadd231ps',
       'vfmadd132ss', 'vfmadd213ss', 'vfmadd231ss', 'vpxor', 'vxorps')

for t in TH:
    try:
        impl = resolve(t)
    except Exception as e:
        print('0x%X  ERR %s' % (t, e))
        continue
    sz = func_end(impl)
    c = collections.Counter()
    for ins in md.disasm(d[impl:impl + sz], impl):
        c[ins.mnemonic] += 1
    vecs = {k: v for k, v in c.items() if k in VEC}
    print('thunk 0x%-7X -> 0x%-6X size=%-5d  %s' % (t, impl, sz, vecs))
