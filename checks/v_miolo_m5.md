# M5 — miolo `0x8B3ED0` (e motor inteiro) por tradução mecânica x86-64 → Rust

> **Estado em 2026-11-25:** em andamento. Este arquivo é o registro vivo de M5. O resumo fica
> no `PLANO_MOTOR_AUDIO.md` §26.

## 1. Método (por que tradução mecânica)

O miolo `0x8B3ED0` tem 4.473 instruções e 127 `call`. Dentro do cluster DSP, o fecho de
chamadas dele chega a 42 funções e cerca de 8,5 mil instruções. Somadas as primitivas da IPP
(stubs + impls), são cerca de 24 mil.

O motor completo, a partir das entradas da API (`create` `0x862E40`, setter `0x862EF0`,
`process` `0x862F00`→`0x864410` e `0x862F10/0x862F40/0x863020/0x863070`), tem **388 funções e
cerca de 110 mil instruções** (FFT incluída).

Transcrever isso à mão não é verificável. A regra do projeto ("mesma aritmética, mesma ordem,
mesmos coeficientes, com RVA") se cumpre literalmente com um **tradutor mecânico**:

- `tools/lift/lift.py` desmonta o dump com capstone, por **descida recursiva**, porque há funções
  partidas em fragmentos `.pdata` com `UNW_FLAG_CHAININFO`. Cada função vira uma `fn` Rust com
  blocos básicos num `match pc`, **uma linha por instrução**, com o RVA e o texto da instrução
  em comentário.
- As instruções não suportadas viram `panic!("NÃO SUPORTADO <RVA> ...")`, e nada é estimado. Elas
  só param o programa se forem executadas.
- O runtime está em `port/src/lifted/rt.rs`:
  - registradores, xmm/ymm (128 + metade alta), flags e memória paginada;
  - a imagem fica na base `0x199B0000` e é lida sob demanda do dump (só leitura, com
    copy-on-write para `.data`);
  - o heap é um bump allocator;
  - as operações float usam **intrinsics SSE/FMA do hardware**, então o MXCSR vale como no
    binário; `ldmxcsr`/`vldmxcsr` escrevem o MXCSR real.
- Folhas sem tradução ficam em `port/src/lifted/leaf.rs`: CRT, cópia/zero de bytes, `__chkstk`
  e imports. Cada assinatura foi conferida no dump.
- Os alvos indiretos ficam assim:
  - stubs IPP (`movsxd rax,[idx]; lea r10,[tab]; jmp [r10+rax*8]`) e `jmp/call [rip+p]` são
    resolvidos pelo dump **só para decidir o que traduzir**; em tempo de execução, o despacho lê
    a memória emulada (`call_va`);
  - `call [IAT]` vira `leaf::import(slot)`.

## 2. Validação do tradutor (bit a bit contra kernels provados à mão)

O arquivo é `port/src/lifted/tests.rs` (`cargo test --release --lib lifted`), com 3 testes, todos
verdes:

| Função traduzida | Comparada com | Casos |
|---|---|---|
| `0x1550` → `0x63640` (divisão, caminhos AVX `vrcpps`+FMA) | `div::div_block_mod32` (M1) | n ∈ {1,7,8,9,16,17,31,32,33,257,513} × offset dst {0,4,12,28} |
| `0x1C8500`/`0x1C84A0`/`0x1C8530` (ln/exp/rcp) | `ippmath` (M3), `rcp` (M2) | n ∈ {1,5,8,15,16,17,33,100,257} |
| `0x8C3C20` (smoother, descritor `0x410`) | `engine::smoother_fwd_back` (J6) | (count,len) ∈ {(1,1),(1,2),(3,17),(5,257),(8,64)} |

## 3. Folhas com handler (leaf.rs) — assinaturas conferidas

- `0x17978C0`: `__chkstk`, sem efeito em valores.
- `0x1796910`: falha de cookie; o binário termina, e o port faz `panic`.
- `0x1798F36` → IAT `0x1D8D590`: `memcpy(dst=rcx, src=rdx, n=r8)`.
- `0x1798F42` → `0x1D8D580`: `memset(rcx, edx, r8)`.
- `0x1D2EB40`, `0x1D2EF40`, `0x699C0`: cópia com **`src = rcx`, `dst = rdx`**, `n = r8`
  (bytes). Provas: `01D2EB42 mov rdi,rcx` + `01D2EB67 vmovdqu ymm0,[rdi]`; `000699D2`;
  `01D2EF52..55`. O `0x699C0` consulta a CPU (`0x2FB900`, `cpuid`) só para escolher o caminho
  temporal ou não-temporal.
- `0x1D2E9E0`, `0x1D2F0C0`: zera `(dst = rcx, n = rdx)`.
- Math da UCRT: `powf 0x1C9AA01`, `logf 0x1C9A9FB`, `expf 0x1C9A9D7`, `pow 0x1C9A5AD`,
  `exp 0x1C9A9D1`, `log 0x1C9A9EF`.

## 4. Pendente para rodar o motor inteiro (`gen_engine.rs`)

- **Instruções** (280 ocorrências, quase todas nas FFTs): `vmovhpd`, `vcvtps2pd`, `vmovsldup`,
  `vmovshdup`, `vpsrlq`, `vmovntdq`, `vaddsubps`, `vpsubq`, `vpsllq`, `vpermps`, `vmaxpd`,
  `vcvtpd2ps`, `vfmaddsub213ps`, `vfmadd132pd`, `vfmsub213pd`, `vcmpnlt_uqps`, `vcmpnle_uqps`,
  `vunpckhpd`, `vfmsub132pd`, `vpbroadcastd`, `vfmadd213pd`, `movntps`, `vhaddpd`,
  `unpcklpd`, `rcpps`, além do AVX-512 do caminho alternativo.
- **Regiões a incluir:** `0x85E6C0` (escritor de descritores, etapa C), `0x56B140`, `0x6B7F00`
  e o interno da IPP em `0x1D2xxxx`/`0x1D4E1C0`/`0x1D66F60`.
- **Folhas de runtime:**
  - imports: `malloc` `0x1D8D730`, `free` `0x1D8D738`, `_aligned_free` `0x1D8D750`,
    `_aligned_malloc` `0x1D8D758`, e os slots `0x1D8D7E8`, `0x1D8D830`, `0x1D8D900`;
  - `0x1796CF4` (`operator new`?), `0x1796930`/`0x1796974`/`0x17969E0`, `0x1797578`/`0x17975CC`;
  - CRT: `roundf 0x1798F8A`, `log10f 0x1C9A5A1`, `cos 0x1C9A9C5`, `log2 0x1C9A9F5`,
    `tan 0x1C9AA13`, `0x1C9A5E0`;
  - helpers do plugin `0x314FE0`/`0x328990`/`0x329020`/`0x3290A0`/`0x32B810`.
- **Interface do host no `create`:** o `rdx` de `0x862E40`/`0x8634A0` é uma tabela de callbacks
  (`[r15+0x18]` registra saídas nomeadas como `"reduction_curve_freq_points_lo"`), e o `process`
  faz chamadas virtuais (`call r8`, `call [rax+0x20]`). É preciso provar se algum valor devolvido
  entra no áudio; se não entra, o handler é inerte.
- **Seleção do índice de CPU:** a tabela `[0x21C7408]` = 4 vem do dump. O emulador lê esse mesmo
  valor, o que vale para a CPU do oráculo.
