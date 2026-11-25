// FUN_18031b730 @ 0x18031b730

undefined8 FUN_18031b730(longlong param_1,int param_2,uint param_3,undefined8 param_4)

{
  int iVar1;
  uint uVar2;
  undefined8 uVar3;
  int *piVar4;
  undefined1 *local_res8;
  
  if (param_2 == *(int *)(param_1 + 100)) {
    uVar2 = (**(code **)(**(longlong **)(param_1 + 0x98) + 0xd8))();
    if (param_3 < uVar2) {
      uVar3 = (**(code **)(**(longlong **)(param_1 + 0x98) + 0xf0))
                        (*(longlong **)(param_1 + 0x98),&local_res8,param_3);
      FUN_180319500(param_4,uVar3);
      piVar4 = (int *)(local_res8 + -0x10);
      if (piVar4 != &DAT_18238a828) {
        LOCK();
        iVar1 = *piVar4;
        *piVar4 = *piVar4 + -1;
        UNLOCK();
        if (iVar1 == 0) {
                    /* WARNING: Subroutine does not return */
          thunk_FUN_181798f60();
        }
      }
      return 0;
    }
  }
  local_res8 = &DAT_18238a838;
  FUN_180319500(param_4,&local_res8);
  piVar4 = (int *)(local_res8 + -0x10);
  if (piVar4 != &DAT_18238a828) {
    LOCK();
    iVar1 = *piVar4;
    *piVar4 = *piVar4 + -1;
    UNLOCK();
    if (iVar1 == 0) {
                    /* WARNING: Subroutine does not return */
      thunk_FUN_181798f60();
    }
  }
  return 1;
}

