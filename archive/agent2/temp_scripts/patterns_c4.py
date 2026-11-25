from pathlib import Path
files={
 'dump':Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes(),
 'dll':Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll').read_bytes(),
}
pats={
 'push imm32 -0x90 (68 70ffffff)':'68'+'70ffffff',
 'push imm8 -0x90 (6a 70)':'6a70',
 'mov r/m64,imm32 -0x90 (c7 /0 70ffffff)':'c7',
 'add rsp,0x90 (4883c490)':'4883c490',
 'sub rsp,0x90 (4883ec90)':'4883ec90',
 'add rsp,-0x90 (4883c470)':'4883c470',
 'sub xxx,0x90 imm8 83 /5 90':'83e890',
 'cmp xxx,0x90 83 /7 90':'83f890',
 'mov eax,0xffffff70 (b870ffffff)':'b870ffffff',
 'mov ecx,0xffffff70 (b970ffffff)':'b970ffffff',
 'mov edx,0xffffff70 (ba70ffffff)':'ba70ffffff',
 'mov r8d,0xffffff70 (41b070ffffff)':'41b070ffffff',
}
def findall(b,p):
    o=[];s=0
    while True:
        i=b.find(p,s)
        if i<0:break
        o.append(i);s=i+1
        if len(o)>500:break
    return o
for name,b in files.items():
    print('====',name)
    for label,h in pats.items():
        p=bytes.fromhex(h)
        hits=findall(b,p)
        print('%-42s %5d %s'%(label,len(hits),' '.join(hex(x) for x in hits[:15])))
    # dword 0xffffff70 aligned on 4 and 8
    q=bytes.fromhex('70ffffff')
    hits=findall(b,q)
    al4=[x for x in hits if x%4==0]
    al8=[x for x in hits if x%8==0]
    print('DWORD ffffff70: total %d aligned4 %d aligned8 %d'%(len(hits),len(al4),len(al8)))
    print('  aligned8 offsets:',[hex(x) for x in al8[:30]])
