// FUN_18087bb60 @ 0x18087bb60

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_18087bb60(longlong param_1,longlong *param_2)

{
  undefined4 uVar1;
  undefined8 uVar2;
  longlong lVar3;
  longlong lVar4;
  longlong lVar5;
  longlong lVar6;
  longlong lVar7;
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
  uint uVar19;
  uint uVar20;
  longlong *plVar21;
  int iVar22;
  int iVar23;
  longlong *plVar24;
  ulonglong uVar25;
  longlong lVar26;
  longlong lVar27;
  longlong lVar28;
  longlong lVar29;
  ulonglong uVar30;
  uint uVar31;
  ulonglong uVar32;
  longlong lVar33;
  longlong lVar34;
  bool bVar35;
  float fVar36;
  float fVar37;
  float fVar38;
  float fVar39;
  undefined4 uVar40;
  longlong local_758 [16];
  uint local_6d8;
  uint uStack_6d4;
  longlong lStack_6d0;
  float local_6c8;
  longlong local_6b8 [16];
  uint local_638;
  uint uStack_634;
  undefined8 uStack_630;
  longlong local_628 [4];
  undefined8 local_608;
  undefined8 uStack_600;
  undefined8 local_5f8;
  undefined8 uStack_5f0;
  undefined8 local_5e8;
  undefined8 uStack_5e0;
  undefined8 local_5d8;
  undefined8 uStack_5d0;
  undefined8 local_5c8;
  undefined8 uStack_5c0;
  undefined8 local_5b8;
  undefined8 uStack_5b0;
  ulonglong local_5a8;
  longlong lStack_5a0;
  longlong local_598 [4];
  undefined8 local_578;
  undefined8 uStack_570;
  undefined8 local_568;
  undefined8 uStack_560;
  undefined8 local_558;
  undefined8 uStack_550;
  undefined8 local_548;
  undefined8 uStack_540;
  undefined8 local_538;
  undefined8 uStack_530;
  undefined8 local_528;
  undefined8 uStack_520;
  undefined8 local_518;
  longlong lStack_510;
  longlong local_508 [16];
  undefined8 local_488;
  longlong lStack_480;
  float local_478;
  undefined4 local_464;
  longlong local_458 [4];
  undefined8 local_438;
  undefined8 uStack_430;
  undefined8 local_428;
  undefined8 uStack_420;
  undefined8 local_418;
  undefined8 uStack_410;
  undefined8 local_408;
  undefined8 uStack_400;
  undefined8 local_3f8;
  undefined8 uStack_3f0;
  undefined8 local_3e8;
  undefined8 uStack_3e0;
  undefined8 local_3d8;
  longlong lStack_3d0;
  longlong local_3c8;
  longlong local_3b8 [16];
  undefined8 local_338;
  longlong lStack_330;
  longlong local_328 [16];
  uint local_2a8;
  int iStack_2a4;
  undefined8 uStack_2a0;
  longlong local_298 [16];
  uint local_218;
  int iStack_214;
  longlong lStack_210;
  longlong local_208 [4];
  undefined8 local_1e8;
  undefined8 uStack_1e0;
  undefined8 local_1d8;
  undefined8 uStack_1d0;
  undefined8 local_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  undefined8 uStack_1b0;
  undefined8 local_1a8;
  undefined8 uStack_1a0;
  undefined8 local_198;
  undefined8 uStack_190;
  uint local_188;
  uint uStack_184;
  undefined4 uStack_180;
  undefined4 uStack_17c;
  longlong local_178 [4];
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
  ulonglong local_f8;
  longlong lStack_f0;
  
  fVar38 = *(float *)(*(longlong *)(param_1 + 0x2c38) + 8);
  fVar36 = (float)FUN_181c9a9fb(DAT_18207a5b0);
  fVar39 = DAT_182079f9c;
  if (fVar38 <= 0.0) {
    fVar38 = 0.0;
  }
  if (DAT_182079f9c <= fVar38) {
    fVar38 = DAT_182079f9c;
  }
  local_6c8 = (float)FUN_181c9a9d7((fVar36 - _DAT_18207a1c0) * fVar38 + _DAT_18207a1c0);
  local_6c8 = local_6c8 - DAT_18207a350;
  fVar38 = *(float *)(*(longlong *)(param_1 + 0x2c38) + 0xc);
  fVar36 = (float)FUN_181c9a9fb(DAT_18207a418);
  fVar37 = (float)FUN_181c9a9fb(DAT_18207a5ac);
  if (fVar38 <= 0.0) {
    fVar38 = 0.0;
  }
  if (fVar39 <= fVar38) {
    fVar38 = fVar39;
  }
  fVar38 = (float)FUN_181c9a9d7((fVar37 - fVar36) * fVar38 + fVar36);
  local_3d8._0_4_ = *(int *)(param_1 + 0x7c8);
  lVar26 = 0;
  local_3d8._4_4_ = *(int *)(param_1 + 2000);
  iVar22 = 0;
  local_464 = (int)param_2[3];
  local_478 = fVar38 - DAT_18207a248;
  if (0 < (int)(uint)local_3d8) {
    plVar21 = local_458;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0x748) - (longlong)local_458) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)(uint)local_3d8);
  }
  local_3b8[0] = 0;
  local_3b8[0xf] = 0;
  lVar27 = 0;
  local_338 = CONCAT44(local_3d8._4_4_,(uint)local_3d8);
  lStack_330 = (longlong)local_3d8._4_4_ << 2;
  local_3b8[1] = 0;
  local_3b8[2] = 0;
  local_3b8[3] = 0;
  local_3b8[4] = 0;
  local_3b8[5] = 0;
  local_3b8[6] = 0;
  local_3b8[7] = 0;
  local_3b8[8] = 0;
  local_3b8[9] = 0;
  local_3b8[10] = 0;
  local_3b8[0xb] = 0;
  local_3b8[0xc] = 0;
  local_3b8[0xd] = 0;
  local_3b8[0xe] = 0;
  if (0 < (int)(uint)local_3d8) {
    uVar31 = *(uint *)(param_2 + 3);
    do {
      uVar19 = uVar31 + local_3d8._4_4_;
      local_3b8[lVar27] = *param_2 + (longlong)(int)uVar31 * 4;
      uVar31 = (uVar19 - (uVar19 & 0xf)) + 0x10;
      if ((uVar19 & 0xf) == 0) {
        uVar31 = uVar19;
      }
      lVar27 = lVar27 + 1;
      *(uint *)(param_2 + 3) = uVar31;
    } while (lVar27 < (int)(uint)local_3d8);
  }
  iVar22 = 0;
  local_3d8._0_4_ = *(uint *)(param_1 + 0x7c8);
  local_3d8._4_4_ = *(int *)(param_1 + 2000);
  if (0 < (int)*(uint *)(param_1 + 0x7c8)) {
    plVar21 = local_458;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0x748) - (longlong)local_458) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)(uint)local_3d8);
  }
  local_298[0] = 0;
  local_298[0xf] = 0;
  lVar27 = 0;
  lStack_210 = (longlong)local_3d8._4_4_ << 2;
  local_298[1] = 0;
  local_298[2] = 0;
  local_298[3] = 0;
  local_298[4] = 0;
  local_298[5] = 0;
  local_298[6] = 0;
  local_298[7] = 0;
  local_298[8] = 0;
  local_298[9] = 0;
  local_298[10] = 0;
  local_298[0xb] = 0;
  local_298[0xc] = 0;
  local_298[0xd] = 0;
  local_298[0xe] = 0;
  local_218 = (uint)local_3d8;
  iStack_214 = local_3d8._4_4_;
  if (0 < (int)(uint)local_3d8) {
    uVar31 = *(uint *)(param_2 + 3);
    do {
      uVar19 = uVar31 + local_3d8._4_4_;
      local_298[lVar27] = *param_2 + (longlong)(int)uVar31 * 4;
      uVar31 = (uVar19 - (uVar19 & 0xf)) + 0x10;
      if ((uVar19 & 0xf) == 0) {
        uVar31 = uVar19;
      }
      lVar27 = lVar27 + 1;
      *(uint *)(param_2 + 3) = uVar31;
    } while (lVar27 < (int)(uint)local_3d8);
  }
  local_628[0] = local_3b8[0];
  local_628[1] = local_3b8[1];
  local_608 = local_3b8[4];
  uStack_600 = local_3b8[5];
  local_628[2] = local_3b8[2];
  local_628[3] = local_3b8[3];
  local_5e8 = local_3b8[8];
  uStack_5e0 = local_3b8[9];
  local_5f8 = local_3b8[6];
  uStack_5f0 = local_3b8[7];
  local_5c8 = local_3b8[0xc];
  uStack_5c0 = local_3b8[0xd];
  local_5d8 = local_3b8[10];
  uStack_5d0 = local_3b8[0xb];
  local_5a8 = local_338;
  lStack_5a0 = lStack_330;
  local_5b8 = local_3b8[0xe];
  uStack_5b0 = local_3b8[0xf];
  FUN_18087a7a0(local_628);
  local_758[0] = local_298[0];
  local_758[1] = local_298[1];
  local_758[4] = local_298[4];
  local_758[5] = local_298[5];
  local_758[2] = local_298[2];
  local_758[3] = local_298[3];
  local_758[8] = local_298[8];
  local_758[9] = local_298[9];
  local_758[6] = local_298[6];
  local_758[7] = local_298[7];
  local_758[0xc] = local_298[0xc];
  local_758[0xd] = local_298[0xd];
  local_758[10] = local_298[10];
  local_758[0xb] = local_298[0xb];
  local_6d8 = local_218;
  uStack_6d4 = iStack_214;
  lStack_6d0 = lStack_210;
  local_758[0xe] = local_298[0xe];
  local_758[0xf] = local_298[0xf];
  FUN_18087a7a0(local_758);
  iVar22 = 0;
  local_3d8._0_4_ = *(int *)(param_1 + 0x7c8);
  local_3d8._4_4_ = *(int *)(param_1 + 2000);
  if (0 < *(int *)(param_1 + 0x7c8)) {
    plVar21 = local_458;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0x748) - (longlong)local_458) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)(uint)local_3d8);
  }
  iVar22 = local_3d8._4_4_;
  local_6b8[0] = 0;
  local_638 = (uint)local_3d8;
  local_6b8[0xf] = 0;
  lVar27 = 0;
  uStack_634 = local_3d8._4_4_;
  uStack_630 = (longlong)local_3d8._4_4_ << 2;
  lVar29 = (longlong)(int)(uint)local_3d8;
  local_6b8[1] = 0;
  local_6b8[2] = 0;
  local_6b8[3] = 0;
  local_6b8[4] = 0;
  local_6b8[5] = 0;
  local_6b8[6] = 0;
  local_6b8[7] = 0;
  local_6b8[8] = 0;
  local_6b8[9] = 0;
  local_6b8[10] = 0;
  local_6b8[0xb] = 0;
  local_6b8[0xc] = 0;
  local_6b8[0xd] = 0;
  local_6b8[0xe] = 0;
  if (0 < (int)(uint)local_3d8) {
    uVar31 = *(uint *)(param_2 + 3);
    do {
      uVar19 = uVar31 + iVar22;
      local_6b8[lVar27] = *param_2 + (longlong)(int)uVar31 * 4;
      uVar31 = (uVar19 - (uVar19 & 0xf)) + 0x10;
      if ((uVar19 & 0xf) == 0) {
        uVar31 = uVar19;
      }
      lVar27 = lVar27 + 1;
      *(uint *)(param_2 + 3) = uVar31;
    } while (lVar27 < lVar29);
  }
  iVar22 = 0;
  uVar40 = *(undefined4 *)(*(longlong *)(param_1 + 0x2c38) + 0x1c);
  uVar1 = *(undefined4 *)(*(longlong *)(param_1 + 0x2c38) + 0x18);
  uStack_6d4 = *(int *)(param_1 + 2000);
  local_758[0] = 0;
  local_758[0xf] = 0;
  local_6d8 = *(int *)(param_1 + 0x7c8);
  lStack_6d0 = (longlong)*(int *)(param_1 + 2000) << 2;
  local_758[1] = 0;
  local_758[2] = 0;
  local_758[3] = 0;
  local_758[4] = 0;
  local_758[5] = 0;
  local_758[6] = 0;
  local_758[7] = 0;
  local_758[8] = 0;
  local_758[9] = 0;
  local_758[10] = 0;
  local_758[0xb] = 0;
  local_758[0xc] = 0;
  local_758[0xd] = 0;
  local_758[0xe] = 0;
  if (0 < *(int *)(param_1 + 0x7c8)) {
    plVar21 = local_758;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0x748) - (longlong)local_758) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)local_6d8);
  }
  local_628[0] = local_758[0];
  local_628[1] = local_758[1];
  local_628[2] = local_758[2];
  local_628[3] = local_758[3];
  local_608 = local_758[4];
  uStack_600 = local_758[5];
  local_5f8 = local_758[6];
  uStack_5f0 = local_758[7];
  local_5e8 = local_758[8];
  uStack_5e0 = local_758[9];
  local_5d8 = local_758[10];
  uStack_5d0 = local_758[0xb];
  local_5c8 = local_758[0xc];
  uStack_5c0 = local_758[0xd];
  local_5a8 = CONCAT44(uStack_6d4,local_6d8);
  local_5b8 = local_758[0xe];
  uStack_5b0 = local_758[0xf];
  lStack_5a0 = lStack_6d0;
  local_598[0] = local_6b8[0];
  local_598[1] = local_6b8[1];
  local_598[2] = local_6b8[2];
  local_598[3] = local_6b8[3];
  local_578 = local_6b8[4];
  uStack_570 = local_6b8[5];
  local_568 = local_6b8[6];
  uStack_560 = local_6b8[7];
  local_558 = local_6b8[8];
  uStack_550 = local_6b8[9];
  local_548 = local_6b8[10];
  uStack_540 = local_6b8[0xb];
  local_538 = local_6b8[0xc];
  uStack_530 = local_6b8[0xd];
  local_518 = CONCAT44(uStack_634,local_638);
  local_528 = local_6b8[0xe];
  uStack_520 = local_6b8[0xf];
  lStack_510 = uStack_630;
  FUN_180882fc0(local_598,local_628,uVar1,uVar40,param_2);
  iVar22 = 0;
  local_3d8._0_4_ = *(int *)(param_1 + 0x7c8);
  local_3d8._4_4_ = *(int *)(param_1 + 2000);
  if (0 < *(int *)(param_1 + 0x7c8)) {
    plVar21 = local_458;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0x748) - (longlong)local_458) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)(uint)local_3d8);
  }
  iVar22 = local_3d8._4_4_;
  local_508[0] = 0;
  local_508[0xf] = 0;
  lVar27 = 0;
  local_488 = CONCAT44(local_3d8._4_4_,(uint)local_3d8);
  lStack_480 = (longlong)local_3d8._4_4_ << 2;
  lVar29 = (longlong)(int)(uint)local_3d8;
  local_508[1] = 0;
  local_508[2] = 0;
  local_508[3] = 0;
  local_508[4] = 0;
  local_508[5] = 0;
  local_508[6] = 0;
  local_508[7] = 0;
  local_508[8] = 0;
  local_508[9] = 0;
  local_508[10] = 0;
  local_508[0xb] = 0;
  local_508[0xc] = 0;
  local_508[0xd] = 0;
  local_508[0xe] = 0;
  if (0 < (int)(uint)local_3d8) {
    uVar31 = *(uint *)(param_2 + 3);
    do {
      uVar19 = uVar31 + iVar22;
      local_508[lVar27] = *param_2 + (longlong)(int)uVar31 * 4;
      uVar31 = (uVar19 - (uVar19 & 0xf)) + 0x10;
      if ((uVar19 & 0xf) == 0) {
        uVar31 = uVar19;
      }
      lVar27 = lVar27 + 1;
      *(uint *)(param_2 + 3) = uVar31;
    } while (lVar27 < lVar29);
  }
  iVar22 = 0;
  uVar40 = *(undefined4 *)(*(longlong *)(param_1 + 0x2c38) + 0x24);
  uVar1 = *(undefined4 *)(*(longlong *)(param_1 + 0x2c38) + 0x20);
  uStack_6d4 = *(int *)(param_1 + 2000);
  local_758[0] = 0;
  local_758[0xf] = 0;
  local_6d8 = *(int *)(param_1 + 0x7c8);
  lStack_6d0 = (longlong)*(int *)(param_1 + 2000) << 2;
  local_758[1] = 0;
  local_758[2] = 0;
  local_758[3] = 0;
  local_758[4] = 0;
  local_758[5] = 0;
  local_758[6] = 0;
  local_758[7] = 0;
  local_758[8] = 0;
  local_758[9] = 0;
  local_758[10] = 0;
  local_758[0xb] = 0;
  local_758[0xc] = 0;
  local_758[0xd] = 0;
  local_758[0xe] = 0;
  if (0 < *(int *)(param_1 + 0x7c8)) {
    plVar21 = local_758;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0x748) - (longlong)local_758) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)local_6d8);
  }
  lVar34 = lStack_480;
  uVar2 = local_488;
  lVar16 = local_508[0xf];
  lVar15 = local_508[0xe];
  lVar14 = local_508[0xd];
  lVar13 = local_508[0xc];
  lVar12 = local_508[0xb];
  lVar11 = local_508[10];
  lVar10 = local_508[9];
  lVar9 = local_508[8];
  lVar8 = local_508[7];
  lVar7 = local_508[6];
  lVar6 = local_508[5];
  lVar5 = local_508[4];
  lVar4 = local_508[3];
  lVar3 = local_508[2];
  lVar28 = local_508[1];
  lVar29 = local_508[0];
  uVar31 = (uint)local_488;
  local_598[0] = local_758[0];
  local_598[1] = local_758[1];
  local_598[2] = local_758[2];
  local_598[3] = local_758[3];
  local_578 = local_758[4];
  uStack_570 = local_758[5];
  local_568 = local_758[6];
  uStack_560 = local_758[7];
  local_558 = local_758[8];
  uStack_550 = local_758[9];
  local_548 = local_758[10];
  uStack_540 = local_758[0xb];
  local_538 = local_758[0xc];
  uStack_530 = local_758[0xd];
  local_518 = CONCAT44(uStack_6d4,local_6d8);
  lStack_510 = lStack_6d0;
  local_528 = local_758[0xe];
  uStack_520 = local_758[0xf];
  local_628[0] = local_508[0];
  local_628[1] = local_508[1];
  local_628[2] = local_508[2];
  local_628[3] = local_508[3];
  local_608 = local_508[4];
  uStack_600 = local_508[5];
  local_5f8 = local_508[6];
  uStack_5f0 = local_508[7];
  local_5e8 = local_508[8];
  uStack_5e0 = local_508[9];
  local_5d8 = local_508[10];
  uStack_5d0 = local_508[0xb];
  local_5c8 = local_508[0xc];
  uStack_5c0 = local_508[0xd];
  local_5b8 = local_508[0xe];
  uStack_5b0 = local_508[0xf];
  local_5a8 = local_488;
  lStack_5a0 = lStack_480;
  plVar21 = param_2;
  FUN_180882fc0(local_628,local_598,uVar1,uVar40,param_2);
  lVar27 = local_6b8[0];
  local_598[0] = local_6b8[0];
  local_598[1] = local_6b8[1];
  local_578 = local_6b8[4];
  uStack_570 = local_6b8[5];
  local_598[2] = local_6b8[2];
  local_598[3] = local_6b8[3];
  local_558 = local_6b8[8];
  uStack_550 = local_6b8[9];
  local_568 = local_6b8[6];
  uStack_560 = local_6b8[7];
  local_538 = local_6b8[0xc];
  uStack_530 = local_6b8[0xd];
  local_548 = local_6b8[10];
  uStack_540 = local_6b8[0xb];
  local_758[0] = local_3b8[0];
  local_758[1] = local_3b8[1];
  local_528 = local_6b8[0xe];
  uStack_520 = local_6b8[0xf];
  local_758[4] = local_3b8[4];
  local_758[5] = local_3b8[5];
  local_758[2] = local_3b8[2];
  local_758[3] = local_3b8[3];
  local_758[8] = local_3b8[8];
  local_758[9] = local_3b8[9];
  local_758[6] = local_3b8[6];
  local_758[7] = local_3b8[7];
  local_758[0xc] = local_3b8[0xc];
  local_758[0xd] = local_3b8[0xd];
  uVar40 = local_338._4_4_;
  uVar32 = local_338 & 0xffffffff;
  local_758[10] = local_3b8[10];
  local_758[0xb] = local_3b8[0xb];
  local_518 = CONCAT44(uStack_634,local_638);
  lStack_510 = uStack_630;
  local_758[0xe] = local_3b8[0xe];
  local_758[0xf] = local_3b8[0xf];
  local_6d8 = (uint)local_338;
  uStack_6d4 = local_338._4_4_;
  lStack_6d0 = lStack_330;
  if ((uint)local_338 == local_638) {
    if (0 < (int)(uint)local_338) {
      lVar27 = 0;
      do {
        FUN_180001340(*(undefined8 *)((longlong)local_598 + lVar27),
                      *(undefined8 *)((longlong)local_758 + lVar27),uVar40);
        lVar27 = lVar27 + 8;
        uVar32 = uVar32 - 1;
      } while (uVar32 != 0);
    }
  }
  else if ((local_638 == 1) && (0 < (int)(uint)local_338)) {
    plVar24 = local_758;
    do {
      FUN_180001340(lVar27,*plVar24,uVar40);
      plVar24 = plVar24 + 1;
      uVar32 = uVar32 - 1;
    } while (uVar32 != 0);
  }
  iVar22 = iStack_214;
  lVar27 = local_508[0];
  uVar40 = (undefined4)((ulonglong)plVar21 >> 0x20);
  local_6b8[0] = local_298[0];
  local_6b8[1] = local_298[1];
  local_6b8[4] = local_298[4];
  local_6b8[5] = local_298[5];
  local_6b8[2] = local_298[2];
  local_6b8[3] = local_298[3];
  local_6b8[8] = local_298[8];
  local_6b8[9] = local_298[9];
  local_6b8[6] = local_298[6];
  local_6b8[7] = local_298[7];
  local_6b8[0xc] = local_298[0xc];
  local_6b8[0xd] = local_298[0xd];
  uVar32 = (ulonglong)local_218;
  local_6b8[10] = local_298[10];
  local_6b8[0xb] = local_298[0xb];
  local_628[0] = lVar29;
  local_628[1] = lVar28;
  local_628[2] = lVar3;
  local_628[3] = lVar4;
  local_608 = lVar5;
  uStack_600 = lVar6;
  local_5f8 = lVar7;
  uStack_5f0 = lVar8;
  local_5e8 = lVar9;
  uStack_5e0 = lVar10;
  local_5d8 = lVar11;
  uStack_5d0 = lVar12;
  local_5c8 = lVar13;
  uStack_5c0 = lVar14;
  local_5b8 = lVar15;
  uStack_5b0 = lVar16;
  local_5a8 = uVar2;
  lStack_5a0 = lVar34;
  local_6b8[0xe] = local_298[0xe];
  local_6b8[0xf] = local_298[0xf];
  local_638 = local_218;
  uStack_634 = iStack_214;
  uStack_630 = lStack_210;
  if (local_218 == uVar31) {
    if (0 < (int)local_218) {
      lVar27 = 0;
      do {
        FUN_180001340(*(undefined8 *)((longlong)local_628 + lVar27),
                      *(undefined8 *)((longlong)local_6b8 + lVar27),iVar22);
        uVar40 = (undefined4)((ulonglong)plVar21 >> 0x20);
        lVar27 = lVar27 + 8;
        uVar32 = uVar32 - 1;
      } while (uVar32 != 0);
    }
  }
  else if ((uVar31 == 1) && (0 < (int)local_218)) {
    plVar24 = local_6b8;
    do {
      FUN_180001340(lVar27,*plVar24,iVar22);
      uVar40 = (undefined4)((ulonglong)plVar21 >> 0x20);
      plVar24 = plVar24 + 1;
      uVar32 = uVar32 - 1;
    } while (uVar32 != 0);
  }
  iVar22 = 0;
  bVar35 = *(int *)(*(longlong *)(param_1 + 0x2c38) + 0xb0) != 1;
  local_3d8._0_4_ = *(uint *)(param_1 + 0x7c8);
  local_3d8._4_4_ = *(int *)(param_1 + 2000);
  if (0 < (int)*(uint *)(param_1 + 0x7c8)) {
    plVar21 = local_458;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0x748) - (longlong)local_458) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)(uint)local_3d8);
  }
  local_328[0] = 0;
  local_2a8 = (uint)local_3d8;
  local_328[0xf] = 0;
  lVar27 = 0;
  iStack_2a4 = local_3d8._4_4_;
  uStack_2a0 = (longlong)local_3d8._4_4_ << 2;
  lVar29 = (longlong)(int)(uint)local_3d8;
  local_328[1] = 0;
  local_328[2] = 0;
  local_328[3] = 0;
  local_328[4] = 0;
  local_328[5] = 0;
  local_328[6] = 0;
  local_328[7] = 0;
  local_328[8] = 0;
  local_328[9] = 0;
  local_328[10] = 0;
  local_328[0xb] = 0;
  local_328[0xc] = 0;
  local_328[0xd] = 0;
  local_328[0xe] = 0;
  if (0 < (int)(uint)local_3d8) {
    uVar31 = *(uint *)(param_2 + 3);
    do {
      uVar19 = uVar31 + local_3d8._4_4_;
      local_328[lVar27] = *param_2 + (longlong)(int)uVar31 * 4;
      uVar31 = (uVar19 - (uVar19 & 0xf)) + 0x10;
      if ((uVar19 & 0xf) == 0) {
        uVar31 = uVar19;
      }
      lVar27 = lVar27 + 1;
      *(uint *)(param_2 + 3) = uVar31;
    } while (lVar27 < lVar29);
  }
  iVar22 = iStack_2a4;
  uVar31 = local_2a8;
  fVar38 = DAT_18207a188;
  uVar32 = (ulonglong)local_2a8;
  lVar27 = param_1 + 0x748;
  local_6d8 = *(int *)(param_1 + 0x7c8);
  iVar23 = 0;
  uStack_6d4 = *(int *)(param_1 + 2000);
  local_758[0] = 0;
  local_758[0xf] = 0;
  lStack_6d0 = (longlong)*(int *)(param_1 + 2000) << 2;
  local_758[1] = 0;
  local_758[2] = 0;
  local_758[3] = 0;
  local_758[4] = 0;
  local_758[5] = 0;
  local_758[6] = 0;
  local_758[7] = 0;
  local_758[8] = 0;
  local_758[9] = 0;
  local_758[10] = 0;
  local_758[0xb] = 0;
  local_758[0xc] = 0;
  local_758[0xd] = 0;
  local_758[0xe] = 0;
  if (bVar35) {
    if (0 < (int)local_6d8) {
      lVar27 = lVar27 - (longlong)local_758;
      plVar21 = local_758;
      do {
        iVar23 = iVar23 + 1;
        *plVar21 = *(longlong *)(lVar27 + (longlong)plVar21);
        plVar21 = plVar21 + 1;
      } while (iVar23 < (int)local_6d8);
    }
    local_598[0] = local_758[0];
    local_598[1] = local_758[1];
    local_598[2] = local_758[2];
    local_598[3] = local_758[3];
    local_578 = local_758[4];
    uStack_570 = local_758[5];
    local_568 = local_758[6];
    uStack_560 = local_758[7];
    local_558 = local_758[8];
    uStack_550 = local_758[9];
    local_548 = local_758[10];
    uStack_540 = local_758[0xb];
    local_538 = local_758[0xc];
    uStack_530 = local_758[0xd];
    local_518 = CONCAT44(uStack_6d4,local_6d8);
    local_528 = local_758[0xe];
    uStack_520 = local_758[0xf];
    lStack_510 = lStack_6d0;
    local_628[0] = local_328[0];
    local_628[1] = local_328[1];
    local_628[2] = local_328[2];
    local_628[3] = local_328[3];
    local_608 = local_328[4];
    uStack_600 = local_328[5];
    local_5f8 = local_328[6];
    uStack_5f0 = local_328[7];
    local_5e8 = local_328[8];
    uStack_5e0 = local_328[9];
    local_5d8 = local_328[10];
    uStack_5d0 = local_328[0xb];
    local_5c8 = local_328[0xc];
    uStack_5c0 = local_328[0xd];
    local_5a8 = CONCAT44(iStack_2a4,local_2a8);
    local_5b8 = local_328[0xe];
    uStack_5b0 = local_328[0xf];
    lStack_5a0 = uStack_2a0;
    FUN_180879cf0(local_628,local_598,lVar27,lVar29,CONCAT44(uVar40,DAT_18207a188));
    fVar39 = *(float *)(*(longlong *)(param_1 + 0x2c38) + 4);
    fVar36 = (float)FUN_181c9a9fb(DAT_18207a514);
    if (fVar39 <= 0.0) {
      fVar39 = 0.0;
    }
    if (DAT_182079f9c <= fVar39) {
      fVar39 = DAT_182079f9c;
    }
    fVar36 = fVar36 * fVar39;
  }
  else {
    if (0 < (int)local_6d8) {
      lVar27 = lVar27 - (longlong)local_758;
      plVar21 = local_758;
      do {
        iVar23 = iVar23 + 1;
        *plVar21 = *(longlong *)(lVar27 + (longlong)plVar21);
        plVar21 = plVar21 + 1;
      } while (iVar23 < (int)local_6d8);
    }
    lVar17 = uStack_2a0;
    lVar34 = local_328[0xf];
    lVar16 = local_328[0xe];
    lVar15 = local_328[0xd];
    lVar14 = local_328[0xc];
    lVar13 = local_328[0xb];
    lVar12 = local_328[10];
    lVar11 = local_328[9];
    lVar10 = local_328[8];
    lVar9 = local_328[7];
    lVar8 = local_328[6];
    lVar7 = local_328[5];
    lVar6 = local_328[4];
    lVar5 = local_328[3];
    lVar4 = local_328[2];
    lVar3 = local_328[1];
    lVar28 = local_328[0];
    uVar2 = CONCAT44(iStack_2a4,local_2a8);
    local_598[0] = local_758[0];
    local_598[1] = local_758[1];
    local_598[2] = local_758[2];
    local_598[3] = local_758[3];
    local_578 = local_758[4];
    uStack_570 = local_758[5];
    local_568 = local_758[6];
    uStack_560 = local_758[7];
    local_558 = local_758[8];
    uStack_550 = local_758[9];
    local_548 = local_758[10];
    uStack_540 = local_758[0xb];
    local_538 = local_758[0xc];
    uStack_530 = local_758[0xd];
    local_518 = CONCAT44(uStack_6d4,local_6d8);
    lStack_510 = lStack_6d0;
    local_528 = local_758[0xe];
    uStack_520 = local_758[0xf];
    local_628[0] = local_328[0];
    local_628[1] = local_328[1];
    local_628[2] = local_328[2];
    local_628[3] = local_328[3];
    local_608 = local_328[4];
    uStack_600 = local_328[5];
    local_5f8 = local_328[6];
    uStack_5f0 = local_328[7];
    local_5e8 = local_328[8];
    uStack_5e0 = local_328[9];
    local_5d8 = local_328[10];
    uStack_5d0 = local_328[0xb];
    local_5c8 = local_328[0xc];
    uStack_5c0 = local_328[0xd];
    local_5b8 = local_328[0xe];
    uStack_5b0 = local_328[0xf];
    lStack_5a0 = uStack_2a0;
    local_5a8 = uVar2;
    FUN_180879cf0(local_628,local_598,lVar27,lVar29,CONCAT44(uVar40,fVar39));
    fVar38 = DAT_18207a188;
    local_598[0] = lVar28;
    local_598[1] = lVar3;
    local_598[2] = lVar4;
    local_598[3] = lVar5;
    local_578 = lVar6;
    uStack_570 = lVar7;
    local_568 = lVar8;
    uStack_560 = lVar9;
    local_558 = lVar10;
    uStack_550 = lVar11;
    local_548 = lVar12;
    uStack_540 = lVar13;
    local_538 = lVar14;
    uStack_530 = lVar15;
    local_528 = lVar16;
    uStack_520 = lVar34;
    local_518 = uVar2;
    lStack_510 = lVar17;
    if (0 < (int)uVar31) {
      plVar21 = local_598;
      do {
        FUN_180001220(fVar38,*plVar21,iVar22);
        plVar21 = plVar21 + 1;
        uVar32 = uVar32 - 1;
      } while (uVar32 != 0);
    }
    fVar39 = *(float *)(*(longlong *)(param_1 + 0x2c38) + 4);
    fVar36 = (float)FUN_181c9a9fb(DAT_18207a450);
    if (fVar39 <= 0.0) {
      fVar39 = 0.0;
    }
    if (DAT_182079f9c <= fVar39) {
      fVar39 = DAT_182079f9c;
    }
    fVar36 = (fVar36 - _DAT_18207a1d0) * fVar39 + _DAT_18207a1d0;
  }
  fVar39 = (float)FUN_181c9a9d7(fVar36);
  local_6b8[0xf] = 0;
  local_6b8[0] = 0;
  iVar22 = 0;
  local_638 = *(int *)(param_1 + 0xc48);
  uStack_634 = *(int *)(param_1 + 0xc50);
  uStack_630 = (longlong)*(int *)(param_1 + 0xc50) << 2;
  local_6b8[1] = 0;
  local_6b8[2] = 0;
  local_6b8[3] = 0;
  local_6b8[4] = 0;
  local_6b8[5] = 0;
  local_6b8[6] = 0;
  local_6b8[7] = 0;
  local_6b8[8] = 0;
  local_6b8[9] = 0;
  local_6b8[10] = 0;
  local_6b8[0xb] = 0;
  local_6b8[0xc] = 0;
  local_6b8[0xd] = 0;
  local_6b8[0xe] = 0;
  if (0 < *(int *)(param_1 + 0xc48)) {
    plVar21 = local_6b8;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0xbc8) - (longlong)local_6b8) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)local_638);
  }
  uVar31 = *(uint *)(param_2 + 3);
  local_508[0] = 0;
  local_508[0xf] = 0;
  lVar27 = 0;
  lStack_480 = (longlong)(int)uStack_634 << 2;
  local_488 = CONCAT44(uStack_634,local_638);
  local_508[1] = 0;
  local_508[2] = 0;
  local_508[3] = 0;
  local_508[4] = 0;
  local_508[5] = 0;
  local_508[6] = 0;
  local_508[7] = 0;
  local_508[8] = 0;
  local_508[9] = 0;
  local_508[10] = 0;
  local_508[0xb] = 0;
  local_508[0xc] = 0;
  local_508[0xd] = 0;
  local_508[0xe] = 0;
  if (0 < (int)local_638) {
    uVar19 = uVar31;
    do {
      uVar20 = uStack_634 + uVar19;
      local_508[lVar27] = *param_2 + (longlong)(int)uVar19 * 4;
      uVar19 = (uVar20 - (uVar20 & 0xf)) + 0x10;
      if ((uVar20 & 0xf) == 0) {
        uVar19 = uVar20;
      }
      lVar27 = lVar27 + 1;
      *(uint *)(param_2 + 3) = uVar19;
    } while (lVar27 < (int)local_638);
  }
  lVar16 = lStack_480;
  uVar2 = local_488;
  lVar15 = local_508[0xf];
  lVar14 = local_508[0xe];
  lVar13 = local_508[0xd];
  lVar12 = local_508[0xc];
  lVar11 = local_508[0xb];
  lVar10 = local_508[10];
  lVar9 = local_508[9];
  lVar8 = local_508[8];
  lVar7 = local_508[7];
  lVar6 = local_508[6];
  lVar5 = local_508[5];
  lVar4 = local_508[4];
  lVar3 = local_508[3];
  lVar28 = local_508[2];
  lVar29 = local_508[1];
  lVar27 = local_508[0];
  local_598[0] = local_508[0];
  local_598[1] = local_508[1];
  local_598[2] = local_508[2];
  local_598[3] = local_508[3];
  local_578 = local_508[4];
  uStack_570 = local_508[5];
  local_568 = local_508[6];
  uStack_560 = local_508[7];
  local_558 = local_508[8];
  uStack_550 = local_508[9];
  local_548 = local_508[10];
  uStack_540 = local_508[0xb];
  local_538 = local_508[0xc];
  uStack_530 = local_508[0xd];
  local_528 = local_508[0xe];
  uStack_520 = local_508[0xf];
  local_518 = local_488;
  lStack_510 = lStack_480;
  FUN_1808833f0(local_598);
  local_758[0] = local_6b8[0];
  local_758[1] = local_6b8[1];
  local_758[2] = local_6b8[2];
  local_758[3] = local_6b8[3];
  local_758[4] = local_6b8[4];
  local_758[5] = local_6b8[5];
  local_758[6] = local_6b8[6];
  local_758[7] = local_6b8[7];
  local_758[8] = local_6b8[8];
  local_758[9] = local_6b8[9];
  local_758[10] = local_6b8[10];
  local_758[0xb] = local_6b8[0xb];
  local_758[0xc] = local_6b8[0xc];
  local_758[0xd] = local_6b8[0xd];
  local_758[0xe] = local_6b8[0xe];
  local_758[0xf] = local_6b8[0xf];
  local_6d8 = local_638;
  uStack_6d4 = uStack_634;
  lStack_6d0 = uStack_630;
  local_628[0] = lVar27;
  local_628[1] = lVar29;
  local_628[2] = lVar28;
  local_628[3] = lVar3;
  local_608 = lVar4;
  uStack_600 = lVar5;
  local_5f8 = lVar6;
  uStack_5f0 = lVar7;
  local_5e8 = lVar8;
  uStack_5e0 = lVar9;
  local_5d8 = lVar10;
  uStack_5d0 = lVar11;
  local_5c8 = lVar12;
  uStack_5c0 = lVar13;
  local_5b8 = lVar14;
  uStack_5b0 = lVar15;
  local_5a8 = uVar2;
  lStack_5a0 = lVar16;
  FUN_1808834c0(local_758);
  *(uint *)(param_2 + 3) = uVar31;
  local_6b8[0xf] = 0;
  iVar22 = 0;
  local_6b8[0] = 0;
  local_638 = *(int *)(param_1 + 0xcd8);
  uStack_634 = *(int *)(param_1 + 0xce0);
  uStack_630 = (longlong)*(int *)(param_1 + 0xce0) << 2;
  local_6b8[1] = 0;
  local_6b8[2] = 0;
  local_6b8[3] = 0;
  local_6b8[4] = 0;
  local_6b8[5] = 0;
  local_6b8[6] = 0;
  local_6b8[7] = 0;
  local_6b8[8] = 0;
  local_6b8[9] = 0;
  local_6b8[10] = 0;
  local_6b8[0xb] = 0;
  local_6b8[0xc] = 0;
  local_6b8[0xd] = 0;
  local_6b8[0xe] = 0;
  if (0 < *(int *)(param_1 + 0xcd8)) {
    plVar21 = local_6b8;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0xc58) - (longlong)local_6b8) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)local_638);
  }
  local_508[0] = 0;
  local_508[0xf] = 0;
  lVar27 = 0;
  lStack_480 = (longlong)(int)uStack_634 << 2;
  local_488 = CONCAT44(uStack_634,local_638);
  local_508[1] = 0;
  local_508[2] = 0;
  local_508[3] = 0;
  local_508[4] = 0;
  local_508[5] = 0;
  local_508[6] = 0;
  local_508[7] = 0;
  local_508[8] = 0;
  local_508[9] = 0;
  local_508[10] = 0;
  local_508[0xb] = 0;
  local_508[0xc] = 0;
  local_508[0xd] = 0;
  local_508[0xe] = 0;
  if (0 < (int)local_638) {
    uVar19 = uVar31;
    do {
      uVar20 = uStack_634 + uVar19;
      local_508[lVar27] = *param_2 + (longlong)(int)uVar19 * 4;
      uVar19 = (uVar20 - (uVar20 & 0xf)) + 0x10;
      if ((uVar20 & 0xf) == 0) {
        uVar19 = uVar20;
      }
      lVar27 = lVar27 + 1;
      *(uint *)(param_2 + 3) = uVar19;
    } while (lVar27 < (int)local_638);
  }
  lVar16 = lStack_480;
  uVar2 = local_488;
  lVar15 = local_508[0xf];
  lVar14 = local_508[0xe];
  lVar13 = local_508[0xd];
  lVar12 = local_508[0xc];
  lVar11 = local_508[0xb];
  lVar10 = local_508[10];
  lVar9 = local_508[9];
  lVar8 = local_508[8];
  lVar7 = local_508[7];
  lVar6 = local_508[6];
  lVar5 = local_508[5];
  lVar4 = local_508[4];
  lVar3 = local_508[3];
  lVar28 = local_508[2];
  lVar29 = local_508[1];
  lVar27 = local_508[0];
  local_598[0] = local_508[0];
  local_598[1] = local_508[1];
  local_598[2] = local_508[2];
  local_598[3] = local_508[3];
  local_578 = local_508[4];
  uStack_570 = local_508[5];
  local_568 = local_508[6];
  uStack_560 = local_508[7];
  local_558 = local_508[8];
  uStack_550 = local_508[9];
  local_548 = local_508[10];
  uStack_540 = local_508[0xb];
  local_538 = local_508[0xc];
  uStack_530 = local_508[0xd];
  local_528 = local_508[0xe];
  uStack_520 = local_508[0xf];
  local_518 = local_488;
  lStack_510 = lStack_480;
  FUN_1808833f0(local_598,fVar39 * fVar38);
  local_758[0] = local_6b8[0];
  local_758[1] = local_6b8[1];
  local_758[2] = local_6b8[2];
  local_758[3] = local_6b8[3];
  local_758[4] = local_6b8[4];
  local_758[5] = local_6b8[5];
  local_758[6] = local_6b8[6];
  local_758[7] = local_6b8[7];
  local_758[8] = local_6b8[8];
  local_758[9] = local_6b8[9];
  local_758[10] = local_6b8[10];
  local_758[0xb] = local_6b8[0xb];
  local_758[0xc] = local_6b8[0xc];
  local_758[0xd] = local_6b8[0xd];
  local_758[0xe] = local_6b8[0xe];
  local_758[0xf] = local_6b8[0xf];
  local_6d8 = local_638;
  uStack_6d4 = uStack_634;
  lStack_6d0 = uStack_630;
  local_628[0] = lVar27;
  local_628[1] = lVar29;
  local_628[2] = lVar28;
  local_628[3] = lVar3;
  local_608 = lVar4;
  uStack_600 = lVar5;
  local_5f8 = lVar6;
  uStack_5f0 = lVar7;
  local_5e8 = lVar8;
  uStack_5e0 = lVar9;
  local_5d8 = lVar10;
  uStack_5d0 = lVar11;
  local_5c8 = lVar12;
  uStack_5c0 = lVar13;
  local_5b8 = lVar14;
  uStack_5b0 = lVar15;
  local_5a8 = uVar2;
  lStack_5a0 = lVar16;
  FUN_1808834c0(local_758);
  *(uint *)(param_2 + 3) = uVar31;
  uVar32 = (ulonglong)(int)*(uint *)(param_1 + 0xd70);
  local_6b8[0xf] = 0;
  iVar22 = 0;
  local_6b8[0] = 0;
  local_638 = *(uint *)(param_1 + 0xd68);
  uStack_634 = *(uint *)(param_1 + 0xd70);
  uStack_630 = uVar32 << 2;
  local_6b8[1] = 0;
  local_6b8[2] = 0;
  local_6b8[3] = 0;
  local_6b8[4] = 0;
  local_6b8[5] = 0;
  local_6b8[6] = 0;
  local_6b8[7] = 0;
  local_6b8[8] = 0;
  local_6b8[9] = 0;
  local_6b8[10] = 0;
  local_6b8[0xb] = 0;
  local_6b8[0xc] = 0;
  local_6b8[0xd] = 0;
  local_6b8[0xe] = 0;
  if (0 < (int)*(uint *)(param_1 + 0xd68)) {
    plVar21 = local_6b8;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0xce8) - (longlong)local_6b8) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)local_638);
    uVar32 = (ulonglong)uStack_634;
  }
  lVar27 = param_2[3];
  lVar29 = 0;
  local_758[0] = 0;
  local_758[0xf] = 0;
  uVar31 = (uint)uVar32;
  lStack_6d0 = (longlong)(int)uVar31 << 2;
  lVar28 = (longlong)(int)local_638;
  local_758[1] = 0;
  local_758[2] = 0;
  local_758[3] = 0;
  local_758[4] = 0;
  local_758[5] = 0;
  local_758[6] = 0;
  local_758[7] = 0;
  local_758[8] = 0;
  local_758[9] = 0;
  local_758[10] = 0;
  local_758[0xb] = 0;
  local_758[0xc] = 0;
  local_758[0xd] = 0;
  local_758[0xe] = 0;
  local_6d8 = local_638;
  uStack_6d4 = uVar31;
  if (0 < (int)local_638) {
    uVar19 = *(uint *)(param_2 + 3);
    do {
      uVar20 = uVar19 + uVar31;
      local_758[lVar29] = *param_2 + (longlong)(int)uVar19 * 4;
      uVar19 = (uVar20 - (uVar20 & 0xf)) + 0x10;
      if ((uVar20 & 0xf) == 0) {
        uVar19 = uVar20;
      }
      lVar29 = lVar29 + 1;
      *(uint *)(param_2 + 3) = uVar19;
    } while (lVar29 < lVar28);
    uVar32 = (ulonglong)uStack_6d4;
  }
  lVar34 = lStack_6d0;
  uVar31 = local_6d8;
  lVar16 = local_758[0xf];
  lVar15 = local_758[0xe];
  lVar14 = local_758[0xd];
  lVar13 = local_758[0xc];
  lVar12 = local_758[0xb];
  lVar11 = local_758[10];
  lVar10 = local_758[9];
  lVar9 = local_758[8];
  lVar8 = local_758[7];
  lVar7 = local_758[6];
  lVar6 = local_758[5];
  lVar5 = local_758[4];
  lVar4 = local_758[3];
  lVar3 = local_758[2];
  lVar28 = local_758[1];
  lVar29 = local_758[0];
  uVar25 = (ulonglong)local_6d8;
  uVar2 = CONCAT44(uStack_6d4,local_6d8);
  local_598[0] = local_758[0];
  local_598[1] = local_758[1];
  local_598[2] = local_758[2];
  local_598[3] = local_758[3];
  local_578 = local_758[4];
  uStack_570 = local_758[5];
  local_568 = local_758[6];
  uStack_560 = local_758[7];
  local_558 = local_758[8];
  uStack_550 = local_758[9];
  local_548 = local_758[10];
  uStack_540 = local_758[0xb];
  local_538 = local_758[0xc];
  uStack_530 = local_758[0xd];
  local_528 = local_758[0xe];
  uStack_520 = local_758[0xf];
  lStack_510 = lStack_6d0;
  local_518 = uVar2;
  FUN_1808833f0(local_598);
  lVar18 = local_328[1];
  lVar17 = local_328[0];
  local_208[2] = local_328[2];
  local_208[3] = local_328[3];
  local_1e8 = local_328[4];
  uStack_1e0 = local_328[5];
  local_1d8 = local_328[6];
  uStack_1d0 = local_328[7];
  local_1c8 = local_328[8];
  uStack_1c0 = local_328[9];
  local_1b8 = local_328[10];
  uStack_1b0 = local_328[0xb];
  local_1a8 = local_328[0xc];
  uStack_1a0 = local_328[0xd];
  local_198 = local_328[0xe];
  uStack_190 = local_328[0xf];
  local_208[0] = local_328[0];
  local_208[1] = local_328[1];
  local_188 = local_2a8;
  uStack_184 = iStack_2a4;
  uStack_180 = (undefined4)uStack_2a0;
  uStack_17c = uStack_2a0._4_4_;
  local_508[0] = lVar29;
  local_508[1] = lVar28;
  local_508[2] = lVar3;
  local_508[3] = lVar4;
  local_508[4] = lVar5;
  local_508[5] = lVar6;
  local_508[6] = lVar7;
  local_508[7] = lVar8;
  local_508[8] = lVar9;
  local_508[9] = lVar10;
  local_508[10] = lVar11;
  local_508[0xb] = lVar12;
  local_508[0xc] = lVar13;
  local_508[0xd] = lVar14;
  local_508[0xe] = lVar15;
  local_508[0xf] = lVar16;
  local_488 = uVar2;
  lStack_480 = lVar34;
  local_3c8 = local_328[0];
  local_6c8 = (float)local_2a8;
  if (uVar31 == local_2a8) {
    if (0 < (int)uVar31) {
      lVar33 = 0;
      uVar30 = uVar25;
      do {
        FUN_180001340(*(undefined8 *)((longlong)local_208 + lVar33),
                      *(undefined8 *)((longlong)local_508 + lVar33),uVar32 & 0xffffffff);
        lVar33 = lVar33 + 8;
        uVar30 = uVar30 - 1;
      } while (uVar30 != 0);
    }
  }
  else if ((local_2a8 == 1) && (0 < (int)uVar31)) {
    plVar21 = local_508;
    uVar30 = uVar25;
    do {
      FUN_180001340(lVar17,*plVar21,uVar32 & 0xffffffff);
      plVar21 = plVar21 + 1;
      uVar30 = uVar30 - 1;
    } while (uVar30 != 0);
  }
  lVar33 = local_3b8[0];
  local_178[0] = local_3b8[0];
  local_178[1] = local_3b8[1];
  local_158 = local_3b8[4];
  uStack_150 = local_3b8[5];
  local_178[2] = local_3b8[2];
  local_178[3] = local_3b8[3];
  local_138 = local_3b8[8];
  uStack_130 = local_3b8[9];
  local_148 = local_3b8[6];
  uStack_140 = local_3b8[7];
  local_118 = local_3b8[0xc];
  uStack_110 = local_3b8[0xd];
  local_128 = local_3b8[10];
  uStack_120 = local_3b8[0xb];
  local_108 = local_3b8[0xe];
  uStack_100 = local_3b8[0xf];
  local_f8 = local_338;
  lStack_f0 = lStack_330;
  local_628[0] = lVar29;
  local_628[1] = lVar28;
  local_628[2] = lVar3;
  local_628[3] = lVar4;
  local_608 = lVar5;
  uStack_600 = lVar6;
  local_5f8 = lVar7;
  uStack_5f0 = lVar8;
  local_5e8 = lVar9;
  uStack_5e0 = lVar10;
  local_5d8 = lVar11;
  uStack_5d0 = lVar12;
  local_5c8 = lVar13;
  uStack_5c0 = lVar14;
  local_5b8 = lVar15;
  uStack_5b0 = lVar16;
  local_5a8 = uVar2;
  lStack_5a0 = lVar34;
  if (uVar31 == (uint)local_338) {
    if (0 < (int)uVar31) {
      lVar33 = 0;
      do {
        FUN_180001340(*(undefined8 *)((longlong)local_178 + lVar33),
                      *(undefined8 *)((longlong)local_628 + lVar33),uVar32 & 0xffffffff);
        lVar33 = lVar33 + 8;
        uVar25 = uVar25 - 1;
      } while (uVar25 != 0);
    }
  }
  else if (((uint)local_338 == 1) && (0 < (int)uVar31)) {
    plVar21 = local_628;
    do {
      FUN_180001340(lVar33,*plVar21,uVar32 & 0xffffffff);
      plVar21 = plVar21 + 1;
      uVar25 = uVar25 - 1;
    } while (uVar25 != 0);
  }
  local_458[0] = local_6b8[0];
  local_458[1] = local_6b8[1];
  local_458[2] = local_6b8[2];
  local_458[3] = local_6b8[3];
  local_438 = local_6b8[4];
  uStack_430 = local_6b8[5];
  local_428 = local_6b8[6];
  uStack_420 = local_6b8[7];
  local_418 = local_6b8[8];
  uStack_410 = local_6b8[9];
  local_408 = local_6b8[10];
  uStack_400 = local_6b8[0xb];
  local_3f8 = local_6b8[0xc];
  uStack_3f0 = local_6b8[0xd];
  local_3e8 = local_6b8[0xe];
  uStack_3e0 = local_6b8[0xf];
  local_3d8 = CONCAT44(uStack_634,local_638);
  lStack_3d0 = uStack_630;
  local_3b8[0] = lVar29;
  local_3b8[1] = lVar28;
  local_3b8[2] = lVar3;
  local_3b8[3] = lVar4;
  local_3b8[4] = lVar5;
  local_3b8[5] = lVar6;
  local_3b8[6] = lVar7;
  local_3b8[7] = lVar8;
  local_3b8[8] = lVar9;
  local_3b8[9] = lVar10;
  local_3b8[10] = lVar11;
  local_3b8[0xb] = lVar12;
  local_3b8[0xc] = lVar13;
  local_3b8[0xd] = lVar14;
  local_3b8[0xe] = lVar15;
  local_3b8[0xf] = lVar16;
  lStack_330 = lVar34;
  local_338 = uVar2;
  FUN_1808834c0(local_458);
  *(int *)(param_2 + 3) = (int)lVar27;
  uVar32 = (ulonglong)(int)*(uint *)(param_1 + 0xe00);
  iVar22 = 0;
  local_6b8[0xf] = 0;
  local_6b8[0] = 0;
  local_638 = *(uint *)(param_1 + 0xdf8);
  uStack_634 = *(uint *)(param_1 + 0xe00);
  uStack_630 = uVar32 << 2;
  local_6b8[1] = 0;
  local_6b8[2] = 0;
  local_6b8[3] = 0;
  local_6b8[4] = 0;
  local_6b8[5] = 0;
  local_6b8[6] = 0;
  local_6b8[7] = 0;
  local_6b8[8] = 0;
  local_6b8[9] = 0;
  local_6b8[10] = 0;
  local_6b8[0xb] = 0;
  local_6b8[0xc] = 0;
  local_6b8[0xd] = 0;
  local_6b8[0xe] = 0;
  if (0 < (int)*(uint *)(param_1 + 0xdf8)) {
    plVar21 = local_6b8;
    do {
      iVar22 = iVar22 + 1;
      *plVar21 = *(longlong *)(((param_1 + 0xd78) - (longlong)local_6b8) + (longlong)plVar21);
      plVar21 = plVar21 + 1;
    } while (iVar22 < (int)local_638);
    uVar32 = (ulonglong)uStack_634;
  }
  uVar31 = *(uint *)(param_2 + 3);
  local_758[0] = 0;
  local_758[0xf] = 0;
  lVar27 = 0;
  uVar19 = (uint)uVar32;
  lStack_6d0 = (longlong)(int)uVar19 << 2;
  lVar29 = (longlong)(int)local_638;
  local_758[1] = 0;
  local_758[2] = 0;
  local_758[3] = 0;
  local_758[4] = 0;
  local_758[5] = 0;
  local_758[6] = 0;
  local_758[7] = 0;
  local_758[8] = 0;
  local_758[9] = 0;
  local_758[10] = 0;
  local_758[0xb] = 0;
  local_758[0xc] = 0;
  local_758[0xd] = 0;
  local_758[0xe] = 0;
  local_6d8 = local_638;
  uStack_6d4 = uVar19;
  if (0 < (int)local_638) {
    do {
      uVar20 = uVar31 + uVar19;
      local_758[lVar27] = *param_2 + (longlong)(int)uVar31 * 4;
      uVar31 = (uVar20 - (uVar20 & 0xf)) + 0x10;
      if ((uVar20 & 0xf) == 0) {
        uVar31 = uVar20;
      }
      lVar27 = lVar27 + 1;
      *(uint *)(param_2 + 3) = uVar31;
    } while (lVar27 < lVar29);
    uVar32 = (ulonglong)uStack_6d4;
  }
  lVar16 = lStack_6d0;
  uVar31 = local_6d8;
  lVar15 = local_758[0xf];
  lVar14 = local_758[0xe];
  lVar13 = local_758[0xd];
  lVar12 = local_758[0xc];
  lVar11 = local_758[0xb];
  lVar10 = local_758[10];
  lVar9 = local_758[9];
  lVar8 = local_758[8];
  lVar7 = local_758[7];
  lVar6 = local_758[6];
  lVar5 = local_758[5];
  lVar4 = local_758[4];
  lVar3 = local_758[3];
  lVar28 = local_758[2];
  lVar29 = local_758[1];
  lVar27 = local_758[0];
  uVar25 = (ulonglong)local_6d8;
  uVar2 = CONCAT44(uStack_6d4,local_6d8);
  local_458[0] = local_758[0];
  local_458[1] = local_758[1];
  local_458[2] = local_758[2];
  local_458[3] = local_758[3];
  local_438 = local_758[4];
  uStack_430 = local_758[5];
  local_428 = local_758[6];
  uStack_420 = local_758[7];
  local_418 = local_758[8];
  uStack_410 = local_758[9];
  local_408 = local_758[10];
  uStack_400 = local_758[0xb];
  local_3f8 = local_758[0xc];
  uStack_3f0 = local_758[0xd];
  local_3e8 = local_758[0xe];
  uStack_3e0 = local_758[0xf];
  lStack_3d0 = lStack_6d0;
  local_3d8 = uVar2;
  FUN_1808833f0(local_458);
  lVar34 = local_3c8;
  if (bVar35) {
    local_458[2] = local_328[2];
    local_458[3] = local_328[3];
    local_438 = local_328[4];
    uStack_430 = local_328[5];
    local_428 = local_328[6];
    uStack_420 = local_328[7];
    local_418 = local_328[8];
    uStack_410 = local_328[9];
    local_408 = local_328[10];
    uStack_400 = local_328[0xb];
    local_3f8 = local_328[0xc];
    uStack_3f0 = local_328[0xd];
    local_3e8 = local_328[0xe];
    uStack_3e0 = local_328[0xf];
    local_3d8 = CONCAT44(iStack_2a4,local_2a8);
    lStack_3d0 = uStack_2a0;
    local_458[0] = lVar17;
    local_458[1] = lVar18;
    local_628[0] = lVar27;
    local_628[1] = lVar29;
    local_628[2] = lVar28;
    local_628[3] = lVar3;
    local_608 = lVar4;
    uStack_600 = lVar5;
    local_5f8 = lVar6;
    uStack_5f0 = lVar7;
    local_5e8 = lVar8;
    uStack_5e0 = lVar9;
    local_5d8 = lVar10;
    uStack_5d0 = lVar11;
    local_5c8 = lVar12;
    uStack_5c0 = lVar13;
    local_5b8 = lVar14;
    uStack_5b0 = lVar15;
    local_5a8 = uVar2;
    lStack_5a0 = lVar16;
    if ((float)uVar31 == local_6c8) {
      if (0 < (int)uVar31) {
        lVar34 = 0;
        uVar30 = uVar25;
        do {
          FUN_180001340(*(undefined8 *)((longlong)local_458 + lVar34),
                        *(undefined8 *)((longlong)local_628 + lVar34),uVar32 & 0xffffffff);
          lVar34 = lVar34 + 8;
          uVar30 = uVar30 - 1;
        } while (uVar30 != 0);
      }
    }
    else if ((local_6c8 == 1.4013e-45) && (0 < (int)uVar31)) {
      plVar21 = local_628;
      uVar30 = uVar25;
      do {
        FUN_180001340(lVar34,*plVar21,uVar32 & 0xffffffff);
        plVar21 = plVar21 + 1;
        uVar30 = uVar30 - 1;
      } while (uVar30 != 0);
    }
  }
  lVar34 = local_298[0];
  local_458[0] = local_298[0];
  local_458[1] = local_298[1];
  local_438 = local_298[4];
  uStack_430 = local_298[5];
  local_458[2] = local_298[2];
  local_458[3] = local_298[3];
  local_418 = local_298[8];
  uStack_410 = local_298[9];
  local_428 = local_298[6];
  uStack_420 = local_298[7];
  local_3f8 = local_298[0xc];
  uStack_3f0 = local_298[0xd];
  local_408 = local_298[10];
  uStack_400 = local_298[0xb];
  local_3e8 = local_298[0xe];
  uStack_3e0 = local_298[0xf];
  local_3d8 = CONCAT44(iStack_214,local_218);
  lStack_3d0 = lStack_210;
  local_628[0] = lVar27;
  local_628[1] = lVar29;
  local_628[2] = lVar28;
  local_628[3] = lVar3;
  local_608 = lVar4;
  uStack_600 = lVar5;
  local_5f8 = lVar6;
  uStack_5f0 = lVar7;
  local_5e8 = lVar8;
  uStack_5e0 = lVar9;
  local_5d8 = lVar10;
  uStack_5d0 = lVar11;
  local_5c8 = lVar12;
  uStack_5c0 = lVar13;
  local_5b8 = lVar14;
  uStack_5b0 = lVar15;
  local_5a8 = uVar2;
  lStack_5a0 = lVar16;
  if (uVar31 == local_218) {
    if (0 < (int)uVar31) {
      do {
        FUN_180001340(*(undefined8 *)((longlong)local_458 + lVar26),
                      *(undefined8 *)((longlong)local_628 + lVar26),uVar32 & 0xffffffff);
        lVar26 = lVar26 + 8;
        uVar25 = uVar25 - 1;
      } while (uVar25 != 0);
    }
  }
  else if ((local_218 == 1) && (0 < (int)uVar31)) {
    plVar21 = local_628;
    do {
      FUN_180001340(lVar34,*plVar21,uVar32 & 0xffffffff);
      plVar21 = plVar21 + 1;
      uVar25 = uVar25 - 1;
    } while (uVar25 != 0);
  }
  local_208[0] = local_6b8[0];
  local_208[1] = local_6b8[1];
  local_1e8 = local_6b8[4];
  uStack_1e0 = local_6b8[5];
  local_1c8 = local_6b8[8];
  uStack_1c0 = local_6b8[9];
  local_1d8 = local_6b8[6];
  uStack_1d0 = local_6b8[7];
  local_1a8 = local_6b8[0xc];
  uStack_1a0 = local_6b8[0xd];
  local_1b8 = local_6b8[10];
  uStack_1b0 = local_6b8[0xb];
  local_208[2] = local_6b8[2];
  local_208[3] = local_6b8[3];
  local_188 = local_638;
  uStack_184 = uStack_634;
  uStack_180 = (undefined4)uStack_630;
  uStack_17c = uStack_630._4_4_;
  local_178[0] = lVar27;
  local_178[1] = lVar29;
  local_178[2] = lVar28;
  local_178[3] = lVar3;
  local_158 = lVar4;
  uStack_150 = lVar5;
  local_148 = lVar6;
  uStack_140 = lVar7;
  local_138 = lVar8;
  uStack_130 = lVar9;
  local_128 = lVar10;
  uStack_120 = lVar11;
  local_118 = lVar12;
  uStack_110 = lVar13;
  local_108 = lVar14;
  uStack_100 = lVar15;
  lStack_f0 = lVar16;
  local_198 = local_6b8[0xe];
  uStack_190 = local_6b8[0xf];
  local_f8 = uVar2;
  FUN_1808834c0(local_208);
  *(undefined4 *)(param_2 + 3) = local_464;
  return;
}

