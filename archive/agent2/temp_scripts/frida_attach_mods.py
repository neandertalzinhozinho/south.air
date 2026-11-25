import subprocess,sys,time,frida
W=r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\worker_no_veh.py'
JS=r"""
setTimeout(function(){
  send({t:'mods',list:Process.enumerateModules().map(function(m){
    return {n:m.name,b:m.base.toString(),s:m.size.toString(),p:m.path};})});
},2500);
"""
p=subprocess.Popen([sys.executable,W],cwd=r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll',stderr=subprocess.PIPE)
d=frida.get_local_device(); s=d.attach(p.pid); sc=s.create_script(JS)
r={}
sc.on('message',lambda m,data: r.update(m['payload']))
sc.load(); time.sleep(4)
try:p.kill()
except:pass
err=p.stderr.read().decode(errors='replace') if p.stderr else ''
print('stderr',err[:400])
for x in r.get('list',[]):
    if int(x['s'],10)>0x500000 or 'dsparse' in x['n'].lower() or 'recover' in x['n'].lower():
        print(x)
