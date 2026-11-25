// FUN_180889bb0 @ 0x180889bb0

void FUN_180889bb0(longlong param_1,longlong *param_2,longlong *param_3,longlong *param_4,
                  undefined1 param_5,undefined1 param_6,longlong *param_7)

{
  undefined4 uVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  longlong *plVar6;
  undefined8 uVar7;
  longlong lVar8;
  longlong lVar9;
  longlong lVar10;
  longlong lVar11;
  longlong lVar12;
  longlong lVar13;
  longlong lVar14;
  longlong lVar15;
  longlong lVar16;
  longlong lVar17;
  longlong lVar18;
  longlong lVar19;
  longlong lVar20;
  longlong lVar21;
  longlong lVar22;
  longlong lVar23;
  longlong lVar24;
  int iVar25;
  uint uVar26;
  uint uVar27;
  longlong *plVar28;
  undefined1 *puVar29;
  int iVar30;
  uint uVar31;
  uint uVar32;
  longlong lVar33;
  char cVar34;
  ulonglong uVar35;
  ulonglong uVar36;
  longlong lVar37;
  undefined8 in_stack_fffffffffffffb58;
  undefined4 uVar38;
  undefined1 local_488 [16];
  longlong local_478 [16];
  uint local_3f8;
  uint uStack_3f4;
  longlong lStack_3f0;
  longlong local_3e8 [16];
  undefined8 local_368;
  longlong lStack_360;
  longlong local_358 [16];
  uint local_2d8;
  uint uStack_2d4;
  longlong lStack_2d0;
  longlong local_2c8 [4];
  longlong local_2a8;
  longlong lStack_2a0;
  longlong local_298;
  longlong lStack_290;
  longlong local_288;
  longlong lStack_280;
  longlong local_278;
  longlong lStack_270;
  longlong local_268;
  longlong lStack_260;
  longlong local_258;
  longlong lStack_250;
  undefined8 local_248;
  longlong lStack_240;
  longlong local_238 [16];
  uint local_1b8;
  uint uStack_1b4;
  longlong lStack_1b0;
  longlong local_1a8 [4];
  longlong local_188;
  longlong lStack_180;
  longlong local_178;
  longlong lStack_170;
  longlong local_168;
  longlong lStack_160;
  longlong local_158;
  longlong lStack_150;
  longlong local_148;
  longlong lStack_140;
  longlong local_138;
  longlong lStack_130;
  undefined8 local_128;
  longlong lStack_120;
  longlong *local_118;
  longlong local_110;
  undefined1 *local_108;
  undefined1 *local_100;
  undefined1 *local_f8;
  
  plVar6 = param_7;
  *(int *)(param_1 + 0x2c30) = *(int *)(param_1 + 0x2c30) - *(int *)((longlong)param_2 + 0x84);
  local_488[0] = *(int *)(*(longlong *)(param_1 + 0x2c38) + 0xb0) == 1;
  if (-1 < *(int *)(param_1 + 0x2c30)) goto LAB_18088ac75;
  iVar25 = *(int *)(param_1 + 0x2c30);
  do {
    iVar25 = iVar25 + *(int *)(param_1 + 0x60);
  } while (iVar25 < 0);
  *(int *)(param_1 + 0x2c30) = iVar25;
  iVar25 = 0;
  param_7._0_1_ = *(char *)(param_1 + 0x2c40);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c40) = 0;
  UNLOCK();
  cVar2 = *(char *)(param_1 + 0x2c41);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c41) = 0;
  UNLOCK();
  cVar34 = *(char *)(param_1 + 0x2c45);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c45) = 0;
  UNLOCK();
  cVar3 = *(char *)(param_1 + 0x2c44);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c44) = 0;
  UNLOCK();
  cVar4 = *(char *)(param_1 + 0x2c43);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c43) = 0;
  UNLOCK();
  cVar5 = *(char *)(param_1 + 0x2c42);
  LOCK();
  *(undefined1 *)(param_1 + 0x2c42) = 0;
  UNLOCK();
  if (cVar2 != '\0') {
    FUN_180878070(param_1);
  }
  if (cVar34 != '\0') {
    FUN_180868f90(param_1);
  }
  uVar38 = (undefined4)((ulonglong)in_stack_fffffffffffffb58 >> 0x20);
  if ((char)param_7 == '\0') {
    if (((cVar5 != '\0') || (cVar2 != '\0')) || (cVar4 != '\0')) goto LAB_180889f46;
  }
  else {
    uVar36 = (ulonglong)(int)*(uint *)(param_1 + 0xaa0);
    local_358[0] = 0;
    local_358[0xf] = 0;
    iVar30 = 0;
    local_2d8 = *(uint *)(param_1 + 0xa98);
    uStack_2d4 = *(uint *)(param_1 + 0xaa0);
    lStack_2d0 = uVar36 << 2;
    local_358[1] = 0;
    local_358[2] = 0;
    local_358[3] = 0;
    local_358[4] = 0;
    local_358[5] = 0;
    local_358[6] = 0;
    local_358[7] = 0;
    local_358[8] = 0;
    local_358[9] = 0;
    local_358[10] = 0;
    local_358[0xb] = 0;
    local_358[0xc] = 0;
    local_358[0xd] = 0;
    local_358[0xe] = 0;
    if (0 < (int)*(uint *)(param_1 + 0xa98)) {
      plVar28 = local_358;
      do {
        iVar30 = iVar30 + 1;
        *plVar28 = *(longlong *)(((param_1 + 0xa18) - (longlong)local_358) + (longlong)plVar28);
        plVar28 = plVar28 + 1;
      } while (iVar30 < (int)local_2d8);
      uVar36 = (ulonglong)uStack_2d4;
    }
    local_478[0] = local_358[0];
    local_478[1] = local_358[1];
    local_478[2] = local_358[2];
    local_478[3] = local_358[3];
    local_478[4] = local_358[4];
    local_478[5] = local_358[5];
    local_478[6] = local_358[6];
    local_478[7] = local_358[7];
    local_478[8] = local_358[8];
    local_478[9] = local_358[9];
    local_478[10] = local_358[10];
    local_478[0xb] = local_358[0xb];
    local_478[0xc] = local_358[0xc];
    local_478[0xd] = local_358[0xd];
    local_478[0xe] = local_358[0xe];
    local_478[0xf] = local_358[0xf];
    local_3f8 = local_2d8;
    uStack_3f4 = uStack_2d4;
    lStack_3f0 = lStack_2d0;
    if (0 < (int)local_2d8) {
      plVar28 = local_478;
      uVar35 = (ulonglong)local_2d8;
      do {
        FUN_1800010d0(*plVar28,uVar36 & 0xffffffff);
        plVar28 = plVar28 + 1;
        uVar35 = uVar35 - 1;
      } while (uVar35 != 0);
    }
    uVar38 = (undefined4)((ulonglong)in_stack_fffffffffffffb58 >> 0x20);
    uVar36 = (ulonglong)(int)*(uint *)(param_1 + 0xbc0);
    local_358[0] = 0;
    local_358[0xf] = 0;
    iVar30 = 0;
    local_2d8 = *(uint *)(param_1 + 3000);
    uStack_2d4 = *(uint *)(param_1 + 0xbc0);
    lStack_2d0 = uVar36 << 2;
    local_358[1] = 0;
    local_358[2] = 0;
    local_358[3] = 0;
    local_358[4] = 0;
    local_358[5] = 0;
    local_358[6] = 0;
    local_358[7] = 0;
    local_358[8] = 0;
    local_358[9] = 0;
    local_358[10] = 0;
    local_358[0xb] = 0;
    local_358[0xc] = 0;
    local_358[0xd] = 0;
    local_358[0xe] = 0;
    if (0 < (int)*(uint *)(param_1 + 3000)) {
      plVar28 = local_358;
      do {
        iVar30 = iVar30 + 1;
        *plVar28 = *(longlong *)(((param_1 + 0xb38) - (longlong)local_358) + (longlong)plVar28);
        plVar28 = plVar28 + 1;
      } while (iVar30 < (int)local_2d8);
      uVar36 = (ulonglong)uStack_2d4;
    }
    local_478[0] = local_358[0];
    local_478[1] = local_358[1];
    local_478[2] = local_358[2];
    local_478[3] = local_358[3];
    local_478[4] = local_358[4];
    local_478[5] = local_358[5];
    local_478[6] = local_358[6];
    local_478[7] = local_358[7];
    local_478[8] = local_358[8];
    local_478[9] = local_358[9];
    local_478[10] = local_358[10];
    local_478[0xb] = local_358[0xb];
    local_478[0xc] = local_358[0xc];
    local_478[0xd] = local_358[0xd];
    local_478[0xe] = local_358[0xe];
    local_478[0xf] = local_358[0xf];
    local_3f8 = local_2d8;
    uStack_3f4 = uStack_2d4;
    lStack_3f0 = lStack_2d0;
    if (0 < (int)local_2d8) {
      plVar28 = local_478;
      uVar35 = (ulonglong)local_2d8;
      do {
        FUN_1800010d0(*plVar28,uVar36 & 0xffffffff);
        uVar38 = (undefined4)((ulonglong)in_stack_fffffffffffffb58 >> 0x20);
        plVar28 = plVar28 + 1;
        uVar35 = uVar35 - 1;
      } while (uVar35 != 0);
    }
LAB_180889f46:
    FUN_18087bb60(param_1);
  }
  if (cVar3 != '\0') {
    FUN_18087e220(param_1);
  }
  if (((((char)param_7 != '\0') || (cVar5 != '\0')) || (cVar3 != '\0')) &&
     ((FUN_18087b2a0(param_1), cVar5 != '\0' || (cVar3 != '\0')))) {
    uVar1 = *(undefined4 *)(param_1 + 0x5c);
    iVar30 = 0;
    local_3e8[0] = 0;
    local_3e8[0xf] = 0;
    local_368 = CONCAT44(*(int *)(param_1 + 2000),*(int *)(param_1 + 0x7c8));
    lStack_360 = (longlong)*(int *)(param_1 + 2000) << 2;
    local_3e8[1] = 0;
    local_3e8[2] = 0;
    local_3e8[3] = 0;
    local_3e8[4] = 0;
    local_3e8[5] = 0;
    local_3e8[6] = 0;
    local_3e8[7] = 0;
    local_3e8[8] = 0;
    local_3e8[9] = 0;
    local_3e8[10] = 0;
    local_3e8[0xb] = 0;
    local_3e8[0xc] = 0;
    local_3e8[0xd] = 0;
    local_3e8[0xe] = 0;
    if (0 < *(int *)(param_1 + 0x7c8)) {
      plVar28 = local_3e8;
      do {
        iVar30 = iVar30 + 1;
        *plVar28 = *(longlong *)(((param_1 + 0x748) - (longlong)local_3e8) + (longlong)plVar28);
        plVar28 = plVar28 + 1;
      } while (iVar30 < (int)(uint)local_368);
    }
    iVar30 = 0;
    uStack_3f4 = *(int *)(param_1 + 0xa10);
    local_478[0] = 0;
    local_478[0xf] = 0;
    local_3f8 = *(int *)(param_1 + 0xa08);
    lStack_3f0 = (longlong)*(int *)(param_1 + 0xa10) << 2;
    local_478[1] = 0;
    local_478[2] = 0;
    local_478[3] = 0;
    local_478[4] = 0;
    local_478[5] = 0;
    local_478[6] = 0;
    local_478[7] = 0;
    local_478[8] = 0;
    local_478[9] = 0;
    local_478[10] = 0;
    local_478[0xb] = 0;
    local_478[0xc] = 0;
    local_478[0xd] = 0;
    local_478[0xe] = 0;
    if (0 < *(int *)(param_1 + 0xa08)) {
      plVar28 = local_478;
      do {
        iVar30 = iVar30 + 1;
        *plVar28 = *(longlong *)(((param_1 + 0x988) - (longlong)local_478) + (longlong)plVar28);
        plVar28 = plVar28 + 1;
      } while (iVar30 < (int)local_3f8);
    }
    local_1a8[0] = local_3e8[0];
    local_1a8[1] = local_3e8[1];
    local_1a8[2] = local_3e8[2];
    local_1a8[3] = local_3e8[3];
    local_188 = local_3e8[4];
    lStack_180 = local_3e8[5];
    local_178 = local_3e8[6];
    lStack_170 = local_3e8[7];
    local_168 = local_3e8[8];
    lStack_160 = local_3e8[9];
    local_158 = local_3e8[10];
    lStack_150 = local_3e8[0xb];
    local_148 = local_3e8[0xc];
    lStack_140 = local_3e8[0xd];
    local_138 = local_3e8[0xe];
    lStack_130 = local_3e8[0xf];
    local_128 = local_368;
    lStack_120 = lStack_360;
    local_2c8[0] = local_478[0];
    local_2c8[1] = local_478[1];
    local_2c8[2] = local_478[2];
    local_2c8[3] = local_478[3];
    local_2a8 = local_478[4];
    lStack_2a0 = local_478[5];
    local_298 = local_478[6];
    lStack_290 = local_478[7];
    local_288 = local_478[8];
    lStack_280 = local_478[9];
    local_278 = local_478[10];
    lStack_270 = local_478[0xb];
    local_268 = local_478[0xc];
    lStack_260 = local_478[0xd];
    local_258 = local_478[0xe];
    lStack_250 = local_478[0xf];
    local_248 = CONCAT44(uStack_3f4,local_3f8);
    lStack_240 = lStack_3f0;
    uVar36 = CONCAT44(uVar38,uVar1);
    FUN_18087f0c0(local_2c8,local_1a8,*(undefined8 *)(param_1 + 0x10),
                  *(undefined8 *)(param_1 + 0x2c38),uVar36,plVar6);
    local_248._0_4_ = *(uint *)(param_1 + 0xa08);
    lVar8 = plVar6[3];
    iVar30 = 0;
    local_248._4_4_ = *(uint *)(param_1 + 0xa10);
    uVar31 = *(uint *)(param_1 + 0xa10);
    if (0 < (int)(uint)local_248) {
      plVar28 = local_2c8;
      do {
        iVar30 = iVar30 + 1;
        *plVar28 = *(longlong *)(((param_1 + 0x988) - (longlong)local_2c8) + (longlong)plVar28);
        plVar28 = plVar28 + 1;
      } while (iVar30 < (int)(uint)local_248);
      uVar31 = local_248._4_4_;
    }
    local_358[0] = 0;
    local_2d8 = (uint)local_248;
    local_358[0xf] = 0;
    lVar33 = 0;
    uStack_2d4 = uVar31;
    lStack_2d0 = (longlong)(int)uVar31 << 2;
    local_358[1] = 0;
    local_358[2] = 0;
    local_358[3] = 0;
    local_358[4] = 0;
    local_358[5] = 0;
    local_358[6] = 0;
    local_358[7] = 0;
    local_358[8] = 0;
    local_358[9] = 0;
    local_358[10] = 0;
    local_358[0xb] = 0;
    local_358[0xc] = 0;
    local_358[0xd] = 0;
    local_358[0xe] = 0;
    if (0 < (int)(uint)local_248) {
      uVar32 = *(uint *)(plVar6 + 3);
      do {
        uVar26 = uVar31 + uVar32;
        local_358[lVar33] = *plVar6 + (longlong)(int)uVar32 * 4;
        uVar32 = (uVar26 - (uVar26 & 0xf)) + 0x10;
        if ((uVar26 & 0xf) == 0) {
          uVar32 = uVar26;
        }
        lVar33 = lVar33 + 1;
        *(uint *)(plVar6 + 3) = uVar32;
      } while (lVar33 < (int)(uint)local_248);
    }
    uVar32 = uStack_2d4;
    uVar31 = local_2d8;
    uVar38 = DAT_182079f9c;
    iVar30 = 0;
    uStack_3f4 = *(int *)(param_1 + 0xa10);
    local_478[0] = 0;
    local_478[0xf] = 0;
    local_3f8 = *(int *)(param_1 + 0xa08);
    lStack_3f0 = (longlong)*(int *)(param_1 + 0xa10) << 2;
    local_478[1] = 0;
    local_478[2] = 0;
    local_478[3] = 0;
    local_478[4] = 0;
    local_478[5] = 0;
    local_478[6] = 0;
    local_478[7] = 0;
    local_478[8] = 0;
    local_478[9] = 0;
    local_478[10] = 0;
    local_478[0xb] = 0;
    local_478[0xc] = 0;
    local_478[0xd] = 0;
    local_478[0xe] = 0;
    if (0 < *(int *)(param_1 + 0xa08)) {
      plVar28 = local_478;
      do {
        iVar30 = iVar30 + 1;
        *plVar28 = *(longlong *)(((param_1 + 0x988) - (longlong)local_478) + (longlong)plVar28);
        plVar28 = plVar28 + 1;
      } while (iVar30 < (int)local_3f8);
    }
    lVar24 = lStack_2d0;
    lVar23 = local_358[0xf];
    lVar22 = local_358[0xe];
    lVar21 = local_358[0xd];
    lVar20 = local_358[0xc];
    lVar19 = local_358[0xb];
    lVar18 = local_358[10];
    lVar17 = local_358[9];
    lVar16 = local_358[8];
    lVar15 = local_358[7];
    lVar14 = local_358[6];
    lVar13 = local_358[5];
    lVar12 = local_358[4];
    lVar11 = local_358[3];
    lVar10 = local_358[2];
    lVar9 = local_358[1];
    lVar33 = local_358[0];
    uVar7 = CONCAT44(uStack_2d4,local_2d8);
    local_2c8[0] = local_358[0];
    local_2c8[1] = local_358[1];
    local_2c8[2] = local_358[2];
    local_2c8[3] = local_358[3];
    local_2a8 = local_358[4];
    lStack_2a0 = local_358[5];
    local_298 = local_358[6];
    lStack_290 = local_358[7];
    local_288 = local_358[8];
    lStack_280 = local_358[9];
    local_278 = local_358[10];
    lStack_270 = local_358[0xb];
    local_268 = local_358[0xc];
    lStack_260 = local_358[0xd];
    local_258 = local_358[0xe];
    lStack_250 = local_358[0xf];
    local_248 = uVar7;
    lStack_240 = lStack_2d0;
    local_1a8[0] = local_478[0];
    local_1a8[1] = local_478[1];
    local_1a8[2] = local_478[2];
    local_1a8[3] = local_478[3];
    local_188 = local_478[4];
    lStack_180 = local_478[5];
    local_178 = local_478[6];
    lStack_170 = local_478[7];
    local_168 = local_478[8];
    lStack_160 = local_478[9];
    local_158 = local_478[10];
    lStack_150 = local_478[0xb];
    local_148 = local_478[0xc];
    lStack_140 = local_478[0xd];
    local_138 = local_478[0xe];
    lStack_130 = local_478[0xf];
    local_128 = CONCAT44(uStack_3f4,local_3f8);
    lStack_120 = lStack_3f0;
    if (0 < (int)uVar31) {
      lVar37 = 0;
      uVar35 = (ulonglong)uVar31;
      do {
        uVar36 = uVar36 & 0xffffffff00000000;
        FUN_180001250(*(undefined8 *)((longlong)local_1a8 + lVar37),
                      *(undefined8 *)((longlong)local_2c8 + lVar37),uVar32,uVar38,uVar36);
        lVar37 = lVar37 + 8;
        uVar35 = uVar35 - 1;
      } while (uVar35 != 0);
    }
    local_2c8[0] = lVar33;
    local_2c8[1] = lVar9;
    local_2c8[2] = lVar10;
    local_2c8[3] = lVar11;
    local_2a8 = lVar12;
    lStack_2a0 = lVar13;
    local_298 = lVar14;
    lStack_290 = lVar15;
    local_288 = lVar16;
    lStack_280 = lVar17;
    local_278 = lVar18;
    lStack_270 = lVar19;
    local_268 = lVar20;
    lStack_260 = lVar21;
    local_258 = lVar22;
    lStack_250 = lVar23;
    local_248 = uVar7;
    lStack_240 = lVar24;
    if (0 < (int)uVar31) {
      plVar28 = local_2c8;
      uVar36 = (ulonglong)uVar31;
      do {
        FUN_1801c8530(*plVar28,*plVar28,uVar32);
        plVar28 = plVar28 + 1;
        uVar36 = uVar36 - 1;
      } while (uVar36 != 0);
    }
    local_238[0] = 0;
    local_238[0xf] = 0;
    lVar37 = 0;
    lStack_1b0 = (longlong)(int)uVar32 << 2;
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
    local_1b8 = uVar31;
    uStack_1b4 = uVar32;
    if (0 < (int)uVar31) {
      uVar26 = *(uint *)(plVar6 + 3);
      do {
        uVar27 = uVar26 + uVar32;
        local_238[lVar37] = *plVar6 + (longlong)(int)uVar26 * 4;
        uVar26 = (uVar27 - (uVar27 & 0xf)) + 0x10;
        if ((uVar27 & 0xf) == 0) {
          uVar26 = uVar27;
        }
        lVar37 = lVar37 + 1;
        *(uint *)(plVar6 + 3) = uVar26;
      } while (lVar37 < (int)uVar31);
    }
    uVar26 = uStack_1b4;
    uVar32 = local_1b8;
    uVar36 = (ulonglong)local_1b8;
    local_478[0] = local_238[0];
    local_478[1] = local_238[1];
    local_478[2] = local_238[2];
    local_478[3] = local_238[3];
    local_478[4] = local_238[4];
    local_478[5] = local_238[5];
    local_478[6] = local_238[6];
    local_478[7] = local_238[7];
    local_478[8] = local_238[8];
    local_478[9] = local_238[9];
    local_478[10] = local_238[10];
    local_478[0xb] = local_238[0xb];
    local_478[0xc] = local_238[0xc];
    local_478[0xd] = local_238[0xd];
    local_478[0xe] = local_238[0xe];
    local_478[0xf] = local_238[0xf];
    local_3f8 = local_1b8;
    uStack_3f4 = uStack_1b4;
    lStack_3f0 = lStack_1b0;
    local_1a8[0] = lVar33;
    local_1a8[1] = lVar9;
    local_1a8[2] = lVar10;
    local_1a8[3] = lVar11;
    local_188 = lVar12;
    lStack_180 = lVar13;
    local_178 = lVar14;
    lStack_170 = lVar15;
    local_168 = lVar16;
    lStack_160 = lVar17;
    local_158 = lVar18;
    lStack_150 = lVar19;
    local_148 = lVar20;
    lStack_140 = lVar21;
    local_138 = lVar22;
    lStack_130 = lVar23;
    lStack_120 = lVar24;
    local_128 = uVar7;
    FUN_1808981e0(local_478,local_1a8);
    local_3e8[0] = local_238[0];
    local_3e8[1] = local_238[1];
    local_3e8[2] = local_238[2];
    local_3e8[3] = local_238[3];
    local_3e8[4] = local_238[4];
    local_3e8[5] = local_238[5];
    local_3e8[6] = local_238[6];
    local_3e8[7] = local_238[7];
    local_3e8[8] = local_238[8];
    local_3e8[9] = local_238[9];
    local_3e8[10] = local_238[10];
    local_3e8[0xb] = local_238[0xb];
    local_3e8[0xc] = local_238[0xc];
    local_3e8[0xd] = local_238[0xd];
    local_3e8[0xe] = local_238[0xe];
    local_3e8[0xf] = local_238[0xf];
    local_368 = CONCAT44(uStack_1b4,local_1b8);
    lStack_360 = lStack_1b0;
    if (0 < (int)uVar32) {
      plVar28 = local_3e8;
      do {
        FUN_1800012e0(uVar38,*plVar28,uVar26);
        plVar28 = plVar28 + 1;
        uVar36 = uVar36 - 1;
      } while (uVar36 != 0);
    }
    uVar36 = (ulonglong)*(int *)(param_1 + 0x500);
    uVar32 = *(uint *)(param_1 + 0x4f8);
    local_3e8[0xf] = 0;
    iVar30 = 0;
    local_3e8[0] = 0;
    local_3e8[1] = 0;
    local_3e8[2] = 0;
    local_3e8[3] = 0;
    local_3e8[4] = 0;
    local_368 = CONCAT44(*(int *)(param_1 + 0x500),uVar32);
    local_3e8[5] = 0;
    local_3e8[6] = 0;
    lStack_360 = uVar36 << 2;
    local_3e8[7] = 0;
    local_3e8[8] = 0;
    local_3e8[9] = 0;
    local_3e8[10] = 0;
    local_3e8[0xb] = 0;
    local_3e8[0xc] = 0;
    local_3e8[0xd] = 0;
    local_3e8[0xe] = 0;
    if (*(char *)(param_1 + 0x58) == '\0') {
      if (0 < (int)uVar32) {
        plVar28 = local_3e8;
        do {
          iVar30 = iVar30 + 1;
          *plVar28 = *(longlong *)(((param_1 + 0x478) - (longlong)local_3e8) + (longlong)plVar28);
          plVar28 = plVar28 + 1;
        } while (iVar30 < (int)(uint)local_368);
        uVar36 = local_368 >> 0x20;
        uVar32 = (uint)local_368;
      }
      lVar37 = local_358[0];
      local_2c8[0] = lVar33;
      local_2c8[1] = lVar9;
      local_2c8[2] = lVar10;
      local_2c8[3] = lVar11;
      local_2a8 = lVar12;
      lStack_2a0 = lVar13;
      local_298 = lVar14;
      lStack_290 = lVar15;
      local_288 = lVar16;
      lStack_280 = lVar17;
      local_278 = lVar18;
      lStack_270 = lVar19;
      local_268 = lVar20;
      lStack_260 = lVar21;
      local_258 = lVar22;
      lStack_250 = lVar23;
      local_248 = uVar7;
      lStack_240 = lVar24;
      local_478[0] = local_3e8[0];
      local_478[1] = local_3e8[1];
      local_478[2] = local_3e8[2];
      local_478[3] = local_3e8[3];
      local_478[4] = local_3e8[4];
      local_478[5] = local_3e8[5];
      local_478[6] = local_3e8[6];
      local_478[7] = local_3e8[7];
      local_478[8] = local_3e8[8];
      local_478[9] = local_3e8[9];
      local_478[10] = local_3e8[10];
      local_478[0xb] = local_3e8[0xb];
      local_478[0xc] = local_3e8[0xc];
      local_478[0xd] = local_3e8[0xd];
      local_478[0xe] = local_3e8[0xe];
      local_478[0xf] = local_3e8[0xf];
      local_3f8 = (uint)local_368;
      uStack_3f4 = local_368._4_4_;
      lStack_3f0 = lStack_360;
      if (uVar32 == uVar31) {
        if (0 < (int)uVar32) {
          lVar33 = 0;
          uVar35 = (ulonglong)uVar32;
          do {
            FUN_180001340(*(undefined8 *)((longlong)local_2c8 + lVar33),
                          *(undefined8 *)((longlong)local_478 + lVar33),uVar36 & 0xffffffff);
            lVar33 = lVar33 + 8;
            uVar35 = uVar35 - 1;
          } while (uVar35 != 0);
        }
      }
      else if ((uVar31 == 1) && (0 < (int)uVar32)) {
        plVar28 = local_478;
        uVar35 = (ulonglong)uVar32;
        do {
          FUN_180001340(lVar37,*plVar28,uVar36 & 0xffffffff);
          plVar28 = plVar28 + 1;
          uVar35 = uVar35 - 1;
        } while (uVar35 != 0);
      }
    }
    else {
      if (0 < (int)uVar32) {
        plVar28 = local_3e8;
        do {
          iVar30 = iVar30 + 1;
          *plVar28 = *(longlong *)(((param_1 + 0x478) - (longlong)local_3e8) + (longlong)plVar28);
          plVar28 = plVar28 + 1;
        } while (iVar30 < (int)(uint)local_368);
        uVar36 = local_368 >> 0x20;
        uVar32 = (uint)local_368;
      }
      lVar37 = local_358[0];
      local_2c8[0] = lVar33;
      local_2c8[1] = lVar9;
      local_2c8[2] = lVar10;
      local_2c8[3] = lVar11;
      local_2a8 = lVar12;
      lStack_2a0 = lVar13;
      local_298 = lVar14;
      lStack_290 = lVar15;
      local_288 = lVar16;
      lStack_280 = lVar17;
      local_278 = lVar18;
      lStack_270 = lVar19;
      local_268 = lVar20;
      lStack_260 = lVar21;
      local_258 = lVar22;
      lStack_250 = lVar23;
      local_248 = uVar7;
      lStack_240 = lVar24;
      local_478[0] = local_3e8[0];
      local_478[1] = local_3e8[1];
      local_478[2] = local_3e8[2];
      local_478[3] = local_3e8[3];
      local_478[4] = local_3e8[4];
      local_478[5] = local_3e8[5];
      local_478[6] = local_3e8[6];
      local_478[7] = local_3e8[7];
      local_478[8] = local_3e8[8];
      local_478[9] = local_3e8[9];
      local_478[10] = local_3e8[10];
      local_478[0xb] = local_3e8[0xb];
      local_478[0xc] = local_3e8[0xc];
      local_478[0xd] = local_3e8[0xd];
      local_478[0xe] = local_3e8[0xe];
      local_478[0xf] = local_3e8[0xf];
      local_3f8 = (uint)local_368;
      uStack_3f4 = local_368._4_4_;
      lStack_3f0 = lStack_360;
      if (uVar32 == uVar31) {
        if (0 < (int)uVar32) {
          lVar33 = 0;
          uVar35 = (ulonglong)uVar32;
          do {
            FUN_180001340(*(undefined8 *)((longlong)local_2c8 + lVar33),
                          *(undefined8 *)((longlong)local_478 + lVar33),uVar36 & 0xffffffff);
            lVar33 = lVar33 + 8;
            uVar35 = uVar35 - 1;
          } while (uVar35 != 0);
        }
      }
      else if ((uVar31 == 1) && (0 < (int)uVar32)) {
        plVar28 = local_478;
        uVar35 = (ulonglong)uVar32;
        do {
          FUN_180001340(lVar37,*plVar28,uVar36 & 0xffffffff);
          plVar28 = plVar28 + 1;
          uVar35 = uVar35 - 1;
        } while (uVar35 != 0);
      }
      uVar36 = (ulonglong)*(int *)(param_1 + 0x500);
      uVar31 = *(uint *)(param_1 + 0x4f8);
      local_3e8[0] = 0;
      local_3e8[0xf] = 0;
      iVar30 = 0;
      local_368 = CONCAT44(*(int *)(param_1 + 0x500),uVar31);
      lStack_360 = uVar36 << 2;
      local_3e8[1] = 0;
      local_3e8[2] = 0;
      local_3e8[3] = 0;
      local_3e8[4] = 0;
      local_3e8[5] = 0;
      local_3e8[6] = 0;
      local_3e8[7] = 0;
      local_3e8[8] = 0;
      local_3e8[9] = 0;
      local_3e8[10] = 0;
      local_3e8[0xb] = 0;
      local_3e8[0xc] = 0;
      local_3e8[0xd] = 0;
      local_3e8[0xe] = 0;
      if (0 < (int)uVar31) {
        plVar28 = local_3e8;
        do {
          iVar30 = iVar30 + 1;
          *plVar28 = *(longlong *)(((param_1 + 0x478) - (longlong)local_3e8) + (longlong)plVar28);
          plVar28 = plVar28 + 1;
        } while (iVar30 < (int)(uint)local_368);
        uVar36 = local_368 >> 0x20;
        uVar31 = (uint)local_368;
      }
      lVar33 = local_238[0];
      local_2c8[0] = local_238[0];
      local_2c8[1] = local_238[1];
      local_2c8[2] = local_238[2];
      local_2c8[3] = local_238[3];
      local_2a8 = local_238[4];
      lStack_2a0 = local_238[5];
      local_298 = local_238[6];
      lStack_290 = local_238[7];
      local_288 = local_238[8];
      lStack_280 = local_238[9];
      local_278 = local_238[10];
      lStack_270 = local_238[0xb];
      local_268 = local_238[0xc];
      lStack_260 = local_238[0xd];
      local_258 = local_238[0xe];
      lStack_250 = local_238[0xf];
      local_248 = CONCAT44(uStack_1b4,local_1b8);
      lStack_240 = lStack_1b0;
      local_478[2] = local_3e8[2];
      local_478[3] = local_3e8[3];
      local_478[0] = local_3e8[0];
      local_478[1] = local_3e8[1];
      local_478[6] = local_3e8[6];
      local_478[7] = local_3e8[7];
      local_478[4] = local_3e8[4];
      local_478[5] = local_3e8[5];
      local_478[10] = local_3e8[10];
      local_478[0xb] = local_3e8[0xb];
      local_478[8] = local_3e8[8];
      local_478[9] = local_3e8[9];
      local_478[0xe] = local_3e8[0xe];
      local_478[0xf] = local_3e8[0xf];
      local_478[0xc] = local_3e8[0xc];
      local_478[0xd] = local_3e8[0xd];
      local_3f8 = (uint)local_368;
      uStack_3f4 = local_368._4_4_;
      lStack_3f0 = lStack_360;
      if (uVar31 == local_1b8) {
        if (0 < (int)uVar31) {
          lVar33 = 0;
          uVar35 = (ulonglong)uVar31;
          do {
            FUN_180001370(*(undefined8 *)((longlong)local_2c8 + lVar33),
                          *(undefined8 *)((longlong)local_478 + lVar33),uVar36 & 0xffffffff);
            lVar33 = lVar33 + 8;
            uVar35 = uVar35 - 1;
          } while (uVar35 != 0);
        }
      }
      else if ((local_1b8 == 1) && (0 < (int)uVar31)) {
        plVar28 = local_478;
        uVar35 = (ulonglong)uVar31;
        do {
          FUN_180001370(lVar33,*plVar28,uVar36 & 0xffffffff);
          plVar28 = plVar28 + 1;
          uVar35 = uVar35 - 1;
        } while (uVar35 != 0);
      }
    }
    FUN_18087f780(param_1,plVar6);
    *(undefined1 *)(param_1 + 0x2bc8) = 1;
    if (*(longlong *)(param_1 + 0x48) != 0) {
      puVar29 = (undefined1 *)(param_1 + 0x2bb8);
      do {
        iVar25 = iVar25 + 1;
        *puVar29 = 1;
        puVar29 = puVar29 + 1;
      } while ((ulonglong)(longlong)iVar25 < *(ulonglong *)(param_1 + 0x48));
    }
    *(int *)(plVar6 + 3) = (int)lVar8;
  }
