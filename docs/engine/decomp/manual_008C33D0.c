// IDA 9.3 nao entregou Hex-Rays para 0x8C33D0 (ida_008C33D0.c so tem o cabecalho).
// Pseudocódigo manual lido de checks/8c33d0.dis (show_func.py, 519 linhas, 0x8C33D0..0x8C3C14).
// Convenção: cada bloco cita o RVA da instrução que o prova. Nomes a1/a2/sao neutros (NAO inventados).
// NÃO PROVADO: a origem de [rbp+0x740]/[rbp+0x744] no primeiro trecho (leitura em 008C34BD/008C34C7
// antes da escrita em 008C371A/008C3724); pode ser estado do chamador ou trecho emendado.

void __fastcall sub_8C33D0(a1 /*rcx*/, a2 /*rdx*/, float xmm2, float xmm3, Arena *arena /*[rbp+0xff0]*/)
{
    // 008C33D0..008C33F2: prólogo; __chkstk(0x1090); frame = 0x1090
    // 008C33F5: arena = [rbp+0xff0]  (5º argumento, via stack)
    // 008C3419: rbx = a2 ; 008C3423: r13 = a1
    // 008C341C/008C341F: xmm6 = xmm3 ; xmm7 = xmm2
    // 008C3422/008C3429: saved_pos = arena->pos ([r15+0x18])

    // ---- bloco 1: copia 8 blocos de 0x80 B (1024 B = 256 floats) de a2 -> local[rbp+0x340]
    // 008C340B: r14d = 8 ; 008C3440..008C3495: 8× (8×movups de 16 B + lea +0x80)
    for (k = 0; k < 8; k++) copy_128_bytes(local_340 + k*0x80, a2 + k*0x80);

    // 008C34A0..008C34B8: memset(&local[rbp+0x758], 0, 0x3f8)   [call 0x1798f42]
    // 008C34A7: qword [rbp+0x750] = 0

    // ---- bloco 2: lê contadores e aloca n blocos alinhados na arena
    // 008C34BD: rsi = (int)[rbp+0x744] ; 008C34C7: r12 = (int)[rbp+0x740]
    n = r12; m = rsi;
    for (i = 0; i < n; i++) {                       // 008C34EE..008C352B
        off = arena->pos;                            // 008C34EE: edx = [r15+0x18]
        ptrs[i] = arena->base + 4*off;               // 008C34F2/008C34F8: rax + rcx*4
        off2 = off + m;                              // 008C34FC: lea eax,[rdx+rsi]
        // alinhamento a 16 floats: 008C3510 and eax,0xf; 008C3513 sub; 008C3516 add 0x10;
        // 008C351A test cl,0xf; 008C351D cmove rdx,rcx
        arena->pos = align16(off + m);               // 008C3524: mov [r15+0x18],edx
    }

    // ---- bloco 3: copia a1 (128 B) -> [rsp+0x30], a2 (8×128 B) -> [rbp+0xb60],
    //      e os ponteiros alocados (8×128 B) -> [rbp+0x340]
    // 008C353A..008C35F6 (a1), 008C35A0..008C3600 (a2), 008C3610..008C3666 (ptrs)
    // 008C354E: xmm2 = [a1+0x80] ; 008C3669: movd eax,xmm2  -> cntA = (int)[a1+0x80]

    if (n == cntA) {                                 // 008C366D cmp r12d,eax / 008C3670 jne
        for (j = 0; j < n; j++)                       // 008C3680: rbx = j*8
            prim_11C0(A[j], B[j], ptrs[j], m);        // 008C3698 call 0x11c0  (dst = b - a)
    } else if (cntA == 1 && n > 0) {
        for (j = 0; j < n; j++)
            prim_11C0(A[0], B[j], ptrs[j], m);        // 008C36D6 call 0x11c0 (broadcast A[0])
    }

    // ---- bloco 4: mesma alocação alinhada em [rbp+0x340], agora para a saída
    // 008C36EB..008C3788: memset(&local[rbp+0x348], 0, 0x3f8); 008C371A/3724/372A escrevem
    //   [rbp+0x740]=n, [rbp+0x744]=m, [rbp+0x748]=4*m
    // 008C377A/3781: r15d=m, r10d=n

    // ---- bloco 5: usa as primitivas B provadas em §17.6
    // 008C3880: rdx=ptrs2[j], xmm3=0, rcx=A[j], r8d=m, [rsp+0x20]=4, 008C389B call 0x1250
    //   -> modo 4 = min(src, 0)  (§17.6: 0x69C0 modo 4)
    // 008C3930: rcx=ptrs2[j], r9d=0, xmm2=0, edx=m, 008C393B call 0x1100
    //   -> modo 0 = max(bound, dst)  (§17.6: 0x3480 modo 0)
    // 008C3A30: rcx=ptrs2[j], r9d=[rbp-0x4c], r8=A[j], xmm1=xmm7, 008C3A43 call 0x11F0
    //   -> dst = escalar*A + dst, escalar = antigo xmm2 (§17.6: 0x5BC0)
    // 008C3B80: mesmo 0x11F0 com xmm1=xmm6 (antigo xmm3)

    // ---- epílogo 008C3BDF..008C3C14: restaura arena->pos = saved_pos (008C3C02), ret
}

// Constantes com RVA:
//   8        008C340B (contador de blocos de 0x80 B)
//   0x80     008C3440/008C35AE (passo de bloco)   | 0x3f8  008C34B2/008C3702 (memset)
//   0xf/0x10 008C3510/008C3516 (alinhamento 16 floats)
//   4        008C3893 [rsp+0x20] (modo min de 0x1250)
//   0        008C3885 xorps xmm3 / 008C3926 xorps xmm2 / 008C3933 xor r9d (modo max de 0x1100)
//   1/2      008C3A54/008C36A9 (contagem de bandas em cntA)
