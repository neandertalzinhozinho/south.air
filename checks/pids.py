import struct
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
names=["depth","attack","release","detail","mix","out_trim","wet_trim","max_cut","sidechain_listen","stereo_link","stereo_mode","stereo_focus","low_latency","mode","quality","linear_phase","delta","bypass","dry_wet","output"]
for n in names:
    b=n.encode()+b"\x00"
    i=d.find(b"\x00"+b)
    hits=[]
    while i!=-1 and len(hits)<8:
        hits.append(i+1)
        i=d.find(b"\x00"+b,i+1)
    print(n,hits)
