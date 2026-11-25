OPTION CASEMAP:NONE
EXTERN dump_2fad37:PROC
EXTERN dump_2fadd2:PROC
EXTERN dump_2fade9:PROC
EXTERN dump_1f26780:BYTE
EXTERN dump_1f267c0:BYTE
EXTERN dump_1f26800:BYTE
EXTERN dump_1f26840:BYTE
EXTERN dump_1f26880:BYTE
EXTERN dump_1f268c0:BYTE
EXTERN dump_1f26900:BYTE
EXTERN dump_1f26940:BYTE
EXTERN dump_1f26980:BYTE
EXTERN dump_1f269c0:BYTE
EXTERN dump_1f26a00:BYTE
.code
PUBLIC Audio_2fa940
PUBLIC dump_2fa940
Audio_2fa940 PROC
dump_2fa940 LABEL NEAR
ins_2fa940:
    endbr64
ins_2fa944:
    push r14
ins_2fa946:
    push r15
ins_2fa948:
    push rbp
ins_2fa949:
    sub rsp, 0120h
ins_2fa950:
    DB 045h,089h,0c1h
ins_2fa953:
    vmovups xmmword ptr [rsp + 0100h], xmm15
ins_2fa95c:
    mov rax, 0ffffffe0h
ins_2fa966:
    vmovups xmmword ptr [rsp + 0f0h], xmm14
ins_2fa96f:
    DB 045h,089h,0cbh
ins_2fa972:
    DB 049h,089h,0d0h
ins_2fa975:
    vmovups xmmword ptr [rsp + 0e0h], xmm13
ins_2fa97e:
    and r11, rax
ins_2fa981:
    vmovups xmmword ptr [rsp + 0d0h], xmm12
ins_2fa98a:
    xor dl, dl
ins_2fa98c:
    vmovups xmmword ptr [rsp + 0c0h], xmm11
ins_2fa995:
    vmovups xmmword ptr [rsp + 0b0h], xmm10
ins_2fa99e:
    vmovups xmmword ptr [rsp + 0a0h], xmm9
ins_2fa9a7:
    vmovups xmmword ptr [rsp + 090h], xmm8
ins_2fa9b0:
    vmovups xmmword ptr [rsp + 080h], xmm7
ins_2fa9b9:
    vmovups xmmword ptr [rsp + 070h], xmm6
ins_2fa9bf:
    mov qword ptr [rsp + 028h], r13
ins_2fa9c4:
    lea r13, [rsp + 06fh]
ins_2fa9c9:
    and r13, 0ffffffffffffffc0h
ins_2fa9cd:
    mov qword ptr [rsp + 0110h], r13
ins_2fa9d5:
    test r9d, r9d
ins_2fa9d8:
    jle dump_2fade9
ins_2fa9de:
    test rcx, rcx
ins_2fa9e1:
    je dump_2fadd2
ins_2fa9e7:
    test r8, r8
ins_2fa9ea:
    je dump_2fadd2
ins_2fa9f0:
    vstmxcsr dword ptr [rsp + 024h]
ins_2fa9f6:
    mov ebp, dword ptr [rsp + 024h]
ins_2fa9fa:
    DB 089h,0e8h
ins_2fa9fc:
    and eax, 0ffc0h
ins_2faa01:
    cmp eax, 01f80h
ins_2faa06:
    je SHORT ins_2faa20
ins_2faa08:
    DB 089h,0e8h
ins_2faa0a:
    mov dl, 2
ins_2faa0c:
    and eax, 0ffff003fh
ins_2faa11:
    add eax, 01f80h
ins_2faa16:
    mov dword ptr [rsp + 024h], eax
ins_2faa1a:
    vldmxcsr dword ptr [rsp + 024h]
ins_2faa20:
    xor eax, eax
ins_2faa22:
    xor r10d, r10d
ins_2faa25:
    test r11d, r11d
ins_2faa28:
    jbe NEAR PTR ins_2fabe4
ins_2faa2e:
    add r11, 01fh
ins_2faa32:
    shr r11, 5
ins_2faa36:
    vmovups zmm30, zmmword ptr [dump_1f26900]
ins_2faa40:
    vmovups zmm29, zmmword ptr [dump_1f26980]
ins_2faa4a:
    vmovups zmm31, zmmword ptr [dump_1f269c0]
ins_2faa54:
    vmovups zmm28, zmmword ptr [dump_1f26800]
ins_2faa5e:
    DB 066h,090h
ins_2faa60:
    inc eax
