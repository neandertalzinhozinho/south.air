"""Frida writer-hunt: CREATE_SUSPENDED worker, attach, hook, resume."""
import ctypes, json, re, subprocess, sys, time, bisect
from pathlib import Path
import frida

TMP=Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
WORKER=Path(r'D:\PROJETOS\shadowFILES\analysis\scripts\p1_frida_delayed_worker.py')
MAP=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.map')
OUT=TMP/'frida_writer_hunt_p1c_report.txt'

AGENT=r"""
const RVA_CALLER=0xF5977, RVA_CALLEE=0x61565F, SLOT_OFF=0x48;
const PAGE_MASK=ptr('0xfffffffffffff000');
let base=null, slot=null, monitoring=false, seq=0, writes=0;
function ev(o){o.n=seq++;try{send(o);}catch(e){}}
function rvaOf(p){if(!base||p.compare(base)<0)return null;return p.sub(base).toString(16);}
function readQ(p,n){try{const u=new Uint8Array(p.readByteArray(n||8));let s='';for(let i=u.length-1;i>=0;i--)s+=('0'+u[i].toString(16)).slice(-2);return '0x'+s;}catch(e){return 'ERR:'+e.message;}}
function ctx(c){return {rsp:c.rsp.toString(),rbp:c.rbp.toString(),r13:c.r13.toString(),r9:c.r9.toString(),rcx:c.rcx.toString(),rdx:c.rdx.toString(),r8:c.r8.toString()};}
function bt(c){try{return Thread.backtrace(c,Backtracer.ACCURATE).map(function(a){return {addr:a.toString(),rva:rvaOf(a)};});}catch(e){return ['btfail:'+e.message];}}
function install(){
  ev({t:'hooks_installed',base:base.toString()});
  Interceptor.attach(base.add(RVA_CALLER),{
    onEnter(){
      const s=this.context.rsp.sub(SLOT_OFF); slot=s;
      ev({t:'caller_enter',slot:s.toString(),before:readQ(s,8),ctx:ctx(this.context),bt:bt(this.context)});
      if(!monitoring){ monitoring=true;
        try{
          const page=s.and(PAGE_MASK);
          MemoryAccessMonitor.enable({ranges:[{base:page,size:0x1000}],onAccess(d){
            try{
              if(!slot||!d.address.equals(slot))return;
              let dis='?';try{const ins=Instruction.parse(d.from);dis=ins.mnemonic+' '+ins.opStr;}catch(e){}
              if(d.operation==='write')writes++;
              ev({t:'write_hit',op:d.operation,from_rva:rvaOf(d.from),from:d.from.toString(),disasm:dis,
                  value_after:readQ(slot,8),low4:readQ(slot,4)});
            }catch(e){ev({t:'cb_err',err:e.message});}
          }});
          ev({t:'mam_enabled',page:page.toString(),slot:s.toString()});
        }catch(e){ev({t:'mam_failed',err:e.message});}
      }
    }
  });
  Interceptor.attach(base.add(RVA_CALLEE),{
    onEnter(){const s=this.context.rsp.add(0x28);
      ev({t:'callee_enter',slot:s.toString(),value:readQ(s,8),ctx:ctx(this.context),bt:bt(this.context)});}
  });
}
try{
  Process.setExceptionHandler(function(d){
    try{ev({t:'exception',type:d.type,addr:d.address?d.address.toString():null,
      pc:d.context?d.context.pc.toString():null,ctx:d.context?ctx(d.context):null,
      slot:slot?slot.toString():null,val:slot?readQ(slot,8):null,writes:writes});}catch(e){}
    return false;
  });
  let attempts=0;
  const onModule=function(m){
    if(base)return;
    if((m.path||'').toLowerCase().indexOf('recovered_dsp_test.dll')>=0){
      base=m.base;
      ev({t:'module_found',name:m.name,base:base.toString(),size:m.size.toString(),path:m.path,attempts:attempts});
      setTimeout(install,150);
    }
  };
  try{Process.attachModuleObserver({onAdded:onModule});}catch(e){ev({t:'observer_err',err:e.message});}
  const timer=setInterval(function(){
    attempts++;
    for(const m of Process.enumerateModules()) onModule(m);
    if(base){clearInterval(timer);return;}
    if(attempts===500){ev({t:'allmods',list:Process.enumerateModules().map(function(m){return {n:m.name,b:m.base.toString(),s:m.size.toString(),p:m.path};})});}
    if(attempts%50===0)ev({t:'poll',attempts:attempts,mods:Process.enumerateModules().length});
    if(attempts>2000){clearInterval(timer);ev({t:'module_timeout'});}
  },10);
  ev({t:'ready'});
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
    p=subprocess.Popen([sys.executable,str(WORKER)],cwd=str(WORKER.parent),stderr=subprocess.PIPE)
    print('worker pid',p.pid,flush=True)
    dev=frida.get_local_device(); s=dev.attach(p.pid)
    sc=s.create_script(AGENT); msgs=[]
    sc.on('message',lambda m,d: msgs.append(m['payload'] if m['type']=='send' else {'t':'script_error','raw':str(m)}))
    sc.load(); print('script loaded; worker runs on its own',flush=True)
    t=time.time()
    while time.time()-t<18 and not any(x.get('t') in ('exception','script_error') for x in msgs):
        time.sleep(0.2)
    try:p.kill()
    except:pass
    try:err=p.stderr.read().decode(errors='replace')[:300]
    except:err=''
    with OUT.open('a',encoding='utf-8') as fh:
        fh.write(f'worker_stderr={err!r}\n')
        for m in msgs:
            k=m.get('t')
            if k=='write_hit':
                fh.write(f"WRITE op={m['op']} from=0x{m['from_rva']} ({sym(m['from_rva'])}) insn={m['disasm']} "
                         f"val_after={m['value_after']} low4={m['low4']}\n")
            elif k in ('caller_enter','callee_enter'):
                fh.write(f"{k} slot={m.get('slot')} val={m.get('before') or m.get('value')} ctx={json.dumps(m.get('ctx'))}\n")
                fh.write(f"   bt={json.dumps([sym(x['rva']) if x.get('rva') else x.get('addr') for x in m.get('bt',[])] )}\n")
            elif k=='exception':
                fh.write(f"EXCEPTION type={m.get('type')} pc={m.get('pc')} ctx={json.dumps(m.get('ctx'))} "
                         f"slot={m.get('slot')} val={m.get('val')} writes={m.get('writes')}\n")
            else:
                fh.write(f"{k} {json.dumps({a:b for a,b in m.items() if a!='t'})}\n")
    print(OUT.read_text(encoding='utf-8',errors='replace')[:16000],flush=True)
if __name__=='__main__':main()
