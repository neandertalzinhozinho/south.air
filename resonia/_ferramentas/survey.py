import json,sys,glob,os,collections
base=r"D:\PROJETOS\soultree FORK\resonia\_fontes_recuperacao"
for f in sorted(glob.glob(base+r"\**\*.jsonl",recursive=True)):
    c=collections.Counter(); tools=collections.Counter()
    for line in open(f,encoding='utf-8'):
        try: o=json.loads(line)
        except Exception as e: c['BAD']+=1; continue
        t=o.get('type'); 
        if t=='response_item' or t=='event_msg':
            pt=o['payload'].get('type'); c[t+':'+str(pt)]+=1
            if pt in('function_call','custom_tool_call'): tools[o['payload'].get('name')]+=1
        else:
            c[t]+=1
            if t=='assistant':
                for b in o['message'].get('content',[]):
                    if isinstance(b,dict) and b.get('type')=='tool_use': tools[b['name']]+=1
            if o.get('isSidechain'): c['sidechain']+=1
    print(os.path.basename(f)); print(' ',dict(c)); print('  tools',dict(tools))