ins_2faa62:
    vmovups zmm7, zmmword ptr [dump_1f26880]
ins_2faa6c:
    lea r14d, [r10 + 010h]
ins_2faa70:
    vmovups zmm2, zmmword ptr [rcx + r14*4]
ins_2faa77:
    vmovups zmm10, zmmword ptr [dump_1f26940]
ins_2faa81:
    vmovups zmm1, zmmword ptr [rcx + r10*4]
ins_2faa88:
    vmovups zmm14, zmmword ptr [dump_1f267c0]
ins_2faa92:
    vmovups zmm21, zmmword ptr [dump_1f26840]
ins_2faa9c:
    vgetexpps zmm6, zmm2, {sae}
ins_2faaa2:
    vgetmantps zmm4, zmm2, {sae}, 0
ins_2faaa9:
    vgetexpps zmm5, zmm1, {sae}
ins_2faaaf:
    vgetmantps zmm3, zmm1, {sae}, 0
ins_2faab6:
    vmovups zmm25, zmmword ptr [dump_1f26a00]
ins_2faac0:
    vmovups zmm8, zmmword ptr [dump_1f268c0]
ins_2faaca:
    vrcp14ps zmm16, zmm4
ins_2faad0:
    vrcp14ps zmm15, zmm3
ins_2faad6:
    vaddps zmm5, zmm5, zmm7, {rn-sae}
ins_2faadc:
    vaddps zmm6, zmm6, zmm7, {rn-sae}
ins_2faae2:
    vandps zmm7, zmm1, zmm8
ins_2faae8:
    vandps zmm8, zmm2, zmm8
ins_2faaee:
    vrndscaleps zmm15, zmm15, {sae}, 058h
ins_2faaf5:
    vrndscaleps zmm16, zmm16, {sae}, 058h
ins_2faafc:
    vpsrld zmm19, zmm15, 013h
ins_2fab03:
    vpsrld zmm20, zmm16, 013h
ins_2fab0a:
    vmovaps zmm9, zmm10
ins_2fab10:
    vfmsub231ps zmm9, zmm30, zmm5, {rn-sae}
ins_2fab16:
    vfmsub231ps zmm10, zmm30, zmm6, {rn-sae}
ins_2fab1c:
    vrndscaleps zmm9, zmm9, {sae}, 9
ins_2fab23:
    vrndscaleps zmm10, zmm10, {sae}, 9
ins_2fab2a:
    vmovaps zmm11, zmm5
ins_2fab30:
    vmovaps zmm12, zmm6
ins_2fab36:
    vfnmadd231ps zmm11, zmm29, zmm9, {rn-sae}
ins_2fab3c:
    vfnmadd231ps zmm12, zmm29, zmm10, {rn-sae}
ins_2fab42:
    vpermps zmm13, zmm11, zmm14
ins_2fab48:
    vpermps zmm14, zmm12, zmm14
ins_2fab4e:
    vmovaps zmm17, zmm31
ins_2fab54:
    vmovaps zmm18, zmm31
ins_2fab5a:
    vfmsub231ps zmm17, zmm3, zmm15, {rn-sae}
ins_2fab60:
    vfmsub231ps zmm18, zmm4, zmm16, {rn-sae}
ins_2fab66:
    vmovaps zmm23, zmm28
ins_2fab6c:
    vmovaps zmm24, zmm28
ins_2fab72:
    vpermt2ps zmm23, zmm19, zmm21
ins_2fab78:
    vpermt2ps zmm24, zmm20, zmm21
ins_2fab7e:
    vmulps zmm21, zmm13, zmm17, {rn-sae}
ins_2fab84:
    vmulps zmm22, zmm14, zmm18, {rn-sae}
ins_2fab8a:
    vscalefps zmm23, zmm23, zmm9, {rn-sae}
ins_2fab90:
    vscalefps zmm24, zmm24, zmm10, {rn-sae}
ins_2fab96:
    vmovaps zmm0, zmm13
ins_2fab9c:
    vmovaps zmm26, zmm14
ins_2faba2:
    vfmadd231ps zmm0, zmm25, zmm21, {rn-sae}
ins_2faba8:
    vfmadd231ps zmm26, zmm25, zmm22, {rn-sae}
ins_2fabae:
    vmulps zmm25, zmm0, zmm23, {rn-sae}
ins_2fabb4:
    vmulps zmm26, zmm26, zmm24, {rn-sae}
ins_2fabba:
    vorps zmm27, zmm25, zmm7
