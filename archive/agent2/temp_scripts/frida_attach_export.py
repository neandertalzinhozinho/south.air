import subprocess,sys,time,frida
W=r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\worker_no_veh.py'
JS=r"""
let n=0;
const t=setInterval(function(){
  n++;
  let ex=null, err=null;
  try{ex=Module.getExportByName(null,'Audio_863170');}catch(e){err=e.message;}
  send({t:'poll',n:n,ex:ex?ex.toString():null,err:err,mods:Process.enumerateModules().length});
  if(ex||n>30)clearInterval(t);
},200);
"""
p=subprocess.Popen([sys.executable,W],cwd=r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll',stderr=subprocess.PIPE)
d=frida.get_local_device(); s=d.attach(p.pid); sc=s.create_script(JS)
msgs=[]
sc.on('message',lambda m,data: msgs.append(m['payload']))
sc.load(); time.sleep(7)
try:out,err=p.communicate(timeout=2)
except subprocess.TimeoutExpired:p.kill();out,err=p.communicate()
for m in msgs:
    if m.get('ex') or m['n'] in (1,5,10,15) or m.get('err'): print(m)
print('stderr',err.decode(errors='replace')[:500])
print('rc',hex(p.returncode & 0xffffffff))