LAB_18088ac75:
  local_108 = &param_6;
  local_100 = local_488;
  local_f8 = &param_5;
  local_2c8[0] = *param_4;
  local_2c8[1] = param_4[1];
  local_2c8[2] = param_4[2];
  local_2c8[3] = param_4[3];
  local_2a8 = param_4[4];
  lStack_2a0 = param_4[5];
  local_288 = param_4[8];
  lStack_280 = param_4[9];
  local_298 = param_4[6];
  lStack_290 = param_4[7];
  local_268 = param_4[0xc];
  lStack_260 = param_4[0xd];
  local_278 = param_4[10];
  lStack_270 = param_4[0xb];
  local_248 = param_4[0x10];
  lStack_240 = param_4[0x11];
  local_258 = param_4[0xe];
  lStack_250 = param_4[0xf];
  local_1a8[0] = *param_3;
  local_1a8[1] = param_3[1];
  local_1a8[2] = param_3[2];
  local_1a8[3] = param_3[3];
  local_188 = param_3[4];
  lStack_180 = param_3[5];
  local_178 = param_3[6];
  lStack_170 = param_3[7];
  local_168 = param_3[8];
  lStack_160 = param_3[9];
  local_158 = param_3[10];
  lStack_150 = param_3[0xb];
  local_148 = param_3[0xc];
  lStack_140 = param_3[0xd];
  local_138 = param_3[0xe];
  lStack_130 = param_3[0xf];
  local_128 = param_3[0x10];
  lStack_120 = param_3[0x11];
  local_478[0] = *param_2;
  local_478[1] = param_2[1];
  local_478[2] = param_2[2];
  local_478[3] = param_2[3];
  local_478[4] = param_2[4];
  local_478[5] = param_2[5];
  local_478[8] = param_2[8];
  local_478[9] = param_2[9];
  local_478[6] = param_2[6];
  local_478[7] = param_2[7];
  local_478[0xc] = param_2[0xc];
  local_478[0xd] = param_2[0xd];
  local_478[10] = param_2[10];
  local_478[0xb] = param_2[0xb];
  local_3f8 = (uint)param_2[0x10];
  uStack_3f4 = *(undefined4 *)((longlong)param_2 + 0x84);
  lStack_3f0 = param_2[0x11];
  local_478[0xe] = param_2[0xe];
  local_478[0xf] = param_2[0xf];
  local_118 = plVar6;
  local_110 = param_1;
  FUN_180899940(param_1 + 0x1408,local_478,local_1a8,local_2c8,*(undefined8 *)(param_1 + 0x60),
                *(undefined8 *)(param_1 + 0x28),&local_118);
  return;
}