ins_2fabc0:
    vorps zmm0, zmm26, zmm8
ins_2fabc6:
    vmovups zmmword ptr [r8 + r10*4], zmm27
ins_2fabcd:
    vmovups zmmword ptr [r8 + r14*4], zmm0
ins_2fabd4:
    add r10d, 020h
ins_2fabd8:
    cmp eax, r11d
ins_2fabdb:
    jb NEAR PTR ins_2faa60
ins_2fabe1:
    shl eax, 5
ins_2fabe4:
    DB 041h,089h,0c3h
ins_2fabe7:
    neg r11d
ins_2fabea:
    cmp eax, r9d
ins_2fabed:
    jae dump_2fad37
ins_2fabf3:
    vmovups zmm10, zmmword ptr [dump_1f26880]
ins_2fabfd:
    mov r10, 0ffffffffh
ins_2fac07:
    vmovups zmm9, zmmword ptr [dump_1f268c0]
ins_2fac11:
    vmovups zmm8, zmmword ptr [dump_1f26900]
ins_2fac1b:
    vmovups zmm7, zmmword ptr [dump_1f26940]
ins_2fac25:
    vmovups zmm6, zmmword ptr [dump_1f26980]
ins_2fac2f:
    vmovups zmm4, zmmword ptr [dump_1f269c0]
ins_2fac39:
    vmovups zmm3, zmmword ptr [dump_1f26a00]
ins_2fac43:
    vmovups zmm5, zmmword ptr [dump_1f267c0]
ins_2fac4d:
    vmovups zmm1, zmmword ptr [dump_1f26800]
ins_2fac57:
    vmovups zmm0, zmmword ptr [dump_1f26840]
ins_2fac61:
    vmovups zmm2, zmmword ptr [dump_1f26780]
ins_2fac6b:
    mov r15d, 010h
ins_2fac71:
    DB 00fh,01fh,084h,000h,000h,000h,000h,000h
ins_2fac79:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_2fac80:
    lea r14d, [r9 + r11]
ins_2fac84:
    cmp r14d, 010h
ins_2fac88:
    vmovaps zmm12, zmm2
ins_2fac8e:
    cmovae r14d, r15d
ins_2fac92:
    add r11d, -010h
ins_2fac96:
    neg r14d
ins_2fac99:
    add r14d, 020h
ins_2fac9d:
    vmovaps zmm13, zmm7
ins_2faca3:
    shrx r14, r10, r14
ins_2faca8:
    kmovw k1, r14d
ins_2facad:
    vmovups zmm12 {k1}, zmmword ptr [rcx + rax*4]
ins_2facb4:
    vgetexpps zmm11, zmm12, {sae}
ins_2facba:
    vgetmantps zmm17, zmm12, {sae}, 0
ins_2facc1:
    vrcp14ps zmm15, zmm17
ins_2facc7:
    vaddps zmm14, zmm11, zmm10, {rn-sae}
ins_2faccd:
    vandps zmm24, zmm12, zmm9
ins_2facd3:
    vrndscaleps zmm16, zmm15, {sae}, 058h
ins_2facda:
    vfmsub231ps zmm13, zmm8, zmm14, {rn-sae}
ins_2face0:
    vpsrld zmm18, zmm16, 013h
ins_2face7:
    vrndscaleps zmm19, zmm13, {sae}, 9
ins_2facee:
    vfmsub213ps zmm17, zmm16, zmm4, {rn-sae}
ins_2facf4:
    vfnmadd231ps zmm14, zmm6, zmm19, {rn-sae}
ins_2facfa:
    vpermps zmm20, zmm14, zmm5
ins_2fad00:
    vpermi2ps zmm18, zmm1, zmm0
ins_2fad06:
    vmulps zmm21, zmm20, zmm17, {rn-sae}
ins_2fad0c:
    vscalefps zmm22, zmm18, zmm19, {rn-sae}
ins_2fad12:
    vfmadd213ps zmm21, zmm3, zmm20, {rn-sae}
ins_2fad18:
    vmulps zmm23, zmm21, zmm22, {rn-sae}
ins_2fad1e:
    vorps zmm25, zmm23, zmm24
ins_2fad24:
    vmovups zmmword ptr [r8 + rax*4] {k1}, zmm25
ins_2fad2b:
    add eax, 010h
ins_2fad2e:
    cmp eax, r9d
ins_2fad31:
    jb NEAR PTR ins_2fac80
Audio_2fa940 ENDP
END
