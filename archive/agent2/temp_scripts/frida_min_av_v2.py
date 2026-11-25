"""Minimal Frida agent: only Process.setExceptionHandler; report exact AV."""
import subprocess,sys,time
from pathlib import Path
import frida
TMP=Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
WORKER=Path(r'D:\PROJETOS\shadowFILES\analysis\scripts\p1_frida_delayed_worker.py')
JS=r"""
let base=null;
Process.setExceptionHandler(function(d){
  const c=d.context;
  send({t:'AV',type:d.type,addr:d.address?d.address.toString():null,
        pc:c?c.pc.toString():null,base:base,
        pc_rva:(base&&c)?c.pc.sub(base).toString(16):null,
        r13:c?c.r13.toString():null,r9:c?c.r9.toString():null,
        rbp:c?c.rbp.toString():null,rsp:c?c.rsp.toString():null,
        rcx:c?c.rcx.toString():null,rdx:c?c.rdx.toString():null});
  return false;
});
recv('base',function(m){base=ptr(m.base);send({t:'base_set',base:base.toString()});});
send({t:'ready'});
"""
def main():
    bf=TMP/'p1_dll_base.txt'; bf.unlink(missing_ok=True)
    env=dict(__import__('os').environ); env['P1_DLL']='recovered_dsp_test_v2.dll'
    p=subprocess.Popen([sys.executable,str(WORKER)],cwd=str(WORKER.parent),env=env)
    real=None; t=time.time()
    while time.time()-t<8 and not real:
        if bf.exists():
            try: real=int(bf.read_text().split()[0])
            except: pass
        time.sleep(0.05)
    if not real: print('no pid'); return
    d=frida.get_local_device(); s=d.attach(real); sc=s.create_script(JS); out=[]
    sc.on('message',lambda m,x: out.append(m['payload'] if m['type']=='send' else {'err':str(m)}))
    sc.load()
    t=time.time(); sent=False
    while time.time()-t<14 and not any(x.get('t')=='AV' or 'err' in x for x in out):
        if not sent and bf.exists():
            try: sc.post({'type':'base','base':bf.read_text().split()[1]}); sent=True
            except: pass
        time.sleep(0.1)
    try:p.kill()
    except:pass
    for x in out: print(x)
if __name__=='__main__':main()
