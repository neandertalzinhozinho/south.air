OPTION CASEMAP:NONE
EXTERN dump_23bc8d:PROC
EXTERN dump_23bd27:PROC
EXTERN dump_23bf0a:PROC
EXTERN dump_23c046:PROC
EXTERN dump_23c08a:PROC
EXTERN dump_23c0ac:PROC
EXTERN dump_1e6b800:BYTE
EXTERN dump_21c7640:BYTE
.code
PUBLIC Audio_23ba20
PUBLIC dump_23ba20
Audio_23ba20 PROC
dump_23ba20 LABEL NEAR
ins_23ba20:
    endbr64
ins_23ba24:
    push rbx
ins_23ba25:
    push rsi
ins_23ba26:
    push rdi
ins_23ba27:
    push r12
ins_23ba29:
    push r14
ins_23ba2b:
    push r15
ins_23ba2d:
    push rbp
ins_23ba2e:
    sub rsp, 0350h
ins_23ba35:
    DB 045h,089h,0c7h
ins_23ba38:
    mov qword ptr [rsp + 0330h], r13
ins_23ba40:
    lea r13, [rsp + 014fh]
ins_23ba48:
    and r13, 0ffffffffffffffc0h
ins_23ba4c:
    xor r9d, r9d
ins_23ba4f:
    mov qword ptr [rsp + 0338h], r13
ins_23ba57:
    and r15d, 0ffffffe0h
ins_23ba5b:
    mov rax, qword ptr [dump_21c7640]
ins_23ba62:
    DB 049h,089h,0cbh
ins_23ba65:
    xor rax, rsp
ins_23ba68:
    xor r10b, r10b
ins_23ba6b:
    mov qword ptr [rsp + 0340h], rax
ins_23ba73:
    xor eax, eax
ins_23ba75:
    test r8d, r8d
ins_23ba78:
    jle dump_23c0ac
ins_23ba7e:
    test r11, r11
ins_23ba81:
    je dump_23c08a
ins_23ba87:
    test rdx, rdx
ins_23ba8a:
    je dump_23c046
ins_23ba90:
    vstmxcsr dword ptr [rsp + 0104h]
ins_23ba99:
    mov ecx, dword ptr [rsp + 0104h]
ins_23baa0:
    DB 089h,0cdh
ins_23baa2:
    and ebp, 0ffc0h
ins_23baa8:
    cmp ebp, 01f80h
ins_23baae:
    je SHORT ins_23bad4
ins_23bab0:
    DB 089h,0cdh
ins_23bab2:
    mov r9d, 2
ins_23bab8:
    and ebp, 0ffff003fh
ins_23babe:
    add ebp, 01f80h
ins_23bac4:
    mov dword ptr [rsp + 0104h], ebp
ins_23bacb:
    vldmxcsr dword ptr [rsp + 0104h]
ins_23bad4:
    xor ebp, ebp
ins_23bad6:
    test r15d, r15d
ins_23bad9:
    je NEAR PTR ins_23bbbc
ins_23badf:
    mov dword ptr [rsp + 0310h], ecx
ins_23bae6:
    DB 048h,089h,0d6h
ins_23bae9:
    mov dword ptr [rsp + 0328h], eax
ins_23baf0:
    DB 04ch,089h,0dbh
ins_23baf3:
    mov dword ptr [rsp + 0318h], r9d
ins_23bafb:
    mov byte ptr [rsp + 0320h], r10b
ins_23bb03:
    mov dword ptr [rsp + 0108h], r8d
ins_23bb0b:
    DB 00fh,01fh,084h,000h,000h,000h,000h,000h
ins_23bb13:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_23bb1a:
    DB 066h,00fh,01fh,044h,000h,000h
ins_23bb20:
    DB 089h,0efh
ins_23bb22:
    lea r12d, [rbp + 010h]
ins_23bb26:
    vmovups zmm3, zmmword ptr [rbx + r12*4]
ins_23bb2d:
    vmovups zmm2, zmmword ptr [rbx + rdi*4]
ins_23bb34:
    vrsqrt14ps zmm0, zmm3
ins_23bb3a:
    vrsqrt14ps zmm1, zmm2
ins_23bb40:
    vmulps zmm0, zmm0, zmm3, {rn-sae}
