// FUN_180867cc0 @ 0x180867cc0

longlong * FUN_180867cc0(longlong *param_1,longlong param_2,int param_3,int param_4)

{
  undefined4 uVar1;
  longlong *plVar2;
  int iVar3;
  
  uVar1 = *(undefined4 *)(param_2 + 0x400);
  iVar3 = 0;
  *param_1 = 0;
  FUN_181798f42(param_1 + 1,0,0x3f8);
  *(undefined4 *)(param_1 + 0x80) = uVar1;
  param_1[0x81] = (longlong)param_4 << 2;
  *(int *)((longlong)param_1 + 0x404) = param_4;
  if (0 < *(int *)(param_2 + 0x400)) {
    plVar2 = param_1;
    do {
      iVar3 = iVar3 + 1;
      *plVar2 = *(longlong *)((param_2 - (longlong)param_1) + (longlong)plVar2) +
                (longlong)param_3 * 4;
      plVar2 = plVar2 + 1;
    } while (iVar3 < *(int *)(param_2 + 0x400));
  }
  return param_1;
}

