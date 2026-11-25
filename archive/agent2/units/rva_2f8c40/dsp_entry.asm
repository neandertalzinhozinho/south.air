OPTION CASEMAP:NONE
EXTERN dump_2f8f17:PROC
EXTERN dump_2f8fad:PROC
EXTERN dump_2f91a6:PROC
EXTERN dump_2f937a:PROC
EXTERN dump_2f93be:PROC
EXTERN dump_2f93e0:PROC
EXTERN dump_1f24a80:BYTE
EXTERN dump_1f24ac0:BYTE
EXTERN dump_1f24b00:BYTE
EXTERN dump_21c7640:BYTE
.code
PUBLIC Audio_2f8c40
PUBLIC dump_2f8c40
Audio_2f8c40 PROC
dump_2f8c40 LABEL NEAR
ins_2f8c40:
    endbr64
ins_2f8c44:
    push rbx
ins_2f8c45:
    push rsi
ins_2f8c46:
    push rdi
ins_2f8c47:
    push r12
ins_2f8c49:
    push r14
ins_2f8c4b:
    push r15
ins_2f8c4d:
    push rbp
ins_2f8c4e:
    sub rsp, 02c0h
ins_2f8c55:
    DB 049h,089h,0cbh
ins_2f8c58:
    mov qword ptr [rsp + 02a8h], r13
ins_2f8c60:
    lea r13, [rsp + 013fh]
ins_2f8c68:
    and r13, 0ffffffffffffffc0h
ins_2f8c6c:
    xor ecx, ecx
ins_2f8c6e:
    mov qword ptr [rsp + 02b0h], r13
ins_2f8c76:
    xor r14b, r14b
ins_2f8c79:
    mov rax, qword ptr [dump_21c7640]
ins_2f8c80:
    xor r9d, r9d
ins_2f8c83:
    xor rax, rsp
ins_2f8c86:
    mov qword ptr [rsp + 02b8h], rax
ins_2f8c8e:
    DB 044h,089h,0c0h
ins_2f8c91:
    and eax, 0fffffff0h
ins_2f8c94:
    test r8d, r8d
ins_2f8c97:
    jle dump_2f93e0
ins_2f8c9d:
    test r11, r11
ins_2f8ca0:
    je dump_2f93be
ins_2f8ca6:
    test rdx, rdx
ins_2f8ca9:
    je dump_2f937a
ins_2f8caf:
    vstmxcsr dword ptr [rsp + 0fch]
ins_2f8cb8:
    mov r10d, dword ptr [rsp + 0fch]
ins_2f8cc0:
    DB 045h,089h,0d7h
ins_2f8cc3:
    and r15d, 0ffc0h
ins_2f8cca:
    cmp r15d, 01f80h
ins_2f8cd1:
    je SHORT ins_2f8cf7
ins_2f8cd3:
    DB 044h,089h,0d1h
ins_2f8cd6:
    and ecx, 0ffff003fh
ins_2f8cdc:
    add ecx, 01f80h
ins_2f8ce2:
    mov dword ptr [rsp + 0fch], ecx
ins_2f8ce9:
    mov ecx, 2
ins_2f8cee:
    vldmxcsr dword ptr [rsp + 0fch]
ins_2f8cf7:
    xor ebp, ebp
ins_2f8cf9:
    xor r15d, r15d
ins_2f8cfc:
    test eax, eax
ins_2f8cfe:
    je NEAR PTR ins_2f8df0
ins_2f8d04:
    vmovups zmm3, zmmword ptr [dump_1f24ac0]
ins_2f8d0e:
    DB 089h,0c7h
ins_2f8d10:
    vmovups zmm2, zmmword ptr [dump_1f24b00]
ins_2f8d1a:
    vpternlogd zmm1, zmm1, zmm1, 0ffh
ins_2f8d21:
    mov dword ptr [rsp + 02a0h], r9d
ins_2f8d29:
    DB 048h,089h,0d6h
ins_2f8d2c:
    mov dword ptr [rsp + 0290h], ecx
ins_2f8d33:
    DB 04ch,089h,0dbh
ins_2f8d36:
    mov dword ptr [rsp + 0298h], r10d
ins_2f8d3e:
    mov dword ptr [rsp + 0288h], r8d
ins_2f8d46:
    DB 00fh,01fh,084h,000h,000h,000h,000h,000h
ins_2f8d4e:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_2f8d55:
    DB 00fh,01fh,040h,000h
ins_2f8d59:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_2f8d60:
    vmovups zmm18, zmmword ptr [rbx + rbp*4]
ins_2f8d67:
    vrsqrt14ps zmm16, zmm18
ins_2f8d6d:
    vpcmpnltd k1, zmm18, zmm3
ins_2f8d74:
    vpcmpled k2, zmm18, zmm2
ins_2f8d7b:
    vmulps zmm17, zmm18, zmm16, {rn-sae}
ins_2f8d81:
    vmovaps zmm0, zmm1
ins_2f8d87:
    vmovaps zmm4, zmm1
ins_2f8d8d:
    vpandnd zmm0 {k1}, zmm18, zmm18
