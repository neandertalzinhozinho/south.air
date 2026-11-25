// FUN_180894170 @ 0x180894170

/* WARNING: Function: __chkstk replaced with injection: alloca_probe */

void FUN_180894170(longlong param_1,longlong *param_2,longlong *param_3,longlong *param_4,
                  undefined1 param_5,undefined1 param_6,undefined8 param_7)

{
  undefined4 uVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  int iVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined4 uVar10;
  longlong lVar11;
  longlong lVar12;
  longlong lVar13;
  longlong lVar14;
  int iVar15;
  longlong lVar16;
  longlong lVar17;
  longlong lVar18;
  longlong lVar19;
  longlong lVar20;
  longlong lVar21;
  longlong lVar22;
  longlong lVar23;
  longlong lVar24;
  longlong lVar25;
  longlong lVar26;
  int iVar27;
  uint uVar28;
  uint uVar29;
  longlong *plVar30;
  int iVar31;
  longlong *plVar32;
  longlong *plVar33;
  undefined1 *puVar34;
  longlong lVar35;
  longlong *plVar36;
  uint uVar37;
  uint uVar38;
  longlong lVar39;
  longlong lVar40;
  char cVar41;
  char cVar42;
  int iVar43;
  ulonglong uVar44;
  ulonglong uVar45;
  longlong lVar46;
  int local_res8;
  undefined1 local_1677 [7];
  undefined4 local_1670;
  undefined4 uStack_166c;
  longlong lStack_1668;
  undefined8 local_1660;
  undefined4 uStack_1658;
  undefined4 uStack_1654;
  longlong local_1648 [16];
  uint local_15c8;
  uint uStack_15c4;
  longlong lStack_15c0;
  undefined8 local_15b8;
  int iStack_15b0;
  int iStack_15ac;
  undefined8 local_15a8;
  int iStack_15a0;
  int iStack_159c;
  undefined8 local_1598;
  undefined8 uStack_1590;
  undefined4 local_1588;
  undefined4 uStack_1584;
  undefined8 uStack_1580;
  undefined4 local_1578;
  undefined4 uStack_1574;
  undefined4 uStack_1570;
  undefined4 uStack_156c;
  undefined8 local_1568;
  longlong local_1560;
  undefined1 *local_1558;
  undefined1 *local_1550;
  undefined1 *local_1548;
  longlong local_1538 [16];
  undefined8 local_14b8;
  longlong lStack_14b0;
  undefined4 local_14a8;
  uint local_1138;
  int local_1134;
  longlong local_1130;
  longlong local_1128 [16];
  uint local_10a8;
  uint uStack_10a4;
  longlong lStack_10a0;
  uint local_d28;
  longlong local_d18 [16];
  undefined8 local_c98;
  longlong lStack_c90;
  uint local_918;
  longlong local_908 [16];
  uint local_888;
  uint uStack_884;
  longlong lStack_880;
  longlong local_4f8 [4];
  undefined8 local_4d8;
  undefined8 uStack_4d0;
  undefined8 local_4c8;
  undefined8 uStack_4c0;
  undefined8 local_4b8;
  undefined8 uStack_4b0;
  undefined8 local_4a8;
  undefined8 uStack_4a0;
  undefined8 local_498;
  undefined8 uStack_490;
  undefined8 local_488;
  undefined8 uStack_480;
  undefined8 local_478;
  longlong lStack_470;
  uint local_f8;
  int local_f4;
  undefined8 uStack_48;
  
  uStack_48 = 0x180894193;
  *(int *)(param_1 + 0x2c30) = *(int *)(param_1 + 0x2c30) - *(int *)((longlong)param_2 + 0x404);
  local_1677[0] = *(int *)(*(longlong *)(param_1 + 0x2c38) + 0xb0) == 1;
  if (-1 < *(int *)(param_1 + 0x2c30)) goto LAB_1808954ac;
  iVar27 = *(int *)(param_1 + 0x2c30);
  do {
    iVar27 = iVar27 + *(int *)(param_1 + 0x60);
  } while (iVar27 < 0);
  *(int *)(param_1 + 0x2c30) = iVar27;
  cVar2 = *(char *)(param_1 + 0x2c40);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c40) = 0;
  UNLOCK();
  cVar3 = *(char *)(param_1 + 0x2c41);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c41) = 0;
  UNLOCK();
  cVar41 = *(char *)(param_1 + 0x2c45);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c45) = 0;
  UNLOCK();
  cVar4 = *(char *)(param_1 + 0x2c44);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c44) = 0;
  UNLOCK();
  cVar5 = *(char *)(param_1 + 0x2c43);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c43) = 0;
  UNLOCK();
  cVar6 = *(char *)(param_1 + 0x2c42);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c42) = 0;
  UNLOCK();
  cVar42 = cVar5;
  if (cVar3 != '\0') {
    FUN_180878070(param_1);
  }
  if (cVar41 != '\0') {
    FUN_180868f90(param_1);
    cVar42 = cVar5;
  }
  if (cVar2 == '\0') {
    if (((cVar6 != '\0') || (cVar3 != '\0')) || (cVar42 != '\0')) goto LAB_180894566;
    plVar32 = (longlong *)CONCAT44(param_7._4_4_,(int)param_7);
  }
  else {
    local_908[0] = 0;
    local_908[0xf] = 0;
    iVar27 = 0;
    local_888 = *(uint *)(param_1 + 0xa98);
    uStack_884 = *(int *)(param_1 + 0xaa0);
    lStack_880 = (longlong)*(int *)(param_1 + 0xaa0) << 2;
    local_908[1] = 0;
    local_908[2] = 0;
    local_908[3] = 0;
    local_908[4] = 0;
    local_908[5] = 0;
    local_908[6] = 0;
    local_908[7] = 0;
    local_908[8] = 0;
    local_908[9] = 0;
    local_908[10] = 0;
    local_908[0xb] = 0;
    local_908[0xc] = 0;
    local_908[0xd] = 0;
    local_908[0xe] = 0;
    if (0 < (int)*(uint *)(param_1 + 0xa98)) {
      plVar32 = local_908;
      do {
        iVar27 = iVar27 + 1;
        *plVar32 = *(longlong *)(((param_1 + 0xa18) - (longlong)local_908) + (longlong)plVar32);
        plVar32 = plVar32 + 1;
      } while (iVar27 < (int)local_888);
    }
    local_1128[0] = local_908[0];
    local_1128[1] = local_908[1];
    local_1128[2] = local_908[2];
    local_1128[3] = local_908[3];
    local_1128[4] = local_908[4];
    local_1128[5] = local_908[5];
    local_1128[6] = local_908[6];
    local_1128[7] = local_908[7];
    local_1128[8] = local_908[8];
    local_1128[9] = local_908[9];
    local_1128[10] = local_908[10];
    local_1128[0xb] = local_908[0xb];
    local_1128[0xc] = local_908[0xc];
    local_1128[0xd] = local_908[0xd];
    local_1128[0xe] = local_908[0xe];
    local_1128[0xf] = local_908[0xf];
    local_10a8 = local_888;
    uStack_10a4 = uStack_884;
    lStack_10a0 = lStack_880;
    if (0 < (int)local_888) {
      plVar32 = local_1128;
      uVar44 = (ulonglong)local_888;
      do {
        FUN_1800010d0(*plVar32);
        plVar32 = plVar32 + 1;
        uVar44 = uVar44 - 1;
      } while (uVar44 != 0);
    }
    uVar44 = (ulonglong)(int)*(uint *)(param_1 + 0xbc0);
    local_908[0] = 0;
    local_908[0xf] = 0;
    iVar27 = 0;
    local_888 = *(uint *)(param_1 + 3000);
    uStack_884 = *(uint *)(param_1 + 0xbc0);
    lStack_880 = uVar44 << 2;
    local_908[1] = 0;
    local_908[2] = 0;
    local_908[3] = 0;
    local_908[4] = 0;
    local_908[5] = 0;
    local_908[6] = 0;
    local_908[7] = 0;
    local_908[8] = 0;
    local_908[9] = 0;
    local_908[10] = 0;
    local_908[0xb] = 0;
    local_908[0xc] = 0;
    local_908[0xd] = 0;
    local_908[0xe] = 0;
    if (0 < (int)*(uint *)(param_1 + 3000)) {
      plVar32 = local_908;
      do {
        iVar27 = iVar27 + 1;
        *plVar32 = *(longlong *)(((param_1 + 0xb38) - (longlong)local_908) + (longlong)plVar32);
        plVar32 = plVar32 + 1;
      } while (iVar27 < (int)local_888);
      uVar44 = (ulonglong)uStack_884;
    }
    local_1128[0] = local_908[0];
    local_1128[1] = local_908[1];
    local_1128[2] = local_908[2];
    local_1128[3] = local_908[3];
    local_1128[4] = local_908[4];
    local_1128[5] = local_908[5];
    local_1128[6] = local_908[6];
    local_1128[7] = local_908[7];
    local_1128[8] = local_908[8];
    local_1128[9] = local_908[9];
    local_1128[10] = local_908[10];
    local_1128[0xb] = local_908[0xb];
    local_1128[0xc] = local_908[0xc];
    local_1128[0xd] = local_908[0xd];
    local_1128[0xe] = local_908[0xe];
    local_1128[0xf] = local_908[0xf];
    local_10a8 = local_888;
    uStack_10a4 = uStack_884;
    lStack_10a0 = lStack_880;
    if (0 < (int)local_888) {
      plVar32 = local_1128;
      uVar45 = (ulonglong)local_888;
      do {
        FUN_1800010d0(*plVar32,uVar44 & 0xffffffff);
        plVar32 = plVar32 + 1;
        uVar45 = uVar45 - 1;
      } while (uVar45 != 0);
    }
LAB_180894566:
    plVar32 = (longlong *)CONCAT44(param_7._4_4_,(int)param_7);
    FUN_18087bb60(param_1);
  }
  if (cVar4 != '\0') {
    FUN_18087e220(param_1);
  }
  if ((((cVar2 == '\0') && (cVar6 == '\0')) && (cVar4 == '\0')) ||
     ((FUN_18087b2a0(param_1), cVar6 == '\0' && (cVar4 == '\0')))) goto LAB_1808954ac;
  uVar1 = *(undefined4 *)(param_1 + 0x5c);
  iVar27 = 0;
  local_d18[0] = 0;
  local_d18[0xf] = 0;
  local_c98 = CONCAT44(*(int *)(param_1 + 2000),*(int *)(param_1 + 0x7c8));
  lStack_c90 = (longlong)*(int *)(param_1 + 2000) << 2;
  local_d18[1] = 0;
  local_d18[2] = 0;
  local_d18[3] = 0;
  local_d18[4] = 0;
  local_d18[5] = 0;
  local_d18[6] = 0;
  local_d18[7] = 0;
  local_d18[8] = 0;
  local_d18[9] = 0;
  local_d18[10] = 0;
  local_d18[0xb] = 0;
  local_d18[0xc] = 0;
  local_d18[0xd] = 0;
  local_d18[0xe] = 0;
  if (0 < *(int *)(param_1 + 0x7c8)) {
    plVar33 = local_d18;
    do {
      iVar27 = iVar27 + 1;
      *plVar33 = *(longlong *)(((param_1 + 0x748) - (longlong)local_d18) + (longlong)plVar33);
      plVar33 = plVar33 + 1;
    } while (iVar27 < (int)(uint)local_c98);
  }
  iVar27 = 0;
  uStack_10a4 = *(int *)(param_1 + 0xa10);
  local_1128[0] = 0;
  local_1128[0xf] = 0;
  local_10a8 = *(int *)(param_1 + 0xa08);
  lStack_10a0 = (longlong)*(int *)(param_1 + 0xa10) << 2;
  local_1128[1] = 0;
  local_1128[2] = 0;
  local_1128[3] = 0;
  local_1128[4] = 0;
  local_1128[5] = 0;
  local_1128[6] = 0;
  local_1128[7] = 0;
  local_1128[8] = 0;
  local_1128[9] = 0;
  local_1128[10] = 0;
  local_1128[0xb] = 0;
  local_1128[0xc] = 0;
  local_1128[0xd] = 0;
  local_1128[0xe] = 0;
  if (0 < *(int *)(param_1 + 0xa08)) {
    plVar33 = local_1128;
    do {
      iVar27 = iVar27 + 1;
      *plVar33 = *(longlong *)(((param_1 + 0x988) - (longlong)local_1128) + (longlong)plVar33);
      plVar33 = plVar33 + 1;
    } while (iVar27 < (int)local_10a8);
  }
  local_4f8[0] = local_d18[0];
  local_4f8[1] = local_d18[1];
  local_4f8[2] = local_d18[2];
  local_4f8[3] = local_d18[3];
  local_4d8 = local_d18[4];
  uStack_4d0 = local_d18[5];
  local_4c8 = local_d18[6];
  uStack_4c0 = local_d18[7];
  local_4b8 = local_d18[8];
  uStack_4b0 = local_d18[9];
  local_4a8 = local_d18[10];
  uStack_4a0 = local_d18[0xb];
  local_498 = local_d18[0xc];
  uStack_490 = local_d18[0xd];
  local_488 = local_d18[0xe];
  uStack_480 = local_d18[0xf];
  local_478 = local_c98;
  lStack_470 = lStack_c90;
  local_1538[0] = local_1128[0];
  local_1538[1] = local_1128[1];
  local_1538[2] = local_1128[2];
  local_1538[3] = local_1128[3];
  local_1538[4] = local_1128[4];
  local_1538[5] = local_1128[5];
  local_1538[6] = local_1128[6];
  local_1538[7] = local_1128[7];
  local_1538[8] = local_1128[8];
  local_1538[9] = local_1128[9];
  local_1538[10] = local_1128[10];
  local_1538[0xb] = local_1128[0xb];
  local_1538[0xc] = local_1128[0xc];
  local_1538[0xd] = local_1128[0xd];
  local_1538[0xe] = local_1128[0xe];
  local_1538[0xf] = local_1128[0xf];
  local_14b8 = CONCAT44(uStack_10a4,local_10a8);
  lStack_14b0 = lStack_10a0;
  FUN_18087f0c0(local_1538,local_4f8,*(undefined8 *)(param_1 + 0x10),
                *(undefined8 *)(param_1 + 0x2c38),uVar1,plVar32);
  local_14b8._0_4_ = *(uint *)(param_1 + 0xa08);
  lVar35 = plVar32[3];
  local_14b8._4_4_ = *(uint *)(param_1 + 0xa10);
  iVar27 = 0;
  if (0 < (int)(uint)local_14b8) {
    plVar33 = local_1538;
    do {
      iVar27 = iVar27 + 1;
      *plVar33 = *(longlong *)(((param_1 + 0x988) - (longlong)local_1538) + (longlong)plVar33);
      plVar33 = plVar33 + 1;
    } while (iVar27 < (int)(uint)local_14b8);
  }
  local_908[0] = 0;
  local_888 = (uint)local_14b8;
  local_908[0xf] = 0;
  lVar40 = 0;
  uStack_884 = local_14b8._4_4_;
  lStack_880 = (longlong)(int)local_14b8._4_4_ << 2;
  local_908[1] = 0;
  local_908[2] = 0;
  local_908[3] = 0;
  local_908[4] = 0;
  local_908[5] = 0;
  local_908[6] = 0;
  local_908[7] = 0;
  local_908[8] = 0;
  local_908[9] = 0;
  local_908[10] = 0;
  local_908[0xb] = 0;
  local_908[0xc] = 0;
  local_908[0xd] = 0;
  local_908[0xe] = 0;
  if (0 < (int)(uint)local_14b8) {
    uVar38 = *(uint *)(plVar32 + 3);
    do {
      uVar28 = local_14b8._4_4_ + uVar38;
      local_908[lVar40] = *plVar32 + (longlong)(int)uVar38 * 4;
      uVar38 = (uVar28 - (uVar28 & 0xf)) + 0x10;
      if ((uVar28 & 0xf) == 0) {
        uVar38 = uVar28;
      }
      lVar40 = lVar40 + 1;
      *(uint *)(plVar32 + 3) = uVar38;
    } while (lVar40 < (int)(uint)local_14b8);
  }
  uVar28 = uStack_884;
  uVar38 = local_888;
  uVar1 = DAT_182079f9c;
  iVar27 = 0;
  uStack_10a4 = *(int *)(param_1 + 0xa10);
  local_1128[0] = 0;
  local_1128[0xf] = 0;
  local_10a8 = *(int *)(param_1 + 0xa08);
  lStack_10a0 = (longlong)*(int *)(param_1 + 0xa10) << 2;
  local_1128[1] = 0;
  local_1128[2] = 0;
  local_1128[3] = 0;
  local_1128[4] = 0;
  local_1128[5] = 0;
  local_1128[6] = 0;
  local_1128[7] = 0;
  local_1128[8] = 0;
  local_1128[9] = 0;
  local_1128[10] = 0;
  local_1128[0xb] = 0;
  local_1128[0xc] = 0;
  local_1128[0xd] = 0;
  local_1128[0xe] = 0;
  if (0 < *(int *)(param_1 + 0xa08)) {
    plVar33 = local_1128;
    do {
      iVar27 = iVar27 + 1;
      *plVar33 = *(longlong *)(((param_1 + 0x988) - (longlong)local_1128) + (longlong)plVar33);
      plVar33 = plVar33 + 1;
    } while (iVar27 < (int)local_10a8);
  }
  lVar26 = lStack_880;
  lVar25 = local_908[0xf];
  lVar24 = local_908[0xe];
  lVar23 = local_908[0xd];
  lVar22 = local_908[0xc];
  lVar21 = local_908[0xb];
  lVar20 = local_908[10];
  lVar19 = local_908[9];
  lVar18 = local_908[8];
  lVar17 = local_908[7];
  lVar16 = local_908[6];
  lVar12 = local_908[5];
  lVar14 = local_908[4];
  lVar13 = local_908[3];
  lVar11 = local_908[2];
  lVar39 = local_908[1];
  lVar40 = local_908[0];
  uVar8 = CONCAT44(uStack_884,local_888);
  local_1538[0] = local_908[0];
  local_1538[1] = local_908[1];
  local_1538[2] = local_908[2];
  local_1538[3] = local_908[3];
  local_1538[4] = local_908[4];
  local_1538[5] = local_908[5];
  local_1538[6] = local_908[6];
  local_1538[7] = local_908[7];
  local_1538[8] = local_908[8];
  local_1538[9] = local_908[9];
  local_1538[10] = local_908[10];
  local_1538[0xb] = local_908[0xb];
  local_1538[0xc] = local_908[0xc];
  local_1538[0xd] = local_908[0xd];
  local_1538[0xe] = local_908[0xe];
  local_1538[0xf] = local_908[0xf];
  local_14b8 = uVar8;
  lStack_14b0 = lStack_880;
  local_4f8[0] = local_1128[0];
  local_4f8[1] = local_1128[1];
  local_4f8[2] = local_1128[2];
  local_4f8[3] = local_1128[3];
  local_4d8 = local_1128[4];
  uStack_4d0 = local_1128[5];
  local_4c8 = local_1128[6];
  uStack_4c0 = local_1128[7];
  local_4b8 = local_1128[8];
  uStack_4b0 = local_1128[9];
  local_4a8 = local_1128[10];
  uStack_4a0 = local_1128[0xb];
  local_498 = local_1128[0xc];
  uStack_490 = local_1128[0xd];
  local_488 = local_1128[0xe];
  uStack_480 = local_1128[0xf];
  local_478 = CONCAT44(uStack_10a4,local_10a8);
  lStack_470 = lStack_10a0;
  if (0 < (int)uVar38) {
    lVar46 = 0;
    uVar44 = (ulonglong)uVar38;
    do {
      FUN_180001250(*(undefined8 *)((longlong)local_4f8 + lVar46),
                    *(undefined8 *)((longlong)local_1538 + lVar46),uVar28,uVar1,0);
      lVar46 = lVar46 + 8;
      uVar44 = uVar44 - 1;
    } while (uVar44 != 0);
    plVar32 = (longlong *)CONCAT44(param_7._4_4_,(int)param_7);
  }
  local_1538[0] = lVar40;
  local_1538[1] = lVar39;
  local_1538[2] = lVar11;
  local_1538[3] = lVar13;
  local_1538[4] = lVar14;
  local_1538[5] = lVar12;
  local_1538[6] = lVar16;
  local_1538[7] = lVar17;
  local_1538[8] = lVar18;
  local_1538[9] = lVar19;
  local_1538[10] = lVar20;
  local_1538[0xb] = lVar21;
  local_1538[0xc] = lVar22;
  local_1538[0xd] = lVar23;
  local_1538[0xe] = lVar24;
  local_1538[0xf] = lVar25;
  local_14b8 = uVar8;
  lStack_14b0 = lVar26;
  if (0 < (int)uVar38) {
    plVar32 = local_1538;
    uVar44 = (ulonglong)uVar38;
    do {
      FUN_1801c8530(*plVar32,*plVar32);
      plVar32 = plVar32 + 1;
      uVar44 = uVar44 - 1;
    } while (uVar44 != 0);
    plVar32 = (longlong *)CONCAT44(param_7._4_4_,(int)param_7);
  }
  local_1648[0] = 0;
  local_1648[0xf] = 0;
  lVar46 = 0;
  lStack_15c0 = (longlong)(int)uVar28 << 2;
  local_1648[1] = 0;
  local_1648[2] = 0;
  local_1648[3] = 0;
  local_1648[4] = 0;
  local_1648[5] = 0;
  local_1648[6] = 0;
  local_1648[7] = 0;
  local_1648[8] = 0;
  local_1648[9] = 0;
  local_1648[10] = 0;
  local_1648[0xb] = 0;
  local_1648[0xc] = 0;
  local_1648[0xd] = 0;
  local_1648[0xe] = 0;
  local_15c8 = uVar38;
  uStack_15c4 = uVar28;
  if (0 < (int)uVar38) {
    uVar37 = *(uint *)(plVar32 + 3);
    do {
      uVar29 = uVar28 + uVar37;
      local_1648[lVar46] = *plVar32 + (longlong)(int)uVar37 * 4;
      uVar37 = (uVar29 - (uVar29 & 0xf)) + 0x10;
      if ((uVar29 & 0xf) == 0) {
        uVar37 = uVar29;
      }
      lVar46 = lVar46 + 1;
      *(uint *)(plVar32 + 3) = uVar37;
    } while (lVar46 < (int)uVar38);
  }
  local_1128[0] = local_1648[0];
  local_1128[1] = local_1648[1];
  local_1128[2] = local_1648[2];
  local_1128[3] = local_1648[3];
  local_1128[4] = local_1648[4];
  local_1128[5] = local_1648[5];
  local_1128[6] = local_1648[6];
  local_1128[7] = local_1648[7];
  local_1128[8] = local_1648[8];
  local_1128[9] = local_1648[9];
  local_1128[10] = local_1648[10];
  local_1128[0xb] = local_1648[0xb];
  local_1128[0xc] = local_1648[0xc];
  local_1128[0xd] = local_1648[0xd];
  local_1128[0xe] = local_1648[0xe];
  local_1128[0xf] = local_1648[0xf];
  local_10a8 = local_15c8;
  uStack_10a4 = uStack_15c4;
  lStack_10a0 = lStack_15c0;
  local_4f8[0] = lVar40;
  local_4f8[1] = lVar39;
  local_4f8[2] = lVar11;
  local_4f8[3] = lVar13;
  local_4d8 = lVar14;
  uStack_4d0 = lVar12;
  local_4c8 = lVar16;
  uStack_4c0 = lVar17;
  local_4b8 = lVar18;
  uStack_4b0 = lVar19;
  local_4a8 = lVar20;
  uStack_4a0 = lVar21;
  local_498 = lVar22;
  uStack_490 = lVar23;
  local_488 = lVar24;
  uStack_480 = lVar25;
  lStack_470 = lVar26;
  local_478 = uVar8;
  FUN_1808981e0(local_1128,local_4f8);
  local_d18[0] = local_1648[0];
  local_d18[1] = local_1648[1];
  local_d18[2] = local_1648[2];
  local_d18[3] = local_1648[3];
  local_d18[4] = local_1648[4];
  local_d18[5] = local_1648[5];
  local_d18[6] = local_1648[6];
  local_d18[7] = local_1648[7];
  local_d18[8] = local_1648[8];
  local_d18[9] = local_1648[9];
  local_d18[10] = local_1648[10];
  local_d18[0xb] = local_1648[0xb];
  local_d18[0xc] = local_1648[0xc];
  local_d18[0xd] = local_1648[0xd];
  local_d18[0xe] = local_1648[0xe];
  local_d18[0xf] = local_1648[0xf];
  local_c98 = CONCAT44(uStack_15c4,local_15c8);
  lStack_c90 = lStack_15c0;
  if (0 < (int)local_15c8) {
    plVar32 = local_d18;
    uVar44 = (ulonglong)local_15c8;
    do {
      FUN_1800012e0(uVar1,*plVar32);
      plVar32 = plVar32 + 1;
      uVar44 = uVar44 - 1;
    } while (uVar44 != 0);
    plVar32 = (longlong *)CONCAT44(param_7._4_4_,(int)param_7);
  }
  local_res8 = *(int *)(param_1 + 0x500);
  uVar28 = *(uint *)(param_1 + 0x4f8);
  iVar27 = 0;
  local_d18[0] = 0;
  local_d18[1] = 0;
  local_d18[2] = 0;
  local_d18[0xf] = 0;
  local_d18[3] = 0;
  local_d18[4] = 0;
  local_c98 = CONCAT44(local_res8,uVar28);
  local_d18[5] = 0;
  local_d18[6] = 0;
  lStack_c90 = (longlong)local_res8 << 2;
  local_d18[7] = 0;
  local_d18[8] = 0;
  local_d18[9] = 0;
  local_d18[10] = 0;
  local_d18[0xb] = 0;
  local_d18[0xc] = 0;
  local_d18[0xd] = 0;
  local_d18[0xe] = 0;
  if (*(char *)(param_1 + 0x58) == '\0') {
    if (0 < (int)uVar28) {
      plVar33 = local_d18;
      do {
        iVar27 = iVar27 + 1;
        *plVar33 = *(longlong *)(((param_1 + 0x478) - (longlong)local_d18) + (longlong)plVar33);
        plVar33 = plVar33 + 1;
      } while (iVar27 < (int)(uint)local_c98);
      local_res8 = local_c98._4_4_;
      uVar28 = (uint)local_c98;
    }
    lVar46 = local_908[0];
    local_1538[0] = lVar40;
    local_1538[1] = lVar39;
    local_1538[2] = lVar11;
    local_1538[3] = lVar13;
    local_1538[4] = lVar14;
    local_1538[5] = lVar12;
    local_1538[6] = lVar16;
    local_1538[7] = lVar17;
    local_1538[8] = lVar18;
    local_1538[9] = lVar19;
    local_1538[10] = lVar20;
    local_1538[0xb] = lVar21;
    local_1538[0xc] = lVar22;
    local_1538[0xd] = lVar23;
    local_1538[0xe] = lVar24;
    local_1538[0xf] = lVar25;
    local_14b8 = uVar8;
    lStack_14b0 = lVar26;
    local_1128[0] = local_d18[0];
    local_1128[1] = local_d18[1];
    local_1128[2] = local_d18[2];
    local_1128[3] = local_d18[3];
    local_1128[4] = local_d18[4];
    local_1128[5] = local_d18[5];
    local_1128[6] = local_d18[6];
    local_1128[7] = local_d18[7];
    local_1128[8] = local_d18[8];
    local_1128[9] = local_d18[9];
    local_1128[10] = local_d18[10];
    local_1128[0xb] = local_d18[0xb];
    local_1128[0xc] = local_d18[0xc];
    local_1128[0xd] = local_d18[0xd];
    local_1128[0xe] = local_d18[0xe];
    local_1128[0xf] = local_d18[0xf];
    local_10a8 = (uint)local_c98;
    uStack_10a4 = local_c98._4_4_;
    lStack_10a0 = lStack_c90;
    if (uVar28 == uVar38) {
      if (0 < (int)uVar28) {
        lVar40 = 0;
        uVar44 = (ulonglong)uVar28;
        do {
          FUN_180001340(*(undefined8 *)((longlong)local_1538 + lVar40),
                        *(undefined8 *)((longlong)local_1128 + lVar40),local_res8);
          lVar40 = lVar40 + 8;
          uVar44 = uVar44 - 1;
        } while (uVar44 != 0);
        goto LAB_18089540f;
      }
    }
    else if ((uVar38 == 1) && (0 < (int)uVar28)) {
      plVar32 = local_1128;
      uVar44 = (ulonglong)uVar28;
      do {
        FUN_180001340(lVar46,*plVar32,local_res8);
        plVar32 = plVar32 + 1;
        uVar44 = uVar44 - 1;
      } while (uVar44 != 0);
      goto LAB_18089540f;
    }
  }
  else {
    if (0 < (int)uVar28) {
      plVar33 = local_d18;
      do {
        iVar27 = iVar27 + 1;
        *plVar33 = *(longlong *)(((param_1 + 0x478) - (longlong)local_d18) + (longlong)plVar33);
        plVar33 = plVar33 + 1;
        uVar28 = (uint)local_c98;
      } while (iVar27 < (int)(uint)local_c98);
    }
    lVar46 = local_908[0];
    local_1538[0] = lVar40;
    local_1538[1] = lVar39;
    local_1538[2] = lVar11;
    local_1538[3] = lVar13;
    local_1538[4] = lVar14;
    local_1538[5] = lVar12;
    local_1538[6] = lVar16;
    local_1538[7] = lVar17;
    local_1538[8] = lVar18;
    local_1538[9] = lVar19;
    local_1538[10] = lVar20;
    local_1538[0xb] = lVar21;
    local_1538[0xc] = lVar22;
    local_1538[0xd] = lVar23;
    local_1538[0xe] = lVar24;
    local_1538[0xf] = lVar25;
    local_14b8 = uVar8;
    lStack_14b0 = lVar26;
    local_1128[0] = local_d18[0];
    local_1128[1] = local_d18[1];
    local_1128[2] = local_d18[2];
    local_1128[3] = local_d18[3];
    local_1128[4] = local_d18[4];
    local_1128[5] = local_d18[5];
    local_1128[6] = local_d18[6];
    local_1128[7] = local_d18[7];
    local_1128[8] = local_d18[8];
    local_1128[9] = local_d18[9];
    local_1128[10] = local_d18[10];
    local_1128[0xb] = local_d18[0xb];
    local_1128[0xc] = local_d18[0xc];
    local_1128[0xd] = local_d18[0xd];
    local_1128[0xe] = local_d18[0xe];
    local_1128[0xf] = local_d18[0xf];
    local_10a8 = (uint)local_c98;
    uStack_10a4 = local_c98._4_4_;
    lStack_10a0 = lStack_c90;
    if (uVar28 == uVar38) {
      if (0 < (int)uVar28) {
        lVar40 = 0;
        uVar44 = (ulonglong)uVar28;
        do {
          FUN_180001340(*(undefined8 *)((longlong)local_1538 + lVar40),
                        *(undefined8 *)((longlong)local_1128 + lVar40));
          lVar40 = lVar40 + 8;
          uVar44 = uVar44 - 1;
        } while (uVar44 != 0);
        goto LAB_18089504f;
      }
    }
    else if ((uVar38 == 1) && (0 < (int)uVar28)) {
      plVar32 = local_1128;
      uVar44 = (ulonglong)uVar28;
      do {
        FUN_180001340(lVar46,*plVar32);
        plVar32 = plVar32 + 1;
        uVar44 = uVar44 - 1;
      } while (uVar44 != 0);
LAB_18089504f:
      plVar32 = (longlong *)CONCAT44(param_7._4_4_,(int)param_7);
    }
    lVar40 = local_1648[0];
    uVar44 = (ulonglong)*(int *)(param_1 + 0x500);
    uVar38 = *(uint *)(param_1 + 0x4f8);
    local_d18[0] = 0;
    local_d18[0xf] = 0;
    iVar27 = 0;
    local_c98 = CONCAT44(*(int *)(param_1 + 0x500),uVar38);
    lStack_c90 = uVar44 << 2;
    local_d18[1] = 0;
    local_d18[2] = 0;
    local_d18[3] = 0;
    local_d18[4] = 0;
    local_d18[5] = 0;
    local_d18[6] = 0;
    local_d18[7] = 0;
    local_d18[8] = 0;
    local_d18[9] = 0;
    local_d18[10] = 0;
    local_d18[0xb] = 0;
    local_d18[0xc] = 0;
    local_d18[0xd] = 0;
    local_d18[0xe] = 0;
    if (0 < (int)uVar38) {
      plVar33 = local_d18;
      do {
        iVar27 = iVar27 + 1;
        *plVar33 = *(longlong *)(((param_1 + 0x478) - (longlong)local_d18) + (longlong)plVar33);
        plVar33 = plVar33 + 1;
      } while (iVar27 < (int)(uint)local_c98);
      uVar44 = local_c98 >> 0x20;
      uVar38 = (uint)local_c98;
    }
    local_1538[0] = local_1648[0];
    local_1538[1] = local_1648[1];
    local_1538[2] = local_1648[2];
    local_1538[3] = local_1648[3];
    local_1538[4] = local_1648[4];
    local_1538[5] = local_1648[5];
    local_1538[6] = local_1648[6];
    local_1538[7] = local_1648[7];
    local_1538[8] = local_1648[8];
    local_1538[9] = local_1648[9];
    local_1538[10] = local_1648[10];
    local_1538[0xb] = local_1648[0xb];
    local_1538[0xc] = local_1648[0xc];
    local_1538[0xd] = local_1648[0xd];
    local_1538[0xe] = local_1648[0xe];
    local_1538[0xf] = local_1648[0xf];
    local_14b8 = CONCAT44(uStack_15c4,local_15c8);
    lStack_14b0 = lStack_15c0;
    local_1128[2] = local_d18[2];
    local_1128[3] = local_d18[3];
    local_1128[0] = local_d18[0];
    local_1128[1] = local_d18[1];
    local_1128[6] = local_d18[6];
    local_1128[7] = local_d18[7];
    local_1128[4] = local_d18[4];
    local_1128[5] = local_d18[5];
    local_1128[10] = local_d18[10];
    local_1128[0xb] = local_d18[0xb];
    local_1128[8] = local_d18[8];
    local_1128[9] = local_d18[9];
    local_1128[0xe] = local_d18[0xe];
    local_1128[0xf] = local_d18[0xf];
    local_1128[0xc] = local_d18[0xc];
    local_1128[0xd] = local_d18[0xd];
    local_10a8 = (uint)local_c98;
    uStack_10a4 = local_c98._4_4_;
    lStack_10a0 = lStack_c90;
    if (uVar38 == local_15c8) {
      if (0 < (int)uVar38) {
        lVar40 = 0;
        uVar45 = (ulonglong)uVar38;
        do {
          FUN_180001370(*(undefined8 *)((longlong)local_1538 + lVar40),
                        *(undefined8 *)((longlong)local_1128 + lVar40),uVar44 & 0xffffffff);
          lVar40 = lVar40 + 8;
          uVar45 = uVar45 - 1;
        } while (uVar45 != 0);
        goto LAB_18089540f;
      }
    }
    else if ((local_15c8 == 1) && (0 < (int)uVar38)) {
      plVar32 = local_1128;
      uVar45 = (ulonglong)uVar38;
      do {
        FUN_180001370(lVar40,*plVar32,uVar44 & 0xffffffff);
        plVar32 = plVar32 + 1;
        uVar45 = uVar45 - 1;
      } while (uVar45 != 0);
LAB_18089540f:
      plVar32 = (longlong *)CONCAT44(param_7._4_4_,(int)param_7);
    }
  }
  FUN_18087f780(param_1);
  iVar27 = 0;
  *(undefined1 *)(param_1 + 0x2bc8) = 1;
  if (*(longlong *)(param_1 + 0x48) != 0) {
    puVar34 = (undefined1 *)(param_1 + 0x2bb8);
    do {
      iVar27 = iVar27 + 1;
      *puVar34 = 1;
      puVar34 = puVar34 + 1;
    } while ((ulonglong)(longlong)iVar27 < *(ulonglong *)(param_1 + 0x48));
  }
  *(int *)(plVar32 + 3) = (int)lVar35;
