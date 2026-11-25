import re
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
pat=re.compile(rb'[\x20-\x7e]{5,}')
hits=[]
for m in pat.finditer(d):
    t=m.group().decode()
    if 'Soothe' in t or 'Soothe' in t.lower() and ('3' in t):
        hits.append((m.start(),t))
print('Soothe strings:',len(hits))
for o,t in hits:
    print(hex(o),t[:180])
