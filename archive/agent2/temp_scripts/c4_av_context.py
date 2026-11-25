"""C4 — 12 patches + VEH ctypes que captura [rsp-8]/[rsp-16] no AV em -0x90.
SOMENTE LEITURA + EXPERIMENTO EM MEMORIA. Nada escrito no repo.
"""
import ctypes as C
import json
import struct
import sys
from ctypes import wintypes as W
from pathlib import Path

TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
DEV = json.loads((TMP / 'c3_deviations.json').read_text())
SITES = sorted([r for r in DEV
                if 0x460650 <= int(r['site_rva'], 16) <= 0x460700 and r['status'] == 'fixable'],
               key=lambda r: int(r['site_rva'], 16))
assert len(SITES) == 12
RUN = sys.argv[1] if len(sys.argv) > 1 else '1'
LOG = TMP / f'c4_av_context_{RUN}.txt'
META = TMP / f'c4_av_context_{RUN}.json'
LOG.write_text('', encoding='utf-8')

k32 = C.WinDLL('kernel32', use_last_error=True)
k32.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, W.DWORD, C.POINTER(W.DWORD)]
k32.VirtualProtect.restype = W.BOOL
k32.AddVectoredExceptionHandler.restype = C.c_void_p
k32.AddVectoredExceptionHandler.argtypes = [W.ULONG, C.c_void_p]
k32.GetCurrentThreadStackLimits.argtypes = [C.POINTER(C.c_size_t),
                                            C.POINTER(C.c_size_t)]
k32.GetCurrentThreadId.restype = W.DWORD


def limits():
    lo, hi = C.c_size_t(), C.c_size_t()
    k32.GetCurrentThreadStackLimits(C.byref(lo), C.byref(hi))
    return lo.value, hi.value


class ER(C.Structure):
    _fields_ = [('code', W.DWORD), ('flags', W.DWORD), ('rec', C.c_void_p),
                ('addr', C.c_void_p), ('n', W.DWORD), ('u', W.DWORD),
                ('info', C.c_void_p * 15)]


class CTX(C.Structure):
    _fields_ = [(n, C.c_uint64) for n in ('P1','P2','P3','P4','P5','P6')] + [
        ('flags', C.c_uint32), ('mxcsr', C.c_uint32)] + [
        (n, C.c_uint16) for n in ('cs','ds','es','fs','gs','ss')] + [
        ('eflags', C.c_uint32)] + [
        (n, C.c_uint64) for n in ('dr0','dr1','dr2','dr3','dr6','dr7')] + [
        (n, C.c_uint64) for n in ('rax','rcx','rdx','rbx','rsp','rbp','rsi','rdi',
                                   'r8','r9','r10','r11','r12','r13','r14','r15','rip')]


class EP(C.Structure):
    _fields_ = [('er', C.POINTER(ER)), ('ctx', C.POINTER(CTX))]


def q(a):
    try:
        return C.string_at(a, 8)
    except Exception:
        return b'\0' * 8


def handler(arg):
    p = C.cast(arg, C.POINTER(EP)).contents
    er, c = p.er.contents, p.ctx.contents
    code = er.code & 0xffffffff
    if code not in (0xc0000005, 0x80000003, 0xc0000094):
        return 0
    regs = {n: getattr(c, n) for n in ('rip','rsp','rbp','rax','rcx','rdx','rbx',
            'rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15')}
    with LOG.open('a', encoding='utf-8') as f:
        lo, hi = limits()
        f.write('EVENT code=%#x addr=%#x info0=%#x info1=%#x tid=%d '
                'stacklo=%#x stackhi=%#x slot=%#x slot_off=%#x\n' % (
            code, er.addr or 0, er.info[0] or 0,
            er.info[1] if er.n >= 2 else 0, k32.GetCurrentThreadId(),
            lo, hi, c.rsp - 8, (c.rsp - 8) - lo))
        f.write('  regs ' + ' '.join('%s=%#x' % (k, v) for k, v in regs.items()) + '\n')
        f.write('  stack(rsp-0x40..rsp+0x80):\n')
        for off in range(-0x40, 0x88, 8):
            v = struct.unpack('<Q', q(c.rsp + off))[0]
            f.write('    rsp%+#05x = %#018x\n' % (off, v))
        if code == 0x80000003:
            f.write('  rip_bytes_before ' + (C.string_at(c.rip - 16, 16).hex(' ')
                    if c.rip >= 0x10000 else '?') + '\n')
        f.flush()
    return 0


CB = C.CFUNCTYPE(C.c_long, C.c_void_p)(handler)
k32.AddVectoredExceptionHandler(1, C.cast(CB, C.c_void_p))

meta = {'run': RUN, 'phase': 'loading'}
META.write_text(json.dumps(meta), encoding='utf-8')
lib = C.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = C.cast(lib._handle, C.c_void_p).value
lib.RecoveredInit()
meta['base'] = hex(BASE)
for r in SITES:
    site = BASE + int(r['site_rva'], 16) + 2
    old = W.DWORD()
    assert k32.VirtualProtect(C.c_void_p(site), 4, 0x40, C.byref(old))
    C.memmove(site, C.create_string_buffer(bytes.fromhex(r['fix_disp32']), 4), 4)
    back = W.DWORD()
    assert k32.VirtualProtect(C.c_void_p(site), 4, old.value, C.byref(back))
meta['phase'] = 'calling'
META.write_text(json.dumps(meta), encoding='utf-8')

calls = [0]


def bump():
    calls[0] += 1
    if calls[0] == 1:
        with LOG.open('a', encoding='utf-8') as f:
            local = C.c_void_p()
            lo, hi = limits()
            f.write('FIRST_CALLBACK local_addr=%#x tid=%d stacklo=%#x stackhi=%#x\n'
                    % (C.addressof(local), k32.GetCurrentThreadId(), lo, hi))


def cb_reg(a, b, c_, d):
    bump()
    return 1


def cb_evt(a):
    bump()
    return 1


f1 = C.CFUNCTYPE(C.c_int, C.c_void_p, C.c_int, C.c_void_p, C.c_int)(cb_reg)
f2 = C.CFUNCTYPE(C.c_int, C.c_void_p)(cb_evt)
host = (C.c_ubyte * 0x80)()
for off, fn in ((0x18, f1), (0x20, f2)):
    C.memmove(C.byref(host, off),
              C.byref(C.c_void_p(C.cast(fn, C.c_void_p).value)), 8)
meta['host_addr'] = hex(C.addressof(host))
META.write_text(json.dumps(meta), encoding='utf-8')
cfg = (C.c_int32 * 64)(*([5] * 64))
lib.Audio_863170.restype = C.c_void_p
lib.Audio_863170.argtypes = [C.c_void_p, C.c_void_p, C.c_double]
ret = lib.Audio_863170(C.byref(host), C.byref(cfg), 48000.0)
meta.update(phase='returned', ret=hex(ret) if ret else 'NULL', callbacks=calls[0])
META.write_text(json.dumps(meta), encoding='utf-8')
print('returned', meta['ret'], calls[0])
