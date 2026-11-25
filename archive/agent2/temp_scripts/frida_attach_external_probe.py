import subprocess, sys, time, frida
WORKER = r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\worker_no_veh.py'
CWD = r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll'
JS = r"""
let done=false;
const t=setInterval(function(){
  if(done) return;
  let ex=null;
  try { ex = Module.getExportByName(null,'Audio_863170'); } catch(e){}
  if (ex) {
     done=true; clearInterval(t);
     const base = ex.sub(0x505996);
     send({t:'found', export:ex.toString(), base:base.toString(),
           m: (function(){try{const m=Process.findModuleByAddress(base);return {name:m.name,size:m.size.toString(),path:m.path};}catch(e){return {err:e.message};}})()});
  }
}, 10);
setTimeout(function(){ if(!done) send({t:'timeout'}); }, 3000);
"""
proc = subprocess.Popen([sys.executable, WORKER], cwd=CWD)
print('popen pid', proc.pid, flush=True)
dev = frida.get_local_device()
t0=time.time()
s = dev.attach(proc.pid)
print('attached in %.3fs' % (time.time()-t0), flush=True)
sc = s.create_script(JS)
sc.on('message', lambda m,d: print('MSG',m,flush=True))
sc.load()
print('script loaded at %.3fs' % (time.time()-t0), flush=True)
try:
    out,err = proc.communicate(timeout=12)
    print('stdout',out.decode(errors='replace'))
    print('stderr',err.decode(errors='replace')[:500])
    print('rc',hex(proc.returncode & 0xffffffff))
except subprocess.TimeoutExpired:
    proc.kill()
