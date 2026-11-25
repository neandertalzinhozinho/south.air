import capstone, struct
DUMP = r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin'
BASE = 0x180000000
data = open(DUMP,'rb').read()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail = True

# 1) qword pointers into the two functions of interest
ranges = {'0x71360..0x713eb':(BASE+0x71360, BASE+0x713eb), '0x715c0..0x71864':(BASE+0x715c0, BASE+0x71864), '0x241400..0x2414b0':(BASE+0x241400, BASE+0x2414b0)}
found = {k:[] for k in ranges}
for off in range(0, len(data)-7, 8):
    v = struct.unpack_from('<Q', data, off)[0]
    for k,(lo,hi) in ranges.items():
        if lo <= v < hi and len(found[k])<30:
            found[k].append((off, v))
for k,v in found.items():
    print(f'qword ptrs into {k}: {len(v)} ->', [(hex(o),hex(x)) for o,x in v[:15]])

# 2) indirect call/jmp in code region 0x6f000..0x72000 (linear sweep)
ind = []
for rva in range(0x6f000, 0x72000, 1):
    pass
code = data[0x6f000:0x72000]
for ins in md.disasm(code, BASE+0x6f000):
    if ins.mnemonic in ('call','jmp') and ins.operands and ins.operands[0].type != capstone.x86.X86_OP_IMM:
        ind.append((ins.address-BASE, ins.mnemonic+' '+ins.op_str))
print(f'\nindirect call/jmp in 0x6f000..0x72000 (linear): {len(ind)}')
for a,s in ind[:60]:
    print(f'  0x{a:x}: {s}')

# 3) exact qword at the specific suspect: any pointer equal to 0x180071360 / 0x1800715c0 / 0x18024140b / 0x180241426
for target in (BASE+0x71360, BASE+0x71380, BASE+0x715c0, BASE+0x24140b, BASE+0x241426):
    pat = struct.pack('<Q', target)
    hits=[]; pos=data.find(pat)
    while pos>=0 and len(hits)<10:
        hits.append(pos); pos=data.find(pat,pos+1)
    print(f'exact qword {target:#x}: {len(hits)} hits {[hex(h) for h in hits]}')
