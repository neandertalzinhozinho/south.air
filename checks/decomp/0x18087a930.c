 (GhidraScript)  

void FUN_18087a930(longlong param_1,undefined8 param_2,undefined8 *param_3,float param_4,
                  undefined8 param_5,longlong *param_6)

{
  longlong lVar1;
  undefined8 uVar2;
  float fVar3;
  uint uVar4;
  undefined8 *puVar5;
  uint uVar6;
  ulonglong uVar7;
  int iVar8;
  int iVar9;
  ulonglong uVar10;
  longlong lVar11;
  float local_res20 [2];
  undefined8 local_328 [16];
  uint local_2a8;
  int iStack_2a4;
  longlong lStack_2a0;
  undefined8 local_298;
  undefined8 uStack_290;
  undefined8 uStack_288;
  undefined8 uStack_280;
  undefined8 uStack_278;
  undefined8 local_270;
  undefined8 uStack_268;
  undefined8 local_260;
  undefined8 uStack_258;
  undefined8 local_250;
  undefined8 uStack_248;
  undefined8 local_240;
  undefined8 uStack_238;
  undefined8 local_230;
  undefined8 uStack_228;
  undefined8 local_220;
  uint local_218;
  int iStack_214;
  longlong lStack_210;
  ulonglong local_208;
  undefined8 local_1f8 [16];
  undefined8 local_178;
  longlong lStack_170;
  undefined8 local_168;
  undefined8 uStack_160;
  undefined8 uStack_158;
  undefined8 uStack_150;
  undefined8 uStack_148;
  undefined8 local_140;
  undefined8 uStack_138;
  undefined8 local_130;
  undefined8 uStack_128;
  undefined8 local_120;
  undefined8 uStack_118;
  undefined8 local_110;
  undefined8 uStack_108;
  undefined8 local_100;
  undefined8 uStack_f8;
  undefined8 local_f0;
  uint local_e8;
  int iStack_e4;
  longlong lStack_e0;
  undefined8 local_d8 [4];
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
  longlong lStack_50;
  
  uVar6 = *(uint *)((longlong)param_3 + 0x84);
  uVar7 = (ulonglong)(int)uVar6;
  *(undefined8 *)(param_1 + 400) = 0x10;
  *(ulonglong *)(param_1 + 0x198) = uVar7;
  uVar10 = (uVar7 - (uVar6 & 3)) + 4;
  if ((uVar7 & 3) == 0) {
    uVar10 = uVar7;
  }
  local_res20[0] = param_4;
  FUN_180878400(param_1 + 0x100,*(undefined4 *)(param_1 + 400),uVar10);
  *(undefined8 *)(param_1 + 0x330) = 0x10;
  *(ulonglong *)(param_1 + 0x338) = uVar7;
  uVar10 = (uVar7 - (uVar6 & 3)) + 4;
  if ((uVar6 & 3) == 0) {
    uVar10 = uVar7;
  }
  FUN_180878400(param_1 + 0x2a0,*(undefined4 *)(param_1 + 0x330),uVar10);
  *(undefined8 *)(param_1 + 0x4d0) = 0x10;
  *(ulonglong *)(param_1 + 0x4d8) = uVar7;
  uVar10 = (uVar7 - (uVar6 & 3)) + 4;
  if ((uVar6 & 3) == 0) {
    uVar10 = uVar7;
  }
  FUN_180878400(param_1 + 0x440,*(undefined4 *)(param_1 + 0x4d0),uVar10);
  local_328[0] = *param_3;
  local_328[1] = param_3[1];
  local_328[2] = param_3[2];
  local_328[3] = param_3[3];
  local_328[4] = param_3[4];
  local_328[5] = param_3[5];
  local_328[8] = param_3[8];
  local_328[9] = param_3[9];
  local_328[6] = param_3[6];
  local_328[7] = param_3[7];
  local_328[0xc] = param_3[0xc];
  local_328[0xd] = param_3[0xd];
  local_328[10] = param_3[10];
  local_328[0xb] = param_3[0xb];
  local_2a8 = *(uint *)(param_3 + 0x10);
  iStack_2a4 = *(undefined4 *)((longlong)param_3 + 0x84);
  lStack_2a0 = param_3[0x11];
  local_328[0xe] = param_3[0xe];
  local_328[0xf] = param_3[0xf];
  FUN_180881be0(param_1,param_2,local_328);
  lVar11 = (longlong)*(int *)(param_1 + 0x330);
  if (0 < lVar11) {
    puVar5 = (undefined8 *)(param_1 + 0x220);
    do {
      puVar5[-0x10] = puVar5[-0x44];
      *puVar5 = puVar5[-0x34];
      puVar5 = puVar5 + 1;
      lVar11 = lVar11 + -1;
    } while (lVar11 != 0);
  }
  fVar3 = DAT_182079f9c;
  local_2a8 = *(uint *)(param_1 + 400);
  if (local_2a8 == 0) {
    local_2a8 = *(uint *)(param_1 + 0x180);
  }
  iStack_2a4 = *(int *)(param_1 + 0x188);
  local_328[0] = 0;
  iVar8 = 0;
  local_328[0xf] = 0;
  lStack_2a0 = (longlong)*(int *)(param_1 + 0x188) << 2;
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
  if (0 < (int)local_2a8) {
    puVar5 = local_328;
    do {
      iVar8 = iVar8 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x100) - (longlong)local_328) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar8 < (int)local_2a8);
  }
  uVar10 = *(ulonglong *)(param_1 + 0x198);
  local_168 = 0;
  local_f0 = 0;
  iVar8 = (int)uVar10;
  local_e8 = local_2a8;
  iStack_e4 = iVar8;
  lStack_e0 = (longlong)iVar8 << 2;
  uStack_160 = 0;
  uStack_158 = 0;
  uStack_150 = 0;
  uStack_148 = 0;
  local_140 = 0;
  uStack_138 = 0;
  local_130 = 0;
  uStack_128 = 0;
  local_120 = 0;
  uStack_118 = 0;
  local_110 = 0;
  uStack_108 = 0;
  local_100 = 0;
  uStack_f8 = 0;
  if (0 < (int)local_2a8) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(&local_168,local_328,(ulonglong)local_2a8 << 3);
  }
  local_2a8 = *(uint *)(param_1 + 0x330);
  if (local_2a8 == 0) {
    local_2a8 = *(uint *)(param_1 + 800);
  }
  iStack_2a4 = *(int *)(param_1 + 0x328);
  iVar9 = 0;
  local_328[0] = 0;
  local_328[0xf] = 0;
  lStack_2a0 = (longlong)*(int *)(param_1 + 0x328) << 2;
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
  if (0 < (int)local_2a8) {
    puVar5 = local_328;
    do {
      iVar9 = iVar9 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x2a0) - (longlong)local_328) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar9 < (int)local_2a8);
  }
  uVar7 = *(ulonglong *)(param_1 + 0x338);
  local_220 = 0;
  iStack_214 = (int)uVar7;
  local_298 = 0;
  local_218 = local_2a8;
  lStack_210 = (longlong)iStack_214 << 2;
  uStack_290 = 0;
  uStack_288 = 0;
  uStack_280 = 0;
  uStack_278 = 0;
  local_270 = 0;
  uStack_268 = 0;
  local_260 = 0;
  uStack_258 = 0;
  local_250 = 0;
  uStack_248 = 0;
  local_240 = 0;
  uStack_238 = 0;
  local_230 = 0;
  uStack_228 = 0;
  if (0 < (int)local_2a8) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(&local_298,local_328,(ulonglong)local_2a8 << 3);
  }
  local_d8[0] = local_168;
  local_d8[1] = uStack_160;
  local_d8[2] = uStack_158;
  local_d8[3] = uStack_150;
  local_b8 = uStack_148;
  uStack_b0 = local_140;
  local_a8 = uStack_138;
  uStack_a0 = local_130;
  local_98 = uStack_128;
  uStack_90 = local_120;
  local_88 = uStack_118;
  uStack_80 = local_110;
  local_78 = uStack_108;
  uStack_70 = local_100;
  local_68 = uStack_f8;
  uStack_60 = local_f0;
  local_58 = CONCAT44(iStack_e4,local_e8);
  lStack_50 = lStack_e0;
  local_1f8[0] = 0;
  local_1f8[1] = 0;
  local_1f8[2] = 0;
  local_1f8[3] = 0;
  local_1f8[4] = 0;
  local_1f8[5] = 0;
  local_1f8[6] = 0;
  local_1f8[7] = 0;
  local_1f8[8] = 0;
  local_1f8[9] = 0;
  local_1f8[10] = 0;
  local_1f8[0xb] = 0;
  local_1f8[0xc] = 0;
  local_1f8[0xd] = 0;
  local_1f8[0xe] = 0;
  local_1f8[0xf] = 0;
  local_178 = CONCAT44(iStack_214,local_2a8);
  lStack_170 = (longlong)iStack_214 << 2;
  if (0 < (int)local_2a8) {
    lVar11 = 0;
    local_208 = (ulonglong)local_2a8;
    do {
      iVar9 = (int)param_6[3];
      uVar2 = *(undefined8 *)((longlong)local_d8 + lVar11);
      lVar1 = *param_6 + (longlong)iVar9 * 4;
      uVar4 = iVar8 + iVar9;
      uVar6 = (uVar4 - (uVar4 & 0xf)) + 0x10;
      if ((uVar4 & 0xf) == 0) {
        uVar6 = uVar4;
      }
      *(uint *)(param_6 + 3) = uVar6;
      FUN_180001490(uVar2,lVar1,uVar10 & 0xffffffff);
      local_res20[0] = 0.0;
      FUN_180001610(lVar1,uVar10 & 0xffffffff,local_res20,1);
      FUN_180001070(uVar2,fVar3 / local_res20[0],*(undefined8 *)((longlong)local_1f8 + lVar11),
                    uVar7 & 0xffffffff);
      local_208 = local_208 - 1;
      lVar11 = lVar11 + 8;
      *(int *)(param_6 + 3) = iVar9;
    } while (local_208 != 0);
  }
  FUN_180882870(param_1 + 0x340,param_1,param_6);
  local_2a8 = *(uint *)(param_1 + 0x330);
  if (local_2a8 == 0) {
    local_2a8 = *(uint *)(param_1 + 800);
  }
  iStack_2a4 = *(int *)(param_1 + 0x328);
  iVar8 = 0;
  local_328[0] = 0;
  local_328[0xf] = 0;
  lStack_2a0 = (longlong)*(int *)(param_1 + 0x328) << 2;
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
  if (0 < (int)local_2a8) {
    puVar5 = local_328;
    do {
      iVar8 = iVar8 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x2a0) - (longlong)local_328) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar8 < (int)local_2a8);
  }
  uVar10 = *(ulonglong *)(param_1 + 0x338);
  local_298 = 0;
  local_220 = 0;
  iStack_214 = (int)uVar10;
  local_218 = local_2a8;
  lStack_210 = (longlong)iStack_214 << 2;
  uStack_290 = 0;
  uStack_288 = 0;
  uStack_280 = 0;
  uStack_278 = 0;
  local_270 = 0;
  uStack_268 = 0;
  local_260 = 0;
  uStack_258 = 0;
  local_250 = 0;
  uStack_248 = 0;
  local_240 = 0;
  uStack_238 = 0;
  local_230 = 0;
  uStack_228 = 0;
  if (0 < (int)local_2a8) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(&local_298,local_328,(ulonglong)local_2a8 << 3);
  }
  local_1f8[0] = 0;
  local_1f8[1] = 0;
  local_1f8[2] = 0;
  local_1f8[3] = 0;
  local_1f8[4] = 0;
  local_1f8[5] = 0;
  local_1f8[6] = 0;
  local_1f8[7] = 0;
  local_1f8[8] = 0;
  local_1f8[9] = 0;
  local_1f8[10] = 0;
  local_1f8[0xb] = 0;
  local_1f8[0xc] = 0;
  local_1f8[0xd] = 0;
  local_1f8[0xe] = 0;
  local_1f8[0xf] = 0;
  local_178 = CONCAT44(iStack_214,local_2a8);
  lStack_170 = (longlong)iStack_214 << 2;
  if (0 < (int)local_2a8) {
    puVar5 = local_1f8;
    uVar7 = (ulonglong)local_2a8;
    do {
      FUN_180001100(*puVar5,uVar10 & 0xffffffff,0,0);
      puVar5 = puVar5 + 1;
      uVar7 = uVar7 - 1;
    } while (uVar7 != 0);
  }
  local_2a8 = *(uint *)(param_1 + 0x4d0);
  if (local_2a8 == 0) {
    local_2a8 = *(uint *)(param_1 + 0x4c0);
  }
  iStack_2a4 = *(int *)(param_1 + 0x4c8);
  iVar8 = 0;
  local_328[0] = 0;
  local_328[0xf] = 0;
  lStack_2a0 = (longlong)*(int *)(param_1 + 0x4c8) << 2;
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
  if (0 < (int)local_2a8) {
    puVar5 = local_328;
    do {
      iVar8 = iVar8 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x440) - (longlong)local_328) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar8 < (int)local_2a8);
  }
  uVar10 = *(ulonglong *)(param_1 + 0x4d8);
  local_220 = 0;
  iStack_214 = (int)uVar10;
  local_298 = 0;
  local_218 = local_2a8;
  lStack_210 = (longlong)iStack_214 << 2;
  uStack_290 = 0;
  uStack_288 = 0;
  uStack_280 = 0;
  uStack_278 = 0;
  local_270 = 0;
  uStack_268 = 0;
  local_260 = 0;
  uStack_258 = 0;
  local_250 = 0;
  uStack_248 = 0;
  local_240 = 0;
  uStack_238 = 0;
  local_230 = 0;
  uStack_228 = 0;
  if (0 < (int)local_2a8) {
                    /* WARNING: Subroutine does not return */
    FUN_181798f36(&local_298,local_328,(ulonglong)local_2a8 << 3);
  }
  local_1f8[0] = 0;
  local_1f8[1] = 0;
  local_1f8[2] = 0;
  local_1f8[3] = 0;
  local_1f8[4] = 0;
  local_1f8[5] = 0;
  local_1f8[6] = 0;
  local_1f8[7] = 0;
  local_1f8[8] = 0;
  local_1f8[9] = 0;
  local_1f8[10] = 0;
  local_1f8[0xb] = 0;
  local_1f8[0xc] = 0;
  local_1f8[0xd] = 0;
  local_1f8[0xe] = 0;
  local_1f8[0xf] = 0;
  local_178 = CONCAT44(iStack_214,local_2a8);
  lStack_170 = (longlong)iStack_214 << 2;
  if (0 < (int)local_2a8) {
    puVar5 = local_1f8;
    uVar7 = (ulonglong)local_2a8;
    do {
      FUN_180001100(*puVar5,uVar10 & 0xffffffff,0,0);
      puVar5 = puVar5 + 1;
      uVar7 = uVar7 - 1;
    } while (uVar7 != 0);
  }
  return;
}

 (GhidraScript)  
