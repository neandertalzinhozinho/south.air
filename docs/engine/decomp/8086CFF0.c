// FUN_18086cff0 @ 0x18086cff0

void FUN_18086cff0(longlong param_1,undefined8 param_2)

{
  longlong *plVar1;
  longlong *plVar2;
  uint uVar3;
  int iVar4;
  longlong lVar5;
  longlong lVar6;
  longlong lVar7;
  longlong lVar8;
  uint uVar9;
  longlong *plVar10;
  int iVar11;
  longlong lVar12;
  ulonglong uVar13;
  longlong lVar14;
  ulonglong uVar15;
  undefined1 auVar16 [16];
  longlong lVar17;
  undefined1 auVar18 [16];
  longlong lVar19;
  longlong local_308 [16];
  uint local_288;
  uint uStack_284;
  longlong lStack_280;
  longlong local_278 [17];
  longlong lStack_1f0;
  undefined8 local_1e8 [4];
  undefined8 local_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  undefined8 uStack_1b0;
  undefined8 local_1a8;
  undefined8 uStack_1a0;
  undefined8 local_198;
  undefined8 uStack_190;
  undefined8 local_188;
  undefined8 uStack_180;
  undefined8 local_178;
  undefined8 uStack_170;
  undefined1 local_168 [16];
  undefined8 local_158;
  undefined8 uStack_150;
  undefined8 local_148;
  undefined8 uStack_140;
  undefined8 local_138;
  undefined8 uStack_130;
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
  undefined1 local_d8 [16];
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  uint local_48;
  uint uStack_44;
  
  FUN_18086f480(param_2,&local_158,*(undefined4 *)(param_1 + 0x84));
  iVar4 = local_d8._4_4_;
  lVar12 = 0;
  local_288 = *(uint *)(param_1 + 0x80);
  local_1e8[0] = local_158;
  local_1e8[1] = uStack_150;
  local_1c8 = local_138;
  uStack_1c0 = uStack_130;
  local_1a8 = local_118;
  uStack_1a0 = uStack_110;
  local_188 = local_f8;
  uStack_180 = uStack_f0;
  local_1e8[2] = local_148;
  local_1e8[3] = uStack_140;
  local_308[1] = 0;
  local_308[2] = 0;
  local_308[0xf] = 0;
  local_308[3] = 0;
  local_308[4] = 0;
  local_308[5] = 0;
  local_308[6] = 0;
  local_308[0] = 0;
  local_308[7] = 0;
  local_308[8] = 0;
  local_308[9] = 0;
  local_308[10] = 0;
  local_308[0xb] = 0;
  local_308[0xc] = 0;
  local_308[0xd] = 0;
  local_308[0xe] = 0;
  local_1b8 = local_128;
  uStack_1b0 = uStack_120;
  local_198 = local_108;
  uStack_190 = uStack_100;
  local_178 = local_e8;
  uStack_170 = uStack_e0;
  local_168 = local_d8;
  uStack_284 = iVar4;
  lStack_280 = (longlong)iVar4 << 2;
  if (0 < (longlong)(int)local_288) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(local_308,param_1,(longlong)(int)local_288 << 3);
  }
  local_278[0] = 0;
  local_278[1] = 0;
  local_278[2] = 0;
  local_278[3] = 0;
  local_278[4] = 0;
  local_278[5] = 0;
  local_278[6] = 0;
  local_278[7] = 0;
  local_278[8] = 0;
  local_278[9] = 0;
  local_278[0xc] = 0;
  local_278[0xd] = 0;
  local_278[10] = 0;
  local_278[0xb] = 0;
  local_278[0x10] = CONCAT44(iVar4,local_288);
  lStack_1f0 = (longlong)iVar4 << 2;
  local_278[0xe] = 0;
  local_278[0xf] = 0;
  if (local_288 == local_d8._0_4_) {
    if (0 < (int)local_288) {
      lVar14 = 0;
      uVar15 = (ulonglong)local_288;
      do {
        FUN_1800013a0(*(undefined8 *)((longlong)local_1e8 + lVar14),
                      *(undefined8 *)((longlong)local_278 + lVar14),iVar4);
        lVar14 = lVar14 + 8;
        uVar15 = uVar15 - 1;
      } while (uVar15 != 0);
    }
  }
  else if ((local_d8._0_4_ == 1) && (0 < (int)local_288)) {
    plVar10 = local_278;
    uVar15 = (ulonglong)local_288;
    do {
      FUN_1800013a0(local_158,*plVar10,iVar4);
      plVar10 = plVar10 + 1;
      uVar15 = uVar15 - 1;
    } while (uVar15 != 0);
  }
  uVar15 = (ulonglong)(int)uStack_44;
  if (0 < (int)uStack_44) {
    iVar11 = 0;
    uVar3 = *(uint *)(param_1 + 0x80);
    local_1e8[0] = local_c8;
    local_1e8[1] = uStack_c0;
    local_1c8 = local_a8;
    uStack_1c0 = uStack_a0;
    local_1e8[2] = local_b8;
    local_1e8[3] = uStack_b0;
    local_1a8 = local_88;
    uStack_1a0 = uStack_80;
    local_1b8 = local_98;
    uStack_1b0 = uStack_90;
    local_308[0xf] = 0;
    local_188 = local_68;
    uStack_180 = uStack_60;
    local_198 = local_78;
    uStack_190 = uStack_70;
    auVar18._0_8_ = CONCAT44(iVar4,iVar4);
    auVar18._8_4_ = iVar4;
    auVar18._12_4_ = iVar4;
    local_178 = local_58;
    uStack_170 = uStack_50;
    local_308[0] = 0;
    local_288 = uVar3;
    uStack_284 = uStack_44;
    lStack_280 = uVar15 << 2;
    local_308[1] = 0;
    local_308[2] = 0;
    local_308[3] = 0;
    local_308[4] = 0;
    local_308[5] = 0;
    local_308[6] = 0;
    local_308[7] = 0;
    local_308[8] = 0;
    local_308[9] = 0;
    local_308[10] = 0;
    local_308[0xb] = 0;
    local_308[0xc] = 0;
    local_308[0xd] = 0;
    local_308[0xe] = 0;
    if (((0 < (int)uVar3) && (7 < uVar3)) && (1 < DAT_1821c7690)) {
      lVar14 = 0;
      uVar9 = uVar3 & 0x80000007;
      if ((int)uVar9 < 0) {
        uVar9 = (uVar9 - 1 | 0xfffffff8) + 1;
      }
      auVar16._8_8_ = 0;
      auVar16._0_8_ = auVar18._0_8_;
      auVar18 = pmovsxdq(auVar18,auVar16);
      lVar17 = auVar18._0_8_ * 4;
      lVar19 = auVar18._8_8_ * 4;
      plVar10 = local_308 + 2;
      do {
        plVar1 = (longlong *)((param_1 - (longlong)(local_308 + 2)) + (longlong)plVar10);
        lVar5 = plVar1[1];
        iVar11 = iVar11 + 8;
        lVar14 = lVar14 + 8;
        plVar2 = (longlong *)((param_1 - (longlong)(local_308 + 2)) + 0x10 + (longlong)plVar10);
        lVar6 = *plVar2;
        lVar7 = plVar2[1];
        plVar2 = plVar10 + 8;
        plVar10[-2] = *plVar1 + lVar17;
        plVar10[-1] = lVar5 + lVar19;
        plVar1 = (longlong *)((param_1 - (longlong)(local_308 + 2)) + -0x20 + (longlong)plVar2);
        lVar5 = *plVar1;
        lVar8 = plVar1[1];
        *plVar10 = lVar6 + lVar17;
        plVar10[1] = lVar7 + lVar19;
        plVar1 = (longlong *)((param_1 - (longlong)(local_308 + 2)) + -0x10 + (longlong)plVar2);
        lVar6 = *plVar1;
        lVar7 = plVar1[1];
        plVar10[2] = lVar5 + lVar17;
        plVar10[3] = lVar8 + lVar19;
        plVar10[4] = lVar6 + lVar17;
        plVar10[5] = lVar7 + lVar19;
        plVar10 = plVar2;
      } while (lVar14 < (int)(uVar3 - uVar9));
      uVar15 = (ulonglong)uStack_284;
    }
    lVar14 = (longlong)iVar11;
    if (lVar14 < (int)uVar3) {
      do {
        local_308[lVar14] = *(longlong *)(param_1 + lVar14 * 8) + (longlong)iVar4 * 4;
        lVar14 = lVar14 + 1;
      } while (lVar14 < (int)uVar3);
      uVar15 = (ulonglong)uStack_284;
    }
    local_278[0] = local_308[0];
    local_278[1] = local_308[1];
    local_278[2] = local_308[2];
    local_278[3] = local_308[3];
    local_278[4] = local_308[4];
    local_278[5] = local_308[5];
    local_278[6] = local_308[6];
    local_278[7] = local_308[7];
    local_278[8] = local_308[8];
    local_278[9] = local_308[9];
    local_278[10] = local_308[10];
    local_278[0xb] = local_308[0xb];
    local_278[0xc] = local_308[0xc];
    local_278[0xd] = local_308[0xd];
    local_278[0x10] = CONCAT44(uStack_284,local_288);
    lStack_1f0 = lStack_280;
    local_278[0xe] = local_308[0xe];
    local_278[0xf] = local_308[0xf];
    if (local_288 == local_48) {
      if (0 < (int)local_288) {
        uVar13 = (ulonglong)local_288;
        do {
          FUN_1800013a0(*(undefined8 *)((longlong)local_1e8 + lVar12),
                        *(undefined8 *)((longlong)local_278 + lVar12),uVar15 & 0xffffffff);
          lVar12 = lVar12 + 8;
          uVar13 = uVar13 - 1;
        } while (uVar13 != 0);
      }
    }
    else if ((local_48 == 1) && (0 < (int)local_288)) {
      plVar10 = local_278;
      uVar13 = (ulonglong)local_288;
      do {
        FUN_1800013a0(local_c8,*plVar10,uVar15 & 0xffffffff);
        plVar10 = plVar10 + 1;
        uVar13 = uVar13 - 1;
      } while (uVar13 != 0);
    }
  }
  return;
}

