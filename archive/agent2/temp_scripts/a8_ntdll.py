import pefile
from pathlib import Path
p=Path(r'C:\Windows\System32\ntdll.dll')
pe=pefile.PE(str(p))
rva=0x17fe00
print('ntdll file version', pe.FileInfo[0][0].Info[0].getValue('FileVersion') if pe.FileInfo else '?')
print('section at rva', [(s.Name, hex(s.VirtualAddress), hex(s.Misc_VirtualSize), hex(s.PointerToRawData)) for s in pe.sections if s.VirtualAddress<=rva<s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData)])
o=pe.get_offset_from_rva(rva)
print('offset',hex(o),'bytes',pe.get_data(rva,64).hex(' '))
print('export near', sorted([(e.address,e.name) for e in (pe.DIRECTORY_ENTRY_EXPORT.symbols if hasattr(pe,'DIRECTORY_ENTRY_EXPORT') else []) if 0x17f800<=e.address<=0x180400])[:20])
