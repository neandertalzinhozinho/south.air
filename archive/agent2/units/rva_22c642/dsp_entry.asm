OPTION CASEMAP:NONE
EXTERN dump_22a654:PROC
EXTERN dump_22c294:PROC
EXTERN dump_2d74a0:PROC
EXTERN dump_1796c40:PROC
EXTERN dump_1e50980:BYTE
EXTERN dump_1e50cc0:BYTE
EXTERN dump_1e51d00:BYTE
EXTERN dump_1e51d40:BYTE
EXTERN dump_1e51ec0:BYTE
EXTERN dump_1e520c0:BYTE
EXTERN dump_1e52100:BYTE
EXTERN dump_1e52140:BYTE
EXTERN dump_1e52180:BYTE
EXTERN dump_1e521c0:BYTE
EXTERN dump_1e52200:BYTE
EXTERN dump_1e52240:BYTE
EXTERN dump_21c7640:BYTE
EXTERN dump_26adfc0:BYTE
R2TEXT SEGMENT ALIGN(1) 'CODE'
PUBLIC Audio_22c642
PUBLIC dump_22c642
Audio_22c642 PROC
dump_22c642 LABEL NEAR
ins_22c642:
    DB 041h,089h,0efh
ins_22c645:
    neg r15d
ins_22c648:
    cmp ebp, r8d
ins_22c64b:
    jae NEAR PTR ins_22c8f0
ins_22c651:
    vmovups zmm21, zmmword ptr [dump_1e51d00]
ins_22c65b:
    DB 048h,089h,0d6h
ins_22c65e:
    vmovups zmm2, zmmword ptr [dump_1e51d40]
ins_22c668:
    vmovups xmmword ptr [rsp + 02e0h], xmm9
ins_22c671:
    vmovups xmmword ptr [rsp + 02f0h], xmm10
ins_22c67a:
    vmovups xmmword ptr [rsp + 0300h], xmm11
ins_22c683:
    vmovups xmmword ptr [rsp + 0310h], xmm12
ins_22c68c:
    vmovups zmm20, zmmword ptr [dump_1e520c0]
ins_22c696:
    DB 044h,089h,0c7h
ins_22c699:
    vmovups zmm18, zmmword ptr [dump_1e52100]
ins_22c6a3:
    vmovups zmm17, zmmword ptr [dump_1e52140]
ins_22c6ad:
    vmovups zmm3, zmmword ptr [dump_1e52180]
ins_22c6b7:
    vmovups zmm4, zmmword ptr [dump_1e521c0]
ins_22c6c1:
    vmovups zmm5, zmmword ptr [dump_1e52200]
ins_22c6cb:
    vmovups zmm16, zmmword ptr [dump_1e52240]
ins_22c6d5:
    vmovups xmmword ptr [rsp + 0320h], xmm13
ins_22c6de:
    vmovups xmmword ptr [rsp + 0330h], xmm14
ins_22c6e7:
    vmovups xmmword ptr [rsp + 0340h], xmm15
ins_22c6f0:
    vmovups zmm19, zmmword ptr [dump_1e51ec0]
ins_22c6fa:
    vmovups zmm1, zmmword ptr [dump_1e50cc0]
ins_22c704:
    vmovups zmm0, zmmword ptr [dump_1e50980]
ins_22c70e:
    mov byte ptr [rsp + 0350h], r11b
ins_22c716:
    DB 04ch,089h,0d3h
ins_22c719:
    mov dword ptr [rsp + 0368h], eax
ins_22c720:
    mov dword ptr [rsp + 0358h], ecx
ins_22c727:
    mov dword ptr [rsp + 0360h], r9d
ins_22c72f:
    DB 00fh,01fh,084h,000h,000h,000h,000h,000h
ins_22c737:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_22c73e:
    DB 066h,090h
ins_22c740:
    mov eax, 010h
ins_22c745:
    lea ecx, [rdi + r15]
ins_22c749:
    cmp ecx, 010h
ins_22c74c:
    mov r11, 0ffffffffh
ins_22c756:
    DB 041h,089h,0ech
ins_22c759:
    cmovae ecx, eax
ins_22c75c:
    xor r14d, r14d
ins_22c75f:
    neg ecx
ins_22c761:
    add ecx, 020h
ins_22c764:
    shrx rax, r11, rcx
ins_22c769:
    mov dword ptr [r13], eax
