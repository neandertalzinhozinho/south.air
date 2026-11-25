// FUN_180899940 @ 0x180899940

void FUN_180899940(longlong param_1,longlong param_2,longlong param_3,longlong param_4,
                  undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  longlong lVar1;
  longlong lVar2;
  longlong *plVar3;
  longlong *plVar4;
  int iVar5;
  longlong lVar6;
  longlong lVar7;
  longlong lVar8;
  longlong lVar9;
  int iVar10;
  uint uVar11;
  int iVar12;
  longlong *plVar13;
  int iVar14;
  uint uVar15;
  longlong lVar16;
  longlong lVar17;
  ulonglong uVar18;
  int iVar19;
  undefined1 auVar20 [16];
  undefined1 auVar21 [16];
  undefined1 auVar22 [16];
  undefined1 in_XMM2 [16];
  longlong local_238 [16];
  undefined8 uStack_1b8;
  longlong lStack_1b0;
  undefined4 local_1a8;
  int local_1a0;
  uint local_19c;
  uint local_198;
  int local_194;
  int local_190;
  longlong local_188;
  ulonglong local_180;
  undefined4 local_178;
  undefined4 uStack_174;
  longlong lStack_170;
  undefined8 local_168;
  undefined4 uStack_160;
  undefined4 uStack_15c;
  longlong local_158 [16];
  undefined8 local_d8;
  longlong lStack_d0;
  undefined8 local_b8;
  int iStack_b0;
  int iStack_ac;
  undefined8 local_a8;
  int iStack_a0;
  int iStack_9c;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  longlong lStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  
  local_1a0 = *(int *)(param_2 + 0x84);
  iVar19 = 0;
  local_190 = local_1a0;
  if (0 < local_1a0) {
    uVar18 = (ulonglong)*(int *)(param_3 + 0x80);
    lVar1 = param_1 + 0x120;
    lVar2 = param_1 + 0x90;
    local_19c = *(uint *)(param_2 + 0x80);
    local_198 = *(uint *)(param_2 + 0x80);
    iVar14 = (int)param_5;
    local_194 = -iVar14;
    local_180 = uVar18;
    local_188 = (longlong)*(int *)(param_4 + 0x80);
    do {
      lVar17 = local_188;
      iVar12 = iVar14;
      if (local_1a0 < iVar14) {
        iVar12 = local_1a0;
      }
      auVar22._4_4_ = iVar19;
      auVar22._0_4_ = iVar19;
      local_238[0xf] = 0;
      lVar16 = 0;
      auVar21._4_4_ = iVar19;
      auVar21._0_4_ = iVar19;
      auVar20._4_4_ = iVar19;
      auVar20._0_4_ = iVar19;
      local_238[0] = 0;
      uStack_1b8._0_4_ = *(uint *)(param_3 + 0x80);
      uStack_1b8._4_4_ = iVar12;
      lStack_1b0 = (longlong)iVar12 << 2;
      local_238[1] = 0;
      local_238[2] = 0;
      local_238[3] = 0;
      local_238[4] = 0;
      local_238[5] = 0;
      local_238[6] = 0;
      local_238[7] = 0;
      local_238[8] = 0;
      local_238[9] = 0;
      local_238[10] = 0;
      local_238[0xb] = 0;
      local_238[0xc] = 0;
      local_238[0xd] = 0;
      local_238[0xe] = 0;
      uVar15 = (uint)uVar18;
      if (((0 < (int)uVar15) && (7 < uVar15)) && (1 < DAT_1821c7690)) {
        uVar11 = uVar15 & 0x80000007;
        if ((int)uVar11 < 0) {
          uVar11 = (uVar11 - 1 | 0xfffffff8) + 1;
        }
        auVar20._8_8_ = 0;
        auVar20 = pmovsxdq(in_XMM2,auVar20);
        in_XMM2._0_8_ = auVar20._0_8_ * 4;
        in_XMM2._8_8_ = auVar20._8_8_ * 4;
        plVar13 = local_238 + 2;
        do {
          plVar3 = (longlong *)((param_3 - (longlong)(local_238 + 2)) + (longlong)plVar13);
          lVar6 = plVar3[1];
          lVar16 = lVar16 + 8;
          plVar4 = (longlong *)((param_3 - (longlong)(local_238 + 2)) + 0x10 + (longlong)plVar13);
          lVar7 = *plVar4;
          lVar8 = plVar4[1];
          plVar4 = plVar13 + 8;
          plVar13[-2] = *plVar3 + in_XMM2._0_8_;
          plVar13[-1] = lVar6 + in_XMM2._8_8_;
          plVar3 = (longlong *)((param_3 - (longlong)(local_238 + 2)) + -0x20 + (longlong)plVar4);
          lVar6 = *plVar3;
          lVar9 = plVar3[1];
          *plVar13 = lVar7 + in_XMM2._0_8_;
          plVar13[1] = lVar8 + in_XMM2._8_8_;
          plVar3 = (longlong *)((param_3 - (longlong)(local_238 + 2)) + -0x10 + (longlong)plVar4);
          lVar7 = *plVar3;
          lVar8 = plVar3[1];
          plVar13[2] = lVar6 + in_XMM2._0_8_;
          plVar13[3] = lVar9 + in_XMM2._8_8_;
          plVar13[4] = lVar7 + in_XMM2._0_8_;
          plVar13[5] = lVar8 + in_XMM2._8_8_;
          plVar13 = plVar4;
        } while (lVar16 < (int)(uVar15 - uVar11));
      }
      uVar18 = local_180;
      if (lVar16 < (longlong)local_180) {
        do {
          local_238[lVar16] = *(longlong *)(param_3 + lVar16 * 8) + (longlong)iVar19 * 4;
          lVar16 = lVar16 + 1;
        } while (lVar16 < (longlong)uVar18);
      }
      iVar10 = uStack_1b8._4_4_;
      local_158[0] = local_238[0];
      local_158[1] = local_238[1];
      local_158[2] = local_238[2];
      local_158[3] = local_238[3];
      local_158[4] = local_238[4];
      local_158[5] = local_238[5];
      local_158[6] = local_238[6];
      local_158[7] = local_238[7];
      local_158[8] = local_238[8];
      local_158[9] = local_238[9];
      local_158[10] = local_238[10];
      local_158[0xb] = local_238[0xb];
      local_158[0xc] = local_238[0xc];
      local_158[0xd] = local_238[0xd];
      local_158[0xe] = local_238[0xe];
      local_158[0xf] = local_238[0xf];
      local_d8._0_4_ = (uint)uStack_1b8;
      local_d8._4_4_ = uStack_1b8._4_4_;
      lStack_d0 = lStack_1b0;
      if (0 < (int)(uint)uStack_1b8) {
        iStack_b0 = uStack_1b8._4_4_;
        iStack_ac = uStack_1b8._4_4_ * 4;
        lVar17 = 0;
        uVar18 = (ulonglong)(uint)uStack_1b8;
        do {
          local_b8 = *(undefined8 *)((longlong)local_158 + lVar17);
          iVar5 = *(int *)(param_1 + 0x11c);
          lStack_1b0 = 0;
          local_1a8 = *(undefined4 *)(param_1 + 0x110);
          local_238[0] = CONCAT44(local_238[0]._4_4_,iVar5);
          local_238[2] = 0;
          local_238[3] = 0;
          local_238[4] = 0;
          local_238[5] = 0;
          local_238[6] = 0;
          local_238[7] = 0;
          local_238[8] = 0;
          local_238[9] = 0;
          local_238[10] = 0;
          local_238[0xb] = 0;
          local_238[0xc] = 0;
          local_238[0xd] = 0;
          local_238[0xe] = 0;
          local_238[0xf] = 0;
          uStack_1b8._0_4_ = 0;
          uStack_1b8._4_4_ = 0;
          local_238[1] = lVar2;
          if (0 < iVar5) {
                    /* WARNING: Subroutine does not return */
            FUN_181798f36(local_238 + 2,lVar2,(longlong)iVar5 << 3);
          }
          uStack_90 = CONCAT44(iStack_ac,iStack_b0);
          local_168 = *(undefined8 *)((longlong)local_238 + lVar17 + 0x10);
          uStack_70 = CONCAT44(uStack_15c,local_1a8);
          local_178 = 1;
          local_88 = CONCAT44(uStack_174,1);
          lStack_170 = lVar2;
          uStack_160 = local_1a8;
          local_98 = local_b8;
          lStack_80 = lVar2;
          local_78 = local_168;
          FUN_1808b3da0(&local_88);
          lVar17 = lVar17 + 8;
          uVar18 = uVar18 - 1;
        } while (uVar18 != 0);
        lVar17 = local_188;
      }
      local_158[1] = lVar2;
      lStack_d0 = 0;
      local_158[3] = 0;
      local_158[4] = 0;
      local_158[5] = 0;
      local_158[6] = 0;
      local_158[7] = 0;
      local_158[8] = 0;
      local_158[9] = 0;
      local_158[10] = 0;
      local_158[0xb] = 0;
      local_158[0xc] = 0;
      local_158[0xd] = 0;
      local_158[0xe] = 0;
      local_158[0xf] = 0;
      local_d8 = 0;
      if (0 < (longlong)*(int *)(param_1 + 0x11c)) {
                    /* WARNING: Subroutine does not return */
        FUN_181798f36(local_158 + 2,lVar2,(longlong)*(int *)(param_1 + 0x11c) << 3);
      }
      local_238[0] = 0;
      *(uint *)(param_1 + 0x110) =
           *(int *)(param_1 + 0x110) + iVar10 & *(int *)(param_1 + 0x118) - 1U;
      uVar15 = *(uint *)(param_4 + 0x80);
      lVar16 = 0;
      local_238[0xf] = 0;
      lStack_1b0 = (longlong)iVar12 << 2;
      uStack_1b8._0_4_ = uVar15;
      uStack_1b8._4_4_ = iVar12;
      local_238[1] = 0;
      local_238[2] = 0;
      local_238[3] = 0;
      local_238[4] = 0;
      local_238[5] = 0;
      local_238[6] = 0;
      local_238[7] = 0;
      local_238[8] = 0;
      local_238[9] = 0;
      local_238[10] = 0;
      local_238[0xb] = 0;
      local_238[0xc] = 0;
      local_238[0xd] = 0;
      local_238[0xe] = 0;
      if (((0 < (int)uVar15) && (7 < uVar15)) && (1 < DAT_1821c7690)) {
        uVar11 = uVar15 & 0x80000007;
        if ((int)uVar11 < 0) {
          uVar11 = (uVar11 - 1 | 0xfffffff8) + 1;
        }
        auVar21._8_8_ = 0;
        auVar20 = pmovsxdq(in_XMM2,auVar21);
        in_XMM2._0_8_ = auVar20._0_8_ * 4;
        in_XMM2._8_8_ = auVar20._8_8_ * 4;
        plVar13 = local_238 + 2;
        do {
          plVar3 = (longlong *)((param_4 - (longlong)(local_238 + 2)) + (longlong)plVar13);
          lVar6 = plVar3[1];
          lVar16 = lVar16 + 8;
          plVar4 = (longlong *)((param_4 - (longlong)(local_238 + 2)) + 0x10 + (longlong)plVar13);
          lVar7 = *plVar4;
          lVar8 = plVar4[1];
          plVar4 = plVar13 + 8;
          plVar13[-2] = *plVar3 + in_XMM2._0_8_;
          plVar13[-1] = lVar6 + in_XMM2._8_8_;
          plVar3 = (longlong *)((param_4 - (longlong)(local_238 + 2)) + -0x20 + (longlong)plVar4);
          lVar6 = *plVar3;
          lVar9 = plVar3[1];
          *plVar13 = lVar7 + in_XMM2._0_8_;
          plVar13[1] = lVar8 + in_XMM2._8_8_;
          plVar3 = (longlong *)((param_4 - (longlong)(local_238 + 2)) + -0x10 + (longlong)plVar4);
          lVar7 = *plVar3;
          lVar8 = plVar3[1];
          plVar13[2] = lVar6 + in_XMM2._0_8_;
          plVar13[3] = lVar9 + in_XMM2._8_8_;
          plVar13[4] = lVar7 + in_XMM2._0_8_;
          plVar13[5] = lVar8 + in_XMM2._8_8_;
          plVar13 = plVar4;
        } while (lVar16 < (int)(uVar15 - uVar11));
      }
      if (lVar16 < lVar17) {
        do {
          local_238[lVar16] = *(longlong *)(param_4 + lVar16 * 8) + (longlong)iVar19 * 4;
          lVar16 = lVar16 + 1;
        } while (lVar16 < lVar17);
      }
      iVar10 = uStack_1b8._4_4_;
      local_158[0] = local_238[0];
      local_158[1] = local_238[1];
      local_158[2] = local_238[2];
      local_158[3] = local_238[3];
      local_158[4] = local_238[4];
      local_158[5] = local_238[5];
      local_158[6] = local_238[6];
      local_158[7] = local_238[7];
      local_158[8] = local_238[8];
      local_158[9] = local_238[9];
      local_158[10] = local_238[10];
      local_158[0xb] = local_238[0xb];
      local_158[0xc] = local_238[0xc];
      local_158[0xd] = local_238[0xd];
      local_158[0xe] = local_238[0xe];
      local_158[0xf] = local_238[0xf];
      local_d8._0_4_ = (uint)uStack_1b8;
      local_d8._4_4_ = uStack_1b8._4_4_;
      lStack_d0 = lStack_1b0;
      if (0 < (int)(uint)uStack_1b8) {
        iStack_a0 = uStack_1b8._4_4_;
        iStack_9c = uStack_1b8._4_4_ * 4;
        lVar17 = 0;
        uVar18 = (ulonglong)(uint)uStack_1b8;
        do {
          local_a8 = *(undefined8 *)((longlong)local_158 + lVar17);
          iVar5 = *(int *)(param_1 + 0x1ac);
          lStack_1b0 = 0;
          local_1a8 = *(undefined4 *)(param_1 + 0x1a0);
          local_238[0] = CONCAT44(local_238[0]._4_4_,iVar5);
          local_238[2] = 0;
          local_238[3] = 0;
          local_238[4] = 0;
          local_238[5] = 0;
          local_238[6] = 0;
          local_238[7] = 0;
          local_238[8] = 0;
          local_238[9] = 0;
          local_238[10] = 0;
          local_238[0xb] = 0;
          local_238[0xc] = 0;
          local_238[0xd] = 0;
          local_238[0xe] = 0;
          local_238[0xf] = 0;
          uStack_1b8._0_4_ = 0;
          uStack_1b8._4_4_ = 0;
          local_238[1] = lVar1;
          if (0 < iVar5) {
                    /* WARNING: Subroutine does not return */
            FUN_181798f36(local_238 + 2,lVar1,(longlong)iVar5 << 3);
          }
          uStack_90 = CONCAT44(iStack_9c,iStack_a0);
          local_168 = *(undefined8 *)((longlong)local_238 + lVar17 + 0x10);
          uStack_70 = CONCAT44(uStack_15c,local_1a8);
          local_178 = 1;
          local_88 = CONCAT44(uStack_174,1);
          lStack_170 = lVar1;
          uStack_160 = local_1a8;
          local_98 = local_a8;
          lStack_80 = lVar1;
          local_78 = local_168;
          FUN_1808b3da0(&local_88);
          lVar17 = lVar17 + 8;
          uVar18 = uVar18 - 1;
        } while (uVar18 != 0);
      }
      lStack_d0 = 0;
      local_158[3] = 0;
      local_158[4] = 0;
      local_158[5] = 0;
      local_158[6] = 0;
      local_158[7] = 0;
      local_158[8] = 0;
      local_158[9] = 0;
      local_158[10] = 0;
      local_158[0xb] = 0;
      local_158[0xc] = 0;
      local_158[0xd] = 0;
      local_158[0xe] = 0;
      local_158[0xf] = 0;
      local_d8 = 0;
      local_158[1] = lVar1;
      if (0 < (longlong)*(int *)(param_1 + 0x1ac)) {
                    /* WARNING: Subroutine does not return */
        FUN_181798f36(local_158 + 2,lVar1,(longlong)*(int *)(param_1 + 0x1ac) << 3);
      }
      *(uint *)(param_1 + 0x1a0) =
           *(int *)(param_1 + 0x1a0) + iVar10 & *(int *)(param_1 + 0x1a8) - 1U;
      FUN_1808acc40(param_1,param_5,param_6,param_7);
      lVar16 = (longlong)(int)local_198;
      local_238[0] = 0;
      local_238[0xf] = 0;
      lStack_1b0 = (longlong)iVar12 << 2;
      lVar17 = 0;
      uStack_1b8 = CONCAT44(iVar12,local_19c);
      local_238[1] = 0;
      local_238[2] = 0;
      local_238[3] = 0;
      local_238[4] = 0;
      local_238[5] = 0;
      local_238[6] = 0;
      local_238[7] = 0;
      local_238[8] = 0;
      local_238[9] = 0;
      local_238[10] = 0;
      local_238[0xb] = 0;
      local_238[0xc] = 0;
      local_238[0xd] = 0;
      local_238[0xe] = 0;
      if (((0 < (int)local_198) && (7 < local_198)) && (1 < DAT_1821c7690)) {
        uVar15 = local_198 & 0x80000007;
        if ((int)uVar15 < 0) {
          uVar15 = (uVar15 - 1 | 0xfffffff8) + 1;
        }
        iVar12 = local_198 - uVar15;
        auVar22._8_8_ = 0;
        auVar20 = pmovsxdq(in_XMM2,auVar22);
        in_XMM2._0_8_ = auVar20._0_8_ * 4;
        in_XMM2._8_8_ = auVar20._8_8_ * 4;
        plVar13 = local_238 + 2;
        do {
          plVar3 = (longlong *)((param_2 - (longlong)(local_238 + 2)) + (longlong)plVar13);
          lVar6 = plVar3[1];
          lVar17 = lVar17 + 8;
          plVar4 = (longlong *)((param_2 - (longlong)(local_238 + 2)) + 0x10 + (longlong)plVar13);
          lVar7 = *plVar4;
          lVar8 = plVar4[1];
          plVar4 = plVar13 + 8;
          plVar13[-2] = *plVar3 + in_XMM2._0_8_;
          plVar13[-1] = lVar6 + in_XMM2._8_8_;
          plVar3 = (longlong *)((param_2 - (longlong)(local_238 + 2)) + -0x20 + (longlong)plVar4);
          lVar6 = *plVar3;
          lVar9 = plVar3[1];
          *plVar13 = lVar7 + in_XMM2._0_8_;
          plVar13[1] = lVar8 + in_XMM2._8_8_;
          plVar3 = (longlong *)((param_2 - (longlong)(local_238 + 2)) + -0x10 + (longlong)plVar4);
          lVar7 = *plVar3;
          lVar8 = plVar3[1];
          plVar13[2] = lVar6 + in_XMM2._0_8_;
          plVar13[3] = lVar9 + in_XMM2._8_8_;
          plVar13[4] = lVar7 + in_XMM2._0_8_;
          plVar13[5] = lVar8 + in_XMM2._8_8_;
          plVar13 = plVar4;
        } while (lVar17 < iVar12);
      }
      if (lVar17 < lVar16) {
        do {
          local_238[lVar17] = *(longlong *)(param_2 + lVar17 * 8) + (longlong)iVar19 * 4;
          lVar17 = lVar17 + 1;
        } while (lVar17 < lVar16);
      }
      local_158[0] = local_238[0];
      local_158[1] = local_238[1];
      local_158[2] = local_238[2];
      local_158[3] = local_238[3];
      local_158[4] = local_238[4];
      local_158[5] = local_238[5];
      local_158[6] = local_238[6];
      local_158[7] = local_238[7];
      local_158[8] = local_238[8];
      local_158[9] = local_238[9];
      local_158[10] = local_238[10];
      local_158[0xb] = local_238[0xb];
      local_158[0xc] = local_238[0xc];
      local_158[0xd] = local_238[0xd];
      local_158[0xe] = local_238[0xe];
      local_158[0xf] = local_238[0xf];
      local_d8 = uStack_1b8;
      lStack_d0 = lStack_1b0;
      FUN_1808ae790(param_1,local_158,(undefined4)param_6);
      iVar19 = iVar19 + iVar14;
      local_1a0 = local_1a0 + local_194;
      uVar18 = (ulonglong)*(uint *)(param_3 + 0x80);
    } while (iVar19 < local_190);
  }
  return;
}

