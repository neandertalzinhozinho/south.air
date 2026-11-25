//! Folhas não traduzidas: CRT, cópia/zero de bytes e `__chkstk`.
//!
//! Convenção: o chamador traduzido já empilhou o endereço de retorno
//! (`c.push(ret)`); o handler faz o efeito e desempilha (equivale a `ret`).
//! Toda assinatura abaixo foi conferida no dump. Prova em
//! `checks/v_miolo_m5.md` §3.

use super::rt::*;

fn ret(c: &mut Cpu) {
    c.r[RSP] = c.r[RSP].wrapping_add(8);
}

fn copy_bytes(c: &mut Cpu, src: u64, dst: u64, n: u64) {
    let mut buf = vec![0u8; n as usize];
    c.mem.read(src, &mut buf);
    c.mem.write(dst, &buf);
}

fn xmm0_f32(c: &Cpu) -> f32 {
    f32::from_bits(c.x[0] as u32)
}
fn xmm1_f32(c: &Cpu) -> f32 {
    f32::from_bits(c.x[1] as u32)
}
fn xmm0_f64(c: &Cpu) -> f64 {
    f64::from_bits(c.x[0] as u64)
}
fn xmm1_f64(c: &Cpu) -> f64 {
    f64::from_bits(c.x[1] as u64)
}

pub fn call(c: &mut Cpu, rva: u32) {
    match rva {
        // _Init_thread_header (`0x17969E0`, lido em checks/w_cadeia_m6.md §3). O dump é uma foto
        // do processo em execução: os guards de estáticos já estão marcados e os objetos apontam
        // para o heap do processo original, que não existe aqui. Na primeira vez que cada guard
        // aparece nesta emulação, força o caminho de inicialização (`*guard = -1`, como
        // `017969FB or dword [rbx], -1` faz com guard 0), para o estático ser reconstruído
        // como num processo novo. O footer `0x1796974` segue traduzido.
        0x17969E0 => {
            let g = c.r[RCX];
            if c.static_guards.insert(g) {
                c.mem.w32(g, 0xFFFF_FFFF);
            }
            ret(c)
        }
        // __chkstk (`0x17978C0`): só toca páginas da pilha; sem efeito em valores.
        0x17978C0 => ret(c),
        // __security_check_cookie falhou (`0x1796910`): no binário, termina o processo.
        0x1796910 => panic!("cookie de pilha corrompido (0x1796910)"),
        // memcpy (`0x1798F36` -> IAT 0x1D8D590, VCRUNTIME140): rcx=dst, rdx=src, r8=n.
        0x1798F36 => {
            let (d, s, n) = (c.r[RCX], c.r[RDX], c.r[R8]);
            copy_bytes(c, s, d, n);
            c.r[RAX] = d;
            ret(c)
        }
        // memset (`0x1798F42` -> IAT 0x1D8D580): rcx=dst, edx=valor, r8=n.
        0x1798F42 => {
            let (d, v, n) = (c.r[RCX], c.r[RDX] as u8, c.r[R8]);
            c.mem.write(d, &vec![v; n as usize]);
            c.r[RAX] = d;
            ret(c)
        }
        // Cópias da IPP: src=rcx, dst=rdx, n=r8 (bytes).
        // 0x1D2EB40 (`01D2EB42 mov rdi,rcx` é a ORIGEM: `01D2EB67 vmovdqu ymm0,[rdi]`),
        // 0x699C0 (`000699D2 mov ebx,r8d`, chamado por 0x26540 com os mesmos rcx/rdx/r8),
        // 0x1D2EF40 (`01D2EF52..01D2EF55` troca: rsi=rcx origem, rdi=rdx destino).
        0x1D2EB40 | 0x1D2EF40 => {
            let (s, d, n) = (c.r[RCX], c.r[RDX], (c.r[R8] as u32 as i32) as i64);
            if n > 0 {
                copy_bytes(c, s, d, n as u64);
            }
            ret(c)
        }
        0x699C0 => {
            let (s, d, n) = (c.r[RCX], c.r[RDX], (c.r[R8] as u32 as i32) as i64);
            if n > 0 {
                copy_bytes(c, s, d, n as u64);
            }
            ret(c)
        }
        // Zero-fill: dst=rcx, n=rdx (bytes). 0x1D2E9E0 (`01D2E9EB movsxd rsi,esi`,
        // `01D2E9EE vxorps`), 0x1D2F0C0 (`01D2F0CC movsxd rcx,esi`, `rep stosb` com al=0).
        0x1D2E9E0 | 0x1D2F0C0 => {
            let (d, n) = (c.r[RCX], (c.r[RDX] as u32 as i32) as i64);
            if n > 0 {
                c.mem.write(d, &vec![0u8; n as usize]);
            }
            ret(c)
        }
        // Math da UCRT (checks/thunk_map.txt; f32 provados contra os imports em
        // checks/j_crt_equiv.rs; f64 chamam a mesma UCRT no x86_64-pc-windows-msvc).
        0x1C9AA01 => {
            let v = xmm0_f32(c).powf(xmm1_f32(c)); // powf
            c.x[0] = v.to_bits() as u128;
            ret(c)
        }
        0x1C9A9FB => {
            let v = xmm0_f32(c).ln(); // logf
            c.x[0] = v.to_bits() as u128;
            ret(c)
        }
        0x1C9A9D7 => {
            let v = xmm0_f32(c).exp(); // expf
            c.x[0] = v.to_bits() as u128;
            ret(c)
        }
        0x1C9A5AD => {
            let v = xmm0_f64(c).powf(xmm1_f64(c)); // pow (double)
            c.x[0] = v.to_bits() as u128;
            ret(c)
        }
        0x1C9A9D1 => {
            let v = xmm0_f64(c).exp(); // exp (double)
            c.x[0] = v.to_bits() as u128;
            ret(c)
        }
        0x1C9A9EF => {
            let v = xmm0_f64(c).ln(); // log (double)
            c.x[0] = v.to_bits() as u128;
            ret(c)
        }
        _ => panic!("folha sem tradução nem handler: RVA 0x{rva:X}"),
    }
}

