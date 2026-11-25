import json,glob
base=r"D:\PROJETOS\soultree FORK\resonia\_fontes_recuperacao\claude"
for f in glob.glob(base+r"\**\*.jsonl",recursive=True):
    uses={}
    for line in open(f,encoding='utf-8'):
        o=json.loads(line)
        if o.get('type')=='assistant':
            for b in o['message'].get('content',[]):
                if isinstance(b,dict) and b.get('type')=='tool_use': uses[b['id']]=b
        if o.get('type')=='user' and isinstance(o['message'].get('content'),list):
            for b in o['message']['content']:
                if isinstance(b,dict) and b.get('type')=='tool_result':
                    u=uses.get(b['tool_use_id'])
                    if u and u['name'] in('Edit','Write'):
                        t=o.get('toolUseResult')
                        if isinstance(t,dict):
                            print(o['timestamp'],u['name'],u['input']['file_path'][-28:],{k:(len(v) if isinstance(v,(str,list)) else v) for k,v in t.items() if k!='filePath'})
                        else: print(o['timestamp'],u['name'],'TUR',type(t),str(t)[:80])
