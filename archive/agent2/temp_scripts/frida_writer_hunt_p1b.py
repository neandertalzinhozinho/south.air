"""Frida P1 writer-hunt (external Popen + attach, MemoryAccessMonitor on slot).
Read-only; outputs to temp."""
import json, re, subprocess, sys, time, bisect
from pathlib import Path
import frida

TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
WORKER = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\worker_no_veh.py')
MAP = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.map')
OUT = TMP / 'frida_writer_hunt_p1b_report.txt'

AGENT = r"""
const RVA_CALLER = 0xF5977;
const RVA_CALLEE = 0x61565F;
const SLOT_OFF_FROM_ENTRY = 0x48;
const PAGE_MASK = ptr('0xfffffffffffff000');
let base=null, slot=null, monitoring=false, seq=0, writeCount=0;
function ev(o){ o.n=seq++; try{send(o);}catch(e){} }
function rvaOf(p){ if(!base||p.compare(base)<0) return null; return p.sub(base).toString(16); }
function readQ(p,n){ try{const u=new Uint8Array(p.readByteArray(n||8));let s='';for(let i=u.length-1;i>=0;i--)s+=('0'+u[i].toString(16)).slice(-2);return '0x'+s;}catch(e){return 'ERR:'+e.message;} }
function dumpCtx(c){return {rsp:c.rsp.toString(),rbp:c.rbp.toString(),r13:c.r13.toString(),r9:c.r9.toString(),rcx:c.rcx.toString(),rdx:c.rdx.toString(),r8:c.r8.toString()};}
function bt(c){try{return Thread.backtrace(c,Backtracer.ACCURATE).map(function(a){return {addr:a.toString(),rva:rvaOf(a)};});}catch(e){return ['btfail:'+e.message];}}

function installHooks(){
  ev({t:'hooks_installed',base:base.toString()});
  Interceptor.attach(base.add(RVA_CALLER),{
    onEnter(){
      const s=this.context.rsp.sub(SLOT_OFF_FROM_ENTRY);
      slot=s;
      ev({t:'caller_enter',slot:s.toString(),before:readQ(s,8),ctx:dumpCtx(this.context),bt:bt(this.context)});
      if(!monitoring){
        monitoring=true;
        try{
          const page=s.and(PAGE_MASK);
          MemoryAccessMonitor.enable({
            ranges:[{base:page,size:0x1000}],
            onAccess(d){
              try{
                if(!slot||!d.address.equals(slot))return;
                const r=rvaOf(d.from);
                let dis='?';try{const ins=Instruction.parse(d.from);dis=ins.mnemonic+' '+ins.opStr;}catch(e){}
                if(d.operation==='write')writeCount++;
                ev({t:'write_hit',op:d.operation,from_rva:r,from:d.from.toString(),disasm:dis,
                    value_after:readQ(slot,8),low4_after:readQ(slot,4)});
              }catch(e){ev({t:'access_cb_err',err:e.message});}
            }
          });
          ev({t:'mam_enabled',page:page.toString(),slot:s.toString()});
        }catch(e){ev({t:'mam_enable_failed',err:e.message});}
      }
    }
  });
  Interceptor.attach(base.add(RVA_CALLEE),{
    onEnter(){
      const s=this.context.rsp.add(0x28);
      ev({t:'callee_enter',slot:s.toString(),value:readQ(s,8),ctx:dumpCtx(this.context),bt:bt(this.context)});
    }
  });
}

try{
  Process.setExceptionHandler(function(d){
    try{ev({t:'exception',type:d.type,address:d.address?d.address.toString():null,
      pc:d.context?d.context.pc.toString():null,ctx:d.context?dumpCtx(d.context):null,
      slot:slot?slot.toString():null,slot_value:slot?readQ(slot,8):null,writes:writeCount});}catch(e){}
    return false;
  });
  function find(){
    for(const m of Process.enumerateModules()){
      if((m.path||'').toLowerCase().indexOf('recovered_dsp_test.dll')>=0){
        base=m.base;
        ev({t:'module_found',name:m.name,base:base.toString(),size:m.size.toString(),path:m.path});
        const ready=function(){
          let ok=false;try{base.add(RVA_CALLER).readByteArray(4);ok=true;}catch(e){}
          if(ok)installHooks();else{ev({t:'code_not_ready'});setTimeout(ready,100);}
        };
        setTimeout(ready,200);
        return true;
      }
    }
    return false;
  }
  const timer=setInterval(function(){if(find())clearInterval(timer);},10);
  find(); ev({t:'ready'});
}catch(e){ev({t:'agent_error',err:e.message,stack:e.stack});}
"""

syms=[]
for l in MAP.read_text(encoding='latin-1').splitlines():
    m=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?',l)
    if m:
        try:syms.append((int(m.group(2),16)-0x180000000,m.group(1)))
        except ValueError:pass
syms.sort(); starts=[s for s,_ in syms]
def sym(h):
    if not h:return ''
    r=int(h,16); i=bisect.bisect_right(starts,r)-1
    return (f'{syms[i][1]}+0x{r-starts[i]:x}' if i>=0 else f'?+0x{r:x}')

def main():
    OUT.write_text('',encoding='utf-8')
    proc=subprocess.Popen([sys.executable,str(WORKER)],cwd=str(WORKER.parent))
    print('worker pid',proc.pid,flush=True)
    dev=frida.get_local_device()
    session=dev.attach(proc.pid)
    script=session.create_script(AGENT)
    msgs=[]
    script.on('message',lambda m,d: msgs.append(m['payload'] if m['type']=='send' else {'t':'script_error','raw':str(m)}))
    script.load()
    print('attached+loaded, waiting...',flush=True)
    t=time.time()
    while time.time()-t<12 and not any(x.get('t')=='exception' or x.get('t')=='script_error' for x in msgs):
        time.sleep(0.2)
    try:proc.kill()
    except Exception:pass
    with OUT.open('a',encoding='utf-8') as fh:
        for m in msgs:
            k=m.get('t')
            if k=='write_hit':
                fh.write(f"WRITE op={m['op']} from_rva=0x{m['from_rva']} ({sym(m['from_rva'])}) "
                         f"insn={m['disasm']} value_after={m['value_after']} low4={m['low4_after']}\n")
            elif k in ('caller_enter','callee_enter'):
                fh.write(f"{k} slot={m.get('slot')} val={m.get('before') or m.get('value')} ctx={json.dumps(m.get('ctx'))}\n")
                fh.write(f"   bt={json.dumps([sym(x['rva']) if x.get('rva') else x.get('addr') for x in m.get('bt',[])] )}\n")
            elif k=='exception':
                fh.write(f"EXCEPTION type={m.get('type')} pc={m.get('pc')} ctx={json.dumps(m.get('ctx'))} "
                         f"slot={m.get('slot')} val={m.get('slot_value')} writes={m.get('writes')}\n")
            else:
                fh.write(f"{k} {json.dumps({a:b for a,b in m.items() if a!='t'})}\n")
    print(OUT.read_text(encoding='utf-8',errors='replace')[:12000],flush=True)

if __name__=='__main__':main()