ins_22c76d:
    kmovw k1, eax
ins_22c771:
    vmovaps zmm14, zmm1
ins_22c777:
    vmovups zmm14 {k1}, zmmword ptr [rbx + r12*4]
ins_22c77e:
    vandps zmm10, zmm14, zmm21
ins_22c784:
    vandnps zmm30, zmm21, zmm14
ins_22c78a:
    vmovaps zmm12, zmm19
ins_22c790:
    vmovaps zmm24, zmm5
ins_22c796:
    vmovaps zmm26, zmm5
ins_22c79c:
    vfmadd231ps zmm12, zmm20, zmm10, {rn-sae}
ins_22c7a2:
    vcmple_oqps k2, zmm10, zmm2, {sae}
ins_22c7a9:
    vcvtps2pd zmm22, ymm10, {sae}
ins_22c7af:
    vpslld zmm9, zmm12, 01fh
ins_22c7b6:
    vsubps zmm13, zmm12, zmm19, {rn-sae}
ins_22c7bc:
    vextractf32x8 ymm11, zmm10, 1
ins_22c7c3:
    vcvtps2pd zmm23, ymm11, {sae}
ins_22c7c9:
    vextractf32x8 ymm15, zmm13, 1
ins_22c7d0:
    vcvtps2pd zmm28, ymm13, {sae}
ins_22c7d6:
    vxorps zmm13, zmm9, zmm30
ins_22c7dc:
    vcvtps2pd zmm29, ymm15, {sae}
ins_22c7e2:
    vfnmadd231pd zmm22, zmm18, zmm28, {rn-sae}
ins_22c7e8:
    vfnmadd231pd zmm23, zmm18, zmm29, {rn-sae}
ins_22c7ee:
    vfnmadd213pd zmm28, zmm17, zmm22, {rn-sae}
ins_22c7f4:
    vfnmadd213pd zmm29, zmm17, zmm23, {rn-sae}
ins_22c7fa:
    vmulpd zmm25, zmm28, zmm28, {rn-sae}
ins_22c800:
    vmulpd zmm27, zmm29, zmm29, {rn-sae}
ins_22c806:
    vfmadd231pd zmm24, zmm16, zmm25, {rn-sae}
ins_22c80c:
    vfmadd231pd zmm26, zmm16, zmm27, {rn-sae}
ins_22c812:
    vfmadd213pd zmm24, zmm25, zmm4, {rn-sae}
ins_22c818:
    vfmadd213pd zmm26, zmm27, zmm4, {rn-sae}
ins_22c81e:
    vfmadd213pd zmm24, zmm25, zmm3, {rn-sae}
ins_22c824:
    vfmadd213pd zmm26, zmm27, zmm3, {rn-sae}
ins_22c82a:
    vmulpd zmm31, zmm24, zmm25, {rn-sae}
ins_22c830:
    vmulpd zmm11, zmm26, zmm27, {rn-sae}
ins_22c836:
    vfmadd213pd zmm31, zmm28, zmm28, {rn-sae}
ins_22c83c:
    vfmadd213pd zmm11, zmm29, zmm29, {rn-sae}
ins_22c842:
    vcvtpd2ps ymm31, zmm31, {rn-sae}
ins_22c848:
    vcvtpd2ps ymm9, zmm11, {rn-sae}
ins_22c84e:
    vinsertf32x8 zmm12, zmm31, ymm9, 1
ins_22c855:
    vxorps zmm15, zmm12, zmm13
ins_22c85b:
    vpternlogd zmm13, zmm13, zmm13, 0ffh
ins_22c862:
    vpandnd zmm13 {k2}, zmm10, zmm10
ins_22c868:
    vptestmd k0, zmm13, zmm13
ins_22c86e:
    kortestw k0, k0
ins_22c872:
    jne dump_22c294+08a3h
ins_22c878:
    test r14d, r14d
ins_22c87b:
    jne NEAR PTR ins_22c96f
ins_22c881:
    kmovw k1, eax
ins_22c885:
    add ebp, 010h
ins_22c888:
    add r15d, -010h
ins_22c88c:
    vmovups zmmword ptr [rsi + r12*4] {k1}, zmm15
ins_22c893:
    cmp ebp, edi
ins_22c895:
    jb NEAR PTR ins_22c740
