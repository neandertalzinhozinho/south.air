import sys, time, frida
JS = r"""
setTimeout(function () {
  const mods = Process.enumerateModules();
  send({t:'mods', list: mods.filter(function(m){
      const n=(m.name||'').toLowerCase();
      return n.indexOf('dsp')>=0 || n.indexOf('recover')>=0 || n.indexOf('soothe')>=0 || n.indexOf('python')>=0;
    }).map(function(m){
      let r1='?',r2='?';
      try { m.base.add(0xf5977).readByteArray(4); r1='ok'; } catch(e){ r1='ERR:'+e.message; }
      try { m.base.add(0x61565f).readByteArray(4); r2='ok'; } catch(e){ r2='ERR:'+e.message; }
      return {name:m.name, base:m.base.toString(), size:m.size.toString(), path:m.path, r_f5977:r1, r_61565f:r2};
    })
  });
}, 5000);
"""
dev=frida.get_local_device()
pid=dev.spawn([sys.executable, r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\worker_no_veh.py'])
s=dev.attach(pid)
sc=s.create_script(JS)
sc.on('message', lambda m,d: print(m,flush=True))
sc.load(); dev.resume(pid)
time.sleep(8)
try: dev.kill(pid)
except Exception: pass
