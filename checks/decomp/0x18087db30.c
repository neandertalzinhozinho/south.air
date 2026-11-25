 (GhidraScript)  

void FUN_18087db30(longlong param_1,longlong *param_2)

{
  longlong lVar1;
  undefined4 uVar2;
  uint uVar3;
  uint uVar4;
  undefined8 *puVar5;
  int iVar6;
  int iVar7;
  ulonglong uVar8;
  longlong lVar9;
  ulonglong uVar10;
  undefined8 local_288 [14];
  undefined8 uStack_218;
  undefined8 local_210;
  uint local_208;
  uint uStack_204;
  longlong lStack_200;
  longlong local_1f8;
  int iStack_1f0;
  int iStack_1ec;
  undefined8 local_1e8 [16];
  undefined8 local_168;
  longlong lStack_160;
  undefined8 local_158 [4];
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
  longlong lStack_d0;
  undefined8 local_c8 [4];
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
  undefined4 local_58;
  undefined4 uStack_54;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined8 local_48;
  longlong lStack_40;
  
  iVar7 = 0;
  uStack_204 = *(int *)(param_1 + 0x590);
  iVar6 = 0;
  local_288[0] = 0;
  local_210 = 0;
  local_208 = *(int *)(param_1 + 0x588);
  lStack_200 = (longlong)*(int *)(param_1 + 0x590) << 2;
  local_288[1] = 0;
  local_288[2] = 0;
  local_288[3] = 0;
  local_288[4] = 0;
  local_288[5] = 0;
  local_288[6] = 0;
  local_288[7] = 0;
  local_288[8] = 0;
  local_288[9] = 0;
  local_288[10] = 0;
  local_288[0xb] = 0;
  local_288[0xc] = 0;
  local_288[0xd] = 0;
  uStack_218 = 0;
  if (0 < *(int *)(param_1 + 0x588)) {
    puVar5 = local_288;
    do {
      iVar6 = iVar6 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x508) - (longlong)local_288) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar6 < (int)local_208);
  }
  local_1e8[0] = local_288[0];
  local_1e8[1] = local_288[1];
  local_1e8[2] = local_288[2];
  local_1e8[3] = local_288[3];
  local_1e8[4] = local_288[4];
  local_1e8[5] = local_288[5];
  local_1e8[6] = local_288[6];
  local_1e8[7] = local_288[7];
  local_1e8[8] = local_288[8];
  local_1e8[9] = local_288[9];
  local_1e8[10] = local_288[10];
  local_1e8[0xb] = local_288[0xb];
  local_1e8[0xc] = local_288[0xc];
  local_1e8[0xd] = local_288[0xd];
  local_1e8[0xe] = uStack_218;
  local_1e8[0xf] = local_210;
  local_168 = CONCAT44(uStack_204,local_208);
  lStack_160 = lStack_200;
  FUN_1808833f0(local_1e8,DAT_18207a350);
  lVar1 = param_2[3];
  iStack_1f0 = (int)*(undefined8 *)(param_1 + 0x40);
  iStack_1ec = iStack_1f0 * 4;
  local_288[0] = 0;
  local_288[1] = 0;
  local_288[2] = 0;
  lVar9 = *param_2 + (longlong)(int)param_2[3] * 4;
  uVar3 = (int)param_2[3] + iStack_1f0;
  local_1f8 = lVar9;
  local_288[3] = 0;
  local_288[4] = 0;
  uVar4 = (uVar3 - (uVar3 & 0xf)) + 0x10;
  if ((uVar3 & 0xf) == 0) {
    uVar4 = uVar3;
  }
  iVar6 = 0;
  *(uint *)(param_2 + 3) = uVar4;
  uStack_204 = *(int *)(param_1 + 2000);
  local_210 = 0;
  local_208 = *(int *)(param_1 + 0x7c8);
  lStack_200 = (longlong)*(int *)(param_1 + 2000) << 2;
  local_288[5] = 0;
  local_288[6] = 0;
  local_288[7] = 0;
  local_288[8] = 0;
  local_288[9] = 0;
  local_288[10] = 0;
  local_288[0xb] = 0;
  local_288[0xc] = 0;
  local_288[0xd] = 0;
  uStack_218 = 0;
  if (0 < *(int *)(param_1 + 0x7c8)) {
    puVar5 = local_288;
    do {
      iVar6 = iVar6 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x748) - (longlong)local_288) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar6 < (int)local_208);
  }
  local_1e8[0] = local_288[0];
  local_1e8[1] = local_288[1];
  local_1e8[2] = local_288[2];
  local_1e8[3] = local_288[3];
  local_1e8[4] = local_288[4];
  local_1e8[5] = local_288[5];
  local_1e8[6] = local_288[6];
  local_1e8[7] = local_288[7];
  local_1e8[8] = local_288[8];
  local_1e8[9] = local_288[9];
  local_1e8[10] = local_288[10];
  local_1e8[0xb] = local_288[0xb];
  local_1e8[0xc] = local_288[0xc];
  local_1e8[0xd] = local_288[0xd];
  local_168 = CONCAT44(uStack_204,local_208);
  local_1e8[0xe] = uStack_218;
  local_1e8[0xf] = local_210;
  lStack_160 = lStack_200;
  FUN_180882de0(&local_1f8,local_1e8,DAT_18207a52c,DAT_18207a2b8,DAT_18207a188);
  uVar10 = (ulonglong)(int)*(uint *)(param_1 + 0x590);
  local_288[0] = 0;
  local_210 = 0;
  local_208 = *(uint *)(param_1 + 0x588);
  iVar6 = 0;
  uStack_204 = *(uint *)(param_1 + 0x590);
  lStack_200 = uVar10 << 2;
  local_288[1] = 0;
  local_288[2] = 0;
  local_288[3] = 0;
  local_288[4] = 0;
  local_288[5] = 0;
  local_288[6] = 0;
  local_288[7] = 0;
  local_288[8] = 0;
  local_288[9] = 0;
  local_288[10] = 0;
  local_288[0xb] = 0;
  local_288[0xc] = 0;
  local_288[0xd] = 0;
  uStack_218 = 0;
  if (0 < (int)*(uint *)(param_1 + 0x588)) {
    puVar5 = local_288;
    do {
      iVar6 = iVar6 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x508) - (longlong)local_288) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar6 < (int)local_208);
    uVar10 = (ulonglong)uStack_204;
  }
  uVar8 = (ulonglong)local_208;
  local_1e8[0] = local_288[0];
  local_1e8[1] = local_288[1];
  local_1e8[2] = local_288[2];
  local_1e8[3] = local_288[3];
  local_1e8[4] = local_288[4];
  local_1e8[5] = local_288[5];
  local_1e8[6] = local_288[6];
  local_1e8[7] = local_288[7];
  local_1e8[8] = local_288[8];
  local_1e8[9] = local_288[9];
  local_1e8[10] = local_288[10];
  local_1e8[0xb] = local_288[0xb];
  local_1e8[0xc] = local_288[0xc];
  local_1e8[0xd] = local_288[0xd];
  local_1e8[0xe] = uStack_218;
  local_1e8[0xf] = local_210;
  local_168 = CONCAT44(uStack_204,local_208);
  lStack_160 = lStack_200;
  if (local_208 == 1) {
    FUN_180001340(lVar9,local_288[0],uVar10 & 0xffffffff);
  }
  else if (0 < (int)local_208) {
    puVar5 = local_1e8;
    do {
      FUN_180001340(lVar9,*puVar5,uVar10 & 0xffffffff);
      puVar5 = puVar5 + 1;
      uVar8 = uVar8 - 1;
    } while (uVar8 != 0);
  }
  *(int *)(param_2 + 3) = (int)lVar1;
  iVar6 = 0;
  local_1e8[0] = 0;
  local_1e8[0xf] = 0;
  local_168 = CONCAT44(*(int *)(param_1 + 0x590),*(int *)(param_1 + 0x588));
  lStack_160 = (longlong)*(int *)(param_1 + 0x590) << 2;
  local_1e8[1] = 0;
  local_1e8[2] = 0;
  local_1e8[3] = 0;
  local_1e8[4] = 0;
  local_1e8[5] = 0;
  local_1e8[6] = 0;
  local_1e8[7] = 0;
  local_1e8[8] = 0;
  local_1e8[9] = 0;
  local_1e8[10] = 0;
  local_1e8[0xb] = 0;
  local_1e8[0xc] = 0;
  local_1e8[0xd] = 0;
  local_1e8[0xe] = 0;
  if (0 < *(int *)(param_1 + 0x588)) {
    puVar5 = local_1e8;
    do {
      iVar6 = iVar6 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x508) - (longlong)local_1e8) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar6 < (int)local_168);
  }
  uVar10 = (ulonglong)(int)*(uint *)(param_1 + 0x620);
  local_288[0] = 0;
  local_210 = 0;
  iVar6 = 0;
  local_208 = *(uint *)(param_1 + 0x618);
  uStack_204 = *(uint *)(param_1 + 0x620);
  lStack_200 = uVar10 << 2;
  local_288[1] = 0;
  local_288[2] = 0;
  local_288[3] = 0;
  local_288[4] = 0;
  local_288[5] = 0;
  local_288[6] = 0;
  local_288[7] = 0;
  local_288[8] = 0;
  local_288[9] = 0;
  local_288[10] = 0;
  local_288[0xb] = 0;
  local_288[0xc] = 0;
  local_288[0xd] = 0;
  uStack_218 = 0;
  if (0 < (int)*(uint *)(param_1 + 0x618)) {
    puVar5 = local_288;
    do {
      iVar6 = iVar6 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x598) - (longlong)local_288) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar6 < (int)local_208);
    uVar10 = (ulonglong)uStack_204;
  }
  local_158[0] = local_1e8[0];
  local_158[1] = local_1e8[1];
  local_158[2] = local_1e8[2];
  local_158[3] = local_1e8[3];
  local_138 = local_1e8[4];
  uStack_130 = local_1e8[5];
  local_128 = local_1e8[6];
  uStack_120 = local_1e8[7];
  local_118 = local_1e8[8];
  uStack_110 = local_1e8[9];
  local_108 = local_1e8[10];
  uStack_100 = local_1e8[0xb];
  local_f8 = local_1e8[0xc];
  uStack_f0 = local_1e8[0xd];
  local_e8 = local_1e8[0xe];
  uStack_e0 = local_1e8[0xf];
  local_d8 = local_168;
  lStack_d0 = lStack_160;
  local_c8[0] = local_288[0];
  local_c8[1] = local_288[1];
  local_c8[2] = local_288[2];
  local_c8[3] = local_288[3];
  local_a8 = local_288[4];
  uStack_a0 = local_288[5];
  local_98 = local_288[6];
  uStack_90 = local_288[7];
  local_88 = local_288[8];
  uStack_80 = local_288[9];
  local_78 = local_288[10];
  uStack_70 = local_288[0xb];
  local_68 = local_288[0xc];
  uStack_60 = local_288[0xd];
  local_58 = (undefined4)uStack_218;
  uStack_54 = uStack_218._4_4_;
  uStack_50 = (undefined4)local_210;
  uStack_4c = local_210._4_4_;
  local_48 = CONCAT44(uStack_204,local_208);
  lStack_40 = lStack_200;
  if (0 < (int)local_208) {
    lVar9 = 0;
    uVar8 = (ulonglong)local_208;
    do {
      FUN_1801c8530(*(undefined8 *)((longlong)local_158 + lVar9),
                    *(undefined8 *)((longlong)local_c8 + lVar9),uVar10 & 0xffffffff);
      lVar9 = lVar9 + 8;
      uVar8 = uVar8 - 1;
    } while (uVar8 != 0);
  }
  uVar2 = DAT_18207a6a8;
  local_210 = 0;
  local_288[0] = 0;
  local_208 = *(uint *)(param_1 + 0x618);
  uStack_204 = *(int *)(param_1 + 0x620);
  lStack_200 = (longlong)*(int *)(param_1 + 0x620) << 2;
  local_288[1] = 0;
  local_288[2] = 0;
  local_288[3] = 0;
  local_288[4] = 0;
  local_288[5] = 0;
  local_288[6] = 0;
  local_288[7] = 0;
  local_288[8] = 0;
  local_288[9] = 0;
  local_288[10] = 0;
  local_288[0xb] = 0;
  local_288[0xc] = 0;
  local_288[0xd] = 0;
  uStack_218 = 0;
  if (0 < (int)*(uint *)(param_1 + 0x618)) {
    puVar5 = local_288;
    do {
      iVar7 = iVar7 + 1;
      *puVar5 = *(undefined8 *)(((param_1 + 0x598) - (longlong)local_288) + (longlong)puVar5);
      puVar5 = puVar5 + 1;
    } while (iVar7 < (int)local_208);
  }
  uVar4 = uStack_204;
  local_158[0] = local_288[0];
  local_158[1] = local_288[1];
  local_158[2] = local_288[2];
  local_158[3] = local_288[3];
  local_138 = local_288[4];
  uStack_130 = local_288[5];
  local_128 = local_288[6];
  uStack_120 = local_288[7];
  local_118 = local_288[8];
  uStack_110 = local_288[9];
  local_108 = local_288[10];
  uStack_100 = local_288[0xb];
  local_f8 = local_288[0xc];
  uStack_f0 = local_288[0xd];
  local_e8 = uStack_218;
  uStack_e0 = local_210;
  local_d8 = CONCAT44(uStack_204,local_208);
  lStack_d0 = lStack_200;
  if (0 < (int)local_208) {
    puVar5 = local_158;
    uVar10 = (ulonglong)local_208;
    do {
      FUN_180001220(uVar2,*puVar5,uVar4);
      puVar5 = puVar5 + 1;
      uVar10 = uVar10 - 1;
    } while (uVar10 != 0);
  }
  return;
}

 (GhidraScript)  
