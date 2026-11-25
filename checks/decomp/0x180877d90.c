 (GhidraScript)  

void FUN_180877d90(longlong param_1)

{
  int iVar1;
  undefined1 *puVar2;
  
  iVar1 = 0;
  *(undefined1 *)(param_1 + 0x2bc8) = 1;
  if (*(longlong *)(param_1 + 0x48) != 0) {
    puVar2 = (undefined1 *)(param_1 + 0x2bb8);
    do {
      iVar1 = iVar1 + 1;
      *puVar2 = 1;
      puVar2 = puVar2 + 1;
    } while ((ulonglong)(longlong)iVar1 < *(ulonglong *)(param_1 + 0x48));
  }
  return;
}

 (GhidraScript)  
