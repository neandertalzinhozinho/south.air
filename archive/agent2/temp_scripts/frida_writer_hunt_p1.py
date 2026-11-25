"""Frida P1 writer-hunt: find WHO writes DWORD 3 into the stack slot that
becomes R13 at dump_715c0+0x5f (AV). Read-only; spawns its own worker.

Outputs: C:/Users/tromb/AppData/Local/Temp/opencode/frida_writer_hunt_p1_report.txt
"""
import json
import re
import sys
import time
from pathlib import Path

import frida

TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
WORKER = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\worker_no_veh.py')
MAP = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.map')
OUT = TMP / 'frida_writer_hunt_p1_report.txt'

# built-DLL RVAs (from static disassembly / MAP)
RVA_CALLER = 0xF5977      # dump_6f360
RVA_CALLEE = 0x61565F     # dump_715c0 (AV function)
RVA_FACTORY = None        # resolved from export
CALLER_PROLOGUE = 0x68    # 4 pushes (0x20) + sub rsp,0x48 -> slot = entry_rsp-0x48
SLOT_OFF_FROM_ENTRY = 0x48

AGENT = r"""
const RVA_CALLER = 0xF5977;
const RVA_CALLEE = 0x61565F;
const SLOT_OFF_FROM_ENTRY = 0x48;
const PAGE_MASK = ptr('0xfffffffffffff000');

let base = null, size = 0, slot = null, monitoring = false;
let seq = 0, writeCount = 0;
const events = [];

function ev(o) { o.n = seq++; try { send(o); } catch (e) {} }

function rvaOf(p) {
    if (!base || p.compare(base) < 0) return null;
    return p.sub(base).toString(16);
}

function readQ(p, n) {
    try {
        const b = p.readByteArray(n || 8);
        const u = new Uint8Array(b);
        let s = '';
        for (let i = u.length - 1; i >= 0; i--) s += ('0' + u[i].toString(16)).slice(-2);
        return '0x' + s;
    } catch (e) { return 'ERR:' + e.message; }
}

function dumpCtx(ctx) {
    return {rsp: ctx.rsp.toString(), rbp: ctx.rbp.toString(),
            r13: ctx.r13.toString(), r9: ctx.r9.toString(),
            rcx: ctx.rcx.toString(), rdx: ctx.rdx.toString(),
            r8: ctx.r8.toString(), rip: ctx.rip.toString()};
}

function bt(ctx) {
    try {
        return Thread.backtrace(ctx, Backtracer.ACCURATE).map(function (a) {
            const r = rvaOf(a);
            return {addr: a.toString(), rva: r};
        });
    } catch (e) { return ['bt-fail:' + e.message]; }
}

function installHooks() {
    const caller = base.add(RVA_CALLER);
    const callee = base.add(RVA_CALLEE);
    ev({t: 'hooks_installed', base: base.toString(), caller: caller.toString(), callee: callee.toString()});

    Interceptor.attach(caller, {
        onEnter() {
            const entry = this.context.rsp;
            slot = entry.sub(SLOT_OFF_FROM_ENTRY);
            const before = readQ(slot, 8);
            ev({t: 'caller_enter', rva: 'f5977', slot: slot.toString(),
                before: before, ctx: dumpCtx(this.context), bt: bt(this.context)});

            if (!monitoring) {
                monitoring = true;
                try {
                    const page = slot.and(PAGE_MASK);
                    MemoryAccessMonitor.enable({
                        ranges: [{base: page, size: 0x1000}],
                        onAccess(details) {
                            try {
                                const a = details.address;
                                if (!slot || !a.equals(slot)) return;
                                const from = details.from;
                                const frva = rvaOf(from);
                                const row = {
                                    t: 'write_hit', op: details.operation,
                                    from: from.toString(), from_rva: frva,
                                    to: details.to ? details.to.toString() : null,
                                    value_after: readQ(slot, 8),
                                    low4_after: readQ(slot, 4)
                                };
                                try {
                                    row.disasm = Instruction.parse(from).mnemonic + ' ' + Instruction.parse(from).opStr;
                                } catch (e) { row.disasm = 'disasm-fail'; }
                                if (details.operation === 'write') writeCount++;
                                ev(row);
                            } catch (e) { ev({t: 'access_cb_err', err: e.message}); }
                        }
                    });
                    ev({t: 'mam_enabled', page: slot.and(PAGE_MASK).toString(), slot: slot.toString()});
                } catch (e) {
                    ev({t: 'mam_enable_failed', err: e.message});
                }
            }
        }
    });

    Interceptor.attach(callee, {
        onEnter() {
            const s = this.context.rsp.add(0x28);   // [callee entry rsp + 0x28] == caller [rsp+0x20]
            ev({t: 'callee_enter', rva: '61565f', slot_expect: s.toString(),
                r13_slot_before_read: readQ(s, 8), r9_slot: readQ(this.context.rsp.add(0x20), 8),
                ctx: dumpCtx(this.context), bt: bt(this.context)});
        }
    });
}

try {
    Process.setExceptionHandler(function (details) {
        try {
            ev({t: 'exception', type: details.type,
                address: details.address ? details.address.toString() : null,
                pc: details.context ? details.context.pc.toString() : null,
                ctx: details.context ? dumpCtx(details.context) : null,
                slot: slot ? slot.toString() : null,
                slot_value: slot ? readQ(slot, 8) : null,
                writeCount: writeCount});
        } catch (e) {}
        return false;
    });

    const findIt = function () {
        if (base) return true;
        for (const m of Process.enumerateModules()) {
            const n = (m.name || '').toLowerCase();
            if (n.indexOf('dsparse') !== -1 || n.indexOf('recovered_dsp') !== -1) {
                base = m.base; size = m.size;
                ev({t: 'module_found', name: m.name, base: base.toString(), size: size.toString()});
                // DLL sections may still be arriving; wait before placing code hooks.
                const tryInstall = function () {
                    let ok = false;
                    try { base.add(RVA_CALLER).readByteArray(4); ok = true; } catch (e) {}
                    if (ok) installHooks();
                    else {
                        ev({t: 'code_not_ready', err: 'retry'});
                        setTimeout(tryInstall, 200);
                    }
                };
                setTimeout(tryInstall, 400);
                return true;
            }
        }
        return false;
    };
    const timer = setInterval(function () {
        if (findIt()) clearInterval(timer);
    }, 20);
    findIt();
    ev({t: 'ready'});
} catch (e) {
    ev({t: 'agent_error', err: e.message, stack: e.stack});
}
"""

