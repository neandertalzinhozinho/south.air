// FUN_180877dd0 @ 0x180877dd0

void FUN_180877dd0(longlong param_1)

{
  char *pcVar1;
  double dVar2;
  double dVar3;
  longlong lVar4;
  undefined8 *puVar5;
  ulonglong uVar6;
  ulonglong uVar7;
  int iVar8;
  ulonglong uVar9;
  int iVar10;
  ulonglong *puVar11;
  int *piVar12;
  double dVar13;
  double dVar14;
  undefined8 local_98;
  int iStack_90;
  uint uStack_8c;
  longlong local_88;
  undefined4 local_78;
  undefined4 uStack_74;
  int iStack_70;
  uint uStack_6c;
  longlong local_68;
  
  iVar10 = *(int *)(param_1 + 0x60);
  puVar11 = (ulonglong *)(param_1 + 0x2c08);
  FUN_1808686d0(puVar11);
  *(int *)(param_1 + 0x2c18) = iVar10 * 2;
  iVar8 = 0;
  uVar9 = 0;
  *(undefined4 *)(param_1 + 0x2c1c) = 1;
  iVar10 = iVar8;
  do {
    lVar4 = (longlong)*(int *)(param_1 + 0x2c18) * 4;
    if ((lVar4 == 0) || (lVar4 = (*DAT_181d8d730)(lVar4 + 0x40), lVar4 == 0)) {
      uVar6 = uVar9;
    }
    else {
      uVar6 = lVar4 + 0x40U & 0xffffffffffffffc0;
      pcVar1 = (char *)(uVar6 - 1);
      *pcVar1 = (char)pcVar1 - (char)lVar4;
    }
    *puVar11 = uVar6;
    iVar10 = iVar10 + 1;
    puVar11 = puVar11 + 1;
  } while (iVar10 < *(int *)(param_1 + 0x2c1c));
  if (0 < *(int *)(param_1 + 0x2c1c)) {
    puVar5 = (undefined8 *)(param_1 + 0x2c08);
    iVar10 = iVar8;
    do {
      FUN_1800010d0(*puVar5,*(undefined4 *)(param_1 + 0x2c18));
      iVar10 = iVar10 + 1;
      puVar5 = puVar5 + 1;
    } while (iVar10 < *(int *)(param_1 + 0x2c1c));
  }
  *(undefined8 *)(param_1 + 0x2c10) = 0;
  dVar2 = DAT_18207a138;
  uVar6 = (ulonglong)(int)*(uint *)(param_1 + 0x2c18);
  local_98 = 0;
  iStack_90 = *(int *)(param_1 + 0x2c1c);
  uStack_8c = *(uint *)(param_1 + 0x2c18);
  local_88 = uVar6 << 2;
  if (0 < *(int *)(param_1 + 0x2c1c)) {
    puVar5 = &local_98;
    do {
      iVar8 = iVar8 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x2c08) - (longlong)&local_98) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar8 < iStack_90);
    uVar6 = (ulonglong)uStack_8c;
  }
  lVar4 = local_98;
  local_78 = (undefined4)local_98;
  uStack_74 = local_98._4_4_;
  iStack_70 = iStack_90;
  uStack_6c = uStack_8c;
  local_68 = local_88;
  dVar14 = DAT_18207a138 / (double)(int)uStack_8c;
  uVar7 = uVar9;
  if (uStack_8c != 0) {
    do {
      *(float *)(local_98 + uVar7 * 4) = (float)((double)uVar7 * dVar14);
      uVar7 = uVar7 + 1;
    } while (uVar7 < (ulonglong)(longlong)(int)uStack_8c);
  }
  if (1 < iStack_90) {
    piVar12 = &iStack_70;
    uVar7 = (ulonglong)(iStack_90 - 1);
    do {
      FUN_1800010a0(lVar4,*(undefined8 *)piVar12,uVar6 & 0xffffffff);
      piVar12 = piVar12 + 2;
      uVar7 = uVar7 - 1;
    } while (uVar7 != 0);
  }
  dVar3 = DAT_18207a1e0;
  dVar14 = DAT_18207a0b8;
  if (0 < (longlong)(int)uVar6) {
    do {
      dVar13 = (double)FUN_181c9a9c5((double)*(float *)(lVar4 + uVar9 * 4) * dVar3);
      dVar13 = (dVar2 - dVar13) * dVar14;
      if (dVar13 <= 0.0) {
        dVar13 = 0.0;
      }
      *(float *)(lVar4 + uVar9 * 4) = (float)dVar13;
      uVar9 = uVar9 + 1;
    } while ((longlong)uVar9 < (longlong)(int)uVar6);
  }
  return;
}

