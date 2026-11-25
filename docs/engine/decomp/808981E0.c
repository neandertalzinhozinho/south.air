// FUN_1808981e0 @ 0x1808981e0

void FUN_1808981e0(longlong param_1,undefined8 *param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined8 uVar3;
  undefined4 uVar4;
  longlong lVar5;
  
  uVar4 = DAT_18207a6a8;
  if (*(int *)(param_1 + 0x80) == *(int *)(param_2 + 0x10)) {
    lVar5 = (longlong)*(int *)(param_1 + 0x80);
    if (0 < lVar5) {
      uVar1 = *(undefined4 *)(param_1 + 0x84);
      param_1 = param_1 - (longlong)param_2;
      do {
        FUN_180001070(*param_2,uVar4,*(undefined8 *)(param_1 + (longlong)param_2),uVar1);
        param_2 = param_2 + 1;
        lVar5 = lVar5 + -1;
      } while (lVar5 != 0);
    }
  }
  else if (*(int *)(param_2 + 0x10) == 1) {
    iVar2 = *(int *)(param_1 + 0x80);
    lVar5 = 0;
    if (0 < (longlong)iVar2) {
      uVar3 = *param_2;
      uVar1 = *(undefined4 *)(param_1 + 0x84);
      do {
        FUN_180001070(uVar3,uVar4,*(undefined8 *)(param_1 + lVar5 * 8),uVar1);
        lVar5 = lVar5 + 1;
      } while (lVar5 < iVar2);
    }
  }
  return;
}

