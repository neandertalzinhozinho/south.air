// FUN_18086ae00 @ 0x18086ae00

void FUN_18086ae00(undefined8 param_1,longlong param_2)

{
  longlong *plVar1;
  longlong *plVar2;
  uint uVar3;
  longlong lVar4;
  longlong lVar5;
  longlong lVar6;
  longlong lVar7;
  int iVar8;
  uint uVar9;
  longlong *plVar10;
  int iVar11;
  longlong lVar12;
  undefined8 *puVar13;
  longlong lVar14;
  ulonglong uVar15;
  undefined1 auVar16 [16];
  longlong lVar17;
  undefined1 in_XMM2 [16];
  longlong lVar18;
  longlong local_2f8 [16];
  uint local_278;
  int iStack_274;
  longlong lStack_270;
  undefined8 local_268 [4];
  undefined8 local_248;
  undefined8 uStack_240;
  undefined8 local_238;
  undefined8 uStack_230;
  undefined8 local_228;
  undefined8 uStack_220;
  undefined8 local_218;
  undefined8 uStack_210;
  undefined8 local_208;
  undefined8 uStack_200;
  undefined8 local_1f8;
  undefined8 uStack_1f0;
  uint local_1e8;
  int iStack_1e4;
  undefined4 uStack_1e0;
  undefined4 uStack_1dc;
  longlong local_1d8 [17];
  longlong lStack_150;
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
  undefined8 local_d8;
  undefined8 uStack_d0;
  uint local_c8;
  int iStack_c4;
  undefined4 uStack_c0;
  undefined4 uStack_bc;
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
  undefined8 local_48;
  undefined8 uStack_40;
  uint local_38;
  int iStack_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  
  FUN_18086f480(param_1,&local_148,*(undefined4 *)(param_2 + 0x84));
  local_278 = *(uint *)(param_2 + 0x80);
  lVar12 = 0;
  local_2f8[0xf] = 0;
  lStack_270 = (longlong)iStack_c4 << 2;
  local_2f8[0] = 0;
  iStack_274 = iStack_c4;
  local_2f8[1] = 0;
  local_2f8[2] = 0;
  local_2f8[3] = 0;
  local_2f8[4] = 0;
  local_2f8[5] = 0;
  local_2f8[6] = 0;
  local_2f8[7] = 0;
  local_2f8[8] = 0;
  local_2f8[9] = 0;
  local_2f8[10] = 0;
  local_2f8[0xb] = 0;
  local_2f8[0xc] = 0;
  local_2f8[0xd] = 0;
  local_2f8[0xe] = 0;
  if (0 < (longlong)(int)local_278) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(local_2f8,param_2,(longlong)(int)local_278 << 3);
  }
  local_1d8[2] = 0;
  local_1d8[3] = 0;
  local_1d8[0] = 0;
  local_1d8[1] = 0;
  local_1d8[6] = 0;
  local_1d8[7] = 0;
  local_1d8[4] = 0;
  local_1d8[5] = 0;
  local_1d8[10] = 0;
  local_1d8[0xb] = 0;
  local_1d8[8] = 0;
  local_1d8[9] = 0;
  local_1d8[0xe] = 0;
  local_1d8[0xf] = 0;
  local_1d8[0xc] = 0;
  local_1d8[0xd] = 0;
  local_268[0] = local_148;
  local_268[1] = uStack_140;
  local_1d8[0x10] = CONCAT44(iStack_c4,local_278);
  lStack_150 = lStack_270;
  local_248 = local_128;
  uStack_240 = uStack_120;
  local_268[2] = local_138;
  local_268[3] = uStack_130;
  local_228 = local_108;
  uStack_220 = uStack_100;
  local_238 = local_118;
  uStack_230 = uStack_110;
  local_208 = local_e8;
  uStack_200 = uStack_e0;
  uVar15 = (ulonglong)local_c8;
  local_218 = local_f8;
  uStack_210 = uStack_f0;
  local_1f8 = local_d8;
  uStack_1f0 = uStack_d0;
  local_1e8 = local_c8;
  iStack_1e4 = iStack_c4;
  uStack_1e0 = uStack_c0;
  uStack_1dc = uStack_bc;
  if (local_c8 == local_278) {
    if (0 < (int)local_c8) {
      lVar14 = 0;
      do {
        FUN_1800010a0(*(undefined8 *)((longlong)local_1d8 + lVar14),
                      *(undefined8 *)((longlong)local_268 + lVar14),iStack_c4);
        lVar14 = lVar14 + 8;
        uVar15 = uVar15 - 1;
      } while (uVar15 != 0);
    }
  }
  else if ((local_278 == 1) && (0 < (int)local_c8)) {
    puVar13 = local_268;
    do {
      FUN_1800010a0(0,*puVar13,iStack_c4);
      puVar13 = puVar13 + 1;
      uVar15 = uVar15 - 1;
    } while (uVar15 != 0);
  }
  iVar8 = iStack_34;
  if (0 < iStack_34) {
    uVar3 = *(uint *)(param_2 + 0x80);
    local_2f8[0xf] = 0;
    iVar11 = 0;
    auVar16._4_4_ = iStack_c4;
    auVar16._0_4_ = iStack_c4;
    local_2f8[0] = 0;
    local_278 = uVar3;
    iStack_274 = iStack_34;
    lStack_270 = (longlong)iStack_34 << 2;
    local_2f8[1] = 0;
    local_2f8[2] = 0;
    local_2f8[3] = 0;
    local_2f8[4] = 0;
    local_2f8[5] = 0;
    local_2f8[6] = 0;
    local_2f8[7] = 0;
    local_2f8[8] = 0;
    local_2f8[9] = 0;
    local_2f8[10] = 0;
    local_2f8[0xb] = 0;
    local_2f8[0xc] = 0;
    local_2f8[0xd] = 0;
    local_2f8[0xe] = 0;
    if (((0 < (int)uVar3) && (7 < uVar3)) && (1 < DAT_1821c7690)) {
      lVar14 = 0;
      uVar9 = uVar3 & 0x80000007;
      if ((int)uVar9 < 0) {
        uVar9 = (uVar9 - 1 | 0xfffffff8) + 1;
      }
      auVar16._8_8_ = 0;
      auVar16 = pmovsxdq(in_XMM2,auVar16);
      lVar17 = auVar16._0_8_ * 4;
      lVar18 = auVar16._8_8_ * 4;
      plVar10 = local_2f8 + 2;
      do {
        plVar1 = (longlong *)((param_2 - (longlong)(local_2f8 + 2)) + (longlong)plVar10);
        lVar4 = plVar1[1];
        iVar11 = iVar11 + 8;
        lVar14 = lVar14 + 8;
        plVar2 = (longlong *)((param_2 - (longlong)(local_2f8 + 2)) + 0x10 + (longlong)plVar10);
        lVar5 = *plVar2;
        lVar6 = plVar2[1];
        plVar2 = plVar10 + 8;
        plVar10[-2] = *plVar1 + lVar17;
        plVar10[-1] = lVar4 + lVar18;
        plVar1 = (longlong *)((param_2 - (longlong)(local_2f8 + 2)) + -0x20 + (longlong)plVar2);
        lVar4 = *plVar1;
        lVar7 = plVar1[1];
        *plVar10 = lVar5 + lVar17;
        plVar10[1] = lVar6 + lVar18;
        plVar1 = (longlong *)((param_2 - (longlong)(local_2f8 + 2)) + -0x10 + (longlong)plVar2);
        lVar5 = *plVar1;
        lVar6 = plVar1[1];
        plVar10[2] = lVar4 + lVar17;
        plVar10[3] = lVar7 + lVar18;
        plVar10[4] = lVar5 + lVar17;
        plVar10[5] = lVar6 + lVar18;
        plVar10 = plVar2;
      } while (lVar14 < (int)(uVar3 - uVar9));
    }
    lVar14 = (longlong)iVar11;
    if (lVar14 < (int)uVar3) {
      do {
        local_2f8[lVar14] = *(longlong *)(param_2 + lVar14 * 8) + (longlong)iStack_c4 * 4;
        lVar14 = lVar14 + 1;
      } while (lVar14 < (int)uVar3);
    }
    lVar14 = local_2f8[0];
    local_1d8[2] = local_2f8[2];
    local_1d8[3] = local_2f8[3];
    local_1d8[0] = local_2f8[0];
    local_1d8[1] = local_2f8[1];
    local_1d8[6] = local_2f8[6];
    local_1d8[7] = local_2f8[7];
    local_1d8[4] = local_2f8[4];
    local_1d8[5] = local_2f8[5];
    local_1d8[10] = local_2f8[10];
    local_1d8[0xb] = local_2f8[0xb];
    local_1d8[8] = local_2f8[8];
    local_1d8[9] = local_2f8[9];
    local_1d8[0xe] = local_2f8[0xe];
    local_1d8[0xf] = local_2f8[0xf];
    local_1d8[0xc] = local_2f8[0xc];
    local_1d8[0xd] = local_2f8[0xd];
    local_268[0] = local_b8;
    local_268[1] = uStack_b0;
    local_1d8[0x10] = CONCAT44(iStack_274,local_278);
    lStack_150 = lStack_270;
    local_248 = local_98;
    uStack_240 = uStack_90;
    local_268[2] = local_a8;
    local_268[3] = uStack_a0;
    local_228 = local_78;
    uStack_220 = uStack_70;
    local_238 = local_88;
    uStack_230 = uStack_80;
    local_208 = local_58;
    uStack_200 = uStack_50;
    local_218 = local_68;
    uStack_210 = uStack_60;
    local_1f8 = local_48;
    uStack_1f0 = uStack_40;
    local_1e8 = local_38;
    iStack_1e4 = iStack_34;
    uStack_1e0 = uStack_30;
    uStack_1dc = uStack_2c;
    if (local_38 == local_278) {
      if (0 < (int)local_38) {
        uVar15 = (ulonglong)local_38;
        do {
          FUN_1800010a0(*(undefined8 *)((longlong)local_1d8 + lVar12),
                        *(undefined8 *)((longlong)local_268 + lVar12),iVar8);
          lVar12 = lVar12 + 8;
          uVar15 = uVar15 - 1;
        } while (uVar15 != 0);
      }
    }
    else if ((local_278 == 1) && (0 < (int)local_38)) {
      puVar13 = local_268;
      uVar15 = (ulonglong)local_38;
      do {
        FUN_1800010a0(lVar14,*puVar13,iVar8);
        puVar13 = puVar13 + 1;
        uVar15 = uVar15 - 1;
      } while (uVar15 != 0);
    }
  }
  return;
}

