import frida, sys, time
JS = r"""
send({t:'api',mam: typeof MemoryAccessMonitor, ex: typeof Process.setExceptionHandler,
      stalker: typeof Stalker, obs: typeof Process.attachModuleObserver,
      inst: typeof Instruction, module: typeof Module, bt: typeof Thread.backtrace,
      fridaVer: Frida.version});
"""
dev = frida.get_local_device()
pid = dev.spawn([sys.executable, "-c", "import time; time.sleep(10)"])
s = dev.attach(pid)
sc = s.create_script(JS)
sc.on('message', lambda m,d: print(m, flush=True))
sc.load()
dev.resume(pid)
time.sleep(2)
try: dev.kill(pid)
except Exception: pass
