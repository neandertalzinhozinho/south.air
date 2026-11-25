// FUN_18086f170 @ 0x18086f170

undefined8 * FUN_18086f170(uint *param_1,undefined8 *param_2,int param_3)

{
  uint uVar1;
  undefined8 *puVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  undefined8 local_58;
  uint uStack_50;
  int iStack_4c;
  longlong local_48;
  undefined8 local_40;
  undefined8 uStack_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 uStack_20;
  undefined8 local_18;
  
  iVar3 = 0;
  local_58 = 0;
  iStack_4c = *(int *)(*(longlong *)(param_1 + 2) + 0x88);
  iVar4 = (param_1[6] - *(int *)(*(longlong *)(param_1 + 2) + 0x88)) + param_3;
  uStack_50 = *param_1;
  iVar5 = 0;
  local_48 = (longlong)iStack_4c << 2;
  if (iVar4 < 1) {
    if (0 < (int)uStack_50) {
      puVar2 = &local_58;
      do {
        iVar5 = iVar5 + 1;
        *puVar2 = *(undefined8 *)
                   ((longlong)param_1 + (0x10 - (longlong)&local_58) + (longlong)puVar2);
        puVar2 = puVar2 + 1;
      } while (iVar5 < (int)uStack_50);
    }
    FUN_18086f340(&local_58,&local_28,param_1[6],param_3);
    uVar1 = *param_1;
    *param_2 = local_28;
    param_2[1] = uStack_20;
    param_2[2] = local_18;
    param_2[3] = 0;
    param_2[4] = (ulonglong)uVar1;
    param_2[5] = 0;
  }
  else {
    if (0 < (int)uStack_50) {
      puVar2 = &local_58;
      do {
        iVar5 = iVar5 + 1;
        *puVar2 = *(undefined8 *)
                   ((longlong)param_1 + (0x10 - (longlong)&local_58) + (longlong)puVar2);
        puVar2 = puVar2 + 1;
      } while (iVar5 < (int)uStack_50);
    }
    FUN_18086f340(&local_58,&local_40,param_1[6],param_3 - iVar4);
    local_58 = 0;
    uStack_50 = *param_1;
    iStack_4c = *(int *)(*(longlong *)(param_1 + 2) + 0x88);
    local_48 = (longlong)*(int *)(*(longlong *)(param_1 + 2) + 0x88) << 2;
    if (0 < (int)*param_1) {
      puVar2 = &local_58;
      do {
        iVar3 = iVar3 + 1;
        *puVar2 = *(undefined8 *)
                   ((longlong)param_1 + (0x10 - (longlong)&local_58) + (longlong)puVar2);
        puVar2 = puVar2 + 1;
      } while (iVar3 < (int)uStack_50);
    }
    FUN_180860b90(&local_28,&local_58,0,iVar4);
    *param_2 = local_40;
    param_2[1] = uStack_38;
    param_2[2] = local_30;
    param_2[3] = local_28;
    param_2[4] = uStack_20;
    param_2[5] = local_18;
  }
  return param_2;
}