ins_22c89b:
    vmovups xmm9, xmmword ptr [rsp + 02e0h]
ins_22c8a4:
    vmovups xmm10, xmmword ptr [rsp + 02f0h]
ins_22c8ad:
    vmovups xmm11, xmmword ptr [rsp + 0300h]
ins_22c8b6:
    vmovups xmm12, xmmword ptr [rsp + 0310h]
ins_22c8bf:
    vmovups xmm13, xmmword ptr [rsp + 0320h]
ins_22c8c8:
    vmovups xmm14, xmmword ptr [rsp + 0330h]
ins_22c8d1:
    vmovups xmm15, xmmword ptr [rsp + 0340h]
ins_22c8da:
    mov eax, dword ptr [rsp + 0368h]
ins_22c8e1:
    mov ecx, dword ptr [rsp + 0358h]
ins_22c8e8:
    mov r9d, dword ptr [rsp + 0360h]
ins_22c8f0:
    fnclex
ins_22c8f2:
    test cl, 1
ins_22c8f5:
    je SHORT ins_22c8fb
ins_22c8f7:
    fldcw word ptr [rsp + 062h]
ins_22c8fb:
    test cl, 2
ins_22c8fe:
    je SHORT ins_22c90d
ins_22c900:
    mov dword ptr [rsp + 064h], r9d
ins_22c905:
    vldmxcsr dword ptr [rsp + 064h]
ins_22c90b:
    jmp SHORT ins_22c929
ins_22c90d:
    vstmxcsr dword ptr [rsp + 064h]
ins_22c913:
    mov edx, dword ptr [rsp + 064h]
ins_22c917:
    test dl, 01fh
ins_22c91a:
    je SHORT ins_22c929
ins_22c91c:
    and edx, 0ffffffe0h
ins_22c91f:
    mov dword ptr [rsp + 064h], edx
ins_22c923:
    vldmxcsr dword ptr [rsp + 064h]
ins_22c929:
    mov rcx, qword ptr [rsp + 0380h]
ins_22c931:
    mov qword ptr [rsp + 0380h], 0
ins_22c93d:
    xor rcx, rsp
ins_22c940:
    cmp rcx, qword ptr [dump_21c7640]
ins_22c947:
    jne SHORT ins_22c966
ins_22c949:
    vzeroupper
ins_22c94c:
    mov r13, qword ptr [rsp + 0370h]
ins_22c954:
    add rsp, 0390h
ins_22c95b:
    pop rbp
ins_22c95c:
    pop r15
ins_22c95e:
    pop r14
ins_22c960:
    pop r12
ins_22c962:
    pop rdi
ins_22c963:
    pop rsi
ins_22c964:
    pop rbx
ins_22c965:
    ret
ins_22c966:
    vzeroupper
ins_22c969:
    call dump_1796c40
ins_22c96e:
    DB 090h
ins_22c96f:
    mov al, byte ptr [rsp + 0350h]
ins_22c976:
    vmovups zmmword ptr [r13 + 080h], zmm14
ins_22c97d:
    vmovups zmmword ptr [r13 + 040h], zmm15
ins_22c984:
    test al, al
ins_22c986:
    je NEAR PTR ins_22cb06
ins_22c98c:
    test r14d, r14d
ins_22c98f:
    jne SHORT ins_22c9a2
ins_22c991:
    vmovups zmm15, zmmword ptr [r13 + 040h]
ins_22c998:
    movzx eax, word ptr [r13]
ins_22c99d:
    jmp NEAR PTR ins_22c881
ins_22c9a2:
    xor eax, eax
ins_22c9a4:
    vmovups xmmword ptr [rsp + 02b0h], xmm6
ins_22c9ad:
    vmovups xmmword ptr [rsp + 02c0h], xmm7
ins_22c9b6:
    vmovups xmmword ptr [rsp + 02d0h], xmm8
ins_22c9bf:
    mov qword ptr [rsp + 048h], r12
ins_22c9c4:
    mov dword ptr [rsp + 050h], r15d
ins_22c9c9:
    mov dword ptr [rsp + 068h], edi
ins_22c9cd:
    DB 089h,0c7h
ins_22c9cf:
    DB 00fh,01fh,084h,000h,000h,000h,000h,000h
ins_22c9d7:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_22c9de:
    DB 066h,090h
ins_22c9e0:
    bt r14d, edi
ins_22c9e4:
    jb NEAR PTR ins_22ca97
