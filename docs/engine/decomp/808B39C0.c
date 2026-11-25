// FUN_1808b39c0 @ 0x1808b39c0

void FUN_1808b39c0(longlong param_1,undefined8 *param_2,undefined8 *param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  longlong lVar5;
  longlong lVar6;
  
  if ((*(int *)(param_1 + 0x400) == *(int *)(param_2 + 0x80)) &&
     (*(int *)(param_1 + 0x400) == *(int *)(param_3 + 1))) {
    lVar5 = (longlong)*(int *)(param_1 + 0x400);
    if (0 < lVar5) {
      uVar1 = *(undefined4 *)(param_1 + 0x404);
      param_1 = param_1 - (longlong)param_3;
      lVar6 = (longlong)param_2 - (longlong)param_3;
      do {
        FUN_180001580(*(undefined8 *)(lVar6 + (longlong)param_3),*param_3,
                      *(undefined8 *)(param_1 + (longlong)param_3),uVar1);
        param_3 = param_3 + 1;
        lVar5 = lVar5 + -1;
      } while (lVar5 != 0);
    }
  }
  else {
    iVar2 = *(int *)(param_2 + 0x80);
    if (1 < iVar2) {
      if (*(int *)(param_3 + 1) == 1) {
        lVar5 = (longlong)*(int *)(param_1 + 0x400);
        if (lVar5 < 1) {
          return;
        }
        uVar1 = *(undefined4 *)(param_1 + 0x404);
        param_1 = param_1 - (longlong)param_2;
        uVar3 = *param_3;
        do {
          FUN_180001580(*param_2,uVar3,*(undefined8 *)(param_1 + (longlong)param_2),uVar1);
          param_2 = param_2 + 1;
          lVar5 = lVar5 + -1;
        } while (lVar5 != 0);
        return;
      }
      iVar2 = *(int *)(param_2 + 0x80);
    }
    if ((iVar2 == 1) && (*(int *)(param_3 + 1) == 1)) {
      iVar2 = *(int *)(param_1 + 0x400);
      lVar5 = 0;
      if (0 < (longlong)iVar2) {
        uVar3 = *param_3;
        uVar4 = *param_2;
        uVar1 = *(undefined4 *)(param_1 + 0x404);
        do {
          FUN_180001580(uVar4,uVar3,*(undefined8 *)(param_1 + lVar5 * 8),uVar1);
          lVar5 = lVar5 + 1;
        } while (lVar5 < iVar2);
      }
    }
  }
  return;
}

