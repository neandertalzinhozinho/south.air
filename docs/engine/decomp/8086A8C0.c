// FUN_18086a8c0 @ 0x18086a8c0

undefined8 *
FUN_18086a8c0(undefined8 *param_1,longlong param_2,undefined8 param_3,undefined4 param_4,
             undefined8 param_5,undefined8 param_6,undefined8 param_7,longlong *param_8)

{
  int iVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  uint uVar4;
  longlong lVar5;
  uint uVar6;
  undefined8 *puVar7;
  int iVar8;
  ulonglong uVar9;
  ulonglong uVar10;
  undefined8 local_c8 [16];
  int local_48;
  int local_44;
  
  *param_1 = param_5;
  FUN_180873440(param_1 + 1);
  FUN_180873440(param_1 + 0x58a,param_2,param_3,param_4,0x100,0,param_5,param_6,param_7,param_8);
  param_1[0xb14] = param_3;
  uVar10 = 0;
  param_1[0xb13] = param_2;
  param_1[0xb15] = 0;
  param_1[0xb16] = 0;
  iVar8 = 0;
  param_1[0xb17] = 0;
  param_1[0xb18] = 0;
  param_1[0xb19] = 0;
  param_1[0xb1a] = 0;
  local_c8[0] = 0;
  local_48 = *(int *)(param_1 + 0xfa);
  local_44 = *(int *)(param_1 + 0xfb);
  if (0 < *(int *)(param_1 + 0xfa)) {
    puVar7 = local_c8;
    do {
      iVar8 = iVar8 + 1;
      *puVar7 = *(undefined8 *)((longlong)param_1 + (0x750 - (longlong)local_c8) + (longlong)puVar7)
      ;
      puVar7 = puVar7 + 1;
    } while (iVar8 < local_48);
  }
  iVar8 = local_44;
  uVar3 = local_c8[0];
  param_1[0xb15] = 0;
  if (((longlong)local_44 * 4 == 0) ||
     (lVar5 = (*DAT_181d8d730)(((longlong)local_44 * 4 + 0x3fU & 0xffffffffffffffc0) + 0x40),
     lVar5 == 0)) {
    uVar9 = 0;
  }
  else {
    uVar9 = lVar5 + 0x40U & 0xffffffffffffffc0;
    *(char *)(uVar9 - 1) = (char)(char *)(uVar9 - 1) - (char)lVar5;
  }
  param_1[0xb15] = uVar9;
  param_1[0xb17] = (longlong)iVar8;
  param_1[0xb16] = 1;
  (**(code **)(param_2 + 0x20))(param_2,0,uVar3,iVar8);
  uVar2 = DAT_182079f9c;
  iVar1 = (int)param_8[3];
  uVar9 = (longlong)iVar8 * param_1[10];
  lVar5 = *param_8 + (longlong)iVar1 * 4;
  uVar4 = (int)uVar9 + iVar1;
  uVar6 = (uVar4 - (uVar4 & 0xf)) + 0x10;
  if ((uVar4 & 0xf) == 0) {
    uVar6 = uVar4;
  }
  *(uint *)(param_8 + 3) = uVar6;
  FUN_180001040(uVar2,lVar5,uVar9 & 0xffffffff);
  (**(code **)(param_2 + 0x20))(param_2,2,lVar5,uVar9 & 0xffffffff);
  *(int *)(param_8 + 3) = iVar1;
  iVar8 = 0;
  local_c8[0] = 0;
  local_48 = *(int *)(param_1 + 0x683);
  local_44 = *(int *)(param_1 + 0x684);
  if (0 < *(int *)(param_1 + 0x683)) {
    puVar7 = local_c8;
    do {
      iVar8 = iVar8 + 1;
      *puVar7 = *(undefined8 *)
                 ((longlong)param_1 + (0x3398 - (longlong)local_c8) + (longlong)puVar7);
      puVar7 = puVar7 + 1;
    } while (iVar8 < local_48);
  }
  iVar8 = local_44;
  uVar3 = local_c8[0];
  lVar5 = param_1[0xb18];
  if (lVar5 != 0) {
    (*DAT_181d8d738)((lVar5 + -1) - (ulonglong)*(byte *)(lVar5 + -1));
  }
  param_1[0xb18] = 0;
  if (((longlong)iVar8 * 4 != 0) &&
     (lVar5 = (*DAT_181d8d730)(((longlong)iVar8 * 4 + 0x3fU & 0xffffffffffffffc0) + 0x40),
     lVar5 != 0)) {
    uVar10 = lVar5 + 0x40U & 0xffffffffffffffc0;
    *(char *)(uVar10 - 1) = (char)(char *)(uVar10 - 1) - (char)lVar5;
  }
  param_1[0xb18] = uVar10;
  param_1[0xb1a] = (longlong)iVar8;
  param_1[0xb19] = 1;
  (**(code **)(param_2 + 0x20))(param_2,1,uVar3,iVar8);
  iVar1 = (int)param_8[3];
  uVar10 = (longlong)iVar8 * param_1[0x593];
  lVar5 = *param_8 + (longlong)iVar1 * 4;
  uVar4 = (int)uVar10 + iVar1;
  uVar6 = (uVar4 - (uVar4 & 0xf)) + 0x10;
  if ((uVar4 & 0xf) == 0) {
    uVar6 = uVar4;
  }
  *(uint *)(param_8 + 3) = uVar6;
  FUN_180001040(uVar2,lVar5,uVar10 & 0xffffffff);
  (**(code **)(param_2 + 0x20))(param_2,3,lVar5,uVar10 & 0xffffffff);
  *(int *)(param_8 + 3) = iVar1;
  lVar5 = *param_8 + (longlong)iVar1 * 4;
  uVar4 = (int)param_1[10] + iVar1;
  uVar6 = (uVar4 - (uVar4 & 0xf)) + 0x10;
  if ((uVar4 & 0xf) == 0) {
    uVar6 = uVar4;
  }
  *(uint *)(param_8 + 3) = uVar6;
  FUN_180001040(uVar2,lVar5);
  (**(code **)(param_2 + 0x20))(param_2,8,lVar5,*(undefined4 *)(param_1 + 10));
  *(int *)(param_8 + 3) = iVar1;
  return param_1;
}

