import json,re,struct
from pathlib import Path
B=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native')
d=json.load(open(B/'dsp'/'dependency_build.json'))
def h(x): return int(x,0) if isinstance(x,str) else x
sp=[(h(u['start']),h(u['end']),u) for u in d]
targets=[0x27be7b,0x27bb7f,0x27b823,0x27b4c7,0x27b18b,0x27ae52,0x27ab10,0x27a7b8,0x27a781,0x27a46c,0x27a150,0x279deb,0x279cd7,0x279cae,0x279c85,0x279c5c]
for t in targets:
    cs=[(a,b,u) for a,b,u in sp if a<=t<b and u.get('byte_identical')]
    print('0x%x:'%t)
    for a,b,u in sorted(cs,key=lambda x:x[1]-x[0])[:8]:
        print('   span 0x%x..0x%x size=0x%x status=%s note=%s' % (a,b,b-a,u.get('status'),u.get('assembler_output','')[:60]))