LAB_1808954ac:
  local_1568 = CONCAT44(param_7._4_4_,(int)param_7);
  lVar35 = 8;
  local_1558 = &param_6;
  local_1550 = local_1677;
  local_1548 = &param_5;
  plVar32 = local_d18;
  do {
    plVar30 = param_4;
    plVar33 = plVar32;
    lVar40 = plVar30[1];
    lVar39 = plVar30[2];
    lVar11 = plVar30[3];
    *plVar33 = *plVar30;
    plVar33[1] = lVar40;
    lVar40 = plVar30[4];
    lVar13 = plVar30[5];
    plVar33[2] = lVar39;
    plVar33[3] = lVar11;
    lVar39 = plVar30[6];
    lVar11 = plVar30[7];
    plVar33[4] = lVar40;
    plVar33[5] = lVar13;
    lVar40 = plVar30[8];
    lVar13 = plVar30[9];
    plVar33[6] = lVar39;
    plVar33[7] = lVar11;
    lVar39 = plVar30[10];
    lVar11 = plVar30[0xb];
    plVar33[8] = lVar40;
    plVar33[9] = lVar13;
    lVar40 = plVar30[0xc];
    lVar13 = plVar30[0xd];
    plVar33[10] = lVar39;
    plVar33[0xb] = lVar11;
    lVar39 = plVar30[0xe];
    lVar11 = plVar30[0xf];
    plVar33[0xc] = lVar40;
    plVar33[0xd] = lVar13;
    plVar33[0xe] = lVar39;
    plVar33[0xf] = lVar11;
    lVar35 = lVar35 + -1;
    plVar32 = plVar33 + 0x10;
    param_4 = plVar30 + 0x10;
  } while (lVar35 != 0);
  lVar35 = plVar30[0x11];
  lVar40 = 8;
  plVar33[0x10] = plVar30[0x10];
  plVar33[0x11] = lVar35;
  plVar32 = local_1128;
  do {
    plVar30 = param_3;
    plVar33 = plVar32;
    lVar35 = plVar30[1];
    lVar39 = plVar30[2];
    lVar11 = plVar30[3];
    *plVar33 = *plVar30;
    plVar33[1] = lVar35;
    lVar35 = plVar30[4];
    lVar13 = plVar30[5];
    plVar33[2] = lVar39;
    plVar33[3] = lVar11;
    lVar39 = plVar30[6];
    lVar11 = plVar30[7];
    plVar33[4] = lVar35;
    plVar33[5] = lVar13;
    lVar35 = plVar30[8];
    lVar13 = plVar30[9];
    plVar33[6] = lVar39;
    plVar33[7] = lVar11;
    lVar39 = plVar30[10];
    lVar11 = plVar30[0xb];
    plVar33[8] = lVar35;
    plVar33[9] = lVar13;
    lVar35 = plVar30[0xc];
    lVar13 = plVar30[0xd];
    plVar33[10] = lVar39;
    plVar33[0xb] = lVar11;
    lVar39 = plVar30[0xe];
    lVar11 = plVar30[0xf];
    plVar33[0xc] = lVar35;
    plVar33[0xd] = lVar13;
    plVar33[0xe] = lVar39;
    plVar33[0xf] = lVar11;
    lVar40 = lVar40 + -1;
    plVar32 = plVar33 + 0x10;
    param_3 = plVar30 + 0x10;
  } while (lVar40 != 0);
  lVar35 = plVar30[0x11];
  lVar40 = 8;
  plVar33[0x10] = plVar30[0x10];
  plVar33[0x11] = lVar35;
  plVar32 = local_4f8;
  do {
    plVar30 = param_2;
    plVar33 = plVar32;
    lVar35 = plVar30[1];
    lVar39 = plVar30[2];
    lVar11 = plVar30[3];
    *plVar33 = *plVar30;
    plVar33[1] = lVar35;
    lVar35 = plVar30[4];
    lVar13 = plVar30[5];
    plVar33[2] = lVar39;
    plVar33[3] = lVar11;
    lVar39 = plVar30[6];
    lVar11 = plVar30[7];
    plVar33[4] = lVar35;
    plVar33[5] = lVar13;
    lVar35 = plVar30[8];
    lVar13 = plVar30[9];
    plVar33[6] = lVar39;
    plVar33[7] = lVar11;
    lVar39 = plVar30[10];
    lVar11 = plVar30[0xb];
    plVar33[8] = lVar35;
    plVar33[9] = lVar13;
    lVar35 = plVar30[0xc];
    lVar13 = plVar30[0xd];
    plVar33[10] = lVar39;
    plVar33[0xb] = lVar11;
    lVar39 = plVar30[0xe];
    lVar11 = plVar30[0xf];
    plVar33[0xc] = lVar35;
    plVar33[0xd] = lVar13;
    plVar33[0xe] = lVar39;
    plVar33[0xf] = lVar11;
    lVar40 = lVar40 + -1;
    plVar32 = plVar33 + 0x10;
    param_2 = plVar30 + 0x10;
  } while (lVar40 != 0);
  uVar1 = *(undefined4 *)((longlong)plVar30 + 0x84);
  lVar35 = plVar30[0x11];
  uVar10 = *(undefined4 *)((longlong)plVar30 + 0x8c);
  iVar27 = 0;
  *(int *)(plVar33 + 0x10) = (int)plVar30[0x10];
  *(undefined4 *)((longlong)plVar33 + 0x84) = uVar1;
  *(int *)(plVar33 + 0x11) = (int)lVar35;
  *(undefined4 *)((longlong)plVar33 + 0x8c) = uVar10;
  uVar44 = *(ulonglong *)(param_1 + 0x28);
  uVar8 = *(undefined8 *)(param_1 + 0x60);
  if (0 < local_f4) {
    lVar35 = param_1 + 0x1498;
    iVar31 = (int)uVar8;
    lVar40 = param_1 + 0x1528;
    param_7._0_4_ = local_f4;
    local_1560 = param_1;
    do {
      uVar38 = local_d28;
      local_1538[0] = 0;
      iVar43 = iVar31;
      if ((int)param_7 < iVar31) {
        iVar43 = (int)param_7;
      }
      FUN_181798f42(local_1538 + 1,0,0x3f8);
      local_1138 = uVar38;
      local_1134 = iVar43;
      local_1130 = (longlong)iVar43 << 2;
      if (0 < (int)uVar38) {
        uVar45 = (ulonglong)uVar38;
        lVar39 = 0;
        do {
          *(longlong *)((longlong)local_1538 + lVar39) =
               *(longlong *)((longlong)local_1128 + lVar39) + (longlong)iVar27 * 4;
          uVar45 = uVar45 - 1;
          lVar39 = lVar39 + 8;
        } while (uVar45 != 0);
      }
      iVar15 = local_1134;
      lVar39 = 8;
      plVar32 = local_908;
      plVar33 = local_1538;
      do {
        plVar36 = plVar33;
        plVar30 = plVar32;
        lVar11 = plVar36[1];
        lVar13 = plVar36[2];
        lVar14 = plVar36[3];
        *plVar30 = *plVar36;
        plVar30[1] = lVar11;
        lVar11 = plVar36[4];
        lVar12 = plVar36[5];
        plVar30[2] = lVar13;
        plVar30[3] = lVar14;
        lVar13 = plVar36[6];
        lVar14 = plVar36[7];
        plVar30[4] = lVar11;
        plVar30[5] = lVar12;
        lVar11 = plVar36[8];
        lVar12 = plVar36[9];
        plVar30[6] = lVar13;
        plVar30[7] = lVar14;
        lVar13 = plVar36[10];
        lVar14 = plVar36[0xb];
        plVar30[8] = lVar11;
        plVar30[9] = lVar12;
        lVar11 = plVar36[0xc];
        lVar12 = plVar36[0xd];
        plVar30[10] = lVar13;
        plVar30[0xb] = lVar14;
        lVar13 = plVar36[0xe];
        lVar14 = plVar36[0xf];
        plVar30[0xc] = lVar11;
        plVar30[0xd] = lVar12;
        plVar30[0xe] = lVar13;
        plVar30[0xf] = lVar14;
        lVar39 = lVar39 + -1;
        plVar32 = plVar30 + 0x10;
        plVar33 = plVar36 + 0x10;
      } while (lVar39 != 0);
      lVar39 = plVar36[0x11];
      plVar30[0x10] = plVar36[0x10];
      plVar30[0x11] = lVar39;
      if (0 < (int)local_1138) {
        iStack_15ac = local_1134 * 4;
        lVar39 = 0;
        uVar45 = (ulonglong)local_1138;
        iStack_15b0 = local_1134;
        do {
          local_15b8 = *(undefined8 *)((longlong)local_908 + lVar39);
          iVar7 = *(int *)(param_1 + 0x1524);
          lStack_14b0 = 0;
          local_14a8 = *(undefined4 *)(param_1 + 0x1518);
          local_1538[0] = CONCAT44(local_1538[0]._4_4_,iVar7);
          local_1538[1] = lVar35;
          local_1538[2] = 0;
          local_1538[3] = 0;
          local_1538[4] = 0;
          local_1538[5] = 0;
          local_1538[6] = 0;
          local_1538[7] = 0;
          local_1538[8] = 0;
          local_1538[9] = 0;
          local_1538[10] = 0;
          local_1538[0xb] = 0;
          local_1538[0xc] = 0;
          local_1538[0xd] = 0;
          local_1538[0xe] = 0;
          local_1538[0xf] = 0;
          local_14b8 = 0;
          if (0 < iVar7) {
                    /* WARNING: Subroutine does not return */
            FUN_181798f36(local_1538 + 2,lVar35,(longlong)iVar7 << 3);
          }
          uStack_1590 = CONCAT44(iStack_15ac,iStack_15b0);
          uVar9 = *(undefined8 *)((longlong)local_1538 + lVar39 + 0x10);
          local_1660._0_4_ = (undefined4)uVar9;
          local_1660._4_4_ = (undefined4)((ulonglong)uVar9 >> 0x20);
          local_1670 = 1;
          local_1578 = (undefined4)local_1660;
          uStack_1574 = local_1660._4_4_;
          uStack_156c = uStack_1654;
          local_1588 = 1;
          uStack_1584 = uStack_166c;
          lStack_1668 = lVar35;
          local_1660 = uVar9;
          uStack_1658 = local_14a8;
          local_1598 = local_15b8;
          uStack_1570 = local_14a8;
          uStack_1580 = lVar35;
          FUN_1808b3da0(&local_1588);
          lVar39 = lVar39 + 8;
          uVar45 = uVar45 - 1;
        } while (uVar45 != 0);
      }
      lStack_14b0 = 0;
      local_1538[3] = 0;
      local_1538[4] = 0;
      local_1538[5] = 0;
      local_1538[6] = 0;
      local_1538[7] = 0;
      local_1538[8] = 0;
      local_1538[9] = 0;
      local_1538[10] = 0;
      local_1538[0xb] = 0;
      local_1538[0xc] = 0;
      local_1538[0xd] = 0;
      local_1538[0xe] = 0;
      local_1538[0xf] = 0;
      local_14b8 = 0;
      local_1538[1] = lVar35;
      if (0 < (longlong)*(int *)(param_1 + 0x1524)) {
                    /* WARNING: Subroutine does not return */
        FUN_181798f36(local_1538 + 2,lVar35,(longlong)*(int *)(param_1 + 0x1524) << 3);
      }
      local_1538[0] = 0;
      *(uint *)(param_1 + 0x1518) =
           *(int *)(param_1 + 0x1518) + iVar15 & *(int *)(param_1 + 0x1520) - 1U;
      FUN_181798f42(local_1538 + 1,0,0x3f8);
      local_1138 = local_918;
      local_1134 = iVar43;
      local_1130 = (longlong)iVar43 << 2;
      if (0 < (int)local_918) {
        uVar45 = (ulonglong)local_918;
        lVar39 = 0;
        do {
          *(longlong *)((longlong)local_1538 + lVar39) =
               *(longlong *)((longlong)local_d18 + lVar39) + (longlong)iVar27 * 4;
          uVar45 = uVar45 - 1;
          lVar39 = lVar39 + 8;
        } while (uVar45 != 0);
      }
      iVar15 = local_1134;
      lVar39 = 8;
      plVar32 = local_908;
      plVar33 = local_1538;
      do {
        plVar36 = plVar33;
        plVar30 = plVar32;
        lVar11 = plVar36[1];
        lVar13 = plVar36[2];
        lVar14 = plVar36[3];
        *plVar30 = *plVar36;
        plVar30[1] = lVar11;
        lVar11 = plVar36[4];
        lVar12 = plVar36[5];
        plVar30[2] = lVar13;
        plVar30[3] = lVar14;
        lVar13 = plVar36[6];
        lVar14 = plVar36[7];
        plVar30[4] = lVar11;
        plVar30[5] = lVar12;
        lVar11 = plVar36[8];
        lVar12 = plVar36[9];
        plVar30[6] = lVar13;
        plVar30[7] = lVar14;
        lVar13 = plVar36[10];
        lVar14 = plVar36[0xb];
        plVar30[8] = lVar11;
        plVar30[9] = lVar12;
        lVar11 = plVar36[0xc];
        lVar12 = plVar36[0xd];
        plVar30[10] = lVar13;
        plVar30[0xb] = lVar14;
        lVar13 = plVar36[0xe];
        lVar14 = plVar36[0xf];
        plVar30[0xc] = lVar11;
        plVar30[0xd] = lVar12;
        plVar30[0xe] = lVar13;
        plVar30[0xf] = lVar14;
        lVar39 = lVar39 + -1;
        plVar32 = plVar30 + 0x10;
        plVar33 = plVar36 + 0x10;
      } while (lVar39 != 0);
      lVar39 = plVar36[0x11];
      plVar30[0x10] = plVar36[0x10];
      plVar30[0x11] = lVar39;
      if (0 < (int)local_1138) {
        iStack_159c = local_1134 * 4;
        lVar39 = 0;
        uVar45 = (ulonglong)local_1138;
        iStack_15a0 = local_1134;
        do {
          local_15a8 = *(undefined8 *)((longlong)local_908 + lVar39);
          iVar7 = *(int *)(param_1 + 0x15b4);
          lStack_14b0 = 0;
          local_14a8 = *(undefined4 *)(param_1 + 0x15a8);
          local_1538[0] = CONCAT44(local_1538[0]._4_4_,iVar7);
          local_1538[1] = lVar40;
          local_1538[2] = 0;
          local_1538[3] = 0;
          local_1538[4] = 0;
          local_1538[5] = 0;
          local_1538[6] = 0;
          local_1538[7] = 0;
          local_1538[8] = 0;
          local_1538[9] = 0;
          local_1538[10] = 0;
          local_1538[0xb] = 0;
          local_1538[0xc] = 0;
          local_1538[0xd] = 0;
          local_1538[0xe] = 0;
          local_1538[0xf] = 0;
          local_14b8 = 0;
          if (0 < iVar7) {
                    /* WARNING: Subroutine does not return */
            FUN_181798f36(local_1538 + 2,lVar40,(longlong)iVar7 << 3);
          }
          uStack_1590 = CONCAT44(iStack_159c,iStack_15a0);
          uVar9 = *(undefined8 *)((longlong)local_1538 + lVar39 + 0x10);
          local_1660._0_4_ = (undefined4)uVar9;
          local_1660._4_4_ = (undefined4)((ulonglong)uVar9 >> 0x20);
          local_1670 = 1;
          local_1578 = (undefined4)local_1660;
          uStack_1574 = local_1660._4_4_;
          uStack_156c = uStack_1654;
          local_1588 = 1;
          uStack_1584 = uStack_166c;
          lStack_1668 = lVar40;
          local_1660 = uVar9;
          uStack_1658 = local_14a8;
          local_1598 = local_15a8;
          uStack_1570 = local_14a8;
          uStack_1580 = lVar40;
          FUN_1808b3da0(&local_1588);
          lVar39 = lVar39 + 8;
          uVar45 = uVar45 - 1;
        } while (uVar45 != 0);
      }
      lStack_14b0 = 0;
      local_1538[3] = 0;
      local_1538[4] = 0;
      local_1538[5] = 0;
      local_1538[6] = 0;
      local_1538[7] = 0;
      local_1538[8] = 0;
      local_1538[9] = 0;
      local_1538[10] = 0;
      local_1538[0xb] = 0;
      local_1538[0xc] = 0;
      local_1538[0xd] = 0;
      local_1538[0xe] = 0;
      local_1538[0xf] = 0;
      local_14b8 = 0;
      local_1538[1] = lVar40;
      if (0 < (longlong)*(int *)(param_1 + 0x15b4)) {
                    /* WARNING: Subroutine does not return */
        FUN_181798f36(local_1538 + 2,lVar40,(longlong)*(int *)(param_1 + 0x15b4) << 3);
      }
      *(uint *)(param_1 + 0x15a8) =
           *(int *)(param_1 + 0x15a8) + iVar15 & *(int *)(param_1 + 0x15b0) - 1U;
      FUN_1808acc40(param_1 + 0x1408,uVar8,uVar44,&local_1568);
      local_1538[0] = 0;
      FUN_181798f42(local_1538 + 1,0,0x3f8);
      local_1138 = local_f8;
      local_1134 = iVar43;
      local_1130 = (longlong)iVar43 << 2;
      if (0 < (int)local_f8) {
        uVar45 = (ulonglong)local_f8;
        lVar39 = 0;
        do {
          *(longlong *)((longlong)local_1538 + lVar39) =
               *(longlong *)((longlong)local_4f8 + lVar39) + (longlong)iVar27 * 4;
          uVar45 = uVar45 - 1;
          lVar39 = lVar39 + 8;
        } while (uVar45 != 0);
      }
      lVar39 = 8;
      plVar32 = local_908;
      plVar33 = local_1538;
      do {
        plVar36 = plVar33;
        plVar30 = plVar32;
        lVar11 = plVar36[1];
        lVar13 = plVar36[2];
        lVar14 = plVar36[3];
        *plVar30 = *plVar36;
        plVar30[1] = lVar11;
        lVar11 = plVar36[4];
        lVar12 = plVar36[5];
        plVar30[2] = lVar13;
        plVar30[3] = lVar14;
        lVar13 = plVar36[6];
        lVar14 = plVar36[7];
        plVar30[4] = lVar11;
        plVar30[5] = lVar12;
        lVar11 = plVar36[8];
        lVar12 = plVar36[9];
        plVar30[6] = lVar13;
        plVar30[7] = lVar14;
        lVar13 = plVar36[10];
        lVar14 = plVar36[0xb];
        plVar30[8] = lVar11;
        plVar30[9] = lVar12;
        lVar11 = plVar36[0xc];
        lVar12 = plVar36[0xd];
        plVar30[10] = lVar13;
        plVar30[0xb] = lVar14;
        lVar13 = plVar36[0xe];
        uVar1 = *(undefined4 *)((longlong)plVar36 + 0x74);
        lVar14 = plVar36[0xf];
        uVar10 = *(undefined4 *)((longlong)plVar36 + 0x7c);
        plVar30[0xc] = lVar11;
        plVar30[0xd] = lVar12;
        *(int *)(plVar30 + 0xe) = (int)lVar13;
        *(undefined4 *)((longlong)plVar30 + 0x74) = uVar1;
        *(int *)(plVar30 + 0xf) = (int)lVar14;
        *(undefined4 *)((longlong)plVar30 + 0x7c) = uVar10;
        lVar39 = lVar39 + -1;
        plVar32 = plVar30 + 0x10;
        plVar33 = plVar36 + 0x10;
      } while (lVar39 != 0);
      uVar1 = *(undefined4 *)((longlong)plVar36 + 0x84);
      lVar39 = plVar36[0x11];
      uVar10 = *(undefined4 *)((longlong)plVar36 + 0x8c);
      *(int *)(plVar30 + 0x10) = (int)plVar36[0x10];
      *(undefined4 *)((longlong)plVar30 + 0x84) = uVar1;
      *(int *)(plVar30 + 0x11) = (int)lVar39;
      *(undefined4 *)((longlong)plVar30 + 0x8c) = uVar10;
      FUN_1808b3af0(param_1 + 0x1408,local_908,uVar44 & 0xffffffff);
      iVar27 = iVar27 + iVar31;
      param_7._0_4_ = (int)param_7 - iVar31;
    } while (iVar27 < local_f4);
  }
  return;
}

