 (GhidraScript)  

void FUN_1808834c0(undefined8 *param_1,float param_2,undefined8 param_3,undefined8 *param_4)

{
  undefined4 uVar1;
  uint uVar2;
  undefined4 uVar3;
  undefined8 *puVar4;
  ulonglong uVar5;
  longlong lVar6;
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
  uint local_168;
  undefined4 uStack_164;
  undefined4 uStack_160;
  undefined4 uStack_15c;
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
  uint local_d8;
  undefined4 uStack_d4;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
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
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 uStack_40;
  
  uVar3 = DAT_182079cf0;
  local_c8[0] = *param_4;
  local_c8[1] = param_4[1];
  local_a8 = param_4[4];
  uStack_a0 = param_4[5];
  local_88 = param_4[8];
  uStack_80 = param_4[9];
  local_68 = param_4[0xc];
  uStack_60 = param_4[0xd];
  local_48 = param_4[0x10];
  uStack_40 = param_4[0x11];
  local_1e8[2] = param_1[2];
  local_1e8[3] = param_1[3];
  local_1b8 = param_1[6];
  uStack_1b0 = param_1[7];
  param_2 = param_2 * DAT_182079d24;
  local_98 = param_4[6];
  uStack_90 = param_4[7];
  local_78 = param_4[10];
  uStack_70 = param_4[0xb];
  local_58 = param_4[0xe];
  uStack_50 = param_4[0xf];
  local_1e8[0] = *param_1;
  local_1e8[1] = param_1[1];
  local_1c8 = param_1[4];
  uStack_1c0 = param_1[5];
  local_1a8 = param_1[8];
  uStack_1a0 = param_1[9];
  local_188 = param_1[0xc];
  uStack_180 = param_1[0xd];
  local_168 = *(uint *)(param_1 + 0x10);
  uVar1 = *(undefined4 *)((longlong)param_1 + 0x84);
  local_198 = param_1[10];
  uStack_190 = param_1[0xb];
  local_c8[2] = param_4[2];
  local_c8[3] = param_4[3];
  local_178 = param_1[0xe];
  uStack_170 = param_1[0xf];
  uStack_164 = uVar1;
  uStack_160 = *(undefined4 *)(param_1 + 0x11);
  uStack_15c = *(undefined4 *)((longlong)param_1 + 0x8c);
  if (0 < (int)local_168) {
    lVar6 = 0;
    uVar5 = (ulonglong)local_168;
    do {
      FUN_180001250(*(undefined8 *)((longlong)local_c8 + lVar6),
                    *(undefined8 *)((longlong)local_1e8 + lVar6),uVar1,uVar3,0);
      lVar6 = lVar6 + 8;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  local_1e8[0] = *param_1;
  local_1e8[1] = param_1[1];
  local_1c8 = param_1[4];
  uStack_1c0 = param_1[5];
  local_1e8[2] = param_1[2];
  local_1e8[3] = param_1[3];
  local_1a8 = param_1[8];
  uStack_1a0 = param_1[9];
  local_1b8 = param_1[6];
  uStack_1b0 = param_1[7];
  local_188 = param_1[0xc];
  uStack_180 = param_1[0xd];
  local_168 = *(uint *)(param_1 + 0x10);
  uVar1 = *(undefined4 *)((longlong)param_1 + 0x84);
  local_198 = param_1[10];
  uStack_190 = param_1[0xb];
  local_178 = param_1[0xe];
  uStack_170 = param_1[0xf];
  uStack_164 = uVar1;
  uStack_160 = *(undefined4 *)(param_1 + 0x11);
  uStack_15c = *(undefined4 *)((longlong)param_1 + 0x8c);
  if (0 < (int)local_168) {
    puVar4 = local_1e8;
    uVar5 = (ulonglong)local_168;
    do {
      FUN_180001220(param_2,*puVar4,uVar1);
      puVar4 = puVar4 + 1;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  local_158[0] = *param_1;
  local_158[1] = param_1[1];
  local_138 = param_1[4];
  uStack_130 = param_1[5];
  local_158[2] = param_1[2];
  local_158[3] = param_1[3];
  local_118 = param_1[8];
  uStack_110 = param_1[9];
  local_128 = param_1[6];
  uStack_120 = param_1[7];
  local_f8 = param_1[0xc];
  uStack_f0 = param_1[0xd];
  local_d8 = *(uint *)(param_1 + 0x10);
  uVar1 = *(undefined4 *)((longlong)param_1 + 0x84);
  local_108 = param_1[10];
  uStack_100 = param_1[0xb];
  local_e8 = param_1[0xe];
  uStack_e0 = param_1[0xf];
  uStack_d4 = uVar1;
  uStack_d0 = *(undefined4 *)(param_1 + 0x11);
  uStack_cc = *(undefined4 *)((longlong)param_1 + 0x8c);
  if (0 < (int)local_d8) {
    puVar4 = local_158;
    uVar5 = (ulonglong)local_d8;
    do {
      FUN_1801c8530(*puVar4,*puVar4,uVar1);
      puVar4 = puVar4 + 1;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  uVar3 = DAT_18207a6d4;
  local_158[0] = *param_1;
  local_158[1] = param_1[1];
  local_138 = param_1[4];
  uStack_130 = param_1[5];
  local_158[2] = param_1[2];
  local_158[3] = param_1[3];
  local_118 = param_1[8];
  uStack_110 = param_1[9];
  local_128 = param_1[6];
  uStack_120 = param_1[7];
  local_f8 = param_1[0xc];
  uStack_f0 = param_1[0xd];
  local_d8 = *(uint *)(param_1 + 0x10);
  uVar1 = *(undefined4 *)((longlong)param_1 + 0x84);
  local_108 = param_1[10];
  uStack_100 = param_1[0xb];
  local_e8 = param_1[0xe];
  uStack_e0 = param_1[0xf];
  uStack_d4 = uVar1;
  uStack_d0 = *(undefined4 *)(param_1 + 0x11);
  uStack_cc = *(undefined4 *)((longlong)param_1 + 0x8c);
  if (0 < (int)local_d8) {
    puVar4 = local_158;
    uVar5 = (ulonglong)local_d8;
    do {
      FUN_180001220(uVar3,*puVar4,uVar1);
      puVar4 = puVar4 + 1;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  local_158[0] = *param_1;
  local_158[1] = param_1[1];
  local_138 = param_1[4];
  uStack_130 = param_1[5];
  local_158[2] = param_1[2];
  local_158[3] = param_1[3];
  local_118 = param_1[8];
  uStack_110 = param_1[9];
  local_128 = param_1[6];
  uStack_120 = param_1[7];
  local_f8 = param_1[0xc];
  uStack_f0 = param_1[0xd];
  local_d8 = *(uint *)(param_1 + 0x10);
  uVar1 = *(undefined4 *)((longlong)param_1 + 0x84);
  local_108 = param_1[10];
  uStack_100 = param_1[0xb];
  local_e8 = param_1[0xe];
  uStack_e0 = param_1[0xf];
  uStack_d4 = uVar1;
  uStack_d0 = *(undefined4 *)(param_1 + 0x11);
  uStack_cc = *(undefined4 *)((longlong)param_1 + 0x8c);
  if (0 < (int)local_d8) {
    puVar4 = local_158;
    uVar5 = (ulonglong)local_d8;
    do {
      FUN_1801c84a0(*puVar4,*puVar4,uVar1);
      puVar4 = puVar4 + 1;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  uVar3 = DAT_18207a6a8;
  local_1e8[0] = *param_1;
  local_1e8[1] = param_1[1];
  local_1c8 = param_1[4];
  uStack_1c0 = param_1[5];
  local_1e8[2] = param_1[2];
  local_1e8[3] = param_1[3];
  local_1a8 = param_1[8];
  uStack_1a0 = param_1[9];
  local_1b8 = param_1[6];
  uStack_1b0 = param_1[7];
  local_188 = param_1[0xc];
  uStack_180 = param_1[0xd];
  local_168 = *(uint *)(param_1 + 0x10);
  uVar1 = *(undefined4 *)((longlong)param_1 + 0x84);
  local_198 = param_1[10];
  uStack_190 = param_1[0xb];
  local_178 = param_1[0xe];
  uStack_170 = param_1[0xf];
  uStack_164 = uVar1;
  uStack_160 = *(undefined4 *)(param_1 + 0x11);
  uStack_15c = *(undefined4 *)((longlong)param_1 + 0x8c);
  if (0 < (int)local_168) {
    puVar4 = local_1e8;
    uVar5 = (ulonglong)local_168;
    do {
      FUN_180001220(uVar3,*puVar4,uVar1);
      puVar4 = puVar4 + 1;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  uVar3 = DAT_182079f9c;
  local_c8[0] = *param_1;
  local_c8[1] = param_1[1];
  local_a8 = param_1[4];
  uStack_a0 = param_1[5];
  local_c8[2] = param_1[2];
  local_c8[3] = param_1[3];
  local_88 = param_1[8];
  uStack_80 = param_1[9];
  local_98 = param_1[6];
  uStack_90 = param_1[7];
  local_68 = param_1[0xc];
  uStack_60 = param_1[0xd];
  uVar2 = *(uint *)(param_1 + 0x10);
  uVar1 = *(undefined4 *)((longlong)param_1 + 0x84);
  local_78 = param_1[10];
  uStack_70 = param_1[0xb];
  local_58 = param_1[0xe];
  uStack_50 = param_1[0xf];
  local_48 = param_1[0x10];
  uStack_40 = param_1[0x11];
  if (0 < (int)uVar2) {
    puVar4 = local_c8;
    uVar5 = (ulonglong)uVar2;
    do {
      FUN_1800012e0(uVar3,*puVar4,uVar1);
      puVar4 = puVar4 + 1;
      uVar5 = uVar5 - 1;
    } while (uVar5 != 0);
  }
  return;
}

 (GhidraScript)  
