import subprocess,sys,time,frida
JS=r"""
try{Process.setExceptionHandler(function(d){send({t:'EXH',type:d.type,pc:d.context?d.context.pc.toString():null});return true;});send({t:'handler_set'});}catch(e){send({t:'err',err:e.message});}
setTimeout(function(){send({t:'crashing'});try{ptr(0).readPointer();}catch(e){send({t:'js_caught',err:e.message});}},1000);
"""
p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(10)'])
d=frida.get_local_device(); s=d.attach(p.pid); sc=s.create_script(JS)
sc.on('message',lambda m,data: print(m,flush=True)); sc.load(); time.sleep(4)
try:p.kill()
except:pass
