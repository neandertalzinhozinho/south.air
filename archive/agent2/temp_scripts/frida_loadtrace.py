import sys, time, frida
JS = r"""
function nm(p){ try{return p.readUtf16String();}catch(e){return '?';} }
try {
  Process.attachModuleObserver({onAdded: function(m){
    send({t:'load', name:m.name, base:m.base.toString(), size:m.size.toString(), path:m.path});
  }});
} catch(e) { send({t:'obserr',err:e.message}); }
const ll = Module.getExportByName('kernel32.dll','LoadLibraryW');
Interceptor.attach(ll, {
  onEnter: function(a){ this.p = nm(a[0]); send({t:'ll_enter', path:this.p}); },
  onLeave: function(r){ send({t:'ll_leave', path:this.p, ret:r.toString()}); }
});
setTimeout(function(){
  let ex=null;
  try { ex = Module.getExportByName(null,'Audio_863170'); } catch(e){ ex='ERR:'+e.message; }
  send({t:'status', export: ex ? ex.toString() : null,
        mods: Process.enumerateModules().filter(function(m){const n=(m.name||'').toLowerCase();return n.indexOf('dsparse')>=0||n.indexOf('recover')>=0;}).map(function(m){return {name:m.name,base:m.base.toString(),size:m.size.toString(),path:m.path};})});
}, 4000);
"""
dev=frida.get_local_device()
pid=dev.spawn([sys.executable, r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\worker_no_veh.py'], cwd=r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll')
s=dev.attach(pid)
sc=s.create_script(JS)
sc.on('message', lambda m,d: print(m,flush=True))
sc.load(); dev.resume(pid)
time.sleep(9)
try: dev.kill(pid)
except Exception: pass
