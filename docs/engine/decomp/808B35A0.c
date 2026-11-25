// FUN_1808b35a0 @ 0x1808b35a0

void FUN_1808b35a0(longlong param_1,longlong param_2,longlong *param_3,longlong *param_4,
                  char param_5)

{
  longlong lVar1;
  longlong lVar2;
  int iVar3;
  int iVar4;
  longlong lVar5;
  longlong lVar6;
  undefined4 uVar7;
  uint uVar8;
  undefined8 *puVar9;
  int iVar10;
  longlong lVar11;
  uint uVar12;
  undefined8 local_868 [128];
  int local_468;
  int local_464;
  undefined8 local_458 [128];
  int local_58;
  
  iVar3 = *(int *)(param_1 + 0x404);
  iVar4 = (int)param_4[3];
  lVar1 = *param_4 + (longlong)iVar4 * 4;
  uVar12 = iVar3 + iVar4;
  uVar8 = (uVar12 - (uVar12 & 0xf)) + 0x10;
  if ((uVar12 & 0xf) == 0) {
    uVar8 = uVar12;
  }
  *(uint *)(param_4 + 3) = uVar8;
  lVar2 = *param_4 + (longlong)(int)uVar8 * 4;
  uVar8 = uVar8 + iVar3;
  uVar12 = (uVar8 - (uVar8 & 0xf)) + 0x10;
  if ((uVar8 & 0xf) == 0) {
    uVar12 = uVar8;
  }
  *(uint *)(param_4 + 3) = uVar12;
  uVar7 = DAT_182079ea8;
  lVar5 = param_3[1];
  lVar11 = *param_3;
  if (lVar11 == lVar5) {
    *(int *)(param_4 + 3) = iVar4;
  }
  else {
    do {
      lVar6 = *(longlong *)(lVar11 + 8);
      if ((*(int *)(lVar11 + 0x10) == 1) && (param_1 != param_2)) {
        FUN_1800010a0(*(undefined8 *)(param_2 + lVar6 * 8),*(undefined8 *)(param_1 + lVar6 * 8),
                      iVar3);
      }
      else {
        local_868[0] = 0;
        FUN_181798f42(local_868 + 1,0,0x3f8);
        puVar9 = local_868;
        iVar10 = 0;
        local_468 = 2;
        local_464 = iVar3;
        do {
          iVar10 = iVar10 + 1;
          *puVar9 = *(undefined8 *)
                     (((longlong)(int)lVar6 * 8 - (longlong)local_868) + param_1 + (longlong)puVar9)
          ;
          puVar9 = puVar9 + 1;
        } while (iVar10 < local_468);
        local_458[0] = 0;
        FUN_181798f42(local_458 + 1,0,0x3f8);
        puVar9 = local_458;
        iVar10 = 0;
        local_58 = 2;
        do {
          iVar10 = iVar10 + 1;
          *puVar9 = *(undefined8 *)
                     (((longlong)(int)lVar6 * 8 - (longlong)local_458) + param_2 + (longlong)puVar9)
          ;
          puVar9 = puVar9 + 1;
        } while (iVar10 < local_58);
        FUN_1800015b0(local_458[0],local_458[1],lVar1,iVar3);
        FUN_1800011c0(local_458[1],local_458[0],lVar2,iVar3);
        if (param_5 == '\0') {
          FUN_1800010a0(lVar1,local_868[0],local_464);
          FUN_1800010a0(lVar2,local_868[1],local_464);
        }
        else {
          FUN_180001070(lVar1,uVar7,local_868[0],local_464);
          FUN_180001070(lVar2,uVar7,local_868[1],local_464);
        }
      }
      lVar11 = lVar11 + 0x18;
    } while (lVar11 != lVar5);
    *(int *)(param_4 + 3) = iVar4;
  }
  return;
}

