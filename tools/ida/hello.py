import idaapi
from pathlib import Path

Path(r"D:\PROJETOS\soultree\checks\ida_hello.txt").write_text(
    "hello from idapython, imagebase=0x%X\n" % idaapi.get_imagebase(), encoding="utf-8")
