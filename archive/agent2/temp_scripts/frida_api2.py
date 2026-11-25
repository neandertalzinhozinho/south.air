import frida,sys,time
JS=r"""
function t(f){try{return typeof f;}catch(e){return 'ERR';}}
send({t:'api', getGlobal:t(Module.getGlobalExportByName), getExp:t(Module.getExportByName),
      modGet:t(Process.getModuleByName('kernel32.dll').getExportByName),
      modFind:t(Process.getModuleByName('kernel32.dll').findExportByName)});
"""
d=frida.get_local_device(); p=d.spawn([sys.executable,'-c','import time;time.sleep(5)'])
s=d.attach(p); sc=s.create_script(JS); sc.on('message',lambda m,x:print(m,flush=True)); sc.load(); d.resume(p)
time.sleep(2)
try:d.kill(p)
except:pass
