OPTION CASEMAP:NONE
EXTERN dump_2f9a51:PROC
EXTERN dump_2f9aec:PROC
EXTERN dump_2f9b03:PROC
EXTERN dump_1f25040:BYTE
EXTERN dump_1f254c0:BYTE
EXTERN dump_1f25500:BYTE
EXTERN dump_1f25540:BYTE
EXTERN dump_1f25580:BYTE
EXTERN dump_1f25600:BYTE
EXTERN dump_1f25640:BYTE
EXTERN dump_1f25680:BYTE
EXTERN dump_1f256c0:BYTE
EXTERN dump_1f25700:BYTE
.code
PUBLIC Audio_2f9680
PUBLIC dump_2f9680
Audio_2f9680 PROC
dump_2f9680 LABEL NEAR
ins_2f9680:
    endbr64
ins_2f9684:
    push r14
ins_2f9686:
    push r15
ins_2f9688:
    push rbp
ins_2f9689:
    sub rsp, 0120h
ins_2f9690:
    DB 045h,089h,0c1h
ins_2f9693:
    vmovups xmmword ptr [rsp + 0100h], xmm15
ins_2f969c:
    mov rax, 0ffffffe0h
ins_2f96a6:
    vmovups xmmword ptr [rsp + 0f0h], xmm14
ins_2f96af:
    DB 045h,089h,0cbh
ins_2f96b2:
    DB 049h,089h,0d0h
ins_2f96b5:
    vmovups xmmword ptr [rsp + 0e0h], xmm13
ins_2f96be:
    and r11, rax
ins_2f96c1:
    vmovups xmmword ptr [rsp + 0d0h], xmm12
ins_2f96ca:
    xor dl, dl
ins_2f96cc:
    vmovups xmmword ptr [rsp + 0c0h], xmm11
ins_2f96d5:
    vmovups xmmword ptr [rsp + 0b0h], xmm10
ins_2f96de:
    vmovups xmmword ptr [rsp + 0a0h], xmm9
ins_2f96e7:
    vmovups xmmword ptr [rsp + 090h], xmm8
ins_2f96f0:
    vmovups xmmword ptr [rsp + 080h], xmm7
ins_2f96f9:
    vmovups xmmword ptr [rsp + 070h], xmm6
ins_2f96ff:
    mov qword ptr [rsp + 028h], r13
ins_2f9704:
    lea r13, [rsp + 06fh]
ins_2f9709:
    and r13, 0ffffffffffffffc0h
ins_2f970d:
    mov qword ptr [rsp + 0110h], r13
ins_2f9715:
    test r9d, r9d
ins_2f9718:
    jle dump_2f9b03
ins_2f971e:
    test rcx, rcx
ins_2f9721:
    je dump_2f9aec
ins_2f9727:
    test r8, r8
ins_2f972a:
    je dump_2f9aec
ins_2f9730:
    vstmxcsr dword ptr [rsp + 024h]
ins_2f9736:
    mov ebp, dword ptr [rsp + 024h]
ins_2f973a:
    DB 089h,0e8h
ins_2f973c:
    and eax, 0ffc0h
ins_2f9741:
    cmp eax, 01f80h
ins_2f9746:
    je SHORT ins_2f9760
ins_2f9748:
    DB 089h,0e8h
ins_2f974a:
    mov dl, 2
ins_2f974c:
    and eax, 0ffff003fh
ins_2f9751:
    add eax, 01f80h
ins_2f9756:
    mov dword ptr [rsp + 024h], eax
ins_2f975a:
    vldmxcsr dword ptr [rsp + 024h]
ins_2f9760:
    xor eax, eax
ins_2f9762:
    xor r10d, r10d
ins_2f9765:
    test r11d, r11d
ins_2f9768:
    jbe NEAR PTR ins_2f991a
ins_2f976e:
    add r11, 01fh
ins_2f9772:
    shr r11, 5
ins_2f9776:
    vmovups zmm30, zmmword ptr [dump_1f25600]
ins_2f9780:
    vmovups zmm29, zmmword ptr [dump_1f25640]
ins_2f978a:
    vmovups zmm28, zmmword ptr [dump_1f25680]
ins_2f9794:
    vmovups zmm27, zmmword ptr [dump_1f256c0]
ins_2f979e:
    vmovups zmm31, zmmword ptr [dump_1f25700]
