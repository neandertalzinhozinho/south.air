 (GhidraScript)  

void FUN_18087b680(longlong param_1,longlong *param_2)

{
  longlong lVar1;
  undefined8 uVar2;
  longlong lVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  undefined8 uVar19;
  uint uVar20;
  longlong lVar21;
  uint uVar22;
  uint uVar23;
  undefined8 *puVar24;
  int iVar25;
  int iVar26;
  ulonglong uVar27;
  ulonglong uVar28;
  longlong local_1e8;
  int iStack_1e0;
  int iStack_1dc;
  undefined8 local_1d8 [16];
  uint local_158;
  uint uStack_154;
  longlong lStack_150;
  undefined8 local_148 [4];
  undefined8 local_128;
  undefined8 uStack_120;
  undefined8 local_118;
  undefined8 uStack_110;
  undefined8 local_108;
  undefined8 uStack_100;
  undefined8 local_f8;
  undefined8 uStack_f0;
  undefined8 local_e8;
  undefined8 uStack_e0;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
  longlong lStack_c0;
  
  uVar27 = (ulonglong)(int)*(uint *)(param_1 + 0x470);
  iVar26 = 0;
  iVar25 = 0;
  local_1d8[0xf] = 0;
  local_1d8[0] = 0;
  local_158 = *(uint *)(param_1 + 0x468);
  uStack_154 = *(uint *)(param_1 + 0x470);
  lStack_150 = uVar27 << 2;
  local_1d8[1] = 0;
  local_1d8[2] = 0;
  local_1d8[3] = 0;
  local_1d8[4] = 0;
  local_1d8[5] = 0;
  local_1d8[6] = 0;
  local_1d8[7] = 0;
  local_1d8[8] = 0;
  local_1d8[9] = 0;
  local_1d8[10] = 0;
  local_1d8[0xb] = 0;
  local_1d8[0xc] = 0;
  local_1d8[0xd] = 0;
  local_1d8[0xe] = 0;
  if (0 < (int)*(uint *)(param_1 + 0x468)) {
    puVar24 = local_1d8;
    do {
      iVar25 = iVar25 + 1;
      *puVar24 = *(undefined8 *)(((param_1 + 1000) - (longlong)local_1d8) + (longlong)puVar24);
      puVar24 = puVar24 + 1;
    } while (iVar25 < (int)local_158);
    uVar27 = (ulonglong)uStack_154;
  }
  lVar21 = lStack_150;
  uVar20 = local_158;
  uVar19 = local_1d8[0xf];
  uVar18 = local_1d8[0xe];
  uVar17 = local_1d8[0xd];
  uVar16 = local_1d8[0xc];
  uVar15 = local_1d8[0xb];
  uVar14 = local_1d8[10];
  uVar13 = local_1d8[9];
  uVar12 = local_1d8[8];
  uVar11 = local_1d8[7];
  uVar10 = local_1d8[6];
  uVar9 = local_1d8[5];
  uVar8 = local_1d8[4];
  uVar7 = local_1d8[3];
  uVar6 = local_1d8[2];
  uVar5 = local_1d8[1];
  uVar4 = local_1d8[0];
  uVar28 = (ulonglong)local_158;
  uVar2 = CONCAT44(uStack_154,local_158);
  local_148[0] = local_1d8[0];
  local_148[1] = local_1d8[1];
  local_148[2] = local_1d8[2];
  local_148[3] = local_1d8[3];
  local_128 = local_1d8[4];
  uStack_120 = local_1d8[5];
  local_118 = local_1d8[6];
  uStack_110 = local_1d8[7];
  local_108 = local_1d8[8];
  uStack_100 = local_1d8[9];
  local_f8 = local_1d8[10];
  uStack_f0 = local_1d8[0xb];
  local_e8 = local_1d8[0xc];
  uStack_e0 = local_1d8[0xd];
  local_d8 = local_1d8[0xe];
  uStack_d0 = local_1d8[0xf];
  lStack_c0 = lStack_150;
  local_c8 = uVar2;
  FUN_18087a7a0(local_148);
  lVar3 = param_2[3];
  local_1d8[0] = 0;
  iStack_1e0 = (int)*(undefined8 *)(param_1 + 0x40);
  iStack_1dc = iStack_1e0 * 4;
  local_1d8[1] = 0;
  local_1d8[2] = 0;
  local_1d8[3] = 0;
  local_1d8[4] = 0;
  lVar1 = *param_2 + (longlong)(int)lVar3 * 4;
  local_1d8[5] = 0;
  local_1d8[6] = 0;
  local_1d8[7] = 0;
  local_1d8[8] = 0;
  local_1d8[9] = 0;
  local_1d8[10] = 0;
  local_1d8[0xb] = 0;
  local_1d8[0xc] = 0;
  local_1d8[0xd] = 0;
  local_1d8[0xe] = 0;
  local_1e8 = lVar1;
  if (*(char *)(param_1 + 0x58) == '\0') {
    uVar22 = (int)param_2[3] + iStack_1e0;
    uVar23 = (uVar22 - (uVar22 & 0xf)) + 0x10;
    if ((uVar22 & 0xf) == 0) {
      uVar23 = uVar22;
    }
    *(uint *)(param_2 + 3) = uVar23;
    uStack_154 = *(int *)(param_1 + 2000);
    local_1d8[0xf] = 0;
    local_158 = *(int *)(param_1 + 0x7c8);
    lStack_150 = (longlong)*(int *)(param_1 + 2000) << 2;
    if (0 < *(int *)(param_1 + 0x7c8)) {
      puVar24 = local_1d8;
      do {
        iVar26 = iVar26 + 1;
        *puVar24 = *(undefined8 *)(((param_1 + 0x748) - (longlong)local_1d8) + (longlong)puVar24);
        puVar24 = puVar24 + 1;
      } while (iVar26 < (int)local_158);
    }
    local_148[0] = local_1d8[0];
    local_148[1] = local_1d8[1];
    local_148[2] = local_1d8[2];
    local_148[3] = local_1d8[3];
    local_128 = local_1d8[4];
    uStack_120 = local_1d8[5];
    local_118 = local_1d8[6];
    uStack_110 = local_1d8[7];
    local_108 = local_1d8[8];
    uStack_100 = local_1d8[9];
    local_f8 = local_1d8[10];
    uStack_f0 = local_1d8[0xb];
    local_e8 = local_1d8[0xc];
    uStack_e0 = local_1d8[0xd];
    local_c8 = CONCAT44(uStack_154,local_158);
    local_d8 = local_1d8[0xe];
    uStack_d0 = local_1d8[0xf];
    lStack_c0 = lStack_150;
    FUN_180882de0(&local_1e8,local_148,DAT_18207a5b4,DAT_18207a1f8,DAT_18207a188);
    local_148[0] = uVar4;
    local_148[1] = uVar5;
    local_148[2] = uVar6;
    local_148[3] = uVar7;
    local_128 = uVar8;
    uStack_120 = uVar9;
    local_118 = uVar10;
    uStack_110 = uVar11;
    local_108 = uVar12;
    uStack_100 = uVar13;
    local_f8 = uVar14;
    uStack_f0 = uVar15;
    local_e8 = uVar16;
    uStack_e0 = uVar17;
    local_d8 = uVar18;
    uStack_d0 = uVar19;
    local_c8 = uVar2;
    lStack_c0 = lVar21;
    if (uVar20 != 1) {
      if (0 < (int)uVar20) {
        puVar24 = local_148;
        do {
          FUN_180001340(lVar1,*puVar24,uVar27 & 0xffffffff);
          puVar24 = puVar24 + 1;
          uVar28 = uVar28 - 1;
        } while (uVar28 != 0);
      }
      goto LAB_18087baf9;
    }
  }
  else {
    uVar22 = (int)param_2[3] + iStack_1e0;
    uVar23 = (uVar22 - (uVar22 & 0xf)) + 0x10;
    if ((uVar22 & 0xf) == 0) {
      uVar23 = uVar22;
    }
    *(uint *)(param_2 + 3) = uVar23;
    uStack_154 = *(int *)(param_1 + 2000);
    local_1d8[0xf] = 0;
    local_158 = *(int *)(param_1 + 0x7c8);
    lStack_150 = (longlong)*(int *)(param_1 + 2000) << 2;
    if (0 < *(int *)(param_1 + 0x7c8)) {
      puVar24 = local_1d8;
      do {
        iVar26 = iVar26 + 1;
        *puVar24 = *(undefined8 *)(((param_1 + 0x748) - (longlong)local_1d8) + (longlong)puVar24);
        puVar24 = puVar24 + 1;
      } while (iVar26 < (int)local_158);
    }
    local_148[0] = local_1d8[0];
    local_148[1] = local_1d8[1];
    local_148[2] = local_1d8[2];
    local_148[3] = local_1d8[3];
    local_128 = local_1d8[4];
    uStack_120 = local_1d8[5];
    local_118 = local_1d8[6];
    uStack_110 = local_1d8[7];
    local_108 = local_1d8[8];
    uStack_100 = local_1d8[9];
    local_f8 = local_1d8[10];
    uStack_f0 = local_1d8[0xb];
    local_e8 = local_1d8[0xc];
    uStack_e0 = local_1d8[0xd];
    local_c8 = CONCAT44(uStack_154,local_158);
    local_d8 = local_1d8[0xe];
    uStack_d0 = local_1d8[0xf];
    lStack_c0 = lStack_150;
    FUN_180882de0(&local_1e8,local_148,DAT_18207a5a8,DAT_18207a1f8,DAT_18207a248);
    local_148[0] = uVar4;
    local_148[1] = uVar5;
    local_148[2] = uVar6;
    local_148[3] = uVar7;
    local_128 = uVar8;
    uStack_120 = uVar9;
    local_118 = uVar10;
    uStack_110 = uVar11;
    local_108 = uVar12;
    uStack_100 = uVar13;
    local_f8 = uVar14;
    uStack_f0 = uVar15;
    local_e8 = uVar16;
    uStack_e0 = uVar17;
    local_d8 = uVar18;
    uStack_d0 = uVar19;
    local_c8 = uVar2;
    lStack_c0 = lVar21;
    if (uVar20 != 1) {
      if (0 < (int)uVar20) {
        puVar24 = local_148;
        do {
          FUN_180001340(lVar1,*puVar24,uVar27 & 0xffffffff);
          puVar24 = puVar24 + 1;
          uVar28 = uVar28 - 1;
        } while (uVar28 != 0);
      }
      goto LAB_18087baf9;
    }
  }
  lStack_c0 = lVar21;
  uStack_d0 = uVar19;
  local_d8 = uVar18;
  uStack_e0 = uVar17;
  local_e8 = uVar16;
  uStack_f0 = uVar15;
  local_f8 = uVar14;
  uStack_100 = uVar13;
  local_108 = uVar12;
  uStack_110 = uVar11;
  local_118 = uVar10;
  uStack_120 = uVar9;
  local_128 = uVar8;
  local_148[3] = uVar7;
  local_148[2] = uVar6;
  local_148[1] = uVar5;
  local_148[0] = uVar4;
  if (0 < (int)uVar20) {
    local_c8 = uVar2;
    FUN_180001340(lVar1,uVar4,uVar27 & 0xffffffff);
  }
LAB_18087baf9:
  *(int *)(param_2 + 3) = (int)lVar3;
  return;
}

 (GhidraScript)  
