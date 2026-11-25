// manual_008CAE90.c — pseudocódigo escrito à mão a partir da DESMONTAGEM.
// Fonte: checks/8cae90.dis (show_func.py, chain-aware, 0x8CAE90..0x8CAFC3,
// 307 B, 80 linhas). Todo RVA abaixo veio da desmontagem; nada inferido de nome.
//
// Chamador provado: 0x8C02F0 chama 2x — 0x8C099C e 0x8C0AE5.
//   chamada 1: rcx=[rbp+0x340] (Set16), rdx=[rbp+0xB60] (Set128),
//              r8=[rsp+0x30]  (Set16)
//   chamada 2: rcx=[rsp+0x30]  (Set16), rdx=[rbp+0xB60] (Set128),
//              r8=[rbp+0x340] (Set16)
// Prova: 008C0917 / 008C0921 / 008C092B e 008C0A76 / 008C0A82 / 008C0A8C.
//
// Convenção Win64: rcx=arg1, rdx=arg2, r8=arg3.

typedef struct {
    float *ptr[16];   // +0x00..+0x7F : 16 ponteiros, passo 8 (008CAF03 lea rbx,[rbx+8])
    int    n;         // +0x80 : movsxd rbp,[rcx+0x80] (008CAEC8), cmp (008CAEB1/008CAEC0)
    int    len;       // +0x84 : mov r14d,[rcx+0x84] (008CAED8) -> r9d
} Set16;              // 0x88 bytes

typedef struct {
    float *ptr[128];  // +0x00..+0x3FF : passo 8 (008CAF52 lea rdi,[rdi+8])
    int    n;         // +0x400 : mov eax,[rdx+0x400] (008CAEA2), cmp 1 (008CAF12)
} Set128;             // 0x404 bytes

// 0x1580 -> 0xCCE0 (tabela 0x21C6488[4], seletor 0x21C7408=4) -> 0x65EA0 -> 0x6CE80.
// 0x6CE80: 0006CEAF vmovups ymm1,[rcx] / 0006CEB7 vmovups ymm0,[rdx]
//          0006CEBB vfmadd213ps ymm1,ymm0,[r8] / 0006CEC4 vmovups [r8],ymm1
// Ou seja: dst(r8)[k] = src1(rcx)[k]*src2(rdx)[k] + dst(r8)[k]   [MAC in place]
// Variante escalar 0xC620 (tabela[0]): 0000C6A0 movss [rcx] / 0000C6A5 mulss [rsi]
// / 0000C6AA addss [r8] / 0000C6B0 movss [r8]. Confirma a ordem dos operandos.
void mac_set16_by_set128(Set16 *dst, Set128 *a, Set16 *b)
{
    int i;
    int n;
    int len;

    // 008CAEA2 mov eax,[rdx+0x400]           a->n
    // 008CAEB1 cmp [rcx+0x80],eax ; jne 8CAF12
    // 008CAEB9 mov eax,[r8+0x80]             b->n
    // 008CAEC0 cmp [rcx+0x80],eax ; jne 8CAF12
    if (dst->n == a->n && dst->n == b->n) {
        n = dst->n;                          // 008CAEC8 movsxd rbp,[rcx+0x80]
        if (n <= 0) goto fim;                // 008CAECF test rbp,rbp ; jle 008CAFB0
        len = dst->len;                      // 008CAED8 mov r14d,[rcx+0x84]
        // 008CAEDF sub rsi,rbx / 008CAEE2 sub rdi,rbx  (indexação por rbx)
        for (i = 0; i < n; ++i)              // 008CAEF0..008CAF0B
            mac(a->ptr[i], b->ptr[i], dst->ptr[i], len);   // 008CAEFE
        goto fim;                            // 008CAF0D jmp 008CAFB0
    }

    // 008CAF12 cmp [rdx+0x400],1 ; jle 008CAF65
    if (a->n > 1) {
        // 008CAF1B cmp [r8+0x80],1 ; jne 008CAF5E
        if (b->n == 1) {                     // broadcast de b, a completo
            n = dst->n;                      // 008CAF25 movsxd rbp,[rcx+0x80]
            if (n <= 0) goto fim;            // 008CAF2F test rbp,rbp ; jle 008CAFB0
            len = dst->len;                  // 008CAF31 mov r14d,[rcx+0x84]
            // 008CAF3B rbx = b->ptr[0] (fixo); 008CAF38 sub rsi,rdi
            for (i = 0; i < n; ++i)          // 008CAF40..008CAF5A
                mac(a->ptr[i], b->ptr[0], dst->ptr[i], len);  // 008CAF4D
        }
        // 008CAF5E: a->n == 1 ?  -> falso aqui (a->n > 1) => retorno em 008CAF65
        goto fim;
    }

    // 008CAF5E cmp [rdx+0x400],1 ; 008CAF65 jne 008CAFB0  -> exige a->n == 1
    // 008CAF67 cmp [r8+0x80],1   ; 008CAF6F jne 008CAFB0  -> exige b->n == 1
    if (a->n != 1 || b->n != 1) goto fim;
    // 008CAF71 movsxd r14,[rcx+0x80] ; n = dst->n
    n = dst->n;
    if (n <= 0) goto fim;                    // 008CAF7A test r14,r14 ; jle 008CAFB0
    // 008CAF7F rbx = b->ptr[0]; 008CAF82 rdi = a->ptr[0]
    // 008CAF8A r15d = dst->len
    for (i = 0; i < n; ++i)                  // 008CAF91..008CFA9, i em rbp
        mac(a->ptr[0], b->ptr[0], dst->ptr[i], len);  // 008CAF9E

fim:
    return;                                  // 008CAFB0..008CAFC2
}

// ordem provada em 0x6CE80: rcx=src1, rdx=src2, r8=dst/acumulador, r9d=len.
// A operação é dst + src1*src2, NÃO dst + src1 + src2.
extern void mac(float *src1, float *src2, float *dst_acc, int len);

// Nenhuma constante float nesta função: `show_func.py 0x8CAE90 | findstr rip`
// devolve 0 linhas. A única constante é imediata: 1 (008CAF12, 008CAF1B,
// 008CAF5E, 008CAF65, 008CAF6F), usada para detectar broadcast.
