import pefile,capstone
p=pefile.PE(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test_v2.dll')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
CALL=0xd8977
for off,label in ((0x16b,'pathB single mov [rsp+0x20],r10'),(0x213,'pathB multi mov [rsp+0x20],rax'),(0x285,'mov dword [r12],3'),(0x9c,'call 0x715c0'),(0x117,'return after call 0x71360')):
    rva=CALL+off
    o=p.get_offset_from_rva(rva); b=bytes(p.__data__[o:o+16])
    print(f'{label}: caller+0x{off:x} = RVA 0x{rva:x} bytes={b[:12].hex()}')
    print('   ', ' ; '.join(f'{i.mnemonic} {i.op_str}' for i in md.disasm(b,rva))[:300])