# symbol table
syms = []
for line in MAP.read_text(encoding='latin-1').splitlines():
    m = re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?', line)
    if m:
        try:
            syms.append((int(m.group(2), 16) - 0x180000000, m.group(1)))
        except ValueError:
            pass
syms.sort()
import bisect
starts = [s for s, _ in syms]

def sym(rva_hex):
    if rva_hex is None:
        return ''
    r = int(rva_hex, 16)
    i = bisect.bisect_right(starts, r) - 1
    if i < 0:
        return f'?+0x{r:x}'
    return f'{syms[i][1]}+0x{r - starts[i]:x}'

def main():
    OUT.write_text('', encoding='utf-8')
    dev = frida.get_local_device()
    pid = dev.spawn([sys.executable, str(WORKER)], cwd=str(WORKER.parent))
    session = dev.attach(pid)
    script = session.create_script(AGENT)
    messages = []

    def on_message(msg, data):
        if msg['type'] != 'send':
            line = f"SCRIPT_{msg['type']}: {msg.get('description') or msg.get('stack')}"
            messages.append({'t': 'script_error', 'raw': line})
        else:
            messages.append(msg['payload'])

    script.on('message', on_message)
    script.load()
    dev.resume(pid)

    deadline = time.time() + 35
    while time.time() < deadline:
        if any(m.get('t') == 'exception' or m.get('t') == 'script_error' for m in messages):
            break
        time.sleep(0.25)
    time.sleep(0.5)
    try:
        dev.kill(pid)
    except Exception:
        pass

    with OUT.open('a', encoding='utf-8') as fh:
        for m in messages:
            t = m.get('t')
            if t in ('write_hit', 'caller_enter', 'callee_enter', 'exception',
                     'hooks_installed', 'mam_enabled', 'mam_enable_failed',
                     'agent_error', 'ready', 'script_error'):
                if t == 'write_hit':
                    fh.write(f"[{m['n']:03d}] WRITE op={m.get('op')} from=0x{m.get('from_rva')}"
                             f" ({sym(m.get('from_rva'))}) insn={m.get('disasm')}"
                             f" value_after={m.get('value_after')} low4={m.get('low4_after')}\n")
                elif t in ('caller_enter', 'callee_enter'):
                    fh.write(f"[{m['n']:03d}] {t} slot={m.get('slot') or m.get('slot_expect')}"
                             f" before={m.get('before') or m.get('r13_slot_before_read')}"
                             f" ctx={json.dumps(m.get('ctx'))}\n")
                    fh.write(f"       bt={json.dumps([sym(x['rva']) if x.get('rva') else x.get('addr') for x in m.get('bt', [])])}\n")
                elif t == 'exception':
                    fh.write(f"[{m['n']:03d}] EXCEPTION type={m.get('type')} addr={m.get('address')}"
                             f" pc={m.get('pc')} ctx={json.dumps(m.get('ctx'))}"
                             f" slot={m.get('slot')} val={m.get('slot_value')} writes={m.get('writeCount')}\n")
                else:
                    fh.write(f"[{m.get('n','?')}] {t} {json.dumps({k:v for k,v in m.items() if k not in ('t','n')})}\n")
        fh.write('\n--- ALL RAW MESSAGES ---\n')
        for m in messages:
            fh.write(json.dumps(m) + '\n')
    print('report:', OUT)
    print(OUT.read_text(encoding='utf-8', errors='replace')[:8000])

if __name__ == '__main__':
    main()
