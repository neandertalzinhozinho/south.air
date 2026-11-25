// FUN_1808ba1b0 @ 0x1808ba1b0

void FUN_1808ba1b0(longlong param_1,undefined8 param_2,longlong param_3)

{
  longlong *plVar1;
  longlong *plVar2;
  uint uVar3;
  longlong lVar4;
  longlong lVar5;
  longlong lVar6;
  longlong lVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined4 uVar12;
  undefined8 *puVar13;
  undefined8 *puVar14;
  undefined8 *puVar15;
  uint uVar16;
  longlong *plVar17;
  undefined8 *puVar18;
  int iVar19;
  longlong lVar20;
  longlong lVar21;
  ulonglong uVar22;
  int iVar23;
  longlong lVar24;
  undefined1 auVar25 [16];
  longlong lVar26;
  undefined1 in_XMM2 [16];
  longlong lVar27;
  longlong local_b28 [16];
  uint local_aa8;
  int iStack_aa4;
  longlong lStack_aa0;
  undefined8 local_a98 [4];
  undefined8 local_a78;
  undefined8 uStack_a70;
  undefined8 local_a68;
  undefined8 uStack_a60;
  undefined8 local_a58;
  undefined8 uStack_a50;
  undefined8 local_a48;
  undefined8 uStack_a40;
  undefined8 local_a38;
  undefined8 uStack_a30;
  undefined8 local_a28;
  undefined8 uStack_a20;
  undefined8 uStack_a10;
  longlong local_a08 [4];
  undefined8 local_9e8;
  undefined8 uStack_9e0;
  undefined8 local_9d8;
  undefined8 uStack_9d0;
  undefined8 local_9c8;
  undefined8 uStack_9c0;
  undefined8 local_9b8;
  undefined8 uStack_9b0;
  undefined8 local_9a8;
  undefined8 uStack_9a0;
  undefined8 local_998;
  undefined8 uStack_990;
  undefined8 local_988;
  longlong lStack_980;
  undefined8 local_978;
  undefined8 uStack_970;
  undefined8 local_968;
  undefined8 uStack_960;
  undefined8 local_958;
  undefined8 uStack_950;
  undefined8 local_948;
  undefined8 uStack_940;
  undefined8 local_938;
  undefined8 uStack_930;
  undefined8 local_928;
  undefined8 uStack_920;
  undefined8 local_918;
  undefined8 uStack_910;
  undefined8 local_908;
  undefined8 uStack_900;
  int iStack_8f4;
  undefined8 uStack_8f0;
  undefined8 local_8e8;
  undefined8 uStack_8e0;
  undefined8 local_8d8;
  undefined8 uStack_8d0;
  undefined8 local_8c8;
  undefined8 uStack_8c0;
  undefined8 local_8b8;
  undefined8 uStack_8b0;
  undefined8 local_8a8;
  undefined8 uStack_8a0;
  undefined8 local_898;
  undefined8 uStack_890;
  undefined8 local_888;
  undefined8 uStack_880;
  undefined8 local_878;
  undefined8 uStack_870;
  int iStack_864;
  undefined8 uStack_860;
  undefined8 local_858 [128];
  uint local_458;
  undefined4 local_454;
  undefined8 local_448 [130];
  
  FUN_18086f480(param_2,&local_978,*(undefined4 *)(param_1 + 0x404));
  iVar23 = iStack_8f4;
  uVar3 = *(uint *)(param_3 + 0x80);
  lVar21 = 0;
  local_b28[0xf] = 0;
  lStack_aa0 = (longlong)iStack_8f4 << 2;
  local_b28[0] = 0;
  iStack_aa4 = iStack_8f4;
  local_b28[1] = 0;
  local_b28[2] = 0;
  local_b28[3] = 0;
  local_b28[4] = 0;
  local_b28[5] = 0;
  local_b28[6] = 0;
  local_b28[7] = 0;
  local_b28[8] = 0;
  local_b28[9] = 0;
  local_b28[10] = 0;
  local_b28[0xb] = 0;
  local_b28[0xc] = 0;
  local_b28[0xd] = 0;
  local_b28[0xe] = 0;
  local_aa8 = uVar3;
  if (0 < (longlong)(int)uVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(local_b28,param_3,(longlong)(int)uVar3 << 3);
  }
  FUN_180867cc0(local_858,param_1,0,iStack_8f4);
  uVar12 = local_454;
  lVar24 = 8;
  lVar20 = 8;
  local_a08[0] = local_b28[0];
  local_a08[1] = local_b28[1];
  local_a08[2] = local_b28[2];
  local_a08[3] = local_b28[3];
  local_9e8 = local_b28[4];
  uStack_9e0 = local_b28[5];
  local_9d8 = local_b28[6];
  uStack_9d0 = local_b28[7];
  local_9c8 = local_b28[8];
  uStack_9c0 = local_b28[9];
  local_9b8 = local_b28[10];
  uStack_9b0 = local_b28[0xb];
  local_9a8 = local_b28[0xc];
  uStack_9a0 = local_b28[0xd];
  local_998 = local_b28[0xe];
  uStack_990 = local_b28[0xf];
  local_988 = CONCAT44(iStack_aa4,local_aa8);
  lStack_980 = lStack_aa0;
  local_a98[0] = local_978;
  local_a98[1] = uStack_970;
  local_a98[2] = local_968;
  local_a98[3] = uStack_960;
  local_a78 = local_958;
  uStack_a70 = uStack_950;
  local_a68 = local_948;
  uStack_a60 = uStack_940;
  local_a58 = local_938;
  uStack_a50 = uStack_930;
  local_a48 = local_928;
  uStack_a40 = uStack_920;
  local_a38 = local_918;
  uStack_a30 = uStack_910;
  local_a28 = local_908;
  uStack_a20 = uStack_900;
  uStack_a10 = uStack_8f0;
  puVar13 = local_448;
  puVar14 = local_858;
  do {
    puVar18 = puVar14;
    puVar15 = puVar13;
    uVar8 = puVar18[1];
    uVar9 = puVar18[2];
    uVar10 = puVar18[3];
    *puVar15 = *puVar18;
    puVar15[1] = uVar8;
    uVar8 = puVar18[4];
    uVar11 = puVar18[5];
    puVar15[2] = uVar9;
    puVar15[3] = uVar10;
    uVar9 = puVar18[6];
    uVar10 = puVar18[7];
    puVar15[4] = uVar8;
    puVar15[5] = uVar11;
    uVar8 = puVar18[8];
    uVar11 = puVar18[9];
    puVar15[6] = uVar9;
    puVar15[7] = uVar10;
    uVar9 = puVar18[10];
    uVar10 = puVar18[0xb];
    puVar15[8] = uVar8;
    puVar15[9] = uVar11;
    uVar8 = puVar18[0xc];
    uVar11 = puVar18[0xd];
    puVar15[10] = uVar9;
    puVar15[0xb] = uVar10;
    uVar9 = puVar18[0xe];
    uVar10 = puVar18[0xf];
    puVar15[0xc] = uVar8;
    puVar15[0xd] = uVar11;
    puVar15[0xe] = uVar9;
    puVar15[0xf] = uVar10;
    lVar20 = lVar20 + -1;
    puVar13 = puVar15 + 0x10;
    puVar14 = puVar18 + 0x10;
  } while (lVar20 != 0);
  uVar8 = puVar18[0x11];
  puVar15[0x10] = puVar18[0x10];
  puVar15[0x11] = uVar8;
  uVar22 = (ulonglong)local_458;
  if (local_458 == uVar3) {
    if (0 < (int)local_458) {
      lVar20 = 0;
      uVar22 = (ulonglong)local_458;
      do {
        FUN_180001190(*(undefined8 *)((longlong)local_a98 + lVar20),
                      *(undefined8 *)((longlong)local_a08 + lVar20),
                      *(undefined8 *)((longlong)local_448 + lVar20),uVar12);
        lVar20 = lVar20 + 8;
        uVar22 = uVar22 - 1;
      } while (uVar22 != 0);
    }
  }
  else if ((uVar3 == 1) && (0 < (int)local_458)) {
    lVar20 = 0;
    do {
      FUN_180001190(*(undefined8 *)((longlong)local_a98 + lVar20),0,
                    *(undefined8 *)((longlong)local_448 + lVar20),uVar12);
      lVar20 = lVar20 + 8;
      uVar22 = uVar22 - 1;
    } while (uVar22 != 0);
    iVar23 = iStack_8f4;
  }
  if (0 < iStack_864) {
    uVar3 = *(uint *)(param_3 + 0x80);
    local_b28[0xf] = 0;
    iVar19 = 0;
    auVar25._4_4_ = iVar23;
    auVar25._0_4_ = iVar23;
    local_b28[0] = 0;
    local_aa8 = uVar3;
    iStack_aa4 = iStack_864;
    lStack_aa0 = (longlong)iStack_864 << 2;
    local_b28[1] = 0;
    local_b28[2] = 0;
    local_b28[3] = 0;
    local_b28[4] = 0;
    local_b28[5] = 0;
    local_b28[6] = 0;
    local_b28[7] = 0;
    local_b28[8] = 0;
    local_b28[9] = 0;
    local_b28[10] = 0;
    local_b28[0xb] = 0;
    local_b28[0xc] = 0;
    local_b28[0xd] = 0;
    local_b28[0xe] = 0;
    if (((0 < (int)uVar3) && (7 < uVar3)) && (1 < DAT_1821c7690)) {
      lVar20 = 0;
      uVar16 = uVar3 & 0x80000007;
      if ((int)uVar16 < 0) {
        uVar16 = (uVar16 - 1 | 0xfffffff8) + 1;
      }
      auVar25._8_8_ = 0;
      auVar25 = pmovsxdq(in_XMM2,auVar25);
      lVar26 = auVar25._0_8_ * 4;
      lVar27 = auVar25._8_8_ * 4;
      plVar17 = local_b28 + 2;
      do {
        plVar1 = (longlong *)((param_3 - (longlong)(local_b28 + 2)) + (longlong)plVar17);
        lVar4 = plVar1[1];
        iVar19 = iVar19 + 8;
        lVar20 = lVar20 + 8;
        plVar2 = (longlong *)((param_3 - (longlong)(local_b28 + 2)) + 0x10 + (longlong)plVar17);
        lVar5 = *plVar2;
        lVar6 = plVar2[1];
        plVar2 = plVar17 + 8;
        plVar17[-2] = *plVar1 + lVar26;
        plVar17[-1] = lVar4 + lVar27;
        plVar1 = (longlong *)((param_3 - (longlong)(local_b28 + 2)) + -0x20 + (longlong)plVar2);
        lVar4 = *plVar1;
        lVar7 = plVar1[1];
        *plVar17 = lVar5 + lVar26;
        plVar17[1] = lVar6 + lVar27;
        plVar1 = (longlong *)((param_3 - (longlong)(local_b28 + 2)) + -0x10 + (longlong)plVar2);
        lVar5 = *plVar1;
        lVar6 = plVar1[1];
        plVar17[2] = lVar4 + lVar26;
        plVar17[3] = lVar7 + lVar27;
        plVar17[4] = lVar5 + lVar26;
        plVar17[5] = lVar6 + lVar27;
        plVar17 = plVar2;
      } while (lVar20 < (int)(uVar3 - uVar16));
    }
    lVar20 = (longlong)iVar19;
    if (lVar20 < (int)uVar3) {
      do {
        local_b28[lVar20] = *(longlong *)(param_3 + lVar20 * 8) + (longlong)iVar23 * 4;
        lVar20 = lVar20 + 1;
      } while (lVar20 < (int)uVar3);
    }
    uVar3 = local_aa8;
    lVar20 = local_b28[0];
    FUN_180867cc0(local_858,param_1,iVar23);
    local_a08[0] = local_b28[0];
    local_a08[1] = local_b28[1];
    local_a08[2] = local_b28[2];
    local_a08[3] = local_b28[3];
    local_9e8 = local_b28[4];
    uStack_9e0 = local_b28[5];
    local_9d8 = local_b28[6];
    uStack_9d0 = local_b28[7];
    local_9c8 = local_b28[8];
    uStack_9c0 = local_b28[9];
    local_9b8 = local_b28[10];
    uStack_9b0 = local_b28[0xb];
    local_9a8 = local_b28[0xc];
    uStack_9a0 = local_b28[0xd];
    local_998 = local_b28[0xe];
    uStack_990 = local_b28[0xf];
    local_988 = CONCAT44(iStack_aa4,local_aa8);
    lStack_980 = lStack_aa0;
    local_a98[0] = local_8e8;
    local_a98[1] = uStack_8e0;
    local_a98[2] = local_8d8;
    local_a98[3] = uStack_8d0;
    local_a78 = local_8c8;
    uStack_a70 = uStack_8c0;
    local_a68 = local_8b8;
    uStack_a60 = uStack_8b0;
    local_a58 = local_8a8;
    uStack_a50 = uStack_8a0;
    local_a48 = local_898;
    uStack_a40 = uStack_890;
    local_a38 = local_888;
    uStack_a30 = uStack_880;
    local_a28 = local_878;
    uStack_a20 = uStack_870;
    uStack_a10 = uStack_860;
    puVar13 = local_448;
    puVar14 = local_858;
    do {
      puVar18 = puVar14;
      puVar15 = puVar13;
      uVar8 = puVar18[1];
      uVar9 = puVar18[2];
      uVar10 = puVar18[3];
      *puVar15 = *puVar18;
      puVar15[1] = uVar8;
      uVar8 = puVar18[4];
      uVar11 = puVar18[5];
      puVar15[2] = uVar9;
      puVar15[3] = uVar10;
      uVar9 = puVar18[6];
      uVar10 = puVar18[7];
      puVar15[4] = uVar8;
      puVar15[5] = uVar11;
      uVar8 = puVar18[8];
      uVar11 = puVar18[9];
      puVar15[6] = uVar9;
      puVar15[7] = uVar10;
      uVar9 = puVar18[10];
      uVar10 = puVar18[0xb];
      puVar15[8] = uVar8;
      puVar15[9] = uVar11;
      uVar8 = puVar18[0xc];
      uVar11 = puVar18[0xd];
      puVar15[10] = uVar9;
      puVar15[0xb] = uVar10;
      uVar9 = puVar18[0xe];
      uVar10 = puVar18[0xf];
      puVar15[0xc] = uVar8;
      puVar15[0xd] = uVar11;
      puVar15[0xe] = uVar9;
      puVar15[0xf] = uVar10;
      lVar24 = lVar24 + -1;
      puVar13 = puVar15 + 0x10;
      puVar14 = puVar18 + 0x10;
    } while (lVar24 != 0);
    uVar8 = puVar18[0x11];
    puVar15[0x10] = puVar18[0x10];
    puVar15[0x11] = uVar8;
    uVar22 = (ulonglong)local_458;
    if (local_458 == uVar3) {
      if (0 < (int)local_458) {
        uVar22 = (ulonglong)local_458;
        do {
          FUN_180001190(*(undefined8 *)((longlong)local_a98 + lVar21),
                        *(undefined8 *)((longlong)local_a08 + lVar21),
                        *(undefined8 *)((longlong)local_448 + lVar21),local_454);
          lVar21 = lVar21 + 8;
          uVar22 = uVar22 - 1;
        } while (uVar22 != 0);
      }
    }
    else if ((uVar3 == 1) && (0 < (int)local_458)) {
      do {
        FUN_180001190(*(undefined8 *)((longlong)local_a98 + lVar21),lVar20,
                      *(undefined8 *)((longlong)local_448 + lVar21),local_454);
        lVar21 = lVar21 + 8;
        uVar22 = uVar22 - 1;
      } while (uVar22 != 0);
    }
  }
  return;
}

