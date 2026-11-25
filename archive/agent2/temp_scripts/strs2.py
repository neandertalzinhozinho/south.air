import re, struct
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
# printable strings with offsets
pat = re.compile(rb'[\x20-\x7e]{6,}')
interesting=[]
for m in pat.finditer(d):
    t=m.group().decode()
    if any(k in t for k in ('Soothe','soothe','AudioProcessor','Processor','FFT','fft','Filter','Notch','Band','Oversamp','LinearPhase','Resonan','VST3','PluginFactory','PACE','pace_')):
        interesting.append((m.start(),t))
print('count',len(interesting))
for o,t in interesting[:200]:
    print(hex(o), t[:150])
