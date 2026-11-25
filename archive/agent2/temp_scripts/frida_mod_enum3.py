import sys, time, frida, json
JS = r"""
setTimeout(function () {
  const mods = Process.enumerateModules();
  send({t:'mods', count:mods.length, list: mods.map(function(m){
      return {name:m.name, base:m.base.toString(), size:m.size.toString(), path:m.path};
    })
  });
}, 5000);
"""
dev=frida.get_local_device()
pid=dev.spawn([sys.executable, r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\worker_no_veh.py'])
s=dev.attach(pid)
sc=s.create_script(JS)
data={}
sc.on('message', lambda m,d: data.update(m['payload']))
sc.load(); dev.resume(pid)
time.sleep(8)
try: dev.kill(pid)
except Exception: pass
print('count',data.get('count'))
for x in data.get('list',[]):
    if 'shadow' in (x['path'] or '').lower() or int(x['size'],16)>0x400000 or 'dsparse' in x['name'].lower():
        print(x['name'], x['base'], x['size'], x['path'])
