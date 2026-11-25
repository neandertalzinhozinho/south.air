import re
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
for lo,hi,label in [(0x238e000,0x2394000,'param names block'),(0x2394000,0x23a0000,'rtti block')]:
    print('===',label,hex(lo),hex(hi))
    for m in re.finditer(rb'[\x20-\x7e]{4,}', d[lo:hi]):
        print(hex(lo+m.start()), m.group().decode()[:160])
