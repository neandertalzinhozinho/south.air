import pefile,capstone
for name in ('recovered_dsp_test_v2.dll','recovered_dsp_test.dll'):
    p=pefile.PE(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\\'+name)
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    print('===',name,'===')
    for rva,label in ((0x5f86be,'AV?'),(0x5f865f,'callee?'),(0xd8977,'caller?'),(0x6156be,'AV-main'),(0xf5977,'caller-main')):
        o=p.get_offset_from_rva(rva); b=bytes(p.__data__[o:o+24])
        ins=list(md.disasm(b,rva))
        print(f'  0x{rva:x} {label}: {b[:16].hex()} | '+' ; '.join(f'{i.mnemonic} {i.op_str}' for i in ins[:4]))