/// Import chamado por slot de IAT (`call [IAT]` ou thunk `jmp [IAT]`). O nome vem dos
/// descritores de import do dump (`gen_engine::import_name`). O chamador já empilhou o
/// retorno; aqui o handler faz o efeito e desempilha.
pub fn import(c: &mut Cpu, slot: u32) {
    let name = super::gen_engine::import_name(slot)
        .or_else(|| super::EXTRA_IMPORT.get().and_then(|x| x(slot)))
        .unwrap_or_else(|| panic!("import sem nome: slot 0x{slot:X}"));
    let f0 = f32::from_bits(c.x[0] as u32);
    let f1 = f32::from_bits(c.x[1] as u32);
    let d0 = f64::from_bits(c.x[0] as u64);
    let d1 = f64::from_bits(c.x[1] as u64);
    let set_f = |c: &mut Cpu, v: f32| c.x[0] = v.to_bits() as u128;
    let set_d = |c: &mut Cpu, v: f64| c.x[0] = v.to_bits() as u128;
    match name {
        // Sincronização: a emulação roda em uma thread só.
        "AcquireSRWLockExclusive" | "ReleaseSRWLockExclusive" | "WakeAllConditionVariable" => {}
        "SleepConditionVariableSRW" => panic!("SleepConditionVariableSRW: esperaria outra thread"),
        "_register_onexit_function" | "_crt_atexit" => c.r[RAX] = 0,
        "_callnewh" => c.r[RAX] = 0,
        "?_Xlength_error@std@@YAXPEBD@Z" | "_CxxThrowException" | "_invalid_parameter_noinfo_noreturn" => {
            panic!("exceção C++/CRT ({name}) no código traduzido")
        }
        // Heap: bump allocator (free não reaproveita; o conteúdo é o mesmo).
        "malloc" => {
            let n = c.r[RCX];
            c.r[RAX] = c.mem.alloc(n);
        }
        "_aligned_malloc" => {
            let (n, al) = (c.r[RCX], c.r[RDX].max(1));
            let a = c.mem.alloc(n + al);
            c.r[RAX] = (a + al - 1) / al * al;
        }
        "free" | "_aligned_free" => {}
        "memcpy" | "memmove" => {
            let (d, s, n) = (c.r[RCX], c.r[RDX], c.r[R8]);
            copy_bytes(c, s, d, n);
            c.r[RAX] = d;
        }
        "memset" => {
            let (d, v, n) = (c.r[RCX], c.r[RDX] as u8, c.r[R8]);
            c.mem.write(d, &vec![v; n as usize]);
            c.r[RAX] = d;
        }
        // Math da UCRT: no x86_64-pc-windows-msvc o std chama as mesmas funções
        // (f32 provado em checks/j_crt_equiv.rs); round/lround são exatos por definição.
        "powf" => set_f(c, f0.powf(f1)),
        "logf" => set_f(c, f0.ln()),
        "expf" => set_f(c, f0.exp()),
        "log10f" => set_f(c, f0.log10()),
        "roundf" => set_f(c, f0.round()),
        "pow" => set_d(c, d0.powf(d1)),
        "exp" => set_d(c, d0.exp()),
        "log" => set_d(c, d0.ln()),
        "log2" => set_d(c, d0.log2()),
        "exp2" => set_d(c, d0.exp2()),
        "cos" => set_d(c, d0.cos()),
        "tan" => set_d(c, d0.tan()),
        "lround" => c.r[RAX] = d0.round() as i32 as u32 as u64,
        "round" => set_d(c, d0.round()),
        "floor" => set_d(c, d0.floor()),
        "ceil" => set_d(c, d0.ceil()),
        "floorf" => set_f(c, f0.floor()),
        "ceilf" => set_f(c, f0.ceil()),
        "sqrt" => set_d(c, d0.sqrt()),
        "sqrtf" => set_f(c, f0.sqrt()),
        "fmod" => set_d(c, d0 % d1),
        "fmodf" => set_f(c, f0 % f1),
        "sin" => set_d(c, d0.sin()),
        "sinf" => set_f(c, f0.sin()),
        "cosf" => set_f(c, f0.cos()),
        "tanf" => set_f(c, f0.tan()),
        "atan" => set_d(c, d0.atan()),
        "atanf" => set_f(c, f0.atan()),
        "atan2" => set_d(c, d0.atan2(d1)),
        "atan2f" => set_f(c, f0.atan2(f1)),
        "asinh" => set_d(c, d0.asinh()),
        "asinhf" => set_f(c, f0.asinh()),
        "sinh" => set_d(c, d0.sinh()),
        "cosh" => set_d(c, d0.cosh()),
        "tanh" => set_d(c, d0.tanh()),
        "tanhf" => set_f(c, f0.tanh()),
        "log10" => set_d(c, d0.log10()),
        "log2f" => set_f(c, f0.log2()),
        "exp2f" => set_f(c, f0.exp2()),
        "log1p" => set_d(c, d0.ln_1p()),
        "expm1" => set_d(c, d0.exp_m1()),
        "hypot" => set_d(c, d0.hypot(d1)),
        "lroundf" => c.r[RAX] = f0.round() as i32 as u32 as u64,
        _ => panic!("import {name} (slot 0x{slot:X}) sem handler"),
    }
    ret(c)
}
