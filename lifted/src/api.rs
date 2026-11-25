//! M6 — o motor traduzido usado pela API que o plugin chama.
//!
//! Prova das assinaturas: `checks/w_cadeia_m6.md`.
//!
//! - `create = 0x862E40(rcx = iface do host, rdx = config, xmm2 = (double)taxa)`. Devolve o
//!   handle `{[0] = engine, [+8] = 0x862EF0, [+0x10] = 0x862F00, ...}` (`00862E5D..00862EE1`).
//!   - **Config:** é estática, `0x23923E0` (campo `+0x18` do descritor `0x23926F0`); medida no
//!     oráculo (`SOULTREE_PROBE`).
//!   - **Iface do host:** funções em `+0x18` (registra saída com nome; retorno ignorado,
//!     `00863577..`), `+0x20` (envia dados de saída) e `+0x28` (saída habilitada?), que no
//!     plugin é `0x338BA0` = `[[iface]+0x94]`, **medido 0** no oráculo. Logo o motor não chama
//!     `+0x20` (`00866730..00866735`). O stub devolve 0.
//! - `process = 0x862F00(handle, rdx = entradas, r8 = saídas, r9 = 0, [rsp+0x28] = n)`:
//!   - `0x862F00` faz `mov rcx,[rcx]` e `jmp 0x864410`;
//!   - com `r9 = 0`, a saída é o array de `r8` (`008645FE..0086462D`).
//! - `set = 0x862EF0(handle, rdx = entrada 0x238E9C0 + i·0x68, xmm2 = (double)norm)` (M4).

use super::rt::*;

/// VAs sentinela das funções do iface do host (além do fim do dump, dentro da janela da imagem).
pub const HOST_FN_BASE: u64 = IMAGE_BASE + 0x82F_0000;
pub const HOST_FN_REGISTER: u64 = HOST_FN_BASE; // iface+0x18
pub const HOST_FN_SEND: u64 = HOST_FN_BASE + 0x10; // iface+0x20
pub const HOST_FN_ENABLED: u64 = HOST_FN_BASE + 0x20; // iface+0x28

/// Número de chamadas a iface+0x20 (diagnóstico).
pub static SENDS: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);

/// Trata uma chamada indireta a um VA sentinela; `true` se tratou.
pub fn host_call(c: &mut Cpu, va: u64, site: u32) -> bool {
    match va {
        HOST_FN_REGISTER => {
            c.r[RAX] = 0;
        }
        HOST_FN_SEND => {
            // 0x338A80 no plugin: copia os dados para buffers de visualização do plugin; nada
            // volta ao motor. Em 0x863690 (create) o motor envia o valor inicial 0 da saída 13
            // sem consultar +0x28. Aqui é inerte; só conta.
            let _ = site;
            SENDS.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        }
        HOST_FN_ENABLED => {
            c.r[RAX] = 0; // 0x338BA0: movzx eax, byte [[iface]+0x94] = 0 (medido)
        }
        _ => return false,
    }
    c.r[RSP] = c.r[RSP].wrapping_add(8); // ret
    true
}

pub struct Engine {
    pub cpu: Cpu,
    pub handle: u64,
    pub n_in: usize,
    pub n_out: usize,
    bufs: Option<(u64, u64, u64, u64, usize)>, // (in_arr, out_arr, in_data, out_data, cap)
}

impl Engine {
    /// `create` com a taxa `fs` (como o plugin passa: double).
    pub fn new(mut cpu: Cpu, fs: f64) -> Engine {
        let iface_obj = cpu.mem.alloc(0x100); // [iface] (objeto do plugin; +0x94 = 0)
        let iface = cpu.mem.alloc(0x40);
        cpu.mem.w64(iface, iface_obj);
        cpu.mem.w64(iface + 0x18, HOST_FN_REGISTER);
        cpu.mem.w64(iface + 0x20, HOST_FN_SEND);
        cpu.mem.w64(iface + 0x28, HOST_FN_ENABLED);
        cpu.r[RCX] = iface;
        cpu.r[RDX] = IMAGE_BASE + 0x23923E0;
        cpu.x[2] = fs.to_bits() as u128;
        call_abi(&mut cpu, 0x862E40, &[]);
        let handle = cpu.r[RAX];
        let eng = cpu.mem.r64(handle);
        let n_in = cpu.mem.r32(eng + 0x10) as usize;
        let n_out = cpu.mem.r32(eng + 0x14) as usize;
        Engine { cpu, handle, n_in, n_out, bufs: None }
    }

    pub fn engine_ptr(&mut self) -> u64 {
        self.cpu.mem.r64(self.handle)
    }

    /// Setter M4: `0x862EF0(handle, entrada i, (double)norm)`.
    pub fn set_param(&mut self, i: usize, norm: f64) {
        self.cpu.r[RCX] = self.handle;
        self.cpu.r[RDX] = IMAGE_BASE + 0x238E9C0 + 0x68 * i as u64;
        self.cpu.x[2] = norm.to_bits() as u128;
        call_abi(&mut self.cpu, 0x862EF0, &[]);
    }

    /// Um bloco: `inputs[ch][n]` -> `outputs[ch][n]`.
    pub fn process(&mut self, inputs: &[&[f32]], outputs: &mut [&mut [f32]]) {
        let n = inputs[0].len();
        let need = n.max(1);
        let (ia, oa, idata, odata) = match self.bufs {
            Some((ia, oa, id, od, cap)) if cap >= need => (ia, oa, id, od),
            _ => {
                let ia = self.cpu.mem.alloc(8 * 16);
                let oa = self.cpu.mem.alloc(8 * 16);
                let id = self.cpu.mem.alloc((4 * need * 16) as u64);
                let od = self.cpu.mem.alloc((4 * need * 16) as u64);
                self.bufs = Some((ia, oa, id, od, need));
                (ia, oa, id, od)
            }
        };
        for (ch, x) in inputs.iter().enumerate() {
            let p = idata + (4 * need * ch) as u64;
            self.cpu.mem.write_f32s(p, x);
            self.cpu.mem.w64(ia + 8 * ch as u64, p);
        }
        for ch in 0..outputs.len() {
            let p = odata + (4 * need * ch) as u64;
            self.cpu.mem.w64(oa + 8 * ch as u64, p);
        }
        self.cpu.r[RCX] = self.handle;
        self.cpu.r[RDX] = ia;
        self.cpu.r[R8] = oa;
        self.cpu.r[R9] = 0;
        call_abi(&mut self.cpu, 0x862F00, &[n as u64]);
        for (ch, y) in outputs.iter_mut().enumerate() {
            let p = odata + (4 * need * ch) as u64;
            let v = self.cpu.mem.read_f32s(p, n);
            y.copy_from_slice(&v);
        }
    }
}

/// Chamada no ABI x64 do Windows: shadow space de 0x20, args extras a partir de `[rsp+0x20]`
/// (vistos pelo chamado em `[rsp+0x28]` depois do endereço de retorno).
pub fn call_abi(c: &mut Cpu, rva: u32, stack_args: &[u64]) {
    let sp0 = c.r[RSP];
    let frame = (0x20 + 8 * stack_args.len() as u64 + 15) & !15;
    c.r[RSP] = (sp0 - frame) & !15;
    let sp = c.r[RSP];
    for (k, v) in stack_args.iter().enumerate() {
        c.mem.w64(sp + 0x20 + 8 * k as u64, *v);
    }
    c.push(0xDEAD_BEEF);
    super::call(c, rva);
    assert_eq!(c.r[RSP], sp, "rsp desbalanceado após 0x{rva:X}");
    c.r[RSP] = sp0;
}
