from pathlib import Path
data=Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
regs={'eax':0xb8,'ecx':0xb9,'edx':0xba,'ebx':0xbb,'esp':0xbc,'ebp':0xbd,'esi':0xbe,'edi':0xbf}
for val,name in ((0x800,'800'),(0x801,'801'),(0x808,'808')):
    print(f'=== mov imm32 {name} ===')
    for rn,op in regs.items():
        pat=bytes([op])+val.to_bytes(4,'little')
        pat2=bytes([0x41,op])+val.to_bytes(4,'little')
        for p,label in ((pat,'r32'),(pat2,'r8')):
            hits=[];s=0
            while True:
                i=data.find(p,s)
                if i<0:break
                hits.append(i);s=i+1
                if len(hits)>=50:break
            if hits:
                print(f'  {label} {rn}: {len(hits)} -> '+', '.join(hex(x) for x in hits[:15]))
