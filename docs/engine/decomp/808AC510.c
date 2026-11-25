// FUN_1808ac510 @ 0x1808ac510

void FUN_1808ac510(longlong *param_1,undefined8 *param_2,undefined8 *param_3)

{
  undefined4 uVar1;
  longlong *plVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  longlong lVar5;
  undefined8 *puVar6;
  uint uVar7;
  uint uVar8;
  int iVar9;
  longlong lVar10;
  longlong lVar11;
  longlong lVar12;
  longlong lVar13;
  int iVar14;
  undefined8 local_e98 [16];
  uint local_e18;
  int iStack_e14;
  longlong lStack_e10;
  undefined8 local_e08 [16];
  uint local_d88;
  int iStack_d84;
  longlong lStack_d80;
  undefined8 local_d78;
  longlong *local_d68;
  undefined4 *local_d60;
  undefined8 local_d58;
  int iStack_d50;
  int iStack_d4c;
  undefined8 local_d48;
  int iStack_d40;
  int iStack_d3c;
  undefined8 local_d38;
  undefined8 uStack_d30;
  undefined8 local_d28;
  undefined8 uStack_d20;
  undefined8 local_d18;
  undefined8 uStack_d10;
  undefined8 local_d08;
  undefined8 uStack_d00;
  undefined8 local_cf8;
  undefined8 uStack_cf0;
  undefined8 local_ce8;
  undefined8 uStack_ce0;
  undefined8 local_cd8;
  undefined8 uStack_cd0;
  undefined8 local_cc8;
  undefined8 uStack_cc0;
  undefined8 local_cb8;
  longlong lStack_cb0;
  undefined8 local_ca8;
  undefined4 local_c98;
  undefined4 uStack_c94;
  int iStack_c90;
  int iStack_c8c;
  undefined4 local_c88;
  undefined4 uStack_c84;
  int iStack_c80;
  int iStack_c7c;
  longlong local_c78;
  undefined1 local_c70 [1016];
  int local_878;
  int local_874;
  longlong local_870;
  longlong local_868;
  undefined1 local_860 [1016];
  int local_468;
  int local_464;
  longlong local_460;
  longlong local_458;
  undefined1 local_450 [1016];
  int local_58;
  int local_54;
  longlong local_50;
  
  plVar2 = (longlong *)*param_1;
  local_d60 = (undefined4 *)(*param_1 + 0x18);
  uVar1 = *local_d60;
  uVar3 = *(undefined8 *)(param_1[1] + 0x40);
  uVar4 = *(undefined8 *)(param_1[1] + 0x48);
  local_c78 = 0;
  FUN_181798f42(local_c70,0,0x3f8);
  iVar14 = (int)uVar3;
  lVar10 = 0;
  local_870 = (longlong)iVar14 << 2;
  local_878 = (int)uVar4;
  lVar11 = (longlong)local_878;
  local_874 = iVar14;
  if (0 < local_878) {
    do {
      *(longlong *)(local_c70 + lVar10 * 8 + -8) = *plVar2 + (longlong)(int)plVar2[3] * 4;
      uVar7 = (int)plVar2[3] + iVar14;
      uVar8 = (uVar7 - (uVar7 & 0xf)) + 0x10;
      if ((uVar7 & 0xf) == 0) {
        uVar8 = uVar7;
      }
      lVar10 = lVar10 + 1;
      *(uint *)(plVar2 + 3) = uVar8;
    } while (lVar10 < lVar11);
  }
  local_d68 = plVar2 + 3;
  lVar10 = *local_d68;
  uVar3 = *(undefined8 *)(param_1[1] + 0x38);
  uVar4 = *(undefined8 *)(param_1[1] + 0x48);
  local_458 = 0;
  FUN_181798f42(local_450,0,0x3f8);
  iVar14 = (int)uVar3;
  lVar11 = 0;
  local_50 = (longlong)iVar14 << 2;
  local_58 = (int)uVar4;
  lVar13 = (longlong)local_58;
  local_54 = iVar14;
  if (0 < local_58) {
    do {
      *(longlong *)(local_450 + lVar11 * 8 + -8) = *plVar2 + (longlong)(int)plVar2[3] * 4;
      uVar7 = (int)plVar2[3] + iVar14;
      uVar8 = (uVar7 - (uVar7 & 0xf)) + 0x10;
      if ((uVar7 & 0xf) == 0) {
        uVar8 = uVar7;
      }
      lVar11 = lVar11 + 1;
      *(uint *)(plVar2 + 3) = uVar8;
    } while (lVar11 < lVar13);
  }
  lVar11 = plVar2[3];
  uVar3 = *(undefined8 *)(param_1[1] + 0x40);
  uVar4 = *(undefined8 *)(param_1[1] + 0x48);
  local_868 = 0;
  FUN_181798f42(local_860,0,0x3f8);
  local_464 = (int)uVar3;
  lVar13 = 0;
  local_460 = (longlong)local_464 << 3;
  local_468 = (int)uVar4;
  lVar12 = (longlong)local_468;
  if (0 < local_468) {
    iVar14 = local_464 * 2;
    do {
      *(longlong *)(local_860 + lVar13 * 8 + -8) = *plVar2 + (longlong)(int)plVar2[3] * 4;
      uVar7 = (int)plVar2[3] + iVar14;
      uVar8 = (uVar7 - (uVar7 & 0xf)) + 0x10;
      if ((uVar7 & 0xf) == 0) {
        uVar8 = uVar7;
      }
      lVar13 = lVar13 + 1;
      *(uint *)(plVar2 + 3) = uVar8;
    } while (lVar13 < lVar12);
  }
  local_d38 = *param_3;
  uStack_d30 = param_3[1];
  local_d28 = param_3[2];
  uStack_d20 = param_3[3];
  local_d18 = param_3[4];
  uStack_d10 = param_3[5];
  local_d08 = param_3[6];
  uStack_d00 = param_3[7];
  local_cf8 = param_3[8];
  uStack_cf0 = param_3[9];
  local_ce8 = param_3[10];
  uStack_ce0 = param_3[0xb];
  local_cd8 = param_3[0xc];
  uStack_cd0 = param_3[0xd];
  local_cc8 = param_3[0xe];
  uStack_cc0 = param_3[0xf];
  local_cb8 = param_3[0x10];
  lStack_cb0 = param_3[0x11];
  local_ca8 = param_3[0x12];
  local_e08[0] = *param_2;
  local_e08[1] = param_2[1];
  local_e08[2] = param_2[2];
  local_e08[3] = param_2[3];
  local_e08[4] = param_2[4];
  local_e08[5] = param_2[5];
  local_e08[6] = param_2[6];
  local_e08[7] = param_2[7];
  local_e08[8] = param_2[8];
  local_e08[9] = param_2[9];
  local_e08[10] = param_2[10];
  local_e08[0xb] = param_2[0xb];
  local_e08[0xc] = param_2[0xc];
  local_e08[0xd] = param_2[0xd];
  local_e08[0xe] = param_2[0xe];
  local_e08[0xf] = param_2[0xf];
  local_d88 = *(uint *)(param_2 + 0x10);
  iStack_d84 = *(undefined4 *)((longlong)param_2 + 0x84);
  lStack_d80 = param_2[0x11];
  local_d78 = param_2[0x12];
  FUN_1808b3ed0(param_1[1],&local_c78,&local_458,&local_868,local_e08,&local_d38,
                *(undefined1 *)param_1[2],*(undefined1 *)param_1[3],plVar2);
  lVar13 = param_1[1];
  iVar14 = 0;
  if (*(longlong *)(lVar13 + 0x48) != 0) {
    lVar12 = 0;
    do {
      lVar5 = *param_1;
      iVar9 = 0;
      iStack_e14 = *(int *)(lVar13 + 0x230);
      local_e98[0] = 0;
      local_e98[0xf] = 0;
      local_e18 = *(int *)(lVar13 + 0x228);
      lStack_e10 = (longlong)*(int *)(lVar13 + 0x230) << 2;
      local_e98[1] = 0;
      local_e98[2] = 0;
      local_e98[3] = 0;
      local_e98[4] = 0;
      local_e98[5] = 0;
      local_e98[6] = 0;
      local_e98[7] = 0;
      local_e98[8] = 0;
      local_e98[9] = 0;
      local_e98[10] = 0;
      local_e98[0xb] = 0;
      local_e98[0xc] = 0;
      local_e98[0xd] = 0;
      local_e98[0xe] = 0;
      if (0 < *(int *)(lVar13 + 0x228)) {
        puVar6 = local_e98;
        do {
          iVar9 = iVar9 + 1;
          *puVar6 = *(undefined8 *)(((lVar13 + 0x1a8) - (longlong)local_e98) + (longlong)puVar6);
          puVar6 = puVar6 + 1;
        } while (iVar9 < (int)local_e18);
      }
      local_d58 = *(undefined8 *)(local_c70 + lVar12 + -8);
      local_e08[0xf] = 0;
      iStack_d50 = local_874;
      iStack_d4c = local_874 * 4;
      iVar9 = 0;
      local_e08[0] = 0;
      local_d88 = *(int *)(lVar13 + 0xf18);
      iStack_d84 = *(int *)(lVar13 + 0xf20);
      lStack_d80 = (longlong)*(int *)(lVar13 + 0xf20) << 2;
      local_e08[1] = 0;
      local_e08[2] = 0;
      local_e08[3] = 0;
      local_e08[4] = 0;
      local_e08[5] = 0;
      local_e08[6] = 0;
      local_e08[7] = 0;
      local_e08[8] = 0;
      local_e08[9] = 0;
      local_e08[10] = 0;
      local_e08[0xb] = 0;
      local_e08[0xc] = 0;
      local_e08[0xd] = 0;
      local_e08[0xe] = 0;
      if (0 < *(int *)(lVar13 + 0xf18)) {
        puVar6 = local_e08;
        do {
          iVar9 = iVar9 + 1;
          *puVar6 = *(undefined8 *)(((lVar13 + 0xe98) - (longlong)local_e08) + (longlong)puVar6);
          puVar6 = puVar6 + 1;
        } while (iVar9 < (int)local_d88);
      }
      iStack_c7c = iStack_d84 * 4;
      iStack_d40 = iStack_d84;
      iStack_d3c = iStack_c7c;
      local_d38 = local_e98[0];
      uStack_d30 = local_e98[1];
      uVar3 = *(undefined8 *)((longlong)local_e08 + lVar12);
      local_d28 = local_e98[2];
      uStack_d20 = local_e98[3];
      local_d18 = local_e98[4];
      uStack_d10 = local_e98[5];
      local_d08 = local_e98[6];
      uStack_d00 = local_e98[7];
      local_cf8 = local_e98[8];
      uStack_cf0 = local_e98[9];
      local_ce8 = local_e98[10];
      uStack_ce0 = local_e98[0xb];
      local_cd8 = local_e98[0xc];
      uStack_cd0 = local_e98[0xd];
      local_cb8 = CONCAT44(iStack_e14,local_e18);
      local_cc8 = local_e98[0xe];
      uStack_cc0 = local_e98[0xf];
      lStack_cb0 = lStack_e10;
      local_d48._0_4_ = (undefined4)uVar3;
      local_d48._4_4_ = (undefined4)((ulonglong)uVar3 >> 0x20);
      local_c88 = (undefined4)local_d48;
      uStack_c84 = local_d48._4_4_;
      local_c98 = (undefined4)local_d58;
      uStack_c94 = local_d58._4_4_;
      iStack_c90 = iStack_d50;
      iStack_c8c = iStack_d4c;
      local_d48 = uVar3;
      iStack_c80 = iStack_d84;
      FUN_1808b30c0(&local_c88,&local_c98,lVar13 + 0x68,&local_d38,lVar5);
      lVar13 = param_1[1];
      iVar14 = iVar14 + 1;
      lVar12 = lVar12 + 8;
    } while ((ulonglong)(longlong)iVar14 < *(ulonglong *)(lVar13 + 0x48));
  }
  lVar13 = param_1[1];
  local_e08[0] = 0;
  iVar14 = 0;
  local_e08[1] = 0;
  local_e08[2] = 0;
  local_e08[0xf] = 0;
  iStack_d84 = *(int *)(lVar13 + 0xf20);
  local_d88 = *(uint *)(lVar13 + 0xf18);
  lStack_d80 = (longlong)*(int *)(lVar13 + 0xf20) << 2;
  local_e08[3] = 0;
  local_e08[4] = 0;
  local_e08[5] = 0;
  local_e08[6] = 0;
  local_e08[7] = 0;
  local_e08[8] = 0;
  local_e08[9] = 0;
  local_e08[10] = 0;
  local_e08[0xb] = 0;
  local_e08[0xc] = 0;
  local_e08[0xd] = 0;
  local_e08[0xe] = 0;
  if (0 < (int)*(uint *)(lVar13 + 0xf18)) {
    puVar6 = local_e08;
    do {
      iVar14 = iVar14 + 1;
      *puVar6 = *(undefined8 *)(((lVar13 + 0xe98) - (longlong)local_e08) + (longlong)puVar6);
      puVar6 = puVar6 + 1;
    } while (iVar14 < (int)local_d88);
  }
  local_e98[0] = 0;
  local_e98[1] = 0;
  local_e98[2] = 0;
  local_e98[0xf] = 0;
  iStack_e14 = (int)(*(ulonglong *)(param_1[1] + 0x38) >> 1);
  lStack_e10 = (longlong)iStack_e14 << 2;
  local_e98[3] = 0;
  local_e98[4] = 0;
  local_e98[5] = 0;
  local_e98[6] = 0;
  local_e98[7] = 0;
  local_e98[8] = 0;
  local_e98[9] = 0;
  local_e98[10] = 0;
  local_e98[0xb] = 0;
  local_e98[0xc] = 0;
  local_e98[0xd] = 0;
  local_e98[0xe] = 0;
  local_e18 = local_d88;
  if (0 < (int)local_d88) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(local_e98,local_e08,(ulonglong)local_d88 << 3);
  }
  lVar13 = param_1[1];
  local_d38 = 0;
  uStack_d30 = 0;
  local_d28 = 0;
  uStack_d20 = 0;
  local_d18 = 0;
  uStack_d10 = 0;
  local_d08 = 0;
  uStack_d00 = 0;
  local_cf8 = 0;
  uStack_cf0 = 0;
  local_ce8 = 0;
  uStack_ce0 = 0;
  local_cd8 = 0;
  uStack_cd0 = 0;
  local_cc8 = 0;
  uStack_cc0 = 0;
  local_cb8 = CONCAT44(iStack_e14,local_d88);
  lStack_cb0 = lStack_e10;
  FUN_1808c4420(lVar13 + ((longlong)*(int *)(lVar13 + 0x2bd0) * 3 + 0x57b) * 8,&local_d38);
  lVar12 = param_1[4];
  *(uint *)(lVar13 + 0x2bd0) = (uint)(*(int *)(lVar13 + 0x2bd0) == 0);
  FUN_180880ae0(lVar12);
  *(int *)(plVar2 + 3) = (int)lVar11;
  *(int *)local_d68 = (int)lVar10;
  *local_d60 = uVar1;
  return;
}

