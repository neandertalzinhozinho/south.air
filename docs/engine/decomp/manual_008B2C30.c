// manual_008B2C30.c — pseudocódigo escrito à mão a partir da DESMONTAGEM.
//
// Hex-Rays NÃO entrega esta função: `ida_008B2C30.c` contém apenas
//   void sub_1808B2C30() { JUMPOUT(0x1808B2C35LL); }
// porque o .pdata parte a função em 0x8B2BCE (8 B), 0x8B2BD6 (83 B),
// 0x8B2C30 (37 B) e 0x8B2C55 (578 B) e o decompiler entra pelo fragmento.
//
// Fonte de cada linha: checks/8b2c30.dis (show_func.py, chain-aware,
// 0x8B2C30..0x8B30BB = 1163 B, 301 instruções). Não há inferência
// arquitetural aqui: só tradução instrução -> C. RWAs entre parênteses.
//
// Convenção Win64: rcx=arg1, xmm1=arg2 (float), r8=arg3. rdx/r9 não são lidos.
//
//   float fir32_scatter(Fir32* S, float x, const float* K);

typedef unsigned long long u64;

typedef struct {
    float buf[32];   // +0x00  (008B2C7C mov ... [rcx+rax*4] / 008B2C81 store)
    u64   pos;       // +0x80  (008B30AD store de (p+1)&0x1f)
} Fir32;

float fir32_scatter(Fir32 *S, float x, const float *K)
{
    u64 p = S->pos;              // 008B2C40  mov rax,[rcx+0x80]
    unsigned j;

    // 008B2C4F  xor r9d,r9d            -> 0.0f (nao -0.0f)
    // 008B2C62  mulss xmm6,[r8]        -> x * K[0]
    // 008B2C7C  addss xmm6,[rcx+rax*4] -> + S->buf[p]
    float y = x * K[0] + S->buf[p];

    // 008B2C81  mov [rcx+rax*4],r9d
    S->buf[p] = 0.0f;

    // 008B2C85  sub rbx,[rcx+0x80]     -> rbx = 31 - p
    // 008B2CA1  and rdx,~3              -> desenrola 4x, depois 16x (mulps), depois resto
    for (j = 1; j <= 31 - p; ++j)               // 008B2CD0 .. 008B2E7E
        S->buf[p + j] = S->buf[p + j] + x * K[j];   // mulss ; addss ; movss

    // 008B2E8A  cmp [rcx+0x80],r9 ; 008B2E91 je 0x8B308F
    if (p != 0) {
        // 008B2EA5  lea r10,[r14+r10*4] com r10 = 32-p  -> K[32-p]
        for (j = 0; j < p; ++j)                 // 008B2EE0 .. 008B308D
            S->buf[j] = S->buf[j] + x * K[32 - p + j];
    }

    // 008B308F  mov rax,[rcx+0x80]
    // 008B3096  movaps xmm0,xmm6        -> retorno
    // 008B30A6  and eax,0x1f
    // 008B30AD  mov [rcx+0x80],rax
    S->pos = (p + 1) & 0x1f;
    return y;
}

// Semantica: y[n] = sum_{m=0..31} K^(n-m)[m] * x[n-m]
//   FIR de 32 taps, coeficientes variantes no tempo, scatter-add em anel.
//   Nao ha subss em nenhum caminho (scan_region.py) -> nao e media movel,
//   nao e delay, nao e allpass.
