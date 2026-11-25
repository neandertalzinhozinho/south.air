# -*- coding: utf-8 -*-
"""Append spec section 19 (FFT do IPP no audio) to docs/engine/dsp-spec.md."""
from pathlib import Path

ADD = r'''

## 19. FFT do IPP no caminho de áudio — PROVADO (2026-11-23)

> Corrige §5.1: `0x885040` **chama** a FFT (via `0x8B2680`), e a transformada é do IPP.
> `PLANO_MOTOR_AUDIO.md` §24.4 é a folha desta etapa.

### 19.1 Cadeia e RVAs

```
0x885040 00886A69 call 0x8B2680        ; 1 por amostra
0x8B2680 008B28D6 call 0x1010          ; FFT direta   -> 0x199B20E0 (RVA 0x20E0)
         008B2949 call 0x1010          ; 2º caminho
         008B28F6 call 0x1520          ; multiplicação espectral -> 0xBD40
         008B290F call 0x1280          ; FFT inversa  -> 0x199B7B40 (RVA 0x7B40)
         008B2929 call 0x1220          ; escala 1/n   -> 0x6160
```

Resolução dos stubs (leitura direta do dump): `dword [0x21C7408] = 4`;
`[0x21C5D48 + 4*8] = 0x199B20E0`; `[0x21C6088 + 4*8] = 0x199B7B40`.

### 19.2 Desmontagem — par forward/inverse

`0x20E0` e `0x7B40` têm 256 B cada e são o **mesmo wrapper**, exceto duas instruções:

| forward (`0x20E0`) | inverse (`0x7B40`) |
|---|---|
| `0000214A call qword ptr [rcx]` | `00007BAA call qword ptr [rcx+8]` |
| `000021B1 call qword ptr [rax+0x18]` | `00007C12 call qword ptr [rax+0x20]` |

```
// assinatura reconstruida de 0x20E0 (arg1=rcx, arg2=rdx, arg3=r8, arg4=r9)
if (!spec)              return -8;   // 000020F1 / 000021B9
if (spec->magic != 7)   return -13;  // 000020FA / 000020FF
if (!src || !dst)       return -8;   // 00002109 / 00002112
inner = spec->inner;                 // 0000211B
alt   = inner->alt;                  // 0000211F
if (alt && alt->kind == 3)           // 00002128
    return alt->fwd(inner, src, dst, alt->data);   // 000021A7..000021B1
u64 desc[2] = { 0x36, 0 };            // 00002130 / 00002142
return inner->vtbl->fwd(inner, src, dst, desc, buf); // 0000214A
```

### 19.3 Constantes

| RVA | valor |
|---|---|
| `0x20FF` | `0xFFFFFFF3` (−13) |
| `0x21B9` | `0xFFFFFFF8` (−8) |
| `0x2130` | `0x36` |
| `0x8B272F` | `1.0f` lido de `0x2079F9C` |
| `0x8B28AA`/`0x8B28AD` | `shr rdi,1` / `inc rdi` → `bins = n/2+1` |
| `0x8B291C`/`0x8B2925` | `cvtdq2ps n` / `divss` → escala `1/n` |
| `0xBDE0`..`0xBDFD` | `vmovsd` / `vshufps 0xb1` / `vfmaddsub213ps` (par complexo) |

### 19.4 Estruturas

| Objeto | Offset | Prova |
|---|---|---|
| spec | `+0` i32 == 7 | `000020FA` |
| spec | `+8` ptr interno | `0000211B` |
| interno | `+0` vtbl forward | `0000214A` |
| interno | `+8` vtbl inverse | `00007BAA` |
| interno | `+0x18` ptr descritor alt. | `0000211F` |
| alt. | `+0` == 3, `+8` dado, `+0x18` fwd, `+0x20` inv | `00002128`, `000021AD`, `000021B1`, `00007C12` |
| estágio | `+0x18` i32 n | `008B2753` |
| estágio | `+0x140` posição (mask `n/2−1`) | `008B2761` |

### 19.5 Rust

`checks/stage_fft_rust.rs` (compila com `rustc --edition 2021 --crate-type lib`): validação
magic-7, códigos `-13/-8/-2`, slots `[rcx]`/`[rcx+8]`, descritor `0x36`, `bins = n/2+1`,
escala `1/n`, multiplicação complexa interleaved de `0xBD40` na mesma ordem. As borboletas
estão como `unimplemented!` — `NÃO EXTRAÍDO`.

### 19.6 `NÃO PROVADO`

Sabor (RToCCS / RToPerm / RToPack) e construtor da spec (`NÃO EXISTE` store imediato de 7 em
toda a imagem; `tools/find_tag7.py` → 0). Próximo comando em `PLANO_MOTOR_AUDIO.md` §25.
'''

p = Path("docs/engine/dsp-spec.md")
t = p.read_bytes().decode("utf-8")
p.write_bytes((t.rstrip() + ADD).encode("utf-8"))
print("ok", len(t) + len(ADD))
