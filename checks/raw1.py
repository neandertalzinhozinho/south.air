import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
# dump raw bytes as hex for 0x1C9A9E0..0x1C9AA40 to inspect
import binascii
off=0x1C9A9E0
print(binascii.hexlify(data[off:off+0x70]).decode())
