import sys, struct
sys.path.insert(0, r'tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = re_lib.data()
BASE = 0x199B0000
md = Cs(CS_ARCH_X86, CS_MODE_64)

def u32(o): return struct.unpack_from('<I', d, o)[0]
def u64(o): return struct.unpack_from('<Q', d, o)[0]


def rip_target(ins):
    # ins.op_str like 'rax, [rip + 0x21c5e51]'
    if 'rip' not in ins.op_str:
        return None
    seg = ins.op_str.split('[rip')
    if len(seg) < 2:
        return None
    tail = seg[1]
    # tail like ' + 0x21c5e51]' or ' - 0x123]'
    tail = tail.split(']')[0].strip()
    sign = 1
    if tail.startswith('-'):
        sign = -1
        tail = tail[1:].strip()
    elif tail.startswith('+'):
        tail = tail[1:].strip()
    if not tail:
        return None
    try:
        disp = int(tail, 16)
    except ValueError:
        return None
    return ins.address + ins.size + sign * disp


def resolve(t):
    ins = list(md.disasm(d[t:t + 0x20], t))
    if len(ins) < 3:
        return None
    gaddr = rip_target(ins[0])
    tab = rip_target(ins[1])
    if gaddr is None or tab is None:
        return None
    idx = u32(gaddr)
    if idx > 0x4000:
        return ('BADIDX', idx, gaddr, tab)
    ent = u64(tab + idx * 8)
    rva = ent - BASE if BASE <= ent < BASE + 0x8300000 else None
    return (idx, gaddr, tab, ent, rva)


thunks = [0x1010, 0x1040, 0x1070, 0x10A0, 0x10D0, 0x1100, 0x1130, 0x1160,
          0x1190, 0x11C0, 0x11F0, 0x1220, 0x1250, 0x1280, 0x12B0, 0x12E0,
          0x1310, 0x1340, 0x1370, 0x13A0, 0x13D0, 0x1400, 0x1430, 0x1460,
          0x1490, 0x14C0, 0x14F0, 0x1520, 0x1550, 0x1580, 0x15B0]

for t in thunks:
    r = resolve(t)
    if r is None:
        print('thunk 0x%-5X <no parse>' % t)
        continue
    if r[0] == 'BADIDX':
        print('thunk 0x%-5X BADIDX idx=%d g=0x%X tab=0x%X' % (t, r[1], r[2], r[3]))
        continue
    idx, gaddr, tab, ent, rva = r
    print('thunk 0x%-5X idx@0x%X=%d tab=0x%X entry=0x%X %s'
          % (t, gaddr, idx, tab, ent, ('RVA 0x%X' % rva) if rva is not None else 'external'))
