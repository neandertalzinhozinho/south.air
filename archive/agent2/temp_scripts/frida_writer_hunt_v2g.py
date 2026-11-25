"""DEFINITIVE writer-hunt: hook LoadLibraryW before the delayed worker loads
the DLL, capture base from return value, install Interceptor + MemoryAccessMonitor.
"""
import bisect, json, re, subprocess, sys, time
from pathlib import Path
import frida

TMP=Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
WORKER=Path(r'D:\PROJETOS\shadowFILES\analysis\scripts\p1_frida_delayed_worker.py')
MAP=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.map')
OUT=TMP/('frida_writer_hunt_v2f_%d.txt' % (time.time()*1000))

AGENT=r"""
const RVA_CALLER=0xD8977, RVA_CALLEE=0x5F865F, SLOT_OFF=0x48;
const PAGE_MASK=ptr('0xfffffffffffff000');
let base=null, slot=null, monitoring=false, seq=0, writes=0;
function ev(o){o.n=seq++;try{send(o);}catch(e){}}
function rvaOf(p){if(!base||p.compare(base)<0)return null;return p.sub(base).toString(16);}
function readQ(p,n){try{const u=new Uint8Array(p.readByteArray(n||8));let s='';for(let i=u.length-1;i>=0;i--)s+=('0'+u[i].toString(16)).slice(-2);return '0x'+s;}catch(e){return 'ERR:'+e.message;}}
function cx(c){return {rsp:c.rsp.toString(),rbp:c.rbp.toString(),r13:c.r13.toString(),r9:c.r9.toString(),rcx:c.rcx.toString(),rdx:c.rdx.toString(),r8:c.r8.toString()};}
function bt(c){try{return Thread.backtrace(c,Backtracer.ACCURATE).map(function(a){return {addr:a.toString(),rva:rvaOf(a)};});}catch(e){return ['btfail:'+e.message];}}

function install(b){
  base=b; ev({t:'hooks_installed',base:base.toString(),caller:base.add(RVA_CALLER).toString(),callee:base.add(RVA_CALLEE).toString()});
  Interceptor.attach(base.add(RVA_CALLER),{
    onEnter(){
      const s=this.context.rsp.sub(SLOT_OFF); slot=s;
      ev({t:'caller_enter',slot:s.toString(),before:readQ(s,8),cx:cx(this.context),bt:bt(this.context)});
      if(!monitoring){monitoring=true;
        try{
          const page=s.and(PAGE_MASK);
          let acc=0;
          MemoryAccessMonitor.enable([{base:page,size:0x1000}],{
            onAccess(d){
              try{
                if(acc++<30)ev({t:'mam_access',addr:d.address?d.address.toString():null,op:d.operation,
                                from_rva:rvaOf(d.from),from:d.from?d.from.toString():null});
                if(!slot||!d.address.equals(slot))return;
                let dis='?';try{const ins=Instruction.parse(d.from);dis=ins.mnemonic+' '+ins.opStr;}catch(e){}
                if(d.operation==='write')writes++;
                ev({t:'write_hit',op:d.operation,from_rva:rvaOf(d.from),from:d.from.toString(),disasm:dis,
                    value_after:readQ(slot,8),low4:readQ(slot,4)});
              }catch(e){ev({t:'cb_err',err:e.message});}
            }
          });
          ev({t:'mam_enabled',page:page.toString(),slot:s.toString()});
        }catch(e){ev({t:'mam_failed',err:e.message});}
      }
    }
  });
  Interceptor.attach(base.add(RVA_CALLEE),{
    onEnter(){const s=this.context.rsp.add(0x28);
      const v=readQ(s,8), lo=readQ(s,4);
      ev({t:'callee_enter',slot:s.toString(),value:v,low4:lo,cx:cx(this.context),bt:bt(this.context)});
      if(lo==='0x00000003')ev({t:'CORRUPT_R13_SOURCE',slot:s.toString(),value:v,cx:cx(this.context),bt:bt(this.context)});}
  });
  // ==== instrument the static suspect sites inside dump_6f360 (v2 RVAs) ====
  const S_W3=0xD8BFC, S_B1=0xD8AE2, S_B2=0xD8B8A, S_PB=0xD8A8E;
  Interceptor.attach(base.add(S_W3),{
    onEnter(){this.t=this.context.r12;this.before=readQ(this.t,8);
      ev({t:'w3_enter',rva:'d8bfc',target:this.t.toString(),before:this.before,cx:cx(this.context)});},
    onLeave(){ev({t:'w3_leave',target:this.t.toString(),before:this.before,after:readQ(this.t,8)});}
  });
  Interceptor.attach(base.add(S_B1),{
    onEnter(){const dst=this.context.rax.add(0x20);ev({t:'slotwrite',site:'d8ae2',dst:dst.toString(),value:readQ(dst,8),src:this.context.r10.toString()});}
  });
  Interceptor.attach(base.add(S_B2),{
    onEnter(){const dst=this.context.r8.add(0x20);ev({t:'slotwrite',site:'d8b8a',dst:dst.toString(),value:readQ(dst,8),src:this.context.rax.toString()});}
  });
  Interceptor.attach(base.add(S_PB),{onEnter(){ev({t:'pathB_hit',cx:cx(this.context)});}});
  Interceptor.attach(base.add(0xD8C04),{onEnter(){
    ev({t:'after_w3',rva:'d8c04',target:this.context.r12.toString(),qword:readQ(this.context.r12,8),low4:readQ(this.context.r12,4)});
  }});
  // dump_715c0: R13 load at 0x5f868b and AV store at 0x5f86be (v2 RVAs)
  Interceptor.attach(base.add(0x5F868B),{
    onEnter(){this.s=this.context.rsp.add(0x3e0);ev({t:'r13load_enter',slot:this.s.toString(),before:readQ(this.s,8)});},
    onLeave(){ev({t:'r13load_leave',r13:this.context.r13.toString(),slot:this.s.toString(),value:readQ(this.s,8),bt:bt(this.context)});}
  });
  Interceptor.attach(base.add(0x5F86BE),{
    onEnter(){ev({t:'AVSTORE_enter',r13:this.context.r13.toString(),ebp:this.context.rbp.toString(),
                  target_low4:readQ(this.context.r13,4),bt:bt(this.context)});}
  });
}
try{
  Process.setExceptionHandler(function(d){
    try{ev({t:'exception',type:d.type,addr:d.address?d.address.toString():null,
      pc:d.context?d.context.pc.toString():null,cx:d.context?cx(d.context):null,
      slot:slot?slot.toString():null,val:slot?readQ(slot,8):null,writes:writes,
      rip_rva:d.context&&base?rvaOf(d.context.pc):null});}catch(e){}
    return false;
  });
  let lc=0;
  const onLoad=function(a){try{const p=a[0].readUtf16String()||'';this.mine=p.toLowerCase().indexOf('recovered_dsp_test.dll')>=0;
      if(lc++<40)ev({t:'loadlib_any',path:p});
      if(this.mine)ev({t:'loadlib_enter',path:p});}catch(e){this.mine=false;}};
  const onLeave=function(r){if(!this.mine)return;const b=r;ev({t:'loadlib_leave',base:b.toString()});
      setTimeout(function(){try{install(b);}catch(e){ev({t:'install_failed',err:e.message});}},120);};
  let hooked=[];
  for(const name of ['LoadLibraryW','LoadLibraryExW']){
    try{const ll=Module.getGlobalExportByName(name);Interceptor.attach(ll,{onEnter:onLoad,onLeave:onLeave});hooked.push(name);}catch(e){ev({t:'hook_lib_failed',name:name,err:e.message});}
  }
  try{
    const ldr=Process.getModuleByName('ntdll.dll').getExportByName('LdrLoadDll');
    Interceptor.attach(ldr,{
      onEnter(a){
        try{
          const us=a[2]; const len=us.readU16(); const buf=us.add(8).readPointer();
          const p=buf.readUtf16String(len/2)||'';
          if(lc++<60)ev({t:'ldr_any',path:p});
          this.mine=p.toLowerCase().indexOf('recovered_dsp_test.dll')>=0;
          this.outPtr=a[3];
          if(this.mine)ev({t:'ldr_enter',path:p,out:a[3].toString()});
        }catch(e){this.mine=false;}
      },
      onLeave(r){
        if(!this.mine)return;
        ev({t:'ldr_leave',status:r.toString(),base:this.outPtr?this.outPtr.toString():null});
      }
    });
    hooked.push('LdrLoadDll');
  }catch(e){ev({t:'ldr_hook_failed',err:e.message});}
  recv('base',function(msg){
    try{
      const b=ptr(msg.base);
      let mz='?';try{mz=readQ(b,2);}catch(e){mz='ERR:'+e.message;}
      let t1000='?';try{t1000=readQ(b.add(0x1000),4);}catch(e){t1000='ERR:'+e.message;}
      let tc='?';try{tc=readQ(b.add(RVA_CALLER).sub(0x10),4);}catch(e){tc='ERR:'+e.message;}
      let mod='?';try{const mm=Process.findModuleByAddress(b);mod=mm?mm.name+' '+mm.base.toString():'null';}catch(e){mod='ERR:'+e.message;}
      ev({t:'base_diag',base:b.toString(),mz:mz,at1000:t1000,nearCaller:tc,module:mod});
      install(b);
    }catch(e){ev({t:'install_failed',err:e.message});}
  });
  ev({t:'ready',hooks:hooked});
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
    basefile=TMP/'p1_dll_base.txt'
    basefile.unlink(missing_ok=True)
    import os
    env=dict(os.environ); env['P1_DLL']=os.environ.get('P1_DLL','recovered_dsp_test.dll')
    p=subprocess.Popen([sys.executable,str(WORKER)],cwd=str(WORKER.parent),stderr=subprocess.PIPE,env=env)
    print('launcher pid',p.pid,flush=True)
    basefile=TMP/'p1_dll_base.txt'; realpid=None; t0=time.time()
    while time.time()-t0<8 and realpid is None:
        if basefile.exists():
            try:
                parts=basefile.read_text(encoding='ascii').split()
                if len(parts)==2: realpid=int(parts[0]); print('real worker pid',realpid,flush=True)
            except Exception: pass
        time.sleep(0.05)
    if realpid is None:
        print('no real pid; abort',flush=True); return
    dev=frida.get_local_device(); s=dev.attach(realpid); sc=s.create_script(AGENT); msgs=[]
    sc.on('message',lambda m,d: msgs.append(m['payload'] if m['type']=='send' else {'t':'script_error','raw':str(m)}))
    sc.load(); print('attached at %.2fs' % (time.time()-t0) if False else 'attached',flush=True)
    t=time.time(); sent=False
    while time.time()-t<20 and not any(x.get('t') in ('exception','script_error') for x in msgs):
        if not sent and basefile.exists():
            try:
                b=basefile.read_text(encoding='ascii').strip().split()[1]
                sc.post({'type':'base','base':b}); sent=True
                print('posted base',b,flush=True)
            except Exception: pass
        time.sleep(0.1)
    try:p.kill()
    except:pass
    try:err=p.stderr.read().decode(errors='replace')[:400]
    except:err=''
    with OUT.open('a',encoding='utf-8') as fh:
        fh.write(f'stderr={err!r}\n')
        for m in msgs:
            k=m.get('t')
            if k=='write_hit':
                fh.write(f"[{m['n']:03d}] WRITE op={m['op']} from=0x{m['from_rva']} ({sym(m['from_rva'])}) "
                         f"insn={m['disasm']} val_after={m['value_after']} low4={m['low4']}\n")
            elif k in ('caller_enter','callee_enter'):
                fh.write(f"[{m['n']:03d}] {k} slot={m.get('slot')} val={m.get('before') or m.get('value')} cx={json.dumps(m.get('cx'))}\n")
                fh.write(f"       bt={json.dumps([sym(x['rva']) if x.get('rva') else x.get('addr') for x in m.get('bt',[])] )}\n")
            elif k=='exception':
                fh.write(f"[{m['n']:03d}] EXCEPTION type={m.get('type')} pc={m.get('pc')} rip_rva={m.get('rip_rva')} "
                         f"cx={json.dumps(m.get('cx'))} slot={m.get('slot')} val={m.get('val')} writes={m.get('writes')}\n")
            else:
                fh.write(f"[{m.get('n','?')}] {k} {json.dumps({a:b for a,b in m.items() if a not in ('t','n')})}\n")
    print(OUT.read_text(encoding='utf-8',errors='replace')[:20000],flush=True)
if __name__=='__main__':main()
