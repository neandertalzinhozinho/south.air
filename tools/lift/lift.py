"""Tradutor mecânico x86-64 -> Rust (M5). Só lê o dump.

Para cada função de entrada, desmonta (capstone) do RVA até o fim do intervalo
.pdata que o contém (ou o tamanho fixado em GIANT) e emite uma `fn` Rust sobre
`crate::lifted::rt::Cpu`, com blocos básicos num `match pc`. Cada instrução vira
uma ou mais linhas, com o RVA e o texto da instrução em comentário. Instruções
não suportadas viram `panic!` com o RVA — nada é estimado.

Alvos de call/jmp:
  - dentro do cluster (LO..HI): traduzidos recursivamente;
  - fora: folhas, resolvidas em tempo de execução por `leaf::call` (handlers
    escritos à mão, com a prova de cada assinatura).

Uso: py tools/lift/lift.py <saida.rs> <rva> [<rva> ...]
"""
import struct, sys, re, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM

DUMP = r'dumpsooth/nyx_soothe3_dump.bin'
d = open(DUMP, 'rb').read()
pe = struct.unpack_from('<I', d, 0x3c)[0]
exc, esz = struct.unpack_from('<II', d, pe + 24 + 112 + 24)
PDATA = []
for i in range(esz // 12):
    b, e, u = struct.unpack_from('<III', d, exc + 12 * i)
    PDATA.append((b, e))
PDATA.sort()
REAL_ENTRY = set()
for i in range(esz // 12):
    b, e, u = struct.unpack_from('<III', d, exc + 12 * i)
    flags = d[u] >> 3
    if not (flags & 0x4):
        REAL_ENTRY.add(b)
GIANT = {0x8B3ED0: 0x8B3ED0 + 20209, 0x8C5C40: 0x8C5C40 + 20209}
LO, HI = 0x860000, 0x8D2000
IMAGE_BASE = 0x199B0000
IAT_LO, IAT_HI = 0x1D8C000, 0x1D8E000  # tabela de imports (FirstThunk)
IMPORTS_USED = set()


def import_names():
    """slot de IAT -> (dll, nome), lido dos descritores de import do dump."""
    out = {}
    # O diretório de import do PE aponta para a tabela do empacotador; a do plugin começa
    # na primeira entrada contígua antes de 0x2175044 (spec §10.4) com FirstThunk no IAT.
    imp = 0x2175044
    while True:
        ft0 = struct.unpack_from('<I', d, imp - 20 + 16)[0]
        if not (IAT_LO <= ft0 < IAT_HI):
            break
        imp -= 20
    i = 0
    while True:
        o, t, f, n, ft = struct.unpack_from('<IIIII', d, imp + 20 * i)
        if o == 0 and ft == 0:
            break
        dll = d[n:n + 64].split(b'\0')[0].decode()
        k = 0
        while True:
            e = struct.unpack_from('<Q', d, o + 8 * k)[0]
            if e == 0:
                break
            nm = d[e + 2:e + 80].split(b'\0')[0].decode() if not (e >> 63) else f'#{e & 0xFFFF}'
            out[ft + 8 * k] = (dll, nm)
            k += 1
        i += 1
    return out
# Regiões traduzidas mecanicamente: stubs IPP, impls IPP simples, cluster DSP, helpers 0x61xxxx.
REGIONS = [(0x1000, 0x2000), (0x2000, 0x200000), (0x1D20000, 0x1D70000), (0x850000, 0x8D2000), (0x610000, 0x620000),
           (0x1796000, 0x1799000),  # runtime C++ (new/delete, thunks jmp [IAT])
           (0x1C9A000, 0x1C9B000),  # thunks da math da UCRT (jmp [IAT])
           (0x310000, 0x330000), (0x330000, 0x340000), (0x560000, 0x570000), (0x690000, 0x6A0000), (0x6B0000, 0x6C0000),  # helpers std::/plugin
           (0x1C8000, 0x1C9000),  # stubs de math da IPP (0x1C84A0 etc.)
           (0x200000, 0x230000), (0x230000, 0x300000)]  # impls de math da IPP sem port provado (0x277C00 = 0x1C84D0)
# Folhas com port provado bit a bit (handlers em port/src/lifted/leaf.rs), nunca traduzidas:
PROVEN = {
    # Cópia/zero de bytes: semântica trivial e exata, assinatura conferida no dump
    # (handlers em port/src/lifted/leaf.rs). 0x699C0 consulta a CPU (0x2FB900/cpuid)
    # só para escolher o caminho temporal/não-temporal.
    0x699C0, 0x1D2E9E0, 0x1D2EB40, 0x1D2EF40, 0x1D2F0C0,
    0x17978C0,  # __chkstk (lê gs:[0x10]; só sonda a pilha)
    0x1796910,  # falha de __security_check_cookie
    0x17969E0,  # _Init_thread_header (handler: reinicializa estáticos do dump)
}


def in_region(t):
    return t not in PROVEN and any(a <= t < b for a, b in REGIONS)

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

REG64 = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi',
         'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
REGMAP = {}
for i, n in enumerate(REG64):
    REGMAP[n] = (i, 64)
for i, n in enumerate(['eax', 'ecx', 'edx', 'ebx', 'esp', 'ebp', 'esi', 'edi']):
    REGMAP[n] = (i, 32)
for i, n in enumerate(['ax', 'cx', 'dx', 'bx', 'sp', 'bp', 'si', 'di']):
    REGMAP[n] = (i, 16)
for i, n in enumerate(['al', 'cl', 'dl', 'bl', 'spl', 'bpl', 'sil', 'dil']):
    REGMAP[n] = (i, 8)
for k in range(8, 16):
    REGMAP[f'r{k}d'] = (k, 32)
    REGMAP[f'r{k}w'] = (k, 16)
    REGMAP[f'r{k}b'] = (k, 8)


def range_end(rva):
    if rva in GIANT:
        return GIANT[rva]
    best = None
    for b, e in PDATA:
        if b <= rva < e:
            best = e
    if best is None:
        # função-folha sem .pdata: vai até o início da próxima entrada .pdata
        nxt = [b for b, e in PDATA if b > rva]
        if not nxt:
            raise SystemExit(f'sem .pdata para 0x{rva:X}')
        return min(nxt)
    return best


class Unsupported(Exception):
    pass


def mask(bits):
    return (1 << bits) - 1


def rname(x, op):
    return x.reg_name(op.reg)


def addr_expr(x, op):
    m = op.mem
    if m.segment != 0:
        raise Unsupported('segmento')
    base = x.reg_name(m.base) if m.base else None
    idx = x.reg_name(m.index) if m.index else None
    if base == 'rip':
        a = IMAGE_BASE + x.address + x.size + m.disp
        if idx:
            raise Unsupported('rip+idx')
        return f'0x{a:X}u64'
    parts = []
    if base:
        bi, bb = REGMAP[base]
        if bb != 64:
            raise Unsupported('base 32')
        parts.append(f'c.r[{bi}]')
    if idx:
        ii, ib = REGMAP[idx]
        if ib != 64:
            raise Unsupported('idx 32')
        parts.append(f'c.r[{ii}].wrapping_mul({m.scale})' if m.scale != 1 else f'c.r[{ii}]')
    e = parts[0] if parts else '0u64'
    for p in parts[1:]:
        e = f'{e}.wrapping_add({p})'
    if m.disp:
        e = f'{e}.wrapping_add({m.disp & 0xFFFFFFFFFFFFFFFF:#x}u64)'
    return e


def is_xmm(name):
    return name.startswith('xmm')


def xi(name):
    i = int(name[3:])
    if i >= 16:
        raise Unsupported('AVX-512 (xmm16+)')
    return i


def rd_int(x, op, bits=None):
    """Expressão u64 do operando inteiro (zero-extendido para u64)."""
    if op.type == X86_OP_REG:
        n = rname(x, op)
        if n not in REGMAP:
            raise Unsupported(f'reg {n}')
        i, b = REGMAP[n]
        return {64: f'c.r[{i}]', 32: f'(c.r[{i}] as u32 as u64)', 16: f'(c.r[{i}] as u16 as u64)',
                8: f'(c.r[{i}] as u8 as u64)'}[b]
    if op.type == X86_OP_IMM:
        b = bits or op.size * 8
        return f'{op.imm & mask(b):#x}u64'
    if op.type == X86_OP_MEM:
        b = op.size * 8
        return f'(c.mem.r{b}({addr_expr(x, op)}) as u64)'
    raise Unsupported('op')


def wr_int(x, op, val):
    if op.type == X86_OP_REG:
        n = rname(x, op)
        i, b = REGMAP[n]
        return {64: f'{{ let v: u64 = {val}; c.r[{i}] = v; }}', 32: f'{{ let v = ({val}) as u32; c.s32({i}, v); }}',
                16: f'{{ let v = ({val}) as u16; c.s16({i}, v); }}', 8: f'{{ let v = ({val}) as u8; c.s8({i}, v); }}'}[b]
    if op.type == X86_OP_MEM:
        b = op.size * 8
        return f'{{ let a = {addr_expr(x, op)}; let v = ({val}) as u{b}; c.mem.w{b}(a, v); }}'
    raise Unsupported('dst')


def op_bits(op):
    return op.size * 8


def rd_x(x, op, nbytes=16):
    """Operando xmm como u128 (memória: carrega nbytes, zero-extendido)."""
    if op.type == X86_OP_REG:
        n = rname(x, op)
        if not is_xmm(n):
            raise Unsupported('não-xmm')
        return f'c.x[{xi(n)}]'
    if op.type == X86_OP_MEM:
        bits = nbytes * 8
        return f'(c.mem.r{bits}({addr_expr(x, op)}) as u128)'
    raise Unsupported('xop')


COND = {'e': 'c.c_e()', 'z': 'c.c_e()', 'ne': '!c.c_e()', 'nz': '!c.c_e()', 'a': 'c.c_a()',
        'ae': 'c.c_ae()', 'nb': 'c.c_ae()', 'b': 'c.c_b()', 'c': 'c.c_b()', 'be': 'c.c_be()',
        'l': 'c.c_l()', 'ge': 'c.c_ge()', 'le': 'c.c_le()', 'g': 'c.c_g()', 's': 'c.c_s()',
        'ns': '!c.c_s()', 'p': 'c.c_p()', 'np': '!c.c_p()'}

SS2 = {'addss': 'addss', 'subss': 'subss', 'mulss': 'mulss', 'divss': 'divss', 'minss': 'minss',
       'maxss': 'maxss', 'addsd': 'addsd', 'subsd': 'subsd', 'mulsd': 'mulsd', 'divsd': 'divsd',
       'minsd': 'minsd', 'maxsd': 'maxsd', 'addps': 'addps', 'subps': 'subps', 'mulps': 'mulps',
       'divps': 'divps', 'minps': 'minps', 'maxps': 'maxps', 'addpd': 'addpd', 'mulpd': 'mulpd',
       'subpd': 'subpd', 'divpd': 'divpd', 'sqrtss': 'sqrtss', 'sqrtsd': 'sqrtsd'}
SCALAR_BYTES = {'ss': 4, 'sd': 8}


def vreg(x, op):
    n = rname(x, op)
    if n.startswith('xmm') or n.startswith('ymm'):
        i = int(n[3:])
        if i >= 16:
            raise Unsupported('AVX-512 (xmm/ymm16+)')
        return i, (128 if n.startswith('xmm') else 256)
    raise Unsupported(f'vreg {n}')


def vsrc(x, op, width, scalar_bytes=None):
    """(lo, hi) de um operando vetorial. Memória: carrega width bits (ou scalar_bytes)."""
    if op.type == X86_OP_REG:
        i, w = vreg(x, op)
        return f'c.x[{i}]', (f'c.y[{i}]' if width == 256 else '0u128')
    a = addr_expr(x, op)
    if scalar_bytes:
        return f'(c.mem.r{scalar_bytes * 8}({a}) as u128)', '0u128'
    if width == 256:
        return f'c.mem.r128({a})', f'c.mem.r128(({a}).wrapping_add(16))'
    return f'c.mem.r128({a})', '0u128'


def vdst(x, op, lo, hi, width):
    i, w = vreg(x, op)
    return f'{{ let lo = {lo}; let hi = {hi}; c.x[{i}] = lo; c.y[{i}] = {"hi" if width == 256 else "0"}; }}'


VPACK = {'vaddps': 'sse::addps', 'vsubps': 'sse::subps', 'vmulps': 'sse::mulps', 'vdivps': 'sse::divps',
         'vminps': 'sse::minps', 'vmaxps': 'sse::maxps', 'vaddpd': 'sse::addpd', 'vmulpd': 'sse::mulpd',
         'vsubpd': 'sse::subpd', 'vdivpd': 'sse::divpd'}
VBIT = {'vandps': '&', 'vandpd': '&', 'vpand': '&', 'vxorps': '^', 'vxorpd': '^', 'vpxor': '^',
        'vorps': '|', 'vorpd': '|', 'vpor': '|'}
VSCAL = {'vaddss': 'sse::addss', 'vsubss': 'sse::subss', 'vmulss': 'sse::mulss', 'vdivss': 'sse::divss',
         'vminss': 'sse::minss', 'vmaxss': 'sse::maxss', 'vaddsd': 'sse::addsd', 'vsubsd': 'sse::subsd',
         'vmulsd': 'sse::mulsd', 'vdivsd': 'sse::divsd', 'vminsd': 'sse::minsd', 'vmaxsd': 'sse::maxsd'}


VCMP_PRED = {'eq': 0, 'lt': 1, 'le': 2, 'unord': 3, 'neq': 4, 'nlt': 5, 'nle': 6, 'ord': 7,
             'eq_uq': 8, 'nge': 9, 'ngt': 10, 'false': 11, 'neq_oq': 12, 'ge': 13, 'gt': 14,
             'true': 15, 'eq_os': 16, 'lt_oq': 17, 'le_oq': 18, 'neq_us': 20, 'nlt_uq': 21, 'nle_uq': 22,
             'ge_oq': 29, 'gt_oq': 30}


def lift_vex(x):
    m = x.mnemonic
    ops = x.operands
    R = 'super::rt::'
    if m == 'vzeroupper':
        return 'c.y = [0; 16];'
    if any(o.type == X86_OP_REG and rname(x, o).startswith('zmm') for o in ops) or \
            any(o.type == X86_OP_MEM and o.size == 64 for o in ops):
        raise Unsupported('AVX-512')
    if m in ('vmovups', 'vmovaps', 'vmovdqu', 'vmovdqa', 'vmovupd', 'vmovapd', 'vlddqu'):
        dst, src = ops
        if dst.type == X86_OP_MEM:
            i, w = vreg(x, src)
            a = addr_expr(x, dst)
            if w == 256:
                return f'{{ let a = {a}; c.mem.w128(a, c.x[{i}]); c.mem.w128(a.wrapping_add(16), c.y[{i}]); }}'
            return f'{{ let a = {a}; c.mem.w128(a, c.x[{i}]); }}'
        i, w = vreg(x, dst)
        lo, hi = vsrc(x, src, w)
        return vdst(x, dst, lo, hi, w)
    if m in ('vmovss', 'vmovsd'):
        nb = 4 if m == 'vmovss' else 8
        mk = (1 << (nb * 8)) - 1
        if len(ops) == 3:
            i, _ = vreg(x, ops[0])
            a, _ = vsrc(x, ops[1], 128)
            b, _ = vsrc(x, ops[2], 128)
            return vdst(x, ops[0], f'({a} & !{mk:#x}u128) | ({b} & {mk:#x}u128)', '0', 128)
        dst, src = ops
        if dst.type == X86_OP_MEM:
            i, _ = vreg(x, src)
            return f'{{ let a = {addr_expr(x, dst)}; c.mem.w{nb * 8}(a, c.x[{i}] as u{nb * 8}); }}'
        return vdst(x, dst, f'(c.mem.r{nb * 8}({addr_expr(x, src)}) as u128)', '0', 128)
    if m in ('vmovd', 'vmovq'):
        bits = 32 if m == 'vmovd' else 64
        dst, src = ops
        if dst.type == X86_OP_REG and rname(x, dst).startswith('xmm'):
            if src.type == X86_OP_REG and rname(x, src).startswith('xmm'):
                i, _ = vreg(x, src)
                return vdst(x, dst, f'c.x[{i}] & {mask(bits):#x}u128', '0', 128)
            return vdst(x, dst, f'(({rd_int(x, src)}) & {mask(bits):#x}u64) as u128', '0', 128)
        i, _ = vreg(x, src)
        return wr_int(x, dst, f'(c.x[{i}] as u{bits} as u64)')
    if m in VPACK or m in VBIT or m in ('vandnps', 'vpandn'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        if m in VPACK:
            f = R + VPACK[m]
            return vdst(x, ops[0], f'{f}({a[0]}, {b[0]})', f'{f}({a[1]}, {b[1]})', w)
        if m in VBIT:
            o = VBIT[m]
            return vdst(x, ops[0], f'{a[0]} {o} {b[0]}', f'{a[1]} {o} {b[1]}', w)
        return vdst(x, ops[0], f'!{a[0]} & {b[0]}', f'!{a[1]} & {b[1]}', w)
    if m in VSCAL:
        nb = 4 if m.endswith('ss') else 8
        a, _ = vsrc(x, ops[1], 128)
        b, _ = vsrc(x, ops[2], 128, nb if ops[2].type == X86_OP_MEM else None)
        return vdst(x, ops[0], f'{R}{VSCAL[m]}({a}, {b})', '0', 128)
    ma = re.match(r'v(fmaddsub|fmsubadd)(132|213|231)ps$', m)
    if ma:
        kind, order = ma.groups()
        i, w = vreg(x, ops[0])
        o1, o2, o3 = vsrc(x, ops[0], w), vsrc(x, ops[1], w), vsrc(x, ops[2], w)
        trip = {'213': (o2, o1, o3), '231': (o2, o3, o1), '132': (o1, o3, o2)}[order]
        f = f'{R}avxd::{kind}_ps'
        return vdst(x, ops[0], f'{f}({trip[0][0]}, {trip[1][0]}, {trip[2][0]})',
                    f'{f}({trip[0][1]}, {trip[1][1]}, {trip[2][1]})', w)
    mf = re.match(r'v(fn?m(?:add|sub))(132|213|231)(ps|ss|sd|pd)$', m)
    if mf:
        kind, order, ty = mf.groups()
        fn = {'fmadd': 'fmadd', 'fmsub': 'fmsub', 'fnmadd': 'fnmadd', 'fnmsub': 'fnmsub'}.get(kind)
        if fn is None:
            raise Unsupported(m)
        i, w = vreg(x, ops[0])
        scal = ty in ('ss', 'sd')
        nb = {'ss': 4, 'sd': 8}.get(ty)
        o1 = vsrc(x, ops[0], w)
        o2 = vsrc(x, ops[1], w)
        o3 = vsrc(x, ops[2], w, nb if (scal and ops[2].type == X86_OP_MEM) else None)
        f = f'{R}avx::{fn}_{ty}' if ty != 'pd' else f'{R}avxd::{fn}_pd'
        if not scal:
            trip = {'213': (o2, o1, o3), '231': (o2, o3, o1), '132': (o1, o3, o2)}[order]
            lo = f'{f}({trip[0][0]}, {trip[1][0]}, {trip[2][0]})'
            hi = f'{f}({trip[0][1]}, {trip[1][1]}, {trip[2][1]})'
            return vdst(x, ops[0], lo, hi, w)
        # escalar: lanes altas vêm de op1
        trip = {'213': (o1, o2, o3), '231': (o2, o3, o1), '132': (o1, o3, o2)}[order]
        mk = (1 << (nb * 8)) - 1
        v = f'{f}({trip[0][0]}, {trip[1][0]}, {trip[2][0]})'
        return vdst(x, ops[0], f'({o1[0]} & !{mk:#x}u128) | ({v} & {mk:#x}u128)', '0', 128)
    if m == 'vbroadcastss':
        i, w = vreg(x, ops[0])
        src = ops[1]
        v = f'c.mem.r32({addr_expr(x, src)})' if src.type == X86_OP_MEM else f'(c.x[{vreg(x, src)[0]}] as u32)'
        return f'{{ let b = {R}avx::broadcast32({v}); c.x[{i}] = b; c.y[{i}] = {"b" if w == 256 else "0"}; }}'
    if m == 'vextractf128':
        i, _ = vreg(x, ops[1])
        half = f'c.y[{i}]' if ops[2].imm & 1 else f'c.x[{i}]'
        if ops[0].type == X86_OP_MEM:
            return f'{{ let a = {addr_expr(x, ops[0])}; c.mem.w128(a, {half}); }}'
        return vdst(x, ops[0], half, '0', 128)
    if m == 'vinsertf128':
        i, _ = vreg(x, ops[0])
        s1 = vsrc(x, ops[1], 256)
        s2 = vsrc(x, ops[2], 128)[0]
        if ops[3].imm & 1:
            return vdst(x, ops[0], s1[0], s2, 256)
        return vdst(x, ops[0], s2, s1[1], 256)
    if m == 'vperm2f128':
        a = vsrc(x, ops[1], 256)
        b = vsrc(x, ops[2], 256)
        imm = ops[3].imm
        sel = [a[0], a[1], b[0], b[1]]
        lo = '0u128' if imm & 0x08 else sel[imm & 3]
        hi = '0u128' if imm & 0x80 else sel[(imm >> 4) & 3]
        return vdst(x, ops[0], lo, hi, 256)
    if m == 'vblendvps':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        mm = vsrc(x, ops[3], w)
        f = f'{R}avx::blendv_ps'
        return vdst(x, ops[0], f'{f}({a[0]}, {b[0]}, {mm[0]})', f'{f}({a[1]}, {b[1]}, {mm[1]})', w)
    if m == 'vmaskmovps':
        if ops[0].type == X86_OP_MEM:  # store: [m] <- src onde mask
            mi, w = vreg(x, ops[1])
            si, _ = vreg(x, ops[2])
            a = addr_expr(x, ops[0])
            n = 8 if w == 256 else 4
            return (f'{{ let a = {a}; for l in 0..{n} {{ let (mk, v) = if l < 4 {{ (c.x[{mi}] >> (32 * l), c.x[{si}] >> (32 * l)) }} '
                    f'else {{ (c.y[{mi}] >> (32 * (l - 4)), c.y[{si}] >> (32 * (l - 4))) }}; '
                    f'if (mk as u32) >> 31 == 1 {{ c.mem.w32(a.wrapping_add(4 * l as u64), v as u32); }} }} }}')
        di, w = vreg(x, ops[0])
        mi, _ = vreg(x, ops[1])
        a = addr_expr(x, ops[2])
        n = 8 if w == 256 else 4
        return (f'{{ let a = {a}; let mut lo = 0u128; let mut hi = 0u128; for l in 0..{n} {{ '
                f'let mk = if l < 4 {{ c.x[{mi}] >> (32 * l) }} else {{ c.y[{mi}] >> (32 * (l - 4)) }}; '
                f'if (mk as u32) >> 31 == 1 {{ let v = c.mem.r32(a.wrapping_add(4 * l as u64)) as u128; '
                f'if l < 4 {{ lo |= v << (32 * l) }} else {{ hi |= v << (32 * (l - 4)) }} }} }} '
                f'c.x[{di}] = lo; c.y[{di}] = {"hi" if w == 256 else "0"}; }}')
    if m == 'vmovhlps':
        a = vsrc(x, ops[1], 128)[0]
        b = vsrc(x, ops[2], 128)[0]
        return vdst(x, ops[0], f'(({a}) & !0xFFFF_FFFF_FFFF_FFFFu128) | (({b}) >> 64)', '0', 128)
    if m == 'vmovlhps':
        a = vsrc(x, ops[1], 128)[0]
        b = vsrc(x, ops[2], 128)[0]
        return vdst(x, ops[0], f'(({a}) & 0xFFFF_FFFF_FFFF_FFFFu128) | (({b}) << 64)', '0', 128)
    if m == 'vshufps':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        imm = ops[3].imm
        return vdst(x, ops[0], f'{R}sse::shufps({a[0]}, {b[0]}, {imm})', f'{R}sse::shufps({a[1]}, {b[1]}, {imm})', w)
    if m == 'vpsllw':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        cnt = vsrc(x, ops[2], 128)[0] if ops[2].type != X86_OP_IMM else f'{ops[2].imm}u128'
        def sh(v):
            return (f'{{ let n = ({cnt}) as u64; let v = {v}; if n > 15 {{ 0u128 }} else {{ let mut r = 0u128; '
                    f'for k in 0..8 {{ let w = ((v >> (16 * k)) as u16) << n; r |= (w as u128) << (16 * k); }} r }} }}')
        return vdst(x, ops[0], sh(a[0]), sh(a[1]), w)
    if m in ('vucomiss', 'vcomiss', 'vucomisd', 'vcomisd'):
        nb = 4 if m.endswith('ss') else 8
        f = 'cmp_ss' if nb == 4 else 'cmp_sd'
        a = vsrc(x, ops[0], 128)[0]
        b = vsrc(x, ops[1], 128, nb if ops[1].type == X86_OP_MEM else None)[0]
        return f'{{ let (u, lt, eq) = {R}sse::{f}({a}, {b}); c.fl_comi(u, lt, eq); }}'
    mc = re.match(r'vcmp(\w+?)(ps|ss)$', m)
    if mc and mc.group(1) in VCMP_PRED:
        pred = VCMP_PRED[mc.group(1)]
        i, w = vreg(x, ops[0])
        if mc.group(2) == 'ss':
            a = vsrc(x, ops[1], 128)[0]
            b = vsrc(x, ops[2], 128, 4 if ops[2].type == X86_OP_MEM else None)[0]
            v = f'{R}avx::cmp_ps({a}, {b}, {pred})'
            return vdst(x, ops[0], f'(({a}) & !0xFFFF_FFFFu128) | (({v}) & 0xFFFF_FFFFu128)', '0', 128)
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        return vdst(x, ops[0], f'{R}avx::cmp_ps({a[0]}, {b[0]}, {pred})', f'{R}avx::cmp_ps({a[1]}, {b[1]}, {pred})', w)
    if m == 'vtestps':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[0], w)
        b = vsrc(x, ops[1], w)
        n = 8 if w == 256 else 4
        return (f'{{ let ma = {R}ilane::movmskps({a[0]}, {a[1]}, {n}); let mb = {R}ilane::movmskps({b[0]}, {b[1]}, {n}); '
                f'c.zf = ma & mb == 0; c.cf = !ma & mb == 0; c.of = false; c.sf = false; c.pf = false; }}')
    if m == 'vcmpps':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        p = ops[3].imm
        return vdst(x, ops[0], f'{R}avx::cmp_ps({a[0]}, {b[0]}, {p})', f'{R}avx::cmp_ps({a[1]}, {b[1]}, {p})', w)
    if m in ('vpaddd', 'vpsubd', 'vpcmpeqd', 'vpcmpgtd', 'vpunpcklqdq', 'vpunpckhqdq', 'vpunpckldq', 'vpunpckhdq'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        f = f'{R}ilane::{m[1:]}'
        return vdst(x, ops[0], f'{f}({a[0]}, {b[0]})', f'{f}({a[1]}, {b[1]})', w)
    if m in ('vpslld', 'vpsrld', 'vpsrad'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        n = f'{ops[2].imm}u64' if ops[2].type == X86_OP_IMM else f'(({vsrc(x, ops[2], 128)[0]}) as u64)'
        f = f'{R}ilane::{m[1:]}'
        return vdst(x, ops[0], f'{f}({a[0]}, {n})', f'{f}({a[1]}, {n})', w)
    if m == 'vmovmskps':
        i, w = vreg(x, ops[1])
        return wr_int(x, ops[0], f'{R}ilane::movmskps(c.x[{i}], c.y[{i}], {8 if w == 256 else 4})')
    if m == 'vpinsrd':
        a = vsrc(x, ops[1], 128)[0]
        v = rd_int(x, ops[2])
        k = ops[3].imm & 3
        return vdst(x, ops[0], f'(({a}) & !(0xFFFF_FFFFu128 << {32 * k})) | (((({v}) as u32) as u128) << {32 * k})', '0', 128)
    if m == 'vpextrd':
        i, _ = vreg(x, ops[1])
        k = ops[2].imm & 3
        return wr_int(x, ops[0], f'((c.x[{i}] >> {32 * k}) as u32 as u64)')
    if m == 'vextracti128':
        i, _ = vreg(x, ops[1])
        half = f'c.y[{i}]' if ops[2].imm & 1 else f'c.x[{i}]'
        if ops[0].type == X86_OP_MEM:
            return f'{{ let a = {addr_expr(x, ops[0])}; c.mem.w128(a, {half}); }}'
        return vdst(x, ops[0], half, '0', 128)
    if m == 'vcvtsd2ss':
        a = vsrc(x, ops[1], 128)[0]
        b = vsrc(x, ops[2], 128, 8 if ops[2].type == X86_OP_MEM else None)[0]
        return vdst(x, ops[0], f'{R}sse::cvtsd2ss({a}, {b})', '0', 128)
    if m == 'vcvtss2sd':
        a = vsrc(x, ops[1], 128)[0]
        b = vsrc(x, ops[2], 128, 4 if ops[2].type == X86_OP_MEM else None)[0]
        return vdst(x, ops[0], f'{R}sse::cvtss2sd({a}, {b})', '0', 128)
    if m in ('vcvtsi2sd', 'vcvtsi2ss'):
        a = vsrc(x, ops[1], 128)[0]
        b = op_bits(ops[2])
        f = f'{m[1:]}{b}'
        return vdst(x, ops[0], f'{R}sse::{f}({a}, ({rd_int(x, ops[2])}) as u{b} as i{b})', '0', 128)
    if m in ('vcvtdq2ps', 'vcvttps2dq', 'vcvtps2dq'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        f = f'{R}sse::{m[1:]}'
        return vdst(x, ops[0], f'{f}({a[0]})', f'{f}({a[1]})', w)
    if m == 'vrsqrtps':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        return vdst(x, ops[0], f'{R}ilane::rsqrt_ps({a[0]})', f'{R}ilane::rsqrt_ps({a[1]})', w)
    if m == 'vstmxcsr':
        return f'{{ let a = {addr_expr(x, ops[0])}; c.mem.w32(a, {R}get_mxcsr()); }}'
    if m == 'vldmxcsr':
        return f'{{ let a = {addr_expr(x, ops[0])}; let v = c.mem.r32(a); {R}set_mxcsr(v); }}'
    if m in ('vmovhpd', 'vmovhps', 'vmovlpd', 'vmovlps'):
        hi = m in ('vmovhpd', 'vmovhps')
        if ops[0].type == X86_OP_MEM:
            i, _ = vreg(x, ops[1])
            v = f'(c.x[{i}] >> 64) as u64' if hi else f'c.x[{i}] as u64'
            return f'{{ let a = {addr_expr(x, ops[0])}; let v = {v}; c.mem.w64(a, v); }}'
        a = vsrc(x, ops[1], 128)[0]
        v = f'(c.mem.r64({addr_expr(x, ops[2])}) as u128)'
        if hi:
            return vdst(x, ops[0], f'(({a}) & 0xFFFF_FFFF_FFFF_FFFFu128) | ({v} << 64)', '0', 128)
        return vdst(x, ops[0], f'(({a}) & !0xFFFF_FFFF_FFFF_FFFFu128) | {v}', '0', 128)
    if m == 'vcvtps2pd':
        i, w = vreg(x, ops[0])
        if w == 256:
            a = vsrc(x, ops[1], 128)[0]
            return f'{{ let (lo, hi) = {R}avxd::cvtps2pd_256({a}); c.x[{i}] = lo; c.y[{i}] = hi; }}'
        a = vsrc(x, ops[1], 128, 8 if ops[1].type == X86_OP_MEM else None)[0]
        return vdst(x, ops[0], f'{R}sse::cvtps2pd({a})', '0', 128)
    if m == 'vcvtpd2ps':
        w = vreg(x, ops[1])[1] if ops[1].type == X86_OP_REG else ops[1].size * 8
        a = vsrc(x, ops[1], w)
        if w == 256:
            return vdst(x, ops[0], f'{R}avxd::cvtpd2ps_256({a[0]}, {a[1]})', '0', 128)
        return vdst(x, ops[0], f'{R}sse::cvtpd2ps({a[0]})', '0', 128)
    if m in ('vmovsldup', 'vmovshdup'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        f = f'{R}avxd::' + ('moveldup' if m == 'vmovsldup' else 'movehdup')
        return vdst(x, ops[0], f'{f}({a[0]})', f'{f}({a[1]})', w)
    if m in ('vpsrlq', 'vpsllq'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        n = f'{ops[2].imm}u32' if ops[2].type == X86_OP_IMM else f'(({vsrc(x, ops[2], 128)[0]}) as u64 as u32)'
        o = '>>' if m == 'vpsrlq' else '<<'

        def sh(v):
            return (f'{{ let n = {n}; let l = {R}sse::lanes64({v}); if n > 63 {{ 0u128 }} else '
                    f'{{ {R}sse::from64([l[0] {o} n, l[1] {o} n]) }} }}')
        return vdst(x, ops[0], sh(a[0]), sh(a[1]), w)
    if m in ('vpsubq', 'vpaddq'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        f = 'wrapping_sub' if m == 'vpsubq' else 'wrapping_add'

        def op2(p, q):
            return (f'{{ let p = {R}sse::lanes64({p}); let q = {R}sse::lanes64({q}); '
                    f'{R}sse::from64([p[0].{f}(q[0]), p[1].{f}(q[1])]) }}')
        return vdst(x, ops[0], op2(a[0], b[0]), op2(a[1], b[1]), w)
    if m in ('vmovntdq', 'vmovntps', 'vmovntpd'):
        i, w = vreg(x, ops[1])
        a = addr_expr(x, ops[0])
        if w == 256:
            return f'{{ let a = {a}; c.mem.w128(a, c.x[{i}]); c.mem.w128(a.wrapping_add(16), c.y[{i}]); }}'
        return f'{{ let a = {a}; c.mem.w128(a, c.x[{i}]); }}'
    if m in ('vaddsubps', 'vaddsubpd', 'vhaddpd', 'vhaddps', 'vmaxpd', 'vminpd'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        f = f'{R}avxd::' + {'vaddsubps': 'addsub_ps', 'vaddsubpd': 'addsub_pd', 'vhaddpd': 'hadd_pd',
                            'vhaddps': 'hadd_ps', 'vmaxpd': 'max_pd', 'vminpd': 'min_pd'}[m]
        return vdst(x, ops[0], f'{f}({a[0]}, {b[0]})', f'{f}({a[1]}, {b[1]})', w)
    if m == 'vpermps':
        i, w = vreg(x, ops[0])
        ix = vsrc(x, ops[1], 256)
        sv = vsrc(x, ops[2], 256)
        return f'{{ let (lo, hi) = {R}avxd::permps({ix[0]}, {ix[1]}, {sv[0]}, {sv[1]}); c.x[{i}] = lo; c.y[{i}] = hi; }}'
    if m in ('vunpckhpd', 'vunpcklpd'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)

        def u(p, q):
            if m == 'vunpcklpd':
                return f'((({p}) & 0xFFFF_FFFF_FFFF_FFFFu128) | ((({q}) & 0xFFFF_FFFF_FFFF_FFFFu128) << 64))'
            return f'((({p}) >> 64) | ((({q}) >> 64) << 64))'
        return vdst(x, ops[0], u(a[0], b[0]), u(a[1], b[1]), w)
    if m == 'vpbroadcastd':
        i, w = vreg(x, ops[0])
        src = ops[1]
        v = f'c.mem.r32({addr_expr(x, src)})' if src.type == X86_OP_MEM else f'(c.x[{vreg(x, src)[0]}] as u32)'
        return f'{{ let b = {R}avx::broadcast32({v}); c.x[{i}] = b; c.y[{i}] = {"b" if w == 256 else "0"}; }}'
    if m == 'vsqrtsd':
        a = vsrc(x, ops[1], 128)[0]
        b = vsrc(x, ops[2], 128, 8 if ops[2].type == X86_OP_MEM else None)[0]
        return vdst(x, ops[0], f'{R}avxd::sqrt_sd({a}, {b})', '0', 128)
    if m in ('vsqrtps', 'vsqrtpd'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        f = f'{R}avxd::sqrt_{m[-2:]}'
        return vdst(x, ops[0], f'{f}({a[0]})', f'{f}({a[1]})', w)
    if m in ('vunpcklps', 'vunpckhps'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        f = f'{R}sse::{m[1:]}'
        return vdst(x, ops[0], f'{f}({a[0]}, {b[0]})', f'{f}({a[1]}, {b[1]})', w)
    if m in ('vpmulld', 'vpmuludq'):
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)
        if m == 'vpmulld':
            f = lambda p, q: f'{R}ilane::map2({p}, {q}, |u, v| u.wrapping_mul(v))'
        else:
            f = lambda p, q: (f'{{ let (p, q) = ({R}sse::lanes64({p}), {R}sse::lanes64({q})); '
                              f'{R}sse::from64([(p[0] as u32 as u64) * (q[0] as u32 as u64), (p[1] as u32 as u64) * (q[1] as u32 as u64)]) }}')
        return vdst(x, ops[0], f(a[0], b[0]), f(a[1], b[1]), w)
    if m == 'vcvtdq2pd':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], 128, (8 if w == 128 else 16) if ops[1].type == X86_OP_MEM else None)[0]
        lo = f'{R}sse::cvtdq2pd({a})'
        hi = f'{R}sse::cvtdq2pd(({a}) >> 64)'
        return vdst(x, ops[0], lo, hi, w)
    if m == 'vbroadcastsd':
        i, w = vreg(x, ops[0])
        src = ops[1]
        v = f'c.mem.r64({addr_expr(x, src)})' if src.type == X86_OP_MEM else f'(c.x[{vreg(x, src)[0]}] as u64)'
        return f'{{ let q = {v} as u128; let b = q | (q << 64); c.x[{i}] = b; c.y[{i}] = {"b" if w == 256 else "0"}; }}'
    if m == 'vbroadcastf128':
        i, _ = vreg(x, ops[0])
        return f'{{ let v = c.mem.r128({addr_expr(x, ops[1])}); c.x[{i}] = v; c.y[{i}] = v; }}'
    if m == 'vpcmpeqw':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        b = vsrc(x, ops[2], w)

        def cw(p, q):
            return (f'{{ let (p, q) = ({p}, {q}); let mut r = 0u128; for k in 0..8 {{ '
                    f'if (p >> (16 * k)) as u16 == (q >> (16 * k)) as u16 {{ r |= 0xFFFFu128 << (16 * k); }} }} r }}')
        return vdst(x, ops[0], cw(a[0], b[0]), cw(a[1], b[1]), w)
    if m == 'vrcpps':
        i, w = vreg(x, ops[0])
        a = vsrc(x, ops[1], w)
        return vdst(x, ops[0], f'{R}avx::rcp_ps({a[0]})', f'{R}avx::rcp_ps({a[1]})', w)
    raise Unsupported(m)


def lift_insn(x, entry, inset, calls, notes):
    """Rust para uma instrução. Devolve (código, termina_bloco)."""
    m = x.mnemonic
    ops = x.operands
    nxt = x.address + x.size
    if m.startswith('v') and m not in ('verr', 'verw'):
        return lift_vex(x), False
    if m in ('nop', 'endbr64', 'prefetcht0', 'prefetcht1', 'prefetcht2', 'prefetchnta', 'sfence', 'lfence',
             'mfence', 'pause', 'fnclex', 'fldcw'):
        return '', False  # sem efeito sobre valores (o x87 não faz conta nestas funções)
    if m == 'fnstcw':
        # palavra de controle x87 padrão (0x027F); só é relida por fldcw, que é no-op aqui
        return f'{{ let a = {addr_expr(x, ops[0])}; c.mem.w16(a, 0x027F); }}', False
    if m in ('stmxcsr', 'ldmxcsr'):
        if m == 'stmxcsr':
            return f'{{ let a = {addr_expr(x, ops[0])}; c.mem.w32(a, super::rt::get_mxcsr()); }}', False
        return f'{{ let a = {addr_expr(x, ops[0])}; let v = c.mem.r32(a); super::rt::set_mxcsr(v); }}', False
    if m == 'popcnt':
        b = op_bits(ops[0])
        return (f'{{ let r = ({rd_int(x, ops[1])}).count_ones() as u64; c.fl_logic(r, {b}); '
                f'{wr_int(x, ops[0], "r")} }}'), False
    if m == 'bt':
        b = op_bits(ops[0])
        n = f'{ops[1].imm % b}u64' if ops[1].type == X86_OP_IMM else f'({rd_int(x, ops[1])} % {b})'
        return f'c.cf = ({rd_int(x, ops[0])} >> {n}) & 1 == 1;', False
    if m in ('shrx', 'shlx', 'sarx'):
        b = op_bits(ops[0])
        n = f'({rd_int(x, ops[2])} & {b - 1})'
        v = rd_int(x, ops[1])
        if m == 'shrx':
            e = f'({v} >> {n})'
        elif m == 'shlx':
            e = f'(({v} << {n}) & {mask(b):#x}u64)'
        else:
            e = f'(((({v} << (64 - {b})) as i64) >> (64 - {b})) >> {n}) as u64 & {mask(b):#x}u64'
        return wr_int(x, ops[0], e), False
    if m == 'int3':
        return f'panic!("int3 em 0x{x.address:X}");', True
    if m == 'mov' and len(ops) == 2 and ops[1].type == X86_OP_MEM and ops[1].mem.segment != 0:
        if x.reg_name(ops[1].mem.segment) != 'gs' or ops[1].mem.base or ops[1].mem.index:
            raise Unsupported('segmento')
        return wr_int(x, ops[0], f'c.gs_read({ops[1].mem.disp:#x}, 0x{x.address:X})'), False
    if m in ('rol', 'ror'):
        b = op_bits(ops[0])
        cnt = f'{ops[1].imm:#x}u64' if ops[1].type == X86_OP_IMM else '(c.r[1] as u8 as u64)'
        fn = 'rotate_left' if m == 'rol' else 'rotate_right'
        cm = 63 if b == 64 else 31
        cfe = 'r & 1 == 1' if m == 'rol' else f'(r >> ({b} - 1)) & 1 == 1'
        return (f'{{ let v = {rd_int(x, ops[0])} as u{b}; let n = ({cnt} & {cm}) as u32 % {b}; '
                f'let r = v.{fn}(n) as u64; if n != 0 {{ c.cf = {cfe}; }} '
                f'{wr_int(x, ops[0], "r")} }}'), False
    if m in ('sbb', 'adc'):
        b = op_bits(ops[0])
        a = rd_int(x, ops[0])
        q = f'{ops[1].imm & mask(b):#x}u64' if ops[1].type == X86_OP_IMM else rd_int(x, ops[1])
        f = 'fl_sub' if m == 'sbb' else 'fl_add'
        return (f'{{ let p = {a}; let q = {q}; let cin = c.cf as u64; let r1 = c.{f}(p, q, {b}); let c1 = c.cf; '
                f'let o1 = c.of; let r = c.{f}(r1, cin, {b}); c.cf |= c1; c.of ^= o1; {wr_int(x, ops[0], "r")} }}'), False
    if m in ('blsr', 'blsi', 'blsmsk', 'tzcnt', 'lzcnt', 'andn', 'bzhi', 'bsf', 'bsr'):
        b = op_bits(ops[0])
        mk = f'{mask(b):#x}u64'
        if m == 'andn':
            p_, q_ = rd_int(x, ops[1]), rd_int(x, ops[2])
            return f'{{ let r = (!{p_}) & {q_} & {mk}; c.fl_logic(r, {b}); {wr_int(x, ops[0], "r")} }}', False
        if m == 'bzhi':
            v_, n_ = rd_int(x, ops[1]), rd_int(x, ops[2])
            return (f'{{ let v = {v_}; let n = ({n_}) & 0xFF; let r = if n >= {b} {{ v & {mk} }} else {{ v & ((1u64 << n) - 1) }}; '
                    f'c.fl_logic(r, {b}); c.cf = n > {b - 1}; {wr_int(x, ops[0], "r")} }}'), False
        v_ = rd_int(x, ops[1])
        if m == 'blsr':
            e = f'v.wrapping_sub(1) & v & {mk}'
            cf = 'v == 0'
        elif m == 'blsi':
            e = f'v.wrapping_neg() & v & {mk}'
            cf = 'v != 0'
        elif m == 'blsmsk':
            e = f'(v.wrapping_sub(1) ^ v) & {mk}'
            cf = 'v == 0'
        elif m == 'tzcnt':
            return (f'{{ let v = {v_} & {mk}; let r = if v == 0 {{ {b} }} else {{ v.trailing_zeros() as u64 }}; '
                    f'c.cf = v == 0; c.zf = r == 0; {wr_int(x, ops[0], "r")} }}'), False
        elif m == 'lzcnt':
            return (f'{{ let v = {v_} & {mk}; let r = if v == 0 {{ {b} }} else {{ (v.leading_zeros() - (64 - {b})) as u64 }}; '
                    f'c.cf = v == 0; c.zf = r == 0; {wr_int(x, ops[0], "r")} }}'), False
        elif m == 'bsf':
            return (f'{{ let v = {v_} & {mk}; c.zf = v == 0; if v != 0 {{ let r = v.trailing_zeros() as u64; '
                    f'{wr_int(x, ops[0], "r")} }} }}'), False
        else:  # bsr
            return (f'{{ let v = {v_} & {mk}; c.zf = v == 0; if v != 0 {{ let r = 63 - v.leading_zeros() as u64; '
                    f'{wr_int(x, ops[0], "r")} }} }}'), False
        return (f'{{ let v = {v_} & {mk}; let r = {e}; c.fl_logic(r, {b}); c.cf = {cf}; '
                f'{wr_int(x, ops[0], "r")} }}'), False
    if m == 'std':
        return 'c.df = true;', False
    if m == 'cld':
        return 'c.df = false;', False
    if m in ('rep stosb', 'rep stosd', 'rep stosq', 'rep movsb', 'rep movsd', 'rep movsq'):
        w = {'b': 1, 'd': 4, 'q': 8}[m[-1]]
        if 'stos' in m:
            return (f'{{ while c.r[1] != 0 {{ let a = c.r[7]; let v = c.r[0]; c.mem.write(a, &v.to_le_bytes()[..{w}]); '
                    f'c.r[7] = if c.df {{ a.wrapping_sub({w}) }} else {{ a.wrapping_add({w}) }}; c.r[1] -= 1; }} }}'), False
        return (f'{{ while c.r[1] != 0 {{ let mut t = [0u8; {w}]; let s_ = c.r[6]; let d_ = c.r[7]; '
                f'c.mem.read(s_, &mut t); c.mem.write(d_, &t); '
                f'c.r[6] = if c.df {{ s_.wrapping_sub({w}) }} else {{ s_.wrapping_add({w}) }}; '
                f'c.r[7] = if c.df {{ d_.wrapping_sub({w}) }} else {{ d_.wrapping_add({w}) }}; c.r[1] -= 1; }} }}'), False
    if m in ('movlps', 'movlpd', 'movhps', 'movhpd'):
        hi = m in ('movhps', 'movhpd')
        dst, src = ops
        if dst.type == X86_OP_MEM:
            i = xi(rname(x, src))
            v = f'(c.x[{i}] >> 64) as u64' if hi else f'c.x[{i}] as u64'
            return f'{{ let a = {addr_expr(x, dst)}; let v = {v}; c.mem.w64(a, v); }}', False
        i = xi(rname(x, dst))
        v = f'c.mem.r64({addr_expr(x, src)}) as u128'
        if hi:
            return f'{{ let v = {v}; c.x[{i}] = (c.x[{i}] & 0xFFFF_FFFF_FFFF_FFFFu128) | (v << 64); }}', False
        return f'{{ let v = {v}; c.x[{i}] = (c.x[{i}] & !0xFFFF_FFFF_FFFF_FFFFu128) | v; }}', False
    if m == 'pextrw':
        i = xi(rname(x, ops[1]))
        k = ops[2].imm & 7
        return wr_int(x, ops[0], f'((c.x[{i}] >> {16 * k}) as u16 as u64)'), False
    if m in ('unpcklpd', 'unpckhpd'):
        d_ = xi(rname(x, ops[0]))
        s_ = rd_x(x, ops[1])
        if m == 'unpcklpd':
            return f'{{ let b = {s_}; c.x[{d_}] = (c.x[{d_}] & 0xFFFF_FFFF_FFFF_FFFFu128) | (b << 64); }}', False
        return f'{{ let b = {s_}; c.x[{d_}] = (c.x[{d_}] >> 64) | ((b >> 64) << 64); }}', False
    if m in ('psrld', 'pslld', 'psrad') and ops[1].type == X86_OP_IMM:
        d_ = xi(rname(x, ops[0]))
        return f'c.x[{d_}] = super::rt::ilane::{m}(c.x[{d_}], {ops[1].imm}u64);', False
    if m in ('pcmpeqd', 'pcmpgtd', 'paddd', 'psubd'):
        d_ = xi(rname(x, ops[0]))
        return f'{{ let b = {rd_x(x, ops[1])}; c.x[{d_}] = super::rt::ilane::{m}(c.x[{d_}], b); }}', False
    if m in ('movntps', 'movntdq', 'movntpd'):
        i = xi(rname(x, ops[1]))
        return f'{{ let a = {addr_expr(x, ops[0])}; c.mem.w128(a, c.x[{i}]); }}', False
    if m == 'rcpps':
        d_ = xi(rname(x, ops[0]))
        return f'c.x[{d_}] = super::rt::avx::rcp_ps({rd_x(x, ops[1])});', False
    if m == 'mov' or m == 'movabs':
        if ops[0].type == X86_OP_REG and is_xmm(rname(x, ops[0])):
            raise Unsupported('mov xmm')
        return wr_int(x, ops[0], rd_int(x, ops[1], op_bits(ops[0]))), False
    if m == 'movzx':
        return wr_int(x, ops[0], rd_int(x, ops[1])), False
    if m in ('movsxd', 'movsx'):
        sb = op_bits(ops[1])
        v = f'(({rd_int(x, ops[1])} as u{sb} as i{sb}) as i64 as u64)'
        return wr_int(x, ops[0], v), False
    if m == 'lea':
        return wr_int(x, ops[0], addr_expr(x, ops[1])), False
    if m in ('add', 'sub', 'cmp', 'and', 'or', 'xor', 'test'):
        b = op_bits(ops[0])
        a = rd_int(x, ops[0])
        s = rd_int(x, ops[1], b)
        if ops[1].type == X86_OP_IMM:
            s = f'{ops[1].imm & mask(b):#x}u64'
        if m in ('xor',) and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG and \
                rname(x, ops[0]) == rname(x, ops[1]):
            return f'c.fl_logic(0, {b}); ' + wr_int(x, ops[0], '0u64'), False
        if m == 'add':
            return f'{{ let p = {a}; let q = {s}; let r = c.fl_add(p, q, {b}); {wr_int(x, ops[0], "r")} }}', False
        if m == 'sub':
            return f'{{ let p = {a}; let q = {s}; let r = c.fl_sub(p, q, {b}); {wr_int(x, ops[0], "r")} }}', False
        if m == 'cmp':
            return f'{{ let p = {a}; let q = {s}; c.fl_sub(p, q, {b}); }}', False
        op = {'and': '&', 'or': '|', 'xor': '^', 'test': '&'}[m]
        if m == 'test':
            return f'{{ let p = {a}; let q = {s}; c.fl_logic(p {op} q, {b}); }}', False
        return f'{{ let p = {a}; let q = {s}; let r = (p {op} q) & {mask(b):#x}u64; c.fl_logic(r, {b}); {wr_int(x, ops[0], "r")} }}', False
    if m in ('inc', 'dec'):
        b = op_bits(ops[0])
        return f'{{ let p = {rd_int(x, ops[0])}; let r = c.fl_incdec(p, {str(m == "inc").lower()}, {b}); {wr_int(x, ops[0], "r")} }}', False
    if m == 'neg':
        b = op_bits(ops[0])
        return f'{{ let p = {rd_int(x, ops[0])}; let r = c.fl_sub(0, p, {b}); {wr_int(x, ops[0], "r")} }}', False
    if m == 'not':
        b = op_bits(ops[0])
        return wr_int(x, ops[0], f'(!{rd_int(x, ops[0])}) & {mask(b):#x}u64'), False
    if m in ('shl', 'shr', 'sar', 'sal'):
        b = op_bits(ops[0])
        if len(ops) == 1:
            cnt = '1u64'
        elif ops[1].type == X86_OP_IMM:
            cnt = f'{ops[1].imm:#x}u64'
        else:
            cnt = '(c.r[1] as u8 as u64)'
        cm = 63 if b == 64 else 31
        a = rd_int(x, ops[0])
        if m in ('shl', 'sal'):
            expr = f'(v << n) & {mask(b):#x}u64'
            cfe = f'(v >> ({b} - n)) & 1 == 1'
        elif m == 'shr':
            expr = 'v >> n'
            cfe = '(v >> (n - 1)) & 1 == 1'
        else:
            expr = f'((((v << (64 - {b})) as i64) >> (64 - {b})) >> n) as u64 & {mask(b):#x}u64'
            cfe = f'((((v << (64 - {b})) as i64) >> (64 - {b})) >> (n - 1)) & 1 == 1'
        return (f'{{ let v = {a}; let n = {cnt} & {cm}; if n != 0 {{ let r = {expr}; '
                f'let cf = {cfe}; c.fl_logic(r, {b}); c.cf = cf; {wr_int(x, ops[0], "r")} }} }}'), False
    if m == 'imul':
        b = op_bits(ops[0])
        if len(ops) == 3:
            a, s = rd_int(x, ops[1]), f'{ops[2].imm & mask(b):#x}u64'
        elif len(ops) == 2:
            a, s = rd_int(x, ops[0]), rd_int(x, ops[1])
        else:
            raise Unsupported('imul 1op')
        return (f'{{ let p = (({a} as u{b} as i{b}) as i128) * (({s} as u{b} as i{b}) as i128); '
                f'let r = (p as u64) & {mask(b):#x}u64; let ov = p != ((r as u{b} as i{b}) as i128); '
                f'c.fl_logic(r, {b}); c.cf = ov; c.of = ov; {wr_int(x, ops[0], "r")} }}'), False
    if m == 'mul' and len(ops) == 1:
        b = op_bits(ops[0])
        if b != 64:
            raise Unsupported('mul !64')
        return (f'{{ let p = (c.r[0] as u128) * ({rd_int(x, ops[0])} as u128); c.r[0] = p as u64; c.r[2] = (p >> 64) as u64; '
                f'let ov = c.r[2] != 0; c.cf = ov; c.of = ov; }}'), False
    if m == 'div':
        b = op_bits(ops[0])
        if b != 64:
            raise Unsupported('div !64')
        return (f'{{ let dv = {rd_int(x, ops[0])}; let n = ((c.r[2] as u128) << 64) | c.r[0] as u128; '
                f'assert!(dv != 0, "div por zero em 0x{x.address:X}"); '
                f'c.r[0] = (n / dv as u128) as u64; c.r[2] = (n % dv as u128) as u64; }}'), False
    if m == 'cdq':
        return 'c.r[2] = if (c.r[0] as u32 as i32) < 0 { 0xFFFF_FFFF } else { 0 };', False
    if m == 'cqo':
        return 'c.r[2] = if (c.r[0] as i64) < 0 { u64::MAX } else { 0 };', False
    if m == 'cdqe':
        return 'c.r[0] = (c.r[0] as u32 as i32) as i64 as u64;', False
    if m == 'xchg':
        a, b = rd_int(x, ops[0]), rd_int(x, ops[1])
        return f'{{ let t0 = {a}; let t1 = {b}; {wr_int(x, ops[0], "t1")} {wr_int(x, ops[1], "t0")} }}', False
    if m == 'push':
        return f'{{ let v = {rd_int(x, ops[0], 64)}; c.push(v); }}', False
    if m == 'pop':
        return f'{{ let v = c.pop(); {wr_int(x, ops[0], "v")} }}', False
    if m.startswith('set'):
        cc = m[3:]
        return wr_int(x, ops[0], f'({COND[cc]} as u64)'), False
    if m.startswith('cmov'):
        cc = m[4:]
        return f'if {COND[cc]} {{ {wr_int(x, ops[0], rd_int(x, ops[1]))} }} else if {op_bits(ops[0])} == 32 {{ {wr_int(x, ops[0], rd_int(x, ops[0]))} }}', False
    # ---------------- controle ----------------
    if m == 'ret':
        return 'c.r[4] = c.r[4].wrapping_add(8); return;', True
    if m == 'call':
        op = ops[0]
        if op.type == X86_OP_IMM:
            t = op.imm
            calls.add(t)
            return f'c.push(0x{IMAGE_BASE + nxt:X}); super::call(c, 0x{t:X});', False
        if op.type == X86_OP_MEM and x.reg_name(op.mem.base) == 'rip':
            slot = x.address + x.size + op.mem.disp
            if IAT_LO <= slot < IAT_HI:  # import da CRT: handler por slot de IAT
                IMPORTS_USED.add(slot)
                return f'c.push(0x{IMAGE_BASE + nxt:X}); super::leaf::import(c, 0x{slot:X});', False
        tgt = rd_int(x, op, 64)
        return f'{{ let t = {tgt}; c.push(0x{IMAGE_BASE + nxt:X}); super::call_va(c, t, 0x{x.address:X}); }}', False
    if m == 'jmp':
        op = ops[0]
        if op.type == X86_OP_IMM:
            t = op.imm
            if t in inset:
                return f'pc = 0x{t:X}; continue;', True
            calls.add(t)
            notes.append(f'tail-jmp 0x{x.address:X} -> 0x{t:X}')
            return f'super::call(c, 0x{t:X}); return;', True
        if op.type == X86_OP_MEM and x.reg_name(op.mem.base) == 'rip':
            slot = x.address + x.size + op.mem.disp
            if IAT_LO <= slot < IAT_HI:  # thunk `jmp [IAT]`: o import consome o retorno do chamador
                IMPORTS_USED.add(slot)
                return f'super::leaf::import(c, 0x{slot:X}); return;', True
        tgt = rd_int(x, op, 64)
        if x.address in SWITCH:
            arms = ' | '.join(f'0x{t:X}' for t in sorted(set(SWITCH[x.address])))
            return (f'{{ let t = ({tgt}).wrapping_sub(0x{IMAGE_BASE:X}) as u32; match t {{ {arms} => {{ pc = t; continue; }} '
                    f'_ => panic!("alvo de switch fora da tabela em 0x{x.address:X}: 0x{{:X}}", t) }} }}'), True
        return f'{{ let t = {tgt}; super::call_va(c, t, 0x{x.address:X}); return; }}', True
    if m.startswith('j'):
        cc = m[1:]
        if cc not in COND:
            raise Unsupported(m)
        t = ops[0].imm
        if t not in inset:
            calls.add(t)
            notes.append(f'jcc-tail 0x{x.address:X} -> 0x{t:X}')
            return f'if {COND[cc]} {{ super::call(c, 0x{t:X}); return; }}', True
        return f'if {COND[cc]} {{ pc = 0x{t:X}; continue; }}', True
    # ---------------- SSE ----------------
    if m in ('movaps', 'movups', 'movdqa', 'movdqu', 'movapd', 'movupd', 'lddqu'):
        dst, src = ops
        if dst.type == X86_OP_MEM:
            return f'{{ let a = {addr_expr(x, dst)}; c.mem.w128(a, {rd_x(x, src)}); }}', False
        return f'c.x[{xi(rname(x, dst))}] = {rd_x(x, src)};', False
    if m in ('movss', 'movsd') and len(ops) == 2:
        nb = 4 if m == 'movss' else 8
        bits = nb * 8
        dst, src = ops
        if dst.type == X86_OP_MEM:
            return f'{{ let a = {addr_expr(x, dst)}; c.mem.w{bits}(a, c.x[{xi(rname(x, src))}] as u{bits}); }}', False
        d_ = xi(rname(x, dst))
        if src.type == X86_OP_MEM:
            return f'c.x[{d_}] = c.mem.r{bits}({addr_expr(x, src)}) as u128;', False
        mk = (1 << bits) - 1
        return f'c.x[{d_}] = (c.x[{d_}] & !{mk:#x}u128) | (c.x[{xi(rname(x, src))}] & {mk:#x}u128);', False
    if m in ('movd', 'movq'):
        bits = 32 if m == 'movd' else 64
        dst, src = ops
        dn = rname(x, dst) if dst.type == X86_OP_REG else None
        sn = rname(x, src) if src.type == X86_OP_REG else None
        if dn and is_xmm(dn):
            if sn and is_xmm(sn):
                return f'c.x[{xi(dn)}] = c.x[{xi(sn)}] & {mask(bits):#x}u128;', False
            return f'c.x[{xi(dn)}] = ({rd_int(x, src)} & {mask(bits):#x}u64) as u128;', False
        # destino inteiro/memória a partir de xmm
        return wr_int(x, dst, f'(c.x[{xi(sn)}] as u{bits} as u64)'), False
    if m in ('xorps', 'xorpd', 'pxor', 'andps', 'andpd', 'pand', 'orps', 'orpd', 'por', 'andnps', 'pandn'):
        d_ = xi(rname(x, ops[0]))
        s = rd_x(x, ops[1])
        if m in ('andnps', 'pandn'):
            return f'c.x[{d_}] = !c.x[{d_}] & {s};', False
        op = {'x': '^', 'p': None}.get(m[0])
        o = '^' if 'xor' in m else ('&' if 'and' in m else '|')
        return f'c.x[{d_}] = c.x[{d_}] {o} {s};', False
    if m in SS2:
        d_ = xi(rname(x, ops[0]))
        suf = m[-2:]
        nb = SCALAR_BYTES.get(suf, 16) if m[-2] == 's' else 16
        if m.endswith('ps') or m.endswith('pd'):
            nb = 16
        return f'c.x[{d_}] = super::rt::sse::{SS2[m]}(c.x[{d_}], {rd_x(x, ops[1], nb)});', False
    if m in ('comiss', 'ucomiss', 'comisd', 'ucomisd'):
        nb = 4 if m.endswith('ss') else 8
        f = 'cmp_ss' if nb == 4 else 'cmp_sd'
        return f'{{ let (u, lt, eq) = super::rt::sse::{f}({rd_x(x, ops[0])}, {rd_x(x, ops[1], nb)}); c.fl_comi(u, lt, eq); }}', False
    if m == 'cvtss2sd':
        d_ = xi(rname(x, ops[0]))
        return f'c.x[{d_}] = super::rt::sse::cvtss2sd(c.x[{d_}], {rd_x(x, ops[1], 4)});', False
    if m == 'cvtsd2ss':
        d_ = xi(rname(x, ops[0]))
        return f'c.x[{d_}] = super::rt::sse::cvtsd2ss(c.x[{d_}], {rd_x(x, ops[1], 8)});', False
    if m in ('cvtps2pd', 'cvtpd2ps', 'cvtdq2ps', 'cvtdq2pd', 'cvttps2dq', 'cvtps2dq'):
        d_ = xi(rname(x, ops[0]))
        nb = 8 if m in ('cvtps2pd', 'cvtdq2pd') else 16
        return f'c.x[{d_}] = super::rt::sse::{m}({rd_x(x, ops[1], nb)});', False
    if m in ('cvtsi2ss', 'cvtsi2sd'):
        d_ = xi(rname(x, ops[0]))
        b = op_bits(ops[1])
        f = f'{m}{b}'
        return f'c.x[{d_}] = super::rt::sse::{f}(c.x[{d_}], {rd_int(x, ops[1])} as u{b} as i{b});', False
    if m in ('cvttss2si', 'cvttsd2si', 'cvtss2si', 'cvtsd2si'):
        b = op_bits(ops[0])
        nb = 4 if 'ss' in m else 8
        f = f'{m}{b}' if m.startswith('cvtt') else f'{m}32'
        return wr_int(x, ops[0], f'(super::rt::sse::{f}({rd_x(x, ops[1], nb)}) as u{b} as u64)'), False
    if m in ('pshufd', 'shufps'):
        d_ = xi(rname(x, ops[0]))
        if m == 'pshufd':
            return f'c.x[{d_}] = super::rt::sse::pshufd({rd_x(x, ops[1])}, {ops[2].imm});', False
        return f'c.x[{d_}] = super::rt::sse::shufps(c.x[{d_}], {rd_x(x, ops[1])}, {ops[2].imm});', False
    if m in ('unpcklps', 'unpckhps'):
        d_ = xi(rname(x, ops[0]))
        return f'c.x[{d_}] = super::rt::sse::{m}(c.x[{d_}], {rd_x(x, ops[1])});', False
    if m in ('psrldq', 'pslldq'):
        d_ = xi(rname(x, ops[0]))
        n = ops[1].imm
        if n >= 16:
            return f'c.x[{d_}] = 0;', False
        o = '>>' if m == 'psrldq' else '<<'
        return f'c.x[{d_}] = c.x[{d_}] {o} {8 * n};', False
    if m in ('psllq', 'psrlq') and ops[1].type == X86_OP_IMM:
        d_ = xi(rname(x, ops[0]))
        n = ops[1].imm
        o = '<<' if m == 'psllq' else '>>'
        return (f'{{ let l = super::rt::sse::lanes64(c.x[{d_}]); c.x[{d_}] = if {n} >= 64 {{ 0 }} else '
                f'{{ super::rt::sse::from64([l[0] {o} {n}, l[1] {o} {n}]) }}; }}'), False
    if m in ('paddq', 'psubq'):
        d_ = xi(rname(x, ops[0]))
        f = 'wrapping_add' if m == 'paddq' else 'wrapping_sub'
        return (f'{{ let a = super::rt::sse::lanes64(c.x[{d_}]); let b = super::rt::sse::lanes64({rd_x(x, ops[1])}); '
                f'c.x[{d_}] = super::rt::sse::from64([a[0].{f}(b[0]), a[1].{f}(b[1])]); }}'), False
    if m in ('paddd', 'psubd'):
        d_ = xi(rname(x, ops[0]))
        f = 'wrapping_add' if m == 'paddd' else 'wrapping_sub'
        return (f'{{ let a = super::rt::sse::lanes32(c.x[{d_}]); let b = super::rt::sse::lanes32({rd_x(x, ops[1])}); '
                f'c.x[{d_}] = super::rt::sse::from32([a[0].{f}(b[0]), a[1].{f}(b[1]), a[2].{f}(b[2]), a[3].{f}(b[3])]); }}'), False
    if m in ('movlhps', 'movhlps'):
        d_ = xi(rname(x, ops[0]))
        s_ = xi(rname(x, ops[1]))
        if m == 'movlhps':  # dst[127:64] = src[63:0]
            return f'c.x[{d_}] = (c.x[{d_}] & 0xFFFF_FFFF_FFFF_FFFFu128) | (c.x[{s_}] << 64);', False
        return f'c.x[{d_}] = (c.x[{d_}] & !0xFFFF_FFFF_FFFF_FFFFu128) | (c.x[{s_}] >> 64);', False
    if m == 'pmovsxdq':
        d_ = xi(rname(x, ops[0]))
        return (f'{{ let l = super::rt::sse::lanes32({rd_x(x, ops[1], 8)}); '
                f'c.x[{d_}] = super::rt::sse::from64([l[0] as i32 as i64 as u64, l[1] as i32 as i64 as u64]); }}'), False
    raise Unsupported(m)


def is_tail(entry, t):
    return t != entry and (t in REAL_ENTRY or t in GIANT or not in_region(t))


SWITCH = {}  # endereço do `jmp reg` -> lista de alvos (jump table MSVC)


def switch_targets(seen, x):
    """Jump table MSVC, padrão estrito:
         cmp rI32, N ; ja/jae ... ; lea rB, [rip - base] (RVA 0) ;
         mov r32, [rB + rI*4 + tab] ; add r64, rB ; jmp r64
    Entradas = RVAs int32. Só aceita se todos os alvos caem na mesma região traduzida,
    a menos de 64 KiB do salto. Senão devolve None (o salto vira call_va e para com RVA)."""
    prev = [seen[k] for k in sorted(seen) if k < x.address][-16:]
    if len(prev) < 3:
        return None
    jr = x.reg_name(x.operands[0].reg)
    add = prev[-1]
    if add.mnemonic != 'add' or len(add.operands) != 2 or add.operands[0].type != X86_OP_REG or \
            add.reg_name(add.operands[0].reg) != jr or add.operands[1].type != X86_OP_REG:
        return None
    rb = add.reg_name(add.operands[1].reg)
    base_ok = tab = n = None
    for y in reversed(prev[:-1]):
        ops = y.operands
        if base_ok is None and y.mnemonic == 'lea' and len(ops) == 2 and ops[0].type == X86_OP_REG and \
                y.reg_name(ops[0].reg) == rb and ops[1].type == X86_OP_MEM and \
                y.reg_name(ops[1].mem.base) == 'rip':
            base_ok = (y.address + y.size + ops[1].mem.disp) == 0
        if tab is None and y.mnemonic == 'mov' and len(ops) == 2 and ops[1].type == X86_OP_MEM and \
                ops[1].mem.scale == 4 and ops[1].mem.index and ops[1].mem.base and \
                y.reg_name(ops[1].mem.base) == rb:
            tab = ops[1].mem.disp
        if n is None and y.mnemonic == 'cmp' and len(ops) == 2 and ops[1].type == X86_OP_IMM:
            n = ops[1].imm + 1
    if not base_ok or tab is None or n is None or not (0 < n <= 1024):
        return None
    ts = [struct.unpack_from('<i', d, tab + 4 * k)[0] for k in range(n)]
    if not all(in_region(t) and abs(t - x.address) < 0x10000 for t in ts):
        return None
    return ts


def discover(entry):
    """Descida recursiva: instruções alcançáveis a partir de entry."""
    seen = {}
    work = [entry]
    while work:
        a = work.pop()
        while a not in seen:
            x = next(md.disasm(d[a:a + 16], a), None)
            if x is None:
                raise SystemExit(f'falha de desmontagem em 0x{a:X}')
            seen[a] = x
            m = x.mnemonic
            if m.startswith('j') and x.operands and x.operands[0].type == X86_OP_IMM:
                t = x.operands[0].imm
                if not is_tail(entry, t):
                    work.append(t)
                if m == 'jmp':
                    break
            elif m == 'jmp' and x.operands and x.operands[0].type == X86_OP_REG:
                ts = switch_targets(seen, x)
                if ts:
                    SWITCH[x.address] = ts
                    work += ts
                break
            elif m == 'jmp' or m == 'ret' or m == 'int3':
                break
            a = x.address + x.size
    return [seen[k] for k in sorted(seen)]


def lift_function(entry):
    insns = discover(entry)
    lo, hi = entry, max(x.address + x.size for x in insns)
    inset = {x.address for x in insns}
    leaders = {entry}
    prev_end = None
    for x in insns:
        if prev_end is not None and x.address != prev_end:
            leaders.add(x.address)  # descontinuidade
        if x.mnemonic.startswith('j') and x.operands and x.operands[0].type == X86_OP_IMM:
            t = x.operands[0].imm
            if t in inset:
                leaders.add(t)
            leaders.add(x.address + x.size)
        if x.mnemonic in ('ret', 'int3', 'jmp'):
            leaders.add(x.address + x.size)
        for t in SWITCH.get(x.address, []):
            leaders.add(t)
        prev_end = x.address + x.size
    calls, notes = set(), []
    out = [f'/// `0x{entry:X}` ({len(insns)} instruções, até 0x{hi:X}).',
           f'pub fn f_{entry:x}(c: &mut Cpu) {{',
           f'    let mut pc: u32 = 0x{entry:X};',
           '    loop {',
           '        match pc {']
    open_block = False
    unsupported = []
    prev_end = None
    for x in insns:
        if x.address in leaders:
            if open_block:
                if prev_end in inset:
                    out.append(f'                pc = 0x{prev_end:X}; continue;')
                else:
                    out.append(f'                panic!("queda para fora do corpo em 0x{prev_end:X}");')
                out.append('            }')
            out.append(f'            0x{x.address:X} => {{ super::rt::set_cur(0x{x.address:X});')
            open_block = True
        try:
            code, _ = lift_insn(x, entry, inset, calls, notes)
        except (Unsupported, ValueError, IndexError, KeyError) as e:
            txt_ = f'{x.mnemonic} {x.op_str} ({e})'.replace('{', '{{').replace('}', '}}').replace('"', "'")
            code = f'panic!("NÃO SUPORTADO 0x{x.address:X}: {txt_}");'
            unsupported.append(f'0x{x.address:X} {x.mnemonic} {x.op_str} ({e})')
        txt = f'{x.mnemonic} {x.op_str}'
        out.append(f'                c.icount += 1; {code} // {x.address:08X} {txt}' if code
                   else f'                // {x.address:08X} {txt}')
        prev_end = x.address + x.size
    if open_block:
        out.append(f'                panic!("queda após 0x{prev_end:X}");')
        out.append('            }')
    out.append('            _ => panic!("pc fora de bloco: 0x{:X}", pc),')
    out.append('        }')
    out.append('    }')
    out.append('}')
    return '\n'.join(out), calls, notes, unsupported, len(insns)


def static_indirect_targets(entry):
    """Alvos de saltos/calls indiretos lidos do dump (só para decidir o que traduzir;
    em tempo de execução o despacho lê a memória emulada):
      - stub IPP: movsxd rax,[rip+idx]; lea r10,[rip+tab]; jmp [r10+rax*8]
      - stub de math: mov rax,[rip+p]; jmp rax   /   jmp/call [rip+p]
    """
    out = []
    insns = discover(entry)
    for k, x in enumerate(insns):
        m, ops = x.mnemonic, x.operands
        if m in ('jmp', 'call') and ops and ops[0].type == X86_OP_MEM:
            mm = ops[0].mem
            base = x.reg_name(mm.base) if mm.base else None
            if base == 'rip':
                p = x.address + x.size + mm.disp
                if not (IAT_LO <= p < IAT_HI):
                    out.append(struct.unpack_from('<Q', d, p)[0] - IMAGE_BASE)
            elif base == 'r10' and k >= 2 and insns[k - 2].mnemonic == 'movsxd':
                a0, a1 = insns[k - 2], insns[k - 1]
                idx = a0.address + a0.size + a0.operands[1].mem.disp
                tab = a1.address + a1.size + a1.operands[1].mem.disp
                i = struct.unpack_from('<i', d, idx)[0]
                out.append(struct.unpack_from('<Q', d, tab + 8 * i)[0] - IMAGE_BASE)
        if m == 'jmp' and ops and ops[0].type == X86_OP_REG and k >= 1:
            p0 = insns[k - 1]
            if p0.mnemonic == 'mov' and p0.operands[1].type == X86_OP_MEM and \
                    x.reg_name(p0.operands[1].mem.base) == 'rip':
                p = p0.address + p0.size + p0.operands[1].mem.disp
                out.append(struct.unpack_from('<Q', d, p)[0] - IMAGE_BASE)
    return out


def main():
    import os
    outp = sys.argv[1]
    roots = [int(a, 16) for a in sys.argv[2:]]
    # LIFT_EXCLUDE=<gen base .rs>: não retraduz o que já está no crate base.
    # LIFT_PREFIX=<caminho>: prefixo do runtime (padrão `super::`; no crate extra,
    # `soultree_lifted::`).
    prefix = os.environ.get('LIFT_PREFIX', 'super::')
    excluded = set()
    if os.environ.get('LIFT_EXCLUDE'):
        txt = open(os.environ['LIFT_EXCLUDE'], encoding='utf-8').read()
        excluded = {int(h, 16) for h in re.findall(r'pub fn f_([0-9a-f]+)\(', txt)}
    todo, done = list(roots), {}
    leaves = collections.Counter()
    allunsup, allnotes = [], []
    while todo:
        f = todo.pop()
        if f in done or f in excluded:
            continue
        if not in_region(f):
            leaves[f] += 1
            continue
        code, calls, notes, unsup, n = lift_function(f)
        done[f] = (code, n)
        allunsup += unsup
        allnotes += notes
        if os.environ.get('LIFT_NOFOLLOW'):
            continue  # só as raízes; chamadas são resolvidas em execução
        todo += sorted(calls)
        for t in static_indirect_targets(f):
            allnotes.append(f'indireto resolvido pelo dump em 0x{f:X} -> 0x{t:X}')
            todo.append(t)
    hdr = ['//! GERADO por tools/lift/lift.py a partir do dump (não editar à mão).',
           f'//! Raízes: {", ".join(f"0x{r:X}" for r in roots)}.',
           f'//! {len(done)} funções, {sum(n for _, n in done.values())} instruções.',
           '#![allow(unused_mut, unused_variables, unreachable_code, unused_braces, clippy::all)]',
           'use super::rt::Cpu;', '']
    body = [done[f][0] for f in sorted(done)]
    disp = ['', '/// Funções traduzidas neste arquivo.',
            'pub fn lifted(rva: u32) -> Option<fn(&mut Cpu)> {', '    Some(match rva {']
    for f in sorted(done):
        disp.append(f'        0x{f:X} => f_{f:x},')
    disp += ['        _ => return None,', '    })', '}']
    names = import_names()
    disp += ['', '/// Imports alcançados pelo código traduzido (slot de IAT -> nome), lidos do dump.',
             "pub fn import_name(slot: u32) -> Option<&'static str> {", '    Some(match slot {']
    for sl in sorted(IMPORTS_USED):
        dll, nm = names.get(sl, ('?', '?'))
        disp.append(f'        0x{sl:X} => "{nm}", // {dll}')
    disp += ['        _ => return None,', '    })', '}']
    out_txt = '\n'.join(hdr + body + disp) + '\n'
    if prefix != 'super::':
        out_txt = out_txt.replace('super::', prefix)
    open(outp, 'w', encoding='utf-8').write(out_txt)
    print(f'{len(done)} funções, {sum(n for _, n in done.values())} instruções -> {outp}')
    print('folhas:', ' '.join(f'0x{k:X}' for k in sorted(leaves)))
    print(f'não suportadas: {len(allunsup)}')
    for u in allunsup:
        print('  ', u)
    for nn in allnotes:
        print('  ', nn)


if __name__ == '__main__':
    main()