ins_2f8d93:
    vpandnd zmm4 {k2}, zmm18, zmm18
ins_2f8d99:
    vpord zmm5, zmm0, zmm4
ins_2f8d9f:
    vptestmd k0, zmm5, zmm5
ins_2f8da5:
    vmulps zmm0, zmm17, zmm18, {rn-sae}
ins_2f8dab:
    kmovw r12d, k0
ins_2f8daf:
    test r12d, r12d
ins_2f8db2:
    jne dump_2f91a6
ins_2f8db8:
    add r15d, 010h
ins_2f8dbc:
    vmovups zmmword ptr [rsi + rbp*4], zmm0
ins_2f8dc3:
    DB 044h,089h,0fdh
ins_2f8dc6:
    cmp r15d, edi
ins_2f8dc9:
    jb SHORT ins_2f8d60
ins_2f8dcb:
    mov r9d, dword ptr [rsp + 02a0h]
ins_2f8dd3:
    DB 049h,089h,0dbh
ins_2f8dd6:
    mov ecx, dword ptr [rsp + 0290h]
ins_2f8ddd:
    DB 048h,089h,0f2h
ins_2f8de0:
    mov r10d, dword ptr [rsp + 0298h]
ins_2f8de8:
    mov r8d, dword ptr [rsp + 0288h]
ins_2f8df0:
    cmp r15d, r8d
ins_2f8df3:
    jae dump_2f8f17
ins_2f8df9:
    mov rax, 0ffffffffh
ins_2f8e03:
    DB 048h,089h,0d6h
ins_2f8e06:
    vmovups zmm3, zmmword ptr [dump_1f24ac0]
ins_2f8e10:
    DB 048h,089h,0c7h
ins_2f8e13:
    vmovups zmm2, zmmword ptr [dump_1f24b00]
ins_2f8e1d:
    vmovups zmm1, zmmword ptr [dump_1f24a80]
ins_2f8e27:
    vpternlogd zmm0, zmm0, zmm0, 0ffh
ins_2f8e2e:
    mov byte ptr [rsp + 0280h], r14b
ins_2f8e36:
    DB 049h,089h,0ech
ins_2f8e39:
    mov dword ptr [rsp + 02a0h], r9d
ins_2f8e41:
    DB 044h,089h,0c5h
ins_2f8e44:
    mov dword ptr [rsp + 0290h], ecx
ins_2f8e4b:
    DB 04ch,089h,0dbh
ins_2f8e4e:
    mov dword ptr [rsp + 0298h], r10d
ins_2f8e56:
    DB 00fh,01fh,000h
ins_2f8e59:
    DB 00fh,01fh,080h,000h,000h,000h,000h
ins_2f8e60:
    DB 041h,089h,0eah
ins_2f8e63:
    mov ecx, 010h
ins_2f8e68:
    sub r10d, r15d
ins_2f8e6b:
    cmp r10d, 010h
ins_2f8e6f:
    vmovaps zmm19, zmm1
ins_2f8e75:
    cmovae r10d, ecx
ins_2f8e79:
    neg r10d
ins_2f8e7c:
    add r10d, 020h
ins_2f8e80:
    shrx rcx, rdi, r10
ins_2f8e85:
    mov dword ptr [r13], ecx
ins_2f8e89:
    kmovw k1, ecx
ins_2f8e8d:
    vmovups zmm19 {k1}, zmmword ptr [rbx + r12*4]
ins_2f8e94:
    vrsqrt14ps zmm17, zmm19
ins_2f8e9a:
    vpcmpnltd k2, zmm19, zmm3
ins_2f8ea1:
    vpcmpled k3, zmm19, zmm2
ins_2f8ea8:
    vmulps zmm18, zmm19, zmm17, {rn-sae}
ins_2f8eae:
    vmovaps zmm4, zmm0
ins_2f8eb4:
    vmovaps zmm5, zmm0
ins_2f8eba:
    vpandnd zmm4 {k2}, zmm19, zmm19
ins_2f8ec0:
    vpandnd zmm5 {k3}, zmm19, zmm19
ins_2f8ec6:
    vpord zmm16, zmm4, zmm5
ins_2f8ecc:
    vmulps zmm4, zmm18, zmm19, {rn-sae}
ins_2f8ed2:
    vptestmd k0, zmm16, zmm16
ins_2f8ed8:
    kmovw r14d, k0
ins_2f8edc:
    test r14d, r14d
ins_2f8edf:
    jne dump_2f8fad
ins_2f8ee5:
    kmovw k1, ecx
ins_2f8ee9:
    add r15d, 010h
ins_2f8eed:
    vmovups zmmword ptr [rsi + r12*4] {k1}, zmm4
ins_2f8ef4:
    DB 045h,089h,0fch
ins_2f8ef7:
    cmp r15d, ebp
ins_2f8efa:
    jb NEAR PTR ins_2f8e60
ins_2f8f00:
    mov r9d, dword ptr [rsp + 02a0h]
ins_2f8f08:
    mov ecx, dword ptr [rsp + 0290h]
ins_2f8f0f:
    mov r10d, dword ptr [rsp + 0298h]
Audio_2f8c40 ENDP
END