ins_23bb46:
    vmulps zmm1, zmm1, zmm2, {rn-sae}
ins_23bb4c:
    vfpclassps k2, zmm3, 05eh
ins_23bb53:
    vfpclassps k1, zmm2, 05eh
ins_23bb5a:
    kmovw eax, k2
ins_23bb5e:
    kmovw r14d, k1
ins_23bb62:
    vorps zmm1 {k1}, zmm2, zmm2
ins_23bb68:
    vorps zmm0 {k2}, zmm3, zmm3
ins_23bb6e:
    shl eax, 010h
ins_23bb71:
    or r14d, eax
ins_23bb74:
    jne dump_23bf0a
ins_23bb7a:
    add ebp, 020h
ins_23bb7d:
    vmovups zmmword ptr [rsi + rdi*4], zmm1
ins_23bb84:
    vmovups zmmword ptr [rsi + r12*4], zmm0
ins_23bb8b:
    cmp ebp, r15d
ins_23bb8e:
    jb SHORT ins_23bb20
ins_23bb90:
    mov ecx, dword ptr [rsp + 0310h]
ins_23bb97:
    DB 049h,089h,0dbh
ins_23bb9a:
    mov eax, dword ptr [rsp + 0328h]
ins_23bba1:
    DB 048h,089h,0f2h
ins_23bba4:
    mov r9d, dword ptr [rsp + 0318h]
ins_23bbac:
    mov r10b, byte ptr [rsp + 0320h]
ins_23bbb4:
    mov r8d, dword ptr [rsp + 0108h]
ins_23bbbc:
    DB 041h,089h,0efh
ins_23bbbf:
    neg r15d
ins_23bbc2:
    cmp ebp, r8d
ins_23bbc5:
    jae dump_23bc8d
ins_23bbcb:
    vmovups zmm0, zmmword ptr [dump_1e6b800]
ins_23bbd5:
    DB 048h,089h,0d6h
ins_23bbd8:
    mov dword ptr [rsp + 0310h], ecx
ins_23bbdf:
    DB 044h,089h,0c7h
ins_23bbe2:
    mov dword ptr [rsp + 0328h], eax
ins_23bbe9:
    DB 04ch,089h,0dbh
ins_23bbec:
    mov dword ptr [rsp + 0318h], r9d
ins_23bbf4:
    mov byte ptr [rsp + 0320h], r10b
ins_23bbfc:
    DB 00fh,01fh,040h,000h
ins_23bc00:
    mov eax, 010h
ins_23bc05:
    lea ecx, [rdi + r15]
ins_23bc09:
    cmp ecx, 010h
ins_23bc0c:
    mov r10, 0ffffffffh
ins_23bc16:
    DB 041h,089h,0ech
ins_23bc19:
    cmovae ecx, eax
ins_23bc1c:
    neg ecx
ins_23bc1e:
    add ecx, 020h
ins_23bc21:
    shrx rax, r10, rcx
ins_23bc26:
    mov dword ptr [r13], eax
ins_23bc2a:
    kmovw k1, eax
ins_23bc2e:
    vmovaps zmm2, zmm0
ins_23bc34:
    vmovups zmm2 {k1}, zmmword ptr [rbx + r12*4]
ins_23bc3b:
    vrsqrt14ps zmm1, zmm2
ins_23bc41:
    vfpclassps k2, zmm2, 05eh
ins_23bc48:
    vmulps zmm1, zmm1, zmm2, {rn-sae}
ins_23bc4e:
    kmovw r14d, k2
ins_23bc52:
    vorps zmm1 {k2}, zmm2, zmm2
ins_23bc58:
    test r14d, r14d
ins_23bc5b:
    jne dump_23bd27
ins_23bc61:
    kmovw k1, eax
ins_23bc65:
    add ebp, 010h
ins_23bc68:
    add r15d, -010h
ins_23bc6c:
    vmovups zmmword ptr [rsi + r12*4] {k1}, zmm1
ins_23bc73:
    cmp ebp, edi
ins_23bc75:
    jb SHORT ins_23bc00
ins_23bc77:
    mov ecx, dword ptr [rsp + 0310h]
ins_23bc7e:
    mov eax, dword ptr [rsp + 0328h]
ins_23bc85:
    mov r9d, dword ptr [rsp + 0318h]
Audio_23ba20 ENDP
END
