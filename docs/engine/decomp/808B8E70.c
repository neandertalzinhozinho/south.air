// FUN_1808b8e70 @ 0x1808b8e70

/* WARNING: Function: __chkstk replaced with injection: alloca_probe */

void FUN_1808b8e70(undefined8 *param_1,longlong *param_2,longlong *param_3,longlong param_4,
                  longlong *param_5)

{
  int iVar1;
  longlong lVar2;
  longlong lVar3;
  longlong lVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  longlong *plVar8;
  longlong *plVar9;
  longlong *plVar10;
  uint uVar11;
  undefined4 *puVar12;
  longlong *plVar13;
  int iVar14;
  longlong lVar15;
  longlong lVar16;
  longlong lVar17;
  longlong lVar18;
  undefined4 *puVar19;
  longlong lVar20;
  uint uVar21;
  ulonglong uVar22;
  ulonglong uVar23;
  undefined1 auVar24 [16];
  undefined1 auVar25 [16];
  longlong alStack_15f8 [2];
  undefined4 local_15e4;
  longlong alStack_15e0 [17];
  undefined1 local_1558 [16];
  int local_1548;
  undefined8 local_1538 [4];
  undefined8 local_1518;
  undefined8 uStack_1510;
  undefined8 local_1508;
  undefined8 uStack_1500;
  undefined8 local_14f8;
  undefined8 uStack_14f0;
  undefined8 local_14e8;
  undefined8 uStack_14e0;
  undefined8 local_14d8;
  undefined8 uStack_14d0;
  undefined8 local_14c8;
  undefined8 uStack_14c0;
  undefined8 local_14b8;
  longlong lStack_14b0;
  longlong local_14a8;
  undefined1 auStack_14a0 [1016];
  uint local_10a8;
  uint local_10a4;
  longlong local_10a0;
  longlong local_1098;
  undefined1 auStack_1090 [1016];
  uint local_c98;
  uint local_c94;
  longlong local_c90;
  longlong local_c88 [130];
  longlong local_878;
  undefined1 auStack_870 [1016];
  uint local_478;
  uint local_474;
  longlong local_470;
  longlong local_468 [132];
  undefined8 uStack_48;
  
  uStack_48 = 0x1808b8e9d;
  local_1548 = (int)param_3[3];
  local_15e4 = (undefined4)param_5[3];
  lVar15 = 8;
  plVar9 = param_2;
  plVar8 = &local_878;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar18 = plVar10[1];
    lVar16 = plVar10[2];
    lVar17 = plVar10[3];
    *plVar13 = *plVar10;
    plVar13[1] = lVar18;
    lVar18 = plVar10[4];
    lVar2 = plVar10[5];
    plVar13[2] = lVar16;
    plVar13[3] = lVar17;
    lVar16 = plVar10[6];
    lVar17 = plVar10[7];
    plVar13[4] = lVar18;
    plVar13[5] = lVar2;
    lVar18 = plVar10[8];
    lVar2 = plVar10[9];
    plVar13[6] = lVar16;
    plVar13[7] = lVar17;
    lVar16 = plVar10[10];
    lVar17 = plVar10[0xb];
    plVar13[8] = lVar18;
    plVar13[9] = lVar2;
    lVar18 = plVar10[0xc];
    lVar2 = plVar10[0xd];
    plVar13[10] = lVar16;
    plVar13[0xb] = lVar17;
    lVar16 = plVar10[0xe];
    lVar17 = plVar10[0xf];
    plVar13[0xc] = lVar18;
    plVar13[0xd] = lVar2;
    plVar13[0xe] = lVar16;
    plVar13[0xf] = lVar17;
    lVar15 = lVar15 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar15 != 0);
  lVar18 = plVar10[0x11];
  lVar15 = 0;
  local_14a8 = 0;
  plVar13[0x10] = plVar10[0x10];
  plVar13[0x11] = lVar18;
  FUN_181798f42(auStack_14a0,0,0x3f8);
  uVar23 = (ulonglong)(int)local_474;
  lVar18 = 0;
  uVar22 = (ulonglong)(int)local_478;
  local_10a8 = local_478;
  local_10a4 = local_474;
  local_10a0 = uVar23 << 2;
  if (0 < (int)local_478) {
    uVar21 = *(uint *)(param_5 + 3);
    do {
      uVar5 = local_474 + uVar21;
      *(longlong *)(auStack_14a0 + lVar18 * 8 + -8) = *param_5 + (longlong)(int)uVar21 * 4;
      uVar21 = (uVar5 - (uVar5 & 0xf)) + 0x10;
      if ((uVar5 & 0xf) == 0) {
        uVar21 = uVar5;
      }
      lVar18 = lVar18 + 1;
      *(uint *)(param_5 + 3) = uVar21;
    } while (lVar18 < (longlong)uVar22);
    uVar23 = (ulonglong)local_10a4;
    uVar22 = (ulonglong)local_10a8;
  }
  uVar21 = (uint)uVar22;
  lVar16 = 8;
  lVar18 = 8;
  plVar9 = local_468;
  do {
    plVar10 = param_2;
    plVar8 = plVar9;
    lVar17 = plVar10[1];
    lVar2 = plVar10[2];
    lVar3 = plVar10[3];
    *plVar8 = *plVar10;
    plVar8[1] = lVar17;
    lVar17 = plVar10[4];
    lVar20 = plVar10[5];
    plVar8[2] = lVar2;
    plVar8[3] = lVar3;
    lVar2 = plVar10[6];
    lVar3 = plVar10[7];
    plVar8[4] = lVar17;
    plVar8[5] = lVar20;
    lVar17 = plVar10[8];
    lVar20 = plVar10[9];
    plVar8[6] = lVar2;
    plVar8[7] = lVar3;
    lVar2 = plVar10[10];
    lVar3 = plVar10[0xb];
    plVar8[8] = lVar17;
    plVar8[9] = lVar20;
    lVar17 = plVar10[0xc];
    lVar20 = plVar10[0xd];
    plVar8[10] = lVar2;
    plVar8[0xb] = lVar3;
    lVar2 = plVar10[0xe];
    lVar3 = plVar10[0xf];
    plVar8[0xc] = lVar17;
    plVar8[0xd] = lVar20;
    plVar8[0xe] = lVar2;
    plVar8[0xf] = lVar3;
    lVar18 = lVar18 + -1;
    plVar9 = plVar8 + 0x10;
    param_2 = plVar10 + 0x10;
  } while (lVar18 != 0);
  lVar18 = plVar10[0x11];
  plVar8[0x10] = plVar10[0x10];
  plVar8[0x11] = lVar18;
  plVar9 = local_c88;
  plVar8 = &local_14a8;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar18 = plVar13[1];
    lVar17 = plVar13[2];
    lVar2 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar18;
    lVar18 = plVar13[4];
    lVar3 = plVar13[5];
    plVar10[2] = lVar17;
    plVar10[3] = lVar2;
    lVar17 = plVar13[6];
    lVar2 = plVar13[7];
    plVar10[4] = lVar18;
    plVar10[5] = lVar3;
    lVar18 = plVar13[8];
    lVar3 = plVar13[9];
    plVar10[6] = lVar17;
    plVar10[7] = lVar2;
    lVar17 = plVar13[10];
    lVar2 = plVar13[0xb];
    plVar10[8] = lVar18;
    plVar10[9] = lVar3;
    lVar18 = plVar13[0xc];
    lVar3 = plVar13[0xd];
    plVar10[10] = lVar17;
    plVar10[0xb] = lVar2;
    lVar17 = plVar13[0xe];
    lVar2 = plVar13[0xf];
    plVar10[0xc] = lVar18;
    plVar10[0xd] = lVar3;
    plVar10[0xe] = lVar17;
    plVar10[0xf] = lVar2;
    lVar16 = lVar16 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar16 != 0);
  lVar18 = plVar13[0x11];
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar18;
  if (0 < (int)uVar21) {
    lVar18 = 0;
    uVar22 = uVar22 & 0xffffffff;
    do {
      FUN_1801c84a0(*(undefined8 *)((longlong)local_468 + lVar18),
                    *(undefined8 *)((longlong)local_c88 + lVar18),uVar23 & 0xffffffff);
      lVar18 = lVar18 + 8;
      uVar22 = uVar22 - 1;
    } while (uVar22 != 0);
  }
  lVar18 = 8;
  plVar9 = local_c88;
  plVar8 = &local_14a8;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar16 = plVar13[1];
    lVar17 = plVar13[2];
    lVar2 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar16;
    lVar16 = plVar13[4];
    lVar3 = plVar13[5];
    plVar10[2] = lVar17;
    plVar10[3] = lVar2;
    lVar17 = plVar13[6];
    lVar2 = plVar13[7];
    plVar10[4] = lVar16;
    plVar10[5] = lVar3;
    lVar16 = plVar13[8];
    lVar3 = plVar13[9];
    plVar10[6] = lVar17;
    plVar10[7] = lVar2;
    lVar17 = plVar13[10];
    lVar2 = plVar13[0xb];
    plVar10[8] = lVar16;
    plVar10[9] = lVar3;
    lVar16 = plVar13[0xc];
    lVar3 = plVar13[0xd];
    plVar10[10] = lVar17;
    plVar10[0xb] = lVar2;
    lVar17 = plVar13[0xe];
    lVar2 = plVar13[0xf];
    plVar10[0xc] = lVar16;
    plVar10[0xd] = lVar3;
    plVar10[0xe] = lVar17;
    plVar10[0xf] = lVar2;
    lVar18 = lVar18 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar18 != 0);
  lVar18 = plVar13[0x11];
  alStack_15e0[1] = *param_1;
  alStack_15e0[2] = param_1[1];
  alStack_15e0[5] = param_1[4];
  alStack_15e0[6] = param_1[5];
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar18;
  alStack_15e0[3] = param_1[2];
  alStack_15e0[4] = param_1[3];
  alStack_15e0[9] = param_1[8];
  alStack_15e0[10] = param_1[9];
  alStack_15e0[7] = param_1[6];
  alStack_15e0[8] = param_1[7];
  alStack_15e0[0xd] = param_1[0xc];
  alStack_15e0[0xe] = param_1[0xd];
  uVar5 = *(uint *)*(undefined1 (*) [16])(param_1 + 0x10);
  alStack_15e0[0xb] = param_1[10];
  alStack_15e0[0xc] = param_1[0xb];
  alStack_15e0[0xf] = param_1[0xe];
  alStack_15e0[0x10] = param_1[0xf];
  local_1558 = *(undefined1 (*) [16])(param_1 + 0x10);
  if (0 < (int)uVar5) {
    lVar18 = 0;
    uVar22 = (ulonglong)uVar5;
    lVar16 = (longlong)*(int *)((longlong)param_1 + 0x84);
    do {
      lVar2 = *(longlong *)((longlong)local_c88 + lVar18);
      lVar17 = 0;
      lVar3 = *(longlong *)((longlong)alStack_15e0 + lVar18 + 8);
      if (3 < lVar16) {
        lVar20 = (lVar16 - 4U >> 2) + 1;
        lVar17 = lVar20 * 4;
        puVar12 = (undefined4 *)(lVar3 + 8);
        puVar19 = (undefined4 *)(lVar2 + 8);
        do {
          puVar12[-2] = puVar19[-2];
          puVar12[-1] = 0;
          *puVar12 = puVar19[-1];
          puVar12[1] = 0;
          puVar12[2] = *puVar19;
          puVar12[3] = 0;
          puVar12[4] = puVar19[1];
          puVar12[5] = 0;
          lVar20 = lVar20 + -1;
          puVar12 = puVar12 + 8;
          puVar19 = puVar19 + 4;
        } while (lVar20 != 0);
      }
      for (; lVar17 < lVar16; lVar17 = lVar17 + 1) {
        *(undefined4 *)(lVar3 + lVar17 * 8) = *(undefined4 *)(lVar2 + lVar17 * 4);
        *(undefined4 *)(lVar3 + 4 + lVar17 * 8) = 0;
      }
      lVar18 = lVar18 + 8;
      uVar22 = uVar22 - 1;
    } while (uVar22 != 0);
  }
  iVar1 = (int)param_3[3];
  local_14a8 = 0;
  FUN_181798f42(auStack_14a0,0,0x3f8);
  local_10a8 = uVar21;
  lVar18 = 0;
  local_10a4 = iVar1;
  local_10a0 = (longlong)iVar1 << 2;
  if (0 < (int)uVar21) {
    uVar5 = *(uint *)(param_5 + 3);
    do {
      uVar6 = uVar5 + iVar1;
      *(longlong *)(auStack_14a0 + lVar18 * 8 + -8) = *param_5 + (longlong)(int)uVar5 * 4;
      uVar5 = (uVar6 - (uVar6 & 0xf)) + 0x10;
      if ((uVar6 & 0xf) == 0) {
        uVar5 = uVar6;
      }
      lVar18 = lVar18 + 1;
      *(uint *)(param_5 + 3) = uVar5;
    } while (lVar18 < (int)uVar21);
  }
  uVar5 = local_10a4;
  uVar21 = local_10a8;
  auVar25 = *(undefined1 (*) [16])(param_1 + 0x10);
  lVar18 = 8;
  alStack_15e0[1] = *param_1;
  alStack_15e0[2] = param_1[1];
  alStack_15e0[3] = param_1[2];
  alStack_15e0[4] = param_1[3];
  alStack_15e0[5] = param_1[4];
  alStack_15e0[6] = param_1[5];
  alStack_15e0[7] = param_1[6];
  alStack_15e0[8] = param_1[7];
  alStack_15e0[9] = param_1[8];
  alStack_15e0[10] = param_1[9];
  alStack_15e0[0xb] = param_1[10];
  alStack_15e0[0xc] = param_1[0xb];
  alStack_15e0[0xd] = param_1[0xc];
  alStack_15e0[0xe] = param_1[0xd];
  alStack_15e0[0xf] = param_1[0xe];
  alStack_15e0[0x10] = param_1[0xf];
  local_1558 = auVar25;
  plVar9 = local_c88;
  plVar8 = &local_14a8;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar16 = plVar13[1];
    lVar17 = plVar13[2];
    lVar2 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar16;
    lVar16 = plVar13[4];
    lVar3 = plVar13[5];
    plVar10[2] = lVar17;
    plVar10[3] = lVar2;
    lVar17 = plVar13[6];
    lVar2 = plVar13[7];
    plVar10[4] = lVar16;
    plVar10[5] = lVar3;
    lVar16 = plVar13[8];
    lVar3 = plVar13[9];
    plVar10[6] = lVar17;
    plVar10[7] = lVar2;
    lVar17 = plVar13[10];
    lVar2 = plVar13[0xb];
    plVar10[8] = lVar16;
    plVar10[9] = lVar3;
    lVar16 = plVar13[0xc];
    lVar3 = plVar13[0xd];
    plVar10[10] = lVar17;
    plVar10[0xb] = lVar2;
    lVar17 = plVar13[0xe];
    lVar2 = plVar13[0xf];
    plVar10[0xc] = lVar16;
    plVar10[0xd] = lVar3;
    plVar10[0xe] = lVar17;
    plVar10[0xf] = lVar2;
    lVar18 = lVar18 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar18 != 0);
  lVar18 = plVar13[0x11];
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar18;
  if (0 < (int)auVar25._0_4_) {
    lVar18 = 0;
    uVar22 = (ulonglong)auVar25._0_4_;
    do {
      FUN_180001280(*(undefined8 *)((longlong)alStack_15e0 + lVar18 + 8),
                    *(undefined8 *)((longlong)local_c88 + lVar18),*(undefined8 *)(*param_3 + 8),
                    *(undefined8 *)param_3[1]);
      lVar18 = lVar18 + 8;
      uVar22 = uVar22 - 1;
    } while (uVar22 != 0);
  }
  lVar18 = 8;
  plVar9 = local_c88;
  plVar8 = &local_14a8;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar16 = plVar13[1];
    lVar17 = plVar13[2];
    lVar2 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar16;
    lVar16 = plVar13[4];
    lVar3 = plVar13[5];
    plVar10[2] = lVar17;
    plVar10[3] = lVar2;
    lVar17 = plVar13[6];
    lVar2 = plVar13[7];
    plVar10[4] = lVar16;
    plVar10[5] = lVar3;
    lVar16 = plVar13[8];
    lVar3 = plVar13[9];
    plVar10[6] = lVar17;
    plVar10[7] = lVar2;
    lVar17 = plVar13[10];
    lVar2 = plVar13[0xb];
    plVar10[8] = lVar16;
    plVar10[9] = lVar3;
    lVar16 = plVar13[0xc];
    lVar3 = plVar13[0xd];
    plVar10[10] = lVar17;
    plVar10[0xb] = lVar2;
    lVar17 = plVar13[0xe];
    lVar2 = plVar13[0xf];
    plVar10[0xc] = lVar16;
    plVar10[0xd] = lVar3;
    plVar10[0xe] = lVar17;
    plVar10[0xf] = lVar2;
    lVar18 = lVar18 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar18 != 0);
  lVar18 = plVar13[0x11];
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar18;
  if (0 < (int)uVar21) {
    uVar22 = (ulonglong)uVar21;
    do {
      FUN_180001220();
      uVar22 = uVar22 - 1;
    } while (uVar22 != 0);
  }
  alStack_15e0[1] = 0;
  alStack_15e0[2] = 0;
  alStack_15e0[3] = 0;
  iVar1 = *(int *)(param_4 + 0x84);
  uVar6 = *(uint *)(param_4 + 0x80);
  iVar7 = iVar1 / 2;
  iVar14 = 0;
  alStack_15e0[0x10] = 0;
  auVar24._4_4_ = iVar7;
  auVar24._0_4_ = iVar7;
  local_1558._4_4_ = iVar1 - iVar7;
  local_1558._0_4_ = uVar6;
  local_1558._8_8_ = (longlong)(iVar1 - iVar7) << 2;
  alStack_15e0[4] = 0;
  alStack_15e0[5] = 0;
  alStack_15e0[6] = 0;
  alStack_15e0[7] = 0;
  alStack_15e0[8] = 0;
  alStack_15e0[9] = 0;
  alStack_15e0[10] = 0;
  alStack_15e0[0xb] = 0;
  alStack_15e0[0xc] = 0;
  alStack_15e0[0xd] = 0;
  alStack_15e0[0xe] = 0;
  alStack_15e0[0xf] = 0;
  uVar11 = uVar6;
  if (((0 < (int)uVar6) && (7 < uVar6)) && (1 < DAT_1821c7690)) {
    lVar18 = 0;
    uVar11 = uVar6 & 0x80000007;
    if ((int)uVar11 < 0) {
      uVar11 = (uVar11 - 1 | 0xfffffff8) + 1;
    }
    auVar24._8_8_ = 0;
    auVar25 = pmovsxdq(auVar25,auVar24);
    lVar16 = auVar25._0_8_ * 4;
    lVar17 = auVar25._8_8_ * 4;
    plVar9 = (longlong *)(param_4 + 0x20);
    do {
      lVar2 = plVar9[-3];
      iVar14 = iVar14 + 8;
      lVar18 = lVar18 + 8;
      lVar3 = plVar9[-2];
      lVar20 = plVar9[-1];
      plVar8 = plVar9 + 8;
      plVar10 = (longlong *)((longlong)alStack_15f8 + (-0x40 - param_4) + (longlong)plVar8);
      *plVar10 = plVar9[-4] + lVar16;
      plVar10[1] = lVar2 + lVar17;
      lVar2 = *plVar9;
      lVar4 = plVar9[1];
      plVar10 = (longlong *)((longlong)alStack_15f8 + (-0x30 - param_4) + (longlong)plVar8);
      *plVar10 = lVar3 + lVar16;
      plVar10[1] = lVar20 + lVar17;
      lVar3 = plVar9[2];
      lVar20 = plVar9[3];
      plVar9 = (longlong *)((longlong)alStack_15f8 + (-0x20 - param_4) + (longlong)plVar8);
      *plVar9 = lVar2 + lVar16;
      plVar9[1] = lVar4 + lVar17;
      plVar9 = (longlong *)((longlong)alStack_15f8 + (-0x10 - param_4) + (longlong)plVar8);
      *plVar9 = lVar3 + lVar16;
      plVar9[1] = lVar20 + lVar17;
      plVar9 = plVar8;
    } while (lVar18 < (int)(uVar6 - uVar11));
    uVar11 = local_1558._0_4_;
  }
  lVar18 = (longlong)iVar14;
  if (lVar18 < (int)uVar6) {
    do {
      alStack_15e0[lVar18 + 1] = *(longlong *)(param_4 + lVar18 * 8) + (longlong)iVar7 * 4;
      lVar18 = lVar18 + 1;
    } while (lVar18 < (int)uVar6);
    uVar11 = local_1558._0_4_;
  }
  lVar18 = alStack_15e0[1];
  local_878 = 0;
  iVar7 = iVar1 / 2;
  FUN_181798f42(auStack_870,0,0x3f8);
  local_470 = (longlong)iVar7 << 2;
  local_478 = uVar21;
  local_474 = iVar7;
  if (0 < (int)uVar21) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(&local_878,&local_14a8,(ulonglong)uVar21 << 3);
  }
  local_1098 = 0;
  uVar22 = (ulonglong)(iVar1 / 2);
  FUN_181798f42(auStack_1090,0,0x3f8);
  local_c98 = uVar21;
  local_c94 = iVar1 / 2;
  local_c90 = uVar22 << 2;
  if (0 < (int)uVar21) {
    uVar22 = (ulonglong)uVar21;
    lVar16 = 0;
    do {
      *(longlong *)(auStack_1090 + lVar16 + -8) =
           *(longlong *)(auStack_14a0 + lVar16 + -8) + (longlong)(iVar1 / 2) * 4;
      uVar22 = uVar22 - 1;
      lVar16 = lVar16 + 8;
    } while (uVar22 != 0);
    uVar22 = (ulonglong)local_c94;
  }
  lVar16 = 8;
  local_1538[0] = alStack_15e0[1];
  local_1538[1] = alStack_15e0[2];
  local_1538[2] = alStack_15e0[3];
  local_1538[3] = alStack_15e0[4];
  local_1518 = alStack_15e0[5];
  uStack_1510 = alStack_15e0[6];
  local_1508 = alStack_15e0[7];
  uStack_1500 = alStack_15e0[8];
  local_14f8 = alStack_15e0[9];
  uStack_14f0 = alStack_15e0[10];
  local_14e8 = alStack_15e0[0xb];
  uStack_14e0 = alStack_15e0[0xc];
  local_14d8 = alStack_15e0[0xd];
  uStack_14d0 = alStack_15e0[0xe];
  local_14c8 = alStack_15e0[0xf];
  uStack_14c0 = alStack_15e0[0x10];
  local_14b8 = local_1558._0_8_;
  lStack_14b0 = local_1558._8_8_;
  plVar9 = local_c88;
  plVar8 = &local_878;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar17 = plVar13[1];
    lVar2 = plVar13[2];
    lVar3 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar17;
    lVar17 = plVar13[4];
    lVar20 = plVar13[5];
    plVar10[2] = lVar2;
    plVar10[3] = lVar3;
    lVar2 = plVar13[6];
    lVar3 = plVar13[7];
    plVar10[4] = lVar17;
    plVar10[5] = lVar20;
    lVar17 = plVar13[8];
    lVar20 = plVar13[9];
    plVar10[6] = lVar2;
    plVar10[7] = lVar3;
    lVar2 = plVar13[10];
    lVar3 = plVar13[0xb];
    plVar10[8] = lVar17;
    plVar10[9] = lVar20;
    lVar17 = plVar13[0xc];
    lVar20 = plVar13[0xd];
    plVar10[10] = lVar2;
    plVar10[0xb] = lVar3;
    lVar2 = plVar13[0xe];
    lVar3 = plVar13[0xf];
    plVar10[0xc] = lVar17;
    plVar10[0xd] = lVar20;
    plVar10[0xe] = lVar2;
    plVar10[0xf] = lVar3;
    lVar16 = lVar16 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar16 != 0);
  lVar16 = plVar13[0x11];
  lVar17 = 8;
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar16;
  plVar9 = local_468;
  plVar8 = &local_1098;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar16 = plVar13[1];
    lVar2 = plVar13[2];
    lVar3 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar16;
    lVar16 = plVar13[4];
    lVar20 = plVar13[5];
    plVar10[2] = lVar2;
    plVar10[3] = lVar3;
    lVar2 = plVar13[6];
    lVar3 = plVar13[7];
    plVar10[4] = lVar16;
    plVar10[5] = lVar20;
    lVar16 = plVar13[8];
    lVar20 = plVar13[9];
    plVar10[6] = lVar2;
    plVar10[7] = lVar3;
    lVar2 = plVar13[10];
    lVar3 = plVar13[0xb];
    plVar10[8] = lVar16;
    plVar10[9] = lVar20;
    lVar16 = plVar13[0xc];
    lVar20 = plVar13[0xd];
    plVar10[10] = lVar2;
    plVar10[0xb] = lVar3;
    lVar2 = plVar13[0xe];
    lVar3 = plVar13[0xf];
    plVar10[0xc] = lVar16;
    plVar10[0xd] = lVar20;
    plVar10[0xe] = lVar2;
    plVar10[0xf] = lVar3;
    lVar17 = lVar17 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar17 != 0);
  lVar16 = plVar13[0x11];
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar16;
  if (local_c98 == uVar11) {
    if (0 < (int)local_c98) {
      lVar18 = 0;
      uVar23 = (ulonglong)local_c98;
      do {
        FUN_180001190(*(undefined8 *)((longlong)local_c88 + lVar18),
                      *(undefined8 *)((longlong)local_1538 + lVar18),
                      *(undefined8 *)((longlong)local_468 + lVar18),uVar22 & 0xffffffff);
        lVar18 = lVar18 + 8;
        uVar23 = uVar23 - 1;
      } while (uVar23 != 0);
    }
  }
  else if ((uVar11 == 1) && (0 < (int)local_c98)) {
    lVar16 = 0;
    uVar23 = (ulonglong)local_c98;
    do {
      FUN_180001190(*(undefined8 *)((longlong)local_c88 + lVar16),lVar18,
                    *(undefined8 *)((longlong)local_468 + lVar16),uVar22 & 0xffffffff);
      lVar16 = lVar16 + 8;
      uVar23 = uVar23 - 1;
    } while (uVar23 != 0);
  }
  alStack_15e0[1] = 0;
  alStack_15e0[0x10] = 0;
  local_1558._4_4_ = iVar1 / 2;
  uVar6 = *(uint *)(param_4 + 0x80);
  lVar18 = (longlong)(iVar1 / 2) << 2;
  local_1558._0_4_ = uVar6;
  alStack_15e0[2] = 0;
  alStack_15e0[3] = 0;
  alStack_15e0[4] = 0;
  alStack_15e0[5] = 0;
  alStack_15e0[6] = 0;
  alStack_15e0[7] = 0;
  alStack_15e0[8] = 0;
  alStack_15e0[9] = 0;
  alStack_15e0[10] = 0;
  alStack_15e0[0xb] = 0;
  alStack_15e0[0xc] = 0;
  alStack_15e0[0xd] = 0;
  alStack_15e0[0xe] = 0;
  alStack_15e0[0xf] = 0;
  local_1558._8_8_ = lVar18;
  if (0 < (longlong)(int)uVar6) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(alStack_15e0 + 1,param_4,(longlong)(int)uVar6 << 3);
  }
  local_878 = 0;
  FUN_181798f42(auStack_870,0,0x3f8);
  local_478 = uVar21;
  local_474 = iVar1 / 2;
  local_470 = (longlong)(iVar1 / 2) << 2;
  if (0 < (int)uVar21) {
    uVar22 = (ulonglong)uVar21;
    lVar18 = 0;
    do {
      *(longlong *)((longlong)local_c88 + lVar18 + 0x410) =
           *(longlong *)(auStack_14a0 + lVar18 + -8) + (longlong)(local_1548 - iVar1 / 2) * 4;
      uVar22 = uVar22 - 1;
      lVar18 = lVar18 + 8;
    } while (uVar22 != 0);
  }
  local_1098 = 0;
  iVar7 = iVar1 / 2;
  FUN_181798f42(auStack_1090,0,0x3f8);
  local_c98 = uVar21;
  local_c94 = iVar7;
  local_c90 = (longlong)iVar7 << 2;
  if (0 < (int)uVar21) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(&local_1098,&local_14a8,(ulonglong)uVar21 << 3);
  }
  lVar18 = 8;
  local_1538[0] = alStack_15e0[1];
  local_1538[1] = alStack_15e0[2];
  local_1538[2] = alStack_15e0[3];
  local_1538[3] = alStack_15e0[4];
  local_1518 = alStack_15e0[5];
  uStack_1510 = alStack_15e0[6];
  local_1508 = alStack_15e0[7];
  uStack_1500 = alStack_15e0[8];
  local_14f8 = alStack_15e0[9];
  uStack_14f0 = alStack_15e0[10];
  local_14e8 = alStack_15e0[0xb];
  uStack_14e0 = alStack_15e0[0xc];
  local_14d8 = alStack_15e0[0xd];
  uStack_14d0 = alStack_15e0[0xe];
  local_14c8 = alStack_15e0[0xf];
  uStack_14c0 = alStack_15e0[0x10];
  local_14b8 = local_1558._0_8_;
  lStack_14b0 = local_1558._8_8_;
  plVar9 = local_468;
  plVar8 = &local_878;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar16 = plVar13[1];
    lVar17 = plVar13[2];
    lVar2 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar16;
    lVar16 = plVar13[4];
    lVar3 = plVar13[5];
    plVar10[2] = lVar17;
    plVar10[3] = lVar2;
    lVar17 = plVar13[6];
    lVar2 = plVar13[7];
    plVar10[4] = lVar16;
    plVar10[5] = lVar3;
    lVar16 = plVar13[8];
    lVar3 = plVar13[9];
    plVar10[6] = lVar17;
    plVar10[7] = lVar2;
    lVar17 = plVar13[10];
    lVar2 = plVar13[0xb];
    plVar10[8] = lVar16;
    plVar10[9] = lVar3;
    lVar16 = plVar13[0xc];
    lVar3 = plVar13[0xd];
    plVar10[10] = lVar17;
    plVar10[0xb] = lVar2;
    lVar17 = plVar13[0xe];
    lVar2 = plVar13[0xf];
    plVar10[0xc] = lVar16;
    plVar10[0xd] = lVar3;
    plVar10[0xe] = lVar17;
    plVar10[0xf] = lVar2;
    lVar18 = lVar18 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar18 != 0);
  lVar18 = plVar13[0x11];
  lVar16 = 8;
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar18;
  plVar9 = local_c88;
  plVar8 = &local_1098;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar18 = plVar13[1];
    lVar17 = plVar13[2];
    lVar2 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar18;
    lVar18 = plVar13[4];
    lVar3 = plVar13[5];
    plVar10[2] = lVar17;
    plVar10[3] = lVar2;
    lVar17 = plVar13[6];
    lVar2 = plVar13[7];
    plVar10[4] = lVar18;
    plVar10[5] = lVar3;
    lVar18 = plVar13[8];
    lVar3 = plVar13[9];
    plVar10[6] = lVar17;
    plVar10[7] = lVar2;
    lVar17 = plVar13[10];
    lVar2 = plVar13[0xb];
    plVar10[8] = lVar18;
    plVar10[9] = lVar3;
    lVar18 = plVar13[0xc];
    lVar3 = plVar13[0xd];
    plVar10[10] = lVar17;
    plVar10[0xb] = lVar2;
    lVar17 = plVar13[0xe];
    lVar2 = plVar13[0xf];
    plVar10[0xc] = lVar18;
    plVar10[0xd] = lVar3;
    plVar10[0xe] = lVar17;
    plVar10[0xf] = lVar2;
    lVar16 = lVar16 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar16 != 0);
  lVar18 = plVar13[0x11];
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar18;
  if (uVar21 == uVar6) {
    if (0 < (int)uVar21) {
      lVar18 = 0;
      uVar22 = (ulonglong)uVar21;
      do {
        FUN_180001190(*(undefined8 *)((longlong)local_468 + lVar18),
                      *(undefined8 *)((longlong)local_1538 + lVar18),
                      *(undefined8 *)((longlong)local_c88 + lVar18),iVar7);
        lVar18 = lVar18 + 8;
        uVar22 = uVar22 - 1;
      } while (uVar22 != 0);
    }
  }
  else if ((uVar6 == 1) && (0 < (int)uVar21)) {
    lVar18 = 0;
    uVar22 = (ulonglong)uVar21;
    do {
      FUN_180001190(*(undefined8 *)((longlong)local_468 + lVar18),0,
                    *(undefined8 *)((longlong)local_c88 + lVar18),iVar7);
      lVar18 = lVar18 + 8;
      uVar22 = uVar22 - 1;
    } while (uVar22 != 0);
  }
  local_1098 = 0;
  FUN_181798f42(auStack_1090,0,0x3f8);
  local_c98 = uVar21;
  local_c94 = uVar5 - iVar1;
  local_c90 = (longlong)(int)(uVar5 - iVar1) << 2;
  if (0 < (int)uVar21) {
    uVar22 = (ulonglong)uVar21;
    lVar18 = 0;
    do {
      *(longlong *)(auStack_1090 + lVar18 + -8) =
           *(longlong *)(auStack_14a0 + lVar18 + -8) + (longlong)iVar1 * 4;
      uVar22 = uVar22 - 1;
      lVar18 = lVar18 + 8;
    } while (uVar22 != 0);
  }
  uVar5 = local_c94;
  uVar22 = 8;
  lVar18 = 8;
  plVar9 = local_c88;
  plVar8 = &local_1098;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar16 = plVar13[1];
    lVar17 = plVar13[2];
    lVar2 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar16;
    lVar16 = plVar13[4];
    lVar3 = plVar13[5];
    plVar10[2] = lVar17;
    plVar10[3] = lVar2;
    lVar17 = plVar13[6];
    lVar2 = plVar13[7];
    plVar10[4] = lVar16;
    plVar10[5] = lVar3;
    lVar16 = plVar13[8];
    lVar3 = plVar13[9];
    plVar10[6] = lVar17;
    plVar10[7] = lVar2;
    lVar17 = plVar13[10];
    lVar2 = plVar13[0xb];
    plVar10[8] = lVar16;
    plVar10[9] = lVar3;
    lVar16 = plVar13[0xc];
    lVar3 = plVar13[0xd];
    plVar10[10] = lVar17;
    plVar10[0xb] = lVar2;
    lVar17 = plVar13[0xe];
    lVar2 = plVar13[0xf];
    plVar10[0xc] = lVar16;
    plVar10[0xd] = lVar3;
    plVar10[0xe] = lVar17;
    plVar10[0xf] = lVar2;
    lVar18 = lVar18 + -1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (lVar18 != 0);
  lVar18 = plVar13[0x11];
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar18;
  if (0 < (int)local_c98) {
    plVar9 = local_c88;
    uVar22 = (ulonglong)local_c98;
    do {
      uVar23 = uVar22;
      FUN_1800010d0(*plVar9,uVar5);
      plVar9 = plVar9 + 1;
      uVar22 = uVar23 - 1;
    } while (uVar22 != 0);
    uVar22 = (ulonglong)((int)uVar23 + 7);
  }
  plVar9 = local_c88;
  plVar8 = &local_14a8;
  do {
    plVar13 = plVar8;
    plVar10 = plVar9;
    lVar18 = plVar13[1];
    lVar16 = plVar13[2];
    lVar17 = plVar13[3];
    *plVar10 = *plVar13;
    plVar10[1] = lVar18;
    lVar18 = plVar13[4];
    lVar2 = plVar13[5];
    plVar10[2] = lVar16;
    plVar10[3] = lVar17;
    lVar16 = plVar13[6];
    lVar17 = plVar13[7];
    plVar10[4] = lVar18;
    plVar10[5] = lVar2;
    lVar18 = plVar13[8];
    lVar2 = plVar13[9];
    plVar10[6] = lVar16;
    plVar10[7] = lVar17;
    lVar16 = plVar13[10];
    lVar17 = plVar13[0xb];
    plVar10[8] = lVar18;
    plVar10[9] = lVar2;
    lVar18 = plVar13[0xc];
    lVar2 = plVar13[0xd];
    plVar10[10] = lVar16;
    plVar10[0xb] = lVar17;
    lVar16 = plVar13[0xe];
    lVar17 = plVar13[0xf];
    plVar10[0xc] = lVar18;
    plVar10[0xd] = lVar2;
    plVar10[0xe] = lVar16;
    plVar10[0xf] = lVar17;
    uVar22 = uVar22 - 1;
    plVar9 = plVar10 + 0x10;
    plVar8 = plVar13 + 0x10;
  } while (uVar22 != 0);
  lVar18 = plVar13[0x11];
  plVar10[0x10] = plVar13[0x10];
  plVar10[0x11] = lVar18;
  local_1538[0] = *param_1;
  local_1538[1] = param_1[1];
  local_1518 = param_1[4];
  uStack_1510 = param_1[5];
  local_1538[2] = param_1[2];
  local_1538[3] = param_1[3];
  local_14f8 = param_1[8];
  uStack_14f0 = param_1[9];
  local_1508 = param_1[6];
  uStack_1500 = param_1[7];
  local_14d8 = param_1[0xc];
  uStack_14d0 = param_1[0xd];
  local_14e8 = param_1[10];
  uStack_14e0 = param_1[0xb];
  local_14b8 = param_1[0x10];
  lStack_14b0 = param_1[0x11];
  local_14c8 = param_1[0xe];
  uStack_14c0 = param_1[0xf];
  if (0 < (int)uVar21) {
    uVar22 = (ulonglong)uVar21;
    do {
      FUN_180001010(*(undefined8 *)((longlong)local_c88 + lVar15),
                    *(undefined8 *)((longlong)local_1538 + lVar15),*(undefined8 *)(*param_3 + 8),
                    *(undefined8 *)param_3[1]);
      lVar15 = lVar15 + 8;
      uVar22 = uVar22 - 1;
    } while (uVar22 != 0);
  }
  *(undefined4 *)(param_5 + 3) = local_15e4;
  return;
}