ins_2f97a8:
    vmovups zmm26, zmmword ptr [dump_1f25540]
ins_2f97b2:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_2f97b9:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_2f97c0:
    inc eax
ins_2f97c2:
    vmovups zmm9, zmmword ptr [dump_1f25580]
ins_2f97cc:
    lea r14d, [r10 + 010h]
ins_2f97d0:
    vmovups zmm2, zmmword ptr [rcx + r14*4]
ins_2f97d7:
    vmovups zmm12, zmmword ptr [dump_1f254c0]
ins_2f97e1:
    vmovups zmm1, zmmword ptr [rcx + r10*4]
ins_2f97e8:
    vmovups zmm0, zmmword ptr [dump_1f25500]
ins_2f97f2:
    vgetexpps zmm6, zmm2, {sae}
ins_2f97f8:
    vgetmantps zmm4, zmm2, {sae}, 0
ins_2f97ff:
    vgetexpps zmm5, zmm1, {sae}
ins_2f9805:
    vgetmantps zmm3, zmm1, {sae}, 0
ins_2f980c:
    vaddps zmm8, zmm6, zmm6, {rn-sae}
ins_2f9812:
    vaddps zmm7, zmm5, zmm5, {rn-sae}
ins_2f9818:
    vrcp14ps zmm13, zmm3
ins_2f981e:
    vrcp14ps zmm14, zmm4
ins_2f9824:
    vaddps zmm5, zmm7, zmm9, {rn-sae}
ins_2f982a:
    vaddps zmm6, zmm8, zmm9, {rn-sae}
ins_2f9830:
    vrndscaleps zmm13, zmm13, {sae}, 058h
ins_2f9837:
    vrndscaleps zmm14, zmm14, {sae}, 058h
ins_2f983e:
    vpsrld zmm17, zmm13, 013h
ins_2f9845:
    vpsrld zmm18, zmm14, 013h
ins_2f984c:
    vmovaps zmm10, zmm29
ins_2f9852:
    vmovaps zmm11, zmm29
ins_2f9858:
    vfmsub231ps zmm10, zmm30, zmm5, {rn-sae}
ins_2f985e:
    vfmsub231ps zmm11, zmm30, zmm6, {rn-sae}
ins_2f9864:
    vrndscaleps zmm7, zmm10, {sae}, 9
ins_2f986b:
    vrndscaleps zmm8, zmm11, {sae}, 9
ins_2f9872:
    vmovaps zmm9, zmm5
ins_2f9878:
    vmovaps zmm10, zmm6
ins_2f987e:
    vfnmadd231ps zmm9, zmm28, zmm7, {rn-sae}
ins_2f9884:
    vfnmadd231ps zmm10, zmm28, zmm8, {rn-sae}
ins_2f988a:
    vpermps zmm11, zmm9, zmm12
ins_2f9890:
    vpermps zmm12, zmm10, zmm12
ins_2f9896:
    vmovaps zmm15, zmm27
ins_2f989c:
    vmovaps zmm16, zmm27
ins_2f98a2:
    vfmsub231ps zmm15, zmm3, zmm13, {rn-sae}
ins_2f98a8:
    vfmsub231ps zmm16, zmm4, zmm14, {rn-sae}
ins_2f98ae:
    vmulps zmm21, zmm11, zmm15, {rn-sae}
ins_2f98b4:
    vmulps zmm22, zmm12, zmm16, {rn-sae}
ins_2f98ba:
    vmovaps zmm19, zmm0
ins_2f98c0:
    vpermt2ps zmm19, zmm17, zmm26
ins_2f98c6:
    vpermt2ps zmm0, zmm18, zmm26
ins_2f98cc:
    vscalefps zmm19, zmm19, zmm7, {rn-sae}
ins_2f98d2:
    vscalefps zmm20, zmm0, zmm8, {rn-sae}
ins_2f98d8:
    vmovaps zmm23, zmm11
ins_2f98de:
    vmovaps zmm24, zmm12
ins_2f98e4:
    vfmadd231ps zmm23, zmm31, zmm21, {rn-sae}
ins_2f98ea:
    vfmadd231ps zmm24, zmm31, zmm22, {rn-sae}
ins_2f98f0:
    vmulps zmm25, zmm23, zmm19, {rn-sae}
