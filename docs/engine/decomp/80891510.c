// FUN_180891510 @ 0x180891510

/* WARNING: Function: __chkstk replaced with injection: alloca_probe */

void FUN_180891510(longlong param_1,longlong param_2,longlong param_3,longlong param_4,
                  undefined8 param_5,undefined1 param_6,longlong *param_7)

{
  char cVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  int iVar7;
  int iVar8;
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
  int iVar23;
  uint uVar24;
  uint uVar25;
  int iVar26;
  int iVar27;
  ulonglong uVar28;
  longlong *plVar29;
  longlong *plVar30;
  longlong *plVar31;
  uint uVar32;
  uint uVar33;
  longlong *plVar34;
  undefined1 *puVar35;
  longlong *plVar36;
  undefined4 *puVar37;
  undefined8 uVar38;
  longlong lVar39;
  ulonglong uVar40;
  ulonglong uVar41;
  longlong lVar42;
  longlong lVar43;
  longlong lVar44;
  undefined4 uVar45;
  undefined1 auVar46 [16];
  undefined1 auVar47 [16];
  undefined1 in_XMM2 [16];
  undefined1 auVar48 [16];
  longlong lVar49;
  undefined1 local_36a8 [8];
  int local_36a0;
  undefined4 local_3698;
  undefined4 uStack_3694;
  longlong lStack_3690;
  undefined8 local_3688;
  undefined8 uStack_3680;
  undefined4 local_3674;
  ulonglong local_3670;
  undefined1 local_3668 [16];
  undefined8 local_3658;
  undefined8 uStack_3650;
  ulonglong local_3648;
  undefined8 local_3640;
  longlong local_3638;
  ulonglong local_3630;
  undefined8 local_3628;
  int iStack_3620;
  int iStack_361c;
  undefined8 local_3618;
  int iStack_3610;
  int iStack_360c;
  undefined8 local_3608;
  undefined8 uStack_3600;
  undefined4 local_35f8;
  undefined4 uStack_35f4;
  uint uStack_35f0;
  undefined4 uStack_35ec;
  longlong *local_35e8;
  longlong local_35e0;
  undefined1 *local_35d8;
  undefined1 *local_35d0;
  undefined8 local_35c8;
  longlong local_35b8 [16];
  undefined8 local_3538;
  longlong lStack_3530;
  undefined4 local_3528;
  longlong alStack_31c8 [2];
  uint local_31b8;
  int local_31b4;
  longlong local_31b0 [17];
  undefined8 local_3128;
  longlong lStack_3120;
  longlong alStack_2db8 [2];
  uint local_2da8;
  int local_2da4;
  longlong local_2da0 [17];
  uint local_2d18;
  uint uStack_2d14;
  longlong lStack_2d10;
  uint local_2998;
  int local_2994;
  longlong local_2990;
  longlong local_2988 [16];
  uint local_2908;
  uint uStack_2904;
  longlong lStack_2900;
  longlong alStack_2598 [2];
  uint local_2588;
  int local_2584;
  longlong local_2580 [8];
  undefined8 uStack_2540;
  undefined8 local_2538;
  undefined8 uStack_2530;
  undefined8 local_2528;
  undefined8 uStack_2520;
  undefined8 local_2518;
  undefined8 uStack_2510;
  undefined8 local_2508;
  undefined8 uStack_2500;
  undefined8 local_24f8;
  longlong lStack_24f0;
  uint local_2178;
  int local_2174;
  longlong local_2170;
  longlong local_2168 [16];
  undefined8 local_20e8;
  longlong lStack_20e0;
  uint local_1d68;
  int local_1d64;
  longlong local_1d60;
  longlong local_1d58;
  undefined1 auStack_1d50 [1016];
  uint local_1958;
  int local_1954;
  longlong local_1950;
  longlong local_1948 [130];
  longlong local_1538 [128];
  uint local_1138;
  int local_1134;
  longlong local_1128 [128];
  uint local_d28;
  int local_d24;
  longlong local_d18 [130];
  longlong local_908 [130];
  longlong local_4f8 [150];
  undefined8 uStack_48;
  
  uStack_48 = 0x180891542;
  *(int *)(param_1 + 0x2c30) = *(int *)(param_1 + 0x2c30) - *(int *)(param_2 + 0x404);
  local_36a8[0] = *(int *)(*(longlong *)(param_1 + 0x2c38) + 0xb0) == 1;
  if (*(int *)(param_1 + 0x2c30) < 0) {
    iVar23 = *(int *)(param_1 + 0x2c30);
    do {
      iVar23 = iVar23 + *(int *)(param_1 + 0x60);
    } while (iVar23 < 0);
    *(int *)(param_1 + 0x2c30) = iVar23;
    cVar1 = *(char *)(param_1 + 0x2c40);
    LOCK();
    *(undefined1 *)(param_1 + 0x2c40) = 0;
    UNLOCK();
    cVar2 = *(char *)(param_1 + 0x2c41);
    LOCK();
    *(undefined1 *)(param_1 + 0x2c41) = 0;
    UNLOCK();
    cVar3 = *(char *)(param_1 + 0x2c45);
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
    if (cVar3 != '\0') {
      FUN_180868c40(param_1);
    }
    if (cVar1 == '\0') {
      if (((cVar6 != '\0') || (cVar2 != '\0')) || (cVar5 != '\0')) goto LAB_1808918f6;
      plVar34 = param_7;
    }
    else {
      local_2988[0] = 0;
      local_2988[0xf] = 0;
      iVar23 = 0;
      local_2908 = *(uint *)(param_1 + 0xa98);
      uStack_2904 = *(int *)(param_1 + 0xaa0);
      lStack_2900 = (longlong)*(int *)(param_1 + 0xaa0) << 2;
      local_2988[1] = 0;
      local_2988[2] = 0;
      local_2988[3] = 0;
      local_2988[4] = 0;
      local_2988[5] = 0;
      local_2988[6] = 0;
      local_2988[7] = 0;
      local_2988[8] = 0;
      local_2988[9] = 0;
      local_2988[10] = 0;
      local_2988[0xb] = 0;
      local_2988[0xc] = 0;
      local_2988[0xd] = 0;
      local_2988[0xe] = 0;
      if (0 < (int)*(uint *)(param_1 + 0xa98)) {
        plVar34 = local_2988;
        do {
          iVar23 = iVar23 + 1;
          *plVar34 = *(longlong *)(((param_1 + 0xa18) - (longlong)local_2988) + (longlong)plVar34);
          plVar34 = plVar34 + 1;
        } while (iVar23 < (int)local_2908);
      }
      local_31b0[1] = local_2988[0];
      local_31b0[2] = local_2988[1];
      local_31b0[3] = local_2988[2];
      local_31b0[4] = local_2988[3];
      local_31b0[5] = local_2988[4];
      local_31b0[6] = local_2988[5];
      local_31b0[7] = local_2988[6];
      local_31b0[8] = local_2988[7];
      local_31b0[9] = local_2988[8];
      local_31b0[10] = local_2988[9];
      local_31b0[0xb] = local_2988[10];
      local_31b0[0xc] = local_2988[0xb];
      local_31b0[0xd] = local_2988[0xc];
      local_31b0[0xe] = local_2988[0xd];
      local_31b0[0xf] = local_2988[0xe];
      local_31b0[0x10] = local_2988[0xf];
      local_3128 = CONCAT44(uStack_2904,local_2908);
      lStack_3120 = lStack_2900;
      if (0 < (int)local_2908) {
        plVar34 = local_31b0;
        uVar40 = (ulonglong)local_2908;
        do {
          plVar34 = plVar34 + 1;
          FUN_1800010d0(*plVar34);
          uVar40 = uVar40 - 1;
        } while (uVar40 != 0);
      }
      uVar40 = (ulonglong)(int)*(uint *)(param_1 + 0xbc0);
      local_2988[0] = 0;
      local_2988[0xf] = 0;
      iVar23 = 0;
      local_2908 = *(uint *)(param_1 + 3000);
      uStack_2904 = *(uint *)(param_1 + 0xbc0);
      lStack_2900 = uVar40 << 2;
      local_2988[1] = 0;
      local_2988[2] = 0;
      local_2988[3] = 0;
      local_2988[4] = 0;
      local_2988[5] = 0;
      local_2988[6] = 0;
      local_2988[7] = 0;
      local_2988[8] = 0;
      local_2988[9] = 0;
      local_2988[10] = 0;
      local_2988[0xb] = 0;
      local_2988[0xc] = 0;
      local_2988[0xd] = 0;
      local_2988[0xe] = 0;
      if (0 < (int)*(uint *)(param_1 + 3000)) {
        plVar34 = local_2988;
        do {
          iVar23 = iVar23 + 1;
          *plVar34 = *(longlong *)(((param_1 + 0xb38) - (longlong)local_2988) + (longlong)plVar34);
          plVar34 = plVar34 + 1;
        } while (iVar23 < (int)local_2908);
        uVar40 = (ulonglong)uStack_2904;
      }
      local_31b0[1] = local_2988[0];
      local_31b0[2] = local_2988[1];
      local_31b0[3] = local_2988[2];
      local_31b0[4] = local_2988[3];
      local_31b0[5] = local_2988[4];
      local_31b0[6] = local_2988[5];
      local_31b0[7] = local_2988[6];
      local_31b0[8] = local_2988[7];
      local_31b0[9] = local_2988[8];
      local_31b0[10] = local_2988[9];
      local_31b0[0xb] = local_2988[10];
      local_31b0[0xc] = local_2988[0xb];
      local_31b0[0xd] = local_2988[0xc];
      local_31b0[0xe] = local_2988[0xd];
      local_31b0[0xf] = local_2988[0xe];
      local_31b0[0x10] = local_2988[0xf];
      local_3128 = CONCAT44(uStack_2904,local_2908);
      lStack_3120 = lStack_2900;
      if ((int)local_2908 < 1) {
LAB_1808918f6:
        plVar34 = param_7;
        FUN_18087bb60(param_1);
      }
      else {
        plVar29 = local_31b0;
        uVar41 = (ulonglong)local_2908;
        do {
          plVar29 = plVar29 + 1;
          FUN_1800010d0(*plVar29,uVar40 & 0xffffffff);
          plVar34 = param_7;
          uVar41 = uVar41 - 1;
        } while (uVar41 != 0);
        FUN_18087bb60(param_1);
      }
    }
    if (cVar4 != '\0') {
      FUN_18087e220(param_1);
    }
    if ((((cVar1 != '\0') || (cVar6 != '\0')) || (cVar4 != '\0')) &&
       ((FUN_18087b2a0(param_1), cVar6 != '\0' || (cVar4 != '\0')))) {
      uVar32 = *(uint *)(param_1 + 0x5c);
      in_XMM2 = ZEXT416(uVar32);
      iVar23 = 0;
      local_2168[0] = 0;
      local_2168[0xf] = 0;
      local_20e8 = CONCAT44(*(int *)(param_1 + 2000),*(int *)(param_1 + 0x7c8));
      lStack_20e0 = (longlong)*(int *)(param_1 + 2000) << 2;
      local_2168[1] = 0;
      local_2168[2] = 0;
      local_2168[3] = 0;
      local_2168[4] = 0;
      local_2168[5] = 0;
      local_2168[6] = 0;
      local_2168[7] = 0;
      local_2168[8] = 0;
      local_2168[9] = 0;
      local_2168[10] = 0;
      local_2168[0xb] = 0;
      local_2168[0xc] = 0;
      local_2168[0xd] = 0;
      local_2168[0xe] = 0;
      if (0 < *(int *)(param_1 + 0x7c8)) {
        plVar29 = local_2168;
        do {
          iVar23 = iVar23 + 1;
          *plVar29 = *(longlong *)(((param_1 + 0x748) - (longlong)local_2168) + (longlong)plVar29);
          plVar29 = plVar29 + 1;
        } while (iVar23 < (int)local_20e8);
      }
      iVar23 = 0;
      local_31b0[1] = 0;
      local_31b0[0x10] = 0;
      local_3128 = CONCAT44(*(int *)(param_1 + 0xa10),*(int *)(param_1 + 0xa08));
      lStack_3120 = (longlong)*(int *)(param_1 + 0xa10) << 2;
      local_31b0[2] = 0;
      local_31b0[3] = 0;
      local_31b0[4] = 0;
      local_31b0[5] = 0;
      local_31b0[6] = 0;
      local_31b0[7] = 0;
      local_31b0[8] = 0;
      local_31b0[9] = 0;
      local_31b0[10] = 0;
      local_31b0[0xb] = 0;
      local_31b0[0xc] = 0;
      local_31b0[0xd] = 0;
      local_31b0[0xe] = 0;
      local_31b0[0xf] = 0;
      if (0 < *(int *)(param_1 + 0xa08)) {
        plVar29 = local_31b0;
        do {
          plVar29 = plVar29 + 1;
          iVar23 = iVar23 + 1;
          *plVar29 = *(longlong *)
                      (((param_1 + 0x988) - (longlong)(local_31b0 + 1)) + (longlong)plVar29);
        } while (iVar23 < (int)local_3128);
      }
      local_2580[1] = local_2168[0];
      local_2580[2] = local_2168[1];
      local_2580[3] = local_2168[2];
      local_2580[4] = local_2168[3];
      local_2580[5] = local_2168[4];
      local_2580[6] = local_2168[5];
      local_2580[7] = local_2168[6];
      uStack_2540 = local_2168[7];
      local_2538 = local_2168[8];
      uStack_2530 = local_2168[9];
      local_2528 = local_2168[10];
      uStack_2520 = local_2168[0xb];
      local_2518 = local_2168[0xc];
      uStack_2510 = local_2168[0xd];
      local_2508 = local_2168[0xe];
      uStack_2500 = local_2168[0xf];
      local_24f8 = local_20e8;
      lStack_24f0 = lStack_20e0;
      local_35b8[0] = local_31b0[1];
      local_35b8[1] = local_31b0[2];
      local_35b8[2] = local_31b0[3];
      local_35b8[3] = local_31b0[4];
      local_35b8[4] = local_31b0[5];
      local_35b8[5] = local_31b0[6];
      local_35b8[6] = local_31b0[7];
      local_35b8[7] = local_31b0[8];
      local_35b8[8] = local_31b0[9];
      local_35b8[9] = local_31b0[10];
      local_35b8[10] = local_31b0[0xb];
      local_35b8[0xb] = local_31b0[0xc];
      local_35b8[0xc] = local_31b0[0xd];
      local_35b8[0xd] = local_31b0[0xe];
      local_35b8[0xe] = local_31b0[0xf];
      local_35b8[0xf] = local_31b0[0x10];
      local_3538 = local_3128;
      lStack_3530 = lStack_3120;
      FUN_18087f0c0(local_35b8,local_2580 + 1,*(undefined8 *)(param_1 + 0x10),
                    *(undefined8 *)(param_1 + 0x2c38),uVar32,plVar34);
      local_3538._0_4_ = *(uint *)(param_1 + 0xa08);
      local_36a0 = (int)plVar34[3];
      iVar23 = 0;
      local_3538._4_4_ = *(uint *)(param_1 + 0xa10);
      if (0 < (int)(uint)local_3538) {
        plVar29 = local_35b8;
        do {
          iVar23 = iVar23 + 1;
          *plVar29 = *(longlong *)(((param_1 + 0x988) - (longlong)local_35b8) + (longlong)plVar29);
          plVar29 = plVar29 + 1;
        } while (iVar23 < (int)(uint)local_3538);
      }
      local_2da0[1] = 0;
      local_2d18 = (uint)local_3538;
      local_2da0[0x10] = 0;
      lVar43 = 0;
      uStack_2d14 = local_3538._4_4_;
      lStack_2d10 = (longlong)(int)local_3538._4_4_ << 2;
      local_2da0[2] = 0;
      local_2da0[3] = 0;
      local_2da0[4] = 0;
      local_2da0[5] = 0;
      local_2da0[6] = 0;
      local_2da0[7] = 0;
      local_2da0[8] = 0;
      local_2da0[9] = 0;
      local_2da0[10] = 0;
      local_2da0[0xb] = 0;
      local_2da0[0xc] = 0;
      local_2da0[0xd] = 0;
      local_2da0[0xe] = 0;
      local_2da0[0xf] = 0;
      if (0 < (int)(uint)local_3538) {
        uVar32 = *(uint *)(plVar34 + 3);
        do {
          uVar24 = uVar32 + local_3538._4_4_;
          local_2da0[lVar43 + 1] = *plVar34 + (longlong)(int)uVar32 * 4;
          uVar32 = (uVar24 - (uVar24 & 0xf)) + 0x10;
          if ((uVar24 & 0xf) == 0) {
            uVar32 = uVar24;
          }
          lVar43 = lVar43 + 1;
          *(uint *)(plVar34 + 3) = uVar32;
        } while (lVar43 < (int)(uint)local_3538);
      }
      uVar24 = uStack_2d14;
      uVar32 = local_2d18;
      lVar43 = local_2da0[1];
      uVar45 = DAT_182079f9c;
      iVar23 = 0;
      local_31b0[1] = 0;
      local_31b0[0x10] = 0;
      local_3128 = CONCAT44(*(int *)(param_1 + 0xa10),*(int *)(param_1 + 0xa08));
      lStack_3120 = (longlong)*(int *)(param_1 + 0xa10) << 2;
      local_31b0[2] = 0;
      local_31b0[3] = 0;
      local_31b0[4] = 0;
      local_31b0[5] = 0;
      local_31b0[6] = 0;
      local_31b0[7] = 0;
      local_31b0[8] = 0;
      local_31b0[9] = 0;
      local_31b0[10] = 0;
      local_31b0[0xb] = 0;
      local_31b0[0xc] = 0;
      local_31b0[0xd] = 0;
      local_31b0[0xe] = 0;
      local_31b0[0xf] = 0;
      if (0 < *(int *)(param_1 + 0xa08)) {
        plVar34 = local_31b0;
        do {
          plVar34 = plVar34 + 1;
          iVar23 = iVar23 + 1;
          *plVar34 = *(longlong *)
                      (((param_1 + 0x988) - (longlong)(local_31b0 + 1)) + (longlong)plVar34);
        } while (iVar23 < (int)local_3128);
      }
      lVar22 = lStack_2d10;
      lVar21 = local_2da0[0x10];
      lVar20 = local_2da0[0xf];
      lVar19 = local_2da0[0xe];
      lVar18 = local_2da0[0xd];
      lVar17 = local_2da0[0xc];
      lVar16 = local_2da0[0xb];
      lVar15 = local_2da0[10];
      lVar14 = local_2da0[9];
      lVar13 = local_2da0[8];
      lVar12 = local_2da0[7];
      lVar11 = local_2da0[6];
      lVar10 = local_2da0[5];
      lVar9 = local_2da0[4];
      lVar42 = local_2da0[3];
      lVar49 = local_2da0[2];
      lVar44 = local_2da0[1];
      uVar38 = CONCAT44(uStack_2d14,local_2d18);
      local_35b8[0] = local_2da0[1];
      local_35b8[1] = local_2da0[2];
      local_35b8[2] = local_2da0[3];
      local_35b8[3] = local_2da0[4];
      local_35b8[4] = local_2da0[5];
      local_35b8[5] = local_2da0[6];
      local_35b8[6] = local_2da0[7];
      local_35b8[7] = local_2da0[8];
      local_35b8[8] = local_2da0[9];
      local_35b8[9] = local_2da0[10];
      local_35b8[10] = local_2da0[0xb];
      local_35b8[0xb] = local_2da0[0xc];
      local_35b8[0xc] = local_2da0[0xd];
      local_35b8[0xd] = local_2da0[0xe];
      local_35b8[0xe] = local_2da0[0xf];
      local_35b8[0xf] = local_2da0[0x10];
      local_3538 = uVar38;
      lStack_3530 = lStack_2d10;
      local_2580[1] = local_31b0[1];
      local_2580[2] = local_31b0[2];
      local_2580[3] = local_31b0[3];
      local_2580[4] = local_31b0[4];
      local_2580[5] = local_31b0[5];
      local_2580[6] = local_31b0[6];
      local_2580[7] = local_31b0[7];
      uStack_2540 = local_31b0[8];
      local_2538 = local_31b0[9];
      uStack_2530 = local_31b0[10];
      local_2528 = local_31b0[0xb];
      uStack_2520 = local_31b0[0xc];
      local_2518 = local_31b0[0xd];
      uStack_2510 = local_31b0[0xe];
      local_2508 = local_31b0[0xf];
      uStack_2500 = local_31b0[0x10];
      local_24f8 = local_3128;
      lStack_24f0 = lStack_3120;
      if (0 < (int)uVar32) {
        lVar39 = 0;
        uVar40 = (ulonglong)uVar32;
        do {
          FUN_180001250(*(undefined8 *)((longlong)local_2580 + lVar39 + 8),
                        *(undefined8 *)((longlong)local_35b8 + lVar39),uVar24,uVar45,0);
          lVar39 = lVar39 + 8;
          uVar40 = uVar40 - 1;
        } while (uVar40 != 0);
      }
      local_35b8[0] = lVar44;
      local_35b8[1] = lVar49;
      local_35b8[2] = lVar42;
      local_35b8[3] = lVar9;
      local_35b8[4] = lVar10;
      local_35b8[5] = lVar11;
      local_35b8[6] = lVar12;
      local_35b8[7] = lVar13;
      local_35b8[8] = lVar14;
      local_35b8[9] = lVar15;
      local_35b8[10] = lVar16;
      local_35b8[0xb] = lVar17;
      local_35b8[0xc] = lVar18;
      local_35b8[0xd] = lVar19;
      local_35b8[0xe] = lVar20;
      local_35b8[0xf] = lVar21;
      local_3538 = uVar38;
      lStack_3530 = lVar22;
      if (0 < (int)uVar32) {
        plVar34 = local_35b8;
        uVar40 = (ulonglong)uVar32;
        do {
          FUN_1801c8530(*plVar34,*plVar34);
          plVar34 = plVar34 + 1;
          uVar40 = uVar40 - 1;
        } while (uVar40 != 0);
      }
      local_2988[0] = 0;
      local_2988[0xf] = 0;
      lVar39 = 0;
      uVar33 = *(uint *)(param_7 + 3);
      lStack_2900 = (longlong)(int)uVar24 << 2;
      local_2988[1] = 0;
      local_2988[2] = 0;
      local_2988[3] = 0;
      local_2988[4] = 0;
      local_2988[5] = 0;
      local_2988[6] = 0;
      local_2988[7] = 0;
      local_2988[8] = 0;
      local_2988[9] = 0;
      local_2988[10] = 0;
      local_2988[0xb] = 0;
      local_2988[0xc] = 0;
      local_2988[0xd] = 0;
      local_2988[0xe] = 0;
      local_2908 = uVar32;
      uStack_2904 = uVar24;
      if (0 < (int)uVar32) {
        do {
          uVar25 = uVar24 + uVar33;
          local_2988[lVar39] = *param_7 + (longlong)(int)uVar33 * 4;
          uVar33 = (uVar25 - (uVar25 & 0xf)) + 0x10;
          if ((uVar25 & 0xf) == 0) {
            uVar33 = uVar25;
          }
          lVar39 = lVar39 + 1;
          *(uint *)(param_7 + 3) = uVar33;
        } while (lVar39 < (int)uVar32);
      }
      uVar24 = local_2908;
      lVar39 = local_2988[0];
      local_31b0[1] = local_2988[0];
      local_31b0[2] = local_2988[1];
      local_31b0[3] = local_2988[2];
      local_31b0[4] = local_2988[3];
      local_31b0[5] = local_2988[4];
      local_31b0[6] = local_2988[5];
      local_31b0[7] = local_2988[6];
      local_31b0[8] = local_2988[7];
      local_31b0[9] = local_2988[8];
      local_31b0[10] = local_2988[9];
      local_31b0[0xb] = local_2988[10];
      local_31b0[0xc] = local_2988[0xb];
      local_31b0[0xd] = local_2988[0xc];
      local_31b0[0xe] = local_2988[0xd];
      local_31b0[0xf] = local_2988[0xe];
      local_31b0[0x10] = local_2988[0xf];
      local_3128 = CONCAT44(uStack_2904,local_2908);
      lStack_3120 = lStack_2900;
      local_2580[1] = lVar44;
      local_2580[2] = lVar49;
      local_2580[3] = lVar42;
      local_2580[4] = lVar9;
      local_2580[5] = lVar10;
      local_2580[6] = lVar11;
      local_2580[7] = lVar12;
      uStack_2540 = lVar13;
      local_2538 = lVar14;
      uStack_2530 = lVar15;
      local_2528 = lVar16;
      uStack_2520 = lVar17;
      local_2518 = lVar18;
      uStack_2510 = lVar19;
      local_2508 = lVar20;
      uStack_2500 = lVar21;
      lStack_24f0 = lVar22;
      local_24f8 = uVar38;
      FUN_1808981e0(local_31b0 + 1,local_2580 + 1);
      local_2168[0] = local_2988[0];
      local_2168[1] = local_2988[1];
      local_2168[2] = local_2988[2];
      local_2168[3] = local_2988[3];
      local_2168[4] = local_2988[4];
      local_2168[5] = local_2988[5];
      local_2168[6] = local_2988[6];
      local_2168[7] = local_2988[7];
      local_2168[8] = local_2988[8];
      local_2168[9] = local_2988[9];
      local_2168[10] = local_2988[10];
      local_2168[0xb] = local_2988[0xb];
      local_2168[0xc] = local_2988[0xc];
      local_2168[0xd] = local_2988[0xd];
      local_2168[0xe] = local_2988[0xe];
      local_2168[0xf] = local_2988[0xf];
      local_20e8 = CONCAT44(uStack_2904,local_2908);
      lStack_20e0 = lStack_2900;
      if (0 < (int)uVar24) {
        uVar40 = (ulonglong)uVar24;
        do {
          FUN_1800012e0();
          uVar40 = uVar40 - 1;
        } while (uVar40 != 0);
      }
      uVar40 = (ulonglong)(int)*(uint *)(param_1 + 0x500);
      local_2d18 = *(uint *)(param_1 + 0x4f8);
      iVar23 = 0;
      uStack_2d14 = *(uint *)(param_1 + 0x500);
      local_2da0[1] = 0;
      local_2da0[2] = 0;
      local_2da0[3] = 0;
      local_2da0[4] = 0;
      local_2da0[5] = 0;
      local_2da0[6] = 0;
      local_2da0[7] = 0;
      local_2da0[8] = 0;
      local_2da0[9] = 0;
      local_2da0[10] = 0;
      local_2da0[0xb] = 0;
      local_2da0[0xc] = 0;
      local_2da0[0xd] = 0;
      local_2da0[0xe] = 0;
      local_2da0[0xf] = 0;
      if (*(char *)(param_1 + 0x58) == '\0') {
        local_2da0[0x10] = 0;
        lStack_2d10 = uVar40 << 2;
        if (0 < (int)local_2d18) {
          plVar34 = local_2da0;
          do {
            plVar34 = plVar34 + 1;
            iVar23 = iVar23 + 1;
            *plVar34 = *(longlong *)
                        (((param_1 + 0x478) - (longlong)(local_2da0 + 1)) + (longlong)plVar34);
          } while (iVar23 < (int)local_2d18);
          uVar40 = (ulonglong)uStack_2d14;
        }
        local_35b8[0] = lVar44;
        local_35b8[1] = lVar49;
        local_35b8[2] = lVar42;
        local_35b8[3] = lVar9;
        local_35b8[4] = lVar10;
        local_35b8[5] = lVar11;
        local_35b8[6] = lVar12;
        local_35b8[7] = lVar13;
        local_35b8[8] = lVar14;
        local_35b8[9] = lVar15;
        local_35b8[10] = lVar16;
        local_35b8[0xb] = lVar17;
        local_35b8[0xc] = lVar18;
        local_35b8[0xd] = lVar19;
        local_35b8[0xe] = lVar20;
        local_35b8[0xf] = lVar21;
        local_3538 = uVar38;
        lStack_3530 = lVar22;
        local_31b0[1] = local_2da0[1];
        local_31b0[2] = local_2da0[2];
        local_31b0[3] = local_2da0[3];
        local_31b0[4] = local_2da0[4];
        local_31b0[5] = local_2da0[5];
        local_31b0[6] = local_2da0[6];
        local_31b0[7] = local_2da0[7];
        local_31b0[8] = local_2da0[8];
        local_31b0[9] = local_2da0[9];
        local_31b0[10] = local_2da0[10];
        local_31b0[0xb] = local_2da0[0xb];
        local_31b0[0xc] = local_2da0[0xc];
        local_31b0[0xd] = local_2da0[0xd];
        local_31b0[0xe] = local_2da0[0xe];
        local_31b0[0xf] = local_2da0[0xf];
        local_31b0[0x10] = local_2da0[0x10];
        local_3128 = CONCAT44(uStack_2d14,local_2d18);
        lStack_3120 = lStack_2d10;
        if (local_2d18 == uVar32) {
          if (0 < (int)local_2d18) {
            lVar43 = 0;
            uVar41 = (ulonglong)local_2d18;
            do {
              FUN_180001340(*(undefined8 *)((longlong)local_35b8 + lVar43),
                            *(undefined8 *)((longlong)local_31b0 + lVar43 + 8),uVar40 & 0xffffffff);
              lVar43 = lVar43 + 8;
              uVar41 = uVar41 - 1;
            } while (uVar41 != 0);
          }
        }
        else if ((uVar32 == 1) && (0 < (int)local_2d18)) {
          plVar34 = local_31b0;
          uVar41 = (ulonglong)local_2d18;
          do {
            plVar34 = plVar34 + 1;
            FUN_180001340(lVar43,*plVar34,uVar40 & 0xffffffff);
            uVar41 = uVar41 - 1;
          } while (uVar41 != 0);
        }
      }
      else {
        local_2da0[0x10] = 0;
        lStack_2d10 = uVar40 << 2;
        if (0 < (int)local_2d18) {
          plVar34 = local_2da0;
          do {
            plVar34 = plVar34 + 1;
            iVar23 = iVar23 + 1;
            *plVar34 = *(longlong *)
                        (((param_1 + 0x478) - (longlong)(local_2da0 + 1)) + (longlong)plVar34);
          } while (iVar23 < (int)local_2d18);
        }
        local_35b8[0] = lVar44;
        local_35b8[1] = lVar49;
        local_35b8[2] = lVar42;
        local_35b8[3] = lVar9;
        local_35b8[4] = lVar10;
        local_35b8[5] = lVar11;
        local_35b8[6] = lVar12;
        local_35b8[7] = lVar13;
        local_35b8[8] = lVar14;
        local_35b8[9] = lVar15;
        local_35b8[10] = lVar16;
        local_35b8[0xb] = lVar17;
        local_35b8[0xc] = lVar18;
        local_35b8[0xd] = lVar19;
        local_35b8[0xe] = lVar20;
        local_35b8[0xf] = lVar21;
        local_3538 = uVar38;
        lStack_3530 = lVar22;
        local_31b0[1] = local_2da0[1];
        local_31b0[2] = local_2da0[2];
        local_31b0[3] = local_2da0[3];
        local_31b0[4] = local_2da0[4];
        local_31b0[5] = local_2da0[5];
        local_31b0[6] = local_2da0[6];
        local_31b0[7] = local_2da0[7];
        local_31b0[8] = local_2da0[8];
        local_31b0[9] = local_2da0[9];
        local_31b0[10] = local_2da0[10];
        local_31b0[0xb] = local_2da0[0xb];
        local_31b0[0xc] = local_2da0[0xc];
        local_31b0[0xd] = local_2da0[0xd];
        local_31b0[0xe] = local_2da0[0xe];
        local_31b0[0xf] = local_2da0[0xf];
        local_31b0[0x10] = local_2da0[0x10];
        local_3128 = CONCAT44(uStack_2d14,local_2d18);
        lStack_3120 = lStack_2d10;
        if (local_2d18 == uVar32) {
          if (0 < (int)local_2d18) {
            lVar43 = 0;
            uVar40 = (ulonglong)local_2d18;
            do {
              FUN_180001340(*(undefined8 *)((longlong)local_35b8 + lVar43),
                            *(undefined8 *)((longlong)local_31b0 + lVar43 + 8));
              lVar43 = lVar43 + 8;
              uVar40 = uVar40 - 1;
            } while (uVar40 != 0);
          }
        }
        else if ((uVar32 == 1) && (0 < (int)local_2d18)) {
          plVar34 = local_31b0;
          uVar40 = (ulonglong)local_2d18;
          do {
            plVar34 = plVar34 + 1;
            FUN_180001340(lVar43,*plVar34);
            uVar40 = uVar40 - 1;
          } while (uVar40 != 0);
        }
        local_2da0[1] = 0;
        local_2da0[0x10] = 0;
        iVar23 = 0;
        local_2da0[2] = 0;
        local_2da0[3] = 0;
        uVar40 = (ulonglong)(int)*(uint *)(param_1 + 0x500);
        local_2d18 = *(uint *)(param_1 + 0x4f8);
        uStack_2d14 = *(uint *)(param_1 + 0x500);
        lStack_2d10 = uVar40 << 2;
        local_2da0[4] = 0;
        local_2da0[5] = 0;
        local_2da0[6] = 0;
        local_2da0[7] = 0;
        local_2da0[8] = 0;
        local_2da0[9] = 0;
        local_2da0[10] = 0;
        local_2da0[0xb] = 0;
        local_2da0[0xc] = 0;
        local_2da0[0xd] = 0;
        local_2da0[0xe] = 0;
        local_2da0[0xf] = 0;
        if (0 < (int)*(uint *)(param_1 + 0x4f8)) {
          plVar34 = local_2da0;
          do {
            plVar34 = plVar34 + 1;
            iVar23 = iVar23 + 1;
            *plVar34 = *(longlong *)
                        (((param_1 + 0x478) - (longlong)(local_2da0 + 1)) + (longlong)plVar34);
          } while (iVar23 < (int)local_2d18);
          uVar40 = (ulonglong)uStack_2d14;
        }
        local_35b8[0] = local_2988[0];
        local_35b8[1] = local_2988[1];
        local_35b8[2] = local_2988[2];
        local_35b8[3] = local_2988[3];
        local_35b8[4] = local_2988[4];
        local_35b8[5] = local_2988[5];
        local_35b8[6] = local_2988[6];
        local_35b8[7] = local_2988[7];
        local_35b8[8] = local_2988[8];
        local_35b8[9] = local_2988[9];
        local_35b8[10] = local_2988[10];
        local_35b8[0xb] = local_2988[0xb];
        local_35b8[0xc] = local_2988[0xc];
        local_35b8[0xd] = local_2988[0xd];
        local_35b8[0xe] = local_2988[0xe];
        local_35b8[0xf] = local_2988[0xf];
        local_3538 = CONCAT44(uStack_2904,local_2908);
        lStack_3530 = lStack_2900;
        local_31b0[1] = local_2da0[1];
        local_31b0[2] = local_2da0[2];
        local_31b0[3] = local_2da0[3];
        local_31b0[4] = local_2da0[4];
        local_31b0[5] = local_2da0[5];
        local_31b0[6] = local_2da0[6];
        local_31b0[7] = local_2da0[7];
        local_31b0[8] = local_2da0[8];
        local_31b0[9] = local_2da0[9];
        local_31b0[10] = local_2da0[10];
        local_31b0[0xb] = local_2da0[0xb];
        local_31b0[0xc] = local_2da0[0xc];
        local_31b0[0xd] = local_2da0[0xd];
        local_31b0[0xe] = local_2da0[0xe];
        local_31b0[0xf] = local_2da0[0xf];
        local_31b0[0x10] = local_2da0[0x10];
        local_3128 = CONCAT44(uStack_2d14,local_2d18);
        lStack_3120 = lStack_2d10;
        if (local_2d18 == uVar24) {
          if (0 < (int)local_2d18) {
            lVar43 = 0;
            uVar41 = (ulonglong)local_2d18;
            do {
              FUN_180001370(*(undefined8 *)((longlong)local_35b8 + lVar43),
                            *(undefined8 *)((longlong)local_31b0 + lVar43 + 8),uVar40 & 0xffffffff);
              lVar43 = lVar43 + 8;
              uVar41 = uVar41 - 1;
            } while (uVar41 != 0);
          }
        }
        else if ((uVar24 == 1) && (0 < (int)local_2d18)) {
          plVar34 = local_31b0;
          uVar41 = (ulonglong)local_2d18;
          do {
            plVar34 = plVar34 + 1;
            FUN_180001370(lVar39,*plVar34,uVar40 & 0xffffffff);
            uVar41 = uVar41 - 1;
          } while (uVar41 != 0);
        }
      }
      plVar34 = param_7;
      FUN_18087f780(param_1);
      iVar23 = 0;
      *(undefined1 *)(param_1 + 0x2bc8) = 1;
      if (*(longlong *)(param_1 + 0x48) != 0) {
        puVar35 = (undefined1 *)(param_1 + 0x2bb8);
        do {
          iVar23 = iVar23 + 1;
          *puVar35 = 1;
          puVar35 = puVar35 + 1;
        } while ((ulonglong)(longlong)iVar23 < *(ulonglong *)(param_1 + 0x48));
      }
      *(int *)(plVar34 + 3) = local_36a0;
      local_35e8 = plVar34;
      goto LAB_1808927bf;
    }
  }
  local_35e8 = param_7;
LAB_1808927bf:
  local_3630 = (ulonglong)*(int *)(param_2 + 0x404);
  local_35d8 = &param_6;
  local_35d0 = local_36a8;
  local_35c8 = param_5;
  local_3648 = 0;
  if (local_3630 != 0) {
    local_3638 = param_1 + 0x1408;
    plVar34 = local_35e8;
    local_35e0 = param_1;
    do {
      uVar40 = local_3648;
      uVar28 = *(longlong *)(param_1 + 0x60) - *(longlong *)(param_1 + 0x2c28);
      local_31b0[1] = 0;
      uVar41 = local_3630 - local_3648;
      if (uVar28 < local_3630 - local_3648) {
        uVar41 = uVar28;
      }
      iVar23 = (int)uVar41;
      *(ulonglong *)(param_1 + 0x2c28) =
           (ulonglong)(*(int *)(param_1 + 0x2c28) + iVar23 & *(int *)(param_1 + 0x60) - 1U);
      local_3670 = uVar41;
      FUN_181798f42(local_31b0 + 2,0,0x3f8);
      local_2da8 = *(uint *)(param_2 + 0x400);
      lVar43 = 0;
      local_2da0[0] = (longlong)iVar23 << 2;
      lVar44 = (longlong)(int)local_2da8;
      iVar27 = (int)uVar40;
      local_2da4 = iVar23;
      if (((0 < (int)local_2da8) && (7 < local_2da8)) && (1 < DAT_1821c7690)) {
        auVar48._4_4_ = iVar27;
        auVar48._0_4_ = iVar27;
        auVar48._8_4_ = iVar27;
        auVar48._12_4_ = iVar27;
        uVar32 = local_2da8 & 0x80000007;
        if ((int)uVar32 < 0) {
          uVar32 = (uVar32 - 1 | 0xfffffff8) + 1;
        }
        iVar26 = local_2da8 - uVar32;
        auVar48 = pmovsxdq(in_XMM2,auVar48);
        in_XMM2._0_8_ = auVar48._0_8_ * 4;
        in_XMM2._8_8_ = auVar48._8_8_ * 4;
        plVar29 = (longlong *)(param_2 + 0x20);
        do {
          lVar49 = plVar29[-3];
          lVar43 = lVar43 + 8;
          lVar42 = plVar29[-2];
          lVar9 = plVar29[-1];
          plVar31 = plVar29 + 8;
          plVar30 = (longlong *)((longlong)alStack_31c8 + (-0x40 - param_2) + (longlong)plVar31);
          *plVar30 = plVar29[-4] + in_XMM2._0_8_;
          plVar30[1] = lVar49 + in_XMM2._8_8_;
          lVar49 = *plVar29;
          lVar10 = plVar29[1];
          plVar30 = (longlong *)((longlong)alStack_31c8 + (-0x30 - param_2) + (longlong)plVar31);
          *plVar30 = lVar42 + in_XMM2._0_8_;
          plVar30[1] = lVar9 + in_XMM2._8_8_;
          lVar42 = plVar29[2];
          lVar9 = plVar29[3];
          plVar29 = (longlong *)((longlong)alStack_31c8 + (-0x20 - param_2) + (longlong)plVar31);
          *plVar29 = lVar49 + in_XMM2._0_8_;
          plVar29[1] = lVar10 + in_XMM2._8_8_;
          plVar29 = (longlong *)((longlong)alStack_31c8 + (-0x10 - param_2) + (longlong)plVar31);
          *plVar29 = lVar42 + in_XMM2._0_8_;
          plVar29[1] = lVar9 + in_XMM2._8_8_;
          plVar29 = plVar31;
        } while (lVar43 < iVar26);
      }
      if (lVar43 < lVar44) {
        do {
          local_31b0[lVar43 + 1] = *(longlong *)(param_2 + lVar43 * 8) + (longlong)iVar27 * 4;
          lVar43 = lVar43 + 1;
        } while (lVar43 < lVar44);
      }
      iVar26 = local_2da4;
      uVar24 = local_2da8;
      local_2580[1] = 0;
      FUN_181798f42(local_2580 + 2,0,0x3f8);
      lVar43 = 0;
      local_2178 = *(uint *)(param_3 + 0x400);
      uVar32 = *(uint *)(param_3 + 0x400);
      local_2170 = (longlong)iVar23 << 2;
      local_2174 = iVar23;
      if (((0 < (int)uVar32) && (7 < uVar32)) && (1 < DAT_1821c7690)) {
        auVar46._4_4_ = iVar27;
        auVar46._0_4_ = iVar27;
        auVar46._8_4_ = iVar27;
        auVar46._12_4_ = iVar27;
        uVar33 = uVar32 & 0x80000007;
        if ((int)uVar33 < 0) {
          uVar33 = (uVar33 - 1 | 0xfffffff8) + 1;
        }
        auVar48 = pmovsxdq(in_XMM2,auVar46);
        in_XMM2._0_8_ = auVar48._0_8_ * 4;
        in_XMM2._8_8_ = auVar48._8_8_ * 4;
        plVar29 = (longlong *)(param_3 + 0x20);
        do {
          lVar44 = plVar29[-3];
          lVar43 = lVar43 + 8;
          lVar49 = plVar29[-2];
          lVar42 = plVar29[-1];
          plVar31 = plVar29 + 8;
          plVar30 = (longlong *)((longlong)alStack_2598 + (-0x40 - param_3) + (longlong)plVar31);
          *plVar30 = plVar29[-4] + in_XMM2._0_8_;
          plVar30[1] = lVar44 + in_XMM2._8_8_;
          lVar44 = *plVar29;
          lVar9 = plVar29[1];
          plVar30 = (longlong *)((longlong)alStack_2598 + (-0x30 - param_3) + (longlong)plVar31);
          *plVar30 = lVar49 + in_XMM2._0_8_;
          plVar30[1] = lVar42 + in_XMM2._8_8_;
          lVar49 = plVar29[2];
          lVar42 = plVar29[3];
          plVar29 = (longlong *)((longlong)alStack_2598 + (-0x20 - param_3) + (longlong)plVar31);
          *plVar29 = lVar44 + in_XMM2._0_8_;
          plVar29[1] = lVar9 + in_XMM2._8_8_;
          plVar29 = (longlong *)((longlong)alStack_2598 + (-0x10 - param_3) + (longlong)plVar31);
          *plVar29 = lVar49 + in_XMM2._0_8_;
          plVar29[1] = lVar42 + in_XMM2._8_8_;
          plVar29 = plVar31;
        } while (lVar43 < (int)(uVar32 - uVar33));
        uVar41 = local_3670;
      }
      if (lVar43 < (int)uVar32) {
        do {
          local_2580[lVar43 + 1] = *(longlong *)(param_3 + lVar43 * 8) + (longlong)iVar27 * 4;
          lVar43 = lVar43 + 1;
        } while (lVar43 < (int)uVar32);
      }
      local_2da0[1] = 0;
      FUN_181798f42(local_2da0 + 2,0,0x3f8);
      lVar43 = 0;
      local_2994 = (int)uVar41;
      local_2998 = *(uint *)(param_4 + 0x400);
      uVar32 = *(uint *)(param_4 + 0x400);
      local_2990 = (longlong)local_2994 << 2;
      if (((0 < (int)uVar32) && (7 < uVar32)) && (1 < DAT_1821c7690)) {
        auVar47._4_4_ = iVar27;
        auVar47._0_4_ = iVar27;
        auVar47._8_4_ = iVar27;
        auVar47._12_4_ = iVar27;
        uVar33 = uVar32 & 0x80000007;
        if ((int)uVar33 < 0) {
          uVar33 = (uVar33 - 1 | 0xfffffff8) + 1;
        }
        auVar48 = pmovsxdq(in_XMM2,auVar47);
        lVar44 = auVar48._0_8_ * 4;
        lVar49 = auVar48._8_8_ * 4;
        plVar29 = (longlong *)(param_4 + 0x20);
        do {
          lVar42 = plVar29[-3];
          lVar43 = lVar43 + 8;
          lVar9 = plVar29[-2];
          lVar10 = plVar29[-1];
          plVar31 = plVar29 + 8;
          plVar30 = (longlong *)((longlong)alStack_2db8 + (-0x40 - param_4) + (longlong)plVar31);
          *plVar30 = plVar29[-4] + lVar44;
          plVar30[1] = lVar42 + lVar49;
          lVar42 = *plVar29;
          lVar11 = plVar29[1];
          plVar30 = (longlong *)((longlong)alStack_2db8 + (-0x30 - param_4) + (longlong)plVar31);
          *plVar30 = lVar9 + lVar44;
          plVar30[1] = lVar10 + lVar49;
          lVar9 = plVar29[2];
          lVar10 = plVar29[3];
          plVar29 = (longlong *)((longlong)alStack_2db8 + (-0x20 - param_4) + (longlong)plVar31);
          *plVar29 = lVar42 + lVar44;
          plVar29[1] = lVar11 + lVar49;
          plVar29 = (longlong *)((longlong)alStack_2db8 + (-0x10 - param_4) + (longlong)plVar31);
          *plVar29 = lVar9 + lVar44;
          plVar29[1] = lVar10 + lVar49;
          plVar29 = plVar31;
        } while (lVar43 < (int)(uVar32 - uVar33));
      }
      if (lVar43 < (int)uVar32) {
        do {
          local_2da0[lVar43 + 1] = *(longlong *)(param_4 + lVar43 * 8) + (longlong)iVar27 * 4;
          lVar43 = lVar43 + 1;
        } while (lVar43 < (int)uVar32);
      }
      local_3674 = (undefined4)plVar34[3];
      local_2168[0] = 0;
      FUN_181798f42(local_2168 + 1,0);
      lVar43 = 0;
      local_1d60 = (longlong)iVar26 << 2;
      local_1d68 = uVar24;
      local_1d64 = iVar26;
      if (0 < (int)uVar24) {
        uVar32 = *(uint *)(plVar34 + 3);
        do {
          uVar33 = iVar26 + uVar32;
          local_2168[lVar43] = *plVar34 + (longlong)(int)uVar32 * 4;
          uVar32 = (uVar33 - (uVar33 & 0xf)) + 0x10;
          if ((uVar33 & 0xf) == 0) {
            uVar32 = uVar33;
          }
          lVar43 = lVar43 + 1;
          *(uint *)(plVar34 + 3) = uVar32;
        } while (lVar43 < (int)uVar24);
      }
      local_2988[0] = 0;
      FUN_181798f42(local_2988 + 1,0);
      lVar43 = 0;
      local_2580[0] = (longlong)iVar26 << 2;
      local_2588 = uVar24;
      local_2584 = iVar26;
      if (0 < (int)uVar24) {
        uVar32 = *(uint *)(plVar34 + 3);
        do {
          uVar33 = iVar26 + uVar32;
          local_2988[lVar43] = *plVar34 + (longlong)(int)uVar32 * 4;
          uVar32 = (uVar33 - (uVar33 & 0xf)) + 0x10;
          if ((uVar33 & 0xf) == 0) {
            uVar32 = uVar33;
          }
          lVar43 = lVar43 + 1;
          *(uint *)(plVar34 + 3) = uVar32;
        } while (lVar43 < (int)uVar24);
      }
      local_1d58 = 0;
      FUN_181798f42(auStack_1d50,0);
      lVar43 = 0;
      local_1958 = uVar24;
      local_1954 = iVar26;
      local_1950 = (longlong)iVar26 << 2;
      if (0 < (int)uVar24) {
        uVar32 = *(uint *)(plVar34 + 3);
        do {
          uVar33 = uVar32 + iVar26;
          *(longlong *)(auStack_1d50 + lVar43 * 8 + -8) = *plVar34 + (longlong)(int)uVar32 * 4;
          uVar32 = (uVar33 - (uVar33 & 0xf)) + 0x10;
          if ((uVar33 & 0xf) == 0) {
            uVar32 = uVar33;
          }
          lVar43 = lVar43 + 1;
          *(uint *)(plVar34 + 3) = uVar32;
        } while (lVar43 < (int)uVar24);
      }
      if (*(char *)(*(longlong *)(param_1 + 0x2c38) + 0x52) == '\0') {
        lVar43 = 8;
        plVar34 = local_1948;
        plVar29 = local_2580 + 1;
        do {
          plVar30 = plVar29;
          plVar31 = plVar34;
          lVar44 = plVar30[1];
          lVar49 = plVar30[2];
          lVar42 = plVar30[3];
          *plVar31 = *plVar30;
          plVar31[1] = lVar44;
          lVar44 = plVar30[4];
          lVar9 = plVar30[5];
          plVar31[2] = lVar49;
          plVar31[3] = lVar42;
          lVar49 = plVar30[6];
          lVar42 = plVar30[7];
          plVar31[4] = lVar44;
          plVar31[5] = lVar9;
          lVar44 = plVar30[8];
          lVar9 = plVar30[9];
          plVar31[6] = lVar49;
          plVar31[7] = lVar42;
          lVar49 = plVar30[10];
          lVar42 = plVar30[0xb];
          plVar31[8] = lVar44;
          plVar31[9] = lVar9;
          lVar44 = plVar30[0xc];
          lVar9 = plVar30[0xd];
          plVar31[10] = lVar49;
          plVar31[0xb] = lVar42;
          lVar49 = plVar30[0xe];
          lVar42 = plVar30[0xf];
          plVar31[0xc] = lVar44;
          plVar31[0xd] = lVar9;
          plVar31[0xe] = lVar49;
          plVar31[0xf] = lVar42;
          lVar43 = lVar43 + -1;
          plVar34 = plVar31 + 0x10;
          plVar29 = plVar30 + 0x10;
        } while (lVar43 != 0);
        lVar43 = plVar30[0x11];
        lVar44 = 8;
        plVar31[0x10] = plVar30[0x10];
        plVar31[0x11] = lVar43;
        plVar34 = local_1538;
        plVar29 = local_2988;
        do {
          plVar30 = plVar29;
          plVar31 = plVar34;
          lVar43 = plVar30[1];
          lVar49 = plVar30[2];
          lVar42 = plVar30[3];
          *plVar31 = *plVar30;
          plVar31[1] = lVar43;
          lVar43 = plVar30[4];
          lVar9 = plVar30[5];
          plVar31[2] = lVar49;
          plVar31[3] = lVar42;
          lVar49 = plVar30[6];
          lVar42 = plVar30[7];
          plVar31[4] = lVar43;
          plVar31[5] = lVar9;
          lVar43 = plVar30[8];
          lVar9 = plVar30[9];
          plVar31[6] = lVar49;
          plVar31[7] = lVar42;
          lVar49 = plVar30[10];
          lVar42 = plVar30[0xb];
          plVar31[8] = lVar43;
          plVar31[9] = lVar9;
          lVar43 = plVar30[0xc];
          lVar9 = plVar30[0xd];
          plVar31[10] = lVar49;
          plVar31[0xb] = lVar42;
          lVar49 = plVar30[0xe];
          lVar42 = plVar30[0xf];
          plVar31[0xc] = lVar43;
          plVar31[0xd] = lVar9;
          plVar31[0xe] = lVar49;
          plVar31[0xf] = lVar42;
          lVar44 = lVar44 + -1;
          plVar34 = plVar31 + 0x10;
          plVar29 = plVar30 + 0x10;
        } while (lVar44 != 0);
        lVar43 = plVar30[0x11];
        iVar23 = 0;
        plVar31[0x10] = plVar30[0x10];
        plVar31[0x11] = lVar43;
        if (*(longlong *)(param_1 + 0x2be0) - *(longlong *)(param_1 + 0x2bd8) >> 3 != 0) {
          lVar44 = 0;
          lVar43 = (longlong)local_1134;
          do {
            puVar37 = *(undefined4 **)((longlong)local_1538 + lVar44);
            uVar38 = *(undefined8 *)(lVar44 + *(longlong *)(param_1 + 0x2bd8));
            if (0 < lVar43) {
              lVar49 = lVar43;
              do {
                uVar45 = FUN_1808b2680(uVar38);
                *puVar37 = uVar45;
                puVar37 = puVar37 + 1;
                lVar49 = lVar49 + -1;
              } while (lVar49 != 0);
            }
            iVar23 = iVar23 + 1;
            lVar44 = lVar44 + 8;
          } while ((ulonglong)(longlong)iVar23 <
                   (ulonglong)
                   (*(longlong *)(param_1 + 0x2be0) - *(longlong *)(param_1 + 0x2bd8) >> 3));
        }
        lVar43 = 8;
        plVar34 = local_d18;
        plVar29 = local_2580 + 1;
        do {
          plVar30 = plVar29;
          plVar31 = plVar34;
          lVar44 = plVar30[1];
          lVar49 = plVar30[2];
          lVar42 = plVar30[3];
          *plVar31 = *plVar30;
          plVar31[1] = lVar44;
          lVar44 = plVar30[4];
          lVar9 = plVar30[5];
          plVar31[2] = lVar49;
          plVar31[3] = lVar42;
          lVar49 = plVar30[6];
          lVar42 = plVar30[7];
          plVar31[4] = lVar44;
          plVar31[5] = lVar9;
          lVar44 = plVar30[8];
          lVar9 = plVar30[9];
          plVar31[6] = lVar49;
          plVar31[7] = lVar42;
          lVar49 = plVar30[10];
          lVar42 = plVar30[0xb];
          plVar31[8] = lVar44;
          plVar31[9] = lVar9;
          lVar44 = plVar30[0xc];
          lVar9 = plVar30[0xd];
          plVar31[10] = lVar49;
          plVar31[0xb] = lVar42;
          lVar49 = plVar30[0xe];
          lVar42 = plVar30[0xf];
          plVar31[0xc] = lVar44;
          plVar31[0xd] = lVar9;
          plVar31[0xe] = lVar49;
          plVar31[0xf] = lVar42;
          lVar43 = lVar43 + -1;
          plVar34 = plVar31 + 0x10;
          plVar29 = plVar30 + 0x10;
        } while (lVar43 != 0);
        lVar43 = plVar30[0x11];
        lVar44 = 8;
        plVar31[0x10] = plVar30[0x10];
        plVar31[0x11] = lVar43;
        plVar34 = local_1128;
        plVar29 = &local_1d58;
        do {
          plVar30 = plVar29;
          plVar31 = plVar34;
          lVar43 = plVar30[1];
          lVar49 = plVar30[2];
          lVar42 = plVar30[3];
          *plVar31 = *plVar30;
          plVar31[1] = lVar43;
          lVar43 = plVar30[4];
          lVar9 = plVar30[5];
          plVar31[2] = lVar49;
          plVar31[3] = lVar42;
          lVar49 = plVar30[6];
          lVar42 = plVar30[7];
          plVar31[4] = lVar43;
          plVar31[5] = lVar9;
          lVar43 = plVar30[8];
          lVar9 = plVar30[9];
          plVar31[6] = lVar49;
          plVar31[7] = lVar42;
          lVar49 = plVar30[10];
          lVar42 = plVar30[0xb];
          plVar31[8] = lVar43;
          plVar31[9] = lVar9;
          lVar43 = plVar30[0xc];
          lVar9 = plVar30[0xd];
          plVar31[10] = lVar49;
          plVar31[0xb] = lVar42;
          lVar49 = plVar30[0xe];
          lVar42 = plVar30[0xf];
          plVar31[0xc] = lVar43;
          plVar31[0xd] = lVar9;
          plVar31[0xe] = lVar49;
          plVar31[0xf] = lVar42;
          lVar44 = lVar44 + -1;
          plVar34 = plVar31 + 0x10;
          plVar29 = plVar30 + 0x10;
        } while (lVar44 != 0);
        lVar43 = plVar30[0x11];
        iVar23 = 0;
        plVar31[0x10] = plVar30[0x10];
        plVar31[0x11] = lVar43;
        if (*(longlong *)(param_1 + 0x2bf8) - *(longlong *)(param_1 + 0x2bf0) >> 3 != 0) {
          lVar44 = 0;
          lVar43 = (longlong)local_d24;
          do {
            puVar37 = *(undefined4 **)((longlong)local_1128 + lVar44);
            uVar38 = *(undefined8 *)(lVar44 + *(longlong *)(param_1 + 0x2bf0));
            if (0 < lVar43) {
              lVar49 = lVar43;
              do {
                uVar45 = FUN_1808b2680(uVar38);
                *puVar37 = uVar45;
                puVar37 = puVar37 + 1;
                lVar49 = lVar49 + -1;
              } while (lVar49 != 0);
            }
            iVar23 = iVar23 + 1;
            lVar44 = lVar44 + 8;
          } while ((ulonglong)(longlong)iVar23 <
                   (ulonglong)
                   (*(longlong *)(param_1 + 0x2bf8) - *(longlong *)(param_1 + 0x2bf0) >> 3));
        }
      }
      else {
        lVar43 = plVar34[3];
        local_35b8[0] = 0;
        FUN_181798f42(local_35b8 + 1,0);
        lVar44 = 0;
        local_31b8 = local_2178;
        local_31b4 = local_2174;
        local_31b0[0] = (longlong)local_2174 << 2;
        if (0 < (int)local_2178) {
          uVar32 = *(uint *)(plVar34 + 3);
          do {
            uVar24 = uVar32 + local_2174;
            local_35b8[lVar44] = *plVar34 + (longlong)(int)uVar32 * 4;
            uVar32 = (uVar24 - (uVar24 & 0xf)) + 0x10;
            if ((uVar24 & 0xf) == 0) {
              uVar32 = uVar24;
            }
            lVar44 = lVar44 + 1;
            *(uint *)(plVar34 + 3) = uVar32;
          } while (lVar44 < (int)local_2178);
        }
        lVar44 = 8;
        plVar29 = local_908;
        plVar31 = local_2580 + 1;
        do {
          plVar36 = plVar31;
          plVar30 = plVar29;
          lVar49 = plVar36[1];
          lVar42 = plVar36[2];
          lVar9 = plVar36[3];
          *plVar30 = *plVar36;
          plVar30[1] = lVar49;
          lVar49 = plVar36[4];
          lVar10 = plVar36[5];
          plVar30[2] = lVar42;
          plVar30[3] = lVar9;
          lVar42 = plVar36[6];
          lVar9 = plVar36[7];
          plVar30[4] = lVar49;
          plVar30[5] = lVar10;
          lVar49 = plVar36[8];
          lVar10 = plVar36[9];
          plVar30[6] = lVar42;
          plVar30[7] = lVar9;
          lVar42 = plVar36[10];
          lVar9 = plVar36[0xb];
          plVar30[8] = lVar49;
          plVar30[9] = lVar10;
          lVar49 = plVar36[0xc];
          lVar10 = plVar36[0xd];
          plVar30[10] = lVar42;
          plVar30[0xb] = lVar9;
          lVar42 = plVar36[0xe];
          lVar9 = plVar36[0xf];
          plVar30[0xc] = lVar49;
          plVar30[0xd] = lVar10;
          plVar30[0xe] = lVar42;
          plVar30[0xf] = lVar9;
          lVar44 = lVar44 + -1;
          plVar29 = plVar30 + 0x10;
          plVar31 = plVar36 + 0x10;
        } while (lVar44 != 0);
        lVar44 = plVar36[0x11];
        lVar49 = 8;
        plVar30[0x10] = plVar36[0x10];
        plVar30[0x11] = lVar44;
        plVar29 = local_4f8;
        plVar31 = local_35b8;
        do {
          plVar36 = plVar31;
          plVar30 = plVar29;
          lVar44 = plVar36[1];
          lVar42 = plVar36[2];
          lVar9 = plVar36[3];
          *plVar30 = *plVar36;
          plVar30[1] = lVar44;
          lVar44 = plVar36[4];
          lVar10 = plVar36[5];
          plVar30[2] = lVar42;
          plVar30[3] = lVar9;
          lVar42 = plVar36[6];
          lVar9 = plVar36[7];
          plVar30[4] = lVar44;
          plVar30[5] = lVar10;
          lVar44 = plVar36[8];
          lVar10 = plVar36[9];
          plVar30[6] = lVar42;
          plVar30[7] = lVar9;
          lVar42 = plVar36[10];
          lVar9 = plVar36[0xb];
          plVar30[8] = lVar44;
          plVar30[9] = lVar10;
          lVar44 = plVar36[0xc];
          lVar10 = plVar36[0xd];
          plVar30[10] = lVar42;
          plVar30[0xb] = lVar9;
          lVar42 = plVar36[0xe];
          lVar9 = plVar36[0xf];
          plVar30[0xc] = lVar44;
          plVar30[0xd] = lVar10;
          plVar30[0xe] = lVar42;
          plVar30[0xf] = lVar9;
          lVar49 = lVar49 + -1;
          plVar29 = plVar30 + 0x10;
          plVar31 = plVar36 + 0x10;
        } while (lVar49 != 0);
        lVar44 = plVar36[0x11];
        uVar38 = *(undefined8 *)(param_1 + 0x10);
        plVar30[0x10] = plVar36[0x10];
        plVar30[0x11] = lVar44;
        FUN_1808b35a0(local_4f8,local_908,uVar38,plVar34,1);
        lVar44 = 8;
        plVar34 = local_d18;
        plVar29 = local_35b8;
        do {
          plVar30 = plVar29;
          plVar31 = plVar34;
          lVar49 = plVar30[1];
          lVar42 = plVar30[2];
          lVar9 = plVar30[3];
          *plVar31 = *plVar30;
          plVar31[1] = lVar49;
          lVar49 = plVar30[4];
          lVar10 = plVar30[5];
          plVar31[2] = lVar42;
          plVar31[3] = lVar9;
          lVar42 = plVar30[6];
          lVar9 = plVar30[7];
          plVar31[4] = lVar49;
          plVar31[5] = lVar10;
          lVar49 = plVar30[8];
          lVar10 = plVar30[9];
          plVar31[6] = lVar42;
          plVar31[7] = lVar9;
          lVar42 = plVar30[10];
          lVar9 = plVar30[0xb];
          plVar31[8] = lVar49;
          plVar31[9] = lVar10;
          lVar49 = plVar30[0xc];
          lVar10 = plVar30[0xd];
          plVar31[10] = lVar42;
          plVar31[0xb] = lVar9;
          lVar42 = plVar30[0xe];
          lVar9 = plVar30[0xf];
          plVar31[0xc] = lVar49;
          plVar31[0xd] = lVar10;
          plVar31[0xe] = lVar42;
          plVar31[0xf] = lVar9;
          lVar44 = lVar44 + -1;
          plVar34 = plVar31 + 0x10;
          plVar29 = plVar30 + 0x10;
        } while (lVar44 != 0);
        lVar44 = plVar30[0x11];
        lVar49 = 8;
        plVar31[0x10] = plVar30[0x10];
        plVar31[0x11] = lVar44;
        plVar34 = local_1128;
        plVar29 = local_2988;
        do {
          plVar30 = plVar29;
          plVar31 = plVar34;
          lVar44 = plVar30[1];
          lVar42 = plVar30[2];
          lVar9 = plVar30[3];
          *plVar31 = *plVar30;
          plVar31[1] = lVar44;
          lVar44 = plVar30[4];
          lVar10 = plVar30[5];
          plVar31[2] = lVar42;
          plVar31[3] = lVar9;
          lVar42 = plVar30[6];
          lVar9 = plVar30[7];
          plVar31[4] = lVar44;
          plVar31[5] = lVar10;
          lVar44 = plVar30[8];
          lVar10 = plVar30[9];
          plVar31[6] = lVar42;
          plVar31[7] = lVar9;
          lVar42 = plVar30[10];
          lVar9 = plVar30[0xb];
          plVar31[8] = lVar44;
          plVar31[9] = lVar10;
          lVar44 = plVar30[0xc];
          lVar10 = plVar30[0xd];
          plVar31[10] = lVar42;
          plVar31[0xb] = lVar9;
          lVar42 = plVar30[0xe];
          lVar9 = plVar30[0xf];
          plVar31[0xc] = lVar44;
          plVar31[0xd] = lVar10;
          plVar31[0xe] = lVar42;
          plVar31[0xf] = lVar9;
          lVar49 = lVar49 + -1;
          plVar34 = plVar31 + 0x10;
          plVar29 = plVar30 + 0x10;
        } while (lVar49 != 0);
        lVar44 = plVar30[0x11];
        iVar23 = 0;
        plVar31[0x10] = plVar30[0x10];
        plVar31[0x11] = lVar44;
        if (*(longlong *)(param_1 + 0x2be0) - *(longlong *)(param_1 + 0x2bd8) >> 3 != 0) {
          lVar49 = 0;
          lVar44 = (longlong)local_d24;
          do {
            puVar37 = *(undefined4 **)((longlong)local_1128 + lVar49);
            uVar38 = *(undefined8 *)(lVar49 + *(longlong *)(param_1 + 0x2bd8));
            if (0 < lVar44) {
              lVar42 = lVar44;
              do {
                uVar45 = FUN_1808b2680(uVar38);
                *puVar37 = uVar45;
                puVar37 = puVar37 + 1;
                lVar42 = lVar42 + -1;
              } while (lVar42 != 0);
            }
            iVar23 = iVar23 + 1;
            lVar49 = lVar49 + 8;
          } while ((ulonglong)(longlong)iVar23 <
                   (ulonglong)
                   (*(longlong *)(param_1 + 0x2be0) - *(longlong *)(param_1 + 0x2bd8) >> 3));
        }
        lVar44 = 8;
        plVar34 = local_1948;
        plVar29 = local_35b8;
        do {
          plVar30 = plVar29;
          plVar31 = plVar34;
          lVar49 = plVar30[1];
          lVar42 = plVar30[2];
          lVar9 = plVar30[3];
          *plVar31 = *plVar30;
          plVar31[1] = lVar49;
          lVar49 = plVar30[4];
          lVar10 = plVar30[5];
          plVar31[2] = lVar42;
          plVar31[3] = lVar9;
          lVar42 = plVar30[6];
          lVar9 = plVar30[7];
          plVar31[4] = lVar49;
          plVar31[5] = lVar10;
          lVar49 = plVar30[8];
          lVar10 = plVar30[9];
          plVar31[6] = lVar42;
          plVar31[7] = lVar9;
          lVar42 = plVar30[10];
          lVar9 = plVar30[0xb];
          plVar31[8] = lVar49;
          plVar31[9] = lVar10;
          lVar49 = plVar30[0xc];
          lVar10 = plVar30[0xd];
          plVar31[10] = lVar42;
          plVar31[0xb] = lVar9;
          lVar42 = plVar30[0xe];
          lVar9 = plVar30[0xf];
          plVar31[0xc] = lVar49;
          plVar31[0xd] = lVar10;
          plVar31[0xe] = lVar42;
          plVar31[0xf] = lVar9;
          lVar44 = lVar44 + -1;
          plVar34 = plVar31 + 0x10;
          plVar29 = plVar30 + 0x10;
        } while (lVar44 != 0);
        lVar44 = plVar30[0x11];
        lVar49 = 8;
        plVar31[0x10] = plVar30[0x10];
        plVar31[0x11] = lVar44;
        plVar34 = local_1538;
        plVar29 = &local_1d58;
        do {
          plVar30 = plVar29;
          plVar31 = plVar34;
          lVar44 = plVar30[1];
          lVar42 = plVar30[2];
          lVar9 = plVar30[3];
          *plVar31 = *plVar30;
          plVar31[1] = lVar44;
          lVar44 = plVar30[4];
          lVar10 = plVar30[5];
          plVar31[2] = lVar42;
          plVar31[3] = lVar9;
          lVar42 = plVar30[6];
          lVar9 = plVar30[7];
          plVar31[4] = lVar44;
          plVar31[5] = lVar10;
          lVar44 = plVar30[8];
          lVar10 = plVar30[9];
          plVar31[6] = lVar42;
          plVar31[7] = lVar9;
          lVar42 = plVar30[10];
          lVar9 = plVar30[0xb];
          plVar31[8] = lVar44;
          plVar31[9] = lVar10;
          lVar44 = plVar30[0xc];
          lVar10 = plVar30[0xd];
          plVar31[10] = lVar42;
          plVar31[0xb] = lVar9;
          lVar42 = plVar30[0xe];
          lVar9 = plVar30[0xf];
          plVar31[0xc] = lVar44;
          plVar31[0xd] = lVar10;
          plVar31[0xe] = lVar42;
          plVar31[0xf] = lVar9;
          lVar49 = lVar49 + -1;
          plVar34 = plVar31 + 0x10;
          plVar29 = plVar30 + 0x10;
        } while (lVar49 != 0);
        lVar44 = plVar30[0x11];
        iVar23 = 0;
        plVar31[0x10] = plVar30[0x10];
        plVar31[0x11] = lVar44;
        if (*(longlong *)(param_1 + 0x2bf8) - *(longlong *)(param_1 + 0x2bf0) >> 3 != 0) {
          lVar49 = 0;
          lVar44 = (longlong)local_1134;
          do {
            puVar37 = *(undefined4 **)((longlong)local_1538 + lVar49);
            uVar38 = *(undefined8 *)(lVar49 + *(longlong *)(param_1 + 0x2bf0));
            if (0 < lVar44) {
              lVar42 = lVar44;
              do {
                uVar45 = FUN_1808b2680(uVar38);
                *puVar37 = uVar45;
                puVar37 = puVar37 + 1;
                lVar42 = lVar42 + -1;
              } while (lVar42 != 0);
            }
            iVar23 = iVar23 + 1;
            lVar49 = lVar49 + 8;
          } while ((ulonglong)(longlong)iVar23 <
                   (ulonglong)
                   (*(longlong *)(param_1 + 0x2bf8) - *(longlong *)(param_1 + 0x2bf0) >> 3));
        }
        *(int *)(param_7 + 3) = (int)lVar43;
      }
      plVar34 = param_7;
      lVar43 = 8;
      plVar29 = local_1538;
      plVar31 = local_2168;
      do {
        plVar36 = plVar31;
        plVar30 = plVar29;
        lVar44 = plVar36[1];
        lVar49 = plVar36[2];
        lVar42 = plVar36[3];
        *plVar30 = *plVar36;
        plVar30[1] = lVar44;
        lVar44 = plVar36[4];
        lVar9 = plVar36[5];
        plVar30[2] = lVar49;
        plVar30[3] = lVar42;
        lVar49 = plVar36[6];
        lVar42 = plVar36[7];
        plVar30[4] = lVar44;
        plVar30[5] = lVar9;
        lVar44 = plVar36[8];
        lVar9 = plVar36[9];
        plVar30[6] = lVar49;
        plVar30[7] = lVar42;
        lVar49 = plVar36[10];
        lVar42 = plVar36[0xb];
        plVar30[8] = lVar44;
        plVar30[9] = lVar9;
        lVar44 = plVar36[0xc];
        lVar9 = plVar36[0xd];
        plVar30[10] = lVar49;
        plVar30[0xb] = lVar42;
        lVar49 = plVar36[0xe];
        lVar42 = plVar36[0xf];
        plVar30[0xc] = lVar44;
        plVar30[0xd] = lVar9;
        plVar30[0xe] = lVar49;
        plVar30[0xf] = lVar42;
        lVar43 = lVar43 + -1;
        plVar29 = plVar30 + 0x10;
        plVar31 = plVar36 + 0x10;
      } while (lVar43 != 0);
      lVar43 = plVar36[0x11];
      plVar30[0x10] = plVar36[0x10];
      plVar30[0x11] = lVar43;
      iVar23 = local_1134;
      if (0 < (int)local_1d68) {
        uVar40 = (ulonglong)local_1d68;
        plVar29 = local_1538;
        do {
          FUN_1800010d0(*plVar29,iVar23);
          plVar29 = plVar29 + 1;
          uVar40 = uVar40 - 1;
        } while (uVar40 != 0);
      }
      FUN_1808982c0(param_1 + 0x2c08,&local_3698);
      in_XMM2._4_4_ = uStack_3694;
      in_XMM2._0_4_ = local_3698;
      in_XMM2._8_8_ = lStack_3690;
      local_35f8 = (undefined4)local_3688;
      uStack_35f4 = local_3688._4_4_;
      uStack_35ec = uStack_3680._4_4_;
      uStack_35f0 = *(int *)(lStack_3690 + 0x10) - 1U & *(int *)(param_1 + 0x60) + (int)uStack_3680;
      lVar43 = 8;
      uStack_3650 = CONCAT44(uStack_3680._4_4_,uStack_35f0);
      local_3658 = local_3688;
      plVar29 = local_1948;
      plVar31 = local_2988;
      do {
        plVar36 = plVar31;
        plVar30 = plVar29;
        lVar44 = plVar36[1];
        lVar49 = plVar36[2];
        lVar42 = plVar36[3];
        *plVar30 = *plVar36;
        plVar30[1] = lVar44;
        lVar44 = plVar36[4];
        lVar9 = plVar36[5];
        plVar30[2] = lVar49;
        plVar30[3] = lVar42;
        lVar49 = plVar36[6];
        lVar42 = plVar36[7];
        plVar30[4] = lVar44;
        plVar30[5] = lVar9;
        lVar44 = plVar36[8];
        lVar9 = plVar36[9];
        plVar30[6] = lVar49;
        plVar30[7] = lVar42;
        lVar49 = plVar36[10];
        lVar42 = plVar36[0xb];
        plVar30[8] = lVar44;
        plVar30[9] = lVar9;
        lVar44 = plVar36[0xc];
        lVar9 = plVar36[0xd];
        plVar30[10] = lVar49;
        plVar30[0xb] = lVar42;
        lVar49 = plVar36[0xe];
        lVar42 = plVar36[0xf];
        plVar30[0xc] = lVar44;
        plVar30[0xd] = lVar9;
        plVar30[0xe] = lVar49;
        plVar30[0xf] = lVar42;
        lVar43 = lVar43 + -1;
        plVar29 = plVar30 + 0x10;
        plVar31 = plVar36 + 0x10;
      } while (lVar43 != 0);
      lVar43 = plVar36[0x11];
      lVar44 = 8;
      plVar30[0x10] = plVar36[0x10];
      plVar30[0x11] = lVar43;
      plVar29 = local_d18;
      plVar31 = local_2168;
      do {
        plVar36 = plVar31;
        plVar30 = plVar29;
        lVar43 = plVar36[1];
        lVar49 = plVar36[2];
        lVar42 = plVar36[3];
        *plVar30 = *plVar36;
        plVar30[1] = lVar43;
        lVar43 = plVar36[4];
        lVar9 = plVar36[5];
        plVar30[2] = lVar49;
        plVar30[3] = lVar42;
        lVar49 = plVar36[6];
        lVar42 = plVar36[7];
        plVar30[4] = lVar43;
        plVar30[5] = lVar9;
        lVar43 = plVar36[8];
        lVar9 = plVar36[9];
        plVar30[6] = lVar49;
        plVar30[7] = lVar42;
        lVar49 = plVar36[10];
        lVar42 = plVar36[0xb];
        plVar30[8] = lVar43;
        plVar30[9] = lVar9;
        lVar43 = plVar36[0xc];
        lVar9 = plVar36[0xd];
        plVar30[10] = lVar49;
        plVar30[0xb] = lVar42;
        lVar49 = plVar36[0xe];
        lVar42 = plVar36[0xf];
        plVar30[0xc] = lVar43;
        plVar30[0xd] = lVar9;
        plVar30[0xe] = lVar49;
        plVar30[0xf] = lVar42;
        lVar44 = lVar44 + -1;
        plVar29 = plVar30 + 0x10;
        plVar31 = plVar36 + 0x10;
      } while (lVar44 != 0);
      lVar43 = plVar36[0x11];
      plVar30[0x10] = plVar36[0x10];
      plVar30[0x11] = lVar43;
      local_3668 = in_XMM2;
      FUN_1808a24b0(local_d18,local_1948,local_3668);
      FUN_1808982c0(param_1 + 0x2c08,local_3668);
      lVar43 = 8;
      local_3698 = local_3668._0_4_;
      uStack_3694 = local_3668._4_4_;
      lStack_3690 = local_3668._8_8_;
      local_3688 = local_3658;
      uStack_3680 = uStack_3650;
      plVar29 = local_1948;
      plVar31 = &local_1d58;
      do {
        plVar36 = plVar31;
        plVar30 = plVar29;
        lVar44 = plVar36[1];
        lVar49 = plVar36[2];
        lVar42 = plVar36[3];
        *plVar30 = *plVar36;
        plVar30[1] = lVar44;
        lVar44 = plVar36[4];
        lVar9 = plVar36[5];
        plVar30[2] = lVar49;
        plVar30[3] = lVar42;
        lVar49 = plVar36[6];
        lVar42 = plVar36[7];
        plVar30[4] = lVar44;
        plVar30[5] = lVar9;
        lVar44 = plVar36[8];
        lVar9 = plVar36[9];
        plVar30[6] = lVar49;
        plVar30[7] = lVar42;
        lVar49 = plVar36[10];
        lVar42 = plVar36[0xb];
        plVar30[8] = lVar44;
        plVar30[9] = lVar9;
        lVar44 = plVar36[0xc];
        lVar9 = plVar36[0xd];
        plVar30[10] = lVar49;
        plVar30[0xb] = lVar42;
        lVar49 = plVar36[0xe];
        lVar42 = plVar36[0xf];
        plVar30[0xc] = lVar44;
        plVar30[0xd] = lVar9;
        plVar30[0xe] = lVar49;
        plVar30[0xf] = lVar42;
        lVar43 = lVar43 + -1;
        plVar29 = plVar30 + 0x10;
        plVar31 = plVar36 + 0x10;
      } while (lVar43 != 0);
      lVar43 = plVar36[0x11];
      lVar44 = 8;
      plVar30[0x10] = plVar36[0x10];
      plVar30[0x11] = lVar43;
      plVar29 = local_d18;
      plVar31 = local_2168;
      do {
        plVar36 = plVar31;
        plVar30 = plVar29;
        lVar43 = plVar36[1];
        lVar49 = plVar36[2];
        lVar42 = plVar36[3];
        *plVar30 = *plVar36;
        plVar30[1] = lVar43;
        lVar43 = plVar36[4];
        lVar9 = plVar36[5];
        plVar30[2] = lVar49;
        plVar30[3] = lVar42;
        lVar49 = plVar36[6];
        lVar42 = plVar36[7];
        plVar30[4] = lVar43;
        plVar30[5] = lVar9;
        lVar43 = plVar36[8];
        lVar9 = plVar36[9];
        plVar30[6] = lVar49;
        plVar30[7] = lVar42;
        lVar49 = plVar36[10];
        lVar42 = plVar36[0xb];
        plVar30[8] = lVar43;
        plVar30[9] = lVar9;
        lVar43 = plVar36[0xc];
        lVar9 = plVar36[0xd];
        plVar30[10] = lVar49;
        plVar30[0xb] = lVar42;
        lVar49 = plVar36[0xe];
        lVar42 = plVar36[0xf];
        plVar30[0xc] = lVar43;
        plVar30[0xd] = lVar9;
        plVar30[0xe] = lVar49;
        plVar30[0xf] = lVar42;
        lVar44 = lVar44 + -1;
        plVar29 = plVar30 + 0x10;
        plVar31 = plVar36 + 0x10;
      } while (lVar44 != 0);
      lVar43 = plVar36[0x11];
      plVar30[0x10] = plVar36[0x10];
      plVar30[0x11] = lVar43;
      FUN_1808a24b0(local_d18,local_1948,&local_3698);
      FUN_1808982c0(param_1 + 0x2c08,local_3668);
      *(uint *)(local_3668._8_8_ + 0xc) =
           *(int *)(local_3668._8_8_ + 0xc) + (int)local_3670 &
           *(int *)(local_3668._8_8_ + 0x10) - 1U;
      if (*(char *)(*(longlong *)(param_1 + 0x2c38) + 0x52) != '\0') {
        lVar43 = 8;
        plVar29 = local_1948;
        plVar31 = local_2168;
        do {
          plVar36 = plVar31;
          plVar30 = plVar29;
          lVar44 = plVar36[1];
          lVar49 = plVar36[2];
          lVar42 = plVar36[3];
          *plVar30 = *plVar36;
          plVar30[1] = lVar44;
          lVar44 = plVar36[4];
          lVar9 = plVar36[5];
          plVar30[2] = lVar49;
          plVar30[3] = lVar42;
          lVar49 = plVar36[6];
          lVar42 = plVar36[7];
          plVar30[4] = lVar44;
          plVar30[5] = lVar9;
          lVar44 = plVar36[8];
          lVar9 = plVar36[9];
          plVar30[6] = lVar49;
          plVar30[7] = lVar42;
          lVar49 = plVar36[10];
          lVar42 = plVar36[0xb];
          plVar30[8] = lVar44;
          plVar30[9] = lVar9;
          lVar44 = plVar36[0xc];
          lVar9 = plVar36[0xd];
          plVar30[10] = lVar49;
          plVar30[0xb] = lVar42;
          lVar49 = plVar36[0xe];
          lVar42 = plVar36[0xf];
          plVar30[0xc] = lVar44;
          plVar30[0xd] = lVar9;
          plVar30[0xe] = lVar49;
          plVar30[0xf] = lVar42;
          lVar43 = lVar43 + -1;
          plVar29 = plVar30 + 0x10;
          plVar31 = plVar36 + 0x10;
        } while (lVar43 != 0);
        lVar43 = plVar36[0x11];
        uVar38 = *(undefined8 *)(param_1 + 0x10);
        plVar30[0x10] = plVar36[0x10];
        plVar30[0x11] = lVar43;
        FUN_1808a1ee0(local_1948,uVar38,plVar34);
      }
      lVar43 = 8;
      plVar34 = local_1128;
      plVar29 = local_2da0 + 1;
      do {
        plVar30 = plVar29;
        plVar31 = plVar34;
        lVar44 = plVar30[1];
        lVar49 = plVar30[2];
        lVar42 = plVar30[3];
        *plVar31 = *plVar30;
        plVar31[1] = lVar44;
        lVar44 = plVar30[4];
        lVar9 = plVar30[5];
        plVar31[2] = lVar49;
        plVar31[3] = lVar42;
        lVar49 = plVar30[6];
        lVar42 = plVar30[7];
        plVar31[4] = lVar44;
        plVar31[5] = lVar9;
        lVar44 = plVar30[8];
        lVar9 = plVar30[9];
        plVar31[6] = lVar49;
        plVar31[7] = lVar42;
        lVar49 = plVar30[10];
        lVar42 = plVar30[0xb];
        plVar31[8] = lVar44;
        plVar31[9] = lVar9;
        lVar44 = plVar30[0xc];
        lVar9 = plVar30[0xd];
        plVar31[10] = lVar49;
        plVar31[0xb] = lVar42;
        lVar49 = plVar30[0xe];
        lVar42 = plVar30[0xf];
        plVar31[0xc] = lVar44;
        plVar31[0xd] = lVar9;
        plVar31[0xe] = lVar49;
        plVar31[0xf] = lVar42;
        lVar43 = lVar43 + -1;
        plVar34 = plVar31 + 0x10;
        plVar29 = plVar30 + 0x10;
      } while (lVar43 != 0);
      lVar43 = plVar30[0x11];
      lVar44 = 8;
      plVar31[0x10] = plVar30[0x10];
      plVar31[0x11] = lVar43;
      plVar34 = local_1538;
      plVar29 = local_2580 + 1;
      do {
        plVar30 = plVar29;
        plVar31 = plVar34;
        lVar43 = plVar30[1];
        lVar49 = plVar30[2];
        lVar42 = plVar30[3];
        *plVar31 = *plVar30;
        plVar31[1] = lVar43;
        lVar43 = plVar30[4];
        lVar9 = plVar30[5];
        plVar31[2] = lVar49;
        plVar31[3] = lVar42;
        lVar49 = plVar30[6];
        lVar42 = plVar30[7];
        plVar31[4] = lVar43;
        plVar31[5] = lVar9;
        lVar43 = plVar30[8];
        lVar9 = plVar30[9];
        plVar31[6] = lVar49;
        plVar31[7] = lVar42;
        lVar49 = plVar30[10];
        lVar42 = plVar30[0xb];
        plVar31[8] = lVar43;
        plVar31[9] = lVar9;
        lVar43 = plVar30[0xc];
        lVar9 = plVar30[0xd];
        plVar31[10] = lVar49;
        plVar31[0xb] = lVar42;
        lVar49 = plVar30[0xe];
        lVar42 = plVar30[0xf];
        plVar31[0xc] = lVar43;
        plVar31[0xd] = lVar9;
        plVar31[0xe] = lVar49;
        plVar31[0xf] = lVar42;
        lVar44 = lVar44 + -1;
        plVar34 = plVar31 + 0x10;
        plVar29 = plVar30 + 0x10;
      } while (lVar44 != 0);
      lVar43 = plVar30[0x11];
      uVar38 = *(undefined8 *)(param_1 + 0x60);
      iVar23 = 0;
      plVar31[0x10] = plVar30[0x10];
      plVar31[0x11] = lVar43;
      local_3640 = uVar38;
      if (0 < local_2174) {
        lVar43 = param_1 + 0x1498;
        lVar44 = param_1 + 0x1528;
        local_36a0 = -(int)uVar38;
        iVar27 = local_2174;
        do {
          uVar32 = local_2178;
          local_1d58 = 0;
          iVar26 = (int)uVar38;
          if (iVar27 < (int)uVar38) {
            iVar26 = iVar27;
          }
          FUN_181798f42(auStack_1d50,0,0x3f8);
          local_1954 = iVar26;
          local_1958 = local_1138;
          local_1950 = (longlong)iVar26 << 2;
          if (0 < (int)uVar32) {
            uVar40 = (ulonglong)uVar32;
            lVar49 = 0;
            do {
              *(longlong *)(auStack_1d50 + lVar49 + -8) =
                   *(longlong *)((longlong)local_1538 + lVar49) + (longlong)iVar23 * 4;
              uVar40 = uVar40 - 1;
              lVar49 = lVar49 + 8;
            } while (uVar40 != 0);
          }
          iVar8 = local_1954;
          lVar49 = 8;
          plVar34 = local_1948;
          plVar29 = &local_1d58;
          do {
            plVar30 = plVar29;
            plVar31 = plVar34;
            lVar42 = plVar30[1];
            lVar9 = plVar30[2];
            lVar10 = plVar30[3];
            *plVar31 = *plVar30;
            plVar31[1] = lVar42;
            lVar42 = plVar30[4];
            lVar11 = plVar30[5];
            plVar31[2] = lVar9;
            plVar31[3] = lVar10;
            lVar9 = plVar30[6];
            lVar10 = plVar30[7];
            plVar31[4] = lVar42;
            plVar31[5] = lVar11;
            lVar42 = plVar30[8];
            lVar11 = plVar30[9];
            plVar31[6] = lVar9;
            plVar31[7] = lVar10;
            lVar9 = plVar30[10];
            lVar10 = plVar30[0xb];
            plVar31[8] = lVar42;
            plVar31[9] = lVar11;
            lVar42 = plVar30[0xc];
            lVar11 = plVar30[0xd];
            plVar31[10] = lVar9;
            plVar31[0xb] = lVar10;
            lVar9 = plVar30[0xe];
            lVar10 = plVar30[0xf];
            plVar31[0xc] = lVar42;
            plVar31[0xd] = lVar11;
            plVar31[0xe] = lVar9;
            plVar31[0xf] = lVar10;
            lVar49 = lVar49 + -1;
            plVar34 = plVar31 + 0x10;
            plVar29 = plVar30 + 0x10;
          } while (lVar49 != 0);
          lVar49 = plVar30[0x11];
          plVar31[0x10] = plVar30[0x10];
          plVar31[0x11] = lVar49;
          if (0 < (int)local_1958) {
            iStack_361c = local_1954 * 4;
            lVar49 = 0;
            uVar40 = (ulonglong)local_1958;
            iStack_3620 = local_1954;
            do {
              local_3628 = *(undefined8 *)((longlong)local_1948 + lVar49);
              iVar7 = *(int *)(param_1 + 0x1524);
              lStack_3530 = 0;
              local_35b8[0] = CONCAT44(local_35b8[0]._4_4_,iVar7);
              local_35b8[1] = lVar43;
              local_35b8[2] = 0;
              local_3528 = *(undefined4 *)(param_1 + 0x1518);
              local_35b8[3] = 0;
              local_35b8[4] = 0;
              local_35b8[5] = 0;
              local_35b8[6] = 0;
              local_35b8[7] = 0;
              local_35b8[8] = 0;
              local_35b8[9] = 0;
              local_35b8[10] = 0;
              local_35b8[0xb] = 0;
              local_35b8[0xc] = 0;
              local_35b8[0xd] = 0;
              local_35b8[0xe] = 0;
              local_35b8[0xf] = 0;
              local_3538 = 0;
              if (0 < iVar7) {
                    /* WARNING: Subroutine does not return */
                FUN_181798f36(local_35b8 + 2,lVar43,(longlong)iVar7 << 3);
              }
              uStack_3600 = CONCAT44(iStack_361c,iStack_3620);
              local_3688 = *(undefined8 *)((longlong)local_35b8 + lVar49 + 0x10);
              uStack_3680 = CONCAT44(uStack_3680._4_4_,*(undefined4 *)(param_1 + 0x1518));
              local_3698 = 1;
              local_3668._4_4_ = uStack_3694;
              local_3668._0_4_ = 1;
              uStack_3650 = uStack_3680;
              local_3668._8_8_ = lVar43;
              lStack_3690 = lVar43;
              local_3658 = local_3688;
              local_3608 = local_3628;
              FUN_1808b3da0(local_3668);
              lVar49 = lVar49 + 8;
              uVar40 = uVar40 - 1;
            } while (uVar40 != 0);
          }
          lStack_3530 = 0;
          local_35b8[3] = 0;
          local_35b8[4] = 0;
          local_35b8[5] = 0;
          local_35b8[6] = 0;
          local_35b8[7] = 0;
          local_35b8[8] = 0;
          local_35b8[9] = 0;
          local_35b8[10] = 0;
          local_35b8[0xb] = 0;
          local_35b8[0xc] = 0;
          local_35b8[0xd] = 0;
          local_35b8[0xe] = 0;
          local_35b8[0xf] = 0;
          local_3538 = 0;
          local_35b8[1] = lVar43;
          if (0 < (longlong)*(int *)(param_1 + 0x1524)) {
                    /* WARNING: Subroutine does not return */
            FUN_181798f36(local_35b8 + 2,lVar43,(longlong)*(int *)(param_1 + 0x1524) << 3);
          }
          local_1d58 = 0;
          *(uint *)(param_1 + 0x1518) =
               *(int *)(param_1 + 0x1518) + iVar8 & *(int *)(param_1 + 0x1520) - 1U;
          FUN_181798f42(auStack_1d50,0,0x3f8);
          local_1954 = iVar26;
          local_1950 = (longlong)iVar26 << 2;
          local_1958 = local_d28;
          if (0 < (int)local_2998) {
            uVar40 = (ulonglong)local_2998;
            lVar49 = 0;
            do {
              *(longlong *)(auStack_1d50 + lVar49 + -8) =
                   *(longlong *)((longlong)local_1128 + lVar49) + (longlong)iVar23 * 4;
              uVar40 = uVar40 - 1;
              lVar49 = lVar49 + 8;
            } while (uVar40 != 0);
          }
          iVar26 = local_1954;
          lVar49 = 8;
          plVar34 = local_1948;
          plVar29 = &local_1d58;
          do {
            plVar30 = plVar29;
            plVar31 = plVar34;
            lVar42 = plVar30[1];
            lVar9 = plVar30[2];
            lVar10 = plVar30[3];
            *plVar31 = *plVar30;
            plVar31[1] = lVar42;
            lVar42 = plVar30[4];
            lVar11 = plVar30[5];
            plVar31[2] = lVar9;
            plVar31[3] = lVar10;
            lVar9 = plVar30[6];
            lVar10 = plVar30[7];
            plVar31[4] = lVar42;
            plVar31[5] = lVar11;
            lVar42 = plVar30[8];
            lVar11 = plVar30[9];
            plVar31[6] = lVar9;
            plVar31[7] = lVar10;
            lVar9 = plVar30[10];
            lVar10 = plVar30[0xb];
            plVar31[8] = lVar42;
            plVar31[9] = lVar11;
            lVar42 = plVar30[0xc];
            lVar11 = plVar30[0xd];
            plVar31[10] = lVar9;
            plVar31[0xb] = lVar10;
            lVar9 = plVar30[0xe];
            lVar10 = plVar30[0xf];
            plVar31[0xc] = lVar42;
            plVar31[0xd] = lVar11;
            plVar31[0xe] = lVar9;
            plVar31[0xf] = lVar10;
            lVar49 = lVar49 + -1;
            plVar34 = plVar31 + 0x10;
            plVar29 = plVar30 + 0x10;
          } while (lVar49 != 0);
          lVar49 = plVar30[0x11];
          plVar31[0x10] = plVar30[0x10];
          plVar31[0x11] = lVar49;
          if (0 < (int)local_1958) {
            iStack_360c = local_1954 * 4;
            lVar49 = 0;
            uVar40 = (ulonglong)local_1958;
            iStack_3610 = local_1954;
            do {
              local_3618 = *(undefined8 *)((longlong)local_1948 + lVar49);
              iVar8 = *(int *)(param_1 + 0x15b4);
              lStack_3530 = 0;
              local_35b8[0] = CONCAT44(local_35b8[0]._4_4_,iVar8);
              local_35b8[1] = lVar44;
              local_35b8[2] = 0;
              local_3528 = *(undefined4 *)(param_1 + 0x15a8);
              local_35b8[3] = 0;
              local_35b8[4] = 0;
              local_35b8[5] = 0;
              local_35b8[6] = 0;
              local_35b8[7] = 0;
              local_35b8[8] = 0;
              local_35b8[9] = 0;
              local_35b8[10] = 0;
              local_35b8[0xb] = 0;
              local_35b8[0xc] = 0;
              local_35b8[0xd] = 0;
              local_35b8[0xe] = 0;
              local_35b8[0xf] = 0;
              local_3538 = 0;
              if (0 < iVar8) {
                    /* WARNING: Subroutine does not return */
                FUN_181798f36(local_35b8 + 2,lVar44,(longlong)iVar8 << 3);
              }
              uStack_3600 = CONCAT44(iStack_360c,iStack_3610);
              local_3688 = *(undefined8 *)((longlong)local_35b8 + lVar49 + 0x10);
              uStack_3680 = CONCAT44(uStack_3680._4_4_,*(undefined4 *)(param_1 + 0x15a8));
              local_3698 = 1;
              local_3668._4_4_ = uStack_3694;
              local_3668._0_4_ = 1;
              uStack_3650 = uStack_3680;
              local_3668._8_8_ = lVar44;
              lStack_3690 = lVar44;
              local_3658 = local_3688;
              local_3608 = local_3618;
              FUN_1808b3da0(local_3668);
              lVar49 = lVar49 + 8;
              uVar40 = uVar40 - 1;
            } while (uVar40 != 0);
          }
          uVar38 = local_3640;
          lVar49 = (longlong)*(int *)(param_1 + 0x15b4);
          lStack_3530 = 0;
          local_35b8[3] = 0;
          local_35b8[4] = 0;
          local_35b8[5] = 0;
          local_35b8[6] = 0;
          local_35b8[7] = 0;
          local_35b8[8] = 0;
          local_35b8[9] = 0;
          local_35b8[10] = 0;
          local_35b8[0xb] = 0;
          local_35b8[0xc] = 0;
          local_35b8[0xd] = 0;
          local_35b8[0xe] = 0;
          local_35b8[0xf] = 0;
          local_3538 = 0;
          local_35b8[1] = lVar44;
          if (0 < lVar49) {
                    /* WARNING: Subroutine does not return */
            FUN_181798f36(local_35b8 + 2,lVar44,lVar49 << 3);
          }
          *(uint *)(param_1 + 0x15a8) =
               *(int *)(param_1 + 0x15a8) + iVar26 & *(int *)(param_1 + 0x15b0) - 1U;
          FUN_1808ac1d0(local_3638,local_3640,lVar49,&local_35e8);
          iVar23 = iVar23 + (int)uVar38;
          iVar27 = iVar27 + local_36a0;
        } while (iVar23 < local_2174);
      }
      lVar43 = 8;
      plVar34 = local_908;
      plVar29 = local_2168;
      do {
        plVar30 = plVar29;
        plVar31 = plVar34;
        lVar44 = plVar30[1];
        lVar49 = plVar30[2];
        lVar42 = plVar30[3];
        *plVar31 = *plVar30;
        lVar10 = local_908[0];
        plVar31[1] = lVar44;
        lVar44 = plVar30[4];
        lVar9 = plVar30[5];
        plVar31[2] = lVar49;
        plVar31[3] = lVar42;
        lVar49 = plVar30[6];
        lVar42 = plVar30[7];
        plVar31[4] = lVar44;
        plVar31[5] = lVar9;
        lVar44 = plVar30[8];
        lVar9 = plVar30[9];
        plVar31[6] = lVar49;
        plVar31[7] = lVar42;
        lVar49 = plVar30[10];
        lVar42 = plVar30[0xb];
        plVar31[8] = lVar44;
        plVar31[9] = lVar9;
        lVar44 = plVar30[0xc];
        lVar9 = plVar30[0xd];
        plVar31[10] = lVar49;
        plVar31[0xb] = lVar42;
        lVar49 = plVar30[0xe];
        lVar42 = plVar30[0xf];
        plVar31[0xc] = lVar44;
        plVar31[0xd] = lVar9;
        plVar31[0xe] = lVar49;
        plVar31[0xf] = lVar42;
        lVar43 = lVar43 + -1;
        plVar34 = plVar31 + 0x10;
        plVar29 = plVar30 + 0x10;
      } while (lVar43 != 0);
      lVar43 = plVar30[0x11];
      lVar44 = 8;
      plVar31[0x10] = plVar30[0x10];
      plVar31[0x11] = lVar43;
      plVar34 = local_2988;
      plVar29 = local_31b0 + 1;
      do {
        plVar30 = plVar29;
        plVar31 = plVar34;
        lVar43 = plVar30[1];
        lVar49 = plVar30[2];
        lVar42 = plVar30[3];
        *plVar31 = *plVar30;
        plVar31[1] = lVar43;
        lVar43 = plVar30[4];
        lVar9 = plVar30[5];
        plVar31[2] = lVar49;
        plVar31[3] = lVar42;
        lVar49 = plVar30[6];
        lVar42 = plVar30[7];
        plVar31[4] = lVar43;
        plVar31[5] = lVar9;
        lVar43 = plVar30[8];
        lVar9 = plVar30[9];
        plVar31[6] = lVar49;
        plVar31[7] = lVar42;
        lVar49 = plVar30[10];
        lVar42 = plVar30[0xb];
        plVar31[8] = lVar43;
        plVar31[9] = lVar9;
        lVar43 = plVar30[0xc];
        lVar9 = plVar30[0xd];
        plVar31[10] = lVar49;
        plVar31[0xb] = lVar42;
        lVar49 = plVar30[0xe];
        lVar42 = plVar30[0xf];
        plVar31[0xc] = lVar43;
        plVar31[0xd] = lVar9;
        plVar31[0xe] = lVar49;
        plVar31[0xf] = lVar42;
        uVar32 = local_1d68;
        lVar44 = lVar44 + -1;
        plVar34 = plVar31 + 0x10;
        plVar29 = plVar30 + 0x10;
      } while (lVar44 != 0);
      lVar43 = plVar30[0x11];
      plVar31[0x10] = plVar30[0x10];
      plVar31[0x11] = lVar43;
      iVar23 = local_2584;
      uVar40 = (ulonglong)local_2da8;
      if (local_2da8 == uVar32) {
        if (0 < (int)local_2da8) {
          lVar43 = 0;
          uVar40 = (ulonglong)local_2da8;
          do {
            FUN_1800010a0(*(undefined8 *)((longlong)local_908 + lVar43),
                          *(undefined8 *)((longlong)local_2988 + lVar43),iVar23);
            lVar43 = lVar43 + 8;
            uVar40 = uVar40 - 1;
          } while (uVar40 != 0);
        }
      }
      else if ((uVar32 == 1) && (0 < (int)local_2da8)) {
        plVar34 = local_2988;
        do {
          FUN_1800010a0(lVar10,*plVar34,iVar23);
          plVar34 = plVar34 + 1;
          uVar40 = uVar40 - 1;
        } while (uVar40 != 0);
      }
      local_3648 = local_3648 + local_3670;
      *(undefined4 *)(param_7 + 3) = local_3674;
      plVar34 = param_7;
    } while (local_3648 < local_3630);
  }
  return;
}

