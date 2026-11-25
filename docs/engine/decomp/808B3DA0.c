// FUN_1808b3da0 @ 0x1808b3da0

void FUN_1808b3da0(undefined8 param_1,longlong *param_2)

{
  longlong lVar1;
  uint uVar2;
  int iVar3;
  undefined8 *puVar4;
  ulonglong uVar5;
  undefined1 local_68 [16];
  undefined8 local_58;
  undefined1 local_48 [16];
  undefined8 local_38;
  undefined8 local_30;
  uint uStack_28;
  int iStack_24;
  undefined8 local_20;
  
  FUN_18086f170(param_1,local_48,(int)param_2[1]);
  uVar2 = local_48._8_4_;
  iVar3 = local_48._12_4_;
  lVar1 = *param_2;
  local_58 = local_38;
  local_68 = local_48;
  if (uVar2 == 1) {
    FUN_1800010a0(lVar1,local_48._0_8_,iVar3);
  }
  else if (0 < (int)uVar2) {
    puVar4 = (undefined8 *)local_68;
    uVar5 = (ulonglong)uVar2;
    do {
      FUN_1800010a0(lVar1,*puVar4,iVar3);
      puVar4 = puVar4 + 1;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  if (0 < iStack_24) {
    local_58 = local_20;
    lVar1 = *param_2 + (longlong)iVar3 * 4;
    if (uStack_28 == 1) {
      FUN_1800010a0(lVar1,local_30,iStack_24);
    }
    else if (0 < (int)uStack_28) {
      puVar4 = (undefined8 *)local_68;
      uVar5 = (ulonglong)uStack_28;
      do {
        FUN_1800010a0(lVar1,*puVar4,iStack_24);
        puVar4 = puVar4 + 1;
        uVar5 = uVar5 - 1;
      } while (uVar5 != 0);
    }
  }
  return;
}

