import frida,sys,time
JS=r"""
const p=Memory.alloc(0x1000);
let hits=0;
try{
 MemoryAccessMonitor.enable([{base:p,size:0x1000}],{onAccess(d){hits++;send({t:'hit',op:d.operation,addr:d.address.toString(),from:d.from.toString()});}});
 send({t:'enabled',base:p.toString()});
}catch(e){send({t:'enable_err',err:e.message});}
setTimeout(function(){
  try{p.add(0x100).writeU32(0xdeadbeef);send({t:'wrote',hits:hits,val:p.add(0x100).readU32().toString(16)});}
  catch(e){send({t:'write_err',err:e.message});}
  setTimeout(function(){try{MemoryAccessMonitor.disable();}catch(e){}send({t:'done',hits:hits});},200);
},200);
"""
d=frida.get_local_device(); pid=d.spawn([sys.executable,'-c','import time;time.sleep(5)'])
s=d.attach(pid); sc=s.create_script(JS)
sc.on('message',lambda m,x:print(m,flush=True)); sc.load(); d.resume(pid); time.sleep(3)
try:d.kill(pid)
except:pass