ins_22c9ea:
    inc edi
ins_22c9ec:
    cmp edi, 010h
ins_22c9ef:
    jl SHORT ins_22c9e0
ins_22c9f1:
    vmovups zmm0, zmmword ptr [dump_1e50980]
ins_22c9fb:
    vmovups xmm6, xmmword ptr [rsp + 02b0h]
ins_22ca04:
    vmovups xmm7, xmmword ptr [rsp + 02c0h]
ins_22ca0d:
    vmovups xmm8, xmmword ptr [rsp + 02d0h]
ins_22ca16:
    vmovups zmm1, zmmword ptr [dump_1e50cc0]
ins_22ca20:
    vmovups zmm2, zmmword ptr [dump_1e51d40]
ins_22ca2a:
    vmovups zmm21, zmmword ptr [dump_1e51d00]
ins_22ca34:
    vmovups zmm3, zmmword ptr [dump_1e52180]
ins_22ca3e:
    vmovups zmm4, zmmword ptr [dump_1e521c0]
ins_22ca48:
    vmovups zmm5, zmmword ptr [dump_1e52200]
ins_22ca52:
    vmovups zmm16, zmmword ptr [dump_1e52240]
ins_22ca5c:
    vmovups zmm17, zmmword ptr [dump_1e52140]
ins_22ca66:
    vmovups zmm18, zmmword ptr [dump_1e52100]
ins_22ca70:
    vmovups zmm20, zmmword ptr [dump_1e520c0]
ins_22ca7a:
    vmovups zmm19, zmmword ptr [dump_1e51ec0]
ins_22ca84:
    mov r12, qword ptr [rsp + 048h]
ins_22ca89:
    mov r15d, dword ptr [rsp + 050h]
ins_22ca8e:
    mov edi, dword ptr [rsp + 068h]
ins_22ca92:
    jmp NEAR PTR ins_22c991
ins_22ca97:
    vzeroupper
ins_22ca9a:
    lea r12, [r13 + rdi*4 + 040h]
ins_22ca9f:
    DB 04ch,089h,0e2h
ins_22caa2:
    lea rcx, [r13 + rdi*4 + 080h]
ins_22caaa:
    call dump_22c294+0184ch
ins_22caaf:
    test eax, eax
ins_22cab1:
    je NEAR PTR ins_22c9ea
ins_22cab7:
    DB 049h,089h,0e2h
ins_22caba:
    lea r15d, [rbp + rdi]
ins_22cabf:
    mov r11d, dword ptr [r12]
ins_22cac3:
    DB 089h,0c1h
ins_22cac5:
    DB 044h,089h,0fah
ins_22cac8:
    DB 049h,089h,0d8h
ins_22cacb:
    DB 049h,089h,0d9h
ins_22cace:
    mov dword ptr [rsi + r15*4], r11d
ins_22cad2:
    lea r11, [dump_26adfc0]
ins_22cad9:
    mov qword ptr [r10 + 020h], rsi
ins_22cadd:
    mov qword ptr [r10 + 028h], rsi
ins_22cae1:
    mov qword ptr [r10 + 030h], r11
ins_22cae5:
    mov dword ptr [rsp + 040h], eax
ins_22cae9:
    call dump_2d74a0
ins_22caee:
    mov eax, dword ptr [rsp + 040h]
ins_22caf2:
    mov r11d, dword ptr [rsi + r15*4]
ins_22caf6:
    mov dword ptr [r12], r11d
ins_22cafa:
    mov dword ptr [rsp + 0368h], eax
ins_22cb01:
    jmp NEAR PTR ins_22c9ea
ins_22cb06:
    DB 048h,089h,0e0h
ins_22cb09:
    lea rcx, [rsp + 062h]
ins_22cb0e:
    mov byte ptr [rcx + 02eeh], 1
ins_22cb15:
    lea r11, [rsp + 060h]
ins_22cb1a:
    mov qword ptr [rax], rcx
ins_22cb1d:
    mov qword ptr [rax + 8], r11
ins_22cb21:
    mov eax, 03fh
ins_22cb26:
    call dump_22a654+0176ch
ins_22cb2b:
    or dword ptr [rsp + 0358h], eax
ins_22cb32:
    jmp NEAR PTR ins_22c98c
Audio_22c642 ENDP
R2TEXT ENDS
END