ins_2f98f6:
    vmulps zmm0, zmm24, zmm20, {rn-sae}
ins_2f98fc:
    vmovups zmmword ptr [r8 + r10*4], zmm25
ins_2f9903:
    vmovups zmmword ptr [r8 + r14*4], zmm0
ins_2f990a:
    add r10d, 020h
ins_2f990e:
    cmp eax, r11d
ins_2f9911:
    jb NEAR PTR ins_2f97c0
ins_2f9917:
    shl eax, 5
ins_2f991a:
    DB 041h,089h,0c3h
ins_2f991d:
    neg r11d
ins_2f9920:
    cmp eax, r9d
ins_2f9923:
    jae dump_2f9a51
ins_2f9929:
    vmovups zmm9, zmmword ptr [dump_1f25580]
ins_2f9933:
    mov r10, 0ffffffffh
ins_2f993d:
    vmovups zmm0, zmmword ptr [dump_1f25540]
ins_2f9947:
    vmovups zmm1, zmmword ptr [dump_1f25500]
ins_2f9951:
    vmovups zmm2, zmmword ptr [dump_1f254c0]
ins_2f995b:
    vmovups zmm8, zmmword ptr [dump_1f25600]
ins_2f9965:
    vmovups zmm7, zmmword ptr [dump_1f25640]
ins_2f996f:
    vmovups zmm6, zmmword ptr [dump_1f25680]
ins_2f9979:
    vmovups zmm5, zmmword ptr [dump_1f256c0]
ins_2f9983:
    vmovups zmm4, zmmword ptr [dump_1f25700]
ins_2f998d:
    vmovups zmm3, zmmword ptr [dump_1f25040]
ins_2f9997:
    mov r15d, 010h
ins_2f999d:
    DB 00fh,01fh,000h
ins_2f99a0:
    lea r14d, [r9 + r11]
ins_2f99a4:
    cmp r14d, 010h
ins_2f99a8:
    vmovaps zmm10, zmm3
ins_2f99ae:
    cmovae r14d, r15d
ins_2f99b2:
    add r11d, -010h
ins_2f99b6:
    neg r14d
ins_2f99b9:
    add r14d, 020h
ins_2f99bd:
    vmovaps zmm13, zmm7
ins_2f99c3:
    shrx r14, r10, r14
ins_2f99c8:
    kmovw k1, r14d
ins_2f99cd:
    vmovups zmm10 {k1}, zmmword ptr [rcx + rax*4]
ins_2f99d4:
    vgetexpps zmm11, zmm10, {sae}
ins_2f99da:
    vgetmantps zmm19, zmm10, {sae}, 0
ins_2f99e1:
    vaddps zmm12, zmm11, zmm11, {rn-sae}
ins_2f99e7:
    vrcp14ps zmm15, zmm19
ins_2f99ed:
    vaddps zmm14, zmm12, zmm9, {rn-sae}
ins_2f99f3:
    vrndscaleps zmm16, zmm15, {sae}, 058h
ins_2f99fa:
    vfmsub231ps zmm13, zmm8, zmm14, {rn-sae}
ins_2f9a00:
    vpsrld zmm17, zmm16, 013h
ins_2f9a07:
    vfmsub213ps zmm19, zmm16, zmm5, {rn-sae}
ins_2f9a0d:
    vrndscaleps zmm18, zmm13, {sae}, 9
ins_2f9a14:
    vfnmadd231ps zmm14, zmm6, zmm18, {rn-sae}
ins_2f9a1a:
    vpermi2ps zmm17, zmm1, zmm0
ins_2f9a20:
    vpermps zmm20, zmm14, zmm2
ins_2f9a26:
    vmulps zmm21, zmm20, zmm19, {rn-sae}
ins_2f9a2c:
    vscalefps zmm22, zmm17, zmm18, {rn-sae}
ins_2f9a32:
    vfmadd213ps zmm21, zmm4, zmm20, {rn-sae}
ins_2f9a38:
    vmulps zmm23, zmm21, zmm22, {rn-sae}
ins_2f9a3e:
    vmovups zmmword ptr [r8 + rax*4] {k1}, zmm23
ins_2f9a45:
    add eax, 010h
ins_2f9a48:
    cmp eax, r9d
ins_2f9a4b:
    jb NEAR PTR ins_2f99a0
Audio_2f9680 ENDP
END
