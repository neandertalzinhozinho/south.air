import json, os
os.chdir(r'D:\PROJETOS\shadowFILES')
c=open('analysis/startup_audit/post_create_candidate_data.bin','rb').read()
o=open('analysis/startup_audit/original_post_data.bin','rb').read()
raw=[i for i in range(min(len(c),len(o))) if c[i]!=o[i]]
fb=set(json.load(open('analysis/startup_audit/noise_floor_original.json'))['volatile_offsets'])
fc=set(json.load(open('analysis/startup_audit/noise_floor_candidate.json'))['volatile_offsets'])
print('raw',len(raw),'outsideB',len([i for i in raw if i not in fb]),'outsideB+cand',len([i for i in raw if i not in fb and i not in fc]))
j2=(0x23CC700-0x217F000, 9436)
j1=(0x26AF000-0x217F000, 4096)
def rng(name,a,n):
    s=[i for i in raw if a<=i<a+n]
    print(name,'off',hex(a),'raw',len(s),'outB',len([i for i in s if i not in fb]),'outB+c',len([i for i in s if i not in fb and i not in fc]),'nz_c',sum(1 for i in range(a,a+n) if c[i]),'nz_o',sum(1 for i in range(a,a+n) if o[i]))
rng('janela2',*j2); rng('janela1',*j1)
inreg=lambda i:(j2[0]<=i<j2[0]+j2[1]) or (j1[0]<=i<j1[0]+j1[1])
print('rest raw',len([i for i in raw if not inreg(i)]),'outB',len([i for i in raw if not inreg(i) and i not in fb]),'outB+c',len([i for i in raw if not inreg(i) and i not in fb and i not in fc]))
off=j2[0]
print('j2 cand',c[off:off+32].hex()); print('j2 orac',o[off:off+32].hex())
off=j1[0]
print('j1 cand',c[off:off+32].hex()); print('j1 orac',o[off:off+32].hex())
print('nz cand',sum(1 for b in c if b),'nz orac',sum(1 for b in o if b))
