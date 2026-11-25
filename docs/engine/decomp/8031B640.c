// FUN_18031b640 @ 0x18031b640

undefined8 FUN_18031b640(longlong param_1,int param_2,undefined4 *param_3)

{
  int iVar1;
  undefined4 uVar2;
  int *piVar3;
  longlong local_res20;
  longlong local_18 [2];
  
  if (param_2 != 0) {
    FUN_181798f42(param_3,0,0x108);
    return 1;
  }
  *param_3 = *(undefined4 *)(param_1 + 100);
  uVar2 = (**(code **)(**(longlong **)(param_1 + 0x98) + 0xd8))();
  param_3[0x41] = uVar2;
  FUN_180398450(&local_res20,"Factory Presets");
  FUN_1803792b0(local_18,&local_res20);
  piVar3 = (int *)(local_res20 + -0x10);
  if (piVar3 != &DAT_18238a828) {
    LOCK();
    iVar1 = *piVar3;
    *piVar3 = *piVar3 + -1;
    UNLOCK();
    if (iVar1 == 0) {
                    /* WARNING: Subroutine does not return */
      thunk_FUN_181798f60();
    }
  }
  FUN_180319500(param_3 + 1,local_18);
  piVar3 = (int *)(local_18[0] + -0x10);
  if (piVar3 != &DAT_18238a828) {
    LOCK();
    iVar1 = *piVar3;
    *piVar3 = *piVar3 + -1;
    UNLOCK();
    if (iVar1 == 0) {
                    /* WARNING: Subroutine does not return */
      thunk_FUN_181798f60();
    }
  }
  return 0;
}

