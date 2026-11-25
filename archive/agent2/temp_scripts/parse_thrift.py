import json, struct, sys

d = json.load(open(sys.argv[1], encoding='utf8'))
reqs = [e['data'] for e in d['events'] if e.get('kind') == 'recv']
print('requests:', len(reqs))
data = bytes.fromhex(reqs[0])
print('total bytes', len(data))

i = 0
print('ver/type', data[0:4].hex())
nlen = struct.unpack('>i', data[4:8])[0]
name = data[8:8 + nlen].decode()
seq = struct.unpack('>i', data[8 + nlen:12 + nlen])[0]
print('method', name, 'seqid', seq)
i = 12 + nlen

TYPES = {2: 'BOOL', 3: 'BYTE', 4: 'DOUBLE', 6: 'I16', 8: 'I32', 10: 'I64', 11: 'STRING', 12: 'STRUCT', 13: 'MAP', 14: 'SET', 15: 'LIST'}


def rd_struct(i, depth=0):
    while i < len(data):
        t = data[i]
        i += 1
        if t == 0:
            print('  ' * depth + 'STOP')
            return i
        ftype = t
        fid = struct.unpack('>h', data[i:i + 2])[0]
        i += 2
        print('  ' * depth + f'field {fid} type {TYPES.get(ftype, ftype)} @{i}')
        if ftype == 8:
            v = struct.unpack('>i', data[i:i + 4])[0]
            print('  ' * depth + f'  I32 = {v} ({v:#x})')
            i += 4
        elif ftype == 10:
            v = struct.unpack('>q', data[i:i + 8])[0]
            print('  ' * depth + f'  I64 = {v}')
            i += 8
        elif ftype == 11:
            ln = struct.unpack('>i', data[i:i + 4])[0]
            i += 4
            print('  ' * depth + f'  STRING len={ln}')
            print('  ' * depth + '   ' + data[i:i + ln].hex())
            i += ln
        elif ftype == 12:
            i = rd_struct(i, depth + 1)
        elif ftype == 2:
            print('  ' * depth + f'  BOOL = {data[i]}')
            i += 1
        else:
            print('  ' * depth + f'  <unhandled type {ftype}> remaining {data[i:i+32].hex()}')
            return len(data)
    return i


rd_struct(i)
