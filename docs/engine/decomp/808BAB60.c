// FUN_1808bab60 @ 0x1808bab60

void FUN_1808bab60(undefined8 param_1,longlong *param_2)

{
  longlong lVar1;
  uint uVar2;
  ulonglong uVar3;
  undefined1 local_58 [32];
  uint uStack_38;
  int iStack_34;
  
  FUN_18086f170(param_1,local_58,(int)param_2[1]);
  uVar2 = local_58._8_4_;
  lVar1 = *param_2;
  if (uVar2 == 1) {
    FUN_1800011f0(lVar1);
  }
  else if (1 < (int)uVar2) {
    uVar3 = (ulonglong)uVar2;
    do {
      FUN_1800011f0(lVar1);
      uVar3 = uVar3 - 1;
    } while (uVar3 != 0);
  }
  if (0 < iStack_34) {
    lVar1 = *param_2 + (longlong)local_58._12_4_ * 4;
    if (uStack_38 == 1) {
      FUN_1800011f0(lVar1);
    }
    else if (1 < (int)uStack_38) {
      uVar3 = (ulonglong)uStack_38;
      do {
        FUN_1800011f0(lVar1);
        uVar3 = uVar3 - 1;
      } while (uVar3 != 0);
    }
  }
  return;
}

