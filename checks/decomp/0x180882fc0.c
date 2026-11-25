 (GhidraScript)  

void FUN_180882fc0(undefined8 *param_1,undefined8 *param_2,undefined4 param_3,undefined4 param_4,
                  longlong *param_5)

{
  longlong lVar1;
  longlong lVar2;
  undefined1 auVar3 [16];
  int iVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  undefined8 *puVar8;
  ulonglong uVar9;
  float fVar10;
  undefined4 uVar11;
  longlong local_208;
  int iStack_200;
  int iStack_1fc;
  undefined8 local_1f8 [4];
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
  undefined8 local_188;
  undefined8 uStack_180;
  undefined1 local_178 [16];
  undefined8 local_168 [4];
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
  undefined4 local_f8;
  undefined4 uStack_f4;
  undefined4 uStack_f0;
  undefined4 uStack_ec;
  undefined1 local_e8 [16];
  undefined8 local_d8;
  undefined8 uStack_d0;
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
  undefined4 local_58;
  undefined4 uStack_54;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  
  iVar4 = *(int *)((longlong)param_1 + 0x84);
  iVar5 = (int)param_5[3];
  _iStack_200 = CONCAT44(iVar4 * 4,iVar4);
  uVar7 = iVar4 + iVar5;
  lVar1 = *param_5 + (longlong)iVar5 * 4;
  uVar6 = (uVar7 - (uVar7 & 0xf)) + 0x10;
  if ((uVar7 & 0xf) == 0) {
    uVar6 = uVar7;
  }
  *(uint *)(param_5 + 3) = uVar6;
  local_208 = lVar1;
  fVar10 = (float)FUN_181c9a5a1(param_3);
  local_1f8[2] = param_2[2];
  local_1f8[3] = param_2[3];
  local_1f8[0] = *param_2;
  local_1f8[1] = param_2[1];
  local_1d8 = param_2[4];
  uStack_1d0 = param_2[5];
  local_1b8 = param_2[8];
  uStack_1b0 = param_2[9];
  local_1c8 = param_2[6];
  uStack_1c0 = param_2[7];
  local_198 = param_2[0xc];
  uStack_190 = param_2[0xd];
  local_1a8 = param_2[10];
  uStack_1a0 = param_2[0xb];
  local_178 = *(undefined1 (*) [16])(param_2 + 0x10);
  local_188 = param_2[0xe];
  uStack_180 = param_2[0xf];
  FUN_18088e130(&local_208,local_1f8,DAT_18207a560,DAT_18207a384,
                (uint)(fVar10 * DAT_18207a3b0) ^ DAT_18207bb20);
  uVar11 = FUN_181c9aa01(DAT_18207a360);
  FUN_180001220(uVar11,lVar1,iVar4);
  _iStack_200 = CONCAT44(iVar4 * 4,iVar4);
  lVar2 = *param_5 + (longlong)(int)param_5[3] * 4;
  uVar6 = (int)param_5[3] + iVar4;
  uVar7 = (uVar6 - (uVar6 & 0xf)) + 0x10;
  if ((uVar6 & 0xf) == 0) {
    uVar7 = uVar6;
  }
  *(uint *)(param_5 + 3) = uVar7;
  local_208 = lVar2;
  fVar10 = (float)FUN_181c9a5a1(param_4);
  local_1f8[2] = param_2[2];
  local_1f8[3] = param_2[3];
  local_1f8[0] = *param_2;
  local_1f8[1] = param_2[1];
  local_1d8 = param_2[4];
  uStack_1d0 = param_2[5];
  local_1b8 = param_2[8];
  uStack_1b0 = param_2[9];
  local_1c8 = param_2[6];
  uStack_1c0 = param_2[7];
  local_198 = param_2[0xc];
  uStack_190 = param_2[0xd];
  local_1a8 = param_2[10];
  uStack_1a0 = param_2[0xb];
  local_178 = *(undefined1 (*) [16])(param_2 + 0x10);
  local_188 = param_2[0xe];
  uStack_180 = param_2[0xf];
  FUN_18088e130(&local_208,local_1f8,DAT_18207a5a8,DAT_18207a384,fVar10 * DAT_18207a3b0);
  uVar11 = FUN_181c9aa01(DAT_18207a360);
  FUN_180001220(uVar11,lVar2,iVar4);
  local_d8 = *param_1;
  uStack_d0 = param_1[1];
  local_c8 = param_1[2];
  uStack_c0 = param_1[3];
  local_b8 = param_1[4];
  uStack_b0 = param_1[5];
  local_98 = param_1[8];
  uStack_90 = param_1[9];
  local_a8 = param_1[6];
  uStack_a0 = param_1[7];
  local_78 = param_1[0xc];
  uStack_70 = param_1[0xd];
  local_88 = param_1[10];
  uStack_80 = param_1[0xb];
  local_58 = *(undefined4 *)(param_1 + 0x10);
  uStack_54 = *(undefined4 *)((longlong)param_1 + 0x84);
  uStack_50 = *(undefined4 *)(param_1 + 0x11);
  uStack_4c = *(undefined4 *)((longlong)param_1 + 0x8c);
  local_68 = param_1[0xe];
  uStack_60 = param_1[0xf];
  FUN_18087a7a0(&local_d8);
  local_148 = param_1[4];
  uStack_140 = param_1[5];
  local_168[2] = param_1[2];
  local_168[3] = param_1[3];
  local_128 = param_1[8];
  uStack_120 = param_1[9];
  local_138 = param_1[6];
  uStack_130 = param_1[7];
  local_108 = param_1[0xc];
  uStack_100 = param_1[0xd];
  auVar3 = *(undefined1 (*) [16])(param_1 + 0x10);
  uVar7 = auVar3._0_4_;
  local_118 = param_1[10];
  uStack_110 = param_1[0xb];
  local_168[0] = *param_1;
  local_168[1] = param_1[1];
  local_f8 = *(undefined4 *)(param_1 + 0xe);
  uStack_f4 = *(undefined4 *)((longlong)param_1 + 0x74);
  uStack_f0 = *(undefined4 *)(param_1 + 0xf);
  uStack_ec = *(undefined4 *)((longlong)param_1 + 0x7c);
  local_e8 = auVar3;
  if (uVar7 == 1) {
    FUN_180001340(lVar1,*param_1,auVar3._4_4_);
  }
  else if (0 < (int)uVar7) {
    puVar8 = local_168;
    uVar9 = (ulonglong)uVar7;
    do {
      FUN_180001340(lVar1,*puVar8,auVar3._4_4_);
      puVar8 = puVar8 + 1;
      uVar9 = uVar9 - 1;
    } while (uVar9 != 0);
  }
  local_1d8 = param_1[4];
  uStack_1d0 = param_1[5];
  local_1f8[2] = param_1[2];
  local_1f8[3] = param_1[3];
  local_1b8 = param_1[8];
  uStack_1b0 = param_1[9];
  local_1c8 = param_1[6];
  uStack_1c0 = param_1[7];
  local_198 = param_1[0xc];
  uStack_190 = param_1[0xd];
  auVar3 = *(undefined1 (*) [16])(param_1 + 0x10);
  uVar7 = auVar3._0_4_;
  local_1a8 = param_1[10];
  uStack_1a0 = param_1[0xb];
  local_1f8[0] = *param_1;
  local_1f8[1] = param_1[1];
  local_188 = param_1[0xe];
  uStack_180 = param_1[0xf];
  local_178 = auVar3;
  if (uVar7 == 1) {
    FUN_180001340(lVar2,*param_1,auVar3._4_4_);
  }
  else if (0 < (int)uVar7) {
    puVar8 = local_1f8;
    uVar9 = (ulonglong)uVar7;
    do {
      FUN_180001340(lVar2,*puVar8,auVar3._4_4_);
      puVar8 = puVar8 + 1;
      uVar9 = uVar9 - 1;
    } while (uVar9 != 0);
  }
  *(int *)(param_5 + 3) = iVar5;
  return;
}

 (GhidraScript)  
